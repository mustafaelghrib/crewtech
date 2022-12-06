from rest_framework import serializers

from ..models.user_model import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "name",
            "image",
            "created_at",
            "updated_at",
        ]
