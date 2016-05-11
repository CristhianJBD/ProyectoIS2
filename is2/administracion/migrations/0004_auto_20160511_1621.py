# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-11 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_auto_20160511_1305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proyecto',
            options={'permissions': (('listar_proyectos', 'Listar todos los proyectos disponibles'), ('listar_proyectos_usuario', 'Listar todos los proyectos de un Usuario'), ('ver_proyecto', 'ver detalles del proyecto'), ('asignar_equipo', 'asignar los miembros del equipo'), ('crear_sprint', 'agregar sprint'), ('editar_sprint', 'editar sprint'), ('eliminar_sprint', 'eliminar sprint'), ('crear_flujo', 'agregar flujo'), ('editar_flujo', 'editar flujo'), ('eliminar_flujo', 'eliminar flujo'))},
        ),
        migrations.AddField(
            model_name='proyecto',
            name='duracion_sprint',
            field=models.PositiveIntegerField(default=30),
        ),
    ]
