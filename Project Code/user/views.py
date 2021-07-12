from datetime import date, datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from hotel.models import HotelRoom, RoomDescription, HotelImage, RoomImage
from registration.models import *
from user.function.getHotelsInStates import getHotelsFromState
from user.function.getInteValue import getInteValue
from user.function.getCityHotels import getCityHotelsList, getOthCityHotelsList
from user.function.getRecommendedHotel import getRecommendedHotel
from user.function.returnFreeRooms import returnFreeRoom, getBookedRoom
from user.models import RoomReservation, Ratings


# Create your views here.


def userHome(request):
    if request.method == 'GET':
        usersession = request.session.get('id')
        userobj = UserRegistration.objects.get(userid=usersession)
        varlogoname = userobj.username
        varuserid = userobj.userid
        cityobj = City.objects.all()
        context = {
            "logoname": varlogoname,
            "cityobj": cityobj,
            "userid": varuserid
        }
        return render(request, 'user_search.html', context)

    if request.method == 'POST':
        checkin_date = request.POST.get('datepicker1')
        checkout_date = request.POST.get('datepicker2')
        print(checkin_date)
        print(checkout_date)
        cityname = request.POST.get('find')
        userid = request.POST.get('userid')
        userobj = UserRegistration.objects.get(userid=userid)
        varlogoname = userobj.username
        cityobj = City.objects.all().filter(cityname=cityname)[0]
        statename = cityobj.statename
        cityobj2 = City.objects.all().filter(cityname=cityname)
        hotelsInState = getHotelsFromState(statename)
        getIntValue = getInteValue(hotelsInState)
        getRecommendedHotelList = getRecommendedHotel(getIntValue)
        getCityHotels = getCityHotelsList(getRecommendedHotelList, cityobj2)
        getOthrHotels = getOthCityHotelsList(getCityHotels, cityobj2)
        if len(getOthrHotels) == 0:
            imgObj = HotelImage.objects.filter(hotelid__in=getCityHotels)
            context = {
                "logoname": varlogoname,
                "rechotelobj": getCityHotels,
                "checkin": checkin_date,
                "checkout": checkout_date,
            }
        else:
            context = {
                "logoname": varlogoname,
                "rechotelobj": getCityHotels,
                "othhotelobj": getOthrHotels,
                "checkin": checkin_date,
                "checkout": checkout_date
            }
        # print(hotelobj)
        return render(request, 'user_hotels.html', context)


def userRoomList(request, hotelid, checkin, checkout):
    if request.method == 'GET':
        usersession = request.session.get('id')
        userobj = UserRegistration.objects.get(userid=usersession)
        varlogoname = userobj.username
        room_list = HotelRoom.objects.filter(hotelid=hotelid)
        returnEmptyRoomList = returnFreeRoom(room_list, checkin, checkout)
        availableRoomObj = HotelRoom.objects.filter(roomid__in=returnEmptyRoomList)
        bookedRoomList = getBookedRoom(room_list, checkin, checkout)
        bookedRoomObj = HotelRoom.objects.filter(roomid__in=bookedRoomList)
        imageobj = HotelImage.objects.get(hotelid=hotelid)
        context = {
            "room_list": room_list,
            "availableRoomObj": availableRoomObj,
            "bookedRoomList": bookedRoomObj,
            "logoname": varlogoname,
            "checkin": checkin,
            "checkout": checkout,
            "imageobj": imageobj
        }
        return render(request, 'user_hotel_room_list.html', context)


def userViewRoom(request, roomid, checkin, checkout):
    if request.method == 'GET':
        usersession = request.session.get('id')
        uemail = UserRegistration.objects.get(userid=usersession)
        roomobj = HotelRoom.objects.get(roomid=roomid)
        hotelid = roomobj.hotelid
        roomdescriptionobj = RoomDescription.objects.get(roomid=roomid)
        room_description_type = 'userRoomBooking'
        roomid = roomobj.roomid
        roomno = roomobj.roomno
        roomtype = roomdescriptionobj.roomtype
        roomdescription = roomdescriptionobj.roomdescription
        roomrent = roomdescriptionobj.roomrent
        roombeds = roomdescriptionobj.roombeds
        imageobj = RoomImage.objects.get(roomid=roomid)
        context = {
            "room_description_type": room_description_type,
            "roomid": roomid,
            "roomno": roomno,
            "roomtype": roomtype,
            "roomdescription": roomdescription,
            "roomrent": roomrent,
            "roombeds": roombeds,
            "uemail": uemail,
            "checkin": checkin,
            "checkout": checkout,
            "imageobj": imageobj
        }
        return render(request, 'view_room.html', context)


def userCancelRoom(request, roomid, checkin, checkout):
    if request.method == 'GET':
        usersession = request.session.get('id')
        uemail = UserRegistration.objects.get(userid=usersession)
        roomobj = HotelRoom.objects.get(roomid=roomid)
        roomdescriptionobj = RoomDescription.objects.get(roomid=roomid)
        room_description_type = 'userRoomBooking'
        roomid = roomobj.roomid
        roomno = roomobj.roomno
        roomtype = roomdescriptionobj.roomtype
        roomdescription = roomdescriptionobj.roomdescription
        roomrent = roomdescriptionobj.roomrent
        roombeds = roomdescriptionobj.roombeds
        imageobj = RoomImage.objects.get(roomid=roomid)
        # Convert string to date
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
        # Change date format
        checkin_strf = checkin_date.strftime("%d-%m-%Y")
        checkout_strf = checkout_date.strftime("%d-%m-%Y")
        context = {
            "room_description_type": room_description_type,
            "roomid": roomid,
            "roomno": roomno,
            "roomtype": roomtype,
            "roomdescription": roomdescription,
            "roomrent": roomrent,
            "roombeds": roombeds,
            "uemail": uemail,
            "checkin": checkin,
            "checkout": checkout,
            "checkin_strf": checkin_strf,
            "checkout_strf": checkout_strf,
            "imageobj": imageobj
        }
        return render(request, 'user_cancel_room.html', context)

    if request.method == 'POST':
        usersession = request.session.get('id')
        uemail = UserRegistration.objects.get(userid=usersession)
        try:
            RoomReservation.objects.filter(userid=uemail, roomid=roomid, checkin=checkin, checkout=checkout).delete()
            messages.success(request, 'Room canceled successfully!!')
        except:
            messages.error(request, 'Room cannot cancel!!')
        return redirect('user_history')


def userBookRoom(request, roomid, checkin, checkout):
    if request.method == 'GET':
        roomid = roomid
        # print(roomid)
        roomrentobj = RoomDescription.objects.all().filter(roomid=roomid)[0]
        roomrent = roomrentobj.roomrent
        # Convert string to date
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
        # Change date format
        checkin_strf = checkin_date.strftime("%d-%m-%Y")
        checkout_strf = checkout_date.strftime("%d-%m-%Y")
        context = {
            "roomid": roomid,
            "checkin": checkin,
            "checkout": checkout,
            "roomrent": roomrent,
            "checkin_strf": checkin_strf,
            "checkout_strf": checkout_strf,
        }
        return render(request, 'user_book_room.html', context)

    if request.method == 'POST':
        usersession = request.session.get('id')
        varroomid = request.POST.get('roomid')

        userobj = UserRegistration.objects.get(userid=usersession)
        roomobj = HotelRoom.objects.get(roomid=varroomid)
        hotelobj = roomobj.hotelid

        checkin_date = request.POST.get('checkinvalue')
        checkout_date = request.POST.get('checkoutvalue')
        cardnumber = request.POST.get('cardnumber')
        # case 1: a room is booked before the check_in date, and checks out after the requested check_in date
        case_1 = RoomReservation.objects.filter(roomid=varroomid, checkin__lte=checkin_date,
                                                checkout__gte=checkin_date).exists()

        # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
        case_2 = RoomReservation.objects.filter(roomid=varroomid, checkin__lte=checkout_date,
                                                checkout__gte=checkout_date).exists()

        case_3 = RoomReservation.objects.filter(roomid=varroomid, checkin__gte=checkin_date,
                                                checkout__lte=checkout_date).exists()

        # if either of these is true, abort and render the error
        if case_1 or case_2 or case_3:
            messages.error(request, 'Room already booked!!')
            return redirect('user_history')

        else:
            RoomReservation.objects.create(userid=userobj, hotelid=hotelobj, roomid=varroomid, checkin=checkin_date,
                                           checkout=checkout_date, cardno=cardnumber)
            messages.success(request, 'Room booked successfully!!')
            return redirect('user_history')


def userHistory(request):
    if request.method == 'GET':
        usersession = request.session.get('id')
        userobj = UserRegistration.objects.get(userid=usersession)
        varuemail = userobj.userid
        # print(varuemail)
        varlogoname = userobj.username
        room_list = RoomReservation.objects.filter(userid=varuemail).order_by('-checkin')
        # print(room_list)
        today = date.today()
        today_reserved = RoomReservation.objects.filter(userid=varuemail, checkin__gt=today).order_by('-checkin')
        if len(today_reserved) > 0:
            today_reserved_list = []
            room_list_2 = []
            for rooms in today_reserved:
                today_reserved_list.append(rooms.roomid)
            for rooms in room_list:
                if rooms.roomid not in today_reserved_list:
                    room_list_2.append(rooms.roomid)
            today_reserved_obj = RoomReservation.objects.filter(userid=varuemail, checkin__gt=today,
                                                                roomid__in=today_reserved_list).order_by('-checkin')
            room_list_obj = RoomReservation.objects.filter(roomid__in=room_list_2).order_by('-checkin')
            historyFor = "cancelrooms"
            context = {
                "logoname": varlogoname,
                "reserverdRooms": today_reserved_obj,
                "room_list": room_list_obj,
                "historyFor": historyFor,
            }
            return render(request, 'user_hotel_room_list_history.html', context)
        else:
            historyFor = "showrooms"
            context = {
                "logoname": varlogoname,
                "room_list": room_list,
                "historyFor": historyFor
            }
            return render(request, 'user_hotel_room_list_history.html', context)


def userRating(request, roomid):
    if request.method == 'GET':
        roomid = roomid
        roomobj = HotelRoom.objects.get(roomid=roomid)
        hotelid = roomobj.hotelid.hotelid
        usersession = request.session.get('id')
        userobj = UserRegistration.objects.get(userid=usersession)
        varuemail = userobj.userid
        varlogoname = userobj.username
        # print(hotelid)
        # print(varuemail)

        if Ratings.objects.filter(userid=varuemail, hotelid=hotelid).exists():
            ratingObj = Ratings.objects.get(userid=varuemail, hotelid=hotelid)
            varservrat = ratingObj.ServiceRatings
            varclearat = ratingObj.CleanlinessRatings
            varlocarat = ratingObj.LocationRatings
            varsleqrat = ratingObj.SleepQualityRatings
            varroomrat = ratingObj.RoomsRatings
            context = {
                'logoname': varlogoname,
                'servrat': varservrat,
                'clearat': varclearat,
                'locarat': varlocarat,
                'sleqrat': varsleqrat,
                'roomrat': varroomrat
            }
            return render(request, 'user_ratings.html', context)
        else:
            # print('User can rate hotel')
            context = {
                'logoname': varlogoname,
                'servrat': 1,
                'clearat': 1,
                'locarat': 1,
                'sleqrat': 1,
                'roomrat': 1,
            }
            return render(request, 'user_ratings.html', context)

    if request.method == 'POST':
        roomid = roomid
        roomobj = HotelRoom.objects.get(roomid=roomid)
        hotelobj = roomobj.hotelid
        hotelid = roomobj.hotelid.hotelid
        usersession = request.session.get('id')
        userobj = UserRegistration.objects.get(userid=usersession)
        varuemail = userobj.userid
        varServiceRatings = request.POST.get('result1')
        varServiceRatings = round(float(varServiceRatings))
        varCleanlinessRatings = request.POST.get('result2')
        varCleanlinessRatings = round(float(varCleanlinessRatings))
        varLocationRatings = request.POST.get('result3')
        varLocationRatings = round(float(varLocationRatings))
        varSleepQualityRatings = request.POST.get('result4')
        varSleepQualityRatings = round(float(varSleepQualityRatings))
        varRoomsRatings = request.POST.get('result5')
        varRoomsRatings = round(float(varRoomsRatings))
        # print(varServiceRatings)
        # print(hotelid)
        # print(varuemail)
        if Ratings.objects.filter(userid=varuemail, hotelid=hotelid).exists():
            Ratings.objects.filter(userid=varuemail, hotelid=hotelid).update(ServiceRatings=varServiceRatings,
                                                                             CleanlinessRatings=varCleanlinessRatings,
                                                                             LocationRatings=varLocationRatings,
                                                                             SleepQualityRatings=varSleepQualityRatings,
                                                                             RoomsRatings=varRoomsRatings)
            messages.success(request, 'Hotel ratings updated successfully!!')
        else:
            Ratings.objects.create(userid=userobj, hotelid=hotelobj, ServiceRatings=varServiceRatings,
                                   CleanlinessRatings=varCleanlinessRatings,
                                   LocationRatings=varLocationRatings,
                                   SleepQualityRatings=varSleepQualityRatings,
                                   RoomsRatings=varRoomsRatings)
            messages.success(request, 'Hotel ratings submitted successfully!!')
        return redirect('user_rating', roomid=roomid)


def userLogout(request):
    request.session.flush()
    messages.success(request, 'Successfully logout!!')
    return redirect('login')
