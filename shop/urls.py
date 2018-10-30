from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import index, registration

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('registration/', registration)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
