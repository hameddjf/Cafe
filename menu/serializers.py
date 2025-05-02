from rest_framework import serializers
from .models import Menu


class MenuChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'slug', 'resizes_images', 'available',]


class MenuParentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'slug', 'prices', 'resizes_images',
                  'description', 'children', 'available']
        
    def get_prices(self, obj):
        prices = {}
        if obj.price_small is not None:
            prices['small'] = obj.price_small
        if obj.price_large is not None:
            prices['large'] = obj.price_large
        return prices

    def get_children(self, obj):
        return MenuChildSerializer(obj.get_children(), many=True).data
