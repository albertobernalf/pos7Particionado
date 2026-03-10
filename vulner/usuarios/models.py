from django.db import models
from django.utils.timezone import now
from smart_selects.db_fields import ChainedForeignKey
from sitios.models import Departamentos, Ciudades
from basicas.models import EstadoCivil


# Create your models here.


class TiposDocumento(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    abreviatura= models.CharField(max_length=2)
    nombre = models.CharField(max_length=50)
    tiposDocCodigoDian = models.CharField(max_length=15, default='')
    tipoDocRips= models.ForeignKey('rips.ripstiposdocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)


    def __str__(self):
        return self.nombre

class TiposUsuario(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)


    def __str__(self):
        return self.nombre

class Usuarios(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'), ]

    id = models.AutoField(primary_key=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #documento =  models.IntegerField(unique=True)
    documento = models.CharField(max_length=30)
    nombre = models.CharField(max_length=80)
    primerNombre = models.CharField(max_length=20,blank=True,null= True)
    segundoNombre = models.CharField(max_length=20,blank=True,null= True)
    primerApellido = models.CharField(max_length=20,blank=True,null= True)
    segundoApellido = models.CharField(max_length=20,blank=True,null= True)
    genero = models.CharField(max_length=1, default ='M',choices=GENERO_CHOICES,)
    centrosC = models.ForeignKey('sitios.Centros', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    tiposUsuario = models.ForeignKey('usuarios.TiposUsuario', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    correo = models.EmailField(blank=True,null= True)
    fechaNacio = models.DateTimeField(default=now,blank=True,null=True, editable=True,)
    pais = models.ForeignKey('sitios.Paises', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True,  on_delete=models.PROTECT)
    municipio = models.ForeignKey('sitios.Municipios', blank=True, null=True, editable=True,  on_delete=models.PROTECT)
    localidad = models.ForeignKey('sitios.Localidades', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    ripsZonaTerritorial = models.ForeignKey('rips.ripsZonaTerritorial', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',  show_all=False)

    direccion = models.CharField(max_length=50)
    telefono  = models.CharField(max_length=20)
    contacto  = models.CharField(max_length=50 ,blank=True,null= True, editable=True,)
    estadoCivil = models.ForeignKey('basicas.EstadoCivil', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ocupacion = models.ForeignKey('basicas.Ocupaciones', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to="fotos",blank=True,null= True, editable=True,)

    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    class Meta:
        unique_together = (('tipoDoc', 'documento'),)

    def __str__(self):
        return self.nombre


class UsuariosContacto(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'), ]
    id = models.AutoField(primary_key=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT ,  related_name='tipoDoc01')
    documento = models.CharField(unique=True,max_length=30)
    nombre = models.CharField(max_length=50)
    genero = models.CharField(max_length=1, default ='L',choices=GENERO_CHOICES,)
    fechaNacio = models.DateTimeField(default=now, blank=True,null= True, editable=True)
    departamentos = models.ForeignKey('sitios.Departamentos', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentos',  show_all=False)
    direccion = models.CharField(max_length=50)
    telefono  = models.CharField(max_length=20)
    correo = models.EmailField()
    #tipoDocPaciente= models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #documentoPaciente = models.ForeignKey('usuarios.Usuarios', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #consecPaciente    = models.IntegerField()
    tiposFamilia= models.ForeignKey('basicas.TiposFamilia', blank=True,null= True, editable=True, on_delete=models.PROTECT)

    tiposContacto = models.ForeignKey('basicas.TiposContacto', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre

