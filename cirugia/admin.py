from django.contrib import admin

# Register your models here.

from cirugia.models import OrganosCirugias, IntervencionCirugias, TiposHeridasOperatorias, PlanificacionCirugia,  FinalidadCirugia, GravedadCirugia, ZonasCirugia, EstadosCirugias

from cirugia.models import ProgramacionCirugias, EstadosSalas, HojasDeGastos,RecordAnestesico, CirugiasParticipantes, CirugiasProcedimientos, EstadosProgramacion, TiposAnestesia, TiposCirugia, RegionesOperatorias, ViasDeAcceso


@admin.register(OrganosCirugias)
class organosCirugiasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(IntervencionCirugias)
class intervencionCirugiasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)



@admin.register(TiposHeridasOperatorias)
class tiposHeridasOperatoriasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)



@admin.register(FinalidadCirugia)
class finalidadCirugiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)



@admin.register(PlanificacionCirugia)
class planificacionCirugiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(ZonasCirugia)
class zonasCirugiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(GravedadCirugia)
class gravedadCirugiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)



@admin.register(EstadosCirugias)
class estadosCirugiasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)



@admin.register(EstadosSalas)
class estadosSalasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(HojasDeGastos)
class hojasDeGastosAdmin(admin.ModelAdmin):
    list_display = ("id", "cirugia")
    search_fields = ("id", "cirugia")
    # Filtrar
    list_filter = ('cirugia',)

@admin.register(RecordAnestesico)
class recordAnestesicoAdmin(admin.ModelAdmin):
    list_display = ("id", "cirugia","fecha")
    search_fields = ("id", "cirugia","fecha")
    # Filtrar
    list_filter = ("id", "cirugia","fecha")

@admin.register(CirugiasProcedimientos)
class cirugiasProcedimientosAdmin(admin.ModelAdmin):
    list_display = ("id", "cirugia","cups","finalidad", "fechaRegistro")
    search_fields = ("id", "cirugia__id","cups","finalidad", "fechaRegistro")
    # Filtrar
    list_filter = ("id", "cirugia","cups","finalidad", "fechaRegistro")

@admin.register(CirugiasParticipantes)
class cirugiasParticipantesAdmin(admin.ModelAdmin):
    list_display = ("id", "cirugia", "tipoHonorarios", "finalidad", "fechaRegistro")
    search_fields = ("id", "cirugia__id","tipoHonorarios", "finalidad", "fechaRegistro")
    # Filtrar
    list_filter = ("id", "cirugia","tipoHonorarios", "finalidad", "fechaRegistro")

@admin.register(EstadosProgramacion)
class estadosProgramacionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(TiposAnestesia)
class tiposAnestesiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(TiposCirugia)
class tiposCirugiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(RegionesOperatorias)
class regionesOperatoriasAdmin(admin.ModelAdmin):
    list_display = ("id", "region", "organos")
    search_fields =  ("id", "region", "organos")
    # Filtrar
    list_filter =  ("id", "region", "organos")

@admin.register(ViasDeAcceso)
class viasDeAccesoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields =  ("id", "nombre")
    # Filtrar
    list_filter =  ("id", "nombre")

