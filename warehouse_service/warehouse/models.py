from uuid import uuid4
from django.db import models

ITEM_SIZE_CHOICES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large')
]

class Item(models.Model):
    available_count = models.PositiveIntegerField(null=False, default=0)
    model = models.CharField(max_length=255, null=False, default='')
    size = models.CharField(choices=ITEM_SIZE_CHOICES, max_length=2)

class OrderItem(models.Model):
    item_uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, null=False)
    canceled = models.BooleanField(default=False)
    order_uuid = models.UUIDField(unique=True)
