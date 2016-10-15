from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class UserCredentials(models.Model):
    user=models.ForeignKey(User,unique=True)
    State=models.CharField(max_length=150,blank=True)
    Address=models.CharField(max_length=100,blank=True)

    def __unicode__(self):
        return '%s' % self.Address


class Adverts (models.Model):
     propertytype=models.CharField(max_length=14)
     state=models.CharField(max_length=14)
     localgovt=models.CharField(max_length=30)
     streetaddress=models.CharField(max_length=150)
     propertyname=models.CharField(max_length=100)
     fulladdress=models.CharField(max_length=250)
     description=models.CharField(max_length=300)

class Facilities(models.Model):
    facadverts=models.ForeignKey(Adverts,unique=True)
    facilityname=models.CharField(max_length=20)

class PropertyPreference(models.Model):
    proadverts=models.ForeignKey(Adverts,unique=True)
    smoking=models.BooleanField()
    pet=models.BooleanField()
    bills=models.BooleanField()
    furnished=models.BooleanField()
    sharing=models.BooleanField()
    gender=models.CharField(max_length=15)

class BasicInfo(models.Model):
    basadverts=models.ForeignKey(Adverts,unique=True)
    no_bathrooms=models.IntegerField()
    no_bedrooms=models.IntegerField()
    no_toilets=models.IntegerField()
    price=models.CharField(max_length=30)
    availability=models.CharField(max_length=30)

class Photo(models.Model):
    adverts = models.ForeignKey(Adverts,related_name='adverts')
    picture = models.ImageField(upload_to='%Y/%m/%d')
    description=models.CharField(max_length=100)



    class Admin:
        def __init__(self):
            pass
