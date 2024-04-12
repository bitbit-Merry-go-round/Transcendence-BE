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
        fields = "__all__"


class UserSimpleSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    class Meta:
        model = User
        fields = ['username', 'avatar', 'level', 'status']


class MyProfileSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    class Meta:
        model = User
        fields = ['username', 'avatar', 'level', 'status', 'message', 'wins', 'loses']


class MyProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = BinaryField()

    class Meta:
        model = User
        fields = ['avatar', 'status', 'message', 'wins', 'loses']
        read_only_fields = ['username']


class MyFriendSerializer(serializers.ModelSerializer):
    to_user = UserSimpleSerializer(read_only=True)

    def validate(self, data):
        from_user = self.context['me']
        request_data = self.context['request'].data
        to_user = request_data.get('to_user')

        from_user = User.objects.filter(username=from_user).first()
        to_user = User.objects.filter(username=to_user).first()

        if from_user is None:
            raise ValidationError("from_user does not exist")
        if to_user is None:
            raise ValidationError("to_user does not exist")
        if from_user == to_user:
            raise ValidationError("from_user and to_user are identical")

        friend = Friend.objects.filter(from_user=from_user, to_user=to_user).first()
        if friend is not None:
            raise ValidationError("friend already exists")

        return data

    def create(self, validated_data):
        from_user = self.context['me']
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


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = BinaryField()
    level = serializers.SerializerMethodField()
    is_me = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()

    def validate(self, data):
        me = self.context["me"]
        username = self.context["username"]

        me = User.objects.filter(username=me).first()
        user = User.objects.filter(username=username).first()

        if me is None:
            raise ValidationError("auth username does not exist")
        if user is None:
            raise ValidationError("username does not exist")

        return data

    def get_level(self, obj):
        return (obj.wins * 2 + obj.loses) / 10 + 1

    def get_is_me(self, obj):
        me = self.context["me"]

        me = User.objects.get(username=me)
        user = obj

        if me == user:
            return True
        else:
            return False

    def get_is_friend(self, user):
        from_user = self.context["me"]
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
