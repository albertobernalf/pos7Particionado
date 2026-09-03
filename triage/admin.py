from django.contrib import admin

# Register your models here.

from triage.models import Triage


@admin.register(Triage)
class triageAdmin(admin.ModelAdmin):
    list_display = ("id", "sedesClinica","fechaSolicita", "fechaAtendio", "tipoDoc","documento","hClinica","regimen","motivo")
    search_fields = ("id", "sedesClinica__nombre","fechaSolicita", "fechaAtendio", "tipoDoc__nombre","documento","hClinica","regimen__nombre","motivo")
    # Filtrar
    list_filter =("id", "sedesClinica","fechaSolicita", "fechaAtendio", "tipoDoc","documento","hClinica","regimen","motivo")

