from registration.models import *


def getHotelsFromState(stateName):
    result = []
    citylist = []
    cityobj2 = City.objects.all().filter(statename=stateName)
    for city in cityobj2:
        if city.cityid not in citylist:
            citylist.append(city.cityid)
    hotelobj = HotelAddress.objects.all().filter(cityid__in=citylist)
    hotelids = []
    for hotels in hotelobj:
        hotelids.append(hotels.hotelid.hotelid)
    result = hotelids
    return result
