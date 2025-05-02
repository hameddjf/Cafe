from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer


# class OrderListCreateView(APIView):
# #     permission_classes = [AllowAny]  


#     def get(self, request):
#         orders = Order.objects.filter(
#             user=request.user).prefetch_related('order_items__menu_item')
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = OrderSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListCreateView(APIView):    
    def get(self, request):
        orders = Order.objects.all().prefetch_related('order_items__menu_item')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# {
#     "order_items": [
#         {
#             "menu_item_id": 1,   // شناسه منوی مرتبط
#             "size": "SMALL",      // اندازه باید یکی از "SMALL" یا "LARGE" باشد
#             "quantity": 2         // تعداد باید حداقل 1 باشد
#         },
#         {
#             "menu_item_id": 2,   // شناسه منوی دیگر
#             "size": "LARGE",      // اندازه می‌تواند "SMALL" یا "LARGE" باشد
#             "quantity": 1         // تعداد حداقل 1
#         }
#     ]
# }