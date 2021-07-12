from numpy import record

from registration.models import *


def getCityHotelsList(bestHotelsList, cityobj):
    cityid = []
    for city in cityobj:
        if city.cityid not in cityid:
            cityid.append(city.cityid)
    # print(cityid)
    reccityHotels = []
    hotelsobj = HotelAddress.objects.all().filter(hotelid__in=bestHotelsList, cityid__in=cityid)
    for hotels in hotelsobj:
        if hotels.hotelid not in reccityHotels:
            reccityHotels.append(hotels.hotelid)
        if len(reccityHotels) > 20:
            break
    print(len(reccityHotels))
    return reccityHotels


def getOthCityHotelsList(getCityHotels, cityobj):
    if len(getCityHotels) < 20:
        cityid = []
        for city in cityobj:
            if city.cityid not in cityid:
                cityid.append(city.cityid)
        otherCity = []
        hotelsobj = HotelAddress.objects.all().filter(cityid__in=cityid)
        for hotels in hotelsobj:
            if hotels.hotelid not in getCityHotels:
                otherCity.append(hotels.hotelid)
        needIdsToAppend = 20 - len(getCityHotels)
        otherCItyAppend = []
        if needIdsToAppend <= 0:
            for i in len(otherCity):
                otherCItyAppend.append(otherCity[i])
                lenTotalHotels = len(otherCItyAppend) + len(getCityHotels)
                if lenTotalHotels == 20:
                    break
        print("Other City list: ", otherCItyAppend)
        return otherCItyAppend
    else:
        otherCItyAppend = []
        return otherCItyAppend
