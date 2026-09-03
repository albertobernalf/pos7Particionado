from django.db import models
from django.utils.timezone import now


import usuarios

# Create your models here.



class TiposPlanta(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,  default='A', editable=False)

    def __str__(self):
        return self.nombre

#class PerfilesPlanta(models.Model):
#    id=models.AutoField(primary_key=True)
#    sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
#    planta = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
#    tiposPlanta  = models.ForeignKey('planta.TiposPlanta', default=1, on_delete=models.PROTECT, null=True)
#    fechaRegistro = models.DateTimeField(default=now, editable=False)
  #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
#    estadoReg = models.CharField(max_length=1, default='A', editable=False)


#    def __str__(self):
#        return str(self.tiposPlanta)


class Planta(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'), ]

    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True ,  related_name='plid1')
    tiposPlanta = models.ForeignKey('planta.TiposPlanta', default=1, on_delete=models.PROTECT, null=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
    documento = models.CharField( max_length=30)
    nombre = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    genero = models.CharField(max_length=1, default ='L',choices=GENERO_CHOICES,)
    direccion = models.CharField(max_length=50)
    telefono  = models.CharField(max_length=20 , blank=True,  null= True, editable=True)
    celular  = models.CharField(max_length=20 , blank=True,  null= True, editable=True)
    esCajero = models.CharField(max_length=1,blank=True, null= True,  default='N', editable=False)
    correo = models.EmailField(blank=True,null= True)
    imagen = models.ImageField(upload_to="fotos",  blank=True,  null= True, editable=True)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    class Meta:
        unique_together = (('tipoDoc', 'documento','nombre'),)

    def __str__(self):
        #return self.nombre
	    return '%s %s' % (self.nombre , self.sedesClinica)
