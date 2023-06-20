from rest_framework.fields import CharField, EmailField, ImageField, BooleanField
from rest_framework.serializers import Serializer


class TokenUserSerializer(Serializer):
    token = CharField(required=True)


class RegistrationUserSerializer(Serializer):
    email = EmailField(required=True, max_length=50)
    password = CharField(required=True, max_length=50)
    confirm_password = CharField(required=True, max_length=50)
    first_name = CharField(required=True, max_length=50)
    last_name = CharField(required=True, max_length=50)


class LoginUserSerializer(Serializer):
    email = EmailField(required=True, max_length=50)
    password = CharField(required=True, max_length=50)


class ImageSerializer(Serializer):
    image = ImageField()


class UserDataSerializer(Serializer):
    email = EmailField(required=True, max_length=50)
    first_name = CharField(required=True, max_length=50)
    last_name = CharField(required=True, max_length=50)
    full_name = CharField(required=True, max_length=100)
    image = BooleanField(required=False)
    phone_number = CharField(required=False, allow_null=True)
    type = CharField(required=True)


class EditProfileSerializer(Serializer):
    first_name = CharField(required=False, max_length=50)
    last_name = CharField(required=False, max_length=50)
    image = ImageField(required=False)
    phone_number = CharField(required=False, max_length=15)
