from django.conf.urls import patterns, url
from administracion.views import views,  view_project


urlpatterns = [
        #url(r'^$', views.user_list, name='user_list'),
        #url(r'^(?P<pk>\d+)$', views.user_detail, name='user_detail'),
        #url(r'^users/add/$', views.user_create, name="user_add"),
        #url(r'^users/(?P<pk>\d+)/delete/$', views.user_delete, name="user_delete"),
        #url(r'^users/(?P<pk>\d+)/edit/$', views.user_edit, name="user_update"),
      url(r'^projects/$', view_project.ProjectList.as_view(), name='project_list'),
      url(r'^projects/add/$', view_project.ProjectCreate.as_view(), name='project_create'),
      url(r'^index/$', views.index, name='index'),
            ]