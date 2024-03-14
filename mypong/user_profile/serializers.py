from rest_framework import serializers

from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    exp = serializers.SerializerMethodField()

    def get_exp(self, obj):
        return obj.wins * 2 + obj.loses

    class Meta:
        model = User
        fields = '__all__'
