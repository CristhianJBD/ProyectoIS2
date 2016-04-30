from django.conf.urls import url
from administracion.views import view_project, views_user, views_rol



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

            ]