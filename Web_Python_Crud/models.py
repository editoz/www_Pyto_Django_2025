from django.db import models
from django.forms import ValidationError

# Create your models here.

class Edicion_Libro(models.Model):
    # Considera usar AutoField si no necesitas una clave primaria específica para el libro
    id = models.AutoField(primary_key=True)
    num_edicion = models.CharField(max_length=11, unique=True)  # Número de edición
    is_active = models.BooleanField(default=True)  # Estado de la edición (activo/inactivo)

    class Meta:
        db_table = 'tbl_edicion_libro'  # Nombre de la tabla en la base de datos
        verbose_name = 'Edición de Libro'
        verbose_name_plural = 'Ediciones de Libros'
        ordering = ['-num_edicion']  # Ordenar por número de edición de manera descendente

    def __str__(self):
        return f"Edición {self.num_edicion}"

#-------------------------------------------------------
class Editorial(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, unique=True)
    is_active = models.BooleanField(default=True)  # Usar un campo más semántico

    class Meta:
        db_table = 'tbl_editorial'
        verbose_name = 'Editorial'
        verbose_name_plural = 'Editoriales'

    def __str__(self):
        return self.nombre

#-----------------------------------------------------------
"""class Pais(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)  # Cambié a un nombre más semántico
    idioma = models.ForeignKey('Idioma', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'tbl_pais'
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __str__(self):
        return self.nombre
"""

class Pais(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)  # Solo una vez
    idioma = models.ForeignKey('Idioma', on_delete=models.CASCADE)
    
    indexes = [
            models.Index(fields=['nombre'])
        ]  # Índice en el campo 'nombre' para optimizar consultas

    class Meta:
        db_table = 'tbl_pais'
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        indexes = [
            models.Index(fields=['nombre'])  # Índice en nombre si consultas por este campo
        ]

    def __str__(self):
        return self.nombre



#---------------------------------------------------------
class Libro(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    titulo = models.CharField(max_length=200, unique=True)  # Cambié tit_libro a un nombre más descriptivo
    is_active = models.BooleanField(default=True)  # Estado del libro (activo o inactivo)

    class Meta:
        db_table = 'tbl_libro'
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'
        ordering = ['titulo']  # Orden alfabético por título
        indexes = [
            models.Index(fields=['titulo'])  # Índice en el campo 'titulo'
        ]


    def __str__(self):
        return self.titulo
#-----------------------------------------------------------
"""
class Prestamo(models.Model):
    id_prestamo = models.CharField(max_length=3, primary_key=True)
    fecha_salida_bib = models.DateField()
    fecha_devolucion_bib = models.DateField()
    is_active = models.BooleanField(default=True)
    # Relaciones
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='prestamos')
    roll = models.ForeignKey('Roll', on_delete=models.CASCADE, related_name='prestamos')

    # Estado del préstamo: 0 - Pendiente, 1 - Devolución realizada
    estado_prestamo = models.BooleanField(default=False)  # `False` para pendiente, `True` para devuelto

    class Meta:
        db_table = 'tbl_prestamo'  # Define el nombre de la tabla en la base de datos
        verbose_name = 'Préstamo'  # Nombre en singular en el administrador
        verbose_name_plural = 'Préstamos'  # Nombre en plural en el administrador
        constraints = [
            models.UniqueConstraint(fields=['id_prestamo'], name='unique_prestamo_id')
        ]

    def __str__(self):
        return f"Prestamo {self.id_prestamo} - {self.persona} ({'Devuelto' if self.estado_prestamo else 'Pendiente'})"

"""
class Prestamo(models.Model):
    id_prestamo = models.CharField(max_length=3, primary_key=True)
    fecha_salida_bib = models.DateField()
    fecha_devolucion_bib = models.DateField()
    is_active = models.BooleanField(default=True)
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='prestamos')
    roll = models.ForeignKey('Roll', on_delete=models.CASCADE, related_name='prestamos')
    estado_prestamo = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_prestamo'
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        constraints = [
            models.UniqueConstraint(fields=['id_prestamo'], name='unique_prestamo_id')
        ]
        indexes = [
            models.Index(fields=['estado_prestamo']),  # Agregar índice en estado_prestamo si se consulta frecuentemente
            models.Index(fields=['fecha_salida_bib']),  # Índice en fecha_salida_bib para optimizar consultas por fecha
            models.Index(fields=['fecha_devolucion_bib']),  # Índice en fecha_devolucion_bib para optimizar consultas por fecha
        ]

    def __str__(self):
        return f"Prestamo {self.id_prestamo} - {self.persona} ({'Devuelto' if self.estado_prestamo else 'Pendiente'})"
#-----------------------------------------------------------
"""
class Detalle_Prestamo_Libro(models.Model):
    ESTADO_LIBRO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
        ('dañado', 'Dañado'),
        ('perdido', 'Perdido'),
    ]
    
    id = models.AutoField(primary_key=True)
    prestamo = models.ForeignKey('Prestamo', on_delete=models.CASCADE)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    estado_libro = models.CharField(max_length=20, choices=ESTADO_LIBRO_CHOICES)  # Usamos un campo con opciones
    genero_libro = models.ForeignKey('Genero_Libro', on_delete=models.CASCADE)
    cantidad_libros = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)  # Estado del detalle de préstamo

    class Meta:
        db_table = 'tbl_detall_prest_libro'
        verbose_name = 'Detalle de préstamo de libro'
        verbose_name_plural = 'Detalles de préstamos de libros'
        constraints = [
            models.UniqueConstraint(fields=['prestamo', 'libro'], name='unique_prestamo_libro')
        ]

    def __str__(self):
        return f"Detalle {self.id} - {self.libro.titulo} ({self.estado_libro})"
"""

class Detalle_Prestamo_Libro(models.Model):
    ESTADO_LIBRO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
        ('dañado', 'Dañado'),
        ('perdido', 'Perdido'),
    ]
    
    def clean(self):
        if self.cantidad_libros <= 0:
            raise ValidationError("La cantidad de libros debe ser mayor a cero.")
    
    
    id = models.AutoField(primary_key=True)
    prestamo = models.ForeignKey('Prestamo', on_delete=models.CASCADE)
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    estado_libro = models.CharField(max_length=20, choices=ESTADO_LIBRO_CHOICES)
    genero_libro = models.ForeignKey('Genero_Libro', on_delete=models.CASCADE)
    cantidad_libros = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tbl_detall_prest_libro'
        verbose_name = 'Detalle de préstamo de libro'
        verbose_name_plural = 'Detalles de préstamos de libros'
        constraints = [
            models.UniqueConstraint(fields=['prestamo', 'libro'], name='unique_prestamo_libro')
        ]
        indexes = [
            models.Index(fields=['prestamo', 'libro']),  # Índice compuesto sobre prestamo y libro
        ]

    def __str__(self):
        return f"Detalle {self.id} - {self.libro.titulo} ({self.estado_libro})"



#----------------------------------------------------------
"""
class Usuario(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # Estado del usuario

    class Meta:
        db_table = 'tbl_usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        constraints = [
            models.UniqueConstraint(fields=['username', 'persona'], name='unique_username_persona')  # Índice único
        ]
        
    def __str__(self):
        return f"{self.username} ({self.persona.primer_nombre} {self.persona.segundo_nombre})"
"""
class Usuario(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tbl_usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        constraints = [
            models.UniqueConstraint(fields=['username', 'persona'], name='unique_username_persona')
        ]
        
    def __str__(self):
        return f"{self.username} ({self.persona.primer_nombre} {self.persona.segundo_nombre})"

#-------------------------------------------------------------

class Genero_Persona(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)  # Estado del género de persona

    class Meta:
        db_table = 'tbl_genero_per'
        verbose_name = 'Género de Persona'
        verbose_name_plural = 'Géneros de Persona'

    def __str__(self):
        return self.nombre
#------------------------------------------------------------

class Genero_Libro(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)  # Estado del género de libro

    class Meta:
        db_table = 'tbl_genero_libro'
        verbose_name = 'Género de Libro'
        verbose_name_plural = 'Géneros de Libro'

    def __str__(self):
        return self.nombre

#-------------------------------------------------------------
class Idioma(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)  # Estado del idioma

    class Meta:
        db_table = 'tbl_idioma'
        verbose_name = 'Idioma'
        verbose_name_plural = 'Idiomas'

    def __str__(self):
        return self.nombre
#------------------------------------------------------------

class Persona(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    primer_nombre = models.CharField(max_length=15)
    segundo_nombre = models.CharField(max_length=15, null=True, blank=True)
    primer_apellido = models.CharField(max_length=15)
    segundo_apellido = models.CharField(max_length=15, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    is_active = models.BooleanField(default=True)  # Estado de la persona (activa o no)

    class Meta:
        db_table = 'tbl_persona'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

#-------------------------------------------------------------

class Roll(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=15, unique=True)
    descripcion = models.CharFAield(max_length=50)
    is_active = models.BooleanField(default=True)  # Estado del rol

    class Meta:
        db_table = 'tbl_roll'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre
#------------------------------------------------------------
class Ciudad(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_ciudad'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.nombre

#--------------------------------------------------------------
class Localidad(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_localidad'
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'

    def __str__(self):
        return self.nombre
#----------------------------------------------------------

class Barrio(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    localidad = models.ForeignKey('Localidad', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_barrio'
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'

    def __str__(self):
        return self.nombre
#-----------------------------------------------------------

class Dat_Adic_Editorial(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    web = models.URLField(max_length=255, null=True, blank=True)
    direccion = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    editorial = models.ForeignKey('Editorial', on_delete=models.CASCADE)
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE)
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'tbl_dat_adict_editorial'
        verbose_name = 'Dato Adicional de Editorial'
        verbose_name_plural = 'Datos Adicionales de Editoriales'

    def __str__(self):
        return f"Datos Adicionales de {self.editorial.nombre}"

#-----------------------------------------------------------
"""

class Dat_Adic_Persona(models.Model):
    id_dat_adict_persona = models.CharField(max_length=10, primary_key=True)
    num_via_dir = models.CharField(max_length=10)
    pref_cuad_dir = models.CharField(max_length=10)
    interse_dir = models.CharField(max_length=10)
    num_placa_dir = models.CharField(max_length=10)
    tipo_viv_dir = models.CharField(max_length=15)
    e_mail_persona = models.CharField(max_length=100)
    num_contac_persona = models.CharField(max_length=15)
    pag_web_persona = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Relaciones con otras tablas
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='dat_adict_persona')
    genero_per = models.ForeignKey('Genero_Persona', on_delete=models.CASCADE, related_name='dat_adict_persona')
    roll = models.ForeignKey('Roll', on_delete=models.CASCADE, related_name='dat_adict_persona')
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE, related_name='dat_adict_persona')
    idioma = models.ForeignKey('Idioma', on_delete=models.CASCADE, related_name='dat_adict_persona')
    ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE, related_name='dat_adict_persona')
    localidad = models.ForeignKey('Localidad', on_delete=models.CASCADE, related_name='dat_adict_persona')
    barrio = models.ForeignKey('Barrio', on_delete=models.CASCADE, related_name='dat_adict_persona')
    is_active = models.BooleanField(default=True)
    # Estado de la persona (0 - Inactivo, 1 - Activo)
    # estado_pers = models.BooleanField(default=|True)  # Usar un campo más semántico 
    class Meta:
        
        db_table = 'tbl_dat_adict_persona'  # Define el nombre de la tabla en la base de datos
        verbose_name = 'Datos Adicionales de Persona'
        verbose_name_plural = 'Datos Adicionales de Personas'
        constraints = [
            models.UniqueConstraint(fields=['id_dat_adict_persona', 'persona'], name='unique_dat_adict_persona')
        ]

    def __str__(self):
        return f"Datos Adicionales {self.id_dat_adict_persona} - {self.persona} ({'Activo' if self.estado_pers else 'Inactivo'})"
"""
class Dat_Adic_Persona(models.Model):
    id_dat_adict_persona = models.CharField(max_length=10, primary_key=True)
    num_via_dir = models.CharField(max_length=10)
    pref_cuad_dir = models.CharField(max_length=10)
    interse_dir = models.CharField(max_length=10)
    num_placa_dir = models.CharField(max_length=10)
    tipo_viv_dir = models.CharField(max_length=15)
    e_mail_persona = models.CharField(max_length=100)
    num_contac_persona = models.CharField(max_length=15)
    pag_web_persona = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    FK_genero_per = models.ForeignKey('Genero_Persona', on_delete=models.CASCADE, related_name='dat_adict_persona')
    FK_Pais = models.ForeignKey('Pais', on_delete=models.CASCADE, related_name='dat_adict_persona')
    FK_Ciudad = models.ForeignKey('Ciudad', on_delete=models.CASCADE, related_name='dat_adict_persona')
    FK_Localidad = models.ForeignKey('Localidad', on_delete=models.CASCADE, related_name='dat_adict_persona')
    FK_Barrio = models.ForeignKey('Barrio', on_delete=models.CASCADE, related_name='dat_adict_persona')
    FK_Persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='dat_adict_persona')
    
    # Relaciones adicionales aquí

    class Meta:
        db_table = 'tbl_dat_adict_persona'
        verbose_name = 'Datos Adicionales de Persona'
        verbose_name_plural = 'Datos Adicionales de Personas'
        constraints = [
            models.UniqueConstraint(fields=['id_dat_adict_persona', 'FK_Persona'], name='unique_dat_adict_persona')
        ]
        

    def __str__(self):
        return f"Datos Adicionales {self.id_dat_adict_persona} - {self.Persona}"

#-----------------------------------------------------------

class Dat_Adic_Libro(models.Model):
    id_dat_adict_libro = models.CharField(max_length=16, primary_key=True)
    cantidad_paginas = models.CharField(max_length=10, null=True, blank=True)
    caracteristicas = models.CharField(max_length=255, null=True, blank=True)
    ubicacion = models.CharField(max_length=255, null=True, blank=True)
    estado_libro = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    # Relaciones con otras tablas
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE, related_name='dat_adict_libro')
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE, related_name='dat_adict_libro')
    roll = models.ForeignKey('Roll', on_delete=models.CASCADE, related_name='dat_adict_libro')
    genero_libro = models.ForeignKey('Genero_Libro', on_delete=models.CASCADE, related_name='dat_adict_libro')
    edicion_libro = models.ForeignKey('Edicion_Libro', on_delete=models.CASCADE, related_name='dat_adict_libro')
    editorial = models.ForeignKey('Editorial', on_delete=models.CASCADE, related_name='dat_adict_libro')
    idioma = models.ForeignKey('Idioma', on_delete=models.CASCADE, related_name='dat_adict_libro')
    pais = models.ForeignKey('Pais', on_delete=models.CASCADE, related_name='dat_adict_libro')
    
    # Estado del libro: 0 - Inactivo, 1 - Activo
    estado_dat_adic_libro = models.BooleanField()

    class Meta:
        db_table = 'tbl_dat_adict_libro'  # Define el nombre de la tabla en la base de datos
        verbose_name = 'Datos Adicionales de Libro'
        verbose_name_plural = 'Datos Adicionales de Libros'
        constraints = [
            models.UniqueConstraint(fields=['id_dat_adict_libro', 'libro'], name='unique_dat_adict_libro')
        ]
    
    def __str__(self):
        return f"Datos Adicionales {self.id_dat_adict_libro} - {self.libro}"