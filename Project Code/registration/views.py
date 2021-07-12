from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from registration.models import *


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        varuserid = request.POST['id']
        varpassword = request.POST['password']

        if HotelRegistration.objects.filter(hotelid=varuserid, hotelpassword=varpassword):
            request.session['id'] = varuserid
            return redirect('hotel_home')

        elif UserRegistration.objects.filter(userid=varuserid, userpassword=varpassword):
            request.session['id'] = varuserid
            return redirect('user_home')

        else:
            messages.error(request, 'Invalid username or password!!')
            return redirect('login')


def userRegistration(request):
    if request.method == 'GET':
        return render(request, 'user_registration.html')

    if request.method == 'POST':
        varuname = request.POST['username']
        varupassword = request.POST['password1']
        varuserid = request.POST['userid']
        varumobile = request.POST['umobno']

        if (HotelRegistration.objects.filter(hotelid=varuserid).exists()) or (
                UserRegistration.objects.filter(userid=varuserid).exists()):
            messages.error(request, varuserid + ' already registered!!')
            return redirect('login')
        else:
            UserRegistration.objects.create(userid=varuserid, username=varuname, userpassword=varupassword,
                                            usermobileno=varumobile)
            messages.success(request, varuserid + ' registered successfully!!')
            return redirect('login')


def hotelRegistration(request):
    if request.method == 'GET':
        return render(request, 'hotel_registration.html')

    if request.method == 'POST':
        varhotelid = request.POST['hotelid']
        varhname = request.POST['hotelname']
        varhpassword = request.POST['password1']
        varhmobile = request.POST['hmobno']
        varhaddress = request.POST['hoteladdress']
        varcity = request.POST['hotelcity']
        varstate = request.POST['hotelstate']
        varcountry = request.POST['hotelcountry']

        if (HotelRegistration.objects.filter(hotelid=varhotelid).exists()) or (
                UserRegistration.objects.filter(userid=varhotelid).exists()):
            messages.error(request, varhotelid + ' already registered!!')
            return redirect('login')
        else:
            if City.objects.filter(cityname=varcity).exists():
                None
            else:
                City.objects.create(cityname=varcity, statename=varstate, countryname=varcountry)

            HotelRegistration.objects.create(hotelid=varhotelid, hotelname=varhname, hotelpassword=varhpassword,
                                             hotelmobileno=varhmobile)

            hotelidobj = HotelRegistration.objects.get(hotelid=varhotelid)
            cityobj = City.objects.get(cityname=varcity)

            HotelAddress.objects.create(hotelid=hotelidobj, cityid=cityobj, hoteladdress=varhaddress)
            messages.success(request, varhotelid + ' registered successfully!!')
            return redirect('login')
