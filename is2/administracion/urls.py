from django.conf.urls import patterns, url
from administracion.views import views,  view_project


urlpatterns = [
        #url(r'^$', views.user_list, name='user_list'),
        #url(r'^(?P<pk>\d+)$', views.user_detail, name='user_detail'),
        #url(r'^users/add/$', views.user_create, name="user_add"),
        #url(r'^users/(?P<pk>\d+)/delete/$', views.user_delete, name="user_delete"),
        #url(r'^users/(?P<pk>\d+)/edit/$', views.user_edit, name="user_update"),
      url(r'^proyecto/lista$', view_project.ProjectList.as_view(), name='project_list'),
      url(r'^proyecto/agregar/$', view_project.ProjectCreate.as_view(), name='project_create'),
      url(r'^proyecto/$', views.projectPersonal, name='project'),
      url(r'^proyecto/(?P<pk>\d+)/$', view_project.ProjectDetail.as_view(), name='project_detail'),
      url(r'^proyecto/(?P<pk>\d+)/editar/$', view_project.ProjectUpdate.as_view(), name='project_update'),
      url(r'^proyecto/(?P<pk>\d+)/eliminar/$', view_project.ProjectDelete.as_view(), name='project_delete'),
      url(r'^proyecto/(?P<pk>\d+)/aprobar/$', view_project.ApproveProject.as_view(), name='project_aprobar')

            ]