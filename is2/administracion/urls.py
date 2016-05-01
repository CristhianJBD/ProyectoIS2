from django.conf.urls import url
from administracion.views import views_rol, views_user, view_project, views



urlpatterns = [
      url(r'^users', views_user.UserList.as_view, name='user_list'),
      url(r'^(?P<pk>\d+)$', views_user.UserDetail.as_view, name='user_detail'),
      url(r'^users/add/$', views_user.AddUser.as_view, name="user_add"),
      url(r'^users/(?P<pk>\d+)/delete/$', views_user.DeleteUser.as_view, name="user_delete"),
      url(r'^users/(?P<pk>\d+)/edit/$', views_user.EditUser.as_view, name="user_edit"),
      url(r'^roles/$', views_rol.RolList.as_view(), name='rol_list'),
      url(r'^roles/(?P<pk>\d+)/$', views_rol.RolDetail.as_view(), name='rol_detail'),
      url(r'^roles/add/$', views_rol.AddRol.as_view(), name="rol_add"),
      url(r'^roles/(?P<pk>\d+)/edit/$', views_rol.EditRol.as_view(), name="rol_edit"),
      url(r'^roles/(?P<pk>\d+)/delete/$', views_rol.DeleteRolView.as_view(), name="rol_delete"),
      url(r'^projects/$', view_project.ProjectList.as_view(), name='project_list'),
      url(r'^projects/add/$', view_project.ProjectCreate.as_view(), name='project_create'),

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