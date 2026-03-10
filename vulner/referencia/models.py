from django.db import models

# Create your models here.

class Referencia(models.Model):
    id = models.AutoField(primary_key=True)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    documento = models.ForeignKey('usuarios.Usuarios', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='DocumentoHistoria9')
    consecAdmision = models.IntegerField(default=0)
    servicio = models.ForeignKey('clinico.Servicios', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    tipoAtencion = models.CharField(max_length=20, default='A', editable=False)
    convenio1 = models.ForeignKey('contratacion.convenios', blank=True, null=True, editable=True,    on_delete=models.PROTECT ,   related_name='convenio22')
    convenio2 = models.ForeignKey('contratacion.convenios', blank=True, null=True, editable=True,  on_delete=models.PROTECT ,   related_name='convenio23')
    contacto = models.ForeignKey('usuarios.UsuariosContacto', blank=True, null=True, editable=True,   on_delete=models.PROTECT)
    anamnesis = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    exaFisico = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    exaDiagnostico  = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    tratamiento = models.CharField(max_length=2000, default='A', editable=False)
    motivoReferencia = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    otroMotivo = models.CharField(max_length=2000, blank=True, null=True, editable=True)
    cups1 = models.ForeignKey('clinico.TiposExamen', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='cups28')
    cups2 = models.ForeignKey('clinico.TiposExamen', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='cups27')
    cups3 = models.ForeignKey('clinico.TiposExamen', blank=True, null=True, editable=True, on_delete=models.PROTECT,   related_name='cups26')
    cups4 = models.ForeignKey('clinico.TiposExamen', blank=True, null=True, editable=True, on_delete=models.PROTECT ,   related_name='cups25')
    cups5 = models.ForeignKey('clinico.TiposExamen', blank=True, null=True, editable=True, on_delete=models.PROTECT ,   related_name='cups24')
    cups6 = models.ForeignKey('clinico.TiposExamen', blank=True, null=True, editable=True, on_delete=models.PROTECT ,   related_name='cups23')
    medico = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT ,   related_name='cups22')
    regimerReferencia = models.ForeignKey('clinico.Regimenes', blank=True, null=True, editable=True,   on_delete=models.PROTECT ,   related_name='dx26')
    dxIngreso = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True,   on_delete=models.PROTECT ,   related_name='dx27')
    dxEgreso = models.ForeignKey('clinico.Diagnosticos', blank=True, null=True, editable=True, on_delete=models.PROTECT )
    fechaRegistro = models.DateTimeField(editable=True, null=True, blank=True)
    fechaPrueba = models.DateTimeField(editable=True, null=True, blank=True)
    usuarioRegistro = models.ForeignKey('planta.Planta', blank=True, null=True, editable=True, on_delete=models.PROTECT)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return str(self.id)


