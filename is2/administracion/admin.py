from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Proyecto, MiembroEquipo,Actividad, Flujo, Sprint, UserStory, Adjunto
from reversion import revisions as reversion
# Register your models here.

class MiembroEquipoInLine(admin.TabularInline):
    model = MiembroEquipo
    extra = 0

class ProyectoAdmin(GuardedModelAdmin):
    inlines = [MiembroEquipoInLine]

class ActividadInLine(admin.TabularInline):
    model = Actividad
    extra = 0

class ActividadAdmin(GuardedModelAdmin):
    inlines = [ActividadInLine]

class UserStoryAdmin(GuardedModelAdmin):
    pass

#admin.site.register(Usuario)
admin.site.register(UserStory, UserStoryAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(MiembroEquipo)
admin.site.register(Flujo, ActividadAdmin)
admin.site.register(Actividad)
admin.site.register(Sprint)
admin.site.register(Adjunto)