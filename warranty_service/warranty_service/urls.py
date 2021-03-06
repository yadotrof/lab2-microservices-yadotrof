from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/warranty/', include('warranty.urls')),
    path('ht/', include('health_check.urls')),
]
