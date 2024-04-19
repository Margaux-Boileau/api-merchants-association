from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from shops.models import Shop
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'is_owner_of_shop']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    shop_working_at = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all(), required=False)

    class Meta:
        model = Account
        fields = ['username', 'password', 'shop_working_at']

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_owner_of_shop:
            validated_data['shop_working_at'] = user.shop_working_at
        return Account.objects.create_user(**validated_data)