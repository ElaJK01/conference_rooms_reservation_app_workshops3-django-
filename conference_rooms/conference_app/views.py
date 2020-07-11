from django.shortcuts import render
from django.views import View
from conference_app.models import Room
from datetime import datetime
from django.shortcuts import redirect
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
        if name: #to przychodzi jeśli name nie jest None i nie jest ""
            rooms = rooms.filter(name__icontains=name)
        if min_capacity:
            rooms = rooms.filter(capacity__gte=min_capacity)
        if has_projector:
            rooms = rooms.filter(has_projector=True)
        ctx = {'rooms': rooms}
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


class TempView(View):
    pass
