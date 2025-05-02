
"""
URL configuration for web_python_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Web_Python_Crud import views  # Importar las vistas de la aplicación 'Web_Python_Crud'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="index"),  # Ruta de la vista 'home' de la aplicación 'Web_Python_Crud'
    path('login/', views.home, name="login"),  # Ruta de la vista 'home' de la aplicación 'Web_Python_Crud'
    path('registro/',views.registro, name='registro'), #Ruta de la vista 'registro' de la aplicación 'Web_Python_Crud'   
    path('nosotros/', views.nosotros, name="nosotros"),  # Ruta de la vista 'nosotros' de la aplicación 'Web_Python_Crud'
    path('base/', views.base, name="base"),  # Ruta de la vista 'base' de la aplicación 'Web_Python_Crud'
    path('personas/', views.listar_personas, name='listar_personas'),  # Ruta de la vista 'registro' de la aplicación 'Web_Python_Crud'
    path('persona_registrada/', views.persona_registrada, name='persona_registrada'),  # Ruta de la vista 'persona_registrada' de la aplicación 'Web_Python_Crud'
    path('persona/<int:id>/', views.detalle_persona, name='detalle_persona'),  # Ruta de la vista 'detalle_persona' de la aplicación 'Web_Python_Crud'
]

