from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError

from admisiones.models import Ingresos, Furips
from usuarios.models import TiposDocumento, Usuarios

from sitios.models import SedesClinica, Dependencias, Departamentos, Municipios, Localidades
from clinico.models import Diagnosticos, EstadosSalida, Servicios, Especialidades, Ips
from basicas.models import Eventos
from planta.models import Planta
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError

import datetime


class crearAdmisionForm(forms.ModelForm):
    extraServicio = forms.ModelChoiceField(queryset=Servicios.objects.filter(id__lt=3))

    def save(self, commit=True):
        extraServicio = self.cleaned_data.get('extraServicio', None)
        # ...do something with extra_field here...
        return super(crearAdmisionForm, self).save(commit=commit)

    class Meta:
        model = Ingresos

        CHOICES = [('1', 'First'), ('2', 'Second')]
        sedesClinica = forms.ModelChoiceField(queryset=SedesClinica.objects.all())
        tipoDoc = forms.ModelChoiceField(queryset=TiposDocumento.objects.all() , required=True)
        documento = forms.IntegerField(label='No Documento' , required=True)
        consec = forms.IntegerField(label='Ingreso No', disabled=True)
        fechaIngreso = forms.DateTimeField(label="Fec.Ingreso : ", initial=datetime.date.today , required=True)
        fechaSalida = forms.DateTimeField(label="Fec.Salida : ", initial=datetime.date.today)
        factura = forms.IntegerField(initial=0, disabled=True)
        numcita = forms.IntegerField(initial=0, disabled=True)
        dependenciasIngreso = forms.ModelChoiceField(label="Dep.Ingreso : ", required=True, queryset=Dependencias.objects.all())
        #dependenciasActual = forms.ModelChoiceField(label="Dep.Actual : ", queryset=Dependencias.objects.all())
        dependenciasSalida = forms.ModelChoiceField(label="Dep.Salida : ", queryset=Dependencias.objects.all())
        dxIngreso = forms.ModelChoiceField(label="Dx.Ingreso : ", required=True, queryset=Diagnosticos.objects.all())
        dxActual = forms.ModelChoiceField(label="Dx.Actual : ", queryset=Diagnosticos.objects.all())
        dxSalida = forms.ModelChoiceField(label="Dx.Salida : ", queryset=Diagnosticos.objects.all())
        estadoSalida = forms.ModelChoiceField(label="Estado Salida : ", queryset=EstadosSalida.objects.all())
        medicoIngreso = forms.ModelChoiceField(label="Med.Ingreso : ", required=True, queryset=Planta.objects.all())
        medicoActual = forms.ModelChoiceField(label="Med Actual : ", queryset=Planta.objects.all())
        medicoSalida = forms.ModelChoiceField(label="Med.Salida : ", queryset=Planta.objects.all())
        especialidadesMedicosIngreso = forms.ModelChoiceField(label="Esp Actual : ", required=True,
                                                              queryset=Especialidades.objects.all())
        especialidadesMedicosActual = forms.ModelChoiceField(label="Esp Actual : ",
                                                             queryset=Especialidades.objects.all())
        especialidadesMedicosSalida = forms.ModelChoiceField(label="Esp Actual : ",
                                                             queryset=Especialidades.objects.all())

        salidaDefinitiva = forms.CharField(label='Salida Definitiva', initial='N', max_length=1)
        usuarioRegistro = forms.CharField(label='SUsuario Registra', initial='N')
        fechaRegistro = forms.CharField(label='Fecha Registro', disabled=True)
        estadoRegistro = forms.CharField(label='Estado Registro', disabled=True, initial='A', max_length=1)

        fields = '__all__'

        widgets = {
            'tipoDoc_id': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "tipoDoc"}),
            'documento_id': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "Documento"}),
            'consec': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "Consecutivo"}),
            # 'fechaIngreso' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Motivo"}),

            'fechaIngreso': forms.DateTimeInput(attrs={'class': 'form-group datetimepicker-input'}),
            'fechaSalida': forms.TextInput(attrs={'class': 'form-group', 'placeholder': "salida"}),

            'factura': forms.TextInput(attrs={'readonly': 'readonly'}),

            'numcita': forms.TextInput(attrs={'readonly': 'readonly'})
        }


    def clean_dxIngreso(self):
        print("Entre a validar diagnostico de imngreso")
        dxIngreso = self.cleaned_data.get('dxIngreso')
        print(dxIngreso)

        if dxIngreso != '':
            print("ok Diagnostico")
        else:
            raise forms.ValidationError('Suministre Diagnostico de Ingreso . ')

        return dxIngreso

    def clean_medicoIngreso(self):
        print("Entre a validar  de medicoIngreso")
        medicoIngreso = self.cleaned_data.get('medicoIngreso')
        print(medicoIngreso)

        if medicoIngreso != '':
            print("ok Medico")
        else:
            raise forms.ValidationError('Suministre medicoIngreso . ')

        return medicoIngreso


# Desde Aquip FURIPS
ESTADOREG_CHOICES = (
        ('A', 'ACTIVO'),
        ('I', 'INACTIVO'),
    )

FLAG_CHOICES = (
        ('S', 'Si'),
        ('N', 'No'),
    )
TIPOCONDICION_CHOICES =(
    ("A", "Asegurado"),
    ("N", "No Asegurado"),
    ("V", "Vehiculo_Fantasma"),
    ("P", "Poliza_Falsa"),
    ("F", "Vehiculo_en_fuga"),
)
TIPO3_CHOICES = (
        ("P", 'Servicio Particular'),
        ("U", 'Servicio Publico'),
        ("O", 'Servicio Oficial'),
        ("D", 'Servicio Diplomatico'),
        ("T", 'De transporte Masivo'),
	    ("E", 'Escolar')
)
TIPO4_CHOICES = (
        ("R", 'Remision'),
        ("O", 'Orden de Servicio'),
)


class furipsForm(forms.ModelForm):

    class Meta:
        model = Furips
        fields = '__all__'
        widgets = {'condicionAccidentado': forms.RadioSelect(choices=Furips.TIPOCONDICION_CHOICES),
                   'estado': forms.RadioSelect(choices=Furips.FLAG_CHOICES),
                   'tipoVehiculo': forms.RadioSelect(choices=Furips.TIPO3_CHOICES),
                   'tipoReferencia': forms.RadioSelect(choices=Furips.TIPO4_CHOICES),
		   'estadoReg': forms.RadioSelect(choices=Furips.ESTADOREG_CHOICES),
                   }

    sedesClinica = forms.ModelChoiceField(queryset=SedesClinica.objects.all())
    fechaRadicado =  forms.DateTimeField()
    numeroRadicacion =  forms.CharField(max_length=30)
    numeroRadicadoAnterior = forms.CharField(max_length=30)
    numeroFactura = forms.CharField(max_length=20)
    primerNombreVictima = forms.CharField(max_length=20)
    segundoNombreVictima = forms.CharField(max_length=20)
    primerApellidoVictima = forms.CharField(max_length=20)
    segundoApellidoVictima = forms.CharField(max_length=20)
    tipoDocVictima        = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
    documentoVictima      = forms.ModelChoiceField(queryset=Usuarios.objects.all())
    consecVictima         = forms.CharField(max_length=8)
    condicionAccidentado = forms.ChoiceField(choices = TIPOCONDICION_CHOICES)
    evento = forms.ModelChoiceField(queryset=Eventos.objects.all())
    direccionEvento = forms.CharField(max_length=80)
    departamentoEvento = forms.ModelChoiceField(queryset=Departamentos.objects.all())
    municipioEvento = forms.ModelChoiceField(queryset=Municipios.objects.all())
    localidadEvento = forms.ModelChoiceField(queryset=Localidades.objects.all())
    zonaEvento =  forms.CharField(max_length=1)
    fechaEvento = forms.DateTimeField()
    eventoDescripcion = forms.CharField(max_length=500)
    estado = forms.ChoiceField(choices = FLAG_CHOICES)
    marcaVehiculo = forms.CharField(max_length=50)
    placaVehiculo = forms.CharField(max_length=20)
    tipoServicioVehiculo = forms.CharField(max_length=20)
    tipoVehiculo = forms.ChoiceField(choices = TIPO3_CHOICES)
    codigoaseguradora = forms.CharField(max_length=20)
    numeroPoliza= forms.CharField(max_length=20)
    fechaIniPoliza = forms.DateTimeField()
    fechaFinPoliza = forms.DateTimeField()
    intervencionAutoridad = forms.CharField(max_length=20)
    cobroExcedentePoliza = forms.CharField(max_length=20)
    primerNombrePropietario = forms.CharField(max_length=20)
    segundoNombrePropietario = forms.CharField(max_length=20)
    primerApellidoPropietario = forms.CharField(max_length=20)
    segundoApellidoPropietario = forms.CharField(max_length=20)
    tipoDocPropietario        = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
    documentoPropietario      =  forms.IntegerField(label='No Documento')
    departamentoPropietario = forms.ModelChoiceField(queryset=Departamentos.objects.all())
    municipioPropietario = forms.ModelChoiceField(queryset=Municipios.objects.all())
    localidadPropietario = forms.ModelChoiceField(queryset=Localidades.objects.all())
    direccionPropietario = forms.CharField(max_length=80)
    primerNombreInvolucrado = forms.CharField(max_length=20)
    segundoNombreInvolucrado = forms.CharField(max_length=20)
    primerApellidoInvolucrado = forms.CharField(max_length=20)
    segundoApellidoInvolucrado = forms.CharField(max_length=20)
    tipoDocInvolucrado        = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
    documentoInvolucrado     =  forms.IntegerField(label='No Documento')
    departamentoInvolucrado = forms.ModelChoiceField(queryset=Departamentos.objects.all())
    municipioInvolucrado = forms.ModelChoiceField(queryset=Municipios.objects.all())
    localidadInvolucrado = forms.ModelChoiceField(queryset=Localidades.objects.all())
    direccionInvolucrado = forms.CharField(max_length=30)
    tipoReferencia =  forms.ChoiceField(choices = TIPO4_CHOICES)
    fechaRemision = forms.DateTimeField()
    prestadorRemite = forms.ModelChoiceField(queryset=Ips.objects.all())
    codigoInscripcion = forms.CharField(max_length=20)
    profesionalRemite = forms.ModelChoiceField(queryset=Planta.objects.all())
    fechaAceptacion = forms.DateTimeField()
    prestadorRecibe = forms.ModelChoiceField(queryset=Ips.objects.all())
    codigoInscripcionRecibe = forms.CharField(max_length=20)
    profesionalRecibe = forms.CharField(max_length=20)
    numeroPlacaTranporto = forms.CharField(max_length=20)
    trasportoVictimaDesde = forms.CharField(max_length=80)
    trasportoVictimaHasta = forms.CharField(max_length=80)
    tipoTransporteTransporto = forms.CharField(max_length=80)
    lugarRecogeVictima = forms.CharField(max_length=80)
    certificacionIngreso = forms.DateTimeField()
    certificacionEgreso =  forms.DateTimeField()
    dxPrincIngreso     = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
    dxRel1Ingreso   = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
    dxRel2Ingreso   = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
    dxPrincEgreso   = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
    dxRel1Egreso    = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
    dxRel2Egreso    = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
    tipoDocProfesionalAtendio   = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
    documentoProfesionalAtendio =   forms.IntegerField(label='No Documento')
    amparoReclamaFacturadoQx =  forms.CharField(max_length=7)
    amparoReclamaAFosygaQx =  forms.CharField(max_length=7)
    amparoReclamaFacturadoGastos =  forms.CharField(max_length=7)
    amparoReclamaAFosygaGastos =  forms.CharField(max_length=7)
    fechaRegistro =  forms.DateTimeField()
    usuarioRegistro = forms.ModelChoiceField(queryset=Usuarios.objects.all())

    widgets = {
        'eventoDescripcion':    forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4", 'placeholder': "Motivo"})
    }


    def clean_documento(self):
        print("entre a validar Documento Historia1 Form")
        documento = self.cleaned_data.get('documento')
        print (documento)
        id_tipo_doc = self.cleaned_data.get('id_tipo_doc')
        print(id_tipo_doc)
        id_tipo_doc1 = TiposDocumento.objects.get(nombre=id_tipo_doc)
        print(id_tipo_doc1.id)
        if Usuarios.objects.all().filter(id_tipo_doc=id_tipo_doc1.id).filter(nombre=documento).exists():
            print("ok Documento")
        else:
            raise forms.ValidationError('Documento de Usuario No existe . ')
            return documento
        return documento

    def clean_fecha(self):
        print("Entre Historia1View validar Fecha")
        fecha = self.cleaned_data.get('fecha')
        print(fecha)

        return fecha


    def clean_motivo(self):
        print("Entre Historia1View validar motivo")
        motivo = self.cleaned_data.get('motivo')
        print(motivo)

        return motivo



## Hasta Aquip FURIPS


