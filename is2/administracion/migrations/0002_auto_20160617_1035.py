# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='mensaje',
            field=models.TextField(help_text=b'Mensaje de descripcion de los avances, motivo de cancelacion o eliminacion', null=True, blank=True),
        ),
    ]
