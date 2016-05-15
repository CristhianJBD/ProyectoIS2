from django.db.models.signals import m2m_changed
from guardian.shortcuts import assign_perm, remove_perm, get_perms_for_model, get_perms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import models
from administracion.signals import add_permissions_team_member
from django.core.urlresolvers import reverse_lazy
# Create your models here.
from base64 import b64encode
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import force_bytes
from reversion import revisions as reversion
from datetime import datetime
from django.db.models import Sum


class Proyecto(models.Model):
    """
    Modelo de Proyecto del sistema.

    """

    opciones_estado = (('PL', 'Planificacion'), ('EJ', 'Ejecutandose'), ('PE', 'Pendiente'), ('CA', 'Cancelado'), ('TE', 'Terminado'))
    nombre = models.CharField(max_length=40)
    estado = models.CharField(choices=opciones_estado, max_length=2, default='PE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(default=datetime.now())
    fecha_fin = models.DateTimeField(default=datetime.now())
    equipo = models.ManyToManyField(User, through='MiembroEquipo')
    duracion_sprint = models.PositiveIntegerField(default=30)




    class Meta:
        # Los permisos estan asociados a los proyectos, entonces los permisos de ABM de las entidades
        #dependientes del proyecto, deben crearse como permisos de proyecto, aqui una lista
        #de permisos personalizados
        permissions = (

            #Permisos especificos del manejo de un proyecto
            ('listar_proyectos', 'Listar Proyectos'),
            ('ver_proyecto', 'Ver detalles del proyecto'),
            ('asignar_equipo', 'Asignar los miembros del equipo'),
            ('aprobar_proyecto', 'Aprobar el proyecto'),
            #permisos especificos para el manejo de sprint dentro del proyecto
            ('crear_sprint', 'Agregar Sprint'),
            ('editar_sprint', 'Editar Sprint'),
            ('eliminar_sprint', 'Eliminar Sprint'),
            ('ver_sprint', 'Ver Sprint'),
            # permisos especificos para el manejo de flujos dentro del proyecto
            ('crear_flujo', 'Agregar Flujo'),
            ('editar_flujo', 'Editar Flujo'),
            ('eliminar_flujo', 'Eliminar Flujo'),
            ('ver_flujo', 'Ver Flujo'),
            # permisos especificos para el manejo de User Storys dentro del proyecto
            ('crear_userstory', 'Agregar User Story'),
            ('editar_userstory', 'Editar User Story'),
            ('eliminar_userstory', 'Eliminar User Story'),
            ('registraractividad_userstory', 'Registrar avances en User Story'),
            ('aprobar_userstory', 'Aprobar User Story completado'),
            ('cancelar_userstory', 'Cancelar User Story completado'),

        )

    def __str__(self):
        return self.nombre

    def clean(self):
        #validacion de la fecha de inicio y final del proyecto
        try:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError({'fecha_inicio': 'Fecha de inicio no puede ser mayor que la fecha de terminacion.'})
        except TypeError:
            pass  # error si una de las fechas es null

    def get_absolute_url(self):
        return reverse_lazy('project_detail', args=[self.pk])

    def get_horas_estimadas(self):
        return self.userstory_set.aggregate(total=Sum('tiempo_estimado'))['total']

    def get_horas_trabajadas(self):
        return self.userstory_set.aggregate(total=Sum('tiempo_registrado'))['total']

    def _get_progreso(self):
        us_total = self.userstory_set.count() - self.userstory_set.filter(estado=4).count()
        us_aprobados = self.userstory_set.filter(estado=3).count()
        progreso = float(us_aprobados) / us_total * 100 if us_total > 0 else 0
        return int(progreso)

    progreso = property(_get_progreso)
'''
class Usuario(models.Model):
    """
    Usuario con roles asociados
    """
    usuario = models.ForeignKey(User)
    roles = models.ManyToManyField(Group)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Usuario, self).save(force_insert, force_update, using, update_fields)



    class Meta:
        default_roles = ()
        verbose_name_plural = 'usuarios'
        unique_together = ('usuario', 'roles')
'''
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
        # Agregamos el permiso ver_proyecto al usuario
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

class Sprint(models.Model):
    """
    Manejo de los sprints del proyecto
    """
    nombre = models.CharField(max_length=20)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    proyecto = models.ForeignKey(Proyecto, null=False, blank=True)



    class Meta:
        default_permissions = ()
        verbose_name = 'sprint'
        verbose_name_plural = 'sprints'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse_lazy('sprint_detail', args=[self.pk])

class Flujo(models.Model):
    """
    Administración de los flujos que forman parte de un proyecto.
    """
    nombre = models.CharField(max_length=20)
    proyecto = models.ForeignKey(Proyecto, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'flujos'
        default_permissions = ()



    def get_absolute_url(self):
        return reverse_lazy('flujo_detail', args=[self.pk])


class Actividad(models.Model):
    """
    Las actividades representan las distintas etapas de las que se componen un flujo
    """
    nombre = models.CharField(max_length=20)
    flujo = models.ForeignKey(Flujo)

    def __str__(self):
        return self.nombre

    class Meta:
        order_with_respect_to = 'flujo'
        verbose_name_plural = 'actividades'






class UserStory(models.Model):
    """
    Manejo de los User Stories. Los User Stories representan a cada
    funcionalidad desde la perspectiva del cliente que debe realizar el sistema.
    """
    estado_actividad_choices = ((0, 'ToDo'), (1, 'Doing'), (2, 'Done'), )
    estado_choices = ((0, 'Inactivo'), (1, 'En curso'), (2, 'Pendiente Aprobacion'), (3, 'Aprobado'), (4,'Cancelado'),)
    #priority_choices = ((0, 'Baja'), (1, 'Media'), (2, 'Alta'))
    nombre_corto = models.CharField(max_length=20)
    nombre_largo = models.CharField(max_length=80)
    descripcion = models.TextField()
    #prioridad = models.IntegerField(choices=priority_choices, default=0)
    valor_negocio = models.IntegerField()
    valor_tecnico = models.IntegerField()
    tiempo_estimado = models.PositiveIntegerField()
    tiempo_registrado = models.PositiveIntegerField(default=0)
    ultimo_cambio = models.DateTimeField(auto_now=True)
    estado = models.IntegerField(choices=estado_choices, default=0)
    estado_actividad = models.IntegerField(choices=estado_actividad_choices, default=0)
    proyecto = models.ForeignKey(Proyecto)
    desarrollador = models.ForeignKey(User, null=True, blank=True)
    sprint = models.ForeignKey(Sprint, null=True, blank=True)
    actividad = models.ForeignKey(Actividad, null=True, blank=True)

    def __unicode__(self):
        return self.nombre

    def _get_progreso(self):
        progreso = float(self.tiempo_registrado) / self.tiempo_estimado * 100
        return int(progreso if progreso <= 100 else 100)
    progreso = property(_get_progreso)


    def get_absolute_url(self):
        return reverse_lazy('userstory_detail', args=[self.pk])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        old_developer = None

        if self.pk is not None:
            old_instance = get_object_or_404(UserStory, pk=self.pk)
            old_developer = old_instance.desarrollador
        super(UserStory, self).save(force_insert, force_update, using, update_fields)
        #borramos los permisos del antiguo desarrollador
        if old_developer:
            for perm in get_perms(old_developer, self):
                remove_perm(perm, old_developer, self)
        #copiamos al user story recién creado los permisos de user story
        if self.proyecto and self.desarrollador:
            membership = get_object_or_404(MiembroEquipo, usuario=self.desarrollador, proyecto=self.proyecto)
            permisos_us = get_perms_for_model(UserStory)
            for rol in membership.roles.all():
                for perm in rol.permissions.all():
                    if perm in permisos_us:
                        assign_perm(perm.codename, self.desarrollador, self)

    class Meta:
        verbose_name_plural = 'user stories'
        default_permissions = ()
        permissions = (
            ('editar_mi_userstory', 'Editar mis User Stories'),
            ('registraractividad_mi_userstory', 'Registrar avances en mis User Stories')

        )

reversion.register(UserStory,fields=['nombre_corto','nombre_largo', 'descripcion', 'valor_negocio', 'valor_tecnico', 'tiempo_estimado'])

#Aqui se llama al models signals y su metodo add_permissions_team_member
#para que se pueda asignar permisos de algun rol a un usuario de un proyecto
m2m_changed.connect(add_permissions_team_member, sender=MiembroEquipo.roles.through,
                    dispatch_uid='add_permissions_signal')



class Adjunto(models.Model):
    """
    Modelo para la administración de archivos adjuntos a un User Story.
    """
    tipo_choices = [('img', 'Imagen'), ('text', 'Texto'), ('misc', 'Otro'), ('src', 'Codigo')]
    lang_choices = [('clike', 'C'), ('python', 'Python'), ('ruby', 'Ruby'), ('css', 'CSS'), ('php', 'PHP'),
                    ('scala', 'Scala'), ('sql', 'SQL'), ('bash', 'Bash'), ('javascript', 'JavaScript'),
                    ('markup', 'Markup')]
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField()
    filename = models.CharField(max_length=100, null=True, editable=False)
    binario = models.BinaryField(null=True, blank=True)
    content_type = models.CharField(null=True, editable=False, max_length=50)
    creacion = models.DateTimeField(auto_now_add=True)
    user_story = models.ForeignKey(UserStory)
    tipo = models.CharField(choices=tipo_choices, default='misc', max_length=10)
    lenguaje = models.CharField(choices=lang_choices, null=True, max_length=10)

    def __unicode__(self):
        return self.nombre

    def img64(self):
        return b64encode(force_bytes(self.binario))

    def get_absolute_url(self):
        return reverse_lazy('project:file_detail', args=[self.pk])

    def get_download_url(self):
        return reverse_lazy('project:download_attachment', args=[self.pk])


















