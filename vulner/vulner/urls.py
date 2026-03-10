"""vulner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf  import settings
from django.conf.urls.static import  static

from django.urls import path, include
from camara import  views as viewsCamara

#from Reportes import views as viewsReportes

from admisiones import views as viewsAdmisiones
from admisiones import viewsReportes as viewsAdmisionesReportes
from triage import views as viewsTriage
from triage import viewsReportes as viewsTriageReportes
from usuarios import views as viewsUsuarios

from django.conf  import settings
from django.conf.urls.static import  static
from clinico import views as viewsClinico
from clinico import viewsReportes as viewsClinicoReportes
from terapeutico import views as viewsApoyoTerapeutico
from facturacion import views as viewsFacturacion
from facturacion import viewsReportes as viewsFacturacionReportes
from contratacion import views as viewsConvenios
from tarifarios import views as viewsTarifarios
from rips import views as viewsRips
from cartera import views as viewsCartera
from cirugia import views as viewsCirugia
from farmacia import views as viewsFarmacia
from enfermeria import views as viewsEnfermeria
from Reportes import views as  viewsReportesR
from sitios import views as  viewsSitios

from autorizaciones import views as viewsAutorizaciones
from autorizaciones import viewsReportes as viewsAutorizacionesReportes

#from mecanicosPacientes import views as viewsmecanicosPacientes
from farmacia import viewsReportes as viewsFarmaciaReportes


urlpatterns = [
    path('admin/', admin.site.urls),

    # Primero Reporteador

    path('chaining/', include('smart_selects.urls')),
    #path('medicalReport/', viewsReportesR.menuAcceso),
    #path('medicalReport/', viewsReportesR.menuAcceso),
    #path('validaAcceso/', viewsReportes.validaAcceso),
    path('validaAccesoR/', viewsReportesR.validaAccesoR),
    path('salir/', viewsAdmisiones.menuAcceso),
    path('pantallaSubgrupos/<str:username>, <str:sedeSeleccionada>, <str:grupo>', viewsReportesR.pantallaSubgrupos),
    path('emergenteGrupos/<str:username>, <str:sedeSeleccionada>, <str:grupo>', viewsReportesR.emergenteGrupos),
    path('combo/<str:username>, <str:sedeSeleccionada>, <str:grupo>, <str:subGrupo>', viewsReportesR.combo),
    #path('/combo/<str:username>, <str:sedeSeleccionada>, <str:grupo>, <str:subGrupo>', views.combo),

    # path('contrasena/<str:documento>', views.contrasena),
 
    ## Invoca Reporte

    path('Reporte1/<str:numreporte>,<str:username>,<str:sedeSeleccionada>,<str:grupo>,<str:subGrupo>',
         viewsReportesR.Reporte1PdfView.as_view()),
    # path('Reporte2/<str:numreporte>,<str:username>,<str:sedeSeleccionada>,<str:grupo>,<str:subGrupo>', views.Reporte1PdfView.as_view()),

    # Fin Reporteador

    #Carque de datos

    path('import_datos_global_1/', viewsUsuarios.import_datos_global_1),
    path('import_datos_global_2/', viewsUsuarios.import_datos_global_2),
    path('import_datos/', viewsUsuarios.import_datos),

    # Acceso al Programa General Clinico

    path('menu/', viewsCamara.menu),
    # path('menuAcceso/validaAcceso/', views.validaAcceso),
    path('contrasena/<str:documento>', viewsCamara.contrasena),
    # path('salir/validaAcceso/', views.validaAcceso),

    # HISTORIA CLINICA

    # path('accesoEspecialidadMedico/historiaView/<str:documento>', viewsClinico.nuevoView.as_view()),
    # path('historia1View/', viewsClinico.historia1View),
    # path('historiaExamenesView/', viewsClinico.historiaExamenesView),
    # path('consecutivo_folios/', viewsClinico.consecutivo_folios),
    # path('buscaExamenes/', viewsClinico.buscaExamenes),
    path('motivoSeñas/', viewsClinico.motivoSeñas),
    path('subjetivoSeñas/', viewsClinico.subjetivoSeñas),
    path('motivoInvidente/', viewsClinico.motivoInvidente),
    # path('resMotivoInvidente/', viewsClinico.s),
    path('reconocerAudio/', viewsCamara.reconocerAudio),
    path('reproduceAudio/', viewsCamara.reproduceAudio),
    path('accesoEspecialidadMedico/<str:documento>', viewsCamara.accesoEspecialidadMedico),
    path('crearHistoriaClinica/', viewsClinico.crearHistoriaClinica),
    # path('crearHistoriaClinica1/', viewsClinico.crearHistoriaClinica1.as_view()),
    #path('buscarAdmisionClinico/', viewsClinico.buscarAdmisionClinico),
    path('cargaPanelMedico/<str:data>',  viewsClinico.load_dataClinico, name='loaddataClinico'),
    #path('buscarAntecedentes/', viewsClinico.buscarAntecedentes),
    path('load_dataClinico/<str:data>', viewsClinico.load_dataClinico, name='loaddataClinico'),
    #path('creacionHC/postConsultaHc/<str:id>/edit/', viewsClinico.PostConsultaHc, name='Post_editHc'),
    #path('creacionHC/<str:id>', viewsClinico.PostConsultaHcli),
    path('creacionHc/postConsultaHcli/', viewsClinico.PostConsultaHcli , name='Post_editHc'),
    path('imprimirHistoriaClinica/', viewsClinicoReportes.ImprimirHistoriaClinica, name='Post_imprimirHc'),
    path('imprimirOrdenIncapacidad/<str:ingresoId> , <str:historiaId>/', viewsClinicoReportes.ImprimirOrdenIncapacidad),
    path('imprimirOrdenLaboratorio/<str:ingresoId> , <str:historiaId>, <str:convenioId>,<str:tipoAdmision>/', viewsClinicoReportes.ImprimirOrdenLaboratorio),
    path('imprimirOrdenTerapia/<str:ingresoId> , <str:historiaId>, <str:convenioId>,<str:tipoAdmision>/', viewsClinicoReportes.ImprimirOrdenTerapia),
    path('imprimirOrdenDeControl/<str:ingresoId> , <str:historiaId>, <str:convenioId>,<str:tipoAdmision>/', viewsClinicoReportes.ImprimirOrdenDeControl),
    path('imprimirOrdenRadiologia/<str:ingresoId> , <str:historiaId>, <str:convenioId>,<str:tipoAdmision>/', viewsClinicoReportes.ImprimirOrdenRadiologia),


    path('traerMedicosEspecialidad/', viewsClinico.TraerMedicosEspecialidad),
    path('load_dataInterConsultas/<str:data>', viewsClinico.load_dataInterConsultas),
    path('guardarInterConsulta/', viewsClinico.GuardarInterConsulta),
    path('leerInterConsulta/', viewsClinico.LeerInterConsulta),
    path('load_dataInfoRadiologia/<str:data>', viewsClinico.load_dataInfoRadiologia),
    path('load_dataInfoLaboratorio/<str:data>', viewsClinico.load_dataInfoLaboratorio),
    path('load_dataInfoTerapia/<str:data>', viewsClinico.load_dataInfoTerapia),
    path('load_dataInfoNoQx/<str:data>', viewsClinico.load_dataInfoNoQx),
    path('load_dataInfoAntecedente/<str:data>', viewsClinico.load_dataInfoAntecedente),
    path('load_dataInfoNotasEnfermeria/<str:data>', viewsClinico.load_dataInfoNotasEnfermeria),
    path('load_dataInfoMedicamento/<str:data>', viewsClinico.load_dataInfoMedicamento),
    path('load_dataInfoInterConsulta/<str:data>', viewsClinico.load_dataInfoInterConsulta),
    path('load_dataInfoRevisionSistemas/<str:data>', viewsClinico.load_dataInfoRevisionSistemas),
    path('load_dataInfoSignosVital/<str:data>', viewsClinico.load_dataInfoSignosVital),
    path('load_dataInfoEnfermedad/<str:data>', viewsClinico.load_dataInfoEnfermedad),
    path('load_dataInfoDiagnostico/<str:data>', viewsClinico.load_dataInfoDiagnostico),
    path('load_dataInfoIncapacidad/<str:data>', viewsClinico.load_dataInfoIncapacidad),
    path('load_dataInfoEvolucion/<str:data>', viewsClinico.load_dataInfoEvolucion),
    path('obtener_pdf/', viewsClinico.Obtener_pdf),


    # Actividaes Mecanicas

    path('prueba/', viewsClinico.prueba),
    #   path('manejoLuz/', viewsmecanicosPacientes.manejoLuz.as_view()),
    #  path('ambienteMusical/', viewsmecanicosPacientes.ambienteMusical.as_view()),
    path('camara/', viewsCamara.camara),
    path('leeAudio/', viewsCamara.leeAudio),

    path('chaining/', include('smart_selects.urls')),

    # Acceso global

    path('medicalSocial/', viewsAdmisiones.menuAcceso),

    # Admisiones

    path('validaAcceso/', viewsAdmisiones.validaAcceso),
    #path('menuAccesoClinico/', viewsAdmisiones.menuAcceso),
    path('validaAccesoClinico/', viewsAdmisiones.validaAcceso),
    path('escoge/', viewsAdmisiones.escogeAcceso),
    path('escoge/<str:Sede>,<str:Username>,<str:Profesional>,<str:Documento>,<str:NombreSede>,<str:escogeModulo>', viewsAdmisiones.escogeAcceso),

    path('retornarAdmision/<str:Sede>, <str:Perfil> , <str:Username>, <str:Username_id>, <str:NombreSede>',
         viewsAdmisiones.retornarAdmision),


    path('retornarMen/<str:Sede>,<str:Username>,<str:Documento>,<str:NombreSede>,<str:Profesional>', viewsAdmisiones.RetornarMen),

    path('grabar1/<str:username>,<str:contrasenaAnt>,<str:contrasenaNueva>,<str:contrasenaNueva2>',
         viewsAdmisiones.validaPassword),
    path('findOne/<str:username> , <str:password> , <str:tipoDoc>/', viewsAdmisiones.Modal),
    # path('buscarAdmision/<str:BusHabitacion>,<str:BusTipoDoc>,<str:BusDocumento>,<str:BusPaciente>,<str:BusDesde>,<str:BusHasta>', viewsAdmisiones.buscarAdmision),
    path('buscarAdmision/', viewsAdmisiones.buscarAdmision),

    path('buscarEspecialidadesMedicos/', viewsAdmisiones.buscarEspecialidadesMedicos),
    path('buscarPaises/', viewsAdmisiones.buscarPaises),
    path('buscarCiudades/', viewsAdmisiones.buscarCiudades),
    path('buscarHabitaciones/', viewsAdmisiones.buscarHabitaciones),
    path('buscarMunicipios/', viewsAdmisiones.buscarMunicipios),

    path('buscarLocalidades/', viewsAdmisiones.buscarLocalidades),

    path('buscarSubServicios/', viewsAdmisiones.buscarSubServicios),
    # path('crearAdmision/<str:Sede>,<str:Perfil>, <str:Username>, <str:Username_id>', viewsAdmisiones.crearAdmision.as_view()),
    path('crearAdmisionDef/', viewsAdmisiones.crearAdmisionDef),

    path('findOneUsuario/', viewsAdmisiones.UsuariosModal),
    path('guardarUsuariosModal/', viewsAdmisiones.guardarUsuariosModal),
    path('crearResponsables/', viewsAdmisiones.crearResponsables),
    path('cambioServicio/', viewsAdmisiones.cambioServicio),
    path('guardaCambioServicio/', viewsAdmisiones.guardaCambioServicio),
    path('load_dataConvenioAdmisiones/<str:data>', viewsAdmisiones.load_dataConvenioAdmisiones, name='loaddataAdmisiones'),
    path('guardaConvenioAdmision/', viewsAdmisiones.GuardaConvenioAdmision, name='guardaConvenioAdmision'),
    path('buscaConveniosAbonoAdmision/', viewsAdmisiones.BuscaConveniosAbonoAdmision, name='buscaConveniosAbono_Admision'),


    path('postDeleteConveniosAdmision/', viewsAdmisiones.PostDeleteConveniosAdmision, name='postDeleteConveniosAdmision'),
    path('guardarResponsableAdmision/', viewsAdmisiones.GuardarResponsableAdmision, name='guardarResponsableAdmision'),
    path('guardarAcompananteAdmision/', viewsAdmisiones.GuardarAcompananteAdmision, name='guardarAcompananteAdmision'),
    path('load_dataAbonosAdmisiones/<str:data>', viewsAdmisiones.load_dataAbonosAdmisiones,   name='loaddataAbonosAdmisiones'),
    path('guardaAbonosAdmision/', viewsAdmisiones.GuardaAbonosAdmision, name='guardaAbonosAdmision'),
    path('postDeleteAbonosAdmision/', viewsAdmisiones.PostDeleteAbonosAdmision, name='postDeleteAbonosAdmision'),
    path('guardaFurips/', viewsAdmisiones.GuardaFurips, name='guardaFurips'),
    #path('encuentraAdmisionModal/<str:tipoDoc> , <str:documento> , <str:consec> , <str:sede>/', viewsAdmisiones.encuentraAdmisionModal, name='encuentraAdmisionModal'),
    path('impresionManilla/', viewsAdmisionesReportes.ImpresionManilla),
    path('encuentraAdmisionModal/', viewsAdmisiones.encuentraAdmisionModal),
    path('load_dataAdmisiones/<str:data>', viewsAdmisiones.load_dataAdmisiones,   name='loaddata_Admisiones'),
    path('load_dataAutorizacionesAdmisiones/<str:data>', viewsAdmisiones.Load_dataAutorizacionesAdmisiones, name='loaddata_AutorizacionesAdmisiones'),
    path('actualizaAdmision/', viewsAdmisiones.ActualizaAdmision),
    path('load_dataCensoAdmisiones/<str:data>', viewsAdmisiones.Load_dataCensoAdmisiones, name='load_dataCenso_Admisiones'),
    path('load_dataHabitacionesAdmisiones/<str:data>', viewsAdmisiones.Load_dataHabitacionesAdmisiones, name='load_dataHabitaciones_Admisiones'),
    path('imprimirAtencionUrgencias/', viewsAdmisionesReportes.ImprimirAtencionUrgencias),
    path('imprimirHojaAdmision/', viewsAdmisionesReportes.ImprimirHojaAdmision),
    path('imprimirHojaAdmisionParametro/<str:ingresoId>/', viewsAdmisionesReportes.ImprimirHojaAdmisionParametro),
    path('imprimirAutorizacionesAdm/', viewsAdmisionesReportes.ImprimirAutorizacionesAdm),
    path('buscarConvenioEmpresa/', viewsAdmisiones.buscarConvenioEmpresa),
    path('indicadores/', viewsAdmisiones.Indicadores , name = "indicadores_1"),
    path('imprimirManillaAdmision/', viewsAdmisionesReportes.ImpresionManilla , name='imprimir_manilla'),


    # Triage

    path('crearTriage/', viewsTriage.crearTriage),
    path('buscarTriage/', viewsTriage.buscarTriage),
    path('buscarSubServiciosTriage/', viewsTriage.buscarSubServiciosTriage),
    path('buscarHabitacionesTriage/', viewsTriage.buscarHabitacionesTriage),
    path('encuentraTriageModal/<str:tipoDoc> , <str:documento>, <str:sede>/', viewsTriage.encuentraTriageModal),
    path('encuentraTriageModal/', viewsTriage.encuentraTriageModal),
    path('findOneUsuarioTriage/', viewsTriage.UsuariosModalTriage),
    path('grabaUsuariosTriage/', viewsTriage.grabaUsuariosTriage),
    path('grabaTriageModal/', viewsTriage.grabaTriageModal),
    path('admisionTriageModal/', viewsTriage.admisionTriageModal),
    path('guardarAdmisionTriage/', viewsTriage.guardarAdmisionTriage),
    path('load_dataTriage/<str:data>', viewsTriage.Load_dataTriage, name='loaddata_Triage'),
    path('buscarEspecialidadesMedicos/', viewsTriage.buscarEspecialidadesMedicos),
    path('imprimirAtencionInicialUrgencias/<str:ingresoId>/', viewsTriageReportes.ImprimirAtencionInicialUrgencias),
    #path('imprimirAtencionUrgencias/', viewsTriageReportes.ImprimirAtencionUrgencias),
    path('imprimirHojaAdmisionParametro/<str:ingresoId>/', viewsTriageReportes.ImprimirHojaAdmision),
    path('imprimirHojaAdmision/', viewsTriageReportes.ImprimirHojaAdmision),
    path('imprimirManilla/<str:ingresoId>/', viewsTriageReportes.ImprimirManilla),
    path('buscarMunicipios/', viewsTriage.buscarMunicipios),
    path('buscarCiudades/', viewsTriage.buscarCiudades),
    path('buscarPaises/', viewsTriage.buscarPaises),
    path('buscarLocalidades/', viewsTriage.buscarLocalidades),
    path('imprimirTriageParametro/<str:data>/', viewsTriageReportes.ImprimirTriageParametro),
    path('imprimirTriage/', viewsTriageReportes.ImprimirTriage),
    path('buscarConvenioEmpresa/', viewsTriage.buscarConvenioEmpresa),

    # Apoyo Terapeutico

    path('load_dataApoyoTerapeutico/<str:data>', viewsApoyoTerapeutico.load_dataApoyoTerapeutico, name='loaddataApoyoTerapeutico'),
    path('load_dataOrdenadosTerapeutico/<str:data>', viewsApoyoTerapeutico.load_dataOrdenadosTerapeutico, name='loaddataOrdenados_Terapeutico'),
    path('load_dataNoOrdenadosTerapeutico/<str:data>', viewsApoyoTerapeutico.load_dataNoOrdenadosTerapeutico, name='loaddataNoOrdenados_Terapeutico'),
    path('load_dataRasgos/<str:data>', viewsApoyoTerapeutico.load_dataRasgos, name='loadDataRasgos'),
    path('postConsultaOrdenadosApoyoTerapeutico/', viewsApoyoTerapeutico.PostConsultaOrdenadosApoyoTerapeutico , name='Post_consultaordenadosApoyoTerapeutico'),
    path('guardarResultadoRasgo/', viewsApoyoTerapeutico.GuardarResultadoRasgo, name='guardarResultado_Rasgo'),
    path('postDeleteExamenesRasgos/', viewsApoyoTerapeutico.PostDeleteExamenesRasgos, name='PostDeleteExamenesRasgos'),
    path('guardarResultado/', viewsApoyoTerapeutico.GuardarResultado, name='GuardarResultado'),
    path('load_dataTerapeuticoConsulta/<str:data>', viewsApoyoTerapeutico.load_dataTerapeuticoConsulta, name='loaddataTerapeuticoConsulta'),
    path('load_dataRasgosConsulta/<str:data>', viewsApoyoTerapeutico.load_dataRasgosConsulta, name='loadDataRasgos_Consulta'),
    path('postConsultaNoOrdenadosTerapeuticoConsulta/', viewsApoyoTerapeutico.PostConsultaNoOrdenadosTerapeuticoConsulta , name='post_ConsultaNoOrdenadosTerapeuticoConsulta'),

    # Facturacion

    path('load_dataLiquidacion/<str:data>', viewsFacturacion.load_dataLiquidacion, name='loaddataLiquidacion'),
    path('load_dataLiquidacionDetalle/<str:data>', viewsFacturacion.load_dataLiquidacionDetalle, name='loaddataLiquidacionDetalle'),
    path('load_dataFacturacionDetalle/<str:data>', viewsFacturacion.load_dataFacturacionDetalle,name='load_data_FacturacionDetalle'),
    path('postConsultaLiquidacion/', viewsFacturacion.PostConsultaLiquidacion , name='Post_editLiquidacion'),
    path('postConsultaLiquidacionDetalle/', viewsFacturacion.PostConsultaLiquidacionDetalle , name='Post_editLiquidacionDetalle'),
    path('guardaAbonosFacturacion/', viewsFacturacion.GuardaAbonosFacturacion, name='guardaAbonosFacturacion'),
    path('postDeleteAbonosFacturacion/', viewsFacturacion.PostDeleteAbonosFacturacion, name='postDeleteAbonosFacturacion'),
    path('postDeleteLiquidacionDetalle/', viewsFacturacion.PostDeleteLiquidacionDetalle, name='postDeleteLiquidacionDetalle'),
    path('guardarLiquidacionDetalle/', viewsFacturacion.GuardarLiquidacionDetalle, name='guardarLiquidacionDetalle'),
    path('editarGuardarLiquidacionDetalle/', viewsFacturacion.EditarGuardarLiquidacionDetalle, name='editarGuardarLiquidacionDetalle'),
    path('load_dataAbonosFacturacion/<str:data>', viewsFacturacion.load_dataAbonosFacturacion, name='loaddataAbonosFacturacion'),
    path('facturarCuenta/', viewsFacturacion.FacturarCuenta, name='facturarCuenta'),
    path('leerTotales/', viewsFacturacion.LeerTotales, name='leerTotales'),
    path('leerTotalesFactura/', viewsFacturacion.LeerTotalesFactura, name='leerTotales_Factura'),
    path('postConsultaFacturacion/', viewsFacturacion.PostConsultaFacturacion , name='PostConsultaFacturacion'),
    path('anularFactura/', viewsFacturacion.AnularFactura , name='anularFactura'),
    path('reFacturar/', viewsFacturacion.ReFacturar , name='reFacturar'),
    path('load_dataFacturacion/<str:data>', viewsFacturacion.load_dataFacturacion, name='loaddataFacturacion'),
    path('guardaApliqueAbonosFacturacion/', viewsFacturacion.GuardaApliqueAbonosFacturacion, name='guardaApliqueAbonosFacturacion'),
    path('trasladarConvenio/', viewsFacturacion.TrasladarConvenio, name='trasladarConvenio'),
    path('buscoAbono/', viewsFacturacion.BuscoAbono, name='buscoAbono'),
    path('imprimirFactura/', viewsFacturacionReportes.ImprimirFactura),
    path('imprimirLiquidacion/', viewsFacturacionReportes.ImprimirLiquidacion),
    path('load_dataReFacturacion/<str:data>', viewsFacturacion.load_dataReFacturacion, name='loaddata_ReFacturacion'),
    path('generarJson/', viewsFacturacion.GenerarJson , name='Generar_json'),
    path('envioDian/', viewsFacturacion.EnvioDian , name='Envio_dian'),
    path('imprimirPazYSalvo/', viewsFacturacionReportes.ImprimirPazYSalvo , name='Imprimir_PazYSalvo'),
    path('crearEnvioDian/', viewsFacturacion.CrearEnvioDian , name='Crear_Envio_dian'),

    # Rips

    path('load_dataEnviosRips/<str:data>', viewsRips.load_dataEnviosRips, name='loaddataEnviosRips'),
    path('guardaEnviosRips/', viewsRips.GuardaEnviosRips, name='GuardaEnviosRips'),
    path('actualizarEmpresaDetalleRips/', viewsRips.ActualizarEmpresaDetalleRips, name='ActualizarEmpresaDetalleRips'),
    path('load_dataDetalleRips/<str:data>', viewsRips.load_dataDetalleRips, name='loaddataDetalleRips'),
    path('guardaDetalleRips/', viewsRips.GuardaDetalleRips, name='GuardaDetalleRips'),
    path('load_dataDetalleRipsAdicionar/<str:data>', viewsRips.load_dataDetalleRipsAdicionar, name='loaddataDetalleRipsAdicionar'),
    path('traeDetalleRips/', viewsRips.TraeDetalleRips, name='TraeDetalleRips'),
    path('traerJsonEnvioRips/', viewsRips.TraerJsonEnvioRips, name='TraerJsonEnvioRips'),
    path('traerJsonRips/', viewsRips.TraerJsonRips, name='TraerJsonRips'),
    path('borrarDetalleRips/', viewsRips.BorrarDetalleRips, name='borrarDetalleRips'),
    path('guardarRadicacionRips/', viewsRips.GuardarRadicacionRips, name='GuardarRadicacion_Rips'),
    path('generarJsonRips/', viewsRips.GenerarJsonRips, name='generarJsonRips'),
    path('enviarJsonRips/', viewsRips.EnviarJsonRips, name='enviarJsonRips'),
    path('load_tablaRipsTransaccion/<str:data>', viewsRips.Load_tablaRipsTransaccion, name='load_tablaRipsTransaccion'),
    path('load_tablaRipsUsuarios/<str:data>', viewsRips.Load_tablaRipsUsuarios, name='load_tablaRipsUsuarios'),
    path('load_tablaRipsProcedimientos/<str:data>', viewsRips.Load_tablaRipsProcedimientos, name='load_tablaRipsProcedimientos'),
    path('load_tablaRipsHospitalizacion/<str:data>', viewsRips.Load_tablaRipsHospitalizacion, name='load_tablaRipsHospitalizacion'),
    path('load_tablaRipsUrgenciasObs/<str:data>', viewsRips.Load_tablaRipsUrgenciasObs, name='load_tablaRipsUrgenciasObs'),
    path('load_tablaRipsMedicamentos/<str:data>', viewsRips.Load_tablaRipsMedicamentos,name='load_tablaRipsMedicamentos'),
    path('load_dataRipsEnviados/<str:data>', viewsRips.load_dataRipsEnviados, name='load_dataRips_Enviados'),
    path('guardarRespuestaRips/', viewsRips.GuardarRespuestaRips, name='guardarRespuestaRips'),
    path('reversarEnvioRips/', viewsRips.ReversarEnvioRips, name='reversarEnvio_Rips'),


    # Autorizaciones

    path('load_dataAutorizaciones/<str:data>', viewsAutorizaciones.load_dataAutorizaciones, name='loaddataAutorizaciones'),
    path('load_dataAutorizacionesDetalle/<str:data>', viewsAutorizaciones.load_dataAutorizacionesDetalle, name='loaddataAutorizacionesDetalle'),
    path('actualizarAutorizacionDetalle/', viewsAutorizaciones.ActualizarAutorizacionDetalle, name='actualizarAutorizacionDetalle'),
    path('leerDetalleAutorizacion/', viewsAutorizaciones.LeerDetalleAutorizacion,  name='LeerDetalleAutorizacion'),
    path('imprimirAut/', viewsAutorizacionesReportes.ImprimirAut, name='Imprimir_Aut'),
    path('imprimirAut/<str:data>', viewsAutorizacionesReportes.ImprimirAut, name='Imprimir_Aut'),

    # Cartera - Glosas

    path('load_dataGlosas/<str:data>', viewsCartera.load_dataGlosas, name='loaddataGlosas'),
    path('guardaGlosas/', viewsCartera.GuardaGlosas, name='GuardaGlosas'),

    path('consultaGlosasDetalle/', viewsCartera.ConsultaGlosasDetalle, name='consulta_GlosasDetalle'),
    path('guardarGlosasDetalleRips/', viewsCartera.GuardarGlosasDetalleRips,name='guardarGlosasDetalle_Rips'),
    path('guardaGlosasEstados/', viewsCartera.GuardaGlosasEstados,name='guardaGlosasEstados'),
    path('load_tablaGlosasDetalle/<str:data>', viewsCartera.Load_tablaGlosasDetalle,name='load_tablaGlosasDetalle'),
    path('load_dataCaja/<str:data>', viewsCartera.Load_dataCaja,name='load_data-Caja'),

    path('editarCaja/', viewsCartera.EditarCaja, name='Editar_Caja'),
    path('guardarCaja/', viewsCartera.GuardarCaja, name='Guardar_Caja'),
    path('load_dataGlosasAdicionar/<str:data>', viewsCartera.load_dataGlosasAdicionar, name='loaddataGlosas_Adicionar'),
    path('guardaGlosasAdicionar/', viewsCartera.GuardaGlosasAdicionar, name='GuardaGlosasAdicionar'),
    path('load_tablaGlosasTotalesDetalle/<str:data>', viewsCartera.Load_tablaGlosasTotalesDetalle,name='load_tablaGlosasTotales_Detalle'),
    path('borraGlosasDetalle/', viewsCartera.BorraGlosasDetalle, name='BorraGlosas_Detalle'),
    path('load_dataNotasCredito/<str:data>', viewsCartera.load_dataNotasCredito, name='loaddata_NotasCredito'),
    path('load_dataNotasCreditoDetalle/<str:data>', viewsCartera.load_dataNotasCreditoDetalle, name='loaddata_NotasCreditoDetalle'),
    path('guardaNotasCredito/', viewsCartera.GuardaNotasCredito, name='guardaNotas_Credito'),
    path('guardaNotasCreditoDetalle/', viewsCartera.GuardaNotasCreditoDetalle, name='guardaNotas_CreditoDetalle'),
    path('load_dataNotasCreditoDetalleRips/<str:data>', viewsCartera.load_dataNotasCreditoDetalleRips, name='loaddata_NotasCreditoDetalleRips'),
    path('guardarNotasCreditoDetalleRips/', viewsCartera.GuardarNotasCreditoDetalleRips, name='guardarNotas_CreditoDetalleRips'),
    path('consultaNotasCreditoDetalleRips/', viewsCartera.ConsultaNotasCreditoDetalleRips, name='consultaNotas_CreditoDetalleRips'),
    path('borraNotasCreditoDetalleRips/', viewsCartera.BorraNotasCreditoDetalleRips, name='BorraNotasCredito_DetalleRips'),
    path('consultaGlosasDetalleRips/', viewsCartera.ConsultaGlosasDetalleRips, name='consulta_GlosasDetalleRi´ps'),
    path('load_tablaGlosasDetalleRips/<str:data>', viewsCartera.Load_tablaGlosasDetalleRips, name='Load_tablaGlosasDetalle_Rips'),

    path('load_dataCartera/<str:data>', viewsCartera.Load_dataCartera, name='loaddata_Cartera'),
    path('load_dataPagosEmpresas/<str:data>', viewsCartera.Load_dataPagosEmpresas,name='load_data_PagosEmpresas'),

    path('guardarPagosEmpresas/', viewsCartera.GuardarPagosEmpresas, name='guardarPagos_Empresas'),
    path('guardarPagosEmpresasDetalle/', viewsCartera.GuardarPagosEmpresasDetalle, name='guardarPagos_EmpresasDetalle'),
    path('load_dataPagosEmpresasDetalle/<str:data>', viewsCartera.Load_dataPagosEmpresasDetalle, name='load_data_PagosEmpresasDetalle'),
    path('load_dataCarteraDetalle/<str:data>', viewsCartera.Load_dataCarteraDetalle, name='loaddata_CarteraDetalle'),
    path('load_dataEmpresas/<str:data>', viewsCartera.Load_dataEmpresas, name='loaddata_Empresas'),

    # Tarifas
	
    path('load_dataTarifariosProcedimientos/<str:data>', viewsTarifarios.Load_dataTarifariosProcedimientos, name='Load_dataTarifariosProcedimientos'),
    path('load_datatarifariosDescripcionProcedimientos/<str:data>', viewsTarifarios.Load_datatarifariosDescripcionProcedimientos, name='Load_data_tarifariosDescripcionProcedimientos'),
    path('guardarDescripcionProcedimientos/', viewsTarifarios.GuardarDescripcionProcedimientos, name='GuardarDescripcionProcedimientos'),
    path('crearTarifarioProcedimientos/', viewsTarifarios.CrearTarifarioProcedimientos,name='CrearTarifario_Procedimientos'),
    path('crearItemTarifario/', viewsTarifarios.CrearItemTarifario, name='crearItem_Tarifario'),
    path('aplicarTarifas/', viewsTarifarios.AplicarTarifas, name='Aplicar_Tarifas'),
    path('guardarEditarTarifarioProcedimientos/', viewsTarifarios.GuardarEditarTarifarioProcedimientos, name='guardarEditarTarifarioProcedimientos'),
    path('traerTarifarioProcedimientos/', viewsTarifarios.TraerTarifarioProcedimientos,name='traerTarifarioProcedimientos'),

    path('load_dataTarifariosSuministros/<str:data>', viewsTarifarios.Load_dataTarifariosSuministros,     name='Load_dataTarifariosSuministros'),
    path('load_datatarifariosDescripcionSuministros/<str:data>',   viewsTarifarios.Load_datatarifariosDescripcionSuministros,   name='Load_data_tarifariosDescripcionSuministros'),
    path('guardarDescripcionSuministros/', viewsTarifarios.GuardarDescripcionSuministros,  name='GuardarDescripcionSuministros'),

    path('crearTarifarioSuministros/', viewsTarifarios.CrearTarifarioSuministros,  name='CrearTarifario_Suministros'),
    path('crearItemTarifarioSuministros/', viewsTarifarios.CrearItemTarifarioSuministros, name='crearItem_Tarifario_Suministros'),
    path('aplicarTarifasSuministros/', viewsTarifarios.AplicarTarifasSuministros, name='Aplicar_TarifasSuministros'),
    path('guardarEditarTarifarioSuministros/', viewsTarifarios.GuardarEditarTarifarioSuministros, name='guardarEditarTarifarioSuministros'),
    path('traerTarifarioSuministros/', viewsTarifarios.TraerTarifarioSuministros,  name='traerTarifarioSuministros'),


    # Contratacion

    path('load_dataConvenios/<str:data>', viewsConvenios.load_dataConvenios, name='loaddataConvenios'),
    path('traerConvenio/', viewsConvenios.TraerConvenio, name='traer_Convenio'),
    path('editarGuardarConvenios/', viewsConvenios.EditarGuardarConvenios, name='editarGuardarConvenios'),
    path('crearGuardarConvenios/', viewsConvenios.CrearGuardarConvenios, name='CrearGuardar_Convenios'),



    path('load_dataConveniosProcedimientos/<str:data>', viewsConvenios.load_dataConveniosProcedimientos, name='loaddataConveniosProcedimientos'),
    path('postConsultaConvenios/', viewsConvenios.PostConsultaConvenios , name='Post_editConvenios'),
    path('guardarConveniosProcedimientos/', viewsConvenios.GuardarConveniosProcedimientos, name='guardarConveniosProcedimientos'),
    path('guardarConvenio/', viewsConvenios.GuardarConvenio , name='guadarConvenio'),
    path('guardarConvenio1/', viewsConvenios.GuardarConvenio1, name='guadarConvenio1'),
    path('grabarTarifa/', viewsConvenios.GrabarTarifa, name='grabarTarifa'),
    path('deleteConveniosProcedimientos/', viewsConvenios.DeleteConveniosProcedimientos, name='deleteConveniosProcedimientos'),

    path('load_dataConveniosSuministros/<str:data>', viewsConvenios.load_dataConveniosSuministros, name='loaddataConveniosSuministros'),
    path('grabarSuministro/', viewsConvenios.GrabarSuministro, name='grabarSuministro'),
    path('deleteConveniosSuministros/', viewsConvenios.DeleteConveniosSuministros, name='deleteConveniosSuministros'),
    path('guardarConveniosSuministros/', viewsConvenios.GuardarConveniosSuministros, name='guardarConveniosSuministros'),

    path('load_dataConveniosHonorarios/<str:data>', viewsConvenios.load_dataConveniosHonorarios, name='loaddataConveniosHonorarios'),
    path('grabarHonorarios/', viewsConvenios.GrabarHonorarios, name='grabarHonorarios'),
    path('deleteConveniosHonorarios/', viewsConvenios.DeleteConveniosHonorarios, name='deleteConveniosHonorarios'),
    path('guardarConveniosHonorarios/', viewsConvenios.GuardarConveniosHonorarios, name='guardarConveniosHonorarios'),



    path('load_dataTarifariosProcedimientos1/<str:data>', viewsConvenios.Load_dataTarifariosProcedimientos1, name='Load_dataTarifariosProcedimientos1'),
    path('load_datatarifariosDescripcionProcedimientos1/<str:data>', viewsConvenios.Load_datatarifariosDescripcionProcedimientos1, name='Load_data_tarifariosDescripcionProcedimientos1'),
    path('load_dataTarifariosSuministros1/<str:data>', viewsConvenios.Load_dataTarifariosSuministros1,     name='Load_dataTarifariosSuministros1'),
    path('load_datatarifariosDescripcionSuministros1/<str:data>',   viewsConvenios.Load_datatarifariosDescripcionSuministros1,   name='Load_data_tarifariosDescripcionSuministros1'),

    # Cirugia
    path('load_dataProgramacionCirugia/<str:data>', viewsCirugia.Load_dataProgramacionCirugia,  name='Load_dataProgramacion_cirugia'),
    path('load_dataSalasCirugia/<str:data>', viewsCirugia.Load_dataSalasCirugia, name='Load_dataSalas_Cirugia'),
    path('crearProgramacionCirugia/', viewsCirugia.CrearProgramacionCirugia, name='crearProgramacion_Cirugia'),
    path('load_dataSolicitudCirugia/<str:data>', viewsCirugia.Load_dataSolicitudCirugia, name='load_dataSolicitud_Cirugia'),
    path('load_dataIngresosCirugia/<str:data>', viewsCirugia.Load_dataIngresosCirugia,    name='load_dataIngresos_Cirugia'),
    path('load_dataDisponibilidadSalas/<str:data>', viewsCirugia.Load_dataDisponibilidadSalas, name='load_dataDisponibilidad_Salas'),
    path('crearSolicitudCirugia/', viewsCirugia.CrearSolicitudCirugia, name='CrearSolicitudCirugia'),
    path('load_dataTraerProcedimientosCirugia/<str:data>', viewsCirugia.Load_dataTraerProcedimientosCirugia, name='Load_dataTraerProcedimiento_Cirugia'),
    path('load_dataTraerParticipantesCirugia/<str:data>', viewsCirugia.Load_dataTraerParticipantesCirugia, name='Load_dataTraerParticipantes_Cirugia'),
    path('crearProcedimientosCirugia/', viewsCirugia.CrearProcedimientosCirugia, name='CrearProcedimiento_Cirugia'),
    path('crearParticipantesCirugia/', viewsCirugia.CrearParticipantesCirugia, name='CrearParticipantes_Cirugia'),
    path('crearParticipantesInformeCirugia/', viewsCirugia.CrearParticipantesInformeCirugia, name='CrearParticipantesInforme_Cirugia'),
    path('buscaProgramacionCirugia/', viewsCirugia.BuscaProgramacionCirugia, name='buscaProgramacion_Cirugia'),
    path('crearMaterialCirugia/', viewsCirugia.CrearMaterialCirugia, name='CrearMaterial_Cirugia'),
    path('load_dataMaterialCirugia/<str:data>', viewsCirugia.Load_dataMaterialCirugia,  name='Load_dataMaterial_Cirugia'),

    path('load_dataDispoSalasCirugia/<str:data>', viewsCirugia.Load_dataDispoSalasCirugia,name='load_dataDispo_SalasCirugia'),

    path('load_dataTraerProcedimientosInformeCirugia/<str:data>', viewsCirugia.Load_dataTraerProcedimientosInformeCirugia,name='Load_dataTraerProcedimientoInforme_Cirugia'),
    path('load_dataTraerParticipantesInformeCirugia/<str:data>', viewsCirugia.Load_dataTraerParticipantesInformeCirugia,name='Load_dataTraerParticipantesInforme_Cirugia'),
    path('load_dataTraerParticipantesInformeXXCirugia/<str:data>', viewsCirugia.Load_dataTraerParticipantesInformeXXCirugia,name='Load_dataTraerParticipantesInformeXX_Cirugia'),
    path('load_dataMaterialInformeCirugia/<str:data>', viewsCirugia.Load_dataMaterialInformeCirugia, name='Load_dataMaterialInforme_Cirugia'),
    path('load_dataMaterialInformeXXCirugia/<str:data>', viewsCirugia.Load_dataMaterialInformeXXCirugia, name='Load_dataMaterialInformeXX_Cirugia'),
    path('borraParticipanteInformeCirugia/', viewsCirugia.BorraParticipanteInformeCirugia, name='BorraParticipanteInforme_Cirugia'),
    path('borraProcedimientosInformeCirugia/', viewsCirugia.BorraProcedimientosInformeCirugia, name='BorraProcedimientosInforme_Cirugia'),
    path('borraMaterialInformeCirugia/', viewsCirugia.BorraMaterialInformeCirugia,name='BorraMaterialInforme_Cirugia'),
    path('borraHojaDeGastoCirugia/', viewsCirugia.BorraHojaDeGastoCirugia,name='BorraHojaDeGasto_Cirugia'),
    path('crearProcedimientosInformeCirugia/', viewsCirugia.CrearProcedimientosInformeCirugia, name='CrearProcedimientoInforme_Cirugia'),
    path('crearMaterialInformeCirugia/', viewsCirugia.CrearMaterialInformeCirugia, name='CrearMaterialInforme_Cirugia'),


    path('load_dataTraerProcedimientosInformeXXCirugia/<str:data>', viewsCirugia.Load_dataTraerProcedimientosInformeXXCirugia, name='Load_dataTraerProcedimientoInformeXX_Cirugia'),
    path('crearAdicionQx/', viewsCirugia.CrearAdicionQx, name='crearAdicion_Qx'),
    path('crearHojaDeGastoCirugia/', viewsCirugia.CrearHojaDeGastoCirugia, name='CrearHojaDeGasto_Cirugia'),
    path('load_dataHojaDeGastoCirugia/<str:data>', viewsCirugia.Load_dataHojaDeGastoCirugia, name='load_dataHojaDeGasto_Cirugia'),
    path('load_dataHojaDeGastoXXCirugia/<str:data>', viewsCirugia.Load_dataHojaDeGastoXXCirugia,name='load_dataHojaDeGastoXX_Cirugia'),
    path('buscaAdicionarQx/', viewsCirugia.BuscaAdicionarQx, name='BuscaAdicionar_Qx'),
    path('seleccionProgramacionCirugia/', viewsCirugia.SeleccionProgramacionCirugia, name='seleccionProgramacion_Cirugia'),
    path('guardarEstadoProgramacionCirugia/', viewsCirugia.GuardarEstadoProgramacionCirugia, name='GuardarEstadoProgramacion_Cirugia'),
    path('guardarEstadoCirugia/', viewsCirugia.GuardarEstadoCirugia, name='GuardarEstado_Cirugia'),
    path('generarLiquidacionCirugia/', viewsCirugia.GenerarLiquidacionCirugia, name='generarLiquidacion_Cirugia'),
    path('buscarProcedimientosDeCirugia/', viewsCirugia.BuscarProcedimientosDeCirugia, name='buscarProcedimientosDe_Cirugia'),
    path('traerInformacionDeCirugia/', viewsCirugia.TraerInformacionDeCirugia, name='traerInformacionDe_Cirugia'),
    path('traerEstadoCirugia/', viewsCirugia.TraerEstadoCirugia, name='TraerEstado_Cirugia'),
    path('traerEstadoProgramacionCirugia/', viewsCirugia.TraerEstadoProgramacionCirugia, name='TraerEstadoProgramacion_Cirugia'),
    path('buscarConveniosCirugiaPaciente/', viewsCirugia.BuscarConveniosCirugiaPaciente, name='BuscarConveniosCirugia_Paciente'),
    path('buscarProcedimientosParticipantesDeCirugia/', viewsCirugia.BuscarProcedimientosParticipantesDeCirugia, name='buscarProcedimientosParticipantesDe_Cirugia'),
    path('buscarProcedimientosMaterialesDeCirugia/', viewsCirugia.BuscarProcedimientosMaterialesDeCirugia,  name='buscarProcedimientosMaterialesDe_Cirugia'),


    # Farmacia

    path('load_dataFarmacia/<str:data>', viewsFarmacia.Load_dataFarmacia,name='load_dataFarmacia'),
    path('load_dataFarmaciaDetalle/<str:data>', viewsFarmacia.Load_dataFarmaciaDetalle,name='load_dataFarmaciaDetalle'),
    path('buscaDatosPaciente/', viewsFarmacia.BuscaDatosPaciente , name='busca_DatosPaciente'),
    path('load_dataFarmaciaDespachosDispensa/<str:data>', viewsFarmacia.Load_dataFarmaciaDespachosDispensa,name='load__dataFarmaciaDespachosDispensa'),
    path('load_dataFarmaciaDespachos/<str:data>', viewsFarmacia.Load_dataFarmaciaDespachos, name='load__dataFarmaciaDespachos'),
    path('adicionarDespachosDispensa/', viewsFarmacia.AdicionarDespachosDispensa , name='Adicionar_Despachos_Dispensa'),
    path('cambiaEstadoDespacho/', viewsFarmacia.CambiaEstadoDespacho, name='cambiaEstado_Despacho'),
    path('load_dataDespachosFarmacia/<str:data>', viewsFarmacia.Load_dataDespachosFarmacia, name='load_dataDespachos_Farmacia'),
    path('load_dataDespachosDetalleFarmacia/<str:data>', viewsFarmacia.Load_dataDespachosDetalleFarmacia,    name='load_dataDespachosDetalle_Farmacia'),
    path('load_dataDevolucionesFarmacia/<str:data>', viewsFarmacia.Load_dataDevolucionesFarmacia,  name='load_dataDevoluciones_Farmacia'),
    path('load_dataDevolucionesDetalleFarmacia/<str:data>',  viewsFarmacia.Load_dataDevolucionesDetalleFarmacia,      name='load_dataDevolucionesDetalle_Farmacia'),
    path('recibirDevolucionFarmacia/', viewsFarmacia.RecibirDevolucionFarmacia, name='RecibirDevolucion_Farmacia'),
    path('recibirDevolucionDetalleFarmacia/', viewsFarmacia.RecibirDevolucionDetalleFarmacia, name='RecibirDevolucionDetalle_Farmacia'),
    path('despachadoFarmaciaDetalle/', viewsFarmacia.DespachadoFarmaciaDetalle, name='despachado_FarmaciaDetalle'),
    path('imprimirDespachoFarmacia/', viewsFarmaciaReportes.ImprimirDespacho , name='Imprimir_despacho'),
    path('imprimirDespachoFarmacia/<str:farmaciaId>, <str:despachoId', viewsFarmaciaReportes.ImprimirDespacho , name='Imprimir_despacho'),
    path('load_dataFarmaciaDetalleOrdenados/<str:data>', viewsFarmacia.Load_dataFarmaciaDetalleOrdenados, name='load_dataFarmaciaDetalleOrdenados'),

    #Enfermeria

    path('load_dataPanelEnfermeria/<str:data>', viewsEnfermeria.Load_dataPanelEnfermeria,name='load_dataPanelEnfermeria'),
    path('load_dataPanelEnfermeria2/<str:data>', viewsEnfermeria.Load_dataPanelEnfermeria2,name='load_dataPanelEnfermeria2'),
    path('load_dataMedicamentosEnfermeria/<str:data>', viewsEnfermeria.Load_dataMedicamentosEnfermeria,    name='load_dataMedicamentosEnfermeria'),
    path('load_dataParaClinicosEnfermeria/<str:data>', viewsEnfermeria.Load_dataParaClinicosEnfermeria,  name='Load_dataParaClinicos_Enfermeria'),
    path('load_dataPedidosEnfermeria/<str:data>', viewsEnfermeria.Load_dataPedidosEnfermeria, name='load_dataPedidos_Enfermeria'),
    path('load_dataPedidosEnfermeriaDetalle/<str:data>', viewsEnfermeria.Load_dataPedidosEnfermeriaDetalle, name='load_dataPedidos_EnfermeriaDetalle'),
    path('buscaDatosPacienteEnfermeria/', viewsEnfermeria.BuscaDatosPacienteEnfermeria, name='busca_DatosPaciente_Enfermeria'),
    path('creaPedidosEnfermeriaCabezote/', viewsEnfermeria.CreaPedidosEnfermeriaCabezote,name='CreaPedidosEnfermeria_Cabezote'),
    path('adicionarFormulacionEnfermeria/', viewsEnfermeria.AdicionarFormulacionEnfermeria,    name='AdicionarFormulacion_Enfermeria'),
    path('load_dataTurnosEnfermeria/<str:data>', viewsEnfermeria.Load_dataTurnosEnfermeria,name='Load_dataTurnos_Enfermeria'),
    path('load_dataPlaneacionEnfermeria/<str:data>', viewsEnfermeria.Load_dataPlaneacionEnfermeria, name='Load_dataPlaneacion_Enfermeria'),
    path('guardaPlaneacionEnfermeria/', viewsEnfermeria.GuardaPlaneacionEnfermeria, name='GuardaPlaneacion_Enfermeria'),
    path('guardaAplicacionEnfermeria/', viewsEnfermeria.GuardaAplicacionEnfermeria, name='GuardaAplicacion_Enfermeria'),
    path('load_dataDietasEnfermeria/<str:data>', viewsEnfermeria.Load_dataDietasEnfermeria, name='Load_dataDietas_Enfermeria'),
    path('guardaDietasEnfermeria/', viewsEnfermeria.GuardaDietasEnfermeria, name='GuardaDietas_Enfermeria'),
    path('guardaNotasEnfermeria/', viewsEnfermeria.GuardaNotasEnfermeria, name='GuardaDNotas_Enfermeria'),
    path('load_dataNotasEnfermeria/<str:data>', viewsEnfermeria.Load_dataNotasEnfermeria,   name='Load_dataNotas_Enfermeria'),
    path('guardarDevolucionEnfermeria/', viewsEnfermeria.GuardarDevolucionEnfermeria, name='GuardarDevolucion_Enfermeria'),
    path('load_dataDevolucionEnfermeria/<str:data>', viewsEnfermeria.Load_dataDevolucionEnfermeria, name='load_dataDevolucionEnfermeria'),

    path('load_dataConsultaDevolucionesEnfermeria/<str:data>', viewsEnfermeria.Load_dataConsultaDevolucionesEnfermeria,      name='load_dataConsulta_DevolucionEnfermeriaa'),
    path('load_dataConsultaDevolucionesDetalleEnfermeria/<str:data>', viewsEnfermeria.Load_dataConsultaDevolucionesDetalleEnfermeria,name='load_dataConsulta_DevolucionesDetalleEnfermeria'),
    path('load_dataSignosVitalesEnfermeria/<str:data>', viewsEnfermeria.Load_dataSignosVitalesEnfermeria,  name='Load_dataSignosVitales_Enfermeria'),
    path('guardaSignosVitalEnfermeria/', viewsEnfermeria.GuardaSignosVitalEnfermeria,name='GuardaSignosVital_Enfermeria'),





    # Citas Medicas

    # Usuarios

    path('crearUsuarios/', viewsUsuarios.crearUsuarios),
    # Fin Acceso al Programa General Clinico


]


if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

# Añadir
admin.site.site_header = 'Administracion Medical Report Vulner2'
admin.site.site_title = "Portal de Medical Report Vulner2"
admin.site.index_title = "Bienvenidos al portal de administración Medical Report Vulner2"
