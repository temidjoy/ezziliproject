# Create your views here.
from rest_framework import generics, status, permissions
from EzziliApp.models import Photo, Adverts, Facilities, PropertyPreference, BasicInfo
from EzziliApp.serializers import Photoserializer, AdvertsSerializer, FacilitiesSerializer, PropertySerializer, BasicInfoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((TokenAuthentication,SessionAuthentication))
def AdvertDataList(request):
    if request.method == 'GET':
        data = Adverts.objects.all()
        serializer = AdvertsSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = Adverts.objects.all()
        serializer = AdvertsSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvertDataView(GenericAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = AdvertsSerializer

    def get(self, request, format=None):
        data = Adverts.objects.all()
        serializer = self.serializer_class(data,many=True,context={'request': request})
        return Response(serializer.data)

    def post(self,request):

        data = Adverts.objects.all()
        serializer = self.serializer_class(data=request.DATA,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "You have successfully added an Advert.","id":serializer.data.get('id')}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvertsPhotos(generics.ListAPIView):

    model = Photo
    serializer_class = Photoserializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    def get_queryset(self):
        queryset=super(AdvertsPhotos,self).get_queryset()
        return queryset.filter(adverts=self.kwargs.get('pk'))

class PhotoList(generics.ListCreateAPIView):
    model=Photo
    serializer_class = Photoserializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class Photodetail(generics.RetrieveUpdateDestroyAPIView):
    model=Photo
    serializer_class = Photoserializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

class AdvertDetails(generics.ListCreateAPIView):
    model=Facilities
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = FacilitiesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset=super(AdvertDetails,self).get_queryset()
        return queryset.filter(facadverts=self.kwargs.get('pk'))

class PropertyAdvertDetails(generics.ListCreateAPIView):
    model=PropertyPreference
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = PropertySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset=super(PropertyAdvertDetails,self).get_queryset()
        return queryset.filter(proadverts=self.kwargs.get('pk'))

class BasicAdvertDetails(generics.ListCreateAPIView):
    model=BasicInfo
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = BasicInfoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset=super(BasicAdvertDetails,self).get_queryset()
        return queryset.filter(basadverts=self.kwargs.get('pk'))
