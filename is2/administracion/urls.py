from django.conf.urls import url
from administracion.views import views_rol, views_user, view_project, views, view_userstory



urlpatterns = [
      url(r'^users/$', views_user.UserList.as_view(), name='user_list'),
      url(r'^(?P<pk>\d+)$', views_user.UserDetail.as_view(), name='user_detail'),
      url(r'^users/add/$', views_user.AddUser.as_view(), name="user_add"),
      url(r'^users/(?P<pk>\d+)/delete/$', views_user.DeleteUser.as_view(), name="user_delete"),
      url(r'^users/(?P<pk>\d+)/edit/$', views_user.EditUser.as_view(), name="user_edit"),

      # ESTO DEBO TENER
      # url(r'^roles/$', views_rol.AddRol.rol_index.as_view(), name='rol_index'),
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
      url(r'^proyecto/(?P<pk>\d+)/aprobar/$', view_project.ApproveProject.as_view(), name='project_aprobar'),



       # USER STORY
      url(r'^userstory/(?P<pk>\d+)/$', view_userstory.UserStoryDetail.as_view(), name='userstory_detail'),
      url(r'^proyecto/(?P<project_pk>\d+)/userstories/add/$', view_userstory.AddUserStory.as_view(), name="userstory_add"),
      url(r'^userstory/(?P<pk>\d+)/edit/$', view_userstory.UpdateUserStory.as_view(), name="userstory_update"),
      url(r'^userstory/(?P<pk>\d+)/registrar/$', view_userstory.RegistrarActividadUserStory.as_view(), name="userstory_registraractividad"),
      url(r'^userstory/(?P<pk>\d+)/delete/$', view_userstory.DeleteUserStory.as_view(), name="userstory_delete"),
      url(r'^userstory/(?P<pk>\d+)/aprobar/$', view_userstory.ApproveUserStory.as_view(), name="userstory_aprobar"),
      url(r'^userstory/(?P<pk>\d+)/rechazar/$', view_userstory.RechazarUserStory.as_view(), name="userstory_rechazar"),
      url(r'^userstory/(?P<pk>\d+)/cancelar/$',view_userstory.CancelUserStory.as_view(),name="userstory_cancelar"),
      url(r'^userstory/(?P<pk>\d+)/version/$', view_userstory.VersionList.as_view(), name="version_list"),
      url(r'^userstory/(?P<pk>\d+)/revert/(?P<version_pk>\d+)/$', view_userstory.UpdateVersion.as_view(), name="version_revert"),
      #url(r'^userstory/(?P<pk>\d+)/files/$', view_userstory.FileList.as_view(), name="file_list"),
      #url(r'^userstory/(?P<pk>\d+)/files/upload/$', view_userstory.UploadFileView.as_view(), name="file_upload"),
      #url(r'^file/(?P<pk>\d+)/$', view_userstory.FileDetail.as_view(), name="file_detail"),
      #url(r'^nota/(?P<pk>\d+)/$', view_userstory.NotaDetail.as_view(), name='nota_detail'),
      #url(r'^userstory/(?P<pk>\d+)/notas/$', view_userstory.NotaList.as_view(), name="nota_list"),




            ]