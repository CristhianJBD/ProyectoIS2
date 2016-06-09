# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 15:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'actividades',
            },
        ),
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField()),
                ('filename', models.CharField(editable=False, max_length=100, null=True)),
                ('binario', models.BinaryField(blank=True, null=True)),
                ('content_type', models.CharField(editable=False, max_length=50, null=True)),
                ('creacion', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('img', 'Imagen'), ('text', 'Texto'), ('misc', 'Otro'), ('src', 'Codigo')], default='misc', max_length=10)),
                ('lenguaje', models.CharField(choices=[('clike', 'C'), ('python', 'Python'), ('ruby', 'Ruby'), ('css', 'CSS'), ('php', 'PHP'), ('scala', 'Scala'), ('sql', 'SQL'), ('bash', 'Bash'), ('javascript', 'JavaScript'), ('markup', 'Markup')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'flujos',
            },
        ),
        migrations.CreateModel(
            name='MiembroEquipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horasDeTrabajo', models.PositiveIntegerField(default=0)),
            ],
            options={
                'default_permissions': (),
                'verbose_name_plural': 'miembros equipo',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('estado', models.CharField(choices=[('PL', 'Planificacion'), ('EJ', 'Ejecutandose'), ('PE', 'Pendiente'), ('CA', 'Cancelado'), ('TE', 'Terminado')], default='PE', max_length=2)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('equipo', models.ManyToManyField(through='administracion.MiembroEquipo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('listar_proyectos', 'Listar Proyectos'), ('ver_proyecto', 'Ver detalles del proyecto'), ('asignar_equipo', 'Asignar los miembros del equipo'), ('aprobar_proyecto', 'Aprobar el proyecto'), ('crear_sprint', 'Agregar Sprint'), ('editar_sprint', 'Editar Sprint'), ('eliminar_sprint', 'Eliminar Sprint'), ('ver_sprint', 'Ver Sprint'), ('crear_flujo', 'Agregar Flujo'), ('editar_flujo', 'Editar Flujo'), ('eliminar_flujo', 'Eliminar Flujo'), ('ver_flujo', 'Ver Flujo'), ('crear_userstory', 'Agregar User Story'), ('editar_userstory', 'Editar User Story'), ('eliminar_userstory', 'Eliminar User Story'), ('registraractividad_userstory', 'Registrar avances en User Story'), ('aprobar_userstory', 'Aprobar User Story completado'), ('cancelar_userstory', 'Cancelar User Story completado'), ('priorizar_userstory', 'asignar prioridad a userstories'), ('add_us_sprint', 'Agregar User Story a Sprint')),
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('estado', models.CharField(choices=[('PL', 'Planificacion'), ('EJ', 'Ejecutandose'), ('PE', 'Pendiente'), ('CA', 'Cancelado'), ('TE', 'Terminado')], default='PE', max_length=2)),
                ('duracion_sprint', models.PositiveIntegerField(default=30)),
                ('horasRegistradaSprint', models.PositiveIntegerField(default=0)),
                ('horasDuracionSprint', models.PositiveIntegerField(default=0)),
                ('equipo', models.ManyToManyField(to='administracion.MiembroEquipo')),
                ('proyecto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.Proyecto')),
            ],
            options={
                'verbose_name': 'sprint',
                'default_permissions': (),
                'verbose_name_plural': 'sprints',
            },
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_corto', models.CharField(max_length=20)),
                ('nombre_largo', models.CharField(max_length=80)),
                ('descripcion', models.TextField()),
                ('prioridad', models.IntegerField(choices=[(0, 'Baja'), (1, 'Media'), (2, 'Alta')], default=0)),
                ('valor_negocio', models.IntegerField()),
                ('valor_tecnico', models.IntegerField()),
                ('prioridadFormula', models.FloatField(blank=True, null=True)),
                ('tiempo_estimado', models.PositiveIntegerField()),
                ('tiempo_registrado', models.PositiveIntegerField(default=0)),
                ('ultimo_cambio', models.DateTimeField(auto_now=True)),
                ('estado', models.IntegerField(choices=[(0, 'Inactivo'), (1, 'En curso'), (2, 'Pendiente Aprobacion'), (3, 'Aprobado'), (4, 'Cancelado')], default=0)),
                ('estado_actividad', models.IntegerField(choices=[(0, 'ToDo'), (1, 'Doing'), (2, 'Done')], default=0)),
                ('actividad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.Actividad')),
                ('desarrollador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.Proyecto')),
                ('sprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.Sprint')),
            ],
            options={
                'permissions': (('editar_mi_userstory', 'Editar mis User Stories'), ('registraractividad_mi_userstory', 'Registrar avances en mis User Stories')),
                'default_permissions': (),
                'verbose_name_plural': 'user stories',
            },
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.Proyecto'),
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='roles',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flujo',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.Proyecto'),
        ),
        migrations.AddField(
            model_name='adjunto',
            name='user_story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.UserStory'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='flujo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.Flujo'),
        ),
        migrations.AlterUniqueTogether(
            name='miembroequipo',
            unique_together=set([('usuario', 'proyecto')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='actividad',
            order_with_respect_to='flujo',
        ),
    ]
