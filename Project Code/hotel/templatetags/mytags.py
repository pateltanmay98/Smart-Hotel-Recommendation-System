from django import template
import datetime
from hotel.models import HotelRoom, RoomDescription, HotelImage, RoomImage
from registration.models import UserRegistration, HotelAddress
from user.models import RoomReservation, Ratings

register = template.Library()


@register.simple_tag
def get_hotel_min_rent(hotelid):
    try:
        roomobj = HotelRoom.objects.filter(hotelid=hotelid)
        # print(roomobj)
        roomidlist = []

        for roomid in roomobj:
            roomidlist.append(roomid.roomid)

        room_list = RoomDescription.objects.filter(roomid__in=roomidlist)

        value_list = []

        for cost in room_list:
            value_list.append(cost.roomrent)

        for i in range(0, len(value_list)):
            value_list[i] = int(value_list[i])

        minrent = min(value_list)

    except:
        minrent = 'Rate not defined'
    return minrent


@register.simple_tag
def get_hotel_max_rent(hotelid):
    try:
        roomobj = HotelRoom.objects.filter(hotelid=hotelid)
        # print(roomobj)
        roomidlist = []

        for roomid in roomobj:
            roomidlist.append(roomid.roomid)

        room_list = RoomDescription.objects.filter(roomid__in=roomidlist)

        value_list = []

        for cost in room_list:
            value_list.append(cost.roomrent)

        for i in range(0, len(value_list)):
            value_list[i] = int(value_list[i])
        maxrent = max(value_list)
    except:
        maxrent = 'Rate not defined'
    # if len(value_list) == 0:
    # else:
    # print(maxrent)
    return maxrent


@register.simple_tag
def get_hotel_name(roomid):
    try:
        roomobj = HotelRoom.objects.get(roomid=roomid)
        # print(roomobj)
        hotelobj = roomobj.hotelid
        hname = hotelobj.hotelname
    except:
        hname = 'Hotel name not found!!'
    return hname


@register.simple_tag
def get_hotel_address(hotelid):
    try:
        addressobj = HotelAddress.objects.get(hotelid=hotelid)
        address = addressobj.hoteladdress
    except:
        address = 'Address not found!!'
    return address


@register.simple_tag
def get_hotel_city(hotelid):
    try:
        addressobj = HotelAddress.objects.get(hotelid=hotelid)
        cityobj = addressobj.cityid
        cityname = cityobj.cityname
    except:
        cityname = 'City name not found!!'
    return cityname


@register.simple_tag
def get_hotel_state(hotelid):
    try:
        addressobj = HotelAddress.objects.get(hotelid=hotelid)
        cityobj = addressobj.cityid
        statename = cityobj.statename
    except:
        statename = 'State name not found!!'
    return statename


@register.simple_tag
def get_room_no(roomid):
    try:
        roomobj = HotelRoom.objects.get(roomid=roomid)
        # print(room_object)
        roomno = roomobj.roomno
    except:
        roomno = 'Room no not found!!'
    return roomno


@register.simple_tag
def get_user_name_obj(userid):
    try:
        username = userid.username
    # print(username)
    except:
        username = 'Username not found!!'
    return username


@register.simple_tag
def get_user_contact_obj(userid):
    try:
        usercontactno = userid.usermobileno
    except:
        usercontactno = 'Contact no not found!!'
    return usercontactno


@register.simple_tag
def date_from(roomid):
    # print(roomid)
    if RoomReservation.objects.filter(roomid=roomid).exists():
        room_list = RoomReservation.objects.filter(roomid=roomid).order_by('-checkin')[0]
        varcheckin = room_list.checkin
        checkin = varcheckin.strftime("%d-%m-%Y")
        return checkin
    else:
        return 'No last checkin date'


@register.simple_tag
def date_to(roomid):
    # print(roomid)
    if RoomReservation.objects.filter(roomid=roomid).exists():
        room_list = RoomReservation.objects.filter(roomid=roomid).order_by('-checkout')[0]
        varcheckout = room_list.checkout
        checkout = varcheckout.strftime("%d-%m-%Y")
        return checkout
    else:
        return 'No last checkout date'


@register.simple_tag
def get_room_rent(roomid):
    try:
        roomdesobj = RoomDescription.objects.get(roomid=roomid)
        room_rent = roomdesobj.roomrent
    except:
        room_rent = 'Room rent not found'
    return room_rent


@register.simple_tag
def get_room_type(roomid):
    try:
        roomdesobj = RoomDescription.objects.get(roomid=roomid)
        room_type = roomdesobj.roomtype
    except:
        room_type = 'Room type not found!!'
    return room_type


@register.simple_tag
def get_occupied_text(roomid):
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if (RoomReservation.objects.filter(roomid=roomid, checkin__gte=today).exists()) or (
                RoomReservation.objects.filter(roomid=roomid, checkout=today).exists()):
            text = "Room occupied for today"
        else:
            text = "Room not occupied"
    except:
        text = "Can't fetch data"
    return text


@register.simple_tag
def get_hotel_image(hotelid):
    imageobj = HotelImage.objects.get(hotelid=hotelid)
    return imageobj


@register.simple_tag
def get_hotel_image2(roomid):
    roomobj = HotelRoom.objects.get(roomid=roomid)
    hotelobj = roomobj.hotelid
    imageobj = HotelImage.objects.get(hotelid=hotelobj)
    return imageobj


@register.simple_tag
def get_room_image(roomid):
    roomobj = HotelRoom.objects.get(roomid=roomid)
    roomid = roomobj.roomid
    imageobj = RoomImage.objects.get(roomid=roomid)
    return imageobj


@register.simple_tag
def get_hotel_total_rating(hotelid):
    try:
        count = Ratings.objects.filter(hotelid=hotelid).count()
        return count
    except:
        return 'Value not found'


@register.simple_tag
def get_hotel_avg_rating(hotelid):
    try:
        a, b, c, d, e = 0, 0, 0, 0, 0
        ratingObj = Ratings.objects.filter(hotelid=hotelid)
        for ratings in ratingObj:
            varservrat = ratings.ServiceRatings
            varclearat = ratings.CleanlinessRatings
            varlocarat = ratings.LocationRatings
            varsleqrat = ratings.SleepQualityRatings
            varroomrat = ratings.RoomsRatings
            varServiceRatings = round(float(varservrat))
            varCleanlinessRatings = round(float(varclearat))
            varLocationRatings = round(float(varlocarat))
            varSleepQualityRatings = round(float(varsleqrat))
            varRoomsRatings = round(float(varroomrat))
            totalrating = varServiceRatings + varCleanlinessRatings + varLocationRatings + varSleepQualityRatings + varRoomsRatings
            avgrat = round(totalrating / 5)
            if avgrat == 1:
                a += 1
            elif avgrat == 2:
                b += 1
            elif avgrat == 3:
                c += 1
            elif avgrat == 4:
                d += 1
            elif avgrat == 5:
                e += 1
        ratingCount = a + b + c + d + e
        a2 = a * 1
        b2 = b * 2
        c2 = c * 3
        d2 = d * 4
        e2 = e * 5
        weightedTotal = a2 + b2 + c2 + d2 + e2
        averageRating = weightedTotal / ratingCount
        averageRatingRound = round(averageRating, 1)
        return averageRatingRound
    except:
        return 'Value not found'
