from django.db import models
from django.utils.timezone import now


from smart_selects.db_fields import GroupedForeignKey
from smart_selects.db_fields import ChainedForeignKey
#from django.db.models import UniqueConstraint

# Create your models here.




class Departamentos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    departamentoCodigoDian = models.CharField(max_length=15, default ='')
    pais = models.ForeignKey('sitios.Paises', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre

class Ciudades(models.Model):
        ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
        id = models.AutoField(primary_key=True)
        departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name = 'ciudades')
        nombre = models.CharField(max_length=50)
        fechaRegistro = models.DateTimeField(default=now, editable=False)
        estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

        def __str__(self):
            return self.nombre

class SedesClinica(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)

    departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',
                                 show_all=False)
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    contacto = models.CharField(max_length=50)
    nit      = models.CharField(max_length=50  , blank=False,null= False, editable=True, default='0')
    codigoHabilitacion      = models.CharField(max_length=20  , blank=False,null= False, editable=True, default='0')

    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre

class Centros(models.Model):
        ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)
        departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)

        ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',
                                     show_all=False)


        ubicacion = models.CharField(max_length=50, default='')
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=20)
        contacto = models.CharField(max_length=50)
        fechaRegistro = models.DateTimeField(default=now, editable=False)
        estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)


        def __str__(self):
                return self.nombre


class DependenciasTipo(models.Model):
        ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50)
        estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

        def __str__(self):
             return self.nombre

class ServiciosSedes(models.Model):
    ESTADOREG_CHOICES = [
    ('A', 'Activo'),
    ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key= True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    servicios = models.ForeignKey('clinico.Servicios', blank=True,null= True, editable=True,  on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    class Meta:
        #constraints = [
          #  unique_together(fields=['sedesClinica', 'servicios'], name='Constraint_ServiciosSedes')

           unique_together = ('sedesClinica', 'servicios',)

          #  models.db.UniqueConstraint(fields=['sedesClinica', 'servicios'],
           #                         name='Constraint_ServiciosSedes')
        #]



    def __str__(self):
                return self.nombre


class SubServiciosSedes(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key= True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #serviciosSedes = ChainedForeignKey(ServiciosSedes, chained_field='sedesClinica', chained_model_field='sedesClinica',
    #                              show_all=False)
    serviciosSedes = models.ForeignKey('sitios.ServiciosSedes', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    subServiciosSedes = models.CharField(max_length=50, default="")
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    class Meta:
        unique_together = ('sedesClinica', 'serviciosSedes','subServiciosSedes',)
        #constraints = [
         #   models.UniqueConstraint(fields=['sedesClinica', 'servicios','subServicios'], name='Constraint_SubServiciosSedes')
        #]



    def __str__(self):
             return self.nombre


class Dependencias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    DISPONIBILIDAD_CHOICES = [
        ('L', 'LIBRE'),
        ('O', 'OCUPADA'),
	('D', 'DESINFECCION'),  ]

    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    dependenciasTipo= models.ForeignKey('sitios.DependenciasTipo', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    serviciosSedes = models.ForeignKey('sitios.ServiciosSedes', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name ='serviciosSedes1')
    subServiciosSedes = models.ForeignKey('sitios.SubServiciosSedes', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    numero =  models.CharField(max_length=50, default="")
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoDepAct')
    consec = models.IntegerField(blank=True, null=True)
    fechaOcupacion = models.DateTimeField(default=now,blank=True,null= True, editable=True)
    fechaLiberacion = models.DateTimeField(default=now,blank=True,null= True, editable=True)
    disponibilidad = models.CharField(max_length=1, default='L', choices=DISPONIBILIDAD_CHOICES,  )
    #tiposEstancias = models.ForeignKey('tarifarios.TiposEstancias', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    cups = models.ForeignKey('clinico.Examenes', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    class Meta:

    #  unique_together = ('sedesClinica', 'serviciosSedes', 'subServicios','numero','dependenciasTipo')
       unique_together = (('tipoDoc', 'documento','consec','disponibilidad'),)	
       #constraints = [
        #   models.UniqueConstraint(fields=[ 'sedesClinica', 'serviciosSedes','servicios','subServicios','numero','dependenciasTipo'], name='Constraint_dependencias')
       # ]

    def __str__(self):
        return self.nombre


class HistorialDependencias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]



    LIBRE = 'L'
    OCUPADA = 'O'
    TIPO_CHOICES = (
        (LIBRE, 'LIBRE'),
        (OCUPADA, 'OCUPADA'),
    )

    id = models.AutoField(primary_key=True)
    dependencias = models.ForeignKey('sitios.Dependencias', blank=True,null= True, editable=True,  on_delete=models.PROTECT)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True,null= True, editable=True, on_delete=models.PROTECT,
                                  related_name='DocumentohistorialDep')
    consec	= models.IntegerField()
    fechaOcupacion = models.DateTimeField(default=now,blank=True,null= True, editable=True)
    fechaLiberacion = models.DateTimeField(default=now,blank=True,null= True, editable=True)
    disponibilidad = models.CharField(max_length=1, default='L', choices=TIPO_CHOICES, )
    fechaRegistro = models.DateTimeField(default=now, editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)



class Municipios(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    municipioCodigoDian = models.CharField(max_length=15 , default ='')
    departamento = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ripsMunicipios = models.ForeignKey('rips.RipsMunicipios', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre



class Paises(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    paisCodigoDian = models.CharField(max_length=15 , default ='')
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class Localidades(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    localidadCodigoDian = models.CharField(max_length=15 , default ='')
    municipio = models.ForeignKey('sitios.Municipios', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class Ubicaciones(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class ServiciosAdministrativos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ubicaciones = models.ForeignKey('sitios.Ubicaciones', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    dependenciaTipo =  models.ForeignKey('sitios.DependenciasTipo', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return '%s %s' % (self.nombre , self.ubicaciones)


class Bodegas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class Salas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    tipoSala =  models.ForeignKey('sitios.TiposSalas', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    dependenciaTipo =  models.ForeignKey('sitios.DependenciasTipo', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    numero =  models.CharField(max_length=50, default="")
    nombre = models.CharField(max_length=50)
    serviciosAdministrativos = models.ForeignKey('sitios.Serviciosadministrativos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    estadoSala = models.ForeignKey('cirugia.EstadosSalas', blank=True, null=True, editable=True,   on_delete=models.PROTECT) 
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    #iniciaServicio =  models.CharField(max_length=5,blank=True, null=True, )
    #finServicio =  models.CharField(max_length=5,blank=True, null=True, )
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return '%s %s %s' % (self.sedesClinica , self.nombre , self.serviciosAdministrativos)


class TiposSalas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre

class DisponibilidadSalas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    ESTADO_DISPONINILIDAD_CHOICES = [
        ('L', 'Libre'),
        ('O', 'Ocupado'),
        ('M', 'Mantenimiento'), ]
    id = models.AutoField(primary_key=True)
    salas =  models.ForeignKey('sitios.salas', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fecha = models.DateField(default=now, editable=True)
    #año = models.IntegerField(blank=True, null=True)
    #mes= models.IntegerField(blank=True, null=True)
    #dia= models.IntegerField(blank=True, null=True)
    desdeHora =	models.CharField(max_length=5,blank=True, null=True)
    hastaHora = models.CharField(max_length=5,blank=True, null=True)
    estadoDisponibilidad = models.CharField(max_length=1,choices=ESTADO_DISPONINILIDAD_CHOICES, default='A', editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='L', editable=False)

    def __int__(self):
        return self.año
