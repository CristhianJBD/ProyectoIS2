# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'actividades',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
                ('filename', models.CharField(max_length=100, null=True, editable=False)),
                ('binario', models.BinaryField(null=True, blank=True)),
                ('content_type', models.CharField(max_length=50, null=True, editable=False)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(default=b'misc', max_length=10, choices=[(b'img', b'Imagen'), (b'text', b'Texto'), (b'misc', b'Otro'), (b'src', b'Codigo')])),
                ('lenguaje', models.CharField(max_length=10, null=True, choices=[(b'clike', b'C'), (b'python', b'Python'), (b'ruby', b'Ruby'), (b'css', b'CSS'), (b'php', b'PHP'), (b'scala', b'Scala'), (b'sql', b'SQL'), (b'bash', b'Bash'), (b'javascript', b'JavaScript'), (b'markup', b'Markup')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'flujos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MiembroEquipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'miembros equipo',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MiembroEquipoSprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('horasDeTrabajo', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'miembros equipo sprint',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.TextField(help_text=b'Mensaje de descripcion de los avances, motivo de cancelacion o eliminacion', null=True, blank=True)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('tiempo_registrado', models.IntegerField(default=0)),
                ('horas_a_registrar', models.IntegerField(default=0)),
                ('estado', models.IntegerField(default=0, choices=[(0, b'Inactivo'), (1, b'En curso'), (2, b'Pendiente Aprobacion'), (3, b'Aprobado'), (4, b'Cancelado')])),
                ('estado_actividad', models.IntegerField(null=True, choices=[(0, b'ToDo'), (1, b'Doing'), (2, b'Done')])),
                ('actividad', models.ForeignKey(to='administracion.Actividad', null=True)),
                ('desarrollador', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('estado', models.CharField(default=b'PE', max_length=2, choices=[(b'PL', b'Planificacion'), (b'EJ', b'Ejecutandose'), (b'PE', b'Pendiente'), (b'CA', b'Cancelado'), (b'TE', b'Terminado')])),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('equipo', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='administracion.MiembroEquipo')),
            ],
            options={
                'permissions': (('listar_proyectos', 'Listar Proyectos'), ('ver_proyecto', 'Ver detalles del proyecto'), ('asignar_equipo', 'Asignar los miembros del equipo'), ('aprobar_proyecto', 'Aprobar el proyecto'), ('crear_sprint', 'Agregar Sprint'), ('editar_sprint', 'Editar Sprint'), ('eliminar_sprint', 'Eliminar Sprint'), ('ver_sprint', 'Ver Sprint'), ('crear_flujo', 'Agregar Flujo'), ('editar_flujo', 'Editar Flujo'), ('eliminar_flujo', 'Eliminar Flujo'), ('ver_flujo', 'Ver Flujo'), ('crear_userstory', 'Agregar User Story'), ('editar_userstory', 'Editar User Story'), ('eliminar_userstory', 'Eliminar User Story'), ('registraractividad_userstory', 'Registrar avances en User Story'), ('aprobar_userstory', 'Aprobar User Story completado'), ('cancelar_userstory', 'Cancelar User Story completado'), ('priorizar_userstory', 'asignar prioridad a userstories')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('estado', models.CharField(default=b'PE', max_length=2, choices=[(b'PL', b'Planificacion'), (b'EJ', b'Ejecutandose'), (b'PE', b'Pendiente'), (b'CA', b'Cancelado'), (b'TE', b'Terminado')])),
                ('duracion_sprint', models.PositiveIntegerField(default=30)),
                ('horasRegistradaSprint', models.PositiveIntegerField(default=0)),
                ('horasDuracionSprint', models.PositiveIntegerField(default=0)),
                ('equipo', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='administracion.MiembroEquipoSprint')),
                ('proyecto', models.ForeignKey(to='administracion.Proyecto', blank=True)),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'sprint',
                'verbose_name_plural': 'sprints',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_corto', models.CharField(max_length=20)),
                ('nombre_largo', models.CharField(max_length=80)),
                ('descripcion', models.TextField()),
                ('prioridad', models.IntegerField(default=0, choices=[(0, b'Baja'), (1, b'Media'), (2, b'Alta')])),
                ('valor_negocio', models.IntegerField()),
                ('valor_tecnico', models.IntegerField()),
                ('prioridadFormula', models.FloatField(null=True, blank=True)),
                ('tiempo_estimado', models.PositiveIntegerField()),
                ('tiempo_registrado', models.PositiveIntegerField(default=0)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('estado', models.IntegerField(default=0, choices=[(0, b'Inactivo'), (1, b'En curso'), (2, b'Pendiente Aprobacion'), (3, b'Aprobado'), (4, b'Cancelado')])),
                ('estado_actividad', models.IntegerField(default=0, choices=[(0, b'ToDo'), (1, b'Doing'), (2, b'Done')])),
                ('actividad', models.ForeignKey(blank=True, to='administracion.Actividad', null=True)),
                ('desarrollador', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('proyecto', models.ForeignKey(to='administracion.Proyecto')),
                ('sprint', models.ForeignKey(blank=True, to='administracion.Sprint', null=True)),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'user stories',
                'permissions': (('editar_mi_userstory', 'Editar mis User Stories'), ('registraractividad_mi_userstory', 'Registrar avances en mis User Stories')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nota',
            name='sprint',
            field=models.ForeignKey(to='administracion.Sprint', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nota',
            name='user_story',
            field=models.ForeignKey(to='administracion.UserStory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miembroequiposprint',
            name='sprint',
            field=models.ForeignKey(to='administracion.Sprint'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miembroequiposprint',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='miembroequiposprint',
            unique_together=set([('usuario', 'sprint')]),
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='proyecto',
            field=models.ForeignKey(to='administracion.Proyecto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='roles',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='miembroequipo',
            unique_together=set([('usuario', 'proyecto')]),
        ),
        migrations.AddField(
            model_name='flujo',
            name='proyecto',
            field=models.ForeignKey(blank=True, to='administracion.Proyecto', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adjunto',
            name='user_story',
            field=models.ForeignKey(to='administracion.UserStory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actividad',
            name='flujo',
            field=models.ForeignKey(to='administracion.Flujo'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='actividad',
            order_with_respect_to='flujo',
        ),
    ]
