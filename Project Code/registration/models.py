from django.db import models


# Create your models here.

class UserRegistration(models.Model):
    userid = models.EmailField(primary_key=True, max_length=50)
    username = models.CharField(max_length=50, null=False)
    userpassword = models.CharField(max_length=40, null=False)
    usermobileno = models.BigIntegerField(null=False)


class HotelRegistration(models.Model):
    hotelid = models.EmailField(primary_key=True, max_length=50)
    hotelname = models.CharField(max_length=50, null=False)
    hotelpassword = models.CharField(max_length=40, null=False)
    hotelmobileno = models.BigIntegerField(null=False)


class City(models.Model):
    cityid = models.AutoField(primary_key=True)
    cityname = models.CharField(max_length=20, null=False)
    statename = models.CharField(max_length=20, null=False, default='Gujarat')
    countryname = models.CharField(max_length=25, null=False, default='India')


class HotelAddress(models.Model):
    hotelid = models.ForeignKey(to=HotelRegistration, on_delete=models.CASCADE)
    cityid = models.ForeignKey(to=City, on_delete=models.CASCADE)
    hoteladdress = models.CharField(max_length=100, null=False)
