from .models import Order
from rest_framework import serializers


ITEM_SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large')
]


class RequestItemSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=255, required=True)
    size = serializers.ChoiceField(choices=ITEM_SIZE_CHOICES, required=True)


class UsersOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid', 'item_uuid', 'date', 'status']


class WarrantyRequestSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=255, required=True)
