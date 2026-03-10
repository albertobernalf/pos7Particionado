from django.contrib import admin

# Register your models here.


from farmacia.models import FarmaciaEstados


@admin.register( FarmaciaEstados)
class   farmaciaEstadosAdmin(admin.ModelAdmin):

    list_display = ( "id","nombre",  "usuarioRegistro")
    search_fields = ( "id","nombre",  "usuarioRegistro")
    # Filtrar
    list_filter =  ( "id","nombre",  "usuarioRegistro")