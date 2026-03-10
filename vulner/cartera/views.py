from django.shortcuts import render
import json
from django import forms
import cv2
import numpy as np
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.utils.timezone import now
from django.db.models import Avg, Max, Min, Sum
from django.utils import timezone

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
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle
from cartera.models import TiposPagos, FormasPagos, Pagos, PagosFacturas, GlosasDetalle, NotasCredito, NotasCreditoDetalle, NotasCreditoDetalleRips, GlosasDetalleRips
from triage.models import Triage
from clinico.models import Servicios
from rips.models  import RipsMedicamentos, RipsConsultas, RipsProcedimientos, RipsOtrosServicios
import pickle
from django.db import transaction, IntegrityError
from django.db.models import Sum
from django.db import transaction, IntegrityError

# Function to convert dictionary keys and values
def convert_keys_and_values(d):
    return {str(k) if isinstance(k, Decimal) else k: (float(v) if isinstance(v, Decimal) else v)
            for k, v in d.items()}


def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


# Create your views here.
def load_dataGlosas(request, data):
    print("Entre load_data Glosas")

    context = {}
    d = json.loads(data)

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
        'O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str(
        'TRIAGE') + "'" + ' group by ser.nombre'

    print("comando = ", comando)

    curt.execute(comando)
    print(comando)

    indicadores = []

    for id, nombre in curt.fetchall():
        indicadores.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(indicadores)

    context['Indicadores'] = indicadores

    # Fin combo Indicadores

    glosas = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT glo.id, "fechaRecepcion", "totalSoportado", "totalAceptado", "totalGlosa",  "totalNotasCredito", observaciones, glo."fechaRegistro", glo."estadoReg", glo."usuarioRegistro_id", "fechaRespuesta", "tipoGlosa_id", tipglo.nombre nombreTipoGlosa,  "usuarioRecepcion_id", "usuarioRespuesta_id", "estadoRadicacion_id", "estadoRecepcion_id", estGlosa.nombre estadoGlosaRecepcion, glo."sedesClinica_id", "ripsEnvio_id" FROM public.cartera_glosas glo, cartera_estadosglosas estGlosa , cartera_tiposglosas tipglo WHERE glo."sedesClinica_id" = ' + "'" + str(sede) + "'" + 'AND tipglo.id = glo."tipoGlosa_id" AND estGlosa.id =  glo."estadoRecepcion_id" AND estGlosa.tipo = ' + "'" + str('RECEPCION') + "'"

    print(detalle)

    curx.execute(detalle)

    for id,  fechaRecepcion,  totalSoportado, totalAceptado,totalGlosa, totalNotasCredito, observaciones, fechaRegistro, estadoReg,  usuarioRegistro_id, fechaRespuesta, tipoGlosa_id,nombreTipoGlosa, usuarioRecepcion_id, usuarioRespuesta_id,   estadoRadicacion_id , estadoRecepcion_id, estadoGlosaRecepcion,  sedesClinica_id, ripsEnvio_id in curx.fetchall():
        glosas.append(
            {"model": "cartera.glosas", "pk": id, "fields":
                {'id': id, 'fechaRecepcion': fechaRecepcion, 'totalSoportado': totalSoportado,'totalAceptado':totalAceptado,
                 'totalGlosa':totalGlosa,  'totalNotasCredito':totalNotasCredito, 'observaciones': observaciones, 'fechaRegistro': fechaRegistro,'estadoReg': estadoReg,  'usuarioRegistro_id': usuarioRegistro_id,  'fechaRespuesta': fechaRespuesta,
                 'tipoGlosa_id': tipoGlosa_id,'nombreTipoGlosa' :nombreTipoGlosa, 'usuarioRecepcion_id': usuarioRecepcion_id,'estadoGlosaRecepcion':estadoGlosaRecepcion, 'usuarioRespuesta_id': usuarioRespuesta_id,
                 'estadoRadicacion_id': estadoRadicacion_id, 'estadoRecepcion_id': estadoRecepcion_id,
                 'sedesClinica_id': sedesClinica_id,'ripsEnvio_id':ripsEnvio_id}})

    miConexionx.close()
    print("glosas "  , glosas)

    context['Glosas'] = glosas

    serialized1 = json.dumps(glosas,  default=str)

    return HttpResponse(serialized1, content_type='application/json')

def load_dataGlosasAdicionar(request, data):
    print("Entre load_data GlosasAdicionar")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    facturaId = d['facturaId']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    # Combo Indicadores

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT ser.nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
        sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + str(
        'O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str(
        'TRIAGE') + "'" + ' group by ser.nombre'

    print("comando = ", comando)

    curt.execute(comando)
    print(comando)

    indicadores = []

    for id, nombre in curt.fetchall():
        indicadores.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(indicadores)

    context['Indicadores'] = indicadores

    # Fin combo Indicadores

    glosasAdicionar = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT glo.id,  glo.factura_id,  "totalGlosa",  "fechaRecepcion", "saldoFactura", "totalSoportado", "totalAceptado",   "totalNotasCredito", conv.nombre nombreConvenio, "fechaRespuesta", "tipoGlosa_id", tipglo.nombre nombreTipoGlosa, "estadoRadicacion_id", "tipoGlosa_id" , "estadoRecepcion_id", convenio_id  FROM public.cartera_glosas glo, cartera_estadosglosas estGlosa , contratacion_convenios conv, cartera_tiposglosas tipglo WHERE glo."sedesClinica_id" = ' + "'" + str(sede) + "'" + 'AND tipglo.id = glo."tipoGlosa_id"   AND  conv.id = glo.convenio_id AND estGlosa.id =  glo."estadoRecepcion_id" AND estGlosa.tipo = ' + "'" + str('RECEPCION') + "' AND glo.factura_id = '" + str(facturaId) + "' ORDER BY glo.id"

    print(detalle)

    curx.execute(detalle)

    for id, factura_id,  totalGlosa,   fechaRecepcion, saldoFactura, totalSoportado, totalAceptado, totalNotasCredito, nombreConvenio,  fechaRespuesta, tipoGlosa_id,nombreTipoGlosa , estadoRadicacion_id, tipoGlosa_id , estadoRecepcion_id, convenio_id  in curx.fetchall():
        glosasAdicionar.append(
            {"model": "cartera.glosas", "pk": id, "fields":
                {'id': id, 'factura_id' : factura_id, 'totalGlosa':totalGlosa, 'fechaRecepcion': fechaRecepcion,'saldoFactura': saldoFactura,   'totalSoportado': totalSoportado,'totalAceptado':totalAceptado,
                   'totalNotasCredito':totalNotasCredito, 'nombreConvenio':nombreConvenio,  'fechaRespuesta': fechaRespuesta,
                 'tipoGlosa_id': tipoGlosa_id,'nombreTipoGlosa' :nombreTipoGlosa, 'estadoRadicacion_id':estadoRadicacion_id, 'tipoGlosa_id':tipoGlosa_id,'estadoRecepcion_id':estadoRecepcion_id, 'convenio_id ':convenio_id }})

    miConexionx.close()
    print("glosasAdicionar "  , glosasAdicionar)
    context['GlosasAdicionar'] = glosasAdicionar

    serialized1 = json.dumps(glosasAdicionar,  default=str)

    return HttpResponse(serialized1, content_type='application/json')


def GuardaGlosas(request):

    print ("Entre Guarda Glosas" )

    sedesClinica_id = request.POST['sedesClinica_id']
    print("sedesClinica_id =", sedesClinica_id)

    fechaRecepcion = request.POST["fechaRecepcion"]
    print("fechaRecepcion =", fechaRecepcion)


    observaciones = request.POST["observaciones"]
    print("observaciones =", observaciones)

    fechaRespuesta = request.POST["fechaRespuesta"]
    print("fechaRespuesta =", fechaRespuesta)


    tipoGlosa_id = request.POST["tipoGlosa_id"]
    print ("tipoGlosa_id =", tipoGlosa_id)

    totalGlosa = request.POST['totalGlosa']
    print ("totalGlosa =", totalGlosa)

    estadoRecepcion_id = request.POST['estadoRecepcion_id']
    print ("estadoRecepcion_id =", estadoRecepcion_id)

    serviciosAdministrativos_id = request.POST['serviciosAdministrativos_id']
    print ("serviciosAdministrativos_id =", serviciosAdministrativos_id)


    usuarioRegistro_id = request.POST['usuarioRegistro_id']
    print ("usuarioRegistro_id =", usuarioRegistro_id)

    estadoReg = 'A'

    fechaRegistro = timezone.now()


    miConexion3 = None

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
    cur3 = miConexion3.cursor()

    try:
        comando = 'INSERT INTO cartera_glosas ("fechaRecepcion", "totalNotasCredito", "totalGlosa" , "totalSoportado", "totalAceptado", observaciones, "fechaRegistro", "estadoReg", "usuarioRegistro_id",  "tipoGlosa_id", "usuarioRecepcion_id",   "estadoRadicacion_id", "estadoRecepcion_id","sedesClinica_id", "ripsEnvio_id" ,"serviciosAdministrativos_id", anulado) VALUES (' + "'" + str(fechaRecepcion) + "'" + ', 0, ' +  str(totalGlosa) +  ',0,0,' + "'" + str(observaciones) + "','" + str(fechaRegistro) + "','" + str(estadoReg) +  "','"  + str(usuarioRegistro_id) + "', '" + str(tipoGlosa_id) + "', '" + str(usuarioRegistro_id) +  "', null, '" + str(estadoRecepcion_id) + "', '" + str(sedesClinica_id)  + "',null,'" + str(serviciosAdministrativos_id) + "','N'" +  ')'

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Glosa creada satisfactoriamente!'})

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


def GuardaNotasCredito(request):

    print ("Entre GuardaNotasCredito" )

    sedesClinica_id = request.POST['sedesClinica_id']
    print("sedesClinica_id =", sedesClinica_id)

    fechaNota = request.POST["fechaNota"]
    print("fechaNota =", fechaNota)

    valorNota = request.POST["valorNota"]
    print("valorNota =", valorNota)

    descripcion = request.POST["descripcion"]
    print("descripcion =", descripcion)

    serviciosAdministrativos_id = request.POST['serviciosAdministrativos_id']
    print ("serviciosAdministrativos_id =", serviciosAdministrativos_id)

    usuarioRegistro_id = request.POST['usuarioRegistro_id']
    print ("usuarioRegistro_id =", usuarioRegistro_id)

    estadoReg = 'A'

    fechaRegistro = timezone.now()


    miConexion3 = None
    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
    cur3 = miConexion3.cursor()

    try:
        comando = 'INSERT INTO cartera_notascredito ("fechaNota",  "fechaRegistro", "estadoReg", "valorNota",  "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id", descripcion, anulado) VALUES (' + "'" + str(fechaNota) + "','" + str(fechaRegistro) + "','A','"   +  str(valorNota) + "','" + str(usuarioRegistro_id) +  "','" + str(sedesClinica_id)  + "','" + str(serviciosAdministrativos_id) + "','" + str(descripcion) +   "','N')"

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Nota credito  creada satisfactoriamente!'})

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


def GuardaNotasCreditoDetalle(request):

    print ("Entre GuardaNotasCreditoDetalle" )

    sedesClinica_id = request.POST['sedesClinica_id']
    print("sedesClinica_id =", sedesClinica_id)

    factura = request.POST['factura']
    print ("factura = ", factura)

    valorNota = request.POST['valorNota']
    print ("valorNota = ", valorNota)

    tipoNotaCredito = request.POST['tipoNotaCredito']
    print ("tipoNotaCredito = ", tipoNotaCredito)

    notaCredito = request.POST['notaCredito']
    print ("notaCredito  = ", notaCredito )

    username_id = request.POST['username_id']
    print ("username_id =", username_id)

    try:
       with transaction.atomic():

           valorParcialFacturaId = Facturacion.objects.get(id=factura)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por:", e)
            return JsonResponse({'success': False, 'Mensajes': 'Factura No existe'})
    
    finally:

        print("no haga nada")

    valorParcialFactura = valorParcialFacturaId.valorApagar
    valorParcialGlosas = valorParcialFacturaId.totalValorAceptado

    if (valorParcialGlosas == None):
            valorParcialGlosas=0

    valorParcialNotasCredito = valorParcialFacturaId.totalNotasCredito

    if (valorParcialNotasCredito == None):
            valorParcialNotasCredito=0

    valorParcialNotasCredito = float(valorParcialNotasCredito) + float(valorNota)

    valorParcialNotasDebito = valorParcialFacturaId.totalNotasDebito

    if (valorParcialNotasDebito == None):
            valorParcialNotasDebito=0

    saldoFactura = float(valorParcialFactura) -  float(valorParcialNotasCredito) + float(valorParcialNotasDebito) -  float(valorParcialGlosas)

    if (float(valorNota) >  float(saldoFactura)):

        return JsonResponse({'success': False, 'Mensajes': 'Valor de la Nota credito No debe ser mayor que el saldo de la factura'})


    notasCreditoId = NotasCredito.objects.get(id=notaCredito)
    print("notasCreditoId =" , notasCreditoId.valorNota)
    totalDetalleNotas = NotasCreditoDetalle.objects.filter(notaCredito_id=notaCredito).aggregate(Sum('valorNota'))
    print ("totalDetalleNotas = ", totalDetalleNotas['valorNota__sum'])


    if (float(notasCreditoId.valorNota) <  (float(totalDetalleNotas['valorNota__sum']) + float(valorNota) )):

        return JsonResponse({'success': False, 'Mensajes': 'Valor supera el total de la nota credito'})


    estadoReg = 'A'

    fechaRegistro = timezone.now()


    miConexion3 = None
    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
    cur3 = miConexion3.cursor()

    try:
        comando = 'INSERT INTO cartera_notascreditodetalle ("notaCredito_id", "factura_id","valorNota",   "fechaRegistro",   "usuarioRegistro_id", "estadoReg", anulado,"tiposNotasCredito_id") VALUES (' + "'" + str(notaCredito) + "','"   + str(factura) + "','" + str(valorNota) + "','"  + str(fechaRegistro) + "','" + str(username_id) +  "','A','N','" + str(tipoNotaCredito) + "'" + ')'

        print(comando)
        cur3.execute(comando)

        #comando = 'UPDATE facturacion_facturacion SET "totalNotasCredito" =  ' + "'" + str(valorParcialNotasCredito) + "'," + '"saldoFactura" = ' + "'" + str(saldoFactura) + "'"  + ' WHERE id = ' + "'" + str(factura) + "'"

        #print(comando)
        #cur3.execute(comando)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Nota credito Detalle  creada satisfactoriamente!'})

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



def GuardaGlosasAdicionar(request):

    print ("Entre Guarda Glosas Adicionar" )

    sedesClinica_id = request.POST['sedesClinica_id']
    print("sedesClinica_id =", sedesClinica_id)


    observaciones = request.POST["observaciones"]
    print("observaciones =", observaciones)

    glosaId = request.POST['glosaId']
    print ("glosaId =", glosaId)


    factura_id = request.POST['factura_id']
    print ("factura_id =", factura_id)


    totalGlosa = request.POST['totalGlosa']
    print ("totalGlosa =", totalGlosa)



    usuarioRegistro_id = request.POST['usuarioRegistro_id']
    print ("usuarioRegistro_id =", usuarioRegistro_id)

    estadoReg = 'A'

    fechaRegistro = timezone.now()


    miConexion3 = None
    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
    cur3 = miConexion3.cursor()

    try:
        comando = 'INSERT INTO cartera_glosasdetalle ("valorNotasCredito", glosa_id, "valorGlosa" , "valorSoportado", "valorAceptado", observaciones, "fechaRegistro", "estadoReg", "usuarioRegistro_id", factura_id, anulado) VALUES (' + "0,'" + str(glosaId) + "','" + str(totalGlosa) + "'" + ',0,0,' + "'" + str(observaciones) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(usuarioRegistro_id) + "', '" + str(factura_id) + "',"  + "'N'" +  ')'

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Factura Adicionada a la glosa satisfactoriamente !'})

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




def Load_tablaGlosasUsuarios(request, data):
    print("Entre load_data Usuarios Glosas")

    context = {}
    d = json.loads(data)


    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)

    facturaId = d['facturaId']
    print("facturaId = ", facturaId)


    usuariosRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT  ripsu.id, ripsu."tipoDocumentoIdentificacion", ripsu."tipoUsuario", ripsu."fechaNacimiento", ripsu."codSexo", ripsu."codZonaTerritorialResidencia_id", ripsu.incapacidad, ripsu.consecutivo, ripsu."fechaRegistro", ripsu."codMunicipioResidencia_id", ripsu."codPaisOrigen_id",ripsu."codPaisResidencia_id", ripsu."usuarioRegistro_id", ripsu."numDocumentoIdentificacion", ripsu."ripsDetalle_id", ripsu."ripsTransaccion_id"  FROM public.rips_ripsusuarios ripsu, public.rips_ripstransaccion ripstra  WHERE ripstra.id = ripsu."ripsTransaccion_id" and cast(ripstra."numFactura" as integer) =' + "'" + str(facturaId) + "'"

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




def Load_tablaGlosasDetalle(request, data):
    print("Entre  Load_tablaGlosasDetalle ACTUAL")

    context = {}
    d = json.loads(data)

    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)

    glosaId = d['glosaId']
    print("glosaId = ", glosaId)


    glosasDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT gloDet.id id, gloDet.factura_id,gloDet."valorGlosa", gloDet."valorSoportado", gloDet."valorAceptado", gloDet."valorNotasCredito", gloDet.id detGloId FROM cartera_glosas glo LEFT JOIN cartera_glosasdetalle gloDet ON (gloDet.glosa_id = glo.id) WHERE glo.id = ' + "'" + str(glosaId) + "'"

    print(detalle)

    curx.execute(detalle)

    for  id, factura_id, valorGlosa, valorSoportado, valorAceptado, valorNotasCredito , detGloId  in curx.fetchall():
        glosasDetalle.append(
            {"model": "rips.GlosasDetalle", "pk": id, "fields":
                {'id': id, 'factura_id':factura_id,  'valorGlosa': valorGlosa, 'valorSoportado': valorSoportado,   'valorAceptado': valorAceptado,
                 'valorNotasCredito': valorNotasCredito,'detGloId':detGloId}})

    miConexionx.close()


    serialized1 = json.dumps(glosasDetalle,  default=str)

    print("glosasDetalle = ", serialized1)

    return HttpResponse(serialized1, content_type='application/json')



def Load_tablaGlosasDetalleRips(request, data):
    print("Entre  Load_tablaGlosasDetalleRips")

    context = {}
    d = json.loads(data)


    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)

    glosaId = d['glosaId']
    print("glosaId = ", glosaId)

    gloDetId = d['gloDetId']
    print("gloDetId = ", gloDetId)

    gloDetId1 = GlosasDetalle.objects.get(id=gloDetId)

    print("facturaId = ", gloDetId1.factura_id)

    glosasDetalleRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select ' + "'" + str('MEDICAMENTOS') + "'" + ' tipo,med.id, med.consecutivo consec, med."itemFactura",cums.cum codigo,cums.nombre nombre,substring(mot.nombre,1,10) glosaNombre,med."vrServicio",  gloDetRips."valorGlosa",    gloDetRips."valorSoportado" valosSoportado,   gloDetRips."valorAceptado" ,    gloDetRips."valorNotasCredito" , gloDetRips.id gloDetRips, gloDet.glosa_id glosaId	FROM rips_ripstransaccion ripstra inner join rips_ripsmedicamentos med on (med."ripsTransaccion_id" = ripstra.id) 	inner join  rips_ripscums cums on (cums.id =med."codTecnologiaSalud_id" ) inner join cartera_glosasdetalle gloDet on (gloDet.id = ' + "'" + str(gloDetId) + "')" + ' left join cartera_glosasdetalleRips gloDetRips on (gloDetRips."glosasDetalle_id" =  gloDet.id and  gloDetRips."itemFactura" = med."itemFactura" AND gloDetRips."ripsMedicamentos_id" = med.id) left join cartera_motivosglosas mot on (mot.id = gloDetRips."motivoGlosa_id") where cast(ripstra."numFactura" as float) = ' + "'" + str(gloDetId1.factura_id) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' UNION select ' + "'" + str('PROCEDIMIENTOS') + "'" + ' tipo, proc.id, proc.consecutivo consec, proc."itemFactura", exa."codigoCups" codigo,	exa.nombre nombre,  substring(mot.nombre,1,10)  glosaNombre,proc."vrServicio",gloDetRips."valorGlosa",    gloDetRips."valorSoportado" valosSoportado,   gloDetRips."valorAceptado" ,    gloDetRips."valorNotasCredito" , gloDetRips.id gloDetRipsId , gloDet.glosa_id glosaId  FROM  rips_ripstransaccion ripstra inner join  rips_ripsprocedimientos proc on (proc."ripsTransaccion_id" = ripstra.id) inner join clinico_examenes exa on ( exa.id =proc."codProcedimiento_id" ) inner join cartera_glosasdetalle gloDet on (gloDet.id = ' + "'" + str(gloDetId) + "')" + ' left join cartera_glosasdetalleRips gloDetRips on (gloDetRips."glosasDetalle_id" =  gloDet.id and  gloDetRips."itemFactura" = proc."itemFactura" AND gloDetRips."ripsProcedimientos_id" = proc.id) left join cartera_motivosglosas mot on (mot.id = gloDetRips."motivoGlosa_id") where cast(ripstra."numFactura" as float) = ' + "'" + str(gloDetId1.factura_id) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' UNION select ' + "'" + str('CONSULTAS') + "'" + ' tipo, cons.id, cons.consecutivo consec, cons."itemFactura", exa."codigoCups" codigo,	exa.nombre nombre, substring(mot.nombre,1,10)  glosaNombre,cons."vrServicio",	gloDetRips."valorGlosa",    gloDetRips."valorSoportado" valosSoportado,   gloDetRips."valorAceptado" ,    gloDetRips."valorNotasCredito", gloDetRips.id gloDetRipsId , gloDet.glosa_id glosaId 	FROM rips_ripstransaccion  ripstra inner join  rips_ripsconsultas cons on (cons."ripsTransaccion_id" = ripstra.id) inner join clinico_examenes exa on ( exa.id =cons."codConsulta_id" ) inner join cartera_glosasdetalle gloDet on (gloDet.id = ' + "'" + str(gloDetId) + "')" + ' left join cartera_glosasdetalleRips gloDetRips on (gloDetRips."glosasDetalle_id" =  gloDet.id and  gloDetRips."itemFactura" = cons."itemFactura" AND gloDetRips."ripsConsultas_id" = cons.id) left join cartera_motivosglosas mot on (mot.id = gloDetRips."motivoGlosa_id")	 where cast(ripstra."numFactura" as float) = ' + "'" + str(gloDetId1.factura_id) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' UNION	select ' + "'" + str('OTROS SERVICIOS') + "'" + ' tipo, serv.id, serv.consecutivo consec, serv."itemFactura", serv."nomTecnologiaSalud" codigo, exa.nombre nombre, substring(mot.nombre,1,10)  glosaNombre, serv."vrServicio",	gloDetRips."valorGlosa",    gloDetRips."valorSoportado" valosSoportado,   gloDetRips."valorAceptado" ,    gloDetRips."valorNotasCredito", gloDetRips.id gloDetRipsId  , gloDet.glosa_id glosaId FROM rips_ripstransaccion  ripstra inner join  rips_ripsotrosservicios serv on (serv."ripsTransaccion_id" = ripstra.id) left join clinico_examenes exa on ( exa.id =serv."codTecnologiaSalud_id" ) inner join cartera_glosasdetalle gloDet on (gloDet.id = ' + "'" + str(gloDetId) + "')" + ' left join cartera_glosasdetalleRips gloDetRips on (gloDetRips."glosasDetalle_id" =  gloDet.id and  gloDetRips."itemFactura" = serv."itemFactura" AND gloDetRips."ripsOtrosServicios_id" = serv.id) left join cartera_motivosglosas mot on (mot.id = gloDetRips."motivoGlosa_id")	where cast(ripstra."numFactura" as float) = ' + "'" + str(gloDetId1.factura_id) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' order by 1,4'

    print(detalle)

    curx.execute(detalle)

    #for  tipo, id, consec, itemFactura, codigo, nombre,   glosaNombre,vrServicio,  valorGlosado,vAceptado, valorSoportado , notasCreditoGlosa , valorGlosa, valorSoportado2 , valorAceptado, valorNotasCredito in curx.fetchall():
    for tipo, id, consec, itemFactura, codigo, nombre, glosaNombre, vrServicio, valorGlosa, valorSoportado, valorAceptado, valorNotasCredito , detGloId , glosaId in curx.fetchall():
        glosasDetalleRips.append(
            {"model": "rips.GlosasDetalle", "pk": id, "fields":
                {'tipo':tipo, 'id': id, 'consec':consec,  'itemFactura': itemFactura ,'codigo': codigo, 'nombre': nombre,'glosaNombre':glosaNombre,'vrServicio':vrServicio,
                 'valorGlosa': valorGlosa, 'valorSoportado': valorSoportado,   'valorAceptado': valorAceptado,
                 'valorNotasCredito': valorNotasCredito,'detGloId':detGloId,'glosaId':glosaId }})

    miConexionx.close()


    serialized1 = json.dumps(glosasDetalleRips,  default=str)

    print("glosasDetalleRips = ", serialized1)

    return HttpResponse(serialized1, content_type='application/json')



def ConsultaGlosasDetalle(request):
    
    print("Entre consultaGlosasDetalle")

    id  = request.POST['id']
    print("id  =", id )

    tipo  = request.POST["tipo"]
    print("tipo  =", tipo )


    medicamentosRipsUnRegistro = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (tipo == 'MEDICAMENTOS'):

        #detalle = 'SELECT ' + "'" + str('MEDICAMENTOS') + "'" + ' tipo, med.id,"itemFactura", "nomTecnologiaSalud" codigo, cums.nombre nombre, "vrServicio",	consecutivo,  "cantidadGlosada", "cantidadAceptada", "cantidadSoportado", "valorGlosado","vAceptado","valorSoportado","motivoGlosa_id", "notasCreditoGlosa" FROM public.rips_ripsmedicamentos med, public.rips_ripscums cums where med.id= ' + "'" + str(id) + "'" + ' and cums.id ="codTecnologiaSalud_id"'
        detalle = 'SELECT ' + "'" + str('MEDICAMENTOS') + "'" + ' tipo, med.id,med."itemFactura", med."nomTecnologiaSalud" codigo, cums.nombre nombre, med."vrServicio",	med.consecutivo,  detGlo."valorGlosa",detGlo."valorAceptado",detGlo."valorSoportado",  detGlo."motivoGlosa_id",   mot.nombre motivo,	detGlo."valorNotasCredito" 	FROM public.rips_ripsmedicamentos med inner join public.rips_ripscums cums  on (cums.id =med."codTecnologiaSalud_id") left join cartera_glosasdetalle detGlo on (detGlo."ripsMedicamentos_id" =med.id) left join cartera_motivosglosas mot on (mot.id = detGlo."motivoGlosa_id" ) where med.id= ' + "'" + str(id) + "'"

    if (tipo == 'PROCEDIMIENTOS'):


        detalle = 'SELECT ' + "'" + str('PROCEDIMIENTOS') + "'" + ' tipo, proc.id,proc."itemFactura", proc."codProcedimiento_id" codigo, exa.nombre nombre, proc."vrServicio",	proc.consecutivo,  detGlo."valorGlosa",detGlo."valorAceptado",detGlo."valorSoportado",  detGlo."motivoGlosa_id",   mot.nombre motivo,	detGlo."valorNotasCredito" 	FROM public.rips_ripsprocedimientos proc inner join clinico_examenes exa  on (exa.id =proc."codProcedimiento_id") left join cartera_glosasdetalle detGlo on (detGlo."ripsProcedimientos_id" =proc.id) left join cartera_motivosglosas mot on (mot.id = detGlo."motivoGlosa_id" ) where proc.id= ' + "'" + str(id) + "'"

    if (tipo == 'CONSULTAS'):

        detalle = 'SELECT ' + "'" + str('CONSULTAS') + "'" + ' tipo, med.id,med."itemFactura", med."nomTecnologiaSalud" codigo, cums.nombre nombre, med."vrServicio",	med.consecutivo,  detGlo."valorGlosa",detGlo."valorAceptado",detGlo."valorSoportado",  detGlo."motivoGlosa_id",   mot.nombre motivo,	detGlo."valorNotasCredito" 	FROM public.rips_ripsconsultas med inner join public.rips_ripscums cums  on (cums.id =med."codTecnologiaSalud_id") left join cartera_glosasdetalle detGlo on (detGlo."ripsConsultas_id" =med.id) left join cartera_motivosglosas mot on (mot.id = detGlo."motivoGlosa_id" ) where med.id= ' + "'" + str(id) + "'"

    if (tipo == 'OTROS SERVICIOS'):


        detalle = 'SELECT ' + "'" + str('OTROS SERVICIOS') + "'" + ' tipo, med.id,med."itemFactura", med."nomTecnologiaSalud" codigo, cums.nombre nombre, med."vrServicio",	med.consecutivo,  detGlo."valorGlosa",detGlo."valorAceptado",detGlo."valorSoportado",  detGlo."motivoGlosa_id",   mot.nombre motivo,	detGlo."valorNotasCredito" 	FROM public.rips_ripsotrosservicios med inner join public.rips_ripscums cums  on (cums.id =med."codTecnologiaSalud_id") left join cartera_glosasdetalle detGlo on (detGlo."ripsOtrosServicios_id" =med.id) left join cartera_motivosglosas mot on (mot.id = detGlo."motivoGlosa_id" ) where med.id= ' + "'" + str(id) + "'"


    print(detalle)

    curx.execute(detalle)

    for tipo, id, itemFactura, codigo, nombre,  vrServicio,  consecutivo, valorGlosa,valorAceptado, valorSoportado , motivoGlosa_id, motivo,  valorNotasCredito   in curx.fetchall():
     medicamentosRipsUnRegistro.append(
            {"model": "rips.ripsmedicamentos", "pk": id, "fields":
                {'tipo':tipo, 'id': id, 'itemFactura': itemFactura , 'codigo': codigo,  'nombre':nombre,
		  'vrServicio':vrServicio,'consecutivo':consecutivo,'valorGlosa':valorGlosa,'valorAceptado':valorAceptado,
                 'valorSoportado':valorSoportado,'motivoGlosa_id':motivoGlosa_id,'motivo':motivo, 'valorNotasCredito':valorNotasCredito
                 }})


    miConexionx.close()
    print("medicamentosRipsUnRegistro "  , medicamentosRipsUnRegistro)
    
    serialized1 = json.dumps(medicamentosRipsUnRegistro, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def ConsultaGlosasDetalleRips(request):
    print("Entre consultaGlosasDetalleRips")

    id = request.POST['id']
    print("id  =", id)

    tipo = request.POST["tipo"]
    print("tipo  =", tipo)

    medicamentosRipsUnRegistro = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (tipo == 'MEDICAMENTOS'):
        # detalle = 'SELECT ' + "'" + str('MEDICAMENTOS') + "'" + ' tipo, med.id,"itemFactura", "nomTecnologiaSalud" codigo, cums.nombre nombre, "vrServicio",	consecutivo,  "cantidadGlosada", "cantidadAceptada", "cantidadSoportado", "valorGlosado","vAceptado","valorSoportado","motivoGlosa_id", "notasCreditoGlosa" FROM public.rips_ripsmedicamentos med, public.rips_ripscums cums where med.id= ' + "'" + str(id) + "'" + ' and cums.id ="codTecnologiaSalud_id"'
        detalle = 'SELECT ' + "'" + str(
            'MEDICAMENTOS') + "'" + ' tipo, med.id,med."itemFactura", med."nomTecnologiaSalud" codigo, cums.nombre nombre, med."vrServicio",	med.consecutivo,  detGloRips."valorGlosa",detGloRips."valorAceptado",detGloRips."valorSoportado",  detGloRips."motivoGlosa_id",   mot.nombre motivo,	detGloRips."valorNotasCredito" 	FROM public.rips_ripsmedicamentos med inner join public.rips_ripscums cums  on (cums.id =med."codTecnologiaSalud_id") left join cartera_glosasdetalleRips detGloRips on (detGloRips."ripsMedicamentos_id" =med.id) left join cartera_motivosglosas mot on (mot.id = detGloRips."motivoGlosa_id" ) where med.id= ' + "'" + str(
            id) + "'"

    if (tipo == 'PROCEDIMIENTOS'):
        detalle = 'SELECT ' + "'" + str(
            'PROCEDIMIENTOS') + "'" + ' tipo, proc.id,proc."itemFactura", proc."codProcedimiento_id" codigo, exa.nombre nombre, proc."vrServicio",	proc.consecutivo,  detGloRips."valorGlosa",detGloRips."valorAceptado",detGloRips."valorSoportado",  detGloRips."motivoGlosa_id",   mot.nombre motivo,detGloRips."valorNotasCredito" FROM public.rips_ripsprocedimientos proc inner join clinico_examenes exa  on (exa.id =proc."codProcedimiento_id") left join cartera_glosasdetalleRips detGloRips on (detGloRips."ripsProcedimientos_id" =proc.id) left join cartera_motivosglosas mot on (mot.id = detGloRips."motivoGlosa_id" ) where proc.id= ' + "'" + str(
            id) + "'"

    if (tipo == 'CONSULTAS'):
        detalle = 'SELECT ' + "'" + str(
            'CONSULTAS') + "'" + ' tipo, med.id,med."itemFactura", med."nomTecnologiaSalud" codigo, cums.nombre nombre, med."vrServicio",	med.consecutivo,  detGloRips."valorGlosa",detGloRips."valorAceptado",detGloRips."valorSoportado", detGloRips."motivoGlosa_id",   mot.nombre motivo,	detGloRips."valorNotasCredito" 	FROM public.rips_ripsconsultas med inner join public.rips_ripscums cums  on (cums.id =med."codTecnologiaSalud_id") left join cartera_glosasdetalleRips detGloRips on (detGloRips."ripsConsultas_id" =med.id) left join cartera_motivosglosas mot on (mot.id = detGloRips."motivoGlosa_id" ) where med.id= ' + "'" + str(
            id) + "'"

    if (tipo == 'OTROS SERVICIOS'):
        detalle = 'SELECT ' + "'" + str(
            'OTROS SERVICIOS') + "'" + ' tipo, med.id,med."itemFactura", med."nomTecnologiaSalud" codigo, cums.nombre nombre, med."vrServicio",	med.consecutivo,  detGloRips."valorGlosa",detGloRips."valorAceptado",detGloRips."valorSoportado", detGloRips."motivoGlosa_id",   mot.nombre motivo,	detGloRips."valorNotasCredito" 	FROM public.rips_ripsotrosservicios med inner join public.rips_ripscums cums  on (cums.id =med."codTecnologiaSalud_id") left join cartera_glosasdetalleRips detGloRips on (detGloRips."ripsOtrosServicios_id" =med.id) left join cartera_motivosglosas mot on (mot.id = detGloRips."motivoGlosa_id" ) where med.id= ' + "'" + str(
            id) + "'"

    print(detalle)

    curx.execute(detalle)

    for tipo, id, itemFactura, codigo, nombre, vrServicio, consecutivo, valorGlosa, valorAceptado, valorSoportado, motivoGlosa_id, motivo, valorNotasCredito in curx.fetchall():
        medicamentosRipsUnRegistro.append(
            {"model": "rips.ripsmedicamentos", "pk": id, "fields":
                {'tipo': tipo, 'id': id, 'itemFactura': itemFactura, 'codigo': codigo, 'nombre': nombre,
                 'vrServicio': vrServicio, 'consecutivo': consecutivo, 'valorGlosa': valorGlosa,
                 'valorAceptado': valorAceptado,
                 'valorSoportado': valorSoportado, 'motivoGlosa_id': motivoGlosa_id, 'motivo': motivo,
                 'valorNotasCredito': valorNotasCredito
                 }})

    miConexionx.close()
    print("medicamentosRipsUnRegistro ", medicamentosRipsUnRegistro)

    serialized1 = json.dumps(medicamentosRipsUnRegistro, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def GuardarGlosasDetalleRips(request):

    print ("Entre Guardar Glosas Detalle" )

    tipoGloDet = request.POST["tipoGloDetRips"]
    print("tipoGloDet =", tipoGloDet)

    post_idGloDet = request.POST["post_idGloDet"]
    print("post_idGloDet =", post_idGloDet)

    glosaDetId = GlosasDetalle.objects.get(id=post_idGloDet)
    glosaId = glosaDetId.glosa_id

    print ("glosaId =", glosaId)

    ripsId = request.POST['glosaGloDetRips']
    print ("ripsId =", ripsId)

    motivoGlosa_id= request.POST["motivoGlosa_idGloDetRips"]
    print ("motivoGlosa_id =", motivoGlosa_id)

    valorGlosado = request.POST['valorGlosadoGloDetRips']

    if (valorGlosado==''):
        valorGlosado=0.0

    valorGlosadox = valorGlosado
    print ("valorGlosado =", valorGlosado)

    if (valorGlosado==''):
        valorGlosado=0.0

    vAceptado = float(request.POST['vAceptadoGloDetRips'])
    print ("vAceptado =", vAceptado)

    if (vAceptado==''):
        vAceptado=0.0

    vAceptadox = vAceptado

    valorSoportado = request.POST['valorSoportadoGloDetRips']
    print ("valorSoportado=",valorSoportado)

    if (valorSoportado==''):
        valorSoportado=0.0

    valorSoportadox = valorSoportado

    notasCreditoGlosa = request.POST['notasCreditoGlosaGloDetRips']
    print ("notasCreditoGlosa=",notasCreditoGlosa)


    if (notasCreditoGlosa==''):
        notasCreditoGlosa=0.0

    notasCreditoGlosax = notasCreditoGlosa

    itemFacturaGloDet = request.POST['itemFacturaGloDetRips']
    print ("itemFacturaGloDet=", itemFacturaGloDet)

    vrServicioGloDet = request.POST['vrServicioGloDetRips']
    print ("vrServicioGloDet=", vrServicioGloDet)

    observacionesGloDet = request.POST['observacionesGloDetRips']
    print ("observacionesGloDet=", observacionesGloDet)

    username_id = request.POST['username_id']
    print ("username_id=", username_id)

    estadoReg = 'A'

    fechaRegistro = timezone.now()

    if ( float(valorGlosado) > float(vrServicioGloDet) ):
        print ("Entre 1")
        print("valorGlosado=", valorGlosado)
        print("vrServicioGloDet=", vrServicioGloDet)
        return JsonResponse({'success': False, 'Error' :'Si', 'Mensajes': 'Valor Glosa mayor que el valor del servicio!'})

    if ( float(valorSoportado) > float(vrServicioGloDet) ):
        print ("Entre 4")
        return JsonResponse({'success': False, 'Error' :'Si','Mensajes': 'Valor Soportado mayor que el valor del servicio!'})

    if ( float(vAceptado) > float(vrServicioGloDet) ):
        print ("Entre 5")
        return JsonResponse({'success': False, 'Error' :'Si','Mensajes': 'Valor aceptado mayor que el valor del servicio!'})


    if (float(vrServicioGloDet) < float(vAceptado)):
        print("Entre 3")
        return JsonResponse(
            {'success': False, 'Error': 'Si', 'Mensajes': 'Valor aceptado no puede ser mayor que el valor glosado!'})

    if (float(notasCreditoGlosa) > float(valorGlosado)):
        print("Entre 3")
        return JsonResponse(
            {'success': False, 'Error': 'Si', 'Mensajes': 'La nota credito no puede ser mayor que el valor glosado!'})



    if ( float((float(vAceptado) + float(valorSoportado))) > float(vrServicioGloDet) ):
        print ("Entre 3")
        return JsonResponse({'success': False, 'Error' :'Si','Mensajes': 'Valor soportado mas valor aceptado mayor que el valor del servicio!'})



    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            cur3 = miConexion3.cursor()

            hayRegistro = 0

            try:
                with transaction.atomic():

                    existeRegistro = GlosasDetalleRips.objects.get(glosdetalle_id=post_idGloDet, itemFactura=itemFacturaGloDet)
                    hayRegistro = existeRegistro.id

            except Exception as e:
                    # Aquí ya se hizo rollback automáticamente
                    print("Se hizo rollback por PRONO SE HACE NADA:", e)
                    hayRegistro=0

            finally:
                    print("No haga nada")


            if tipoGloDet == 'MEDICAMENTOS' :

                if (hayRegistro == 0):

	                comando = 'INSERT INTO cartera_glosasdetalleRips ( "itemFactura", "valorServicio", "valorGlosa", "valorSoportado", "valorAceptado","valorNotasCredito", observaciones, "estadoReg", "glosasDetalle_id", "motivoGlosa_id", "usuarioRegistro_id", "fechaRegistro", "ripsId",  anulado, "ripsMedicamentos_id"	) VALUES ( ' +  "'" + str(itemFacturaGloDet) + "','" + str(vrServicioGloDet) + "','" + str(valorGlosado)  + "','" + str(valorSoportado) + "','" + str(vAceptado) + "','" + str(notasCreditoGlosa) + "','" + str(observacionesGloDet) + "','A','" + str(post_idGloDet) + "','" + str(motivoGlosa_id) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','" + str(ripsId) + "','N','" + str(ripsId) + "')"

                else:

                    comando = 'UPDATE cartera_glosasdetalleRips SET "itemFactura" = ' +  "'" + str(itemFacturaGloDet) + "'," + ' "valorServicio"  = ' + "'"  + str(vrServicioGloDet) + "'," + ' "valorGlosa" = ' + "'" + str(valorGlosado) + "'," + ' "valorSoportado" = ' + "'" + str(valorSoportado) + "'," + ' "valorAceptado" = ' + "'" + str(vAceptado) + "', " + ' "valorNotasCredito" = ' + "'" + str(notasCreditoGlosa) + "'," + ' observaciones = ' + "'" + str(observacionesGloDet) + "'," + '"estadoReg" = ' + "'A'," + ' "motivoGlosa_id" = ' + "'" + str(motivoGlosa_id) + "'," + ' "usuarioRegistro_id" = ' + "'" + str(username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(fechaRegistro) + "'," + '"ripsId" = ' + "'" + str(ripsId) + "'," + ' anulado = ' + "'N'," + ' "ripsMedicamentos_id" = ' + "'" + str(ripsId) + "' WHERE glosa_id = " + "'" + str(glosaId) + "'" + ' AND "itemFactura" = ' + "'" + str(itemFacturaGloDet) + "'"


            if tipoGloDet == 'PROCEDIMIENTOS' :

                if (hayRegistro == 0):

                    comando = 'INSERT INTO cartera_glosasdetalleRips ( "itemFactura", "valorServicio", "valorGlosa", "valorSoportado", "valorAceptado","valorNotasCredito", observaciones, "estadoReg", "glosasDetalle_id", "motivoGlosa_id", "usuarioRegistro_id", "fechaRegistro", "ripsId",  anulado, "ripsProcedimientos_id"	) VALUES ( ' +  "'" + str(itemFacturaGloDet) + "','" + str(vrServicioGloDet) + "','" + str(valorGlosado)  + "','" + str(valorSoportado) + "','" + str(vAceptado) + "','" + str(notasCreditoGlosa) + "','" + str(observacionesGloDet) + "','A','" + str(post_idGloDet) + "','" + str(motivoGlosa_id) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','" + str(ripsId) + "','N','" + str(ripsId) + "')"

                else:

                    comando = 'UPDATE cartera_glosasdetalleRips SET "itemFactura" = ' +  "'" + str(itemFacturaGloDet) + "'," + ' "valorServicio"  = ' + "'"  + str(vrServicioGloDet) + "'," + ' "valorGlosa" = ' + "'" + str(valorGlosado) + "'," + ' "valorSoportado" = ' + "'" + str(valorSoportado) + "'," + ' "valorAceptado" = ' + "'" + str(vAceptado) + "', " + ' "valorNotasCredito" = ' + "'" + str(notasCreditoGlosa) + "'," + ' observaciones = ' + "'" + str(observacionesGloDet) + "'," + '"estadoReg" = ' + "'A'," + ' "motivoGlosa_id" = ' + "'" + str(motivoGlosa_id) + "'," + ' "usuarioRegistro_id" = ' + "'" + str(username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(fechaRegistro) + "'," + '"ripsId" = ' + "'" + str(ripsId) + "'," + ' anulado = ' + "'N'," + ' "ripsProcedimientos_id" = ' + "'" + str(ripsId) + "' WHERE glosa_id = " + "'" + str(glosaId) + "'" + ' AND "itemFactura" = ' + "'" + str(itemFacturaGloDet) + "'"

	
            if tipoGloDet == 'CONSULTAS' :

                if (hayRegistro == 0):


	                comando = 'INSERT INTO cartera_glosasdetalleRips ( "itemFactura", "valorServicio", "valorGlosa", "valorSoportado", "valorAceptado","valorNotasCredito", observaciones, "estadoReg", "glosasDetalle_id", "motivoGlosa_id", "usuarioRegistro_id", "fechaRegistro", "ripsId",  anulado, "ripsConsultas_id"	) VALUES ( ' +  "'" + str(itemFacturaGloDet) + "','" + str(vrServicioGloDet) + "','" + str(valorGlosado)  + "','" + str(valorSoportado) + "','" + str(vAceptado) + "','" + str(notasCreditoGlosa) + "','" + str(observacionesGloDet) + "','A','" + str(post_idGloDet) + "','" + str(motivoGlosa_id) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','" + str(ripsId) + "','N','" + str(ripsId) + "')"

                else:

                    comando = 'UPDATE cartera_glosasdetalleRips SET "itemFactura" = ' +  "'" + str(itemFacturaGloDet) + "'," + ' "valorServicio"  = ' + "'"  + str(vrServicioGloDet) + "'," + ' "valorGlosa" = ' + "'" + str(valorGlosado) + "'," + ' "valorSoportado" = ' + "'" + str(valorSoportado) + "'," + ' "valorAceptado" = ' + "'" + str(vAceptado) + "', " + ' "valorNotasCredito" = ' + "'" + str(notasCreditoGlosa) + "'," + ' observaciones = ' + "'" + str(observacionesGloDet) + "'," + '"estadoReg" = ' + "'A'," + ' "motivoGlosa_id" = ' + "'" + str(motivoGlosa_id) + "'," + ' "usuarioRegistro_id" = ' + "'" + str(username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(fechaRegistro) + "'," + '"ripsId" = ' + "'" + str(ripsId) + "'," + ' anulado = ' + "'N'," + ' "ripsConsultas_id" = ' + "'" + str(ripsId) + "' WHERE glosa_id = " + "'" + str(glosaId) + "'" + ' AND "itemFactura" = ' + "'" + str(itemFacturaGloDet) + "'"



            if tipoGloDet == 'OTROS SERVICIOS' :

                if (hayRegistro == 0):

	                comando = 'INSERT INTO cartera_glosasdetalleRips ( "itemFactura", "valorServicio", "valorGlosa", "valorSoportado", "valorAceptado","valorNotasCredito", observaciones, "estadoReg", "glosasDetalle_id", "motivoGlosa_id", "usuarioRegistro_id", "fechaRegistro", "ripsId",  anulado, "ripsOtrosServicios_id"	) VALUES ( ' +  "'" + str(itemFacturaGloDet) + "','" + str(vrServicioGloDet) + "','" + str(valorGlosado)  + "','" + str(valorSoportado) + "','" + str(vAceptado) + "','" + str(notasCreditoGlosa) + "','" + str(observacionesGloDet) + "','A','" + str(post_idGloDet) + "','" + str(motivoGlosa_id) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','" + str(ripsId) + "','N','" + str(ripsId) + "')"

                else:

                    comando = 'UPDATE cartera_glosasdetalleRips SET "itemFactura" = ' +  "'" + str(itemFacturaGloDet) + "'," + ' "valorServicio"  = ' + "'"  + str(vrServicioGloDet) + "'," + ' "valorGlosa" = ' + "'" + str(valorGlosado) + "'," + ' "valorSoportado" = ' + "'" + str(valorSoportado) + "'," + ' "valorAceptado" = ' + "'" + str(vAceptado) + "', " + ' "valorNotasCredito" = ' + "'" + str(notasCreditoGlosa) + "'," + ' observaciones = ' + "'" + str(observacionesGloDet) + "'," + '"estadoReg" = ' + "'A'," + ' "motivoGlosa_id" = ' + "'" + str(motivoGlosa_id) + "'," + ' "usuarioRegistro_id" = ' + "'" + str(username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(fechaRegistro) + "'," + '"ripsId" = ' + "'" + str(ripsId) + "'," + ' anulado = ' + "'N'," + ' "ripsOtrosServicios_id" = ' + "'" + str(ripsId) + "' WHERE glosa_id = " + "'" + str(glosaId) + "'" + ' AND "itemFactura" = ' + "'" + str(itemFacturaGloDet) + "'"


            print(comando)
            cur3.execute(comando)
            miConexion3.commit()


            #TOTALES NOTAS CREDITO

            comando2 = 'SELECT sum(gloDetRips."valorAceptado")  vAceptado, sum(gloDetRips."valorSoportado") valorSoportado, sum(gloDetRips."valorGlosa") valorGlosado , sum(gloDetRips."valorGlosa") totalGlosa , sum(gloDetRips."valorNotasCredito") totalNotasCredito  FROM cartera_glosasdetalle gloDet, cartera_glosasdetalleRips gloDetRips WHERE gloDet.glosa_id = ' + "'" + str(glosaId) + "'" + ' AND gloDetRips."glosasDetalle_id" = gloDet.id AND gloDet.factura_id = ' + "'" + str(glosaDetId.factura_id) + "'"
            print(comando2)
            cur3.execute(comando2)

            traeSum = []

            for vAceptado, valorSoportado, valorGlosado, totalGlosa, totalNotasCredito  in cur3.fetchall():
                traeSum.append({'vAceptado':vAceptado,'valorSoportado':valorSoportado,'valorGlosado':valorGlosado,'totalGlosa':totalGlosa,'totalNotasCredito':totalNotasCredito})

                totalAceptadoMed = vAceptado
                totalSoportadoMed= valorSoportado
                totalGlosadoMed = valorGlosado
                totalGlosaMed = totalGlosa
                totalNotasCreditoMed =totalNotasCredito
                totalAceptadoMed  = totalAceptadoMed

                if (totalAceptadoMed == '' or totalAceptadoMed=='None'):
                    totalAceptadoMed = 0.0

                if (totalSoportadoMed == '' or totalSoportadoMed=='None'):

                    totalSoportadoMed = 0.0

                if (totalGlosadoMed == '' or totalGlosadoMed=='None'):
        	        totalGlosadoMed = 0.0

                if (totalGlosaMed == '' or totalGlosaMed=='None'):
        	        totalGlosaMed = 0.0

                if (totalNotasCreditoMed == '' or totalNotasCreditoMed == 'None'):
         	       totalNotasCreditoMed = 0.0

                totalAceptado = float(totalAceptadoMed)
                totalSoportado = float(totalSoportadoMed)
                totalGlosado = float(totalGlosadoMed)
                totalGlosa = float(totalGlosaMed)
                totalNotasCredito = float(totalNotasCreditoMed)

                print ("totalAceptado = ",totalAceptado)
                print("totalSoportado = ", totalSoportado)
                print("totalGlosado = ", totalGlosado)


	            # AQUI FALTA ACTUALIZAR EL SALDO DE LA FACTURA

            	# TIENE QUE ACTUALIZAR CARTERA_GLOSAS LOS TOTALES / PENDIENTE SALDO FACTURA

                comando6 = 'UPDATE cartera_glosasdetalle SET "valorSoportado"= ' +"'" + str(totalSoportado) + "'," + '"valorGlosa" = ' + "'" + str(totalGlosado) + "'," + ' "valorAceptado" = ' + "'" +str(totalAceptado) + "'," +  '"valorNotasCredito" = ' + "'" + str(totalNotasCredito) + "'"   +  ' WHERE id = ' + str(post_idGloDet)

                print(comando6)
                cur3.execute(comando6)
                miConexion3.commit()

            ## aqui lo mispo péro para carteraglosas

            comando2 = 'SELECT sum(gloDet."valorAceptado")  vAceptado, sum(gloDet."valorSoportado") valorSoportado, sum(gloDet."valorGlosa") valorGlosado , sum(gloDet."valorNotasCredito") totalNotasCredito  FROM cartera_glosas glosas, cartera_glosasdetalle gloDet  WHERE gloDet.glosa_id = glosas.id AND glosas.id = ' + "'" + str(glosaId) + "'"
            print(comando2)
            cur3.execute(comando2)

            traeSum = []

            for vAceptado, valorSoportado, valorGlosado,  totalNotasCredito in cur3.fetchall():
                traeSum.append(
                    {'vAceptado': vAceptado, 'valorSoportado': valorSoportado, 'valorGlosado': valorGlosado,
                     'totalNotasCredito': totalNotasCredito})

                totalAceptadoMed = vAceptado
                totalSoportadoMed = valorSoportado
                totalGlosadoMed = valorGlosado
                totalNotasCreditoMed = totalNotasCredito

                if (totalAceptadoMed == '' or totalAceptadoMed == 'None'):
                    totalAceptadoMed = 0.0

                if (totalSoportadoMed == '' or totalSoportadoMed == 'None'):
                    totalSoportadoMed = 0.0

                if (totalGlosadoMed == '' or totalGlosadoMed == 'None'):
                    totalGlosadoMed = 0.0

                if (totalNotasCreditoMed == '' or totalNotasCreditoMed == 'None'):
                    totalNotasCreditoMed = 0.0

                totalAceptado = float(totalAceptadoMed)
                totalSoportado = float(totalSoportadoMed)
                totalGlosado = float(totalGlosadoMed)
                totalNotasCredito = float(totalNotasCreditoMed)
                print("totalAceptado = ", totalAceptado)
                print("totalSoportado = ", totalSoportado)
                print("totalGlosado = ", totalGlosado)

                saldoFactura = 0
                # AQUI FALTA ACTUALIZAR EL SALDO DE LA FACTURA

                # TIENE QUE ACTUALIZAR CARTERA_GLOSAS LOS TOTALES / PENDIENTE SALDO FACTURA

                comando6 = 'UPDATE cartera_glosas SET "totalSoportado"= ' + "'" + str(
                    totalSoportado) + "'," + '"totalGlosa" = ' + "'" + str(
                    totalGlosado) + "'," + ' "totalAceptado" = ' + "'" + str(
                    totalAceptado) + "'," + '"totalNotasCredito" = ' + "'" + str(
                    totalNotasCredito) + "'" + ' WHERE id = ' + str(glosaId)

                print(comando6)
                cur3.execute(comando6)
                miConexion3.commit()

            ## aqui debe ir la rutina que actulizar los totales de la glosa en la tabla facturacion

            ## DESDE AQUIP ACTUALIZAR EL SALDO DE LA FACTURA

            comando6 = 'UPDATE facturacion_facturacion SET "totalValorGlosado" = COALESCE("totalValorGlosado",0) + ' +  str(valorGlosadox) + ' ,"totalValorAceptado" = COALESCE("totalValorAceptado",0) + ' + str(
                vAceptadox) + ' , "totalValorSoportado" = COALESCE("totalValorSoportado",0) +  ' + str(valorSoportadox) + ' where id = ' + "'" + str(glosaDetId.factura_id) + "'"

            print(comando6)
            cur3.execute(comando6)

            comando6 = 'UPDATE facturacion_facturacion SET "saldoFactura" =  COALESCE("valorApagar",0)  - COALESCE("totalValorAceptado",0) - COALESCE("totalNotasCredito",0) + COALESCE("totalNotasDebito",0) where id = ' + "'" + str(glosaDetId.factura_id) + "'"
            print(comando6)
            cur3.execute(comando6)

            miConexion3.commit()
            cur3.close()
            miConexion3.close()

            return JsonResponse({'success': True, 'Mensajes': 'Glosa Detalle actualizada !'})

            ## AQUI FALTA EL INSERT A LA TABLA GLOSASDETALLE


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




def GuardaGlosasEstados(request):

    print ("Entre Guarda Glosas Estados" )

    glosaId = request.POST.get('post_idGlo')
    print ("id =", glosaId)

    tipoGlosa = request.POST["tipoGlosa_idGlo"]
    print ("tipoGlosa =", tipoGlosa)

    estadoRadicacion = request.POST["estadoRadicacion_idGlo"]
    print ("estadoRadicacion =", estadoRadicacion)

    estadoRecepcion = request.POST["estadoRecepcion_idGlo"]
    print ("estadoRecepcion =", estadoRecepcion)

    sedesClinica_id = request.POST["sedesClinica_idGlo"]
    print("sedesClinica_id =", sedesClinica_id)

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE cartera_glosas SET "tipoGlosa_id"= ' +"'" + str(tipoGlosa) + "'," + ' "estadoRadicacion_id" = ' + "'" +str(estadoRadicacion) + "'," + '"estadoRecepcion_id" = ' + "'" + str(estadoRecepcion) + "'" + '   WHERE id = ' + str(glosaId)

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Glosa Actualizada satisfactoriamente!'})


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



def GuardarCaja(request):

    print ("Entre GuardarCaja" )

    cajaId = request.POST.get('cajaId')
    print ("cajaId =", cajaId)

    serviciosAdministrativos = request.POST["serviciosAdministrativos_id"]
    print("serviciosAdministrativos =", serviciosAdministrativos)
    fecha = request.POST["fecha"]
    print("fecha =", fecha)
    usuarioEntrega = request.POST["usuarioEntrega_id"]
    print("usuarioEntrega =", usuarioEntrega)
    usuarioRecibe = request.POST["usuarioRecibe_id"]
    print("usuarioRecibe =", usuarioRecibe)
    usuarioSuperviza = request.POST["usuarioSuperviza_id"]
    print("usuarioSuperviza =", usuarioSuperviza)
    totalEfectivo = request.POST["totalEfectivo"]
    print("totalEfectivo =", totalEfectivo)
    totalTarjetasDebito = request.POST["totalTarjetasDebito"]
    print("totalTarjetasDebito =", totalTarjetasDebito)

    totalTarjetasCredito = request.POST["totalTarjetasCredito"]
    print("totalTarjetasCredito =", totalTarjetasCredito)
    totalCheques = request.POST["totalCheques"]
    print("totalCheques =", totalCheques)
    total = request.POST["total"]
    print("total =", total)
    estadoCaja = request.POST["estadoCaja"]
    print("estadoCaja =", estadoCaja)

    username = request.POST["username_idC"]
    print("username =", username)

    sede = request.POST["sedeC"]
    print("sede =", sede)

    fechaRegistro = timezone.now()


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE cartera_caja SET "fechaRegistro"= ' +"'" + str(fechaRegistro) + "'," + ' "totalEfectivo" = ' + "'" +str(totalEfectivo) + "'," + '"totalTarjetasDebito" = ' + "'" + str(totalTarjetasDebito) + "',"  + '"totalTarjetasCredito" = ' + "'" + str(totalTarjetasCredito) + "',"  + '"totalCheques" = ' + "'" + str(totalCheques) + "'," + '"total" = ' + "'" + str(total) + "',"   + '"usuarioEntrega_id" = ' + "'" + str(usuarioEntrega) + "'," + '"usuarioRecibe_id" = ' + "'" + str(usuarioRecibe) + "'," + '"usuarioSuperviza_id" = ' + "'" + str(usuarioSuperviza) + "',"  + '"estadoCaja" = ' + "'" + str(estadoCaja) + "'," + '"serviciosAdministrativos_id" = ' + "'" + str(serviciosAdministrativos) + "'," + '"estadoReg" = ' + "'" + str('A') + "'"  + '   WHERE id = ' + str(cajaId)

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Caja actualizada satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            #miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


def EditarCaja(request):
    
    print("Entre EditarCaja")

    cajaId  = request.POST['cajaId']
    print("cajaId  =", cajaId)

    caja = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()
	
    detalle = 'SELECT id, fecha, "totalEfectivo", "totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", total, "serviciosAdministrativos_id", "usuarioEntrega_id", "usuarioRecibe_id", "usuarioSuperviza_id", "estadoCaja" , "totalEfectivoEsperado", "totalTarjetasDebitoEsperado", "totalTarjetasCreditoEsperado", "totalChequesEsperado", "totalEsperado"   FROM cartera_caja WHERE id =  ' + "'" + str(cajaId) + "'"

    print(detalle)

    curx.execute(detalle)

    for  id, fecha, totalEfectivo, totalTarjetasDebito,totalTarjetasCredito,totalCheques, total, serviciosAdministrativos_id, usuarioEntrega_id, usuarioRecibe_id,  usuarioSuperviza_id, estadoCaja,   totalEfectivoEsperado, totalTarjetasDebitoEsperado,totalTarjetasCreditoEsperado,totalChequesEsperado, totalEsperado  in curx.fetchall():
     caja.append(
            {"model": "cartera.caja", "pk": id, "fields":
                {'id': id, 'fecha': fecha , 'totalEfectivo': totalEfectivo,  'totalTarjetasDebito':totalTarjetasDebito,
		  'totalTarjetasCredito':totalTarjetasCredito,'totalCheques':totalCheques,'total':total,'serviciosAdministrativos_id':serviciosAdministrativos_id,'usuarioEntrega_id':usuarioEntrega_id,'usuarioRecibe_id':usuarioRecibe_id,'usuarioSuperviza_id':usuarioSuperviza_id,'estadoCaja':estadoCaja,
                 'totalEfectivoEsperado': totalEfectivoEsperado, 'totalTarjetasDebitoEsperado': totalTarjetasDebitoEsperado,
                 'totalTarjetasCreditoEsperado': totalTarjetasCreditoEsperado, 'totalChequesEsperado': totalChequesEsperado, 'totalEsperado': totalEsperado
                 }})

    miConexionx.close()
    print("caja = "  , caja)
    
    serialized1 = json.dumps(caja, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataCaja(request, data):

    print("Entre load_data Load_dataCaja")

    context = {}
    d = json.loads(data)

    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)

    caja = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT caj.id, fecha, "totalEfectivo", "totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", total, caj."fechaRegistro", caj."estadoReg", "serviciosAdministrativos_id", pla1.nombre usuarioEntrega_id, pla2.nombre usuarioRecibe_id, "usuarioRegistro_id", pla3.nombre usuarioSuperviza_id, "estadoCaja", caj."sedesClinica_id", "totalChequesEsperado", "totalEfectivoEsperado", "totalEsperado", "totalTarjetasCreditoEsperado", "totalTarjetasDebitoEsperado"  FROM cartera_caja caj LEFT JOIN planta_planta pla1 ON (pla1.id = caj."usuarioEntrega_id") LEFT JOIN planta_planta pla2 ON (pla2.id = caj."usuarioRecibe_id") LEFT JOIN planta_planta pla3 ON (pla3.id = caj."usuarioSuperviza_id")  WHERE caj."sedesClinica_id" = ' + "'" + str(sedesClinica_id) + "'"

    print ("detalle = ", detalle)

    curx.execute(detalle)

    for id,  fecha, totalEfectivo, totalTarjetasDebito,totalTarjetasCredito, totalCheques,  total,  fechaRegistro,  estadoReg , serviciosAdministrativos_id,  usuarioEntrega_id, usuarioRecibe_id, usuarioRegistro_id, usuarioSuperviza_id, estadoCaja, sedesClinica_id, totalChequesEsperado, totalEfectivoEsperado, totalEsperado, totalTarjetasCreditoEsperado, totalTarjetasDebitoEsperado in curx.fetchall():
        caja.append(
            {"model": "cartera.caja", "pk": id, "fields":
                {'id': id, 'fecha': fecha , 'totalEfectivo': totalEfectivo, 'totalTarjetasDebito': totalTarjetasDebito, 'totalTarjetasCredito':totalTarjetasCredito,
                 'totalCheques':totalCheques, 'total':total, 'fechaRegistro':fechaRegistro,
                 estadoReg:estadoReg, 'serviciosAdministrativos_id':serviciosAdministrativos_id, 'usuarioEntrega_id':usuarioEntrega_id, 'usuarioRecibe_id':usuarioRecibe_id,
                 'usuarioRegistro_id':usuarioRegistro_id, 'usuarioSuperviza_id':usuarioSuperviza_id,'estadoCaja':estadoCaja,'sedesClinica_id':sedesClinica_id,
                 'totalChequesEsperado':totalChequesEsperado,'totalEfectivoEsperado':totalEfectivoEsperado, 'totalEsperado':totalEsperado,
                 'totalTarjetasCreditoEsperado':totalTarjetasCreditoEsperado,'totalTarjetasDebitoEsperado':totalTarjetasDebitoEsperado
                 }})



    miConexionx.close()
    print("caja "  , caja)

    serialized1 = json.dumps(caja, default=str)

    return HttpResponse(serialized1, content_type='application/json')



def Load_tablaGlosasTotalesDetalle(request, data):
    print("Entre  Load_tablaGlosasTotalesDetalle ACTUAL")

    context = {}
    d = json.loads(data)

    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)

    glosaId = d['glosaId']
    print("glosaId = ", glosaId)

    # facturaId = d['factura_id']
    # print("facturaId = ", facturaId)

    glosasTotalesDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select ' + "'" + str('MEDICAMENTOS') + "'" + ' tipo,med.id, med.consecutivo consec, med."itemFactura",cums.cum codigo,cums.nombre nombre,substring(mot.nombre,1,10) glosaNombre,med."vrServicio",  detGlo."valorGlosa",    detGlo."valorSoportado" valosSoportado2,   detGlo."valorAceptado" ,    detGlo."valorNotasCredito"	FROM rips_ripstransaccion ripstra 	inner join rips_ripsmedicamentos med on (med."ripsTransaccion_id" = ripstra.id) 	inner join  rips_ripscums cums on (cums.id =med."codTecnologiaSalud_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id =cast(ripstra."numFactura" as float) and  det."consecutivoFactura" = med."itemFactura" ) left join cartera_motivosglosas mot on (mot.id = med."motivoGlosa_id")  left join cartera_glosasdetalle detGlo on (detGlo."ripsMedicamentos_id" = med.id)	where  cast(ripstra."numFactura" as float) = ' + "'" + str(facturaId) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' UNION select ' + "'" + str('PROCEDIMIENTOS') + "'" + ' tipo, proc.id, proc.consecutivo consec, proc."itemFactura", exa."codigoCups" codigo,	exa.nombre nombre,  substring(mot.nombre,1,10)  glosaNombre,proc."vrServicio",detGlo."valorGlosa",    detGlo."valorSoportado" valosSoportado2,   detGlo."valorAceptado" ,    detGlo."valorNotasCredito" FROM  rips_ripstransaccion ripstra inner join  rips_ripsprocedimientos proc on (proc."ripsTransaccion_id" = ripstra.id) inner join clinico_examenes exa on ( exa.id =proc."codProcedimiento_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id=cast(ripstra."numFactura" as float) and det."consecutivoFactura" = proc."itemFactura") left join cartera_motivosglosas mot on (mot.id = proc."motivoGlosa_id") left join cartera_glosasdetalle detGlo on (detGlo."ripsProcedimientos_id" = proc.id) where cast(ripstra."numFactura" as float) = ' + "'" + str(facturaId) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' UNION select ' + "'" + str('CONSULTAS') + "'" + ' tipo, cons.id, cons.consecutivo consec, cons."itemFactura", exa."codigoCups" codigo,	exa.nombre nombre, substring(mot.nombre,1,10)  glosaNombre,cons."vrServicio",	detGlo."valorGlosa",    detGlo."valorSoportado" valosSoportado2,   detGlo."valorAceptado" ,    detGlo."valorNotasCredito"	FROM rips_ripstransaccion  ripstra inner join  rips_ripsconsultas cons on (cons."ripsTransaccion_id" = ripstra.id) inner join clinico_examenes exa on ( exa.id =cons."codConsulta_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id=cast(ripstra."numFactura" as float) and det."consecutivoFactura" = cons."itemFactura") left join cartera_motivosglosas mot on (mot.id = cons."motivoGlosa_id") left join cartera_glosasdetalle detGlo on (detGlo."ripsConsultas_id" = cons.id)	 where cast(ripstra."numFactura" as float) = ' + "'" + str(facturaId) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' UNION	select ' + "'" + str('OTROS SERVICIOS') + "'" + ' tipo, serv.id, serv.consecutivo consec, serv."itemFactura", serv."nomTecnologiaSalud" codigo, exa.nombre nombre, substring(mot.nombre,1,10)  glosaNombre, serv."vrServicio",	detGlo."valorGlosa",    detGlo."valorSoportado" valosSoportado2,   detGlo."valorAceptado" ,    detGlo."valorNotasCredito"	FROM rips_ripstransaccion  ripstra inner join  rips_ripsotrosservicios serv on (serv."ripsTransaccion_id" = ripstra.id) left join clinico_examenes exa on ( exa.id =serv."codTecnologiaSalud_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id=cast(ripstra."numFactura" as float) and det."consecutivoFactura" = serv."itemFactura") left join cartera_motivosglosas mot on (mot.id = serv."motivoGlosa_id") left join cartera_glosasdetalle detGlo on (detGlo."ripsOtrosServicios_id" = serv.id)	where cast(ripstra."numFactura" as float) = ' + "'" + str(facturaId) + "'" + ' and ripstra."numNota"= ' + "'" + str('0') + "'" + ' order by 1,4'


    print(detalle)

    curx.execute(detalle)

    #for  tipo, id, consec, itemFactura, codigo, nombre,   glosaNombre,vrServicio,  valorGlosado,vAceptado, valorSoportado , notasCreditoGlosa , valorGlosa, valorSoportado2 , valorAceptado, valorNotasCredito in curx.fetchall():
    for tipo, id, consec, itemFactura, codigo, nombre, glosaNombre, vrServicio, valorGlosa, valorSoportado2, valorAceptado, valorNotasCredito in curx.fetchall():
        glosasTotalesDetalle.append(
            {"model": "rips.GlosasDetalle", "pk": id, "fields":
                {'tipo':tipo, 'id': id, 'consec':consec,  'itemFactura': itemFactura ,'codigo': codigo, 'nombre': nombre,'glosaNombre':glosaNombre,'vrServicio':vrServicio,
                 'valorGlosa': valorGlosa, 'valorSoportado2': valorSoportado2,   'valorAceptado': valorAceptado,
                 'valorNotasCredito': valorNotasCredito }})

    miConexionx.close()


    serialized1 = json.dumps(glosasTotalesDetalle,  default=str)

    print("glosasTotalesDetalle = ", serialized1)

    return HttpResponse(serialized1, content_type='application/json')


def BorraGlosasDetalle(request):
    
    print("Entre BorraGlosasDetalle")

    detGloId  = request.POST['detGloId']
    print("detGloId  =", detGloId)

    ripsId= request.POST['ripsId']
    print("ripsId  =", ripsId)

    glosaId= request.POST['glosaId']
    print("glosaId  =", glosaId)

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'DELETE FROM cartera_glosasdetalle where id = ' + "'" + str(detGloId) + "'"

        print(detalle)
        cur3.execute(detalle)

        comando2 = 'SELECT sum("valorAceptado")  vAceptado, sum("valorSoportado") valorSoportado, sum("valorGlosa") valorGlosado , sum("valorGlosa") totalGlosa , sum("valorNotasCredito") totalNotasCredito  FROM cartera_glosasdetalle WHERE glosa_id = ' + "'" + str(glosaId) + "'"
        print(comando2)
        cur3.execute(comando2)

        traeSum = []

        for vAceptado, valorSoportado, valorGlosado, totalGlosa, totalNotasCredito  in cur3.fetchall():
            traeSum.append({'vAceptado':vAceptado,'valorSoportado':valorSoportado,'valorGlosado':valorGlosado,'totalGlosa':totalGlosa,'totalNotasCredito':totalNotasCredito})

        totalAceptadoMed = traeSum[0]['vAceptado']
        totalAceptadoMed = str(totalAceptadoMed)
        totalAceptadoMed = totalAceptadoMed.replace("(", ' ')
        totalAceptadoMed = totalAceptadoMed.replace(")", ' ')
        totalAceptadoMed = totalAceptadoMed.replace(",", ' ')
        totalAceptadoMed = totalAceptadoMed.replace("'", ' ')
        totalAceptadoMed = totalAceptadoMed.replace("Decimal", ' ')

        totalSoportadoMed = traeSum[0]['valorSoportado']
        totalSoportadoMed = str(totalSoportadoMed)
        totalSoportadoMed = totalSoportadoMed.replace("(", ' ')
        totalSoportadoMed = totalSoportadoMed.replace(")", ' ')
        totalSoportadoMed = totalSoportadoMed.replace(",", ' ')
        totalSoportadoMed = totalSoportadoMed.replace("'", ' ')
        totalSoportadoMed = totalSoportadoMed.replace("Decimal", ' ')

        totalGlosadoMed = traeSum[0]['valorGlosado']
        totalGlosadoMed = str(totalGlosadoMed)
        totalGlosadoMed = totalGlosadoMed.replace("(", ' ')
        totalGlosadoMed = totalGlosadoMed.replace(")", ' ')
        totalGlosadoMed = totalGlosadoMed.replace(",", ' ')
        totalGlosadoMed = totalGlosadoMed.replace("'", ' ')
        totalGlosadoMed = totalGlosadoMed.replace("Decimal", ' ')

        totalGlosaMed = traeSum[0]['totalGlosa']
        totalGlosaMed = str(totalGlosaMed)
        totalGlosaMed = totalGlosaMed.replace("(", ' ')
        totalGlosaMed = totalGlosaMed.replace(")", ' ')
        totalGlosaMed = totalGlosaMed.replace(",", ' ')
        totalGlosaMed = totalGlosaMed.replace("'", ' ')
        totalGlosaMed = totalGlosaMed.replace("Decimal", ' ')

        totalNotasCreditoMed = traeSum[0]['totalNotasCredito']
        totalNotasCreditoMed = str(totalNotasCreditoMed)
        totalNotasCreditoMed = totalNotasCreditoMed.replace("(", ' ')
        totalNotasCreditoMed = totalNotasCreditoMed.replace(")", ' ')
        totalNotasCreditoMed = totalNotasCreditoMed.replace(",", ' ')
        totalNotasCreditoMed = totalNotasCreditoMed.replace("'", ' ')
        totalNotasCreditoMed = totalNotasCreditoMed.replace("Decimal", ' ')

        print("totalAceptadoMed = ", totalAceptadoMed)
        print("totalSoportadoMed = ", totalSoportadoMed)
        print("totalGlosadoMed = ", totalGlosadoMed)
        print("totalNotasCreditoMed = ", totalNotasCreditoMed)


        if (totalAceptadoMed == '' or totalAceptadoMed=='None'):
            totalAceptadoMed = 0.0

        if (totalSoportadoMed == '' or totalSoportadoMed=='None'):
            totalSoportadoMed = 0.0

        if (totalGlosadoMed == '' or totalGlosadoMed=='None'):
            totalGlosadoMed = 0.0

        if (totalGlosaMed == '' or totalGlosaMed=='None'):
            totalGlosaMed = 0.0

        if (totalNotasCreditoMed == '' or totalNotasCreditoMed == 'None'):
            totalNotasCreditoMed = 0.0

        totalAceptado = float(totalAceptadoMed)
        totalSoportado = float(totalSoportadoMed)
        totalGlosado = float(totalGlosadoMed)
        totalGlosa = float(totalGlosaMed)
        totalNotasCredito = float(totalNotasCreditoMed)

        print ("totalAceptado = ",totalAceptado)
        print("totalSoportado = ", totalSoportado)
        print("totalGlosado = ", totalGlosado)

        saldoFactura = 0
        # AQUI FALTA ACTUALIZAR EL SALDO DE LA FACTURA

        # TIENE QUE ACTUALIZAR CARTERA_GLOSAS LOS TOTALES / PENDIENTE SALDO FACTURA

        comando6 = 'UPDATE cartera_glosas SET "totalSoportado"= ' +"'" + str(totalSoportado) + "'," + '"totalGlosa" = ' + "'" + str(totalGlosado) + "'," + ' "totalAceptado" = ' + "'" +str(totalAceptado) + "'," + '"saldoFactura" = ' + "'" + str(saldoFactura) + "'," +  '"totalNotasCredito" = ' + "'" + str(totalNotasCredito) + "'"   +  ' WHERE id = ' + str(glosaId)

        print(comando6)
        cur3.execute(comando6)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Glosa Detalle eliminada !'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            #miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()



def BorraGlosasDetalleRips(request):
    
    print("Entre BorraGlosasDetalleRips")

    detGloRipsId  = request.POST['detGloRipsId']
    print("detGloRipsId  =", detGloRipsId)

    detGloId  = request.POST['detGloId']
    print("detGloId  =", detGloId)

    ripsId= request.POST['ripsId']
    print("ripsId  =", ripsId)

    glosaId= request.POST['glosaId'] # Esta es la glosa glosa
    print("glosaId  =", glosaId)

    detGlo = GlosasDetalle.objects.get(id=detGloId)
    facturaId = detGlo.factura_id

    detGloRips = GlosasDetalleRips.objects.get(id=detGloRipsId)

    valorGlosa= detGloRips.valorGlosa
    if (valorGlosa == '' or valorGlosa=='None'):
          valorGlosa = 0.0

    valorAceptado= detGloRips.valorAceptado
    if (valorAceptado == '' or valorAceptado=='None'):
          valorAceptado = 0.0

    valorSoportado= detGloRips.valorSoportado
    if (valorSoportado == '' or valorSoportado=='None'):
          valorSoportado = 0.0

    valorNotasCredito= detGloRips.valorNotasCredito
    if (valorNotasCredito == '' or valorNotasCredito=='None'):
          valorNotasCredito = 0.0

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'DELETE FROM cartera_glosasdetalleRips where id = ' + "'" + str(detGloRipsId) + "'"

        print(detalle)
        cur3.execute(detalle)

        comando2 = 'SELECT sum(gloDetRip."valorAceptado")  vAceptado, sum(gloDetRip."valorSoportado") valorSoportado, sum(gloDetRip."valorGlosa") valorGlosado , sum(gloDetRip."valorNotasCredito") totalNotasCredito  FROM cartera_glosasdetalleRips gloDetRips, cartera_glosasdetalle gloDet WHERE gloDetRips."glosasDetalle_id" = gloDet.id AND gloDet.id = ' + "'" + str(detGloId) + "'"
        print(comando2)
        cur3.execute(comando2)

        traeSum = []

        for vAceptado, valorSoportado, valorGlosado, totalGlosa, totalNotasCredito  in cur3.fetchall():
            traeSum.append({'vAceptado':vAceptado,'valorSoportado':valorSoportado,'valorGlosado':valorGlosado,'totalNotasCredito':totalNotasCredito})

            totalAceptadoMed = vAceptado
            totalSoportadoMed = valorSoportado
            totalGlosadoMed = valorGlosado
            totalNotasCreditoMed = totalNotasCredito

            print("totalAceptadoMed = ", totalAceptadoMed)
            print("totalSoportadoMed = ", totalSoportadoMed)
            print("totalGlosadoMed = ", totalGlosadoMed)
            print("totalNotasCreditoMed = ", totalNotasCreditoMed)

            if (totalAceptadoMed == '' or totalAceptadoMed=='None'):
               totalAceptadoMed = 0.0

            if (totalSoportadoMed == '' or totalSoportadoMed=='None'):
               totalSoportadoMed = 0.0

            if (totalGlosadoMed == '' or totalGlosadoMed=='None'):
               totalGlosadoMed = 0.0

            if (totalNotasCreditoMed == '' or totalNotasCreditoMed == 'None'):
               totalNotasCreditoMed = 0.0

            totalAceptado = float(totalAceptadoMed)
            totalSoportado = float(totalSoportadoMed)
            totalGlosado = float(totalGlosadoMed)
            totalNotasCredito = float(totalNotasCreditoMed)
            print ("totalAceptado = ",totalAceptado)
            print("totalSoportado = ", totalSoportado)
            print("totalGlosado = ", totalGlosado)

            # TIENE QUE ACTUALIZAR CARTERA_GLOSAS LOS TOTALES / PENDIENTE SALDO FACTURA

            comando6 = 'UPDATE cartera_glosasdetalle SET "valorSoportado"= ' +"'" + str(totalSoportado) + "'," + '"valorGlosa" = ' + "'" + str(totalGlosado) + "'," + ' "valorAceptado" = ' + "'" +str(totalAceptado) + "'," + '"valorNotasCredito" = ' + "'" + str(totalNotasCredito) + "'"   +  ' WHERE id = ' + str(detGloId)

            print(comando6)
            cur3.execute(comando6)


        ## DESDE AQUI SALDO EN CARTERA GLOSAS

        comando2 = 'SELECT sum(gloDet."valorAceptado")  vAceptado, sum(gloDet."valorSoportado") valorSoportado, sum(gloDet."valorGlosa") valorGlosado , sum(gloDet."valorNotasCredito") totalNotasCredito  FROM cartera_glosasdetalle gloDet WHERE gloDet.glosa_id = ' + "'" + str(glosaId) + "'"
        print(comando2)
        cur3.execute(comando2)

        traeSum = []

        for vAceptado, valorSoportado, valorGlosado, totalGlosa, totalNotasCredito  in cur3.fetchall():
            traeSum.append({'vAceptado':vAceptado,'valorSoportado':valorSoportado,'valorGlosado':valorGlosado,'totalNotasCredito':totalNotasCredito})

            totalAceptadoMed = vAceptado
            totalSoportadoMed = valorSoportado
            totalGlosadoMed = valorGlosado
            totalNotasCreditoMed = totalNotasCredito

            print("totalAceptadoMed = ", totalAceptadoMed)
            print("totalSoportadoMed = ", totalSoportadoMed)
            print("totalGlosadoMed = ", totalGlosadoMed)
            print("totalNotasCreditoMed = ", totalNotasCreditoMed)

            if (totalAceptadoMed == '' or totalAceptadoMed=='None'):
               totalAceptadoMed = 0.0

            if (totalSoportadoMed == '' or totalSoportadoMed=='None'):
               totalSoportadoMed = 0.0

            if (totalGlosadoMed == '' or totalGlosadoMed=='None'):
               totalGlosadoMed = 0.0

            if (totalNotasCreditoMed == '' or totalNotasCreditoMed == 'None'):
               totalNotasCreditoMed = 0.0

            totalAceptado = float(totalAceptadoMed)
            totalSoportado = float(totalSoportadoMed)
            totalGlosado = float(totalGlosadoMed)
            totalNotasCredito = float(totalNotasCreditoMed)
            print ("totalAceptado = ",totalAceptado)
            print("totalSoportado = ", totalSoportado)
            print("totalGlosado = ", totalGlosado)

            # TIENE QUE ACTUALIZAR CARTERA_GLOSAS LOS TOTALES / PENDIENTE SALDO FACTURA

            comando6 = 'UPDATE cartera_glosas SET "totalSoportado"= ' +"'" + str(totalSoportado) + "'," + '"totalGlosa" = ' + "'" + str(totalGlosado) + "'," + ' "totalAceptado" = ' + "'" +str(totalAceptado) + "'," + '"totalNotasCredito" = ' + "'" + str(totalNotasCredito) + "'"   +  ' WHERE id = ' + str(detGloId)

            print(comando6)
            cur3.execute(comando6)


        ## DESDE AQUIP ACTUALIZAR EL SALDO DE LA FACTURA

        comando6 = 'UPDATE facturacion_facturacion SET "totalValorGlosado" = COALESCE("totalValorGlosado",0) - detGloRips.valorGlosa,"totalValorAceptado" = COALESCE("totalValorAceptado",0) - ' + float(valorAceptado) + ' , "totalValorSoportado" = COALESCE("totalValorSoportado",0) - ' + float(valorSoportado) + ' ,	"totalNotasCredito" = COALESCE("totalNotasCredito",0) - ' + float(valorNotasCredito) + ',"saldoFactura" =  float("valorApagar") - float("totalValorAceptado") - float("totalNotasCredito") + float("totalNotasDebito") where id = ' + "'" + str(facturaId) + "'"

        print(comando6)
        cur3.execute(comando6)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Glosa Detalle eliminada !'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            #miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()



def BorraNotasCreditoDetalleRips(request):
    print("Entre BorraNotasCreditoDetalleRips")

    detCreRipsId = request.POST['detCreRipsId']
    print("detCreRipsId  =", detCreRipsId)

    if (detCreRipsId == None):

        return JsonResponse({'success': True, 'Mensajes': ''})

    ripsId = request.POST['ripsId']
    print("ripsId  =", ripsId)

    valorNota = request.POST['valorNota']

    if (valorNota == None):
        valorNota=0

    print("valorNota  =", valorNota)

    notasCreditoDetalleRipsId = NotasCreditoDetalleRips.objects.get(id=detCreRipsId)
    notasCreditoDetalleId = NotasCreditoDetalle.objects.get(id=notasCreditoDetalleRipsId.notaCreditoDetalle_id)
    factura = notasCreditoDetalleId.factura_id
    facturaId = Facturacion.objects.get(id=factura)

    saldoFactura = float(facturaId.saldoFactura) + float(valorNota)

    totalNotasCredito = float(facturaId.totalNotasCredito) - float(valorNota)

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'DELETE FROM cartera_notascreditodetallerips where id = ' + "'" + str(detCreRipsId) + "'"

        print(detalle)
        cur3.execute(detalle)

        comando6 = 'UPDATE facturacion_facturacion SET "saldoFactura" = ' + "'" + str(
            saldoFactura) + "'," + '"totalNotasCredito" = ' + "'" + str(totalNotasCredito) + "' WHERE id = '" + str(
            factura) + "'"

        print(comando6)
        cur3.execute(comando6)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Glosa Detalle eliminada !'})

    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            # miConexion3.rollback()

        message_error = str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()



def load_dataNotasCredito(request, data):
    print("load_dataNotasCredito")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    notasCredito = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT nc.id,  nc."fechaNota", nc."valorNota", nc."fechaRegistro", nc."usuarioRegistro_id", nc.descripcion FROM public.cartera_notascredito nc, facturacion_liquidacion fac ,contratacion_convenios conv WHERE nc."sedesClinica_id" = ' + "'" + str(sede) + "'" + 'AND fac.convenio_id  = conv.id '

    print(detalle)

    curx.execute(detalle)

    for id,  fechaNota, valorNota, fechaRegistro,  usuarioRegistro_id, descripcion  in curx.fetchall():
        notasCredito.append(
            {"model": "cartera.notasCredito", "pk": id, "fields":
                {'id': id, 'valorNota':valorNota, 'fechaRegistro': fechaRegistro, 'usuarioRegistro_id': usuarioRegistro_id,'descripcion':descripcion}})

    miConexionx.close()
    print("notasCredito "  , notasCredito)
    context['NotasCredito'] = notasCredito

    serialized1 = json.dumps(notasCredito,  default=str)

    return HttpResponse(serialized1, content_type='application/json')

    


def load_dataNotasCreditoDetalle(request, data):
    print("load_dataNotasCreditoDetalle")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    notaCredito = d['notaCredito']
    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("notaCredito:", notaCredito)



    notasCreditoDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT ncDet.id , nc.id notaCredito, ncDet.factura_id , ncDet."valorNota", ncDet."tiposNotasCredito_id" tipoNota, tip.nombre nombreTipoNota,  ncDet."fechaRegistro",  ncDet."usuarioRegistro_id", fac."valorApagar", fac."totalValorAceptado", fac."totalNotasCredito", fac."saldoFactura" FROM public.cartera_notascredito nc, cartera_notascreditodetalle ncDet, cartera_tiposnotasCredito tip, facturacion_facturacion fac WHERE ncDet."notaCredito_id" = ' + "'" + str(notaCredito) + "'" + ' AND ncDet."notaCredito_id" = nc.id AND ncDet.factura_id= fac.id AND nc."sedesClinica_id" = ' + "'" + str(sede) + "'" + 'AND ncDet."tiposNotasCredito_id"  = tip.id '

    print(detalle)

    curx.execute(detalle)

    for id,  notaCredito,factura_id, valorNota, tipoNota, nombreTipoNota, fechaRegistro, usuarioRegistro_id, totalFactura, totalGlosas, totalNotasCredito, saldoFactura  in curx.fetchall():
        notasCreditoDetalle.append(
            {"model": "cartera.notasCreditoDetalle", "pk": id, "fields":
                {'id': id, 'notaCredito':notaCredito,'factura_id':factura_id, 'valorNota':valorNota,'tipoNota':tipoNota, 'nombreTipoNota':nombreTipoNota,
		'fechaRegistro': fechaRegistro, 'usuarioRegistro_id': usuarioRegistro_id,'totalFactura':totalFactura, 'totalGlosas':totalGlosas,'totalNotasCredito':totalNotasCredito, 'saldoFactura':saldoFactura }})

    miConexionx.close()
    print("notasCreditoDetalle = "  , notasCreditoDetalle)
    context['NotasCreditoDetalle'] = notasCreditoDetalle

    serialized1 = json.dumps(notasCreditoDetalle,  default=str)

    return HttpResponse(serialized1, content_type='application/json')

    

def load_dataNotasCreditoDetalleRips(request, data):
    print("load_dataNotasCreditoDetalleRips")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    notaCreditoDetalle = d['notaCreditoDetalle']
    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("notaCreditoDetalle:", notaCreditoDetalle)

    notaCreditoDetalleId = NotasCreditoDetalle.objects.get(id=notaCreditoDetalle)
    factura = notaCreditoDetalleId.factura_id
    notaCreditoId = notaCreditoDetalleId.notaCredito_id

    notasCreditoDetalleRips = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select ' + "'" + str('MEDICAMENTOS') + "'" + ' tipo,med.id, med.consecutivo consec, med."itemFactura",cums.cum codigo,cums.nombre nombre,med."vrServicio",  detCreRips."valorNota", detCre.id detCreId, detCreRips.id detCreRipsId, detCre."notaCredito_id" notaCreditoId	FROM rips_ripstransaccion ripstra inner join rips_ripsmedicamentos med on (med."ripsTransaccion_id" = ripstra.id) inner join  rips_ripscums cums on (cums.id =med."codTecnologiaSalud_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id =cast(ripstra."numFactura" as float) and  det."consecutivoFactura" = med."itemFactura" ) left join cartera_notascreditodetalle detCre on (detCre."notaCredito_id" = ' + "'" + str(notaCreditoId) + "'" + ') left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id" = detCre.id AND  detCreRips."ripsMedicamentos_id" = med.id)	where  ripstra."numFactura"= ' + "'" + str(factura) + "'"  + ' and cast(ripstra."numNota" as integer) =0 UNION select ' + "'" + str('PROCEDIMIENTOS') + "'" + ' tipo,proc.id, proc.consecutivo consec, proc."itemFactura",exa."codigoCups" codigo,exa.nombre nombre,	proc."vrServicio",  detCreRips."valorNota", detCre.id detCreId, detCreRips.id detCreRipsId, detCre."notaCredito_id" notaCreditoId	FROM rips_ripstransaccion ripstra inner join rips_ripsprocedimientos proc on (proc."ripsTransaccion_id" = ripstra.id) inner join  clinico_examenes exa on (exa.id =proc."codProcedimiento_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id =cast(ripstra."numFactura" as float) and  det."consecutivoFactura" = proc."itemFactura" ) left join cartera_notascreditodetalle detCre on (detCre."notaCredito_id" = ' + "'" + str(notaCreditoId) + "'" + ') left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id" = detCre.id AND  detCreRips."ripsProcedimientos_id" = proc.id) where  ripstra."numFactura"= ' + "'" + str(factura) + "'"   + ' and cast(ripstra."numNota" as integer) =0  UNION select ' + "'" + str('CONSULTAS') + "'" + ' tipo,cons.id, cons.consecutivo consec, cons."itemFactura",exa."codigoCups" codigo,exa.nombre nombre, cons."vrServicio",  detCreRips."valorNota", detCre.id detCreId, detCreRips.id detCreRipsId, detCre."notaCredito_id" notaCreditoId	FROM rips_ripstransaccion ripstra inner join rips_ripsconsultas cons on (cons."ripsTransaccion_id" = ripstra.id) 	inner join  clinico_examenes exa on (exa.id =cons."codConsulta_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id =cast(ripstra."numFactura" as float) and  det."consecutivoFactura" = cons."itemFactura" ) left join cartera_notascreditodetalle detCre on (detCre."notaCredito_id" = ' + "'" + str(notaCreditoId) + "'" + ') left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id" = detCre.id AND  detCreRips."ripsConsultas_id" = cons.id) where  ripstra."numFactura"= ' + "'" + str(factura) + "'"   + ' and cast(ripstra."numNota" as integer) =0 UNION select ' + "'" + str('OTROS SERVICIOS') + "'" + ' tipo,otros.id, otros.consecutivo consec, otros."itemFactura",exa."codigoCups" codigo,exa.nombre nombre,	otros."vrServicio",  detCreRips."valorNota", detCre.id detCreId, detCreRips.id detCreRipsId, detCre."notaCredito_id" notaCreditoId FROM rips_ripstransaccion ripstra inner join rips_ripsotrosservicios otros on (otros."ripsTransaccion_id" = ripstra.id) inner join  clinico_examenes exa on (exa.id =otros."codTecnologiaSalud_id" ) inner join facturacion_facturaciondetalle det on (det.facturacion_id =cast(ripstra."numFactura" as float) and  det."consecutivoFactura" = otros."itemFactura" ) left join cartera_notascreditodetalle detCre on (detCre."notaCredito_id" = ' + "'" + str(notaCreditoId) + "'" + ') left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id" = detCre.id AND  detCreRips."ripsOtrosServicios_id" = otros.id) where  ripstra."numFactura"= ' + "'" + str(factura) + "'" + ' and cast(ripstra."numNota" as integer) = 0'

    print(detalle)

    curx.execute(detalle)

    #for  tipo, id, consec, itemFactura, codigo, nombre,   ,vrServicio,  valorGlosado,vAceptado, valorSoportado , notasCreditoGlosa , valorGlosa, valorSoportado2 , valorAceptado, valorNotasCredito in curx.fetchall():
    for tipo, id, consec, itemFactura, codigo, nombre, vrServicio , valorNota, detCreId , detCreRipsId, notaCreditoId in curx.fetchall():
        notasCreditoDetalleRips.append(
            {"model": "cartera.notasCreditoDetalleRips", "pk": id, "fields":
                {'tipo':tipo, 'id': id, 'consec':consec,  'itemFactura': itemFactura ,'codigo': codigo, 'nombre': nombre,'vrServicio':vrServicio,
                 'valorNota': valorNota, 'detCreId':detCreId,'detCreRipsId':detCreRipsId,'notaCreditoId':notaCreditoId }})

    miConexionx.close()
    serialized1 = json.dumps(notasCreditoDetalleRips,  default=str)
    print("notasCreditoDetalleRips = ", serialized1)

    return HttpResponse(serialized1, content_type='application/json')


def GuardarNotasCreditoDetalleRips(request):
    print("Entre GuardarNotasCreditoDetalleRips")


    ripsId = request.POST["post_id"]
    print("ripsId =", ripsId)

    tipo = request.POST["tipo"]
    print("tipo =", tipo)

    notaCreditoDetalle = request.POST['notasCreditoDetalle']
    print("notaCreditoDetalle =", notaCreditoDetalle)

    itemFactura = request.POST['itemFactura']
    print("itemFactura =", itemFactura)

    vrServicio = request.POST['vrServicio']
    print("vrServicio =", vrServicio)

    valorNota = request.POST['valorNota']
    print("valorNota =", valorNota)

    if (valorNota == ''):
        valorNota = 0.0


    print("valorNota =", valorNota)

    if (vrServicio == ''):
        vrServicio = 0.0


    print("vrServicio =", vrServicio)

    username_id = request.POST['username_id']
    print("username_id=", username_id)

    estadoReg = 'A'

    fechaRegistro = timezone.now()

    if (float(valorNota) > float(vrServicio)):
        print("Entre 1")
        print("valorNota=", valorNota)
        print("vrServicio=", vrServicio)
        return JsonResponse( {'success': False,  'Mensajes': 'Valor Nota mayor que el valor del servicio RIPS!'})

    # Aqui controlamos el valor de la glosadetalle

    notasCreditoDetalleId = NotasCreditoDetalle.objects.get(id=notaCreditoDetalle)

    notasCreditoDetalle = notasCreditoDetalleId.valorNota

    if (notasCreditoDetalle == None):
        notasCreditoDetalle=0

    notasCreditoDetalleRipsId = NotasCreditoDetalleRips.objects.filter(notaCreditoDetalle_id=notaCreditoDetalle).aggregate(Sum('valorNota'))
    notasCreditoDetalleRips = notasCreditoDetalleRipsId['valorNota__sum']

    print("notasCreditoDetalleRips" , notasCreditoDetalleRips)

    if (notasCreditoDetalleRips == None):
        notasCreditoDetalleRips=0

    if (float(notasCreditoDetalleRips) + float(valorNota) ) > float(notasCreditoDetalle):
        print("Entre 2")
        return JsonResponse( {'success': False,  'Mensajes': 'Valor de Notas en RIPS no puede ser mayor que la Nota Credito !'})


    try:
        with transaction.atomic():

            notaCreditoDetalleId = NotasCreditoDetalle.objects.get(id=notaCreditoDetalle)
            valorParcialFacturaId = Facturacion.objects.get(id=notaCreditoDetalleId.factura_id)

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)
        #return JsonResponse({'success': False, 'Mensajes': 'Factura No existe'})

    finally:

        print("no haga nada")


    valorParcialFactura = valorParcialFacturaId.valorApagar
    valorParcialGlosas = valorParcialFacturaId.totalValorAceptado

    if (valorParcialGlosas == None):
            valorParcialGlosas=0

    valorParcialNotasCredito = valorParcialFacturaId.totalNotasCredito

    if (valorParcialNotasCredito == None):
            valorParcialNotasCredito=0

    valorParcialNotasCredito = float(valorParcialNotasCredito) + float(valorNota)

    valorParcialNotasDebito = valorParcialFacturaId.totalNotasDebito

    if (valorParcialNotasDebito == None):
            valorParcialNotasDebito=0

    saldoFactura = float(valorParcialFactura) -  float(valorParcialNotasCredito) + float(valorParcialNotasDebito) -  float(valorParcialGlosas)


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        hayRegistro = 0

        try:
            with transaction.atomic():

                existeRegistro = NotasCreditoDetalleRips.objects.get(notaCreditoDetalle_id=notasCreditoDetalle, itemFactura=itemFactura)
                hayRegistro = existeRegistro.id

        except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            hayRegistro = 0

        finally:
            print("No haga nada")

        if tipo == 'MEDICAMENTOS':

            if (hayRegistro == 0):

                comando = 'INSERT INTO cartera_notascreditodetalleRips ( "itemFactura", "valorServicio", "valorNota", "estadoReg", "notaCreditoDetalle_id", "usuarioRegistro_id", "fechaRegistro", anulado, "ripsMedicamentos_id"	) VALUES ( ' + "'" + str(
                    itemFactura) + "','" + str(vrServicio) + "','" + str(valorNota) + "','A','" + str(
                    notaCreditoDetalle) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','N','" + str(ripsId) + "')"

            else:

                comando = 'UPDATE cartera_notascreditodetalleRips SET "itemFactura" = ' + "'" + str(
                    itemFactura) + "'," + ' "valorServicio"  = ' + "'" + str(
                    vrServicio) + "'," + ' "valorNota" = ' + "'" + str(
                    valorNota) + "',"  + '"estadoReg" = ' + "'A'," + ' "usuarioRegistro_id" = ' + "'" + str(
                    username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(
                    fechaRegistro) + "',"  + ' anulado = ' + "'N'," + ' "ripsMedicamentos_id" = ' + "'" + str(
                    ripsId) + "'" + ' WHERE "notaCreditoDetalle_id"  = ' + "'" + str(notaCreditoDetalle) + "'" + ' AND "itemFactura" = ' + "'" + str(
                    itemFactura) + "'"

        if tipo == 'PROCEDIMIENTOS':

            if (hayRegistro == 0):

                comando = 'INSERT INTO cartera_notascreditodetalleRips ( "itemFactura", "valorServicio", "valorNota", "estadoReg", "notaCreditoDetalle_id", "usuarioRegistro_id", "fechaRegistro", anulado, "ripsProcedimientos_id"	) VALUES ( ' + "'" + str(
                    itemFactura) + "','" + str(vrServicio) + "','" + str(valorNota) + "','A','" + str(
                    notaCreditoDetalle) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','N','" + str(ripsId) + "')"

            else:

                comando = 'UPDATE cartera_notascreditodetalleRips SET "itemFactura" = ' + "'" + str(
                    itemFactura) + "'," + ' "valorServicio"  = ' + "'" + str(
                    vrServicio) + "'," + ' "valorNota" = ' + "'" + str(
                    valorNota) + "',"  + '"estadoReg" = ' + "'A'," + ' "usuarioRegistro_id" = ' + "'" + str(
                    username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(
                    fechaRegistro) + "',"  + ' anulado = ' + "'N'," + ' "ripsProcedimientos_id" = ' + "'" + str(
                    ripsId) + "'" + ' WHERE "notaCreditoDetalle_id"  = ' + "'" + str(notaCreditoDetalle) + "'" + ' AND "itemFactura" = ' + "'" + str(
                    itemFactura) + "'"

        if tipo == 'CONSULTAS':

            if (hayRegistro == 0):

                comando = 'INSERT INTO cartera_notascreditodetalleRips ( "itemFactura", "valorServicio", "valorNota", "estadoReg", "notaCreditoDetalle_id", "usuarioRegistro_id", "fechaRegistro", anulado, "ripsConsultas_id"	) VALUES ( ' + "'" + str(
                    itemFactura) + "','" + str(vrServicio) + "','" + str(valorNota) + "','A','" + str(
                    notaCreditoDetalle) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','N','" + str(ripsId) + "')"

            else:

                comando = 'UPDATE cartera_notascreditodetalleRips SET "itemFactura" = ' + "'" + str(
                    itemFactura) + "'," + ' "valorServicio"  = ' + "'" + str(
                    vrServicio) + "'," + ' "valorNota" = ' + "'" + str(
                    valorNota) + "',"  + '"estadoReg" = ' + "'A'," + ' "usuarioRegistro_id" = ' + "'" + str(
                    username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(
                    fechaRegistro) + "',"  + ' anulado = ' + "'N'," + ' "ripsConsultas_id" = ' + "'" + str(
                    ripsId) + "'" + ' WHERE "notaCreditoDetalle_id"  = ' + "'" + str(notaCreditoDetalle) + "'" + ' AND "itemFactura" = ' + "'" + str(
                    itemFactura) + "'"

        if tipo == 'OTROS SERVICIOS':

            if (hayRegistro == 0):

                comando = 'INSERT INTO cartera_notascreditodetalleRips ( "itemFactura", "valorServicio", "valorNota", "estadoReg", "notaCreditoDetalle_id", "usuarioRegistro_id", "fechaRegistro", anulado, "ripsOtrosServicios_id"	) VALUES ( ' + "'" + str(
                    itemFactura) + "','" + str(vrServicio) + "','" + str(valorNota) + "','A','" + str(
                    notaCreditoDetalle) + "','" + str(username_id) + "','" + str(fechaRegistro) + "','N','" + str(ripsId) + "')"

            else:

                comando = 'UPDATE cartera_notascreditodetalleRips SET "itemFactura" = ' + "'" + str(
                    itemFactura) + "'," + ' "valorServicio"  = ' + "'" + str(
                    vrServicio) + "'," + ' "valorNota" = ' + "'" + str(
                    valorNota) + "',"  + '"estadoReg" = ' + "'A'," + ' "usuarioRegistro_id" = ' + "'" + str(
                    username_id) + "'," + ' "fechaRegistro" = ' + "'" + str(
                    fechaRegistro) + "',"  + ' anulado = ' + "'N'," + ' "ripsOtrosServicios_id" = ' + "'" + str(
                    ripsId) + "'" + ' WHERE "notaCreditoDetalle_id"  = ' + "'" + str(notaCreditoDetalle) + "'" + ' AND "itemFactura" = ' + "'" + str(
                    itemFactura) + "'"

        print(comando)
        cur3.execute(comando)

        comando = 'UPDATE facturacion_facturacion SET "totalNotasCredito" =  ' + "'" + str(valorParcialNotasCredito) + "'," + '"saldoFactura" = ' + "'" + str(saldoFactura) + "'"  + ' WHERE id = ' + "'" + str(notaCreditoDetalleId.factura_id) + "'"

        print(comando)
        cur3.execute(comando)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Nota  Credito actualizada !'})



    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()
        message_error = str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()

    ## OJO DE PRONTO POR AQUI HACE FALATA UN PEDAZO DE CODIGO
    # EN GLOSASDETALLE ESTA ESTE CODIGO PEO OPS VERIFICAR AHI HAY UN ERROR PAPABEROL


def ConsultaNotasCreditoDetalleRips(request):
    print("Entre ConsultaNotasCreditoDetalleRips")

    id = request.POST['id']
    print("id  =", id)

    tipo = request.POST["tipo"]
    print("tipo  =", tipo)

    detCreId = request.POST["detCreId"]
    print("detCreId  =", detCreId)

    itemFactura = request.POST["itemFactura"]
    print("itemFactura  =", itemFactura)

    medicamentosRipsUnRegistro = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (tipo == 'MEDICAMENTOS'):

        detalle = 'SELECT ' + "'" + str('MEDICAMENTOS') + "'" + ' tipo, detCre.id detCreId, med.id,med."itemFactura", med."nomTecnologiaSalud" codigo, cums.nombre nombre, med."vrServicio",	med.consecutivo,  detCreRips."valorNota" 	FROM public.rips_ripsmedicamentos med inner join public.rips_ripscums cums  on (cums.id =med."codTecnologiaSalud_id") left join cartera_notascreditodetalle detCre on (detCre.id= ' + "'" + str(detCreId) + "')" + ' left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id"  = detCre.id AND  detCreRips."ripsMedicamentos_id" =med.id)  where med.id= ' + "'" + str(id) + "'"

    if (tipo == 'PROCEDIMIENTOS'):
        detalle = 'SELECT ' + "'" + str('PROCEDIMIENTOS') + "'" + ' tipo,  detCre.id detCreId, proc.id,proc."itemFactura", proc."codProcedimiento_id" codigo, exa.nombre nombre, proc."vrServicio",	proc.consecutivo,  detCreRips."valorNota" FROM public.rips_ripsprocedimientos proc inner join clinico_examenes exa  on (exa.id =proc."codProcedimiento_id") left join cartera_notascreditodetalle detCre on (detCre.id= ' + "'" + str(detCreId) + "')" + ' left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id"  = detCre.id AND detCreRips."ripsProcedimientos_id" =proc.id)  where proc.id= ' + "'" + str(id) + "'"

    if (tipo == 'CONSULTAS'):

        detalle = 'SELECT ' + "'" + str('CONSULTAS') + "'" + ' tipo, detCre.id detCreId, proc.id,proc."itemFactura", proc."codProcedimiento_id" codigo, exa.nombre nombre, proc."vrServicio",	proc.consecutivo,  detCreRips."valorNota" FROM public.rips_ripsconsultas proc inner join clinico_examenes exa  on (exa.id =proc."codConsulta_id") left join cartera_notascreditodetalle detCre on (detCre.id= ' + "'" + str(detCreId) + "')" + ' left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id"  = detCre.id AND detCreRips."ripsConsultas_id" =proc.id)  where proc.id= ' + "'" + str(id) + "'"

    if (tipo == 'OTROS SERVICIOS'):

        detalle = 'SELECT ' + "'" + str('OTROS SERVICIOS') + "'" + ' tipo, detCre.id detCreId, proc.id,proc."itemFactura", proc."codTecnologiaSaludCups_id" codigo, exa.nombre nombre, proc."vrServicio",	proc.consecutivo,  detCreRips."valorNota" FROM public.rips_ripsotrosservicios proc inner join clinico_examenes exa  on (exa.id =proc."codTecnologiaSalud_id") left join cartera_notascreditodetalle detCre on (detCre.id= ' + "'" + str(detCreId) + "')" + ' left join cartera_notascreditodetalleRips detCreRips on (detCreRips."notaCreditoDetalle_id"  = detCre.id AND detCreRips."ripsOtrosServicios_id" =proc.id)  where proc.id= ' + "'" + str(id) + "'"

    print(detalle)

    curx.execute(detalle)

    for tipo, detCreId ,id, itemFactura, codigo, nombre, vrServicio, consecutivo, valorNota in curx.fetchall():
        medicamentosRipsUnRegistro.append(
            {"model": "rips.ripsmedicamentos", "pk": id, "fields":
                {'tipo': tipo, 'detCreId':detCreId, 'id': id, 'itemFactura': itemFactura, 'codigo': codigo, 'nombre': nombre,
                 'vrServicio': vrServicio, 'consecutivo': consecutivo, 'valorNota': valorNota  }})

    miConexionx.close()
    print("medicamentosRipsUnRegistro ", medicamentosRipsUnRegistro)

    serialized1 = json.dumps(medicamentosRipsUnRegistro, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataCartera(request, data):

    print("Entre Load_dataCartera")

    context = {}
    d = json.loads(data)

    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)

    cartera = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT car.id, car.factura_id factura, fac."fechaFactura" fecha, emp.nombre empresa, usu.nombre, car.valor, car.pagos, car.saldo FROM cartera_cartera car, facturacion_facturacion fac, usuarios_usuarios usu, facturacion_empresas emp  WHERE car."sedesClinica_id" = ' + "'" + str(sedesClinica_id) + "' AND fac.id = car.factura_id AND " + 'fac."tipoDoc_id" = usu."tipoDoc_id" AND fac.documento_id = usu.id and emp.id=car.empresa_id'

    print ("detalle = ", detalle)

    curx.execute(detalle)

    for id,  factura, fecha, empresa, nombre,valor, pagos, saldo  in curx.fetchall():
        cartera.append(
            {"model": "cartera.cartera", "pk": id, "fields":
                {'id': id, 'factura': factura , 'fecha':fecha, 'empresa':empresa , 'nombre':nombre, 'valor': valor, 'pagos': pagos, 'saldo':saldo            }})



    miConexionx.close()
    print("cartera"  , cartera)

    serialized1 = json.dumps(cartera, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataPagosEmpresas(request, data):

    print("Entre Load_dataCartera")

    context = {}
    d = json.loads(data)

    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)


    empresaId = d['empresaId']
    print("empresaId = ", empresaId)


    pagosEmpresas = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT pag.id id, emp.nombre empresa, pag.fecha, forma.nombre formaPago, tipo.nombre tipoPago , pag.valor , pag.descripcion, pag."fechaRegistro", pag.radicado, serv.nombre servicio FROM cartera_pagosEmpresas pag INNER JOIN facturacion_empresas emp ON (emp.id=pag.empresa_id) INNER JOIN cartera_formaspagos forma ON (forma.id = pag."formaPago_id") INNER JOIN cartera_tipospagos tipo ON (tipo.id="tipoPago_id") LEFT JOIN sitios_serviciosadministrativos serv on (serv.id= pag."serviciosAdministrativos_id")  WHERE pag."sedesClinica_id" = ' + "'" + str(sedesClinica_id) + "' AND pag.empresa_id = "  + "'" + str(empresaId) + "'"

    print ("detalle = ", detalle)

    curx.execute(detalle)

    for id, empresa, fecha, formaPago, tipoPago, valor, descripcion, fechaRegistro,radicado, servicio  in curx.fetchall():
        pagosEmpresas.append(
            {"model": "cartera.pagosEmpresasa", "pk": id, "fields":
                {'id': id, 'empresa': empresa , 'fecha':fecha, 'formaPago':formaPago , 'tipoPago':tipoPago, 'valor': valor, 'descripcion': descripcion, 'fechaRegistro':fechaRegistro, 'radicado':radicado, 'servicio':servicio}})


    print("pagosEmpresasAntes"  , pagosEmpresas)
    miConexionx.close()
    print("pagosEmpresas"  , pagosEmpresas)

    serialized1 = json.dumps(pagosEmpresas, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def GuardarPagosEmpresas(request):

    print ("Entre GuardarPagosEmpresas" )


    serviciosAdministrativos = request.POST["servicio"]
    print("serviciosAdministrativos =", serviciosAdministrativos)
    fecha = request.POST["fechaPago"]
    print("fecha =", fecha)
    empresaPago = request.POST["empresaPago"]
    print("empresaPago =", empresaPago)
    formaPago= request.POST["formaPago"]
    print("formaPago =", formaPago)
    tipoPago= request.POST["tipoPago"]
    print("tipoPago =", tipoPago)

    valorPago= request.POST["valorPago"]
    print("valorPago =", valorPago)

    descripcionPago= request.POST["descripcionPago"]
    print("descripcionPago =", descripcionPago)

    radicado= request.POST["radicado"]
    print("radicado =", radicado)

    username = request.POST["usernamePago"]
    print("username =", username)
    sede = request.POST["sedePago"]
    print("sede =", sede)

    fechaRegistro = timezone.now()
    print("fechaRegistro", fechaRegistro)	

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        print ("armo comando")
        comando = 'INSERT INTO cartera_pagosempresas (fecha,valor,descripcion,"fechaRegistro", "estadoReg", empresa_id, "formaPago_id", "sedesClinica_id" , "serviciosAdministrativos_id", "tipoPago_id", radicado) VALUES ( ' + "'" + str(fecha) + "','" + str(valorPago) + "','" + str(descripcionPago) + "','" + str(fechaRegistro) + "','A','" + str(empresaPago) + "','" + str(formaPago) + "','" + str(sede) + "','" +  str(serviciosAdministrativos) + "','" + str(tipoPago) + "','" + str(radicado) + "')"

        print(comando)
        cur3.execute(comando)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Pago registrado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            #miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


def Load_dataPagosEmpresasDetalle(request, data):

    print("Entre Load_dataPagosEmpresasDetalle")

    context = {}
    d = json.loads(data)

    sedesClinica_id = d['sedesClinica_id']
    print("sedesClinica_id = ", sedesClinica_id)

    pagoId = d['pagoId']
    print("pagoId = ", pagoId)

    pagosEmpresasDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT pagDetalle.id id, pagDetalle.factura_id facturaId ,pagDetalle.valor, pagDetalle."radicadoFactura", serv.nombre nombreServicio FROM cartera_pagosEmpresas pag INNER JOIN cartera_pagosEmpresasdetalle pagDetalle ON (pagDetalle."pagosEmpresas_id"=pag.id)  LEFT JOIN sitios_serviciosadministrativos serv on (serv.id= pagDetalle."serviciosAdministrativos_id")  WHERE pagDetalle."pagosEmpresas_id" = ' + "'" + str(pagoId) + "'"

    print ("detalle = ", detalle)

    curx.execute(detalle)

    for id, facturaId, valor, radicadoFactura, nombreServicio  in curx.fetchall():
        pagosEmpresasDetalle.append(
            {"model": "cartera.pagosEmpresasDetalle", "pk": id, "fields":
                {'id': id, 'facturaId': facturaId , 'valor':valor, 'radicadoFactura':radicadoFactura , 'nombreServicio':nombreServicio}})


    miConexionx.close()
    print("pagosEmpresasDetalle"  , pagosEmpresasDetalle)

    serialized1 = json.dumps(pagosEmpresasDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def GuardarPagosEmpresasDetalle(request):

    print ("Entre GuardarPagosEmpresasDetalle" )


    serviciosAdministrativos = request.POST["servicioDetalle"]
    print("serviciosAdministrativos =", serviciosAdministrativos)

    valorPagoDetalle= request.POST["valorPagoDetalle"]
    print("valorPagoDetalle =", valorPagoDetalle)

    facturaPago = request.POST["facturaPago"]
    print("facturaPago =", facturaPago)

    radicadoPago= request.POST['radicadoPagoMuestra']
    print("radicadoPago =", radicadoPago)

    radicadoPago = request.POST["radicadoFactura"]
    print("radicadoPago =", radicadoPago)

    empresaPagoMuestra= request.POST["empresaPagoMuestra"]
    print("empresaPagoMuestra =", empresaPagoMuestra)

    username = request.POST["usernamePago_id"]
    print("username =", username)
    sede = request.POST["sedePago"]
    print("sede =", sede)

    fechaRegistro = timezone.now()
    print("fechaRegistro", fechaRegistro)	

    # Validaciones

    try:
        print("paso_00")
        with transaction.atomic():
            print("paso_0111")

            facturaId = Facturacion.objects.get(id=facturaPago)
            print("paso_01")
            if (facturaId.totalFactura > int(valorPagoDetalle)):
                print("paso_02")
                return JsonResponse({'success': False, 'Mensaje': 'Pago mayor que el valor de la Factura'})


    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por PRONO SE HACE NADA:", e)
        print ("Entre exception")
        #return JsonResponse({'success': False, 'Mensaje': e})
        return JsonResponse({'success': False, 'Mensajes': 'Factura No existe'})

    finally:
        print ("entre finally")
        pass

    print("paso_03")

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        print ("armo comando")
        comando = 'INSERT INTO cartera_pagosempresasDetalle (valor,"fechaRegistro", "estadoReg", factura_id, "pagosEmpresas_id" ,"radicadoFactura" , "serviciosAdministrativos_id") VALUES ( ' + "'" + str(valorPagoDetalle) + "','" + str(fechaRegistro) + "','A','" + str(facturaPago) + "','" + str(empresaPagoMuestra) + "','" + str(radicadoPago) + "','" +  str(serviciosAdministrativos) + "');"

        print(comando)
        cur3.execute(comando)

        comando = 'UPDATE cartera_cartera cartera SET pagos = pagos + ' + str(valorPagoDetalle) + ' WHERE cartera.factura_id = ' + "'" + str(facturaPago) + "'"

        print(comando)
        cur3.execute(comando)

        comando = 'UPDATE cartera_cartera cartera SET saldo = valor - pagos  WHERE cartera.factura_id = ' + "'" + str(facturaPago) + "'"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Pago Detalle registrado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            #miConexion3.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()




def Load_dataCarteraDetalle(request, data):

    print("Entre Load_dataCarteraDetalle")

    context = {}
    print("aqui01")
    d = json.loads(data)

    print("aqui02")

    sede = d['sedesClinica_id']
    print("sedesClinica_id = ", sede)

    facturaId = d['facturaId']
    print("facturaId = ", facturaId)

    carteraDetalle = []

    print ("carteraDetalle carteraDetalle = ")

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")

    curx = miConexionx.cursor()

    print ("antesde detalle = ")

    comando = 'select car.id id, emp.nombre nombreEmpresa,  pagosEmp.id pagoId, pagosEmp.fecha,car.factura_id factura,car.valor,car.pagos,car.saldo FROM  cartera_cartera car  LEFT JOIN cartera_pagosempresasdetalle pagDet ON (pagDet.factura_id = car.factura_id) LEFT JOIN cartera_pagosempresas pagosEmp ON (pagosEmp.id = pagDet."pagosEmpresas_id")  INNER JOIN facturacion_empresas emp on (emp.id=car.empresa_id) WHERE car."sedesClinica_id" = ' + "'" + str(sede) + "' AND pagDet.factura_id = " + "'" + str(facturaId) + "'"

    print ("comando = ", comando)

    curx.execute(comando)

    for id, nombreEmpresa, pagoId, fecha, factura, valor, pagos, saldo  in curx.fetchall():
        carteraDetalle.append(
            {"model": "cartera.pagosEmpresasDetalle", "pk": id, "fields":
                {'id': id, 'nombreEmpresa': nombreEmpresa , 'pagoId':pagoId, 'fecha':fecha , 'factura':factura, 'valor':valor, 'pagos':pagos, 'saldo':saldo}})


    miConexionx.close()
    print("carteraDetalle "  , carteraDetalle )

    serialized1 = json.dumps(carteraDetalle , default=str)

    return HttpResponse(serialized1, content_type='application/json')



def Load_dataEmpresas(request, data):

    print("Entre Load_dataEmpresas")

    context = {}
    print("aqui01")
    d = json.loads(data)

    print("aqui02")

    sede = d['sedesClinica_id']
    print("sedesClinica_id = ", sede)

    empresas = []


    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")

    curx = miConexionx.cursor()

    print ("antesde detalle = ")

    comando ='SELECT emp.id id, tipEmp.nombre tipoEmpresa,tipDoc.nombre  tipoDoc,  documento, emp.nombre empresa ,"codigoEapb",dep.nombre departamento, mun.nombre municipio, direccion, telefono,representante   FROM facturacion_empresas emp INNER JOIN sitios_departamentos dep on (dep.id= emp.departamento_id) INNER JOIN sitios_municipios mun on (mun.departamento_id = dep.id AND mun.id = emp.municipio_id) INNER JOIN usuarios_tiposdocumento tipDoc on (tipDoc.id = emp."tipoDoc_id") LEFT JOIN facturacion_tiposempresa tipEmp on (tipEmp.id=emp."tipoEmpresa_id") where emp."estadoReg" = ' + "'" + str('A') + "'" + ' order by emp.nombre'

    print ("comando = ", comando)

    curx.execute(comando)

    for id, tipoEmpresa, tipoDoc, documento, empresa, codigoEapb, departamento, municipio,direccion, telefono,  representante  in curx.fetchall():
        empresas.append(
            {"model": "cartera.Empresas", "pk": id, "fields":
                {'id': id, 'tipoEmpresa': tipoEmpresa , 'tipoDoc':tipoDoc, 'documento':documento , 'empresa':empresa,
                 'codigoEapb':codigoEapb, 'departamento':departamento, 'municipio':municipio, 'direccion':direccion, 'telefono': telefono, 'representante':representante}})


    miConexionx.close()
    print("empresas "  , empresas )

    serialized1 = json.dumps(empresas , default=str)

    return HttpResponse(serialized1, content_type='application/json')

