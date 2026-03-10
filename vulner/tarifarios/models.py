from django.db import models

# Create your models here.

class TiposTarifaProducto (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
        return str(self.nombre)

class TiposTarifa (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposTarifaProducto = models.ForeignKey('tarifarios.TiposTarifaProducto', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoTarifa11')
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(self.nombre + ' ' + str(self.tiposTarifaProducto))

class TiposHonorarios(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    ripsTipoOtrosServicios = models.ForeignKey('rips.ripstipoOtrosServicios', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipooTROsERV01')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
        return str(self.nombre)


class TarifariosDescripcion (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm30')
    tiposTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoTarifa11')
    columna =  models.CharField(max_length=15,  blank=True,null= True, editable=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
        return str(str(self.tiposTarifa) + ' '  + str(self.descripcion))

class TarifariosDescripcionHonorarios (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
         return str(self.nombre)


class TarifariosProcedimientos (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm31')
    tiposTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoTarifa171')
    codigoCups = models.ForeignKey('clinico.Examenes', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Cups10121')
    codigoHomologado = models.CharField(max_length=10, blank=True, null=True, editable=True)
    concepto = models.ForeignKey('facturacion.Conceptos', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Concepto2271')
    colValorBase =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor1 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor2 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor3 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor4 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor5 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor6 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor7 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor8 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor9 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor10 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='plantas2020')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    class Meta:
        unique_together = (('tiposTarifa', 'codigoCups'),)

    class Meta:
        indexes = [
            models.Index(fields=['tiposTarifa','codigoCups'], name='tarifProcedTipostarifaIdx'),
        ]

    def __str__(self):
        return str(self.codigoHomologado)

class TarifariosProcedimientosHonorarios (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm33')
    tiposTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoTarifa1711')
    codigoCups = models.ForeignKey('clinico.Examenes', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Cups101211')
    #tipoHonorario = models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoHonorario1122')
    codigoHomologado = models.CharField(max_length=10, blank=True, null=True, editable=True)
    concepto = models.ForeignKey('facturacion.Conceptos', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Concepto22714')
    valorHonorarioCirujano =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    valorHonorarioAnestesiologo =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    valorHonorarioAyudante =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    valorHonorarioPerfucionista =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    valorHonorarioViaAcceso =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    valorHonorarioUnicaVia =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    valorHonorarioDobleVia =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValorBase =  models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor1 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor2 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor3 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor4 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor5 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor6 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor7 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    ##colValor8 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor9 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    #colValor10 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='plantas20205')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
        return str(self.codigoHomologado)





class TarifariosSuministros (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm34')
    tiposTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoTarifa172')
    codigoCum = models.ForeignKey('facturacion.Suministros', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Suministro10121')
    codigoHomologado = models.CharField(max_length=10, blank=True, null=True, editable=True)
    concepto = models.ForeignKey('facturacion.Conceptos', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Concepto22712')
    colValorBase = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor1 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor2 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor3 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor4 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor5 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor6 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor7 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor8 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor9 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    colValor10 = models.DecimalField( max_digits=20, decimal_places=4,blank=True,null= True, editable=True,)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='plantas20202')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    class Meta:
        unique_together = (('tiposTarifa', 'codigoCum'),)

    class Meta:
        indexes = [
            models.Index(fields=['tiposTarifa','codigoCum'], name='tarifSuministTipostarifaIdx'),
        ]


    def __str__(self):
        return str(self.codigoHomologado)


class GruposQx(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(self.nombre)

class MinimosLegales(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    año = models.CharField(max_length=4, blank=True, null=True, editable=True)
    valor =  models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
        return str(self.nombre)


class TablaHonorariosSoat(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposTarifaProducto = models.ForeignKey('tarifarios.TiposTarifaProducto', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tiposHonorarios =  models.ForeignKey('tarifarios.TiposHonorarios', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    homologado = models.CharField(max_length=8,  blank=True, null=True, editable=True)
    grupoQx =  models.ForeignKey('tarifarios.GruposQx', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    smldv = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.id)

class TablaHonorariosIss(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposTarifaProducto = models.ForeignKey('tarifarios.TiposTarifaProducto', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tiposHonorarios =  models.ForeignKey('tarifarios.TiposHonorarios', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    homologado = models.CharField(max_length=8,  blank=True, null=True, editable=True)
    valorUvr = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.id)


class TablaMaterialSuturaCuracion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposTarifaProducto = models.ForeignKey('tarifarios.TiposTarifaProducto', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    homologado = models.CharField(max_length=8,  blank=True, null=True, editable=True)
    grupoQx =  models.ForeignKey('tarifarios.GruposQx', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tipoHonorario = models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoHonorario14754')
    smldv = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=True)
    minimosLegales = models.ForeignKey('tarifarios.MinimosLegales', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    cruento = models.CharField(max_length=1, blank=True, null=True ,editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.id)

class TablaMaterialSuturaCuracionIss(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposTarifaProducto = models.ForeignKey('tarifarios.TiposTarifaProducto', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tiposSala = models.ForeignKey('sitios.TiposSalas', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tipoHonorario = models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoHonorario11244')
    homologado = models.CharField(max_length=8,  blank=True, null=True, editable=True)
    desdeUvr =  models.CharField(max_length=3,  blank=True, null=True, editable=True)
    hastaUvr = models.CharField(max_length=3,  blank=True, null=True, editable=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)


class TablaSalasDeCirugia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposTarifaProducto = models.ForeignKey('tarifarios.TiposTarifaProducto', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    homologado = models.CharField(max_length=8,  blank=True, null=True, editable=True)
    grupoQx =  models.ForeignKey('tarifarios.GruposQx', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tipoHonorario = models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoHonorario14452')
    smldv = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=True)
    cruento = models.CharField(max_length=1, blank=True, null=True ,editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)

class TablaSalasDeCirugiaIss(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposTarifaProducto = models.ForeignKey('tarifarios.TiposTarifaProducto', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tiposSala = models.ForeignKey('sitios.TiposSalas', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tipoHonorario = models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoHonorario11222')
    homologado = models.CharField(max_length=8,  blank=True, null=True, editable=True)
    desdeUvr =  models.CharField(max_length=3,  blank=True, null=True, editable=True)
    hastaUvr = models.CharField(max_length=3,  blank=True, null=True, editable=True)
    valor = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)

class Estancias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    TIPOTARIFA_CHOICES = [
        ('S', 'SOAT'),
        ('I', 'ISS'), 
        ('P', 'PARTICULAR'), 

]
    id = models.AutoField(primary_key=True)
    #referencia = models.CharField(max_length=5, blank=True, null=True, editable=True)
    #codigo = models.CharField(max_length=6, blank=True, null=True, editable=True)
    homologado = models.CharField(max_length=8, blank=True, null=True, editable=True)
    #nivelesEstancias = models.ForeignKey('tarifarios.NivelesEstancias', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    nivelesClinica = models.ForeignKey('clinico.NivelesClinica', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    especialidadesEnEstancias = models.ForeignKey('tarifarios.EspecialidadesEnEstancias', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tiposEstancias = models.ForeignKey('tarifarios.TiposEstancias', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=30, blank=True, null=True, editable=True) 
    tiposTarifa = models.ForeignKey('tarifarios.TiposTarifa', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='TipoTarifa1891')
    cups = models.ForeignKey('clinico.Examenes', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    diasMinimosLegales = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    uvrs = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    valor = models.DecimalField( max_digits=15, decimal_places=0 , blank=True,null= True, editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False )

    def __str__(self):
        return str(self.descripcion)

class NivelesEstancias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(self.nombre)

class EspecialidadesEnEstancias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(self.nombre)

class TiposEstancias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(self.nombre)
