#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from guardian.shortcuts import assign_perm, remove_perm, get_perms_for_model,get_perms
from django.core.urlresolvers import reverse_lazy
from django.db.models.signals import m2m_changed


class Proyecto(models.Model):
    """
    Aqui el modelo de proyecto del sistema

    """
    nombre = models.CharField(max_length=40)
    anho= models.IntegerField()
    fechainicio= models.DateTimeField()
    fechafin= models.DateTimeField()
    #cliente= Cliente
    #estado= EstadoProyecto
    #duracionSprint= models.PositiveIntegerField(default=30)
    #flujo= Flujo
    descripcion= models.TextField()
    equipo= models.ManyToManyField(User, through='MiembroEquipo')
    #Los permisos estan asociados al proyecto, los permisos de ABM por defecto
    #son 'add', 'change', 'delete' para difereciarlos con los permisos personalizados
    #se usa 'agregar', 'modificar', 'eliminar' para evitar confusiones
    class Meta:

        permissions = (
            ('listar_todos_los_proyectos', 'listar los proyectos disponibles'),
            ('listar_proyectos_de_usuario','listar los proyectos de un usuario'),
            ('ver_proyecto', 'ver el proyecto'),
            ('aprobar_proyecto', 'aprobar el proyecto'),
            ('asignar_scrum_master', 'asignar scrum master al equipo'),

        )
        #llamando al objeto se mostrara el nombre
    def __unicode__(self):
        return self.nombre


    def get_absolute_url(self):
        return reverse_lazy('administrarProyectos:AdministrarProyectos_detail', args=[self.pk])

    #para corroborar  que la fecha de inicio no sea mayor a la de fecha final
    def clean(self):
        try:
            if self.fechainicio > self.fechafin:
                raise ValidationError({'fechainicio': 'Fecha de inicio no puede ser mayor '
                                                 'que la fecha de final.'})
        except TypeError:
            pass  # si una de las fechas es null, clean_field() se encarga de lanzar error

class MiembroEquipo(models.Model):
    """
    Miembros del equipo encargado de un proyecto especifico
    """
    usuario = models.ForeignKey(User)
    proyecto = models.ForeignKey(Proyecto)
    roles = models.ManyToManyField(Group) #manytomanyfield para que tengan dentro varios valores


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(MiembroEquipo, self).save(force_insert,force_update, using, update_fields)
        #Se agrega el permiso ver_proyecto al usuario
        assign_perm('ver_proyecto',self.usuario, self.proyecto)

    def delete(self, using=None, keep_parents=False):
        for role in self.roles.all():
            for perm in self.role.permissions.all():
                remove_perm(perm.codename, self.usuario, self.proyecto)
        super(MiembroEquipo, self).delete(using)

    class meta(models.Model):
        default_permissions = {}
        verbose_name_plural= 'Miembros Equipo'
        unique_together = {'usuario', 'proyecto'} #en conjunto deben ser unicos

from administrarProyectos.signals import add_permissions_team_member
m2m_changed.connect(add_permissions_team_member, sender=MiembroEquipo.roles.through,
                    dispatch_uid='add_permissions_signal')