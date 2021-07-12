from django.contrib import messages
from django.shortcuts import render, redirect
import datetime
from hotel.models import HotelRoom, RoomDescription, HotelImage, RoomImage
from registration.models import HotelRegistration
from user.models import RoomReservation


# Create your views here.

def hotelHome(request):
    if request.method == 'GET':
        sessionid = request.session.get('id')
        hotelobj = HotelRegistration.objects.get(hotelid=sessionid)
        varlogoname = hotelobj.hotelname
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        todayroomobj = RoomReservation.objects.filter(hotelid=sessionid, checkin__gte=today)
        allregistrationsobj = RoomReservation.objects.filter(hotelid=sessionid, checkin__lt=today).order_by('-checkin')
        context = {
            "name": 'Tanmay',
            "logoname": varlogoname,
            "todayroomobj": todayroomobj,
            "allregistrationsobj": allregistrationsobj,
        }
        return render(request, 'hotel_home.html', context)
        # return render(request, 'test.html')


def hotelAddRoom(request):
    if request.method == 'GET':
        sessionid = request.session.get('id')
        varhotelid = HotelRegistration.objects.get(hotelid=sessionid)
        varlogoname = varhotelid.hotelname

        context = {
            "name": 'Tanmay',
            "logoname": varlogoname,

        }
        return render(request, 'hotel_add_room.html', context)

    if request.method == 'POST':
        sessionid = request.session.get('id')
        # hotelid is object
        hotelobj = HotelRegistration.objects.get(hotelid=sessionid)
        # We required variable hotelid because we want email address from hotelid oblect
        varhotelid = hotelobj.hotelid
        varroomno = request.POST['roomno']
        varstrroomno = str(varroomno)
        varroomid = varhotelid + '_' + varstrroomno
        varroomtype = request.POST['roomtype']
        varroomdescription = request.POST['roomdescription']
        varroombeds = request.POST['roombeds']
        varroomrent = request.POST['roomrent']
        pic = request.FILES['image']
        if HotelRoom.objects.filter(roomid=varroomid).exists():
            messages.error(request, 'Room No:' + varroomno + ' already registered!!')
            return redirect('hotel_add_room')

        else:
            HotelRoom.objects.create(roomid=varroomid, hotelid=hotelobj, roomno=varroomno)
            roomobj = HotelRoom.objects.get(roomid=varroomid)
            RoomDescription.objects.create(roomid=roomobj, roomtype=varroomtype, roomdescription=varroomdescription,
                                           roombeds=varroombeds, roomrent=varroomrent)
            RoomImage.objects.create(roomid=roomobj, roomimg=pic)
            messages.success(request, 'Room No:' + varroomno + ' registered successfully!!')
            return redirect('hotel_add_room')


def hotelAddImage(request):
    if request.method == 'GET':
        sessionid = request.session.get('id')
        hotelobj = HotelRegistration.objects.get(hotelid=sessionid)
        varhotelid = hotelobj.hotelid
        if HotelImage.objects.filter(hotelid=varhotelid).exists():
            imageexist = 'YES'
            imageobj = HotelImage.objects.get(hotelid=varhotelid)
            hotelimg = imageobj.hotelimg
            # print(hotelimg)
            context = {
                "imageexist": imageexist,
                "image": hotelimg,
            }
            return render(request, 'hotel_add_image.html', context)
        else:
            imageexist = 'NO'
            context = {
                "imageexist": imageexist,
            }
            return render(request, 'hotel_add_image.html', context)

    if request.method == 'POST':
        sessionid = request.session.get('id')
        hotelobj = HotelRegistration.objects.get(hotelid=sessionid)
        pic = request.FILES['image']
        varhotelid = hotelobj.hotelid
        if HotelImage.objects.filter(hotelid=varhotelid).exists():
            HotelImage.objects.filter(hotelid=varhotelid).delete()
            HotelImage.objects.create(hotelid=hotelobj, hotelimg=pic)
        else:
            HotelImage.objects.create(hotelid=hotelobj, hotelimg=pic)
        return redirect('hotel_add_image')


def hotelLogout(request):
    request.session.flush()
    messages.success(request, 'Successfully logout!!')
    return redirect('login')
