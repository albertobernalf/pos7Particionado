from django.shortcuts import render
import json
from django import forms
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
from django.http \
import JsonResponse
#import MySQLdb
import pyodbc
import psycopg2
import json 
import datetime as dt
#from datetime import datetime, timedelta, timezone
from datetime import  timedelta, timezone
from django.utils import timezone
from decimal import Decimal
from admisiones.models import Ingresos
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle, Refacturacion, Suministros, Conceptos, ConsecutivosDian
from cartera.models import TiposPagos, FormasPagos, Pagos, PagosFacturas
from triage.models import Triage
from clinico.models import Servicios, Examenes
import pickle
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.db.models import F
from cirugia.models import EstadosCirugias, EstadosProgramacion, Cirugias
from django.db.models import F
from sitios.models import ServiciosSedes, SedesClinica
from contratacion.models import Convenios
import os
import xmltodict
#import xml.etree.ElementTree as ET

import qrcode
import hashlib
#import xml.etree.ElementTree as etree
#from lxml import etree
#import xml.etree
from lxml import etree

import xmlsec

import base64
import zeep
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from zeep import Client , Plugin
from zeep.wsse.username import UsernameToken
from zeep.wsse.utils import WSU

#from signxml import XMLSigner
#from signxml.methods import detached, enveloping
from signxml import XMLSigner, XMLVerifier, namespaces
#from signxml import namespaces

from facturacion import serializers


from cryptography.hazmat.primitives import serialization
from cryptography import x509
from zeep import xsd
import zipfile
import logging
import sys
from zeep.plugins import HistoryPlugin
import traceback


class WsseTimestampPlugin(Plugin):
    """Plugin para inyectar Timestamp de forma segura sin conflictos de nombres."""
    def egress(self, envelope, http_headers, operation, binding_options):
        header = envelope.find('{http://xmlsoap.org}Header')
        if header is None:
            header = etree.SubElement(envelope, '{http://xmlsoap.org}Header')
        
        ns_wsu = "http://oasis-open.org"
        
        # Construir <wsu:Timestamp> con lxml
        timestamp = etree.Element(f'{{{ns_wsu}}}Timestamp')
        
        # Usando el alias 'dt' no habrá confusión con ninguna otra importación
        now = dt.datetime.now(dt.timezone.utc)
        expires = now + dt.timedelta(minutes=5)
        
        # Formatear las marcas de tiempo requeridas por la DIAN
        etree.SubElement(timestamp, f'{{{ns_wsu}}}Created').text = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        etree.SubElement(timestamp, f'{{{ns_wsu}}}Expires').text = expires.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        
        header.append(timestamp)
        return envelope, http_headers





def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 


# Create your views here.
def load_dataLiquidacion(request, data):
    print ("Entre load_data Liquidacion")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)
    

       # Combo Indicadores

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()


    comando = 'SELECT ser.nombre nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = sd.id AND dep.disponibilidad = ' + "'" + str('O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = '  + "'" + str('TRIAGE') + "'" + ' group by ser.nombre'

    curt.execute(comando)
    print(comando)

    indicadores = []

    for nombre, total in curt.fetchall():
        indicadores.append({'nombre': nombre, 'total':total})
        if (nombre == 'HOSPITALIZACION' ):
            context['Hospitalizados'] = total
        if (nombre == 'TRIAGE'):
            context['Triage'] = total
        if (nombre == 'URGENCIAS'):
            context['Urgencias'] = total
        if (nombre == 'AMBULATORIO'):
            context['Ambulatorios'] = total

    miConexiont.close()
    print(indicadores)

    context['Indicadores'] = indicadores

    total = len(indicadores)

    print ("total ", total)

    print("YA PASE INDICADORES")

# Fin combo Indicadores


    liquidacion = []

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",     password="123456")
    curx = miConexionx.cursor()
   
    #Esta es la original u propia


    #detalle = 'SELECT ' + "'" + str('INGRESO') + "'||'-'||i.id||'-'||case when conv.id != 0 then conv.id else " + "'" + str('00') + "'" + " end id, tp.nombre tipoDoc, u.documento documento,u.nombre nombre,i.consec consec , " + ' i."fechaIngreso" , i."fechaSalida", sd.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual,conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica FROM admisiones_ingresos i 	INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" 	and sd.id  = i."serviciosActual_id")  inner join clinico_servicios ser on (ser.id = sd.servicios_id) INNER JOIN  sitios_dependencias dep  ON (dep."sedesClinica_id" =  i."sedesClinica_id" and dep.id = i."dependenciasActual_id" and dep."serviciosSedes_id" = sd.id   AND  (dep.disponibilidad= ' + "'" + str('O') + "'" + ' OR (dep.disponibilidad = ' + "'" + str('L') + "'" + ' AND ser.id=3)) AND dep."serviciosSedes_id" = sd.id ) 	INNER JOIN sitios_dependenciastipo deptip ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" = i."tipoDoc_id" and u.id = i."documento_id" )  INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") 	INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxActual_id") LEFT JOIN facturacion_conveniospacienteingresos fac ON ( fac."tipoDoc_id" = i."tipoDoc_id" and fac.documento_id = i.documento_id and  fac."consecAdmision" = i.consec  and fac.factura_id is null) LEFT JOIN contratacion_convenios conv ON (conv.id  = fac.convenio_id) WHERE i."sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND ((i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' )) 	UNION SELECT ' + "'" + str('INGRESO') + "'||'-'||i.id||'-'||case when conv.id != 0 then conv.id else " +  "'" + str('00') + "'" + " end id, tp.nombre tipoDoc, 	u.documento documento,u.nombre nombre,i.consec consec ," + ' i."fechaIngreso" , i."fechaSalida", sd.nombre servicioNombreIng,	dep.nombre camaNombreIng , diag.nombre dxActual,conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica FROM admisiones_ingresos i 	INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" 	and sd.id  = i."serviciosActual_id")  inner join clinico_servicios ser on (ser.id = sd.servicios_id) INNER JOIN sitios_historialdependencias histdep  ON (histdep."tipoDoc_id" = i."tipoDoc_id" and histdep.documento_id=i.documento_id and histdep.consec=i.consec AND disponibilidad=' + "'" + str('O') + "')" + ' INNER JOIN sitios_dependencias dep ON (dep.id = histdep.dependencias_id) INNER JOIN sitios_dependenciastipo  deptip  ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN  usuarios_usuarios u  ON (u."tipoDoc_id" = i."tipoDoc_id" and u.id = i."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id")  INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxActual_id") LEFT JOIN  facturacion_conveniospacienteingresos  fac ON (fac."tipoDoc_id" = i."tipoDoc_id" and fac.documento_id = i.documento_id and fac."consecAdmision" = i.consec and fac.factura_id is null) LEFT JOIN contratacion_convenios conv ON (conv.id = fac.convenio_id) WHERE i."sedesClinica_id" = ' + "'" + str(sede) + "'" + '  AND ((i."salidaDefinitiva" = ' + "'" + str('R') + "'" + '))   UNION SELECT ' + "'" + str('TRIAGE') + "'" + "||'-'||" + ' t.id' + "||" + "'" + "-'||case when conv.id != 0 then conv.id else " + "'" + str('00') + "'" + ' end id, tp.nombre tipoDoc,u.documento documento,u.nombre nombre, t.consec consec , t."fechaSolicita" , cast(' + "'" + str('0001-01-01 00:00:00') + "'" + ' as timestamp) fechaSalida,sd.nombre servicioNombreIng, dep.nombre camaNombreIng , ' + "' '" + ' dxActual , conv.nombre convenio, conv.id convenioId , ' + "'" + str('N') + "'" + ' salidaClinica  FROM triage_triage t   INNER JOIN sitios_serviciosSedes sd ON (t."sedesClinica_id" = sd."sedesClinica_id" AND sd.id = t."serviciosSedes_id" )  INNER JOIN clinico_servicios ser ON ( ser.id = sd.servicios_id AND ser.nombre = ' + "'" + str('TRIAGE') + "')" + '  INNER JOIN  sitios_dependencias dep  ON (dep."sedesClinica_id" =  t."sedesClinica_id" and dep.id = t.dependencias_id  AND dep.disponibilidad = ' + "'" + str('O') + "'" + ' AND dep."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and t."consecAdmision" = 0 and dep."documento_id" = t."documento_id") INNER JOIN sitios_dependenciastipo deptip ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" = t."tipoDoc_id" and u.id = t."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") LEFT JOIN facturacion_conveniospacienteingresos fac ON ( fac."tipoDoc_id" = t."tipoDoc_id" and fac.documento_id = t.documento_id and  fac."consecAdmision" = t.consec ) LEFT JOIN contratacion_convenios conv ON (conv.id  = fac.convenio_id) WHERE  t."sedesClinica_id" = ' + "'" + str(sede) + "' UNION "  + 'SELECT ' + "'" + str("INGRESO") + "'" + "||'-'||i.id||'-'||case when conv.id != 0 then conv.id else " + "'" + str('00') + "'" + ' end id, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,i.consec consec , i."fechaIngreso" , i."fechaSalida", sd.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual,conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica FROM admisiones_ingresos i INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" 	and sd.id  = i."serviciosActual_id")   inner join clinico_servicios ser on (ser.id = sd.servicios_id)  INNER join sitios_historialdependencias histdep on (i."tipoDoc_id" = histdep."tipoDoc_id" and i.documento_id = histdep."documento_id" and i.consec=histdep.consec)  INNER JOIN  sitios_dependencias dep  ON (dep.id =  histdep.dependencias_id) INNER JOIN sitios_dependenciastipo deptip ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" = i."tipoDoc_id" and u.id = i.documento_id ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxActual_id") LEFT JOIN facturacion_conveniospacienteingresos fac ON ( fac."tipoDoc_id" = i."tipoDoc_id" and fac.documento_id = i.documento_id and  fac."consecAdmision" = i.consec )  LEFT JOIN contratacion_convenios conv ON (conv.id  = fac.convenio_id) inner join facturacion_refacturacion refact on (cast(refact."facturaAnulada" as integer)  = fac.factura_id)  WHERE i."sedesClinica_id" =  ' + "'" +  str(sede) + "'"  + ' AND ((i."salidaDefinitiva" = ' + "'" + str('R') + "'))" + 'and (histdep.id = (select max(histdep1.id) from sitios_historialdependencias histdep1 where histdep1."tipoDoc_id" = histdep."tipoDoc_id" and histdep1.documento_id = histdep.documento_id and histdep1.consec = histdep.consec))'
    detalle = 'SELECT ' + "'" + str('INGRESO') + "'||'-'||i.id||'-'||case when conv.id != 0 then conv.id else " + "'" + str('00') + "'" + " end id, tp.nombre tipoDoc, u.documento documento,u.nombre nombre,i.consec consec , " + ' i."fechaIngreso" , i."fechaSalida", sd.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual,conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica FROM admisiones_ingresos i 	INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" 	and sd.id  = i."serviciosActual_id")  inner join clinico_servicios ser on (ser.id = sd.servicios_id) INNER JOIN  sitios_dependencias dep  ON (dep."sedesClinica_id" =  i."sedesClinica_id" and dep.id = i."dependenciasActual_id" and dep."serviciosSedes_id" = sd.id   AND  (dep.disponibilidad= ' + "'" + str('O') + "'" + ' OR (dep.disponibilidad = ' + "'" + str('L') + "'" + ' AND ser.id=3)) AND dep."serviciosSedes_id" = sd.id ) 	INNER JOIN sitios_dependenciastipo deptip ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" = i."tipoDoc_id" and u.id = i."documento_id" )  INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") 	INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxActual_id") LEFT JOIN facturacion_conveniospacienteingresos fac ON ( fac."tipoDoc_id" = i."tipoDoc_id" and fac.documento_id = i.documento_id and  fac."consecAdmision" = i.consec  and fac.factura_id is null) LEFT JOIN contratacion_convenios conv ON (conv.id  = fac.convenio_id) WHERE i."sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND ((i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' ))    UNION SELECT ' + "'" + str('TRIAGE') + "'" + "||'-'||" + ' t.id' + "||" + "'" + "-'||case when conv.id != 0 then conv.id else " + "'" + str('00') + "'" + ' end id, tp.nombre tipoDoc,u.documento documento,u.nombre nombre, t.consec consec , t."fechaSolicita" , cast(' + "'" + str('0001-01-01 00:00:00') + "'" + ' as timestamp) fechaSalida,sd.nombre servicioNombreIng, dep.nombre camaNombreIng , ' + "' '" + ' dxActual , conv.nombre convenio, conv.id convenioId , ' + "'" + str('N') + "'" + ' salidaClinica  FROM triage_triage t   INNER JOIN sitios_serviciosSedes sd ON (t."sedesClinica_id" = sd."sedesClinica_id" AND sd.id = t."serviciosSedes_id" )  INNER JOIN clinico_servicios ser ON ( ser.id = sd.servicios_id AND ser.nombre = ' + "'" + str('TRIAGE') + "')" + '  INNER JOIN  sitios_dependencias dep  ON (dep."sedesClinica_id" =  t."sedesClinica_id" and dep.id = t.dependencias_id  AND dep.disponibilidad = ' + "'" + str('O') + "'" + ' AND dep."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and t."consecAdmision" = 0 and dep."documento_id" = t."documento_id") INNER JOIN sitios_dependenciastipo deptip ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" = t."tipoDoc_id" and u.id = t."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") LEFT JOIN facturacion_conveniospacienteingresos fac ON ( fac."tipoDoc_id" = t."tipoDoc_id" and fac.documento_id = t.documento_id and  fac."consecAdmision" = t.consec ) LEFT JOIN contratacion_convenios conv ON (conv.id  = fac.convenio_id) WHERE  t."sedesClinica_id" = ' + "'" + str(sede) + "' UNION "  + 'SELECT ' + "'" + str("INGRESO") + "'" + "||'-'||i.id||'-'||case when conv.id != 0 then conv.id else " + "'" + str('00') + "'" + ' end id, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,i.consec consec , i."fechaIngreso" , i."fechaSalida", sd.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual,conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica FROM admisiones_ingresos i INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" 	and sd.id  = i."serviciosActual_id")   inner join clinico_servicios ser on (ser.id = sd.servicios_id)  INNER join sitios_historialdependencias histdep on (i."tipoDoc_id" = histdep."tipoDoc_id" and i.documento_id = histdep."documento_id" and i.consec=histdep.consec)  INNER JOIN  sitios_dependencias dep  ON (dep.id =  histdep.dependencias_id) INNER JOIN sitios_dependenciastipo deptip ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" = i."tipoDoc_id" and u.id = i.documento_id ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxActual_id") LEFT JOIN facturacion_conveniospacienteingresos fac ON ( fac."tipoDoc_id" = i."tipoDoc_id" and fac.documento_id = i.documento_id and  fac."consecAdmision" = i.consec )  LEFT JOIN contratacion_convenios conv ON (conv.id  = fac.convenio_id) inner join facturacion_refacturacion refact on (cast(refact."facturaAnulada" as integer)  = fac.factura_id)  WHERE i."sedesClinica_id" =  ' + "'" +  str(sede) + "'"  + ' AND ((i."salidaDefinitiva" = ' + "'" + str('R') + "'))" + 'and (histdep.id = (select max(histdep1.id) from sitios_historialdependencias histdep1 where histdep1."tipoDoc_id" = histdep."tipoDoc_id" and histdep1.documento_id = histdep.documento_id and histdep1.consec = histdep.consec))'
    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual , convenio, convenioId, salidaClinica in curx.fetchall():
        liquidacion.append(
		{"model":"ingresos.ingresos","pk":id,"fields":
			{ 'id':id, 'tipoDoc': tipoDoc, 'documento': documento, 'nombre': nombre, 'consec': consec,
                         'fechaIngreso': fechaIngreso, 'fechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'dxActual': dxActual,'convenio':convenio, 'convenioId':convenioId,'salidaClinica':salidaClinica }})

    miConexionx.close()
    print(liquidacion)
    context['Liquidacion'] = liquidacion

    serialized1 = json.dumps(liquidacion, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')


def PostConsultaLiquidacion(request):
    print ("Entre PostConsultaLiquidacion ")

    Post_id = request.POST["post_id"]
    username_id = request.POST["username_id"]
    sede = request.POST["sede"]


    print("id = ", Post_id)
    llave = Post_id.split('-')
    print ("llave = " ,llave)
    print ("primero=" ,llave[0])
    print("segundo = " ,llave[1])
    print("tercero o convenio  = " ,llave[2])

    # Combo TiposPagos

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id,c.nombre nombre FROM cartera_tiposPagos c order by c.nombre'

    curt.execute(comando)
    print(comando)

    tiposPagos = []

    #tiposPagos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposPagos.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    print(tiposPagos)

    #context['TiposPagos'] = tiposPagos

    # Fin combo tiposPagos


    # Combo FormasPago

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id,c.nombre nombre FROM cartera_formasPagos c order by c.nombre'

    curt.execute(comando)
    print(comando)

    formasPagos = []

    #formasPagos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        formasPagos.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    print(formasPagos)


    # Fin combo formasPagos

    # Combo Cups

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id,c.nombre ||' + "'" + str(' ') + "'" +  '||c."codigoCups" nombre FROM clinico_examenes c order by c.nombre'

    curt.execute(comando)
    print(comando)

    cups = []

    cups.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        cups.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    print(cups)


    # Fin combo Cups


    # Combo Suministros

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    #comando = 'SELECT c.id id, c.nombre||' + "' '" +  '||c.cums nombre FROM facturacion_suministros c order by c.nombre'
    comando = 'SELECT c.id id, c.nombre||' + "' '||" + 'c.cums nombre FROM facturacion_suministros c order by c.nombre'

    curt.execute(comando)
    print(comando)

    suministros = []

    suministros.append({'id': '', 'nombre': ''})

    for id,  nombre in curt.fetchall():
        suministros.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    print(suministros)

    # Fin combo suministros

    convenioId = llave[2]
    convenioId = convenioId.strip()

    print("Convenio despues de strip = ", convenioId)
    print("convenioId FINAL= ", convenioId)

    if llave[0] == 'INGRESO':
        ingresoId = Ingresos.objects.get(id=llave[1])
        print ("ingresoId = ", ingresoId)
        print ("tipodDoc_id =" ,ingresoId.tipoDoc_id)
        print("documento_id =", ingresoId.documento_id)
        print("consec =", ingresoId.consec)
    else:
        triageId = Triage.objects.get(id=llave[1])
        print ("triageId = ", triageId.id)
        print ("tipodDoc_id =" ,triageId.tipoDoc_id)
        print("documento_id =", triageId.documento_id)
        print("consec =", triageId.consec)


    estadoReg= 'A'
    fechaRegistro = timezone.now()


    # Primero colocamos el convenio en la tabla facturacion_facturacionliquidacion

    ##Liquidacion.objects.filter(tipoDoc_id=str(ingresoId.tipoDoc_id),documento_id=str(ingresoId.documento_id),consecAdmision = str(ingresoId.consec)).update(convenio_id=convenioId)

    # Validacion si existe o No existe CABEZOTE

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres", password="123456")

    curt = miConexiont.cursor()

    if llave[0] == 'INGRESO':
        #if (convenioId == '0'):

        #    print ("Entre Convenio=0 ");
        #    comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + str(ingresoId.tipoDoc_id) + ' AND documento_id = ' + str(ingresoId.documento_id) + ' AND "consecAdmision" = ' + str(ingresoId.consec) + ' and convenio_id is null'
        #else:
        #print ("Entre Convenio = " , convenioId);
        comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + str(ingresoId.tipoDoc_id) + ' AND documento_id = ' + str(ingresoId.documento_id) + ' AND "consecAdmision" = ' + str(ingresoId.consec) + ' and convenio_id = ' + "'" + str(convenioId) + "'"

    else:
        #if (convenioId == '0' ):
        #    comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + str(triageId.tipoDoc_id) + ' AND documento_id = ' + str(triageId.documento_id) + ' AND "consecAdmision" = ' + str(triageId.consec) + ' and convenio_id is null'
        #else:
        comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + str(triageId.tipoDoc_id) + ' AND documento_id = ' + str(triageId.documento_id) + ' AND "consecAdmision" = ' + str(triageId.consec) + ' and convenio_id = ' + "'" + str(convenioId) + "'"

    curt.execute(comando)
    print(comando)
    cabezoteLiquidacion = []

    for id in curt.fetchall():
        cabezoteLiquidacion.append({'id': id})

    miConexiont.close()

    print ("OJOOOOO cabezoteLiquidacion"  , cabezoteLiquidacion)

    cabezote = str(cabezoteLiquidacion)
    cabezote = cabezote.replace("[", ' ')
    cabezote = cabezote.replace("]", ' ')
    cabezote = cabezote.replace("(", ' ')
    cabezote = cabezote.replace(")", ' ')
    cabezote = cabezote.replace(",", ' ')
    print("OJOOOOO cabezote", cabezote)


    miConexiont = None
    try:

      if (cabezoteLiquidacion == []):
                print ("OJOOOOOO ENTRE AL CABEZOTE LIQUIDACION")
                # Si no existe liquidacion CABEZOTE se debe crear con los totales, abonos, anticipos, procedimiento, suministros etc


                miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432",       user="postgres", password="123456")
                curt = miConexiont.cursor()

                #if (llave[0] == 'INGRESO'  and convenioId == '0') :

                #        comando = 'INSERT INTO facturacion_liquidacion ("tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos" , "totalRecibido" , "sedesClinica_id" , anulado) VALUES (' + str(ingresoId.tipoDoc_id)  + ',' +  str(ingresoId.documento_id) + ',' + str(ingresoId.consec) + ',' +  "'" +  str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "', null"  + ',' + "'" + str(username_id) + "',0,0," + "'" + str(sede) + "','A') RETURNING id"
                #        print ("Entre1")

                #if (llave[0] == 'INGRESO' and convenioId != '0'):
                if (llave[0] == 'INGRESO'):

                    	 comando = 'INSERT INTO facturacion_liquidacion ("tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos" , "totalRecibido" , "sedesClinica_id" , anulado) VALUES (' + str(ingresoId.tipoDoc_id)  + ',' +  str(ingresoId.documento_id) + ',' + str(ingresoId.consec) + ',' +  "'" +  str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(convenioId) + ',' + "'" + str(username_id) + "',0,0," + "'" + str(sede) + "','A') RETURNING id"
                #        print("Entre2")

                #if (llave[0] == 'TRIAGE' and  convenioId == '0'):
                else:

                #        comando = 'INSERT INTO facturacion_liquidacion ("tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos" , "totalRecibido" , "sedesClinica_id" , anulado) VALUES (' + str(triageId.tipoDoc_id)  + ',' +  str(triageId.documento_id) + ',' + str('0') + ',' +  "'" +  str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "', null" + ',' + "'" + str(username_id) + "',0,0," + "'" + str(sede) + "','A') RETURNING id"
                #        print("Entre3")

                #if (llave[0] == 'TRIAGE' and  convenioId != '0'):

                         comando = 'INSERT INTO facturacion_liquidacion ("tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos" , "totalRecibido" , "sedesClinica_id" , anulado) VALUES (' + str(triageId.tipoDoc_id)  + ',' +  str(triageId.documento_id) + ',' + str('0') + ',' +  "'" +  str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(convenioId) + ',' + "'" + str(username_id) + "',0,0," + "'" + str(sede) + "','A') RETURNING id"
                #        print("Entre4")

                print("comando =" , comando)

                curt.execute(comando)
                liquidacionId = curt.fetchone()[0]
                print("liquidacionId PARCIAL = ", liquidacionId)
                miConexiont.commit()
                curt.close()
                miConexiont.close()

      else:
                print("Por qui no entro")
                liquidacionId = cabezoteLiquidacion[0]['id']
                liquidacionId = str(liquidacionId)
                print("liquidacionId = ", liquidacionId)
                liquidacionId = str(liquidacionId)
                liquidacionId = liquidacionId.replace("(", ' ')
                liquidacionId = liquidacionId.replace(")", ' ')
                liquidacionId = liquidacionId.replace(",", ' ')

      print("liquidacionId FINAL = ", liquidacionId)


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


    # Fin validacion de Liquidacion cabezote

    if request.method == 'POST':

        # Abro Conexion

        miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",password="123456")
        cur = miConexionx.cursor()

        if llave[0] == 'INGRESO':	

            #comando = 'select ' + "'"  + str('INGRESO') + "'" + '  tipo, liq.id id,  "consecAdmision",  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,"totalSuministros", "totalLiquidacion", "valorApagar", "fechaCorte", anticipos, "detalleAnulacion", "fechaAnulacion", observaciones, liq."fechaRegistro", "estadoRegistro", convenio_id, liq."tipoDoc_id" , liq.documento_id, liq."usuarioRegistro_id", "totalAbonos", conv.nombre nombreConvenio, usu.nombre paciente, adm.id ingresoId1, usu.documento documento, tip.nombre tipoDocumento FROM facturacion_liquidacion liq, contratacion_convenios conv, usuarios_usuarios usu, admisiones_ingresos adm, usuarios_tiposdocumento  tip where adm.id = ' + "'" + str(llave[1]) + "'" + '  AND  liq.convenio_id = conv.id and usu.id = liq.documento_id  and adm."tipoDoc_id" = liq."tipoDoc_id"   AND tip.id = adm."tipoDoc_id" AND adm.documento_id = liq.documento_id  AND adm.consec = liq."consecAdmision" AND conv.id = ' + str(convenioId)
            comando =  'select ' + "'"  + str('INGRESO') + "'" + '  tipo, adm."salidaDefinitiva" salidaDefinitiva,liq.id id, dep.nombre dependenciaNombre, sd.nombre servicioNombre , "consecAdmision",  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,"totalSuministros", "totalLiquidacion", "valorApagar", "fechaCorte", anticipos, "detalleAnulacion", "fechaAnulacion", observaciones,  liq."fechaRegistro", "estadoRegistro", liq.convenio_id, liq."tipoDoc_id" , liq.documento_id, liq."usuarioRegistro_id", "totalAbonos",  conv.nombre nombreConvenio, usu.nombre paciente, adm.id ingresoId1, usu.documento documento, tip.nombre tipoDocumento , adm."salidaClinica" salidaClinica FROM facturacion_liquidacion liq INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id" = liq."tipoDoc_id" AND usu.id = liq.documento_id) INNER JOIN admisiones_ingresos adm ON (adm."tipoDoc_id" = liq."tipoDoc_id"  AND adm.documento_id = liq.documento_id  AND adm.consec = liq."consecAdmision"  ) INNER JOIN usuarios_tiposdocumento  tip ON (tip.id = adm."tipoDoc_id")  LEFT JOIN sitios_serviciossedes sd ON (sd.id=adm."serviciosActual_id") LEFT JOIN clinico_servicios serv ON (serv.id = sd.servicios_id) LEFT JOIN sitios_dependencias dep on (dep.id =adm."dependenciasActual_id") LEFT JOIN  contratacion_convenios conv ON (conv.id = liq.convenio_id) where liq.id = ' + "'" +  str(liquidacionId) + "'" + ' AND adm.id = ' + "'" + str(llave[1]) + "'"
            comandoP = 'SELECT conv.id, conv.nombre FROM contratacion_convenios conv INNER JOIN facturacion_conveniospacienteingresos convPac ON (convPac.convenio_id = conv.id) WHERE convPac."tipoDoc_id" = ' + "'" + str(ingresoId.tipoDoc_id) + "'" + ' AND convPac.documento_id =  ' + "'" + str(ingresoId.documento_id) + "'" + ' AND convPac."consecAdmision" = ' + "'" + str(ingresoId.consec) + "'"
        else:

            #comando = 'select ' + "'"  + str('TRIAGE') + "'" + ' tipo, liq.id id,  tri."consecAdmision" consecAdmision,  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,"totalSuministros", "totalLiquidacion", "valorApagar", "fechaCorte", anticipos, "detalleAnulacion", "fechaAnulacion", tri.observaciones, liq."fechaRegistro", "estadoRegistro", convenio_id, liq."tipoDoc_id" , liq.documento_id, liq."usuarioRegistro_id", "totalAbonos", conv.nombre nombreConvenio, usu.nombre paciente, tri.id triageId1, usu.documento documento, tip.nombre tipoDocumento FROM facturacion_liquidacion liq, contratacion_convenios conv, usuarios_usuarios usu, triage_triage tri, usuarios_tiposdocumento  tip where tri.id = ' + "'" + str(llave[1]) + "'" + '  AND  liq.convenio_id = conv.id and usu.id = liq.documento_id  and tri."tipoDoc_id" = liq."tipoDoc_id"   AND tip.id = tri."tipoDoc_id" AND tri.documento_id = liq.documento_id  AND tri.consec = liq."consecAdmision" AND conv.id = ' + str(convenioId)
            comando =  'select ' + "'"  + str('TRIAGE') + "'" + ' tipo, tri."salidaDefinitiva" salidaDefinitiva, liq.id id, ' + "'" + str('Triage') + "'" + ' dependenciaNombre, ' + "'" + str('TRIAGE') + "'" + '  servicioNombre, tri."consecAdmision",  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,"totalSuministros", "totalLiquidacion", "valorApagar", "fechaCorte", anticipos, "detalleAnulacion", "fechaAnulacion", tri.observaciones, liq."fechaRegistro", "estadoRegistro", liq.convenio_id, liq."tipoDoc_id" , liq.documento_id, liq."usuarioRegistro_id", "totalAbonos", conv.nombre nombreConvenio, usu.nombre paciente, tri.id triageId1, usu.documento documento, tip.nombre tipoDocumento, ' + "'N'" + ' salidaClinica  FROM facturacion_liquidacion liq inner join  triage_triage tri on (tri."tipoDoc_id" = liq."tipoDoc_id"  and tri.documento_id = liq.documento_id  AND tri.consec = liq."consecAdmision" ) left join  contratacion_convenios conv on (conv.id = liq.convenio_id) inner join  usuarios_usuarios usu on (usu."tipoDoc_id" = liq."tipoDoc_id" AND usu.id = liq.documento_id) inner join usuarios_tiposdocumento  tip on (tip.id = usu."tipoDoc_id") where liq.id = ' + "'" +  str(liquidacionId) + "'" + ' AND tri.id = ' + "'" + str(llave[1]) + "'"
            comandoP = 'SELECT conv.id id, conv.nombre nombre FROM contratacion_convenios conv INNER JOIN facturacion_conveniospacienteingresos convPac ON (convPac.convenio_id = conv.id) WHERE convPac."tipoDoc_id" = ' + "'" + str(triageId.tipoDoc_id) + "'" + ' AND convPac.documento_id =  ' + "'" + str(triageId.documento_id) + "'" + ' AND convPac."consecAdmision" = ' + "'" + str(triageId.consec) + "'"
            print(comando)

        cur.execute(comando)

        liquidacion = []

        if llave[0] == 'INGRESO':

          for tipo, salidaDefinitiva,id, dependenciaNombre, servicioNombre, consecAdmision,fecha ,totalCopagos,totalCuotaModeradora,totalProcedimientos ,totalSuministros, totalLiquidacion, valorApagar, fechaCorte, anticipos, detalleAnulacion, fechaAnulacion, observaciones, fechaRegistro, estadoRegistro, convenio_id, tipoDoc_id , documento_id, usuarioRegistro_id, totalAbonos, nombreConvenio , paciente, ingresoId1 , documento, tipoDocumento, salidaClinica in cur.fetchall():
            liquidacion.append( {"tipo":tipo, "salidaDefinitiva":salidaDefinitiva, "id": id, "dependenciaNombre":dependenciaNombre,"servicioNombre":servicioNombre,
                     "consecAdmision": consecAdmision,
                     "fecha": fecha,
                     "totalCopagos": totalCopagos, "totalCuotaModeradora": totalCuotaModeradora,
                     "totalProcedimientos": totalProcedimientos,
                                 "totalSuministros": totalSuministros,
                                 "totalLiquidacion": totalLiquidacion, "valorApagar": valorApagar,
                                 "fechaCorte": fechaCorte,  "anticipos": anticipos,
                                 "detalleAnulacion": detalleAnulacion,  "fechaAnulacion": fechaAnulacion,  "observaciones": observaciones,
                                 "fechaRegistro": fechaRegistro, "estadoRegistro": estadoRegistro, "convenio_id": convenio_id,
            "tipoDoc_id": tipoDoc_id, "documento_id":documento_id,  "usuarioRegistro_id": usuarioRegistro_id,
            "totalAbonos": totalAbonos, "nombreConvenio": nombreConvenio,   "paciente": paciente,
            "ingresoId1": ingresoId1, "documento": documento, "tipoDocumento": tipoDocumento, "salidaClinica":salidaClinica
                                 })
        else:
          for tipo, salidaDefinitiva, id, dependenciaNombre, servicioNombre, consecAdmision,fecha ,totalCopagos,totalCuotaModeradora,totalProcedimientos ,totalSuministros, totalLiquidacion, valorApagar, fechaCorte, anticipos, detalleAnulacion, fechaAnulacion, observaciones, fechaRegistro, estadoRegistro, convenio_id, tipoDoc_id , documento_id, usuarioRegistro_id, totalAbonos, nombreConvenio , paciente, triageId1 , documento, tipoDocumento , salidaClinica in cur.fetchall():
            liquidacion.append( { "tipo":tipo, "salidaDefinitiva":salidaDefinitiva, "id": id, "dependenciaNombre":dependenciaNombre,"servicioNombre":servicioNombre,
                     "consecAdmision": consecAdmision,
                     "fecha": fecha,
                     "totalCopagos": totalCopagos, "totalCuotaModeradora": totalCuotaModeradora,
                     "totalProcedimientos": totalProcedimientos,
                                 "totalSuministros": totalSuministros,
                                 "totalLiquidacion": totalLiquidacion, "valorApagar": valorApagar,
                                 "fechaCorte": fechaCorte,  "anticipos": anticipos,
                                 "detalleAnulacion": detalleAnulacion,  "fechaAnulacion": fechaAnulacion,  "observaciones": observaciones,
                                 "fechaRegistro": fechaRegistro, "estadoRegistro": estadoRegistro, "convenio_id": convenio_id,
            "tipoDoc_id": tipoDoc_id, "documento_id":documento_id,  "usuarioRegistro_id": usuarioRegistro_id,
            "totalAbonos": totalAbonos, "nombreConvenio": nombreConvenio,   "paciente": paciente,
            "triageId1": triageId1, "documento": documento, "tipoDocumento": tipoDocumento, "salidaClinica":salidaClinica
                                 })

        miConexionx.close()
        print("liquidacion = " , liquidacion)

        ##Conveniso Paciente

        conveniosPaciente = []

        miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curx = miConexionx.cursor()
        curx.execute(comandoP)

        for id, nombre in curx.fetchall():
            conveniosPaciente.append({'id': id, 'nombre': nombre})

        miConexionx.close()
        print("conveniosPaciente = " ,conveniosPaciente)

        # Cierro Conexion

        if llave[0] == 'INGRESO':


            ## esto traigo de cirugia


            ## FIN esto traigo de cirugia
            pass

        else:

            ## esto traigo de cirugia
            pass

            # Rutina Guarda en cabezote los totales

            ## FIN esto traigo de cirugia

        if llave[0] == 'INGRESO':

            return JsonResponse({'pk':liquidacion[0]['id'],'tipo':liquidacion[0]['tipo'], 'salidaDefinitiva':liquidacion[0]['salidaDefinitiva'] , 'id':liquidacion[0]['id'],  "dependenciaNombre":liquidacion[0]['dependenciaNombre'] ,"servicioNombre":liquidacion[0]['servicioNombre'],'consecAdmision':liquidacion[0]['consecAdmision'],'fecha':liquidacion[0]['fecha'],
                             'totalCopagos':liquidacion[0]['totalCopagos'],  'totalCuotaModeradora': liquidacion[0]['totalCuotaModeradora'],
                             'totalProcedimientos': liquidacion[0]['totalProcedimientos'],
                             'totalSuministros': liquidacion[0]['totalSuministros'],
                             'totalLiquidacion': liquidacion[0]['totalLiquidacion'],
                             'fechaCorte': liquidacion[0]['fechaCorte'],
                             'valorApagar': liquidacion[0]['valorApagar'],
                             'anticipos': liquidacion[0]['anticipos'],
                             'detalleAnulacion': liquidacion[0]['detalleAnulacion'],
                             'fechaAnulacion': liquidacion[0]['fechaAnulacion'],
                             'observaciones': liquidacion[0]['observaciones'],
                             'fechaRegistro': liquidacion[0]['fechaRegistro'],
                             'estadoRegistro': liquidacion[0]['estadoRegistro'],
                             'convenio_id': liquidacion[0]['convenio_id'],
                             'tipoDoc_id': liquidacion[0]['tipoDoc_id'],
                             'documento_id': liquidacion[0]['documento_id'],
                             'usuarioRegistro_id': liquidacion[0]['usuarioRegistro_id'],
                             'totalAbonos': liquidacion[0]['totalAbonos'],
                             'nombreConvenio': liquidacion[0]['nombreConvenio'],
                             'paciente': liquidacion[0]['paciente'], 'Suministros':suministros, 'Cups':cups,
                            'TiposPagos':tiposPagos, 'FormasPagos':formasPagos,
			     'ingresoId1': ingresoId1, 'documento': documento, 'tipoDocumento': tipoDocumento, 'ConveniosPaciente':conveniosPaciente,
                                'salidaClinica':salidaClinica

            })
        else:
            return JsonResponse(
                {'pk': liquidacion[0]['id'], 'tipo':liquidacion[0]['tipo'], 'salidaDefinitiva':liquidacion[0]['salidaDefinitiva'] , 'id':liquidacion[0]['id'] ,"dependenciaNombre":liquidacion[0]['dependenciaNombre'] ,"servicioNombre":liquidacion[0]['servicioNombre'],  'consecAdmision': liquidacion[0]['consecAdmision'],
                 'fecha': liquidacion[0]['fecha'],
                 'totalCopagos': liquidacion[0]['totalCopagos'],
                 'totalCuotaModeradora': liquidacion[0]['totalCuotaModeradora'],
                 'totalProcedimientos': liquidacion[0]['totalProcedimientos'],
                 'totalSuministros': liquidacion[0]['totalSuministros'],
                 'totalLiquidacion': liquidacion[0]['totalLiquidacion'],
                 'fechaCorte': liquidacion[0]['fechaCorte'],
                 'valorApagar': liquidacion[0]['valorApagar'],
                 'anticipos': liquidacion[0]['anticipos'],
                 'detalleAnulacion': liquidacion[0]['detalleAnulacion'],
                 'fechaAnulacion': liquidacion[0]['fechaAnulacion'],
                 'observaciones': liquidacion[0]['observaciones'],
                 'fechaRegistro': liquidacion[0]['fechaRegistro'],
                 'estadoRegistro': liquidacion[0]['estadoRegistro'],
                 'convenio_id': liquidacion[0]['convenio_id'],
                 'tipoDoc_id': liquidacion[0]['tipoDoc_id'],
                 'documento_id': liquidacion[0]['documento_id'],
                 'usuarioRegistro_id': liquidacion[0]['usuarioRegistro_id'],
                 'totalAbonos': liquidacion[0]['totalAbonos'],
                 'nombreConvenio': liquidacion[0]['nombreConvenio'],
                 'paciente': liquidacion[0]['paciente'], 'Suministros': suministros, 'Cups': cups,
                 'TiposPagos': tiposPagos,
                 'FormasPagos': formasPagos,
                 'triageId1': triageId1, 'documento': documento, 'tipoDocumento': tipoDocumento , 'ConveniosPaciente':conveniosPaciente,
                 'salidaClinica': salidaClinica

                 })

    else:
        datosMensaje = {'success': True, 'Mensaje': 'Something went wrong!'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')


def load_dataLiquidacionDetalle(request, data):
    print("Entre load_data LiquidacionDetalle")

    context = {}

    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    #valor = d['valor']
    liquidacionId = d['liquidacionId']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("liquidacionId:",liquidacionId)


    # Abro Conexion para la Liquidacion Detalle

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexionx.cursor()

    comando = 'select liq.id id,consecutivo ,  cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" , hono.nombre tipoHonorario, cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , exa.nombre||' + "' '||" + ' "codigoCups"  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg, liq.anulado anulado   FROM facturacion_liquidaciondetalle liq LEFT JOIN tarifarios_tiposhonorarios hono ON (hono.id = liq."tipoHonorario_id") inner join clinico_examenes exa on (exa.id = liq."examen_id")  where liquidacion_id= ' + "'" +  str(liquidacionId) + "'" +  ' UNION select liq.id id,consecutivo , cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" , hono.nombre tipoHonorario,  cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre||' + "' '||" + 'cums  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg , liq.anulado anulado FROM facturacion_liquidaciondetalle liq LEFT JOIN tarifarios_tiposhonorarios hono ON (hono.id = liq."tipoHonorario_id")  inner join facturacion_suministros sum on (sum.id = liq.cums_id)  where liquidacion_id= '  + "'" +  str(liquidacionId) + "'" + ' ORDER BY consecutivo'

    print(comando)

    cur.execute(comando)

    liquidacionDetalle = []

    for id, consecutivo, fecha, cantidad, valorUnitario, valorTotal, tipoHonorario, cirugia, fechaCrea, observaciones, estadoRegistro, examen_id, cums_id, nombreExamen, liquidacion_id, tipoHonorario_id, tipoRegistro, estadoReg, anulado in cur.fetchall():
        liquidacionDetalle.append(
            {"model": "liquidacionDetalle.liquidacionDetalle", "pk": id, "fields":
                {"id": id, "consecutivo": consecutivo,
                 "fecha": fecha,
                 "cantidad": cantidad,
                 "valorUnitario": valorUnitario, "valorTotal": valorTotal, "tipoHonorario":tipoHonorario,
                 "cirugia": cirugia,
                 #"fechaCrea": fechaCrea,
                 "observaciones": observaciones,
                 "estadoRegistro": estadoRegistro, "examen_id": examen_id,
                 "cums_id": cums_id, "nombreExamen": nombreExamen,
                 "liquidacion_id": liquidacion_id, "tipoHonorario_id": tipoHonorario_id,
                 "tipoRegistro": tipoRegistro, "estadoReg":estadoReg,'anulado':anulado}})

    miConexionx.close()
    print("Envio esto : " , liquidacionDetalle)


    # Cierro Conexion

    #Ojo probar estop
    #serializedPrueba = pickle.dumps(liquidacionDetalle)
    serialized1 = json.dumps(liquidacionDetalle, default=decimal_serializer)
    #serialized1 = json.dumps(liquidacionDetalle, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')


def PostConsultaLiquidacionDetalle(request):
    print ("Entre PostConsultaLiquidacionDetalle ")
    post_id =  request.POST["post_id"]

    # Combo Cups

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id,c.nombre ||' + "'" + str(' ') + "'" +  '||c."codigoCups" nombre FROM clinico_examenes c order by c.nombre'

    curt.execute(comando)
    print(comando)

    cups = []

    cups.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        cups.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    #print(cups)


    # Fin combo Cups


    # Combo Suministros

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()


    comando = 'SELECT c.id id, c.nombre nombre FROM facturacion_suministros c order by c.nombre'

    curt.execute(comando)
    print(comando)

    suministros = []

    suministros.append({'id': '', 'nombre': ''})

    for id,  nombre in curt.fetchall():
        suministros.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    #print(suministros)

    # Fin combo suministros

    # Aqui RUTINA Leer el registro liquidacionDetalle


    miConexionx = None
    try:

            miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curx = miConexionx.cursor()

            #comando = 'select liq.id id,consecutivo ,  cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id cirugia ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , exa.nombre  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro"  FROM facturacion_liquidaciondetalle liq left join clinico_examenes exa on (exa.id = liq."examen_id")  where liq.liquidacion_id= ' + str(post_id)  +  ' UNION select liq.id id,consecutivo , cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id cirugia ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro"  FROM facturacion_liquidaciondetalle liq left join facturacion_suministros sum on (sum.id = liq.cums_id)  where liq.id= '  + str(post_id)
            comando = 'select liq.id id,consecutivo ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id cirugia ,    liq.observaciones ,  "estadoRegistro" ,  examen_id ,  cums_id , exa.nombre  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro"  FROM facturacion_liquidaciondetalle liq inner join clinico_examenes exa on (exa.id = liq.examen_id)  where liq.id= ' + str(post_id)  +  ' UNION select liq.id id,consecutivo , liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id cirugia ,   liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro"  FROM facturacion_liquidaciondetalle liq inner join facturacion_suministros sum on (sum.id = liq.cums_id)  where liq.id= '  + str(post_id)

            print(comando)

            curx.execute(comando)

            liquidacionDetalleU = []

            for id, consecutivo, cantidad, valorUnitario, valorTotal, cirugia,  observaciones, estadoRegistro, examen_id, cums_id, nombreExamen, liquidacion_id, tipoHonorario_id, tipoRegistro in curx.fetchall():
                liquidacionDetalleU.append(
                      {'id': id, 'consecutivo': consecutivo, 'cantidad': cantidad, 'valorUnitario': valorUnitario, 'valorTotal': valorTotal,
                         'cirugia': cirugia, 'observaciones': observaciones,'estadoRegistro': estadoRegistro, 'examen_id': examen_id,
                         'cums_id': cums_id, 'nombreExamen': nombreExamen,'liquidacion_id': liquidacion_id, 'tipoHonorario_id': tipoHonorario_id,
                         'tipoRegistro': tipoRegistro})

            miConexionx.close()
            print("Que pasa liquidacionDetalleU =" , post_id)
            print(liquidacionDetalleU)
            # Cierro Conexion


            return JsonResponse({'pk':liquidacionDetalleU[0]['id'], 'id':liquidacionDetalleU[0]['id'], 'consecutivo':liquidacionDetalleU[0]['consecutivo'],'cantidad':liquidacionDetalleU[0]['cantidad'],
                                     'valorUnitario':liquidacionDetalleU[0]['valorUnitario'],  'valorTotal': liquidacionDetalleU[0]['valorTotal'],
                                     'cirugia': liquidacionDetalleU[0]['cirugia'], 'observaciones': liquidacionDetalleU[0]['observaciones'],
                                     'estadoRegistro': liquidacionDetalleU[0]['estadoRegistro'],  'examen_id': liquidacionDetalleU[0]['examen_id'],
                                     'cums_id': liquidacionDetalleU[0]['cums_id'], 'liquidacion_id': liquidacionDetalleU[0]['liquidacion_id'],
                                     'tipoHonorario_id': liquidacionDetalleU[0]['tipoHonorario_id'], 'tipoRegistro': liquidacionDetalleU[0]['tipoRegistro'], 'Cups': cups, 'Suministros': suministros
                                                                })
    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexionx.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexionx:
            curx.close()
            miConexionx.close()


    #serialized1 = json.dumps(liquidacionDetalleU, default=decimal_serializer)
    #serialized1 = json.dumps(liquidacionDetalleU, default=serialize_datetime)


def GuardaAbonosFacturacion(request):

    print ("Entre GuardaAbonosFacturacion" )

    liquidacionId = request.POST['liquidacionId2']
    print("liquidacionId =", liquidacionId)
    #sede = request.POST['sede']
    tipoPago = request.POST['tipoPago']
    print ("tipoPago =", tipoPago)

    formaPago = request.POST['formaPago']
    print ("formaPago =", formaPago)
    valor = request.POST['valorAbono']
    descripcion = request.POST['descripcionAbono']
    print ("liquidacionId  = ", liquidacionId )
    # print("sede = ", sede)


    fechaRegistro = timezone.now()

    registroId = Liquidacion.objects.get(id=liquidacionId)
    print  ("registroId documento =" , registroId.documento_id)
    print  ("registroId tipoDoc =" , registroId.tipoDoc_id)
    print  ("registroId consec =" , registroId.consecAdmision)

    ## falta usuarioRegistro_id

    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            cur3 = miConexion3.cursor()
            comando = 'insert into cartera_Pagos ("fecha", "tipoDoc_id" , documento_id, consec,  "tipoPago_id" , "formaPago_id", valor, descripcion ,"fechaRegistro","estadoReg", saldo, "totalAplicado", "valorEnCurso") values ('  + "'" + str(fechaRegistro) + "'," +  "'" + str(registroId.tipoDoc_id) + "'" + ' , ' + "'" + str(registroId.documento_id) + "'" + ', ' + "'" + str(registroId.consecAdmision) + "'" + '  , ' + "'" + str(tipoPago) + "'" + '  , ' + "'" + str(formaPago) + "'" + ', ' + "'" + str(valor) + "',"   + "'" + str(descripcion) + "','"   + str(fechaRegistro) + "'," + "'" +  str("A") +  "','" + str(valor) + "',0,0);"
            print(comando)
            cur3.execute(comando)
            miConexion3.commit()
            miConexion3.close()


            # Actualizo el total recibido

            miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()
            comando = 'UPDATE  facturacion_liquidacion SET "totalRecibido" = "anticipos" +  "totalAbonos" + "totalCuotaModeradora" +  "totalCopagos"  WHERE id = ' + "'" + str(liquidacionId) + "'"

            print(comando)
            cur3.execute(comando)
            miConexion3.commit()
            miConexion3.close()

            return JsonResponse({'success': True, 'Mensajes': 'Abono Actualizado satisfactoriamente!'})

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

def PostDeleteAbonosFacturacion(request):

    print ("Entre PostDeleteAbonosFacturacion" )

    id = request.POST["id"]
    print ("el id es = ", id)

    ## Se debe verificar antes que no haya valor aplicado en PagosFacturas

    valorSaldo = PagosFacturas.objects.get(pago_id=id, estadoReg='A')
    print ("Saldo = ", valorSaldo.saldo)

    if (valorSaldo.saldo > 0):

        datosMensaje = {'success': True, 'Mensaje': 'No se puede anular Abono con Facturas relacionadas!'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')


    miConexion3 = None
    try:



        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE cartera_Pagos SET "estadoReg" = ' + "'" + str('N') + "' WHERE id =  " + id
        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()


        return JsonResponse({'success': False, 'Mensajes': 'Abono cancelado'})


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


def GuardarLiquidacionDetalle(request):

    print ("Entre GuardarLiquidacionDetalle" )

    liquidacionId = request.POST["liquidacionId"]
    print ("liquidacionId  = ", liquidacionId )
    cups = request.POST["cups"]
    print ("cups  = ", cups )
    suministros = request.POST["suministros"]
    print ("suministros  = ", suministros )
    cantidad = request.POST["cantidad"]
    valorUnitario = request.POST['valorUnitario']
    print("cantidad =",cantidad )
    print("valorUnitario =", valorUnitario)
    valorTotal =  float(cantidad)  * float(valorUnitario)
    observaciones = request.POST['observaciones']
    username_id = request.POST['username_id']
    print ("liquidacionId  = ", liquidacionId )
    print ("observaciones" , observaciones)
    estadoReg= 'A'

    inicialSuministros=0.0
    inicialCups=0.0

    if (cups==''):
           print("Entre cups")
           cups="null"
           inicialSuministros =  valorTotal
           print("inicialSuministros = ", inicialSuministros)
           suministroId=Suministros.objects.get(id=suministros.strip())           
           print("suministroId = ", suministroId.nombre) 
           conceptoId=suministroId.concepto_id
           print("conceptoId = ", conceptoId) 
        

    if (suministros==''):
           print("Entre cups")
           suministros="null"
           inicialCups = valorTotal
           cupsId=Examenes.objects.get(id=cups.strip())           
           conceptoId=cupsId.concepto_id
           print("conceptoId = ", conceptoId)

    fechaRegistro = timezone.now()

    registroId = Liquidacion.objects.get(id=liquidacionId)
    print  ("registroId documento =" , registroId.documento_id)
    print  ("registroId tipoDoc =" , registroId.tipoDoc_id)
    print  ("registroId consec =" , registroId.consecAdmision)

    # Aqui RUTINA busca consecutivo de liquidacion


    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",        password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT COALESCE(max(p.consecutivo),0) + 1 cons FROM facturacion_liquidaciondetalle p WHERE liquidacion_id = ' + liquidacionId
    curt.execute(comando)

    print(comando)

    consecLiquidacion = []

    for cons in curt.fetchall():
         consecLiquidacion.append({'cons': cons})

    miConexiont.close()
    print("consecLiquidacion = ", consecLiquidacion[0])

    consecLiquidacion = consecLiquidacion[0]['cons']
    consecLiquidacion = str(consecLiquidacion)
    print ("consecLiquidacion = ", consecLiquidacion)

    consecLiquidacion = consecLiquidacion.replace("(",' ')
    consecLiquidacion = consecLiquidacion.replace(")", ' ')
    consecLiquidacion = consecLiquidacion.replace(",", ' ')

    # Fin RUTINA busca consecutivo de liquidacion

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia_id,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id", cums_id,  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", observaciones, anulado, concepto_id) VALUES (' + "'" +  str(consecLiquidacion)  + "','" + str(fechaRegistro) + "','" + str(cantidad) + "','"  + str(valorUnitario) + "','" + str(valorTotal)  + "',null" + ",'" +  str(fechaRegistro) + "','" +  str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(cups) + "," + str(suministros) +   ",'"  + str(username_id) + "'," + liquidacionId + ",'MANUAL'," + "'"  + str(observaciones) + "','N','" + str(conceptoId) + "')"
        print(comando)
        cur3.execute(comando)

        # Falta la RUTINA que actualica los cabezotes de la liquidacion
        print("pase_0", liquidacionId)

        try:
            with transaction.atomic():

               totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(examen_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'),Decimal('0.00')))        
               totalSuministros = (totalSuministros['totalS']) + 0
               print ("totalSuministros  =", totalSuministros )

        except Exception as e:
                # Aquí ya se hizo rollback automáticamente
                print("Se hizo rollback por PRONO SE HACE NADA:", e)
                totalSuministros=0.0

        finally:
            print("No haga nada")


        print("pase_1")
 
        print("totalSuministros", totalSuministros)

        try:
            with transaction.atomic():

               totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(cums_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), Decimal('0.00')))
               totalProcedimientos = (totalProcedimientos['totalP']) + 0
               print("totalProcedimientos", totalProcedimientos)

        except Exception as e:
                # Aquí ya se hizo rollback automáticamente
                print("Se hizo rollback por PRONO SE HACE NADA:", e)
                totalProcedimientos=0.0
 
        finally:
            print("No haga nada")
            

 
        print("totalProcedimientos", totalProcedimientos)

        # Si en otra pantalla estan actualizando abonos pues se veri reflejadop

        registroPago = Liquidacion.objects.get(id=liquidacionId)
        totalCopagos = registroPago.totalCopagos
        totalCuotaModeradora = registroPago.totalCuotaModeradora
        totalAnticipos = registroPago.anticipos
        totalAbonos = registroPago.totalAbonos
        #valorEnCurso = registroPago.valorEnCurso
        totalRecibido = registroPago.totalRecibido
        totalAnticipos = registroPago.anticipos
        totalLiquidacion = 0.0


        if (totalSuministros==None):
            totalSuministros=0.0
        if (totalProcedimientos==None):
            totalProcedimientos=0.0

        if (totalRecibido==None):
            totalRecibido=0.0
        if (totalLiquidacion==None):
            totalLiquidacion=0.0
        if (totalAnticipos == None):
            totalAnticipos = 0.0

        if (totalAbonos==None):
            totalAbonos=0.0

        if (totalCuotaModeradora==None):
            totalCuotaModeradora=0.0

        if (totalCopagos==None):
            totalCopagos=0.0

        totalSuministros = float(totalSuministros) + float(inicialSuministros)
        totalProcedimientos = float(totalProcedimientos) + float(inicialCups)
        totalLiquidacion = float(totalSuministros) + float(totalProcedimientos)
        print("totalSuministros FINAL", totalSuministros)
        print("totalProcedimientos FINAL", totalProcedimientos)
        print("totalLiquidacion FINAL= ", totalLiquidacion)
        print("totalRecibido FINAL= ", totalRecibido)


        valorApagar = float(totalLiquidacion) -  float(totalRecibido)


        # Rutina Guarda en cabezote los totales

        print ("Voy a grabar el cabezote")

        comando1 = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + str(totalSuministros) + ',"totalProcedimientos" = ' + str(totalProcedimientos) + ', "totalCopagos" = ' + str(totalCopagos) + ' , "totalCuotaModeradora" = ' + str(totalCuotaModeradora) + ', anticipos = ' +  str(totalAnticipos) + ' ,"totalAbonos" = ' + str(totalAbonos) + ', "totalLiquidacion" = ' + str(totalLiquidacion) + ', "valorApagar" = ' + str(valorApagar) +  ', "totalRecibido" = ' + str(totalRecibido) + ' WHERE id =' + str(liquidacionId)
        cur3.execute(comando1)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Registro guardado stisfactoriamente !'})



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


    ## Fin rutina actualiza cabezotes

def PostDeleteLiquidacionDetalle(request):

    print ("Entre PostDeleteLiquidacionDetalle" )

    id = request.POST["id"]
    print ("el id es = ", id)
    liquidacionId = id
    #post = LiquidacionDetalle.objects.get(id=id)
    #post.delete()

    liqId= LiquidacionDetalle.objects.get(id=liquidacionId)

    if(liqId.anulado=='S'):
        return JsonResponse({'success': False, 'Mensajes': 'Registro ya ANULADO. No se puede anular!'})


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE facturacion_liquidaciondetalle SET "estadoRegistro" = ' + "'" + str('I') + "', anulado = " + "'" + str('S') + "'" + '  WHERE id =  ' + id
        print(comando)
        cur3.execute(comando)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()



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

    miConexion3 = None
    try:

        totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liqId.liquidacion_id).filter(examen_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
        totalSuministros = (totalSuministros['totalS']) + 0
        print("totalSuministros", totalSuministros)
        totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liqId.liquidacion_id).filter(cums_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
        totalProcedimientos = (totalProcedimientos['totalP']) + 0
        print("totalProcedimientos", totalProcedimientos)

        # Si en otra pantalla estan actualizando abonos pues se veri reflejadop
        antesDe = LiquidacionDetalle.objects.get(id=liquidacionId)
        luegoLiquidacionId = antesDe.liquidacion_id
        registroPago = Liquidacion.objects.get(id=luegoLiquidacionId)
        totalCopagos = registroPago.totalCopagos
        totalCuotaModeradora = registroPago.totalCuotaModeradora
        totalAnticipos = registroPago.anticipos
        totalAbonos = registroPago.totalAbonos
        #valorEnCurso = registroPago.valorEnCurso
        totalRecibido = registroPago.totalRecibido
        totalAnticipos = registroPago.anticipos
        totalLiquidacion = totalSuministros + totalProcedimientos

        if totalRecibido == None:
            totalRecibido=0

        print ("totalRecibido = ",totalRecibido )
        print("totalLiquidacion = ",totalLiquidacion )


        valorApagar = totalLiquidacion -  totalRecibido

        # Rutina Guarda en cabezote los totales

        print ("Voy a grabar el cabezote")

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        #comando1 = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + "'" + str(totalSuministros) +  "'" + ',"totalProcedimientos" = ' + "'" +  str(totalProcedimientos) + "'" + ', "totalCopagos" = ' + "'" + str(totalCopagos) + "'" + ' , "totalCuotaModeradora" = ' + "'"  + str(totalCuotaModeradora) + "'" + ', anticipos = ' + "'" +  str(totalAnticipos) + "'" + ' ,"totalAbonos" = ' + "'" + str(totalAbonos) + "'" + ', "totalLiquidacion" = ' + "'" + str(totalLiquidacion) + "'" + ', "valorApagar" = ' + "'" + str(valorApagar)  + "'" +  ', "totalRecibido" = ' + "'" + str(totalRecibido) + "'"  +  ' WHERE id =' + str(liqId.liquidacion_id)
        comando1 = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + str(totalSuministros) + ',"totalProcedimientos" = ' + str(totalProcedimientos) + ', "totalCopagos" = ' + str(totalCopagos) + ' , "totalCuotaModeradora" = ' + str(totalCuotaModeradora) + ', anticipos = ' +  str(totalAnticipos) + ' ,"totalAbonos" = ' + str(totalAbonos) + ', "totalLiquidacion" = ' + str(totalLiquidacion) + ', "valorApagar" = ' + str(valorApagar) +  ', "totalRecibido" = ' + str(totalRecibido) + ' WHERE id =' + str(liqId.liquidacion_id)
        print(comando1)
        cur3.execute(comando1)

        miConexion3.commit()

        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Registro de Liquidacion Anulado!'})


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




def EditarGuardarLiquidacionDetalle(request):

    print ("Entre EditarGuardarLiquidacionDetalle" )

    liquidacionDetalleId = request.POST['liquidacionDetalleId']

    print ("liquidacionDetalleId =", liquidacionDetalleId)

    cups = request.POST["ldcups"]
    suministros = request.POST["ldsuministros"]
    cantidad = request.POST['ldcantidad']
    valorUnitario = request.POST['ldvalorUnitario']
    valorTotal = request.POST['ldvalorTotal']
    observaciones = request.POST['ldobservaciones']
    username_id = request.POST['username_id2']
    print ("liquidacionDetalleId  = ", liquidacionDetalleId )
    tipoRegistro = request.POST['ldtipoRegistro']
    print ("tipoRegistro  = ", tipoRegistro )
    tipoRegistro='MANUAL'

    estadoReg='A'

    if cups == '':
           cups="null"
           suministroId=Suministros.objects.get(id=suministros)           
           conceptoId=suministroId.concepto_id

    if suministros == '':
           suministros="null"
           cupsId=Examenes.objects.get(id=cups)           
           conceptoId=cupsId.concepto_id


    fechaRegistro = timezone.now()

    registroId = LiquidacionDetalle.objects.get(id=liquidacionDetalleId)
    print  ("liquiacion_id =" , registroId.liquidacion_id)

    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()
        #comando = 'insert into facturacion_liquidacionDetalle ("fecha", "tipoDoc_id" , documento_id, consec,  "tipoPago_id" , "formaPago_id", valor, descripcion ,"fechaRegistro","estadoReg", concepto_id) values ('  + "'" + str(fechaRegistro) + "'," +  "'" + str(registroId.tipoDoc_id) + "'" + ' , ' + "'" + str(registroId.documento_id) + "'" + ', ' + "'" + str(registroId.consec) + "'" + '  , ' + "'" + str(tipoPago) + "'" + '  , ' + "'" + str(formaPago) + "'" + ', ' + "'" + str(valor) + "',"   + "'" + str(descripcion) + "','"   + str(fechaRegistro) + "'," + "'" +  str("A") + "','" + str(conceptoId) + "');"
        comando = 'UPDATE facturacion_liquidaciondetalle SET fecha = ' + "'" + str(fechaRegistro) + "', observaciones = " + "'" +  str(observaciones) + "', cantidad = "  + str(cantidad) +  ',"valorUnitario" = ' + str(valorUnitario) + ', "valorTotal" = '  +      str(valorTotal) + ',"fechaCrea" = '  + "'" + str(fechaRegistro) + "'" + ',"estadoRegistro" = ' + "'" + str(estadoReg) + "'" + ',"examen_id" = ' + str(cups) +  ', cums_id = ' + str(suministros) +  ', "usuarioRegistro_id" = ' + "'" + str(username_id) + "', liquidacion_id = " + str(registroId.liquidacion_id) + ', "tipoRegistro" = ' + "'" + str(tipoRegistro) + "' WHERE id = " + str(liquidacionDetalleId)
        print(comando)
        cur3.execute(comando)


        # Rutina Guarda en cabezote los totales


        miConexion3.commit()
        cur3.close()
        miConexion3.close()


    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()
        message_error=str(error)
        print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


    # Falta la RUTINA que actualica los cabezotes de la liquidacion

    totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=registroId.liquidacion_id).filter(examen_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
    totalSuministros = (totalSuministros['totalS']) + 0
    print("totalSuministros", totalSuministros)
    totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=registroId.liquidacion_id).filter(cums_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
    totalProcedimientos = (totalProcedimientos['totalP']) + 0
    print("totalProcedimientos", totalProcedimientos)
    registroPago = Liquidacion.objects.get(id=registroId.liquidacion_id)
    totalCopagos = registroPago.totalCopagos
    totalCuotaModeradora = registroPago.totalCuotaModeradora
    totalAnticipos = registroPago.anticipos
    totalAbonos = registroPago.totalAbonos
    #valorEnCurso = registroPago.valorEnCurso
    totalRecibido = registroPago.totalRecibido
    if totalRecibido == None:
           totalRecibido=0

    print ("totalRecibido", totalRecibido )
    totalAnticipos = registroPago.anticipos
    totalLiquidacion = totalSuministros + totalProcedimientos
    print("totalLiquidacion", totalLiquidacion)
    valorApagar = totalLiquidacion -  totalRecibido
    print("valorApagar", valorApagar)


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        print("Voy a grabar el cabezote")

        comando1 = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + str(
            totalSuministros) + ',"totalProcedimientos" = ' + str(totalProcedimientos) + ', "totalCopagos" = ' + str(
            totalCopagos) + ' , "totalCuotaModeradora" = ' + str(totalCuotaModeradora) + ', anticipos = ' + str(
            totalAnticipos) + ' ,"totalAbonos" = ' + str(totalAbonos) + ', "totalLiquidacion" = ' + str(
            totalLiquidacion) + ', "valorApagar" = ' + str(valorApagar) + ', "totalRecibido" = ' + str(
            totalRecibido) + ' WHERE id =' + str(registroId.liquidacion_id)
        cur3.execute(comando1)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()
        message_error=str(error)
        print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()

    return JsonResponse({'success': True, 'Mensajes': 'Registro Actualizado satisfactoriamente!'})


def load_dataAbonosFacturacion(request, data):
    print("Entre  load_dataAbonosFacturacion")

    context = {}
    d = json.loads(data)
    
    tipoIngreso = d['tipoIngreso']
    liquidacion = d['liquidacionId']
    liquidacionId = Liquidacion.objects.get(id=liquidacion)

    if tipoIngreso == 'INGRESO':

       print("ingresoIdPilas:", liquidacionId)
    else:

       print("triageId Pilos:", liquidacionId)

    sede = d['sede']

    print("sede:", sede)

    convenio = liquidacionId.convenio_id

    if convenio == '':
           convenio="null"

    # print("data = ", request.GET('data'))

    abonos  = []

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if tipoIngreso == 'INGRESO':
      detalle = 'SELECT pag.id id , i."tipoDoc_id" tipoDoc , i.documento_id documentoId ,u.documento documento,u.nombre nombre,i."consecAdmision" consec , tipdoc.nombre nombreDocumento , cast(date(pag.fecha) as text)  fecha, pag."tipoPago_id" tipoPago , pag."formaPago_id" formaPago, pag.valor valor, pag.descripcion descripcion ,tip.nombre tipoPagoNombre,forma.nombre formaPagoNombre, pag."totalAplicado" totalAplicado, pag.saldo saldo , pag."estadoReg" estadoReg, pag."valorEnCurso"  valorEnCurso FROM facturacion_liquidacion i, cartera_pagos pag ,usuarios_usuarios u ,usuarios_tiposdocumento tipdoc, cartera_tiposPagos tip, cartera_formasPagos forma WHERE i.id = ' + "'" + str(liquidacionId.id) + "'" + ' and i.documento_id = u.id and i."tipoDoc_id" = pag."tipoDoc_id" and i.documento_id  = pag.documento_id and  i."consecAdmision" = pag.consec AND tipdoc.id = i."tipoDoc_id" and pag."tipoPago_id" = tip.id and pag."formaPago_id" = forma.id  and pag.convenio_id = i.convenio_id and i.convenio_id = ' + str(convenio)  + ' ORDER BY pag.fecha desc'
    else:
      detalle = 'SELECT pag.id id , t."tipoDoc_id" tipoDoc , t.documento_id documentoId ,u.documento documento,u.nombre nombre,t."consecAdmision" consec , tipdoc.nombre nombreDocumento , cast(date(pag.fecha) as text)  fecha, pag."tipoPago_id" tipoPago , pag."formaPago_id" formaPago, pag.valor valor, pag.descripcion descripcion ,tip.nombre tipoPagoNombre,forma.nombre formaPagoNombre, pag."totalAplicado" totalAplicado, pag.saldo saldo , pag."estadoReg" estadoReg , pag."valorEnCurso"  valorEnCurso FROM facturacion_liquidacion t, cartera_pagos pag ,usuarios_usuarios u ,usuarios_tiposdocumento tipdoc, cartera_tiposPagos tip, cartera_formasPagos forma WHERE t.id = ' + "'" + str(liquidacionId.id) + "'" + ' and t.documento_id = u.id and t."tipoDoc_id" = pag."tipoDoc_id" and t.documento_id  = pag.documento_id and  t."consecAdmision" = pag.consec AND tipdoc.id = t."tipoDoc_id" and pag."tipoPago_id" = tip.id and pag."formaPago_id" = forma.id and pag.convenio_id = t.convenio_id and t.convenio_id = '  + str(convenio)  + ' ORDER BY pag.fecha desc'

    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc, documentoId, documento, nombre, consec, nombreDocumento , fecha, tipoPago, formaPago, valor, descripcion, tipoPagoNombre,formaPagoNombre,totalAplicado, saldo, estadoReg , valorEnCurso in curx.fetchall():
        abonos.append(
            {"model": "cartera_pagos.cartera_pagos", "pk": id, "fields":
                {'id': id, 'tipoDoc': tipoDoc, 'documentoId': documentoId, 'nombre':nombre,'consec':consec,  'nombreDocumento': nombreDocumento,
                 'fecha': fecha, 'tipoPago': tipoPago, 'formaPago': formaPago, 'valor':valor, 'descripcion':descripcion,'tipoPagoNombre': tipoPagoNombre, 'formaPagoNombre': formaPagoNombre, 'totalAplicado':totalAplicado, 'saldo':saldo , 'estadoReg': estadoReg, 'valorEnCurso': valorEnCurso}})

    miConexionx.close()
    print(abonos)
    context['Abonos '] = abonos

    serialized2 = json.dumps(abonos,  default=decimal_serializer)

    print("Envio = ", serialized2)

    return HttpResponse(serialized2, content_type='application/json')


def FacturarCuenta(request):

    print ("Entre FacturarCuenta" )

    liquidacionId = request.POST["liquidacionId"]
    print ("liquidacionId = ", liquidacionId)
    username_id = request.POST["username_id"]
    sede = request.POST["sede"]
    print("sede = ", sede)
    tipoFactura = request.POST["tipoFactura"]
    serviciosAdministrativos = request.POST["serviciosAdministrativos"]

    #usuarioId = Liquidacion.objects.get(id=liquidacionId)

    #print ("Usuario", usuarioId.documento_id)
    #print ("TipoDoc", usuarioId.tipoDoc_id)
    #print ("Consec", usuarioId.consecAdmision)

    totalCirugias=0

    fechaRegistro = timezone.now()
	
    liquidacionDatos = Liquidacion.objects.get(id=liquidacionId)
    print("convenio de la liquidaciony = " , liquidacionDatos.convenio_id);

    facturaConvenio = liquidacionDatos.convenio_id

    print("tipoFactura =" ,tipoFactura )

    if (tipoFactura == 'REFACTURA'):

        facturaAnula = Refacturacion.objects.get(tipoDoc_id=liquidacionDatos.tipoDoc_id, documento_id=liquidacionDatos.documento_id,consecAdmision=liquidacionDatos.consecAdmision, facturaNueva=0)
        print("facturaAnula",facturaAnula )
        facturaAnulada = facturaAnula.facturaAnulada

    numConveniosActivos=0

    try:
	
	    numConveniosActivos =  Liquidacion.objects.filter(tipoDoc_id=liquidacionDatos.tipoDoc_id, documento_id=liquidacionDatos.documento_id, consecAdmision=liquidacionDatos.consecAdmision ).count()

    except (ValueError, TypeError) as e:

        message_error= str(e)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
	    print ("ok")

    if (liquidacionDatos.convenio_id =='' and tipoFactura == 'FACTURA'):
            print("ENTRE convenio de la liquidacion = " + liquidacionDatos.convenio_id)
            return JsonResponse({'success': False, 'Mensajes': 'Favor ingresar Convenio a Facturar !', 'Factura' : 0 })

     # OPS PAILAS SI LO QUE VA A FACTURAR ES UN TRIAGE

    flag=''

    if	(liquidacionDatos.consecAdmision == 0 ): #Es triage

	    triageId = Triage.objects.get(tipoDoc_id=liquidacionDatos.tipoDoc_id , documento_id=liquidacionDatos.documento_id ,consec=liquidacionDatos.consecAdmision)
	    print ("triageId = ", triageId.id)
	    flag='TRIAGE'
	    return JsonResponse({'success': False, 'Mensajes': 'No es posible facturar cuenta Triage. Favor hospitalizar o a cama de Urgencias!'})

    else:
        print("Entre ingreso Admision")
        ingresoId = Ingresos.objects.get(tipoDoc_id=liquidacionDatos.tipoDoc_id , documento_id=liquidacionDatos.documento_id ,consec=liquidacionDatos.consecAdmision)
        print ("ingresoId = ", ingresoId.id)
        flag='INGRESO'
        servicioSedeAmb = ServiciosSedes.objects.get(sedesClinica_id=sede, id=ingresoId.serviciosActual_id)
        servicioAmb = Servicios.objects.get(nombre='AMBULATORIO')
        if (servicioSedeAmb.servicios_id==servicioAmb.id):
            flag='AMBULATORIO'


    print ("IngresoId", ingresoId.id)
    print("flag" ,flag)

    if (flag=='INGRESO'):
        print("flag2", flag)
        if (ingresoId.salidaClinica=='N' and servicioSedeAmb.servicios_id != servicioAmb.id  ):
            print("flag3", flag)
            return JsonResponse({'success': False, 'Mensajes': 'Paciente NO tiene Salida Clinica. Consultar medico tratante !', 'Factura' : 0 })

    # AQUI VALDAR SI HAY CIRUGIAS QUE NO ESTEN REALIZADAS  ## OPS ESTO SI HAY QUE REVIZARLO
 
    print ( "Evaluo cirugia"   )
    estadoCirugiaRealizada = EstadosCirugias.objects.get(nombre='REALIZADA')
    estadoCirugiaFacturada = EstadosCirugias.objects.get(nombre='FACTURADA')
    estadoCirugiaDescripcionQx = EstadosCirugias.objects.get(nombre='CON DESCRIPCION QX')
    estadoProgramacionRealizada = EstadosProgramacion.objects.get(nombre='Realizada')
    estadoProgramacionProgramada = EstadosProgramacion.objects.get(nombre='Programada')
    estadoProgramacionSolicitud = EstadosProgramacion.objects.get(nombre='Solicitud')

    try:
        with transaction.atomic():

            totalCirugias = Cirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision, estadoCirugia_id= estadoCirugiaRealizada.id).count()
            print ( "total cirugias", totalCirugias   )

            if (totalCirugias >=1):
                Cirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision , estadoCirugia_id= estadoCirugiaRealizada.id).update(estadoCirugia_id=estadoCirugiaFacturada.id)
                Cirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision , estadoCirugia_id= estadoCirugiaDescripcionQx.id).update(estadoCirugia_id=estadoCirugiaFacturada.id)
                Programacioncirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision , estadoProgramacion_id= estadoProgramacionSolicitud.id).update(estadoProgramacion_id=estadoProgramacionRealizada.id)
                Programacioncirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision , estadoProgramacion_id= estadoProgramacionProgramada.id).update(estadoProgramacion_id=estadoProgramacionRealizada.id)

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por PRONO SE HACE NADA:", e)

    finally:
        print("No haga nada")

    ## RUTINA ACTUALIZA DX, SERV ,
    print ( "pase cirugia"   )
    miConexion3 = None
    try:
        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",   password="123456")
        cur3 = miConexion3.cursor()

        if (tipoFactura == 'FACTURA'):

            if (flag=='INGRESO' or flag=='AMBULATORIO'):

                if (numConveniosActivos <= 1):

                    comando = 'UPDATE admisiones_ingresos SET  "dxSalida_id"= "dxActual_id", "medicoSalida_id" = "medicoActual_id",  "serviciosSalida_id" = "serviciosActual_id" , "dependenciasSalida_id" = "dependenciasActual_id", "especialidadesMedicosSalida_id" = "especialidadesMedicosActual_id" ,"salidaDefinitiva" = ' + "'" + str('S') + "'" + ',"fechaSalida"= ' + "'" + str(fechaRegistro) + "'"  + ' WHERE id =  ' + "'" +  str(ingresoId.id) + "'"
                    print(comando)
                    cur3.execute(comando)

            if (flag=='TRIAGE'):

	               print ("nO HAGA NADA")       

            if (numConveniosActivos<=1):

                    ## AQUI RUTINA HISTORICO CAMA-DEPENDENCIA
                    if (flag != 'TRIAGE'):

                        comando1 = 'INSERT INTO sitios_historialdependencias (consec,"fechaLiberacion","fechaRegistro","estadoReg", dependencias_id,documento_id,"tipoDoc_id","usuarioRegistro_id",disponibilidad)  SELECT consec,' + "'" + str(fechaRegistro) + "'," + "'" + str(fechaRegistro) + "'," + "'" + str('A') + "'" + ", id" + ",'" + str(ingresoId.documento_id) + "'," + "'" + str(ingresoId.tipoDoc_id) + "'," + "'" + str(username_id) + "'," + "'" + str('L') + "'" +  ' from sitios_dependencias where "tipoDoc_id" = ' + "'" + str(ingresoId.tipoDoc_id) + "' AND documento_id = "  + "'" + str(ingresoId.documento_id) + "' AND consec = " + "'" + str(ingresoId.consec) + "'"
                    else:
                        comando1 = 'INSERT INTO sitios_historialdependencias (consec,"fechaLiberacion","fechaRegistro","estadoReg", dependencias_id,documento_id,"tipoDoc_id","usuarioRegistro_id",disponibilidad)  SELECT consec,' + "'" + str(fechaRegistro) + "'," + "'" + str(fechaRegistro) + "'," + "'" + str('A') + "'" + ", id" + ",'" + str(triageId.documento_id) + "'," + "'" + str(triageId.tipoDoc_id) + "'," + "'" + str(username_id) + "'," + "'" + str('L') + "'" +  ' from sitios_dependencias where "tipoDoc_id" = ' + "'" + str(triageId.tipoDoc_id) + "' AND documento_id = "  + "'" + str(triageId.documento_id) + "' AND consec = " + "'" + str(triageId.consec) + "'"

                    print(comando1)
                    cur3.execute(comando1)

                       ## FIN HISTORICO CAMAA-DEPENDENCIA

                       ## AQUI RUTINA DESOCUPAR CAMA-DEPENDENCIA

                    if (flag != 'TRIAGE'):

                        comando2 = 'UPDATE sitios_dependencias SET disponibilidad = ' + "'" + str('L') + "'," + ' "tipoDoc_id" = null , documento_id = null,  consec= null, "fechaLiberacion" = null , "fechaOcupacion" = null  WHERE "tipoDoc_id" = ' + "'" + str(ingresoId.tipoDoc_id) + "'" + ' AND documento_id = ' + "'" + str(ingresoId.documento_id) + "'" + ' AND consec = ' + str(ingresoId.consec)
                    else:
                        comando2 = 'UPDATE sitios_dependencias SET disponibilidad = ' + "'" + str('L') + "'," + ' "tipoDoc_id" = null , documento_id = null,  consec= null, "fechaLiberacion" = null , "fechaOcupacion" = null  WHERE "tipoDoc_id" = ' + "'" + str(triageId.tipoDoc_id) + "'" + ' AND documento_id = ' + "'" + str(triageId.documento_id) + "'" + ' AND consec = ' + str(triageId.consec)

                    print(comando2)
                    cur3.execute(comando2)

        comando3 = 'INSERT INTO facturacion_facturacion ("sedesClinica_id", documento_id, "consecAdmision", "fechaFactura", "totalCopagos", "totalCuotaModeradora","totalProcedimientos",   "totalSuministros", "totalFactura", "valorApagar", anulado, anticipos, "fechaRegistro", "estadoReg", "fechaAnulacion", observaciones, "fechaCorte",convenio_id, "tipoDoc_id","usuarioAnula_id","usuarioRegistro_id",  "totalAbonos", "totalRecibido", "serviciosAdministrativos_id", "saldoFactura") SELECT ' "'" + str(sede) + "'" + ', documento_id, "consecAdmision", ' + "'" + str(fechaRegistro) + "'" + ' , "totalCopagos", "totalCuotaModeradora", "totalProcedimientos",  "totalSuministros", "totalLiquidacion", "valorApagar", ' + "'" + str('N') + "'" + ' , anticipos, ' + "'" + str(fechaRegistro) + "'" + ' ,  ' + "'" + str('A') + "'" + ' , "fechaAnulacion", observaciones, "fechaCorte",convenio_id, "tipoDoc_id","usuarioAnula_id", ' + "'" + str(username_id) + "'" + '  , "totalAbonos", "totalRecibido" , ' + "'" + str(serviciosAdministrativos) + "'" + ', "valorApagar" FROM facturacion_liquidacion WHERE id =  ' + liquidacionId + ' RETURNING id  '

        # AQUI CONSEGUIR EL ID DE LA FACTURA RECIEN CREADA

        print(comando3)
        cur3.execute(comando3)
        facturacionId = cur3.fetchone()[0]

        ## Datos para el prefijo de la factura
        sedePrefijoDian = SedesClinica.objects.get(id=sede)
        prefijoDian = sedePrefijoDian.prefijoDian
        print("prefijoDian = ", prefijoDian.prefijoDian)
        consecutivosDian = ConsecutivosDian.objects.get(prefijoDian_id = prefijoDian , estadoReg='A')
        print("consecutivosDian = ", consecutivosDian.actual)
        consecutivoVoy = consecutivosDian.actual + 1
        print ("consecutivoVoy = ", consecutivoVoy)
        numeroFacturaPrefijo =  prefijoDian.prefijoDian + str(consecutivoVoy)
        print ("numeroFacturaPrefijo = " , numeroFacturaPrefijo)
 
        ## Fin datos prefijo factura

        
        print("facturacionId = " , facturacionId)
        comando32 = 'update facturacion_facturacion set "valorAPagarLetras" = obtienevlrletras(cast("totalFactura" as integer)) ,  factura = ' + "'" +  str(numeroFacturaPrefijo) + "'" + ', prefijo= ' + "'"  + str(prefijoDian.prefijoDian) + "'" + '  WHERE id = ' + str(facturacionId)
        print ("comando32 = ", comando32)
        cur3.execute(comando32)

        print ("facturacionId = ", facturacionId)

        comando32 = 'update facturacion_consecutivosdian set actual = ' 	 + str(consecutivoVoy) + ' WHERE id = ' + str(consecutivosDian.id)
        print ("comando32 = ", comando32)
        cur3.execute(comando32)

        # AHORA EL DETALLE

        comando5 = 'INSERT INTO facturacion_facturaciondetalle ("consecutivoFactura", fecha, cantidad, "valorUnitario", "valorTotal",  cirugia_id , "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro", "examen_id", cums_id, "usuarioModifica_id", "usuarioRegistro_id", facturacion_id, "tipoHonorario_id", "tipoRegistro", anulado, "historiaMedicamento_id","codigoHomologado", mipres, "autorizacionDetalle_id", concepto_id) SELECT  consecutivo, fecha, cantidad, "valorUnitario", "valorTotal",  cirugia_id , "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro", "examen_id", cums_id, "usuarioModifica_id", "usuarioRegistro_id", ' + str(facturacionId) + ', "tipoHonorario_id", "tipoRegistro", anulado , "historiaMedicamento_id", "codigoHomologado", mipres ,"autorizacionDetalle_id", concepto_id  FROM facturacion_liquidaciondetalle WHERE liquidacion_id =  ' + liquidacionId + ' AND anulado != ' + "'" + str('S') + "'"
        print("comando5 = ", comando5)
        cur3.execute(comando5)

        ## AQUI BORRAMOS EL DETALLE DE LA LIQUIDACION

        comando8 = 'DELETE FROM facturacion_liquidaciondetalle WHERE liquidacion_id =  ' + liquidacionId
        print(comando8)
        cur3.execute(comando8)

        ## AQUI BORRAMOS EL CABEZOTE DE LA LIQUIDACION

        comando9 = 'DElETE FROM facturacion_liquidacion WHERE id =  ' + liquidacionId

        print(comando9)
        cur3.execute(comando9)

        # ACTALIZAMPOS LA FACTURA EN LA TABLA CONVENIONPACIENTEINGRESOS

        comando10 = 'UPDATE facturacion_conveniospacienteingresos  SET factura_id = ' + "'" + str(facturacionId) + "'" + ' WHERE documento_id = ' + "'" + str(liquidacionDatos.documento_id) + "'" + ' AND "tipoDoc_id" = ' + "'" + str(liquidacionDatos.tipoDoc_id) + "'" + ' AND "consecAdmision" = ' + "'" + str(liquidacionDatos.consecAdmision) + "'  AND convenio_id = " + "'" + str(liquidacionDatos.convenio_id) + "'"

        print(comando10)
        cur3.execute(comando10)

        ## COLOCAR EN LA TABLA INGRESOS , LA FECHA DE EGRESO Y EL NUMERO DE LA FACTURA GENERADO SI SE FACTURA


        comando4 = 'UPDATE admisiones_ingresos SET factura = ' + "'" +  str(facturacionId) + "'"  + ' WHERE id =' + str(ingresoId.id)
        cur3.execute(comando4)


        if ((tipoFactura == 'REFACTURA' or tipoFactura == 'FACTURA')  and flag != 'TRIAGE'  and numConveniosActivos <= 1):

            comando4 = 'UPDATE admisiones_ingresos SET "salidaDefinitiva" = ' + "'" + str('S') + "'"  + ' WHERE id =' + str(ingresoId.id)
            cur3.execute(comando4)

        #AQUI ACTUALIZAMOS LOS PAGOS DEL PACIENTE

        comando6 = 'INSERT INTO cartera_pagosFacturas ("valorAplicado", "fechaRegistro","estadoReg", "facturaAplicada_id",pago_id, "serviciosAdministrativos_id",anulado, "sedesClinica_id") SELECT "valorEnCurso", ' + "'" + str(fechaRegistro) + "','A'," + str(facturacionId) + ', id ,' + "'" + str(serviciosAdministrativos) + "','N','" + str(sede) + "'" + ' FROM cartera_pagos WHERE documento_id = ' + "'" + str(liquidacionDatos.documento_id) + "'" + ' AND "tipoDoc_id" = ' + "'" + str(liquidacionDatos.tipoDoc_id) + "'" + ' AND consec = ' + "'" + str(liquidacionDatos.consecAdmision) + "' AND anulado != 'S' AND " + '"valorEnCurso" != 0'

        print(comando6)
        cur3.execute(comando6)

        comando7 = 'UPDATE cartera_pagos SET "totalAplicado" =  "totalAplicado" + "valorEnCurso", "valorEnCurso" = 0 ' + ' WHERE documento_id = ' + "'" + str(liquidacionDatos.documento_id) + "'" + ' AND "tipoDoc_id" = ' + "'" + str(liquidacionDatos.tipoDoc_id) + "'" + ' AND consec = ' + "'" + str(liquidacionDatos.consecAdmision) + "'"

        print(comando7)
        cur3.execute(comando7)

        comando7 = 'UPDATE cartera_pagos SET saldo  = valor - "totalAplicado" ' + ' WHERE documento_id = ' + "'" + str(liquidacionDatos.documento_id) + "'" + ' AND "tipoDoc_id" = ' + "'" + str(liquidacionDatos.tipoDoc_id) + "'" + ' AND consec = ' + "'" + str(liquidacionDatos.consecAdmision) + "'"

        print(comando7)
        cur3.execute(comando7)

        # AQUI ACTUALIZAMOS EL ESTADO DE LA CIRUGIA

        print("tipofactura =", tipoFactura)
        print("flag =", flag)

        if (totalCirugias >= 1):

            estadoCirugiaFacturada = EstadosCirugias.objects.get(nombre='FACTURADA')

            comando10= 'UPDATE cirugia_cirugias SET "estadoCirugia_id" = ' + "'" + str(estadoCirugiaFacturada.id) + "' WHERE documento_id = " + "'" + str(liquidacionDatos.documento_id) + "'" + ' AND "tipoDoc_id" = ' + "'" + str(liquidacionDatos.tipoDoc_id) + "', " + '"consecAdmision" = ' + "'" +  str(liquidacionDatos.consecAdmision) + "' AND " + '"estadoCirugia_id" = ' + "'" + str(estadoCirugiaRealizada.id) + "'"
            print(comando10)
            cur3.execute(comando10)


        if (tipoFactura == 'REFACTURA'):


            if (flag == 'INGRESO' or flag== 'AMBULATORIO'):
                print("facturaInicial = ", ingresoId.factura)
                comando4 = 'UPDATE facturacion_refacturacion SET "facturaNueva" = ' + "'" +  str(facturacionId) + "'" +  ' WHERE documento_id = ' + "'" + str(ingresoId.documento_id) + "' and " + '"tipoDoc_id" = ' + "'" + str(ingresoId.tipoDoc_id) + "' and " + '"consecAdmision" = ' + "'" + str(ingresoId.consec) + "' AND "  + ' "facturaAnulada"  = ' + "'"  + str(facturaAnulada) + "'"
                cur3.execute(comando4)
                print(comando4)

            else:
                comando4 = 'UPDATE facturacion_refacturacion SET "facturaNueva" = ' + "'" + str(facturacionId) + "'" + ' WHERE documento_id = ' + "'" + str(triageId.documento_id) + "' and " + '"tipoDoc_id" = ' + "'" + str(triageId.tipoDoc_id) + "' and " + '"consecAdmision" = ' + "'" + str(triageId.consec) + "' AND "  + ' "facturaAnulada"  = ' + "'"  + str(facturaAnulada) + "'"
                cur3.execute(comando4)


        #miConexion3.commit()


	# Aqui creo el registro en cartera

        comando100 ='select fac."totalFactura" totalFactura, conv.empresa_id empresa_id FROM facturacion_facturacion fac INNER JOIN contratacion_convenios conv on (conv.id=fac.convenio_id) where fac.id=' + str(facturacionId)
     
        cur3.execute(comando100)

        for totalFactura , empresa_id in cur3.fetchall():
 
             print("aui voy")
             #facturaFisica = Facturacion.objects.get(id=facturacionId)
             #convenioFisico = Convenios.objects.get(id=facturaFisica.convenio_id)
             comando11 = 'INSERT INTO cartera_cartera (pagos,saldo,valor,  "fechaRegistro","estadoReg", factura_id, "sedesClinica_id", empresa_id) VALUES ( 0 , ' +  str(totalFactura) + "," + str(totalFactura) + ",'" + str(fechaRegistro) + "','A'," + str(facturacionId) + ",'" + str(sede) + "'," + str(empresa_id) + ")"
             print(comando11)
             cur3.execute(comando11)


        ## A partir de aqui seria la rutina de crear la factura de copago si la factura tiene copago. Solo es el INSERT a las dos tablas ??
     

        ## FIn rutina registro nueva factura copago

        ## Crear Directorio Factura_xxx CON PREFIJO para almacenar los objetos e la facturacion electronica de la factura

        caracter_especial = "\\"

        nombre_carpeta = "C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\Facturas\\"+  str(numeroFacturaPrefijo)
        print("nombre_carpeta = ", nombre_carpeta)
        #nombre_carpeta_linux = "mi_nueva_carpeta_linux"

        try:
             # Crea la carpeta. exist_ok=True evita errores si ya existe.
             os.makedirs(nombre_carpeta, exist_ok=True)
             print(f"Carpeta '{nombre_carpeta}' lista para usar en windows.")
        except OSError as e:

             print(f"Error al crear la carpeta: {e}")

        ## Aqui se genera el JSON De la factura 


        nombre_archivoJson = nombre_carpeta + caracter_especial + str(numeroFacturaPrefijo) + '.txt'
        print("nombre_archivoJson =", nombre_archivoJson)

        funcionJson = []

        detalle = 'SELECT FacturaJsonDian_2(' + str(facturacionId) + ") dato"


        print ("facturacionId= ", facturacionId)
        print ('detalle a FacturaJsonDian_2 = ', detalle)

        cur3.execute(detalle)

        for dato in cur3.fetchall():
            funcionJson.append({'dato': dato})

        print("funcionJson[0]", funcionJson[0])

        try:
           with open(nombre_archivoJson, 'w' , encoding='utf-8') as archivo:
               # Escribir el texto en el archivo
               file = open(nombre_archivoJson, "w")
               print("funcionJson[0]['dato']" , funcionJson[0]['dato'])
               file.writelines(funcionJson[0]['dato'])
               file.close()


        except IOError as e:
           print(f"Error al guardar el archivo: {e}")
           datosMensaje = {'success': False, 'Mensajes': 'Cerrar Archivo cargado en browser'}
           json_data = json.dumps(datosMensaje, default=str)

           return HttpResponse(json_data, content_type='application/json')

        except UnicodeEncodeError as e:
           print(f"Error encoding character: {e}")

        except Exception as e:
           print(f"Error al abrir el archivo: {e}")


        nombre_archivoPdf = nombre_carpeta + caracter_especial + str(numeroFacturaPrefijo) + '.pdf'

        ## Aqui podria generar el cufe y guardar el valor del CUFE en la tabla 

        nombre_archivoPdf = nombre_carpeta + caracter_especial + str(numeroFacturaPrefijo) + '.pdf'

        # --- 2. GENERAR CUFE (Algoritmo SHA-384 simplificado) ---
        # En producción se concatenan: Num + Fecha + Hora + Valor + NITs + ... + CLTecnica
        print("voy a generar el CUFE")
        dati= funcionJson[0]['dato']
        cabezote = str(dati)
        cabezote = cabezote.replace("('", ' ')
        cabezote = cabezote.replace("',)", ' ')
        print("OJOOOOO cabezote", cabezote)

        data = json.loads(cabezote)


        print("Numfac = ", data[0]["NumFac"])
        print("Fecfac = ", data[0]["FecFac"])

        raw_cufe = f'{data[0]["NumFac"]}{data[0]["FecFac"]}{data[0]["HoraFac"]}{data[0]["NitFac"]}{data[0]["DocAdq"]}{data[0]["ValFac"]}{data[0]["ValIva"]}{data[0]["ValOtroIm"]}{data[0]["ValTotFac"]}'
        print ("raw_cufe = ", raw_cufe ) 
        cufe = hashlib.sha384(raw_cufe.encode()).hexdigest()
        print(f"CUFE Generado: {cufe}")
  

        ## Aqui podria generar el QR y guardar la ruta del Qr  (.png)  en la carpeta prefijo

        # --- 3. GENERAR CÓDIGO QR ---
        url_dian = f"https://catalogo-vpfe.dian.gov.co/document/searchqr?documentkey={cufe}"
        qr = qrcode.make(url_dian)
        print ("qr = ", qr)
        nombre_archivoQr = nombre_carpeta + caracter_especial + str(numeroFacturaPrefijo) + '.png'
        print("nombre_archivoQr =", nombre_archivoQr)

        #qr.save("qr_factura.png")
        qr.save(nombre_archivoQr)
        

        ## Aqui podria generar el XML y guardar el  (.xml) en la ruta prefijo

        # --- 4. GENERAR XML (Estructura UBL 2.1 básica) ---

        # Nota: La firma electrónica (signature) es obligatoria en producción.

        nombre_archivoXml = nombre_carpeta + caracter_especial + str(numeroFacturaPrefijo) + '.xml'
        print("nombre_archivoXml =", nombre_archivoXml)


        # 1. Definición de Namespaces (Obligatorio UBL 2.1)
        nsmap = {
             None: 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            'ds': 'http://w3.org',
            'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
            'sts': 'dian:gov:co:facturaelectronica:Structures-2-1',
            'xsi': 'http://w3.org'
        }

        # Raíz del XML
        root = etree.Element('Invoice', nsmap=nsmap)

        print("ya namespaces")

        print ("VERIFICACION VAMOS A COMENZAR")
        print(etree.tostring(root, pretty_print=True, encoding='unicode'))
    
        # --- UBL Extensions (Firma) ---
        print("ya firma_0")
        #exts = etree.SubElement(root, 'ext:UBLExtensions')
        print("ya firma_1")
        #ext = etree.SubElement(exts, 'ext:UBLExtension')
        print("ya firma_2")
        #etree.SubElement(ext, 'ext:ExtensionContent') # Aquí va la firma XAdES

        # --- Cabecera General ---
        fecha_actual = timezone.now()
        print("fecha_actual", fecha_actual)
        fecha_hoy = fecha_actual.strftime("%Y-%m-%d")
        print("fecha_hoy:", fecha_hoy)
        print("Factura Dian No " ,  data[0]["NumFac"])

        # 2. Crear la raíz con el nsmap
        roota = etree.Element('{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice', nsmap=nsmap)

        # 3. Agregar cbc:UBLVersionID usando el namespace explícito
        # Esta es la forma correcta si ya definiste el nsmap en la raíz:
        ubl_version = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}UBLVersionID')
        print("voya poner la version")
        ubl_version.text = 'UBL 2.1' # La DIAN espera '2.1', no 'UBL 2.1'

        print ("VERIFICACION DESPUES VERSION")
        print(etree.tostring(roota, pretty_print=True, encoding='unicode'))

        # Definir la URI del namespace cbc
        cbc_ns = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"

        # Crear el subelemento usando el formato {URI}etiqueta
        customization_id = etree.SubElement(
            roota, 
            f"{{{cbc_ns}}}CustomizationID"
        )
        customization_id.text = 'SS_CUFE'
        # Crear el subelemento usando el formato {URI}etiqueta


        print ("VERIFICACION DESPUES de CustomizationID")
        print(etree.tostring(roota, pretty_print=True, encoding='unicode'))

        # 3. Agregar ProfileExecutionID correctamente
        profile_id2 = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ProfileID')
        profile_id2.text = 'DIAN 2.1: Factura Electrónica de Venta' # '1' para habilitación, '2' para producción
       
        # 3. Agregar ProfileExecutionID correctamente
        profile_id = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ProfileExecutionID')
        profile_id.text = '1' # '1' para habilitación, '2' para producción

        # Añadir SubElement con el NS completo (Forma Correcta)
        cbc_id = etree.SubElement(roota, f"{{{nsmap['cbc']}}}ID")
        cbc_id.text = data[0]["NumFac"] # Ejemplo de prefijo de resolución
        print ("Aqui_toy_001")
        # Ejemplo de estructura anidada
        #cac_party = etree.SubElement(roota, f"{{{nsmap['cac']}}}AccountingSupplierParty")
        #cbc_name = etree.SubElement(cac_party, f"{{{nsmap['cbc']}}}CustomerAssignedAccountID")
        #cbc_name.text = data[0]["NumFac"]

        # 3. Crear el elemento UUID usando la sintaxis {URI}etiqueta
        # Note: 'cbc:' no se usa aquí, se usa la URI definida arriba.
        uuid_element = etree.SubElement(
                      roota, 
                      "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}UUID"
        )


        # 4. Asignar atributos y valor
        uuid_element.set("schemeID", "1")
        uuid_element.set("schemeName", "CUFE-SHA384")
        ## Aqui creo va el cufe en el XML AQUI CREO ES EL ERROR verificar mañana
        uuid_element.text = str(cufe)

        #etree.SubElement(root, 'cbc:IssueDate').text = fecha_hoy
 
        issue_date = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate')
        issue_date.text = data[0]["FecFac"]
        print ("Aqui_toy_2")

        #etree.SubElement(roota, 'cbc:IssueTime').text = datetime.now()
        issue_time = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueTime')
        print ("Aqui_toy_3",  data[0]["HoraFac"])
        issue_time.text = data[0]["HoraFac"]

        issue_date2 = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DueDate')
        issue_date2.text = '12:00'  ## Fecha de vencimiento de la factura o sea digamos 3 meses o por el contrato tambien

        print ("VERIFICACION DESPUES de issue_time")
        print(etree.tostring(roota, pretty_print=True, encoding='unicode'))

        #etree.SubElement(root, 'cbc:InvoiceTypeCode').text = '01' # 01: Factura de venta

        # 3. Crear el subelemento correctamente
        sub = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoiceTypeCode')
        sub.text = '01'

        # 3. Crear el subelemento correctamente
        # <cbc:LineCountNumeric>
        line_count = etree.SubElement(
               roota, 
               "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}LineCountNumeric"
        )
        line_count.text = "NroItems"  ## Nro total de items de la factura


        # 2. Crear InvoicePeriod con el NS de AggregateComponents (cac)
        invoice_period = etree.SubElement(roota, '{%s}InvoicePeriod' % nsmap['cac'])

        # 3. Agregar elementos hijos (ej. fechas) con el NS de BasicComponents (cbc)
        start_date = etree.SubElement(invoice_period, '{%s}StartDate' % nsmap['cbc'])
        start_date.text = fecha_hoy # Fecha inicio periodo de facturacion

        start_timeDate = etree.SubElement(invoice_period, '{%s}StartTime' % nsmap['cbc'])
        start_timeDate.text = '12:00' # Fecha hora inicio periodo de facturacion

        end_date = etree.SubElement(invoice_period, '{%s}EndDate' % nsmap['cbc'])
        end_date.text = fecha_hoy # ebe contener la fecha de fin de vigencia de la resolución de autorización de numeración
        end_timeDate = etree.SubElement(invoice_period, '{%s}EndTime' % nsmap['cbc'])
        end_timeDate.text = '12:00' # Fecha hora fin periodo de facturacion
        # Para verificar el resultado

        print ("VERIFICACION Termina fechas issue_date_time : ")

        print(etree.tostring(roota, pretty_print=False, encoding='unicode'))

        print("Comienza el EMISOR")

        # --- Emisor (AccountingSupplierParty) ---
        # 3. Crear cac:AccountingSupplierParty usando la referencia directa del namespace
        supplier_party = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty')

        # 4. Añadir hijos (ejemplo Party)
        #party = etree.SubElement(supplier_party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party')

        cac_ns = nsmap['cac']
        cbc_ns = nsmap['cbc']

        # Ejemplo: PartyName
        party = etree.SubElement(supplier_party, f'{{{cac_ns}}}Party')
        party_name = etree.SubElement(party, f'{{{cac_ns}}}PartyName')
        #name = etree.SubElement(party_name, f'{{{cbc_ns}}}Name')
        #name.text = data[1]['emisor']['nombreRazonSocial']
        party_name.text = data[1]['emisor']['nombreRazonSocial']
        print ("Emisor data[1]['emisor']['nombreRazonSocial'] =", data[1]['emisor']['nombreRazonSocial'])


        # 3. Crear el subelemento usando el URI completo en lugar de "cac:"
        # La forma correcta es: {URI}NombreTag
        physical_location = etree.SubElement(
           party, 
           '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PhysicalLocation'
        )


        # 2. Forma correcta de crear subelementos con NS
        # En lugar de '<cac:PhysicalLocation>', usa qname con el namespace
        physical_loc = etree.SubElement(roota, '{%s}PhysicalLocation' % nsmap['cac'])
        address = etree.SubElement(physical_location, '{%s}Address' % nsmap['cac'])

        #address = etree.SubElement(
        #        physical_location,
        #       '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Address',
        #       nsmap=nsmap
        #)

        # 3. Crear SubElementos usando la sintaxis {URI}tag
        # Esto genera <cbc:ID> correctamente, asociando la URI al prefijo definido
        cbc_id = etree.SubElement(address, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID")
        print ("Emisor data[1]['emisor']['ciudadCodigo'] =", data[1]['emisor']['ciudadCodigo'])
        cbc_id.text = data[1]['emisor']['ciudadCodigo']  ## codigo DANE para bogota
  

        # 3. Correcta creación de elementos cbc
        city_name = etree.SubElement(
                 address,
                 '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CityName',
                 nsmap=nsmap
        )
        print ("Emisor data[1]['emisor']['ciudadNombre'] =", data[1]['emisor']['ciudadNombre'])

        city_name.text = data[1]['emisor']['ciudadNombre']


        # Crear subelemento cbc:CountrySubentity
        country_element = etree.SubElement(
              address, 
              f"{{{nsmap['cbc']}}}CountrySubentity"
        )
        print ("Emisor data[1]['emisor']['paisNombre'] =", data[1]['emisor']['paisNombre'])
        country_element.text = data[1]['emisor']['paisNombre']

          # 3. Crear SubElementos usando la sintaxis {URI}localname
        # Esto crea  correctamente
        country_sub = etree.SubElement(
                address, 
               '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CountrySubentityCode'
        )
        print ("misor data[1]['emisor']['paisCodigo'] =", data[1]['emisor']['paisCodigo'])
        country_sub.text =  data[1]['emisor']['paisCodigo'] # Ejemplo: Bogotá





        # 4. LA SOLUCIÓN: Usar el NS completo en SubElement
        # AddressLine dentro de PhysicalLocation
        address_line = etree.SubElement(address, "{%s}AddressLine" % nsmap['cac'])
        line_text = etree.SubElement(address_line, "{%s}Line" % nsmap['cbc'])
        print ("Emisor data[1]['emisor'] direccion =", data[1]['emisor']['direccion']['direccion'])
        line_text.text =data[1]['emisor']['direccion']['direccion']

        # 3. Crear subelementos usando Clark Notation {URI}tag
        # Esto asignará automáticamente el prefijo 'cac' al tag
        country = etree.SubElement(  address,     "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Country"
        )

        # 4. Crear sub-subelemento con prefijo cbc
        code = etree.SubElement(
               country,            "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode"
        )
        code.text = "CO"

        # URL del namespace CommonBasicComponents-2
        CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"

        ## AQUI COMIENZAN LOS IMPUESTOS DEL EMISOR



        # FORMA CORRECTA: Agregar PartyTaxScheme
        party_tax_scheme = etree.SubElement(roota, "{" + nsmap['cac'] + "}PartyTaxScheme")

        registration_name = etree.SubElement(party_tax_scheme, "{" + nsmap['cbc'] + "}RegistrationName")
        print("Aqui toy receptor_00611")
        print ("Emisor registration_name.text =", data[1]['emisor']['nombreRazonSocial'])
        registration_name.text = data[1]['emisor']['nombreRazonSocial']

        # 2. Crear cbc:CompanyID con el NS completo y atributos
        company_id = etree.SubElement(  registration_name,   "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID",
              schemeID="8",
              schemeName="31",
              schemeAgencyID="195",
              schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)"
        )
        company_id.text = data[1]['emisor']['nit'] # NIT del emisor/receptor

        # 3. Solución a tu problema específico: {URI} + etiqueta
        # Nota: La DIAN requiere que cbc:TaxLevelCode esté dentro de cac:PartyTaxScheme
        tax_level_code = etree.SubElement(
             registration_name, 
              '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxLevelCode',
              listName="No Aplica"
              )
        tax_level_code.text = 'O-13;O-15'



        # 3. Crear RegistrationAddress usando el NS completo (Clark Notation)
        #
        address = etree.SubElement(
            party_tax_scheme,
           '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}RegistrationAddress'
            )


         # 2. Crear ID dentro de RegistrationAddress
        id_element = etree.SubElement(party_tax_scheme, '{%s}ID' % nsmap['cbc'])
        id_element.text = '11001' # Agregar el valor


         # 4. Para elementos hijos cbc, igual:
        city = etree.SubElement(
            address, 
            '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CityName'
            )
        city.text = data[1]['emisor']['ciudadNombre']

        country_sub = etree.SubElement(
                address, 
                "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CountrySubentity"
                )
        country_sub.text = data[1]['emisor']['ciudadNombre']

        cbc_ns = nsmap['cbc']
        country_sub_code = etree.SubElement(address, f"{{{cbc_ns}}}CountrySubentityCode")
        country_sub_code.text = data[1]['emisor']['ciudadCodigo']

        address_line = etree.SubElement(
            address, 
           "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AddressLine",
            nsmap=nsmap
            )

        CBC_NS = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"

 
        # Suponiendo que 'parent' es tu elemento <cac:AddressLine> o similar
        linea = etree.SubElement(address_line, f"{{{CBC_NS}}}Line")
        linea.text = data[1]['emisor']['direccion']['direccion']

        country = etree.SubElement(address, '{%s}Country' % nsmap['cac'])
        print ("Aquip voy 01")
 
        # 4. Añadir sub-elementos internos (ejemplo: Codigo de pais)
        identification_code = etree.SubElement(country, '{%s}IdentificationCode' % nsmap['cbc'])
        identification_code.text = data[1]['emisor']['ciudadCodigo']

        monetary = etree.SubElement(
               country,
               "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name",
                languageID="es"
                )
        monetary.text = "Colombia"
        print ("Aquip voy 0001")

        tax_scheme = etree.SubElement(
              party_tax_scheme, 
                f"{{{nsmap['cac']}}}TaxScheme"
              )
 
        # 2. Agregar subelementos (ID, Name, etc.)
        tax_scheme_id = etree.SubElement(tax_scheme, f"{{{nsmap['cbc']}}}ID")
        tax_scheme_id.text = "01" # Ejemplo IVA

        monetary = etree.SubElement(
               tax_scheme, 
              '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name'
               )
        monetary.text = 'IVA'

        print(etree.tostring(roota, pretty_print=True, encoding='unicode'))

        ## FIN PARTE DE IMPUESTOS EMISOR 

        ## AQUI COMIENZA LA PARTE LEGAL DEL EMISOR
        party = etree.SubElement(roota, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party')
        party_legal = etree.SubElement(party, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyLegalEntity')

        # 3. Agregar subelementos (ejemplo)
        registration_name = etree.SubElement(party_legal, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName')
        registration_name.text = data[1]['emisor']['nombreRazonSocial']


        company_id = etree.SubElement(
             party_legal, 
             "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CompanyID",
             schemeID="8", 
             schemeName="31", 
             schemeAgencyID="195", 
             schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)",
             nsmap=nsmap # Opcional aquí si ya está en la raíz
             )
        company_id.text = data[1]['emisor']['nit'] # Tu NIT

        print("Aqui toy receptor_006")

  
        # 1. Define los namespaces más comunes que usa la DIAN
        cac_ns = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"

        # 2. Crea el elemento asignándole la URL del NS entre llaves
        name = etree.SubElement(
                party_legal, 
                f"{{{cac_ns}}}CorporateRegistrationScheme"
       )
        print("Aqui toy receptor_000006")
        name.text = data[2]['receptor']['prefijo']  ## OPS AQUI ES EL PREFIJO

        contacto = etree.SubElement(party_legal, "{" + nsmap['cac'] + "}Contact")
        contacto.text = ""
        print("Aqui toy receptor_0000061111")
        phone = etree.SubElement(contacto, "{%s}Telephone" % nsmap['cbc'])
        phone.text = data[1]['emisor']['telefono']

        contact = etree.SubElement(root, "Contact")


        # 2. FORMA CORRECTA: Usar el namespace cbc explícitamente
        email = etree.SubElement(contacto, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ElectronicMail")
        email.text = data[1]['emisor']['correo']   ## "fact.electronica@clinicamedical.com.co"

        print(etree.tostring(roota, pretty_print=True, encoding='unicode'))
        print("Aqui imprimi ya PartyLegalEntity")

       # Crea el elemento con el nombre directo
        cbc_ns = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
        el = etree.SubElement(roota, f"{{{cbc_ns}}}AdditionalAccountID")

        # Definir la URI del namespace cac
        cac_ns = "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}"

        # Crear el elemento Party dentro de AccountingSupplierParty
        #party = etree.SubElement(roota, f"{cac_ns}AccountingSupplierParty")
        #party_inner = etree.SubElement(party, f"{cac_ns}Party")


        # 2. Crear el elemento raíz con los namespaces
        #invoice = etree.Element('{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice', nsmap=nsmap)

        # 3. Crear estructuras superiores (ejemplo Party)
        #party = etree.SubElement(invoice, '{' + nsmap['cac'] + '}Party')
        #party = etree.SubElement(roota, '{' + nsmap['cac'] + '}Party')

        # 4. SOLUCIÓN: PartyIdentification con namespace completo
        #party_id = etree.SubElement(party, '{' + nsmap['cac'] + '}PartyIdentification')

        # 5. ID del tercero con namespace cbc
        #id_element = etree.SubElement(party_id, '{' + nsmap['cbc'] + '}ID', schemeID='9', schemeName='31', schemeAgencyID='195', schemeAgencyName='CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)')
        #id_element.text = data[2]['receptor']['nit'] # NIT del Adquiriente

        ################### FIN EMISOR
        print ("FIN EMISOR")

        print ("Creo desde aquip customer - receptor")	
        ################### INICIO CUSTOMER


        # 3. Crear el subelemento AccountingCustomerParty correctamente
        # La DIAN exige: cac:AccountingCustomerParty
        customer_party = etree.SubElement(
                roota, 
                "{%s}AccountingCustomerParty" % nsmap['cac']
        )

        # 4. Agregar subelementos con el NS 'cac'
        party = etree.SubElement(customer_party, "{%s}Party" % nsmap['cac'])


        # Crear PartyIdentification - AQUI ESTABA TU ERROR
        party_id = etree.SubElement(
                party, 
                '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyIdentification'
        )

        # Añadir el ID con el valor (cbc:ID)
        id_node = etree.SubElement(
             party_id,
            '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID',
             schemeID="31", # Por ejemplo: NIT
             schemeName="31",
             schemeAgencyID="6",
             schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)"
             )
        id_node.text = data[2]['receptor']['nit'] # NIT del cliente

        # 5. Agregar elementos básicos con el NS 'cbc' (ej. Nombre)
        party_name = etree.SubElement(party, "{%s}PartyName" % nsmap['cac'])
        name = etree.SubElement(party_name, "{%s}Name" % nsmap['cbc'])
        name.text = data[2]['receptor']['nombreRazonSocial']

        print("Aqui voy receprorazo_01")

        NS_CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"


        # Agregar el nodo nieto <cac:PhysicalLocation>
        physical_location = etree.SubElement(party, etree.QName(NS_CAC, 'PhysicalLocation'))


        print("Aqui voy receprorazo_011")
        # 3. Crear Address dentro de PhysicalLocation
        address = etree.SubElement(
              physical_location, 
              "{%s}Address" % nsmap['cac']
              )

        # 4. Añadir sub-elementos (ejemplo)
        address_id = etree.SubElement(address, "{%s}ID" % nsmap['cbc'])
        address_id.text = "11001"

        city_name = etree.SubElement(address, "{%s}CityName" % nsmap['cbc'])

        # 3. Asignar el valor
        city_name.text = data[2]['receptor']['ciudadNombre']

        # cbc:CountrySubentity
        country_sub = etree.SubElement(address, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}CountrySubentity')
        country_sub.text = data[2]['receptor']['ciudadCodigo'] # Ejemplo: Bogotá

        # 3. Crear cbc:CountrySubentityCode dentro de Address
        country_subentity_code = etree.SubElement(address, '{' + nsmap['cbc'] + '}CountrySubentityCode')
        country_subentity_code.text = data[2]['receptor']['ciudadCodigo'] # Ejemplo: Bogota

        address_line = etree.SubElement(address, '{%s}AddressLine' % nsmap['cac'])
        line = etree.SubElement(address_line, '{%s}Line' % nsmap['cbc'])

        # 3. Asignar el valor
        line.text = data[2]['receptor']['direccion']['direccion']

        country = etree.SubElement(address, '{' + nsmap['cac'] + '}Country')
        ident_code = etree.SubElement(country, '{' + nsmap['cbc'] + '}IdentificationCode')


        # 3. Asignar el valor
        ident_code.text = data[2]['receptor']['paisCodigo'] # Ejemplo: Colombia

        # 4. cbc:Name (dentro de Country) con atributo languageID
        cbc_name = etree.SubElement(country, "{%s}Name" % nsmap['cbc'])
        cbc_name.set("languageID", "es")

        cbc_name.text = data[2]['receptor']['paisNombre'] 
        print("Aqui voy receprorazo_0222")

        NS_CAC = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"

        # 4. Crear el nodo hijo con el mismo NS
        party_tax_scheme = etree.SubElement(
            customer_party, 
            f"{{{NS_CAC}}}PartyTaxScheme"
        )

        #party_tax_scheme = etree.SubElement(party, "cac:PartyTaxScheme")
        print("Aqui voy receprorazo_02223333")
        # 3. Crear el elemento final con el nombre

        registration_name = etree.SubElement(party_tax_scheme, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}RegistrationName')
        registration_name.text = data[2]['receptor']['nombreRazonSocial'] 
        print("Aqui voy receprorazo_03")
        # Añadir subelementos (ejemplo: CompanyID)
        #company_id = etree.SubElement(party_tax_scheme, "cbc:CompanyID")

        NS_CBC = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"


        # 4. Incluir los atributos en su respectivo tag
        company_id = etree.SubElement(
              party_tax_scheme, 
              f"{{{NS_CBC}}}CompanyID", 
              schemeID="6", 
              schemeName="31", 
              schemeAgencyID="195", 
              schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)"
        )
        company_id.text = data[2]['receptor']['nit'] # Reemplaza con tu NIT sin puntos

        print("Aqui voy receprorazo_031")
        company_id.set("schemeID", "6")

        # 4. TaxLevelCode (con atributo listName)
        tax_level = etree.SubElement(
            party_tax_scheme, 
            f"{{{nsmap['cbc']}}}TaxLevelCode",
            listName="No Aplica"
        )
        tax_level.text = "0-13"
        print("Aqui voy receprorazo_03111")
        # 4. <cac:RegistrationAddress>
        address = etree.SubElement(party_tax_scheme, '{%s}RegistrationAddress' % nsmap['cac'])
        print("Aqui voy receprorazo_0312")
        # --- cbc:ID ---
        id_el = etree.SubElement(address, '{%s}ID' % nsmap['cbc'])

 
        id_el.text = data[2]['receptor']['ciudadCodigo'] # Código de la ciudad, por ejemplo
  
        city = etree.SubElement(address, '{%s}CityName' % nsmap['cbc'])
        city.text = data[2]['receptor']['ciudadNombre']

        country_subentity = etree.SubElement(address, "{%s}CountrySubentity" % nsmap['cbc'])

        # 4. Asignar el valor
        country_subentity.text = data[2]['receptor']['ciudadCodigo'] # Ejemplo: Cundinamarca


        country_subentity = etree.SubElement(address, f"{{{NS_CBC}}}CountrySubentityCode")


        # 3. Asignar valor
        country_subentity.text = data[2]['receptor']['ciudadCodigo']

        # 5. <cbc:AddressLine>
        address_line = etree.SubElement(address, '{%s}AddressLine' % nsmap['cbc'])

        # 6. Añadir contenido (ejemplo)
        line_content = etree.SubElement(address_line, '{%s}Line' % nsmap['cbc'])
        line_content.text = data[2]['receptor']['direccion']['direccion']

        # <cac:Country>
        country = etree.SubElement(address, '{' + nsmap['cac'] + '}Country')

        # Crear IdentificationCode
        id_code = etree.SubElement(country, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IdentificationCode")
        id_code.text = data[2]['receptor']['paisCodigo']

        # 4. Crear el elemento final con atributo
        name = etree.SubElement(country, '{%s}Name' % nsmap['cbc'], languageID="es")
        name.text = data[2]['receptor']['paisNombre']

        # 5. Crear TaxScheme y TaxScheme/Name
        tax_scheme = etree.SubElement(party_tax_scheme, "{%s}TaxScheme" % nsmap['cac'])

        # Opcional: Agregar ID dentro del TaxScheme
        tax_id = etree.SubElement(tax_scheme, f"{{{nsmap['cbc']}}}ID")
        tax_id.text = "01" # Ejemplo

        name = etree.SubElement(tax_scheme, "{%s}Name" % nsmap['cbc'])
        name.text = "IVA"

        # 3. Crear cac:PartyLegalEntity dentro de cac:Party
        party_legal = etree.SubElement(party, f"{{{nsmap['cac']}}}PartyLegalEntity")

        # 4. Agregar subelementos con cbc (RegistrationName, CompanyID)
        reg_name = etree.SubElement(party_legal, f"{{{nsmap['cbc']}}}RegistrationName")
        reg_name.text =data[2]['receptor']['nombreRazonSocial']

        company_id = etree.SubElement(
                party_legal, 
                "{%s}CompanyID" % nsmap['cbc'],
                schemeID="6", 
                schemeName="31", 
                schemeAgencyID="195", 
                schemeAgencyName="CO, DIAN (Dirección de Impuestos y Aduanas Nacionales)"
        )

        company_id.text = data[1]['emisor']['nit'] # NIT del emisor

        corp_reg = etree.SubElement(party_legal, f"{{{nsmap['cac']}}}CorporateRegistrationScheme")

        # Ejemplo para agregar un dato dentro
        name = etree.SubElement(corp_reg, f"{{{nsmap['cbc']}}}Name")
        name.text = data[2]['receptor']['nombreRazonSocial']

        contact = etree.SubElement(party, '{%s}Contact' % nsmap['cac'])
        name = etree.SubElement(contact, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name')
        print("Aqui voy receprorazo_031222200")
        # 4. Asignar valor
        name.text = data[2]['receptor']['contacto']
        print("Aqui voy receprorazo_0312222")
        # 4. Añadir datos dentro del Contact (ejemplo)
        phone = etree.SubElement(contact, '{%s}Telephone' % nsmap['cbc'])
        phone.text = data[2]['receptor']['telefono']

        email = etree.SubElement(contact, '{%s}ElectronicMail' % nsmap['cbc'])

        # 3. Asignar el valor
        email.text = data[2]['receptor']['correo']


        # Imprimir resultado
        print(etree.tostring(roota, pretty_print=True, encoding='unicode'))
      

        ## fin customer
        ########################################

        ## inicio totales
        ########################################

 
        # 3. MODO CORRECTO DE CREAR PaymentMeans (SubElement + Clark Notation)
        # No uses "<cac:PaymentMeans>", usa "{URI}tag"
        cac_ns = nsmap['cac']
        payment_means = etree.SubElement(roota, f'{{{cac_ns}}}PaymentMeans')

        print("Totales_01")
        # Agregar ID y PaymentMeansCode con URI de 'cbc'
        id_pm = etree.SubElement(
            payment_means, 
            '{' + nsmap['cbc'] + '}ID'
        )
        id_pm.text = '2' # Ejemplo: 1=Contado, 2=Credito
        print("Totales_02")

        # Código del medio de pago (Obligatorio)
        pm_code = etree.SubElement(
        payment_means, 
           '{' + nsmap['cbc'] + '}PaymentMeansCode'
        )
        pm_code.text = '47' # 10=Efectivo, 42=Consignacion, etc.

        payment_due_date = etree.SubElement(payment_means, '{' + nsmap['cbc'] + '}PaymentDueDate')
        print("Voy a la fecha = ", fecha_hoy)

        payment_due_date.text = fecha_hoy

        monetary = etree.SubElement(
                roota, 
                "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}LegalMonetaryTotal"
        )

        # 3. Agregar subelementos hijos con el namespace cbc
        line_extension = etree.SubElement(
               monetary,
               "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}LineExtensionAmount"
        )
        print("Totales_03 = ", data[4])
        line_extension.text = data[4]['totales']['valorBruto']
        line_extension.set("currencyID", "COP")
        print("Totales_04")
        # 3. Crear cbc:TaxExclusiveAmount (hijo con atributo)
        tax_exclusive = etree.SubElement(monetary, '{%s}TaxExclusiveAmount' % nsmap['cbc'], currencyID="COP")
        tax_exclusive.text ="0.00" # Tu valor aquí

        # 4. Crear cbc:PayableAmount (hijo con atributo)
        #payable = etree.SubElement(monetary, '{%s}PayableAmount' % nsmap['cbc'], currencyID="COP")
        #payable.text = data[4]['totales']['valorBruto'] # Tu valor aquí

        # 3. Crear TaxInclusiveAmount
        tax_incl = etree.SubElement(monetary, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxInclusiveAmount', currencyID="COP")
        tax_incl.text = data[4]['totales']['valorBruto'] # Tu valor total
        print("Totales_05")
        # 2. Crear cbc:AllowanceTotalAmount bajo LegalMonetaryTotal
        allowance_amount = etree.SubElement(monetary, "{%s}AllowanceTotalAmount" % nsmap['cbc'])
        print("Totales_06")

        # 3. Asignar atributos y valor
        allowance_amount.set("currencyID", "COP")
        allowance_amount.text = "0.00"  # O el valor que necesites

        # 2. Crear LegalMonetaryTotal
        monetary = etree.SubElement(roota, '{' + nsmap['cac'] + '}LegalMonetaryTotal', nsmap=nsmap)
        print("Totales_07")

        # 3. Crear ChargeTotalAmount con atributo currencyID
        # Usamos el prefijo cbc para los hijos de monetary
        charge_amount = etree.SubElement(monetary, '{' + nsmap['cbc'] + '}ChargeTotalAmount')
        charge_amount.set('currencyID', 'COP')
        charge_amount.text = '0.00' # O el valor correspondiente

        print("Totales_08")

        payable_amount = etree.SubElement(monetary, '{' + nsmap['cbc'] + '}PayableAmount')
        payable_amount.set('currencyID', 'COP')
        print("Totales_09 = ", data[4]['totales']['valorNeto'] )
        payable_amount.text = str(data[4]['totales']['valorNeto'])
        print("Totales_10")
       # Imprimir resultado
        print(etree.tostring(roota, pretty_print=True, encoding='unicode'))
      
        print("Vamos en totales")
        ## FIN TOTALES
        ########################################

        total_base = 0
        total_iva = 0
        print("Items ")
        print("data[3]['items'][0] = ", data[3]['items'][0])

        for i, p in enumerate(data[3]['items'], 1):

            print ("entre_01")
            print ("i = ", i)
            print ("p =" , p)
            print ("p valorUnitario =" , p['valorUnitario'])
            print ("p cantidad =" , p['cantidad'])
            print ("p valorTotal =" , p['valorTotal'])

 

            line_base = float(p['cantidad']) * float(p['valorUnitario'])
            print("line_base =", line_base)
            #line_iva = line_base * (p['iva_rate'] / 100)
            #line_iva = line_base * ( data[3]['items'][0]['impuestos']['porcentaje'] / 100)
            line_iva=0
            total_base += line_base
            total_iva += line_iva
            print("Aqui toy_items_01")

            ## desde aquip items

            # 3. Crear InvoiceLine correctamente (sin etiquetas crudas)
            invoice_line = etree.SubElement(roota, "{%s}InvoiceLine" % nsmap["cac"])

            # 4. Crear los subelementos internos
            line_id = etree.SubElement(invoice_line, "{%s}ID" % nsmap["cbc"])
            line_id.text = str(i)
            print("Aqui toy_items_02")
            # 3. Crear cbc:InvoicedQuantity con el atributo unitCode
            invoiced_qty = etree.SubElement(invoice_line, f"{{{nsmap['cbc']}}}InvoicedQuantity", unitCode="94")
            invoiced_qty.text = str(p['cantidad']) # Ejemplo de cantidad
            print("Aqui toy_items_03")
            # 3. Crear LineExtensionAmount con el atributo currencyID
            line_ext_amount = etree.SubElement(invoice_line, '{%s}LineExtensionAmount' % nsmap['cbc'])
            line_ext_amount.set('currencyID', 'COP')
            line_ext_amount.text = str(p['valorTotal'])  # El valor de la línea
            print("Aqui toy_items_04")
            free_of_charge = etree.SubElement(invoice_line, "{%s}FreeOfChargeIndicator" % nsmap["cbc"])
            free_of_charge.text = "false" # Ejemplo de valor (true/false)

            # 2. Crear Item bajo InvoiceLine
            item = etree.SubElement(invoice_line, f"{{{nsmap['cac']}}}Item")

            # 3. Crear Description bajo Item
            description = etree.SubElement(item, f"{{{nsmap['cbc']}}}Description")
            description.text = p['nombreProducto']

            sellers_id = etree.SubElement(item, '{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}SellersItemIdentification')
            print("Aqui toy_items_05")
            # Ejemplo: Un elemento CBC (con valor)
            cbc_id = etree.SubElement(sellers_id, '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID')
            print("Aqui toy_items_06") 
            cbc_id.text = str(p['codigoProducto'])

            extended_id = etree.SubElement(sellers_id, '{%s}ExtendedID' % nsmap['cbc'])
            print("Aqui toy_items_06") 
            # 4. Asignar valor
            extended_id.text = str(p['codigoProducto'])

            # 3. Crear StandardItemIdentification dentro de Item
            standard_id = etree.SubElement(item, '{%s}StandardItemIdentification' % nsmap['cac'])

            # 4. Agregar campos básicos (cbc)
            id_item = etree.SubElement(standard_id, '{%s}ID' % nsmap['cbc'])
            id_item.text = str(p['codigoProducto']) # Código del producto

            # 3. Agregar subelementos (como Price) dentro de InvoiceLine
            price = etree.SubElement(invoice_line, '{%s}Price' % nsmap['cac'])
            price_amount = etree.SubElement(price, '{%s}PriceAmount' % nsmap['cbc'])
            price_amount.text = str(p['valorUnitario'])

            base_qty = etree.SubElement(price, etree.QName(nsmap['cbc'], 'BaseQuantity'), unitCode="94")
            base_qty.text = str(p['cantidad'])

            ## hasta aquip items

        print(etree.tostring(roota, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode())
        print("FINAL ITEMS")


        # --- Finalización y Cierre de tags ---
        tree = etree.ElementTree(roota)
        # tostring cierra automáticamente todos los tags
        print("lo de siempre")
        #xml_final = etree.tostring(tree, pretty_print=False, xml_declaration=True, encoding='UTF-8')

        print("consola tree")
        print(etree.tostring(root, encoding='UTF-8').decode('UTF-8'))

        # Al cargar el XML original, usa esto para limpiar:
        #parser = etree.XMLParser(remove_blank_text=True)
        #tree = etree.parse(nombre_archivoXml, parser)
        #root = tree.getroot()
        #etree.indent(tree, space="  ", level=0)
        print("VOY A GUARDAR nombre_archivoXml = ", nombre_archivoXml)
        tree.write(nombre_archivoXml, pretty_print=False, xml_declaration=True, encoding='UTF-8', standalone=False)
        print("YA GUARDE VERIFICA ")
  	## FIN GENERAR XML CON TAGS


        # Aqui se debe crear kla ruta, el nombre del archivo CML_FIRMADO para la dian

        nombre_archivoXml_Firmado = nombre_carpeta + caracter_especial + str(numeroFacturaPrefijo) + '_Firmado.xml'
        print("nombre_archivoXml_Firmado =", nombre_archivoXml_Firmado)



        ## Fin rutina XML FIRMADO dian y agregarlo en el UPDATE que esta a continuacion


	## Aqui guardo todos los datos de facturacion electronica en las tablas

        detalle = 'UPDATE facturacion_facturacion SET "cufeValor" = ' + "'" + str(cufe) + "'," + '"cufeDefinitivo" = ' + "'" + str(cufe) + "'," + '"codigoQr" = ' + "'" + str(qr) + "'," + '"rutaQr" = ' + "'" + str(nombre_archivoQr) + "',"  + '"rutaXml" = ' + "'" + str(nombre_archivoXml) + "'," + '"rutaJson" = ' + "'" + str(nombre_archivoJson)  + "'," + '"rutaPdf" = ' + "'" + str(nombre_archivoPdf) + "'," + '"rutaXmlFirmado" = "' + str(nombre_archivoXml_Firmado) + "' WHERE id = " + str(facturacionId)
        print ('detalle = ', detalle)
        cur3.execute(detalle)
      
        miConexion3.commit()

        cur3.close()
        miConexion3.close()

        ##OJO aqui deberia invocar ImprimirFactura para imprimirla en pdf

        # Ver como hacer estop

        return JsonResponse({'success': True, 'Mensajes': 'Factura Elaborada  No !' , 'Factura' : facturacionId})


    except psycopg2.DatabaseError as error:

            print("Entre por rollback", error)
            if miConexion3:
                print("Entro ha hacer el Rollback")
                miConexion3.rollback()

            print("Voy a hacer el jsonresponde")
            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})



    finally:
            if miConexion3:
                cur3.close()
                miConexion3.close()


def LeerTotales(request):

    print ("Entre Leer Totales" )
    liquidacionId = request.POST["liquidacionId"]
    print ("liquidacionId = ", liquidacionId)

    liquidacionId1 = Liquidacion.objects.get(id=liquidacionId)


    try:
        with transaction.atomic():

         ingresoId=Ingresos.objects.get(tipoDoc_id=liquidacionId1.tipoDoc_id, documento_id=liquidacionId1.documento_id, consec=liquidacionId1.consecAdmision)
         ingreso=ingresoId.id
         tipoIngreso= 'INGRESO'
         comando =  'select ' + "'"  + str('INGRESO') + "'" + '  tipo, adm."salidaDefinitiva" salidaDefinitiva,liq.id id, dep.nombre dependenciaNombre,                                                     sd.nombre servicioNombre , "consecAdmision",  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,"totalSuministros", "totalLiquidacion", "valorApagar", "fechaCorte", anticipos, "detalleAnulacion", "fechaAnulacion", observaciones,  liq."fechaRegistro", "estadoRegistro", liq.convenio_id, liq."tipoDoc_id" , liq.documento_id, liq."usuarioRegistro_id", "totalAbonos","totalRecibido",   conv.nombre nombreConvenio, usu.nombre paciente, adm.id ingresoId1, usu.documento documento, tip.nombre tipoDocumento , adm."salidaClinica" salidaClinica FROM facturacion_liquidacion liq INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id" = liq."tipoDoc_id" AND usu.id = liq.documento_id) INNER JOIN admisiones_ingresos adm ON (adm."tipoDoc_id" = liq."tipoDoc_id"  AND adm.documento_id = liq.documento_id  AND adm.consec = liq."consecAdmision"  ) INNER JOIN usuarios_tiposdocumento  tip ON (tip.id = adm."tipoDoc_id")  LEFT JOIN sitios_serviciossedes sd ON (sd.id=adm."serviciosActual_id") LEFT JOIN clinico_servicios serv ON (serv.id = sd.servicios_id) LEFT JOIN sitios_dependencias dep on (dep.id =adm."dependenciasActual_id") LEFT JOIN  contratacion_convenios conv ON (conv.id = liq.convenio_id) where liq.id = ' + "'" +  str(liquidacionId) + "'"
 

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por PRONO SE HACE NADA:", e)

        triageId = Triage.objects.get(tipoDoc_id=liquidacionId1.tipoDoc_id, documento_id=liquidacionId1.documento_id,consecAdmision=liquidacionId1.consecAdmision)
        triage = triageId.id
        tipoIngreso = 'TRIAGE'
        comando =  'select ' + "'"  + str('TRIAGE') + "'" + ' tipo, tri."salidaDefinitiva" salidaDefinitiva, liq.id id, ' + "'" + str('Triage') + "'" + ' dependenciaNombre, ' + "'" + str('TRIAGE') + "'" + '  servicioNombre, tri."consecAdmision",  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,"totalSuministros", "totalLiquidacion", "valorApagar", "fechaCorte", anticipos, "detalleAnulacion", "fechaAnulacion", tri.observaciones, liq."fechaRegistro", "estadoRegistro", liq.convenio_id, liq."tipoDoc_id" , liq.documento_id, liq."usuarioRegistro_id", "totalAbonos","totalRecibido",  conv.nombre nombreConvenio, usu.nombre paciente, tri.id triageId1, usu.documento documento, tip.nombre tipoDocumento, ' + "'N'" + ' salidaClinica  FROM facturacion_liquidacion liq inner join  triage_triage tri on (tri."tipoDoc_id" = liq."tipoDoc_id"  and tri.documento_id = liq.documento_id  AND tri.consec = liq."consecAdmision" ) left join  contratacion_convenios conv on (conv.id = liq.convenio_id) inner join  usuarios_usuarios usu on (usu."tipoDoc_id" = liq."tipoDoc_id" AND usu.id = liq.documento_id) inner join usuarios_tiposdocumento  tip on (tip.id = usu."tipoDoc_id") where liq.id = ' + "'" +  str(liquidacionId) + "'"

    finally:
        print("No haga nada")


    miConexionx = None
    try:

            miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curx = miConexionx.cursor()

            if (tipoIngreso == 'INGRESO'):

                curx.execute(comando)
                for tipo, salidaDefinitiva,id, dependenciaNombre, servicioNombre, consecAdmision,fecha ,totalCopagos,totalCuotaModeradora,totalProcedimientos ,totalSuministros, totalLiquidacion, valorApagar, fechaCorte, anticipos, detalleAnulacion, fechaAnulacion, observaciones, fechaRegistro, estadoRegistro, convenio_id, tipoDoc_id , documento_id, usuarioRegistro_id, totalAbonos,totalRecibido, nombreConvenio , paciente, ingresoId1 , documento, tipoDocumento, salidaClinica in curx.fetchall():

                    paciente = paciente
                    salidaDefinitiva =salidaDefinitiva
                    dependenciaNombre =dependenciaNombre
                    servicioNombre = servicioNombre
                    consecAdmision= consecAdmision
                    fecha =fecha

                    return JsonResponse({'totalSuministros':totalSuministros,'totalProcedimientos':totalProcedimientos,'totalCopagos':totalCopagos,'totalCuotaModeradora':totalCuotaModeradora,'anticipos':anticipos, 'totalAbonos':totalAbonos, 'totalRecibido':totalRecibido, 'totalLiquidacion':totalLiquidacion, 'totalAPagar':valorApagar,'paciente': paciente,'salidaDefinitiva':salidaDefinitiva , "dependenciaNombre":dependenciaNombre ,"servicioNombre":servicioNombre,'consecAdmision':consecAdmision,'fecha':fecha})

            else:

                curx.execute(comando)
                for tipo, salidaDefinitiva, id, dependenciaNombre, servicioNombre, consecAdmision,fecha ,totalCopagos,totalCuotaModeradora,totalProcedimientos ,totalSuministros, totalLiquidacion, valorApagar, fechaCorte, anticipos, detalleAnulacion, fechaAnulacion, observaciones, fechaRegistro, estadoRegistro, convenio_id, tipoDoc_id , documento_id, usuarioRegistro_id, totalAbonos, totalRecibido,  nombreConvenio , paciente, triageId1 , documento, tipoDocumento , salidaClinica in curx.fetchall():

                    paciente = paciente
                    salidaDefinitiva =salidaDefinitiva
                    dependenciaNombre =dependenciaNombre
                    servicioNombre = servicioNombre
                    consecAdmision= consecAdmision
                    fecha =fecha

                    return JsonResponse({'totalSuministros':totalSuministros,'totalProcedimientos':totalProcedimientos,'totalCopagos':totalCopagos,
                         'totalCuotaModeradora':totalCuotaModeradora,'totalAnticipos':totalAnticipos, 'totalAbonos':totalAbonos, 'totalRecibido':totalRecibido, 'totalLiquidacion':totalLiquidacion, 'totalAPagar':valorApagar,'paciente': paciente,'salidaDefinitiva':salidaDefinitiva , "dependenciaNombre":dependenciaNombre ,"servicioNombre":servicioNombre,'consecAdmision':consecAdmision,'fecha':fecha})


    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexionx.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexionx:
            curx.close()
            miConexionx.close()



def LeerTotalesFactura(request):

    print ("Entre Leer Totales Factura" )
    facturaId = request.POST["facturaId"]
    print ("facturaId = ", facturaId)

    facturaId1 = Liquidacion.objects.get(id=facturaId)

    totalSuministros = FacturaDetalle.objects.all().filter(facturacion_id=facturaId).filter(examen_id = None).exclude(estadoRegistro='S').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
    totalSuministros = (totalSuministros['totalS']) + 0
    print("totalSuministros", totalSuministros)
    totalProcedimientos = FacturacionDetalle.objects.all().filter(facturacion_id=facturaId).filter(cums_id = None).exclude(estadoRegistro='S').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
    totalProcedimientos = (totalProcedimientos['totalP']) + 0
    print("totalProcedimientos", totalProcedimientos)
    registroPago = Facturacion.objects.get(id=facturacionId)
    totalCopagos = registroPago.totalCopagos
    totalCuotaModeradora = registroPago.totalCuotaModeradora
    totalAnticipos = registroPago.anticipos
    totalAbonos = registroPago.totalAbonos
    totalRecibido = registroPago.totalRecibido
    totalAnticipos = registroPago.anticipos
    valorApagar = registroPago.valorApagar
    totalLiquidacion = registroPago.totalLiquidacion

    miConexionx = None
    try:

            miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curx = miConexionx.cursor()

            comando = 'SELECT fac."totalSuministros",fac."totalProcedimientos", fac."totalCopagos", fac."totalCuotaModeradora", fac."totalAnticipos",fac."totalAbonos", fac."totalRecibido" , fac."totalLiquidacion", fac."totalAPagar" valorApagar FROm facturacion_facturacion WHERE id = ' + "'" + str(facturaId) + "'"

            for totalSuministros,totalProcedimientos, totalCopagos,totalCuotaModeradora,totalAnticipos,totalAbonos,totalRecibido , totalLiquidacion,  valorApagar in curx.fetchall():

                return JsonResponse({'totalSuministros':totalSuministros,'totalProcedimientos':totalProcedimientos,'totalCopagos':totalCopagos,
			         'totalCuotaModeradora':totalCuotaModeradora,'totalAnticipos':totalAnticipos, 'totalAbonos':totalAbonos, 'totalRecibido':totalRecibido, 'totalLiquidacion':totalLiquidacion, 'totalAPagar':valorApagar})


    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexionx.rollback()

        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})

    finally:
        if miConexionx:
            curx.close()
            miConexionx.close()



# Create your views here.
def load_dataFacturacion(request, data):
    print ("Entre load_data Facturacion")
    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)

    hastaFecha = timezone.now()
    bandera = d['bandera']
    if bandera == "Por Fecha":
        desdeFecha = '2025-01-01 00:00:00'
        hastaFecha = timezone.now()

    else:
        desdeFactura = d['desdeFactura']
        hastaFactura = d['hastaFactura']


    # Combo Indicadores

    # Fin combo Indicadores

    facturacion = []

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",     password="123456")
    curx = miConexionx.cursor()

    print ("bandera = " , bandera)
   
    if bandera == "Por Fecha":

       print ("Entre por Fecha")
       #detalle = 'SELECT facturas.id id , facturas."fechaFactura" fechaFactura, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,i.consec consec , i."fechaIngreso" fechaIngreso , i."fechaSalida" fechaSalida, ser.nombre servicioNombreSalida, dep.nombre camaNombreSalida , diag.nombre dxSalida , conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica, facturas."estadoReg" estadoReg FROM admisiones_ingresos i INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id") INNER JOIN sitios_dependencias dep ON (dep."sedesClinica_id" = i."sedesClinica_id" AND dep."serviciosSedes_id" = sd.id AND dep.id = i."dependenciasSalida_id")  INNER JOIN sitios_dependenciastipo deptip  ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" =  i."tipoDoc_id" AND u.id = i."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") INNER JOIN clinico_servicios ser  ON ( ser.id  = i."serviciosSalida_id")  INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxSalida_id") INNER JOIN facturacion_facturacion facturas ON (facturas.documento_id = i.documento_id and facturas."tipoDoc_id" = i."tipoDoc_id" and facturas."consecAdmision" = i.consec ) LEFT JOIN contratacion_convenios conv  ON (conv.id = facturas.convenio_id ) WHERE i."fechaSalida" between ' + "'" + str(desdeFecha) + "'" + '  and ' + "'" + str(hastaFecha) + "'" + ' AND i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND i."fechaSalida" is not null '
       detalle = 'SELECT facturas.id id , facturas."fechaFactura" fechaFactura, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,	i.consec consec , i."fechaIngreso" fechaIngreso , i."fechaSalida" fechaSalida, ser.nombre servicioNombreSalida,	dep.nombre camaNombreSalida , substring(diag.nombre,1,30) dxSalida , conv.nombre convenio, conv.id convenioId , 	i."salidaClinica" salidaClinica, facturas."estadoReg" estadoReg, facturas.anulado FROM admisiones_ingresos i INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" and sd.id = i."serviciosSalida_id") 	INNER JOIN sitios_historialdependencias histdep ON ( histdep.dependencias_id = i."dependenciasSalida_id")  INNER JOIN sitios_dependencias dep ON (dep.id=histdep.dependencias_id) 	INNER JOIN sitios_dependenciastipo deptip  ON (deptip.id = dep."dependenciasTipo_id")  INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" =  i."tipoDoc_id" AND u.id = i."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") 	INNER JOIN clinico_servicios ser  ON ( ser.id  = sd.servicios_id ) INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxSalida_id") INNER JOIN facturacion_facturacion facturas ON (facturas.documento_id = i.documento_id and facturas."tipoDoc_id" = i."tipoDoc_id" and facturas."consecAdmision" = i.consec ) inner JOIN contratacion_convenios conv  ON (conv.id = facturas.convenio_id ) WHERE i."fechaSalida" between ' + "'" + str(desdeFecha) + "'" + ' and ' + "'" + str(hastaFecha) + "'" + ' AND i."sedesClinica_id" = ' + "'" + str(sede) + "'" + '  GROUP BY 	facturas.id  , facturas."fechaFactura" , tp.nombre ,u.documento ,u.nombre , i.consec , i."fechaIngreso"  , i."fechaSalida" , ser.nombre ,	dep.nombre  , diag.nombre  , conv.nombre , conv.id  , 	i."salidaClinica" , facturas."estadoReg"  UNION SELECT facturas.id id , facturas."fechaFactura" fechaFactura, tp.nombre tipoDoc,u.documento documento,u.nombre nombre, i.consec consec , i."fechaIngreso" fechaIngreso , i."fechaSalida" fechaSalida, ser.nombre servicioNombreSalida,dep.nombre camaNombreSalida , diag.nombre dxSalida , conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica, facturas."estadoReg" estadoReg, facturas.anulado  FROM admisiones_ingresos i left JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" and sd.id = i."serviciosSalida_id") left JOIN sitios_historialdependencias histdep ON ( histdep.dependencias_id = i."dependenciasSalida_id") left JOIN sitios_dependencias dep ON (dep.id=histdep.dependencias_id) 	left JOIN sitios_dependenciastipo deptip  ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" =  i."tipoDoc_id" AND u.id = i."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") inner JOIN clinico_servicios ser  ON ( ser.id  = sd.servicios_id ) INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxSalida_id") INNER JOIN facturacion_facturacion facturas ON (facturas.documento_id = i.documento_id and facturas."tipoDoc_id" = i."tipoDoc_id" and facturas."consecAdmision" = i.consec ) inner JOIN contratacion_convenios conv  ON (conv.id = facturas.convenio_id ) inner JOIN facturacion_conveniospacienteingresos convPac  ON (convPac.convenio_id = conv.id and  convPac.factura_id =facturas.id  ) WHERE i."fechaSalida" is null AND i."sedesClinica_id" = ' + "'" + str(sede) +"'" + 'GROUP BY 	facturas.id  , facturas."fechaFactura" , tp.nombre ,u.documento ,u.nombre , i.consec , i."fechaIngreso"  , i."fechaSalida" , ser.nombre ,	dep.nombre  , diag.nombre  , conv.nombre , conv.id  , 	i."salidaClinica" , facturas."estadoReg" '


    else:

        print ("Entre por Factura")
        #detalle = 'SELECT facturas.id id , facturas."fechaFactura" fechaFactura, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,i.consec consec , i."fechaIngreso" fechaIngreso , i."fechaSalida" fechaSalida, ser.nombre servicioNombreSalida, dep.nombre camaNombreSalida , diag.nombre dxSalida , conv.nombre convenio, conv.id convenioId , i."salidaClinica" salidaClinica, facturas."estadoReg" estadoReg FROM admisiones_ingresos i INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id") INNER JOIN sitios_dependencias dep ON (dep."sedesClinica_id" = i."sedesClinica_id" AND dep."serviciosSedes_id" = sd.id AND dep.id = i."dependenciasSalida_id")  INNER JOIN sitios_dependenciastipo deptip  ON (deptip.id = dep."dependenciasTipo_id") INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" =  i."tipoDoc_id" AND u.id = i."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") INNER JOIN clinico_servicios ser  ON ( ser.id  = i."serviciosSalida_id")  INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxSalida_id") INNER JOIN facturacion_facturacion facturas ON (facturas.documento_id = i.documento_id and facturas."tipoDoc_id" = i."tipoDoc_id" and facturas."consecAdmision" = i.consec ) LEFT JOIN contratacion_convenios conv  ON (conv.id = facturas.convenio_id ) WHERE facturas.id between ' + "'" + str(desdeFactura) + "'" + '  and ' + "'" + str(hastaFactura) + "'" + ' AND i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND  i."fechaSalida" is not null '
        detalle = 'SELECT facturas.id id , facturas."fechaFactura" fechaFactura, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,	i.consec consec , i."fechaIngreso" fechaIngreso , i."fechaSalida" fechaSalida, ser.nombre servicioNombreSalida,	dep.nombre camaNombreSalida , diag.nombre dxSalida , conv.nombre convenio, conv.id convenioId , 	i."salidaClinica" salidaClinica, facturas."estadoReg" estadoReg , facturas.anulado FROM admisiones_ingresos i INNER JOIN sitios_serviciosSedes sd ON (sd."sedesClinica_id" = i."sedesClinica_id" and sd.id = i."serviciosSalida_id") 	INNER JOIN sitios_historialdependencias histdep ON (histdep."tipoDoc_id" = i."tipoDoc_id" AND histdep.documento_id = i.documento_id AND histdep.consec=i.consec AND histdep.disponibilidad= ' + "'" + str('L') + "')" + ' INNER JOIN sitios_dependencias dep ON (dep.id=histdep.dependencias_id) 	INNER JOIN sitios_dependenciastipo deptip  ON (deptip.id = dep."dependenciasTipo_id")  INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" =  i."tipoDoc_id" AND u.id = i."documento_id" ) INNER JOIN usuarios_tiposDocumento tp ON (tp.id = u."tipoDoc_id") 	INNER JOIN clinico_servicios ser  ON ( ser.id  = sd.servicios_id ) INNER JOIN clinico_Diagnosticos diag ON (diag.id = i."dxSalida_id") INNER JOIN facturacion_facturacion facturas ON (facturas.documento_id = i.documento_id and facturas."tipoDoc_id" = i."tipoDoc_id" and facturas."consecAdmision" = i.consec ) inner JOIN contratacion_convenios conv  ON (conv.id = facturas.convenio_id ) WHERE facturas.id between ' + "'" + str(desdeFactura) + "'" + ' and ' + "'" + str(hastaFactura) + "'" + ' AND i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' GROUP BY 	facturas.id  , facturas."fechaFactura" , tp.nombre ,u.documento ,u.nombre , i.consec , i."fechaIngreso"  , i."fechaSalida" , ser.nombre ,	dep.nombre  , diag.nombre  , conv.nombre , conv.id  , 	i."salidaClinica" , facturas."estadoReg" '

    print("detalle = ", detalle)

    curx.execute(detalle)

    for id ,fechaFactura, tipoDoc, documento, nombre, consec , fechaIngreso , fechaSalida, servicioNombreSalida, camaNombreSalida , dxSalida , convenio, convenioId , salidaClinica , estadoReg , anulado in curx.fetchall():
        facturacion.append(
		{"model":"facturacion.facturacion","pk":id,"fields":
			{'id':id, 'fechaFactura':fechaFactura, 'tipoDoc': tipoDoc, 'documento': documento, 'nombre': nombre, 'consec': consec,
                         'fechaIngreso': fechaIngreso, 'fechaSalida': fechaSalida,
                         'servicioNombreSalida': servicioNombreSalida, 'camaNombreSalida': camaNombreSalida,
                         'dxSalida': dxSalida,'convenio':convenio, 'convenioId':convenioId, 'salidaClinica':salidaClinica, 'estadoReg' : estadoReg, 'anulado':anulado}})

    miConexionx.close()
    print(facturacion)


    serialized1 = json.dumps(facturacion, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')



def PostConsultaFacturacion(request):
    print ("Entre PostConsultaFacturacion")

    Post_id = request.POST["post_id"]
    username_id = request.POST["username_id"]

    # Abro Conexion

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    cur = miConexionx.cursor()

    comando = 'select fac.id id, fac.id factura, fac."fechaFactura" fechaFactura, tip.nombre tipoDoc, usu.documento documento, usu.nombre paciente, fac."consecAdmision" consecAdmision, conv.nombre nombreConvenio,  "totalSuministros","totalProcedimientos","totalCopagos","totalCuotaModeradora","totalAbonos","totalRecibido", anticipos totalAnticipos,"valorApagar","totalFactura" , "valorAPagarLetras" , fac."estadoReg" estadoReg, fac.anulado anulado, "rutaXml" rutaXml, "rutaJson" rutaJson, "rutaPdf" rutaPdf,"rutaXmlRta" rutaXmlRta FROM facturacion_facturacion fac, contratacion_convenios conv, usuarios_usuarios usu, usuarios_tiposdocumento tip where fac.id = ' + "'" + str(Post_id) + "'" + '  AND  fac.convenio_id = conv.id and usu.id = fac.documento_id  and fac."tipoDoc_id" = usu."tipoDoc_id"   AND tip.id = fac."tipoDoc_id" AND fac.documento_id = usu.id  AND conv.id = fac.convenio_id '

    print(comando)

    cur.execute(comando)

    facturacion = []

    for id,factura , fechaFactura , tipoDoc, documento, paciente, consecAdmision , nombreConvenio , totalSuministros,totalProcedimientos,totalCopagos,totalCuotaModeradora,totalAbonos,totalRecibido,totalAnticipos,valorApagar,totalFactura , valorAPagarLetras , estadoReg, anulado, rutaXml, rutaJson, rutaPdf ,rutaXmlRta in cur.fetchall():
            facturacion.append( {"id": id,"factura":factura, "fechaFactura" : fechaFactura, "tipoDoc":tipoDoc, "documento":documento,
                     "paciente": paciente, "consecAdmision": consecAdmision, "nombreConvenio": nombreConvenio,'totalSuministros':totalSuministros,'totalProcedimientos':totalProcedimientos,'totalCopagos':totalCopagos,'totalCuotaModeradora':totalCuotaModeradora,'totalAbonos':totalAbonos,'totalRecibido':totalRecibido,'totalAnticipos':totalAnticipos,'valorApagar':valorApagar,'totalFactura':totalFactura, 'valorAPagarLetras':valorAPagarLetras,
                                 'estadoReg':estadoReg, 'anulado':anulado, 'rutaXml':rutaXml,'rutaPdf':rutaPdf, 'rutaJson':rutaJson, 'rutaXmlRta':rutaXmlRta
                                 })
            rutaXml = rutaXml
            rutaJson = rutaJson
            rutaPdf = rutaPdf
            rutaXmlRta = rutaXmlRta




    miConexionx.close()
    print(facturacion)

    # Cierro Conexion

    #Extraigo la info del xml
    contenido_completo=''
    contenido_completoJson = ''
    print ("rutaXml")

    #if os.path.exists(rutaXml):
    if os.path.exists(rutaJson):

        try:
            # Abre el archivo en modo lectura ('r') con codificación UTF-8
            with open(rutaJson, 'r', encoding='utf-8') as archivo:
                contenido_completoJson = archivo.read()
                print("Contenido completo del archivo:")
                print(contenido_completoJson)

            with open(rutaXml, 'r', encoding='utf-8') as archivo:
                contenido_completoXml = archivo.read()
                print("Contenido completoXml del archivo:")
                print(contenido_completoXml)



        except FileNotFoundError:
            print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
            #except Exception as e:
            #    print(f"Ocurrió un error al leer el archivo: {e}")

    else:
        ## El archivo no existe
        print(f"Error: The file '{rutaXml}' was not found.")
        content = "Default content because the file was not found."
        print("Using default content:")
        print(content)




    return JsonResponse({'pk':facturacion[0]['id'],'id':facturacion[0]['id'], 'factura':facturacion[0]['factura'],'fechaFactura':facturacion[0]['fechaFactura'],
		          'tipoDoc':facturacion[0]['tipoDoc'],'documento':facturacion[0]['documento'],'paciente':facturacion[0]['paciente'],  'consecAdmision':facturacion[0]['consecAdmision'],
                             'nombreConvenio':facturacion[0]['nombreConvenio'] , 
			'totalSuministros':facturacion[0]['totalSuministros'] ,'totalProcedimientos':facturacion[0]['totalProcedimientos'] ,'totalCopagos':facturacion[0]['totalCopagos'] ,'totalCuotaModeradora':facturacion[0]['totalCuotaModeradora'] ,'totalAbonos':facturacion[0]['totalAbonos'] ,'totalRecibido':facturacion[0]['totalRecibido'] ,'totalAnticipos':facturacion[0]['totalAnticipos'] ,
			'valorApagar':facturacion[0]['valorApagar'] ,'totalFactura':facturacion[0]['totalFactura'],'valorAPagarLetras':facturacion[0]['valorAPagarLetras'],
                         'estadoReg': facturacion[0]['estadoReg'], 'anulado': facturacion[0]['anulado'], 'contenido_Xml': contenido_completoXml , 'contenido_Json': contenido_completoJson, 'contenido_XmlRta':contenido_completoXml
       })



def AnularFactura(request):
    print ("Entre AnularFactura")
    facturacionId = request.POST["facturacionId"]
    username_id = request.POST["username_id"]

    print ("el id es = ", facturacionId)
    fechaRegistro = timezone.now()

    #Que pasa con los abonos aquip
    ##Rutina liberar Abonos, es decir devolverles el saldo/Aunque la factura original quede modificada por estos abonos

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE facturacion_facturacion SET "estadoReg" = ' + "'" + str('A') + "'" + ', anulado = ' + "'" + str('S') + "', " + '"fechaAnulacion" =   '  + "'" + str(fechaRegistro) + "'," + '"usuarioAnula_id" = ' + "'" + str(username_id) + "'"  + ' WHERE id =  ' + str(facturacionId )
        print(comando)
        cur3.execute(comando)


        comando1 = 'UPDATE facturacion_facturaciondetalle SET "estadoRegistro" = ' + "'" + str('A') + "'" + ', anulado = ' + "'" + str('S')  + "' WHERE facturacion_id =  " + str(facturacionId )
        print(comando1)
        cur3.execute(comando1)


        miConexion3.commit()
        miConexion3.close()


    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        print("Voy a hacer el jsonresponde")
        message_error=str(error)
        return JsonResponse({'success': False, 'Mensajes': error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


    return JsonResponse({'success': True, 'Mensajes': 'Factura ANULADA !', 'estadoFactura':'S'})


def ReFacturar(request):

    print ("Entre ReFacturar")
    usuarioRegistro = request.POST["username_id"]

    facturacionId = request.POST["facturacionId"]
    print ("el id es = ", facturacionId)

    serviciosAdministrativos = request.POST["serviciosAdministrativos"]
    print ("serviciosAdministrativos", serviciosAdministrativos)

    facturacionId2 = Facturacion.objects.get(id=facturacionId)

    fechaRegistro = timezone.now()

    if (facturacionId2.anulado !='S'):
        print("Fcctura debe star ANULADA previamente")
        return JsonResponse({'success': False, 'Mensajes': 'Factura debe ser anulada previamente'})

    print("Me voy a ANULAR")

    miConexion3 = None
    try:

                miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
                cur3 = miConexion3.cursor()

                comando = 'UPDATE facturacion_facturacion SET "anulado" = ' + "'" + str('R') + "'"  +  ', "usuarioRegistro_id" = ' + "'" + str(usuarioRegistro) + "'"  +  ', "fechaRegistro" = ' + "'" + str(fechaRegistro) + "'," + '"serviciosAdministrativos_id" = ' + "'" + str(serviciosAdministrativos) + "'"  +  ' WHERE id =  ' + facturacionId
                print (comando)
                cur3.execute(comando)


                comando = 'UPDATE facturacion_facturaciondetalle SET "anulado" = ' + "'" + str('R') + "'"  +  ', "usuarioRegistro_id" = ' + "'" + str(usuarioRegistro) + "'"  +  ', "fechaRegistro" = ' + "'" + str(fechaRegistro) + "'"  +  ' WHERE facturacion_id =  ' + facturacionId
                print (comando)
                cur3.execute(comando)


                liquidacionU = Liquidacion.objects.all().aggregate(maximo=Coalesce(Max('id'), 0))
                liquidacionId = (liquidacionU['maximo']) + 1

                liquidacionId = str(liquidacionId)
                liquidacionId = liquidacionId.replace("(", ' ')
                liquidacionId = liquidacionId.replace(")", ' ')
                liquidacionId = liquidacionId.replace(",", ' ')
                print ("liquidacionid = ", liquidacionId)


                # Aquip hacer los INSERT A LIQUIDACION a partir de facturacion

                comando1 = 'INSERT INTO facturacion_liquidacion (id, documento_id ,  "consecAdmision" ,  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,  "totalSuministros" ,  "totalLiquidacion" ,  "valorApagar" ,  anulado ,  "fechaCorte" ,  anticipos ,  "detalleAnulacion" ,  "fechaAnulacion" ,  observaciones ,  "fechaRegistro" ,  "estadoRegistro" ,  convenio_id ,  "tipoDoc_id" ,  "usuarioAnula_id" , "usuarioRegistro_id" ,  "totalAbonos" ,  "totalRecibido", "sedesClinica_id" ) SELECT ' + "'" + str(liquidacionId) + "'," + ' documento_id ,  "consecAdmision" ,  "fechaFactura" ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,  "totalSuministros" ,  "totalFactura" ,  "valorApagar" ,  anulado ,  "fechaCorte" ,  anticipos ,  "detalleAnulacion" ,  "fechaAnulacion" ,  observaciones ,  "fechaRegistro" ,  "estadoReg" ,  convenio_id ,  "tipoDoc_id" ,  "usuarioAnula_id" , "usuarioRegistro_id" ,  "totalAbonos" ,  "totalRecibido" , "sedesClinica_id" FROM facturacion_facturacion WHERE id =  ' + facturacionId
                print(comando1)
                cur3.execute(comando1)


                # Aquip hacer los INSERT A LIQUIDACIONDETALLE a partir de facturacion detalle

                comando2 = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo ,  fecha ,  cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  "fechaCrea" ,  "fechaModifica" ,  observaciones ,  "fechaRegistro" ,  "estadoRegistro" ,  "examen_id" ,  cums_id ,  "usuarioModifica_id" ,  "usuarioRegistro_id" ,  liquidacion_id ,  "tipoHonorario_id" ,  "tipoRegistro" , anulado, "codigoHomologado", mipres ,"autorizacionDetalle_id" , concepto_id ) SELECT "consecutivoFactura" ,  fecha ,  cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  "fechaCrea" ,  "fechaModifica" ,  observaciones ,  "fechaRegistro" , ' + "'" + str('A') + "'" + ' ,  "examen_id" ,  cums_id ,  "usuarioModifica_id" ,  "usuarioRegistro_id" , ' + "'" + str(liquidacionId) + "'" + ' ,  "tipoHonorario_id" ,  "tipoRegistro", anulado, "codigoHomologado" , mipres ,"autorizacionDetalle_id" , concepto_id  FROM facturacion_facturaciondetalle WHERE facturacion_id =  ' + facturacionId
                print(comando2)
                cur3.execute(comando2)


               ##  Aquip hacer el INSERT a la tabla facturacion_refactura


                comando3 = 'INSERT INTO facturacion_refacturacion (documento_id,"consecAdmision" ,fecha ,  "facturaAnulada" ,  "facturaNueva" ,  "fechaRegistro" ,  "estadoRegistro" ,  "tipoDoc_id" ,  "usuarioRegistro_id" , "sedesClinica_id", anulado ) values (' + str(facturacionId2.documento_id) + "," + str(facturacionId2.consecAdmision) + ","  + "'" + str(fechaRegistro) + "'," + str(facturacionId2.id) + ',0,' + "'" + str(fechaRegistro) + "'," + "'" + str('A') + "'," +  "'" + str(facturacionId2.tipoDoc_id) + "','" +  str(usuarioRegistro) + "','"+ str(facturacionId2.sedesClinica_id) + "', 'N')"
                print(comando3)
                cur3.execute(comando3)

                ## Actualiza campo salidaDefinitiva = R

                ingresoId = Ingresos.objects.get(tipoDoc_id=facturacionId2.tipoDoc_id  , documento_id= facturacionId2.documento_id , consec = facturacionId2.consecAdmision)

                comando4 = 'UPDATE admisiones_ingresos SET "salidaDefinitiva"= ' + "'" + str('R') + "'" + ' WHERE  id = ' + str(ingresoId.id)
                print(comando4)
                cur3.execute(comando4)


                comando5 = 'SELECT id id2, "valorAplicado" valorAplicado, pago_id  pagoId FROM cartera_pagosfacturas WHERE "facturaAplicada_id" = ' + "'"+ str(facturacionId)  + "'"
                print(comando5)
                cur3.execute(comando5)

                pagosFactura = []

                for id2,valorAplicado , pagoId in cur3.fetchall():
                            pagosFactura.append( {"id2": id2,"valorAplicado":valorAplicado, "pagoId" : pagoId 	 })

                            pagosFac = PagosFacturas.objects.get(facturaAplicada_id=facturacionId, pago_id=pagoId)
                            pagosFac2 = PagosFacturas.objects.filter(facturaAplicada_id = facturacionId, pago_id=pagoId).update(estadoReg='N')
                            print("ppagosFac.valorAplicado =", pagosFac.valorAplicado)

                            vale = pagosFac.valorAplicado
                            carteraPag = Pagos.objects.filter(id=pagoId).update(totalAplicado = F('totalAplicado') - float(vale))
                            carteraPag1 = Pagos.objects.filter(id=pagoId).update(saldo = F('saldo') - F('totalAplicado'))
                            carteraPag2 = Pagos.objects.filter(id=pagoId).update(valorEnCurso=float(vale))

                miConexion3.commit()
                cur3.close()
                miConexion3.close()

                datosMensaje = {'success': True, 'Mensajes': 'Factura Refacturada!'}
                json_data = json.dumps(datosMensaje, default=str)
                #return HttpResponse(json_data, content_type='application/json')

                return JsonResponse({'success': True, 'Mensajes': 'Factura Refacturada!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensajes': error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()


def GuardaApliqueAbonosFacturacion(request):

    print ("Entre ApliqueParcialAbonos" )

    liquidacionId = request.POST['liquidacionIdA']
    #tipoPago = request.POST['AtipoPago']
    #formaPago = request.POST['aformaPago']
    valor = request.POST['avalorAbono']
    valorEnCurso = request.POST['avalorEnCurso']
    saldo = request.POST['aSaldo']
    print ("liquidacionId  = ", liquidacionId )
    abonoId = request.POST["aabonoId"]
    print ("abonoId = ", abonoId)
    aformaPago = request.POST["aformaPago"]

    print("aformaPago = ", aformaPago)


    fechaRegistro = timezone.now()

    registroId = Liquidacion.objects.get(id=liquidacionId)
    print  ("registroId documento =" , registroId.documento_id)
    print  ("registroId tipoDoc =" , registroId.tipoDoc_id)
    print  ("registroId consec =" , registroId.consecAdmision)

    try:
        with transaction.atomic():

            grabo1 = Pagos.objects.filter(id=abonoId).update(valorEnCurso=valorEnCurso)


        # Aqui Crear rutina que haga la sumatoria de los valores en curso por forma de pago y luego si actualizar el valor en curso, con estas sumatorias con ORM


        # Voy a actualizar el total de Abono, o Moderadora o Anticipo


            if aformaPago == "1":
                print("Entre 1")

                sumatoriaAnticipos = Pagos.objects.filter(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consec=registroId.consecAdmision,convenio_id=registroId.convenio_id, formaPago_id=aformaPago).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalA=Coalesce(Sum('valorEnCurso'), 0))
                sumatoriaAnticipos = (sumatoriaAnticipos['totalA']) + 0
                print("sumatoriaAnticipos", sumatoriaAnticipos)
                grabo2 = Liquidacion.objects.filter(id=liquidacionId).update(anticipos=sumatoriaAnticipos)
            if aformaPago == "2":
                print("Entre 2")

                sumatoriaAbonos = Pagos.objects.filter(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consec=registroId.consecAdmision,convenio_id=registroId.convenio_id,formaPago_id=aformaPago).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalAb=Coalesce(Sum('valorEnCurso'), 0))
                sumatoriaAbonos = (sumatoriaAbonos['totalAb']) + 0
                print("sumatoriaAbonos", sumatoriaAbonos)
                grabo2 = Liquidacion.objects.filter(id=liquidacionId).update(totalAbonos=sumatoriaAbonos)

            if aformaPago == "3":
                print("Entre 3")
                sumatoriaCuotaModeradora = Pagos.objects.filter(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consec=registroId.consecAdmision,convenio_id=registroId.convenio_id,formaPago_id=aformaPago).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalM=Coalesce(Sum('valorEnCurso'), 0))
                sumatoriaCuotaModeradora = (sumatoriaCuotaModeradora['totalM']) + 0
                print("sumatoriaCuotaModeradora", sumatoriaCuotaModeradora)
                grabo2 = Liquidacion.objects.filter(id=liquidacionId).update(totalCuotaModeradora=sumatoriaCuotaModeradora)

            if aformaPago == "4":
                print ("Entre 4")

                sumatoriaCopagos = Pagos.objects.filter(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consec=registroId.consecAdmision,convenio_id=registroId.convenio_id,formaPago_id=aformaPago).exclude(estadoReg='S').exclude(anulado='S').aggregate(totalC=Coalesce(Sum('valorEnCurso'), 0))
                sumatoriaCopagos = (sumatoriaCopagos['totalC']) + 0
                print("sumatoriaCopagos", sumatoriaCopagos)
                grabo2 = Liquidacion.objects.filter(id=liquidacionId).update(totalCopagos=sumatoriaCopagos)

            grabo3 = Liquidacion.objects.filter(id=liquidacionId).update(totalRecibido= F('anticipos') + F('totalAbonos') + F('totalCuotaModeradora') + F('totalCopagos'))


            grabo4 = Liquidacion.objects.filter(id=liquidacionId).update(valorApagar  = F('totalProcedimientos') + F('totalSuministros') - F('totalRecibido'))

            return JsonResponse({'success': True, 'Mensaje': 'Aplique abono en curso guardado satisfactoriamente!'})

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)
        message_error= str(e)
        return JsonResponse({'success': False, 'Mensajes': message_error})



    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        # Falta la RUTINA que actualica los cabezotes de la liquidacion

        totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(examen_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
        totalSuministros = (totalSuministros['totalS']) + 0

        print("totalSuministros", totalSuministros)
        totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(cums_id = None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
        totalProcedimientos = (totalProcedimientos['totalP']) + 0

        print("totalProcedimientos", totalProcedimientos)

        # Si en otra pantalla estan actualizando abonos pues se veri reflejadop

        registroPago = Liquidacion.objects.get(id=liquidacionId)
        totalCopagos = registroPago.totalCopagos
        totalCuotaModeradora = registroPago.totalCuotaModeradora
        totalAnticipos = registroPago.anticipos
        totalAbonos = registroPago.totalAbonos
        #valorEnCurso = registroPago.valorEnCurso
        totalRecibido = registroPago.totalRecibido
        totalAnticipos = registroPago.anticipos
        totalLiquidacion = 0.0


        if (totalSuministros==None):
            totalSuministros=0.0
        if (totalProcedimientos==None):
            totalProcedimientos=0.0

        if (totalRecibido==None):
            totalRecibido=0.0
        if (totalLiquidacion==None):
            totalLiquidacion=0.0
        if (totalAnticipos == None):
            totalAnticipos = 0.0

        if (totalAbonos==None):
            totalAbonos=0.0

        if (totalCuotaModeradora==None):
            totalCuotaModeradora=0.0

        if (totalCopagos==None):
            totalCopagos=0.0

        totalSuministros = float(totalSuministros) + float(inicialSuministros)
        totalProcedimientos = float(totalProcedimientos) + float(inicialCups)
        totalLiquidacion = float(totalSuministros) + float(totalProcedimientos)
        print("totalSuministros FINAL", totalSuministros)
        print("totalProcedimientos FINAL", totalProcedimientos)
        print("totalLiquidacion FINAL= ", totalLiquidacion)
        print("totalRecibido FINAL= ", totalRecibido)


        valorApagar = float(totalLiquidacion) -  float(totalRecibido)


        # Rutina Guarda en cabezote los totales

        print ("Voy a grabar el cabezote")

        comando1 = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' +"'" +  + str(totalSuministros) + "'"  + ',"totalProcedimientos" = ' + "'" + + str(totalProcedimientos) + "'" + ', "totalCopagos" = ' + "'" + str(totalCopagos) + "'"  + ' , "totalCuotaModeradora" = ' + "'" + str(totalCuotaModeradora) + "'" + ', anticipos = ' + "'" +  str(totalAnticipos) + "'" + ' ,"totalAbonos" = ' + "'"  + str(totalAbonos) + "'"   + ', "totalLiquidacion" = ' + "'" + str(totalLiquidacion) + "'" + ', "valorApagar" = ' + "'" + str(valorApagar) + "'" +  ', "totalRecibido" = ' + "'" + str(totalRecibido) + + "'" +  ' WHERE id =' + str(liquidacionId)
        cur3.execute(comando1)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Registro guardado stisfactoriamente !'})


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


    ## Fin rutina actualiza cabezotes





def TrasladarConvenio(request):
    print ("Entre a Trasladar Convenio" )

    liquidacionId = request.POST['liquidacionId']
    tipoIng = request.POST['tipoIng']
    username_id =  request.POST['username_id']
    convenioId = request.POST['convenioId']
    print ("liquidacionId = ", liquidacionId)
    print ("convenioId = ", convenioId)

    convenioIdHacia = request.POST['convenioIdHacia']
    print ("convenioIdHacia = ", convenioIdHacia)


    fechaRegistro = timezone.now()
    estadoReg= 'A'

    registroId = Liquidacion.objects.get(id=liquidacionId)
    print  ("registroId documento =" , registroId.documento_id)
    print  ("registroId tipoDoc =" , registroId.tipoDoc_id)
    print  ("registroId consec =" , registroId.consecAdmision)

    ## Primero debo averiguar si existe cabezote para el nuevo convenio. So no existe se crea el cabezote

    # Busco las liquidacionesId de cada convenio

    #if (convenioId == ''):
    #    liquidacionIdDesde = Liquidacion.objects.get(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consecAdmision=registroId.consecAdmision ,convenio_id ='None')
    #else:
    liquidacionIdDesde = Liquidacion.objects.get(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consecAdmision=registroId.consecAdmision, convenio_id = convenioId)


    liquidacionIdHasta = Liquidacion.objects.get(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consecAdmision=registroId.consecAdmision, convenio_id = convenioIdHacia)

    print ("liquidacionIdDesde =", liquidacionIdDesde )
    print("liquidacionIdHasta", liquidacionIdHasta )

    print ("liquidacionIdDesde.id =", liquidacionIdDesde.id )
    print("liquidacionIdHasta.id", liquidacionIdHasta.id )


    ## Se busca de que columna se van a traer los valores


    miConexiont = None
    try:

        # Busco la columna de Procedimientos a leer la tarifa

        miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando1 = 'SELECT descrip.columna columnaProced FROM facturacion_liquidacion liq,contratacion_convenios conv,tarifarios_tarifariosdescripcion descrip where liq.id =	' + "'" + str(
            liquidacionIdHasta) + "'" + ' AND liq.convenio_id = conv.id and descrip.id = conv."tarifariosDescripcionProc_id"'
        curt.execute(comando1)
        print(comando1)

        columnaProcedimientos = []

        for columnaProced  in curt.fetchall():
                columnaProcedimientos.append( {"columnaProced": columnaProced})

        if columnaProcedimientos != []:

        	print ("columnaProcedimientos", columnaProcedimientos[0]['columnaProced'])

	        columnaProcedimientos = columnaProcedimientos[0]['columnaProced']
        	columnaProcedimientos = str(columnaProcedimientos)


	        columnaProcedimientos = columnaProcedimientos.replace("(", ' ')
        	columnaProcedimientos = columnaProcedimientos.replace(")", ' ')
	        columnaProcedimientos = columnaProcedimientos.replace(",", ' ')
        	columnaProcedimientos = columnaProcedimientos.replace("'", '')
	        columnaProcedimientos = columnaProcedimientos.replace(" ", '')
	        print("columnaProcedimientos QUEDO= ", columnaProcedimientos)

        else:

            columnaProcedimientos = "colValorBase"


        # Busco la columna de Suministros a leer la tarifa

        comando2 = 'SELECT descrip.columna columnaSuminist FROM facturacion_liquidacion liq,contratacion_convenios conv,tarifarios_tarifariosdescripcion descrip where liq.id =	' + "'" + str(liquidacionIdHasta) + "'" + ' AND liq.convenio_id = conv.id and descrip.id = conv."tarifariosDescripcionSum_id"'
        print("comando = ", comando2)

        curt.execute(comando2)

        columnaSuministros = []

        for columnaSuminist  in curt.fetchall():
                columnaSuministros.append( {"columnaSuminist": columnaSuminist})


        if columnaSuministros != []:

            print ("columnaSuministros", columnaSuministros[0]['columnaSuminist'])

            columnaSuministros = columnaSuministros[0]['columnaSuminist']
            columnaSuministros = str(columnaSuministros)


            columnaSuministros = columnaSuministros.replace("(", ' ')
            columnaSuministros = columnaSuministros.replace(")", ' ')
            columnaSuministros = columnaSuministros.replace(",", ' ')

            columnaSuministros = columnaSuministros.replace("'", '')
            columnaSuministros = columnaSuministros.replace(" ", '')

        else:
            columnaSuministros = "colValorBase"
	    

        print("columnaSuministros = ", columnaSuministros)



        ## Segundo busco los Cups desde y los envio Hasta
        #
        comando3 = 'INSERT INTO facturacion_liquidaciondetalle ( consecutivo, fecha, cantidad, "valorUnitario", "valorTotal", cirugia_id, "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro",examen_id,  "usuarioModifica_id", "usuarioRegistro_id", liquidacion_id, "tipoHonorario_id", "tipoRegistro", "historiaMedicamento_id",anulado,"codigoHomologado" , mipres ,"autorizacionDetalle_id", concepto_id ) select  det.consecutivo, liq.fecha, cantidad, proc."' + str(columnaProcedimientos) + '"' + ', proc."' + str(columnaProcedimientos) + '"' + ' * cantidad, cirugia_id, "fechaCrea", "fechaModifica", liq.observaciones, liq."fechaRegistro", liq."estadoRegistro", examen_id, "usuarioModifica_id", liq."usuarioRegistro_id",' + "'" + str(liquidacionIdHasta.id) + "'" + ' , "tipoHonorario_id",	"tipoRegistro", "historiaMedicamento_id", ' + "'" + str('N') + "'" + ', det."codigoHomologado", mipres ,"autorizacionDetalle_id", det.concepto_id  from facturacion_liquidacion liq  , facturacion_liquidaciondetalle det, contratacion_convenios conv,	  tarifarios_tarifariosdescripcion descrip, tarifarios_tipostarifa tiptar, tarifarios_tarifariosProcedimientos proc where det.liquidacion_id = liq.id and det.liquidacion_id = ' + "'" + str(liquidacionIdDesde.id) + "'" + ' and conv.id = ' + "'" + str(liquidacionIdHasta.convenio_id) + "'" + ' and det."estadoRegistro" = ' + "'" + str('A') + "'" + ' and descrip.id = conv."tarifariosDescripcionProc_id" and tiptar.id = descrip."tiposTarifa_id" and tiptar.id = proc."tiposTarifa_id" and proc."codigoCups_id" = det.examen_id'
        print("comando = ", comando3)
        curt.execute(comando3)


        ## Tercero busco los Cums desde y los envio Hasta

        comando4 = 'INSERT INTO facturacion_liquidaciondetalle ( consecutivo, fecha, cantidad, "valorUnitario", "valorTotal", cirugia_id, "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro",cums_id,  "usuarioModifica_id", "usuarioRegistro_id", liquidacion_id, "tipoHonorario_id", "tipoRegistro", "historiaMedicamento_id", anulado, "codigoHomologado", mipres ,"autorizacionDetalle_id" , concepto_id) select  det.consecutivo, liq.fecha, cantidad, sum.' + '"' + str(columnaSuministros) + '"' + ', sum."' + str(columnaSuministros) + '"'  + ' * cantidad, cirugia_id, "fechaCrea", "fechaModifica", liq.observaciones, liq."fechaRegistro", liq."estadoRegistro", cums_id, "usuarioModifica_id", liq."usuarioRegistro_id",' + "'" + str(liquidacionIdHasta.id) + "'" + ' , "tipoHonorario_id",	"tipoRegistro", "historiaMedicamento_id", ' + "'" + str('N') + "'" + ', det."codigoHomologado" , mipres,"autorizacionDetalle_id" , det.concepto_id from facturacion_liquidacion liq  , facturacion_liquidaciondetalle det, contratacion_convenios conv,	  tarifarios_tarifariosdescripcion descrip, tarifarios_tipostarifa tiptar, tarifarios_tarifariosSuministros sum where det.liquidacion_id = liq.id and det.liquidacion_id = ' + "'" + str(liquidacionIdDesde.id) + "'" + ' and conv.id = ' + "'" + str(liquidacionIdHasta.convenio_id) + "'" + ' and det."estadoRegistro" =  ' + "'" + str('A') + "'" + ' and descrip.id = conv."tarifariosDescripcionSum_id" and tiptar.id = descrip."tiposTarifa_id" and tiptar.id = sum."tiposTarifa_id" and sum."codigoCum_id" = det.cums_id'
        print("comando = ", comando4)
        curt.execute(comando4)

        # Ops fata Anular todo el detalle de la cuenta donde estaba

        comando5 = 'UPDATE facturacion_liquidaciondetalle set anulado=' + "'" + str('S') + "'," + '"fechaRegistro" = ' + "'" + str(fechaRegistro) + "' WHERE liquidacion_id = " + "'" + str(liquidacionIdDesde.id) + "'"
        print("comando = ", comando5)
        curt.execute(comando5)


        miConexiont.commit()
        curt.close()
        miConexiont.close()


        ## Faltan trasladar los Abonos sera por el apicativo abonos ??

    except psycopg2.DatabaseError as error:
        print ("Entre rollback. " , error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexiont.rollback()

        message_error=error
        print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensajes': error})

    finally:
        if miConexiont:
            curt.close()
            miConexiont.close()

    print ("Voy a grabar el cabezote")

    totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionIdHasta.id).filter(examen_id = None).exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
    totalSuministros = (totalSuministros['totalS']) + 0
    print("totalSuministros", totalSuministros)
    totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionIdHasta.id).filter(cums_id = None).exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
    totalProcedimientos = (totalProcedimientos['totalP']) + 0
    print("totalProcedimientos", totalProcedimientos)
    registroPago = Liquidacion.objects.get(id=liquidacionIdHasta.id)
    totalCopagos = registroPago.totalCopagos
    totalRecibido=0
    totalRecibido = registroPago.totalRecibido
    totalAnticipos = registroPago.anticipos


    if (totalCopagos==None):
        totalCopagos=0

    totalCuotaModeradora = registroPago.totalCuotaModeradora
    if (totalCuotaModeradora==None):
        totalCuotaModeradora=0
    totalAnticipos = registroPago.anticipos

    if (totalRecibido==None):
        totalRecibido=0

    totalAbonos = registroPago.totalAbonos
    if (totalAbonos==None):
        totalAbonoso=0

    #valorEnCurso = registroPago.valorEnCurso

    totalLiquidacion = float(totalSuministros) + float(totalProcedimientos)
    print("totalLiquidacion", totalLiquidacion)
    print("totalRecibido", totalRecibido)
    valorApagar = float(totalLiquidacion) - float(totalRecibido)


    miConexiont = None

    try:


        miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + "'" + str(
            totalSuministros) + "'" +  ',"totalProcedimientos" = ' + "'" + str(totalProcedimientos) + "'"  + ', "totalCopagos" = ' + "'" + str(
            totalCopagos) + "'" + ' , "totalCuotaModeradora" = ' + "'" + str(totalCuotaModeradora) + "'"  + ', anticipos = ' + "'" + str(
            totalAnticipos) + "'" + ' ,"totalAbonos" = ' + "'"  + str(totalAbonos) + "'" + ', "totalLiquidacion" = ' +"'" + str(
            totalLiquidacion) + "'" + ', "valorApagar" = ' + "'" + str(valorApagar) +"'" + ', "totalRecibido" = ' + "'" +  str(
            totalRecibido) + "'"  + ' WHERE id =' + str(liquidacionIdHasta.id)
        curt.execute(comando)

        comando = 'UPDATE facturacion_liquidacion SET "totalSuministros" = 0,"totalProcedimientos" =0 , "totalCopagos" = 0, "totalCuotaModeradora" = 0 ,anticipos = 0, "totalAbonos" = 0, "totalLiquidacion" = 0, "valorApagar" = 0 , "totalRecibido" = 0 WHERE id =' + str(liquidacionIdDesde.id)

        curt.execute(comando)
        miConexiont.commit()
        curt.close()
        miConexiont.close()

        # Rutina Guarda en cabezote los totales


        print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': True, 'Mensajes': 'Traslado realizado satisfactoriamente!'})


    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexiont.rollback()

        print("Voy a hacer el jsonresponde")
        message_error=str(error)
        return JsonResponse({'success': False, 'Mensajes': error})

    finally:
        if miConexiont:
            curt.close()
            miConexiont.close()


def BuscoAbono(request):
    print ("Entre a BuscoAbono" )
    abonoId = request.POST["abonoId"]

    # Combo TiposPagos

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id,c.nombre nombre FROM cartera_tiposPagos c order by c.nombre'

    curt.execute(comando)
    print(comando)

    tiposPagos = []

    # tiposPagos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposPagos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposPagos)

    # context['TiposPagos'] = tiposPagos

    # Fin combo tiposPagos

    # Combo FormasPago

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id,c.nombre nombre FROM cartera_formasPagos c order by c.nombre'

    curt.execute(comando)
    print(comando)

    formasPagos = []

    # formasPagos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        formasPagos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(formasPagos)

    # Fin combo formasPagos

    # Abro Conexion

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    cur = miConexionx.cursor()

    comando = 'select pag.id id, pag.fecha fecha, pag.consec consec, pag.valor valor , pag.descripcion descripcion, pag."estadoReg" estadoReg, pag."tipoPago_id"  tipoPago_id, pag."formaPago_id" formaPago_id,  pag.saldo saldo, pag."totalAplicado" totalAplicado, pag."valorEnCurso" valorEnCurso FROM cartera_pagos pag where pag.id = ' + "'" + str(abonoId) + "'"

    print(comando)

    cur.execute(comando)

    abonoPaciente = []

    for id, fecha , consec, valor, descripcion, estadoReg, tipoPago_id, formaPago_id, saldo, totalAplicado, valorEnCurso in cur.fetchall():
            abonoPaciente.append( {"id": id,"consec":consec, "valor" : valor, "descripcion":descripcion, "estadoReg":estadoReg, "tipoPago_id":tipoPago_id,
                     "formaPago_id": formaPago_id, "saldo": saldo, "totalAplicado": totalAplicado, "valorEnCurso":valorEnCurso
                                 })


    miConexionx.close()
    print("abonoPaciente = " , abonoPaciente)

    # Cierro Conexion    

    return JsonResponse({'pk':abonoPaciente[0]['id'],'id':abonoPaciente[0]['id'], 'consec':abonoPaciente[0]['consec'],'valor':abonoPaciente[0]['valor'],
		          'descripcion':abonoPaciente[0]['descripcion'],'estadoReg':abonoPaciente[0]['estadoReg'],'tipoPago_id':abonoPaciente[0]['tipoPago_id'],  'formaPago_id':abonoPaciente[0]['formaPago_id'],
                         'saldo': abonoPaciente[0]['saldo'], 'totalAplicado':abonoPaciente[0]['totalAplicado'] , 'valorEnCurso':abonoPaciente[0]['valorEnCurso'], 'FormasPagos':formasPagos, 'TiposPagos':tiposPagos      })



def load_dataFacturacionDetalle(request, data):
    print("Entre load_dataFacturacionDetalle")

    context = {}

    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    #valor = d['valor']
    liquidacionId = d['liquidacionId']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("liquidacionId:",liquidacionId)


    # Abro Conexion para la Liquidacion Detalle

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexionx.cursor()

    comando = 'select liq.id id,"consecutivoFactura" consecutivo ,  cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , exa.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg FROM facturacion_facturaciondetalle liq inner join clinico_examenes exa on (exa.id = liq."examen_id")  where facturacion_id= ' + "'" +  str(liquidacionId) + "'" +  ' AND (anulado=' + "'" + str('N') + "' OR anulado = 'R')" + ' UNION select liq.id id,"consecutivoFactura"  consecutivo, cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg FROM facturacion_facturaciondetalle liq inner join facturacion_suministros sum on (sum.id = liq.cums_id)  where facturacion_id= '  + "'" +  str(liquidacionId) + "' AND (anulado='N' or anulado = 'R')" + ' order by consecutivo'

    print(comando)

    cur.execute(comando)

    facturacionDetalle = []

    for id, consecutivo, fecha, cantidad, valorUnitario, valorTotal, cirugia, fechaCrea, observaciones, estadoRegistro, examen_id, cums_id, nombreExamen, liquidacion_id, tipoHonorario_id, tipoRegistro, estadoReg in cur.fetchall():
        facturacionDetalle.append(
            {"model": "facturacionDetalle.facturacionDetalle", "pk": id, "fields":
                {"id": id, "consecutivo": consecutivo,
                 "fecha": fecha,
                 "cantidad": cantidad,
                 "valorUnitario": valorUnitario, "valorTotal": valorTotal,
                 "cirugia": cirugia,
                 #"fechaCrea": fechaCrea,
                 "observaciones": observaciones,
                 "estadoRegistro": estadoRegistro, "examen_id": examen_id,
                 "cums_id": cums_id, "nombreExamen": nombreExamen,
                 "liquidacion_id": liquidacion_id, "tipoHonorario_id": tipoHonorario_id,
                 "tipoRegistro": tipoRegistro, "estadoReg":estadoReg}})

    miConexionx.close()
    print(facturacionDetalle)

    # Cierro Conexion

    serialized1 = json.dumps(facturacionDetalle, default=decimal_serializer)


    return HttpResponse(serialized1, content_type='application/json')


def load_dataReFacturacion(request, data):
    print ("Entre load_data ReFacturacion")
    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)
    flag = d['flag']
    if (flag=='FACTURACION'):
        facturacion = d['facturacionId']
        print("facturacion:", facturacion)
        facturacionId = Facturacion.objects.get(id=facturacion)
    else:
        liquidacion = d['liquidacionId']
        print("liquidacion:", liquidacion)
        liquidacionId = Liquidacion.objects.get(id=liquidacion)


    try:
        with transaction.atomic():

            if (flag == 'FACTURACION'):

                ingresoId=Ingresos.objects.get(tipoDoc_id=facturacionId.tipoDoc_id, documento_id=facturacionId.documento_id, consec=facturacionId.consecAdmision)
                ingreso=ingresoId.id
            else:
                ingresoId=Ingresos.objects.get(tipoDoc_id=liquidacionId.tipoDoc_id, documento_id=liquidacionId.documento_id, consec=liquidacionId.consecAdmision)
                ingreso=ingresoId.id



            tipoIngreso= 'INGRESO'

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por PRONO SE HACE NADA:", e)

        if (flag == 'FACTURACION'):

            triageId = Triage.objects.get(tipoDoc_id=facturacionId.tipoDoc_id, documento_id=facturacionId.documento_id,consecAdmision=facturacionId.consecAdmision)
        else:
            triageId = Triage.objects.get(tipoDoc_id=liquidacionId.tipoDoc_id, documento_id=liquidacionId.documento_id,consecAdmision=liquidacionId.consecAdmision)
            triage = triageId.id
            tipoIngreso = 'TRIAGE'

    finally:
        print("No haga nada")

    reFacturacion = []

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",     password="123456")
    curx = miConexionx.cursor()

    if (tipoIngreso=='INGRESO'):

        detalle = 'SELECT fac.id id , fac.fecha fecha,fac."facturaNueva" , fac."facturaAnulada"  , serv.nombre servicio FROM facturacion_refacturacion fac LEFT JOIN sitios_serviciosadministrativos serv  ON (serv.id= fac."serviciosAdministrativos_id") WHERE fac."tipoDoc_id" = ' + "'" + str(ingresoId.tipoDoc_id) + "' and fac.documento_id = " + "'" + str(ingresoId.documento_id) + "' AND " + ' "facturaAnulada" = ' + "'" + str(facturacion) + "'"

    else:
        print("estriage")
        triageId = Triage.objects.get(id=triage)
        pass

    print("detalle = ", detalle)

    curx.execute(detalle)

    for id ,fecha, facturaNueva, facturaAnulada, servicio in curx.fetchall():
        reFacturacion.append(
		{"model":"refacturacion.refacturacion","pk":id,"fields":
			{'id':id, 'fecha':fecha, 'facturaNueva': facturaNueva, 'facturaAnulada': facturaAnulada, 'servicio': servicio}})

    miConexionx.close()
    print(reFacturacion)


    serialized1 = json.dumps(reFacturacion, default=serialize_datetime)

    return HttpResponse(serialized1, content_type='application/json')

def GuardarRespuestaXml(request):
    print ("GuardarRespuestaXml.." )

    facturaId = request.POST["facturaId"]
    print("facturaId = ", facturaId)
    respuestaXml = request.POST["respuestaXml"]
    print("respuestaXml = ", respuestaXml)

    miConexiont = None

    try:

        miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT factura FROM facturacion_facturacion where id = ' + str(facturaId) 
        curt.execute(comando)

        for factura in  curt.fetchall():
            fac = factura
            print("fac = ", fac)

        cabezote = str(fac)
        cabezote = cabezote.replace("('", ' ')
        cabezote = cabezote.replace("',)", ' ')
        cabezote=cabezote.strip()
        print("OJOOOOO cabezote", cabezote)

        caracter_especial = "\\"
        nombre_carpeta = "C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\Facturas\\"+  str(cabezote)
        
        rutaXmlRta = nombre_carpeta + caracter_especial + str(cabezote) + '_Rpta.xml'

        print("rutaXmlRta = ", rutaXmlRta)

        comando = 'UPDATE facturacion_facturacion SET "rutaXmlRta" = ' + "'"  + str(rutaXmlRta) + "'" + ' WHERE id = ' + str(facturaId)
        curt.execute(comando)

        try:
          # 2. GUARDAR: Convertir diccionario a archivo .json
          with open(rutaXmlRta, 'w', encoding='utf-8') as archivo_escritura:
            # indent=4 lo hace legible para humanos
            json.dump(respuestaXml, archivo_escritura, indent=4, ensure_ascii=False)

          # --- En este punto el archivo ya existe en tu disco ---

          # 3. CARGAR: Leer el archivo recién guardado a una variable
          #with open(nombre_archivo, 'r', encoding='utf-8') as archivo_lectura:
          #  datos_cargados = json.load(archivo_lectura)

          # 4. ENVIAR: Retornar los datos cargados mediante JsonResponse
          # return JsonResponse(datos_cargados, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


        miConexiont.commit()
        curt.close()
        miConexiont.close()

        print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': True, 'Mensajes': 'Respuesta XMl guardada satisfactoriamente!'})


    except psycopg2.DatabaseError as error:
        print("Entre por rollback", error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexiont.rollback()

        print("Voy a hacer el jsonresponde")
        message_error=str(error)
        return JsonResponse({'success': False, 'Mensajes': error})

    finally:
        if miConexiont:
            curt.close()
            miConexiont.close()

def LeerJson(request):
    print ("Entre a LeerJson.." )

    facturaId = request.POST["facturaId"]
    print("facturaId = ", facturaId)

    # Abro Conexion

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    curx = miConexionx.cursor()
    print("Aqui voy")

    comando = 'SELECT "rutaJson" , "rutaXml", "rutaXmlRta" FROM facturacion_facturacion WHERE id = ' + str(facturaId)

    print(comando)
    curx.execute(comando)

    for rutaJson, rutaXml, rutaXmlRta in curx.fetchall():

      print("rutaJson=", rutaJson)
      print("rutaXml=", rutaXml)
      print("rutaXmlRta=", rutaXmlRta)


      try:
        # 2. Abrir y leer el archivo
        with open(rutaJson, 'r', encoding='utf-8') as archivo:
            # 3. Cargar el contenido en una variable (diccionario)
            contenido_Json = json.load(archivo)
            
        # 4. Retornar la variable usando JsonResponse
        # return JsonResponse(contenido_Json, safe=False)
        
      except FileNotFoundError:
        print ("El archivo JSON no existe")

      except json.JSONDecodeError:
        print ("Error al decodificar el JSON")


      try:
        # 2. Abrir y leer el archivo
        with open(rutaXml, 'r', encoding='utf-8') as archivo:
            # 3. Cargar el contenido en una variable (diccionario)
            print("Voy a leer XML")
            xml_content = archivo.read()
            print("Voy a leer XML_listo")
            #contenido_Xml = json.load(archivo)
            data_Xml = {
               'status': 'success',
               'filename': rutaXml,
                'content': xml_content  # El contenido XML enviado como texto
                  }

            
        # 4. Retornar la variable usando JsonResponse
        # return JsonResponse(contenido_json, safe=False)
        
      except FileNotFoundError:
        print ("El archivo XML no existe")

      except json.JSONDecodeError:
        print ("Error al decodificar el XML")


      try:
        # 2. Abrir y leer el archivo
        with open(rutaXmlRta, 'r', encoding='utf-8') as archivo:
            # 3. Cargar el contenido en una variable (diccionario)
            print("Voy a leer XML")
            xml_content = archivo.read()
            print("Voy a leer XML_listo")

            #contenido_XmlRta = json.load(archivo)
            #
            data_XmlRta = {
               'status': 'success',
               'filename': rutaXmlRta,
                'content': xml_content  # El contenido XML enviado como texto
                  }
      
        
      except FileNotFoundError:
        print ("El archivo XML no existe")

      except json.JSONDecodeError:
        print ("Error al decodificar el RTA XML")



    #comando = 'UPDATE facturacion_facturacion SET "rutaXmlRta" = ' + "'" + str() + "'" + ' WHERE id = ' + str(facturaId)
    #print(comando)
    #curx.execute(comando)

    #miConexionx.commit()
    miConexionx.close()

    return JsonResponse({'success': True, 'Mensajes': 'Factura JSON Xml enviado Respuesta Xml !', 'contenido_Json':contenido_Json, 'contenido_Xml':data_Xml, 'contenido_XmlRta':data_XmlRta} )



def EnvioDian(request):
    print ("Entre a EnvioDyan" )

    facturaId = request.POST["facturaDianId"]
    print("facturaId = ", facturaId)

    # Abro Conexion

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    curx = miConexionx.cursor()

    comando = 'SELECT fac.id, fac."fechaEnvioDian" , fac."fechaRespuestaDian" , fac."respuestaDian", dian.nombre estadoEnvioDian FROM facturacion_facturacion fac LEFT JOIN  facturacion_estadoEnvioDian dian   ON (dian.id=fac."estadoEnvioDian_id")  WHERE fac.id = ' + "'" + str(facturaId) + "'"

    print(comando)

    curx.execute(comando)

    envioDian = []	

    for id ,fechaEnvioDian, fechaRespuestaDian, respuestaDian, estadoEnvioDian in curx.fetchall():
        envioDian.append(
		{"model":"refacturacion.refacturacion","pk":id,"fields":
			{'id':id, 'fechaEnvioDian':fechaEnvioDian, 'fechaRespuestaDian': fechaRespuestaDian, 'respuestaDian': respuestaDian,'estadoEnvioDian':estadoEnvioDian}})


    miConexionx.close()

    serialized1 = json.dumps(envioDian, default=str)

    return HttpResponse(serialized1, content_type='application/json')



def CrearEnvioDian(request):
    print ("Entre a CrearEnvioDian" )

    facturaId = request.POST["facturaDianId"]
    print("facturaId = ", facturaId)

    fechaEnvioDian = request.POST["fechaEnvioDian"]
    print("fechaEnvioDian = ", fechaEnvioDian)

    fechaRespuestaDian = request.POST["fechaRespuestaDian"]
    print("fechaRespuestaDian = ", fechaRespuestaDian)

    if (fechaRespuestaDian ==''):
	    fechaRespuestaDian='null'

    respuestaDian = request.POST["respuestaDian"]
    print("respuestaDian = ", respuestaDian)

    if (respuestaDian ==''):
	    respuestaDian='null'


    estadoEnvioDian = request.POST["estadoEnvioDian"]
    print("estadoEnvioDian = ", estadoEnvioDian)

    # Abro Conexion

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    curx = miConexionx.cursor()

    comando = 'UPDATE facturacion_facturacion SET "fechaEnvioDian" = ' + "'" + str(fechaEnvioDian) + "'," + '"fechaRespuestaDian" = ' + str(fechaRespuestaDian) + "," + ' "respuestaDian" = ' + "'" + str(respuestaDian) + "'," + '"estadoEnvioDian_id" = ' + "'" + str(estadoEnvioDian) + "'" + ' WHERE id = ' + "'" + str(facturaId) + "'"

    print(comando)

    curx.execute(comando)
    miConexionx.commit()

    miConexionx.close()


    return JsonResponse({'success': True, 'Mensajes': 'Factura Actualizada !'})


class EnviarFacturaDianView(APIView):
    def post(self, request):
        
       # Forzar la salida de errores ocultos de red a la consola
      logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
      logging.getLogger('zeep').setLevel(logging.DEBUG)

      history = HistoryPlugin()


      # Configura los logs para que muestren la comunicación de zeep y requests
      #logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
      #logging.getLogger('zeep.client').setLevel(logging.DEBUG)
      #logging.getLogger('zeep.transports').setLevel(logging.DEBUG)

      
      factura = request.POST["facturaDianId"]
      print ("Entre Envio Dian" , factura)

      factura =  Facturacion.objects.get(id=factura)
      rutaXml=factura.rutaXml
      print ("rutaXml" , rutaXml)
      rutaXmlFirmado=factura.rutaXmlFirmado
      print ("rutaXmlFirmado" , rutaXmlFirmado)

      try:
        # 2. Abrir y leer el archivo
        #with open(rutaXml, 'r', encoding='utf-8') as archivo:
        with open(rutaXml, 'rb') as archivo:
            # 3. Cargar el contenido en una variable (diccionario)
            print("Voy a leer XML")
            xml_bytes = archivo.read()
          
            data_Xml = {
               'status': 'success',
               'filename': rutaXml,
                'content': xml_bytes  # El contenido XML enviado como texto
                  }
        
      except FileNotFoundError:
        print ("El archivo XML no existe")

      except json.JSONDecodeError:
        print ("Error al decodificar el XML")
        
      # 2. CONSUMIR EL WEB SERVICE SOAP DE LA DIAN, Pruebas
      wsdl_url = "https://vpfe-hab.dian.gov.co/WcfDianCustomerServices.svc?wsdl"

      # Credenciales de Software propio (proporcionadas por la DIAN)
      usuario = "8093266e-a39a-4080-8be7-af9588db3add" # Ej: Nit + ID de software
      password = "75AAbb??cc"
      
      #print("xml_bytes = ", xml_bytes)
      print(" Este es el web Service")
        
      try:
            #client = zeep.Client(wsdl=wsdl_url)
            # 1. Configurar cliente y seguridad
            #client = Client(wsdl=wsdl_url, wsse=UsernameToken(usuario, password) )
            #client = Client(wsdl=wsdl_url, wsse=UsernameToken(usuario, password)  ,               plugins=[WsseTimestampPlugin()]) #, use_digest=False

            # Configura el token con use_digest (por defecto es False)
            token = UsernameToken(usuario, password, use_digest=False)


            #client = Client(wsdl=wsdl_url, wsse=UsernameToken(usuario, password ),  use_digest=False  ) 
            client = Client(wsdl=wsdl_url, wsse=token  ) 
            print ("Pase Cliente ", client)


            test_set_id = "62edb572-e4b6-42dd-a896-f4765e4ee8bb"

            # Construcción de los Headers HTTP
            header_value = {
                    'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': 'SendTestSetAsync',  # Acción del Web Service de la DIAN
                    'TestSetId': test_set_id          # Encabezado donde se incluye el TestSetId
            }

            # 2. Construir los encabezados (Headers) HTTP/SOAP donde va el TestSetId
            print ("Ya cargue los headers")

            ##  ojo aqui falta la rutina python de envio de documento firmado
            ############################################################################################

            #################################################################################
            #Firma un archivo XML para la Facturación Electrónica de la DIAN.

            XML_ORIGINAL = factura.rutaXml
            XML_FIRMADO  = factura.rutaXmlFirmado
            CERTIFICADO_PEM = "c:\\DIAN\\certificado.pem"
            CONTRASENA_PEM = "PEJKIkz8BRVURFOf" # Dejar en None si tu .pem no está cifrado

            #Proceso completo de firmado XAdES / XMLDSig para la DIAN
 
            # Cargar llaves desde el .pem
            private_key, certificate, cert_raw = cargar_credenciales_pem(CERTIFICADO_PEM, CONTRASENA_PEM)
    
            print("ya cargue el private key")
            # Leer y parsear el archivo XML original de la factura
            parser = etree.XMLParser(remove_blank_text=True)
            roota = etree.parse(XML_ORIGINAL, parser).getroot()
            print("Cargue el XML original")

            # Configurar el firmador siguiendo las reglas obligatorias de la DIAN:
            # - Algoritmo de firma: Enveloped (la firma reside dentro del propio documento)
            # - Algoritmo de Hash: SHA-256


            # 2. Initialize your signer

            signer = XMLSigner()

            # 3. If you want to force the default namespace to be 'ds', use the imported module
            # Note: Use 'namespaces' (not 'methods')

            signer.namespaces = {None: "http://w3.org"}

            # Load data and key
            root = etree.fromstring("<Root><Foo/></Root>")

            with open("c:\\DIAN\\llave_privada.pem", "rb") as f:
                key = f.read()

            print ("pase lectura llave primaria")

            # Sign the document
            signed_root = signer.sign(root, key=key)


            print("pase signer")
    
            # Generar la estructura <Signature> firmada
            # El parámetro 'cert' incrusta automáticamente el certificado público en <X509Data>
            signed_node = signer.sign(
                   roota,
                   key=private_key,
                   cert=cert_raw
            )
    
            print("pase signer_node")

            # Nota DIAN: La normativa exige que la firma se ubique de manera exacta dentro 
            # de las extensiones UBL de la factura: /Invoice/ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent
            namespaces = {
                    'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2'
            }
    
            # Buscar el nodo contenedor de la firma destinado en tu plantilla XML
            # Comúnmente es la segunda o última extensión UBL
            print("paso_1")
            extension_content = roota.xpath('//ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent', namespaces=namespaces)
            print("paso_2")

            if extension_content:
               # Insertamos el nodo firmado (<Signature>) en el contenedor del XML
               extension_content[-1].append(signed_node)
            else:
               # Caída de respaldo si el XML no viene estructurado con estándares UBL
               roota.append(signed_node)
               print("Advertencia: No se encontró la etiqueta ext:ExtensionContent. Se adjuntó al final de la raíz.")
            print("paso_3")
            # Guardar el archivo XML firmado e incrustado
            tree = etree.ElementTree(roota)
            print("paso_4",XML_FIRMADO)
            tree.write(XML_FIRMADO, pretty_print=True, xml_declaration=True, encoding="UTF-8")
            print ("XML_FIRMADO = " ,XML_FIRMADO )
            print(f"✅ Proceso exitoso. Archivo firmado guardado en: {XML_FIRMADO}")


            ########### FIN Firma un archivo XML para la facturacion Electronica de la DIAN
            #################################################################################

            print(" Este es el web Service_01")            
            # Estructura del payload según el método SendBillAsync de la DIAN
            ## Despues de que se firma el archivo ahi si se convierte a base64
            #archivo_base64 = base64.b64encode(XML_FIRMADO).decode('utf-8')

            archivo_base64 = base64.b64decode(XML_FIRMADO)
  

            print(" Este es el web Service_02")    
            # 3. Preparar los datos que exige el método 'SendBillSync' de la DIAN
            datos_envio = {
                 #"fileName": "fv_SETG_980000002.xml", # El nombre debe coincidir con el XML
                 "fileName": "SETG980000002.xml", # El nombre debe coincidir con el XML
                 "contentFile": archivo_base64  # xml_firmado_bytes
            }

            print ("pase archivo_base64")
            print(" Envio Documento : ", archivo_base64)
            #response = client.service.SendBillAsync(
            #    fileName="doc_firmado.xml",
            #    contentFile=archivo_base64
            #)

            print ("header_value =  ", header_value)

            # 1. Define la estructura del elemento con su Namespace
            header_element = xsd.Element(
                  '{http://oasis-open.org}Security',
                  xsd.ComplexType([
                  xsd.Element('UsernameToken', xsd.ComplexType([
                  xsd.Element('Username', xsd.String()),
                  xsd.Element('Password', xsd.String()),
                                ]))
                          ])
            )

            #timestamp_token = Timestamp()
            print("Nuevo desarrollo_01")
            timestamp_token = WSU.Timestamp()
            #today_datetime = datetime.datetime.today()
            today_datetime = dt.datetime.today()
            #expires_datetime = today_datetime + datetime.timedelta(minutes=10)
            expires_datetime = today_datetime + dt.timedelta(minutes=10)
            print("Nuevo desarrollo_02")

            timestamp_elements = [
                        WSU.Created(today_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")),
                        WSU.Expires(expires_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
            ]

            timestamp_token.extend(timestamp_elements)
            print("Nuevo desarrollo_03", )

            # 2. INSTANCIA el elemento con los datos reales
            header_value = header_element(
                      UsernameToken={
                         'Username': usuario,                       
                         'Password': password 	
                                   }
            )


            ################ ojo esto es el ZIP  
            print ("Voy a zipiar")

            # Reemplazar "Java" por "Python"

            rutaArchivoZip = factura.rutaXml.replace(".xml",".zip")
            print("rutaArchivoZip =", rutaArchivoZip)

            #with zipfile.ZipFile('archivo_final.zip', 'w' , zipfile.ZIP_DEFLATED) as csv_zip:
            with zipfile.ZipFile(rutaArchivoZip, 'w' , zipfile.ZIP_DEFLATED) as csv_zip:
               csv_zip.write(rutaXmlFirmado, arcname=rutaXmlFirmado)


            # 1. Crear el archivo ZIP
            #with zipfile.ZipFile("factura.zip", "w") as z:
            #     z.write(datos_envio['contentFile'])
            print ("Voy a leer zip")
            # 2. Leer el ZIP como bytes binarios
            #with open("factura.zip", "rb") as f:
            with open(rutaArchivoZip, "rb") as f:
                zip_bytes = f.read()  # Arreglo de bytes puro
            print ("Voy a ENVIAR zip")

            # 3. Enviar al webservice
            #response = client.service.SendTestSetAsync(
            #      #fileName="factura.zip", contentFile=zip_bytes, testSetId=test_set_id
            #      fileName=rutaArchivoZip, contentFile=zip_bytes, testSetId=test_set_id
            #)

            ##################  FIN zip

            # 3. Pásalo OBLIGATORIAMENTE dentro de una lista []
            #response = await client.service.SendTestSetAsync(

            print("Aqui voy con datatime = ")
            print("Aqui voy con datatime = ", dt.datetime.now())

            print("Voy a contactar client.service.SendTestSetAsync ...",rutaArchivoZip )

            response = client.service.SendTestSetAsync(
                testSetId=test_set_id,
                fileName=rutaArchivoZip,
                contentFile=zip_bytes
                #_soapheaders=[header_value] # Debe ser una lista
            )
            print("Acabo de contactar client.service.SendTestSetAsync ...")

            #response = client.service.SendTestSetAsync(
            #     fileName=datos_envio['fileName'],
            #     contentFile=datos_envio['contentFile'],
            #     _soapheaders= soap_headers  #[header_value]
            #)

            print ("Aquip ya lo envio a la DIAN DIAN DIAN ")
            print("Abajo esta repetido")

            #return Response({
            #    "mensaje": "Factura enviada a la DIAN exitosamente",
            #    "respuesta_dian": response
            #}, status=status.HTTP_200_OK)

      except Exception as e:

            print("\n❌ --- ERROR CAPTURADO EN EXCEPT --- ❌")
            print(f"Tipo de error: {type(e).__name__}")
            print(f"Mensaje del error: {e}\n")
            print("=== RASTREO DETALLADO DE LA LÍNEA DEL FALLO (TRACEBACK) ===")
            traceback.print_exc(file=sys.stdout)


            #print(" Ops Entre con error de la DIAN = ", str(e))
            #return Response({
            #    "error": "Error al conectar con la DIAN",
            #    "detalles": str(e)
            #}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


      finally:
           print("\n=== TRASPASO DE TRÁFICO XML ===")
           # Forma segura de verificar si la cola de zeep contiene datos antes de acceder a ella
           try:
              if history.last_sent is not None:
                  print("XML Enviado detectado correctamente.")
           except IndexError:
                  print("Aviso: No se envió ninguna trama XML. La conexión se cerró antes de armar el mensaje.")
        
           try:
              if history.last_received is not None:
                 print("XML Recibido detectado correctamente.")
           except IndexError:
                 print("Aviso: No se recibió respuesta XML del servidor.")




def cargar_credenciales_pem(pem_path, password=None):

    #Carga la llave privada y el certificado público desde el archivo .pem

    print ("Entre function cargar credenciales pem = " , pem_path)
    print ("Entre function cargar credenciales pem = ", password)
    llave_privada = "C:\\DIAN\llave_privada.pem"
    with open(llave_privada, "rb") as f:
        llave_privada_pem = f.read()


    with open(pem_path, "rb") as f:
        pem_data = f.read()

    decoded_data = base64.b64decode(pem_data)
    
    # 1. Extraer la llave privada
    # Si el archivo tiene contraseña, cámbiala en el parámetro 'password' (en bytes)
    password_bytes = password.encode() if password else None
    print("decoded_data = " , decoded_data)
    print("password_bytes = " , password_bytes)

    private_key = serialization.load_pem_private_key(
        llave_privada_pem,
        password=None # password_bytes
    )

    print("pase private_key")
    print("private_key = " ,  private_key) 
   
    # 2. Extraer el certificado público
    # Busca la sección del certificado dentro del mismo archivo .pem
    cert_start = pem_data.find(b"-----BEGIN CERTIFICATE-----")

    cert_data = pem_data[cert_start:]
    print("cert_data = " ,  cert_data) 
    certificate = x509.load_pem_x509_certificate(cert_data)
    
    return private_key, certificate, cert_data