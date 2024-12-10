from .models import Task
from django import forms


# Creamos un formulario para el modelo Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Campos que queremos incluir en el formulario
        fields = ['title', 'description', 'important']
        # Los widgets nos permiten personalizar la representación de los campos en HTML
        widgets = {
            # El campo 'title' se representará como un <input type="text"> con clases de Bootstrap y un 'placeholder'
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write a title'}),

            # El campo 'description' se representará como un <textarea> con clases de Bootstrap y un 'placeholder'
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write a description'}),

            # El campo 'important' se representará como un <input type="checkbox"> centrado horizontalmente
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }
