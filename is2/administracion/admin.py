from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Proyecto, MiembroEquipo

# Register your models here.

class MiembroEquipoInLine(admin.TabularInline):
    model = MiembroEquipo
    extra = 0

class ProyectoAdmin(GuardedModelAdmin):
    inlines = [MiembroEquipoInLine]

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(MiembroEquipo)
