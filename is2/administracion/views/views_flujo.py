# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.views import generic
from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin
from guardian.shortcuts import get_perms
from administracion.forms import ActividadFormSet, FlujosCreateForm
from administracion.models import Flujo, Proyecto, Sprint, UserStory
from administracion.views.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin, ActiveProjectRequiredMixin


class FlujoList(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.ListView):
    """
    Vista de Listado de Flujos en el sistema de acuerdo a un proyecto
    """
    model = Flujo
    template_name = 'administracion/flujo/flujo_list.html'
    permission_required = 'administracion.ver_proyecto'
    context_object_name = 'flujos'
    project = None

    def get_permission_object(self):
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.project

    def get_context_data(self, **kwargs):

        context = super(FlujoList, self).get_context_data(**kwargs)
        context['proyecto_perms'] = get_perms(self.request.user, self.project)
        return context

    def get_queryset(self):
        if not self.project:
            self.project = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return Flujo.objects.filter(proyecto=self.project)


class FlujoDetail(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DetailView):
    """
    Vista de Detalles de un flujo
    """
    model = Flujo
    template_name = 'administracion/flujo/flujo_detail.html'
    permission_required = 'administracion.ver_proyecto'
    context_object_name = 'flujo'

    def get_permission_object(self):
        '''
        Objeto por el cual comprobar el permiso
        '''
        return self.get_object().proyecto

    def get_context_data(self, **kwargs):
        """
        Agregar lista de actividades al contexto
        :param kwargs: diccionario de argumentos claves
        :return: contexto
        """
        context = super(FlujoDetail, self).get_context_data(**kwargs)
        #actividades[nombre de actividad, contador de us en actividad]
        context['actividades'] = [[a, a.userstory_set.count()]for a in self.object.actividad_set.all()]
        context['act_us'] = [[a, a.userstory_set.order_by('-prioridad')] for a in self.object.actividad_set.all()]
        us = self.object.proyecto.userstory_set.filter(actividad__flujo=self.object) #User Stories del Flujo
        time = us.aggregate(registrado=Sum('tiempo_registrado'), estimado=Sum('tiempo_estimado')) #Aggregate retorna None en vez de 0
        context.update(time)
        return context


class FlujoDetailSprint(FlujoDetail):
    sprint = None

    def get_context_data(self, **kwargs):
        """
        Agregar lista de actividades al contexto
        :param kwargs: diccionario de argumentos claves
        :return: contexto
        """
        self.sprint = get_object_or_404(UserStory, pk=self.kwargs['sprint_pk'])
        context = super(generic.DetailView, self).get_context_data(**kwargs)
        context['actividades'] = [[a, a.userstory_set.filter(sprint=self.sprint).count()] for a in self.object.actividad_set.all()]
        context['sprint'] = self.sprint
        context['act_us'] = [a.userstory_set.filter(sprint=self.sprint).order_by('-prioridad') for a in self.object.actividad_set.all()]
        us = self.object.proyecto.userstory_set.filter(actividad__flujo=self.object, sprint=self.sprint) #User Stories del Flujo
        time = us.aggregate(registrado=Sum('tiempo_registrado'), estimado=Sum('tiempo_estimado'))
        context.update(time)
        return context





class AddFlujo(ActiveProjectRequiredMixin, LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    View que agrega un flujo al sistema
    """
    model = Flujo
    template_name = 'administracion/flujo/flujo_form.html'
    form_class = FlujosCreateForm
    permission_required = 'administracion.crear_flujo'

    def get_proyecto(self):
        if not self.proyecto:
            self.proyecto = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])
        return self.proyecto

    def get_permission_object(self):
        '''
        Objeto por el cual comprobar el permiso
        '''
        return get_object_or_404(Proyecto, id=self.kwargs['project_pk'])

    def get_context_data(self, **kwargs):
        self.proyecto = get_object_or_404(Proyecto, pk=self.kwargs['project_pk'])

        """
        Agregar datos al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(AddFlujo, self).get_context_data(**kwargs)
        context['current_action'] = "Agregar"

        context['actividad_form'] = ActividadFormSet(self.request.POST if self.request.method == 'POST' else None)
        return context

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del flujo agregado.
        """
        return reverse('flujo_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprobar validez del formulario. Crea una instancia de flujo para asociar con la actividad
        :param form: formulario recibido
        :param actividad_form: formulario recibido de actividad
        :return: URL de redireccion
        """
        self.object = form.save(commit=False)
        self.object.proyecto = self.get_proyecto()
        self.object.proyecto.estado = 'EJ'
        self.object.proyecto.save()
        self.object.save()
        actividad_form = ActividadFormSet(self.request.POST, instance=self.object)
        if actividad_form.is_valid():
            actividad_form.save()
            order = [form.instance.id for form in actividad_form.ordered_forms]
            self.object.set_actividad_order(order)

            return HttpResponseRedirect(self.get_success_url())

        return render(self.request, self.get_template_names(), {'form': form,
                                                                     'actividad_form': actividad_form},
                           context_instance=RequestContext(self.request))


class UpdateFlujo(ActiveProjectRequiredMixin, LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    View que agrega un flujo al sistema
    """
    model = Flujo
    template_name = 'administracion/flujo/flujo_form.html'
    form_class = FlujosCreateForm
    permission_required = 'administracion.editar_flujo'

    def get_proyecto(self):
        return self.get_object().proyecto

    def get_permission_object(self):
        return self.get_object().proyecto

    def get_context_data(self, **kwargs):
        """
        Agregar datos al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(UpdateFlujo, self).get_context_data(**kwargs)
        context['current_action'] = "Editar"
        context['actividad_form'] = ActividadFormSet(self.request.POST if self.request.method == 'POST' else None, instance=self.object)

        return context

    def get_success_url(self):
        """
        :return:la url de redireccion a la vista de los detalles del flujo agregado.
        """
        return reverse('flujo_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        """
        Comprobar validez del formulario. Crea una instancia de flujo para asociar con la actividad
        :param form: formulario recibido
        :param actividad_form: formulario recibido de actividad
        :return: URL de redireccion
        """
        self.object = form.save()
        actividad_form = ActividadFormSet(self.request.POST, instance=self.object)
        if actividad_form.is_valid():
            actividad_form.save()
            order = [form.instance.id for form in actividad_form.ordered_forms]
            self.object.set_actividad_order(order)

            return HttpResponseRedirect(self.get_success_url())

        return render(self.request, self.get_template_names(), {'form': form,
                                                                     'actividad_form': actividad_form},
                           context_instance=RequestContext(self.request))


class DeleteFlujo(ActiveProjectRequiredMixin, LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DeleteView):
    """
    Vista de Eliminacion de Flujos
    """
    model = Flujo
    template_name = 'administracion/flujo/flujo_eliminar.html'
    permission_required = 'administracion.eliminar_flujo'
    context_object_name = 'flujo'

    def get_proyecto(self):
        return self.get_object().proyecto

    def get_permission_object(self):
        return self.get_object().proyecto

    def get_success_url(self):
        return reverse_lazy('flujo_list', kwargs={'project_pk': self.get_object().proyecto.id})


