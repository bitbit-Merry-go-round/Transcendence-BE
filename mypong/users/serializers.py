import base64

from rest_framework import serializers

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
    exp = serializers.SerializerMethodField()

    def get_exp(self, obj):
        return obj.wins * 2 + obj.loses

    class Meta:
        model = User
        fields = ['uid', 'avatar', 'status', 'exp']


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    exp = serializers.SerializerMethodField()

    def get_exp(self, obj):
        return obj.wins * 2 + obj.loses

    class Meta:
        model = User
        exclude = ['friends']


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = BinaryField()

    class Meta:
        model = User
        fields = ['message', 'avatar']
        read_only_fields = ['uid', 'status', 'wins', 'loses']


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'
