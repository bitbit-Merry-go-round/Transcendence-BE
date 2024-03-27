import base64

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, Friend


class BinaryField(serializers.Field):
    def to_representation(self, value):
        return base64.b64encode(value)

    def to_internal_value(self, value):
        return base64.b64decode(value)


class UserInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    class Meta:
        model = User
        fields = ['uid', 'avatar', 'level', 'status']


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    class Meta:
        model = User
        fields = ['uid', 'avatar', 'level', 'status', 'message', 'wins', 'loses']


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = BinaryField()

    class Meta:
        model = User
        fields = ['message', 'avatar']
        read_only_fields = ['uid', 'status', 'wins', 'loses']


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        exclude = ['id']

    def validate(self, data):
        from_user = self.context['from_user']
        if from_user != data['from_user'].uid:
            raise ValidationError('from_user does not match.')
        if from_user == data['to_user'].uid:
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
