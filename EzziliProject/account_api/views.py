# Create your views here.
from django.conf import settings
from django.core import exceptions
from django.http import HttpResponse, HttpResponseServerError

from rest_framework import status,permissions,exceptions,generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt import authentication
from EzziliApp.models import UserCredentials
from account_api.serializers import AccountSerializer, UserCredentialsSerializer, UserDetailsSerializer, LoginSerializer, TokenSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, PasswordChangeSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)

@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def new_account(request):
    """
    Registration
    """
    if request.method =='GET':
        tasks = User.objects.all()
        serializer = AccountSerializer(tasks, many=True,)
        return Response({"success":"You are not allowed to view resource"})
    if request.method =='POST':
        json_data=simplejson.loads(request.POST['_content'])
        username =(json_data['username'])
        password = make_password((json_data['password']))
        firstname=(json_data['first_name'])
        lastname=(json_data['last_name'])
        email =(json_data['email'])
        State =(json_data['State'])
        Address =(json_data['Address'])
        Data={'username':username,'password':password,'email':email,'first_name':firstname,'last_name':lastname}
        serializer = AccountSerializer(data=Data)
        if serializer.is_valid():
            serializer.save()
            Data_cred={'user':User.objects.get(username=username).id,'password':password,'first_name':firstname,'last_name':lastname,'email':email,'State':State,'Address':Address}
            user_cred=UserCredentialsSerializer(data=Data_cred)
            if user_cred.is_valid():
                user_cred.save()
                return Response(user_cred.data, status=status.HTTP_201_CREATED)
            else:
                user=AccountSerializer(data=Data)
                user.delete()
                return Response(user_cred.errors, status=status.HTTP_400_BAD_REQUEST)
            #serializer.data.get('username')

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(RetrieveAPIView):
    """
    Returns User's details in JSON format.

    Accepts the following GET parameters: token
    Accepts the following POST parameters:
        Required: token
        Optional: email, first_name, last_name and UserProfile fields
    Returns the updated UserProfile and/or User object.
    """
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    model=UserCredentials
    serializer_class = UserDetailsSerializer

    def get_object(self):
        """Ensure POSTing form over token auth with correct credentials passes and does not require CSRF"""
        return self.request.user

    def get(self, request, format=None):
        """ Retrieve profile of current user or return 401 if not authenticated. """
        serializer = self.serializer_class(request.user, context=self.get_serializer_context())
        return Response(serializer.data)


class UserCred(generics.ListAPIView):
    model=UserCredentials
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = UserCredentialsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset=super(UserCred,self).get_queryset()
        return queryset.filter(user=self.kwargs.get('pk'))



class Login(GenericAPIView):

    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token
    response_serializer = TokenSerializer

    def login(self):
        self.user = self.serializer.object['user']
        self.token, created = self.token_model.objects.get_or_create(
            user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, self.user)

    def get_response(self):
        return Response(self.response_serializer(self.token).data,
            status=status.HTTP_200_OK)

    def get_error_response(self):
        return Response(self.serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.DATA)
        if not self.serializer.is_valid():
            return self.get_error_response()
        self.login()
        return self.get_response()


class Logout(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)

        return Response({"success": "Successfully logged out."},
                        status=status.HTTP_200_OK)


class PasswordReset(GenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.DATA
        serializer = self.get_serializer(data=request.DATA)

        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        # Return the success message with OK HTTP status
        return Response({"success": "Password reset e-mail has been sent."},
                         status=status.HTTP_200_OK)


class PasswordResetConfirm(GenericAPIView):

    """
    Password reset e-mail link is confirmed, therefore this resets the user's password.

    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"success": "Password has been reset with the new password."})


class PasswordChange(GenericAPIView):

    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"success": "New password has been saved."})
