import datetime
import pytz

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Warranty
from .serializers import WarrantySerializer
from .serializers import WarrantyRequestSerializer


@api_view(['GET', 'POST','DELETE'])
def warranty_actions(request, item_uuid):
    if request.method == 'GET':
        """
        Check warranty status.
        """
        object = get_object_or_404(Warranty, item_uuid=item_uuid)
        serializer = WarrantySerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        """
        Start warranty
        """
        Warranty.objects.create(comment='',
                                status='ON_WARRANTY',
                                item_uuid=item_uuid)
        return Response({'message': 'Warranty started for item'}, status.HTTP_204_NO_CONTENT)

    if request.method == 'DELETE':
        """
        Stop warranty
        """
        warranty = get_object_or_404(Warranty, item_uuid=item_uuid)
        warranty.delete()
        return Response({'message': 'Warranty closed for item'}, status.HTTP_204_NO_CONTENT)

    return Response({'message': f'Bad request'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_warranty(request, item_uuid):
    """
    Requesr warranty
    """
    serializer = WarrantyRequestSerializer(data=request.data)
    if serializer.is_valid():
        target_date = (datetime.datetime.today() - datetime.timedelta(days=30)).replace(tzinfo=pytz.UTC)
        object = get_object_or_404(Warranty, item_uuid=item_uuid)
        if object.status == 'ON_WARRANTY' and object.date > target_date:
            if serializer.validated_data['avaliable_count'] > 0:
                result = 'RETURN'
            else:
                result = 'FIXING'
            object.status = 'USE_WARRANTY'
            object.save()
        else:
            result = 'REFUSED'
            object.status = 'REMOVED_FROM_WARRANTY'
            object.save()
        return Response({'decision': result, 'date': object.date},
                        status.HTTP_200_OK)
    else:
        return Response({'message': f'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)
