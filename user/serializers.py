from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser  # for type hinting
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # users should not be able to directly update their last login
    last_login = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'last_login')


class SignUpSerializer(serializers.ModelSerializer):
    """
    serializer for signing up a new user
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField()
    password = serializers.CharField(required=True, write_only=True)

    # successful signup should return a token to make subsequent request
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'token')

    def validate_email(self, email: str):
        """
        email should be unique
        :param email: user email address
        :return: email address
        """

        exist = User.objects.filter(email=email).exists()
        if exist:
            raise ValidationError("Email provided is already in use.")
        return email

    def create(self, validated_data):
        """
        create a new user
        :param validated_data:
        :return: created user
        """

        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')

        # create user
        new_user: AbstractUser = User.objects.create(username=username, email=email, first_name=first_name,
                                                     last_name=last_name)

        # assign password
        new_user.set_password(password)
        new_user.save()

        # return newly created user
        return new_user

    def get_token(self, user: AbstractUser):
        """
        get auth token for user
        """

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
