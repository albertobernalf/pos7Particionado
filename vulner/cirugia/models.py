from django.db import models
from datetime import date

# Create your models here.

class Cirugias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.Sedesclinica', blank=True, null=True, editable=True,     on_delete=models.PROTECT)
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True, editable=True, related_name='Historia127')
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='DocumentoHistoria54')
    consecAdmision = models.IntegerField(default=0)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm126')
    especialidad = models.ForeignKey('clinico.Especialidades', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    convenio = models.ForeignKey('contratacion.Convenios', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    urgente = models.CharField(max_length=1, blank=True, null=True, editable=True)
    tipoQx = models.CharField(max_length=20, blank=True, null=True, editable=True)
    anestesia = models.ForeignKey('cirugia.TiposAnestesia', blank=True, null=True, editable=True,  on_delete=models.PROTECT)
    autorizacion =  models.ForeignKey('autorizaciones.Autorizaciones', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='DocumentoHistoria54')
    usuarioSolicita = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Usuario40')
    fechaSolicita = models.DateTimeField()
    solicitaHospitalizacion = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True, null=True, editable=True)
    solicitaAyudante = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True, null=True, editable=True)
    solicitaTiempoQx =  models.CharField(max_length=20, blank=True, null=True, editable=True)
    solicitatipoQx = models.CharField(max_length=20, blank=True, null=True, editable=True)
    solicitaAnestesia = models.CharField(max_length=1 ,choices=FLAG_CHOICES , blank=True, null=True, editable=True)
    solicitaSangre = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True, null=True, editable=True)
    describeSangre = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    cantidadSangre = models.CharField(max_length=10, blank=True, null=True, editable=True)
    solicitaCamaUci = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True, null=True, editable=True)
    solicitaMicroscopio = models.CharField(max_length=1, blank=True, null=True, editable=True)
    solicitaRx = models.CharField(max_length=1, blank=True, null=True, editable=True)
    solicitaAutoSutura = models.CharField(max_length=1, blank=True, null=True, editable=True)
    solicitaOsteosintesis = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    soliictaSoporte = models.CharField(max_length=1, blank=True, null=True, editable=True)
    solicitaBiopsia = models.CharField(max_length=1, blank=True, null=True, editable=True)
    solicitaMalla = models.CharField(max_length=1, blank=True, null=True, editable=True)
    solicitaOtros = models.CharField(max_length=1, blank=True, null=True, editable=True)
    describeOtros = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    sala = models.ForeignKey('sitios.Salas', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    fechaProg = models.DateField(default=date.today,  blank=True, null=True, editable=True)
    HoraProg = models.CharField(max_length=5, blank=True, null=True, editable=True)
    ingresoQuirofano = models.DateField(default=date.today,   blank=True, null=True, editable=True)
    horaIngresoQuirofano = models.CharField(max_length=8, blank=True, null=True, editable=True)
    fechaIniAnestesia = models.DateField(default=date.today,   blank=True, null=True, editable=True)
    HoraIniAnestesia = models.CharField(max_length=8, blank=True, null=True, editable=True)
    fechaQxInicial = models.DateField(default=date.today,   blank=True, null=True, editable=True)
    horaQxInicial = models.CharField(max_length=8, blank=True, null=True, editable=True)
    fechaQxFinal = models.DateField(default=date.today,   blank=True, null=True, editable=True)
    horaQxFinal = models.CharField(max_length=8, blank=True, null=True, editable=True)
    fechaFinAnestesia = models.DateField(default=date.today,   blank=True, null=True, editable=True)
    horaFinAnestesia = models.CharField(max_length=8, blank=True, null=True, editable=True)
    salidaQuirofano = models.DateField(default=date.today,   blank=True, null=True, editable=True)
    horaSalidaQuirofano = models.CharField(max_length=8, blank=True, null=True, editable=True)
    ingresoRecuperacion = models.DateField(default=date.today,  blank=True, null=True, editable=True)
    horaIngresoRecuperacion = models.CharField(max_length=8, blank=True, null=True, editable=True)
    salidaRecuperacion = models.DateField(default=date.today,  blank=True, null=True, editable=True)
    horaSalidaRecuperacion = models.CharField(max_length=8, blank=True, null=True, editable=True)
    intervencion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    riesgos = models.CharField(max_length=3000, blank=True, null=True, editable=True)
    observaciones = models.CharField(max_length=5000, blank=True, null=True, editable=True)
    dxPreQx = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Dx511')
    dxPostQx = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT ,    related_name='Dx521')
    dxPrinc = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT ,    related_name='Dx531')
    impresionDx = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Dx541')
    dxRel1 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Dx542')
    #dxRel2 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Dx553')
    #dxRel3 = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Dx564')
    descripcionQx = models.CharField(max_length=10000, blank=True, null=True, editable=True)
    analisis = models.CharField(max_length=10000, blank=True, null=True, editable=True)
    planx = models.CharField(max_length=10000, blank=True, null=True, editable=True)
    dxComplicacion =models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Dx555')
    complicaciones = models.CharField(max_length=3000, blank=True, null=True, editable=True)
    patologia = models.CharField(max_length=500, blank=True, null=True, editable=True)
    formaRealiza = models.CharField(max_length=15, blank=True, null=True, editable=True)
    estadoCirugia = models.ForeignKey('cirugia.EstadosCirugias', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    estadoProgramacion = models.ForeignKey('cirugia.EstadosProgramacion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    tiposCirugia = models.ForeignKey('cirugia.TiposCirugia', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    estadoSalida = models.CharField(max_length=1, default='A', blank=True, null=True, editable=True)
    vboAdmon = models.CharField(max_length=1, blank=True, null=True, editable=True)
    hallazgos = models.CharField(max_length=5000, blank=True, null=True, editable=True)
    osteosintesis = models.CharField(max_length=300, blank=True, null=True, editable=True)
    auxiliar = models.CharField(max_length=200, blank=True, null=True, editable=True)
    materialEspecial = models.CharField(max_length=300, blank=True, null=True, editable=True)
    reprogramada = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True, null=True, editable=True)
    motivoReprogramada = models.CharField(max_length=500, blank=True, null=True, editable=True)
    tipoCancela = models.CharField(max_length=15, blank=True, null=True, editable=True)
    motivoCancela = models.CharField(max_length=500, blank=True, null=True, editable=True)
    tiempoMaxQx = models.CharField(max_length=10, blank=True, null=True, editable=True)
    observacionesProgramacion = models.CharField(max_length=500, blank=True, null=True, editable=True)
    usuarioPrograma = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Usuario41')
    fechaPrograma = models.DateTimeField( blank=True, null=True, editable=True)
    usuarioCancela = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT ,    related_name='Usuario42')
    fechaCancela = models.DateTimeField( blank=True, null=True, editable=True)
    usuarioReprograma = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,   on_delete=models.PROTECT,    related_name='Usuario43')
    fechaReprograma = models.DateTimeField( blank=True, null=True, editable=True)
    intensificador = models.CharField(max_length=1, blank=True, null=True, editable=True)
    tipofractura = models.CharField(max_length=40, blank=True, null=True, editable=True)
    recomendacionenfermeria = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    folioEvolucionPreQx = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True, editable=True)
    folioEvolucionPostQx= models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True, editable=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='planta39')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __integer__(self):
        return str(self.historia)


class CirugiasProcedimientos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    cirugia = models.ForeignKey('cirugia.Cirugias', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='cirugias12')
    cups = models.ForeignKey('clinico.Examenes', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Cups104')
    finalidad = models.ForeignKey('cirugia.FinalidadCirugia', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Final004')
    cruento = models.CharField(max_length=1,choices=FLAG_CHOICES, blank=True, null=True ,editable=False)
    incruento = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, blank=True, null=True, editable=False)
    viasDeAcceso = models.ForeignKey('cirugia.ViasDeAcceso', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Cups104')
    regionOperatoria = models.ForeignKey('cirugia.RegionesOperatorias', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Cups104')
    autorizacionDetalle = models.ForeignKey('autorizaciones.AutorizacionesDetalle', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='AutDetCir101')
    mipres = models.CharField(max_length=50, null=True, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='planta67')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __integer__(self):
        return str(self.cups)


class CirugiasParticipantes(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    cirugia = models.ForeignKey('cirugia.Cirugias', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='cirugias13')
    cirugiaProcedimiento = models.ForeignKey('cirugia.CirugiasProcedimientos', blank=True, null=True, editable=True,   on_delete=models.PROTECT ,    related_name='CiruProc10') 	
    #cups = models.ForeignKey('clinico.Examenes', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Cups1024')
    tipoHonorarios = models.ForeignKey('tarifarios.TiposHonorarios', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='TipoHonorario12')
    medico = models.ForeignKey('clinico.EspecialidadesMedicos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='TipoHonorario12')
    #especialidad = models.ForeignKey('clinico.EspecialidadesMedicos', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='TipoHonorario12')
    finalidad =  models.ForeignKey('cirugia.FinalidadCirugia', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Final005')
    #viasDeAcceso = models.ForeignKey('cirugia.ViasDeAcceso', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='acceso104')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='planta68')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.cups)


class EstadosCirugias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class TiposAnestesia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class CirugiasMaterialQx(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    HOJADEGASTO_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    cirugia = models.ForeignKey('cirugia.Cirugias', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    cirugiaProcedimiento = models.ForeignKey('cirugia.CirugiasProcedimientos', blank=True, null=True, editable=True,   on_delete=models.PROTECT) 	
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,  on_delete=models.PROTECT)
    #cups = models.ForeignKey('clinico.Examenes', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='Cups1544')
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    unitario = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    valorLiquidacion = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True, editable=True)
    hojaDeGasto = models.CharField(max_length=1, choices=HOJADEGASTO_CHOICES, default='N', blank=True,null= True, editable=True,)
    #facturable = models.CharField(max_length=1,blank=True, null=True , editable=False)
    autorizacionDetalle = models.ForeignKey('autorizaciones.AutorizacionesDetalle', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='AutMatQx101')
    mipres = models.CharField(max_length=50, null=True, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __integer__(self):
        return str(self.cirugia)


class RecordAnestesico(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    cirugia = models.ForeignKey('cirugia.Cirugias', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    fecha = models.DateTimeField()
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __integer__(self):
        return str(self.cirugia)


class HojasDeGastos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    cirugia = models.ForeignKey('cirugia.Cirugias', blank=True, null=True, editable=True, on_delete=models.PROTECT,    related_name='cirugias17')
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,  on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __integer__(self):
        return str(self.cirugia)

class EstadosSalas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class EstadosProgramacion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class ProgramacionCirugias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.Sedesclinica', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm129')
    cirugia = models.ForeignKey('cirugia.Cirugias', blank=True, null=True, editable=True,   on_delete=models.PROTECT , related_name='cir212')
    sala = models.ForeignKey('sitios.Salas', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    #estadoSala = models.ForeignKey('cirugia.EstadosSalas', blank=True, null=True, editable=True,   on_delete=models.PROTECT) 
    estadoProgramacion = models.ForeignKey('cirugia.EstadosProgramacion', blank=True, null=True, editable=True,   on_delete=models.PROTECT) 
    fechaProgramacionInicia = models.DateField(default=date.today, blank=True, null=True, editable=True)
    horaProgramacionInicia = models.CharField(max_length=5, blank=True, null=True, editable=True)
    fechaProgramacionFin = models.DateField(default=date.today, blank=True, null=True, editable=True)
    horaProgramacionFin = models.CharField(max_length=5, blank=True, null=True, editable=True)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True,  on_delete=models.PROTECT, related_name='DocumentoHistoria123')
    consecAdmision = models.IntegerField(default=0)
    fechaRegistro = models.DateTimeField(default=date.today,  editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)


    def __str__(self):
        return str(self.sala)


class OrganosCirugias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)


class IntervencionCirugias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class TiposHeridasOperatorias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class FinalidadCirugia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class PlanificacionCirugia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class ZonasCirugia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombred)


class GravedadCirugia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class TiposCirugia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class RegionesOperatorias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=50, blank=True, null=True, editable=True)
    organos  = models.CharField(max_length=250, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.region)

class ViasDeAcceso(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)