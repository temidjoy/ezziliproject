from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from django.forms import widgets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_jwt.utils import get_user_model
from EzziliApp.models import UserCredentials
try:
    from django.utils.http import urlsafe_base64_decode as uid_decoder
except:
    # make compatible with django 1.5
    from django.utils.http import base36_to_int as uid_decoder

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','email','first_name','last_name',)


class UserCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredentials
        fields = ('user','State','Address')


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key','user','created')


class LoginSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        attrs = super(LoginSerializer, self).validate(attrs)

        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                user = attrs['user']
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError('E-mail is not verified.')
        return attrs


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    UserMoreinfo = serializers.HyperlinkedIdentityField('Userinfo',view_name='More-list')

    class Meta:
        model = get_user_model()
        fields = ('id','username','password', 'email', 'first_name', 'last_name','UserMoreinfo')


class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, attrs, source):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=attrs)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError('Error')
        return attrs

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}
        # Get the UserModel
        UserModel = get_user_model()
        # Decode the uidb64 to uid to get User object
        try:
            uid = uid_decoder(attrs['uid'])
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            self._errors['uid'] = ['Invalid value']

        self.custom_validation(attrs)

        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(user=self.user,
            data=attrs)
        if not self.set_password_form.is_valid():
            self._errors['token'] = ['Invalid value']

        if not default_token_generator.check_token(self.user, attrs['token']):
            self._errors['token'] = ['Invalid value']

    def save(self):
        self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(settings,
            'OLD_PASSWORD_FIELD_ENABLED', False)
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, attrs, source):
        if self.old_password_field_enabled and self.user and \
            not self.user.check_password(attrs.get(source, '')):
            raise serializers.ValidationError('Invalid password')
        return attrs

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(user=self.user,
            data=attrs)

        if not self.set_password_form.is_valid():
            self._errors = self.set_password_form.errors
            return None
        return attrs

    def save(self):
        self.set_password_form.save()


