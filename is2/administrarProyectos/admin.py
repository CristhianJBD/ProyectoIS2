from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from administrarProyectos.models import Proyecto, MiembroEquipo

#en linea de administracion django
class MiembrosdeEquipoInLine(admin.TabularInline):
    model = MiembroEquipo
    extra = 0  #0 formularios extras predeterminado

class ProyectoAdmin(GuardedModelAdmin):
    inlines = [MiembrosdeEquipoInLine]

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(MiembroEquipo)


