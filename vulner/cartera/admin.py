from django.contrib import admin

# Register your models here.

from cartera.models import FormasPagos, TiposPagos,Pagos,TiposGlosas,MotivosGlosas, Radicaciones, Remisiones, TiposNotas, EstadosGlosas, GlosasConceptoGeneral, GlosasConceptoEspecifico, Caja, TiposNotasCredito, NotasCreditoDetalle, NotasCreditoDetalleRips, PagosEmpresas, PagosEmpresasDetalle

@admin.register(FormasPagos)
class formasPagosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(TiposPagos)
class tiposPagosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(Pagos)
class pagosAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "documento", "tipoPago","formaPago")
    search_fields = ("id", "fecha", "documento", "tipoPago__nombre","formaPago__nombre")
    # Filtrar
    list_filter = ("id", "fecha", "documento", "tipoPago","formaPago")

@admin.register(TiposGlosas)
class tiposGlosasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ("id", "nombre")

@admin.register(EstadosGlosas)
class estadosGlosasAdmin(admin.ModelAdmin):
    list_display = ("id",  "tipo", "nombre")
    search_fields = ("id",  "tipo", "nombre")
    # Filtrar
    list_filter = ("id",  "tipo", "nombre")


@admin.register(GlosasConceptoGeneral)
class glosasConceptoGeneralAdmin(admin.ModelAdmin):
    list_display = ("id",  "codigo", "nombre")
    search_fields = ("id",  "codigo", "nombre")
    # Filtrar
    list_filter = ("id",  "codigo", "nombre")



@admin.register(GlosasConceptoEspecifico)
class glosasConceptoEspecificoAdmin(admin.ModelAdmin):
    list_display = ("id", "conceptoGeneral", "codigo", "nombre")
    search_fields = ("id", "conceptoGeneral", "codigo", "nombre")
    # Filtrar
    list_filter = ("id", "conceptoGeneral",  "codigo", "nombre")



@admin.register(MotivosGlosas)
class motivosGlosasAdmin(admin.ModelAdmin):
    list_display = ("id","conceptoGeneral", "conceptoEspecifico",  "conceptoGlosa", "nombre","descripcion")
    search_fields = ("id","conceptoGeneral", "conceptoEspecifico","conceptoGlosa", "nombre","descripcion")
    # Filtrar
    list_filter = ("id", "conceptoGeneral", "conceptoEspecifico","conceptoGlosa", "nombre","descripcion")



@admin.register(Radicaciones)
class radicacionesAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "radicacion")
    search_fields = ("id","fecha", "radicacion")
    # Filtrar
    list_filter = ("id", "fecha","radicacion")



@admin.register(Remisiones)
class remisionesAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha","remision")
    search_fields = ("id", "fecha","remision")
    # Filtrar
    list_filter = ("id", "fecha","remision")


@admin.register(TiposNotas)
class tiposNotasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(Caja)
class cajaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "serviciosAdministrativos","usuarioEntrega","totalEfectivo","totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", "total" )
    search_fields = ("id", "fecha", "serviciosAdministrativos__nombre","usuarioEntrega__nombre","totalEfectivo","totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", "total" )
    # Filtrar
    list_filter = ("id", "fecha", "serviciosAdministrativos","usuarioEntrega","totalEfectivo","totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", "total" )


@admin.register(TiposNotasCredito)
class tiposNotasCreditoAdmin(admin.ModelAdmin):
    list_display = ("id", "codigo","nombre")
    search_fields = ("id", "codigo","nombre")
    # Filtrar
    list_filter = ("codigo",'nombre',)

@admin.register(NotasCreditoDetalle)
class notasCreditoDetalleAdmin(admin.ModelAdmin):
    list_display = ("id", "notaCredito","valorNota","tiposNotasCredito")
    search_fields = ("id", "notaCredito","valorNota","tiposNotasCredito__nombre")
    # Filtrar
    list_filter = ("id", "notaCredito","valorNota","tiposNotasCredito")

@admin.register(NotasCreditoDetalleRips)
class notasCreditoDetalleRipsAdmin(admin.ModelAdmin):
    list_display = ("id", "notaCreditoDetalle","valorNota","tiposNotasCredito","ripsProcedimientos","ripsMedicamentos", "ripsConsultas", "ripsOtrosServicios")
    search_fields = ("id", "notaCreditoDetalle","valorNota","tiposNotasCredito__nombre")
    # Filtrar
    list_filter = ("id", "notaCreditoDetalle","valorNota","tiposNotasCredito")


@admin.register(PagosEmpresas)
class pagosEmpresasAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "sedesClinica", "serviciosAdministrativos", "empresa" ,"tipoPago","formaPago","valor", "descripcion")
    search_fields = ("id", "fecha", "sedesClinica__nombre", "serviciosAdministrativos_nombre", "empresa__nombre" ,"tipoPago_nombre","formaPago__nombre","valor", "descripcion")
    # Filtrar
    list_filter = ("id", "fecha", "sedesClinica", "serviciosAdministrativos", "empresa" ,"tipoPago","formaPago","valor", "descripcion")
