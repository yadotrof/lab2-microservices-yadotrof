from django.conf import settings
from celery import shared_task
from .externalcall import external_call, ExternalCallException
import requests
@shared_task(bind=True)
def request_warranty(self, item_uuid, data):
        try:
            res = external_call(requests.post,
                                f'{settings.WARRANTY_URL}api/v1/warranty/{item_uuid}/warranty',
                                data=data)
        except (ExternalCallException) as exc:
            raise self.retry(exc=exc, countdown=30)
