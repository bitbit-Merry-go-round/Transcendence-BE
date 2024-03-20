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
    # avatar = BinaryField()
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    class Meta:
        model = User
        fields = ['uid', 'status', 'level']  # 아바타 추가할것


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    class Meta:
        model = User
        fields = ['uid', 'avatar', 'level', 'status', 'message']


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


class FriendListSerializer(serializers.ModelSerializer):
    to_user = UserSimpleSerializer(read_only=True)

    def get_queryset(self, from_user):
        return Friend.objects.filter(from_user=from_user).values()

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop('to_user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation

    class Meta:
        model = Friend
        fields = ['to_user']
