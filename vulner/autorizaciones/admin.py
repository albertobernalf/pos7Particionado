from django.contrib import admin

# Register your models here.


from autorizaciones.models import  Autorizaciones, AutorizacionesDetalle, AutorizacionesCirugias, EstadosAutorizacion


@admin.register(Autorizaciones)
class autorizacionesAdmin(admin.ModelAdmin):
    list_display = ("id", "sedesClinica", "historia","estadoAutorizacion", "fechaSolicitud","empresa","fechaAutorizacion")
    #search_fields = ['id', 'sedesClinica__nombre', 'historia','estadoAutorizacion_nombre', 'fechaSolicitud','empresa','fechaAutorizacion',]
    search_fields = ['id', 'sedesClinica__nombre','historia__id','estadoAutorizacion__nombre' , 'fechaSolicitud','empresa__nombre','fechaAutorizacion']
    # Filtrar
    list_filter = ("id", "sedesClinica", "historia", "estadoAutorizacion","fechaSolicitud","empresa","fechaAutorizacion")


@admin.register(AutorizacionesDetalle)
class autorizacionesDetalleAdmin(admin.ModelAdmin):
    list_display = ("id",  "autorizaciones", "estadoAutorizacion","cantidadSolicitada","cantidadAutorizada","numeroAutorizacion")
    search_fields = ("id", "autorizaciones", "estadoAutorizacion__nombre","cantidadSolicitada","cantidadAutorizada","numeroAutorizacion")
    # Filtrar
    # list_filter =("id",  "autorizaciones","estadoAutorizacion","cantidadSolicitada","cantidadAutorizada","numeroAutorizacion")



@admin.register(AutorizacionesCirugias)
class autorizacionesCirugiasAdmin(admin.ModelAdmin):

   list_display = ("id", "sedesClinica", "tipoDoc","documento","hClinica","consec", "autorizacionesId","fechaRegistro","usuarioRegistro")
   search_fields = ("id", "sedesClinica__nombre", "tipoDoc__nombre","documento","hClinica","consec", "autorizacionesId","fechaRegistro","usuarioRegistro")
   # Filtrar
   # list_filter = ("id", "sedesClinica", "tipoDoc","documento","hClinica","consec", "autorizacionesId","fechaRegistro","usuarioRegistro")

@admin.register(EstadosAutorizacion)
class estadosAutorizacionAdmin(admin.ModelAdmin):

   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   # list_filter = ("id", "nombre")

