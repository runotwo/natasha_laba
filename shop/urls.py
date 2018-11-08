from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import settings
from .views import index, registration, goods, good_page, cart, order,lout, lin

urlpatterns = [
    path('', index),
    path('cart/', cart),
    path('order/', order),
    path('goods/<id>/', good_page),
    path('goods/', goods),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('registration/', registration),
    path('logout/', lout),
    path('login/', lin),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
