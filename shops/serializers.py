from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'schedule', 'phone', 'sector', 'image', 'instagram', 'facebook', 'webpage']
class UpdateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'schedule', 'phone', 'instagram', 'facebook', 'webpage', 'sector', 'image']