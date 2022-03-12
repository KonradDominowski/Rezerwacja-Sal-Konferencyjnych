from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from rezerwacje.models import Room, Reservation
from django.db import IntegrityError


def homepage(request):
    return render(request, 'homepage.html')


class AddRoom(View):
    def get(self, request):
        return render(request, 'add-room.html')

    def post(self, request):
        room_name = request.POST.get('roomName')
        is_projector = True if request.POST.get('projector') else False
        try:
            room_capacity = int(request.POST.get('roomCapacity'))
        except ValueError:
            return HttpResponse('Podaj liczbe')

        if room_capacity <= 0:
            return HttpResponse('Nieprawidłowa pojemność sali')
        if room_name == '':
            return HttpResponse('Podaj nazwę sali')

        try:
            Room.objects.create(name=room_name,
                                capacity=room_capacity,
                                projector=is_projector)
        except IntegrityError:
            return HttpResponse('Nazwa sali już istnieje.')

        return redirect('/')


class RoomList(View):
    def get(self, request):
        room_list = Room.objects.all()
        context = {'room_list': room_list}

        return render(request, 'room-list.html', context)


class DeleteRoom(View):
    def get(self, request, room_id):
        Room.objects.get(id=room_id).delete()
        return redirect('/room_list')


class ModifyRoom(View):
    def get(self, request, room_id):
        return render(request, 'add-room.html')

    def post(self, request, room_id):
        new_room_name = request.POST.get('roomName')
        new_room_capacity = request.POST.get('roomCapacity')
        new_is_projector = True if request.POST.get('projector') else False

        if new_room_name != '':
            Room.objects.filter(id=room_id).update(name=new_room_name)
        if new_room_capacity != '':
            if int(new_room_capacity) > 0:
                Room.objects.filter(id=room_id).update(capacity=int(new_room_capacity))
            else:
                return HttpResponse('Wprowadź poprawną liczbę')
        if new_is_projector != '':
            Room.objects.filter(id=room_id).update(projector=new_is_projector)

        return redirect('/room_list')


class ReserveRoom(View):
    def get(self, request, room_id):
        return render(request, 'reservation.html')

    def post(self, request, room_id):
        date = request.POST.get('reservationDate')
        comment = request.POST.get('reservationComment')

        try:
            Reservation.objects.create(date=date,
                                       room_id=Room.objects.get(id=room_id),
                                       comment=comment)
        except IntegrityError:
            return HttpResponse('Ten dzień jest już zajęty')

        return redirect('/room_list')


class RoomInfo(View):
    def get(self, request, room_id):
        room = Room.objects.get(id=room_id)
        reservations = Reservation.objects.filter(room_id=room_id)
        context = {
            'room': room,
            'reservations': reservations
        }
        return render(request, 'room-info.html', context)
