from rest_framework import serializers
from .models import Menu


class MenuChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'slug', 'resizes_images', 'available', ]


class MenuParentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'slug', 'price_small', 'price_large', 'resizes_images',
                  'description', 'children', 'available']

    def get_children(self, obj):
        return MenuChildSerializer(obj.get_children(), many=True).data
