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
from django.http \
import JsonResponse
#import MySQLdb
import pyodbc
import psycopg2
import json 
import datetime
from django.utils import timezone
from decimal import Decimal
from admisiones.models import Ingresos
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle, Refacturacion
from cartera.models import TiposPagos, FormasPagos, Pagos, PagosFacturas
from triage.models import Triage
from clinico.models import Servicios
import pickle
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.db.models import F
from cirugia.models import EstadosCirugias, EstadosProgramacion, Cirugias
from django.db.models import F
from sitios.models import ServiciosSedes
from contratacion.models import Convenios
import os

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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",     password="123456")
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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")

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


                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",       user="postgres", password="123456")
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

        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",password="123456")
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

        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexionx.cursor()

    comando = 'select liq.id id,consecutivo ,  cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" , hono.nombre tipoHonorario, cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , exa.nombre||' + "' '||" + ' "codigoCups"  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg, liq.anulado anulado   FROM facturacion_liquidaciondetalle liq LEFT JOIN tarifarios_tiposhonorarios hono ON (hono.id = liq."tipoHonorario_id") inner join clinico_examenes exa on (exa.id = liq."examen_id")  where liquidacion_id= ' + "'" +  str(liquidacionId) + "'" +  ' UNION select liq.id id,consecutivo , cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" , hono.nombre tipoHonorario,  cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre||' + "' '||" + 'cums  nombreExamen  ,  liquidacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg , liq.anulado anulado FROM facturacion_liquidaciondetalle liq LEFT JOIN tarifarios_tiposhonorarios hono ON (hono.id = liq."tipoHonorario_id")  inner join facturacion_suministros sum on (sum.id = liq.cums_id)  where liquidacion_id= '  + "'" +  str(liquidacionId) + "'" + ' AND "estadoRegistro"= ' +"'" + str('A') + "'" + ' ORDER BY consecutivo'

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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

            miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            cur3 = miConexion3.cursor()
            comando = 'insert into cartera_Pagos ("fecha", "tipoDoc_id" , documento_id, consec,  "tipoPago_id" , "formaPago_id", valor, descripcion ,"fechaRegistro","estadoReg", saldo, "totalAplicado", "valorEnCurso") values ('  + "'" + str(fechaRegistro) + "'," +  "'" + str(registroId.tipoDoc_id) + "'" + ' , ' + "'" + str(registroId.documento_id) + "'" + ', ' + "'" + str(registroId.consecAdmision) + "'" + '  , ' + "'" + str(tipoPago) + "'" + '  , ' + "'" + str(formaPago) + "'" + ', ' + "'" + str(valor) + "',"   + "'" + str(descripcion) + "','"   + str(fechaRegistro) + "'," + "'" +  str("A") +  "','" + str(valor) + "',0,0);"
            print(comando)
            cur3.execute(comando)
            miConexion3.commit()
            miConexion3.close()


            # Actualizo el total recibido

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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



        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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
    cups = request.POST["cups"]
    suministros = request.POST["suministros"]
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

    if cups == '':
           cups="null"
           inicialSuministros =  valorTotal

    if suministros == '':
           suministros="null"
           inicialCups = valorTotal

 

    fechaRegistro = timezone.now()

    registroId = Liquidacion.objects.get(id=liquidacionId)
    print  ("registroId documento =" , registroId.documento_id)
    print  ("registroId tipoDoc =" , registroId.tipoDoc_id)
    print  ("registroId consec =" , registroId.consecAdmision)

    # Aqui RUTINA busca consecutivo de liquidacion


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",        password="123456")
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

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia_id,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id", cums_id,  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", observaciones, anulado) VALUES (' + "'" +  str(consecLiquidacion)  + "','" + str(fechaRegistro) + "','" + str(cantidad) + "','"  + str(valorUnitario) + "','" + str(valorTotal)  + "',null" + ",'" +  str(fechaRegistro) + "','" +  str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(cups) + "," + str(suministros) +   ",'"  + str(username_id) + "'," + liquidacionId + ",'MANUAL'," + "'"  + str(observaciones) + "','N')"
        print(comando)
        cur3.execute(comando)

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

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

    if suministros == '':
           suministros="null"

    fechaRegistro = timezone.now()

    registroId = LiquidacionDetalle.objects.get(id=liquidacionDetalleId)
    print  ("liquiacion_id =" , registroId.liquidacion_id)

    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()
        #comando = 'insert into facturacion_liquidacionDetalle ("fecha", "tipoDoc_id" , documento_id, consec,  "tipoPago_id" , "formaPago_id", valor, descripcion ,"fechaRegistro","estadoReg") values ('  + "'" + str(fechaRegistro) + "'," +  "'" + str(registroId.tipoDoc_id) + "'" + ' , ' + "'" + str(registroId.documento_id) + "'" + ', ' + "'" + str(registroId.consec) + "'" + '  , ' + "'" + str(tipoPago) + "'" + '  , ' + "'" + str(formaPago) + "'" + ', ' + "'" + str(valor) + "',"   + "'" + str(descripcion) + "','"   + str(fechaRegistro) + "'," + "'" +  str("A") + "');"
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

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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
    print("convenio de la liquidacion = " , liquidacionDatos.convenio_id);

    facturaConvenio = liquidacionDatos.convenio_id

    if (tipoFactura == 'REFACTURA'):

        facturaAnula = Refacturacion.objects.get(tipoDoc_id=liquidacionDatos.tipoDoc_id, documento_id=liquidacionDatos.documento_id,consecAdmision=liquidacionDatos.consecAdmision)
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
            return JsonResponse({'success': False, 'message': 'Favor ingresar Convenio a Facturar !', 'Factura' : 0 })

     # OPS PAILAS SI LO QUE VA A FACTURAR ES UN TRIAGE

    flag=''

    if	(liquidacionDatos.consecAdmision == 0 ): #Es triage

	    triageId = Triage.objects.get(tipoDoc_id=liquidacionDatos.tipoDoc_id , documento_id=liquidacionDatos.documento_id ,consec=liquidacionDatos.consecAdmision)
	    print ("triageId = ", triageId.id)
	    flag='TRIAGE'
	    return JsonResponse({'success': False, 'Mensaje': 'No es posible facturar cuenta Triage. Favor hospitalizar o a cama de Urgencias!'})

    else:
	    ingresoId = Ingresos.objects.get(tipoDoc_id=liquidacionDatos.tipoDoc_id , documento_id=liquidacionDatos.documento_id ,consec=liquidacionDatos.consecAdmision)
	    print ("ingresoId = ", ingresoId.id)
	    flag='INGRESO'
	    servicioSedeAmb = ServiciosSedes.objects.get(sedesClinica_id=sede, id=ingresoId.serviciosActual_id)
	    servicioAmb = Servicios.objects.get(nombre='AMBULATORIO')
	    if (servicioSedeAmb.servicios_id==servicioAmb.id):
        	flag='AMBULATORIO'


    print ("IngresoId", ingresoId.id)
    print("falg" ,flag)

    if (flag=='INGRESO'):
        print("flag2", flag)
        if (ingresoId.salidaClinica=='N' and servicioSedeAmb.servicios_id != servicioAmb.id  ):
            print("flag3", flag)
            return JsonResponse({'success': False, 'Mensajes': 'Paciente NO tiene Salida Clinica. Consultar medico tratante !', 'Factura' : 0 })

    # AQUI VALDAR SI HAY CIRUGIAS QUE NO ESTEN REALIZADAS  ## OPS ESTO SI HAY QUE REVIZARLO
 
    print ( "Evaluo cirugia"   )
    estadoCirugiaRealizada = EstadosCirugias.objects.get(nombre='REALIZADA')
    estadoCirugiaFacturada = EstadosCirugias.objects.get(nombre='FACTURADA')
    estadoProgramacionRealizada = EstadosProgramacion.objects.get(nombre='Realizada')

    try:
        with transaction.atomic():

            totalCirugias = Cirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision, estadoCirugia_id= estadoCirugiaRealizada.id).count()
            print ( "total cirugias", totalCirugias   )

            if (cirugias >=1):
                Cirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision , estadoCirugia_id= estadoCirugiaRealizada.id).update(estadoCirugia_id=estadoCirugiaFacturada.id)
                Programacioncirugias.objects.filter(tipoDoc_id=usuarioId.tipoDoc_id , documento_id=usuarioId.documento_id ,consec=usuarioId.consecAdmision , estadoCirugia_id= estadoCirugiaRealizada.id).update(estadoProgramacion_id=estadoProgramacionRealizada.id)

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por PRONO SE HACE NADA:", e)

    finally:
        print("No haga nada")

    ## RUTINA ACTUALIZA DX, SERV ,
    print ( "pase cirugia"   )
    miConexion3 = None
    try:
        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",   password="123456")
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

        comando32 = 'update facturacion_facturacion set "valorAPagarLetras" = obtienevlrletras(cast("totalFactura" as integer)) ,  "cufeDefinitivo" = ' + "'" + str('6b7dd1910792ec82b16f5a30d83da5c8f10895b42e3a685a8ee0f0edfc9e32e087576ba23525a50091a6eeb5bd9a9c5e') + "'," + '"codigoQr" =' + "'" + str('C:/EntornosPython/Pos7Particionado/vulner/JSONCLINICA/CodigosQr/Factura_1.png')  + "'" + ' WHERE id = ' +"'" + str(facturacionId) + "'"
        cur3.execute(comando32)

        print ("facturacionId = ", facturacionId)

        # AHORA EL DETALLE

        comando5 = 'INSERT INTO facturacion_facturaciondetalle ("consecutivoFactura", fecha, cantidad, "valorUnitario", "valorTotal",  cirugia_id , "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro", "examen_id", cums_id, "usuarioModifica_id", "usuarioRegistro_id", facturacion_id, "tipoHonorario_id", "tipoRegistro", anulado, "historiaMedicamento_id","codigoHomologado") SELECT  consecutivo, fecha, cantidad, "valorUnitario", "valorTotal",  cirugia_id , "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro", "examen_id", cums_id, "usuarioModifica_id", "usuarioRegistro_id", ' + str(facturacionId) + ', "tipoHonorario_id", "tipoRegistro", anulado , "historiaMedicamento_id", "codigoHomologado"  FROM facturacion_liquidaciondetalle WHERE liquidacion_id =  ' + liquidacionId + ' AND anulado != ' + "'" + str('S') + "'"
        print(comando5)
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


        miConexion3.commit()


	# Aqui creo el registro en cartera

        print("aui voy")
        facturaFisica = Facturacion.objects.get(id=facturacionId)
        convenioFisico = Convenios.objects.get(id=facturaFisica.convenio_id)
        print("aui pase")

        comando11 = 'INSERT INTO cartera_cartera (pagos,saldo,valor,  "fechaRegistro","estadoReg", factura_id, "sedesClinica_id", empresa_id) VALUES ( 0 , ' +  str(facturaFisica.totalFactura) + "," + str(facturaFisica.totalFactura) + ",'" + str(fechaRegistro) + "','A'," + str(facturacionId) + ",'" + str(sede) + "'," + str(convenioFisico.empresa_id) + ")"
        print(comando11)
        cur3.execute(comando11)


        miConexion3.commit()


        cur3.close()
        miConexion3.close()

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

            miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

            miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",     password="123456")
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    cur = miConexionx.cursor()

    comando = 'select fac.id id, fac.id factura, fac."fechaFactura" fechaFactura, tip.nombre tipoDoc, usu.documento documento, usu.nombre paciente, fac."consecAdmision" consecAdmision, conv.nombre nombreConvenio,  "totalSuministros","totalProcedimientos","totalCopagos","totalCuotaModeradora","totalAbonos","totalRecibido", anticipos totalAnticipos,"valorApagar","totalFactura" , "valorAPagarLetras" , fac."estadoReg" estadoReg, fac.anulado anulado, "rutaXml" rutaXml, "rutaJson" rutaJson, "rutaPdf" rutaPdf  FROM facturacion_facturacion fac, contratacion_convenios conv, usuarios_usuarios usu, usuarios_tiposdocumento tip where fac.id = ' + "'" + str(Post_id) + "'" + '  AND  fac.convenio_id = conv.id and usu.id = fac.documento_id  and fac."tipoDoc_id" = usu."tipoDoc_id"   AND tip.id = fac."tipoDoc_id" AND fac.documento_id = usu.id  AND conv.id = fac.convenio_id '

    print(comando)

    cur.execute(comando)

    facturacion = []

    for id,factura , fechaFactura , tipoDoc, documento, paciente, consecAdmision , nombreConvenio , totalSuministros,totalProcedimientos,totalCopagos,totalCuotaModeradora,totalAbonos,totalRecibido,totalAnticipos,valorApagar,totalFactura , valorAPagarLetras , estadoReg, anulado, rutaXml, rutaJson, rutaPdf  in cur.fetchall():
            facturacion.append( {"id": id,"factura":factura, "fechaFactura" : fechaFactura, "tipoDoc":tipoDoc, "documento":documento,
                     "paciente": paciente, "consecAdmision": consecAdmision, "nombreConvenio": nombreConvenio,'totalSuministros':totalSuministros,'totalProcedimientos':totalProcedimientos,'totalCopagos':totalCopagos,'totalCuotaModeradora':totalCuotaModeradora,'totalAbonos':totalAbonos,'totalRecibido':totalRecibido,'totalAnticipos':totalAnticipos,'valorApagar':valorApagar,'totalFactura':totalFactura, 'valorAPagarLetras':valorAPagarLetras,
                                 'estadoReg':estadoReg, 'anulado':anulado, 'rutaXml':rutaXml,'rutaPdf':rutaPdf, 'rutaJson':rutaJson
                                 })
            rutaXml = rutaXml
            rutaJson = rutaJson
            rutaPdf = rutaPdf




    miConexionx.close()
    print(facturacion)

    # Cierro Conexion

    #Extraigo la info del xml
    contenido_completo=''
    contenido_completoJson = ''
    print ("rutaXml")


    if (rutaXml == None):
        rutaXml = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\Facturas\\XML\\Factura_' + str(Post_id) + '.xml'

    if (rutaJson == None):
        rutaJson = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\Facturas\\JSON\\Factura_' + str(Post_id) + '.xml'

    print("rutaXml", rutaXml)
    print("rutaJson", rutaJson)

    #if os.path.exists(rutaXml):
    if os.path.exists(rutaJson):

        try:
            # Abre el archivo en modo lectura ('r') con codificación UTF-8
            with open(rutaJson, 'r', encoding='utf-8') as archivo:
                contenido_completoJson = archivo.read()
                print("Contenido completo del archivo:")
                print(contenido_completoJson)

            with open(rutaXml, 'r', encoding='utf-8') as archivo:
                contenido_completo = archivo.read()
                print("Contenido completo del archivo:")
                print(contenido_completo)



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
                         'estadoReg': facturacion[0]['estadoReg'], 'anulado': facturacion[0]['anulado'], 'Xml': contenido_completo , 'Json': contenido_completoJson
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

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE facturacion_facturacion SET "estadoReg" = ' + "'" + str('I') + "'" + ', anulado = ' + "'" + str('S') + "', " + '"fechaAnulacion" =   '  + "'" + str(fechaRegistro) + "'," + '"usuarioAnula_id" = ' + "'" + str(username_id) + "'"  + ' WHERE id =  ' + str(facturacionId )
        print(comando)
        cur3.execute(comando)


        comando1 = 'UPDATE facturacion_facturaciondetalle SET "estadoRegistro" = ' + "'" + str('I') + "'" + ', anulado = ' + "'" + str('S')  + "' WHERE facturacion_id =  " + str(facturacionId )
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

        return JsonResponse({'success': False, 'Mensaje': 'Factura debe ser anulada previamente'})


    miConexion3 = None
    try:

                miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

                comando1 = 'INSERT INTO facturacion_liquidacion (id, documento_id ,  "consecAdmision" ,  fecha ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,  "totalSuministros" ,  "totalLiquidacion" ,  "valorApagar" ,  anulado ,  "fechaCorte" ,  anticipos ,  "detalleAnulacion" ,  "fechaAnulacion" ,  observaciones ,  "fechaRegistro" ,  "estadoRegistro" ,  convenio_id ,  "tipoDoc_id" ,  "usuarioAnula_id" , "usuarioRegistro_id" ,  "totalAbonos" ,  "totalRecibido", "sedesClinica_id", anulado ) SELECT ' + "'" + str(liquidacionId) + "'," + ' documento_id ,  "consecAdmision" ,  "fechaFactura" ,  "totalCopagos" ,  "totalCuotaModeradora" ,  "totalProcedimientos" ,  "totalSuministros" ,  "totalFactura" ,  "valorApagar" ,  anulado ,  "fechaCorte" ,  anticipos ,  "detalleAnulacion" ,  "fechaAnulacion" ,  observaciones ,  "fechaRegistro" ,  "estadoReg" ,  convenio_id ,  "tipoDoc_id" ,  "usuarioAnula_id" , "usuarioRegistro_id" ,  "totalAbonos" ,  "totalRecibido" , "sedesClinica_id" FROM facturacion_facturacion WHERE id =  ' + facturacionId
                print(comando1)
                cur3.execute(comando1)


                # Aquip hacer los INSERT A LIQUIDACIONDETALLE a partir de facturacion detalle

                comando2 = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo ,  fecha ,  cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  "fechaCrea" ,  "fechaModifica" ,  observaciones ,  "fechaRegistro" ,  "estadoRegistro" ,  "examen_id" ,  cums_id ,  "usuarioModifica_id" ,  "usuarioRegistro_id" ,  liquidacion_id ,  "tipoHonorario_id" ,  "tipoRegistro" , anulado, "codigoHomologado" ) SELECT "consecutivoFactura" ,  fecha ,  cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  "fechaCrea" ,  "fechaModifica" ,  observaciones ,  "fechaRegistro" , ' + "'" + str('A') + "'" + ' ,  "examen_id" ,  cums_id ,  "usuarioModifica_id" ,  "usuarioRegistro_id" , ' + "'" + str(liquidacionId) + "'" + ' ,  "tipoHonorario_id" ,  "tipoRegistro", anulado, "codigoHomologado"  FROM facturacion_facturaciondetalle WHERE facturacion_id =  ' + facturacionId
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

                datosMensaje = {'success': True, 'Mensaje': 'Factura Refacturada!'}
                json_data = json.dumps(datosMensaje, default=str)
                return HttpResponse(json_data, content_type='application/json')

                #return JsonResponse({'success': True, 'Mensajes': 'Factura Refacturada!'})

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

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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
        comando3 = 'INSERT INTO facturacion_liquidaciondetalle ( consecutivo, fecha, cantidad, "valorUnitario", "valorTotal", cirugia_id, "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro",examen_id,  "usuarioModifica_id", "usuarioRegistro_id", liquidacion_id, "tipoHonorario_id", "tipoRegistro", "historiaMedicamento_id",anulado,"codigoHomologado") select  det.consecutivo, liq.fecha, cantidad, proc."' + str(columnaProcedimientos) + '"' + ', proc."' + str(columnaProcedimientos) + '"' + ' * cantidad, cirugia_id, "fechaCrea", "fechaModifica", liq.observaciones, liq."fechaRegistro", liq."estadoRegistro", examen_id, "usuarioModifica_id", liq."usuarioRegistro_id",' + "'" + str(liquidacionIdHasta.id) + "'" + ' , "tipoHonorario_id",	"tipoRegistro", "historiaMedicamento_id", ' + "'" + str('N') + "'" + ', "codigohomologado" from facturacion_liquidacion liq  , facturacion_liquidaciondetalle det, contratacion_convenios conv,	  tarifarios_tarifariosdescripcion descrip, tarifarios_tipostarifa tiptar, tarifarios_tarifariosProcedimientos proc where det.liquidacion_id = liq.id and det.liquidacion_id = ' + "'" + str(liquidacionIdDesde.id) + "'" + ' and conv.id = ' + "'" + str(liquidacionIdHasta.convenio_id) + "'" + ' and det."estadoRegistro" = ' + "'" + str('A') + "'" + ' and descrip.id = conv."tarifariosDescripcionProc_id" and tiptar.id = descrip."tiposTarifa_id" and tiptar.id = proc."tiposTarifa_id" and proc."codigoCups_id" = det.examen_id'
        print("comando = ", comando3)
        curt.execute(comando3)


        ## Tercero busco los Cums desde y los envio Hasta

        comando4 = 'INSERT INTO facturacion_liquidaciondetalle ( consecutivo, fecha, cantidad, "valorUnitario", "valorTotal", cirugia_id, "fechaCrea", "fechaModifica", observaciones, "fechaRegistro", "estadoRegistro",cums_id,  "usuarioModifica_id", "usuarioRegistro_id", liquidacion_id, "tipoHonorario_id", "tipoRegistro", "historiaMedicamento_id", anulado, "codigoHomologado") select  det.consecutivo, liq.fecha, cantidad, sum.' + '"' + str(columnaSuministros) + '"' + ', sum."' + str(columnaSuministros) + '"'  + ' * cantidad, cirugia_id, "fechaCrea", "fechaModifica", liq.observaciones, liq."fechaRegistro", liq."estadoRegistro", cums_id, "usuarioModifica_id", liq."usuarioRegistro_id",' + "'" + str(liquidacionIdHasta.id) + "'" + ' , "tipoHonorario_id",	"tipoRegistro", "historiaMedicamento_id", ' + "'" + str('N') + "'" + ', "codigoHomologado" from facturacion_liquidacion liq  , facturacion_liquidaciondetalle det, contratacion_convenios conv,	  tarifarios_tarifariosdescripcion descrip, tarifarios_tipostarifa tiptar, tarifarios_tarifariosSuministros sum where det.liquidacion_id = liq.id and det.liquidacion_id = ' + "'" + str(liquidacionIdDesde.id) + "'" + ' and conv.id = ' + "'" + str(liquidacionIdHasta.convenio_id) + "'" + ' and det."estadoRegistro" =  ' + "'" + str('A') + "'" + ' and descrip.id = conv."tarifariosDescripcionSum_id" and tiptar.id = descrip."tiposTarifa_id" and tiptar.id = sum."tiposTarifa_id" and sum."codigoCum_id" = det.cums_id'
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


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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
        return JsonResponse({'success': False, 'Mensajes': 'Traslado realizado satisfactoriamente!'})


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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",password="123456")
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexionx.cursor()

    comando = 'select liq.id id,"consecutivoFactura" consecutivo ,  cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , exa.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg FROM facturacion_facturaciondetalle liq inner join clinico_examenes exa on (exa.id = liq."examen_id")  where facturacion_id= ' + "'" +  str(liquidacionId) + "'" +  ' AND "estadoRegistro" = ' + "'" + str('A') + "'" + ' and anulado=' + "'" + str('N') + "'" + ' UNION select liq.id id,"consecutivoFactura"  consecutivo, cast(date(fecha)||\' \'||to_char(fecha, \'HH:MI:SS\') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||\' \'||to_char("fechaCrea", \'HH:MI:SS\') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg FROM facturacion_facturaciondetalle liq inner join facturacion_suministros sum on (sum.id = liq.cums_id)  where facturacion_id= '  + "'" +  str(liquidacionId) + "'" + ' AND "estadoRegistro" = ' + "'" + str('A') + "' and anulado='N' or anulado = 'R'" + ' order by consecutivo'

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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",     password="123456")
    curx = miConexionx.cursor()

    if (tipoIngreso=='INGRESO'):

        detalle = 'SELECT fac.id id , fac.fecha fecha,fac."facturaNueva" , fac."facturaAnulada"  , serv.nombre servicio FROM facturacion_refacturacion fac LEFT JOIN sitios_serviciosadministrativos serv  ON (serv.id= fac."serviciosAdministrativos_id") WHERE fac."tipoDoc_id" = ' + "'" + str(ingresoId.tipoDoc_id) + "' and fac.documento_id = " + "'" + str(ingresoId.documento_id) + "'"

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



def GenerarJson(request):
    print ("Entre a GenerarJson" )

    facturaId = request.POST["facturaId"]
    textoXml = request.POST["textoXml"]
    print("facturaId = ", facturaId)
    print("textoXml = ", textoXml)

    carpetaXml = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\FACTURAS\\XML\\'
    print("carpetaXml = ", carpetaXml)

    carpetaJson = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\FACTURAS\\JSON\\'
    print("carpetaJson = ", carpetaJson)

    nombre_archivo = carpetaXml + '' + 'Factura_' + str(facturaId) + '.xml'
    print("nombre_archivo =", nombre_archivo)

    nombre_archivoJson = carpetaJson + '' + 'Factura_' + str(facturaId) + '.txt'
    print("nombre_archivoJson =", nombre_archivoJson)

    # Abro Conexion

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    curx = miConexionx.cursor()
    print("Aqui voy")

    comando = 'UPDATE facturacion_facturacion SET "rutaXml" = ' + "'" + str(nombre_archivo) + "'" + ' WHERE id = ' + str(facturaId)
    print("Aqui voy2")

    print(comando)

    curx.execute(comando)

    comando = 'UPDATE facturacion_facturacion SET "rutaJson" = ' + "'" + str(nombre_archivoJson) + "'" + ' WHERE id = ' + str(facturaId)
    print("Aqui voy3")

    print(comando)

    curx.execute(comando)

    funcionJson = []

    detalle = 'SELECT FacturaJsonDian_2(' + "'" + str(facturaId) + "') dato"

    print ('detalle a FacturaJsonDian_2 = ', detalle)

    curx.execute(detalle)

    for dato in curx.fetchall():
            funcionJson.append({'dato': dato})

    print("funcionJson[0]", funcionJson[0])

    miConexionx.commit()
    miConexionx.close()

    try:
        with open(nombre_archivo, 'w' , encoding='utf-8') as archivo:
            # Escribir el texto en el archivo
            archivo.write(textoXml)
            print(f"El archivo '{nombre_archivo}' se ha guardado correctamente.")
            file = open(nombre_archivoJson, "w")
            print("funcionJson[0]['dato']" , funcionJson[0]['dato'])
            file.writelines(funcionJson[0]['dato'])
            file.close()


    except IOError as e:
        print(f"Error al guardar el archivo: {e}")
        datosMensaje = {'success': False, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)

        return HttpResponse(json_data, content_type='application/json')

    except UnicodeEncodeError as e:
        print(f"Error encoding character: {e}")

    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

    return JsonResponse({'success': True, 'Mensajes': 'Factura JSON y/o Xml enviado generado !', 'ArchivoJson':funcionJson[0]['dato']})



def EnvioDian(request):
    print ("Entre a EnvioDyan" )

    facturaId = request.POST["facturaDianId"]
    print("facturaId = ", facturaId)

    # Abro Conexion

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",password="123456")
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

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    curx = miConexionx.cursor()

    comando = 'UPDATE facturacion_facturacion SET "fechaEnvioDian" = ' + "'" + str(fechaEnvioDian) + "'," + '"fechaRespuestaDian" = ' + str(fechaRespuestaDian) + "," + ' "respuestaDian" = ' + "'" + str(respuestaDian) + "'," + '"estadoEnvioDian_id" = ' + "'" + str(estadoEnvioDian) + "'" + ' WHERE id = ' + "'" + str(facturaId) + "'"

    print(comando)

    curx.execute(comando)
    miConexionx.commit()

    miConexionx.close()


    return JsonResponse({'success': True, 'Mensajes': 'Factura Actualizada !'})

