from django.urls import path, re_path
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    re_path(r'^(?P<uuid>[0-9a-fA-F-]+)$', views.OrderActions.as_view(), name='actions'),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)$', views.OrderDetail.as_view(), name='detail'),
    re_path(r'^(?P<order_uuid>[0-9a-fA-F-]+)/warranty$', views.Warranty.as_view(), name='warranty'),
    path('openapi', get_schema_view(title="Order service",
                                    description="Order service API",
                                    version="1.0.0"), name='openapi-schema')
]
