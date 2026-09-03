from django.db import models
from django.utils.timezone import now
from smart_selects.db_fields import GroupedForeignKey

#from tarifas.models import Tarifas


# Create your models here.





class Convenios (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm315')
    tarifariosDescripcionProc = models.ForeignKey('tarifarios.TarifariosDescripcion', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TarifariosDescripcion0121')
    tarifariosDescripcionSum = models.ForeignKey('tarifarios.TarifariosDescripcion', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TarifariosDescripcion0123')
    tarifariosDescripcionHono = models.ForeignKey('tarifarios.TarifariosDescripcionHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TarifariosDescripcionHonor0124')
    nombre = models.CharField(max_length=80, blank=True,null= True, editable=True)
    descripcion = models.CharField(max_length=80, blank=True,null= True, editable=True)
    empresa =  models.ForeignKey('facturacion.Empresas', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    vigenciaDesde = models.DateField()
    vigenciaHasta = models.DateField()
    #tipoTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT)    
    porcTarifario = models.DecimalField( max_digits=5, decimal_places=2, blank=True,null= True, editable=True)
    porcSuministros = models.DecimalField( max_digits=5, decimal_places=2, blank=True,null= True, editable=True)
    valorOxigeno = models.DecimalField( max_digits=8, decimal_places=2, blank=True,null= True, editable=True)
    porcEsterilizacion = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null= True, editable=True)
    porcMaterial  = models.DecimalField( max_digits=5, decimal_places=2,blank=True,null= True, editable=True)
    hospitalario = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True,null= True, editable=True)
    urgencias = models.CharField(max_length=1, choices=FLAG_CHOICES,blank=True,null= True, editable=True)
    ambulatorio = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True,null= True, editable=True)
    consultaExterna = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True,null= True, editable=True)
    copago = models.CharField(max_length=1, choices=FLAG_CHOICES, blank=True,null= True, editable=True)
    moderadora = models.CharField(max_length=1,choices=FLAG_CHOICES,  blank=True,null= True, editable=True)
    tipofactura  = models.CharField(max_length=1, blank=True,null= True, editable=True)
    particular  = models.CharField(max_length=1, choices=FLAG_CHOICES, blank=True,null= True, editable=True)
    agrupada = models.CharField(max_length=1, blank=True,null= True, editable=True)
    facturacionSuministros = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True,null= True, editable=True)
    facturacionCups  = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True,null= True, editable=True)
    cuentaContable= models.CharField(max_length=20, blank=True,null= True, editable=True)
    requisitos = models.CharField(max_length=2000, blank=True,null= True, editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(str(self.empresa) + str(' ') + str(self.tarifariosDescripcionProc) + str(' ') +  str(self.nombre)  )


class ConveniosTarifasHonorarios (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm16')
    convenio = models.ForeignKey('contratacion.Convenios', blank=True,null= True, editable=True, on_delete=models.PROTECT)        
    tipoTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT)    
    tipoHonorario =  models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='TipoHonorario05')
    codigoHomologado = models.CharField(max_length=10, blank=True, null=True, editable=True)
    cups = models.ForeignKey('clinico.Examenes',  blank=True,null= True, editable=True, on_delete=models.PROTECT,  related_name='Cups215')
    valor = models.DecimalField( max_digits=15, decimal_places=2, blank=True,null= True, editable=True)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    class Meta:
        unique_together = (('convenio','tipoTarifa', 'tipoHonorario'),)


    def __str__(self):
            return self.convenio


class ConveniosSuministros(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm17')
    convenio = models.ForeignKey('contratacion.Convenios', blank=True,null= True, editable=True, on_delete=models.PROTECT)        
    #tipoTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT)    
    #codigoHomologado = models.CharField(max_length=10, blank=True, null=True, editable=True)
    #concepto = models.ForeignKey('facturacion.Conceptos', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Concepto221')
    #suministro = models.ForeignKey('facturacion.Suministros',on_delete=models.PROTECT, null= False)
    #valor = models.DecimalField( max_digits=15, decimal_places=2, blank=True,null= True, editable=True)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)



    def __str__(self):
            return self.convenio



class ConveniosLiquidacionTarifasHonorarios(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm18')
    convenio = models.ForeignKey('contratacion.Convenios', blank=True,null= True, editable=True, on_delete=models.PROTECT)  
    tipoTarifa =  models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='TipoTarifa037')
    codigoHomologado = models.CharField(max_length=10, blank=True,null= True , editable=True )
    tipoHonorario =  models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='TipoHonorario017')
    concepto = models.ForeignKey('facturacion.Conceptos', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Concepto224')
    descripcion =  models.CharField(max_length=300, blank=True,null= True , editable=True )
    #codigoSuministro =  models.ForeignKey('facturacion.Suministros', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Suminis1277')
    suministro =  models.ForeignKey('facturacion.Suministros', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Suminis1277')
    #codigoCups = models.ForeignKey('clinico.Examenes', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Cups1177')
    cups = models.ForeignKey('clinico.Examenes',   blank=True,null= True, editable=True,  on_delete=models.PROTECT,  related_name='Cups209')
    valor =  models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='plantas2177')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES,  default='A', editable=False )


    def __str__(self):
            return self.descripcion




