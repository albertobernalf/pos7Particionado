
from django import forms

from Administracion.models import Mae_Reportes

class Mae_ReportesForm(forms.ModelForm):
          cuerpo_sql = forms.CharField( widget=forms.Textarea(attrs={'rows': 15, 'cols': 200}))
          encabezados = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 200}))
          excel = forms.CheckboxInput()
          pdf = forms.CheckboxInput()
          csv = forms.CheckboxInput()
          grilla = forms.CheckboxInput()

          class Meta:
            model = Mae_Reportes
            fields = ('__all__')