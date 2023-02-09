from APIAuth.models import Authentication
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authentication
        fields = "__all__"
