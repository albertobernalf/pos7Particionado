from django.contrib import admin

# Register your models here.

from clinico.models import Medicos, Especialidades , TiposExamen, Examenes, Historia, HistoriaExamenes, HistoriaResultados, EspecialidadesMedicos, Servicios, Diagnosticos, EstadosSalida,   EstadoExamenes,  Enfermedades, TiposFolio, TiposAntecedente,  CausasExterna, ViasIngreso , TiposIncapacidad,  HistorialAntecedentes, TiposDiagnostico, HistorialDiagnosticos, HistorialInterconsultas, EstadosInterconsulta
from clinico.models import TiposRadiologia,ViasEgreso, RevisionSistemas, NivelesClinica, TiposTriage, TurnosEnfermeria, TiposSalidas, Eps, TiposCotizante,  Regimenes, Recomendaciones, Hallazgos, NivelesRegimenes, Ips, TiposInterconsulta, ViasAdministracion, UnidadesDeMedidaDosis, FrecuenciasAplicacion, HistoriaMedicamentos, PrincipiosActivos, Medicamentos
from clinico.models import CodigosAtc, FormasFarmaceuticas, HistorialIncapacidades, ExamenesRasgos, HistoriaResultados, HistoriaOxigeno, TipoOxigenacion, TipoDietas, HistorialDietas, HistorialNotasEnfermeria, Enfermedades, HistorialEnfermedades, MedicamentosDci

@admin.register(Servicios)
class serviciosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(Especialidades)
class especialidadesAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)

@admin.register(EspecialidadesMedicos)
class especialidadesMedicosAdmin(admin.ModelAdmin):
    list_display = ("id", "especialidades" ,  "planta", "nombre")
    search_fields = ("id", "especialidades__nombre", "planta__nombre", "nombre")
    # Filtrar
    list_filter = ( "especialidades", "planta", "nombre")


@admin.register(EstadoExamenes)
class estadoExamenesAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)


@admin.register(Enfermedades)
class enfermedadesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)




@admin.register(TiposExamen)
class tiposExamenAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)


@admin.register(TiposFolio)
class tiposFolioAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)

@admin.register(TiposAntecedente)
class tiposAntecedenteAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)


@admin.register(CausasExterna)
class causasExternaAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre","ripsCausaExterna")
            search_fields = ("id", "nombre" ,"ripsCausaExterna")
            # Filtrar
            list_filter = ('nombre',"ripsCausaExterna")

@admin.register(ViasIngreso)
class viasIngresoAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)

@admin.register(TiposIncapacidad)
class tiposIncapacidadAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)

@admin.register(Examenes)
class examenesAdmin(admin.ModelAdmin):

    list_display = ("id","nombre","TiposExamen")
    search_fields = ("id","nombre","TiposExamen__nombre")
    # Filtrar
    list_filter = ("id","nombre","TiposExamen")



@admin.register(HistoriaExamenes)
class historiaExamenesAdmin(admin.ModelAdmin):

    list_display = ( "id", "cantidad","tiposExamen","codigoCups","fechaToma","estadoExamenes")
    search_fields = ( "id", "cantidad","tiposExamen__nombre","codigoCups","fechaToma","estadoExamenes__nombre")
    # Filtrar
    list_filter = ( "id", "cantidad","tiposExamen","codigoCups","fechaToma","estadoExamenes")




@admin.register(HistorialDiagnosticos)
class historialDiagnosticosAdmin(admin.ModelAdmin):
        list_display = ("id", "diagnosticos","tiposDiagnostico")
        search_fields = ("id", "diagnosticos__nombre","tiposDiagnostico__nombre")
        # Filtrar
        list_filter = ("id", "diagnosticos","tiposDiagnostico")



@admin.register(Historia)
class historiaAdmin(admin.ModelAdmin):

        list_display = ("id", "tipoDoc", "documento","folio","fecha","causasExterna")
        search_fields = ("id", "tipoDoc", "documento","folio","fecha","causasExterna__nombre")
        # Filtrar
        list_filter = ('id', 'tipoDoc', 'documento', 'folio', 'fecha', 'causasExterna')



@admin.register(TiposDiagnostico)
class tiposDiagnosticoAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)



@admin.register(Diagnosticos)
class diagnosticosAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre","edadIni","edadFin")
     search_fields = ("id", "nombre","edadIni","edadFin")
      # Filtrar
     list_filter = ('id', 'nombre',"edadIni","edadFin")

@admin.register(EstadosSalida)
class estadosSalidaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")

    # Filtrar
    list_filter = ('id', 'nombre',)


@admin.register(HistorialAntecedentes)
class historialAntecedentesAdmin(admin.ModelAdmin):

        list_display = ("id", "historia","tiposAntecedente","descripcion")
        search_fields = ("id", "historia__id","tiposAntecedente__nombre","descripcion")
        # Filtrar
        list_filter = ("id", "historia","tiposAntecedente","descripcion")

@admin.register(EstadosInterconsulta)
class estadosInterconsultaAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ("id", "nombre")

@admin.register(TiposInterconsulta)
class tiposInterconsultaAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ('id', 'nombre',)



@admin.register(HistorialInterconsultas)
class historialInterconsultasAdmin(admin.ModelAdmin):

        list_display = ("id", "historia","descripcionConsulta","especialidadConsultada","respuestaConsulta","especialidadConsultada","medicoConsultado")
        search_fields = ("id", "historia__id","descripcionConsulta","especialidadConsultada__nombre","respuestaConsulta","especialidadConsultada__nombre","medicoConsultado__nombre")
        # Filtrar
        list_filter =("id", "historia","descripcionConsulta","especialidadConsultada","respuestaConsulta","especialidadConsultada","medicoConsultado")


@admin.register(Medicos)
class medicosAdmin(admin.ModelAdmin):

        list_display = ("id", "planta","departamento")
        search_fields = ("id", "planta","departamento")
        # Filtrar
        list_filter =("id", "planta", "departamento")



@admin.register(Regimenes)
class regimenesAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ('id', 'nombre',)


@admin.register(TiposCotizante)
class tiposCotizanteAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ('id', 'nombre',)


@admin.register(Eps)
class epsAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ('id', 'nombre',)

@admin.register(TiposSalidas)
class tiposSalidasAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ('id', 'nombre',)


@admin.register(TurnosEnfermeria)
class turnosEnfermeriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('id', 'nombre',)


@admin.register(TiposTriage)
class tiposTriageAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('id', 'nombre',)


@admin.register(NivelesClinica)
class nivelesClinicaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('id', 'nombre',)


@admin.register(RevisionSistemas)
class revisionSistemasAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('id', 'nombre',)


@admin.register(Recomendaciones)
class recomendacionesesAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)

@admin.register(Hallazgos)
class hallazgosAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre","miembrosSuperiores","miembrosInferiores","columna","ojos","nariz","oidos","cara","neurologicos","fxCraneo","torax","abdomen","exaMdGeneral","factorTvp","cuello")
            search_fields = ("id", "nombre","miembrosSuperiores","miembrosInferiores","columna","ojos","nariz","oidos","cara","neurologicos","fxCraneo","torax","abdomen","exaMdGeneral","factorTvp","cuello")
            # Filtrar
            list_filter = ("id", "nombre","miembrosSuperiores","miembrosInferiores","columna","ojos","nariz","oidos","cara","neurologicos","fxCraneo","torax","abdomen","exaMdGeneral","factorTvp","cuello")

@admin.register(NivelesRegimenes)
class nivelesRegimenesAdmin(admin.ModelAdmin):
            list_display = ("id","nombre", "regimen","porCuotaModeradora","porCopago","porTopeEve","porTopeAnual")
            search_fields = ("id","nombre", "regimen","porCuotaModeradora","porCopago","porTopeEve","porTopeAnual")
            # Filtrar
            list_filter = ("id", "nombre","regimen","porCuotaModeradora","porCopago","porTopeEve","porTopeAnual")


@admin.register(Ips)
class ipssAdmin(admin.ModelAdmin):

    list_display = ("id", "nombre")
    search_fields =("id", "nombre")
    # Filtrar
    list_filter =("id", "nombre")

@admin.register(TiposRadiologia)
class tiposRadiologiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ("id", "nombre")

@admin.register(ViasAdministracion)
class viasAdministracionAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ("id", "nombre")


@admin.register(UnidadesDeMedidaDosis)
class UnidadesDeMedidaDosisAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion","unidadaDeMedidaPrincipioA")
    search_fields = ("id", "descripcion","unidadaDeMedidaPrincipioA")
    # Filtrar
    list_filter = ("id", "descripcion","unidadaDeMedidaPrincipioA")



@admin.register(FrecuenciasAplicacion)
class frecuenciasAplicacionAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion")
    search_fields = ("id", "descripcion")
    # Filtrar
    list_filter = ("id", "descripcion")


@admin.register(HistoriaMedicamentos)
class historiaMedicamentosAdmin(admin.ModelAdmin):
    list_display = ("id","suministro","historia")
    search_fields = ("id","suministro","historia__id")
    # Filtrar
    list_filter = ("id","suministro","historia")

@admin.register(Medicamentos)
class medicamentosAdmin(admin.ModelAdmin):
    list_display = ("id","nombre")
    search_fields = ("id","nombre")
    # Filtrar
    list_filter = ("id","nombre")

@admin.register(PrincipiosActivos)
class principiosActivosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ("id", "nombre")


@admin.register(CodigosAtc)
class codigoAtcAdmin(admin.ModelAdmin):
    list_display = ("id","codigo",  "nombre")
    search_fields =  ("id","codigo",  "nombre")
    # Filtrar
    list_filter =  ("id","codigo",  "nombre")


@admin.register(FormasFarmaceuticas)
class formasFarmaceuticasAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)


@admin.register(HistorialIncapacidades)
class historialIncapacidadesAdmin(admin.ModelAdmin):

    list_display = ("id", "historia","tiposIncapacidad","desdeFecha","hastaFecha","numDias")
    search_fields =("id", "historia__id","tiposIncapacidad__nombre","desdeFecha","hastaFecha","numDias")
    # Filtrar
    list_filter =("id", "historia","tiposIncapacidad","desdeFecha","hastaFecha","numDias")


@admin.register(ExamenesRasgos)
class examenesRasgosAdmin(admin.ModelAdmin):

        list_display = ("id", "tiposExamen", "codigoCups", "nombre", "unidad","minimo","maximo")
        search_fields = ("id", "tiposExamen__nombre", "codigoCups", "nombre","unidad","minimo","maximo")
        # Filtrar
        list_filter = ("id", "tiposExamen", "codigoCups", "nombre", "unidad","minimo","maximo")


@admin.register(HistoriaResultados)
class historiaResultadosAdmin(admin.ModelAdmin):
    list_display = ("id", "historiaExamenes","fechaServicio","fechaResultado","examenesRasgos","valor")
    search_fields = ("id","historiaExamenes","fechaServicio","fechaResultado","examenesRasgos","valor")
    # Filtrar
    list_filter = ("id", "historiaExamenes","fechaServicio","fechaResultado","examenesRasgos","valor")



@admin.register(TipoOxigenacion)
class tipoOxigenacionAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre", "flujoLtsOxigeno","flujoLtsAire","codFacturar")
        search_fields =("id", "nombre", "flujoLtsOxigeno","flujoLtsAire","codFacturar")
        # Filtrar
        list_filter = ("id", "nombre", "flujoLtsOxigeno","flujoLtsAire","codFacturar")


@admin.register(HistoriaOxigeno)
class historiaOxigenoAdmin(admin.ModelAdmin):

        list_display = ("id", "historia", "tipoOxigenacion","aire","saturacionOxigeno")
        search_fields = ("id", "historia__id", "tipoOxigenacion__nombre","aire","saturacionOxigeno")
        # Filtrar
        list_filter = ("id", "historia", "tipoOxigenacion","aire","saturacionOxigeno")

@admin.register(TipoDietas)
class tipoDietasAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre","fechaRegistro")
        search_fields = ("id", "nombre","fechaRegistro")
        # Filtrar
        list_filter = ('nombre',"fechaRegistro")

@admin.register(HistorialDietas)
class historialDietasAdmin(admin.ModelAdmin):

        list_display = ("id", "historia","tipoDieta","consecutivo","observaciones")
        search_fields = ("id", "historia__id","tipoDieta__nombre","consecutivo","observaciones")
        # Filtrar
        list_filter = ("id", "historia","tipoDieta","consecutivo","observaciones")

@admin.register(HistorialNotasEnfermeria)
class historialNotasEnfermeriaAdmin(admin.ModelAdmin):

        list_display = ("id", "historia","observaciones","fechaRegistro")
        search_fields = ("id", "historia__id","observaciones","fechaRegistro")
        # Filtrar
        list_filter = ("id", "historia","observaciones","fechaRegistro")

@admin.register(HistorialEnfermedades)
class historialEnfermedadesAdmin(admin.ModelAdmin):

        list_display = ("id", "historia","enfermedad","observaciones")
        search_fields = ("id", "historia","enfermedad__nombre","observaciones")
        # Filtrar
        list_filter = ("id", "historia","enfermedad","observaciones")

@admin.register(MedicamentosDci)
class medicamentosDciAdmin(admin.ModelAdmin):

        list_display = ("id", "codigoMipres","descripcionDciConcentracion","tipoMedicamento")
        search_fields = ("id", "codigoMipres","descripcionDciConcentracion","tipoMedicamento")
        # Filtrar
        list_filter =("id", "codigoMipres","descripcionDciConcentracion","tipoMedicamento")