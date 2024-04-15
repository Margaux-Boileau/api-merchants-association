from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'is_owner_of_shop']


class RegisterSerializer(serializers.ModelSerializer):
    #validators=[validate_password]
    password = serializers.CharField(write_only=True,)

    class Meta:
        model = Account
        fields = ['username', 'password', 'is_owner_of_shop']

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)