from django.contrib import admin

from django import forms

# Register your models here.

from Administracion.models import Mae_Reportes , Mae_GrupoReportes, Mae_RepUsuarios, Mae_RepParametros, Mae_TiposCampo, Imhotep_SedesReportes , Mae_SubGrupoReportes
from Administracion.forms import Mae_ReportesForm


#@admin.register(Mae_ReportesAdmin)
class mae_ReportesAdmin(admin.ModelAdmin):

    list_display  = ("id","mae_gruporeportes","mae_subgruporeportes","nom_reporte","usuario_crea","fechaRegistro","descripcion","cuerpo_sql", "encabezados","excel","pdf","csv", "grilla","estadoreg")
    search_fields = ("id","mae_gruporeportes__id","mae_subgruporeportes__id","nom_reporte","usuario_crea","fechaRegistro","descripcion","cuerpo_sql", "encabezados", "excel","pdf","csv", "grilla","estadoreg")
    # Filtrar
    list_filter = ("mae_gruporeportes","mae_subgruporeportes","nom_reporte","usuario_crea","fechaRegistro","descripcion", "excel","pdf","csv","grilla", "estadoreg")

    form = Mae_ReportesForm






class mae_GrupoReportesAdmin(admin.ModelAdmin):

    list_display  = ("id","nom_grupo","logo","estadoreg")
    search_fields = ("id","nom_grupo","logo","estadoreg")
    # Filtrar
    list_filter = ("id","nom_grupo","logo","estadoreg")

    def get_actions(self, request):
        actions = super(mae_GrupoReportesAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class mae_SubGrupoReportesAdmin(admin.ModelAdmin):

    list_display  = ("id","mae_gruporeportes","nom_subgrupo","logo","estadoreg")
    search_fields = ("id","mae_gruporeportes","nom_subgrupo","logo","estadoreg")
    # Filtrar
    list_filter = ("id","mae_gruporeportes","nom_subgrupo","logo","estadoreg")

    def get_actions(self, request):
        actions = super(mae_SubGrupoReportesAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False



class mae_RepUsuariosAdmin(admin.ModelAdmin):
    list_display = ("cod_sede","mae_reportes", "cod_usuario", "estadoreg")
    search_fields = ("mae_reportes__id","cod_usuario", "estadoreg")
    # Filtrar

    list_filter = ("cod_sede", "mae_reportes", "cod_usuario",  "estadoreg")

class mae_RepParametrosAdmin(admin.ModelAdmin):
    list_display = ("id", "mae_reportes","parametro","parametro_texto","mae_tiposcampo",  "estadoreg")
    search_fields =("id", "mae_reportes","parametro","parametro_texto","mae_tiposcampo",  "estadoreg")
    # Filtrar

    list_filter = ( "mae_reportes","parametro_texto", "estadoreg")

class mae_TiposCampoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields =("id", "nombre")
    # Filtrar

    list_filter = ("id", "nombre")

    def get_actions(self, request):
        actions = super(mae_TiposCampoAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class imhotep_SedesReportesAdmin(admin.ModelAdmin):
        list_display = ("id", "codreg_sede", "nom_sede","codreg_ips","direccion","telefono","departamento","municipio")
        search_fields = ("id", "codreg_sede", "nom_sede","codreg_ips","direccion","telefono","departamento","municipio")
        # Filtrar

        list_filter = ("id", "codreg_sede", "nom_sede","codreg_ips","direccion","telefono","departamento","municipio")

        def get_actions(self, request):
            actions = super(imhotep_SedesReportesAdmin, self).get_actions(request)
            if 'delete_selected' in actions:
                del actions['delete_selected']
            return actions

        def has_delete_permission(self, request, obj=None):

            return False

admin.site.register(Mae_Reportes, mae_ReportesAdmin)
admin.site.register(Mae_GrupoReportes, mae_GrupoReportesAdmin)
admin.site.register(Mae_SubGrupoReportes, mae_SubGrupoReportesAdmin)
admin.site.register(Mae_RepUsuarios, mae_RepUsuariosAdmin)
admin.site.register(Mae_RepParametros, mae_RepParametrosAdmin)
admin.site.register(Mae_TiposCampo, mae_TiposCampoAdmin)
admin.site.register(Imhotep_SedesReportes, imhotep_SedesReportesAdmin)

