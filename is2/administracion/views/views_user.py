from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView
from django.views.generic import DetailView
from guardian.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from administracion.forms import UserCreateForm, UserEditForm
from administracion.views.views import CreateViewPermissionRequiredMixin, GlobalPermissionRequiredMixin


class UserList(LoginRequiredMixin, ListView):
    """
    Muestra la lista de usuarios
    """

    model = User
    context_object_name = 'usuario'
    template_name =  'administracion/users/user_list.html'

    def get_queryset(self):
        """
        Muestra la lista de Usuarios
        :return: Lista de usuariios
        """
        return User.objects.exclude(id=-1)

class UserDetail(LoginRequiredMixin,DetailView):
    """
    Ver los detalles de un Usuario
    """
    model = User
    context_object_name = 'usuario'
    template_name = 'administracion/users/user_detail.html'

    def get_context_data(self, **kwargs):
        """
        Muestra los detalles de un Usuario
        :param kwargs: recibe un diccionario de argumentos claves
        :return:el contexto
        """
        context = super(UserDetail, self).get_context_data(**kwargs)
        context['proyectos'] = self.object.miembroequipo_set.all()
        return context

class AddUser(LoginRequiredMixin, CreateViewPermissionRequiredMixin, generic.CreateView):
    """
    Agregar un Usuario al Sistema
    """
    model = User
    form_class = UserCreateForm
    template_name = 'administracion/users/user_form.html'
    permission_required = 'auth.add_user'

    def get_context_data(self, **kwargs):
        context = super(AddUser, self).get_context_data(**kwargs)
        context['current_action'] = 'Agregar'
        return context

    def get_success_url(self):
        """
        Retorno url del usuario
        :return:url del UserDetail
        """
        return reverse('user_detail', kwargs={'pk':self.object.id})

    def form_valid(self, form):
        """
        Verificar la validez del formulario
        :param form: el parametro es el formulario completado
        :return: retorna la url de la lista de usuarios
        """
        super(AddUser, self).form_valid(form)
        seleccionadas = self.request.POST.getlist('general_perms')
        for permname in seleccionadas:
            perm = Permission.objects.get(codename=permname)
            self.object.user_permissions.add(perm)

        return HttpResponseRedirect(self.get_success_url())

class DeleteUser(LoginRequiredMixin, GlobalPermissionRequiredMixin, generic.DeleteView):
    """
    Elimina un Usuario del Sistema
    """
    model = User
    template_name = 'administracion/users/user_delete.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('user_list')
    permission_required = 'auth.delete_user'

    def delete(self, request, *args, **kwargs):
        """
        elimina un usuario del sistema(cambia a estado incativo) y luego se redirige a la url de la lista de ususarios
        :return: retorna la url de la lista de usuarios
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

class EditUser(LoginRequiredMixin,GlobalPermissionRequiredMixin, generic.UpdateView):
    """
    Edita un Usuario del Sistema
    """
    model = User
    template_name = 'administracion/users/user_form.html'
    permission_required = 'auth.change_user'
    form_class = modelform_factory(User, form=UserEditForm,
                                   fields=['first_name', 'last_name', 'email', 'username', 'is_active'], )

    def get_context_data(self, **kwargs):
        context = super(EditUser, self).get_context_data(**kwargs)
        context['current_action'] = 'Editar'
        return context

    def get_success_url(self):
        """
        Se redirige a la url del detalle del usuario
        :return: url de UserDetail
        """
        return reverse('user_detail', kwargs={'pk': self.object.id})

    def get_initial(self):
        """
        Obtener datos iniciales para el formulario
        :return: diccionario con los datos iniciales
        """
        modelo = self.get_object()
        first_name= self.object.first_name
        last_name= self.object.last_name
        email=self.object.email
        username=self.object.username
        password=self.object.password
        perm_list = [perm.codename for perm in list(modelo.user_permissions.all())]

        initial = {'general_perms': perm_list , 'first_name':first_name, 'last_name':last_name, 'email':email, 'username':username, 'password':password}

        return initial


    def form_valid(self, form):
        """
        Comprobar validez del formulario recibido
        :param form: Formulario recibido
           :return: URL de UserDetail
        """
        super(EditUser, self).form_valid(form)
        self.object.user_permissions.clear()
        escogidas = self.request.POST.getlist('general_perms')
        for permname in escogidas:
            perm = Permission.objects.get(codename=permname)
            self.object.user_permissions.add(perm)

        return HttpResponseRedirect(self.get_success_url())



