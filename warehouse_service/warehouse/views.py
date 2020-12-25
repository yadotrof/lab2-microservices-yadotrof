import requests
from uuid import uuid4

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import OrderItem, Item
from .serializers import ItemSerializer
from .serializers import OrderRequestSerializer
from .serializers import OrderItemSerializer
from .serializers import WarrantyRequestSerializer


class ItemDetail(APIView):
    def get(self, request, item_uuid, format=None):
        """
        Get item detail.
        """
        object = get_object_or_404(OrderItem, item_uuid=item_uuid)
        serializer = ItemSerializer(object.item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, item_uuid, format=None):
        """
        Return item.
        """
        orderitem = get_object_or_404(OrderItem, item_uuid=item_uuid)
        if not orderitem.canceled:
            item = orderitem.item
            item.available_count = F('available_count') + 1
            item.save()
            orderitem.canceled = True
            orderitem.save()
            return Response({'message': 'Item returned'},
                            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response({'message': 'Item already returned'},
                            status=status.HTTP_400_BAD_REQUEST)


class Purchase(APIView):
    def post(self, request, format=None):
        """
        Add order.
        """
        serializer = OrderRequestSerializer(data=request.data)
        if serializer.is_valid():
            item = get_object_or_404(Item,
                                     model=serializer.validated_data['model'],
                                     size=serializer.validated_data['size'])
            if not item.available_count:
                return Response({'message': 'Item not avaliable'},
                                status=status.HTTP_409_CONFLICT)
            item.available_count = F('available_count') - 1
            item.save()
            object = OrderItem.objects.create(item_uuid=uuid4(),
                                              item=item,
                                              canceled=False,
                                              order_uuid=serializer.validated_data['order_uuid'])
            return Response(OrderItemSerializer(object).data, status=status.HTTP_200_OK)
        return Response({'message': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)


class Warranty(APIView):
    def post(self, request, item_uuid, format=None):
        """
        Request warranty.
        """
        seriallizer = WarrantyRequestSerializer(data=request.data)
        if seriallizer.is_valid():
            object = get_object_or_404(OrderItem,
                                       item_uuid=item_uuid)
            data = seriallizer.validated_data
            data['avaliable_count'] = object.item.available_count
            res = requests.post(f'{settings.WARRANTY_URL}api/v1/warranty/{item_uuid}/warranty',
                                data=data)
            return Response(res.json(), res.status_code)
        return Response({'message': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)
