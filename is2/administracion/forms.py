# -*-coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, Permission, User
from guardian.shortcuts import get_perms_for_model
from administracion.models import Proyecto, Sprint, Flujo, Actividad, UserStory
from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
import datetime
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet
from django.utils import timezone


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
    perms_flujo_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Proyecto) if 'flujo' in perm.codename]
    perms_sprint_list = [(perm.codename, perm.name) for perm in get_perms_for_model(Proyecto) if 'sprint' in perm.codename]
    #muestra las opciones a elegir por medio de multiplechoiceField
    perms_proyecto = forms.MultipleChoiceField(perms_proyecto_list, widget=forms.CheckboxSelectMultiple, label=Proyecto._meta.verbose_name_plural.title(), required=False)
    perms_flujo = forms.MultipleChoiceField(perms_flujo_list, widget=forms.CheckboxSelectMultiple, label=Flujo._meta.verbose_name_plural.title(), required=False)
    perms_sprint = forms.MultipleChoiceField(perms_sprint_list, widget=forms.CheckboxSelectMultiple, label=Sprint._meta.verbose_name_plural.title(), required=False)

    class Meta:
        model = Group
        fields = ["name"]

class FlujosCreateForm(forms.ModelForm):
    """
    Formulario para la creacion de flujos
    """
    class Meta:
        model = Flujo
        fields = ['nombre']


#ActividadFormSet utilizamos este form para agregar la actividad al flujo, extra es la cantidad que aparecera en el formulario, can_order es
#para poder ordenar(aun a prueba hasta que le encuentre el uso)
ActividadFormSet = inlineformset_factory(Flujo, Actividad, can_order=True, can_delete=True, max_num=None, extra=1, fields='__all__',)

class AddSprintBaseForm(forms.ModelForm):
    """
    Formulario base para la creacion de Sprints
    """

    class Meta:
        model= Sprint
        fields = ['nombre', 'fecha_inicio', 'proyecto']

    def clean(self):
        """
        Chequea que  las fechas  de los Sprints no se solapen
        """
        if any(self.errors):
            return

        if 'fecha_inicio' and 'proyecto' in self.cleaned_data:
            inicio = self.cleaned_data['fecha_inicio']
            proyecto = self.cleaned_data['proyecto']
            fin = inicio + datetime.timedelta(days=proyecto.duracion_sprint)
            today = timezone.now().date()
            sprint = proyecto.sprint_set.filter(inicio__lte=fin, fin__gte=inicio).exclude(pk=self.instance.pk)
            if (inicio.date() < today) & (inicio != self.instance.inicio):
                raise ValidationError({'fecha_inicio': 'Fecha inicio debe ser mayor o igual a la fecha actual '})
            if sprint.exists():
                raise ValidationError({'fecha_inicio': 'Durante este tiempo existe  ' + str(sprint[0].nombre)})
            if inicio.date() < proyecto.inicio.date():
                raise ValidationError({'fecha_inicio': 'Fecha inicio debe ser mayor o igual a la fecha de inicio del proyecto'})
            if inicio.date() >= proyecto.fin.date():
                raise ValidationError({'fecha_inicio': 'Fecha inicio debe ser menor a la fecha de fin del proyecto'})
            if fin.date() > proyecto.fin.date():
                raise ValidationError({'fecha_inicio': 'Fin del sprint supera la fecha de fin del proyecto'})


class AddToSprintForm(forms.Form):
    """
    formulario para la agregacion de userStory, desarrollador y flujo a un Sprint
    """
    #userStory = forms.ModelChoiceField(queryset=UserStory.objects.all())
    desarrollador = forms.ModelChoiceField(queryset=User.objects.all())
    flujo = forms.ModelChoiceField(queryset=Flujo.objects.all())


class AddToSprintFormset(BaseFormSet):
    def clean(self):
        """
        Chequea que no se incluye el mismo user story más de una vez en el sprint
        """
        if any(self.errors):
            return #si algún form del formset tiene errores, no se hace la validación
'''
        userstories = []
        for form in self.forms:
            if 'userStory' in form.cleaned_data and not form in self.deleted_forms:
                us = form.cleaned_data['userStory']
                if us in userstories:
                    raise forms.ValidationError("Un mismo User Story puede aparecer sólo una vez en el sprint.")
                userstories.append(us)

                userstories.append(us)

'''
class MiembrosEquipoFormset(BaseInlineFormSet):
  def clean(self):
        super(MiembrosEquipoFormset, self).clean()
        for form in self.forms:
            if form in self.deleted_forms:
                usuario = form.cleaned_data['usuario']
                proyecto = form.cleaned_data['proyecto']

class MiembrosEquipoFormset(BaseInlineFormSet):
  def clean(self):
        super(MiembrosEquipoFormset, self).clean()
        for form in self.forms:
            if form in self.deleted_forms:
                usuario = form.cleaned_data['usuario']
                proyecto = form.cleaned_data['proyecto']

class UsuarioFormset(BaseInlineFormSet):
  def clean(self):
        super(UsuarioFormset, self).clean()
        for form in self.forms:
            if form in self.deleted_forms:
                usuario = form.cleaned_data['usuario']

class RegistrarActividadForm(forms.ModelForm):
    '''
    Formulario para registrar actividad en un User Story
    '''
    horas_a_registrar = forms.IntegerField(min_value=0, error_messages={'required':'Ingrese cantidad de horas'}, initial=0)

    class Meta:
        model = UserStory
        fields = ["estado_actividad"]