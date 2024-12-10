from django.contrib import admin
from .models import Task


# Clase personalizada para la administración de tareas
class TaskAdmin(admin.ModelAdmin):
    # Campos de solo lectura que no podrán ser modificados desde el panel de administración
    readonly_fields = ("created",)


# Registrar el modelo Task junto con su clase personalizada en el admin
admin.site.register(Task, TaskAdmin)
