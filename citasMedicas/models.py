from django.db import models
from django.utils import timezone


# Create your models here.
class Calendario(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica3021')
    fechaDia = models.DateField(default=timezone.now, editable=False)
    nombre = models.CharField(max_length=30, default="" , null = False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta349')
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)


    def __str__(self):
        return self.nombre


class TiposCitasMedicas(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,null= True, editable=False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class TiposAtencion(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,null= True, editable=False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class EstadosCitasMedicas(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,null= True, editable=False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class EstadosConsultorios(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,null= True, editable=False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class EstadosProgramacionCitasMedicas(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,null= True, editable=False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre


class Consultorios(models.Model):

    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ],
    ESTADO_CONSULTORIO = [
        ('D', 'Disponible'),
        ('N', 'No Disponible'),
        ('M', 'Mantenimiento'),
        ],
    DURACION_CITA = [
        ('Veinte', '20 Minutos'),
        ('Quince', '15 Minutos'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_453011')
    dependencia  = models.ForeignKey('sitios.Dependencias',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='dependencia1099')
    consultorio  =  models.ForeignKey('citasMedicas.Consultorios',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='consul01')
    nombre = models.CharField(max_length=30, default="" , null = False)
    dia  = models.DateField(default=timezone.now, editable=True)
    estadosConsultorios  =  models.ForeignKey('citasMedicas.EstadosConsultorios',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='estadosConsul01')
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta45')
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.dependencia


class AgendasMedicas(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_333011')
    especialidad = models.ForeignKey('clinico.Especialidades', blank=True,null= True, on_delete=models.PROTECT)
    especialidadesMedicos = models.ForeignKey('clinico.EspecialidadesMedicos',blank=True,null= True, on_delete=models.PROTECT)
    estadoAgenda = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta12')
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)


    def __integer__(self):
        return self.especialidadesMedicos

class AgendasMedicasProgramacion(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ],
    DURACION_CITA = [
        ('Veinte', '20 Minutos'),
        ('Quince', '15 Minutos'),
        ('Diez', '10 Minutos'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_2345301')
    agendaMedica = models.ForeignKey('citasMedicas.AgendasMedicas', blank=True,null= True, on_delete=models.PROTECT)
    consultorio =  models.ForeignKey('citasMedicas.Consultorios',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='consul102')
    atiendeDesde = models.DateTimeField(default=timezone.now, editable=False)
    atiendeHasta = models.DateTimeField(default=timezone.now, editable=False)
    desDeHoraDeAlmuerzo = models.DateTimeField(default=timezone.now, editable=False)
    hastaHoraDeAlmuerzo = models.DateTimeField(default=timezone.now, editable=False)
    duracionCita = models.CharField(max_length=15, choices=DURACION_CITA,default='Diez', editable=False)
    estadosProgramacioncitasMedicas = models.ForeignKey('citasMedicas.EstadosProgramacionCitasMedicas',blank=True,null= True,  on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta90')
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


    def __integer__(self):
        return self.agendaMedica

class EstadoRestriccionAgendas(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30,blank=True,null= True, editable=False)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __str__(self):
        return self.nombre

class AgendasMedicasRestriccionProgramacion(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_679301')
    agendasMedicasProgramacion = models.ForeignKey('citasMedicas.AgendasMedicasProgramacion', blank=True,null= True, on_delete=models.PROTECT)
    noAtiendeDesde = models.DateTimeField(default=timezone.now, editable=False)
    noAatiendeHasta = models.DateTimeField(default=timezone.now, editable=False)
    estadoRestriccionAgendas = models.ForeignKey('citasMedicas.EstadoRestriccionAgendas',   blank=True,null= True, on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta58')
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)


    def __integer__(self):
        return self.agendasMedicasProgramacion



class CitasMedicas(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ],
    PRIMERAVEZ = [
        ('S', 'Si'),
        ('N', 'No'),
        ],
    SOAT = [
        ('S', 'Si'),
        ('N', 'No'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_678301')
    agendasMedicasProgramacion = models.ForeignKey('citasMedicas.AgendasMedicasProgramacion',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='agendasMedicasPorgramacion01')
    admision = models.ForeignKey('admisiones.Ingresos',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='ingresos_01')
    soatAccidente = models.CharField(max_length=1, choices=SOAT,default='N', editable=False)
    furips = models.ForeignKey('admisiones.Furips', blank=True,null= True, on_delete=models.PROTECT ,related_name ='furips_01')
    fechaReserva = models.DateTimeField(default=timezone.now, editable=True)
    fechaSolicitada = models.DateTimeField(default=timezone.now, editable=True)
    fechaAtencion = models.DateTimeField(default=timezone.now, editable=True)
    fechaCancelada = models.DateTimeField(default=timezone.now, editable=True)
    usuario = models.ForeignKey('usuarios.Usuarios',blank=True,null= True, on_delete=models.PROTECT)
    convenio = models.ForeignKey('contratacion.Convenios',blank=True,null= True,  on_delete=models.PROTECT)
    tiposAtencion = models.ForeignKey('citasMedicas.TiposAtencion',blank=True,null= True,  on_delete=models.PROTECT)
    citaPrimeraVez = models.CharField(max_length=1, default='S', editable=False)
    estadosCitasMedicas = models.ForeignKey('citasMedicas.EstadosCitasMedicas',blank=True,null= True,  on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta98')
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


    def __integer__(self):
        return self.agendasMedicasProgramacion


class CitasMedicasDetalle(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_67301')
    citasMedicas = models.ForeignKey('citasMedicas.CitasMedicas',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='citasMedicas01')
    cantidad =  models.DecimalField(max_digits=6, decimal_places=0)
    cups = models.ForeignKey('clinico.Examenes',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='cupsCitas_01')
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta56')
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)


    def __integer__(self):
        return self.citasMedicas

class CronologiaCitasMedicas(models.Model):
    STATUS_CHOICES = [
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ]
    id = models.AutoField(primary_key=True)
    #sedesClinica = models.ForeignKey('sitios.SedesClinica',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='sedesClinica_45301')
    citasMedicas = models.ForeignKey('citasMedicas.CitasMedicas',   blank=True,null= True, on_delete=models.PROTECT ,related_name ='citasMedicas21')
    estadosCitasMedicas = models.ForeignKey('citasMedicas.EstadosCitasMedicas',blank=True,null= True,  on_delete=models.PROTECT)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta',  blank=True, null=True, editable=True, on_delete=models.PROTECT,related_name ='usuarioRegistroPlanta76')
    estadoReg = models.CharField(max_length=1, choices=STATUS_CHOICES,default='A', editable=False)

    def __integer__(self):
        return self.agendasMedicasProgramacion

