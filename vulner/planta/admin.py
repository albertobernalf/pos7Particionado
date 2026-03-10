from django.contrib import admin

# Register your models here.

from planta.models import TiposPlanta, Planta


@admin.register(TiposPlanta)
class tiposPlantaAdmin(admin.ModelAdmin):

    list_display=("id","nombre")
    search_fields =("id","nombre")
    #readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ('nombre', )

#@admin.register(PerfilesPlanta)
#class perfilesPlantaAdmin(admin.ModelAdmin):

#        list_display = ("id", "sedesClinica",  "tiposPlanta", "planta", "esCajero")
#        search_fields =  ("id", "sedesClinica__nombre",  "tiposPlanta_nombre", "planta__nombre", "esCajero")
        # Filtrar
#        list_filter = ('sedesClinica','planta','tiposPlanta')

@admin.register(Planta)
class plantaAdmin(admin.ModelAdmin):

    list_display = ("id","sedesClinica","tiposPlanta","tipoDoc","documento","nombre","genero","direccion","telefono", "esCajero")
    search_fields = ("id","sedesClinica__nombre","tiposPlanta__nombre","tipoDoc__nombre","documento","nombre","genero","direccion","telefono", "esCajero")
    # Filtrar
    list_filter = ('nombre','sedesClinica',"tiposPlanta",'documento','genero', "esCajero")




