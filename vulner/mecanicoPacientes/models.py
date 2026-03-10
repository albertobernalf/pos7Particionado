from django.db import models

# Create your models here.

class Farmacia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica390')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaFarmacia01')
    ingresoPaciente =  models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servAdmFarm01')
    tipoOrigen = models.ForeignKey('enfermeria.EnfermeriaTipoOrigen', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='TipoEnfermeria04')
    tipoMovimiento = models.ForeignKey('enfermeria.EnfermeriaTipoMovimiento', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='TipoEnfermeria05')
    estado = models.ForeignKey('farmacia.FarmaciaEstados', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='Farmaciaestados01')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3450')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES,  default='A', editable=False,  blank=True, null=True,)

    def __integer__(self):
        return str(self.historia)

class FarmaciaDetalle(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    farmacia = models.ForeignKey('farmacia.Farmacia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='Farmacia01')
    historiaMedicamentos = models.ForeignKey('clinico.HistoriaMedicamentos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servAdmFarm01')
    consecutivoMedicamento = models.IntegerField(blank=True, null=True)
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    dosisCantidad = models.DecimalField(max_digits=20, decimal_places=3)
    dosisUnidad = models.ForeignKey('clinico.UnidadesDeMedidaDosis', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    viaAdministracion = models.ForeignKey('clinico.ViasAdministracion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    #frecuencia = models.ForeignKey('clinico.FrecuenciasAplicacion', blank=True, null=True, editable=True,               on_delete=models.PROTECT)
    cantidadOrdenada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    #diasTratamiento =  models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3451')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)

class FarmaciaDespachos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    serviciosAdministrativosEntrega = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servAdmFarm02')
    usuarioEntrega = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3472')
    serviciosAdministrativosRecibe = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servAdmFarm03')
    usuarioRecibe = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3473')
    farmacia = models.ForeignKey('farmacia.Farmacia', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='FarmaDespacho02')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3452')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)


class FarmaciaDespachosDispensa(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    farmaciaDetalle = models.ForeignKey('farmacia.FarmaciaDetalle', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='FarmaciaDetalle01')
    despacho = models.ForeignKey('farmacia.FarmaciaDespachos', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='FarmaciaDespachos01')
    #consecutivoMedicamento = models.IntegerField(blank=True, null=True)
    #item = models.CharField(max_length=5, blank=True, null=True)
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    dosisCantidad = models.DecimalField(max_digits=20, decimal_places=3)
    dosisUnidad = models.ForeignKey('clinico.UnidadesDeMedidaDosis', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    viaAdministracion = models.ForeignKey('clinico.ViasAdministracion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    #frecuencia = models.ForeignKey('clinico.FrecuenciasAplicacion', blank=True, null=True, editable=True,               on_delete=models.PROTECT)
    cantidadOrdenada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadDevuelta = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    netoCantidad = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    #diasTratamiento =  models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaFarmacia2253')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)

class FarmaciaEstados(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre =  models.CharField(max_length=50, default='A', editable=True,  blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3459')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.nombre)

class FarmaciaDevolucion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica39022')
    serviciosAdministrativosDevuelve = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servDevuelve331')
    usuarioDevuelve = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaDevuelve453')
    serviciosAdministrativosRecibe = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servRecibe3231')
    usuarioRecibe = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaRecibe453')
    #observaciones =  models.CharField(max_length=250,  editable=True,  blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaFarmaciaDev3453')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)

class FarmaciaDevolucionDetalle(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    farmaciaDevolucion = models.ForeignKey('farmacia.FarmaciaDevolucion', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='FarmaciaDevolucion01')
    farmaciaDespachosDispensa = models.ForeignKey('farmacia.FarmaciaDespachosDispensa', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='FarmaciaDespachos21201')
    cantidadDevuelta = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadDevueltaRecibida = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    observaciones =  models.CharField(max_length=250,  editable=True,  blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaFarmaciaDevDet3453')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)