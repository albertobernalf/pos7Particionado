from django.db import models
from django.utils.timezone import now
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db.models import CharField
from django.db.models import Index

# Create your models here.

class HistorialDiagnosticosCabezote(models.Model):

    id = models.AutoField(primary_key=True)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios',  blank=True, null=True, editable=True, on_delete=models.PROTECT,  related_name='DocumentoHistoriaDiag')
    consecAdmision = models.IntegerField()
    folio = models.IntegerField()
    observaciones = models.CharField(max_length=200)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.observaciones


class TiposRadiologia(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    nombre = models.CharField(max_length=50, null=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre



class Servicios(models.Model):
    id = models.AutoField(primary_key=True)
    #sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
    nombre = models.CharField(max_length=30, null = False)


    def __str__(self):
        return self.nombre

class EspecialidadesMedicos(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica301')
    especialidades = models.ForeignKey('clinico.Especialidades', on_delete=models.PROTECT, null=False,related_name ='especialidadesMedicos1')
    #tiposPlanta = models.ForeignKey('planta.TiposPlanta',    blank=True,null= True, on_delete=models.PROTECT ,related_name ='tiposPlanta301')
    planta = models.ForeignKey('planta.Planta',      blank=True,null= True ,on_delete = models.PROTECT)
    nombre = models.CharField(max_length=30, default="" , null = False)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta')
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    class Meta:
            unique_together = (('sedesClinica','planta','especialidades'),)


    def __integer__(self):
        return self.especialidades


class Especialidades(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30 , null = False)
    #examen = models.ForeignKey('clinico.Examenes',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    #examenCita = models.ForeignKey('clinico.Examenes',  blank=True, null=True, editable=True, on_delete=models.PROTECT ,related_name ='cuposCita')
    especialidadesEnEstancias = models.ForeignKey('tarifarios.EspecialidadesEnEstancias',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    interconsulta = models.CharField(max_length=1,  blank=True,null= True, editable=True,)
    cExterna    = models.CharField(max_length=1,  blank=True,null= True, editable=True,)
    quirurgica =  models.CharField(max_length=1,  blank=True,null= True, editable=True,)
    valoracionInicial =  models.CharField(max_length=1,  blank=True,null= True, editable=True,)
    #codigoCups = models.CharField(max_length=1,  blank=True,null= True, editable=True,)
    agenda = models.CharField(max_length=1,  blank=True, null=True, editable=True,)
    quirurgica = models.CharField(max_length=1,  blank=True, null=True, editable=True,)
    citaDeControl = models.CharField(max_length=1,  blank=True, null=True, editable=True,)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A', editable=False)


    def __str__(self):
        return self.nombre


class Medicos(models.Model):
        id = models.AutoField(primary_key=True)
        planta = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
        #tipoDoc = models.ForeignKey('usuarios.TiposDocumento',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
        #documento = models.IntegerField(default=1)
        #nombre = models.CharField(max_length=30)
        #especialidades = models.ForeignKey('clinico.Especialidades',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
        registroMedico = models.CharField(max_length=50, default='')
        departamento = models.ForeignKey('sitios.Departamentos',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
        ciudad = models.ForeignKey('sitios.Ciudades',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=20)
        contacto = models.CharField(max_length=50)
        centro = models.ForeignKey('sitios.Centros', blank=True, null=True, editable=True, on_delete=models.PROTECT)
        #firma = models.file()

        estado = models.CharField(max_length=1)

        class Meta:
            unique_together = (('planta'),)

        def __str__(self):
            return self.registroMedico



class EstadoExamenes(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
          return self.nombre


class Enfermedades(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, null=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre



class TiposExamen(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class TiposFolio(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class TiposAntecedente(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre





class CausasExterna(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    ripsCausaExterna = models.ForeignKey('rips.RipsCausaExterna',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class ViasIngreso(models.Model):
        id = models.AutoField(primary_key=True)
        STATUS_CHOICES = [
            ('A', 'Activo'),
            ('I', 'Inactivo'),
        ]
        nombre = models.CharField(max_length=50, null=True)
        estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

        def __str__(self):
            return self.nombre

class ViasEgreso(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True,blank=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')


    def __str__(self):
        return self.nombre


class TiposIncapacidad(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre




class Examenes(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    TiposExamen = models.ForeignKey('clinico.TiposExamen',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    codigoCups = models.CharField(max_length=20, null=False,  blank=True)
    #nombre = models.CharField(max_length=300)
    nombre = models.CharField(max_length=300 , null=True,  blank=True , unique=True)
    edadIni = models.IntegerField(blank=True, null=True, editable=True)
    edadFin = models.IntegerField( blank=True, null=True, editable=True)
    tipoHonorario =  models.ForeignKey('tarifarios.TiposHonorarios', blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name='TipoHonorario76091')
    solicitaEnfermeria = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', null=False, blank=True, )
    citaControl = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, null=True, editable=True)
    concepto = models.ForeignKey('facturacion.Conceptos', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    codigoRips = models.CharField(max_length=6,  blank=True, null=True, editable=True)
    grupoQx =  models.ForeignKey('tarifarios.GruposQx',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    cantidadUvr =  models.CharField(max_length=10,blank=True, null=True, editable=True)
    #uvrAño = models.ForeignKey('tarifas.Uvr', blank=True,null= True, editable=True, on_delete=models.PROTECT , related_name='Uvr105')
    honorarios = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, null=True, editable=True)
    requiereAutorizacion = models.CharField(max_length=1,  blank=True, null=True, editable=True, choices=FLAG_CHOICES ,default='N')
    tipoRadiologia = models.ForeignKey('clinico.TiposRadiologia',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    cupsGrupo = models.CharField(max_length=15,  blank=True, null=True, editable=True)
    cupsSubgrupo = models.CharField(max_length=15, blank=True, null=True, editable=True)
    cupsCategoria = models.CharField(max_length=15, blank=True, null=True, editable=True)
    cupsSubCategoria = models.CharField(max_length=15, blank=True, null=True, editable=True)
    resolucion1132 = models.CharField(max_length=15, blank=True, null=True, editable=True)
    nivelAtencion  =  models.CharField(max_length=15, blank=True, null=True, editable=True)
    centroCosto = models.CharField(max_length=15,  blank=True, null=True, editable=True)
    finalidad = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, null=True, editable=True)
    duracion =   models.CharField(max_length=15, blank=True, null=True, editable=True)
    manejaInterfaz = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, null=True, editable=True)
    distribucionTerceros = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, null=True, editable=True)
    consentimientoInformado = models.CharField(max_length=1,choices=FLAG_CHOICES, default='N', blank=True, null=True, editable=True)
    cita1Vez = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, null=True, editable=True)
    cuentaContable = models.CharField(max_length=20, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    class Meta:
        ordering = [Cast('nombre' , output_field=CharField), Cast('codigoCups' , output_field=CharField) ]

    class Meta:
        unique_together = (('codigoCups'),)

    class Meta:
        indexes = [
            models.Index(fields=['nombre'], name='examenesNombreIdx'),
	    models.Index(fields=['codigoCups'], name='cups_Idx'),
        ]


    def __str__(self):
        return '%s %s' % (self.codigoCups, self.nombre  )
        #return self.nombre

class EstadosInterconsulta(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class TiposInterconsulta(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class HistorialInterconsultas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id  = models.AutoField(primary_key=True)
    historia =  models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag11')
    ordenMedica = models.CharField(max_length=80, blank=True, null=True)
    tipoInterconsulta = models.ForeignKey('clinico.TiposInterconsulta',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    descripcionConsulta = models.CharField(max_length=200)
    especialidadConsulta = models.ForeignKey('clinico.EspecialidadesMedicos', default=1, on_delete=models.PROTECT, null=False)
    medicoConsulta  = models.ForeignKey('clinico.Medicos',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    especialidadConsultada = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT, null=False,    related_name='espe22')
    medicoConsultado  = models.ForeignKey('clinico.Medicos',  blank=True, null=True, editable=True, on_delete=models.PROTECT ,   related_name='med22')
    respuestaConsulta = models.CharField(max_length=5000 ,  blank=True, null=True)
    fechaRespuesta = models.DateTimeField(default=now ,  blank=True, null=True )
    diagnosticos = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadosInterconsulta = models.ForeignKey('clinico.EstadosInterconsulta',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.descripcionConsulta

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]



class TiposEvolucion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre




class Historia(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]

    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica367')
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True, null=True, editable=True,      on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoria5672')
    consecAdmision = models.IntegerField(default=0)
    folio = models.IntegerField(default=0)
    fecha = models.DateTimeField()
    tiposFolio = models.ForeignKey('clinico.TiposFolio', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    causasExterna = models.ForeignKey('clinico.causasExterna', blank=True, null=True, editable=True,             on_delete=models.PROTECT)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='seradm50')
    #dependenciasRealizado = models.ForeignKey('sitios.Dependencias', blank=True, null=True, editable=True,            on_delete=models.PROTECT)
    especialidades = models.ForeignKey('clinico.Especialidades', blank=True, null=True, editable=True,             on_delete=models.PROTECT)
    especialidadesMedicos = models.ForeignKey('clinico.EspecialidadesMedicos', blank=True, null=True, editable=True,             on_delete=models.PROTECT)
    planta = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    motivo = models.CharField(max_length=250,  blank=True, null=True,)
    subjetivo = models.CharField(max_length=250,  blank=True, null=True,)
    objetivo = models.CharField(max_length=250,  blank=True, null=True,)
    analisis = models.CharField(max_length=250,  blank=True, null=True,)
    plann = models.CharField(max_length=250,  blank=True, null=True,)
    ordenMedicaLab = models.CharField(max_length=30, blank=True, null=True)
    ordenMedicaRad = models.CharField(max_length=30, blank=True, null=True)
    ordenMedicaTer = models.CharField(max_length=30, blank=True, null=True)
    ordenMedicaMed = models.CharField(max_length=30, blank=True, null=True)
    ordenMedicaOxi = models.CharField(max_length=30, blank=True, null=True)
    ordenMedicaInt = models.CharField(max_length=30, blank=True, null=True)
    ordenDeControl = models.CharField(max_length=20000,  blank=True, null=True,)
    enfermedadActual = models.CharField(max_length=5000,  blank=True, null=True,)
    ingestaAlcohol = models.CharField(max_length=5000,  blank=True, null=True,)
    monitoreo = models.CharField(max_length=1,  blank=True, null=True,choices=STATUS_CHOICES,)
    examenFisico = models.CharField(max_length=5000,  blank=True, null=True,)
    justificacion = models.CharField(max_length=5000,  blank=True, null=True,)
    tipoEvolucion = models.ForeignKey('clinico.TiposEvolucion', blank=True, null=True, editable=True,               on_delete=models.PROTECT)
    apache2 = models.IntegerField(default=0 ,  blank=True, null=True,)
    indiceMortalidad = models.IntegerField(default=0 ,  blank=True, null=True )
    epicrisis = models.CharField(max_length=20000,  blank=True, null=True,)
    manejoQx = models.CharField(max_length=20000,  blank=True, null=True,)
    noQx = models.CharField(max_length=30,  blank=True, null=True,)
    antibioticos = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    tratamiento = models.CharField(max_length=5000,  blank=True, null=True,)
    llenadoCapilar = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    pulsos = models.CharField(max_length=1, blank=True, null=True, choices=FLAG_CHOICES,)
    vomito = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    nauseas = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    irritacion = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    neurologia = models.CharField(max_length=1, blank=True, null=True, choices=FLAG_CHOICES,)
    retiroPuntos = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    movilidadLimitada = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    interconsulta = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    observaciones = models.CharField(max_length=5000,  blank=True, null=True,)
    riesgos = models.CharField(max_length=5000,  blank=True, null=True,)
    notaAclaratoria = models.CharField(max_length=1,  blank=True, null=True, choices=FLAG_CHOICES,)
    fecNotaAclaratoria = models.DateTimeField(blank=True,  null=True,)
    textoNotaAclaratoria = models.CharField(max_length=5000,  blank=True, null=True,)
    usuarioNotaAclaratoria = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True,          on_delete=models.PROTECT)
    inmovilizacion = models.CharField(max_length=1, blank=True, null=True,choices=FLAG_CHOICES,)
    inmovilizacionObservaciones = models.CharField(max_length=5000,  blank=True, null=True,)
    riesgoHemodinamico = models.CharField(max_length=15,  blank=True, null=True,)
    riesgoVentilatorio = models.CharField(max_length=15,  blank=True, null=True,)
    leucopenia = models.CharField(max_length=50,  blank=True, null=True,)
    trombocitopenia = models.CharField(max_length=50,  blank=True, null=True,)
    hipotension = models.CharField(max_length=50,  blank=True, null=True,)
    mipres = models.CharField(max_length=30, null=True, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   ,          related_name='lanta345')
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES, default='A',editable=False,  blank=True,)

    def __integer__(self):
        return str(self.documento)

    class Meta:
        unique_together = (('tipoDoc', 'documento','consecAdmision','folio'),)
        indexes = [
            # Crea un índice compuesto sobre 'nombre' y 'email'
            Index(fields=['tipoDoc', 'documento','folio']),
            # Opcionalmente, puedes definir restricciones únicas (que también generan índices)
            # models.UniqueConstraint(fields=['email'], name='unique_email_constraint')
        ]
        ordering = ["tipoDoc", "documento", "folio", "fecha", "especialidades", "motivo", "subjetivo", "objetivo",
                    "analisis", "plann"]



class HistoriaExamenes(models.Model):
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    tiposExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT, null=False)
    codigoCups = models.CharField(max_length=20, null=False, blank=True)
    #dependenciasRealizado = models.ForeignKey('sitios.Dependencias', blank=True, null=True, editable=True,            on_delete=models.PROTECT)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True, null=True, editable=True,            on_delete=models.PROTECT)
    #ordenMedica = models.CharField(max_length=80, blank=True, null=True)
    #mipres = models.CharField(max_length=30, null=True, blank=True)
    consecutivo = models.IntegerField(blank=True, null=True)
    consecutivoLiquidacion = models.IntegerField(blank=True, null=True)
    cantidad = models.IntegerField()
    observaciones = models.CharField(max_length=200, editable=True,blank=True, null=True)
    autorizacion = models.ForeignKey('autorizaciones.Autorizaciones', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='aut01') 
    fechaToma = models.DateTimeField(blank=True, null=True)
    usuarioToma = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,  on_delete=models.PROTECT, related_name='usuarioToma1')
    #preliminar1 = models.CharField(max_length=300, editable=True,blank=True, null=True)
    interpretacion1 = models.CharField(max_length=5000, editable=True ,blank=True, null=True)
    #medicoInterpretacion1 = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='medInterpreta1')
    medicoInterpretacion1  = models.ForeignKey('clinico.Medicos', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='interpreta01')
    fechaInterpretacion1 = models.DateTimeField(blank=True, null=True)
    #preliminar2 = models.CharField(max_length=300, editable=True,blank=True, null=True)
    interpretacion2 = models.CharField(max_length=5000, editable=True,blank=True, null=True)
    medicoInterpretacion2  = models.ForeignKey('clinico.Medicos', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='interpreta02')
    #medicoInterpretacion2 = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='medInterpreta2')
    fechaInterpretacion2 = models.DateTimeField(blank=True, null=True)
    #preliminar3 = models.CharField(max_length=300, editable=True,blank=True, null=True)
    interpretacion3 = models.CharField(max_length=500, editable=True,blank=True, null=True)
    #medicoInterpretacion3 = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,  on_delete=models.PROTECT, related_name='medInterpreta3')
    medicoInterpretacion3  = models.ForeignKey('clinico.Medicos', blank=True,null= True, editable=True, on_delete=models.PROTECT,   related_name='interpreta03')
    fechaInterpretacion3 = models.DateTimeField(blank=True, null=True)
    resultado = models.CharField(max_length=20000, editable=True,blank=True, null=True)
    medicoReporte = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,  on_delete=models.PROTECT, related_name='medReporte')
    fechaReporte = models.DateTimeField(blank=True, null=True)
    opinion = models.CharField(max_length=1000, editable=True,blank=True, null=True)
    facturado = models.CharField(max_length=1, choices=FLAG_CHOICES,default='N',editable=True ,blank=True, null=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, editable=True, default = 'N')
    usuarioAnula = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,  on_delete=models.PROTECT, related_name='usuarioAnula1')
    rutaImagen = models.CharField(max_length=100, blank=True, null=True ,default='')
    rutaVideo = models.CharField(max_length=100, default='',blank=True, null=True)
    estadoExamenes = models.ForeignKey('clinico.EstadoExamenes', default=1, on_delete=models.PROTECT)
    observaciones = models.CharField(max_length=2000, editable=True,blank=True, null=True)
    usuaroRegistra = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT, related_name='usuarioRegistra1')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.codigoCups)

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]


class HistoriaResultados(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('N', 'Inactivo'), ]


    id = models.AutoField(primary_key=True)
    #historia = models.ForeignKey('clinico.Historia', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    historiaExamenes = models.ForeignKey('clinico.HistoriaExamenes', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    #dependenciasRealizado = models.ForeignKey('sitios.Dependencias', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaServicio = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    fechaResultado = models.DateTimeField(default=now, blank=True, null=True, editable=True)
    examenesRasgos = models.ForeignKey('clinico.ExamenesRasgos', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    valor =  models.CharField(max_length=20,  blank=True, null=True, editable=True)
    observaciones =  models.CharField(max_length=255,  blank=True, null=True, editable=True)
    consecResultado = models.IntegerField(default=0, blank=True, null=True, editable=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.historiaExamenes

    class Meta:
        indexes = [
            Index(fields=['historiaExamenes']),
        ]


class TiposDiagnostico(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('N', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES,  default='A', editable=False)

    def __str__(self):
        return self.nombre



class Diagnosticos(models.Model):
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    cie10  = models.CharField(max_length=15, default='')
    nombre = models.CharField(max_length=300 , null=False)
    descripcion = models.CharField(max_length=300)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    edadIni = models.IntegerField(editable=True, null=True, blank=True)
    edadFin = models.IntegerField(editable=True, null=True, blank=True)
    flagSivigila = models.CharField(max_length=1, default='A', editable=False, choices=FLAG_CHOICES)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    #usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class EstadosSalida(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class HistorialIncapacidades(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='DocumentoHistoriaDiag10')
    #ordenMedica = models.CharField(max_length=80, blank=True, null=True)
    tiposIncapacidad =  models.ForeignKey('clinico.TiposIncapacidad',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    desdeFecha = models.DateField(default=now ,blank=True, null=True)
    hastaFecha = models.DateField(default=now ,blank=True, null=True)
    numDias  = models.IntegerField(editable=True, null=True, blank=True)
    descripcion = models.CharField(max_length=4000 ,blank=True, null=True)
    diagnosticosIncapacidad = models.ForeignKey('clinico.Diagnosticos',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.historia

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]



class HistorialDiagnosticos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia =  models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag8')
    tiposDiagnostico = models.ForeignKey('clinico.TiposDiagnostico',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='tiposDiagnostico')
    diagnosticos =  models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='dxPpal')
    consecutivo = models.IntegerField(blank=True, null=True)
    observaciones = models.CharField(max_length=2000 ,blank=True, null=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.historia

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]



class HistorialEnfermedades(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia =  models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='historia_32')
    enfermedad = models.ForeignKey('clinico.Enfermedades',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='enfer001')
    observaciones = models.CharField(max_length=2000 ,blank=True, null=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.historia

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]


class HistorialAntecedentes(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia =  models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,  related_name='DocumentoHistoriaDiag9')
    tiposAntecedente = models.ForeignKey('clinico.TiposAntecedente', on_delete=models.PROTECT, null=False)
    #antecedentes  = models.ForeignKey('clinico.Antecedentes', on_delete=models.PROTECT, null=False)
    descripcion = models.CharField(max_length=200)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('usuarios.Usuarios',  blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.descripcion

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]


## Desde aquip ingresar en Admin

class Regimenes(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class TiposCotizante(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class Eps(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class TiposSalidas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class TurnosEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre


class TiposTriage(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class NivelesClinica(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class RevisionSistemas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class Recomendaciones(models.Model):

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Hallazgos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag13')
    nombre = models.CharField(max_length=50)
    miembrosSuperiores = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    miembrosInferiores = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    columna = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    ojos = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    nariz = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    oidos = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    cara = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    neurologicos = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    fxCraneo = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    torax = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    abdomen = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    exaMdGeneral = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    factorTvp = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    cuello = models.CharField(max_length=1, default='N', choices=FLAG_CHOICES, )
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre



class NivelesRegimenes(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    regimen = models.ForeignKey('clinico.Regimenes', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    porCuotaModeradora = models.DecimalField(max_digits=5, decimal_places=2)
    porCopago = models.DecimalField(max_digits=5, decimal_places=2)
    porTopeEve = models.DecimalField(max_digits=5, decimal_places=2)
    porTopeAnual = models.DecimalField(max_digits=5, decimal_places=2)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(self.regimen)


class Ips(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id       = models.AutoField(primary_key=True)
    nombre  =  models.CharField(max_length=30, blank=True,null= True, editable=True,)
    fechaRegistro = models.DateTimeField(default=now, blank=True,null= True, editable=True, )
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class Grupos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    grupo = models.CharField(max_length=80, blank=True, null=True, editable=False)
    nombre = models.CharField(max_length=80, blank=True, null=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombred)

class SubGrupos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    grupo = models.ForeignKey('clinico.Grupos', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=80, blank=True, null=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class ViasAdministracion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    ripsViasAdministracion = models.ForeignKey('rips.RipsViasAdministracion', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class UnidadesDeMedida(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nomenclatura = models.CharField(max_length=50, blank=True, null=True, editable=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES,  default='A', editable=False)

    def __str__(self):
        return str(self.descripcion)

class Presentacion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)


class FormasFarmaceuticas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class UnidadesDeMedidaDosis(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    unidadaDeMedidaPrincipioA = models.CharField(max_length=50, blank=True, null=True, editable=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.descripcion)


class FrecuenciasAplicacion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    numeroHoras =  models.IntegerField( blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.descripcion)

class IndicacionesEspeciales(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.descripcion)


class TiposMedicamento(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)

class MedicamentosDci(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    descripcionDciConcentracion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    tipoMedicamento = models.ForeignKey('clinico.TiposMedicamento', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)


class ExpedienteDCI(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    #formaFarmaceutica = models.ForeignKey('clinico.FormasFarmaceuticas', blank=True, null=True, editable=True,  on_delete=models.PROTECT)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.id)

class TiposDispositivoMedico(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.descripcion)

class TiposProductosNutricion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True, editable=True)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)

class ProductosNutricion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigoMipres = models.DecimalField(max_digits=5, decimal_places=0 , blank=True, null=True, editable=True)
    nombreComercial = models.CharField(max_length=100, blank=True, null=True, editable=True)
    grupo =  models.CharField(max_length=100, blank=True, null=True, editable=True)
    formaFarmaceutica = models.ForeignKey('clinico.FormasFarmaceuticas', blank=True, null=True, editable=True,  on_delete=models.PROTECT)
    presentacion = models.ForeignKey('clinico.Presentacion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    unidades = models.ForeignKey('clinico.UnidadesDeMedida', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    habilitadoMipres = models.CharField(max_length=1, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.id)

class SignosVitales(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag23')
    fecha = models.DateTimeField(default=now ,blank=True, null=True)
    frecCardiaca = models.CharField(max_length=5,null=True,  blank=True)
    frecRespiratoria = models.CharField(max_length=5,null=True,  blank=True)
    tensionADiastolica = models.CharField(max_length=5,null=True,  blank=True)
    tensionASistolica = models.CharField(max_length=5,null=True,  blank=True)
    tensionAMedia = models.CharField(max_length=5,null=True,  blank=True)
    temperatura = models.CharField(max_length=5,null=True,  blank=True)
    saturacion = models.CharField(max_length=5,null=True,  blank=True)
    glucometria = models.CharField(max_length=5,null=True,  blank=True)
    glasgow = models.CharField(max_length=5,null=True,  blank=True)
    apache = models.CharField(max_length=5,null=True,  blank=True)
    pvc = models.CharField(max_length=5,null=True,  blank=True)
    cuna = models.CharField(max_length=5,null=True,  blank=True)
    ic = models.CharField(max_length=5,null=True,  blank=True)
    glasgowOcular = models.CharField(max_length=5,null=True,  blank=True)
    glasgowVerbal = models.CharField(max_length=5,null=True,  blank=True)
    glasgowMotora = models.CharField(max_length=5,null=True,  blank=True)
    observacion = models.CharField(max_length=5000, null=True, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)

class HistoriaSignosVitales(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaSig2')
    fecha = models.DateTimeField(default=now ,blank=True, null=True)
    frecCardiaca = models.CharField(max_length=5,null=True,  blank=True)
    frecRespiratoria = models.CharField(max_length=5,null=True,  blank=True)
    tensionADiastolica = models.CharField(max_length=5,null=True,  blank=True)
    tensionASistolica = models.CharField(max_length=5,null=True,  blank=True)
    tensionAMedia = models.CharField(max_length=5,null=True,  blank=True)
    temperatura = models.CharField(max_length=5,null=True,  blank=True)
    saturacion = models.CharField(max_length=5,null=True,  blank=True)
    glucometria = models.CharField(max_length=5,null=True,  blank=True)
    glasgow = models.CharField(max_length=5,null=True,  blank=True)
    apache = models.CharField(max_length=5,null=True,  blank=True)
    pvc = models.CharField(max_length=5,null=True,  blank=True)
    cuna = models.CharField(max_length=5,null=True,  blank=True)
    ic = models.CharField(max_length=5,null=True,  blank=True)
    glasgowOcular = models.CharField(max_length=5,null=True,  blank=True)
    glasgowVerbal = models.CharField(max_length=5,null=True,  blank=True)
    glasgowMotora = models.CharField(max_length=5,null=True,  blank=True)
    observacion = models.CharField(max_length=5000, null=True, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['historia'], name='signosVitales_idx1'),

        ]

    def __str__(self):
        return str(self.id)

class HistoriaRevisionSistemas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaRev1')
    revisionSistemas = models.ForeignKey('clinico.RevisionSistemas', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    observacion = models.CharField(max_length=5000, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]


class Trasfusiones(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag25')
    #ordenMedica = models.CharField(max_length=80, blank=True, null=True)
    fecha = models.DateTimeField()
    selloCalidad = models.CharField(max_length=5000, blank=True)
    grupoBolsa = models.CharField(max_length=50, blank=True)
    fechaCaducidad = models.DateTimeField()
    realizoTrasfusion = models.CharField(max_length=50, blank=True)
    trasfusionInicio = models.CharField(max_length=50, blank=True)
    trasfusionFinal = models.CharField(max_length=50, blank=True)
    complicaciones = models.CharField(max_length=5000, blank=True)
    tipoComponente = models.CharField(max_length=50, blank=True)
    epicrisis = models.CharField(max_length=5000, blank=True)
    compReactRtha = models.CharField(max_length=15, blank=True)
    compEnfInjerto = models.CharField(max_length=15, blank=True)
    compSobreCargaCirc = models.CharField(max_length=15, blank=True)
    compLesPulmonar = models.CharField(max_length=15, blank=True)
    compReacAlergica = models.CharField(max_length=15, blank=True)
    compSepsis = models.CharField(max_length=15, blank=True)
    compPurpPostTrans = models.CharField(max_length=15, blank=True)
    compReacFHemolitica = models.CharField(max_length=15, blank=True)
    compReacFNoHemolitica = models.CharField(max_length=15, blank=True)
    compEmboAereo = models.CharField(max_length=15, blank=True)
    compHipocalemia = models.CharField(max_length=15, blank=True)
    compHipotermia = models.CharField(max_length=15, blank=True)
    compTransMasiva = models.CharField(max_length=15, blank=True)
    compEscalofrios = models.CharField(max_length=15, blank=True)
    compOtro = models.CharField(max_length=15, blank=True)
    compOtroDesc = models.CharField(max_length=2000, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,     on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.historia)


class HistoriaOxigeno(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag29')
    #ordenMedica = models.CharField(max_length=80, blank=True, null=True)
    fechaInicio = models.DateTimeField()
    fechaFinal = models.DateTimeField()
    tipoOxigenacion = models.ForeignKey('clinico.TipoOxigenacion',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='tipoOxigenacion02')
    aire = models.CharField(max_length=1, blank=True)
    saturacionOxigeno = models.DecimalField(max_digits=3, decimal_places=2)
    #flujoLtsOxigeno = models.DecimalField(max_digits=3, decimal_places=2)
    #flujoLtsAire = models.DecimalField(max_digits=3, decimal_places=2)
    horasOxigeno = models.DecimalField(max_digits=3, decimal_places=2)
    horasAire = models.DecimalField(max_digits=3, decimal_places=2)
    totalLtsoxigeno = models.DecimalField(max_digits=3, decimal_places=2)
    totalLtsAire = models.DecimalField(max_digits=3, decimal_places=2)
    totalMetrocubicoOxigeno = models.DecimalField(max_digits=3, decimal_places=2)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.tipoOxigenacion)

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]


class TipoOxigenacion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    flujoLtsOxigeno = models.DecimalField(max_digits=3, decimal_places=0)
    flujoLtsAire = models.DecimalField(max_digits=3, decimal_places=0)
    codFacturar =  models.CharField(max_length=30, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)



class ImHaloTerapia(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag27')
    fecha = models.DateTimeField()
    salbutamol = models.CharField(max_length=50, blank=True)
    ipratropio = models.CharField(max_length=50, blank=True)
    beclometazona = models.CharField(max_length=50, blank=True)
    berudual = models.CharField(max_length=50, blank=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)


    def __str__(self):
        return str(self.historia)

class Antibiotico(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoriaDiag28')
    fechaSolicitud = models.DateTimeField()
    fechaInicio = models.DateTimeField()
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True, on_delete=models.PROTECT ,related_name='sumins03')
    profilaxis = models.CharField(max_length=10, blank=True, null=True, editable=True)
    ttoEmpirico = models.CharField(max_length=10, blank=True, null=True, editable=True)
    ttoetiologico = models.CharField(max_length=10, blank=True, null=True, editable=True)
    ampliacionTto = models.CharField(max_length=10, blank=True, null=True, editable=True)
    cambioEsquema = models.CharField(max_length=10, blank=True, null=True, editable=True)
    saludPublica = models.CharField(max_length=10, blank=True, null=True, editable=True)
    dxInfeccion = models.CharField(max_length=1000, blank=True, null=True, editable=True)
    germenAislado = models.CharField(max_length=1000, blank=True, null=True, editable=True)
    fechaVigencia = models.DateTimeField()
    fallaRenal = models.CharField(max_length=10, blank=True, null=True, editable=True)
    fallaHepatica = models.CharField(max_length=10, blank=True, null=True, editable=True)
    infeccionSevera = models.CharField(max_length=10, blank=True, null=True, editable=True)
    inmunoSupresion = models.CharField(max_length=10, blank=True, null=True, editable=True)
    aprobado = models.CharField(max_length=15, blank=True, null=True, editable=True)
    prescripcion = models.CharField(max_length=1000, blank=True, null=True, editable=True)
    protocolo = models.CharField(max_length=1000, blank=True, null=True, editable=True)
    noProtocolo = models.CharField(max_length=1000, blank=True, null=True, editable=True)
    ajustadoCultivo = models.CharField(max_length=1000, blank=True, null=True, editable=True)
    ajustadoDosiRenal = models.CharField(max_length=1000, blank=True, null=True, editable=True)
    autInfectologia = models.CharField(max_length=2, blank=True, null=True, editable=True)
    observacionEpidemilogia = models.CharField(max_length=10000, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.historia)

class Medicamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True, editable=True)
    def __str__(self):
        return str(self.id)
	
class HistoriaMedicamentos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]

    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia', default=1, on_delete=models.PROTECT, null=False, related_name='DocumentoHistoriaDiag12')
    #ordenMedica = models.CharField(max_length=80, blank=True, null=True)
    item = models.CharField(max_length=5, blank=True, null=True)
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    dosisCantidad = models.DecimalField(max_digits=20, decimal_places=3)
    dosisUnidad = models.ForeignKey('clinico.UnidadesDeMedidaDosis', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    frecuencia = models.ForeignKey('clinico.FrecuenciasAplicacion', blank=True, null=True, editable=True,               on_delete=models.PROTECT)
    viaAdministracion = models.ForeignKey('clinico.ViasAdministracion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    concentracionMedicamento = 	models.CharField(max_length=100, blank=True, null=True)
    nota = models.CharField(max_length=5000, blank=True , null=True)
    #autorizacion = models.ForeignKey('autorizaciones.AutorizacionesDetalle', blank=True, null=True, editable=True, on_delete=models.PROTECT , related_name='aut02') 
    autorizacion_id = models.DecimalField(max_digits=10, decimal_places=0 , blank=True, null=True, editable=True)
    cantidadOrdenada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    diasTratamiento =  models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadSolicitada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadEntregada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadDispensada = models.ForeignKey('rips.RipsUnidadUpr', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    cantidadAplicada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadDevuelta = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadfacturada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    nopos = models.CharField(max_length=1, blank=True, null=True, editable=True)
    estadoMedicamento = models.CharField(max_length=1, blank=True, null=True, editable=True)
    horarioDosis = models.CharField(max_length=200, blank=True, null=True, editable=True)
    dosisUnica = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True )
    dosisRescate = models.CharField(max_length=200, blank=True, null=True, editable=True)
    dosisProfilaxis = models.CharField(max_length=200, blank=True, null=True, editable=True)
    dosisAdelanto = models.CharField(max_length=200, blank=True, null=True, editable=True)
    urgente = models.CharField(max_length=1,choices=FLAG_CHOICES,  blank=True, null=True, editable=True)
    dosificacion = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    antibiotico = models.CharField(max_length=1,choices=FLAG_CHOICES,  blank=True, null=True, editable=True)
    fechaSuspension = models.DateTimeField( blank=True, null=True, editable=True)
    consecutivoLiquidacion = models.IntegerField(blank=True, null=True)
    consecutivoMedicamento = models.IntegerField(blank=True, null=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.historia)

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]


class PrincipiosActivos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=300, null=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.nombre

class CodigosAtc(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, blank=True, null=True, editable=True)
    nombre = models.CharField(max_length=50, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return str(self.codigo)


class ExamenesRasgos(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    tiposExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT, null=False)
    codigoCups = models.CharField(max_length=20, null=False, blank=True)
    nombre = models.CharField(max_length=80, null=False)
    unidad = models.CharField(max_length=20, null=False)
    minimo = models.CharField(max_length=20, null=False)
    maximo = models.CharField(max_length=20, null=False)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class TipoDietas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null = False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False )

    def __str__(self):
        return self.nombre

class HistorialDietas(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia =  models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='Dietas001g8')
    tipoDieta = models.ForeignKey('clinico.TipoDietas',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='tipoDietas001')
    consecutivo = models.IntegerField(blank=True, null=True)
    observaciones = models.CharField(max_length=2000 ,blank=True, null=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.observaciones

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]


class HistorialNotasEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='NotaEnfHistoria001')
    observaciones = models.CharField(max_length=4000 ,blank=True, null=True)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return self.historia

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]

class HistorialCirugias(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    historia =  models.ForeignKey('clinico.Historia',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='historia_3223')
    cirugia =  models.ForeignKey('cirugia.Cirugias',  blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='cirugia_3221')
    observaciones = models.CharField(max_length=2000 ,blank=True, null=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.historia

    class Meta:
        indexes = [
            Index(fields=['historia']),
        ]
