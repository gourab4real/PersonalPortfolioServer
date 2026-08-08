from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('photoapp/', include('PhotoApp.urls')),
    path('userapp/', include('UserApp.urls')),
]
