
from django.contrib.auth.models import User, Group
from rest_framework import serializers,exceptions
from EzziliApp.models import Photo, Adverts, PropertyPreference, Facilities, BasicInfo

class Photoserializer(serializers.ModelSerializer):
    image = serializers.Field('picture.url')

    class Meta:
        model=Photo

#class Facilities(serializers.ModelSerializer):

class FacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model =Facilities
        fields = ('facadverts','id','facilityname')

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPreference
        fields = ('proadverts','smoking','pet','bills','furnished','sharing','gender')

class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = ('basadverts','no_bathrooms','no_bedrooms','no_toilets','price','availability')


class AdvertsSerializer(serializers.ModelSerializer):
        picture = serializers.HyperlinkedIdentityField('picture',view_name='advertphoto-list')
        facilities = serializers.HyperlinkedIdentityField('facadverts',view_name='Facility-list')
        property = serializers.HyperlinkedIdentityField('proadverts',view_name='Property-list')
        basicadverts = serializers.HyperlinkedIdentityField('basadverts',view_name='Basic-list')
        class Meta:
            model = Adverts
            fields = ('id','propertytype','state','localgovt','streetaddress','propertyname','fulladdress','description','picture','facilities','property','basicadverts')
