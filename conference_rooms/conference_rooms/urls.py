"""conference_rooms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from conference_app.views import AddRoom, RoomDetails, RoomsList, RoomModify, RoomReservation, TempView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/new/', AddRoom.as_view(), name='new_room'),
    path('room/modify/<int:id>/', RoomModify.as_view(), name='room_modify'),
    path('room/delete/<int:id>/', TempView.as_view()),
    path('room/<int:id>/', RoomDetails.as_view(), name='room_details'),
    path('', RoomsList.as_view(), name ='rooms_list'),
    path('reservation/<int:id>/', RoomReservation.as_view(), name='room-reservation')
]
