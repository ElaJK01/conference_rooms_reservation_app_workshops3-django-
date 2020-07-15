from django.shortcuts import render
from django.views import View
from conference_app.models import Room, Reservation
from datetime import datetime, date
from django.shortcuts import redirect
from django.db import IntegrityError
# Create your views here.

class AddRoom(View):
    def get(self, request):
        return render(request, 'new_room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        has_projector = 'has_projector' in request.POST
        if name and capacity:
            room_temp = Room.objects.create(name=name, capacity=int(capacity), has_projector=has_projector)
            room_temp.save()
            ctx = {
                "msg": f"Dodano nową salę."
            }
            return render(request, "new_room.html", ctx)
        else:
            ctx = {
                "msg": "Error. You need to provide valid name and/or capacity",
            }
            return render(request, "new_room.html", ctx)

class RoomsList(View):
    def get(self, request):
        name = request.GET.get('name')
        min_capacity = request.GET.get('min_capacity')
        has_projector = 'has_projector' in request.GET
        rooms = Room.objects.all()
        reservation = Reservation.objects.all()
        if name: #to przychodzi jeśli name nie jest None i nie jest ""
            rooms = rooms.filter(name__icontains=name)
        if min_capacity:
            rooms = rooms.filter(capacity__gte=min_capacity)
        if has_projector:
            rooms = rooms.filter(has_projector=True)
        today = date.today()
        str_today = today.strftime('%Y-%m-%d')
        for r in rooms:
            r_all_reservations = Reservation.objects.filter(room__pk = r.pk)
            for res in r_all_reservations:
                res.date = res.date.strftime('%Y-%m-%d')
                if res.date == str_today:
                    status = 'zajęta'
                else:
                    status = 'wolna'
                ctx = {'rooms': rooms,
                        'today': today,
                        'status': status,
                        'reservation': reservation}
                return render(request, 'rooms_list.html', ctx)


class RoomModify(View):
    def get(self, request, id):
        if id is None:
            return HttpResponse('Nie ma takiej sali')
        else:
            room = Room.objects.get(id=id)
            ctx = {"room": room,
                   }
        return render(request, "room_modify.html", ctx)

    def post(self,request, id):
        id = request.POST.get('id')
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        has_projector = 'projector' in request.POST
        if name and capacity:
            Room.objects.filter(pk=id).update(name=name, capacity=capacity, has_projector=has_projector)
            return redirect('rooms_list')
        else:
            room = Room.objects.get(id=id)
            ctx = { 'room': room,
                    'msg': "Wypełnij wszystkie pola"}
            return render(request, "room_modify.html", ctx)

class RoomDetails(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        reservations = Reservation.objects.filter(room=room)
        today = date.today()
        if room:
            ctx = {'room': room,
                   'reservations': reservations,
                   'today': today}
            return render(request, 'room_details.html', ctx)
        else:
            ctx = {'msg': "Nie ma sali o podanym numerze!"}
            return render(request, 'room_details.html', ctx)

class RoomReservation(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        reservations = Reservation.objects.filter(room=room)
        ctx = {'room': room,
               'reservations': reservations}
        return render(request, "room-reservation.html", ctx)

    def post(self, request,id):
        reservation_date = request.POST.get('reserv-date')
        reservation_date = datetime.strptime(reservation_date, '%Y-%m-%d').date()
        comment = request.POST.get('comment')
        room_id = request.POST.get('id')
        today = date.today()
        room_to_reserv = Room.objects.get(pk=room_id)
        # room_to_reserv_all_reservations = Reservation.objects.filter(room__pk=room_id)
        if reservation_date < today:
            ctx = {'msg': "Nieprawidłowa data!"}
            return render(request, 'room-reservation.html', ctx)
        try:
            reserv = Reservation.objects.create(date=reservation_date, comment=comment, room=room_to_reserv)
            reserv.save()
            return redirect('rooms_list')
        except IntegrityError as e: #w modelu Reservation jest klasa meta unique_together co pozwala na walidację czy nie ma już rezerwacji dla sali w danym dniu
            #dlatego import IntegrityError i wychwycenie wyjatku
            ctx = {'msg': "Sala jest zarezerwowana w tym terminie!"}
            return render(request, 'room-reservation.html', ctx)


class DeleteRoom(View):
    def get(self, request, id):
        if id is None:
            return HttpResponse('Nie ma takiej sali')
        else:
            room = Room.objects.get(pk=id)
            room.delete()
            ctx = {'msg': "Sala została usunięta!",
                   'room': room}
            return render(request, 'room-delete.html', ctx)



