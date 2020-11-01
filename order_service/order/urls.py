from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^(?P<uuid>[0-9a-fA-F-]+)$', views.order_actions),
    re_path(r'^(?P<user_uuid>[0-9a-fA-F-]+)/(?P<order_uuid>[0-9a-fA-F-]+)$', views.order_detail),
    re_path(r'^(?P<order_uuid>[0-9a-fA-F-]+)/warranty$', views.warranty_request),
]

