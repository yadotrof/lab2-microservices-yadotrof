from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^(?P<item_uuid>[0-9a-fA-F-]+)$', views.warranty_actions),
    re_path(r'^(?P<item_uuid>[0-9a-fA-F-]+)/warranty$', views.request_warranty),
    path('ht/', include('health_check.urls')),
]

