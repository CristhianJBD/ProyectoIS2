# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.forms import formset_factory, HiddenInput, CheckboxSelectMultiple
from django.forms.extras import SelectDateWidget
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import get_perms
from administracion.forms import AddToSprintForm, AddToSprintFormset, AddSprintBaseForm, MiembrosEquipoFormset, \
    MiembrosEquipoSprintFormset
from administracion.models import Sprint, Proyecto, Actividad, Flujo, MiembroEquipoSprint, Nota
from administracion.views.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin, ActiveProjectRequiredMixin
from django.views import generic
from django.core.urlresolvers import reverse
from administracion.models import UserStory
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string
from django.core.urlresolvers import reverse, reverse_lazy

class SprintList(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.ListView):
    """
    Vista de Listado de Sprint en el sistema
    """
    model = Sprint
    template_name = 'administracion/sprint/sprint_list.html'
    permission_required = 'administracion.ver_proyecto'
    context_object_name = 'sprint'
    project = None

    def get_permission_object(self):
        """
        Obtener el permiso de un objeto
        :param: self
        :return: retorna el objeto proyecto donde se comprueba el permiso
        """
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.project

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param:**kwargs : argumentos clave
        :return: retorna el contexto
        """
        context = super(SprintList, self).get_context_data(**kwargs)
        context['proyecto_perms'] = get_perms(self.request.user, self.project)
        return context

    def get_queryset(self):
        """
        obtiene el projecto correspondiente al seleccionado previamente
        :return: Los objetos Spritn del proyecto previamente seleccionado
        """
        project_pk = self.kwargs['project_pk']
        self.project = get_object_or_404(Proyecto, pk=project_pk)
        return Sprint.objects.filter(proyecto=self.project)

class SprintDetail(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DetailView):
    """
    Vista del detalle de un Sprint en el sistema
    """
    model = Sprint
    permission_required = 'administracion.ver_proyecto'
    template_name = 'administracion/sprint/sprint_detail.html'
    context_object_name = 'sprint'


    def get_permission_object(self):
        """
        Obtener el permiso de un objeto
        :param: self
        :return: retorna el objeto proyecto donde se comprueba el permiso
        """
        return self.get_object().proyecto

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param:**kwargs : argumentos clave
        :return: retorna el contexto
        """
        context = super(SprintDetail, self).get_context_data(**kwargs)
        context['userStory'] = self.object.userstory_set.order_by('-prioridadFormula')
        self.object.sumarHoras()
        self.object.registrarHoras()
        return context



class AddSprintView(ActiveProjectRequiredMixin, LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    Vista para agregar un Sprint en el sistema y añadir este sprint, un desarrollador y una actividad al user Story
    """
    #TODO Mostrar como initial data del formset los US que quedaron del sprint anterior
    model = Sprint
    template_name = 'administracion/sprint/sprint_form.html'
    permission_required = 'administracion.crear_sprint'
    form_class = modelform_factory(Sprint,form=AddSprintBaseForm,
                                   widgets={'fecha_inicio': SelectDateWidget, 'proyecto':HiddenInput},
                                   fields={'nombre', 'fecha_inicio','duracion_sprint','estado', 'proyecto'})
    TeamMemberInlineFormSet = inlineformset_factory(Sprint, MiembroEquipoSprint, formset=MiembrosEquipoSprintFormset, can_delete=True,
                                                    fields=['usuario', 'horasDeTrabajo'],
                                                    extra=1)
    proyecto = None

    def get_proyecto(self):
        return get_object_or_404(Proyecto, id=self.kwargs['project_pk'])

    def get_initial(self):
        """
        Datos iniciales para el formulario
        :return: diccionario de datos
        """
        initial = {'proyecto': self.get_proyecto()}
        return initial

    def get_permission_object(self):
        """
        Obtener el permiso de un objeto
        :param: self
        :return: retorna el objeto proyecto donde se comprueba el permiso
        """
        return get_object_or_404(Proyecto, id=self.kwargs['project_pk'])

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del sprint agregado.
        """
        return reverse('sprint_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        """
        Especifica los datos de contexto a pasar al template
        :param kwargs: Diccionario con parametros con nombres clave
        :return: los datos de contexto
        """
        context= super(AddSprintView,self).get_context_data(**kwargs)

        context['current_action'] = 'Agregar'
        context['formset'] = self.TeamMemberInlineFormSet(self.request.POST if self.request.method == 'POST' else None)
        self.__filtrar_formset__(context['formset'])
        return context

    def __filtrar_formset__(self, formset):
        for userformset in formset.forms:
            userformset.fields['usuario'].queryset = User.objects.filter(miembroequipo__roles__name__exact='Desarrollador', miembroequipo__proyecto=self.get_proyecto())


    def form_valid(self, form):
        """
        Guarda el desarrollador, actividad y sprint asociado al un projecto dentro de un User Story
        :param form: formulario del sprint
        :return: vuelve a la pagina de detalle del sprint o renderea la pagina marcando los errores para volver a enviar sin errores
        """

        self.proyecto = self.get_proyecto()
        self.object= form.save(commit=False)
        self.object.fecha_fin= self.object.fecha_inicio + datetime.timedelta(days=self.object.duracion_sprint)
        self.proyecto.estado = 'EJ'
        self.proyecto.save()
        self.object.save()
        formset = self.TeamMemberInlineFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(self.get_success_url())

        return render(self.request, self.get_template_names(), {'form': form, 'formset': formset},
                      context_instance=RequestContext(self.request))


class UpdateSprintView(ActiveProjectRequiredMixin, LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    Vista para actualizar los datos del Sprint y  del UserStory que son el desarrollador, la actividad y el Sprint
    """
    model = Sprint
    permission_required = 'administracion.editar_sprint'
    template_name = 'administracion/sprint/sprint_form.html'
    form_class = modelform_factory(Sprint,form=AddSprintBaseForm,
                                   widgets={'fecha_inicio': SelectDateWidget,'proyecto': HiddenInput},
                                   fields={'nombre', 'fecha_inicio','duracion_sprint','estado','proyecto'})
    UserStoryFormset = formset_factory(AddToSprintForm, formset=AddToSprintFormset, can_delete=True, extra=1)
    formset = None

    def get_proyecto(self):
        return self.get_object().proyecto

    def get_permission_object(self):
        """
        permiso para add, edit o delete
        :return: los permisos
        """
        return self.get_object().proyecto

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del sprint modificado.
        """
        return reverse('sprint_detail', kwargs={'pk': self.object.id})

    def __filtrar_formset__(self, formset):
            for userformset in formset.forms:
                userformset.fields['desarrollador'].queryset = User.objects.filter(miembroequiposprint__sprint=self.object)
                userformset.fields['flujo'].queryset = Flujo.objects.filter(proyecto=self.get_proyecto())
                userformset.fields['userStory'].queryset = UserStory.objects.filter(Q(proyecto=self.get_proyecto()), Q(estado=0)).order_by('-prioridadFormula')

    def get_context_data(self, **kwargs):
        """
        Especifica los datos de contexto a pasar al template
        :param kwargs: Diccionario con parametros con nombres clave
        :return: los datos de contexto
        """
        context= super(UpdateSprintView,self).get_context_data(**kwargs)
        current_us = self.get_object().userstory_set.all()
        formset= self.UserStoryFormset(self.request.POST if self.request.method == 'POST' else None)
        self.__filtrar_formset__(formset)
        context['current_action'] = 'Editar'
        context['formset'] = formset
        return context

    def form_valid(self, form):
        """
        Guarda el desarrollador, actividad y sprint asociado al un projecto dentro de un User Story
        :param form: formulario del sprint
        :return: vuelve a la pagina de detalle del sprint
        """
        self.object= form.save(commit=False)
        self.object.fecha_fin= self.object.fecha_inicio + datetime.timedelta(days=self.object.duracion_sprint)
        self.object.sumarHoras()
        self.object.registrarHoras()
        self.object.save()
        formsetb= self.UserStoryFormset(self.request.POST)
        if formsetb.is_valid():
            proccessed_forms = []
            for subform in formsetb:
                if subform.has_changed() and 'userStory' in subform.cleaned_data:
                    new_userStory = subform.cleaned_data['userStory']
                    if subform in formsetb.deleted_forms and not new_userStory in proccessed_forms:
                        # desaciamos los user story que se eliminaron del form
                        new_userStory.desarrollador = None
                        new_userStory.sprint = None
                        new_userStory.actividad = None

                    else:
                        new_flujo = subform.cleaned_data['flujo']
                        self.flujo = new_flujo
                        new_desarrollador = subform.cleaned_data['desarrollador']
                        if new_userStory.estado != 3 and new_userStory.estado != 4:  # si el user story no ha finalizado
                            new_userStory.desarrollador = new_desarrollador
                            new_userStory.sprint = self.object
                            new_userStory.actividad = self.flujo.actividad_set.first()
                            new_userStory.estado = 1
                            new_userStory.estado_actividad = 0

                    self.notify(new_userStory)
                    new_userStory.save()
                    proccessed_forms.append(new_userStory)
            return HttpResponseRedirect(self.get_success_url())

        self.__filtrar_formset__(formsetb)

        return render(self.request, self.get_template_names(), {'form': form, 'formset': formsetb},
                      context_instance=RequestContext(self.request))

    def notify(self, userstory):
        proyecto = userstory.proyecto
        subject = 'Asignacion a User Story: {} - {}'.format(userstory, proyecto)
        domain = get_current_site(self.request).domain
        message = render_to_string('administracion/mail/notificacion_asignacion.html',
                                   {'proyecto': proyecto, 'us': userstory, 'domain': domain})
        recipients = [userstory.desarrollador.email]


        send_mail(subject, message, 'proyectois2.2016@gmail.com', recipients, html_message=message)

class DeleteUsSprintView(LoginRequiredMixin, ActiveProjectRequiredMixin, generic.FormView):
    """
    Vista cancelacion de User Stories
    """
    form_class = modelform_factory(Nota, fields=['mensaje'])
    template_name = 'administracion/sprint/userstory_eliminar.html'
    user_story = None

    def get_user_story(self):
        if not self.user_story:
            self.user_story = get_object_or_404(UserStory, pk=self.kwargs['pk'])
        return self.user_story

    def get_proyecto(self):
        return self.get_user_story().proyecto

    def get_context_data(self, **kwargs):
        context = super(DeleteUsSprintView, self).get_context_data(**kwargs)
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
        return super(DeleteUsSprintView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        nota = form.save(commit=False)
        self.get_user_story().estado = 0
        self.get_user_story().desarrollador = None
        self.get_user_story().sprint= None
        self.get_user_story().actividad = None
        self.user_story.save()

        return HttpResponseRedirect(self.get_success_url())