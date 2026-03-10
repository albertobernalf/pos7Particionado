from django.contrib import admin

# Register your models here.

from sitios.models import Departamentos, Ciudades, Centros, SedesClinica, DependenciasTipo, Dependencias,  ServiciosSedes, SubServiciosSedes, HistorialDependencias, Municipios, Paises, Localidades,  ServiciosAdministrativos, Ubicaciones, Bodegas, Salas, TiposSalas, DisponibilidadSalas



@admin.register(SedesClinica)
class sedesClinicaAdmin(admin.ModelAdmin):


    list_display = ("id","nit","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
    search_fields = ("id","nit","departamentos__nombre","ciudades__nombre", "nombre","direccion", "telefono", "contacto","fechaRegistro")
    #Filtrar
    list_filter =('nombre', "nit", 'ciudades')


class CiudadesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre","departamentos")
    search_fields = ("id", "nombre","departamentos__nombre")

    # Filtrar
    list_filter = ('nombre',"departamentos")


class DepartamentosAdmin(admin.ModelAdmin):


    list_display=("id","nombre")

    search_fields =("id","nombre")
    # Filtrar
    list_filter = ('nombre',)

admin.site.register(Departamentos, DepartamentosAdmin)
admin.site.register(Ciudades, CiudadesAdmin)




@admin.register(Centros)
class centrosAdmin(admin.ModelAdmin):
        list_related_name = 'ciudadesDepartamentos'

        list_display = ("id","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
        search_fields = ("id","departamentos__nombre","ciudades__nombre" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
        # Filtrar
        list_filter = ('nombre','departamentos','ciudades','contacto')



@admin.register(ServiciosSedes)
class serviciosSedesAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "servicios","nombre")
    search_fields = ("id","sedesClinica__nombre", "servicios_nombre","nombre")
    # Filtrar
    list_filter = ('nombre', "sedesClinica", "servicios",)


@admin.register(SubServiciosSedes)
class SubServiciosSedesAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "serviciosSedes", "subServiciosSedes","nombre")
    search_fields = ("id","sedesClinica__nombre", "serviciosSedes__nombre","subServiciosSedes","nombre")
    # Filtrar
    list_filter = ('nombre', "sedesClinica", "serviciosSedes","subServiciosSedes")



@admin.register(DependenciasTipo)
class dependenciasTipoAdmin(admin.ModelAdmin):


    list_display = ("id","nombre")
    search_fields = ("id","nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(Dependencias)
class dependenciasAdmin(admin.ModelAdmin):


    list_display = ("id", "sedesClinica","serviciosSedes","subServiciosSedes","numero", "dependenciasTipo", "nombre", "descripcion","cups")
    search_fields =  ("id", "sedesClinica__nombre","serviciosSedes__nombre","subServiciosSedes__nombre","numero", "dependenciasTipo__nombre", "nombre", "descripcion","cups__nombre")
    #fields =  ("sedesClinica","subServicios", "dependenciasTipo","numero", "nombre", "descripcion","cups")
    # Filtrar
    #list_filter = ('nombre', "sedesClinica","subServicios","numero", 'dependenciasTipo','descripcion')


@admin.register(HistorialDependencias)
class historialDependenciasAdmin(admin.ModelAdmin):


    list_display = ("id","dependencias", "tipoDoc", "documento","consec","fechaOcupacion", "fechaLiberacion", "fechaRegistro")
    fields = ( "dependencias__nombre", "tipoDoc__nombre", "documento", "consec", "fechaOcupacion", "fechaLiberacion", "fechaRegistro")
    search_fields = ("id","dependencias", "tipoDoc", "documento","consec","fechaOcupacion", "fechaLiberacion", "fechaRegistro")


@admin.register(Municipios)
class municipiosAdmin(admin.ModelAdmin):


    list_display = ("id", "nombre", "ripsMunicipios","municipioCodigoDian","departamento", "fechaRegistro")
    search_fields = ("id", "nombre", "ripsMunicipios__nombre","departamento", "fechaRegistro")
    # Filtrar
    list_filter = ("id", "nombre","ripsMunicipios", "municipioCodigoDian","departamento", "fechaRegistro")


@admin.register(Paises)
class paisAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "paisCodigoDian", "fechaRegistro")
    search_fields = ("id", "nombre", "paisCodigoDian",  "fechaRegistro")
    # Filtrar
    list_filter = ("id", "nombre", "paisCodigoDian", "fechaRegistro")


@admin.register(Localidades)
class localidadesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "localidadCodigoDian", "municipio", "fechaRegistro")
    search_fields = ("id", "nombre", "localidadCodigoDian", "municipio", "fechaRegistro")
    # Filtrar
    list_filter = ("id", "nombre", "localidadCodigoDian", "municipio", "fechaRegistro")


@admin.register(ServiciosAdministrativos)
class serviciosAdministrativosAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "ubicaciones","dependenciaTipo", "nombre")
    search_fields = ("id","sedesClinica__nombre", "ubicaciones__nombre","dependenciaTipo__nombre", "nombre")
    # Filtrar
    list_filter = ("id","sedesClinica", "ubicaciones","dependenciaTipo", "nombre")


@admin.register(Ubicaciones)
class ubicacionesAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "nombre")
    search_fields = ("id","sedesClinica", "nombre")
    # Filtrar
    list_filter = ("id","sedesClinica", "nombre")


@admin.register(Bodegas)
class bodegasAdmin(admin.ModelAdmin):

    list_display = ("id","sedesClinica","serviciosAdministrativos", "nombre")
    search_fields = ("id","sedesClinica__nombre","serviciosAdministrativos__nombre", "nombre")
    # Filtrar
    list_filter = ("id","sedesClinica","serviciosAdministrativos", "nombre")


@admin.register(Salas)
class salasAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "tipoSala", "dependenciaTipo", "numero", "nombre","serviciosAdministrativos")
    search_fields = ("id","sedesClinica__nombre","tipoSala__nombre", "dependenciaTipo__nombre", "numero", "nombre", "serviciosAdministrativos__nombre")
    # Filtrar
    list_filter = ("id","sedesClinica", "tipoSala", "dependenciaTipo",  "numero","nombre", "serviciosAdministrativos")


@admin.register(TiposSalas)
class tiposSalasAdmin(admin.ModelAdmin):

    list_display = ("id","nombre")
    search_fields = ("id","nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(DisponibilidadSalas)
class disponibilidadSalasAdmin(admin.ModelAdmin):

    list_display = ("id","salas", "fecha", "desdeHora", "hastaHora", "estadoDisponibilidad")
    search_fields = ("id","salas__nombre", "fecha", "desdeHora", "hastaHora", "estadoDisponibilidad")
    # Filtrar
    list_filter = ("id","salas", "fecha", "desdeHora", "hastaHora", "estadoDisponibilidad")



admin.site.site_header = 'Clinica Vulnerable'
admin.site.index_title = 'Panel de control '
admin.site.site_title = 'Administracion'



