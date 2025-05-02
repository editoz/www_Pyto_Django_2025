from django.db import connection
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .formulario_Reg import PersonaForm
from Web_Python_Crud.models import Persona
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'login/login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()  # Obtener el valor del campo username y eliminar espacios
        password = request.POST.get('password', '').strip()  # Obtener el valor del campo password
        
        # Validación de campo 'username'
        if not username:
            # Si el campo username está vacío, redirigir con un mensaje de error
            return render(request, 'index.html', {'username_error': 'Este campo es obligatorio.'})
                
        # Si el campo 'username' está diligenciado, verificamos 'password'
        if not password:
            # Si el campo password está vacío, redirigir con un mensaje de error
            return render(request, 'index.html', {'password_error': 'Este campo es obligatorio.'})
        
        # Aquí iría el código para validar las credenciales del usuario (username y password)
        # Si todo está bien, redirigimos a la página principal o a la vista correspondiente
        return render(request, 'home.html', {'username': username})

    # Si la solicitud no es POST, simplemente renderizamos la página de inicio
    return render(request, 'index.html')

# Vista para la página de registro
def registro (request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva persona en la base de datos
            return redirect('persona_registrada')  # Redirige a alguna página de confirmación
        else:
            print("Error en formulario Registro")
            print(form.errors)
    else:
        form = PersonaForm()

    return render(request, 'registro/registro.html', {'form': form})

# Vista para la página acerca de
def nosotros(request):
    return render(request, 'nosotros/nosotros.html')

# Vista para la página maestra
def base(request):
    return render(request, 'base/base.html')

def registrar_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva persona en la base de datos
            return redirect('persona_registrada')  # Redirige a alguna página de confirmación
    else:
        form = PersonaForm()

    return render(request, 'registro_persona.html', {'form': form})

#Procedimientos almacenados
def registrar_persona_procedimiento(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Aquí puedes llamar al procedimiento almacenado con los datos del formulario
            with connection.cursor() as cursor:
                cursor.callproc('sp_registrar_persona',[
                    data['id'],
                    data['primer nombre'], 
                    data['segundo nombre'], 
                    data['primer apellido'],
                    data['segundo apellido'],
                    data['fecha de nacimiento'],                         
                ])
                
            return redirect('listar_personas')  # Redirige a alguna página de confirmación
            # Si el procedimiento almacenado se ejecuta correctamente, redirige a la página de confirmación
            # Puedes usar el método fetchone() para obtener el resultado del procedimiento almacenado si es necesario
            # resultado = cursor.fetchone()
            # if resultado:
            #     # Manejar el resultado si es necesario
            #     pass
    else:
        form = PersonaForm()
    return render(request,'regitro/registro.html', {'form': form})  # Redirige a alguna página de confirmación

def listar_personas(request):
    with connection.cursor() as cursor:
        # Llamar al procedimiento almacenado para listar personas
        cursor.callproc('sp_listar_personas')
        columnas = [col[0] for col in cursor.description]
        personas = [dict(zip(columnas, row)) for row in cursor.fetchall()]
    return render(request, 'registro/listar_personas.html', {'personas': personas})

def editar_persona(request, id):
    persona_data = None
    with connection.cursor() as cursor:
        # Llamar al procedimiento almacenado para obtener los datos de la persona
        cursor.callproc('sp_obtener_persona', [id])
        row = cursor.fetchone()
        if row:
           persona_data = dict(zip([col[0] for col in cursor.description], row))
    if not persona_data:
        return HttpResponse("Persona no encontrada", status=404)
    
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Aquí puedes llamar al procedimiento almacenado para actualizar la persona
            with connection.cursor() as cursor:
                cursor.callproc('sp_actualizar_persona',[
                    id,
                    data['primer nombre'], 
                    data['segundo nombre'], 
                    data['primer apellido'],
                    data['segundo apellido'],
                    data['fecha de nacimiento'],
                ])
            return redirect('listar_personas')  # Redirige a la página de listado de personas
    else:
        form = PersonaForm(initial=persona_data)
    return render(request, 'registro/editar_persona.html', {'form': form, 'id': id  }) # Redirige a la página de edición de persona

def eliminar_persona(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Llamar al procedimiento almacenado para eliminar la persona
            cursor.callproc('sp_eliminar_persona', [id])
        return redirect('listar_personas')
    return render(request, 'registro/eliminar_persona.html', {'id': id})  # Redirige a la página de confirmación de eliminación
