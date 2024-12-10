from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Vista principal que muestra la página de inicio
def home(request):
    return render(request, 'home.html')


# Vista para el registro de usuarios (signup)
def signup(request):
    if request.method == 'GET':
        # Si la petición es GET, se muestra el formulario de registro
        return render(request, 'signup.html', {
            'form': UserCreationForm()  # Instancia del formulario de creación de usuario
        })
    else:
        # Validar que los campos no estén vacíos
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Si algún campo está vacío, se retorna el formulario con un mensaje de error
        if not username or not password1 or not password2:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': 'All fields are required!'  # Mensaje de error para campos vacíos
            })

        # Verificar si las contraseñas coinciden
        if password1 == password2:
            try:
                # Intentar crear el usuario
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)  # Autenticar y loguear al usuario
                return redirect('tasks')  # Redirigir a la vista de tareas
            except IntegrityError:
                # Error cuando el nombre de usuario ya existe
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Username already exists!'  # Mensaje de error cuando el usuario ya existe
                })

        # Si las contraseñas no coinciden, mostrar el formulario con un mensaje de error
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Passwords do not match!'  # Mensaje de error para contraseñas que no coinciden
        })


# Vista para el inicio de sesión (signin)
def signin(request):
    if request.method == 'POST':
        # Obtener los valores enviados en el formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificar si los campos están vacíos
        if not username or not password:
            return render(request, 'login.html', {
                "form": AuthenticationForm(),
                "error": "Both fields are required."  # Mensaje de error para campos vacíos
            })

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        if user is None:
            # Si la autenticación falla, se retorna un mensaje de error
            return render(request, 'login.html', {
                "form": AuthenticationForm(),
                "error": "Username or password is incorrect."  # Error de autenticación fallida
            })

        # Si la autenticación es exitosa, loguear al usuario y redirigir a la vista de tareas
        login(request, user)
        return redirect('tasks')

    else:
        # Si la petición es GET, mostrar el formulario de login
        return render(request, 'login.html', {"form": AuthenticationForm()})


# Vista para cerrar sesión
@login_required
def logout_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('home')  # Redirigir a la página de inicio


# Vista principal de tareas (solo muestra tareas no completadas)
@login_required
def tasks(request):
    # Obtener todas las tareas pendientes (sin completar) del usuario actual
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)

    # Obtener el tipo de toast (mensaje emergente) de la sesión si existe
    toast_type = request.session.pop('toast_type', None)  # Eliminar la variable de sesión después de leerla

    # Renderizar la plantilla con la lista de tareas y el tipo de toast
    return render(request, 'tasks.html', {
        'tasks': tasks,
        'toast_type': toast_type,  # Pasar el tipo de toast a la plantilla
    })


# Vista para mostrar tareas completadas
@login_required
def tasks_completed(request):
    # Obtener todas las tareas completadas del usuario actual, ordenadas por fecha de completado
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')

    # Renderizar la plantilla de tareas completadas
    return render(request, 'tasks_completed.html', {"tasks": tasks})


# Vista para crear una nueva tarea
@login_required
def create_tasks(request):
    if request.method == "POST":
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)  # Crear la tarea sin guardarla aún
            new_task.user = request.user  # Asignar el usuario autenticado a la tarea
            new_task.save()  # Guardar la tarea
            messages.success(request, '🗸 Task created successfully.')  # Mostrar mensaje de éxito
            request.session['toast_type'] = 'create'  # Marcar que se creó una nueva tarea
            return redirect('tasks')
        except ValueError:
            # Si hay algún error en los datos, retornar el formulario con un mensaje de error
            return render(request, 'create_task.html', {'form': TaskForm, 'error': 'Please provide valid data.'})

    # Si es una petición GET, mostrar el formulario vacío para crear la tarea
    return render(request, 'create_task.html', {'form': TaskForm})


# Vista para ver y editar los detalles de una tarea
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Obtener la tarea o retornar error 404 si no existe
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST, instance=task)  # Crear el formulario con los datos de la tarea existente
            form.save()  # Guardar los cambios en la tarea
            messages.success(request, '🗸 Task edited successfully.')  # Mostrar mensaje de éxito
            request.session['toast_type'] = 'edit'  # Marcar que se editó la tarea
            return redirect('tasks')
        except ValueError:
            # Si hay algún error en la edición, retornar el formulario con un mensaje de error
            form = TaskForm(instance=task)
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error updating task."})
    else:
        # Si es una petición GET, mostrar el formulario con los datos de la tarea
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})


# Vista para marcar una tarea como completa o incompleta
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Obtener la tarea o retornar error 404

    if request.method == 'POST':
        if task.date_completed:
            # Si la tarea ya está completada, desmarcarla como incompleta
            task.date_completed = None
            messages.success(request, '🗸 Task marked as incomplete.')  # Mostrar mensaje de tarea desmarcada
            request.session['toast_type'] = 'uncomplete'  # Marcar que se desmarcó la tarea
        else:
            # Si la tarea no está completada, marcarla como completa
            task.date_completed = timezone.now()
            messages.success(request, '🗸 Task marked as complete.')  # Mostrar mensaje de tarea completada
            request.session['toast_type'] = 'complete'  # Marcar que se completó la tarea

        task.save()  # Guardar los cambios
        return redirect('tasks')


# Vista para eliminar una tarea
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Obtener la tarea o retornar error 404
    if request.method == 'POST':
        task.delete()  # Eliminar la tarea
        messages.success(request, '❕ Task deleted successfully.')  # Mostrar mensaje de éxito
        request.session['toast_type'] = 'deleted'  # Marcar que se eliminó la tarea
        return redirect('tasks')
