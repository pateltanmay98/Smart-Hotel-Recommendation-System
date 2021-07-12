from django.db import models

# Create your models here.
from registration.models import HotelRegistration


class HotelRoom(models.Model):
    roomid = models.CharField(primary_key=True, max_length=60)
    hotelid = models.ForeignKey(to=HotelRegistration, on_delete=models.CASCADE)
    roomno = models.IntegerField(null=False)


class RoomDescription(models.Model):
    roomid = models.ForeignKey(to=HotelRoom, on_delete=models.CASCADE)
    roomtype = models.CharField(max_length=10, null=False)
    roomdescription = models.CharField(max_length=100, null=False)
    roombeds = models.IntegerField(null=False)
    roomrent = models.CharField(max_length=6, null=False)


class HotelImage(models.Model):
    hotelid = models.ForeignKey(to=HotelRegistration, on_delete=models.CASCADE)
    hotelimg = models.ImageField(upload_to="hotelimage", null=True, blank=True)


class RoomImage(models.Model):
    roomid = models.ForeignKey(to=HotelRoom, on_delete=models.CASCADE)
    roomimg = models.ImageField(upload_to="roomimage", null=True, blank=True)
