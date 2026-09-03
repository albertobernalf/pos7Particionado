from django.contrib import admin


# Register your models here.

from planta.models import Planta
from seguridad.models import Modulos, ModulosElementos,ModulosElementosDef, Perfiles, PerfilesOpciones, Perfiles, PerfilesClinica, PerfilesClinicaOpciones, PerfilesUsu, PerfilesGralUsu

@admin.register(Modulos)
class modulosAdmin(admin.ModelAdmin):

    list_display=("id","nombre","nomenclatura","logo","estadoReg")
    search_fields =("id","nombre","nomenclatura","logo","estadoReg")
    #readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ('nombre', "nomenclatura")

@admin.register(ModulosElementos)
class modulosElementosAdmin(admin.ModelAdmin):

    list_display=("id","nombre")
    search_fields = ("id","nombre")
    #readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ("id","nombre")


@admin.register(ModulosElementosDef)
class modulosElementosDefAdmin(admin.ModelAdmin):

    list_display=("id","modulosId","modulosElementosId","nombre","descripcion","url","estadoReg")
    search_fields =("id","modulosId","modulosElementosId","nombre","descripcion","url","estadoReg")
    #readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ('nombre', "descripcion","estadoReg")





@admin.register(Perfiles)
class perfilesAdmin(admin.ModelAdmin):

    list_display = ("id", "nombre", "estadoReg")
    search_fields = ("id", "nombre", "estadoReg")
    # readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ("id","nombre")


@admin.register(PerfilesOpciones)
class perfilesOpcionesAdmin(admin.ModelAdmin):
    list_display = ("id", "perfilesId", "modulosElementosDefId", "estadoReg")
    search_fields = ("id", "perfilesId", "modulosElementosDefId", "estadoReg")
    # readonly_fields = ["nombre"]
    # Filtrar
    list_filter =  ("id", "perfilesId", "modulosElementosDefId", "estadoReg")

@admin.register(PerfilesClinica)
class perfilesClinicaAdmin(admin.ModelAdmin):

    list_display = ("id","sedesClinica", "nombre", "modulosId","estadoReg")
    search_fields = ("id", "sedesClinica__nombre", "nombre","modulosId", "estadoReg")
    # readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ('id', "sedesClinica","modulosId",'nombre')


@admin.register(PerfilesClinicaOpciones)
class perfilesClinicaOpcionesAdmin(admin.ModelAdmin):
    list_display = ("id", "perfilesClinicaId", "modulosElementosDefId", "estadoReg")
    search_fields = ("id", "perfilesClinicaId", "modulosElementosDefId", "estadoReg")
    # readonly_fields = ["nombre"]
    # Filtrar
    list_filter =  ("id", "perfilesClinicaId", "modulosElementosDefId", "estadoReg")


@admin.register(PerfilesUsu)
class perfilesUsuAdmin(admin.ModelAdmin):
    list_display = ("id", "plantaId","perfilesClinicaOpcionesId", "adicion", "estadoReg")
    search_fields = ("id", "plantaId__nombre","perfilesClinicaOpcionesId", "adicion", "estadoReg")
    # readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ("id", "plantaId","perfilesClinicaOpcionesId", "adicion", "estadoReg")


@admin.register(PerfilesGralUsu)
class perfilesGralUsuAdmin(admin.ModelAdmin):
    list_display = ("id", "plantaId","perfilesClinicaId",  "estadoReg")
    search_fields = ("id", "plantaId__nombre","perfilesClinicaId__nombre",  "estadoReg")
    # readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ("id", "plantaId","perfilesClinicaId",  "estadoReg")



