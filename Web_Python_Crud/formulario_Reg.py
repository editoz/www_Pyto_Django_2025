from django import forms
from .models import Persona
from datetime import date

class PersonaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],  # Formato de fecha esperado
    )
    class Meta:
        
        model = Persona
        fields = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'fecha_nacimiento']
        
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones adicionales si lo deseas
        # Ejemplo: validación de fecha de nacimiento
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')
        if fecha_nacimiento:
            if fecha_nacimiento > date.today():
                raise forms.ValidationError("La fecha de nacimiento no puede ser mayor a la fecha actual.")
        
        return cleaned_data