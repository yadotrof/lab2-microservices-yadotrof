from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/store/', include('store.urls')),
    path('ht/', include('health_check.urls')),
]
