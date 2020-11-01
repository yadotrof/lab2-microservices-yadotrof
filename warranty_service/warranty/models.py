from django.db import models

WARRANTY_STATUS_CHOICES = [
    ('ON_WARRANTY', 'On warranty'),
    ('USE_WARRANTY', 'Use warranty'),
    ('REMOVED_FROM_WARRANTY', 'Removed from warranty')]


class Warranty(models.Model):
    comment = models.TextField()
    status = models.CharField(max_length=25, choices=WARRANTY_STATUS_CHOICES)
    item_uuid = models.UUIDField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
