import requests

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from.models import User
from .serializers import RequestItemSerializer
from .serializers import WarrantyRequestSerializer


@api_view(['POST'])
def purchase(request, user_uuid):
    """
    Create purchase.
    """
    get_object_or_404(User, uuid=user_uuid)
    serializer = RequestItemSerializer(data=request.data)
    if serializer.is_valid():
        res = requests.post(f'{settings.ORDER_URL}api/v1/orders/{user_uuid}',
                            data={'model': serializer.validated_data['model'],
                                'size': serializer.validated_data['size']})
        resp = Response(res.json(), 201 if res.status_code == 200 else res.status_code)
        if res.status_code == 200:
            resp['Location'] = f'{settings.ORDER_URL}api/v1/orders/{user_uuid}/{res.json()["order_uuid"]}'
        return resp
    else:
        return Response({'message': f'Bad request'},
                status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_list(request, user_uuid):
    """
    Get user`s orders.
    """
    get_object_or_404(User, uuid=user_uuid)
    res = requests.get(f'{settings.ORDER_URL}api/v1/orders/{user_uuid}')
    orders = res.json()
    for order in orders:
        res = requests.get(f'{settings.WAREHOUSE_URL}api/v1/warehouse/{order["item_uuid"]}')
        item = res.json()
        order['model'] = item['model']
        order['size'] = item['size']
        res = requests.get(f'{settings.WARRANTY_URL}api/v1/warranty/{order["item_uuid"]}')
        warranty = res.json()
        print(warranty.keys(), warranty)
        order['warranty_date'] = warranty['date']
        order['warranty_status'] = warranty['status']
    return Response(orders, status.HTTP_200_OK)

@api_view(['GET'])
def order_detail(request, user_uuid, order_uuid):
    """
    Get order detail.
    """
    get_object_or_404(User, uuid=user_uuid)
    res = requests.get(f'{settings.ORDER_URL}api/v1/orders/{user_uuid}/{order_uuid}')
    order = res.json()
    res = requests.get(f'{settings.WAREHOUSE_URL}api/v1/warehouse/{order["item_uuid"]}')
    item = res.json()
    order['model'] = item['model']
    order['size'] = item['size']
    res = requests.get(f'{settings.WARRANTY_URL}api/v1/warranty/{order["item_uuid"]}')
    warranty = res.json()
    order['warranty_date'] = warranty['date']
    order['warranty_status'] = warranty['status']
    return Response(order, status.HTTP_200_OK)


@api_view(['POST'])
def request_warranty(request, user_uuid, order_uuid):
    """
    Request warranty.
    """
    get_object_or_404(User, uuid=user_uuid)
    seriallizer = WarrantyRequestSerializer(data=request.data)
    if seriallizer.is_valid():
        res = requests.post(f'{settings.ORDER_URL}api/v1/orders/{order_uuid}/warranty',
                            data=seriallizer.validated_data)
        data = res.json()
        return Response(res.json(), res.status_code)
    else:
        return Response({'message': f'Bad request'},
                status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def request_refund(request, user_uuid, order_uuid):
    """
    Request refund.
    """
    get_object_or_404(User, uuid=user_uuid)
    res = requests.delete(f'{settings.ORDER_URL}api/v1/orders/{order_uuid}')
    return Response(res.json(), res.status_code)
