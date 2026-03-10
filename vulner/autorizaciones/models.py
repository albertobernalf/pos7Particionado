from django.db import models

from django.utils.timezone import now

# Create your models here.

class Autorizaciones(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id           = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'SedesClinica13')
    #tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #documento = models.ForeignKey('usuarios.Usuarios',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Documento7')
    #hClinica = models.CharField(max_length=20,blank=True,null= True, editable=True,)
    #consec    = models.IntegerField()
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm03')
    historia =  models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='Historia476')  
    fechaSolicitud = models.DateTimeField( editable=True, null=True, blank=True)
    empresa = models.ForeignKey('facturacion.Empresas',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='empresa765')
    prioritario = models.CharField(max_length=1,choices= FLAG_CHOICES,blank=True,null= True, editable=True,)
    justificacion =  models.CharField(max_length=5000,blank=True,null= True, editable=True,)
    plantaOrdena = models.ForeignKey('planta.Planta',blank=True,null= True, editable=True, on_delete=models.PROTECT)
    numeroAutorizacion=  models.CharField(max_length=5000,blank=True,null= True, editable=True,)
    fechaAutorizacion = models.DateTimeField( editable=True, null=True, blank=True)
    #plantaAutoriza = models.ForeignKey('planta.Planta',blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name ='Planta1')
    autorizadoPor =  models.CharField(max_length=80,blank=True,null= True, editable=True,)
    observaciones =  models.CharField(max_length=1000,blank=True,null= True, editable=True,)
    estadoAutorizacion = models.ForeignKey('autorizaciones.EstadosAutorizacion',blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fechaModifica = models.DateTimeField( editable=True, null=True, blank=True)
    numeroSolicitud = models.DecimalField(max_digits=6, decimal_places=2 , null=True, blank=True)
    fechaVigencia = models.DateTimeField( editable=True, null=True, blank=True)
    convenio = models.ForeignKey('contratacion.Convenios', blank=True, null=True, editable=True, on_delete=models.PROTECT  , related_name='convenios02271')
    #medicoAutoriza = models.ForeignKey('clinico.Medicos',blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #dxPrinc = models.ForeignKey('clinico.Diagnosticos',blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='dx21' )
    #dxRel1      = models.ForeignKey('clinico.Diagnosticos',blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='dx22' )
    #dxRel2      = models.ForeignKey('clinico.Diagnosticos',blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='dx23' )
    fechaRegistro = models.DateTimeField(default=now, blank=True,null= True, editable=True, )
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True,null=True, editable=True, on_delete=models.PROTECT, related_name ='Planta2')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)


    def __str__(self):
        return str(self.estadoAutorizacion)


class AutorizacionesDetalle(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]

    id           = models.AutoField(primary_key=True)
    #sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'SedesClinica14')
    #tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #documento = models.ForeignKey('usuarios.Usuarios',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Documento8')
    #hClinica = models.CharField(max_length=20,blank=True,null= True, editable=True,)
    #consec    = models.IntegerField()
    autorizaciones = models.ForeignKey('autorizaciones.Autorizaciones',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Documento88')
    #codigoCups =  models.ForeignKey('clinico.TiposExamen',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Documento888')
    numeroAutorizacion=  models.CharField(max_length=5000,blank=True,null= True, editable=True,)
    tiposExamen = models.ForeignKey('clinico.TiposExamen',blank=True,null= True,  default=1, on_delete=models.PROTECT)
    tipoSuministro =   models.ForeignKey('facturacion.TiposSuministro', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    examenes =  models.ForeignKey('clinico.Examenes', blank=True, null=True, on_delete=models.PROTECT,  related_name='Examen829')
    cums =  models.ForeignKey('facturacion.Suministros',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Suminist304')
    #autorizado = models.CharField(max_length=1,blank=True,null= True, editable=True,)
    estadoAutorizacion = models.ForeignKey('autorizaciones.EstadosAutorizacion',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='estAut02')
    cantidadSolicitada = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    cantidadAutorizada =  models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    valorSolicitado = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    valorAutorizado =  models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    historiaMedicamentos = models.ForeignKey('clinico.HistoriaMedicamentos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='AutMed01')
    fechaRegistro = models.DateTimeField(default=now, blank=True,null= True, editable=True, )
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=False,null= False, editable=True, on_delete=models.PROTECT, related_name ='Planta3')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)


    def __str__(self):
        return str(self.numeroAutorizacion)


class AutorizacionesCirugias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id= models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'SedesClinica5')
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Documento9')
    hClinica = models.CharField(max_length=20,blank=True,null= True, editable=True,)
    consec    = models.IntegerField()
    autorizacionesId = models.ForeignKey('autorizaciones.Autorizaciones',blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Documento99')
    fechaRegistro = models.DateTimeField(default=now, blank=True,null= True, editable=True, )
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name ='usuarioRegistroPlanta2')
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __integer__(self):
        return str(self.nombre)

class EstadosAutorizacion(models.Model):
      ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
      id = models.AutoField(primary_key=True)
      nombre = models.CharField(max_length=30, null=False)
      estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

      def __str__(self):
          return str(self.nombre)


