from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Historia, Especialidades, Medicos
from usuarios.models import TiposDocumento, Usuarios
from clinico.models import TiposExamen, Examenes, HistoriaExamenes, TiposFolio, CausasExterna, TiposIncapacidad, HistorialIncapacidades, Diagnosticos, HistorialDiagnosticosCabezote, SignosVitales, HistoriaSignosVitales , Historia
from sitios.models import Dependencias, DependenciasTipo
from planta.models import Planta
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError
from datetime import datetime



class IncapacidadesForm(forms.ModelForm):

    class Meta:
        model = HistorialIncapacidades
        fields = '__all__'

        historia = forms.IntegerField(disabled=True, initial=0)
        tiposIncapacidad = forms.ModelChoiceField(queryset=TiposIncapacidad.objects.all())
        diagnosticosIncapacidad = forms.ModelChoiceField(queryset=Diagnosticos.objects.all())
        desdeFecha = forms.DateField()
        hastaFecha = forms.DateField()
        numDias    = forms.IntegerField(label='Numero de dias', disabled=False, initial=0)
        descripcion = forms.CharField(max_length=4000)
        estadoReg = forms .CharField(max_length=1)

        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'width': "50%", 'cols': "80", 'rows': "4",
                                                   'placeholder': "descripcion"}),
            'desdeFecha': forms.TextInput(attrs={'type': 'datetime-local'}),
            'hastaFecha': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

class HistoriaSignosVitalesForm(forms.ModelForm):

        class Meta:
            model = HistoriaSignosVitales
            fields = '__all__'

        historia = forms.IntegerField(disabled=True)
        fecha = forms.DateTimeField()
        frecCardiaca = forms.CharField(max_length=5)
        frecRespiratoria = forms.CharField(max_length=5)
        tensionADiastolica = forms.CharField(max_length=5)
        tensionASistolica = forms.CharField(max_length=5)
        tensionAMedia = forms.CharField(max_length=5)
        temperatura = forms.CharField(max_length=5)
        saturacion = forms.CharField(max_length=5)
        glucometria = forms.CharField(max_length=5)
        glasgow = forms.CharField(max_length=5)
        apache = forms.CharField(max_length=5)
        pvc = forms.CharField(max_length=5)
        cuna = forms.CharField(max_length=5)
        ic = forms.CharField(max_length=5)
        glasgowOcular = forms.CharField(max_length=5)
        glasgowVerbal = forms.CharField(max_length=5)
        glasgowMotora = forms.CharField(max_length=5)
        observacion = forms.CharField(max_length=5000)
        fechaRegistro = forms.DateTimeField()
        estadoReg = forms.CharField(max_length=1)

        widgets = {
                'observacion': forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "80", 'rows': "4",
                                                   'placeholder': "observaciones"}),
                'fecha': forms.TextInput(attrs={'type': 'datetime-local'}),
        }


class HistorialDiagnosticosCabezoteForm(forms.ModelForm):

    class Meta:
        model = HistorialDiagnosticosCabezote

        tipoDoc = forms.IntegerField(label='Tipo Doc')
        documento = forms.IntegerField(label='No Documento')
        consecAdmision= forms.IntegerField(label='Admision No', disabled=True, initial=0)
        folio = forms.IntegerField(label='No Folio', disabled=True, initial=0)
        observaciones = forms.CharField(max_length=200)
        estadoReg = forms.CharField(max_length=1)

        fields = '__all__'

        widgets = {
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "4",
                                                   'placeholder': "Observaciones"})
        }


class historiaForm(forms.ModelForm):

    class Meta:
        model = Historia
        fields = '__all__'
        widgets = {'antibioticos': forms.RadioSelect(choices=Historia.STATUS_CHOICES,attrs={"placeholder": 'Antibiotico'}),
                   'monitoreo': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'movilidadLimitada': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'nauseas': forms.RadioSelect(choices=Historia.STATUS_CHOICES ,attrs={"placeholder": 'Nauseas'}),
                   'llenadoCapilar': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'neurologia': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'irritacion': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'pulsos': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'retiroPuntos': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'vomito': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'inmovilizacion': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   'notaAclaratoria': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
           		   'inmovilizacion': forms.RadioSelect(choices=Historia.STATUS_CHOICES),
                   }

        tipoDoc = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
        documento = forms.IntegerField(label='No Documento')
        consecAdmision = forms.IntegerField(label='Admision No', disabled=True, initial=0)
        folio = forms.IntegerField(label='No Folio', disabled=True, initial=0)
        fecha = forms.DateTimeField()

        tiposFolio = forms.ModelChoiceField(queryset=TiposFolio.objects.all())
        causasExterna = forms.ModelChoiceField(queryset=CausasExterna.objects.all())
        dependenciasRealizado = forms.ModelChoiceField(queryset=DependenciasTipo.objects.all())
        especialidades = forms.ModelChoiceField(queryset=Especialidades.objects.all())
        planta = forms.ModelChoiceField(queryset=Planta.objects.all())
        apache2 = forms.IntegerField(label='Apache', disabled=True, initial=0)
        antibioticos = forms.CharField(max_length=1, help_text="Antibiotico")
        monitoreo = forms.CharField(max_length=1 , help_text="Monitoreo")
        movilidadLimitada = forms.CharField(max_length=1 , help_text="Movilidad Limitada")
        nauseas  = forms.CharField(max_length=1 , help_text="Nauseas")
        llenadoCapilar = forms.CharField(max_length=1 , help_text="Llenado capilar")
        neurologia = forms.CharField(max_length=1 , help_text="Neurologia")
        irritacion = forms.CharField(max_length=1)
        pulsos = forms.CharField(max_length=1)
        retiroPuntos = forms.CharField(max_length=1)
        vomito  = forms.CharField(max_length=1)
        inmovilizacion = forms.CharField(max_length=1)
        notaAclaratoria = forms.CharField(max_length=1)
        fecNotaAclaratoria  = forms.DateTimeField()
        textoNotaAclaratoria = forms.CharField(max_length=5000)
        examenFisico = forms.CharField(max_length=5000)
        noQx = forms.CharField(max_length=30)
        observaciones = forms.CharField(max_length=5000)
        riesgoHemodinamico = forms.CharField(max_length=15)
        riesgoVentilatorio = forms.CharField(max_length=15)
        riesgos = forms.CharField(max_length=5000)
        trombocitopenia = forms.CharField(max_length=50)
        hipotension = forms.CharField(max_length=50)
        indiceMortalidad = forms.IntegerField(label='Indice mortalidad', disabled=True, initial=0)
        ingestaAlcohol = forms.CharField(max_length=5000)
        inmovilizacionObservaciones = forms.CharField(max_length=5000)
        justificacion = forms.CharField(max_length=5000)
        leucopenia = forms.CharField(max_length=50)
        manejoQx = forms.CharField(max_length=20000)
        mipres = forms.CharField(max_length=30)
        ordenMedicaLab = forms.CharField(max_length=30)
        ordenMedicaRad = forms.CharField(max_length=30)
        ordenMedicaTer = forms.CharField(max_length=30)
        ordenMedicaMed = forms.CharField(max_length=30)
        ordenMedicaOxi = forms.CharField(max_length=30)
        ordenMedicaInt = forms.CharField(max_length=30)

        fechaRegistro =  forms.DateTimeField()
        usuarioRegistro = forms.ModelChoiceField(queryset=Usuarios.objects.all())



        widgets = {
            'motivo':    forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "80", 'rows': "6", 'placeholder': "Motivo"}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "80", 'rows': "6", 'placeholder': "tratamiento"}),
            'subjetivo': forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "80", 'rows': "6", 'placeholder': "Subjetivo"}),
            'objetivo':  forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "80", 'rows': "6", 'placeholder': "Objetivo"}),
            'analisis':  forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "80", 'rows': "6", 'placeholder': "Analisis"}),
            'plann':     forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "80", 'rows': "6", 'placeholder': "Plan"}),
            'ordenDeControl': forms.Textarea(attrs={'class': 'form-control', 'width': "100%", 'cols': "40", 'rows': "6", 'placeholder': "Orden De Control"}),
            'textoNotaAclaratoria':     forms.Textarea(attrs={'width': "30%", 'cols': "20", 'rows': "4", 'placeholder': "textoNotaAclaratoria"}),
            'examenFisico':     forms.Textarea(attrs={'width': "30%", 'cols': "20", 'rows': "4", 'placeholder': "examenFisico"}),
            'observaciones':     forms.Textarea(attrs={'width': "30%", 'cols': "20", 'rows': "4", 'placeholder': "observaciones"}),
            'ingestaAlcohol':     forms.Textarea(attrs={'width': "30%", 'cols': "20", 'rows': "4", 'placeholder': "ingestaAlcohol"}),
            'inmovilizacionObservaciones':     forms.Textarea(attrs={'width': "30%", 'cols': "20", 'rows': "4", 'placeholder': "inmovilizacionObservaciones"}),
            'manejoQx':     forms.Textarea(attrs={ 'width': "30%", 'cols': "20", 'rows': "4", 'placeholder': "manejoQx"}),
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






class historiaExamenesForm(forms.ModelForm):

    class Meta:
        model = HistoriaExamenes

        id_tipo_doc = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
        documento = forms.IntegerField(label='No Documento')
        folio = forms.IntegerField(label='No Folio', disabled=True, initial=0)
        fecha = forms.DateTimeField()
        id_TipoExamen = forms.ModelChoiceField(queryset=TiposExamen.objects.all())
        id_examen = forms.ModelChoiceField(queryset=Examenes.objects.all())
        cantidad = forms.IntegerField(label='Cantidad')

        estado_folio = forms.CharField(label='Estado del Folio', disabled=True, initial='A', max_length=1)

        fields = '__all__'

    def clean_fecha(self):
        print ("Entre Fecha")
        fecha = self.cleaned_data.get('fecha')
        print(fecha)

        return fecha

    def clean_cantidad(self):
            print("Entre cantidad")
            cantidad = self.cleaned_data.get('cantidad')
            print(cantidad)

            return cantidad

    def clean_estado_folio(self):
        print("Entre esadofoklio")
        estado_folio = self.cleaned_data.get('estado_folio')
        print(estado_folio)

        return estado_folio


    def clean_id_examen(self):
        print("Entre id_examen")
        id_examen = self.cleaned_data.get('id_examen')
        print(id_examen)

        return id_examen

    def clean_id_TipoExamen(self):
        print("Entre id_TipoExamen")
        id_TipoExamen = self.cleaned_data.get('id_TipoExamen')
        print(id_TipoExamen)

        return id_TipoExamen







