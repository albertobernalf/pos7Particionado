from django.db import models
from django.utils.timezone import now


from smart_selects.db_fields import GroupedForeignKey
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.


class EstadoCivil(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class Ocupaciones(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class CentrosCosto(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class Eventos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    causasExterna = models.ForeignKey('clinico.CausasExterna', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class TiposFamilia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre

class TiposContacto(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class Periodos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    año  = models.IntegerField()
    mes =  models.IntegerField()
    diaInicial = models.DateField(default=now, editable=True)
    diaFinal   = models.DateField(default=now, editable=True)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class FuripsLista(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False )


    def __str__(self):
        return self.nombre

class FuripsParametro(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    furipsLista =  models.ForeignKey('basicas.FuripsLista', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
        return self.nombre


class Archivos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    TIPO_CHOICES = [
        ('P', 'Plano'),
        ('R', 'Reporte'), ]
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=1, default='P', editable=False ,choices = TIPO_CHOICES)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre

class Parametros(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    parametro1 = models.CharField(max_length=300, blank=True,null= True, editable=True) 
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class TiposProfesional(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre