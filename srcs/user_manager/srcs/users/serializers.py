import base64

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Friend

class BinaryField(serializers.Field):
    def to_representation(self, value):
        return base64.b64encode(value)

    def to_internal_value(self, value):
        return base64.b64decode(value)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSimpleSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    class Meta:
        model = User
        fields = ['username', 'avatar', 'level', 'status']



class UserDetailSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()
    is_me = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    def get_is_me(self, user):
        me = self.context["auth_user"]
        me = User.objects.get(username=me)
        user = User.objects.get(username=user)
        if me == user:
            return True
        else:
            return False

    def get_is_friend(self, user):
        from_user = self.context["auth_user"]
        to_user = self.context["username"]
        from_user = User.objects.get(username=from_user)
        to_user = User.objects.get(username=to_user)
        friend = Friend.objects.filter(from_user=from_user, to_user=to_user).first()
        if friend is None:
            return False
        else:
            return True

    class Meta:
        model = User
        fields = ['username', 'avatar', 'level', 'status', 'message', 'wins', 'loses', 'is_me', 'is_friend']


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = BinaryField()

    class Meta:
        model = User
        fields = ['message', 'avatar']
        read_only_fields = ['username', 'status', 'wins', 'loses']


class FriendCreationSerializer(serializers.ModelSerializer):
    to_user = UserDetailSerializer(read_only=True)

    def validate(self, data):
        from_user = self.context['auth_user']
        request_data = self.context['request'].data
        username = request_data.get('to_user')
        to_user = User.objects.get(username=username)
        if to_user is None:
            raise ValidationError('to_user does not exist.')
        if from_user == to_user:
            raise ValidationError('from_user and to_user are identical.')
        return data

    def create(self, validated_data):
        from_user = self.context['auth_user']
        request_data = self.context['request'].data
        to_user = request_data.get('to_user')
        from_user = User.objects.get(username=from_user)
        to_user = User.objects.get(username=to_user)
        friend = Friend.objects.create(from_user=from_user, to_user=to_user)
        return friend

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop('to_user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation

    class Meta:
        model = Friend
        fields = ['to_user']


class FriendListSerializer(serializers.ModelSerializer):
    to_user = UserSimpleSerializer(read_only=True)

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop('to_user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation

    class Meta:
        model = Friend
        fields = ['to_user']
