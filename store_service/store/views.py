import requests

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import RequestItemSerializer
from .serializers import WarrantyRequestSerializer
from .externalcall import external_call, ExternalCallException


class Purchase(APIView):
    def post(self, request, user_uuid, format=None):
        """
        Create purchase.
        """
        get_object_or_404(User, uuid=user_uuid)
        serializer = RequestItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                res = external_call(requests.post,
                                    f'{settings.ORDER_URL}api/v1/orders/{user_uuid}',
                                    data={'model': serializer.validated_data['model'],
                                        'size': serializer.validated_data['size']})
            except ExternalCallException as e:
                return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
            resp = Response(res.json(), 201 if res.status_code == 200 else res.status_code)
            if res.status_code == 200:
                resp['Location'] = f'{settings.ORDER_URL}api/v1/orders/{user_uuid}/{res.json()["order_uuid"]}'
            return resp
        return Response({'message': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)


class OrderList(APIView):
    def get(self, request, user_uuid, format=None):
        """
        Get user`s orders.
        """
        get_object_or_404(User, uuid=user_uuid)
        try:
            res = external_call(requests.get,
                                f'{settings.ORDER_URL}api/v1/orders/{user_uuid}')
        except ExternalCallException as e:
            return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
        orders = res.json()
        for order in orders:
            try:
                res = external_call(requests.get,
                                    f'{settings.WAREHOUSE_URL}api/v1/warehouse/{order["item_uuid"]}')
                item = res.json()
                order['model'] = item['model']
                order['size'] = item['size']
            except ExternalCallException as e:
                pass
            try:
                res = external_call(requests.get,
                                    f'{settings.WARRANTY_URL}api/v1/warranty/{order["item_uuid"]}')
                warranty = res.json()
                order['warranty_date'] = warranty['date']
                order['warranty_status'] = warranty['status']
            except ExternalCallException as e:
                pass
        return Response(orders, status.HTTP_200_OK)


class OrderDetail(APIView):
    def get(self, request, user_uuid, order_uuid, format=None):
        """
        Get order detail.
        """
        get_object_or_404(User, uuid=user_uuid)
        try:
            res = external_call(requests.get,
                                f'{settings.ORDER_URL}api/v1/orders/{user_uuid}/{order_uuid}')
        except ExternalCallException as e:
            return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
        order = res.json()
        try:
            res = external_call(requests.get,
                                f'{settings.WAREHOUSE_URL}api/v1/warehouse/{order["item_uuid"]}')
            item = res.json()
            order['model'] = item['model']
            order['size'] = item['size']
        except ExternalCallException as e:
            pass
        try:
            res = external_call(requests.get,
                                f'{settings.WARRANTY_URL}api/v1/warranty/{order["item_uuid"]}')
            warranty = res.json()
            order['warranty_date'] = warranty['date']
            order['warranty_status'] = warranty['status']
        except ExternalCallException as e:
            pass
        return Response(order, status.HTTP_200_OK)


class Warranty(APIView):
    def post(self, request, user_uuid, order_uuid, format=None):
        """
        Request warranty.
        """
        get_object_or_404(User, uuid=user_uuid)
        seriallizer = WarrantyRequestSerializer(data=request.data)
        if seriallizer.is_valid():
            try:
                res = external_call(requests.post,
                                    f'{settings.ORDER_URL}api/v1/orders/{order_uuid}/warranty',
                                    data=seriallizer.validated_data)
            except ExternalCallException as e:
                return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
            return Response(res.json(), res.status_code)
        return Response({'message': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)


class Refund(APIView):
    def delete(self, request, user_uuid, order_uuid, format=None):
        """
        Request refund.
        """
        get_object_or_404(User, uuid=user_uuid)
        try:
            res = external_call(requests.delete,
                                f'{settings.ORDER_URL}api/v1/orders/{order_uuid}')
        except ExternalCallException as e:
            return Response({'message': str(e)}, status.HTTP_400_BAD_REQUEST)
        return Response(res.json(), res.status_code)
