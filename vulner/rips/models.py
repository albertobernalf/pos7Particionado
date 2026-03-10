from django.db import models
from django.utils.timezone import now

# Create your models here.

class RipsTipos (models.Model):


   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsEnvios (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    TIPO_CHOICES = [
        ('E', 'ENVIADA'),
        ('P', 'PENDIENTE'), ]
    TIPO1_CHOICES = [
        ('F', 'FACTURA'),
        ('N', 'NOTA'), ]

    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'SedesClinica759')
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm26')
    ripsTiposNotas = models.ForeignKey('rips.RipsTiposNotas', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'RipsTipóNotas01')
    empresa =  models.ForeignKey('facturacion.Empresas', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = "empre12")
    fechaCreacion  =  models.DateTimeField(default=now, blank=True, null=True, editable=True)	
    fechaEnvio  =  models.DateTimeField(default=now, blank=True, null=True, editable=True)
    fechaRadicacion  =  models.DateTimeField(default=now, blank=True, null=True, editable=True)
    fechaGeneracionjson  =  models.DateTimeField(default=now, blank=True, null=True, editable=True)
    fechaRespuesta =  models.DateTimeField(default=now, blank=True, null=True, editable=True)
    respuesta = models.CharField(max_length=50000, blank=True,null= True, editable=True)
    rutaRespuestaJson = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    cantidadFacturas = models.CharField(max_length=5, blank=True,null= True, editable=True)
    cantidadPasaron = models.CharField(max_length=5, blank=True,null= True, editable=True)
    cantidadRechazadas = models.CharField(max_length=5, blank=True,null= True, editable=True)
    rutaJson = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    rutaZip = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    rutaPdf = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    #estadoPasoMinisterio=  models.CharField(max_length=10,  editable=False ,  default='PENDIENTE')
    ripsEstados = models.ForeignKey('rips.RipsEstados', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'RipsEstados02')
    usuarioEnvia = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='planta145')
    usuarioGeneraJson = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='planta146')
    usuarioRadicacion = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='planta149')
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.estadoPasoMinisterio

class RipsDetalle (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    TIPO1_CHOICES = [
        ('E', 'Enviada'),
        ('R', 'Rechazada'), 
        ('S', 'SinRespuesta'),]
    id = models.AutoField(primary_key=True)
    ripsEnvios =  models.ForeignKey('rips.RipsEnvios', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='Envios01')
    numeroFactura  =  models.ForeignKey('facturacion.Facturacion', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    glosa  =  models.ForeignKey('cartera.Glosas', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    notaCredito =  models.ForeignKey('cartera.NotasCredito', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    #numeroFactura  =  models.CharField(max_length=50, blank=True,null= True, editable=True)
    cuv  =  models.CharField(max_length=500, blank=True,null= True, editable=True)
    estadoPasoMinisterio=  models.CharField(max_length=10,  editable=False , choices = TIPO1_CHOICES, default='E')
    ripsEstados = models.ForeignKey('rips.RipsEstados', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'RipsEtados01')
    estado = models.CharField(max_length=20, blank=True,null= True, editable=True)
    rutaJsonFactura = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    rutaJsonRespuesta = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    rutaZip = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    rutaPdf = models.CharField(max_length=5000, blank=True,null= True, editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.numeroFactura

class RipsTransaccion (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'SedesClinica769')
    ripsEnvio =  models.ForeignKey('rips.RipsEnvios', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle01')
    numDocumentoIdObligado =   models.CharField(max_length=50, blank=True,null= True, editable=True)
    numFactura =  models.CharField(max_length=20, default='S', editable=False)
    tipoNota  =  models.ForeignKey('rips.RipsTiposNotas', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='TipoNota01')
    numNota =  models.CharField(max_length=20, default='S', editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.numDocumentoIdObligado

class RipsTipoUsuario (models.Model):
   ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsEstados (models.Model):

   id = models.AutoField(primary_key=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsPaises (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=3, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre



class RipsUsuarios (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    ZONAS_CHOICES = [
        ('UNO', 'Rural'),
        ('DOS', 'Urbano'), ]

    INCAPACIDAD_CHOICES = [
        ('SI', 'Si'),
        ('NO', 'No'), ]

    GENERO_CHOICES = [
        ('H', 'Masculino'),
        ('M', 'Femenino'), 
        ('I', 'Indeterminado'), ]

    id = models.AutoField(primary_key=True)
    ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle02')
    ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_02')
    tipoDocumentoIdentificacion =   models.CharField(max_length=9, blank=True,null= True, editable=True)
    numDocumentoIdentificacion = models.CharField(max_length=20, blank=True,null= True, editable=True)
    tipoUsuario  =  models.CharField(max_length=20, blank=True,null= True, editable=True)
    fechaNacimiento   = models.DateField(blank=True, null=True, editable=True)
    codSexo =  models.CharField(max_length=13, default='A', editable=False ,choices = GENERO_CHOICES)
    codPaisResidencia = models.ForeignKey('rips.RipsPaises', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='Paises01')
    codMunicipioResidencia = models.ForeignKey('sitios.Municipios', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='MunicipioRes01')
    codZonaTerritorialResidencia = models.ForeignKey('rips.RipsZonaTerritorial', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='SonaRes01')
    incapacidad = models.CharField(max_length=2, default='A', editable=False ,choices = INCAPACIDAD_CHOICES)
    consecutivo = models.CharField(max_length=10, blank=True,null= True, editable=True)
    ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion12')
    codPaisOrigen = models.ForeignKey('rips.RipsPaises', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='Usu01')
    fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class RipsGrupoServicios (models.Model):


   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsModalidadAtencion (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsServicios (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=4, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsFinalidadConsulta (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsCausaExterna (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsConceptoRecaudo (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsTiposDocumento (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre



class RipsConsultas (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    DIAGNOSTICO_CHOICES = [
        ('UNO', 'Impresion Diagnostica'),
        ('DOS', 'Confirmado nuevo'), 
        ('TRES', 'Confirmado repetido'), ]
    id = models.AutoField(primary_key=True)
    ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle03')
    ripsTipos =  models.ForeignKey('rips.RipsTipos', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsTipos01')   
    ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_03')
    codPrestador =  models.CharField(max_length=12, blank=True,null= True, editable=True)
    fechaInicioAtencion = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    numAutorizacion = models.CharField(max_length=30, blank=True,null= True, editable=True)
    codConsulta = models.ForeignKey('clinico.Examenes', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Examen01')
    modalidadGrupoServicioTecSal = models.ForeignKey('rips.RipsGrupoServicios', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Modal01')
    grupoServicios = models.ForeignKey('rips.RipsGrupoServicios', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Grupo01')
    codServicio =   models.ForeignKey('rips.RipsServicios', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Servicio01')
    finalidadTecnologiaSalud    = models.ForeignKey('rips.RipsFinalidadConsulta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Final01')
    causaMotivoAtencion = models.ForeignKey('rips.RipsCausaExterna', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Causa01')
    codDiagnosticoPrincipal = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost01')
    codDiagnosticoRelacionado1 =  models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost02')
    codDiagnosticoRelacionado2 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost03')
    codDiagnosticoRelacionado3 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost04')
    tipoDiagnosticoPrincipal = models.CharField(max_length=21, default='A', editable=False ,choices =DIAGNOSTICO_CHOICES)
    tipoDocumentoIdentificacion = models.ForeignKey('rips.RipsTiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    numDocumentoIdentificacion = models.CharField(max_length=20, blank=True,null= True, editable=True)
    vrServicio = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null= True, editable=True)
    conceptoRecaudo  = models.ForeignKey('rips.RipsConceptoRecaudo', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Recau01')
    tipoPagoModerador =  models.ForeignKey('rips.ripstipospagomoderador', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='modera031')
    valorPagoModerador = models.DecimalField(max_digits=10, decimal_places=0, blank=True,null= True, editable=True)
    numFEVPagoModerador =  models.CharField(max_length=20, blank=True,null= True, editable=True)
    consecutivo = models.IntegerField(editable=True, null=True, blank=True)
    ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion13')
    glosa = models.ForeignKey('cartera.Glosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosas02')
    notaCredito = models.ForeignKey('cartera.NotasCredito', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='NotaCredito0002')
    itemFactura  = models.IntegerField(editable=True, null=True, blank=True)
    #motivoGlosa = models.ForeignKey('cartera.MotivosGlosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosa02')
    #cantidadGlosada = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    #valorGlosado = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    #cantidadAceptada =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    #vAceptado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    #cantidadSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    #valorSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    notasCreditoGlosa =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    notasCreditoOtras =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    notasDebito = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Plantas01')
    fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)


    def __str__(self):
        return self.codPrestador

class RipsViasIngresoSalud (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsProcedimientos (models.Model):
   ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

   id = models.AutoField(primary_key=True)
   ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle04')
   ripsTipos =  models.ForeignKey('rips.RipsTipos', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsTipos02')   
   ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_04')
   codPrestador = models.CharField(max_length=12, blank=True,null= True, editable=True)
   fechaInicioAtencion = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   idMIPRES = models.CharField(max_length=15, blank=True,null= True, editable=True)
   numAutorizacion = models.CharField(max_length=30, blank=True,null= True, editable=True)
   codProcedimiento =  models.ForeignKey('clinico.Examenes', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Examen05')
   viaIngresoServicioSalud = models.ForeignKey('rips.RipsViasIngresoSalud', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='IngresoSal01')
   modalidadGrupoServicioTecSal = models.ForeignKey('rips.RipsModalidadAtencion', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ModalServ01')
   grupoServicios =  models.ForeignKey('rips.RipsGrupoServicios', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='GrupoServicios01')
   codServicio = models.ForeignKey('rips.RipsServicios', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Serrvicio02')
   finalidadTecnologiaSalud = models.ForeignKey('rips.RipsFinalidadConsulta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Finalidad02')
   tipoDocumentoIdentificacion = models.ForeignKey('rips.RipsTiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='TipoDocu05')
   numDocumentoIdentificacion = models.CharField(max_length=30, blank=True,null= True, editable=True)
   codDiagnosticoPrincipal = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost10')
   codDiagnosticoRelacionado = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost11')
   codComplicacion = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost12')
   vrServicio =  models.DecimalField(max_digits=15, decimal_places=2,  blank=True, null=True, editable=True)
   conceptoRecaudo = models.ForeignKey('rips.RipsConceptoRecaudo', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Recaudo05')
   tipoPagoModerador =  models.ForeignKey('rips.ripstipospagomoderador', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='modera01')
   valorPagoModerador =  models.DecimalField(max_digits=10, decimal_places=0, blank=True,null= True, editable=True)
   numFEVPagoModerador = models.CharField(max_length=20, blank=True,null= True, editable=True)
   consecutivo  = models.IntegerField(editable=True, null=True, blank=True)
   ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion14')
   glosa = models.ForeignKey('cartera.Glosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosas04')
   notaCredito = models.ForeignKey('cartera.NotasCredito', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='NotaCredito0003')
   itemFactura  = models.IntegerField(editable=True, null=True, blank=True)
   #motivoGlosa = models.ForeignKey('cartera.MotivosGlosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosa04')
   #cantidadGlosada = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorGlosado = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadAceptada =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #vAceptado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasCreditoGlosa =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasCreditoOtras =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasDebito = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)

   usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Plantas02')
   fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

   def __str__(self):
        return self.codPrestador

class RipsDestinoEgreso (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

  

class RipsUrgenciasObservacion (models.Model):
   ESTADOREG_CHOICES = [
        ('A', 'Activo'),
       ('I', 'Inactivo'), ]
   id = models.AutoField(primary_key=True)
   ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle05')
   ripsTipos =  models.ForeignKey('rips.RipsTipos', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsTipos03')   
   ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_05')
   codPrestador = models.CharField(max_length=12, blank=True,null= True, editable=True)
   fechaInicioAtencion = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   causaMotivoAtencion = models.ForeignKey('rips.RipsCausaExterna', blank=True, null=True, editable=True, on_delete=models.PROTECT)
   codDiagnosticoPrincipal =  models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost21')
   codDiagnosticoPrincipalE = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost22')
   codDiagnosticoRelacionadoE1 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost23')
   codDiagnosticoRelacionadoE2 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost24')
   codDiagnosticoRelacionadoE3 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost25')
   condicionDestinoUsuarioEgreso = models.ForeignKey('rips.RipsDestinoEgreso', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='DestinoEgre01')
   codDiagnosticoCausaMuerte = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost26')
   fechaEgreso = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   consecutivo =  models.IntegerField(editable=True, null=True, blank=True)
   ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion15')
   #GlosaId = models.ForeignKey('cartera.Glosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosas05')
   #itemFactura = models.DecimalField(max_digits=7, decimal_places=0, default=0)
   #motivoGlosa = models.ForeignKey('cartera.MotivosGlosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosa05')
   #cantidadGlosada = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorGlosado = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadAceptada =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #vAceptado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #notasCreditoGlosa =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #notasCreditoOtras =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #notasDebito = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Plantas05')
   fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)


   def __str__(self):
        return self.codPrestador




class RipsHospitalizacion (models.Model):
   ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

   id = models.AutoField(primary_key=True)
   ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle09')
   ripsTipos =  models.ForeignKey('rips.RipsTipos', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsTipos04')   
   #tipoRips = models.CharField(max_length=10,  blank=True, null=True, editable=False , default='FACTURA')
   ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_06')
   codPrestador = models.CharField(max_length=12, blank=True,null= True, editable=True)
   viaIngresoServicioSalud = models.ForeignKey('rips.RipsViasIngresoSalud', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='IngresoSal11')
   fechaInicioAtencion = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   numAutorizacion = models.CharField(max_length=30, blank=True,null= True, editable=True)
   causaMotivoAtencion = models.ForeignKey('rips.RipsCausaExterna', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='CausaExt05')
   codDiagnosticoPrincipal = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost31')
   codDiagnosticoPrincipalE  = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost32')
   codDiagnosticoRelacionadoE1 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost33')
   codDiagnosticoRelacionadoE2 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost34')
   codDiagnosticoRelacionadoE3 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost35')
   codComplicacion = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost36')
   condicionDestinoUsuarioEgreso = models.ForeignKey('rips.RipsDestinoEgreso', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='DestinoUsu02') 
   codDiagnosticoCausaMuerte = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost37')
   fechaEgreso = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   consecutivo =  models.IntegerField(editable=True, null=True, blank=True)
   ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion17')
   usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Plantas21')
   fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)



   def __str__(self):
        return self.codPrestador

class RipsRecienNacido(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    H =  'Masculino'
    M = 'Femenino'
    I = 'Indeterminado'
    TIPO_SEXO = (
        (H, 'Masculino'),
        (M, 'Femenino'),
	(I, 'Indeterminado'),
     )
    id = models.AutoField(primary_key=True)
    ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle08')
    ripsTipos =  models.ForeignKey('rips.RipsTipos', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsTipos05')   
    ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_07')
    codPrestador = models.CharField(max_length=12, blank=True,null= True, editable=True)
    tipoDocumentoIdentificacion = models.ForeignKey('rips.RipsTiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='TipoDocRips01')
    numDocumentoIdentificacion = models.CharField(max_length=20, blank=True,null= True, editable=True)
    fechaNacimiento = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    edadGestacional = models.CharField(max_length=2, blank=True,null= True, editable=True)
    numConsultasCPrenatal =  models.CharField(max_length=10, blank=True,null= True, editable=True)
    codSexoBiologico = models.CharField(max_length=13, default='A', editable=False ,choices = TIPO_SEXO)
    peso =   models.CharField(max_length=10, blank=True,null= True, editable=True)
    codDiagnosticoPrincipal = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost41')
    condicionDestinoUsuarioEgreso =  models.ForeignKey('rips.RipsDestinoEgreso', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost42')
    codDiagnosticoCausaMuerte = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost43')
    fechaEgreso = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    consecutivo =  models.IntegerField(editable=True, null=True, blank=True)
    ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion18')
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Plantas33')
    fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)


    def __str__(self):

        return self.codPrestador

class RipsTipoMedicamento (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsCums (models.Model):

   id = models.AutoField(primary_key=True)
   #codigo = models.CharField(max_length=15, blank=True,null= True, editable=True)
   cum = models.CharField(max_length=15, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=300, blank=True,null= True, editable=True)
   descripcion =   models.CharField(max_length=300, blank=True,null= True, editable=True)
   codigoAtc =    models.CharField(max_length=50, blank=True,null= True, editable=True)
   nombreAtc =    models.CharField(max_length=300, blank=True,null= True, editable=True)
   invima =    models.CharField(max_length=50, blank=True,null= True, editable=True)
   #principioActivo =    models.CharField(max_length=300, blank=True,null= True, editable=True)
   #administracion =    models.CharField(max_length=100, blank=True,null= True, editable=True)
   #viaAdministracion =  models.ForeignKey('clinico.ViasAdministracion', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ViasAdmon10')
   ripsViasAdministracion =  models.ForeignKey('rips.RipsViasAdministracion', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ViasAdmon10')
   principiosActivos =  models.ForeignKey('clinico.PrincipiosActivos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ViasAdmon11')
   ripsUnidadMedida = models.ForeignKey('rips.RipsUmm', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='RipsUnidad12')
   ripsTipoMedicamento = models.ForeignKey('rips.RipsTipoMedicamento', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='RipsTipo11')

   def __str__(self):
        return self.nombre


class RipsUmm (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=4, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)
   descripcion = models.CharField(max_length=80, blank=True,null= True, editable=True)   

   def __str__(self):
        return self.nombre

class RipsFormaFarmaceutica (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=6, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)
   descripcion = models.CharField(max_length=500, blank=True,null= True, editable=True)   

   def __str__(self):
        return self.nombre


class RipsUnidadUpr (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsMedicamentos(models.Model):
   ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

   id = models.AutoField(primary_key=True)
   ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle07')
   ripsTipos =  models.ForeignKey('rips.RipsTipos', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsTipos06')   
   ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_09')
   codPrestador = models.CharField(max_length=12, blank=True,null= True, editable=True)
   numAutorizacion = models.CharField(max_length=30, blank=True,null= True, editable=True)
   idMIPRES = models.CharField(max_length=15, blank=True,null= True, editable=True)
   fechaDispensAdmon = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   codDiagnosticoPrincipal = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost51')
   codDiagnosticoRelacionado = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Diagnost52')
   tipoMedicamento = models.ForeignKey('rips.RipsTipoMedicamento', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='TipoMed01')
   codTecnologiaSalud  = models.ForeignKey('rips.RipsCums', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Cums01')
   nomTecnologiaSalud = models.CharField(max_length=30, blank=True,null= True, editable=True)
   concentracionMedicamento = models.CharField(max_length=100, blank=True,null= True, editable=True)
   unidadMedida =  models.ForeignKey('rips.RipsUmm', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Umedida11')
   formaFarmaceutica = models.ForeignKey('rips.RipsFormaFarmaceutica', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Farmaceu01')
   unidadMinDispensa = models.ForeignKey('rips.RipsUnidadUpr', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='UnidadUpr01')
   cantidadMedicamento = models.DecimalField(max_digits=10, decimal_places=0, blank=True,null= True, editable=True)
   diasTratamiento = models.DecimalField(max_digits=3, decimal_places=0,   blank=True,null= True, editable=True)
   tipoDocumentoIdentificacion  = models.ForeignKey('rips.RipsTiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='RipsTiposDoc31')
   numDocumentoIdentificacion= models.CharField(max_length=20, blank=True,null= True, editable=True)
   vrUnitMedicamento = models.DecimalField(max_digits=15, decimal_places=0,blank=True,null= True, editable=True)
   vrServicio = models.DecimalField(max_digits=15, decimal_places=2, blank=True,null= True, editable=True)
   conceptoRecaudo = models.ForeignKey('rips.RipsConceptoRecaudo', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Recaudo41')
   valorPagoModerador = models.DecimalField(max_digits=10, decimal_places=0, blank=True,null= True, editable=True)
   numFEVPagoModerador = models.CharField(max_length=20, blank=True,null= True, editable=True)
   consecutivo =  models.IntegerField(editable=True, null=True, blank=True)
   ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion19')
   glosa = models.ForeignKey('cartera.Glosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosas06')
   notaCredito = models.ForeignKey('cartera.NotasCredito', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='NotaCredito00304')
   itemFactura = models.IntegerField(editable=True, null=True, blank=True)
   #motivoGlosa = models.ForeignKey('cartera.MotivosGlosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosa06')
   #cantidadGlosada = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorGlosado = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadAceptada =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #vAceptado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasCreditoGlosa =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasCreditoOtras =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasDebito = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)

   usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Plantas61')
   fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)
 


   def __str__(self):
        return self.codPrestador

class RipsTipoOtrosServicios (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsDci (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsOtrosServicios(models.Model):
   ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]


   id = models.AutoField(primary_key=True)
   ripsDetalle =  models.ForeignKey('rips.RipsDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsDetalle06')
   ripsTipos =  models.ForeignKey('rips.RipsTipos', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpsTipos07')   
   codPrestador = models.CharField(max_length=12, blank=True,null= True, editable=True)
   ingreso =  models.ForeignKey('admisiones.Ingresos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='ingre_10')
   numAutorizacion = models.CharField(max_length=30, blank=True,null= True, editable=True)
   idMIPRES = models.CharField(max_length=15, blank=True,null= True, editable=True)
   fechaSuministroTecnologia =  models.DateTimeField(default=now, blank=True, null=True, editable=True)
   tipoOS = models.ForeignKey('rips.RipsTipoOtrosServicios', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='OtrosServ01')
   codTecnologiaSalud =  models.ForeignKey('rips.RipsCums', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='RipsCums11')
   codTecnologiaSaludCups =  models.ForeignKey('clinico.Examenes', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='RipsCups11')
   nomTecnologiaSalud = models.CharField(max_length=60, blank=True,null= True, editable=True)
   nomTecnologiaSaludCups = models.CharField(max_length=60, blank=True,null= True, editable=True)
   cantidadOS  =   models.DecimalField(max_digits=5, decimal_places=0, blank=True,null= True, editable=True)
   tipoDocumentoIdentificacion = models.ForeignKey('rips.RipsTiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='RipsTiposDoc21')
   numDocumentoIdentificacion = models.CharField(max_length=20, blank=True,null= True, editable=True)
   vrUnitOS = models.DecimalField(max_digits=15, decimal_places=0, blank=True,null= True, editable=True)
   vrServicio = models.DecimalField(max_digits=15, decimal_places=2, blank=True,null= True, editable=True)
   conceptoRecaudo = models.ForeignKey('rips.RipsConceptoRecaudo', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Recaudo50')
   tipoPagoModerador =  models.ForeignKey('rips.ripstipospagomoderador', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='modera012')
   valorPagoModerador = models.DecimalField(max_digits=10, decimal_places=0, blank=True,null= True, editable=True)
   numFEVPagoModerador = models.CharField(max_length=20, blank=True,null= True, editable=True)
   consecutivo = models.IntegerField(editable=True, null=True, blank=True)
   ripsTransaccion =  models.ForeignKey('rips.RipsTransaccion', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='RpipsTransaccion20')
   glosa = models.ForeignKey('cartera.Glosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosas07')
   notaCredito = models.ForeignKey('cartera.NotasCredito', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='NotaCredito00214')
   itemFactura = models.IntegerField(editable=True, null=True, blank=True)
   #motivoGlosa = models.ForeignKey('cartera.MotivosGlosas', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Glosa07')
   #cantidadGlosada = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorGlosado = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadAceptada =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #vAceptado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #cantidadSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   #valorSoportado =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasCreditoGlosa =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasCreditoOtras =models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)
   notasDebito = models.DecimalField( max_digits=15, decimal_places=2 , blank=True,null= True, editable=True)

   usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='Plantas12')
   fechaRegistro = models.DateTimeField(default=now, blank=True, null=True, editable=True)
   estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)
 


   def __str__(self):
        return self.codPrestador


class RipsTiposNotas (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsTiposPagoModerador (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)
   codigoAplicativo = models.CharField(max_length=10, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsZonaTerritorial (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsMunicipios (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=5, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre


class RipsViasAdministracion (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre

class RipsCups (models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
    nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)
    descripcion =  models.ForeignKey('facturacion.conceptos', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='RipsCups_01')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class RipsTipoDiagnosticoPrincipal (models.Model):

   id = models.AutoField(primary_key=True)
   codigo = models.CharField(max_length=2, blank=True,null= True, editable=True)
   nombre =   models.CharField(max_length=80, blank=True,null= True, editable=True)

   def __str__(self):
        return self.nombre