from django.db import models

# Create your models here.

class TiposTurnosEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]


    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_377')
    nombre = models.CharField(max_length=50, blank=False, null=False,  editable = True)
    horario = models.CharField(max_length=50, default='A', editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT ,   related_name='usuarioenf01')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.nombre)


class TurnosEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]

    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_398')
    tiposTurnosEnfermeria = models.ForeignKey('enfermeria.TiposTurnosEnfermeria',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='tiposTurno01')  
    #nombre = models.CharField(max_length=50, blank=False, null=False,  editable = True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='serenf01')
    enfermeraTurno = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,    on_delete=models.PROTECT ,   related_name='usuarioenf02')
    estadoReg = models.CharField(max_length=1,  choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.id)

class CuidadosEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica378')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaCuidadosEnfermeria01')
    turno = models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    barraSeguridad = models.CharField(max_length=3000, blank=False, null=False, editable=True)
    cambioCama = models.CharField(max_length=100, blank=False, null=False, editable=True)
    cambioPañal = models.CharField(max_length=100, blank=False, null=False, editable=True)
    heridas = models.CharField(max_length=100, blank=False, null=False, default='L' , editable = True)
    prevenirUlceras = models.CharField(max_length=100, blank=False, null=False,      editable = True)
    nutricion = models.CharField(max_length=100, blank=False, null=False,            editable = True)
    ostomia = models.CharField(max_length=100, blank=False, null=False,      editable = True)
    realizaBaño = models.CharField(max_length=100, blank=False, null=False,   editable = True)
    lavadoManos = models.CharField(max_length=100, blank=False, null=False,   editable = True)
    recibeVisitas = models.CharField(max_length=100, blank=False, null=False,          editable = True)
    retiroVendajes = models.CharField(max_length=100, blank=False, null=False,   editable = True)
    sondasDrenes = models.CharField(max_length=100, blank=False, null=False,         editable = True)
    soporteO2 = models.CharField(max_length=100, blank=False, null=False,       editable = True)
    trasladoProcedimiento = models.CharField(max_length=100, blank=False, null=False,  editable = True)
    trasladoEgreso = models.CharField(max_length=100, blank=False, null=False,          editable = True)
    observaBarreraSeguridad = models.CharField(max_length=2000, blank=False, null=False,          editable = True)
    observaCambioCama = models.CharField(max_length=2000, blank=False, null=False,          editable = True)
    observacambioPañal = models.CharField(max_length=2000, blank=False, null=False,   editable = True)
    observaHeridas = models.CharField(max_length=2000, blank=False, null=False,   editable = True)
    observaPrevenirUlceras = models.CharField(max_length=2000, blank=False, null=False,           editable = True)
    observaNutricion = models.CharField(max_length=2000, blank=False, null=False,    editable = True)
    obsostomia = models.CharField(max_length=2000, blank=False, null=False,      editable = True)
    observaRealizoBaño = models.CharField(max_length=2000, blank=False, null=False,    editable = True)
    observaLavadoManos = models.CharField(max_length=2000, blank=False, null=False,        editable = True)
    observaRecibeVisitas = models.CharField(max_length=2000, blank=False, null=False,   editable = True)
    observaRetiroVendajes = models.CharField(max_length=2000, blank=False, null=False,    editable = True)
    observaSondasDrenes = models.CharField(max_length=2000, blank=False, null=False,          editable = True)
    bservaSoporteO2 = models.CharField(max_length=2000, blank=False, null=False,   editable = True)
    observaTrasladoProcedimiento = models.CharField(max_length=2000, blank=False, null=False,   editable = True)
    observaTrasladoEgreso = models.CharField(max_length=2000, blank=False, null=False,   editable = True)
    fechaRegistro = models.DateTimeField()
    horaRegistro = models.CharField(max_length=5, blank=False, null=False,             editable = True)
    dispositivosVasculares = models.CharField(max_length=3000, blank=False, null=False,   editable = True)
    observaDispositivosVasculares = models.CharField(max_length=3000, blank=False, null=False,   editable = True)
    cirugia = models.ForeignKey('cirugia.Cirugias', blank=True, null=True, editable=True,on_delete=models.PROTECT)
    dosisProf1 = models.CharField(max_length=50, blank=False, null=False,   editable = True)
    observaDosisProf1 = models.CharField(max_length=1000, blank=False, null=False,     editable = True)
    horaMedProf1 = models.CharField(max_length=5, blank=False, null=False,            editable = True)
    segundaDosis = models.CharField(max_length=50, blank=False, null=False,             editable = True)
    observaSegundaDosis = models.CharField(max_length=1000, blank=False, null=False,  editable = True)
    horaSegundaDosis = models.CharField(max_length=5, blank=False, null=False,   editable = True)
    diuresis = models.CharField(max_length=50, blank=False, null=False,          editable = True)
    observaDiuresis = models.CharField(max_length=5000, blank=False, null=False,      editable = True)
    dolor = models.CharField(max_length=50, blank=False, null=False,     editable = True)
    observaDolor = models.CharField(max_length=5000, blank=False, null=False,            editable = True)
    drenes = models.CharField(max_length=50, blank=False, null=False,         editable = True)
    observaDrenes = models.CharField(max_length=5000, blank=False, null=False,   editable = True)
    funcional = models.CharField(max_length=50, blank=False, null=False,             editable = True)
    observaFuncional = models.CharField(max_length=5000, blank=False, null=False,          editable = True)
    heridasCuraciones = models.CharField(max_length=50, blank=False, null=False,        editable = True)
    observaHeridasCuraciones = models.CharField(max_length=5000, blank=False, null=False,     editable = True)
    hospitaliacion = models.CharField(max_length=50, blank=False, null=False,    editable = True)
    observaHospitalizacion = models.CharField(max_length=5000, blank=False, null=False,   editable = True)
    liquidosCv = models.CharField(max_length=50, blank=False, null=False,            editable = True)
    observaLiquidosCv = models.CharField(max_length=5000, blank=False, null=False,           editable = True)
    sondaNasogastrica = models.CharField(max_length=100, blank=False, null=False,      editable = True)
    observaSondaNasogastrica = models.CharField(max_length=5000, blank=False, null=False,        editable = True)
    sondaVesical = models.CharField(max_length=50, blank=False, null=False,             editable = True)
    observaSondaVesical = models.CharField(max_length=5000, blank=False, null=False,             editable = True)
    trasladoCx = models.CharField(max_length=100, blank=False, null=False,        editable = True)
    observaTrasladoCx = models.CharField(max_length=2000, blank=False, null=False, editable = True)
    dispositivosOrtopedicos = models.CharField(max_length=100, blank=False, null=False,  editable = True)
    observaDispositivosOrtopedicos = models.CharField(max_length=2000, blank=False, null=False,             editable = True)
    reduccionCerrada = models.CharField(max_length=100, blank=False, null=False,        editable = True)
    observaReduccionCerrada = models.CharField(max_length=2000, blank=False, null=False,      editable = True)
    suturas = models.CharField(max_length=50, blank=False, null=False,     editable = True)
    observaSuturas = models.CharField(max_length=5000, blank=False, null=False,             editable = True)
    inmovilizacion = models.CharField(max_length=50, blank=False, null=False,          editable = True)
    observaInmovilizacion = models.CharField(max_length=5000, blank=False, null=False,    editable = True)
    curacion = models.CharField(max_length=50, blank=False, null=False,    editable = True)
    observaCuracion =models.CharField(max_length=5000, blank=False, null=False,             editable = True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,   on_delete=models.PROTECT ,   related_name='usuarioenf03')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)


    def __str__(self):
        return str(self.id)

class DolorEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica379')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaDolorEnfermeria01')
    turno = models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True, null=True, editable=True,     on_delete=models.PROTECT)
    fechaCreacion = models.DateTimeField()
    zona = models.CharField(max_length=3000, blank=False, null=False, editable=True)
    dolorPorcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    dolorDescripcion = models.CharField(max_length=100, blank=False, null=False, editable=True)
    lateralidad = models.CharField(max_length=100, blank=False, null=False, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.dolorDescripcion)

class HeridasEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica380')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaHeridasEnfermeria01')
    turno = models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True, null=True, editable=True,        on_delete=models.PROTECT)
    area = models.CharField(max_length=3000, blank=False, null=False, editable=True)
    tipoHerida = models.CharField(max_length=100, blank=False, null=False, editable=True)
    diasPop = models.CharField(max_length=100, blank=False, null=False, editable=True)
    tamaño = models.CharField(max_length=100, blank=False, null=False, editable=True)
    estado = models.CharField(max_length=100, blank=False, null=False, editable=True)
    materialOrganico = models.BooleanField()
    enrojecimiento = models.BooleanField()
    necrosis =models.BooleanField()
    secrecion = models.BooleanField()
    edema = models.BooleanField()
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,            on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.historia)

class TipoBalanceLiquidosEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=False, null=False,            editable = True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.nombre)

class PosicionPacientesEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica381')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaPosicionEnfermeria01')
    fecha = models.DateTimeField()
    turno = models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True, null=True, editable=True,      on_delete=models.PROTECT)
    horario = models.CharField(max_length=3000, blank=False, null=False, editable=True)
    posicion = models.CharField(max_length=100, blank=False, null=False, editable=True)
    realizado = models.CharField(max_length=100, blank=False, null=False, editable=True)
    observaciones = models.CharField(max_length=20000, blank=False, null=False, editable=True)
    zonaPresion = models.CharField(max_length=20000, blank=False, null=False, editable=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True,           on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)


    def __str__(self):
        return str(self.nombre)



class NotasEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica383')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaNotasEnfermeria01')
    turno = models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True, null=True, editable=True,       on_delete=models.PROTECT)
    tipoNota = models.CharField(max_length=3000, blank=False, null=False, editable=True)
    nota = models.CharField(max_length=20000, blank=False, null=False, editable=True)
    fecha = models.DateTimeField()
    tipoEvento = models.CharField(max_length=2000, blank=False, null=False, editable=True)
    descripcion = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    actividadPrevencion = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    notificacionevento = models.CharField(max_length=500, blank=False, null=False, editable=True)
    selloCalidad = models.CharField(max_length=5, blank=False, null=False, editable=True)
    grupoSanguineo = models.CharField(max_length=100, blank=False, null=False, editable=True)
    fechaVencimiento = models.DateTimeField()
    accesoVenoso = models.CharField(max_length=2000, blank=False, null=False, editable=True)
    volumenHemocomponente = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    signosVitales = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    acompañamientoMedico = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    tripulacionAmbulancia = models.CharField(max_length=2000, blank=False, null=False, editable=True)
    movil = models.CharField(max_length=3000, blank=False, null=False, editable=True)
    auxiliarEncargado = models.CharField(max_length=100, blank=False, null=False, editable=True)
    traslado = models.CharField(max_length=500, blank=False, null=False, editable=True)
    estadoPaciente = models.CharField(max_length=1000, blank=False, null=False, editable=True)
    soporte = models.CharField(max_length=500, blank=False, null=False, editable=True)
    estadoPiel = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    acompañante = models.ForeignKey('usuarios.UsuariosContacto', blank=True, null=True, editable=True,
                                    on_delete=models.PROTECT)
    entregaDocumentos = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    duracionMasaje = models.CharField(max_length=500, blank=False, null=False, editable=True)
    codigoHuella = models.CharField(max_length=100, blank=False, null=False, editable=True)
    epicrisis = models.CharField(max_length=5000, blank=False, null=False, editable=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False)

    def __str__(self):
        return str(self.historia)


class BalanceLiquidosEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica384')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaBalanceLiquidosEnfermeria01')
    turno= models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fecha=models.DateTimeField()
    tipo=models.ForeignKey('enfermeria.TipoBalanceLiquidosEnfermeria', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    liquido=models.DecimalField(max_digits=5, decimal_places=0)
    horaUno=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaDos = models.CharField(max_length=100, blank=False, null=False, editable=True)
    horaTres=models.CharField(max_length=100, blank=False,null= False, editable=True)
    horaCuatro=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaCinco=		models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaSeis=models.CharField(max_length=100, blank=False,null= False, editable=True)
    horaSiete=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaOcho=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaNueve=models.CharField(max_length=100, blank=False,null= False, editable=True)
    horaDiez=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaOnce=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaDoce=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaTrece=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaCatorce=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaQuince=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaDiezYSeis=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaDiezYSiete= models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaDiezYOcho=models.CharField(max_length=100, blank=False,null= False, editable=True)
    horaDiezYNueve=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaVeinte=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaVeinteYUno=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaVeinteyDos=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaVeinteyTres=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaVeinteyCuatro=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    adminMañana=	 models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='admin001')
    adminTarfe=models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='admin002')
    adminNoche=models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='admin003')
    medicamento=models.IntegerField(default=0)  #NO SE POR EL MOMENTO ASIP
    totalAdministrado= models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    residuoMezclas=models.IntegerField(default=0)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False)

    def __str__(self):
        return str(self.historia)

class SignosEnfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica385')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaSignosEnfermeria01')
    turno= models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    fecha=models.DateTimeField()
    taSistolica=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    taDiastolica=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    taMedia=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    frecuenciaCardiaca=models.CharField(max_length=100, blank=False,null= False, editable=True)
    frecuenciaRespiratoria=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    temperatura=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    pvc=models.CharField(max_length=100, blank=False,null= False, editable=True)
    glucometria=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    saturacionO=models.CharField(max_length=100, blank=False,null= False, editable=True)
    pia=models.CharField(max_length=100, blank=False,null= False, editable=True)
    pulsoPeriferico=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    unidadesinsulina=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    glasgowVerbal=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    glasgowOcular=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    glasgowTotal=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    pupilasOdt=models.CharField(max_length=100, blank=False,null= False, editable=True)
    pupilasOdr=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    pupilasOir=models.CharField(max_length=100, blank=False,null= False, editable=True)
    pic=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    pam=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    fuerzaMsd=models.CharField(max_length=100, blank=False,null= False, editable=True)
    fuerzaMsi=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    fuerzaMid=models.CharField(max_length=100, blank=False,null= False, editable=True)
    fuerzaMii=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    ppc=models.CharField(max_length=100, blank=False,null= False, editable=True)
    uniddesDeInsulina=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    tipo=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    reflejos=models.CharField(max_length=100, blank=False,null= False, editable=True)
    sensibilidad=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    cefalea=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    marcha=models.CharField(max_length=100, blank=False,null= False,editable=True)
    vomito=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    memoria=models.CharField(max_length=100, blank=False,null= False, editable=True)
    coordinacion=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    rigidezEsfiter=models.CharField(max_length=100, blank=False,null= False, editable=True)
    tos=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    disnea=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    cianosis=models.CharField(max_length=100, blank=False,null= False, editable=True)
    sdra=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    dolorToraxico=models.CharField(max_length=100, blank=False,null= False,editable=True)
    hemoptisis=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    dolorAbdominal=	models.CharField(max_length=100, blank=False,null= False,  editable=True)
    presenciaHematemesis=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    signosIrritacion=models.CharField(max_length=100, blank=False,null= False, editable=True)
    melenas=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    presenciaDeposicion=models.CharField(max_length=100, blank=False,null= False, editable=True)
    vomitoGastro=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    doopler=models.CharField(max_length=100, blank=False,null= False, editable=True)
    lividez=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    pulsos=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    llenadoCapilar=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    controlPerimetro=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    ansiedad=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    continuaObservacion=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    horaVitales=	models.CharField(max_length=5, blank=False,null= False, editable=True)
    horaNeurologica=models.CharField(max_length=5, blank=False,null= False, editable=True)
    horaRespiratoria=models.CharField(max_length=5, blank=False,null= False,  editable=True)
    horaGastroIntestinal=models.CharField(max_length=5, blank=False,null= False,  editable=True)
    horaVasculares=	models.CharField(max_length=5, blank=False,null= False,  editable=True)
    usuSignosNeurologicos=models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='usu12')
    usuCompresp=models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='usu13')
    usuGastro=models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='usu14')
    usuCompVascular=	models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT ,  related_name='usu15')
    ta=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    deposicion=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    glasgow=models.CharField(max_length=100, blank=False,null= False, editable=True)
    hematemesis=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    hemotitis=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    diuresis=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    observaDiuresis=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    dolor=models.CharField(max_length=100, blank=False,null= False,  editable=True)
    observaDolor=models.CharField(max_length=50, blank=False,null= False, editable=True)
    drenes=models.CharField(max_length=50, blank=False,null= False, editable=True)
    observaDrenes=models.CharField(max_length=50, blank=False,null= False, editable=True)
    funcional=models.CharField(max_length=50, blank=False,null= False, editable=True)
    observaFuncional=models.CharField(max_length=50, blank=False,null= False,  editable=True)
    suturas=models.CharField(max_length=50, blank=False,null= False,  editable=True)
    observaSuturas=models.CharField(max_length=50, blank=False,null= False, editable=True)
    inmovilizacion=models.CharField(max_length=50, blank=False,null= False,  editable=True)
    observaInmovilizacion=models.CharField(max_length=50, blank=False,null= False,  editable=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True,null= True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES,  default='A', editable=False)



    def __str__(self):
        return str(self.id)


class Enfermeria(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica386')
    historia = models.ForeignKey('clinico.Historia', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='HistoriaEnfermeria01')
    ingresoPaciente =   models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    serviciosAdministrativos = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servAdmEnfermeria101')
    tipoOrigen = models.ForeignKey('enfermeria.EnfermeriaTipoOrigen', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='TipoEnfermeria01')
    tipoMovimiento = models.ForeignKey('enfermeria.EnfermeriaTipoMovimiento', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='TipoEnfermeria02')
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3460')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES,default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.historia)

class EnfermeriaDetalle(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    enfermeria = models.ForeignKey('enfermeria.Enfermeria', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='Enfermeria01')
    historiaMedicamentos = models.ForeignKey('clinico.HistoriaMedicamentos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servAdmEnfermeria102')
    farmaciaDetalle = models.ForeignKey('farmacia.FarmaciaDetalle', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='farmaciaDetalle')
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    dosisCantidad = models.DecimalField(max_digits=20, decimal_places=3)
    dosisUnidad = models.ForeignKey('clinico.UnidadesDeMedidaDosis', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    viaAdministracion = models.ForeignKey('clinico.ViasAdministracion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    frecuencia = models.ForeignKey('clinico.FrecuenciasAplicacion', blank=True, null=True, editable=True,               on_delete=models.PROTECT)
    cantidadOrdenada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    diasTratamiento =  models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3462')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)


class EnfermeriaRecibe(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    enfermeriaDetalle = models.ForeignKey('enfermeria.EnfermeriaDetalle', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='EnfermeriaDetalle1101')
    despachos = models.ForeignKey('farmacia.FarmaciaDespachos', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='FarmaciaDispensa01')
    #item = models.CharField(max_length=5, blank=True, null=True)
    farmaciaDetalle = models.ForeignKey('farmacia.FarmaciaDetalle', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='farmaciaDetalle02')
    farmaciaDespachosDispensa = models.ForeignKey('farmacia.FarmaciaDespachosDispensa', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='farmaciaDespachosDispensa0222')
    #consecutivoMedicamento = models.IntegerField(blank=True, null=True)
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    dosisCantidad = models.DecimalField(max_digits=20, decimal_places=3)
    dosisUnidad = models.ForeignKey('clinico.UnidadesDeMedidaDosis', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    viaAdministracion = models.ForeignKey('clinico.ViasAdministracion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    #frecuencia = models.ForeignKey('clinico.FrecuenciasAplicacion', blank=True, null=True, editable=True,               on_delete=models.PROTECT)
    cantidadDispensada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadDevuelta = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    netoCantidad = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    #diasTratamiento =  models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3478')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)

class EnfermeriaPlaneacion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    enfermeria = models.ForeignKey('enfermeria.Enfermeria', blank=True, null=True, editable=True,   on_delete=models.PROTECT) 
    enfermeriaRecibe = models.ForeignKey('enfermeria.EnfermeriaRecibe', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='EnfermeriaRecibe1102')
    consecutivoPlaneacion = models.IntegerField(default=0)
    fechaPlanea = models.DateTimeField(editable=True, null=True, blank=True)
    fechaAplica = models.DateTimeField(editable=True, null=True, blank=True)
    suministro = models.ForeignKey('facturacion.Suministros', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    dosisCantidad = models.DecimalField(max_digits=20, decimal_places=3)
    dosisUnidad = models.ForeignKey('clinico.UnidadesDeMedidaDosis', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    viaAdministracion = models.ForeignKey('clinico.ViasAdministracion', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    frecuencia = models.ForeignKey('clinico.FrecuenciasAplicacion', blank=True, null=True, editable=True,               on_delete=models.PROTECT)
    cantidadDispensada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadPlaneada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    cantidadAplicada = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    diasTratamiento =  models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    turnoEnfermeriaPlanea = models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True, null=True, editable=True,   on_delete=models.PROTECT ,  related_name='EnfermeriaTipoTurno11012') 
    turnoEnfermeriaAplica = models.ForeignKey('enfermeria.TurnosEnfermeria', blank=True, null=True, editable=True,   on_delete=models.PROTECT ,  related_name='EnfermeriaTipoTurno11013') 
    enfermeraPlanea = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaEnfermeraPlanea3468')
    enfermeraAplica = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaEnfermera3468')
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3488')
    estadoReg = models.CharField(max_length=1, default='A', choices=ESTADOREG_CHOICES, editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)

class EnfermeriaTipoOrigen(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default='F', editable=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3467')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.nombre)

class EnfermeriaTipoMovimiento(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default='F', editable=True,  blank=True, null=True,)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='Planta3469')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.nombre)

class EnfermeriaDevolucion(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica3Enf9022')
    serviciosAdministrativosDevuelve = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servDevuelve3231')
    usuarioDevuelve = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaDevuelve4353')
    serviciosAdministrativosRecibe = models.ForeignKey('sitios.ServiciosAdministrativos', blank=True,null= True, editable=True,  on_delete=models.PROTECT,   related_name='servRecibe32431')
    usuarioRecibe = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaRecibe4553')
    #observaciones =  models.CharField(max_length=250,  editable=True,  blank=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaEnfermeriaia3453')
    estadoReg = models.CharField(max_length=1, choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)

class EnfermeriaDevolucionDetalle(models.Model):
    ESTADOREG_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'), ]
    FLAG_CHOICES = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    enfermeriaDevolucion = models.ForeignKey('enfermeria.EnfermeriaDevolucion', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='EnfermeriDevolos261201')
    enfermeriaRecibe = models.ForeignKey('enfermeria.EnfermeriaRecibe', on_delete=models.PROTECT, blank=True, null=True,  editable=True,  related_name='EnfermeriaRecibe201')
    cantidadDevuelta = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True, editable=True)
    observaciones =  models.CharField(max_length=250,  editable=True,  blank=True)
    anulado = models.CharField(max_length=1, choices=FLAG_CHOICES, default='N', blank=True, editable=False)
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT   , related_name='PlantaEnfermeria3453')
    estadoReg = models.CharField(max_length=1,choices=ESTADOREG_CHOICES, default='A', editable=False,  blank=True, null=True,)

    def __str__(self):
        return str(self.id)