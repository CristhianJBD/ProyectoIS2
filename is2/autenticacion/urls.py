from django.conf.urls import url

from . import views
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^$', views.login_view, name='login_view'),
    url(r'^auth_view/$', views.auth_view, name='auth_view'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout_view'),
    url(r'^index/$', views.index, name='index'),
    url(r'^invalid/$', views.invalid, name='invalid'),


]


