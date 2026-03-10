from django.contrib import admin

# Register your models here.

from facturacion.models import Suministros, TiposEmpresa ,Empresas,  Conceptos,  ConveniosPacienteIngresos, SalariosLegales, RegimenesTipoPago, TiposSuministro,  ConceptosAfacturar,   SalariosMinimosLegales, EstadoEnvioDian


@admin.register(Empresas)
class empresasAdmin(admin.ModelAdmin):

   list_display = ("id", "tipoDoc", "tipoEmpresa","documento","nombre","codigoEapb","direccion","telefono")
   search_fields = ("id", "tipoDoc__nombre", "tipoEmpresa__nombre", "documento","nombre","codigoEapb","direccion","telefono")
   # Filtrar
   list_filter = ("id", "tipoDoc",  "tipoEmpresa","documento","nombre","codigoEapb","direccion","telefono")


@admin.register(Conceptos)
class conceptosAdmin(admin.ModelAdmin):
   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")


@admin.register(ConveniosPacienteIngresos)
class conveniosPacienteIngresosAdmin(admin.ModelAdmin):
   list_display = ("id", "tipoDoc", "documento", "consecAdmision", "convenio")
   search_fields = ("id", "tipoDoc__nombre", "documento", "consecAdmision", "convenio__nombre")
   # Filtrar
   list_filter = ("id", "tipoDoc", "documento", "consecAdmision", "convenio")


@admin.register(SalariosLegales)
class salariosLegalesAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")


@admin.register(RegimenesTipoPago)
class regimenesTipoPagoAdmin(admin.ModelAdmin):

   list_display = ("id", "regimen","salarioLegal", "año","valorModeradora","valorCopago")
   search_fields = ("id", "regimen","salarioLegal", "año","valorModeradora","valorCopago")
   # Filtrar
   list_filter = ("id", "regimen","salarioLegal", "año","valorModeradora","valorCopago")


@admin.register(TiposSuministro)
class tiposSuministroAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")

@admin.register(Suministros)
class suministroAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre","tipoSuministro","nombreGenerico","descripcionComercial","ripsFormaFarmaceutica")
   search_fields =("id", "nombre","tipoSuministro__nombre","cums","nombreGenerico","descripcionComercial","ripsFormaFarmaceutica__nombre")
   # Filtrar
   list_filter = ("id", "nombre","tipoSuministro","nombreGenerico","descripcionComercial","ripsFormaFarmaceutica")




@admin.register(TiposEmpresa)
class tiposEmpresaAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")

@admin.register(ConceptosAfacturar)
class conceptosAfacturarAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")




@admin.register(SalariosMinimosLegales)
class salariosMinimosLegalesAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre", "año","valor","valorSubsidio")
   search_fields = ("id", "nombre", "año","valor","valorSubsidio")
   # Filtrar
   list_filter = ("id", "nombre", "año","valor","valorSubsidio")


@admin.register(EstadoEnvioDian)
class estadoEnvioDianAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")


