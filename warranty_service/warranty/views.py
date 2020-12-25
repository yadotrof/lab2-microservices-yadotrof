import datetime
import pytz

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Warranty
from .serializers import WarrantySerializer
from .serializers import WarrantyRequestSerializer


class WarrantyActions(APIView):
    def get(self, request, item_uuid, format=None):
        """
        Check warranty status.
        """
        object = get_object_or_404(Warranty, item_uuid=item_uuid)
        serializer = WarrantySerializer(object)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, item_uuid, format=None):
        """
        Start warranty
        """
        Warranty.objects.create(comment='',
                                status='ON_WARRANTY',
                                item_uuid=item_uuid)
        return Response({'message': 'Warranty started for item'}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def delete(self, request, item_uuid, format=None):
        """
        Stop warranty
        """
        warranty = get_object_or_404(Warranty, item_uuid=item_uuid)
        warranty.delete()
        return Response({'message': 'Warranty closed for item'}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class RequestWarranty(APIView):
    def post(self, request, item_uuid, format=None):
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
        return Response({'message': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)
