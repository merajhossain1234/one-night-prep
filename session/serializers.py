from rest_framework import serializers
from .models import Session, SessionMember
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class SessionMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())


    class Meta:
        model = SessionMember
        fields = ['id', 'user', 'permission']

class SessionSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    class Meta:
        model = Session
        fields = ['id', 'creator', 'members']

