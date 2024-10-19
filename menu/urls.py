from django.urls import path
from .views import MenuListView, MenuDetailView

urlpatterns = [
    path('menus/', MenuListView.as_view(), name='menu-list'),
    path('menus/<slug:slug>/', MenuDetailView.as_view(), name='menu-detail'),
]
