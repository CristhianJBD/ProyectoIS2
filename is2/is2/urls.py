from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('autenticacion.urls')),
    url(r'', include('administracion.urls')),

]