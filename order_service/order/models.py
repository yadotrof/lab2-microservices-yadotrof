from django.db import models
from uuid import uuid4


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=False, default='PAID')
    item_uuid = models.UUIDField(default=uuid4, unique=True)
    user_uuid = models.UUIDField(default=uuid4)
