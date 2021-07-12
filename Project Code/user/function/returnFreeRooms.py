from user.models import *
from django.db.models import Q


# This function return rooms object which is not occupied
def returnFreeRoom(room_list, checkin, checkout):
    roomids = []
    for rooms in room_list:
        if rooms.roomid not in roomids:
            roomids.append(rooms.roomid)
    availableRoomList = []
    for rooms in roomids:
        case_1 = RoomReservation.objects.filter(roomid=rooms, checkin__lte=checkin,
                                                checkout__gte=checkin).exists()

        # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
        case_2 = RoomReservation.objects.filter(roomid=rooms, checkin__lte=checkout,
                                                checkout__gte=checkout).exists()

        case_3 = RoomReservation.objects.filter(roomid=rooms, checkin__gte=checkin,
                                                checkout__lte=checkout).exists()
        if case_1 or case_2 or case_3:
            None
        else:
            availableRoomList.append(rooms)
    # print("Available room ids: ", availableRoomList)
    return availableRoomList


def getBookedRoom(room_list, checkin, checkout):
    roomids = []
    for rooms in room_list:
        if rooms.roomid not in roomids:
            roomids.append(rooms.roomid)
    bookedRoomList = []
    for rooms in roomids:
        case_1 = RoomReservation.objects.filter(roomid=rooms, checkin__lte=checkin,
                                                checkout__gte=checkin).exists()

        # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
        case_2 = RoomReservation.objects.filter(roomid=rooms, checkin__lte=checkout,
                                                checkout__gte=checkout).exists()

        case_3 = RoomReservation.objects.filter(roomid=rooms, checkin__gte=checkin,
                                                checkout__lte=checkout).exists()
        if case_1 or case_2 or case_3:
            bookedRoomList.append(rooms)
    print("Booked room ids: ", bookedRoomList)
    return bookedRoomList
