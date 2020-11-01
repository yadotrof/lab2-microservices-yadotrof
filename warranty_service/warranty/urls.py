from django.urls import path, re_path, include
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    re_path(r'^(?P<item_uuid>[0-9a-fA-F-]+)$', views.WarrantyActions.as_view()),
    re_path(r'^(?P<item_uuid>[0-9a-fA-F-]+)/warranty$', views.RequestWarranty.as_view()),
    path('openapi', get_schema_view(title="Warranty service",
                                description="Warranty service API",
                                version="1.0.0"), name='openapi-schema')
]

