from django.conf.urls import url
from administracion.views import views_rol, views_user, view_project, views, views_flujo, view_userstory, views_sprints, views_adjunto, nota_views



urlpatterns = [

      #usuarios
      url(r'^users/$', views_user.UserList.as_view(), name='user_list'),
      url(r'^(?P<pk>\d+)$', views_user.UserDetail.as_view(), name='user_detail'),
      url(r'^users/add/$', views_user.AddUser.as_view(), name="user_add"),
      url(r'^users/(?P<pk>\d+)/delete/$', views_user.DeleteUser.as_view(), name="user_delete"),
      url(r'^users/(?P<pk>\d+)/edit/$', views_user.EditUser.as_view(), name="user_edit"),

      #roles
      # url(r'^roles/$', views_rol.AddRol.rol_index.as_view(), name='rol_index'),
      url(r'^roles/$', views_rol.RolList.as_view(), name='rol_list'),
      url(r'^roles/(?P<pk>\d+)/$', views_rol.RolDetail.as_view(), name='rol_detail'),
      url(r'^roles/add/$', views_rol.AddRol.as_view(), name="rol_add"),
      url(r'^roles/(?P<pk>\d+)/edit/$', views_rol.EditRol.as_view(), name="rol_edit"),
      url(r'^roles/(?P<pk>\d+)/delete/$', views_rol.DeleteRolView.as_view(), name="rol_delete"),




      # proyecto
      url(r'^proyectos/$', view_project.ProjectList.as_view(), name='project_list'),
      url(r'^proyectos/agregar/$', view_project.ProjectCreate.as_view(), name='project_create'),
      url(r'^proyectos/$', views.projectPersonal, name='project'),
      url(r'^proyectos/(?P<pk>\d+)/$', view_project.ProjectDetail.as_view(), name='project_detail'),
      url(r'^proyectos/(?P<pk>\d+)/editar/$', view_project.ProjectUpdate.as_view(), name='project_update'),
      url(r'^proyectos/(?P<pk>\d+)/eliminar/$', view_project.ProjectDelete.as_view(), name='project_delete'),

      # flujos dentro del proyecto
      url(r'^proyectos/(?P<project_pk>\d+)/flujo/add/$', views_flujo.AddFlujo.as_view(), name="flujo_add"),
      url(r'^proyectos/(?P<project_pk>\d+)/flujo/$', views_flujo.FlujoList.as_view(), name='flujo_list'),
      url(r'^flujo/(?P<pk>\d+)/$', views_flujo.FlujoDetail.as_view(), name='flujo_detail'),
      url(r'^flujo/(?P<pk>\d+)/editar/$', views_flujo.UpdateFlujo.as_view(), name="flujo_update"),
      url(r'^flujo/(?P<pk>\d+)/eliminar/$', views_flujo.DeleteFlujo.as_view(), name="flujo_delete"),
      url(r'^flujo/(?P<pk>\d+)/sprint/(?P<sprint_pk>\d+)/$', views_flujo.FlujoDetailSprint.as_view(),name='flujo_detail_sprint'),

      # sprint dentro del proyecto FALTA BURNDOWN
      url(r'^proyectos/(?P<project_pk>\d+)/sprint/$', views_sprints.SprintList.as_view(), name='sprint_list'),
      url(r'^sprint/(?P<pk>\d+)/$', views_sprints.SprintDetail.as_view(), name='sprint_detail'),
      url(r'^proyectos/(?P<project_pk>\d+)/sprint/add/$', views_sprints.AddSprintView.as_view(), name="sprint_add"),
      url(r'^sprint/(?P<pk>\d+)/edit/$', views_sprints.UpdateSprintView.as_view(), name="sprint_update"),
      url(r'^sprint/(?P<pk>\d+)/eliminarus/$', views_sprints.DeleteUsSprintView.as_view(), name="sprint_delete_us"),
      url(r'^sprint/(?P<pk>\d+)/reasignarus/$', views_sprints.Reasignar.as_view(), name="sprint_reasignar_us"),
      #url(r'^sprint/(?P<pk>\d+)/addUS/$', views_sprints.AddUsSprint.as_view(), name="add_US_sprint"),



      #user stories
      url(r'^proyectos/(?P<project_pk>\d+)/userstories/$', view_userstory.UserStoriesList.as_view(), name='product_backlog'),
      url(r'^proyectos/(?P<project_pk>\d+)/userstories/add/$', view_userstory.AddUserStory.as_view(),name="userstory_add"),
      url(r'^userstory/(?P<pk>\d+)/$', view_userstory.UserStoryDetail.as_view(), name='userstory_detail'),
      url(r'^userstory/(?P<pk>\d+)/version/$', view_userstory.VersionList.as_view(), name="version_list"),
      url(r'^userstory/(?P<pk>\d+)/editar/$', view_userstory.UpdateUserStory.as_view(), name="userstory_update"),
      url(r'^userstory/(?P<pk>\d+)/cancelar/$', view_userstory.CancelUserStory.as_view(), name="userstory_cancelar"),
      url(r'^userstory/(?P<pk>\d+)/registrar/$', view_userstory.RegistrarActividadUserStory.as_view(),name="userstory_registraractividad"),
      url(r'^userstory/(?P<pk>\d+)/registrodeactividad/$', nota_views.NotaList.as_view(),name="userstory_registrodeactividad"),
      url(r'^nota/(?P<pk>\d+)/$', nota_views.NotaDetail.as_view(), name='nota_detail'),
      url(r'^userstory/(?P<pk>\d+)/eliminardesprint/$', views_sprints.DeleteUsSprintView.as_view(), name="userstory_delete"),


      # adjunto
      url(r'^adjuntoarchivo/(?P<pk>\d+)/$', views_adjunto.download_attachment, name='download_attachment'),
      url(r'^userstory/(?P<pk>\d+)/archivos/$', views_adjunto.FileList.as_view(), name="file_list"),
      url(r'^userstory/(?P<pk>\d+)/archivos/subir/$', views_adjunto.UploadFileView.as_view(), name="file_upload"),
      url(r'^archivo/(?P<pk>\d+)/$', views_adjunto.FileDetail.as_view(), name="file_detail"),

      #no visto aun

      url(r'^userstory/(?P<pk>\d+)/aprobar/$', view_userstory.AprobarUserStory.as_view(), name="userstory_aprobar"),
      url(r'^userstory/(?P<pk>\d+)/rechazar/$', view_userstory.RechazarUserStory.as_view(), name="userstory_rechazar"),
      url(r'^proyectos/(?P<project_pk>\d+)/userstories/pendientes/$',view_userstory.AprobarPendientesUserStories.as_view(), name='pendientes_userstories'),

      url(r'^userstory/(?P<pk>\d+)/revert/(?P<version_pk>\d+)/$', view_userstory.UpdateVersion.as_view(), name="version_revert"),

]