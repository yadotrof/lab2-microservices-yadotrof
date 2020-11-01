from django.db import models
from uuid import uuid4


class User(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, null=False, unique=True)
