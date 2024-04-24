from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'bio','address', 'schedule', 'phone', 'sector', 'image', 'instagram', 'facebook', 'webpage', 'mail']
class UpdateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name','bio', 'address', 'schedule', 'phone', 'instagram', 'facebook', 'webpage', 'mail', 'sector', 'image']