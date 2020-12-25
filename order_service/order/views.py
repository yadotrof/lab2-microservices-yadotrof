from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UsersOrderSerializer, RequestItemSerializer, WarrantyRequestSerializer
from .models import Order
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests
from uuid import uuid4

from .externalcall import external_call, ExternalCallException

class OrderActions(APIView):
    def get(self, request, uuid, format=None):
        """
        Get all user`s orders.
        """
        objects = Order.objects.filter(user_uuid=uuid)
        serializer = UsersOrderSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, uuid, format=None):
        """
        Add order.
        """
        serializer = RequestItemSerializer(data=request.data)
        if serializer.is_valid():
            order_uuid = uuid4()
            try:
                res = external_call(requests.post,
                                    f'{settings.WAREHOUSE_URL}api/v1/warehouse/',
                                    data={'model': serializer.validated_data['model'],
                                        'size': serializer.validated_data['size'],
                                        'order_uuid': order_uuid})
            except ExternalCallException as e:
                return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
            if res.status_code == 200:
                data = res.json()
                try:
                    external_call(requests.post, 
                                  f'{settings.WARRANTY_URL}api/v1/warranty/{data["item_uuid"]}')
                except ExternalCallException as e:
                    try:
                        external_call(requests.delete,
                                    f'{settings.WAREHOUSE_URL}api/v1/warehouse/{data['item_uuid']}')
                        except ExternalCallException as e:
                            pass
                    return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
                Order.objects.create(uuid=data['order_uuid'],
                                     item_uuid=data['item_uuid'],
                                     user_uuid=uuid)
                return Response({'order_uuid': order_uuid}, status.HTTP_200_OK)
            if res.status_code == 409:
                return Response({'message': 'Item not avaliable'}, status.HTTP_409_CONFLICT)
            print(res)
        return Response({'message': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        """
        Delete order
        """
        order = get_object_or_404(Order, uuid=uuid)
        try:
            external_call(requests.delete,
                          f'{settings.WARRANTY_URL}api/v1/warranty/{order.item_uuid}')
        except ExternalCallException as e:
            return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
        try:
            res = external_call(requests.delete,
                                f'{settings.WAREHOUSE_URL}api/v1/warehouse/{order.item_uuid}')
        except ExternalCallException as e:
            try:
                external_call(requests.post, 
                              f'{settings.WARRANTY_URL}api/v1/warranty/{order.item_uuid}')
            except ExternalCallException as e:
                pass
            return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
        order.delete()
        if res.status_code == 203:
            return Response({'message': 'Order returned'}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        if res.status_code == 404:
            return Response({'message': 'Order not found'}, status.HTTP_404_NOT_FOUND)
        if res.status_code == 400:
            return Response({'message': 'Order already returned'}, status.HTTP_404_NOT_FOUND)


class OrderDetail(APIView):
    def get(self, request, user_uuid, order_uuid, format=None):
        """
        Get user`s order info.
        """
        object = get_object_or_404(Order, user_uuid=user_uuid, uuid=order_uuid)
        serializer = UsersOrderSerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Warranty(APIView):
    def post(self, request, order_uuid, format=None):
        """
        Request warranty.
        """
        serializer = WarrantyRequestSerializer(data=request.data)
        if serializer.is_valid():
            object = get_object_or_404(Order, uuid=order_uuid)
            data = serializer.validated_data
            try:
                res = external_call(requests.post,
                                    f'{settings.WAREHOUSE_URL}api/v1/warehouse/{object.item_uuid}/warranty',
                                    data=data)
            except ExternalCallException as e:
                return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
            return Response(res.json(), res.status_code)
        return Response({'message': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)
