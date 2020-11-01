from .models import Warranty
from rest_framework import serializers


class WarrantySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Warranty
        fields = ['item_uuid', 'date', 'status']


class WarrantyRequestSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=255, required=True)
    avaliable_count = serializers.IntegerField(required=True)


class WarrantyDecisionSerializer(serializers.Serializer):
    decision = serializers.CharField(max_length=255, required=True)
    date = serializers.DateTimeField(required=True)
