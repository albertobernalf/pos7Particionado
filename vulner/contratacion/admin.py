from django.contrib import admin

# Register your models here.


from clinico.models import TiposExamen
from contratacion.models import  Convenios,  ConveniosTarifasHonorarios,ConveniosLiquidacionTarifasHonorarios
@admin.register(Convenios)
class conveniosAdmin(admin.ModelAdmin):

    list_display = ( "id","tarifariosDescripcionProc","tarifariosDescripcionSum","tarifariosDescripcionHono","nombre","descripcion", "empresa","vigenciaDesde","vigenciaHasta")
    search_fields = ( "id","tarifariosDescripcionProc","tarifariosDescripcionSum","tarifariosDescripcionHono","nombre","descripcion", "empresa__nombre","vigenciaDesde","vigenciaHasta")
    # Filtrar
    list_filter = ( "id","tarifariosDescripcionProc","tarifariosDescripcionSum","tarifariosDescripcionHono","nombre","descripcion", "empresa","vigenciaDesde","vigenciaHasta")



@admin.register( ConveniosTarifasHonorarios)
class  conveniosTarifasHonorariosAdmin(admin.ModelAdmin):

    list_display = ( "id","convenio",  "valor")
    search_fields = ( "id","convenio__nombre","valor")
    # Filtrar
    list_filter =  ( "id","convenio",  "valor")








@admin.register(ConveniosLiquidacionTarifasHonorarios)
class conveniosLiquidacionTarifasHonorariosAdmin(admin.ModelAdmin):

   list_display = ("id", "descripcion","tipoTarifa","codigoHomologado", "valor")
   search_fields = ("id", "descripcion","tipoTarifa","codigoHomologado", "valor")
   # Filtrar
   list_filter = ("id", "descripcion","tipoTarifa","codigoHomologado", "valor")

