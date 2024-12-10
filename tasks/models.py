from django.db import models
from django.contrib.auth.models import User


# Definición del modelo Task
class Task(models.Model):
    # Campo para almacenar el título de la tarea, con una longitud máxima de 100 caracteres
    title = models.CharField(max_length=100)

    # Campo opcional (puede estar en blanco) para la descripción de la tarea
    description = models.TextField(blank=True)

    # Campo que almacena la fecha y hora en que se creó la tarea. Se llena automáticamente cuando se crea la tarea
    created = models.DateTimeField(auto_now_add=True)

    # Campo para almacenar la fecha y hora en que la tarea fue completada. Puede estar vacío o nulo
    date_completed = models.DateTimeField(null=True, blank=True)

    # Campo booleano para indicar si la tarea es importante. Por defecto, es `False` (no importante)
    important = models.BooleanField(default=False)

    # Relación con el modelo User (usuarios). Define que cada tarea pertenece a un usuario, y si el usuario se
    # elimina, también se elimina la tarea (on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Método para devolver una representación en string del objeto, mostrando el título y el nombre de usuario que
    # creó la tarea
    def __str__(self):
        return self.title + ' ' + 'by' + ' ' + self.user.username
