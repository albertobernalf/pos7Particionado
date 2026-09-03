from django.contrib import admin

# Register your models here.



from basicas.models import EstadoCivil,  Ocupaciones, CentrosCosto, Eventos, TiposFamilia, TiposContacto, Periodos, FuripsLista, FuripsParametro, Archivos, Parametros, TiposProfesional

@admin.register(EstadoCivil)
class estadoCivilAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(Ocupaciones)
class ocupacionesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(CentrosCosto)
class centrosCostoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(Eventos)
class eventosoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ("id", "nombre")

@admin.register(TiposFamilia)
class tiposFamiliaCostoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(TiposContacto)
class tiposContactoCostoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(Periodos)
class periodosoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre","año","mes","diaInicial","diaFinal")
    search_fields = ("id", "nombre","año","mes","diaInicial","diaFinal")
    # Filtrar
    list_filter =("id", "nombre","año","mes","diaInicial","diaFinal")

@admin.register(FuripsLista)
class furipsListaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(FuripsParametro)
class furipsParametroAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre","furipsLista")
    search_fields = ("id", "nombre","furipsLista")
    # Filtrar
    list_filter = ('nombre',"furipsLista")

@admin.register(Archivos)
class archivosAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo", "nombre")
    search_fields = ("id", "tipo", "nombre")
    # Filtrar
    list_filter = ('nombre',"tipo")

@admin.register(Parametros)
class parametrosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "parametro1","fechaRegistro")
    search_fields = ("id", "nombre", "parametro1","fechaRegistro")
    # Filtrar
    list_filter = ("id", "nombre", "parametro1","fechaRegistro")

@admin.register(TiposProfesional)
class tiposProfesionalAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)