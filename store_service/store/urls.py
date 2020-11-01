from django.urls import path, re_path, include
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/purchase$', views.Purchase.as_view()),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/orders$', views.OrderList.as_view()),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)$', views.OrderDetail.as_view()),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)/warranty$', views.Warranty.as_view()),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)/refund$', views.Refund.as_view()),
    path('openapi', get_schema_view(title="Store service",
                                description="Store service API",
                                version="1.0.0"), name='openapi-schema')
    ]
