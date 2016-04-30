# -*-coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission, User
from guardian.shortcuts import get_perms_for_model
from administracion.models import Proyecto
from django import forms
from django.forms.models import BaseInlineFormSet


def __general_perms_list__():
    """
    Devuelve los permisos generales
    :return: lista de permisos que pueden agregarse en general
    """
    permlist= []
    permlist.append(Permission.objects.get(codename="listar_proyectos"))
    permlist.append(Permission.objects.get(codename="listar_proyectos_usuario"))
    permlist.append(Permission.objects.get(codename= "add_proyecto"))
    return permlist

def __user_and_group_permissions__():
    #Querysets, se utiliza para hacer busquedas en cache
    perms_user_list = [(perm.codename, perm.name) for perm in get_perms_for_model((User))]
    perms_group_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Group)]
    perms = []
    #se agrega a perms los permisos asociados a el usuario y al rol
    perms.extend(perms_user_list)
    perms.extend(perms_group_list)
    return perms

class UserCreateForm(UserCreationForm):
    """
    Formulario para creación de usuarios
    """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    general_perms_list = [(perm.codename, perm.name) for perm in __general_perms_list__()]
    general_perms_list.extend(__user_and_group_permissions__())
    general_perms = forms.MultipleChoiceField(general_perms_list, widget=forms.CheckboxSelectMultiple, label="General permissions", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class UserEditForm(UserChangeForm):
    """
    Formulario para edición de usuarios
    """

    general_perms_list = [(perm.codename, perm.name) for perm in __general_perms_list__()]
    general_perms_list.extend(__user_and_group_permissions__())
    general_perms = forms.MultipleChoiceField(general_perms_list, widget=forms.CheckboxSelectMultiple, label="General permissions", required=False)


class RolForm(forms.ModelForm):
    """
    Formulario para el manejo de roles
    """
    perms_proyecto_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Proyecto) if 'proyecto' in perm.codename]

    perms_proyecto = forms.MultipleChoiceField(perms_proyecto_list, widget=forms.CheckboxSelectMultiple, label=Proyecto._meta.verbose_name_plural.title(), required=False)

    class Meta:
        model = Group
        fields = ["name"]

class MiembrosEquipoFormset(BaseInlineFormSet):
  def clean(self):
        super(MiembrosEquipoFormset, self).clean()
        print("En chequeo")
        for form in self.forms:
            if form in self.deleted_forms:
                usuario = form.cleaned_data['usuario']
                proyecto = form.cleaned_data['proyecto']
