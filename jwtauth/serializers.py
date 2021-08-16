import requests
import json
import logging
from django.contrib.auth import get_user_model, authenticate, user_logged_in
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .signals import log_user_logged_in_success, log_user_logged_in_failed, get_client_ip

User = get_user_model()

webhook_url = 'http://www.google.com'
# https://encrusxqoan0b.x.pipedream.net/


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

#     {
#   "username": "user1",
#   "email":"user1@gmail.com",
#   "password":"123",
#   "password2": "123"
# }

# {
#     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyODYwMjMwOCwianRpIjoiMTU3OWJmNDgxOTRlNDY1Y2FkNDFjNzA4MWFmNTViNGMiLCJ1c2VyX2lkIjozfQ.sNsQU-EaGVWiOSTh2LE513W50jE4iySzNbR2NMUXMXE",
#     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI4NTE2MjA4LCJqdGkiOiJlYWUxZTcyMGI2NmM0MGQ2YmFhNTYzOGY3OWM1Y2ZjNCIsInVzZXJfaWQiOjN9.zuz1fccr0E4I37K2Ob2mbv4bvpkZiz6n17keK-82cc0"
# }
    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        """
            Validate login
        """
        try:
            valid = super().validate(attrs)
            log_user_logged_in_success(sender=attrs[self.username_field].__class__, 
                request=self.context["request"], user=attrs[self.username_field])
            self.send_notification_to_team(attrs, self.context["request"])
            logging.info("Login successful")
        except Exception as ex:
            authenticate_kwargs = {
                "username": attrs[self.username_field],
                'password': attrs['password'],
            }
            logging.debug("Exception %s"%ex)
            log_user_logged_in_failed(sender=attrs[self.username_field].__class__, 
                request=self.context["request"], credentials=authenticate_kwargs)
        return {}

    
    def send_notification_to_team(self,attrs, request_data):
        """
            Send notification to team
        """
        user_ip = get_client_ip(request_data)
        data = {
            "user": attrs[self.username_field],
            "id": user_ip
        }
        r = requests.post(webhook_url, json.dumps(data), headers={'Content-Type': 'application/json'})
        return r


   