import base64

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Friend

User = get_user_model()


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

    def get_is_me(self, obj):
        auth_user = self.context['auth_user']
        return auth_user.pk == obj.pk

    def get_is_friend(self, obj):
        auth_user = self.context['auth_user']
        obj = Friend.objects.filter(from_user=auth_user.pk, to_user=obj.pk).first()
        if obj is None:
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


class FriendDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        exclude = ['id']

    def validate(self, data):
        from_user = self.context['from_user']
        if from_user != data['from_user'].username:
            raise ValidationError('from_user does not match.')
        if from_user == data['to_user'].username:
            raise ValidationError('from_user and to_user are identical.')
        return data


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
