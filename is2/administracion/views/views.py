# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from guardian.mixins import PermissionRequiredMixin
from administracion.models import Proyecto
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from administracion.forms import UserCreateForm, UserEditForm



class GlobalPermissionRequiredMixin(PermissionRequiredMixin):
    """
    Mixin que permite requerir un permiso
    """
    accept_global_perms = True
    return_403 = True
    raise_exception = True


class CreateViewPermissionRequiredMixin(GlobalPermissionRequiredMixin):
    """
    Mixin que permite requerir un permiso
    """

    def get_object(self):
        return None

'''
class ActiveProjectRequiredMixin(object):
    proyecto = None

    def get_proyecto(self):
        return self.proyecto

    def dispatch(self, request, *args, **kwargs):
        proyecto = self.get_proyecto()
        if proyecto.estado != 'AP':
            return super(ActiveProjectRequiredMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()
'''
@login_required()

def home(request):
    """
    Vista para la pantalla principal.
    """
    context = {}
    context['users_count'] = User.objects.count()
    context['proyectos'] = Proyecto.objects.all()


    return render(request, 'administracion/home.html', context)


def get_selected_perms(POST):
    """
    Obtiene los permisos marcados en el formulario

    :param POST: diccionario con los datos del formulario
    :return: lista de permisos
    """
    current_list = POST.getlist('perms_proyecto')
    return current_list

@permission_required('auth.add_user')
def user_create(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.set_password(request.POST.get('password'))
            usuario.save()
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render_to_response('users/user_create.html', {'form': form}, context)


@permission_required('auth.delete_user')
def user_delete(request, pk):
    context = RequestContext(request)
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('user_list')
    return render_to_response('users/user_delete.html', {'usuario':usuario}, context)

@permission_required('auth.change_user')
def user_edit(request, pk):
    context = RequestContext(request)
    usuario = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render_to_response('users/user_edit.html', {'form': form}, context)

@login_required()
def user_list(request):
    context = RequestContext(request)
    query = request.GET.get('query','')
    if (query != ''):
        usuarios = User.objects.filter(Q(username__icontains=query) |
                                       Q(first_name__icontains=query) |
                                       Q(last_name__icontains=query))
    else:
        usuarios = User.objects.all()
    return render_to_response('users/user_list.html', { 'usuarios': usuarios, 'query': query}, context)

@login_required()
def user_detail(request, pk):
    context = RequestContext(request)
    usuario = get_object_or_404(User, pk=pk)
    return render_to_response('users/user_detail.html', {'usuario':usuario}, context)

