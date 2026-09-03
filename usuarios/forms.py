from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError

from admisiones.models import Ingresos
from usuarios.models import TiposDocumento, Usuarios, TiposUsuario

from sitios.models import SedesClinica, Dependencias, Centros
from clinico.models import Diagnosticos, EstadosSalida, Servicios, Especialidades
from planta.models import Planta
import datetime



class crearUsuariosForm(forms.ModelForm):

    extraServicio = forms.ModelChoiceField(queryset=Servicios.objects.filter(id__lt =3))

    def save(self, commit=True):
        extraServicio = self.cleaned_data.get('extraServicio', None)
        # ...do something with extra_field here...
        return super(crearAdmisionForm, self).save(commit=commit)



    class Meta:
        model = Usuarios

        CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]
        tipoDoc = forms.ModelChoiceField(queryset=TiposDocumento.objects.all())
        documento = forms.IntegerField(label='No Documento')
        nombre = forms.CharField(label='Nombre', initial='N', max_length=50)
        genero =forms.CharField(label='Genero', initial='N', max_length=1)
        centrosC = forms.ModelChoiceField(label="Centro : ", queryset=Centros.objects.all())
        tiposUsuario = forms.ModelChoiceField(label="Tipo Usuarios : ", queryset=TiposUsuario.objects.all())
        direccion = forms.CharField(label='Direccion', initial='N', max_length=50)
        telefono = forms.CharField(label='Direccion', initial='N', max_length=20)
        contacto = forms.CharField(label='Direccion', initial='N', max_length=50)
       # imagen = models.ImageField(upload_to="fotos", null=True)

        fechaRegistro = forms.CharField(label='Fecha Registro', disabled=True)
        estadoRegistro = forms.CharField(label='Estado Registro', disabled=True, initial='A', max_length=1)


        fields = '__all__'

        widgets = {
            'tipoDoc_id' :  forms.TextInput(attrs={'class': 'form-group', 'placeholder': "tipoDoc"}),
            'documento_id' : forms.TextInput(attrs={'class': 'form-group', 'placeholder': "Documento"}),

        }

