from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/purchase$', views.purchase),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/orders$', views.order_list),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)$', views.order_detail),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)/warranty$', views.request_warranty),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)/refund$', views.request_refund)
    ]
