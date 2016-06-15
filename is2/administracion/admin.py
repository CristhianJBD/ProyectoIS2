from django.contrib import admin
from guardian.admin import GuardedModelAdmin


from .models import Proyecto, MiembroEquipo, MiembroEquipoSprint,Actividad, Flujo, Sprint, UserStory, Adjunto, Nota
import reversion

# Register your models here.

class MiembroEquipoInLine(admin.TabularInline):
    model = MiembroEquipo
    extra = 0

class MiembroEquipoSprintInLine(admin.TabularInline):
    model = MiembroEquipoSprint
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

class SprintAdmin(GuardedModelAdmin):
    inlines = [MiembroEquipoSprintInLine]

class NotaAdmin(reversion.VersionAdmin):
    pass

#admin.site.register(Usuario)
admin.site.register(UserStory, UserStoryAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(MiembroEquipo)
admin.site.register(MiembroEquipoSprint)
admin.site.register(Flujo, ActividadAdmin)
admin.site.register(Actividad)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(Adjunto)
admin.site.register(Nota, NotaAdmin)
