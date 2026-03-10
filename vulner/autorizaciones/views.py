from django.shortcuts import render
import json
from django import forms
import cv2
import numpy as np
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.utils.timezone import now
from django.db.models import Avg, Max, Min, Sum

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.http import JsonResponse
#import MySQLdb
import pyodbc
import psycopg2
import json
import datetime
from decimal import Decimal
from admisiones.models import Ingresos
from autorizaciones.models import AutorizacionesDetalle, Autorizaciones, EstadosAutorizacion
import io
from clinico.models import Historia, HistoriaMedicamentos
from facturacion.models import Liquidacion, LiquidacionDetalle
from django.utils import timezone
from farmacia.models import FarmaciaEstados
from cartera.models import Pagos
from triage.models import Triage


def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")



# Create your views here.

# Create your views here.
def load_dataAutorizaciones(request, data):
    print("Entre load_dataAutorizaciones")

    print("llegue bien01")

    context = {}
    d = json.loads(data)

    print("llegue bien02")

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    estadoAutorizado = EstadosAutorizacion.objects.get(nombre='AUTORIZADO')

    # Combo Indicadores

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT ser.nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
        sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + str(
        'O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str(
        'N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(
        sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str(
        'TRIAGE') + "'" + ' group by ser.nombre'

    curt.execute(comando)
    print(comando)

    indicadores = []

    for id, nombre in curt.fetchall():
        indicadores.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(indicadores)

    context['Indicadores'] = indicadores

    # Fin combo Indicadores

    autorizaciones = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    #detalle = 'select aut.id id ,aut."sedesClinica_id" ,sed.nombre sede,usu.nombre paciente,historia_id folio,"fechaSolicitud",aut.justificacion,"numeroAutorizacion","fechaAutorizacion", pla.nombre medico, aut.observaciones, estado.nombre estadoAutorizacion, "numeroSolicitud", "fechaVigencia", empresa_id, emp.nombre empresaNombre, "plantaOrdena_id", aut."usuarioRegistro_id" FROM autorizaciones_autorizaciones aut, sitios_sedesClinica sed, facturacion_empresas emp, clinico_historia historia, usuarios_usuarios usu, planta_planta pla , autorizaciones_estadosAutorizacion estado  where historia.id = aut.historia_id and sed.id = aut."sedesClinica_id" and emp.id = aut.empresa_id and usu."tipoDoc_id" = historia."tipoDoc_id" and usu.id = historia.documento_id and pla.id = aut."plantaOrdena_id" and estado.id = aut."estadoAutorizacion_id"          '
    detalle = 'select aut.id id ,aut."sedesClinica_id" ,sed.nombre sede,usu.nombre paciente,historia_id folio,"fechaSolicitud",aut.justificacion, "numeroAutorizacion","fechaAutorizacion", pla.nombre medico, aut.observaciones, estado.nombre estadoAutorizacion, "numeroSolicitud", "fechaVigencia", empresa_id, emp.nombre empresaNombre, "plantaOrdena_id", aut."usuarioRegistro_id" FROM autorizaciones_autorizaciones aut INNER JOIN sitios_sedesClinica sed on (sed.id = aut."sedesClinica_id") LEFT JOIN  facturacion_empresas emp ON (emp.id = aut.empresa_id) INNER JOIN  clinico_historia historia ON (historia.id = aut.historia_id ) INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id" = historia."tipoDoc_id" and usu.id = historia.documento_id) INNER JOIN planta_planta pla ON (pla.id = aut."plantaOrdena_id") INNER JOIN  autorizaciones_estadosAutorizacion estado ON (estado.id = aut."estadoAutorizacion_id" ) INNER JOIN sitios_dependencias dep on (dep."tipoDoc_id" = historia."tipoDoc_id" AND dep.documento_id = historia.documento_id and dep.consec=historia."consecAdmision") where aut."sedesClinica_id" = ' + "'"  + str(sede) + "' AND " + ' aut."estadoAutorizacion_id" != ' + "'" + str(estadoAutorizado.id) + "'"

    print(detalle)

    curx.execute(detalle)

    for id ,sedesClinica_id,sede,paciente,folio,fechaSolicitud,justificacion,numeroAutorizacion,fechaAutorizacion, medico,observaciones,estadoAutorizacion,numeroSolicitud,fechaVigencia,empresa_id, empresaNombre,plantaOrdena_id,usuarioRegistro_id in curx.fetchall():
        autorizaciones.append(
            {"model": "autorizaciones_autorizaciones", "pk": id, "fields":
                {'id': id, 'sedesClinica_id': sedesClinica_id, 'sede': sede,'paciente': paciente,'folio': folio,'fechaSolicitud': fechaSolicitud,'justificacion':justificacion,   'numeroAutorizacion':numeroAutorizacion,'fechaAutorizacion':fechaAutorizacion,
                   'numeroAutorizacion': numeroAutorizacion, 'fechaAutorizacion':fechaAutorizacion,  'medico': medico, 'observaciones': observaciones,'estadoAutorizacion':estadoAutorizacion, 'numeroSolicitud':numeroSolicitud,
                 'fechaVigencia': fechaVigencia, 'empresa_id':empresa_id, 'empresaNombre':empresaNombre, 'plantaOrdena_id':plantaOrdena_id,'usuarioRegistro_id':usuarioRegistro_id}})
    miConexionx.close()
    print("autorizaciones "  , autorizaciones)
    context['Autorizaciones'] = autorizaciones

    serialized1 = json.dumps(autorizaciones, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')


def load_dataAutorizacionesDetalle(request, data):
    print("Entre load_dataAutorizacionesDetalle")

    print("llegue bien01")

    context = {}
    d = json.loads(data)

    print("llegue bien02")

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    autorizacionId = d['autorizacionId']
    print("autorizacionId:", autorizacionId)

    autorizado = EstadosAutorizacion.objects.get(nombre='AUTORIZADO')

    # Combo Indicadores

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT ser.nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
        sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + str(
        'O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str(
        'N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(
        sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str(
        'TRIAGE') + "'" + ' group by ser.nombre'

    curt.execute(comando)
    print(comando)

    indicadores = []

    for id, nombre in curt.fetchall():
        indicadores.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(indicadores)

    context['Indicadores'] = indicadores

    # Fin combo Indicadores

    autorizacionesDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'select ' + "'" + str('CUPS') + "'" + ' tipoTipoExamen, autdet.id id ,tipoexa.nombre tipoExamen,autdet.examenes_id examenId, exa.nombre examen,autdet."cantidadSolicitada", autdet."cantidadAutorizada",autdet."valorSolicitado", autdet."valorAutorizado", estado.nombre autorizado , autdet."usuarioRegistro_id" from autorizaciones_autorizacionesdetalle autdet, clinico_tiposexamen tipoexa, clinico_examenes exa , autorizaciones_estadosAutorizacion estado where autdet.autorizaciones_id = ' + "'" + str(autorizacionId) + "'" + ' and autdet."tiposExamen_id" = tipoexa.id and autdet.examenes_id = exa.id and autdet.examenes_id is not null and estado.id=autdet."estadoAutorizacion_id" union select ' + "'" + str('SUMINISTRO') + "'" + ' tipoTipoExamen, autdet.id id, tiposum.nombre tiposum, autdet.cums_id examenId, sum.nombre suministro, autdet."cantidadSolicitada", autdet."cantidadAutorizada", autdet."valorSolicitado", autdet."valorAutorizado" , estado.nombre ,autdet."usuarioRegistro_id"  from autorizaciones_autorizacionesdetalle autdet, facturacion_tipossuministro tiposum, facturacion_suministros sum , autorizaciones_estadosAutorizacion estado where autdet.autorizaciones_id = ' + "'" + str(autorizacionId) + "'" + ' and autdet."tipoSuministro_id" = tiposum.id and autdet.cums_id = sum.id and autdet.cums_id is not null and estado.id=autdet."estadoAutorizacion_id" AND autdet."estadoAutorizacion_id" != ' +"'" + str(autorizado.id) +"'"

    print(detalle)

    curx.execute(detalle)

    for tipoTipoExamen, id , tipoExamen, examenId, examen,cantidadSolicitada, cantidadAutorizada, valorSolicitado,valorAutorizado,autorizado , usuarioRegistro_id in curx.fetchall():
        autorizacionesDetalle.append(
            {"model": "autorizaciones_autorizacionesDetalle", "pk": id, "fields":
                {'tipoTipoExamen': tipoTipoExamen, 'id': id, 'tipoExamen': tipoExamen, 'examenId':examenId,'examen': examen,'cantidadSolicitada': cantidadSolicitada,'cantidadAutorizada': cantidadAutorizada,'valorSolicitado': valorSolicitado,'valorAutorizado':valorAutorizado,
                 'autorizado':autorizado,'usuarioRegistro_id':usuarioRegistro_id}})
    miConexionx.close()
    print("autorizacionesDetalle "  , autorizacionesDetalle)

    serialized1 = json.dumps(autorizacionesDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def ActualizarAutorizacionDetalle(request):

    print ("Entre ActualizarAutorizacionDetalle" )

    autorizacionDetalleId = request.POST['autorizacionDetalleId']
    print("autorizacionDetalleId =", autorizacionDetalleId)

    estadoAutorizacion = request.POST['estadoAutorizacion']
    print("estadoAutorizacion =", estadoAutorizacion)

    estadoAutorizacionAutorizado = EstadosAutorizacion.objects.get(nombre='AUTORIZADO')
    print("estadoAutorizacion =", estadoAutorizacion)

    serviciosAdministrativos = request.POST['AserviciosAdministrativos']
    print("estadoAutorizacionAutorizado =", estadoAutorizacionAutorizado)

    numeroAutorizacion = request.POST['numeroAutorizacion']
    print("numeroAutorizacion =", numeroAutorizacion)

    examenId =request.POST['examenes_id']
    print("examenId:", examenId)

    tipoTipoExamen = request.POST['tipoTipoExamen']
    print("tipoTipoExamen:", tipoTipoExamen)

    cantidadAutorizada = request.POST['cantidadAutorizada']
    print("cantidadAutorizada =", cantidadAutorizada)

    valorAutorizado = request.POST['valorAutorizado']
    print("valorAutorizado =", valorAutorizado)

    convenioId = request.POST['Aconvenios']
    print("convenioId =", convenioId)

    sede = request.POST['Psede']
    print("sede =", sede)

    fechaRegistro = timezone.now()
    print("fechaRegistro = ", fechaRegistro)

    estadoReg = 'A'
    usuarioRegistro_id = request.POST['usuarioRegistro2_id']

    print ("usuarioRegistro_id", usuarioRegistro_id)
    # ACTUALIZA DETALLE AUTORIZACION

    #miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
    #                               password="123456")
    #curx = miConexionx.cursor()

    #detalle = 'UPDATE autorizaciones_autorizacionesdetalle SET  "estadoAutorizacion_id" =   ' + "'" + str(estadoAutorizacion) + "'," + ' "numeroAutorizacion" = '   + "'" + str(numeroAutorizacion) + "'," + ' "valorAutorizado" = ' + "'" + str(valorAutorizado) + "'," +   ' "fechaRegistro" = ' + "'" + str(fechaRegistro) + "',"  + ' "cantidadAutorizada" = ' + "'" + str(cantidadAutorizada) +  "'" +  ' WHERE id = ' + "'" + str(autorizacionDetalleId) + "'"

    #print("detalle = ", detalle)

    #curx.execute(detalle)
    #miConexionx.commit()
    #miConexionx.close()

    # RUTINA SI ESTA AUTORIZADO DEBE CREAR EN FACTURACONDETALLE, OPS CON TARIFA ?????? o el valor lo trae de la autoprizacion mejor

    datosAut1 = AutorizacionesDetalle.objects.get(id = autorizacionDetalleId)
    datosAut = Autorizaciones.objects.get(id=datosAut1.autorizaciones_id)

    print ("Historia = ", datosAut.historia_id)		

    datosHc = Historia.objects.get(id=datosAut.historia_id)
    print ("TipoDoc Paciente = ", datosHc.tipoDoc_id)
    print ("Paciente Cedula= ", datosHc.documento_id)
    print ("Paciente Ingreso= ", datosHc.consecAdmision)

    if (datosHc.consecAdmision!=0):

        ingresoId = Ingresos.objects.get(tipoDoc_id=datosHc.tipoDoc_id, documento_id=datosHc.documento_id,consec=datosHc.consecAdmision)
    else:
        triageId = Triage.objects.get(tipoDoc_id=datosHc.tipoDoc_id, documento_id=datosHc.documento_id,consec=datosHc.consecAdmision, consecAdmision=0)

    estadoFarmaciaSolicitud = FarmaciaEstados.objects.get(nombre='SOLICITUD')

    miConexiont = None
    try:

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        datosliq = Liquidacion.objects.get(tipoDoc_id=datosHc.tipoDoc.id, documento_id=datosHc.documento_id,    consecAdmision=datosHc.consecAdmision, convenio_id=convenioId)
        liquidacionId = datosliq.id
        consecLiquidacionU = LiquidacionDetalle.objects.filter(liquidacion_id=liquidacionId).aggregate(maximo=Coalesce(Max('consecutivo'), 0))
        consecLiquidacion = (consecLiquidacionU['maximo']) + 1

        if (tipoTipoExamen == 'CUPS'):

            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia_id,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro",anulado) VALUES (' + "'" + str(
                consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str(cantidadAutorizada) + "','" + str(
                valorAutorizado) + "','" + str(valorAutorizado) + "',null," + "'" + str(
                fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(
                examenId) + "','" + str(usuarioRegistro_id) + "','" + str(liquidacionId) + "','" + str(
                'SISTEMA') + "'" + ",'N')"
            print("comando = ", comando)
            curt.execute(comando)

        else:

            # Aqui Gaurdar FARMACIA

            if (datosHc.consecAdmision != 0):

                comando = 'INSERT INTO farmacia_farmacia(historia_id,"serviciosAdministrativos_id","tipoOrigen_id","tipoMovimiento_id","fechaRegistro", "usuarioRegistro_id","sedesClinica_id",estado_id,"ingresoPaciente") VALUES (' + "'" + str(
                    datosAut.historia_id) + "','" + str(serviciosAdministrativos) + "',1,1," + "'" + str(
                    fechaRegistro) + "','" + str(usuarioRegistro_id) + "','" + str(sede) + "','" + str(
                    estadoFarmaciaSolicitud.id) + "','" + str(ingresoId.id) + "') RETURNING id"
                print("comando = ", comando)
                resultado = curt.execute(comando)
                farmaciaId = curt.fetchone()[0]

            else:

                comando = 'INSERT INTO farmacia_farmacia(historia_id,"serviciosAdministrativos_id","tipoOrigen_id","tipoMovimiento_id","fechaRegistro", "usuarioRegistro_id","sedesClinica_id",estado_id,"ingresoPaciente") VALUES (' + "'" + str(
                    datosAut.historia_id) + "','" + str(serviciosAdministrativos) + "',1,1," + "'" + str(
                    fechaRegistro) + "','" + str(usuarioRegistro_id) + "','" + str(sede) + "','" + str(
                    estadoFarmaciaSolicitud.id) + "','" + str(triageId.id) + "') RETURNING id"
                print("comando = ", comando)
                resultado = curt.execute(comando)
                farmaciaId = curt.fetchone()[0]



            # Aqui Guardar ENFERMERIA
            if (datosHc.consecAdmision != 0):

                comando = 'INSERT INTO enfermeria_enfermeria(historia_id,"serviciosAdministrativos_id","tipoOrigen_id","tipoMovimiento_id","fechaRegistro", "usuarioRegistro_id","sedesClinica_id","estadoReg","ingresoPaciente",anulado) VALUES (' + "'" + str(
                    datosAut.historia_id) + "','" + str(serviciosAdministrativos) + "',1,1," + "'" + str(
                    fechaRegistro) + "','" + str(usuarioRegistro_id) + "','" + str(sede) + "','" + str(
                    estadoReg) + "','" + str(ingresoId.id) + "','N') RETURNING id"
                resultado = curt.execute(comando)
                print("comando = ", comando)
                enfermeriaId = curt.fetchone()[0]
            else:
                comando = 'INSERT INTO enfermeria_enfermeria(historia_id,"serviciosAdministrativos_id","tipoOrigen_id","tipoMovimiento_id","fechaRegistro", "usuarioRegistro_id","sedesClinica_id","estadoReg","ingresoPaciente", anulado) VALUES (' + "'" + str(
                    datosAut.historia_id) + "','" + str(serviciosAdministrativos) + "',1,1," + "'" + str(
                    fechaRegistro) + "','" + str(usuarioRegistro_id) + "','" + str(sede) + "','" + str(
                    estadoReg) + "','" + str(triageId.id) + "','A') RETURNING id"
                resultado = curt.execute(comando)
                print("comando = ", comando)
                enfermeriaId = curt.fetchone()[0]

            # Aqui Guardar FARMACIA DETALLE
            comando = 'INSERT INTO farmacia_farmaciadetalle(farmacia_id, "historiaMedicamentos_id",suministro_id,"dosisCantidad", "dosisUnidad_id","viaAdministracion_id","cantidadOrdenada","fechaRegistro","usuarioRegistro_id", "estadoReg", "consecutivoMedicamento")  SELECT ' + "'" + str(
                farmaciaId) + "', id," + ' suministro_id,"dosisCantidad" , "dosisUnidad_id" , "viaAdministracion_id" ,"cantidadSolicitada",' + "'"  + str(
                fechaRegistro) + "'," + "'"  + str(usuarioRegistro_id) + "',"  + "'A'" + ', "consecutivoMedicamento"  FROM clinico_HistoriaMedicamentos WHERE historia_id = ' + "'" + str(
                datosAut.historia_id) + "' AND " + ' id = ' + "'" + str(datosAut1.historiaMedicamentos_id) + "' RETURNING id"
            print("comando = ", comando)

            resultado = curt.execute(comando)
            farmaciaDetalleId = curt.fetchone()[0]

            # Aqui Guardar ENFERMERIA DETALLE
            comando = 'INSERT INTO enfermeria_enfermeriadetalle(enfermeria_id, "historiaMedicamentos_id","farmaciaDetalle_id", suministro_id,"dosisCantidad", "dosisUnidad_id","viaAdministracion_id","cantidadOrdenada","fechaRegistro","usuarioRegistro_id", "estadoReg", frecuencia_id, "diasTratamiento",anulado)  SELECT ' + "'" + str(
                enfermeriaId) + "'," + ' id,' + "'" + str(farmaciaDetalleId) + "'," + ' suministro_id,"dosisCantidad" , "dosisUnidad_id" , "viaAdministracion_id" ,"cantidadSolicitada",' + "'" + str(fechaRegistro) + "','" + str(usuarioRegistro_id) + "','A'," + ' frecuencia_id, "diasTratamiento" ,' + "'" + str('N') + "'" + ' FROM clinico_HistoriaMedicamentos WHERE historia_id = ' + "'" + str(
                datosAut.historia_id) + "' AND " + ' id = ' + "'" + str(datosAut1.historiaMedicamentos_id) + "'"
            print("comando = ", comando)
            curt.execute(comando)

        ## Vamops a actualizar los totales de la Liquidacion:
                #
        # Rutina Guarda en cabezote los totales

        print ("Voy a grabar el cabezote")
        print ("liquidacionId = ", liquidacionId)

        miConexiont.commit()
        miConexiont.close()

        #message_error= str(error)

    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexiont.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexiont:
            curt.close()
            miConexiont.close()


    # VA tocar sacar encabezados

    print ("voy a a totalizar")

    totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(examen_id=None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
    totalSuministros = (totalSuministros['totalS']) + 0
    print("totalSuministros", totalSuministros)
    totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(
        cums_id=None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
    totalProcedimientos = (totalProcedimientos['totalP']) + 0
    print("totalProcedimientos", totalProcedimientos)
    registroPago = Liquidacion.objects.get(id=liquidacionId)

    # Continua Aqui

    totalCopagos = Pagos.objects.all().filter(tipoDoc_id=datosHc.tipoDoc_id).filter(
        documento_id=datosHc.documento_id).filter(consec=datosHc.consecAdmision).filter(formaPago_id=4).exclude(
        estadoReg='I').exclude(anulado='S').aggregate(totalC=Coalesce(Sum('valorEnCurso'), 0))
    totalCopagos = (totalCopagos['totalC']) + 0
    print("totalCopagos", totalCopagos)
    totalCuotaModeradora = Pagos.objects.all().filter(tipoDoc_id=datosHc.tipoDoc_id).filter(
        documento_id=datosHc.documento_id).filter(consec=datosHc.consecAdmision).filter(formaPago_id=3).exclude(
        estadoReg='I').exclude(anulado='S').aggregate(totalM=Coalesce(Sum('valorEnCurso'), 0))
    totalCuotaModeradora = (totalCuotaModeradora['totalM']) + 0
    print("totalCuotaModeradora", totalCuotaModeradora)
    totalAnticipos = Pagos.objects.all().filter(tipoDoc_id=datosHc.tipoDoc_id).filter(
        documento_id=datosHc.documento_id).filter(consec=datosHc.consecAdmision).filter(formaPago_id=1).exclude(
        estadoReg='I').exclude(anulado='S').aggregate(Anticipos=Coalesce(Sum('valorEnCurso'), 0))
    totalAnticipos = (totalAnticipos['Anticipos']) + 0
    print("totalAnticipos", totalAnticipos)
    totalAbonos = Pagos.objects.all().filter(tipoDoc_id=datosHc.tipoDoc_id).filter(
        documento_id=datosHc.documento_id).filter(consec=datosHc.consecAdmision).filter(formaPago_id=2).exclude(
        estadoReg='I').exclude(anulado='S').aggregate(totalAb=Coalesce(Sum('valorEnCurso'), 0))
    totalAbonos = (totalAbonos['totalAb']) + 0
    # totalAbonos = totalCopagos + totalAnticipos + totalCuotaModeradora
    print("totalAbonos", totalAbonos)

    totalRecibido = totalCopagos + totalCuotaModeradora + totalAnticipos + totalAbonos
    totalApagar = totalSuministros + totalProcedimientos - totalRecibido
    totalLiquidacion = totalSuministros + totalProcedimientos
    print("totalLiquidacion", totalLiquidacion)
    print("totalAPagar", totalApagar)

    miConexiont = None
    try:

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        curt = miConexiont.cursor()

        comanda = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' +  "'" +  str(totalSuministros) + "'" + ',"totalProcedimientos" = ' + "'" +  str(totalProcedimientos) + "'"  + ', "totalCopagos" = ' + "'" +  str(totalCopagos) + "'"  + ' , "totalCuotaModeradora" = ' + "'" +  str(totalCuotaModeradora) + "'" + ', anticipos = ' + "'" +  str(totalAnticipos) + "'"  + ' ,"totalAbonos" = ' + "'" + str(totalAbonos) + "'" + ', "totalLiquidacion" = ' + "'" + str(totalLiquidacion) + "'" + ', "valorApagar" = ' + "'" + str(totalApagar) + "'"   + ', "totalRecibido" = ' + "'" + str(totalRecibido) + "'"  + ' WHERE id =' + "'" + str(liquidacionId) + "'"
        print("COMANDA = " , comanda)

        curt.execute(comanda)

        detalle = 'UPDATE autorizaciones_autorizacionesdetalle SET  "estadoAutorizacion_id" =   ' + "'" + str(estadoAutorizacion) + "'," + ' "numeroAutorizacion" = '   + "'" + str(numeroAutorizacion) + "'," + ' "valorAutorizado" = ' + "'" + str(valorAutorizado) + "'," +   ' "fechaRegistro" = ' + "'" + str(fechaRegistro) + "',"  + ' "cantidadAutorizada" = ' + "'" + str(cantidadAutorizada) +  "'" +  ' WHERE id = ' + "'" + str(autorizacionDetalleId) + "'"
        print("detalle = ", detalle)
        curt.execute(detalle)

        miConexiont.commit()
        miConexiont.close()


    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexiont.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexiont:
            curt.close()
            miConexiont.close()

    # fin rutina totales


    ## Aqui rutina actualizar el cabezote de autorizaciones el estado AUTORIZADO si todos los hijos autorizacionesdetalle esta AUTORIZADOS

    print ("datosAut.id = ", datosAut.id)
    print("estadoAutorizacionAutorizado.id= " , estadoAutorizacionAutorizado.id)

    noAutorizados = AutorizacionesDetalle.objects.filter(autorizaciones_id = datosAut.id).exclude(estadoAutorizacion_id=estadoAutorizacionAutorizado.id).count()
    print("noAutorizados = ", noAutorizados )

    if (noAutorizados == 0):

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando12 = 'UPDATE autorizaciones_autorizaciones SET "estadoAutorizacion_id" = ' + "'" + str(estadoAutorizacionAutorizado.id) + "' WHERE id = " + "'" + str(datosAut.id) + "'"
        print("COMANDO12 = " , comando12)
        curt.execute(comando12)

        miConexiont.commit()
        miConexiont.close()

    ## si no existe hay que crear cabezote
    ## Aqui actualiza el numero de autorizacion para medicamentos

    if (tipoTipoExamen != 'CUPS'):

        HistoriaMedicamentos.objects.filter(historia_id=datosHc.id).update(autorizacion_id=datosAut.id)


    ## Fin Actualiza autorizacion para medicamentos

    return JsonResponse({'success': True, 'Mensajes': 'Detalle de Autorizacion actualizado satisfactoriamente!'})


def LeerDetalleAutorizacion(request):

    autorizacionDetalleId = request.POST['autorizacionDetalleId']
    print("autorizacionDetalleId =", autorizacionDetalleId)


    tipotipoExamen = AutorizacionesDetalle.objects.get(id=autorizacionDetalleId)

    print (" tipotipoExamen = ",tipotipoExamen.examenes_id )

    #Lee detalle Autorizacion

    context = {}

    autorizacionDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    print("tipotipoExamen.examenes_id =" ,tipotipoExamen.examenes_id )
    print("tipotipoExamen.cums_id =", tipotipoExamen.cums_id)

    if (tipotipoExamen.examenes_id != '' and tipotipoExamen.examenes_id != None ):

        print ("entre cups")

        detalle = 'select ' + "'" + str('CUPS') + "' tipoTipoExamen," + ' det.id, "cantidadSolicitada", "cantidadAutorizada", det."fechaRegistro", det."estadoReg", autorizaciones_id, det."usuarioRegistro_id", tipexa.nombre tipNombre  , exa.nombre exaNombre,  examenes_id, "valorAutorizado", "valorSolicitado", "tiposExamen_id", "tipoSuministro_id", det."estadoAutorizacion_id", det."numeroAutorizacion" , est.nombre estadoNombre , aut.convenio_id convenioId FROM autorizaciones_autorizaciones aut, autorizaciones_autorizacionesdetalle det, autorizaciones_estadosautorizacion est, clinico_tiposexamen tipexa, clinico_examenes exa  WHERE aut.id = det."autorizaciones_id" AND det.id =' + "'" + str(autorizacionDetalleId) + "'" + ' AND tipexa.id = det."tiposExamen_id" AND exa.id = det.examenes_id AND est.id = det."estadoAutorizacion_id"'

    if (tipotipoExamen.cums_id != '' and tipotipoExamen.cums_id != None):
        print("entre suministros")

        #detalle = 'select ' + "'" + str('SUMINISTROS') + "' tipoTipoExamen," + ' det.id, "cantidadSolicitada", "cantidadAutorizada", det."fechaRegistro", det."estadoReg", autorizaciones_id, det."usuarioRegistro_id",  tipsum.nombre tipNombre, exa.nombre exaNombre,  cums_id, "valorAutorizado", "valorSolicitado", "tiposExamen_id", det."tipoSuministro_id", det."estadoAutorizacion_id", det."numeroAutorizacion" , est.nombre estadoNombre, aut.convenio_id convenioId FROM autorizaciones_autorizacionesdetalle det, autorizaciones_estadosautorizacion est, facturacion_tipossuministro tipsum, facturacion_suministros exa                                       WHERE aut.id = det."autorizaciones_id" and det.id =' + "'" + str(autorizacionDetalleId) + "'" + 'AND tipsum.id = det."tipoSuministro_id"  AND exa.id = det.cums_id AND  est.id = det."estadoAutorizacion_id"'
        detalle =  'select ' + "'" + str('SUMINISTROS') + "' tipoTipoExamen," + ' det.id, "cantidadSolicitada", "cantidadAutorizada", det."fechaRegistro", det."estadoReg", autorizaciones_id, det."usuarioRegistro_id", tipsum.nombre tipNombre  , exa.nombre exaNombre,  cums_id, "valorAutorizado", "valorSolicitado", "tiposExamen_id", det."tipoSuministro_id", det."estadoAutorizacion_id", det."numeroAutorizacion" , est.nombre estadoNombre , aut.convenio_id convenioId FROM autorizaciones_autorizaciones aut, autorizaciones_autorizacionesdetalle det, autorizaciones_estadosautorizacion est, facturacion_tipossuministro tipsum, facturacion_suministros exa  WHERE aut.id = det."autorizaciones_id" AND det.id =' + "'" + str(autorizacionDetalleId) + "'" + ' AND tipsum.id = det."tipoSuministro_id" AND exa.id = det.cums_id AND  est.id = det."estadoAutorizacion_id"'

    print(detalle)

    curx.execute(detalle)

    for tipoTipoExamen,id, cantidadSolicitada, cantidadAutorizada, fechaRegistro, estadoReg, autorizaciones_id, usuarioRegistro_id, tipNombre, exaNombre, examenes_id,  valorAutorizado,	valorSolicitado, tiposExamen_id, tipoSuministro_id, estadoAutorizacion_id, numeroAutorizacion, estadoNombre , convenioId in curx.fetchall():
        autorizacionDetalle.append(
            {"model": "autorizaciones_autorizacionesdetalle", "pk": id, "fields":
                {'tipoTipoExamen':tipoTipoExamen, 'id':id, 'cantidadSolicitada':cantidadSolicitada,'cantidadAutorizada':cantidadAutorizada,'fechaRegistro':fechaRegistro,'estadoReg':estadoReg,
                 'autorizaciones_id':autorizaciones_id,'usuarioRegistro_id':usuarioRegistro_id,'tipNombre':tipNombre, 'exaNombre':exaNombre, 'examenes_id':examenes_id,'valorAutorizado':valorAutorizado,
                 'valorSolicitado':valorSolicitado,'tiposExamen_id':tiposExamen_id,'tipoSuministro_id':tipoSuministro_id,'estadoAutorizacion_id':estadoAutorizacion_id,'numeroAutorizacion':id,'numeroAutorizacion':numeroAutorizacion,'estadoNombre':estadoNombre, 'convenio_id':convenioId}})

    miConexionx.close()
    print("autorizacionDetalle ", autorizacionDetalle)


    serialized1 = json.dumps(autorizacionDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')
