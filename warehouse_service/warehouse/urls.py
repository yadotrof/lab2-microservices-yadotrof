from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^$', views.add_order),
    re_path(r'^(?P<item_uuid>[0-9a-fA-F-]+)$', views.item_detail),
    re_path(r'^(?P<item_uuid>[0-9a-fA-F-]+)/warranty$', views.request_warranty),
]

