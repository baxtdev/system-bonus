from django.contrib.auth import get_user_model
from django.db.models.fields import IntegerField
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField

# from .auth_backend import PasswordlessAuthBackend
from django.contrib.auth import authenticate

User = get_user_model()

def can_register(code):
    user = User.objects.filter(code=code).first()
    if user and user.password:
        raise serializers.ValidationError(_('User with this code already exist.'))


class LoginUserSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=13)
    password = serializers.CharField(required=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
