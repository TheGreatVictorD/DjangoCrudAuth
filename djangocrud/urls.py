"""
Configuración de URLs para el proyecto djangocrud.

La lista `urlpatterns` enruta las URLs a las vistas. Para más información consulta:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Ejemplos:
Vistas basadas en funciones:
    1. Agregar una importación:  from my_app import views
    2. Agregar una URL a urlpatterns:  path('', views.home, name='home')
Vistas basadas en clases:
    1. Agregar una importación:  from other_app.views import Home
    2. Agregar una URL a urlpatterns:  path('', Home.as_view(), name='home')
Incluir otro archivo URLconf:
    1. Importar la función include(): from django.urls import include, path
    2. Agregar una URL a urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views  # Importar las vistas del archivo views.py de la aplicación tasks

urlpatterns = [
    # Ruta para acceder al panel de administración de Django
    path('admin/', admin.site.urls, name='admin'),

    # Ruta para la página de inicio, llama a la vista home
    path('', views.home, name='home'),

    # Ruta para mostrar las tareas pendientes, llama a la vista tasks
    path('tasks/', views.tasks, name='tasks'),

    # Ruta para mostrar las tareas completadas, llama a la vista tasks_completed
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),

    # Ruta para crear una nueva tarea, llama a la vista create_tasks
    path('tasks/create/', views.create_tasks, name='create_task'),

    # Ruta para ver los detalles de una tarea específica, llama a la vista task_detail
    # El parámetro <int:task_id> captura el id de la tarea en la URL
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),

    # Ruta para marcar una tarea como completa o incompleta, llama a la vista complete_task
    # El parámetro <int:task_id> captura el id de la tarea en la URL
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),

    # Ruta para eliminar una tarea específica, llama a la vista delete_task
    # El parámetro <int:task_id> captura el id de la tarea en la URL
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),

    # Ruta para registrar un nuevo usuario, llama a la vista signup
    path('signup/', views.signup, name='signup'),

    # Ruta para iniciar sesión, llama a la vista signin
    path('login/', views.signin, name='login'),

    # Ruta para cerrar sesión, llama a la vista logout_sesion
    path('logout/', views.logout_sesion, name='logout'),
]
