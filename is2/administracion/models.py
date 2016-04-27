from django.db.models.signals import m2m_changed
from guardian.shortcuts import assign_perm, remove_perm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import models
from administracion.signals import add_permissions_team_member
# Create your models here.



class Proyecto(models.Model):
    """
    Modelo de Proyecto del sistema.

    """

    opciones_estado = (('PL', 'Planificacion'), ('EJ', 'Ejecutandose'), ('PE', 'Pendiente'), ('CA', 'Cancelado'), ('TE', 'Terminado'))
    nombre = models.CharField(max_length=40)
    estado = models.CharField(choices=opciones_estado, max_length=2, default='PE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    equipo = models.ManyToManyField(User, through='MiembroEquipo')




    class Meta:
        # Los permisos estan asociados a los proyectos, entonces los permisos de ABM de las entidades
        #dependientes del proyecto, deben crearse como permisos de proyecto, aqui una lista
        #de permisos personalizados
        permissions = (
            ('listar_proyectos', 'Listar todos los proyectos disponibles'),
            ('listar_proyectos_usuario', 'Listar todos los proyectos de un Usuario'),
            ('ver_proyecto', 'ver detalles del proyecto'),
            ('asignar_equipo', 'asignar los miembros del equipo'),
            ('aprobar_proyecto', 'permiso para aprobar el proyecto')

        )

    def __str__(self):
        return self.nombre

    def clean(self):
        #validacion de la fecha de inicio y final del proyecto
        try:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError({'inicio': 'Fecha de inicio no puede ser mayor que la fecha de terminacion.'})
        except TypeError:
            pass  # error si una de las fechas es null



class MiembroEquipo(models.Model):
    """
    Miembros del equipo de un proyecto
    """

    usuario = models.ForeignKey(User)
    proyecto = models.ForeignKey(Proyecto)
    roles = models.ManyToManyField(Group)

    # nota: si se quiere eliminar o guardar se llama al delete o save de cada objeto

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        super(MiembroEquipo, self).save(force_insert, force_update, using, update_fields)
        # Agregamos el permiso view_proyect al usuario
        assign_perm('ver_proyecto', self.usuario, self.proyecto)

    def delete(self, using=None):
        for role in self.roles.all():
            for perm in role.permissions.all():
                remove_perm(perm.codename, self.usuario, self.proyecto)
        super(MiembroEquipo, self).delete(using)

    class Meta:
        default_permissions = ()
        verbose_name_plural = 'miembros equipo'
        unique_together = ('usuario', 'proyecto')

#Aqui se llama al models signals y su metodo add_permissions_team_member
#para que se pueda asignar permisos de algun rol a un usuario de un proyecto

m2m_changed.connect(add_permissions_team_member, sender=MiembroEquipo.roles.through,
                    dispatch_uid='add_permissions_signal')



class Cliente(models.Model):
    """
    Modelo de cliente del sistema
    """
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=50)
    proyecto = models.ForeignKey(Proyecto)

    # nota: si se quiere eliminar o guardar se llama al delete o save de cada objeto

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        super(MiembroEquipo, self).save(force_insert, force_update, using, update_fields)
        # Agregamos el permiso ver_proyecto al usuario
        assign_perm('ver_proyecto', self.usuario, self.proyecto)

    def delete(self, using=None):
        for role in self.roles.all():
            for perm in role.permissions.all():
                remove_perm(perm.codename, self.usuario, self.proyecto)
        super(MiembroEquipo, self).delete(using)


















