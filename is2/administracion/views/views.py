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
from django.core.exceptions import PermissionDenied



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

class ActiveProjectRequiredMixin(object):
    proyecto = None

    def get_proyecto(self):
        return self.proyecto

    def dispatch(self, request, *args, **kwargs):
        proyecto = self.get_proyecto()
        if proyecto.estado != 'AP':
            return super(ActiveProjectRequiredMixin, self).dispatch(request, *args, **kwargs)
        raise PermissionDenied()


def get_selected_perms(POST):
    """
    Obtiene los permisos marcados en el formulario

    :param POST: diccionario con los datos del formulario
    :return: lista de permisos
    """
    current_list = POST.getlist('perms_proyecto')
    current_list.extend(POST.getlist('perms_userstory'))
    current_list.extend(POST.getlist('perms_flujo'))
    current_list.extend(POST.getlist('perms_sprint'))
    return current_list



@login_required()
def projectPersonal(request):

    return render_to_response('administracion/proyecto/project_Personal.html', )


