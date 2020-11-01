from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UsersOrderSerializer, RequestItemSerializer, WarrantyRequestSerializer
from .models import Order
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests
from uuid import uuid4

@api_view(['GET', 'POST','DELETE'])
def order_actions(request, uuid):
    if request.method == 'GET':
        """
        Get all user`s orders.
        """
        objects = Order.objects.filter(user_uuid=uuid)
        serializer = UsersOrderSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        """
        Add order.
        """
        serializer = RequestItemSerializer(data=request.data)
        if serializer.is_valid():
            order_uuid = uuid4()
            res = requests.post(f'{settings.WAREHOUSE_URL}api/v1/warehouse/', 
                                data={'model': serializer.validated_data['model'],
                                        'size': serializer.validated_data['size'],
                                        'order_uuid': order_uuid})
            if res.status_code == 200:
                data = res.json()
                requests.post(f'{settings.WARRANTY_URL}api/v1/warranty/{data["item_uuid"]}')
                Order.objects.create(uuid=data['order_uuid'],
                                     item_uuid = data['item_uuid'],
                                     user_uuid = uuid)
                return Response({'order_uuid': order_uuid}, status.HTTP_200_OK)
            if res.status_code == 409:
                return Response({'message': 'Item not avaliable'}, status.HTTP_409_CONFLICT)

    if request.method == 'DELETE':
        """
        Delete order
        """
        order = get_object_or_404(Order, uuid=uuid)
        try:
            requests.delete(f'{settings.WARRANTY_URL}api/v1/warranty/{order.item_uuid}')
            res = requests.delete(f'{settings.WAREHOUSE_URL}api/v1/warehouse/{order.item_uuid}')
            order.delete()
        except:
            return Response({'message': 'External request failed'}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        if res.status_code == 204:
            return Response({'message': 'Order returned'}, status.HTTP_204_NO_CONTENT)
        if res.status_code == 404:
            return Response({'message': 'Order not found'}, status.HTTP_404_NOT_FOUND)
        if res.status_code == 400:
            return Response({'message': 'Order already returned'}, status.HTTP_404_NOT_FOUND)
    return Response({'message': f'Bad request'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_detail(request, user_uuid, order_uuid):
    """
    Get user`s order info.
    """
    object = get_object_or_404(Order, user_uuid=user_uuid, uuid=order_uuid)
    serializer = UsersOrderSerializer(object)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def warranty_request(request, order_uuid):
    """
    Request warranty.
    """
    serializer = WarrantyRequestSerializer(data=request.data)
    if serializer.is_valid():
        object = get_object_or_404(Order, uuid=order_uuid)
        data = serializer.validated_data
        res = requests.post(f'{settings.WAREHOUSE_URL}api/v1/warehouse/{object.item_uuid}/warranty',
                            data=data)
        return Response(res.json(), res.status_code)
    else:
        return Response({'message': f'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)
