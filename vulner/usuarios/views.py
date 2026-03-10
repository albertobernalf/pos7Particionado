from django.shortcuts import render
from django.shortcuts import render
import MySQLdb
import pyodbc
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from .forms import crearUsuariosForm
from datetime import datetime
from usuarios.models import Usuarios
from django.db.models import Max

from sitios.models import  HistorialDependencias
import csv
from decimal import Decimal
from clinico.models import Examenes, TiposExamen, EspecialidadesMedicos, Especialidades, TiposFolio, CausasExterna, EstadoExamenes, EstadosInterconsulta,   EstadosInterconsulta, Servicios
from basicas.models import EstadoCivil, Ocupaciones, CentrosCosto, Archivos, Eventos, FuripsLista, FuripsParametro,Parametros, Periodos, TiposContacto, TiposFamilia , TiposProfesional
from autorizaciones.models import EstadosAutorizacion
from cartera.models import TiposPagos, TiposNotas, TiposGlosas, FormasPagos,EstadosGlosas, GlosasConceptoEspecifico, GlosasConceptoGeneral, MotivosGlosas
from cirugia.models import EstadosCirugias, EstadosProgramacion, EstadosSalas,FinalidadCirugia, GravedadCirugia, IntervencionCirugias, OrganosCirugias, RegionesOperatorias, TiposAnestesia, TiposCirugia, TiposHeridasOperatorias, ViasDeAcceso, ZonasCirugia
from clinico.models import CausasExterna, Eps, EstadosSalida, Enfermedades, EstadoExamenes, Ips, NivelesClinica, Regimenes, TipoDietas, EstadosInterconsulta, CodigosAtc, Diagnosticos, Especialidades, Examenes, EstadosInterconsulta
from clinico.models import ExamenesRasgos, FormasFarmaceuticas, FrecuenciasAplicacion, NivelesRegimenes, PrincipiosActivos, Recomendaciones, RevisionSistemas, TipoOxigenacion, TiposAntecedente, TiposCotizante, TiposDiagnostico, TiposExamen, TiposFolio, TiposIncapacidad, TiposInterconsulta, TiposRadiologia, TiposSalidas, TiposTriage, UnidadesDeMedidaDosis,  ViasAdministracion, ViasIngreso
from enfermeria.models import EnfermeriaTipoMovimiento, EnfermeriaTipoOrigen, EnfermeriaTipoOrigen, TiposTurnosEnfermeria
from farmacia.models import FarmaciaEstados
from planta.models import TiposPlanta

from tarifarios.models import TiposHonorarios, GruposQx, Estancias, GruposQx, MinimosLegales, TablaHonorariosIss, TablaHonorariosSoat, TablaMaterialSuturaCuracion, TablaMaterialSuturaCuracionIss, TablaSalasDeCirugia, TablaSalasDeCirugiaIss, TarifariosDescripcion, TarifariosDescripcionHonorarios, TarifariosProcedimientos, TarifariosProcedimientosHonorarios, TarifariosSuministros, TiposHonorarios, TiposTarifa, TiposTarifaProducto
from rips.models import RipsTipoOtrosServicios, RipsViasAdministracion, RipsConceptoRecaudo, RipsDestinoEgreso,RipsEstados, RipsFinalidadConsulta, RipsFormaFarmaceutica, RipsGrupoServicios,RipsModalidadAtencion, RipsMunicipios, RipsPaises, RipsServicios, RipsTipoMedicamento, RipsTipos, RipsTiposDocumento, RipsTiposNotas, RipsTiposPagoModerador, RipsTipoUsuario, RipsUmm, RipsUnidadUpr, RipsViasIngresoSalud, RipsZonaTerritorial, RipsCums, RipsMunicipios, RipsTiposDocumento, RipsCausaExterna, RipsDestinoEgreso
from facturacion.models import TiposSuministro, Conceptos, ConceptosAfacturar, RegimenesTipoPago, SalariosLegales, SalariosMinimosLegales, TiposEmpresa, Suministros, Empresas
from sitios.models import Paises, Departamentos, Municipios, SedesClinica, Ciudades, Ubicaciones, TiposSalas, Salas, Bodegas, Centros, Dependencias, DependenciasTipo, Localidades, ServiciosAdministrativos, ServiciosSedes
from usuarios.models import TiposDocumento, TiposUsuario
from seguridad.models import Modulos, ModulosElementos,Perfiles, ModulosElementosDef, PerfilesClinica, PerfilesGralUsu, PerfilesOpciones, PerfilesUsu


# Create your views here.


class crearUsuarios(TemplateView):
    print("Entre a Crear el usuario")

    template_name = 'admisiones/crearUsuario.html'


    def post(self, request, *args, **kwargs):
        print("Entre POST de Crear Admisiones")
        data = {}
        context = {}
        #sedesClinica = request.POST['sedesClinica']
        sedesClinica = request.POST['Sede']
        Sede = request.POST['Sede']
        context['Sede'] = Sede
        Perfil = request.POST['Perfil']
        context['Perfil'] = Perfil


        print("Sedes Clinica = ", sedesClinica)
        print ("Sede = ",Sede)


        Username = request.POST["Username"]
        print(" = " , Username)
        context['Username'] = Username

        Username_id = request.POST["Username_id"]
        print("Username_id = ", Username_id)
        context['Username_id'] = Username_id



        tipoDoc = request.POST['tipoDoc']
        documento = request.POST['documento']
        print("tipoDoc = ", tipoDoc)
        print("documento = ", documento)




        usuarioRegistro = Username_id

        print("usuarioRegistro =", usuarioRegistro)
        now = datetime.now()
        dnow=now.strftime("%Y-%m-%d %H:%M:%S")
        print ("NOW  = ", dnow)

        fechaRegistro = dnow
        estadoReg = "A"
        print("estadoRegistro =", estadoReg)


        # VAmos a guardar el Usuarios

        grabo = Usuarios(
                         sedesClinica_id=Sede,
                         tipoDoc_id=tipoDoc,
                         documento_id=documento,
                         consec=consec,
                         fechaIngreso=fechaIngreso,
                         fechaSalida=fechaSalida,
                         factura=factura,
                         numcita=numcita,
                         dependenciasIngreso_id=dependenciasIngreso,
                         dxIngreso_id=dxIngreso,
                         medicoIngreso_id=medicoIngreso,
                         especialidadesMedicosIngreso_id=especialidadesMedicos,
                         dependenciasActual_id=dependenciasActual,
                         dxActual_id = dxActual,
                         medicoActual_id=medicoActual,
                         especialidadesMedicosActual_id=especialidadesMedicosActual,
                         dependenciasSalida_id = dependenciasSalida,
                         dxSalida_id = dxSalida,
                         medicoSalida_id=medicoSalida,
                         especialidadesMedicosSalida_id="",
                         estadoSalida_id = estadoSalida,

                         salidaClinica = salidaClinica,
                         salidaDefinitiva=salidaDefinitiva,
                         fechaRegistro=fechaRegistro,
                         usuarioRegistro_id=usuarioRegistro,
                         estadoReg=estadoReg

        )

        grabo.save()
        print("yA grabe 2", grabo.id)
        grabo.id

        # RUTINA ARMADO CONTEXT

        ingresos = []

        miConexionx = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curx = miConexionx.cursor()


        detalle = "SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , fechaIngreso , fechaSalida, ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag  , sitios_serviciosSedes sd WHERE  sd.sedesClinica_id = i.sedesClinica_id  and   sd.servicios_id  = ser.id and   i.sedesClinica_id = dep.sedesClinica_id AND i.dependenciasActual_id = dep.id AND i.sedesClinica_id= '" + str(
            Sede) + "'  AND  deptip.id = dep.dependenciasTipo_id and dep.servicios_id = ser.id AND i.salidaDefinitiva = 'N' and tp.id = u.tipoDoc_id and u.id = i.documento_id and diag.id = i.dxactual_id"
        print(detalle)

        curx.execute(detalle)

        for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        # Combo de Servicios
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()
        comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo de SubServicios
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()
        comando = "SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed.sedesClinica_id ='" + str(
            Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id"
        curt.execute(comando)
        print(comando)

        subServicios = []
        subServicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            subServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(subServicios)

        context['SubServicios'] = subServicios

        # Fin combo SubServicios

        # Combo TiposDOc
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
        curt.execute(comando)
        print(comando)

        tiposDoc = []
        tiposDoc.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDoc.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDoc)

        context['TiposDoc'] = tiposDoc

        # Fin combo TiposDOc

        # Combo Habitaciones
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM sitios_dependencias where sedesClinica_id = '" + str(
            Sede) + "' AND dependenciasTipo_id = 2"
        curt.execute(comando)
        print(comando)

        habitaciones = []

        for id, nombre in curt.fetchall():
            habitaciones.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(habitaciones)

        context['Habitaciones'] = habitaciones

        # Fin combo Habitaciones

        # Combo Especialidades
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM clinico_Especialidades"
        curt.execute(comando)
        print(comando)

        especialidades = []
        especialidades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidades)

        context['Especialidades'] = especialidades

        # Fin combo Especialidades

        # Combo Medicos
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(
            Sede) + "' AND perf.tiposPlanta_id = 1   and p.id = perf.planta_id "

        curt.execute(comando)
        print(comando)

        medicos = []
        medicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            medicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicos)

        context['Medicos'] = medicos

        # Fin combo Medicos

        # FIN RUTINA ARMADO CONTEXT


        return render(request, "admisiones/panelHospAdmisionesBravo.html", context)


    def get_context_data(self,  **kwargs):
        print("Entre a Contexto Usuarios")


        context = super().get_context_data(**kwargs)
        print(context['Sede'])
        Sede = context['Sede']
        Documento = context['Username']
        print ("Documento = ", Documento)

        context['Documento'] = Documento
        # Consigo la sede Nombre

        miConexion = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        cur = miConexion.cursor()
        comando = "SELECT id, nombre   FROM sitios_sedesClinica WHERE id ='" + Sede + "'"
        cur.execute(comando)
        print(comando)

        nombreSedes = []

        for id, nombre in cur.fetchall():
            nombreSedes.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print(nombreSedes)

        context['NombreSede'] = nombreSedes

        print (context['NombreSede'])

        # Combo de Servicios
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()
        comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(Sede) + "' AND sed.servicios_id = ser.id"
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo Medicos
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p ,  planta_perfilesplanta perf WHERE p.sedesClinica_id = perf.sedesClinica_id and  perf.sedesClinica_id = '" + str(
            Sede) + "' AND perf.tiposPlanta_id = 1   and p.id = perf.planta_id "

        curt.execute(comando)
        print(comando)

        medicos = []
        medicos.append({'id': '', 'nombre': ''})

        #for id, nombre in curt.fetchall():
        #    medicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicos)

        context['Medicos'] = medicos

        # Fin combo Medicos

        # Combo Especialidades
        miConexiont = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM clinico_Especialidades"
        curt.execute(comando)
        print(comando)

        especialidades = []
        especialidades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidades)

        context['Especialidades'] = especialidades

        # Fin combo Especialidades

        context['title'] = 'Mi gran Template'
        context['form'] = crearUsuariosForm

        print("Se supone voya a cargar la forma de usuarios")
        print (context)
        return context

def import_datos(request):
    print("Entre importar datos")

    file_path = request.GET["file_path"]
    print("file_path", file_path)

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosAutorizacion.csv'
    print("file_path", file_path)

    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)

        for row in reader:
            try:
                print("row nombre = ", row[1])
                estadosAutorizacion = EstadosAutorizacion.objects.create(
                    nombre=row[1],
                    estadoReg=row[2],

                )
            except (valueError, IndexError) as e:

                print("Error al crear : {e}")
                return JsonResponse({'success': False, 'Mensaje': e})

    return JsonResponse({'success': True, 'Mensaje': 'Los datos se importaron correctamente ¡'})


def import_datos_global_1(request):
    print("Entre importar datos GLOBAL")

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Parametros.csv'
    print("file_path", file_path)

    parametros = Parametros.objects.count()
    print("ya conte Parametros", parametros)

    if (parametros == 0  ):
        print("ENTRE  Parametros", parametros)

        with open(file_path,  'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    parametros = Parametros.objects.create(
                        nombre=row[1],
                        parametro1=row[2],
                        # fechaRegistro=row[3],
                        estadoReg=row[4])

                except (valueError, IndexError) as e:
                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Servicios.csv'
    print("file_path", file_path)

    servicios = Servicios.objects.count()
    print("ya conte servicios", servicios)

    if (servicios == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    servicios = Servicios.objects.create(
                        nombre=row[1]
                    )
                except (valueError, IndexError) as e:
                    print("Error al crear : {e}")

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadoCivil.csv'
    print("file_path", file_path)


    estadoCivil = EstadoCivil.objects.count()

    if (estadoCivil == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadoCivil = EstadoCivil.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Ocupaciones.csv'
    print("file_path", file_path)


    ocupaciones = Ocupaciones.objects.count()

    if (ocupaciones == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    ocupaciones = Ocupaciones.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\CentrosCosto.csv'
    print("file_path", file_path)

    centrosCosto = CentrosCosto.objects.count()

    if (centrosCosto == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    centroCosto = CentrosCosto.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposProfesional.csv'
    print("file_path", file_path)

    tiposProfesional = TiposProfesional.objects.count()

    if (parametros == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposProfesional = TiposProfesional.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposContacto.csv'
    print("file_path", file_path)


    tiposContacto = TiposContacto.objects.count()

    if (tiposContacto == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposContacto = TiposContacto.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposFamilia.csv'
    print("file_path", file_path)

    tiposFamilia = TiposFamilia.objects.count()

    if (tiposFamilia == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposFamilia = TiposFamilia.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\FuripsLista.csv'
    print("file_path", file_path)

    furipsLista = FuripsLista.objects.count()

    if (furipsLista == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    furipsLista = FuripsLista.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Archivos.csv'
    print("file_path", file_path)

    archivos = Archivos.objects.count()

    if (archivos == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    archivos = Archivos.objects.create(
                        tipo=row[1],
                        nombre=row[2],
                        # fechaRegistro=row[2],
                        estadoReg=row[4]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Parametros.csv'
    print("file_path", file_path)

    parametros = Parametros.objects.count()

    if (parametros == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    parametros = Parametros.objects.create(
                        nombre=row[1],
                        parametro1=row[2],
                        # fechaRegistro=row[3],
                        estadoReg=row[4]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\CausasExterna.csv'
    print("file_path", file_path)


    causasExterna = CausasExterna.objects.count()

    if (causasExterna == 0  ):



        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    causasExterna = CausasExterna.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\RipsCausaExterna.csv'
    print("file_path", file_path)


    ripsCausaExterna = RipsCausaExterna.objects.count()

    if (ripsCausaExterna == 0  ):



        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    ripsCausaExterna = RipsCausaExterna.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\RipsDestinoEgreso.csv'
    print("file_path", file_path)


    ripsDestinoEgreso = RipsDestinoEgreso.objects.count()

    if (ripsDestinoEgreso == 0  ):



        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    ripsDestinoEgreso = RipsDestinoEgreso.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Periodos.csv'
    print("file_path", file_path)

    periodos = Periodos.objects.count()

    if (periodos == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    periodos = Periodos.objects.create(
                        nombre=row[1],
                        año=row[2],
                        mes=row[3],
                        diaInicial=row[4],
                        diaFinal=row[5],
                        # fechaRegistro=row[3],
                        estadoReg=row[7],


                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosAutorizacion.csv'
    print("file_path", file_path)

    estadosAutorizacion = EstadosAutorizacion.objects.count()

    if (estadosAutorizacion == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosAutorizacion = EstadosAutorizacion.objects.create(
                        nombre=row[1],
                        estadoReg=row[2]
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposPagos.csv'
    print("file_path", file_path)

    tiposPagos = TiposPagos.objects.count()
    if (tiposPagos == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposPagos = TiposPagos.objects.create(
                        nombre=row[1]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposNotas.csv'
    print("file_path", file_path)

    tiposNotas = TiposNotas.objects.count()

    if (tiposNotas == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposNotas = TiposNotas.objects.create(
                        codigo=row[1],
                        nombre=row[2]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposGlosas.csv'
    print("file_path", file_path)

    tiposGlosas = TiposGlosas.objects.count()

    if (tiposGlosas == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposGlosas = TiposGlosas.objects.create(
                        nombre=row[1]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\FormasPagos.csv'
    print("file_path", file_path)

    formasPagos = FormasPagos.objects.count()

    if (formasPagos == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    formasPagos = FormasPagos.objects.create(
                        nombre=row[1],
                        codigoRips=row[2]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosGlosas.csv'
    print("file_path", file_path)

    estadosGlosas = EstadosGlosas.objects.count()
    if (estadosGlosas == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosGlosas = EstadosGlosas.objects.create(
                        tipo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\GlosasConceptoGeneral.csv'
    print("file_path", file_path)

    glosasConceptoGeneral = GlosasConceptoGeneral.objects.count()

    if (glosasConceptoGeneral == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    glosasConceptoGeneral = GlosasConceptoGeneral.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})







    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosCirugias.csv'
    print("file_path", file_path)

    estadosCirugias = EstadosCirugias.objects.count()

    if (estadosCirugias == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosCirugias = EstadosCirugias.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosProgramacion.csv'
    print("file_path", file_path)

    estadosProgramacion = EstadosProgramacion.objects.count()
    if (estadosProgramacion == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosProgramacion = EstadosProgramacion.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosSalas.csv'
    print("file_path", file_path)

    estadosSalas = EstadosSalas.objects.count()

    if (estadosSalas == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosSalas = EstadosSalas.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\FinalidadCirugia.csv'
    print("file_path", file_path)
    finalidadCirugia = FinalidadCirugia.objects.count()
    if (finalidadCirugia == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    finalidadCirugia = FinalidadCirugia.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\GravedadCirugia.csv'
    print("file_path", file_path)

    gravedadCirugia = GravedadCirugia.objects.count()
    if (gravedadCirugia == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    gravedadCirugia = GravedadCirugia.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\GravedadCirugia.csv'
    print("file_path", file_path)

    with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    gravedadCirugia = GravedadCirugia.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\IntervencionCirugia.csv'
    print("file_path", file_path)

    intervencionCirugias = IntervencionCirugias.objects.count()

    if (intervencionCirugias == 0 ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    intervencionCirugias = IntervencionCirugias.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\OrganosCirugias.csv'
    print("file_path", file_path)

    organosCirugias = OrganosCirugias.objects.count()

    if (organosCirugias == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    organosCirugias = OrganosCirugias.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposAnestesia.csv'
    print("file_path", file_path)

    tiposAnestesia = TiposAnestesia.objects.count()

    if (tiposAnestesia == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposAnestesia = TiposAnestesia.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposCirugia.csv'
    print("file_path", file_path)

    tiposCirugia = TiposCirugia.objects.count()

    if (tiposCirugia == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposCirugia = TiposCirugia.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\ViasDeAcceso.csv'
    print("file_path", file_path)

    viasDeAcceso = ViasDeAcceso.objects.count()

    if (viasDeAcceso == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    ViasDeAceso = ViasDeAcceso.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\ZonasCirugia.csv'
    print("file_path", file_path)
    zonasCirugia = ZonasCirugia.objects.count()

    if (zonasCirugia == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    zonasCirugia = ZonasCirugia.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposHeridasOperatorias.csv'
    print("file_path", file_path)
    tiposHeridasOperatorias = TiposHeridasOperatorias.objects.count()

    if (tiposHeridasOperatorias == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposHeridasOperatorias = TiposHeridasOperatorias.objects.create(
                        nombre=row[1],
                        #fechaRegistro=row[2],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\RegionesOperatorias.csv'
    print("file_path", file_path)

    regionesOperatorias = RegionesOperatorias.objects.count()
    if (regionesOperatorias == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    regionesOperatorias = RegionesOperatorias.objects.create(
                        region=row[1],
                        organos=row[2],
                        #fechaRegistro=row[3],
                        estadoReg=row[4],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Eps.csv'
    print("file_path", file_path)
    eps = Eps.objects.count()
    if (eps == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    eps = Eps.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosSalida.csv'
    print("file_path", file_path)

    estadosSalida = EstadosSalida.objects.count()

    if (estadosSalida == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosSalida = EstadosSalida.objects.create(
                        nombre=row[1],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Enfermedades.csv'
    print("file_path", file_path)

    enfermedades = Enfermedades.objects.count()
    if (enfermedades == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    enfermedades = Enfermedades.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadoExamenes.csv'
    print("file_path", file_path)
    estadoExamenes = EstadoExamenes.objects.count()
    if (estadoExamenes == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosExamenes = EstadoExamenes.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Ips.csv'
    print("file_path", file_path)
    ips = Ips.objects.count()

    if (ips == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    ips = Ips.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\\NivelesClinica.csv'

    print("file_path", file_path)
    nivelesClinica = NivelesClinica.objects.count()
    if (nivelesClinica == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    nivelesClinica = NivelesClinica.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Regimenes.csv'
    print("file_path", file_path)

    regimenes = Regimenes.objects.count()

    if (regimenes == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    regimenes = Regimenes.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TipoDietas.csv'
    print("file_path", file_path)

    tipoDietas = TipoDietas.objects.count()

    if (tipoDietas == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tipoDietas = TipoDietas.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\EstadosInterconsulta.csv'
    print("file_path", file_path)

    estadosInterconsulta = EstadosInterconsulta.objects.count()

    if (estadosInterconsulta== 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    estadosInterconsulta = EstadosInterconsulta.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\CodigosAtc.csv'
    print("file_path", file_path)
    codigosAtc = CodigosAtc.objects.count()

    if (codigosAtc == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    codigosAtc = CodigosAtc.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                        estadoReg=row[4],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Diagnosticos.csv'
    print("file_path", file_path)
    diagnosticos = Diagnosticos.objects.count()
    if (diagnosticos == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    diagnosticos = Diagnosticos.objects.create(
                        cie10=row[1],
                        nombre=row[2],
                        descripcion=row[3],
                        estadoReg=row[5],
                        edadFin=row[6],
                        edadIni=row[7],
                        flagSivigila=row[8],

                        habilitadoMipres=row[9],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\RipsTipoOtrosServicios.csv'
    print("file_path", file_path)

    ripsTipoOtrosServicios = RipsTipoOtrosServicios.objects.count()
    if (ripsTipoOtrosServicios == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    ripsTipoOtrosServicios = RipsTipoOtrosServicios.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposHonorarios.csv'
    print("file_path", file_path)

    tiposHonorarios = TiposHonorarios.objects.count()

    if (tiposHonorarios == 0  ):

              with open(file_path, 'r') as f:
                    reader = csv.reader(f, delimiter=';')
                    next(reader)

                    for row in reader:
                        try:
                            print("row nombre = ", row[1])

                            tiposHonorarios = TiposHonorarios.objects.create(
                                nombre=row[1],
                                estadoReg=row[3],
                                ripsTipoOtrosServicios_id= row[4],
                            )
                        except (valueError, IndexError) as e:

                            print("Error al crear : {e}")
                            return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposSuministros.csv'
    print("file_path", file_path)

    tiposSuministro = TiposSuministro.objects.count()

    if (tiposSuministro == 0  ):

              with open(file_path, 'r') as f:
                    reader = csv.reader(f, delimiter=';')
                    next(reader)

                    for row in reader:
                        try:
                            print("row nombre = ", row[1])

                            tiposSuministro = TiposSuministro.objects.create(
                                nombre=row[1],
                                estadoReg=row[3],
                            )
                        except (valueError, IndexError) as e:

                            print("Error al crear : {e}")
                            return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\GruposQx.csv'
    print("file_path", file_path)

    gruposQx = GruposQx.objects.count()

    if (gruposQx == 0  ):

              with open(file_path, 'r') as f:
                    reader = csv.reader(f, delimiter=';')
                    next(reader)

                    for row in reader:
                        try:
                            print("row nombre = ", row[1])

                            gruposQx = GruposQx.objects.create(
                                nombre=row[1],
                                estadoReg=row[3],
                                )
                        except (valueError, IndexError) as e:

                            print("Error al crear : {e}")
                            return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposExamen.csv'
    print("file_path", file_path)

    tiposExamen = TiposExamen.objects.count()

    if (tiposExamen == 0  ):

              with open(file_path, 'r') as f:
                    reader = csv.reader(f, delimiter=';')
                    next(reader)

                    for row in reader:
                        try:
                            print("row nombre = ", row[1])

                            tiposExamen = TiposExamen.objects.create(
                                nombre=row[1],
                                estadoReg=row[2],
                            )
                        except (valueError, IndexError) as e:

                            print("Error al crear : {e}")
                            return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Especialidades.csv'
    print("file_path", file_path)

    especialidades = Especialidades.objects.count()

    if (especialidades == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    especialidades = Especialidades.objects.create(
                        nombre=row[1],
                        cExterna=row[2],
                        agenda=row[3],
                        interconsulta=row[4],
                        quirurgica=row[5],
                        citaDeControl=row[6],
                        estadoReg=row[7],
                        valoracionInicial = row[8],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/PrincipiosActivos.csv'
    print("file_path", file_path)

    principiosActivos = PrincipiosActivos.objects.count()

    if (principiosActivos == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    principiosActivos = PrincipiosActivos.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Recomendaciones.csv'
    print("file_path", file_path)

    recomendaciones = Recomendaciones.objects.count()

    if (recomendaciones == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    recomendaciones = Recomendaciones.objects.create(
                        nombre=row[1],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RevisionSistemas.csv'
    print("file_path", file_path)

    revisionSistemas = RevisionSistemas.objects.count()

    if (revisionSistemas == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    revisionSistemas = RevisionSistemas.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposDietas.csv'
    print("file_path", file_path)

    tipoDietas = TipoDietas.objects.count()

    if (tipoDietas == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tipoDietas = TipoDietas.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TipoOxigenacion.csv'
    print("file_path", file_path)

    tipoOxigenacion = TipoOxigenacion.objects.count()

    if (tipoOxigenacion == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tipoOxigenacion = TipoOxigenacion.objects.create(
                        nombre=row[1],
                        flujoLtsOxigeno=row[2],
                        flujoLtsAire=row[3],
                        codFacturar=row[4],
                        estadoReg=row[6],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposAntecedente.csv'
    print("file_path", file_path)

    tiposAntecedente = TiposAntecedente.objects.count()

    if (tiposAntecedente == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposAntecedente = TiposAntecedente.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposCotizante.csv'
    print("file_path", file_path)

    tiposCotizante = TiposCotizante.objects.count()

    if (tiposCotizante == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposCotizante = TiposCotizante.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposDiagnostico.csv'
    print("file_path", file_path)

    tiposDiagnostico = TiposDiagnostico.objects.count()

    if (tiposDiagnostico == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposDiagnostico = TiposDiagnostico.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposFolio.csv'
    print("file_path", file_path)

    tiposFolio = TiposFolio.objects.count()

    if (tiposFolio == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposFolio = TiposFolio.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposIncapacidad.csv'
    print("file_path", file_path)

    tiposIncapacidad = TiposIncapacidad.objects.count()

    if (tiposIncapacidad == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposIncapacidad = TiposIncapacidad.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposInterconsulta.csv'
    print("file_path", file_path)

    tiposInterConsulta = TiposInterconsulta.objects.count()

    if (tiposInterConsulta == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposInterConsulta = TiposInterconsulta.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposRadiologia.csv'
    print("file_path", file_path)

    tiposRadiologia = TiposRadiologia.objects.count()

    if (tiposRadiologia == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposRadiologia = TiposRadiologia.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposSalidas.csv'
    print("file_path", file_path)

    tiposSalidas = TiposSalidas.objects.count()

    if (tiposSalidas == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposSalidas = TiposSalidas.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposTriage.csv'
    print("file_path", file_path)

    tiposTriage = TiposTriage.objects.count()

    if (tiposTriage == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposTriage = TiposTriage.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/UnidadesDeMedidaDosis.csv'
    print("file_path", file_path)

    unidadesDeMedidaDosis = UnidadesDeMedidaDosis.objects.count()

    if (unidadesDeMedidaDosis == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    unidadesDeMedidaDosis = UnidadesDeMedidaDosis.objects.create(
                        unidadaDeMedidaPrincipioA=row[1],
                        descripcion=row[2],
                        estadoReg=row[4],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/ViasIngreso.csv'
    print("file_path", file_path)

    viasIngreso = ViasIngreso.objects.count()

    if (viasIngreso == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    viasIngreso = ViasIngreso.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/EnfermeriaTipoMovimiento.csv'
    print("file_path", file_path)

    enfermeriaTipoMovimiento = EnfermeriaTipoMovimiento.objects.count()

    if (enfermeriaTipoMovimiento == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    enfermeriaTipoMovimiento = EnfermeriaTipoMovimiento.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/EnfermeriaTipoOrigen.csv'
    print("file_path", file_path)

    enfermeriaTipoOrigen = EnfermeriaTipoOrigen.objects.count()

    if (enfermeriaTipoOrigen == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    enfermeriaTipoOrigen = EnfermeriaTipoOrigen.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/ConceptosAFacturar.csv'
    print("file_path", file_path)

    conceptosAFacturar = ConceptosAfacturar.objects.count()

    if (conceptosAFacturar == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    conceptosAFacturar = ConceptosAfacturar.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/SalariosLegales.csv'
    print("file_path", file_path)

    salariosLegales = SalariosLegales.objects.count()

    if (salariosLegales == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    salariosLegales = SalariosLegales.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],


                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/SalariosMinimosLegales.csv'
    print("file_path", file_path)

    salariosMinimosLegales = SalariosMinimosLegales.objects.count()

    if (salariosMinimosLegales == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    salariosMinimosLegales = SalariosMinimosLegales.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                        año=row[4],
                        valor=row[5],
                        valorSubsidio=row[6],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposEmpresa.csv'
    print("file_path", file_path)

    tiposEmpresa = TiposEmpresa.objects.count()

    if (tiposEmpresa == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposEmpresa = TiposEmpresa.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/FarmaciaEstados.csv'
    print("file_path", file_path)

    farmaciaEstados = FarmaciaEstados.objects.count()

    if (farmaciaEstados == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    farmaciaEstados = FarmaciaEstados.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposPlanta.csv'
    print("file_path", file_path)

    tiposPlanta = TiposPlanta.objects.count()

    if (tiposPlanta == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposPlanta = TiposPlanta.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/PrincipiosActivos.csv'
    print("file_path", file_path)

    principiosActivos = PrincipiosActivos.objects.count()

    if (principiosActivos == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    principiosActivos = PrincipiosActivos.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposRadiologia.csv'
    print("file_path", file_path)

    tiposRadiologia = TiposRadiologia.objects.count()

    if (tiposRadiologia == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposRadiologia = tiposRadiologia.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsConceptoRecaudo.csv'
    print("file_path", file_path)

    ripsConceptoRecaudo = RipsConceptoRecaudo.objects.count()

    if (ripsConceptoRecaudo == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsConceptoRecaudo = RipsConceptoRecaudo.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsDestinoEgreso.csv'
    print("file_path", file_path)

    ripsDestinoEgreso = RipsDestinoEgreso.objects.count()

    if (ripsConceptoRecaudo == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsDestinoEgreso = RipsDestinoEgreso.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsEstados.csv'
    print("file_path", file_path)

    ripsEstados = RipsEstados.objects.count()

    if (ripsEstados == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsEstados = RipsEstados.objects.create(
                        nombre=row[1],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsFinalidadConsulta.csv'
    print("file_path", file_path)

    ripsFinalidadConsulta = RipsFinalidadConsulta.objects.count()

    if (ripsFinalidadConsulta == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsFinalidadConsulta = RipsFinalidadConsulta.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsFormaFarmaceutica.csv'
    print("file_path", file_path)

    ripsFormaFarmaceutica = RipsFormaFarmaceutica.objects.count()

    if (ripsFormaFarmaceutica == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsFormaFarmaceutica = RipsFormaFarmaceutica.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsGrupoServicios.csv'
    print("file_path", file_path)

    ripsGrupoServicios = RipsGrupoServicios.objects.count()

    if (ripsGrupoServicios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsGrupoServicios = RipsGrupoServicios.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsModalidadAtencion.csv'
    print("file_path", file_path)

    ripsModalidadAtencion = RipsModalidadAtencion.objects.count()

    if (ripsModalidadAtencion == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsModalidadAtencion = RipsModalidadAtencion.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsMunicipios.csv'
    print("file_path", file_path)

    ripsMunicipios = RipsMunicipios.objects.count()

    if (ripsMunicipios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsMunicipios = RipsMunicipios.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsPaises.csv'
    print("file_path", file_path)

    ripsPaises = RipsPaises.objects.count()

    if (ripsPaises == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsPaises = RipsPaises.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsServicios.csv'
    print("file_path", file_path)

    ripsServicios = RipsServicios.objects.count()

    if (ripsServicios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsServicios = RipsServicios.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsTipoMedicamento.csv'
    print("file_path", file_path)

    ripsTipoMedicamento = RipsTipoMedicamento.objects.count()

    if (ripsTipoMedicamento == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsTipoMedicamento = RipsTipoMedicamento.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsTipos.csv'
    print("file_path", file_path)

    ripsTipos = RipsTipos.objects.count()

    if (ripsTipos == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsTipos = RipsTipos.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsTiposDocumento.csv'
    print("file_path", file_path)

    ripsTiposDocumento = RipsTiposDocumento.objects.count()

    if (ripsTiposDocumento == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsTiposDocumento = RipsTiposDocumento.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsTiposNotas.csv'
    print("file_path", file_path)

    ripsTiposNotas = RipsTiposNotas.objects.count()

    if (ripsTiposNotas == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsTiposNotas = RipsTiposNotas.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsTiposPagosModerador.csv'
    print("file_path", file_path)

    ripsTiposPagoModerador = RipsTiposPagoModerador.objects.count()

    if (ripsTiposPagoModerador == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsTiposPagoModerador = RipsTiposPagoModerador.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                        codigoAplicativo=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsTipoUsuario.csv'
    print("file_path", file_path)

    ripsTipoUsuario = RipsTipoUsuario.objects.count()

    if (ripsTipoUsuario == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsTipoUsuario = RipsTipoUsuario.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsSumm.csv'
    print("file_path", file_path)

    ripsUmm = RipsUmm.objects.count()

    if (ripsUmm == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsUmm = RipsUmm.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                        descripcion=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsUnidadUpr.csv'
    print("file_path", file_path)

    ripsUnidadUpr = RipsUnidadUpr.objects.count()

    if (ripsUnidadUpr == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsUnidadUpr = RipsUnidadUpr.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsViasIngresoSalud.csv'
    print("file_path", file_path)

    ripsViasIngresoSalud = RipsViasIngresoSalud.objects.count()

    if (ripsViasIngresoSalud == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsViasIngresoSalud = RipsViasIngresoSalud.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsZonaTerritorial.csv'
    print("file_path", file_path)

    ripsZonaTerritorial = RipsZonaTerritorial.objects.count()

    if (ripsZonaTerritorial == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsZonaTerritorial = RipsZonaTerritorial.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsMunicipios.csv'
    print("file_path", file_path)

    ripsMunicipios = RipsMunicipios.objects.count()

    if (ripsMunicipios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsMunicipios = RipsMunicipios.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsTiposDocumento.csv'
    print("file_path", file_path)

    ripsTiposDocumento = RipsTiposDocumento.objects.count()

    if (ripsTiposDocumento == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsTiposDocumento = RipsTiposDocumento.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Paises.csv'
    print("file_path", file_path)

    paises = Paises.objects.count()

    if (paises == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    paises = Paises.objects.create(
                        nombre=row[1],
                        paisCodigoDian=row[2],
                        estadoReg=row[4],


                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Departamentos.csv'
    print("file_path", file_path)

    departamentos = Departamentos.objects.count()

    if (departamentos == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    departamentos = Departamentos.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                        departamentoCodigoDian=row[4],
                        pais_id=row[5],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})




    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Municipios.csv'
    print("file_path", file_path)

    municipios = Municipios.objects.count()

    if (municipios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    municipios = Municipios.objects.create(
                        nombre=row[1],
                        municipioCodigoDian=row[2],
                        estadoReg=row[4],
                        departamento_id=row[5],
                        ripsMunicipios_id=row[6],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Ciudades.csv'
    print("file_path", file_path)

    ciudades = Ciudades.objects.count()

    if (ciudades == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ciudades = Ciudades.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                        departamentos_id=row[4],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Modulos.csv'
    print("file_path", file_path)

    modulos = Modulos.objects.count()

    if (modulos == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    modulos = Modulos.objects.create(
                        nombre=row[1],
                        nomenclatura=row[2],
                        logo=row[3],
                        estadoReg=row[4],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/ModulosElementos.csv'
    print("file_path", file_path)

    modulosElementos = ModulosElementos.objects.count()

    if (modulosElementos == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    modulosElementos = ModulosElementos.objects.create(
                        nombre=row[1],
                        estadoReg=row[2]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Perfiles.csv'
    print("file_path", file_path)

    perfiles = Perfiles.objects.count()

    if (perfiles == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    perfiles = Perfiles.objects.create(
                        nombre=row[1],
                        estadoReg=row[2]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposSalas.csv'
    print("file_path", file_path)

    tiposSalas = TiposSalas.objects.count()

    if (tiposSalas == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposSalas = TiposSalas.objects.create(
                        nombre=row[1],
                        estadoReg=row[2]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/SedesClinica.csv'
    print("file_path", file_path)

    sedesClinica = SedesClinica.objects.count()

    if (sedesClinica == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    sedesClinica = SedesClinica.objects.create(
                        nombre=row[1],
                        ubicacion=row[2],
                        direccion=row[3],
                        telefono=row[4],
                        contacto=row[5],
                        estadoReg=row[7],
                        ciudades_id=row[8],
                        departamentos_id=row[9],
                        nit=row[10],
                        codigoHabilitacion=row[11],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Ubicaciones.csv'
    print("file_path", file_path)

    ubicaciones = Ubicaciones.objects.count()

    if (ubicaciones == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ubicaciones = Ubicaciones.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                        sedesClinica_id = row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/GruposQx.csv'
    print("file_path", file_path)

    gruposQx = GruposQx.objects.count()

    if (gruposQx == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    gruposQx = GruposQx.objects.create(
                        nombre=row[1],
                        estadoReg=row[3]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/DependenciasTipo.csv'
    print("file_path", file_path)

    dependenciasTipo = DependenciasTipo.objects.count()

    if (dependenciasTipo == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    dependenciasTipo = DependenciasTipo.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposTarifaProducto.csv'
    print("file_path", file_path)

    tiposTarifaProducto = TiposTarifaProducto.objects.count()

    if (tiposTarifaProducto == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposTarifaProducto = TiposTarifaProducto.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/MinimosLegales.csv'
    print("file_path", file_path)

    minimosLegales = MinimosLegales.objects.count()

    if (minimosLegales == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    minimosLegales = MinimosLegales.objects.create(
                        nombre=row[1],
                        año=row[2],
                        valor=row[3],
                        estadoReg=row[5],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TarifariosDescripcionHonorarios.csv'
    print("file_path", file_path)

    tarifariosDescripcionHonorarios = TarifariosDescripcionHonorarios.objects.count()

    if (tarifariosDescripcionHonorarios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tarifariosDescripcionHonorarios = TarifariosDescripcionHonorarios.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposUsuario.csv'
    print("file_path", file_path)


    tiposUsuario = TiposUsuario.objects.count()

    if (tiposUsuario == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposUsuario = TiposUsuario.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\FormasFarmaceuticas.csv'
    print("file_path", file_path)


    formasFarmaceuticas = FormasFarmaceuticas.objects.count()

    if (formasFarmaceuticas == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    formasFarmaceuticas = FormasFarmaceuticas.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\FrecuenciasAplicacion.csv'
    print("file_path", file_path)


    frecuenciasAplicacion = FrecuenciasAplicacion.objects.count()

    if (frecuenciasAplicacion == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    frecuenciasAplicacion = FrecuenciasAplicacion.objects.create(
                        descripcion=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[3],
                        numeroHoras=row[4],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\TiposTurnosEnfermeria.csv'
    print("file_path", file_path)


    tiposTurnosEnfermeria = TiposTurnosEnfermeria.objects.count()

    if (tiposTurnosEnfermeria == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    tiposTurnosEnfermeria = TiposTurnosEnfermeria.objects.create(
                        nombre=row[1],
                        horario=row[2],
                        estadoReg=row[4],
                        sedesClinica_id=row[5],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})





    return JsonResponse({'success': True, 'Mensaje': 'Los datos se importaron correctamente ¡'})



def import_datos_global_2(request):
    print("Entre importar datos GLOBAL2")

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\FuripsParametro.csv'
    print("file_path", file_path)

    furipsParametro = FuripsParametro.objects.count()

    if (furipsParametro == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    furipsParametro = FuripsParametro.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[2],
                        estadoReg=row[2],
                        furipsLista_id=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\GlosasConceptoEspecifico.csv'
    print("file_path", file_path)

    glosasConceptoEspecifico = GlosasConceptoEspecifico.objects.count()

    if (glosasConceptoEspecifico == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    glosasConceptoEspecifico = GlosasConceptoEspecifico.objects.create(
                        codigo=row[1],
                        nombre=row[2],
                        conceptoGeneral_id=row[3],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Eventos.csv'
    print("file_path", file_path)

    eventos = Eventos.objects.count()

    if (eventos == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    eventos = Eventos.objects.create(
                        nombre=row[1],
                        # fechaRegistro=row[3],
                        estadoReg=row[3],
                        causasExterna_id = row[4]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\MotivosGlosas.csv'
    print("file_path", file_path)

    motivosGlosas = MotivosGlosas.objects.count()

    if (motivosGlosas == 0  ):


        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    motivosGlosas = MotivosGlosas.objects.create(
                        nombre=row[1],
                        descripcion=row[2],
                        conceptoDeAplicacion=row[3],
                        conceptoGlosa=row[4],
                        conceptoEspecifico_id=row[5],
                        conceptoGeneral_id=row[6],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Conceptos.csv'
    print("file_path", file_path)

    conceptos = Conceptos.objects.count()

    if (conceptos == 0  ):

              with open(file_path, 'r') as f:
                    reader = csv.reader(f, delimiter=';')
                    next(reader)

                    for row in reader:
                        try:
                            print("row nombre = ", row[1])

                            conceptos = Conceptos.objects.create(
                                nombre=row[1],
                                estadoReg=row[3],
                                tipoCups_id=row[4],
                                tiposSuministro_id=row[5],

                            )
                        except (valueError, IndexError) as e:

                            print("Error al crear : {e}")
                            return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial\Examenes_20260126_2.csv'
    print("file_path", file_path)
    examenes= Examenes.objects.count()

    if (examenes == 0  ):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])
                    #if (row[1] != 'SOMATOMEDINA C [FACTOR I DE CRECIMIENTO SIMILAR A LA INSULINA O IGF-1]' and row[1] != 'APICOGRAMA'):
                    print("Aqui voy con Examenes_2026")

                    examenes = Examenes.objects.create(
                        nombre=row[1],
                        TiposExamen_id=row[2],
                        requiereAutorizacion=row[3],
                        citaControl=row[4],
                        codigoCups=row[5],
                        codigoRips=row[6],
                        concepto_id=row[7],
                        edadFin = row[8],
                        edadIni = row[9],
                        estadoReg=row[10],
                        tipoRadiologia_id=row[11],
                        solicitaEnfermeria=row[12],
                        centroCosto=row[13],
                        cita1Vez=row[14],
                        consentimientoInformado=row[15],
                        cuentaContable=row[16],
                        cupsCategoria=row[17],
                        cupsGrupo=row[18],
                        cupsSubgrupo=row[19],
                        distribucionTerceros=row[20],
                        duracion=row[21],
                        finalidad=row[22],
                        manejaInterfaz=row[23],
                        nivelAtencion=row[24],
                        resolucion1132=row[25],
                        grupoQx_id=row[26],
                        cantidadUvr=row[27],
                        honorarios=row[28],
                        cupsSubCategoria=row[29],
                        #uvrAño=row[30],
                        tipoHonorario_id=row[30],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/NivelesRegimenes.csv'
    print("file_path", file_path)

    nivelesRegimenes = NivelesRegimenes.objects.count()

    if (nivelesRegimenes == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    nivelesRegimenes = NivelesRegimenes.objects.create(
                        porCuotaModeradora=row[1],
                        porCopago=row[2],
                        porTopeEve=row[3],
                        porTopeAnual=row[4],
                        estadoReg=row[5],
                        regimen_id=row[6],
                        nombre=row[7],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RegimenesTipoPago.csv'
    print("file_path", file_path)

    regimenesTipoPago = RegimenesTipoPago.objects.count()

    if (regimenesTipoPago == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    regimenesTipoPago = RegimenesTipoPago.objects.create(
                        año=row[1],
                        valorModeradora=row[2],
                        valorCopago=row[3],
                        valorTopeMaximoCopagoEvento=row[4],
                        valorTopeMaximoCopagoCalendario=row[5],
                        estadoReg=row[7],
                        regimen_id=row[8],
                        salarioLegal_id=row[9],
                    )

                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsViasAdministracion.csv'
    print("file_path", file_path)

    ripsViasAdministracion = RipsViasAdministracion.objects.count()

    if (ripsViasAdministracion == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsViasAdministracion = RipsViasAdministracion.objects.create(
                        codigo=row[1],
                        nombre=row[2],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/ViasAdministracion.csv'
    print("file_path", file_path)

    viasAdministracion = ViasAdministracion.objects.count()

    if (viasAdministracion == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    viasAdministracion = ViasAdministracion.objects.create(
                        codigoMipres=row[1],
                        nombre=row[2],
                        habilitadoMipres=row[3],
                        estadoReg=row[5],
                        ripsViasAdministracion_id=row[6],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsPaises.csv'
    print("file_path", file_path)

    ripsPaises = RipsPaises.objects.count()

    if (ripsPaises == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsPaises = RipsPaises.objects.create(
                        nombre=row[1],
                        paisCodigoDian=row[2],
                        estadoReg=row[4],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposDocumento.csv'
    print("file_path", file_path)

    tiposDocumento = TiposDocumento.objects.count()

    if (tiposDocumento == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposDocumento = TiposDocumento.objects.create(
                        abreviatura=row[1],
                        nombre=row[2],
                        estadoReg=row[4],
                        tiposDocCodigoDian=row[5],
                        tipoDocRips_id=row[6],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Empresas.csv'
    print("file_path", file_path)

    empresas = Empresas.objects.count()

    if (empresas == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    empresas = Empresas.objects.create(
                        documento=row[1],
                        nombre=row[2],
                        codigoEapb=row[3],
                        direccion=row[4],
                        telefono=row[5],
                        representante=row[6],
                        fosyga=row[7],
                        particular=row[8],
                        codigoPostal=row[9],
                        responsableFiscal=row[10],
                        identificadorDian=row[11],
                        estadoReg=row[13],
                        departamento_id=row[14],
                        municipio_id=row[15],
                        regimen_id=row[16],
                        tipoDoc_id=row[17],
                        tipoEmpresa_id=row[18],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/RipsCums.csv'
    print("file_path", file_path)

    ripsCums = RipsCums.objects.count()

    if (ripsCums == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ripsCums = RipsCums.objects.create(
                        nombre=row[1],
                        codigoAtc=row[2],
                        cum=row[3],
                        descripcion=row[4],
                        invima=row[5],
                        nombreAtc=row[6],
                        principiosActivos_id=row[7],
                        ripsUnidadMedida_id=row[8],
                        ripsTipoMedicamento_id=row[9],
                        ripsViasAdministracion_id=row[10],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Suministros.csv'
    print("file_path", file_path)

    suministros = Suministros.objects.count()

    if (suministros == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    suministros = Suministros.objects.create(
                        nombre=row[1],
                        nombreGenerico=row[2],
                        fraccion=row[3],
                        unidadFraccion=row[4],
                        vence=row[5],
                        control=row[6],
                        antibiotico=row[7],
                        pos=row[8],
                        facturable=row[9],
                        stockMinimo=row[10],
                        stockMaximo=row[11],
                        maxOrdenar=row[12],
                        estabilidad=row[13],
                        invFarmacia=row[14],
                        invAlmacen=row[15],
                        enfermeria=row[16],
                        terapia=row[17],
                        nutricion=row[18],
                        cantidad=row[19],
                        cums=row[20],
                        regSanitario=row[21],
                        altoCosto=row[22],
                        vrCompra=row[23],
                        vrUltimaCompra=row[24],
                        codigoAtc=row[25],
                        infusion=row[26],
                        tipoAdministracion=row[27],
                        regulado=row[28],
                        vaorRegulado=row[29],
                        observaciones=row[30],
                        sispro=row[31],
                        oncologico=row[32],
                        ortesis=row[33],
                        epiHigiene=row[34],
                        controlStock=row[35],
                        AnatoPos=row[36],
                        magistralControl=row[37],
                        genericoPos=row[38],
                        estadoReg=row[40],
                        concentracion_id=row[41],
                        concepto_id=row[42],
                        grupo_id=row[43],
                        subGrupo_id=row[44],
                        tipoSuministro_id=row[45],
                        unidadMedida_id=row[46],
                        viaAdministracion_id=row[47],
                        principioActivo_id=row[48],
                        descripcionComercial=row[49],
                        fechaExpedicion=row[50],
                        fechaVencimiento=row[51],
                        registroSanitario=row[52],
                        ripsCums_id=row[53],
                        ripsDci_id=row[54],
                        ripsFormaFarmaceutica_id=row[55],
                        ripsTipoMedicamento_id=row[56],
                        ripsUnidadDispensa_id=row[57],
                        ripsUnidadMedida_id=row[58],
                        tipoHonorario_id=row[59],
                        cantidadUvr=row[60],
                        ripsUnidadUpr_id=row[61],
                        requiereAutorizacion=row[62],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/ModulosElementosDef.csv'
    print("file_path", file_path)

    modulosElementosDef = ModulosElementosDef.objects.count()

    if (modulosElementosDef == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    modulosElementosDef = ModulosElementosDef.objects.create(
                        nombre=row[1],
                        descripcion=row[2],
                        url=row[3],
                        estadoReg=row[4],
                        modulosElementosId_id=row[5],
                        modulosId_id=row[6],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    #file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/PerfilesClinica.csv'
    #print("file_path", file_path)

    #perfilesClinica = PerfilesClinica.objects.count()

    #if (perfilesClinica == 0):

            #    with open(file_path, 'r') as f:
            #reader = csv.reader(f, delimiter=';')
            #next(reader)

            #for row in reader:
                    #    try:
                    #print("row nombre = ", row[1])

                    #        perfilesClinica = PerfilesClinica.objects.create(
                    #   nombre=row[1],
                    #    estadoReg=row[2],
                    #   modulosId_id=row[3],
                    #   sedesClinica_id=row[4],

                    #)
                    #except (valueError, IndexError) as e:

                    #print("Error al crear : {e}")
                    #return JsonResponse({'success': False, 'Mensaje': e})


    #file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/PerfilesGralUsu.csv'
    #print("file_path", file_path)

    #perfilesGralUsu = PerfilesGralUsu.objects.count()

    #if (perfilesGralUsu == 0):

            #with open(file_path, 'r') as f:
            #reader = csv.reader(f, delimiter=';')
            #next(reader)

            #for row in reader:
                #try:
                    #print("row nombre = ", row[1])

                    #perfilesGralUsu = PerfilesGralUsu.objects.create(

                        #estadoReg=row[1],
                        #perfilesClinicaId_id=row[2],
                        #plantaId_id=row[3],

                    #)
                    #except (valueError, IndexError) as e:

                    #print("Error al crear : {e}")
                    #return JsonResponse({'success': False, 'Mensaje': e})


    #file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/PerfilesOpciones.csv'
    #print("file_path", file_path)

    #perfilesOpciones = PerfilesOpciones.objects.count()

    #if (perfilesOpciones == 0):

        #with open(file_path, 'r') as f:
            #reader = csv.reader(f, delimiter=';')
            #next(reader)

            #for row in reader:
                #try:
                    #print("row nombre = ", row[1])

                    #perfilesOpciones = PerfilesOpciones.objects.create(

                        #estadoReg=row[1],
                        #modulosElementosDefId_id=row[2],
                        #perfilesId_id=row[3],

                    #)
                #except (valueError, IndexError) as e:

                    #print("Error al crear : {e}")
                    #return JsonResponse({'success': False, 'Mensaje': e})


    #file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/PerfilesUsu.csv'
    #print("file_path", file_path)

    #perfilesUsu = PerfilesUsu.objects.count()

    #if (perfilesUsu == 0):

        #with open(file_path, 'r') as f:
            #reader = csv.reader(f, delimiter=';')
            #next(reader)

            #for row in reader:
                #try:
                    #print("row nombre = ", row[1])

                    #perfilesUsu = PerfilesUsu.objects.create(
                    #    adicion=row[1],
                    ##    estadoReg=row[2],
                    #   perfilesClinicaOpcionesId_id=row[3],
                    #   plantaId_id=row[4],
                    #)
                #except (valueError, IndexError) as e:

                    #print("Error al crear : {e}")
                    #return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Ubicaciones.csv'
    print("file_path", file_path)

    ubicaciones = Ubicaciones.objects.count()

    if (ubicaciones == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    ubicaciones = Ubicaciones.objects.create(
                        nombre=row[1],
                        estadoReg=row[2],
                        sedesClinica_id = row[3]

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Localidades.csv'
    print("file_path", file_path)

    localidades = Localidades.objects.count()

    if (localidades == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    localidades = Localidades.objects.create(
                        nombre=row[1],
                        localidadCodigoDian=row[2],
                        estadoReg=row[4],
                        municipio_id = row[5],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Centros.csv'
    print("file_path", file_path)

    centros = Centros.objects.count()

    if (centros == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    centros = Centros.objects.create(
                        nombre=row[1],
                        ubicacion=row[2],
                        direccion=row[3],
                        telefono = row[4],
                        contacto=row[5],
                        estadoReg=row[7],
                        ciudades_id=row[8],
                        departamentos_id=row[9],



                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/ServiciosAdministrativos.csv'
    print("file_path", file_path)

    serviciosAdministrativos = ServiciosAdministrativos.objects.count()

    if (serviciosAdministrativos == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    serviciosAdministrativos = ServiciosAdministrativos.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                        dependenciaTipo_id=row[4],
                        sedesClinica_id=row[5],
                        ubicaciones_id=row[6],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Salas.csv'
    print("file_path", file_path)

    salas = Salas.objects.count()

    if (salas == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    salas = Salas.objects.create(
                        numero=row[1],
                        nombre=row[2],
                        estadoReg=row[4],
                        dependenciaTipo_id=row[5],
                        sedesClinica_id=row[6],
                        serviciosAdministrativos_id=row[7],
                        estadoSala_id=row[8],
                        tipoSala_id=row[9],
                        finServicio=row[10],
                        iniciaServicio=row[11],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposTarifa.csv'
    print("file_path", file_path)

    tiposTarifa = TiposTarifa.objects.count()

    if (tiposTarifa == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposTarifa = TiposTarifa.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                        tiposTarifaProducto_id=row[4],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})



    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TiposHonorarios.csv'
    print("file_path", file_path)

    tiposHonorarios = TiposHonorarios.objects.count()

    if (tiposHonorarios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tiposHonorarios = TiposHonorarios.objects.create(
                        nombre=row[1],
                        estadoReg=row[3],
                        ripsTipoOtrosServicios_id=row[4],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    #file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/ServiciosSedes.csv'
    #print("file_path", file_path)

    #serviciosSedes = ServiciosSedes.objects.count()

    #if (serviciosSedes == 0):

    #    with open(file_path, 'r') as f:
    #        reader = csv.reader(f, delimiter=';')
    #        next(reader)

    #        for row in reader:
    #            try:
    #                print("row nombre = ", row[1])

    #                serviciosSedes = ServiciosSedes.objects.create(
    #                    nombre=row[1],
    #                    descripcion=row[2],
    #                    estadoReg=row[3],
    #                    sedesClinica_id=row[4],
    #                    servicios_id=row[5],
    #                )
    #            except (valueError, IndexError) as e:

    #                print("Error al crear : {e}")
    #                return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TarifariosDescripcion.csv'
    print("file_path", file_path)

    tarifariosDescripcion = TarifariosDescripcion.objects.count()

    if (tarifariosDescripcion == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tarifariosDescripcion = TarifariosDescripcion.objects.create(
                        columna=row[1],
                        descripcion=row[2],
                        estadoReg=row[4],
                        tiposTarifa_id=row[5],
                        serviciosAdministrativos_id=row[6],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/Estancias.csv'
    print("file_path", file_path)

    estancias = Estancias.objects.count()

    if (estancias == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    estancias = Estancias.objects.create(
                        referencia=row[1],
                        codigo=row[2],
                        descripcion=row[3],
                        tipoEstancia=row[4],
                        valor=row[5],
                        estadoReg=row[7],
                        cups_id=row[8],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    #file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TarifariosProcedimientos.csv'
    #print("file_path", file_path)

    #tarifariosProcedimientos = TarifariosProcedimientos.objects.count()

    #if (tarifariosProcedimientos == 0):

    #   with open(file_path, 'r') as f:
    #       reader = csv.reader(f, delimiter=';')
    #       next(reader)

    #       for row in reader:
    #           try:
    #               print("row nombre = ", row[1])

    #               tarifariosProcedimientos = TarifariosProcedimientos.objects.create(
    #                   codigoHomologado=row[1],
    #                   colValorBase=row[2],
    #                   colValor1=row[3],
    #                   colValor2=row[4],
    #                   colValor3=row[5],
    #                   colValor4=row[6],
    #                   colValor5=row[7],
    #                   colValor6=row[8],
    #                   colValor7=row[9],
    #                   colValor8=row[10],
    #                   colValor9=row[11],
    #                   colValor10=row[12],
    #                   estadoReg=row[14],
    #                   codigoCups_id=row[15],
    #                   concepto_id=row[16],
    #                   tiposTarifa_id=row[17],
    #                   serviciosAdministrativos_id=row[19],

    #               )
    #           except (valueError, IndexError) as e:

    #               print("Error al crear : {e}")
    #               return JsonResponse({'success': False, 'Mensaje': e})

    #file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TarifariosSSuministros.csv'
    #print("file_path", file_path)

    #tarifariosSSuministros = TarifariosSSuministros.objects.count()

    #if (tarifariosSSuministros == 0):

    #   with open(file_path, 'r') as f:
    #        reader = csv.reader(f, delimiter=';')
    #            next(reader)

    #        for row in reader:
                    #            try:
                    #                    print("row nombre = ", row[1])

                    #tarifariosSSuministros = TarifariosSSuministros.objects.create(
                    #    codigoHomologado=row[1],
                    #   colValorBase=row[2],
                    #   colValor1=row[3],
                    #   colValor2=row[4],
                    #   colValor3=row[5],
                    #   colValor4=row[6],
                    #   colValor5=row[7],
                    #   colValor6=row[8],
                    #   colValor7=row[9],
                    #   colValor8=row[10],
                    #   colValor9=row[11],
                    #   colValor10=row[12],
                    #   estadoReg=row[14],
                    #   codigoCum_id=row[15],
                    #   concepto_id=row[16],
                    #   tiposTarifa_id=row[17],
                    #   serviciosAdministrativos_id=row[19],

                    #)
                    #except (valueError, IndexError) as e:

                    #print("Error al crear : {e}")
                    #return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TablaHonorariosIss.csv'
    print("file_path", file_path)

    tablaHonorariosIss = TablaHonorariosIss.objects.count()

    if (tablaHonorariosIss == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tablaHonorariosIss = TablaHonorariosIss.objects.create(
                        homologado=row[1],
                        valorUvr=row[2],
                        estadoReg=row[4],
                        tiposHonorarios_id=row[5],
                        tiposTarifaProducto_id=row[6],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TablaHonorariosSoat.csv'
    print("file_path", file_path)

    tablaHonorariosSoat = TablaHonorariosSoat.objects.count()

    if (tablaHonorariosSoat == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tablaHonorariosSoat = TablaHonorariosSoat.objects.create(
                        homologado=row[1],
                        smldv=row[2],
                        estadoReg=row[4],
                        grupoQx_id=row[5],
                        tiposHonorarios_id=row[6],
                        tiposTarifaProducto_id=row[7],
                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TablaMaterialSuturaCuracion.csv'
    print("file_path", file_path)

    tablaMaterialSuturaCuracion = TablaMaterialSuturaCuracion.objects.count()

    if (tablaMaterialSuturaCuracion == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tablaMaterialSuturaCuracion = TablaMaterialSuturaCuracion.objects.create(
                        homologado=row[1],
                        smldv=row[2],
                        cruento=row[3],
                        estadoReg=row[5],
                        grupoQx_id=row[6],
                        tiposTarifaProducto_id=row[7],
                        minimosLegales_id=row[9],
                        tipoHonorario_id=row[10],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TablaMaterialSuturaCuracionIss.csv'
    print("file_path", file_path)

    tablaMaterialSuturaCuracionIss = TablaMaterialSuturaCuracionIss.objects.count()

    if (tablaMaterialSuturaCuracionIss == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tablaMaterialSuturaCuracionIss = TablaMaterialSuturaCuracionIss.objects.create(
                        homologado=row[1],
                        desdeUvr=row[2],
                        hastaUvr=row[3],
                        valor=row[4],
                        estadoReg=row[6],
                        tiposSala_id=row[7],
                        tiposTarifaProducto_id=row[8],
                        tipoHonorario_id=row[10],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TablaSalasDeCirugia.csv'
    print("file_path", file_path)

    tablaSalasDeCirugia = TablaSalasDeCirugia.objects.count()

    if (tablaSalasDeCirugia == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tablaSalasDeCirugia = TablaSalasDeCirugia.objects.create(
                        homologado=row[1],
                        smldv=row[2],
                        cruento=row[3],
                        estadoReg=row[5],
                        grupoQx_id=row[6],
                        tiposTarifaProducto_id=row[7],
                        tipoHonorario_id=row[9],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})


    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TablaSalasDeCirugiaIss.csv'
    print("file_path", file_path)

    tablaSalasDeCirugiaIss = TablaSalasDeCirugiaIss.objects.count()

    if (tablaSalasDeCirugiaIss == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tablaSalasDeCirugiaIss = TablaSalasDeCirugiaIss.objects.create(
                        homologado=row[1],
                        desdeUvr=row[2],
                        hastaUvr=row[3],
                        valor=row[4],
                        estadoReg=row[6],
                        tiposTarifaProducto_id=row[7],
                        tiposSala_id=row[9],
                        tipoHonorario_id=row[10],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})

    file_path = 'C:\EntornosPython\pos7ParticionadoLienzo/vulner\CargueInicial/TarifariosProcedimientosHonorarios.csv'
    print("file_path", file_path)

    tarifariosProcedimientosHonorarios = TarifariosProcedimientosHonorarios.objects.count()

    if (tarifariosProcedimientosHonorarios == 0):

        with open(file_path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            for row in reader:
                try:
                    print("row nombre = ", row[1])

                    tarifariosProcedimientosHonorarios = TarifariosProcedimientosHonorarios.objects.create(
                        codigoHomologado=row[1],
                        valorHonorarioAnestesiologo=row[2],
                        valorHonorarioCirujano=row[3],
                        valorHonorarioDobleVia=row[4],
                        valorHonorarioPerfucionista=row[5],
                        valorHonorarioUnicaVia=row[6],
                        valorHonorarioViaAcceso=row[7],
                        valorHonorarioAyudante=row[8],
                        estadoReg=row[10],
                        codigoCups_id=row[11],
                        concepto_id=row[12],
                        tiposTarifa_id=row[13],
                        serviciosAdministrativos_id=row[15],

                    )
                except (valueError, IndexError) as e:

                    print("Error al crear : {e}")
                    return JsonResponse({'success': False, 'Mensaje': e})




    return JsonResponse({'success': True, 'Mensaje': 'Los datos se importaron correctamente ¡'})