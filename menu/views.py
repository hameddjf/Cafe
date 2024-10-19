from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from .models import Menu
from .serializers import MenuChildSerializer, MenuParentSerializer


class MenuListView(APIView):
    def get(self, request):
        parent_menus = Menu.objects.filter(parent=None).prefetch_related(
            Prefetch('children', queryset=Menu.objects.all(),
                     to_attr='prefetched_children')
        )
        serializer = MenuParentSerializer(parent_menus, many=True)
        return Response(serializer.data)


class MenuDetailView(APIView):
    def get(self, request, slug):
        menu = get_object_or_404(Menu.objects.prefetch_related(
            Prefetch('children', queryset=Menu.objects.all(),
                     to_attr='prefetched_children')
        ), slug=slug)
        serializer = MenuParentSerializer(menu)
        return Response(serializer.data)
