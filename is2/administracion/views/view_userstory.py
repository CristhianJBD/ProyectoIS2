# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import modelform_factory, inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.views import generic
from django.views.generic import detail
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import get_perms, get_perms_for_model, assign_perm
from guardian.utils import get_403_or_None
from reversion import revisions as reversion
from administracion.forms import RegistrarActividadForm
from administracion.models import UserStory, Proyecto, Actividad
from administracion.views.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin, ActiveProjectRequiredMixin
from django.contrib.sites.shortcuts import get_current_site


class UserStoriesList(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.ListView):
    '''
    Lista de User Stories del proyecto
    '''
    model = UserStory
    template_name = 'administracion/userstory/userstory_list.html'
    permission_required = 'administracion.ver_proyecto'
    context_object_name = 'userstories'
    project = None

    def get_permission_object(self):
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.project

    def get_context_data(self, **kwargs):
        context = super(UserStoriesList, self).get_context_data(**kwargs)
        context['proyecto_perms'] = get_perms(self.request.user, self.project)
        return context

    def get_queryset(self):
        manager = UserStory.objects
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return manager.filter(proyecto=self.project)

class AprobarPendientesUserStories(UserStoriesList):
    """
    Vista que sirve para aprobar user storys pendientes
    """
    permission_required = 'administracion.aprobar_userstory'
    template_name = 'administracion/userstory/userstory_pendiente.html'

    def get_queryset(self):
        manager = UserStory.objects
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return manager.filter(proyecto=self.project, estado=2)

class UserStoryDetail(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DetailView):
    """
    Vista de Detalles de un user story
    """
    model = UserStory
    permission_required = 'administracion.ver_proyecto'
    template_name = 'administracion/userstory/userstory_detail.html'
    context_object_name = 'userstory'

    def get_permission_object(self):
        '''
        Retorna el objeto al cual corresponde el permiso
        '''
        return self.get_object().proyecto

class AddUserStory(ActiveProjectRequiredMixin, LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    View que agrega un user story al sistema
    """
    model = UserStory
    template_name = 'administracion/userstory/userstory_form.html'
    permission_required = 'administracion.crear_userstory'

    def get_context_data(self, **kwargs):
        context = super(AddUserStory, self).get_context_data(**kwargs)

        context['current_action'] = 'Crear'
        return context

    def get_proyecto(self):
        self.proyecto = get_object_or_404(Proyecto, id=self.kwargs['project_pk'])
        return self.proyecto

    def get_form_class(self):
        project = get_object_or_404(Proyecto, id=self.kwargs['project_pk'])
        form_fields = ['nombre_corto','nombre_largo', 'descripcion', 'valor_negocio', 'valor_tecnico', 'tiempo_estimado']
        if 'priorizar_userstory' in get_perms(self.request.user, project):
            form_fields.insert(2, 'prioridad')
        form_class = modelform_factory(UserStory, fields=form_fields)
        return form_class

    def get_permission_object(self):
        '''
        Objeto por el cual comprobar el permiso
        '''
        return self.get_proyecto()

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del user story agregado.
        """
        return reverse('userstory_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprobar validez del formulario.
        :param form: formulario recibido
        :return: URL de redireccion
        """
        self.object = form.save(commit=False)
        self.object.proyecto = self.get_proyecto()
        self.object.proyecto.estado = 'EJ'
        self.object.proyecto.save()
        with transaction.atomic(), reversion.create_revision():
            reversion.set_user(self.request.user)
            reversion.set_comment("Version Inicial")
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())

class UpdateUserStory(ActiveProjectRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    """
    View que actualiza un user story del sistema
    """
    model = UserStory
    template_name = 'administracion/userstory/userstory_form.html'

    def get_proyecto(self):
        return self.get_object().proyecto

    def dispatch(self, request, *args, **kwargs):
        """
        Comprobación de permisos hecha antes de la llamada al dispatch que inicia el proceso de respuesta al request de la url
        :param request: request hecho por el cliente
        :param args: argumentos adicionales posicionales
        :param kwargs: argumentos adicionales en forma de diccionario
        :return: PermissionDenied si el usuario no cuenta con permisos
        """
        if 'editar_userstory' in get_perms(request.user, self.get_object().proyecto):
            return super(UpdateUserStory, self).dispatch(request, *args, **kwargs)
        elif 'editar_mi_userstory' in get_perms(self.request.user, self.get_object()):
            return super(UpdateUserStory, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_form_class(self):
        project = self.get_object().proyecto
        form_fields = ['nombre_corto','nombre_largo', 'descripcion', 'valor_negocio', 'valor_tecnico', 'tiempo_estimado']
        if 'priorizar_userstory' in get_perms(self.request.user, project):
            form_fields.insert(2, 'prioridad')
        form_class = modelform_factory(UserStory, fields=form_fields)
        return form_class

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(UpdateUserStory, self).get_context_data(**kwargs)
        context['current_action'] = "Editar"
        return context

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del user story agregado.
        """
        return reverse('userstory_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprobar validez del formulario. Crea una instancia de user story
        :param form: formulario recibido
        :return: URL de redireccion
        """
    
        if form.has_changed():
            with transaction.atomic(), reversion.create_revision():
                self.object = form.save()
                reversion.set_user(self.request.user)
                reversion.set_comment("Modificacion: {}".format(str.join(', ', form.changed_data)))


        return HttpResponseRedirect(self.get_success_url())



class CancelUserStory(LoginRequiredMixin, ActiveProjectRequiredMixin, generic.FormView):
    """
    Vista cancelacion de User Stories
    """
    form_class = modelform_factory(UserStory, fields=[])
    template_name = 'administracion/userstory/userstory_cancel.html'
    user_story = None

    def get_user_story(self):
        if not self.user_story:
            self.user_story = get_object_or_404(UserStory, pk=self.kwargs['pk'])
        return self.user_story

    def get_proyecto(self):
        return self.get_user_story().proyecto

    def get_context_data(self, **kwargs):
        context = super(CancelUserStory, self).get_context_data(**kwargs)
        context['userstory'] = self.get_user_story()
        return context

    def get_success_url(self):
        return reverse_lazy('product_backlog', kwargs={'project_pk': self.get_proyecto().id})

    def dispatch(self, request, *args, **kwargs):
        """
        Comprobacion de permisos hecha antes de la llamada al dispatch que inicia el proceso de respuesta al request de la url
        :param request: request hecho por el cliente
        :param args: argumentos adicionales posicionales
        :param kwargs: argumentos adicionales en forma de diccionario
        :return: PermissionDenied si el usuario no cuenta con permisos
        """
        return super(CancelUserStory, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save(commit=False)
        self.get_user_story().estado = 4
        self.user_story.save()

        return HttpResponseRedirect(self.get_success_url())


class RegistrarActividadUserStory(ActiveProjectRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    """
    View que permite registrar los cambios aplicados a un user story
    """
    model = UserStory
    template_name = 'administracion/userstory/userstory_registraractividad_form.html'
    error_template = 'administracion/userstory/userstory_error.html'


    def get_proyecto(self):
        return self.get_object().proyecto

    def get_context_data(self, **kwargs):
        context = super(RegistrarActividadUserStory, self).get_context_data(**kwargs)

        return context




    def get_form_class(self):
        """
        Retorna el tipo de formulario que se mostrará en el template. En caso de que
        el usuario cuente con el permiso de editar userstory se le permitirá cambiar la actividad
        del User Story.
        """
        actual_fields = ['estado_actividad']
        if 'editar_userstory' in get_perms(self.request.user, self.get_object().proyecto) or \
                        'editar_mi_userstory' in get_perms(self.request.user, self.get_object()):
            actual_fields.insert(1, 'actividad')
        return modelform_factory(UserStory, form=RegistrarActividadForm, fields=actual_fields)

    def get_form(self, form_class = None):
        '''
        Personalización del form retornado
        '''

        form = super(RegistrarActividadUserStory, self).get_form(form_class)
        if 'actividad' in form.fields:
            form.fields['actividad'].queryset = Actividad.objects.filter(flujo=self.get_object().actividad.flujo)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tiempo_registrado = self.object.tiempo_registrado + form.cleaned_data['horas_a_registrar']
        new_estado = 0
        #movemos el User Story a la sgte actividad en caso de que haya llegado a Done
        if form.cleaned_data['estado_actividad'] == 2:
            new_estado = 0
            try:
                next_actividad = self.object.actividad.get_next_in_order()
            except ObjectDoesNotExist:
                next_actividad = self.object.actividad
                self.object.estado = 2 #Lo marcamos como pendiente de aprobación
                new_estado = 2

            self.object.actividad = next_actividad
            self.object.estado_actividad = new_estado

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class DeleteUserStory(ActiveProjectRequiredMixin, LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DeleteView):
    """
    Vista de Eliminacion de User Stories
    """
    model = UserStory
    template_name = 'administracion/userstory/userstory_delete.html'
    permission_required = 'administracion.eliminar_userstory'
    context_object_name = 'userstory'

    def get_proyecto(self):
        return self.get_object().proyecto
    def get_permission_object(self):
        return self.get_proyecto()

    def get_success_url(self):
        return reverse_lazy('product_backlog', kwargs={'project_pk': self.get_object().proyecto.id})




class AprobarUserStory(ActiveProjectRequiredMixin, LoginRequiredMixin, GlobalPermissionRequiredMixin, SingleObjectTemplateResponseMixin, detail.BaseDetailView):
    """
    Vista de Aprobación de User Story
    """
    model = UserStory
    template_name = 'administracion/userstory/userstory_aprobar.html'
    permission_required = 'administracion.aprobar_userstory'
    context_object_name = 'userstory'

    def get_proyecto(self):
        self.proyecto = self.get_object().proyecto
        return self.proyecto

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.estado == 2:
            return super(AprobarUserStory, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_permission_object(self):
        return self.get_proyecto()

    def get_success_url(self):
        return reverse_lazy('product_backlog', kwargs={'project_pk': self.get_object().proyecto.id})

    def post(self, request, *args, **kwargs):
        us = self.get_object()
        user = self.request.user

        us.estado = 3  # Aprobado
        action = "aprobado"
        # comprobamos si quedan User Stories en el proyecto para marcarlo como completado
        p = us.proyecto
        us_count = p.userstory_set.exclude(estado=4).count()
        approved_us_count = p.userstory_set.filter(estado=3).count()
        approved_us_count += 1  # sumamos el actual que todavia no se ha guardado
        if us_count == approved_us_count:
            p.estado = 'TE'
            p.save()
        us.save()


        return HttpResponseRedirect(self.get_success_url())




class RechazarUserStory(ActiveProjectRequiredMixin, LoginRequiredMixin, generic.UpdateView):
    model = UserStory
    template_name = 'administracion/userstory/userstory_rechazar.html'
    fields = ['actividad', 'estado_actividad']
    permission_required = 'administracion.aprobar_userstory'
    context_object_name = 'userstory'

    def get_proyecto(self):
        return self.get_object().proyecto

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.estado == 2:
            return super(RechazarUserStory, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_form(self):
        '''
        Personalización del form retornado
        '''

        form = super(RechazarUserStory, self).get_form()
        form.fields['actividad'].queryset = Actividad.objects.filter(flujo=self.get_object().actividad.flujo)
        return form

    def get_permission_object(self):
        return self.get_proyecto()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.estado = 1
        self.object.save()
        action = "rechazado"

        return HttpResponseRedirect(self.get_success_url())


class VersionList(LoginRequiredMixin, generic.ListView):
    """
    Vista que devuelve una lista de versiones del User Story deseado.
    """
    context_object_name = 'versions'
    template_name = 'administracion/userstory/version_list_us.html'
    permission_required = ['administracion.editar_userstory', 'administracion.editar_mi_userstory']
    us = None

    def dispatch(self, request, *args, **kwargs):
        """
        Comprobación de permisos hecha antes de la llamada al dispatch que inicia el proceso de respuesta al request de la url
        :param request: request hecho por el cliente
        :param args: argumentos adicionales posicionales
        :param kwargs: argumentos adicionales en forma de diccionario
        :return: PermissionDenied si el usuario no cuenta con permisos
        """
        self.us = get_object_or_404(UserStory, pk=self.kwargs['pk'])
        if 'editar_userstory' in get_perms(request.user, self.us.proyecto):
            return super(VersionList, self).dispatch(request, *args, **kwargs)
        elif 'editar_mi_userstory' in get_perms(self.request.user, self.us):
            return super(VersionList, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    def get_queryset(self):
        """
        Obtiene el user story y sus versiones
        """
        return reversion.get_for_object(self.us)

    def get_context_data(self, **kwargs):
        """
        Agrega el user story al contexto.
        """
        context = super(VersionList, self).get_context_data(**kwargs)
        context['userstory'] = self.us
        return context


class UpdateVersion(UpdateUserStory):
    '''
    Vista que permite revertir un User Story a una version anterior.
    '''
    version = None

    def get_initial(self):
        """
        Obtiene la version deseada del User Story.
        :return: diccionarnio con los datos de la version anterior.
        """
        version_pk = self.kwargs['version_pk']
        self.version = get_object_or_404(reversion.models.Version, pk=version_pk)
        initial = self.version.field_dict
        return initial

    def form_valid(self, form):
        """
        Comprobar validez del formulario. Crea una instancia de user story
        :param form: formulario recibido
        :return: URL de redireccion
        """
        with transaction.atomic(), reversion.create_revision():
            self.object = form.save()
            reversion.set_user(self.request.user)
            # rev = self.version.revision
            reversion.set_comment("Reversion: {}".format(str.join(', ', form.changed_data)))

        return HttpResponseRedirect(self.get_success_url())


