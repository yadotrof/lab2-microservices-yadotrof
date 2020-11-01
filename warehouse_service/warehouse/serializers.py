from .models import Item, OrderItem
from rest_framework import serializers


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['model', 'size']


ITEM_SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large')
]


class OrderRequestSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=255, required=True)
    size = serializers.ChoiceField(choices=ITEM_SIZE_CHOICES, required=True)
    order_uuid = serializers.UUIDField(required=True)


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order_uuid', 'item_uuid', 'model', 'size']
    model = serializers.SerializerMethodField('get_item_model')
    size = serializers.SerializerMethodField('get_item_size')

    def get_item_model(self, obj):
        return obj.item.model

    def get_item_size(self, obj):
        return obj.item.size


class WarrantyRequestSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=255, required=True)
