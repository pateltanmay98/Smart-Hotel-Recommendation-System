from django.db import models

# Create your models here.
from registration.models import HotelRegistration, UserRegistration


class RoomReservation(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    hotelid = models.ForeignKey(to=HotelRegistration, on_delete=models.CASCADE)
    roomid = models.CharField(max_length=40, null=False, default='tanmay')
    checkin = models.DateField(null=False)
    checkout = models.DateField(null=False)
    cardno = models.CharField(max_length=20, null=True)


class Ratings(models.Model):
    userid = models.ForeignKey(to=UserRegistration, on_delete=models.CASCADE)
    hotelid = models.ForeignKey(to=HotelRegistration, on_delete=models.CASCADE)
    ServiceRatings = models.IntegerField()
    CleanlinessRatings = models.IntegerField()
    LocationRatings = models.IntegerField()
    SleepQualityRatings = models.IntegerField()
    RoomsRatings = models.IntegerField()
