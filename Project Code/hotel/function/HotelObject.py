from registration.models import HotelRegistration


def returnHotelName(hotelid):
    hotel_object = HotelRegistration.objects.get(hotelid=hotelid)
    hotel_name = hotel_object.hname
    return hotel_name
