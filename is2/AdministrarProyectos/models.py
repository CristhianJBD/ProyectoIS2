#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


class Proyecto(models.Model):
    """
    Aqui el modelo de proyecto del sistema

    """
    nombre = models.CharField(max_length=40)
    anho= models.IntegerField()
    fechainicio= models.DateTimeField()
    fechafin= models.DateTimeField()
    cliente= Cliente
    estado= EstadoProyecto
    #duracionSprint= models.PositiveIntegerField(default=30)
    #flujo= Flujo
    descripcion= models.TextField()
    equipo= models.ManyToManyField(User, trough='MiembrosdeEquipo')
    #Los permisos estan asociados al proyecto, los permisos de ABM por defecto
    #son 'add', 'change', 'delete' para difereciarlos con los permisos personalizados
    #se usa 'agregar', 'modificar', 'eliminar' para evitar confusiones

    permissions = (
        ('listar_todos_los_proyectos', 'listar los proyectos disponibles'),
        ('listar_proyectos_de_usuario','listar los proyectos de un usuario')
        ('ver_proyecto', 'ver el proyecto'),
        ('aprobar_proyecto', 'aprobar el proyecto'),
        ('asignar_scrum_master', 'asignar scrum master al equipo'),

    )
    def __unicode__(self):
        return self.nombre

    def clean(self):
        try:
            if self.fechainicio > self.fechafin:
                raise ValidationError({'fechainicio': 'Fecha de inicio no puede ser mayor '
                                                 'que la fecha de final.'})
        except TypeError:
            pass  # si una de las fechas es null, clean_field() se encarga de lanzar error


