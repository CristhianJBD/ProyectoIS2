from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views import generic
from guardian.shortcuts import remove_perm, get_perms
from administracion.forms import RolForm
from administracion.views.views import CreateViewPermissionRequiredMixin, get_selected_perms, GlobalPermissionRequiredMixin


class AddRol(LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    Agregar Rol al sistema
    """
    model = Group
    template_name = 'administracion/roles/rol_form.html'
    form_class = RolForm
    permission_required = 'auth.add_group'

    def get_context_data(self, **kwargs):
        """
        Se agregan datos al contexto
        :param kwargs: argumentos claves
        :return: contexto
        """
        context = super(AddRol,self).get_context_data(**kwargs)
        context['current_action'] = "Agregar"
        return context

    def get_success_url(self):
        """
        Se redirije a la url de detalles del rol
        :return: url de rol_detail
        """
        return reverse('rol_detail', kwargs={'pk':self.object.id})
    
    def form_valid(self, form):
        """
        Comprobar validez del formulario
        :param form: formulario recibido
        :return: url de rol_detail
        """
        super(AddRol, self).form_valid(form)
        seleccionadas = get_selected_perms(self.request.POST)
        for permname in seleccionadas:
            perm = Permission.objects.get(codename=permname)
            self.object.permissions.add(perm)
        return HttpResponseRedirect(self.get_success_url())


class EditRol(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    Vista de Actualizacion de Roles
    """
    model = Group
    template_name = 'administracion/roles/rol_form.html'
    form_class = RolForm
    permission_required = 'auth.change_group'

    def get_context_data(self, **kwargs):
        """
        Agregar datos adicionales al contexto
        :param kwargs: argumentos clave
        :return: contexto
        """
        context = super(EditRol, self).get_context_data(**kwargs)
        context['current_action'] = "Editar"
        return context

    def get_success_url(self):
        """
        :return: URL de redireccion correcta a UserDetail
        """
        return reverse('rol_detail', kwargs={'pk': self.object.id})

    def get_initial(self):
        """
        Obtener datos iniciales para el formulario
        :return: diccionario de datos iniciales
        """
        modelo = self.get_object()
        perm_list = [perm.codename for perm in list(modelo.permissions.all())]
        initial = {'perms_proyecto': perm_list}
        return initial


    def form_valid(self, form):
        """
        Comprobar validez del formulario
        :param form: formulario recibido
        :return: URL de redireccion correcta
        """
        super(EditRol, self).form_valid(form)
        # eliminamos permisos anteriores
        self.object.permissions.clear()
        selecionadas = get_selected_perms(self.request.POST)
        for permname in selecionadas:
            perm = Permission.objects.get(codename=permname)
            self.object.permissions.add(perm)
        # actualizamos los permisos de los miembros de equipos que tienen este rol
        team_members_set = self.object.miembroequipo_set.all()
        for team_member in team_members_set:
            user = team_member.usuario
            project = team_member.proyecto
            # borramos todos los permisos que tiene asociado el usuario en el proyecto
            for perm in get_perms(user, project):
                if perm!='ver_proyecto': #cuidamos de no eliminar permiso de ver proyecto
                    remove_perm(perm, user, project)

            all_roles = team_member.roles.all()
            for role in all_roles:
                team_member.roles.remove(role)  #desasociamos al usuario de los demas roles con los que contaba (para que se eliminen los permisos anteriores)
                team_member.roles.add(role)  #volvemos a agregar para que se copien los permisos actualizados
        return HttpResponseRedirect(self.get_success_url())


class DeleteRolView(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DeleteView):
    """
    Vista de Eliminacion de Roles
    """
    model = Group
    template_name = 'administracion/roles/rol_delete.html'
    success_url = reverse_lazy('rol_list')
    permission_required = 'auth.delete_group'

    def delete(self, request, *args, **kwargs):
        '''
        Borrar permisos en miembros que hayan tenido este rol asignado luego de eliminar el rol
        :param request: request del cliente
        :param args: lista de argumentos
        :param kwargs: lista de argumentos con palabras claves
        :return: HttpResponseRedirect a la nueva URL
        '''
        self.object = self.get_object()
        success_url = self.get_success_url()
        miembroequipo_set = self.object.miembroequipo_set

        # actualizamos los permisos de los miembros de equipos que tienen este rol
        team_members_set = miembroequipo_set.all()
        self.object.delete()
        for team_member in team_members_set:
            user = team_member.usuario
            project = team_member.proyecto
            #borramos todos los permisos que tiene asociado el usuario en el proyecto
            for perm in get_perms(user, project):
                if perm != 'ver_proyeto':
                    remove_perm(perm, user, project)


            other_roles = team_member.roles.all()
            for role in other_roles:
                team_member.roles.remove(role)  #desacociamos al usuario de los demas roles con los que contaba (para que se eliminen los permisos anteriores)
                team_member.roles.add(role)  #volvemos a agregar para que se copien los permisos actualizados

        return HttpResponseRedirect(success_url)

class RolList(LoginRequiredMixin, generic.ListView):
    """
    Vista de Listado de Roles
    """
    model = Group
    template_name = 'administracion/roles/rol_list.html'
    context_object_name = 'roles'


class RolDetail(LoginRequiredMixin, generic.DetailView):
    """
    Vista de Detalles de Rol
    """
    model = Group
    template_name = 'administracion/roles/rol_detail.html'
    context_object_name = 'roles'












