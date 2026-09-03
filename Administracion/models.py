from django.db import models
from django.utils.timezone import now


# Create your models here.

class Mae_Reportes(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    nom_reporte = models.CharField(max_length=120, unique = True)
    descripcion = models.CharField(max_length=500, default='')
    cuerpo_sql = models.TextField(max_length=15000, default='', editable=True)
    encabezados = models.CharField(max_length=1000, default='', editable=True)
    mae_gruporeportes = models.ForeignKey('Mae_GrupoReportes',blank=True,null= True, editable=True, on_delete=models.PROTECT)
    mae_subgruporeportes = models.ForeignKey('Mae_SubGrupoReportes',blank=True,null= True, editable=True, on_delete=models.PROTECT)
    usuario_crea = models.CharField(max_length=20, default='')
    fechaRegistro = models.DateTimeField(default=now, editable=True)
    excel = models.CharField(max_length=1, default='I', editable=True, choices=TIPO_CHOICES, )
    pdf = models.CharField(max_length=1, default='I', editable=True, choices=TIPO_CHOICES, )
    csv = models.CharField(max_length=1, default='I', editable=True, choices=TIPO_CHOICES, )
    grilla = models.CharField(max_length=1, default='I', editable=True, choices=TIPO_CHOICES, )
    estadoreg = models.CharField(max_length=1, default='A', editable=True ,choices=TIPO_CHOICES,)

    def __str__(self):
        return self.nom_reporte


class Mae_GrupoReportes(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    nom_grupo = models.CharField(max_length=120, unique = True)
    logo = models.CharField(max_length=120,blank=True,null= True, editable=True, unique=False)
    estadoreg = models.CharField(max_length=1, default='A', editable=True ,choices=TIPO_CHOICES,)

    def __str__(self):
        return self.nom_grupo


class Mae_SubGrupoReportes(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    mae_gruporeportes = models.ForeignKey('Mae_GrupoReportes',blank=True,null= True, editable=True, on_delete=models.PROTECT)
    nom_subgrupo = models.CharField(max_length=120, unique=True)
    logo = models.CharField(max_length=120, default='' ,  unique=False)
    estadoreg = models.CharField(max_length=1, default='A', editable=True ,choices=TIPO_CHOICES,)

    class Meta:
        unique_together = ("mae_gruporeportes","nom_subgrupo")

    def __str__(self):
        return self.nom_subgrupo


class Mae_RepUsuarios(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    cod_sede = models.ForeignKey('sitios.SedesClinica',blank=True,null= True, editable=True, on_delete=models.PROTECT, related_name = 'cod_sede')
    mae_reportes = models.ForeignKey('Mae_Reportes',blank=True,null= True, editable=True,  on_delete=models.PROTECT,  related_name = 'mae_reportes')
    cod_usuario = models.CharField(max_length=15, editable=True)
    estadoreg = models.CharField(max_length=1, default='A', editable=True ,choices=TIPO_CHOICES,)

    class Meta:
        unique_together = ("cod_sede", "mae_reportes", "cod_usuario")

    def __str__(self):
        return self.cod_usuario


class Mae_RepParametros(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    mae_reportes = models.ForeignKey('Mae_Reportes',blank=True,null= True, editable=True, on_delete=models.PROTECT)
    parametro = models.IntegerField()
    parametro_texto = models.CharField(max_length=100, editable=True)
    mae_tiposcampo = models.ForeignKey('Mae_TiposCampo',blank=True,null= True, editable=True, on_delete=models.PROTECT)
   # parametro_valor = models.CharField(max_length=30, editable=True)
    estadoreg = models.CharField(max_length=1, default='A', editable=True ,choices=TIPO_CHOICES,)

    class Meta:
        unique_together = ("mae_reportes", "parametro")


    def __str__(self):
        return self.parametro_texto


class Mae_TiposCampo(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, editable=True)
    estadoreg = models.CharField(max_length=1, default='A', editable=True ,choices=TIPO_CHOICES,)

    def __str__(self):
        return self.nombre


class Imhotep_SedesReportes(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    codreg_sede = models.CharField(max_length=30, default='')
    nom_sede = models.CharField(max_length=30, default='')
    codreg_ips = models.CharField(max_length=30, default='')
    direccion = models.CharField(max_length=200, default='')
    telefono = models.CharField(max_length=120, default='')
    departamento = models.CharField(max_length=120, default='')
    municipio = models.CharField(max_length=120, default='')
    zona = models.CharField(max_length=120, default='')
    sede = models.CharField(max_length=120, default='')
    estadoreg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    class Meta:
        unique_together = ("codreg_sede", "nom_sede")

    def __str__(self):
        return self.nom_sede
