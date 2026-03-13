from django.shortcuts import render
import json
from django import forms
import cv2
import numpy as np
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.utils.timezone import now
from django.db.models import Avg, Max, Min, Sum
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.http import JsonResponse
from django.db.models import Max
from django.utils import timezone
#import MySQLdbg
import pyodbc
import psycopg2
import json
import datetime
from decimal import Decimal
from admisiones.models import Ingresos
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle, TiposSuministro, Conceptos
from cartera.models import TiposPagos, FormasPagos, Pagos, PagosFacturas, Glosas, NotasCredito
from triage.models import Triage
from clinico.models import Servicios
from rips.models import RipsTransaccion, RipsUsuarios, RipsEnvios, RipsDetalle, RipsTiposNotas
import pickle
import io
from rips.models import RipsEstados, RipsEnvios, RipsDetalle, RipsTransaccion, RipsHospitalizacion, RipsProcedimientos, RipsMedicamentos, RipsRecienNacido, RipsUrgenciasObservacion, RipsConsultas
from django.db.models import Q


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
def load_dataEnviosRips(request, data):
    print("Entre load_data Envios Rips")

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

    enviosRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT env.id,  env."fechaEnvio", env."fechaRespuesta", env."cantidadFacturas", env."cantidadPasaron", env."cantidadRechazadas",env."ripsEstados_id",  estrips.nombre estadoMinisterio, env."fechaRegistro", env."estadoReg", env."usuarioRegistro_id", env.empresa_id, env."sedesClinica_id" , sed.nombre nombreClinica, emp.nombre nombreEmpresa , pla.nombre nombreRegistra , tiposNotas.nombre tipoNota FROM public.rips_ripsenvios env, sitios_sedesclinica sed, facturacion_empresas emp, planta_planta pla , rips_ripstiposnotas tiposNotas , rips_ripsestados estrips where env."sedesClinica_id" = sed.id and env.empresa_id=emp.id AND pla.id = env."usuarioRegistro_id" AND env."ripsTiposNotas_id" = tiposNotas.id AND estrips.id = env."ripsEstados_id" AND env."sedesClinica_id" =' +  "'" + str(sede) + "' AND (estRips.nombre = " + "'" + str('PENDIENTE') + "' or estRips.nombre = '" + str('PENDIENTE CON JSON GENERADO') + "')"

    print(detalle)

    curx.execute(detalle)

    for id,  fechaEnvio, fechaRespuesta, cantidadFacturas, cantidadPasaron, cantidadRechazadas, estadoPasoMinisterio, estadoMinisterio ,fechaRegistro, estadoReg, usuarioRegistro_id, empresa_id, sedesClinica_id, nombreClinica, nombreEmpresa, nombreRegistra, tipoNota in curx.fetchall():
        enviosRips.append(
            {"model": "rips.ripsEnvios", "pk": id, "fields":
                {'id': id, 'fechaEnvio': fechaEnvio, 'fechaRespuesta': fechaRespuesta, 'cantidadFacturas': cantidadFacturas,
                 'cantidadPasaron': cantidadPasaron, 'cantidadRechazadas': cantidadRechazadas,
                 'estadoMinisterio': estadoMinisterio, 'estadoMinisterio':estadoMinisterio,  'fechaRegistro': fechaRegistro, 'estadoReg': estadoReg,'usuarioRegistro_id':usuarioRegistro_id, 'empresa_id':empresa_id, 'sedesClinica_id': sedesClinica_id, 'nombreClinica':nombreClinica, 'nombreEmpresa':nombreEmpresa,'nombreRegistra':nombreRegistra, 'tipoNota':tipoNota}})

    miConexionx.close()
    print("EnviosRips "  , enviosRips)
    context['EnviosRips'] = enviosRips

    serialized1 = json.dumps(enviosRips, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')


def GuardaEnviosRips(request):

    print ("Entre Guarda Envios Rips" )

    empresa_id = request.POST['empresa_id']
    print("empresa_id =", empresa_id)

    sedesClinica_id = request.POST['sedesClinica_id']
    print("sedesClinica_id =", sedesClinica_id)

    tipoRips = request.POST['ripsTiposNotas']
    print("ripsTiposNotas =", tipoRips)

    fechaEnvio = request.POST['fechaEnvio']
    print ("fechaEnvio =", fechaEnvio)

    fechaRespuesta = request.POST['fechaRespuesta']
    print ("fechaRespuesta =", fechaRespuesta)

    cantidadFacturas = request.POST['cantidadFacturas']
    print ("cantidadFacturas =", cantidadFacturas)
    cantidadPasaron = request.POST['cantidadPasaron']
    print ("cantidadPasaron =", cantidadPasaron)
    cantidadRechazadas = request.POST['cantidadRechazadas']
    print ("cantidadRechazadas =", cantidadRechazadas)
    serviciosAdministrativos = request.POST['serviciosAdministrativos']
    print ("serviciosAdministrativos =", serviciosAdministrativos)

    estadoMinisterio = request.POST['estadoMinisterio']
    print ("estadoMinisterio =", estadoMinisterio)
    usuarioRegistro_id = request.POST['usuarioRegistro_id']
    print ("usuarioRegistro_id =", usuarioRegistro_id)
    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    if (fechaEnvio==''):
        fechaEnvio= fechaRegistro

    if (fechaRespuesta==''):
        fechaRespuesta= None

    print("fechaEnvio =", fechaEnvio)
    print ("fechaRespuesta =", fechaRespuesta)

    estadoRips = RipsEstados.objects.get(nombre='PENDIENTE')

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()
        comando = 'insert into rips_ripsEnvios  ("fechaEnvio","cantidadFacturas", "cantidadPasaron", "cantidadRechazadas","ripsEstados_id", "fechaRegistro", "estadoReg", "usuarioRegistro_id", empresa_id, "sedesClinica_id", "ripsTiposNotas_id", "fechaCreacion","serviciosAdministrativos_id") values ('  + "'" + str(fechaEnvio) + "',"  +  "'" + str(cantidadFacturas) + "'" + ' , '  + "'" + str(cantidadPasaron) + "'" + ', ' + "'" + str(cantidadRechazadas) + "'" + '  , ' + "'" + str(estadoRips.id) + "'" + '  , '  "'" + str(fechaRegistro) + "','"   + str(estadoReg) + "'," + "'" + str(usuarioRegistro_id) + "','" + str(empresa_id) + "','" + str(sedesClinica_id) + "','" + str(tipoRips) +  "','" + str(fechaRegistro) + "','" + str(serviciosAdministrativos) + "'" + ');'
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Envio creado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


    #  DESDE AQUI EL DETALLE

def load_dataDetalleRips(request, data):
    print("Entre load_data Detalle Rips")

    context = {}
    d = json.loads(data)

    empresaId = d['empresaId']
    print("empresaId = ", empresaId)

    envioRipsId = d['envioRipsId']
    print("envioRipsId = ", envioRipsId)


    detalleRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    #detalle = 'SELECT id,  "numeroFactura_id"  numeroFactura , glosa_id glosaId, "notaCredito_id" notaCreditoId , "cuv", "estadoPasoMinisterio","rutaJsonRespuesta", "rutaJsonFactura",  "fechaRegistro", "estadoReg", "ripsEnvios_id",  "usuarioRegistro_id", "rutaPdf", "rutaZip"  FROM public.rips_ripsDetalle WHERE "ripsEnvios_id" =  ' + "'" + str(envioRipsId) + "'"
    detalle = 'SELECT rips_ripsDetalle.id,  "numeroFactura_id"  numeroFactura , usu.nombre nombre, glosa_id glosaId, "notaCredito_id" notaCreditoId , "cuv", "estadoPasoMinisterio","rutaJsonRespuesta", "rutaJsonFactura",  rips_ripsDetalle."fechaRegistro", rips_ripsDetalle."estadoReg", "ripsEnvios_id",  rips_ripsDetalle."usuarioRegistro_id", rips_ripsDetalle."rutaPdf", rips_ripsDetalle."rutaZip"  FROM public.rips_ripsDetalle INNER JOIN facturacion_facturacion fac on (fac.id=rips_ripsDetalle."numeroFactura_id") INNER JOIN usuarios_usuarios usu on (usu.id =fac.documento_id) WHERE "ripsEnvios_id" =  ' + "'" + str(envioRipsId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id,  numeroFactura,nombre, glosaId , notaCreditoId, cuv, estadoPasoMinisterio,rutaJsonRespuesta,rutaJsonFactura,  fechaRegistro, estadoReg, ripsEnvios_id, usuarioRegistro_id, rutaPdf, rutaZip in curx.fetchall():
        detalleRips.append(
            {"model": "rips.detalleRips", "pk": id, "fields":
                {'id': id, 'numeroFactura': numeroFactura ,'nombre':nombre ,'glosaId':glosaId,  'notaCreditoId':notaCreditoId, 'cuv': cuv, 'estadoPasoMinisterio': estadoPasoMinisterio, 'rutaJsonRespuesta':rutaJsonRespuesta, 'rutaJsonFactura':rutaJsonFactura,
                   'fechaRegistro': fechaRegistro, 'estadoReg': estadoReg, 'ripsEnvios_id' :ripsEnvios_id, 'usuarioRegistro_id':usuarioRegistro_id, 'rutaPdf':rutaPdf,
                 'rutaZip': rutaZip}})

    miConexionx.close()
    print("detalleRips "  , detalleRips)
    context['DetalleRips'] = detalleRips

    serialized1 = json.dumps(detalleRips, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')


def GuardaDetalleRips(request):

    print ("Entre Guarda Detalle Rips" )

    detalleRipsId = request.POST['detalleRipsId']
    print("detalleRipsId =", detalleRipsId)


    numeroFactura_id = request.POST['numeroFacturaT']
    print("numeroFactura_id =", numeroFactura_id)

    cuv = request.POST['cuv']
    print("cuv =", cuv)

    estadoPasoMinisterio = request.POST['estadoPasoMinisterio']
    print ("estadoPasoMinisterio =", estadoPasoMinisterio)

    rutaJsonRespuesta = request.POST['rutaJsonRespuesta']
    print ("rutaJsonRespuesta =", rutaJsonRespuesta)

    rutaJsonFactura = request.POST['rutaJsonFactura']
    print ("rutaJsonFactura =", rutaJsonFactura)


    ripsEnvios_id = request.POST['ripsEnvios']
    print("ripsEnvios_id =", ripsEnvios_id)

    usuarioRegistro_id = request.POST['UsuarioRegistro_id']
    print ("usuarioRegistro_id =", usuarioRegistro_id)


    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    ripsEnvios_id = request.POST['ripsEnvios']
    print("ripsEnvios_id =", ripsEnvios_id)

    rutaPdf = request.POST['rutaPdf']
    print("rutaPdf =", rutaPdf)

    rutaZip = request.POST['rutaZip']
    print("rutaZip =", rutaZip)


    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()
        comando = 'UPDATE  rips_ripsdetalle SET cuv =  ' +  "'" + str(cuv) + "'," +  '"estadoPasoMinisterio" = ' + "'" + str(estadoPasoMinisterio) +  "'," + '"rutaJsonRespuesta"  = ' + "'" + str(rutaJsonRespuesta) + "'" + ',"rutaJsonFactura" = '  + "'" + str(rutaJsonFactura) + "'," +  ' "fechaRegistro" = ' + "'" + str(fechaRegistro) + "',"   + ' "estadoReg" = ' + "'" + str('A') + "'," + '"usuarioRegistro_id" =' + "'" + str(usuarioRegistro_id) + "'," + '"rutaPdf" = ' + "'" +str(rutaPdf) + "'," + '"rutaZip" =  ' + "'" + str(rutaZip)  + "' WHERE id =" + detalleRipsId

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Factura Adicionada al Envio satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


def load_dataDetalleRipsAdicionar(request, data):
    print("Entre load_data Detalle Rips Adicionar")

    context = {}
    d = json.loads(data)

    empresaId = d['empresaId']
    print("empresaId = ", empresaId)

    tipoRips = d['tipoRips']
    print("tipoRips = ", tipoRips)

    detalleRipsAdicion = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (tipoRips == 'Factura'):

        detalle = 'SELECT f.id,  f.id factura,0 as glosaId, f."fechaFactura", u.nombre paciente , f."totalFactura", f.estado  FROM public.facturacion_facturacion f, admisiones_ingresos i, usuarios_usuarios u  , contratacion_convenios c WHERE  i."tipoDoc_id" = f."tipoDoc_id" AND i.documento_id = f.documento_id AND f.convenio_id =  c.id AND   c.empresa_id = ' + "'" + str(empresaId) + "'" + ' AND f."ripsEnvio_id" IS NULL AND i."tipoDoc_id" = u."tipoDoc_id" AND i.documento_id = u.id AND i.consec = f."consecAdmision"'


    if (tipoRips == 'Glosa'):

        #detalle = 'SELECT g.id,  g.factura_id factura,g.id glosaId, g."fechaRecepcion" fechaFactura, u.nombre paciente , g."totalGlosa" totalFactura, g."estadoRecepcion_id" estado  FROM public.cartera_glosas g, facturacion_facturacion f , admisiones_ingresos i, usuarios_usuarios u  , contratacion_convenios c WHERE  g.factura_id  =  f.id and i."tipoDoc_id" = f."tipoDoc_id" AND i.documento_id = f.documento_id AND f.convenio_id =  c.id AND   c.empresa_id = ' + "'" + str(empresaId) + "'" + ' AND g."ripsEnvio_id" IS NULL AND i."tipoDoc_id" = u."tipoDoc_id" AND i.documento_id = u.id AND i.consec = f."consecAdmision" and g."totalGlosa" >0'
        detalle = 'SELECT glosas.id,  ' + "' '" + ' factura, glosas.id glosa_id, glosas."fechaRecepcion" fechaFactura, u.nombre paciente , gloDet."valorAceptado" totalFactura,' + "' '" + ' estado  FROM cartera_glosas glosas , facturacion_facturacion f , admisiones_ingresos i, usuarios_usuarios u  , cartera_glosasdetalle gloDet 	WHERE gloDet."glosa_id" = glosas.id AND  gloDet.factura_id = f.id AND i."tipoDoc_id" = f."tipoDoc_id" AND i.documento_id = f.documento_id AND i.consec = f."consecAdmision"  AND glosas."ripsEnvio_id" IS NULL AND i."tipoDoc_id" = u."tipoDoc_id" AND 	i.documento_id = u.id  and glosas."totalAceptado" >0'

    if (tipoRips == 'Nota Credito'):
        
	    detalle = 'SELECT nc.id,  ' + "' '" +  ' factura, nc.id glosa_id, nc."fechaNota" fechaFactura, u.nombre paciente , ncDet."valorNota" totalFactura,' + "' '" + ' estado  FROM cartera_notascredito nc , facturacion_facturacion f , admisiones_ingresos i, usuarios_usuarios u  , cartera_notascreditodetalle ncDet 	WHERE ncDet."notaCredito_id" = nc.id AND  ncDet.factura_id = f.id AND i."tipoDoc_id" = f."tipoDoc_id" AND i.documento_id = f.documento_id AND i.consec = f."consecAdmision"  AND nc."ripsEnvio_id" IS NULL AND i."tipoDoc_id" = u."tipoDoc_id" AND 	i.documento_id = u.id  and nc."valorNota" >0'

    print("DETALLE DE RIPSADICIONAR = ", detalle)

    curx.execute(detalle)

    for id,  factura, glosaId, fechaFactura, paciente,totalFactura,estado in curx.fetchall():
        detalleRipsAdicion.append(
            {"model": "facturacion_facturacion", "pk": id, "fields":
                {'id': id, 'factura': factura ,'glosaId': glosaId,  'fechaFactura': fechaFactura, 'paciente': paciente, 'totalFactura':totalFactura, 'estado':estado
                }})

    miConexionx.close()
    print("detalleRipsAdicion "  , detalleRipsAdicion)
    context['DetalleRipsAdicion'] = detalleRipsAdicion

    serialized1 = json.dumps(detalleRipsAdicion, default=str)
    #serialized1 = json.dumps(detalleRipsAdicion)

    return HttpResponse(serialized1, content_type='application/json')




def ActualizarEmpresaDetalleRips(request):

    print ("Entre ActualzaEmpresaDetalleRips" )

    envioRipsId = request.POST['envioRipsId']
    print("envioRipsId =", envioRipsId)

    empresaId = request.POST['empresaId']
    print("empresaId =", empresaId)

    username_id = request.POST['username_id']
    print("username_id =", username_id)

    facturaId = request.POST['facturaId']
    print("facturaId =", facturaId)

    glosaId = request.POST['glosaId']
    print("glosaId =", glosaId)

    notaCreditoId = request.POST['notaCreditoId']
    print("notaCreditoId =", notaCreditoId)

    tipoRips = request.POST['tipoRips']
    print("tipoRips =", tipoRips)

    fechaRegistro = datetime.datetime.now()
    estadoReg = 'A'



    miConexion3 = None
    try:

            #Primero el UPDATE

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()

            if (tipoRips == 'Factura'):

                comando = 'UPDATE facturacion_facturacion SET "ripsEnvio_id" = ' + "'" + str(envioRipsId) + "'" + ' WHERE id =  ' + "'" + str(facturaId) + "'"

            if (tipoRips == 'Nota Credito'):

                comando = 'UPDATE cartera_notascredito SET "ripsEnvio_id" = ' + "'" + str(envioRipsId) + "'" + ' WHERE id =  ' + "'" + str(glosaId) + "'"

            if (tipoRips == 'Nota Debito'):
                pass

            if (tipoRips == 'Glosa'):

                comando = 'UPDATE cartera_glosas SET "ripsEnvio_id" = ' + "'" + str(envioRipsId) + "'" + ' WHERE id =  ' + "'" + str(glosaId) + "'"

            print(comando)
            cur3.execute(comando)

            # Segundo eL INSERT A detalleRips

            empresa = []

            if (tipoRips == 'Factura'):

                comando1 = 'INSERT INTO RIPS_RIPSDETALLE ("numeroFactura_id", "estadoPasoMinisterio", "fechaRegistro", "estadoReg", "ripsEnvios_id", "usuarioRegistro_id", estado) VALUES (' +  "'" + str(facturaId) + "','N'," + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "',"  +  "'" + str(envioRipsId) + "'," +  "'" +str(username_id) + "'," + "'" + str('ELABORADA') + "')"

            if (tipoRips == 'Glosa'):

                #comando1 = 'INSERT INTO RIPS_RIPSDETALLE ("numeroFactura_id",glosa_id, "estadoPasoMinisterio", "fechaRegistro", "estadoReg", "ripsEnvios_id", "usuarioRegistro_id", estado) VALUES (' + "'" + str(facturaId)  + "','" + str(glosaId) + "','N'," + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(envioRipsId) + "'," + "'" + str(username_id) + "'," + "'" + str('ELABORADA') + "')"
                comando1 = 'INSERT INTO RIPS_RIPSDETALLE ("numeroFactura_id","glosa_id", "estadoPasoMinisterio", "fechaRegistro", "estadoReg",	"ripsEnvios_id", "usuarioRegistro_id", estado) select gloDet.factura_id, gloDet."glosa_id",' + "'" + str('N') + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(envioRipsId) + "'," + "'" + str(username_id) + "'," + "'" + str('ELABORADA') + "'" + ' FROM cartera_glosasdetalle gloDet where gloDet."glosa_id"=' + "'" + str(glosaId) + "'"


            if (tipoRips == 'Nota Credito'):

                #comando1 = 'INSERT INTO RIPS_RIPSDETALLE ("notaCredito_id", "estadoPasoMinisterio", "fechaRegistro", "estadoReg", "ripsEnvios_id", "usuarioRegistro_id", estado) VALUES (' + "'" + str(glosaId)  + "','N'," + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(envioRipsId) + "'," + "'" + str(username_id) + "'," + "'" + str('ELABORADA') + "')"
                comando1 = 'INSERT INTO RIPS_RIPSDETALLE ("numeroFactura_id","notaCredito_id", "estadoPasoMinisterio", "fechaRegistro", "estadoReg",	"ripsEnvios_id", "usuarioRegistro_id", estado) select ncDet.factura_id, ncDet."notaCredito_id",' + "'" + str('N') + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(envioRipsId) + "'," + "'" + str(username_id) + "'," + "'" + str('ELABORADA') + "'" + ' FROM cartera_notascreditodetalle ncDet where ncDet."notaCredito_id"=' + "'" + str(notaCreditoId) + "'"

            print(comando)
            cur3.execute(comando1)
            miConexion3.commit()
            cur3.close()
            miConexion3.close()


            return JsonResponse({'success': True, 'Mensajes': 'Factura Adicionada al Envio satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()

def TraeDetalleRips(request):
    print("Entre a TraerDetalleRips")

    detalleRipsId = request.POST['detalleRipsId']
    print("detalleRipsId =", detalleRipsId)

    context = {}

    enviarDetalleRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()
    
    detalle = 'SELECT d.id, d.cuv, d."numeroFactura_id" numeroFactura, d."rutaJsonRespuesta", d."rutaJsonFactura" , d."fechaRegistro", d."ripsEnvios_id", d."usuarioRegistro_id", d.estado, d."rutaPdf", d."rutaZip"  FROM public.rips_ripsdetalle d WHERE  id = ' + "'" + str(detalleRipsId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, cuv, numeroFactura, rutaJsonRespuesta, rutaJsonFactura,fechaRegistro,ripsEnvios_id, usuarioRegistro_id, estado, rutaPdf, rutaZip in curx.fetchall():
        enviarDetalleRips.append(
            {"model": "facturacion_facturacion", "pk": id, "fields":
                {'id': id, 'cuv':cuv ,'numeroFactura': numeroFactura , 'rutaJsonRespuesta': rutaJsonRespuesta, 'rutaJsonFactura': rutaJsonFactura, 'fechaRegistro':fechaRegistro,
                 'ripsEnvios_id':ripsEnvios_id, 'estado':estado, 'rutaPdf':rutaPdf, 'rutaZip':rutaZip
                }})

    miConexionx.close()
    print("enviarDetalleRips "  , enviarDetalleRips)
    context['EnviarDetalleRips'] = enviarDetalleRips

    serialized1 = json.dumps(enviarDetalleRips, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def GenerarJsonRips(request):
    print("Entre a GenerarJsonRips")

    envioRipsId = request.POST['envioRipsId']
    print("envioRipsId =", envioRipsId)

    sede = request.POST["sede"]
    print("sede =", sede)

    username_id = request.POST['username_id']
    print("username_id =", username_id)

    tipoRips = request.POST['tipoRips']
    print("tipoRips =", tipoRips)

    fechaRegistro = timezone.now()
    print("fechaRegistro = ", fechaRegistro)

    #Rutinas subir a tablas de rips todos la INFO MINISTERIO JSON RIPS

    # Verificar si esta enviada con lo cual no generaria nuevos rips

    enviadoRips = RipsEnvios.objects.get(id=envioRipsId)
    print ("enviadoRips = ", enviadoRips.ripsEstados)

    if (tipoRips == 'Factura'):


        detalleRips= RipsDetalle.objects.filter(ripsEnvios_id =envioRipsId  , glosa_id__isnull=False).count()

        print("detalleRips = ", detalleRips)
        if (detalleRips >= 1):

            return JsonResponse({'success': True, 'Mensajes': 'No es posible generar RIPS con glosas Activas. Favor cancelar las glosas!'})


    if (enviadoRips.ripsEstados =='1'):

	    return JsonResponse({'success': True, 'Mensajes': 'No es posible generar RIPS enviados!'})

    miConexionx = None
    try:

            miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            curx = miConexionx.cursor()

            # Primero Borra RIPS USUARIOS


            detalle =  'DELETE from rips_ripsusuarios u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(envioRipsId) +"');"
            resultado = curx.execute(detalle)
            print ("BORRO USUARIOS ", detalle)



            # Primero Borra RIPS consultas

            detalle1 = 'DELETE from rips_ripsconsultas u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(envioRipsId) + "')"
            resultado = curx.execute(detalle1)
            print("BORRO consultas ", detalle1)

            # Primero Borra RIPS otros servicios

            detalle1 = 'DELETE from rips_ripsotrosservicios u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(envioRipsId) + "')"
            resultado = curx.execute(detalle1)
            print("BORRO otrosservicios ", detalle1)


            # Primero Borra RIPS procedimientos

            detalle1 = 'DELETE from rips_ripsprocedimientos u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(envioRipsId) + "')"
            resultado = curx.execute(detalle1)
            print("BORRO procedimientos ", detalle1)



            # Primero Borra RIPS Medicamentos

            detalle2 = 'DELETE from rips_ripsmedicamentos u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(envioRipsId) + "')"
            resultado = curx.execute(detalle2)
            print("BORRO Medicamentos ", detalle2)
            # Primero Borra RIPS HOSPITALIZACION



            detalle3 = 'DELETE from rips_ripshospitalizacion u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(
                envioRipsId) + "')"
            resultado = curx.execute(detalle3)
            print("BORRO HOSPITALIZACION ", detalle3)

            # Primero Borra RIPS URGENCIAS

            detalle4 = 'DELETE from rips_ripsurgenciasobservacion u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(
                envioRipsId) + "')"
            resultado = curx.execute(detalle4)
            print("BORRO URGENCIAS ", detalle4)

            # Primero Borra RIPS RECIEN NACIDO

            detalle5 = 'DELETE from rips_ripsreciennacido u where u."ripsTransaccion_id" in (select id from rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = ' + "'" + str(
                envioRipsId) + "')"
            resultado = curx.execute(detalle5)
            print("BORRO RECIEN NACIDO ", detalle5)

            # Primero Borra RIPS TRANSACCION

            detalle6 = 'DELETE from rips_ripstransaccion u where u."ripsEnvio_id" = ' + "'" + str(envioRipsId) + "'"
            resultado = curx.execute(detalle6)
            print("BORRO tx ", detalle6)


            miConexionx.commit()
            curx.close()
            miConexionx.close()

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexionx:
            print("Entro ha hacer el Rollback")
            miConexionx.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})
    finally:
        if miConexionx:
            curx.close()
            miConexionx.close()

    ## Aqui big Modificacion, pues tine que crear todos los rips de todas las facturas del Envio

    ## Aqui consigo la cantidad de Facturas del Envio 

    barridoFacturas = []

    miConexionx = None
    try:

            miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curx = miConexionx.cursor()

            if (tipoRips == 'Factura'):

                detalle =  'SELECT id, "numeroFactura_id" item , "numeroFactura_id" itemOtro from rips_ripsdetalle det where det."ripsEnvios_id"  = ' + "'" + str(envioRipsId) +"'"
                curx.execute(detalle)

                for id, item, itemOtro in curx.fetchall():
                    barridoFacturas.append({'id':id, 'item': item,'itemOtro':itemOtro })


            if (tipoRips == 'Glosa'):


                #detalle =  'SELECT id, glosa_id item , "numeroFactura_id" itemOtro from rips_ripsdetalle det where det."ripsEnvios_id"  = ' + "'" + str(envioRipsId) +"'"
                detalle = 'SELECT det.id, det."glosa_id" item , gloDet.factura_id itemOtro from rips_ripsdetalle det left join cartera_glosas glosas on (glosas."ripsEnvio_id" =det."ripsEnvios_id" and glosas.id =det."glosa_id" ) left join cartera_glosasdetalle gloDet on (gloDet."glosa_id" =glosas.id  and gloDet.factura_id = det."numeroFactura_id") where det."ripsEnvios_id"  = ' + "'" + str(envioRipsId) + "'"

                curx.execute(detalle)

                for id, item, itemOtro in curx.fetchall():
                    barridoFacturas.append({'id':id, 'item': item ,'itemOtro':itemOtro})


            if (tipoRips == 'Nota Credito'):


                detalle = 'SELECT det.id, det."notaCredito_id" item , ncDet.factura_id itemOtro from rips_ripsdetalle det left join cartera_notascredito nc on (nc."ripsEnvio_id" =det."ripsEnvios_id" and nc.id =det."notaCredito_id" ) left join cartera_notascreditodetalle ncDet on (ncDet."notaCredito_id" =nc.id  and ncDet.factura_id = det."numeroFactura_id") where det."ripsEnvios_id"  = ' + "'" + str(envioRipsId) + "'"
                curx.execute(detalle)

                for id, item, itemOtro in curx.fetchall():
                    barridoFacturas.append({'id':id, 'item': item ,'itemOtro':itemOtro})

            print ("detalle = ", detalle)

            # INICIO BARRIDO DE FOR

            print ("barridoFacturas = " , barridoFacturas)

            for elementox in barridoFacturas:
                print ("elementox =" , elementox)
                print("elementox = " , elementox['item'])
                elemento = elementox['item']
                print("elemento = ", elemento)
                elementoOtro = elementox['itemOtro']
                traigoConsecutivo=1


                ### RIPS TRANSACCION
                #

                if (tipoRips == 'Factura'):

                    facturaId = Facturacion.objects.get(id=elemento)

                    ingresoId = Ingresos.objects.get(tipoDoc_id=facturaId.tipoDoc_id, documento_id=facturaId.documento_id,consec=facturaId.consecAdmision)
                    print ("ingreso = ",ingresoId.id)

                    detalle = 'INSERT into rips_ripstransaccion ("numDocumentoIdObligado","numFactura",  "numNota","fechaRegistro", "tipoNota_id","usuarioRegistro_id"  , "ripsEnvio_id", "sedesClinica_id" ,"estadoReg") select substring(sed.nit,1,9) , fac.id, 0, now(), null ' + ",'" +str(username_id) +"'"  + ', e.id, sed.id , ' + "'" + str('A') + "'" + '   from sitios_sedesclinica sed, facturacion_facturacion fac, rips_ripsEnvios e  , cartera_tiposnotas tipnot where e.id = ' + "'" + str(envioRipsId) +"'" +  ' and e."sedesClinica_id" = sed.id and fac."ripsEnvio_id" = e.id  AND tipnot.nombre = ' + "'" + str('Factura') + "' AND fac.id = " + "'" + str(elemento) + "' RETURNING id ;"

                    resultado = curx.execute(detalle)
                    transaccionId= curx.fetchone()[0]
                    print ("transaccionId = ", transaccionId)

                if (tipoRips == 'Glosa'):


                    facturaId = Facturacion.objects.get(id=elementoOtro)
                    ingresoId = Ingresos.objects.get(tipoDoc_id=facturaId.tipoDoc_id, documento_id=facturaId.documento_id,consec=facturaId.consecAdmision)

                    #detalle = 'INSERT into rips_ripstransaccion ("numDocumentoIdObligado",  "numNota","fechaRegistro", "tipoNota_id","usuarioRegistro_id" ,"ripsEnvio_id","sedesClinica_id" ,"numFactura" ,"estadoReg") select substring(sed.nit,1,9) ,  glo.id, now(), tipnot.id, ' + "'" + str(username_id) + "'" + ', e.id, sed.id , glo.factura_id , ' + "'" + str('A') + "'" + ' from sitios_sedesclinica sed, cartera_glosas glo, rips_ripsEnvios e  , rips_ripsdetalle det ,rips_ripstiposnotas tipnot where e.id = ' + "'" + str(envioRipsId) + "'" + ' and e."sedesClinica_id" = sed.id and glo."ripsEnvio_id" = e.id and det."ripsEnvios_id" = e.id and e."ripsTiposNotas_id" = tipnot.id and tipnot.nombre=' + "'" + str('Glosa') + "' AND glo.id = " + "'" + str(elemento) + "' and glo.id = det.glosa_id  RETURNING id ;"
                    detalle =  'INSERT into rips_ripstransaccion ("numDocumentoIdObligado",  "numNota","fechaRegistro", "tipoNota_id","usuarioRegistro_id" ,"ripsEnvio_id","sedesClinica_id" ,"numFactura" ,"estadoReg") select substring(sed.nit,1,9) ,  glosas.id, now(), tipnot.id,' + "'" + str(username_id) + "'" + ' , e.id, sed.id , gloDet.factura_id ,' + "'" + str('A') + "'" + ' from sitios_sedesclinica sed, cartera_glosas glosas, cartera_glosasdetalle gloDet, rips_ripsEnvios e  , rips_ripsdetalle det ,rips_ripstiposnotas tipnot where e.id = ' + "'" + str(envioRipsId) + "'" + ' and e."sedesClinica_id" = sed.id and glosas."ripsEnvio_id" = e.id and det."ripsEnvios_id" = e.id and e."ripsTiposNotas_id" = tipnot.id and tipnot.nombre=' + "'" + str('Glosa') + "'" + ' AND gloDet.factura_id = ' + "'" + str(elementoOtro) + "'"  + ' and glosas.id = gloDet."glosa_id" and det."glosa_id" = glosas.id and det."numeroFactura_id" = gloDet.factura_id RETURNING id ;'

                    print ("detalle = ", detalle)
                    resultado = curx.execute(detalle)
                    transaccionId = curx.fetchone()[0]
                    print ("transaccionId = ", transaccionId)


                if (tipoRips == 'Nota Credito'):


                    facturaId = Facturacion.objects.get(id=elementoOtro)
                    ingresoId = Ingresos.objects.get(tipoDoc_id=facturaId.tipoDoc_id, documento_id=facturaId.documento_id,consec=facturaId.consecAdmision)


                    detalle = 'INSERT into rips_ripstransaccion ("numDocumentoIdObligado",  "numNota","fechaRegistro", "tipoNota_id","usuarioRegistro_id" ,"ripsEnvio_id","sedesClinica_id" ,"numFactura" ,"estadoReg") select substring(sed.nit,1,9) ,  nc.id, now(), tipnot.id,' + "'" + str(username_id) + "'" + ' , e.id, sed.id , ncDet.factura_id ,' + "'" + str('A') + "'" + ' from sitios_sedesclinica sed, cartera_notascredito nc, cartera_notascreditodetalle ncDet, rips_ripsEnvios e  , rips_ripsdetalle det ,rips_ripstiposnotas tipnot where e.id = ' + "'" + str(envioRipsId) + "'" + ' and e."sedesClinica_id" = sed.id and nc."ripsEnvio_id" = e.id and det."ripsEnvios_id" = e.id and e."ripsTiposNotas_id" = tipnot.id and tipnot.nombre=' + "'" + str('Nota Credito') + "'" + ' AND ncDet.factura_id = ' + "'" + str(elementoOtro) + "'"  + ' and nc.id = ncDet."notaCredito_id" and det."notaCredito_id" = nc.id and det."numeroFactura_id" = ncDet.factura_id RETURNING id ;'

                    print ("detalle = ", detalle)
                    resultado = curx.execute(detalle)
                    transaccionId = curx.fetchone()[0]
                    print ("transaccionId = ", transaccionId)




                print ("detalle = " , detalle)

                print ("transaccionId = " , transaccionId )

                # RIPS USUARIOS

                ## OJO FALTA CREAR LA RUTINA SI TIENE O NO INCAPACIDAD
                ## HACER UN QUERY POR APARTE
                #

                if (tipoRips == 'Factura'):

                    detalle ='INSERT INTO rips_ripsusuarios ("tipoDocumentoIdentificacion", "tipoUsuario", "fechaNacimiento", "codSexo", "codZonaTerritorialResidencia_id", incapacidad, consecutivo, "fechaRegistro", "codMunicipioResidencia_id", "codPaisOrigen_id", "codPaisResidencia_id", "usuarioRegistro_id", "numDocumentoIdentificacion", "ripsDetalle_id", "ripsTransaccion_id","estadoReg", ingreso_id) SELECT tipdoc."tipoDocRips_id", tipousu.codigo, cast(u."fechaNacio" as date) , u.genero,u."ripsZonaTerritorial_id",   (select i.incapacidad from admisiones_ingresos i WHERE i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id=fac.documento_id and i.consec=fac."consecAdmision")      , row_number() OVER(ORDER BY det.id) AS consecutivo, now(), muni.id,  case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, ' + "'" + str(username_id) + "'" + ',u.documento, det.id, ' + "'" + str(transaccionId) + "','A'," + "'" + str(ingresoId.id) + "'" + 'from rips_ripsenvios e	inner join rips_ripsdetalle det on (det."ripsEnvios_id"  = e.id)  inner join  facturacion_facturacion fac on (fac.id = det."numeroFactura_id" ) inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id"  and i.documento_id = fac.documento_id  and i.consec = fac."consecAdmision") inner join usuarios_tiposdocumento tipdoc on ( tipdoc.id=i."tipoDoc_id" )  inner join usuarios_usuarios u on (u."tipoDoc_id"=i."tipoDoc_id" and u.id = i.documento_id) left join sitios_paises  pais on (pais.id= u.pais_id)  left join sitios_municipios muni on ( muni.id = u.municipio_id) left join rips_ripstipousuario tipousu on (tipousu.id = i."ripsTipoUsuario_id") where  e.id= ' + "'" + str(envioRipsId) + "'" + ' AND det."numeroFactura_id"  = ' + "'" + str(elemento) + "'"

                if (tipoRips == 'Glosa'):

                    #detalle  = 'INSERT INTO rips_ripsusuarios ("tipoDocumentoIdentificacion", "tipoUsuario", "fechaNacimiento", "codSexo", "codZonaTerritorialResidencia_id", incapacidad, consecutivo, "fechaRegistro", "codMunicipioResidencia_id", "codPaisOrigen_id", "codPaisResidencia_id", "usuarioRegistro_id", "numDocumentoIdentificacion", "ripsDetalle_id", "ripsTransaccion_id","estadoReg", ingreso_id) SELECT tipdoc."tipoDocRips_id", tipousu.codigo, cast(u."fechaNacio" as date) , u.genero,u."ripsZonaTerritorial_id",   (select i.incapacidad from admisiones_ingresos i WHERE i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id=fac.documento_id and i.consec=fac."consecAdmision")      , row_number() OVER(ORDER BY det.id) AS consecutivo, now(), muni.id,  case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, ' + "'" + str(username_id) + "'" + ',u.documento, det.id, ' + "'" + str(transaccionId) + "','A'," + "'" + str(ingresoId.id) + "'" + 'from rips_ripsenvios e	inner join rips_ripsdetalle det on (det."ripsEnvios_id"  = e.id)  inner join  facturacion_facturacion fac on (fac.id = det."numeroFactura_id" ) inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id"  and i.documento_id = fac.documento_id  and i.consec = fac."consecAdmision") inner join usuarios_tiposdocumento tipdoc on ( tipdoc.id=i."tipoDoc_id" )  inner join usuarios_usuarios u on (u."tipoDoc_id"=i."tipoDoc_id" and u.id = i.documento_id) left join sitios_paises  pais on (pais.id= u.pais_id)  left join sitios_municipios muni on ( muni.id = u.municipio_id) left join rips_ripstipousuario tipousu on (tipousu.id = i."ripsTipoUsuario_id") where  e.id= ' + "'" + str(envioRipsId) + "'" + ' AND det.glosa_id = ' + "'" + str(elemento) + "'"
                    detalle  = 'INSERT INTO rips_ripsusuarios ("tipoDocumentoIdentificacion", "tipoUsuario", "fechaNacimiento", "codSexo", "codZonaTerritorialResidencia_id", incapacidad, consecutivo, "fechaRegistro", "codMunicipioResidencia_id", "codPaisOrigen_id", "codPaisResidencia_id", "usuarioRegistro_id", "numDocumentoIdentificacion", "ripsDetalle_id", "ripsTransaccion_id","estadoReg", ingreso_id) SELECT tipdoc."tipoDocRips_id", tipousu.codigo, cast(u."fechaNacio" as date) , u.genero,u."ripsZonaTerritorial_id",   (select i.incapacidad from admisiones_ingresos i WHERE i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id=fac.documento_id and i.consec=fac."consecAdmision")      , row_number() OVER(ORDER BY det.id) AS consecutivo, now(), muni.id,  case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, ' + "'" + str(username_id) + "'" + ',u.documento, det.id, ' + "'" + str(transaccionId) + "','A'," + "'" + str(ingresoId.id) + "'" + 'from rips_ripsenvios e	inner join rips_ripsdetalle det on (det."ripsEnvios_id"  = e.id)  inner join  facturacion_facturacion fac on (fac.id = det."numeroFactura_id" and fac.id = ' + "'" + str(elementoOtro) + "'" + ') inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id"  and i.documento_id = fac.documento_id  and i.consec = fac."consecAdmision") inner join usuarios_tiposdocumento tipdoc on ( tipdoc.id=i."tipoDoc_id" )  inner join usuarios_usuarios u on (u."tipoDoc_id"=i."tipoDoc_id" and u.id = i.documento_id) left join sitios_paises  pais on (pais.id= u.pais_id)  left join sitios_municipios muni on ( muni.id = u.municipio_id) left join rips_ripstipousuario tipousu on (tipousu.id = i."ripsTipoUsuario_id") where  e.id= ' + "'" + str(envioRipsId) + "'" + ' AND det."glosa_id" = ' + "'" + str(elemento) + "'"



                if (tipoRips == 'Nota Credito'):

                    detalle  = 'INSERT INTO rips_ripsusuarios ("tipoDocumentoIdentificacion", "tipoUsuario", "fechaNacimiento", "codSexo", "codZonaTerritorialResidencia_id", incapacidad, consecutivo, "fechaRegistro", "codMunicipioResidencia_id", "codPaisOrigen_id", "codPaisResidencia_id", "usuarioRegistro_id", "numDocumentoIdentificacion", "ripsDetalle_id", "ripsTransaccion_id","estadoReg", ingreso_id) SELECT tipdoc."tipoDocRips_id", tipousu.codigo, cast(u."fechaNacio" as date) , u.genero,u."ripsZonaTerritorial_id",   (select i.incapacidad from admisiones_ingresos i WHERE i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id=fac.documento_id and i.consec=fac."consecAdmision")      , row_number() OVER(ORDER BY det.id) AS consecutivo, now(), muni.id,  case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, case when pais.id is null then ' + "'" + str('1') + "'" + ' else pais.id end, ' + "'" + str(username_id) + "'" + ',u.documento, det.id, ' + "'" + str(transaccionId) + "','A'," + "'" + str(ingresoId.id) + "'" + 'from rips_ripsenvios e	inner join rips_ripsdetalle det on (det."ripsEnvios_id"  = e.id)  inner join  facturacion_facturacion fac on (fac.id = det."numeroFactura_id" and fac.id = ' + "'" + str(elementoOtro) + "'" + ') inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id"  and i.documento_id = fac.documento_id  and i.consec = fac."consecAdmision") inner join usuarios_tiposdocumento tipdoc on ( tipdoc.id=i."tipoDoc_id" )  inner join usuarios_usuarios u on (u."tipoDoc_id"=i."tipoDoc_id" and u.id = i.documento_id) left join sitios_paises  pais on (pais.id= u.pais_id)  left join sitios_municipios muni on ( muni.id = u.municipio_id) left join rips_ripstipousuario tipousu on (tipousu.id = i."ripsTipoUsuario_id") where  e.id= ' + "'" + str(envioRipsId) + "'" + ' AND det."notaCredito_id" = ' + "'" + str(elemento) + "'"


                print ("detalle = ", detalle)
                curx.execute(detalle)

            # Busca cantidad de Medicamentos +  Suministros para proratear en ABONOS elemento= factura , elementoOtro=glosa


                try:
                    with transaction.atomic():

                        codigoModeradora = FormasPagos.objects.get(nombre='CUOTA MODERADORA')

                        categorias = ['N','R']
                        categoriasPagos = ['CUOTA MODERADORA', 'COPAGO']
                        print("tipoRipsA =" , tipoRips)


                        if (tipoRips == 'Factura'):
                            print("Entre FACTURA =", tipoRips)
                            pagosFactura = PagosFacturas.objects.filter(facturaAplicada_id=elemento,anulado = 'N').aggregate(totalAb=Sum('valorAplicado'))
                            print("sumatoria de pagos =" ,pagosFactura['totalAb'])

                            datosFactura=Facturacion.objects.get(id=elemento)
                            datosIngreso = Ingresos.objects.get(tipoDoc_id = datosFactura.tipoDoc_id, documento_id=datosFactura.documento_id, consec=datosFactura.consecAdmision)

                            totalParaclinicos = FacturacionDetalle.objects.filter(facturacion_id = elemento).filter(Q(anulado='N') | Q(anulado='R')).count()
                            #totalAbonos = Pagos.objects.get(tipoDoc_id = datosFactura.tipoDoc_id, documento_id=datosFactura.documento_id, consec=datosFactura.consec, formasPago_id = codigoModeradora)
                            totalAbonos=pagosFactura['totalAb']
                            print("totalAbonos = ", totalAbonos)
                            if (totalAbonos==None):
                                totalAbonos=0

                            print("totalParaclinicos = ", totalParaclinicos)

                            if (totalParaclinicos != None):
                                proRata = totalAbonos/totalParaclinicos


                        if (tipoRips == 'Glosa'):
                            print("Entre GLOSA =", tipoRips)
                            pagosFactura = PagosFacturas.objects.filter(facturaAplicada_id=elementoOtro,anulado = 'N').aggregate(totalAb=Sum('valorAplicado'))
                            datosGlosa  = Glosas.objects.get(id=elemento)
                            datosFactura = Facturacion.objects.get(id=elementoOtro)
                            datosIngreso = Ingresos.objects.get(tipoDoc_id=datosFactura.tipoDoc_id, documento_id=datosFactura.documento_id, consec=datosFactura.consecAdmision)
                            totalParaclinicos = FacturacionDetalle.objects.filter(facturacion_id=elementoOtro).filter(Q(anulado='N') | Q(anulado='R')).count()
                            totalAbonos=pagosFactura['totalAb']
                            if (totalAbonos==None):
                                totalAbonos=0

                            print("totalParaclinicos = ", totalParaclinicos)

                            if (totalParaclinicos != None):

                                proRata = totalAbonos / totalParaclinicos


                        if (tipoRips == 'Nota Credito'):
                            print("Entre Nota Credito =", tipoRips)
                            pagosFactura = PagosFacturas.objects.filter(facturaAplicada_id=elementoOtro,anulado = 'N').aggregate(totalAb=Sum('valorAplicado'))
                            #datosNotaCredito  = NotasCreditoDetalle.objects.get(notaCredito_id=elemento, factura_id=elementoOtro)
                            datosFactura = Facturacion.objects.get(id=elementoOtro)
                            datosIngreso = Ingresos.objects.get(tipoDoc_id=datosFactura.tipoDoc_id, documento_id=datosFactura.documento_id, consec=datosFactura.consecAdmision)
                            totalParaclinicos = FacturacionDetalle.objects.filter(facturacion_id=elementoOtro).filter(Q(anulado='N') | Q(anulado='R')).count()
                            totalAbonos=pagosFactura['totalAb']
                            if (totalAbonos==None):
                                totalAbonos=0

                            print("totalParaclinicos = ", totalParaclinicos)

                            if (totalParaclinicos != None):

                                proRata = totalAbonos / totalParaclinicos


                except Exception as e:
                    # Aquí ya se hizo rollback automáticamente
                    print("Se hizo rollback por:", e)
                    proRata=0


                # RIPS PROCEDIMIENTOS
                #

                aplicoAbono = 'NO'

                if (tipoRips == 'Factura'):

                    detalle = ' INSERT INTO rips_ripsprocedimientos ("codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "vrServicio",	"valorPagoModerador", "numFEVPagoModerador", consecutivo, "fechaRegistro", "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id", "tipoDocumentoIdentificacion_id","usuarioRegistro_id", "viaIngresoServicioSalud_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", "tipoPagoModerador_id", "ripsTransaccion_id", "estadoReg" , ingreso_id)  SELECT sed."codigoHabilitacion", facdet."fecha", facdet.mipres mipres, facdet."autorizacionDetalle_id" numeroAutorizacion,usu.documento,facdet."valorTotal",' +  str(proRata)  + ', fac.id, row_number() OVER(ORDER BY facdet.id) AS consecutivo, now(), null,diag1.id,diag2.id,	exa.id, serv.id, ' + str('5')  + ', 	final.id, gru.id, mod.id, tipdocrips.id, ' +  str(username_id) + ', ingreso.id, detrips.id, facdet."consecutivoFactura", ' +  str('4')  + ', (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora where  i."tipoDoc_id" =  pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),' + str(transaccionId) + ",'A','"  + str(ingresoId.id) + "'"  + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)  inner join  facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = ' + "'" + str('N')  + "'" +  ' or facdet.anulado = ' + "'" + str('R') + "')" + ' and ' + '"tipoRegistro" = ' + "'" + str('MANUAL') + "')" +  ' inner join clinico_examenes exa ON (exa.id = facdet."examen_id" )    inner  join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") left join rips_ripsviasingresosalud ingreso ON (ingreso.id = i."ripsViaIngresoServicioSalud_id") inner  join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) left join rips_ripsmodalidadatencion  mod ON (mod.id = i."ripsmodalidadGrupoServicioTecSal_id") left join rips_ripsgruposervicios gru ON (gru.id = i."ripsGrupoServicios_id")    left join rips_ripsServicios serv ON (serv.id = i."ripsGrupoServicios_id")  left join rips_ripsfinalidadconsulta final on (final.id = i."ripsFinalidadConsulta_id")  inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join clinico_diagnosticos diag1 on (diag1.id=i."dxActual_id") left join clinico_diagnosticos diag2 on (diag2.id= i."dxIngreso_id") left join autorizaciones_autorizaciones aut ON (aut.ingreso_id= i.id)	 left join autorizaciones_estadosautorizacion autEst on (autEst.nombre=' + "'" + str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autDet ON (autDet.autorizaciones_id= aut.id AND autDet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id" )	   where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "' and facdet.examen_id is not null"
                    print("detalle = ", detalle)
                    curx.execute(detalle)
                    print("transaccionId = ", transaccionId)

                    totalProced = []
                    detalle = 'SELECT count(*) totalProc FROM  rips_ripsprocedimientos where "ripsTransaccion_id"  =' + "'" + str(transaccionId) + "'"
                    curx.execute(detalle)

                    for totalProc  in curx.fetchall():
                        totalProced.append(
                            {'totalProc': totalProc})

                    print("totalProced =" , totalProced)
                    print("totalProced =", totalProced[0]['totalProc'])

                    totalProced = str(totalProced[0]['totalProc'])
                    totalProced = totalProced.replace("(", ' ')
                    totalProced = totalProced.replace(")", ' ')
                    totalProced = totalProced.replace(",", ' ')
                    traigoConsecutivo = totalProced

                    print("traigoConsecutivoId", traigoConsecutivo)

                    detalle1 = ' INSERT INTO rips_ripsprocedimientos ("codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "vrServicio",	"valorPagoModerador", "numFEVPagoModerador", consecutivo, "fechaRegistro", "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id", "tipoDocumentoIdentificacion_id","usuarioRegistro_id", "viaIngresoServicioSalud_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", "tipoPagoModerador_id", "ripsTransaccion_id", "estadoReg", ingreso_id )  SELECT sed."codigoHabilitacion", facdet."fecha", facdet.mipres, facdet."autorizacionDetalle_id", usu.documento, facdet."valorTotal", ' + str(proRata) + ', fac.id, row_number()  OVER(ORDER BY facdet.id) + ' + str(traigoConsecutivo) + ' AS consecutivo, now(), (select max(diag4.id) from clinico_diagnosticos diag4 where  diag4.id = i."dxComplicacion_id"), (select  max(diag1.id) from clinico_historia his ,clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1 where his."tipoDoc_id" = i."tipoDoc_id" AND his.documento_id = i.documento_id and his."consecAdmision" = i.consec AND histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('1') + "'" + '),(select  max(diag1.id) from clinico_historia his ,clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1 where his."tipoDoc_id" = i."tipoDoc_id" AND his.documento_id = i.documento_id and his."consecAdmision" = i.consec AND histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('2')  + "'" + '), exa.id, serv.id,' + str('5')  + '  , final.id, gru.id, mod.id, tipdocrips.id, ' + "'" + str(username_id) + "'" + ', ingreso.id, detrips.id, facdet."consecutivoFactura", ' + "'" + str('4') + "'" + ', (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), ' + "'" + str(transaccionId) + "','A','" + str(ingresoId.id) + "'"  + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') + "')" + ' and "tipoRegistro" = ' + "'" + str('SISTEMA') + "')" + ' inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") left join rips_ripsviasingresosalud ingreso ON (ingreso.id = i."ripsViaIngresoServicioSalud_id") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) left join rips_ripsmodalidadatencion mod ON (mod.id = i."ripsmodalidadGrupoServicioTecSal_id") left join  rips_ripsgruposervicios gru ON (gru.id = i."ripsGrupoServicios_id")    left join rips_ripsServicios serv ON (serv.id = i."ripsGrupoServicios_id")  left join  rips_ripsfinalidadconsulta final on (final.id = i."ripsFinalidadConsulta_id") inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id )   left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_estadosautorizacion autEst on (autEst.nombre='+ "'" + str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "' and facdet.examen_id is not null"
                    print("detalle = ", detalle1)
                    curx.execute(detalle1)


                    detalle2 ='UPDATE rips_ripsprocedimientos set "valorPagoModerador" = 0 WHERE "ripsTransaccion_id" = ' + "'" + str(transaccionId) + "'"
                    curx.execute(detalle2)


                    if (totalAbonos==None):
                        totalAbonos=0

                    detalle3 ='UPDATE rips_ripsprocedimientos set "valorPagoModerador" = ' + "'" + str(totalAbonos) + "'" + ' WHERE "ripsTransaccion_id" = ' + "'" + str(transaccionId) + "'" + ' AND consecutivo = 1'
                    curx.execute(detalle3)


                    aplicoAbono ='SI'


                if (tipoRips == 'Glosa'):

                    #detalle = 'INSERT INTO rips_ripsprocedimientos(glosa_id,"codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "vrServicio","valorPagoModerador", "numFEVPagoModerador", consecutivo, "fechaRegistro", "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id","tipoDocumentoIdentificacion_id","usuarioRegistro_id", "viaIngresoServicioSalud_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", "tipoPagoModerador_id", "ripsTransaccion_id", "estadoReg", ingreso_id , "motivoGlosa_id", "notasCreditoGlosa", "notasCreditoOtras","notasDebito","vAceptado","valorGlosado","valorSoportado") SELECT glosa.id, 	"codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "notasCreditoGlosa","valorPagoModerador", "numFEVPagoModerador", row_number() OVER(ORDER BY proc.id) AS consecutivo , ' + "'" + str(fechaRegistro) + "'" + ' , "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id","tipoDocumentoIdentificacion_id", ' + "'" + str(username_id) + "'" + ' , "viaIngresoServicioSalud_id",' + "'" + str(elementox['id']) + "'" + ', proc."itemFactura", proc."ripsTipos_id", 	proc."tipoPagoModerador_id",' + "'" +  str(transaccionId) + "'," + "'A'," + "'" + str(ingresoId.id) + "'" + ' , gloDet."motivoGlosa_id", gloDet."valorNotasCredito", gloDet."valorNotasCreditoOtras",gloDet."valorNotasDebito",gloDet."valorAceptado",gloDet."valorGlosa",gloDet."valorSoportado"  FROM rips_ripsProcedimientos proc inner join cartera_glosasdetalle gloDet on (gloDet."ripsProcedimientos_id" = proc.id) inner join cartera_glosas glosa on (glosa.id = gloDet.glosa_id and glosa.factura_id = cast(proc."numFEVPagoModerador"  as integer)) inner join rips_ripsdetalle det on (det."numeroFactura_id" =  cast(proc."numFEVPagoModerador"  as integer) and  det.glosa_id=glosa.id and det.glosa_id= ' + "'" + str(elemento) + "'" + ') where proc."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"

                    detalle = 'INSERT INTO rips_ripsprocedimientos("glosa_id","codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "vrServicio","valorPagoModerador", "numFEVPagoModerador", consecutivo, "fechaRegistro", "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id","tipoDocumentoIdentificacion_id","usuarioRegistro_id", "viaIngresoServicioSalud_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", "tipoPagoModerador_id", "ripsTransaccion_id", "estadoReg", ingreso_id , "notasCreditoOtras") SELECT glosas.id, "codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "vrServicio","valorPagoModerador", "numFEVPagoModerador", row_number() OVER(ORDER BY proc.id) AS consecutivo , ' + "'" + str(fechaRegistro) + "'" + ' , "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id","tipoDocumentoIdentificacion_id", ' + "'" + str(username_id) + "'" + ' , "viaIngresoServicioSalud_id",' + "'" + str(elementox['id']) + "'" + ', proc."itemFactura", proc."ripsTipos_id", 	proc."tipoPagoModerador_id",' + "'" +  str(transaccionId) + "'," + "'A'," + "'" + str(ingresoId.id) + "'," +  ' gloDetRips."valorAceptado" FROM rips_ripsProcedimientos proc inner join cartera_glosasdetallerips gloDetRips on (gloDetRips."ripsProcedimientos_id" = proc.id) inner join cartera_glosasDetalle gloDet on (gloDet.id =  gloDetRips."glosasDetalle_id") inner join cartera_glosas glosas on (glosas.id = gloDet."glosa_id") inner join rips_ripsdetalle det on (det."numeroFactura_id" =  gloDet.factura_id and  det."glosa_id" = ' + "'" + str(elemento) + "'" + ') where proc."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"

                    print("detalle PROCEDIMIENTOS= ", detalle)
                    curx.execute(detalle)

                if (tipoRips == 'Nota Credito'):

                    detalle = 'INSERT INTO rips_ripsprocedimientos("notaCredito_id","codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "vrServicio","valorPagoModerador", "numFEVPagoModerador", consecutivo, "fechaRegistro", "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id","tipoDocumentoIdentificacion_id","usuarioRegistro_id", "viaIngresoServicioSalud_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", "tipoPagoModerador_id", "ripsTransaccion_id", "estadoReg", ingreso_id , "notasCreditoOtras") SELECT nc.id, "codPrestador", "fechaInicioAtencion", "idMIPRES", "numAutorizacion","numDocumentoIdentificacion", "vrServicio","valorPagoModerador", "numFEVPagoModerador", row_number() OVER(ORDER BY proc.id) AS consecutivo , ' + "'" + str(fechaRegistro) + "'" + ' , "codComplicacion_id", "codDiagnosticoPrincipal_id","codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id",	"grupoServicios_id", "modalidadGrupoServicioTecSal_id","tipoDocumentoIdentificacion_id", ' + "'" + str(username_id) + "'" + ' , "viaIngresoServicioSalud_id",' + "'" + str(elementox['id']) + "'" + ', proc."itemFactura", proc."ripsTipos_id", 	proc."tipoPagoModerador_id",' + "'" +  str(transaccionId) + "'," + "'A'," + "'" + str(ingresoId.id) + "'," +  ' ncDetRips."valorNota" FROM rips_ripsProcedimientos proc inner join cartera_notascreditodetallerips ncDetRips on (ncDetRips."ripsProcedimientos_id" = proc.id) inner join cartera_notascreditoDetalle ncDet on (ncDet.id =  ncDetRips."notaCreditoDetalle_id") inner join cartera_notascredito nc on (nc.id = ncDet."notaCredito_id") inner join rips_ripsdetalle det on (det."numeroFactura_id" =  ncDet.factura_id and  det."notaCredito_id" = ' + "'" + str(elemento) + "'" + ') where proc."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"

                    print("detalle PROCEDIMIENTOS= ", detalle)
                    curx.execute(detalle)



                print (" Vamos parta hospitalizacion")

                # RIPS HOSPITALIZACION
                #

                if (tipoRips == 'Factura'):

                    detalle = 'INSERT INTO rips_ripshospitalizacion ("codPrestador","viaIngresoServicioSalud_id","fechaInicioAtencion", "numAutorizacion","causaMotivoAtencion_id","codComplicacion_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id",  "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id", "codDiagnosticoRelacionadoE3_id","condicionDestinoUsuarioEgreso_id", "codDiagnosticoCausaMuerte_id","fechaEgreso",  consecutivo, "usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", "ripsTransaccion_id",  "fechaRegistro", ingreso_id, "estadoReg")  SELECT sed."codigoHabilitacion",i."ripsViaIngresoServicioSalud_id",cast(i."fechaIngreso" as date), aut."numeroAutorizacion" , i."ripsCausaMotivoAtencion_id", (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxComplicacion_id"),(select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxIngreso_id"), (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxSalida_id"),     (select max(diag1.id)  from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1 , clinico_historia his where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('1') + "'" + ' and histdiag1.diagnosticos_id = diag1.id and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" = fac."consecAdmision") ,   (select max(diag1.id)  from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1, clinico_historia his  where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('2') + "'" + ' and histdiag1.diagnosticos_id = diag1.id  and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" =fac."consecAdmision"),  (select max(diag1.id) from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1, clinico_historia his where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('3') + "'" + ' and histdiag1.diagnosticos_id = diag1.id  and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" =fac."consecAdmision" ), i."ripsCondicionDestinoUsuarioEgreso_id", null,  cast(i."fechaSalida" as date), row_number() OVER(ORDER BY i.id) AS consecutivo ,' + "'" + str(username_id) + "'" + ' ,det.id,env."ripsEstados_id",  ripstra.id,now() ' + ",'" + str(ingresoId.id) + "','A'"  + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join admisiones_ingresos i ON (i."sedesClinica_id" = sed.id and i."tipoDoc_id" =fac."tipoDoc_id" and i.documento_id = fac.documento_id AND i.consec =fac."consecAdmision") inner join rips_ripsenvios env ON (env."sedesClinica_id" = sed.id) inner join rips_ripsdetalle det ON ( det."ripsEnvios_id" = env.id and  det."ripsEnvios_id" = fac."ripsEnvio_id" and cast(det."numeroFactura_id" as float) = fac.id )  inner join rips_ripstransaccion ripstra ON ( ripstra."sedesClinica_id" = sed.id and ripstra."ripsEnvio_id" = env.id and ripstra."numFactura" = cast(fac.id as text))  left join autorizaciones_autorizaciones aut  on (aut.id = i.autorizaciones_id) inner join 	clinico_servicios serv on (serv.nombre = ' + "'" + str('HOSPITALIZACION') +"')" + ' left join 	sitios_dependencias dep on (dep.id = i."dependenciasSalida_id" ) left join 	sitios_serviciossedes servsedes on (servsedes.id = dep."serviciosSedes_id" and servsedes.servicios_id= serv.id)    where sed.id = ' + "'" + str(sede) + "'" + ' AND env.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                if (tipoRips == 'Glosa'):

                    detalle = 'INSERT INTO rips_ripshospitalizacion ("codPrestador","viaIngresoServicioSalud_id","fechaInicioAtencion", "numAutorizacion","causaMotivoAtencion_id","codComplicacion_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id",  "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id", "codDiagnosticoRelacionadoE3_id","condicionDestinoUsuarioEgreso_id", "codDiagnosticoCausaMuerte_id","fechaEgreso",  consecutivo, "usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", "ripsTransaccion_id",  "fechaRegistro", ingreso_id, "estadoReg") SELECT  "codPrestador","viaIngresoServicioSalud_id","fechaInicioAtencion", "numAutorizacion","causaMotivoAtencion_id","codComplicacion_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id",  "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id", "codDiagnosticoRelacionadoE3_id","condicionDestinoUsuarioEgreso_id", "codDiagnosticoCausaMuerte_id","fechaEgreso",  consecutivo, ripshosp."usuarioRegistro_id",'  + "'" + str(elementox['id']) + "'" +  ' , "ripsTipos_id",' + "'" + str(transaccionId) + "'" + ',  ripshosp."fechaRegistro",' + "'" + str(ingresoId.id) + "','A'"  + ' FROM rips_ripshospitalizacion ripshosp, rips_ripsdetalle det , rips_ripstransaccion ripstra where  ripshosp."ripsTransaccion_id" = ripstra.id and ripshosp."ripsDetalle_id" = det.id and cast(ripstra."numFactura" as float) =  det."numeroFactura_id" and cast(ripstra."numFactura" as float) = ' + "'" + str(elementoOtro) + "' " + ' and cast(ripstra."numNota" as integer) = 0'


                if (tipoRips == 'Nota Credito'):

                    detalle = 'INSERT INTO rips_ripshospitalizacion ("codPrestador","viaIngresoServicioSalud_id","fechaInicioAtencion", "numAutorizacion","causaMotivoAtencion_id","codComplicacion_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id",  "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id", "codDiagnosticoRelacionadoE3_id","condicionDestinoUsuarioEgreso_id", "codDiagnosticoCausaMuerte_id","fechaEgreso",  consecutivo, "usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", "ripsTransaccion_id",  "fechaRegistro", ingreso_id, "estadoReg") SELECT  "codPrestador","viaIngresoServicioSalud_id","fechaInicioAtencion", "numAutorizacion","causaMotivoAtencion_id","codComplicacion_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id",  "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id", "codDiagnosticoRelacionadoE3_id","condicionDestinoUsuarioEgreso_id", "codDiagnosticoCausaMuerte_id","fechaEgreso",  consecutivo, ripshosp."usuarioRegistro_id",'  + "'" + str(elementox['id']) + "'" +  ' , "ripsTipos_id",' + "'" + str(transaccionId) + "'" + ',  ripshosp."fechaRegistro",' + "'" + str(ingresoId.id) + "','A'"  + ' FROM rips_ripshospitalizacion ripshosp, rips_ripsdetalle det , rips_ripstransaccion ripstra where  ripshosp."ripsTransaccion_id" = ripstra.id and ripshosp."ripsDetalle_id" = det.id and cast(ripstra."numFactura" as float) =  det."numeroFactura_id" and cast(ripstra."numFactura" as float) = ' + "'" + str(elementoOtro) + "' " + ' and cast(ripstra."numNota" as integer) = 0'


                print("detalle = ", detalle)
                curx.execute(detalle)



                # HASTA AQUI RIPS HOSPITALIZACION

                # RIPS URGENCIAS
                #

                if (tipoRips == 'Factura'):

                    detalle = 'INSERT INTO rips_ripsurgenciasobservacion ("codPrestador", "fechaInicioAtencion", "fechaEgreso", consecutivo, "fechaRegistro", "causaMotivoAtencion_id", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id", "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id","codDiagnosticoRelacionadoE3_id", "condicionDestinoUsuarioEgreso_id", "usuarioRegistro_id", "ripsDetalle_id",  "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id)  SELECT sed."codigoHabilitacion", cast(i."fechaIngreso" as date) ,cast(i."fechaSalida" as date), row_number() OVER(ORDER BY i.id) AS consecutivo  ,now() ,i."ripsCausaMotivoAtencion_id", (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxComplicacion_id"), (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxIngreso_id"), (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxSalida_id"), (select max(diag1.id)  from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1 , clinico_historia his where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('2') + "'" + ' and histdiag1.diagnosticos_id = diag1.id and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" = fac."consecAdmision") ,  (select max(diag1.id)  from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1, clinico_historia his  where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('3') + "'" + '  and histdiag1.diagnosticos_id = diag1.id  and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" =fac."consecAdmision"),  (select max(diag1.id) from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1, clinico_historia his where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('4') + "'" + ' and histdiag1.diagnosticos_id = diag1.id  and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" =fac."consecAdmision" ),i."ripsCondicionDestinoUsuarioEgreso_id", ' + "'" + str(username_id) + "'" + ' ,det.id,env."ripsEstados_id",  ripstra.id, ' "'" + str('A') + "','"  + str(ingresoId.id) + "'"  + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join admisiones_ingresos i ON (i."sedesClinica_id" = sed.id and i."tipoDoc_id" =fac."tipoDoc_id" and i.documento_id = fac.documento_id AND i.consec =fac."consecAdmision") inner join rips_ripsenvios env ON (env."sedesClinica_id" = sed.id) inner join rips_ripsdetalle det ON ( det."ripsEnvios_id" = env.id and  det."ripsEnvios_id" = fac."ripsEnvio_id" and det."numeroFactura_id" = fac.id ) inner join rips_ripstransaccion ripstra ON ( ripstra."sedesClinica_id" = sed.id and ripstra."ripsEnvio_id" = env.id and ripstra."numFactura" = cast(fac.id as text)) 	 left join autorizaciones_autorizaciones aut  on (aut.id = i.autorizaciones_id)  inner join 	clinico_servicios serv on (serv.nombre = ' + "'" + str('URGENCIAS') +"')" + ' inner join 	sitios_dependencias dep on (dep.id = i."dependenciasSalida_id" ) inner join 	sitios_serviciossedes servsedes on (servsedes.id = dep."serviciosSedes_id" and servsedes.servicios_id= serv.id)  where sed.id = ' + "'" + str(sede) + "'" + ' AND env.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                if (tipoRips == 'Glosa'):

                    detalle = 'INSERT INTO rips_ripsurgenciasobservacion ("codPrestador", "fechaInicioAtencion", "fechaEgreso", consecutivo, "fechaRegistro", "causaMotivoAtencion_id","codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id", "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id","codDiagnosticoRelacionadoE3_id", "condicionDestinoUsuarioEgreso_id", "usuarioRegistro_id", "ripsDetalle_id",  "ripsTipos_id", "ripsTransaccion_id", ingreso_id) SELECT "codPrestador", "fechaInicioAtencion", "fechaEgreso", consecutivo, ripsobs."fechaRegistro", "causaMotivoAtencion_id","codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id", "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id","codDiagnosticoRelacionadoE3_id", "condicionDestinoUsuarioEgreso_id", ripsobs."usuarioRegistro_id",' + "'" + str(elementox['id']) + "'" + ',  "ripsTipos_id",' + "'" + str(transaccionId) + "','"  + str(ingresoId.id) + "'"   + ' FROM  rips_ripsurgenciasobservacion ripsobs, rips_ripsdetalle det , rips_ripstransaccion ripstra where  ripstra."ripsEnvio_id" = det."ripsEnvios_id" and  ripsobs."ripsTransaccion_id" = ripstra.id and ripsobs."ripsDetalle_id" = det.id and cast(ripstra."numFactura" as float) =  det."numeroFactura_id" and  cast(ripstra."numFactura" as float) = ' + "'" + str(elementoOtro) + "'"

                if (tipoRips == 'Nota Credito'):

                    detalle = 'INSERT INTO rips_ripsurgenciasobservacion ("codPrestador", "fechaInicioAtencion", "fechaEgreso", consecutivo, "fechaRegistro", "causaMotivoAtencion_id","codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id", "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id","codDiagnosticoRelacionadoE3_id", "condicionDestinoUsuarioEgreso_id", "usuarioRegistro_id", "ripsDetalle_id",  "ripsTipos_id", "ripsTransaccion_id", ingreso_id) SELECT "codPrestador", "fechaInicioAtencion", "fechaEgreso", consecutivo, ripsobs."fechaRegistro", "causaMotivoAtencion_id","codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id", "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id","codDiagnosticoRelacionadoE3_id", "condicionDestinoUsuarioEgreso_id", ripsobs."usuarioRegistro_id",' + "'" + str(elementox['id']) + "'" + ',  "ripsTipos_id",' + "'" + str(transaccionId) + "','"  + str(ingresoId.id) + "'"   + ' FROM  rips_ripsurgenciasobservacion ripsobs, rips_ripsdetalle det , rips_ripstransaccion ripstra where  ripstra."ripsEnvio_id" = det."ripsEnvios_id" and  ripsobs."ripsTransaccion_id" = ripstra.id and ripsobs."ripsDetalle_id" = det.id and cast(ripstra."numFactura" as float) =  det."numeroFactura_id" and  cast(ripstra."numFactura" as float) = ' + "'" + str(elementoOtro) + "'" + ' and cast(ripstra."numNota" as integer) = 0'

                print("detalle = ", detalle)
                curx.execute(detalle)

                # HASTA AQUI RIPS URGENCIAS
                #

                # RIPS MEDICAMENTOS
                #
                tipoMedicamento = TiposSuministro.objects.get(nombre='MEDICAMENTOS')
                if (tipoRips == 'Factura'):

                    detalle = 'INSERT INTO rips_ripsmedicamentos ("codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", 	"diasTratamiento",	"numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",consecutivo, "fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id", "tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura","ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id ) SELECT sed."codigoHabilitacion", aut."numeroAutorizacion", null, facdet.fecha , null, histmed."concentracionMedicamento",histmed."cantidadOrdenada", histmed."diasTratamiento",planta.documento, facdet."valorUnitario", facdet."valorTotal", 0,  fac.id, row_number() OVER(ORDER BY histmed.id), now(), diag1.id, diag2.id, ripscums.id, (select min(ripsRecaudo.id) FROM cartera_pagos pagos INNER JOIN cartera_formaspagos carteraFormasPago ON (carteraFormasPago.id =pagos."formaPago_id" ) INNER JOIN rips_ripsconceptorecaudo ripsRecaudo ON (ripsRecaudo.id = cast(carteraFormasPago."codigoRips" as integer)) WHERE pagos.documento_id=fac.documento_id and pagos."tipoDoc_id" = fac."tipoDoc_id" and pagos.consec=fac."consecAdmision") recaudo, ripsfarma.id, ripstipdoc.id, tipmed.id, ripsumm.id, ripsupr.id, ' + "'" + str(username_id) + "'" + ' , det.id, facdet."consecutivoFactura",' + "'" + str('8') + "'" + ' , rips_ripstransaccion.id , '  + "'" + str('A') + "','" + str(ingresoId.id) + "'" + '  from rips_ripstransaccion inner join rips_ripsenvios env on(env."sedesClinica_id" = rips_ripstransaccion."sedesClinica_id" and env.id = rips_ripstransaccion."ripsEnvio_id" ) inner join sitios_sedesclinica sed on (sed.id = env."sedesClinica_id" ) inner join rips_ripsdetalle det on (det."ripsEnvios_id" = env.id and det."numeroFactura_id" = cast(rips_ripstransaccion."numFactura" as numeric)) inner join facturacion_facturacion fac on (fac.id = det."numeroFactura_id" ) inner join facturacion_facturaciondetalle facdet on (facdet."facturacion_id" = fac.id and facdet."cums_id" is not null and (facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') +"'" +  ')  AND facDet."tipoRegistro" = ' + "'" + str('SISTEMA') + "'" + ' ) inner join clinico_historiamedicamentos histmed on (histmed.id = facdet."historiaMedicamento_id") left join autorizaciones_autorizacionesDetalle  aut on (aut.id = histmed.autorizacion_id) inner join facturacion_suministros sum on (sum.id = facdet.cums_id)  inner join facturacion_tipossuministro tiposSum ON (tiposSum.id=sum."tipoSuministro_id" and tiposSum.nombre=' + "'" + str(tipoMedicamento.nombre) + "')" + '  left join rips_ripstipomedicamento tipmed on (tipmed.id = sum."ripsTipoMedicamento_id" ) inner join rips_ripscums ripscums  on (ripscums.cum = sum."cums") left join rips_ripsumm ripsumm on (ripsumm.id = sum."ripsUnidadMedida_id") left join rips_RipsFormaFarmaceutica ripsfarma on (ripsfarma.id = sum."ripsFormaFarmaceutica_id")  left join rips_ripsunidadupr ripsupr on (ripsupr.id = sum."ripsUnidadUpr_id") inner join clinico_historia historia on (historia.id = histmed.historia_id) inner join planta_planta planta on (planta.id = historia."usuarioRegistro_id") left join usuarios_tiposdocumento usutipdoc on (usutipdoc.id = planta."tipoDoc_id") left join rips_ripstiposdocumento ripstipdoc on (ripstipdoc.id = usutipdoc."tipoDocRips_id")  left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id = historia.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('1') + "')" + ' left join clinico_historialdiagnosticos histdiag2 on (histdiag2.historia_id = historia.id and histdiag2."tiposDiagnostico_id" = ' + "'" + str('2') + "')" + ' left join clinico_diagnosticos diag1 on (diag1.id = histdiag1.diagnosticos_id) left join clinico_diagnosticos diag2 on (diag2.id = histdiag2.diagnosticos_id) where env.id =  ' + "'" + str(envioRipsId) + "'" + ' and rips_ripstransaccion."ripsEnvio_id" = env.id  and cast(rips_ripstransaccion."numFactura" as numeric) = fac.id  and fac.id = ' + "'" + str(elemento) + "' AND facdet.cums_id is not null"
                    curx.execute(detalle)
                    print("detalle =", detalle)



                    totalMedica = []
                    detalle = 'SELECT count(*) totalMed FROM  rips_ripsmedicamentos where "ripsTransaccion_id"  =' + "'" + str(transaccionId) + "'"
                    curx.execute(detalle)

                    for totalMed  in curx.fetchall():
                        totalMedica.append(
                            {'totalMed': totalMed})

                    print("totalMedica =" , totalMedica)
                    print("totalMedica =", totalMedica[0]['totalMed'])

                    totalMedica = str(totalMedica[0]['totalMed'])
                    totalMedica = totalMedica.replace("(", ' ')
                    totalMedica = totalMedica.replace(")", ' ')
                    totalMedica = totalMedica.replace(",", ' ')
                    traigoConsecutivo = totalMedica

                    print("traigoConsecutivoId", traigoConsecutivo)

                    detalle1 = 'INSERT INTO rips_ripsmedicamentos ("codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", 	"diasTratamiento",	"numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio","valorPagoModerador", "numFEVPagoModerador",consecutivo, "fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id","codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id", "tipoMedicamento_id", "unidadMedida_id","unidadMinDispensa_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura","ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id ) SELECT sed."codigoHabilitacion", null, null, facdet.fecha,null,null ,null ,null ,planta.documento, facdet."valorUnitario",	facdet."valorTotal", 0,  fac.id, row_number() OVER(ORDER BY facdet.id)  + ' + str(traigoConsecutivo) + ' , now(),diag1.id , diag2.id, ripscums.id, (select min(ripsRecaudo.id)  FROM cartera_pagos pagos INNER JOIN cartera_formaspagos carteraFormasPago ON (carteraFormasPago.id =pagos."formaPago_id" ) INNER JOIN rips_ripsconceptorecaudo ripsRecaudo ON (ripsRecaudo.id = cast(carteraFormasPago."codigoRips" as integer)) 	WHERE pagos.documento_id=fac.documento_id and pagos."tipoDoc_id" = fac."tipoDoc_id" and pagos.consec=fac."consecAdmision") recaudo, ripsfarma.id, ripstipdoc.id, tipmed.id, ripsumm.id, ripsupr.id, ' + "'" + str(username_id) + "'" + ' , det.id, facdet."consecutivoFactura", ' + "'" + str('8') + "'" + ' , rips_ripstransaccion.id , ' + "'" + str('A') + "','" + str(ingresoId.id) + "'"  + ' from rips_ripstransaccion inner join rips_ripsenvios env on(env."sedesClinica_id" = rips_ripstransaccion."sedesClinica_id" and env.id = rips_ripstransaccion."ripsEnvio_id" ) inner join sitios_sedesclinica sed on (sed.id = env."sedesClinica_id") inner join rips_ripsdetalle det on (det."ripsEnvios_id" = env.id and det."numeroFactura_id" = cast(rips_ripstransaccion."numFactura" as numeric)) inner join facturacion_facturacion fac on (fac.id = det."numeroFactura_id") inner join facturacion_facturaciondetalle facdet on (facdet."facturacion_id" = fac.id and facdet."cums_id" is not null and (facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') + "')" + ' AND facDet."tipoRegistro" = ' + "'" + str('MANUAL') + "')" + ' inner join facturacion_suministros sum on (sum.id = facdet.cums_id) inner join facturacion_tipossuministro tiposSum ON (tiposSum.id=sum."tipoSuministro_id" and tiposSum.nombre=' + "'" + str(tipoMedicamento.nombre) + "')" + '   left join rips_ripstipomedicamento tipmed on (tipmed.id = sum."ripsTipoMedicamento_id" ) inner join rips_ripscums ripscums  on (ripscums.cum = sum."cums") left join rips_ripsumm ripsumm on (ripsumm.id = sum."ripsUnidadMedida_id") left join rips_RipsFormaFarmaceutica ripsfarma on (ripsfarma.id = sum."ripsFormaFarmaceutica_id") left join rips_ripsunidadupr ripsupr on (ripsupr.id = sum."ripsUnidadUpr_id") inner join admisiones_ingresos adm on (adm."tipoDoc_id" = fac."tipoDoc_id" and adm.documento_id=fac.documento_id and adm.consec=fac."consecAdmision") left join 	clinico_medicos medico on (medico.id =adm."medicoActual_id") inner join planta_planta planta on (planta.id = medico.planta_id) left join usuarios_tiposdocumento usutipdoc on (usutipdoc.id = planta."tipoDoc_id") left join rips_ripstiposdocumento ripstipdoc on (ripstipdoc.id = usutipdoc."tipoDocRips_id")   left join clinico_diagnosticos diag1 on (diag1.id=adm."dxActual_id") left join clinico_diagnosticos diag2 on (diag2.id=adm."dxIngreso_id") where env.id =  ' + "'" + str(envioRipsId) + "'" + ' and rips_ripstransaccion."ripsEnvio_id" = env.id  and cast(rips_ripstransaccion."numFactura" as numeric) = fac.id  and fac.id = ' + "'" + str(elemento) + "' AND facdet.cums_id is not null"
                    curx.execute(detalle1)
                    print("detalle =", detalle1)

                    if (aplicoAbono == 'NO'):

                        detalle3 ='UPDATE rips_ripsmedicamentos set "valorPagoModerador" = ' + "'" + str(totalAbonos) + "'" + ' WHERE "ripsTransaccion_id" = ' + "'" + str(transaccionId) + "'" + ' AND consecutivo = 1'
                        curx.execute(detalle3)


                    # FALTA EL UNION DE FACTURACION MANUAL CABALLERO

                if (tipoRips == 'Glosa'):

                    #detalle = 'INSERT INTO rips_ripsmedicamentos (glosa_id,"codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", "diasTratamiento",	"numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",consecutivo, "fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id","tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura","ripsTipos_id", "ripsTransaccion_id", ingreso_id, "estadoReg" , "motivoGlosa_id", "notasCreditoGlosa", "notasCreditoOtras","notasDebito","vAceptado","valorGlosado","valorSoportado") SELECT glosa.id, "codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", "diasTratamiento",	"numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",row_number() OVER(ORDER BY med.id) AS consecutivo , med."fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id","tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", med."usuarioRegistro_id", ' + "'" + str(elementox['id']) + "'" + ' , med."itemFactura",med."ripsTipos_id", ' + "'" + str(transaccionId) + "','"  + str(ingresoId.id) + "','A'"  + ' , gloDet."motivoGlosa_id", gloDet."valorNotasCredito", gloDet."valorNotasCreditoOtras",gloDet."valorNotasDebito",gloDet."valorAceptado",gloDet."valorGlosa",gloDet."valorSoportado"  FROM rips_ripsMedicamentos med inner join cartera_glosasdetalle gloDet on (gloDet."ripsMedicamentos_id" = med.id) inner join cartera_glosas glosa on (glosa.id = gloDet.glosa_id and glosa.factura_id = cast(med."numFEVPagoModerador"  as integer)) inner join rips_ripsdetalle det on (det."numeroFactura_id" =  cast(med."numFEVPagoModerador"  as integer) and  det.glosa_id=glosa.id and det.glosa_id=' + "'" + str(elemento) + "'" + ')  where med."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"

                    detalle = 'INSERT INTO rips_ripsmedicamentos ("glosa_id","codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", "diasTratamiento",	"numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",consecutivo, "fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id","tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura","ripsTipos_id", "ripsTransaccion_id", ingreso_id, "estadoReg" , "notasCreditoOtras") SELECT glosas.id, "codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", "diasTratamiento","numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",row_number() OVER(ORDER BY med.id) AS consecutivo , med."fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id","tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", med."usuarioRegistro_id", ' + "'" + str(elementox['id']) + "'" + ' , med."itemFactura",med."ripsTipos_id", ' + "'" + str(transaccionId) + "','"  + str(ingresoId.id) + "','A'"  + ', gloDetRips."valorAceptado"  FROM rips_ripsMedicamentos med  inner join cartera_glosasdetallerips gloDetRips  ON (gloDetRips."ripsMedicamentos_id" = med.id)  inner join cartera_glosasdetalle  gloDet on (gloDet.id = gloDetRips."glosasDetalle_id") inner join cartera_glosas glosas on (glosas.id = gloDet."glosa_id" and gloDet.factura_id = cast(med."numFEVPagoModerador"  as integer)) inner join rips_ripsdetalle det on (det."numeroFactura_id" =  cast(med."numFEVPagoModerador"  as integer) and  det."glosa_id" = glosas.id and det."glosa_id"=' + "'" + str(elemento) + "'" + ')  where med."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"


                    print("detalle = ", detalle)
                    curx.execute(detalle)


                if (tipoRips == 'Nota Credito'):

                    detalle = 'INSERT INTO rips_ripsmedicamentos ("notaCredito_id","codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", "diasTratamiento",	"numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",consecutivo, "fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id","tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura","ripsTipos_id", "ripsTransaccion_id", ingreso_id, "estadoReg" , "notasCreditoOtras") SELECT nc.id, "codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", "diasTratamiento","numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",row_number() OVER(ORDER BY med.id) AS consecutivo , med."fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id","tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", med."usuarioRegistro_id", ' + "'" + str(elementox['id']) + "'" + ' , med."itemFactura",med."ripsTipos_id", ' + "'" + str(transaccionId) + "','"  + str(ingresoId.id) + "','A'"  + ', ncDetRips."valorNota"  FROM rips_ripsMedicamentos med  inner join cartera_notascreditodetallerips ncDetRips  ON (ncDetRips."ripsMedicamentos_id" = med.id)  inner join cartera_notascreditodetalle  ncDet on (ncDet.id = ncDetRips."notaCreditoDetalle_id") inner join cartera_notascredito nc on (nc.id = ncDet."notaCredito_id" and ncDet.factura_id = cast(med."numFEVPagoModerador"  as integer)) inner join rips_ripsdetalle det on (det."numeroFactura_id" =  cast(med."numFEVPagoModerador"  as integer) and  det."notaCredito_id" =nc.id and det."notaCredito_id"=' + "'" + str(elemento) + "'" + ')  where med."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)


                # HASTA AQUI RIPSMedicamentos

                # RIPS RECIEN NACIDOS
                #
                print ("vamos a recien nacidos")

                if (tipoRips == 'Factura'):

                    detalle = 'INSERT INTO rips_ripsreciennacido ("codPrestador", "numDocumentoIdentificacion", "fechaNacimiento", "edadGestacional", "numConsultasCPrenatal","codSexoBiologico", peso, "fechaEgreso", consecutivo, "fechaRegistro", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id","condicionDestinoUsuarioEgreso_id","tipoDocumentoIdentificacion_id", "usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id ) SELECT sed."codigoHabilitacion",	usu.documento,	usu."fechaNacio", i."ripsEdadGestacional", i."ripsNumConsultasCPrenatal" ,	usu.genero, i."ripsPesoRecienNacido" ,cast(i."fechaSalida" as date), row_number() OVER(ORDER BY i.id) AS consecutivo ,now(), (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxSalida_id"), (select max(diag1.id) from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1 , clinico_historia his where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('1') + "'" + ' and histdiag1.diagnosticos_id = diag1.id and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" = fac."consecAdmision") , dest.id, tipoDoc."tipoDocRips_id", ' + "'" + str(username_id) + "'" + ' ,det.id,' + "'" + str('7') + "'" + ' , ripstra.id, ' + "'" + str('A') +"','" + str(ingresoId.id) + "'"   + '	FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join admisiones_ingresos i ON (i."sedesClinica_id" = sed.id and i."tipoDoc_id" =fac."tipoDoc_id" and i.documento_id = fac.documento_id AND i.consec =fac."consecAdmision")  inner join rips_ripsenvios env ON (env."sedesClinica_id" = sed.id) inner join rips_ripsdetalle det ON ( det."ripsEnvios_id" = env.id and  det."ripsEnvios_id" = fac."ripsEnvio_id" and det."numeroFactura_id" = fac.id )  inner join rips_ripstransaccion ripstra ON ( ripstra."sedesClinica_id" = sed.id and ripstra."ripsEnvio_id" = env.id and ripstra."numFactura" = cast(fac.id as text))  left join rips_ripsdestinoegreso dest  on (dest.id = i."ripsCondicionDestinoUsuarioEgreso_id") inner join usuarios_usuarios usu on (usu."tipoDoc_id" = i."tipoDoc_id" AND usu.id = i.documento_id) inner join usuarios_tiposdocumento tipoDoc on (tipoDoc.id = i."tipoDoc_id") where sed.id = ' + "'" + str(sede) + "'" + ' AND env.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'" + ' and i."ripsRecienNacido" = ' + "'" + str('S') + "'"

                if (tipoRips == 'Glosa'):

                    #detalle = 'INSERT INTO rips_ripsreciennacido ("codPrestador", "numDocumentoIdentificacion", "fechaNacimiento", "edadGestacional", "numConsultasCPrenatal","codSexoBiologico", peso,"fechaEgreso", consecutivo, "fechaRegistro", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id","condicionDestinoUsuarioEgreso_id","tipoDocumentoIdentificacion_id","usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", "ripsTransaccion_id", ingreso_id) SELECT "codPrestador", "numDocumentoIdentificacion", "fechaNacimiento", "edadGestacional", "numConsultasCPrenatal","codSexoBiologico", peso,"fechaEgreso", consecutivo, ripsnac."fechaRegistro", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id","condicionDestinoUsuarioEgreso_id","tipoDocumentoIdentificacion_id",ripsnac."usuarioRegistro_id",' + "'" + str(elementox['id']) + "'" + ', "ripsTipos_id", ' + "'" + str(transaccionId) + "','" + str(ingresoId.id) + "'"   + ' FROM rips_ripsreciennacido ripsnac, rips_ripsdetalle det, rips_ripstransaccion ripstra where ripstra."ripsEnvio_id" = det."ripsEnvios_id" and ripsnac."ripsTransaccion_id" = ripstra.id and ripsnac."ripsDetalle_id" = det.id and cast(ripstra."numFactura" as float) =  det."numeroFactura_id" and cast(ripstra."numFactura" as float) = ' + "'" + str(elementoOtro) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'" + ' and i."ripsRecienNacido" = ' + "'" + str('S') + "'"
                    #aQUIP macehte temporal
                    detalle = 'INSERT INTO rips_ripsreciennacido ("codPrestador", "numDocumentoIdentificacion", "fechaNacimiento", "edadGestacional", "numConsultasCPrenatal","codSexoBiologico", peso, "fechaEgreso", consecutivo, "fechaRegistro", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id","condicionDestinoUsuarioEgreso_id","tipoDocumentoIdentificacion_id", "usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id ) SELECT sed."codigoHabilitacion",	usu.documento,	usu."fechaNacio", i."ripsEdadGestacional", i."ripsNumConsultasCPrenatal" ,	usu.genero, i."ripsPesoRecienNacido" ,cast(i."fechaSalida" as date), row_number() OVER(ORDER BY i.id) AS consecutivo ,now(), (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxSalida_id"), (select max(diag1.id) from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1 , clinico_historia his where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('1') + "'" + ' and histdiag1.diagnosticos_id = diag1.id and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" = fac."consecAdmision") , dest.id, tipoDoc."tipoDocRips_id", ' + "'" + str(username_id) + "'" + ' ,det.id,' + "'" + str('7') + "'" + ' , ripstra.id, ' + "'" + str('A') +"','" + str(ingresoId.id) + "'"   + '	FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join admisiones_ingresos i ON (i."sedesClinica_id" = sed.id and i."tipoDoc_id" =fac."tipoDoc_id" and i.documento_id = fac.documento_id AND i.consec =fac."consecAdmision")  inner join rips_ripsenvios env ON (env."sedesClinica_id" = sed.id) inner join rips_ripsdetalle det ON ( det."ripsEnvios_id" = env.id and  det."ripsEnvios_id" = fac."ripsEnvio_id" and det."numeroFactura_id" = fac.id )  inner join rips_ripstransaccion ripstra ON ( ripstra."sedesClinica_id" = sed.id and ripstra."ripsEnvio_id" = env.id and ripstra."numFactura" = cast(fac.id as text))  left join rips_ripsdestinoegreso dest  on (dest.id = i."ripsCondicionDestinoUsuarioEgreso_id") inner join usuarios_usuarios usu on (usu."tipoDoc_id" = i."tipoDoc_id" AND usu.id = i.documento_id) inner join usuarios_tiposdocumento tipoDoc on (tipoDoc.id = i."tipoDoc_id") where sed.id = ' + "'" + str(sede) + "'" + ' AND env.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'" + ' and i."ripsRecienNacido" = ' + "'" + str('S') + "'" + ' and cast(ripstra."numNota" as integer) = 0'


                if (tipoRips == 'Nota Credito'):

                    detalle = 'INSERT INTO rips_ripsreciennacido ("codPrestador", "numDocumentoIdentificacion", "fechaNacimiento", "edadGestacional", "numConsultasCPrenatal","codSexoBiologico", peso, "fechaEgreso", consecutivo, "fechaRegistro", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id","condicionDestinoUsuarioEgreso_id","tipoDocumentoIdentificacion_id", "usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id ) SELECT sed."codigoHabilitacion",	usu.documento,	usu."fechaNacio", i."ripsEdadGestacional", i."ripsNumConsultasCPrenatal" ,	usu.genero, i."ripsPesoRecienNacido" ,cast(i."fechaSalida" as date), row_number() OVER(ORDER BY i.id) AS consecutivo ,now(), (select diag1.id from clinico_diagnosticos diag1 where  diag1.id = i."dxSalida_id"), (select max(diag1.id) from clinico_historialdiagnosticos histdiag1, clinico_diagnosticos diag1 , clinico_historia his where histdiag1.historia_id = his.id and histdiag1."tiposDiagnostico_id" = ' + "'" + str('1') + "'" + ' and histdiag1.diagnosticos_id = diag1.id and his."tipoDoc_id" = fac."tipoDoc_id" and his.documento_id = fac.documento_id AND his."consecAdmision" = fac."consecAdmision") , dest.id, tipoDoc."tipoDocRips_id", ' + "'" + str(username_id) + "'" + ' ,det.id,' + "'" + str('7') + "'" + ' , ripstra.id, ' + "'" + str('A') +"','" + str(ingresoId.id) + "'"   + '	FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join admisiones_ingresos i ON (i."sedesClinica_id" = sed.id and i."tipoDoc_id" =fac."tipoDoc_id" and i.documento_id = fac.documento_id AND i.consec =fac."consecAdmision")  inner join rips_ripsenvios env ON (env."sedesClinica_id" = sed.id) inner join rips_ripsdetalle det ON ( det."ripsEnvios_id" = env.id and  det."ripsEnvios_id" = fac."ripsEnvio_id" and det."numeroFactura_id" = fac.id )  inner join rips_ripstransaccion ripstra ON ( ripstra."sedesClinica_id" = sed.id and ripstra."ripsEnvio_id" = env.id and ripstra."numFactura" = cast(fac.id as text))  left join rips_ripsdestinoegreso dest  on (dest.id = i."ripsCondicionDestinoUsuarioEgreso_id") inner join usuarios_usuarios usu on (usu."tipoDoc_id" = i."tipoDoc_id" AND usu.id = i.documento_id) inner join usuarios_tiposdocumento tipoDoc on (tipoDoc.id = i."tipoDoc_id") where sed.id = ' + "'" + str(sede) + "'" + ' AND env.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'" + ' and i."ripsRecienNacido" = ' + "'" + str('S') + "'" + ' and cast(ripstra."numNota" as integer) = 0'

                print("detalle = ", detalle)
                curx.execute(detalle)



                # HASTA AQUI RECIEN NACIDOS# ##########################


                ## AQUI RIPS CONSULTAS PARA CONSULTA EXTERNA


                ## AQUI RIPS OTROS SERVICIOS

                if (tipoRips == 'Factura'):

                    # Cirugia INSUMOS SISTEMA
                    detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSalud_id","nomTecnologiaSalud", "cantidadOS",     "tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",       "tipoPagoModerador_id", "valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",       "ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", facdet."autorizacionDetalle_id", facdet.mipres, facdet."fecha",   ripsOtros.id,  exa.id,  substring(exa.nombre,1,60), facdet.cantidad,        tipdocrips.id, usu.documento,facdet."valorUnitario",    facdet."valorTotal", (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),  fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo, now(), ' + "'" + str(username_id) + "'" + ',detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "'" + ',' + str(transaccionId) + ",'" + str('A') + "'" + ',i.id  FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."cums_id" is not null and (facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') + "'" + ') and "tipoRegistro" = ' + "'" + str('SISTEMA') + "'" + ' AND facDet.cirugia_id is not null) inner join facturacion_suministros exa ON (exa.id = facdet."cums_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id)  inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) 	inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) inner join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_estadosautorizacion autEst on (autEst.nombre='+ "'" + str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" and tipHonor.nombre =' + "'" + str('MATERIALES DE SUTURA Y CURACIO') + "')" + ' inner join rips_ripstipootrosservicios ripsOtros on (ripsOtros.id=tipHonor."ripsTipoOtrosServicios_id") where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)

                    totalOtros1 = []
                    detalle = 'SELECT count(*) totalOtros FROM  rips_ripsotrosservicios where "ripsTransaccion_id"  =' + "'" + str(transaccionId) + "'"
                    curx.execute(detalle)

                    for totalOtros  in curx.fetchall():
                        totalOtros1.append(
                            {'totalOtros': totalOtros})

                    print("totalOtros =" , totalOtros1)
                    print("totaltotalOtros1 =", totalOtros1[0]['totalOtros'])

                    totalOtros = str(totalOtros1[0]['totalOtros'])
                    totalOtros = totalOtros.replace("(", ' ')
                    totalOtros = totalOtros.replace(")", ' ')
                    totalOtros = totalOtros.replace(",", ' ')
                    traigoConsecutivo = totalOtros

                    print("CREO AQUI VAMOS_0")
                    print("traigoConsecutivoId", traigoConsecutivo)

                    print("CREO AQUI VAMOS_1")

                    #detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSalud_id","nomTecnologiaSalud", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id","ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", autdet."numeroAutorizacion", his.mipres, facdet."fecha",   ripsOtros.id,  ripsCums.id,  substring(exa.nombre,1,60), facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal", (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),  (select carFac."valorAplicado"	from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),   fac.id, row_number()  OVER(ORDER BY facdet.id) + ' + str(traigoConsecutivo) + '  AS consecutivo, now(), ' + "'" + str(
                    #    username_id) + "'" + ',detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "','" + str(
                    #    transaccionId) + "','A'," + "'" + str(
                    #    ingresoId.id) + "'" + '	FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."cums_id" is not null and (facdet.anulado = ' + "'" + str(
                    #    'N') + "'" + ' or facdet.anulado = ' + "'" + str(
                    #    'R') + "')" + ' and "tipoRegistro" = ' + "'" + str(
                    #    'MANUAL') + "'" + ' AND facDet.cirugia_id is not null) inner join facturacion_suministros exa ON (exa.id = facdet."cums_id") inner join rips_ripscums ripsCums ON (ripsCums.id = exa."ripsCums_id")	inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id)  inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) 	left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id )  left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) inner join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) left join autorizaciones_autorizaciones  aut on (aut.historia_id = his.id) left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) inner join rips_ripstipootrosservicios ripsOtros on (ripsOtros.nombre=' + "'" + str(
                    #    'DISPOSITIVOS MEDICOS E INSUMOS') + "')" + ' where sed.id = ' + "'" + str(
                    #    sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(
                    #    elemento) + "'"

                    # Cirugia INSUMOS manual
                    detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSalud_id","nomTecnologiaSalud", "cantidadOS",     "tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",       "tipoPagoModerador_id", "valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",       "ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", facdet."autorizacionDetalle_id", autdet.mipres, facdet."fecha",   ripsOtros.id,  exa.id,  substring(exa.nombre,1,60), facdet.cantidad,        tipdocrips.id, usu.documento,facdet."valorUnitario",    facdet."valorTotal", (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),  fac.id, row_number()  OVER(ORDER BY facdet.id) + ' + str(traigoConsecutivo) + '  AS consecutivo, now(), ' + "'" + str(username_id) + "'" + ',detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "'" + ',' + str(transaccionId) + ",'" + str('A') + "'" + ',i.id  FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."cums_id" is not null and (facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') + "'" + ') and "tipoRegistro" = ' + "'" + str('MANUAL') + "'" + ' AND facDet.cirugia_id is not null) inner join facturacion_suministros exa ON (exa.id = facdet."cums_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id)  inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) 	inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) inner join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_estadosautorizacion autEst on (autEst.nombre=' + "'" + str('AUTORIZADO') + "'" + ')  left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" and tipHonor.nombre =' + "'" + str('MATERIALES DE SUTURA Y CURACIO') + "')" + ' inner join rips_ripstipootrosservicios ripsOtros on (ripsOtros.id=tipHonor."ripsTipoOtrosServicios_id") where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)

                    totalOtros1 = []
                    detalle = 'SELECT count(*) totalOtros FROM  rips_ripsotrosservicios where "ripsTransaccion_id"  =' + "'" + str(transaccionId) + "'"
                    curx.execute(detalle)

                    for totalOtros  in curx.fetchall():
                        totalOtros1.append(
                            {'totalOtros': totalOtros})

                    print("CREO AQUI VAMOS_3")
                    print("totalOtros =" , totalOtros1)
                    print("CREO AQUI VAMOS_2")
                    print("totaltotalOtros1 =", totalOtros1[0]['totalOtros'])
                    print("CREO AQUI VAMOS_4")
                    totalOtros = str(totalOtros1[0]['totalOtros'])
                    totalOtros = totalOtros.replace("(", ' ')
                    totalOtros = totalOtros.replace(")", ' ')
                    totalOtros = totalOtros.replace(",", ' ')
                    traigoConsecutivo = totalOtros

                    print("traigoConsecutivoId", traigoConsecutivo)

                    # aQUI TRAE HONORARIOS SISTEMA

                    detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", facdet."autorizacionDetalle_id", facdet.mipres, facdet."fecha",	ripsOtros.id,  exa.id,  substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal",  (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), fac.id, row_number()  OVER(ORDER BY facdet.id) +  ' + str(traigoConsecutivo) + ' AS consecutivo, now(), ' + "'" + str(
                        username_id) + "'" + ',detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "','" + str(
                        transaccionId) + "','A'," + "'" + str(
                        ingresoId.id) + "'" + '	FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)	inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = ' + "'" + str(
                        'N') + "'" + ' or facdet.anulado = ' + "'" + str(
                        'R') + "')" + ' and "tipoRegistro" = ' + "'" + str(
                        'SISTEMA') + "'" + ' AND facDet.cirugia_id is not null) inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id )  left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) INNER join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id ) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id)	left join autorizaciones_estadosautorizacion autEst on (autEst.nombre=' + "'" + str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" ) inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.id=tipHonor."ripsTipoOtrosServicios_id" and ripsOtros.nombre=' + "'" + str(
                        'HONORARIOS') + "')" + ' where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(
                        envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)

                    totalOtros1 = []
                    detalle = 'SELECT count(*) totalOtros FROM  rips_ripsotrosservicios where "ripsTransaccion_id"  =' + "'" + str(transaccionId) + "'"
                    curx.execute(detalle)

                    for totalOtros  in curx.fetchall():
                        totalOtros1.append(
                            {'totalOtros': totalOtros})

                    print("totalOtros =" , totalOtros1)
                    print("totaltotalOtros1 =", totalOtros1[0]['totalOtros'])

                    totalOtros = str(totalOtros1[0]['totalOtros'])
                    totalOtros = totalOtros.replace("(", ' ')
                    totalOtros = totalOtros.replace(")", ' ')
                    totalOtros = totalOtros.replace(",", ' ')
                    traigoConsecutivo = totalOtros
                    print("CREO AQUI VAMOS_5")
                    print("traigoConsecutivoId", traigoConsecutivo)
                    print("CREO AQUI VAMOS_6")

                    conceptoEstancias = Conceptos.objects.get(nombre='ESTANCIAS')
                    print("conceptoEstancias", conceptoEstancias.id)
                   

                    detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", facdet."autorizacionDetalle_id", facdet.mipres, facdet."fecha",	ripsOtros.id,  exa.id,  substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal",  (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), fac.id, row_number()  OVER(ORDER BY facdet.id) +  ' + str(traigoConsecutivo) + ' AS consecutivo, now(), ' + "'" + str(
                        username_id) + "'" + ',detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "','" + str(
                        transaccionId) + "','A'," + "'" + str(
                        ingresoId.id) + "'" + '	FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)	inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = ' + "'" + str(
                        'N') + "'" + ' or facdet.anulado = ' + "'" + str(
                        'R') + "')" + ' and "tipoRegistro" = ' + "'" + str(
                        'MANUAL') + "'" + ' AND facDet.cirugia_id is not null) inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id )  left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) INNER join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id ) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_estadosautorizacion autEst on (autEst.nombre=' + "'"+ str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" ) inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.id=tipHonor."ripsTipoOtrosServicios_id" and ripsOtros.nombre=' + "'" + str(
                        'HONORARIOS') + "')" + ' where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(
                        envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)


                    totalOtros1 = []
                    detalle = 'SELECT count(*) totalOtros FROM  rips_ripsotrosservicios where "ripsTransaccion_id"  =' + "'" + str(transaccionId) + "'"
                    curx.execute(detalle)

                    for totalOtros  in curx.fetchall():
                        totalOtros1.append(
                            {'totalOtros': totalOtros})

                    print("totalOtros =" , totalOtros1)
                    print("totaltotalOtros1 =", totalOtros1[0]['totalOtros'])

                    totalOtros = str(totalOtros1[0]['totalOtros'])
                    totalOtros = totalOtros.replace("(", ' ')
                    totalOtros = totalOtros.replace(")", ' ')
                    totalOtros = totalOtros.replace(",", ' ')
                    traigoConsecutivo = totalOtros
                    print("CREO AQUI VAMOS_7")
                    print("traigoConsecutivoId", traigoConsecutivo)
                    print("CREO AQUI VAMOS_8")

                    conceptoEstancias = Conceptos.objects.get(nombre='ESTANCIAS')
                    print("conceptoEstancias", conceptoEstancias.id)

                    #Estancias con SISTEMA

                    detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", facdet."autorizacionDetalle_id", facdet.mipres, facdet."fecha",	ripsOtros.id,  exa.id, substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal",  (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo,  now(), ' + "'" + str(username_id) + "'," + ' detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "','" + str(transaccionId) + "','" + str('A') + "','" + str(ingresoId.id) + "'" + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') + "')" + '  And "tipoRegistro" = ' + "'"  + str('SISTEMA') + "')" + ' inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_estadosautorizacion autEst on (autEst.nombre=' + "'" + str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.nombre=' + "'" + str('ESTANCIAS') + "')" +' inner join sitios_dependencias dep on (dep.id = i."dependenciasSalida_id") inner join 	sitios_serviciossedes servSedes ON (servSedes."sedesClinica_id" = sed.id and servSedes.id =dep."serviciosSedes_id" ) inner join 	clinico_servicios serv ON (serv.id =servSedes.servicios_id ) inner join tarifarios_estancias estancias ON (estancias.cups_id= facDet.examen_id) where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" +  str(elemento) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)


		    #Estancias con MANUAL

                    detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", facdet."autorizacionDetalle_id", facdet.mipres, facdet."fecha",	ripsOtros.id,  exa.id, substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal",  (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo,  now(), ' + "'" + str(username_id) + "'," + ' detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "','" + str(transaccionId) + "','" + str('A') + "','" + str(ingresoId.id) + "'" + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') + "')" + '  And "tipoRegistro" = ' + "'" + str('MANUAL') + "')" + ' inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id)  left join autorizaciones_estadosautorizacion autEst on (autEst.nombre=' + "'"+ str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.nombre=' + "'" + str('ESTANCIAS') + "')" + ' inner join sitios_dependencias dep on (dep.id = i."dependenciasSalida_id") inner join 	sitios_serviciossedes servSedes ON (servSedes."sedesClinica_id" = sed.id and servSedes.id =dep."serviciosSedes_id" ) inner join 	clinico_servicios serv ON (serv.id =servSedes.servicios_id ) inner join tarifarios_estancias estancias ON (estancias.cups_id= facDet.examen_id) where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)


                if (tipoRips == 'Glosa'):


                    # Por aqui GLOSA

                    detalle = 'INSERT INTO rips_ripsotrosservicios ("glosa_id","codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia", "nomTecnologiaSalud", "cantidadOS", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio", "valorPagoModerador", "numFEVPagoModerador", consecutivo, "fechaRegistro", "codTecnologiaSalud_id", "conceptoRecaudo_id", "tipoDocumentoIdentificacion_id", "tipoOS_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "notasCreditoOtras","estadoReg", ingreso_id, "tipoPagoModerador_id") SELECT glosas.id,"codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia", "nomTecnologiaSalud", "cantidadOS", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio", "valorPagoModerador", "numFEVPagoModerador", row_number() OVER(ORDER BY ripsOtros.id) AS consecutivo , ripsOtros."fechaRegistro", "codTecnologiaSalud_id", "conceptoRecaudo_id", "tipoDocumentoIdentificacion_id", "tipoOS_id",ripsOtros."usuarioRegistro_id",' + "'" + str(
                        elementox['id']) + "'" + ', ripsOtros."itemFactura", ripsOtros."ripsTipos_id", ' + "'" + str(
                        transaccionId) + "'," + 'gloDetRips."valorNotasCredito" ' + ",'A','" + str(
                        ingresoId.id) + "'," + '"tipoPagoModerador_id" FROM rips_ripsotrosservicios ripsOtros inner join cartera_glosasdetallerips gloDetRips ON (gloDetRips."ripsOtrosServicios_id" = ripsOtros.id) inner join cartera_glosasdetalle gloDet on (gloDet.id = gloDetRips."glosasDetalle_id") inner join cartera_glosas glosas on (glosas.id = gloDet."glosa_id" and gloDet.factura_id = cast(ripsOtros."numFEVPagoModerador"  as integer)) inner join rips_ripsdetalle det on (det."numeroFactura_id" =  cast(ripsOtros."numFEVPagoModerador" as integer) and det."glosa_id"=glosas.id and det."glosa_id" =' + "'" + str(
                        elemento) + "'" + ') where ripsOtros."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"

                    print("detalle = ", detalle)
                    curx.execute(detalle)


                if (tipoRips == 'Nota Credito'):

                    # Por aqui Nota Credito
                    detalle = 'INSERT INTO rips_ripsotrosservicios ("notaCredito_id","codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia", "nomTecnologiaSalud", "cantidadOS", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio", "valorPagoModerador", "numFEVPagoModerador", consecutivo, "fechaRegistro", "codTecnologiaSalud_id", "conceptoRecaudo_id", "tipoDocumentoIdentificacion_id", "tipoOS_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "notasCreditoOtras","estadoReg", ingreso_id, "tipoPagoModerador_id") SELECT nc.id,"codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia", "nomTecnologiaSalud", "cantidadOS", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio", "valorPagoModerador", "numFEVPagoModerador", row_number() OVER(ORDER BY ripsOtros.id) AS consecutivo , ripsOtros."fechaRegistro", "codTecnologiaSalud_id", "conceptoRecaudo_id", "tipoDocumentoIdentificacion_id", "tipoOS_id",ripsOtros."usuarioRegistro_id",' + "'" + str(
                        elementox['id']) + "'" + ', ripsOtros."itemFactura", ripsOtros."ripsTipos_id", ' + "'" + str(
                        transaccionId) + "'," + 'ncDetRips."valorNota" ' + ",'A','" + str(
                        ingresoId.id) + "'," + '"tipoPagoModerador_id" FROM rips_ripsotrosservicios ripsOtros inner join cartera_notascreditodetallerips ncDetRips ON (ncDetRips."ripsOtrosServicios_id" = ripsOtros.id) inner join cartera_notascreditodetalle ncDet on (ncDet.id = ncDetRips."notaCreditoDetalle_id") inner join cartera_notascredito nc on (nc.id = ncDet."notaCredito_id" and ncDet.factura_id = cast(ripsOtros."numFEVPagoModerador"  as integer)) inner join rips_ripsdetalle det on (det."numeroFactura_id" =  cast(ripsOtros."numFEVPagoModerador" as integer) and det."notaCredito_id"=nc.id and det."notaCredito_id" =' + "'" + str(
                        elemento) + "'" + ') where ripsOtros."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"
                    print("detalle = ", detalle)
                    curx.execute(detalle)


        		## Aqui RIPS DE CONSULTA
                #
                print("Voy a Rips de CONSULTA")

                if (tipoRips == 'Factura'):

                    comando = 'INSERT INTO rips_ripsconsultas ( "codPrestador","fechaInicioAtencion","numAutorizacion","tipoDiagnosticoPrincipal", "numDocumentoIdentificacion","vrServicio","valorPagoModerador","numFEVPagoModerador",consecutivo, "itemFactura",  "fechaRegistro", "estadoReg","causaMotivoAtencion_id","codConsulta_id", "codDiagnosticoPrincipal_id",  "codDiagnosticoRelacionado1_id", "codDiagnosticoRelacionado2_id", "codDiagnosticoRelacionado3_id", "codServicio_id", "finalidadTecnologiaSalud_id", "grupoServicios_id",ingreso_id, "modalidadGrupoServicioTecSal_id","ripsDetalle_id","ripsTipos_id", "ripsTransaccion_id","tipoDocumentoIdentificacion_id", "usuarioRegistro_id") SELECT sed."codigoHabilitacion",i."fechaIngreso",facdet."autorizacionDetalle_id",dxTipo.codigo,usu.documento,	(select sum(facDet1."valorTotal") 	 FROM facturacion_facturaciondetalle facDet1 WHERE facDet1.anulado=' + "'" + str('N') + "'" + ' and facDet1."estadoRegistro"='  "'" + str('A') + "'" + ' and facDet1.facturacion_id=fac.id ) vrServicio, 	0 valorPagoModerador, 	fac.id ,row_number()  OVER(ORDER BY facdet.id), facdet."consecutivoFactura", now(),' + "'" + str('A') + "'" + ', causaExternaRips.id, facdet.examen_id, 	(select histdiag1.diagnosticos_id from clinico_historia his2 left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('PRINCIPAL') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)  where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision" 	) principal,(select histdiag1.diagnosticos_id  from clinico_historia his2	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('RELACIONADO 1') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)  where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision" 	) relacionado1,	(select histdiag1.diagnosticos_id  from clinico_historia his2 	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('RELACIONADO 3') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)  where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision" 	) relacionado2,	(select histdiag1.diagnosticos_id  from clinico_historia his2 left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('RELACIONADO 3') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id) where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision") relacionado3, ripsServicios.id, finConsulta.id, grupoServicios.id,i.id ingreso, modalAtencion.id, detrips.id,3,' + "'" + str(transaccionId) + "'" + ' ,  tipdocrips.id   ,' + "'" + str(username_id) + "'" + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet.examen_id is not null and 	(facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') +"')" + ' and "tipoRegistro" = ' + "'" + str('SISTEMA') + "'" + ' AND facDet.cirugia_id is not null ) inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision")	 inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) inner join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) inner  join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_estadosautorizacion autEst on (autEst.nombre=' + "'" + str('AUTORIZADO') + "'" + ') left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id AND autdet."estadoAutorizacion_id" = autEst.id and autdet.id = facdet."autorizacionDetalle_id") INNER JOIN 	tarifarios_tiposhonorarios hono ON (hono.id= facDet."tipoHonorario_id" and hono.nombre=' + "'" + str('CIRUJANO') + "')" + ' INNER JOIN sitios_dependencias dep ON (dep.id= i."dependenciasSalida_id") INNER JOIN sitios_serviciosSedes servSedes on (servSedes.id=dep."serviciosSedes_id") INNER JOIN sitios_subServiciosSedes subServSedes on (subServSedes.id=dep."subServiciosSedes_id") INNER JOIN clinico_servicios serv on (serv.id = servSedes.servicios_id AND serv.nombre=' + "'" + str('AMBULATORIO') + "')" + ' INNER JOIN rips_ripstipodiagnosticoPrincipal dxTipo on (dxTipo.nombre=' + "'"  +  str('Impresión diagnóstica') + "')" + ' LEFT JOIN rips_ripscausaexterna causaExternaRips ON (causaExternaRips.id = i."ripsCausaMotivoAtencion_id") left join rips_ripsservicios ripsServicios ON (ripsServicios.id = i."ripsServiciosIng_id" ) left join rips_ripsfinalidadconsulta finConsulta ON (finConsulta.id = i."ripsFinalidadConsulta_id" ) left join rips_ripsgruposervicios grupoServicios ON (grupoServicios.id = i."ripsGrupoServicios_id" ) left join rips_ripsmodalidadatencion modalAtencion ON (modalAtencion.id = i."ripsmodalidadGrupoServicioTecSal_id" ) where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

                    print("comando = ", comando)
                    curx.execute(comando)

                if (tipoRips == 'Glosa'):

                    detalle = 'INSERT INTO rips_ripsconsultas ("glosa_id","codPrestador", "numAutorizacion", 	"numDocumentoIdentificacion",  "vrServicio", "valorPagoModerador", "numFEVPagoModerador",consecutivo, "fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id",  "tipoDocumentoIdentificacion_id", "usuarioRegistro_id", "ripsDetalle_id", "itemFactura","ripsTipos_id", "ripsTransaccion_id", ingreso_id, "estadoReg" , "notasCreditoOtras") SELECT glosas.id, "codPrestador", "numAutorizacion","numDocumentoIdentificacion", "vrServicio", "valorPagoModerador", "numFEVPagoModerador",row_number() OVER(ORDER BY med.id) AS consecutivo , med."fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id",  "tipoDocumentoIdentificacion_id", med."usuarioRegistro_id", ' + "'" + str(elementox['id']) + "'" + ' , med."itemFactura",med."ripsTipos_id", ' + "'" + str(transaccionId) + "','"  + str(ingresoId.id) + "','A'"  + ', gloDetRips."valorAceptado"  FROM rips_ripsConsultas cons inner join cartera_glosasdetallerips gloDetRips  ON (gloDetRips."ripsConsultas_id" = cons.id)  inner join cartera_glosasdetalle  gloDet on (gloDet.id = gloDetRips."glosasDetalle_id") inner join cartera_glosas glosas on (glosas.id = gloDet."glosa_id" and gloDet.factura_id = cast(cons."numFEVPagoModerador"  as integer)) inner join rips_ripsdetalle det on (det."numeroFactura_id" =  cast(cons."numFEVPagoModerador"  as integer) and  det."glosa_id" = glosas.id and det."glosa_id"=' + "'" + str(elemento) + "'" + ')  where cons."numFEVPagoModerador" = ' + "'" + str(elementoOtro) + "'"
                    print ("Rips Conulta glosas")

                if (tipoRips == 'Nota Credito'):

                    pass
                    print("Rips Conulta glosas")



                # Busco el id del estado Rips PENDIENTE CON JSON GENERADO

                ripsEstados = RipsEstados.objects.get(nombre="PENDIENTE CON JSON GENERADO")
                print ("El estado es = ", ripsEstados.id )

                # Aqui generamos los JSON de la Factura
                #
                traza = []
                comando='SELECT id from rips_ripstransaccion where id =' + "'" + str(transaccionId) +  "'"

                curx.execute(comando)

                for id in curx.fetchall():
                    traza.append({'id': id})

                print ("traza1 tx = ", traza)
                traza = []

                comando = 'SELECT id from rips_ripshospitalizacion where "ripsTransaccion_id" =' + "'" + str(transaccionId) + "'"

                curx.execute(comando)

                for id in curx.fetchall():
                    traza.append({'id': id})

                print("traza2 hospit = ", traza)

                traza = []

                comando = 'SELECT id from rips_ripsprocedimientos where "ripsTransaccion_id" =' + "'" + str(transaccionId) + "'"

                curx.execute(comando)

                for id in curx.fetchall():
                    traza.append({'id': id})

                print("traza3  procedimientos = ", traza)

                traza = []

                comando = 'SELECT id from rips_ripsmedicamentos where "ripsTransaccion_id" =' + "'" + str(transaccionId) + "'"

                curx.execute(comando)

                for id in curx.fetchall():
                    traza.append({'id': id})

                print("traza4 Medicamentos = ", traza)

                comando = 'SELECT id from rips_ripsotrosservicios where "ripsTransaccion_id" =' + "'" + str(transaccionId) + "'"

                curx.execute(comando)

                for id in curx.fetchall():
                    traza.append({'id': id})

                print("traza4 rips_ripsotrosservicios = ", traza)

                print("voy a generar el json con transaccionId =" ,  transaccionId)

                funcionJson = []

                if (tipoRips == 'Factura'):

                    #detalle = 'SELECT generaFacturaJSONBAK1(' + "'" +  str(envioRipsId) + "','" + str(elemento) + "'"  +  ',' + "'" + str('FACTURA') + "'" + ',0) dato'
                    detalle = 'SELECT generaFacturaJSONBAK1(' + "'" + str(envioRipsId) + "','" + str(elemento) + "'" + ',' + "'" + str('FACTURA') + "'," + str(transaccionId) + ') dato'

                if (tipoRips == 'Glosa'):

                    detalle = 'SELECT generaFacturaJSONBak1(' + str(envioRipsId) + "," + str(elemento) +  ',' + "'" + str('GLOSA') + "'," +  str(transaccionId)  + ') dato'

                if (tipoRips == 'Nota Credito'):

                    detalle = 'SELECT generaFacturaJSONBak1(' + str(envioRipsId) + "," + str(elemento) +  ',' + "'" + str('NOTA CREDITO') + "'," +  str(transaccionId)  + ') dato'

                print ('detalle a generaJSONFactura= ', detalle)
                curx.execute(detalle)

                for dato in curx.fetchall():

                    funcionJson.append({'dato': dato})

                print("funcionJson[0]", funcionJson[0])

                miConexionx.commit()

                if (tipoRips == 'Factura'):
                    print("Factura = ", elemento)
                    archivo = 'Fac' + str(elemento) + '.txt'
                    nombreCarpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\' + str(archivo)

                if (tipoRips == 'Glosa'):
                    print("Glosa = ", elemento)
                    archivo = 'Glo_' + str(elemento) + '_' + str(elementoOtro) + '.txt'
                    nombreCarpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\' + str(archivo)


                if (tipoRips == 'Nota Credito'):
                    print("Nota Credito = ", elemento)
                    archivo = 'NotCre_' + str(elemento) + '_' + str(elementoOtro) + '.txt'
                    nombreCarpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\' + str(archivo)


                print("ruta =", nombreCarpeta)


                # Aqui crea el archivo

                try:

                    file = open(nombreCarpeta, "w")
                    print("funcionJson[0]['dato']" , funcionJson[0]['dato'])
                    file.writelines(funcionJson[0]['dato'])
                    file.close()

                except Exception as e:
                    print ("error ", e)

                    message_error= str(e)
                    #return JsonResponse({'success': False, 'Mensajes': message_error})


                # Aqui Actualiza la ruta en la tabla rips_ripsdetalle

                if (tipoRips == 'Factura'):

                    detalle = 'UPDATE rips_ripsDetalle SET "rutaJsonFactura" = ' + "'" + str(nombreCarpeta) + "', " + ' "ripsEstados_id" = ' + "'" + str(ripsEstados.id) + "'" +  ' WHERE "ripsEnvios_id" = '  + "'" + str(envioRipsId) + "'" + '  AND "numeroFactura_id" = ' +"'" +str(elemento) + "'"

                if (tipoRips == 'Glosa'):

                    detalle = 'UPDATE rips_ripsDetalle SET "rutaJsonFactura" = ' + "'" + str(nombreCarpeta) + "', " + ' "ripsEstados_id" = ' + "'" + str(ripsEstados.id) + "'" +  ' WHERE "ripsEnvios_id" =  '  + "'" + str(envioRipsId) + "'" + ' AND "glosa_id" = ' +"'" +str(elemento) + "'"

                if (tipoRips == 'Nota Credito'):

                    detalle = 'UPDATE rips_ripsDetalle SET "rutaJsonFactura" = ' + "'" + str(nombreCarpeta) + "', " + ' "ripsEstados_id" = ' + "'" + str(ripsEstados.id) + "'" +  ' WHERE "ripsEnvios_id" =  '  + "'" + str(envioRipsId) + "'" + ' AND "notaCredito_id" = ' +"'" +str(elemento) + "'" + ' AND "numeroFactura_id" = ' + "'" + str(elementoOtro) + "'"

                print ("detalle = ", detalle)
                curx.execute(detalle)

            # Aqui generamos el JSON GLOBAL DE TODOS LOS ELEMENTOS (Facturas o Glosas) DEL ENVIO
                #
            print("voya  generar el Envio GRANDE")

            funcionGlobalJson = []

            if (tipoRips == 'Factura'):

                detalle = 'SELECT generaEnvioRipsJSON1(' + str(envioRipsId) + ',' + "'" + str('FACTURA') + "'" + ') dato'

            if (tipoRips == 'Glosa'):

                detalle = 'SELECT generaEnvioRipsJSON1(' + str(envioRipsId) + ',' + "'" + str('GLOSA') + "'" + ') dato'

            if (tipoRips == 'Nota Credito'):

                detalle = 'SELECT generaEnvioRipsJSON1(' + str(envioRipsId) + ',' + "'" + str('NOTA CREDITO') + "'" + ') dato'


            curx.execute(detalle)

            for dato in curx.fetchall():
                    funcionGlobalJson.append({'dato': dato})


            archivo = 'Env' + str(envioRipsId) + '.txt'
            nombreCarpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\' + str(archivo)

            for y in funcionGlobalJson[0]['dato']:

                print("tesxto funcionJson = ", y)

                # Aqui crea el archivo
                #
                file = open(nombreCarpeta, "w")
                file.writelines(y)
                file.close()

            totalItems = RipsDetalle.objects.filter(ripsEnvios_id=envioRipsId).count()

            print ("totalItems = ", totalItems)

            # Aqui grabo la ruta del JSON GLOBAL

            detalle = 'UPDATE rips_ripsEnvios SET "cantidadFacturas" = ' + "'" + str(totalItems) + "'," + ' "fechaGeneracionjson" = ' + "'" + str(fechaRegistro) + "'" +', "usuarioGeneraJson_id" = ' + "'" + str(username_id) + "'," + '"rutaJson" = ' + "'" + str(nombreCarpeta) + "'," + '"ripsEstados_id" = ' + "'" + str(ripsEstados.id) + "'" + ' WHERE id = '  + "'" + str(envioRipsId) + "'"
            curx.execute(detalle)
            miConexionx.commit()
            miConexionx.close()

            return JsonResponse({'success': True, 'message': 'Rips JSON generados satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexionx:
            print("Entro ha hacer el Rollback")
            miConexionx.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})
    finally:
        if miConexionx:
            curx.close()
            miConexionx.close()



def Load_tablaRipsTransaccion(request, data):
    print("Entre load_data Transaccion Rips")

    context = {}
    d = json.loads(data)


    envioRipsId = d['envioRipsId']
    print("envioRipsId = ", envioRipsId)


    transaccionRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT id, "numDocumentoIdObligado", "numNota","fechaRegistro", "tipoNota_id","usuarioRegistro_id"  , "ripsEnvio_id", "sedesClinica_id"  FROM public.rips_ripstransaccion WHERE  "ripsEnvio_id" = ' + "'" + str(envioRipsId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id,  numDocumentoIdObligado, numNota, fechaRegistro,tipoNota_id, usuarioRegistro_id,  ripsEnvio_id,  sedesClinica_id in curx.fetchall():
        transaccionRips.append(
            {"model": "rips.RipsTransaccion", "pk": id, "fields":
                {'id': id, 'numDocumentoIdObligado': numDocumentoIdObligado , 'numNota': numNota, 'fechaRegistro': fechaRegistro, 'tipoNota_id':tipoNota_id, 'usuarioRegistro_id':usuarioRegistro_id,
                   'ripsEnvio_id': ripsEnvio_id, 'sedesClinica_id' :sedesClinica_id}})



    miConexionx.close()
    print("transaccionRips "  , transaccionRips)
    #context['TransaccionRips'] = transaccionRips

    serialized1 = json.dumps(transaccionRips, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')


def Load_tablaRipsUsuarios(request, data):
    print("Entre load_data Transaccion Rips")

    context = {}
    d = json.loads(data)


    envioRipsId = d['envioRipsId']
    print("envioRipsId = ", envioRipsId)


    usuariosRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT  ripsu.id, ripsu."tipoDocumentoIdentificacion", ripsu."tipoUsuario", ripsu."fechaNacimiento", ripsu."codSexo", "codZonaTerritorialResidencia_id", ripsu.incapacidad, ripsu.consecutivo, ripsu."fechaRegistro", "codMunicipioResidencia_id", "codPaisOrigen_id", "codPaisResidencia_id", ripsu."usuarioRegistro_id", "numDocumentoIdentificacion", ripsu."ripsDetalle_id", ripsu."ripsTransaccion_id"  FROM public.rips_ripsusuarios ripsu, public.rips_ripstransaccion ripstra  WHERE  ripstra."ripsEnvio_id" = ' + "'" + str(envioRipsId) + "'" + ' AND ripstra.id = ripsu."ripsTransaccion_id" '

    print(detalle)

    curx.execute(detalle)

    for id,  tipoDocumentoIdentificacion, tipoUsuario, fechaNacimiento,codSexo, codZonaTerritorialResidencia,  incapacidad,  consecutivo, fechaRegistro, codMunicipioResidencia_id , codPaisOrigen_id, codPaisResidencia_id, usuarioRegistro_id , numDocumentoIdentificacion,ripsDetalle_id, ripsTransaccion_id in curx.fetchall():
        usuariosRips.append(
            {"model": "rips.RipsTransaccion", "pk": id, "fields":
                {'id': id, 'tipoDocumentoIdentificacion': tipoDocumentoIdentificacion , 'tipoUsuario': tipoUsuario, 'fechaNacimiento': fechaNacimiento, 'codSexo':codSexo, 'codZonaTerritorialResidencia':codZonaTerritorialResidencia,
                   'incapacidad': incapacidad, 'consecutivo' :consecutivo ,'fechaRegistro':fechaRegistro, 'codMunicipioResidencia_id':codMunicipioResidencia_id,'codPaisOrigen_id':codPaisOrigen_id,'codPaisResidencia_id':codPaisResidencia_id,'usuarioRegistro_id':usuarioRegistro_id ,'numDocumentoIdentificacion':numDocumentoIdentificacion,
                    'ripsDetalle_id':ripsDetalle_id,'ripsTransaccion_id':ripsTransaccion_id
                 }})



    miConexionx.close()
    print("usuariosRips "  , usuariosRips)
    #context['usuariosRips'] = usuariosRips

    serialized1 = json.dumps(usuariosRips, default=str)

    return HttpResponse(serialized1, content_type='application/json')



def EnviarJsonRips(request):
    print("Entre a EnviarJsonRips")

    envioRipsId = request.POST['envioRipsId']
    print("envioRipsId =", envioRipsId)

    sede = request.POST["sede"]
    print("sede =", sede)

    username_id = request.POST['username_id']
    print("username_id =", username_id)

    tipoRips = request.POST['tipoRips']
    print("tipoRips =", tipoRips)

    fechaRegistro = timezone.now()
    print("fechaRegistro = ", fechaRegistro)

    ripsEstadosId = RipsEstados.objects.get(nombre="ENVIADA")
    print ("El estado es = ", ripsEstadosId.id )


    ### Aqui actualizar cosas de la tabla rips_ripsenvios

    miConexionx = None
    try:

        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curx = miConexionx.cursor()

        detalle = 'UPDATE rips_ripsEnvios SET "fechaEnvio" = ' + "'" + str(fechaRegistro) + "'" +', "ripsEstados_id" = ' + "'" + str(ripsEstadosId.id) + "'," + '"usuarioEnvia_id"= ' + "'" + str(username_id)  + "' WHERE id =" + "'" + str(envioRipsId) + "'"
        curx.execute(detalle)
        miConexionx.commit()

        miConexionx.close()

        return JsonResponse({'success': True, 'Mensajes': 'Rips JSON marcados para Envio satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexionx:
            print("Entro ha hacer el Rollback")
            miConexionx.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexionx:
            curx.close()
            miConexionx.close()


def Load_tablaRipsProcedimientos(request, data):
    print("Entre load_data Procedimientos Rips")

    context = {}
    d = json.loads(data)


    envioRipsId = d['envioRipsId']
    print("envioRipsId = ", envioRipsId)


    procedimientosRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT  ripsproc.id id, "codPrestador", cast("fechaInicioAtencion" as date), "idMIPRES", "numAutorizacion", ripsproc."numDocumentoIdentificacion", "vrServicio", "valorPagoModerador", ripsproc."numFEVPagoModerador", ripsproc.consecutivo, ripsproc."fechaRegistro", "codComplicacion_id", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codProcedimiento_id", "codServicio_id", "conceptoRecaudo_id", "finalidadTecnologiaSalud_id", "grupoServicios_id", "modalidadGrupoServicioTecSal_id", ripsproc."tipoDocumentoIdentificacion_id", ripsproc."usuarioRegistro_id", "viaIngresoServicioSalud_id", ripsproc."ripsDetalle_id", "itemFactura", ripsproc."ripsTipos_id", "tipoPagoModerador_id", ripsproc."ripsTransaccion_id"  FROM public.rips_ripstransaccion ripstra, public.rips_ripsprocedimientos ripsproc , public.rips_ripsenvios env, rips_ripsdetalle det WHERE  env.id=det."ripsEnvios_id" AND det.id= ripsproc."ripsDetalle_id" AND env.id = ' + "'" + str(envioRipsId) + "'" + ' AND  ripstra.id = ripsproc."ripsTransaccion_id" '

    print(detalle)

    curx.execute(detalle)

    for id,  codPrestador, fechaInicioAtencion, idMIPRES,numAutorizacion, numDocumentoIdentificacion,  vrServicio,  valorPagoModerador, numFEVPagoModerador, consecutivo , fechaRegistro,  codComplicacion_id, codDiagnosticoPrincipal_id, codDiagnosticoRelacionado_id, codProcedimiento_id, codServicio_id, conceptoRecaudo_id, finalidadTecnologiaSalud_id, grupoServicios_id, modalidadGrupoServicioTecSal_id, tipoDocumentoIdentificacion_id, usuarioRegistro_id, viaIngresoServicioSalud_id, ripsDetalle_id, itemFactura, ripsTipos_id, tipoPagoModerador_id, ripsTransaccion_id in curx.fetchall():
        procedimientosRips.append(
            {"model": "rips.RipsProcedimientos", "pk": id, "fields":
                {'id': id, 'codPrestador': codPrestador , 'fechaInicioAtencion': fechaInicioAtencion, 'idMIPRES': idMIPRES, 'numAutorizacion':numAutorizacion, 'numDocumentoIdentificacion':numDocumentoIdentificacion,'vrServicio':vrServicio, 'valorPagoModerador':valorPagoModerador,'numFEVPagoModerador':numFEVPagoModerador,'consecutivo':consecutivo,'fechaRegistro':fechaRegistro,'codComplicacion_id':codComplicacion_id, 'codDiagnosticoPrincipal_id':codDiagnosticoPrincipal_id,'codDiagnosticoRelacionado_id':codDiagnosticoRelacionado_id, 'codProcedimiento_id':codProcedimiento_id,'codServicio_id':codServicio_id,'conceptoRecaudo_id':conceptoRecaudo_id,'finalidadTecnologiaSalud_id':finalidadTecnologiaSalud_id, 'grupoServicios_id':grupoServicios_id, 'modalidadGrupoServicioTecSal_id':modalidadGrupoServicioTecSal_id,'tipoDocumentoIdentificacion_id':tipoDocumentoIdentificacion_id,'usuarioRegistro_id':usuarioRegistro_id,'viaIngresoServicioSalud_id':viaIngresoServicioSalud_id,'ripsDetalle_id':ripsDetalle_id,  'itemFactura': itemFactura,'ripsTipos_id ':ripsTipos_id,'tipoPagoModerador_id':tipoPagoModerador_id , 'ripsTransaccion_id':ripsTransaccion_id
                 }})



    miConexionx.close()
    print("procedimientosRips "  , procedimientosRips)


    serialized1 = json.dumps(procedimientosRips,  default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_tablaRipsHospitalizacion(request, data):
    print("Entre load_data Hospitalizacion Rips")

    context = {}
    d = json.loads(data)


    envioRipsId = d['envioRipsId']
    print("envioRipsId = ", envioRipsId)


    hospitalizacionRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT  ripshosp.id id, "codPrestador", "fechaInicioAtencion", "numAutorizacion", "fechaEgreso", consecutivo, ripshosp."fechaRegistro", "causaMotivoAtencion_id", "codComplicacion_id", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id", "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id", "codDiagnosticoRelacionadoE3_id", "condicionDestinoUsuarioEgreso_id", ripshosp."usuarioRegistro_id" usuarioRegistro_id, "viaIngresoServicioSalud_id", "ripsDetalle_id", env."ripsTiposNotas_id", ripshosp."ripsTransaccion_id"  FROM public.rips_ripstransaccion ripstra , public.rips_ripshospitalizacion ripshosp , public.rips_ripsenvios env, rips_ripsdetalle det WHERE  env.id=det."ripsEnvios_id" AND det.id= ripshosp."ripsDetalle_id" AND env.id = ' + "'" + str(envioRipsId) + "'" + ' AND  ripstra.id = ripshosp."ripsTransaccion_id" '

    print(detalle)

    curx.execute(detalle)

    for id,  codPrestador, fechaInicioAtencion, numAutorizacion, fechaEgreso, consecutivo, fechaRegistro,  causaMotivoAtencion_id,  codComplicacion_id, codDiagnosticoCausaMuerte_id, codDiagnosticoPrincipal_id , codDiagnosticoPrincipalE_id,  codDiagnosticoRelacionadoE1_id, codDiagnosticoRelacionadoE2_id,        codDiagnosticoRelacionadoE3_id, condicionDestinoUsuarioEgreso_id, usuarioRegistro_id,  viaIngresoServicioSalud_id, ripsDetalle_id, ripsTiposNotas_id, ripsTransaccion_id in curx.fetchall():
        hospitalizacionRips.append(
            {"model": "rips.RipsHopsitalizacion", "pk": id, "fields":
                {'id': id, 'codPrestador': codPrestador , 'fechaInicioAtencion': fechaInicioAtencion,  'numAutorizacion':numAutorizacion, 'fechaEgreso':fechaEgreso,'consecutivo':consecutivo,'fechaRegistro':fechaRegistro,'causaMotivoAtencion_id':causaMotivoAtencion_id,
		'codComplicacion_id':codComplicacion_id, 'codDiagnosticoCausaMuerte_id':codDiagnosticoCausaMuerte_id, 'codDiagnosticoPrincipal_id':codDiagnosticoPrincipal_id, 'codDiagnosticoPrincipalE_id':codDiagnosticoPrincipalE_id,'codDiagnosticoRelacionadoE1_id':codDiagnosticoRelacionadoE1_id,'codDiagnosticoRelacionadoE2_id':codDiagnosticoRelacionadoE2_id,'codDiagnosticoRelacionadoE3_id':codDiagnosticoRelacionadoE3_id,
                 'condicionDestinoUsuarioEgreso_id':condicionDestinoUsuarioEgreso_id, 'usuarioRegistro_id':usuarioRegistro_id, 'viaIngresoServicioSalud_id':viaIngresoServicioSalud_id, 'ripsDetalle_id':ripsDetalle_id, 'ripsTiposNotas_id':ripsTiposNotas_id,'ripsTransaccion_id':ripsTransaccion_id
                 }})



    miConexionx.close()
    print("hospitalizacionRips "  , hospitalizacionRips)
    #context['usuariosRips'] = usuariosRips

    serialized1 = json.dumps(hospitalizacionRips,  default=str)

    return HttpResponse(serialized1, content_type='application/json')



def Load_tablaRipsUrgenciasObs(request, data):
    print("Entre load_data Urgencias Rips")

    context = {}
    d = json.loads(data)


    envioRipsId = d['envioRipsId']
    print("envioRipsId = ", envioRipsId)


    urgenciasObsRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT  ripsUrg.id, "codPrestador", "fechaInicioAtencion", "fechaEgreso", consecutivo, ripsUrg."fechaRegistro", "causaMotivoAtencion_id", "codDiagnosticoCausaMuerte_id", "codDiagnosticoPrincipal_id", "codDiagnosticoPrincipalE_id", "codDiagnosticoRelacionadoE1_id", "codDiagnosticoRelacionadoE2_id", "codDiagnosticoRelacionadoE3_id", "condicionDestinoUsuarioEgreso_id", ripsUrg."usuarioRegistro_id", "ripsDetalle_id", "ripsTipos_id", ripsUrg."ripsTransaccion_id"  FROM public.rips_ripstransaccion ripstra , public.rips_ripsurgenciasobservacion ripsUrg , public.rips_ripsenvios env, rips_ripsdetalle det WHERE  env.id=det."ripsEnvios_id" AND det.id= ripsUrg."ripsDetalle_id" AND env.id = ' + "'" + str(envioRipsId) + "'" + ' AND  ripstra.id = ripsUrg."ripsTransaccion_id" '

    print(detalle)

    curx.execute(detalle)

    for id,  codPrestador, fechaInicioAtencion,  fechaEgreso, consecutivo, fechaRegistro,  causaMotivoAtencion_id,  codDiagnosticoCausaMuerte_id, codDiagnosticoPrincipal_id , codDiagnosticoPrincipalE_id,  codDiagnosticoRelacionadoE1_id, codDiagnosticoRelacionadoE2_id,        codDiagnosticoRelacionadoE3_id, condicionDestinoUsuarioEgreso_id, usuarioRegistro_id,  ripsDetalle_id, ripsTipos_id, ripsTransaccion_id in curx.fetchall():
        urgenciasObsRips.append(
            {"model": "rips.RipsHopsitalizacion", "pk": id, "fields":
                {'id': id, 'codPrestador': codPrestador , 'fechaInicioAtencion': fechaInicioAtencion,   'fechaEgreso':fechaEgreso,'consecutivo':consecutivo,'fechaRegistro':fechaRegistro,'causaMotivoAtencion_id':causaMotivoAtencion_id,
		'codDiagnosticoCausaMuerte_id':codDiagnosticoCausaMuerte_id, 'codDiagnosticoPrincipal_id':codDiagnosticoPrincipal_id, 'codDiagnosticoPrincipalE_id':codDiagnosticoPrincipalE_id,'codDiagnosticoRelacionadoE1_id':codDiagnosticoRelacionadoE1_id,'codDiagnosticoRelacionadoE2_id':codDiagnosticoRelacionadoE2_id,'codDiagnosticoRelacionadoE3_id':codDiagnosticoRelacionadoE3_id,
                 'condicionDestinoUsuarioEgreso_id':condicionDestinoUsuarioEgreso_id, 'usuarioRegistro_id':usuarioRegistro_id, 'ripsDetalle_id':ripsDetalle_id, 'ripsTipos_id':ripsTipos_id,'ripsTransaccion_id':ripsTransaccion_id
                 }})



    miConexionx.close()
    print("urgenciasObsRips "  , urgenciasObsRips)
 
    serialized1 = json.dumps(urgenciasObsRips,  default=str)

    return HttpResponse(serialized1, content_type='application/json')




def Load_tablaRipsMedicamentos(request, data):
    print("Entre  Load_tablaRipsMedicamentos Rips")

    context = {}
    d = json.loads(data)


    envioRipsId = d['envioRipsId']
    print("envioRipsId = ", envioRipsId)


    medicamentosRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT  ripsmed.id, "codPrestador", "numAutorizacion", "idMIPRES", "fechaDispensAdmon", "nomTecnologiaSalud", "concentracionMedicamento", "cantidadMedicamento", "diasTratamiento", "numDocumentoIdentificacion", "vrUnitMedicamento", "vrServicio", "valorPagoModerador", "numFEVPagoModerador", consecutivo, ripsmed."fechaRegistro", "codDiagnosticoPrincipal_id", "codDiagnosticoRelacionado_id", "codTecnologiaSalud_id", "conceptoRecaudo_id", "formaFarmaceutica_id", "tipoDocumentoIdentificacion_id", "tipoMedicamento_id", "unidadMedida_id", "unidadMinDispensa_id", ripsmed."usuarioRegistro_id", "ripsDetalle_id", "itemFactura", "ripsTipos_id", ripsmed."ripsTransaccion_id" FROM public.rips_ripstransaccion ripstra , public.rips_ripsmedicamentos ripsmed , public.rips_ripsenvios env, rips_ripsdetalle det WHERE  env.id=det."ripsEnvios_id" AND det.id= ripsmed."ripsDetalle_id" AND env.id = ' + "'" + str(envioRipsId) + "'" + ' AND  ripstra.id = ripsmed."ripsTransaccion_id" '

    print(detalle)

    curx.execute(detalle)

    for  id, codPrestador, numAutorizacion, idMIPRES, fechaDispensAdmon, nomTecnologiaSalud, concentracionMedicamento, cantidadMedicamento, diasTratamiento, numDocumentoIdentificacion, vrUnitMedicamento, vrServicio, valorPagoModerador, numFEVPagoModerador, consecutivo, fechaRegistro, codDiagnosticoPrincipal_id, codDiagnosticoRelacionado_id, codTecnologiaSalud_id, conceptoRecaudo_id, formaFarmaceutica_id, tipoDocumentoIdentificacion_id, tipoMedicamento_id, unidadMedida_id, unidadMinDispensa_id, usuarioRegistro_id, ripsDetalle_id, itemFactura, ripsTipos_id, ripsTransaccion_id in curx.fetchall():
        medicamentosRips.append(
            {"model": "rips.RipsMedicamentos", "pk": id, "fields":
                {'id': id, 'codPrestador': codPrestador , 'numAutorizacion': numAutorizacion,  'idMIPRES':idMIPRES, 'fechaDispensAdmon':fechaDispensAdmon,'nomTecnologiaSalud':nomTecnologiaSalud,'concentracionMedicamento':concentracionMedicamento,'cantidadMedicamento':cantidadMedicamento,
		'diasTratamiento':diasTratamiento, 'numDocumentoIdentificacion':numDocumentoIdentificacion, 'vrUnitMedicamento':vrUnitMedicamento, 'vrServicio':vrServicio,'valorPagoModerador':valorPagoModerador,'numFEVPagoModerador':numFEVPagoModerador,'consecutivo':consecutivo,
                 'fechaRegistro':fechaRegistro, 'codDiagnosticoPrincipal_id':codDiagnosticoPrincipal_id, 'codDiagnosticoRelacionado_id':codDiagnosticoRelacionado_id, 'codTecnologiaSalud_id':codTecnologiaSalud_id, 'conceptoRecaudo_id':conceptoRecaudo_id,'formaFarmaceutica_id':formaFarmaceutica_id,'tipoDocumentoIdentificacion_id':tipoDocumentoIdentificacion_id,'tipoMedicamento_id':tipoMedicamento_id,'unidadMedida_id':unidadMedida_id,'unidadMinDispensa_id':unidadMinDispensa_id,'usuarioRegistro_id':usuarioRegistro_id,'ripsDetalle_id':ripsDetalle_id,'itemFactura':itemFactura,'ripsTipos_id':ripsTipos_id,'ripsTransaccion_id':ripsTransaccion_id
                 }})



    miConexionx.close()
    print("medicamentosRips "  , medicamentosRips)


    serialized1 = json.dumps(medicamentosRips,  default=str)

    return HttpResponse(serialized1, content_type='application/json')


def TraerJsonRips(request):
    print("Entre a TraerJsonRips")

    envioRipsId = request.POST['envioRipsId']
    print("envioRipsId =", envioRipsId)

    facturaId = request.POST['facturaId']
    print("facturaId =", facturaId)

    glosaId = request.POST['glosaId']
    print("glosaId =", glosaId)

    notaCreditoId = request.POST['notaCreditoId']
    print("notaCreditoId =", notaCreditoId)



    tipoRips = request.POST['tipoRips']
    print("tipoRips =", tipoRips)


    context = {}

    jsonRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (tipoRips == 'Factura'):

        detalle = 'select generaFacturaJSONBAK1('  + "'" + str(envioRipsId) + "','" + str(facturaId)  + "'," + "'" + str('FACTURA') + "',0" + ') valorJson'

    if (tipoRips == 'Glosa'):
        transaccionId = RipsTransaccion.objects.get(ripsEnvio_id=envioRipsId, numFactura=facturaId, numNota=glosaId)
        transaccion=transaccionId.id
        print("transaccion = " ,transaccion )

        detalle = 'select generaFacturaJSONBAK1('  + "'" + str(envioRipsId) + "','" + str(glosaId)  + "'," + "'" + str('GLOSA') + "'," + str(transaccion)   + ') valorJson'


    if (tipoRips == 'Nota Credito'):
        transaccionId = RipsTransaccion.objects.get(ripsEnvio_id=envioRipsId, numFactura=facturaId, numNota=notaCreditoId)
        transaccion=transaccionId.id
        print("transaccion = " ,transaccion )

        detalle = 'select generaFacturaJSONBAK1('  + "'" + str(envioRipsId) + "','" + str(notaCreditoId)  + "'," + "'" + str('NOTA CREDITO') + "'," + str(transaccion)   + ') valorJson'



    print(detalle)

    curx.execute(detalle)

    for valorJson in curx.fetchall():
        jsonRips.append(
            {"model": "rips_ripsdetalle", "pk": id, "fields":
                {'valorJson':valorJson }})

    miConexionx.close()
    print("jsonRips ", jsonRips)
    context['JsonRips'] = jsonRips

    serialized1 = json.dumps(jsonRips, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def TraerJsonEnvioRips(request):
    print("Entre a TraerJsonEnvioRips")

    envioRipsId = request.POST['envioRipsId']
    print("envioRipsId =", envioRipsId)

    tipoRips = request.POST['tipoRips']
    print("tipoRips =", tipoRips)

    context = {}

    jsonRips = []

    try:
        miConexion3 = None
        try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()
            # Primero creamos el despacho

            if (tipoRips == 'Factura'):

                detalle = 'select generaEnvioRipsJSON1('  + "'" + str(envioRipsId) + "','" + str('FACTURA') + "'" + ') valorJson'

            if (tipoRips == 'Glosa'):

                detalle = 'select generaEnvioRipsJSON1('  + "'" + str(envioRipsId) +  "','" + str('GLOSA') + "'" + ') valorJson'


            if (tipoRips == 'Nota Credito'):

                detalle = 'select generaEnvioRipsJSON1('  + "'" + str(envioRipsId) +  "','" + str('NOTA CREDITO') + "'" + ') valorJson'



            print(detalle)

            cur3.execute(detalle)

            for valorJson in cur3.fetchall():
                jsonRips.append(
                    {"model": "rips_ripsdetalle", "pk": id, "fields":
                        {'valorJson':valorJson }})


            miConexion3.close()
            print("jsonRips ", jsonRips)
            context['JsonRips'] = jsonRips

            serialized1 = json.dumps(jsonRips, default=str)

            return HttpResponse(serialized1, content_type='application/json')


        except psycopg2.DatabaseError as error:
            print("Entre por rollback", error)
            if miConexion3:
                print("Entro ha hacer el Rollback")
                miConexion3.rollback()

            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})

        finally:
            if miConexion3:
                cur3.close()
                miConexion3.close()

    except Exception as e:
        message_error = 'Debe seleccionar el envio Rips . Mensaje:' + str(e)
        print ("entre por qui", message_error)
        return JsonResponse({'success': False, 'Mensajes': message_error})


def BorrarDetalleRips(request):

    print ("Entre BorrarDetalleRips" )

    envioDetalleRipsId = request.POST["envioDetalleRipsId"]
    print ("el envioDetalleRipsId es = ", envioDetalleRipsId)

    envioDetalle = RipsDetalle.objects.get(id=envioDetalleRipsId)
    envio = RipsEnvios.objects.get(id=envioDetalle.ripsEnvios_id)
    print ("tipo de envio =", envio.ripsTiposNotas_id)
    tipoNota= RipsTiposNotas.objects.get(id=envio.ripsTiposNotas_id)
    print("tipo de envio en ripstiposnotas =", tipoNota.nombre)

    # Ojo primero debo borrar todos los rips generados a esa factura

    try:
        with transaction.atomic():


            RipsHospitalizacion.objects.filter(ripsDetalle_id=envioDetalleRipsId).delete()
            RipsMedicamentos.objects.filter(ripsDetalle_id=envioDetalleRipsId).delete()
            RipsProcedimientos.objects.filter(ripsDetalle_id=envioDetalleRipsId).delete()
            RipsRecienNacido.objects.filter(ripsDetalle_id=envioDetalleRipsId).delete()
            RipsUsuarios.objects.filter(ripsDetalle_id=envioDetalleRipsId).delete()
            RipsConsultas.objects.filter(ripsDetalle_id=envioDetalleRipsId).delete()
            RipsUrgenciasObservacion.objects.filter(ripsDetalle_id=envioDetalleRipsId).delete()


            # Primero debo conseguir la factura a borrar

            if (tipoNota.nombre == 'Factura'):

                a = Facturacion.objects.filter(id=envioDetalle.numeroFactura_id).update(ripsEnvio_id = '')

            if (tipoNota.nombre == 'Glosa'):

                a = Glosas.objects.filter(id=envioDetalle.glosa_id).update(ripsEnvio_id = '')

            if (tipoNota.nombre == 'Nota Credito'):

                a = NotasCredito.objects.filter(id=envioDetalle.notaCredito_id).update(ripsEnvio_id = '')


    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por esto :", e)
            message_error= str(e)
            return JsonResponse({'success': False, 'Mensajes': message_error})


    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'DELETE FROM rips_ripsdetalle WHERE id = '  + "'" + str(envioDetalleRipsId) + "'"
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        miConexion3.close()

        # Despues tengo que actualizar en la factura el campo enviorips_id a NULL , por ORM

        return JsonResponse({'success': True, 'Mensajes': 'Detalle de Rips eliminado !'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()



def GuardarRadicacionRips(request):

    print ("Entre GuardarRadiacionRips" )


    envioRipsId = request.POST['envioRipsId']
    print ("envioRipsId =", envioRipsId)

    fechaRadicacion = request.POST['fechaRadicacion']
    print ("fechaRadicacion =", fechaRadicacion)

    fechaRegistro = timezone.now()
    print("fechaRegistro = ", fechaRegistro)

    if (fechaRadicacion == None):
        print("Entre Fecha radiacion NONE")
        fechaRadicacion=fechaRegistro

    usuarioRadicacion= request.POST['username_id']
    print ("usuarioRegistro_id =", usuarioRadicacion)
    estadoReg = 'A'

    fechaRegistro = datetime.datetime.now()


    ripsEstadosId = RipsEstados.objects.get(nombre="RADICADO")
    print ("El estado es = ", ripsEstadosId.id )


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()
        comando = 'UPDATE rips_ripsEnvios  SET "fechaRadicacion" = ' + "'" +str(fechaRadicacion) + "'," + '"usuarioRadicacion_id" = ' + "'" + str(usuarioRadicacion) + "'," + '"ripsEstados_id" = ' + "'" + str(ripsEstadosId.id) + "'" +  ' WHERE id =' + str(envioRipsId)
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Fecha de radicacion actualizada satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


def load_dataRipsEnviados(request, data):
    print("Entre load_data Rips Enviados")

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

    ripsEnviados = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    #detalle = 'SELECT env.id,  env."fechaEnvio", env."fechaRespuesta", env."cantidadFacturas", env."cantidadPasaron", env."cantidadRechazadas",env."ripsEstados_id",  estrips.nombre estadoMinisterio, env."fechaRegistro", env."estadoReg", env."usuarioRegistro_id", env.empresa_id, env."sedesClinica_id" , sed.nombre nombreClinica, emp.nombre nombreEmpresa , pla.nombre nombreRegistra , tiposNotas.nombre tipoNota FROM public.rips_ripsenvios env, sitios_sedesclinica sed, facturacion_empresas emp, planta_planta pla , rips_ripstiposnotas tiposNotas , rips_ripsestados estrips where env."sedesClinica_id" = sed.id and env.empresa_id=emp.id AND pla.id = env."usuarioRegistro_id" AND env."ripsTiposNotas_id" = tiposNotas.id AND estrips.id = env."ripsEstados_id" AND env."sedesClinica_id" =' +  "'" + str(sede) + "' AND (estRips.nombre = " + "'" + str('ENVIADA') + "' or estRips.nombre = '" + str('RADICADO') + "'  or estRips.nombre = '" + str('RECHAZADA') + "')"
    detalle = 'SELECT env.id,  env."fechaEnvio",  env."fechaRadicacion",  env."fechaRespuesta", env."cantidadFacturas", env."cantidadPasaron", env."cantidadRechazadas",env."ripsEstados_id",  estrips.nombre estadoMinisterio, env."fechaRegistro", env."estadoReg", env."usuarioRegistro_id", env.empresa_id, env."sedesClinica_id" , sed.nombre nombreClinica, emp.nombre nombreEmpresa , pla.nombre nombreRegistra , tiposNotas.nombre tipoNota FROM public.rips_ripsenvios env, sitios_sedesclinica sed, facturacion_empresas emp, planta_planta pla , rips_ripstiposnotas tiposNotas , rips_ripsestados estrips where env."sedesClinica_id" = sed.id and env.empresa_id=emp.id AND pla.id = env."usuarioRegistro_id" AND env."ripsTiposNotas_id" = tiposNotas.id AND estrips.id = env."ripsEstados_id" AND env."sedesClinica_id" =' +  "'" + str(sede) + "' AND (estRips.nombre = " + "'" + str('ENVIADA') + "' or estRips.nombre = '" + str('CON RESPUESTA') + "' or estRips.nombre = '" + str('RADICADO') + "'  or estRips.nombre = '" + str('RECHAZADA') + "')"
    print(detalle)

    curx.execute(detalle)

    for id,  fechaEnvio, fechaRadicacion, fechaRespuesta, cantidadFacturas, cantidadPasaron, cantidadRechazadas, estadoPasoMinisterio, estadoMinisterio ,fechaRegistro, estadoReg, usuarioRegistro_id, empresa_id, sedesClinica_id, nombreClinica, nombreEmpresa, nombreRegistra, tipoNota in curx.fetchall():
        ripsEnviados.append(
            {"model": "rips.ripsEnvios", "pk": id, "fields":
                {'id': id, 'fechaEnvio': fechaEnvio,'fechaRadicacion':fechaRadicacion,  'fechaRespuesta': fechaRespuesta, 'cantidadFacturas': cantidadFacturas,
                 'cantidadPasaron': cantidadPasaron, 'cantidadRechazadas': cantidadRechazadas,
                 'estadoMinisterio': estadoMinisterio, 'estadoMinisterio':estadoMinisterio,  'fechaRegistro': fechaRegistro, 'estadoReg': estadoReg,'usuarioRegistro_id':usuarioRegistro_id, 'empresa_id':empresa_id, 'sedesClinica_id': sedesClinica_id, 'nombreClinica':nombreClinica, 'nombreEmpresa':nombreEmpresa,'nombreRegistra':nombreRegistra, 'tipoNota':tipoNota}})

    miConexionx.close()
    print("ripsEnviados"  , ripsEnviados)
    context['RipsEnviados'] = ripsEnviados

    serialized1 = json.dumps(ripsEnviados, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')


def GuardarRespuestaRips(request):

    print ("Entre GuardarRespuestaRips" )


    envioRipsId = request.POST['envioRipsId']
    print ("envioRipsId =", envioRipsId)

    fechaRespuesta = request.POST['fechaRespuesta']
    print ("fechaRespuesta =", fechaRespuesta)

    respuesta = request.POST['respuesta']
    print ("respuesta =", respuesta)

    cantidadPasaron = request.POST['cantidadPasaron']
    print ("cantidadPasaron =", cantidadPasaron)

    cantidadRechazadas = request.POST['cantidadRechazadas']
    print ("cantidadRechazadas =", cantidadRechazadas)


    rutaRespuestaJson = request.POST['rutaRespuestaJson']
    print ("rutaRespuestaJson =", rutaRespuestaJson)

    fechaRegistro = timezone.now()
    print("fechaRegistro = ", fechaRegistro)

    if (fechaRespuesta == ''):
        print("Entre Fecha respuesta NONE")
        fechaRespuesta=fechaRegistro

    usuarioRadicacion= request.POST['username_id']
    print ("usuarioRegistro_id =", usuarioRadicacion)
    estadoReg = 'A'

    fechaRegistro = datetime.datetime.now()


    ripsEstadosId = RipsEstados.objects.get(nombre="CON RESPUESTA")
    print ("El estado es = ", ripsEstadosId.id )


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()
        comando = 'UPDATE rips_ripsEnvios  SET "fechaRespuesta" = ' + "'" +str(fechaRespuesta) + "',respuesta = '" + str(respuesta) +"'," + '"cantidadPasaron" = ' + "'" + str(cantidadPasaron) + "'," + '"cantidadRechazadas" = ' + "'" + str(cantidadRechazadas) + "'," + '"usuarioRadicacion_id" = ' + "'" + str(usuarioRadicacion) + "'," + '"ripsEstados_id" = ' + "'" + str(ripsEstadosId.id) + "',"  + '"rutaRespuestaJson" = ' + "'" + str(rutaRespuestaJson) + "'" +  ' WHERE id =' + str(envioRipsId)
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Respuesta de Envio actualizada satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


def ReversarEnvioRips(request):

    print ("Entre ReversarEnvioRips" )


    ripsId = request.POST['ripsId']
    print ("ripsId =", ripsId)
    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    ripsEstadosId = RipsEstados.objects.get(nombre="SOLICITUD")
    print ("El estado es = ", ripsEstadosId.id )

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()
        comando = 'UPDATE rips_ripsEnvios  SET "fechaRespuesta" =  ' + "'" + str('') + "',respuesta = '',"   + '"fechaRadicacion" = ' + "'" + str('') + "'," + ' "ripsEstados_id" = ' + "'" + str(ripsEstadosId.id) + "'" + ' WHERE id =' + str(ripsId)
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Rips Reversado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()
