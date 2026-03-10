from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
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
from django.db import transaction, IntegrityError
import json
import datetime
from datetime import date, timedelta
import time
from decimal import Decimal
from admisiones.models import Ingresos
from farmacia.models import FarmaciaEstados
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle, Conceptos, Suministros
from clinico.models import Servicios, EspecialidadesMedicos, UnidadesDeMedidaDosis, ViasAdministracion, FrecuenciasAplicacion, TiposFolio, Historia, TipoDietas
import io
from enfermeria.models import Enfermeria,EnfermeriaRecibe, EnfermeriaDetalle, TurnosEnfermeria, TiposTurnosEnfermeria, EnfermeriaPlaneacion
import pandas as pd
from cirugia.models import EstadosCirugias, EstadosSalas, EstadosProgramacion, ProgramacionCirugias, Cirugias, ProgramacionCirugias
from contratacion.models import Convenios
from django.db.models import Min, Max, Avg
from django.db.models import F
from triage.models import Triage

# Create your views here.


def Load_dataPanelEnfermeria(request, data):
    print("Entre Load_dataPanelEnfermeria")

    context = {}
    d = json.loads(data)

    Sede = d['sede']
    print("sede = ", Sede)

    ingresos = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    #detalle = 'SELECT i.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual, (select count(*)  from facturacion_conveniospacienteingresos conv where conv."tipoDoc_id" = i."tipoDoc_id" and conv.documento_id=i.documento_id  and conv."consecAdmision"=i.consec) numConvenios,(select count(*)  from cartera_pagos pag where pag."tipoDoc_id" = i."tipoDoc_id" and pag.documento_id=i.documento_id  and pag.consec=i.consec) numPagos, empresa.nombre Empresa  FROM admisiones_ingresos i, usuarios_usuarios u, facturacion_empresas empresa , sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and empresa.id = i.empresa_id AND sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
    #        Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and ser.nombre != ' + "'" + str('TRIAGE') + "'" + ' AND dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"'
    #detalle = 'SELECT i.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual, (select count(*)  from facturacion_conveniospacienteingresos conv where conv."tipoDoc_id" = i."tipoDoc_id" and conv.documento_id=i.documento_id  and conv."consecAdmision"=i.consec) numConvenios,	(select count(*)  from cartera_pagos pag where pag."tipoDoc_id" = i."tipoDoc_id" and pag.documento_id=i.documento_id  and pag.consec=i.consec) numPagos,	empresa.nombre Empresa, date_part(' + "'" + str('YEAR') + "'" + ' ,  AGE(CURRENT_DATE , U."fechaNacio")) edad, i."salidaClinica" salidaClinica FROM admisiones_ingresos i inner join usuarios_usuarios u on ( u."tipoDoc_id" = i."tipoDoc_id"  and u.id = i."documento_id" ) left join facturacion_empresas empresa on (empresa.id = i.empresa_id) inner join sitios_dependencias dep on (dep.id = i."dependenciasActual_id" and dep."sedesClinica_id" =  i."sedesClinica_id" AND dep.disponibilidad = ' + "'" + str('O') + "')"  + ' inner join clinico_servicios ser on (ser.id = i."serviciosActual_id" and ser.nombre != ' + "'" + str('TRIAGE') + "')" + ' inner join usuarios_tiposDocumento tp on (tp.id = u."tipoDoc_id") inner join sitios_dependenciastipo deptip on ( deptip.id = dep."dependenciasTipo_id") left join  clinico_Diagnosticos diag on (diag.id = i."dxActual_id") inner join sitios_serviciosSedes sd on (sd."sedesClinica_id" = i."sedesClinica_id" and sd.id= dep."serviciosSedes_id" and sd.servicios_id  = ser.id) WHERE  i."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' AND i."fechaSalida" is null '
    detalle = 'SELECT i.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual, (select count(*)  from facturacion_conveniospacienteingresos conv where conv."tipoDoc_id" = i."tipoDoc_id" and conv.documento_id=i.documento_id  and conv."consecAdmision"=i.consec) numConvenios,	(select count(*)  from cartera_pagos pag where pag."tipoDoc_id" = i."tipoDoc_id" and pag.documento_id=i.documento_id  and pag.consec=i.consec) numPagos,	empresa.nombre Empresa, date_part(' + "'" + str('YEAR') + "'" + ' ,  AGE(CURRENT_DATE , U."fechaNacio")) edad, i."salidaClinica" salidaClinica FROM admisiones_ingresos i inner join usuarios_usuarios u on ( u."tipoDoc_id" = i."tipoDoc_id"  and u.id = i."documento_id" ) left join facturacion_empresas empresa on (empresa.id = i.empresa_id) inner join sitios_dependencias dep on (dep.id = i."dependenciasActual_id" and dep."sedesClinica_id" =  i."sedesClinica_id" AND dep.disponibilidad = ' + "'" + str('O') + "')"  + ' inner join clinico_servicios ser on (ser.nombre != ' + "'" + str('TRIAGE') + "')" + ' inner join usuarios_tiposDocumento tp on (tp.id = u."tipoDoc_id") inner join sitios_dependenciastipo deptip on ( deptip.id = dep."dependenciasTipo_id") left join  clinico_Diagnosticos diag on (diag.id = i."dxActual_id") inner join sitios_serviciosSedes sd on (sd."sedesClinica_id" = i."sedesClinica_id" and sd.id= dep."serviciosSedes_id" and sd.servicios_id  = ser.id) where i."sedesClinica_id" ='  + "'" + str(Sede) + "'" + ' and i."fechaSalida" is null  union SELECT tri.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , tri.consec consec , tri."fechaSolicita" , ser.nombre servicioNombreIng, ' + "'" + str('TRIAGE') + "'" + ' camaNombreIng , ' + "'" + str('' ) + "'" +  '  dxActual, (select count(*) from facturacion_conveniospacienteingresos conv where conv."tipoDoc_id" = tri."tipoDoc_id" and conv.documento_id=tri.documento_id  and conv."consecAdmision"=tri.consec) numConvenios,    (select count(*)  from cartera_pagos pag where pag."tipoDoc_id" = tri."tipoDoc_id" and pag.documento_id=tri.documento_id  and pag.consec=tri.consec) numPagos,  empresa.nombre Empresa, date_part(' + "'" + str('YEAR') + "'" + ' ,  AGE(CURRENT_DATE , U."fechaNacio")) edad, ' + "'" + str('N') + "'" + ' salidaClinica FROM triage_triage tri 	inner join usuarios_usuarios u on ( u."tipoDoc_id" = tri."tipoDoc_id"  and u.id = tri."documento_id" ) left join facturacion_empresas empresa on (empresa.id = tri.empresa_id) 	inner join usuarios_tiposDocumento tp on (tp.id = u."tipoDoc_id")  inner join sitios_serviciosSedes sd on (sd."sedesClinica_id" = tri."sedesClinica_id" and sd.id= tri."serviciosSedes_id" ) inner join clinico_servicios ser on (ser.id = sd.servicios_id )  WHERE  tri."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tri."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' AND tri."consecAdmision" = 0 '
    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc, documento, nombre, consec, fechaIngreso,  servicioNombreIng, camaNombreIng, dxActual, numConvenios, numPagos, Empresa , edad, salidaClinica in curx.fetchall():
            ingresos.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id, 'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre,
                 'Consec': consec, 'FechaIngreso': fechaIngreso,   'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                   'DxActual': dxActual,'numConvenios':numConvenios,'numPagos':numPagos, 'Empresa':Empresa,'edad':edad, 'salidaClinica': salidaClinica}})

    miConexionx.close()
    print("ingresos = " , ingresos)
    context['Ingresos'] = ingresos


    serialized1 = json.dumps(ingresos, default=str)

    return HttpResponse(serialized1, content_type='application/json')



def Load_dataPanelEnfermeria2(request, data):
    print("Entre Load_dataPanelEnfermeria2")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    enfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'select far.id id,origen.nombre origen, mov.nombre mov , serv.nombre servicio, far.historia_id historia FROM enfermeria_enfermeria far INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id =  far."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id= far."tipoMovimiento_id") INNER JOIN sitios_serviciosadministrativos serv ON (serv.id = far."serviciosAdministrativos_id") WHERE far."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND far."fechaRegistro" >= ' +  "'" +  str('2025-01-01') + "'" + ' ORDER BY far."fechaRegistro" desc'

    print(detalle)

    curx.execute(detalle)

    for id, origen, mov, servicio, historia in curx.fetchall():
        enfermeria.append(
            {"model": "enfermeria.enfermeria", "pk": id, "fields":
                {'id': id, 'origen': origen, 'mov':mov, 'servicio': servicio, 'historia': historia  }})

    miConexionx.close()
    print(enfermeria)

    serialized1 = json.dumps(enfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataMedicamentosEnfermeria(request, data):
    print("Entre Load_dataMedicamentosEnfermeria")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']

    print ("ingresoId =", ingresoId)


    esTriage='N'
    try:
        with transaction.atomic():

           ingresoId = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")


    medicamentosEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    if (esTriage == 'N'):

        detalle = 'SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, hist.folio folio,   fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis, recibe."cantidadDispensada" cantidad, 	  medida.descripcion UnidadMedida, sum.nombre medicamento, via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento" , recibe.despachos_id despacho FROM admisiones_ingresos ing INNER JOIN clinico_historia hist ON (hist."tipoDoc_id" = ing."tipoDoc_id" AND hist.documento_id=ing.documento_id AND hist."consecAdmision" = ing.consec) INNER JOIN farmacia_farmacia far ON (far.historia_id= hist.id) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN	enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN	enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id") INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = ing.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id")	WHERE ing.id=' + "'" + str(ingresoId.id) + "' UNION " + ' SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, 0 folio,  fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis,  recibe."cantidadDispensada" cantidad, 	  medida.descripcion UnidadMedida, sum.nombre medicamento, via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento" , recibe.despachos_id despacho  FROM admisiones_ingresos ing INNER JOIN farmacia_farmacia far ON (far."ingresoPaciente"= ing.id and far.historia_id <= 0) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN	enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id")  INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = ing.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id")	WHERE ing.id=' + "'" + str(ingresoId.id) + "' ORDER BY 5,6"
    else:

        detalle = 'SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, hist.folio folio,  fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis, recibe."cantidadDispensada" cantidad,   medida.descripcion UnidadMedida, sum.nombre medicamento,via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento" , recibe.despachos_id despacho FROM triage_triage tri 	INNER JOIN clinico_historia hist ON (hist."tipoDoc_id" = tri."tipoDoc_id" AND hist.documento_id=tri.documento_id AND hist."consecAdmision" = tri.consec) INNER JOIN farmacia_farmacia far ON (far.historia_id= hist.id) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN      enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id") INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) 	INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = tri.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id") WHERE tri.id=' + "'" + str(triageId.id) + "'" + ' UNION  SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, 0 folio, fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis,  recibe."cantidadDispensada" cantidad,  medida.descripcion UnidadMedida, sum.nombre medicamento, via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento" , recibe.despachos_id despacho FROM triage_triage tri INNER JOIN farmacia_farmacia far ON (far."ingresoPaciente"= tri.id and far.historia_id is null) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN   enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id") INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) 	INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") 	LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = tri.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id") WHERE tri.id=' + "'" + str(triageId.id) + "'" + ' ORDER BY 5,6'

    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc, documento, paciente, folio,  consecutivoMedicamento, dosis, cantidad,  UnidadMedida, medicamento, via, frecuencia, diasTratamiento, despacho in curx.fetchall():
            medicamentosEnfermeria.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id, 'tipoDoc': tipoDoc, 'Documento': documento, 'paciente': paciente,
                 'folio': folio,   'consecutivoMedicamento': consecutivoMedicamento, 'dosis':dosis,   'cantidad': cantidad, 'UnidadMedida': UnidadMedida,
                   'medicamento': medicamento,'via':via, 'frecuencia':frecuencia, 'diasTratamiento':diasTratamiento, 'despacho':despacho}})

    miConexionx.close()
    print("AQUI TOYYY")	
    print("medicamentosEnfermeria = " , medicamentosEnfermeria)


    serialized1 = json.dumps(medicamentosEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataParaClinicosEnfermeria(request, data):
    print("Entre Load_dataParaClinicosEnfermeria")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']

    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingresoAdmision = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")



    paraClinicosEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()


    if (esTriage=='N'):
        detalle = 'SELECT histExa.id id ,planta.nombre medico,hist.fecha fecha,hist.folio folio, tiposExa.nombre tipo ,histExa.consecutivo consecutivo,   histExa."codigoCups" cups,  exa.nombre examen, histExa.cantidad FROM clinico_historia hist INNER JOIN 	clinico_historiaexamenes histExa ON (histExa.historia_id = hist.id) INNER JOIN 	clinico_tiposexamen tiposExa ON ( tiposExa.id = histExa."tiposExamen_id") INNER JOIN clinico_examenes exa ON (exa."TiposExamen_id" = tiposExa.id and exa."codigoCups" = histExa."codigoCups") INNER JOIN planta_planta planta on (planta.id=hist.planta_id) WHERE hist."tipoDoc_id" = ' + "'" + str(ingresoAdmision.tipoDoc_id) + "' AND hist.documento_id = " + "'" + str(ingresoAdmision.documento_id) + "'" + ' and hist."consecAdmision" = ' + "'" + str(ingresoAdmision.consec) + "'" + ' order by hist.fecha, hist.folio'
    else:
        detalle = 'SELECT histExa.id id ,planta.nombre medico,hist.fecha fecha,hist.folio folio, tiposExa.nombre tipo ,histExa.consecutivo consecutivo,   histExa."codigoCups" cups,  exa.nombre examen, histExa.cantidad FROM clinico_historia hist INNER JOIN 	clinico_historiaexamenes histExa ON (histExa.historia_id = hist.id) INNER JOIN 	clinico_tiposexamen tiposExa ON ( tiposExa.id = histExa."tiposExamen_id") INNER JOIN clinico_examenes exa ON (exa."TiposExamen_id" = tiposExa.id and exa."codigoCups" = histExa."codigoCups") INNER JOIN planta_planta planta on (planta.id=hist.planta_id)  INNER JOIN triage_triage tri ON (tri."tipoDoc_id" = hist."tipoDoc_id"  AND  tri.documento_id = hist.documento_id and tri.consec=0 and tri."consecAdmision"= 0 and tri."fechaSolicita" <= hist.fecha)  WHERE hist."tipoDoc_id" = ' + "'" + str(triageId.tipoDoc_id) + "' AND hist.documento_id = " + "'" + str(triageId.documento_id) + "'" + ' and hist."consecAdmision" = ' + "'" + str(triageId.consec) + "'" + ' order by hist.fecha, hist.folio'

    print(detalle)

    curx.execute(detalle)

    for id, medico, fecha, folio, tipo, consecutivo, cups, examen,  cantidad  in curx.fetchall():
            paraClinicosEnfermeria.append({"model": "paraclinicos", "pk": id, "fields":
                {'id': id, 'medico': medico, 'fecha': fecha, 'folio' : folio,  'tipo': tipo,
                 'consecutivo': consecutivo, 'cups': cups,   'examen': examen, 'cantidad': cantidad}})

    miConexionx.close()
    print("paraClinicosEnfermeria = " , paraClinicosEnfermeria)


    serialized1 = json.dumps(paraClinicosEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataPedidosEnfermeria(request, data):
    print("Entre Load_PedidosEnfermeria")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']

    print ("ingresoId =", ingresoId)


    esTriage='N'
    try:
        with transaction.atomic():

           ingresoAdmision = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")



    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    enfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (esTriage=='N'):

        detalle = '	select enf.id id,origen.nombre origen, mov.nombre mov , serv.nombre servicio, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, serv.nombre servicio FROM enfermeria_enfermeria enf INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id =  enf."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id= enf."tipoMovimiento_id")  INNER JOIN sitios_serviciosadministrativos serv ON (serv.id = enf."serviciosAdministrativos_id") INNER JOIN admisiones_ingresos adm ON (adm.id = enf."ingresoPaciente" AND adm.id=' + "'" +  str(ingresoId) + "')"  + ' INNER JOIN usuarios_usuarios usu ON (usu.id = adm.documento_id ) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = adm."tipoDoc_id") WHERE enf."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND enf."fechaRegistro" >= ' + "'" + str('2025-01-01') + "'"  +  ' AND origen.nombre = ' + "'" + str('ENFERMERIA') +"'" + ' AND mov.nombre='  + "'" + str('PEDIDOS ENFERMERIA') + "'" + ' ORDER BY enf."fechaRegistro" desc'
    else:
        detalle = '	select enf.id id,origen.nombre origen, mov.nombre mov , serv.nombre servicio, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, serv.nombre servicio FROM enfermeria_enfermeria enf INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id =  enf."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id= enf."tipoMovimiento_id")  INNER JOIN sitios_serviciosadministrativos serv ON (serv.id = enf."serviciosAdministrativos_id") INNER JOIN triage_triage tri ON (tri.id = enf."ingresoPaciente" AND tri.id=' + "'" +  str(triageId.id) + "')"  + ' INNER JOIN usuarios_usuarios usu ON (usu.id = tri.documento_id ) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = tri."tipoDoc_id") WHERE enf."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND enf."fechaRegistro" >= ' + "'" + str('2025-01-01') + "'"  +  ' AND origen.nombre = ' + "'" + str('ENFERMERIA') +"'" + ' AND mov.nombre='  + "'" + str('PEDIDOS ENFERMERIA') + "'" + ' ORDER BY enf."fechaRegistro" desc'

    print(detalle)

    curx.execute(detalle)

    for id, origen, mov, servicio, tipoDoc, documento,paciente, servicio  in curx.fetchall():
        enfermeria.append(
            {"model": "enfermeria.enfermeria", "pk": id, "fields":
                {'id': id, 'origen': origen, 'mov':mov, 'servicio': servicio, 'tipoDoc':tipoDoc,'documento':documento, 'paciente':paciente, 'servicio':servicio }})

    miConexionx.close()
    print(enfermeria)

    serialized1 = json.dumps(enfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataPedidosEnfermeriaDetalle(request, data):
    print("Entre Load_dataPedidosEnfermeriaDetalle")

    context = {}
    envioDatos = {}

    d = json.loads(data)

    enfermeriaId = d['enfermeriaId']

    print("enfermeriaId =", enfermeriaId)


    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    enfermeriaDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = '	select  det.id id,origen.nombre origenNombre, mov.nombre movNombre, sum.nombre suministro, det."dosisCantidad" dosis, dosis.descripcion unidadDosis,   vias.nombre via,	det."cantidadOrdenada" cantidad, via.nombre viaAdministracion FROM enfermeria_enfermeria enf INNER JOIN enfermeria_enfermeriadetalle det  ON (det.enfermeria_id = enf.id) 		INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id = enf."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id = enf."tipoOrigen_id") 	INNER JOIN facturacion_suministros sum ON (sum.id= det.suministro_id) 	INNER JOIN clinico_viasadministracion vias ON (vias.id= det."viaAdministracion_id") 	INNER JOIN clinico_unidadesdemedidadosis dosis ON (dosis.id= det."dosisUnidad_id") 	INNER JOIN clinico_viasadministracion via ON (via.id= det."viaAdministracion_id")  where det.enfermeria_id =' + "'" + str(enfermeriaId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, origenNombre,movNombre,suministro, dosis, unidadDosis, via, cantidad , viaAdministracion  in curx.fetchall():
        enfermeriaDetalle.append(
            {"model": "famacia.farmaciaDetalle", "pk": id, "fields":
                {'id': id, 'origenNombre': origenNombre ,'movNombre':movNombre,'suministro':suministro,'dosis':dosis ,'unidadDosis':unidadDosis ,'cantidad':cantidad , 'viaAdministracion':viaAdministracion}})

    miConexionx.close()
    print(enfermeriaDetalle)

    print("envioDatos = " , envioDatos)

    serialized1 = json.dumps(enfermeriaDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def BuscaDatosPacienteEnfermeria(request):
    print("Entre BuscaDatosPacienteEnfermeria")


    ingresoId = request.POST['ingresoId']
    print ("ingresoId =", ingresoId)


    esTriage='N'
    try:
        with transaction.atomic():

           ingresoAdmision = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")


    # Combo Datos Paciente

    datosPacienteEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (esTriage == 'N'):

        detalle = 'select usu.id id,  i."tipoDoc_id" tipoDoc, tipos.nombre nombreTipoDoc, usu.documento documento, usu.nombre paciente, i."consec" consecutivoAdmision, serv.nombre servicio, dep.numero cama FROM admisiones_ingresos i INNER JOIN usuarios_usuarios usu ON (usu.id=i.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=i."tipoDoc_id")  INNER Join sitios_dependencias dep on (dep.id=i."dependenciasActual_id") INNER JOIN sitios_serviciossedes sd ON (sd.id=i."serviciosActual_id") INNER Join clinico_servicios serv on (serv.id=sd.servicios_id) where i.id= ' + "'" + str(ingresoId) + "'"
    else:

        detalle = 'select usu.id id,  tri."tipoDoc_id" tipoDoc, tipos.nombre nombreTipoDoc, usu.documento documento, usu.nombre paciente, tri."consec" consecutivoAdmision, serv.nombre servicio, ' + "'" + str('TRIAGE') + "'" + ' cama FROM triage_triage tri INNER JOIN usuarios_usuarios usu ON (usu.id=tri.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=tri."tipoDoc_id")    INNER JOIN sitios_serviciossedes sd ON (sd.id=tri."serviciosSedes_id")  INNER Join clinico_servicios serv on (serv.id=sd.servicios_id ) where tri.id= ' + "'" + str(triageId.id) + "'"


    print(detalle)

    curx.execute(detalle)

    for id,tipoDoc,nombreTipoDoc, documento, paciente ,consecutivoAdmision, servicio, cama  in curx.fetchall():
        datosPacienteEnfermeria.append(
            {"model": "datosPacienteEnfermeria", "pk": id, "fields":
                {'id':id, 'tipoDoc': tipoDoc, 'nombreTipoDoc':nombreTipoDoc, 'documento': documento,'paciente':paciente,'consecutivoAdmision':consecutivoAdmision ,'servicio':servicio, 'cama':cama}})

    miConexionx.close()
    print(datosPacienteEnfermeria)


    # Fin Combo

    serialized1 = json.dumps(datosPacienteEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def CreaPedidosEnfermeriaCabezote(request):
    print("Entre CreaPedidosEnfermeriaCabezote")

    ingresoId = request.POST['ingresoId']
    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingresoAdmision = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")


    username_id = request.POST['username_id']
    print ("username_id =", username_id)

    sede = request.POST['sede']
    print ("sede =", sede)

    enfermeriaTipoOrigen = request.POST['enfermeriaTipoOrigen']
    print ("enfermeriaTipoOrigen =", enfermeriaTipoOrigen)

    enfermeriaTipoMovimiento = request.POST['enfermeriaTipoMovimiento']
    print ("enfermeriaTipoMovimiento =", enfermeriaTipoMovimiento)

    servicioEnfermeria = request.POST['servicioEnfermeria']
    print ("servicioEnfermeria =", servicioEnfermeria)

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    #Actualiza estado despacho


    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (esTriage == 'N'):

        detalle = 'INSERT INTO enfermeria_enfermeria ( "tipoMovimiento_id", "fechaRegistro", "estadoReg", historia_id, "serviciosAdministrativos_id", "usuarioRegistro_id", "tipoOrigen_id", "sedesClinica_id","ingresoPaciente") VALUES (' + "'" + str(enfermeriaTipoMovimiento) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "',null,'" + str(servicioEnfermeria) + "','" + str(username_id) + "','"  + str(enfermeriaTipoOrigen) + "','" + str(sede) + "','" + str(ingresoId) + "')"
    else:
        detalle = 'INSERT INTO enfermeria_enfermeria ( "tipoMovimiento_id", "fechaRegistro", "estadoReg", historia_id, "serviciosAdministrativos_id", "usuarioRegistro_id", "tipoOrigen_id", "sedesClinica_id","ingresoPaciente") VALUES (' + "'" + str(enfermeriaTipoMovimiento) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "',null,'" + str(servicioEnfermeria) + "','" + str(username_id) + "','"  + str(enfermeriaTipoOrigen) + "','" + str(sede) + "','" + str(triageId.id) + "')"

    print(detalle)

    curx.execute(detalle)
    miConexionx.commit()
    miConexionx.close()


    return JsonResponse({'success': True, 'Mensaje': 'Pedido de Enfermeria Creado!'})


def AdicionarFormulacionEnfermeria(request):
    print("Entre AdicionarFormulacionenfermeria")

    context = {}

    username = request.POST['username']
    sede = request.POST['sede']
    username_id = request.POST['username_id']
    enfermeriaId = request.POST['enfermeriaId']

    enfermeria = Enfermeria.objects.get(id=enfermeriaId)


    servicioAdmonEnfermeria = request.POST['servicioAdmonEnfermeria']
    print("servicioAdmonEnfermeria:", servicioAdmonEnfermeria)

    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("enfermeriaId:", enfermeriaId)

    # Desde aqui

    formulacionEnfermeria = request.POST['formulacionEnfermeria']

    print("voy a validar Medicamentos =", formulacionEnfermeria)

    jsonFormulacionEnfermeria = json.loads(formulacionEnfermeria)

    print("voy para el FOR")

    print("voy a validar JSONMedicamentos =", jsonFormulacionEnfermeria)
    medicamentos= ""
    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    miConexion3 = None
    try:

        solicitud = FarmaciaEstados.objects.get(nombre='SOLICITUD')

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        # Creamos el Pedido de enfermeria en Farmacia

        comando = 'INSERT INTO farmacia_farmacia ("tipoMovimiento_id", "fechaRegistro", "estadoReg","serviciosAdministrativos_id", "usuarioRegistro_id","tipoOrigen_id", "sedesClinica_id", estado_id, "ingresoPaciente") VALUES (' + "'" + str(enfermeria.tipoMovimiento_id) + "','" + str( fechaRegistro) + "','" + str(estadoReg) + "','" + str(servicioAdmonEnfermeria) +  "','" + str(username_id) + "','" + str(enfermeria.tipoOrigen_id) + "','" + str(sede) + "','" + str(solicitud.id)  + "','"  + str(enfermeria.ingresoPaciente_id) + "') RETURNING id ;"
        print(comando)

        resultado = cur3.execute(comando)
        farmaciaId = cur3.fetchone()[0]

        print("farmaciaId = ", farmaciaId)

        ##############################################
        ##############################################

        # Segundo creamos la dispensacion del despacho
        item = 0

        for key in jsonFormulacionEnfermeria:

            if key["medicamentos"] != '':
                item = item +1
                medicamentos = key["medicamentos"].strip()
                print("medicamentos=", medicamentos)

                dosis = key["dosis"].strip()
                print("dosis=", dosis)
                uMedidaDosis = key["uMedidaDosis"].strip()
                print("uMedidaDosis=", uMedidaDosis)
                MedidaDosis = UnidadesDeMedidaDosis.objects.get(descripcion=uMedidaDosis)
                print ("MedidaDosis =", MedidaDosis.id)

                # frecuencia = key["frecuencia"]
                # print("frecuencia=", frecuencia)
                # vias = key["vias"]
                # print("vias =", vias )
                viasAdministracion = key["viasAdministracion"].strip()
                print("viasAdministracion =", viasAdministracion)
                vias = ViasAdministracion.objects.get(nombre=viasAdministracion)
                print ("vias =", vias)

                cantidadMedicamento = key["cantidadMedicamento"].strip()
                print("cantidadMedicamento=", cantidadMedicamento)
                # diasTratamiento = key["diasTratamiento"]
                # print("diasTratamiento=", diasTratamiento)


                # Creamos el detalle del pedido en Farmacia

                comando = 'INSERT INTO farmacia_farmaciadetalle ("dosisCantidad","cantidadOrdenada","fechaRegistro", "estadoReg", "dosisUnidad_id", "farmacia_id", "suministro_id","usuarioRegistro_id", "viaAdministracion_id")  VALUES ( ' + "'" + str(dosis) + "','" + str(cantidadMedicamento) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(MedidaDosis.id) + "','" + str(farmaciaId) + "','" + str(medicamentos) + "','" + str(username_id) + "','" + str(vias.id) +  "') RETURNING id ;"
                print(comando)
                resultado = cur3.execute(comando)
                farmaciaDetalle = cur3.fetchone()[0]

                ## Desde aqui INSERTAMOS EL DETALLE DE ENFERMERIA

                comando = 'INSERT INTO enfermeria_enfermeriadetalle ("dosisCantidad","cantidadOrdenada","fechaRegistro", "estadoReg", "dosisUnidad_id", "enfermeria_id", "suministro_id","usuarioRegistro_id", "viaAdministracion_id", "farmaciaDetalle_id")  VALUES ( ' + "'" + str(dosis) + "','" + str(cantidadMedicamento) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(MedidaDosis.id) + "','" + str(enfermeriaId) + "','" + str(medicamentos) + "','" + str(username_id) + "','" + str(vias.id) + "','" + str(farmaciaDetalle)   +  "')"

                print(comando)
                cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Pedido Enferemria creado satisfactoriamente!' })


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




    # Guarda en Enfermeriarecibe

    # Guarda en la cuenta del paciente facturacion_liquidaciondetalle


    # Creo eso es todop


def Load_dataTurnosEnfermeria(request, data):
    print("Entre Load_dataTurnosEnfermeria")

    context = {}
    d = json.loads(data)

    sede = d['sede']
    print ("sede =", sede)


    turnosEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    detalle = 'select turnos.id id, serv.nombre servicio, tipos.nombre tipoNombre , planta.nombre plantaNombre, tipos.horario horario FROM enfermeria_turnosenfermeria turnos INNER JOIN enfermeria_tiposturnosenfermeria tipos on (tipos.id = turnos."tiposTurnosEnfermeria_id") INNER JOIN planta_planta planta on (planta.id = turnos."enfermeraTurno_id") INNER JOIN sitios_serviciosadministrativos serv on (serv.id = turnos."serviciosAdministrativos_id") WHERE turnos."sedesClinica_id" = ' + "'" + str(sede) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, servicio, tipoNombre, plantaNombre, horario in curx.fetchall():
            turnosEnfermeria.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id, 'servicio': servicio, 'tipoNombre': tipoNombre, 'plantaNombre': plantaNombre,
                 'horario': horario}})

    miConexionx.close()
    print("turnosEnfermeria = " , turnosEnfermeria)


    serialized1 = json.dumps(turnosEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataPlaneacionEnfermeria(request, data):
    print("Entre Load_dataPlaneacionEnfermeria")

    context = {}
    d = json.loads(data)

    sede = d['sede']
    print ("sede =", sede)

    ingresoId = d['ingresoId']
    username_id = d['username_id']

    print ("ingresoId =", ingresoId)

    try:
        with transaction.atomic():

	        turnoenfermera = TurnosEnfermeria.objects.get(sedesClinica_id=sede,enfermeraTurno_id=username_id)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            return JsonResponse({'success': False, 'Mensajes': 'Enfermera  no tiene asignado un turno!'})

    finally:
        print("No haga nada")


    esTriage='N'
    try:
        with transaction.atomic():

           ingresoAdmision = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")


    enfermeriaRecibeId = d['enfermeriaRecibeId']
    print("enfermeriaRecibeId =", enfermeriaRecibeId)


    planeacionEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    if (esTriage=='N'):
        detalle = 'select pla.id id, pla."fechaPlanea" fechaPlanea, tipos1.nombre turnoPlanea, planta1.nombre enfermeraPlanea, pla."cantidadPlaneada" cantidadPlaneada, 	 pla."fechaAplica" fechaAplica, tipos2.nombre turnoAplica, planta2.nombre enfermeraAplica,   pla."cantidadAplicada" cantidadAplicada,	 pla."dosisCantidad" dosis, medida.descripcion medida, sum.nombre suministro, vias.nombre via, frec.descripcion frecuencia,	pla."diasTratamiento" dias FROM enfermeria_enfermeriaplaneacion pla INNER JOIN enfermeria_enfermeria enf ON (enf.id=pla.enfermeria_id)	 LEFT JOIN planta_planta planta1 ON (planta1.id = pla."enfermeraPlanea_id") LEFT JOIN planta_planta planta2 ON (planta2.id = pla."enfermeraAplica_id") INNER JOIN clinico_viasadministracion vias ON (vias.id = pla."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = pla."dosisUnidad_id") INNER JOIN clinico_frecuenciasaplicacion frec ON (frec.id = pla.frecuencia_id) INNER JOIN facturacion_suministros sum	ON (sum.id = pla.suministro_id) LEFT JOIN enfermeria_tiposturnosenfermeria tipos1 ON ( tipos1.id = pla."turnoEnfermeriaPlanea_id") LEFT JOIN enfermeria_tiposturnosenfermeria tipos2 ON ( tipos2.id = pla."turnoEnfermeriaAplica_id") WHERE enf."sedesClinica_id" = ' + "'" + str(sede) + "'" +  ' AND enf."ingresoPaciente" = ' + "'" + str(ingresoAdmision.id) + "'" + ' AND pla."enfermeriaRecibe_id" = ' + "'" + str(enfermeriaRecibeId) + "'"
    else:
        detalle = 'select pla.id id, pla."fechaPlanea" fechaPlanea, tipos1.nombre turnoPlanea, planta1.nombre enfermeraPlanea, pla."cantidadPlaneada" cantidadPlaneada, 	 pla."fechaAplica" fechaAplica, tipos2.nombre turnoAplica, planta2.nombre enfermeraAplica,   pla."cantidadAplicada" cantidadAplicada,	 pla."dosisCantidad" dosis, medida.descripcion medida, sum.nombre suministro, vias.nombre via, frec.descripcion frecuencia,	pla."diasTratamiento" dias FROM enfermeria_enfermeriaplaneacion pla INNER JOIN enfermeria_enfermeria enf ON (enf.id=pla.enfermeria_id)	 LEFT JOIN planta_planta planta1 ON (planta1.id = pla."enfermeraPlanea_id") LEFT JOIN planta_planta planta2 ON (planta2.id = pla."enfermeraAplica_id") INNER JOIN clinico_viasadministracion vias ON (vias.id = pla."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = pla."dosisUnidad_id") INNER JOIN clinico_frecuenciasaplicacion frec ON (frec.id = pla.frecuencia_id) INNER JOIN facturacion_suministros sum	ON (sum.id = pla.suministro_id) LEFT JOIN enfermeria_tiposturnosenfermeria tipos1 ON ( tipos1.id = pla."turnoEnfermeriaPlanea_id") LEFT JOIN enfermeria_tiposturnosenfermeria tipos2 ON ( tipos2.id = pla."turnoEnfermeriaAplica_id") WHERE enf."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND enf."ingresoPaciente" = ' + "'" + str(triageId.id) + "'" + ' AND pla."enfermeriaRecibe_id" = ' + "'" + str(enfermeriaRecibeId) + "'"


    print(detalle)

    curx.execute(detalle)

    for id, fechaPlanea, turnoPlanea, enfermeraPlanea, cantidadPlaneada,fechaAplica, turnoAplica, enfermeraAplica, cantidadAplicada, dosis, medida, suministro, via, frecuencia, dias  in curx.fetchall():
            planeacionEnfermeria.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id, 'fechaPlanea': fechaPlanea, 'turnoPlanea': turnoPlanea, 'enfermeraPlanea': enfermeraPlanea,
                 'cantidadPlaneada': cantidadPlaneada,'fechaAplica': fechaAplica, 'turnoAplica': turnoAplica, 'enfermeraAplica': enfermeraAplica, 'cantidadAplicada': cantidadAplicada,
                 'dosis':dosis, 'medida':medida, 'suministro':suministro, 'via':via, 'frecuencia':frecuencia, 'dias':dias}})

    miConexionx.close()
    print("planeacionEnfermeria = " , planeacionEnfermeria)


    serialized1 = json.dumps(planeacionEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def GuardaPlaneacionEnfermeria(request):
    print("Entre GuardaPlaneacionEnfermeria")

    username_id = request.POST['username_id']
    print ("username_id =", username_id)

    sede = request.POST['sede']
    print ("sede =", sede)

    enfermeriaRecibeId = request.POST['enfermeriaRecibeId']
    print ("enfermeriaRecibeId =", enfermeriaRecibeId)

    recibe = EnfermeriaRecibe.objects.get(id=enfermeriaRecibeId)
    detalle = EnfermeriaDetalle.objects.get(id=recibe.enfermeriaDetalle_id)
    enfermeria = Enfermeria.objects.get(id=detalle.enfermeria_id)

    turnoEnfermeria = TurnosEnfermeria.objects.get(enfermeraTurno_id=username_id)
    tiposTurnoEnfermeria = TiposTurnosEnfermeria.objects.get(id=turnoEnfermeria.tiposTurnosEnfermeria_id)

    suministro = request.POST['suministroP']
    print("suministro =", suministro)

    desdePlanea = request.POST['desdePlanea']
    print ("desdePlanea =", desdePlanea)
    numeroPlaneos = request.POST['numeroPlaneos']
    print ("numeroPlaneos =", numeroPlaneos)
    dosis = request.POST['dosisP']
    print("dosis =", dosis)
    cantidad = request.POST['dosisP']
    print("cantidad =", cantidad)
    medida = request.POST['medidaP']

    medidaId = UnidadesDeMedidaDosis.objects.get(descripcion=medida)

    print("medida =", medida)

    sum = Suministros.objects.get(id=recibe.suministro_id)

    via = request.POST['viaP']
    print("via =", via)
    viaId = ViasAdministracion.objects.get(nombre=via)

    diasTratamiento = request.POST['diasTratamientoP']

    print("diasTratamiento =", diasTratamiento)

    frecuenciaP = request.POST['frecuenciaP']
    print ("frecuenciaP =", frecuenciaP)

    frecuencia = FrecuenciasAplicacion.objects.get(descripcion=frecuenciaP)
    print ("frecuencia =", frecuencia.id)

    horasAMultiplicar = frecuencia.numeroHoras
    horasAMultiplicarTotales = 0

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    #Actualiza Planeacion de Enfermeria

    fechaPlanea=desdePlanea
    consecutivoPlaneacion = 1

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()
        # Primero creamos el despacho

        print ("aqui voy")

        for x in range(1, int(numeroPlaneos) + 1):

            detalle = 'INSERT INTO enfermeria_enfermeriaplaneacion ( "consecutivoPlaneacion",  "fechaPlanea", "dosisCantidad", "cantidadPlaneada",  "diasTratamiento", "fechaRegistro", "estadoReg", "dosisUnidad_id", "enfermeraPlanea_id", frecuencia_id, suministro_id, "usuarioRegistro_id", "viaAdministracion_id", "enfermeriaRecibe_id",  enfermeria_id,  "turnoEnfermeriaPlanea_id", anulado) VALUES (' + "'" + str(consecutivoPlaneacion) + "', cast('" + str(desdePlanea) + "' as timestamp)" + ' + INTERVAL ' + "'"  + str(horasAMultiplicarTotales) + str(' Hours') + "'," + str(dosis) + ",'" + str(cantidad) + "','" + str(diasTratamiento) +  "','"  + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(medidaId.id) + "','" + str(username_id) + "','"  + str(frecuencia.id) + "','" + str(sum.id) + "','" + str(username_id) + "','" + str(viaId.id) +  "','" + str(enfermeriaRecibeId) + "','"+ str(enfermeria.id) + "','" + str(turnoEnfermeria.id) + "','N')"
            print(detalle)
            cur3.execute(detalle)

            horasAMultiplicarTotales = horasAMultiplicar * x
            print("horasAMultiplicarTotales", horasAMultiplicarTotales)
            consecutivoPlaneacion = consecutivoPlaneacion + 1

        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Planeacion de Enfermeria Creado!'})

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


def GuardarDevolucionEnfermeria(request):
    print("Entre GuardarDevolucionEnfermeria")

    username_id = request.POST['username_id']
    print ("username_id =", username_id)

    sede = request.POST['sede']
    print ("sede =", sede)

    servicioAdmonEnfermeria = request.POST['servicioAdmonEnfermeria']
    print ("servicioAdmonEnfermeria =", servicioAdmonEnfermeria)


    devolucionEnfermeria = request.POST["formulacionDevolucion"]
    print("devolucionEnfermeria =", devolucionEnfermeria)

    ## Rutina leer el JSON de devolucionEnfermeria en python primero
    consecutivo = 0
    jsondevolucionEnfermeria = json.loads(devolucionEnfermeria)

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        # Primero cDevolucion cabezote

        print("aqui a Devolver a framacia ")

        detalle = 'INSERT INTO enfermeria_enfermeriadevolucion (  "fechaRegistro", "estadoReg", "sedesClinica_id", "serviciosAdministrativosDevuelve_id",  "usuarioDevuelve_id", "usuarioRegistro_id", anulado) VALUES (' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(sede) + "','" + str(servicioAdmonEnfermeria) + "','" + str(username_id)  + "','" + str(username_id) + "','N') RETURNING id"
        print(detalle)
        cur3.execute(detalle)
        devolucionId =  cur3.fetchone()[0]

        print("aqui lo que llega a farmacia ")

        detalle = 'INSERT INTO farmacia_farmaciadevolucion ("fechaRegistro", "estadoReg", "sedesClinica_id", "serviciosAdministrativosDevuelve_id", "usuarioDevuelve_id",  "usuarioRegistro_id") VALUES (' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(sede) + "','" + str(servicioAdmonEnfermeria) + "','" + str(username_id)  + "','" + str(username_id) + "') RETURNING id"
        print(detalle)
        cur3.execute(detalle)
        farmaciaId =  cur3.fetchone()[0]


        for key1 in jsondevolucionEnfermeria:

            print("key1 = ", key1)
            queda = key1
            enfermeriaRecibeId = key1["enfermeriaRecibeId"]
            print("enfermeriaRecibeId", enfermeriaRecibeId)
            medicamentos = key1["medicamentos"].strip()
            print("medicamentos = ", medicamentos)
            dosis = key1["dosis"]
            print("dosis", dosis)
            uMedidaDosis = key1["uMedidaDosis"]
            print("uMedidaDosis", uMedidaDosis)
            viasAdministracion = key1["viasAdministracion"]
            print("viasAdministracion", viasAdministracion)
            cantidadMedicamento = key1["cantidadMedicamento"]
            print("cantidadMedicamento", cantidadMedicamento)
            observaciones = key1["observaciones"]
            print("observaciones", observaciones)

            if medicamentos != "":

                    # Segundo Devolucion detalle

                    enfermeriaRecibe = EnfermeriaRecibe.objects.get(id=enfermeriaRecibeId)

                    if enfermeriaRecibe.cantidadDevuelta == None:
                        cantidadDevuelta = 0
                    else:
                        cantidadDevuelta = enfermeriaRecibe.cantidadDevuelta


                    if enfermeriaRecibe.netoCantidad == None:
                        netoCantidad = 0
                    else:
                        netoCantidad = enfermeriaRecibe.netoCantidad

                    netoCantidad = str(int(netoCantidad) - int(cantidadDevuelta))

                    detalle = 'INSERT INTO enfermeria_enfermeriadevoluciondetalle ("cantidadDevuelta", "fechaRegistro", "estadoReg", "enfermeriaDevolucion_id", "usuarioRegistro_id", observaciones, "enfermeriaRecibe_id", anulado) VALUES (' + "'" + str(cantidadMedicamento) + "','"  +  str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(devolucionId) + "','" + str(username_id) + "','" + str(observaciones)  + "','" + str(enfermeriaRecibeId) + "','N')"

                    print(detalle)
                    cur3.execute(detalle)

                    # Tercero actualiza totales cantidades

                    detalle = 'UPDATE enfermeria_enfermeriarecibe SET "cantidadDevuelta" = ' + "'" + str(cantidadMedicamento) + "'," + '"netoCantidad" = ' + "'" + str(netoCantidad) + "'"  + ' WHERE id = ' + "'" + str(enfermeriaRecibeId) + "'"

                    print(detalle)
                    cur3.execute(detalle)

                    # Cuarto actualiza detalle de farmaciadevolucion

                    if enfermeriaRecibe.farmaciaDespachosDispensa_id == None:
                        farmaciaDespachosDispensa_id = 0
                    else:
                        farmaciaDespachosDispensa_id = enfermeriaRecibe.farmaciaDespachosDispensa_id

                    if observaciones == '':
                        observaciones='.'

                    detalle = 'INSERT INTO farmacia_farmaciadevoluciondetalle ("cantidadDevuelta", "fechaRegistro", "estadoReg", "farmaciaDespachosDispensa_id", "farmaciaDevolucion_id", "usuarioRegistro_id", observaciones) VALUES (' + "'" + str(cantidadMedicamento) + "','"  +  str(fechaRegistro) + "','" + str(estadoReg) + "','" +  str(farmaciaDespachosDispensa_id)  + "','" + str(farmaciaId) + "','" + str(username_id) + "','" + str(observaciones) +  "')"

                    print(detalle)
                    cur3.execute(detalle)



        miConexion3.commit()
        miConexion3.close()

        # Tercero actualizamos acumulados


        return JsonResponse({'success': True, 'Mensajes': 'Devolucion de Enfermeria Creado! ' })


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


def GuardaAplicacionEnfermeria(request):
    print("Entre GuardaAplicacionEnfermeria")

    registroAplica = request.POST['registroAplica']
    print ("registroAplica =", registroAplica)

    registroPlaneaId = EnfermeriaPlaneacion.objects.get(id=registroAplica)

    username_id = request.POST['username_id']
    print ("username_id =", username_id)

    sede = request.POST['sede']
    print ("sede =", sede)

    #enfermeriaRecibeId = request.POST['enfermeriaRecibeId']
    #print ("enfermeriaRecibeId =", enfermeriaRecibeId)

    #recibe = EnfermeriaRecibe.objects.get(id=enfermeriaRecibeId)
    #detalle = EnfermeriaDetalle.objects.get(id=recibe.enfermeriaDetalle_id)
    #enfermeria = Enfermeria.objects.get(id=detalle.enfermeria_id)

    turnoEnfermeria = TurnosEnfermeria.objects.get(enfermeraTurno_id=username_id)
    tiposTurnoEnfermeria = TiposTurnosEnfermeria.objects.get(id=turnoEnfermeria.tiposTurnosEnfermeria_id)

    fechaAplica = request.POST['fechaAplica']
    print ("fechaAplica =", fechaAplica)
    dosis = request.POST['dosisA']
    print("dosis =", dosis)
    cantidad = request.POST['cantidadA']
    print("cantidad =", cantidad)
    medida = request.POST['medidaA']

    medidaId = UnidadesDeMedidaDosis.objects.get(descripcion=medida)

    print("medida =", medida)
    suministro = request.POST['suministroA']
    print("suministro =", suministro)

    sum = Suministros.objects.get(id=registroPlaneaId.suministro_id)

    via = request.POST['viaA']
    print("via =", via)
    viaId = ViasAdministracion.objects.get(nombre=via)

    diasTratamiento = request.POST['diasTratamientoA']

    print("diasTratamiento =", diasTratamiento)

    frecuenciaA = request.POST['frecuenciaA']
    print ("frecuenciaA =", frecuenciaA)

    frecuencia = FrecuenciasAplicacion.objects.get(descripcion=frecuenciaA)
    print ("frecuencia =", frecuencia.id)

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    #Actualiza Planeacion de Enfermeria

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()
        # Primero creamos el despacho

        print ("aqui voy")


        detalle = 'UPDATE enfermeria_enfermeriaplaneacion SET "turnoEnfermeriaAplica_id" = ' + "'" + str(turnoEnfermeria.id) + "'," + '"enfermeraAplica_id" = ' + "'" + str(username_id) + "'"  + ', "fechaAplica" = ' + "'" + str(fechaAplica) + "'" + ',"cantidadAplicada" = ' + "'" + str(cantidad) +  "' WHERE id =" + "'" + str(registroAplica) +"'"
        print(detalle)
        cur3.execute(detalle)


        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Aplicacion de Enfermeria Creado!'})

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



def Load_dataDietasEnfermeria(request, data):
    print("Entre Load_dataDietasEnfermeria")

    context = {}
    d = json.loads(data)

    sede = d['sede']
    print ("sede =", sede)

    ingresoId = d['ingresoId']

    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingresoId = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")


    dietasEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    if (esTriage=='N'):

        detalle = 'SELECT dieta.id id, dieta.consecutivo consecutivo, his.folio folio, tipoDieta.nombre nombreTipoDieta, dieta.observaciones, pla.nombre profesional FROM clinico_historialdietas dieta INNER JOIN clinico_tipodietas tipoDieta ON (tipoDieta.id = dieta."tipoDieta_id") INNER JOIN clinico_historia his ON (his.id = dieta.historia_id) INNER JOIN admisiones_ingresos ing on (ing."tipoDoc_id" = his."tipoDoc_id" AND ing.documento_id = his.documento_id AND ing.consec = his."consecAdmision") INNER JOIN planta_planta pla on (pla.id = his."usuarioRegistro_id") WHERE ing.id = ' + "'" + str(
            ingresoId.id) + "'"
    else:

        detalle = 'SELECT dieta.id id, dieta.consecutivo consecutivo, his.folio folio, tipoDieta.nombre nombreTipoDieta, dieta.observaciones, pla.nombre profesional FROM clinico_historialdietas dieta INNER JOIN clinico_tipodietas tipoDieta ON (tipoDieta.id = dieta."tipoDieta_id") INNER JOIN clinico_historia his ON (his.id = dieta.historia_id) INNER JOIN triage_triage tri on (tri."tipoDoc_id" = his."tipoDoc_id" AND tri.documento_id = his.documento_id AND tri.consec = his."consecAdmision") INNER JOIN planta_planta pla on (pla.id = his."usuarioRegistro_id") WHERE tri.id = ' + "'" + str(
            triageId.id) + "'"


    print(detalle)

    curx.execute(detalle)

    for id, consecutivo, folio, nombreTipoDieta, observaciones, profesional in curx.fetchall():
            dietasEnfermeria.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id, 'consecutivo': consecutivo, 'folio': folio, 'nombreTipoDieta': nombreTipoDieta,
                 'observaciones': observaciones,   'profesional': profesional}})

    miConexionx.close()
    print("dietasEnfermeria = " , dietasEnfermeria)


    serialized1 = json.dumps(dietasEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def GuardaDietasEnfermeria(request):
    print("Entre GuardaDietasEnfermeria")



    username_id = request.POST['username_id']
    print ("username_id =", username_id)

    sede = request.POST['sede']
    print ("sede =", sede)

    ingresoId = request.POST['ingresoId']
    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingreso = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")

    tiposDietas = request.POST['tiposDietasD']
    print ("tiposDietas =", tiposDietas)

    #tiposDietasId = TipoDietas.objects.get(nombre=tiposDietas)
    #print ("tiposDietasId =", tiposDietasId.id)

    observaciones = request.POST['observacionesD']
    print ("observaciones =", observaciones)
    serviciosAdministrativos = request.POST['serviciosAdministrativosD']
    print ("serviciosAdministrativos =", serviciosAdministrativos)

    tiposFolio = TiposFolio.objects.get(nombre='ENFERMERIA')

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    #Crea Dieta Enfermeria

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        # Primero buscamos el numero del folio nuevo

        if (esTriage=='N'):

            ultimofolio = Historia.objects.all().filter(tipoDoc_id=ingreso.tipoDoc_id).filter(documento_id=ingreso.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))
        else:
            ultimofolio = Historia.objects.all().filter(tipoDoc_id=triageId.tipoDoc_id).filter(documento_id=triageId.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))

        print("ultimo folio = ", ultimofolio)
        print("ultimo folio = ", ultimofolio['maximo'])
        ultimofolio2 = (ultimofolio['maximo']) + 1
        print("ultimo folio2 = ", ultimofolio2)

        # Segundo  INSERT en clinico_historial

        if (esTriage == 'N'):

            detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(ingreso.consec) + "','" + str(ultimofolio2) +  "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) +"','" + str(ingreso.documento_id) + "','" + str(ingreso.tipoDoc_id) + "','" + str(username_id)  + "','" + str(tiposFolio.id)  + "','" + str(username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"
        else:
            detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(triageId.consec) + "','" + str(ultimofolio2) +  "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) +"','" + str(triageId.documento_id) + "','" + str(triageId.tipoDoc_id) + "','" + str(username_id)  + "','" + str(tiposFolio.id)  + "','" + str(username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"

        print(detalle)
        resultado = cur3.execute(detalle)
        historiaId = cur3.fetchone()[0]
        print("historiaId = ", historiaId)

        # Segundo  INSERT en clinico_historialdietas

        detalle = 'INSERT INTO clinico_historialdietas ( observaciones, "estadoReg", historia_id, "tipoDieta_id" )  VALUES (' + "'" + str(observaciones) + "','" + str(estadoReg) +"','" + str(historiaId) + "','" + str(tiposDietas) + "')"
        print(detalle)
        cur3.execute(detalle)
        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Dieta Paciente Creada!'})

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


def GuardaNotasEnfermeria(request):
    print("Entre GuardaNotasEnfermeria")


    username_id = request.POST['username_id']
    print ("username_id =", username_id)

    sede = request.POST['sede']
    print ("sede =", sede)

    ingresoId = request.POST['ingresoId']
    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingreso = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")


    observaciones = request.POST['observacionesN']
    print ("observaciones =", observaciones)
    serviciosAdministrativos = request.POST['serviciosAdministrativosN']
    print ("serviciosAdministrativos =", serviciosAdministrativos)

    tiposFolio = TiposFolio.objects.get(nombre='ENFERMERIA')

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    #Crea Dieta Enfermeria

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        # Primero buscamos el numero del folio nuevo
        if (esTriage=='N'):
            ultimofolio = Historia.objects.all().filter(tipoDoc_id=ingreso.tipoDoc_id).filter(documento_id=ingreso.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))
        else:
            ultimofolio = Historia.objects.all().filter(tipoDoc_id=triageId.tipoDoc_id).filter(documento_id=triageId.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))




        print("ultimo folio = ", ultimofolio)
        print("ultimo folio = ", ultimofolio['maximo'])
        ultimofolio2 = (ultimofolio['maximo']) + 1
        print("ultimo folio2 = ", ultimofolio2)

        # Segundo  INSERT en clinico_historial

        if (esTriage=='N'):
            detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(ingreso.consec) + "','" + str(ultimofolio2) +  "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) +"','" + str(ingreso.documento_id) + "','" + str(ingreso.tipoDoc_id) + "','" + str(username_id)  + "','" + str(tiposFolio.id)  + "','" + str(username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"
        else:
            detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(triageId.consec) + "','" + str(ultimofolio2) +  "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) +"','" + str(triageId.documento_id) + "','" + str(triageId.tipoDoc_id) + "','" + str(username_id)  + "','" + str(tiposFolio.id)  + "','" + str(username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"

        print(detalle)
        resultado = cur3.execute(detalle)
        historiaId = cur3.fetchone()[0]
        print("historiaId = ", historiaId)

        # Segundo  INSERT en clinico_historialdietas

        detalle = 'INSERT INTO clinico_historialnotasenfermeria ( observaciones, "fechaRegistro", "estadoReg", historia_id )  VALUES (' + "'" + str(observaciones) + "','" + str(fechaRegistro)  + "','" + str(estadoReg) +"','" + str(historiaId) + "')"
        print(detalle)
        cur3.execute(detalle)
        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Dieta Paciente Creada!'})

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


def Load_dataNotasEnfermeria(request, data):
    print("Entre Load_dataNotasEnfermeria")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']

    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingresoId = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")



    notasEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()
	
    if (esTriage == 'N'):
        detalle = 'SELECT notas.id id, his.folio folio,  notas.observaciones, pla.nombre profesional FROM clinico_historialnotasenfermeria notas  INNER JOIN clinico_historia his ON (his.id = notas.historia_id) INNER JOIN admisiones_ingresos ing on (ing."tipoDoc_id" = his."tipoDoc_id" AND ing.documento_id = his.documento_id AND ing.consec = his."consecAdmision") INNER JOIN planta_planta pla on (pla.id = his."usuarioRegistro_id") WHERE ing.id = ' + "'" + str(
            ingresoId.id) + "'"
    else:

        detalle = 'SELECT notas.id id, his.folio folio,  notas.observaciones, pla.nombre profesional FROM clinico_historialnotasenfermeria notas  INNER JOIN clinico_historia his ON (his.id = notas.historia_id) INNER JOIN triage_triage tri  on (tri."tipoDoc_id" = his."tipoDoc_id" AND tri.documento_id = his.documento_id AND tri.consec = his."consecAdmision") INNER JOIN planta_planta pla on (pla.id = his."usuarioRegistro_id") WHERE tri.id = ' + "'" + str(
            triageId.id) + "'"


    print(detalle)

    curx.execute(detalle)

    for id, folio, observaciones, profesional in curx.fetchall():
            notasEnfermeria.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id,  'folio': folio,  'observaciones': observaciones,   'profesional': profesional}})

    miConexionx.close()
    print("notasEnfermeria = " , notasEnfermeria)


    serialized1 = json.dumps(notasEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataDevolucionEnfermeria(request, data):
    print("Entre Load_dataDevolucionEnfermeria")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']

    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingresoId = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")


    devolucionEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    if (esTriage=='N'):

            detalle = 'SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, hist.folio folio,   fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis, recibe."cantidadDispensada" cantidad, 	  medida.descripcion UnidadMedida, sum.nombre medicamento, via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento" , dev."cantidadDevuelta" FROM admisiones_ingresos ing INNER JOIN clinico_historia hist ON (hist."tipoDoc_id" = ing."tipoDoc_id" AND hist.documento_id=ing.documento_id AND hist."consecAdmision" = ing.consec) INNER JOIN farmacia_farmacia far ON (far.historia_id= hist.id) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN	enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN	enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id") INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = ing.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id") LEFT JOIN enfermeria_enfermeriadevoluciondetalle dev ON (dev."enfermeriaRecibe_id" = recibe.id )	WHERE ing.id=' + "'" + str(ingresoId.id) + "' UNION " + ' SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, 0 folio,  fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis,  recibe."cantidadDispensada" cantidad, 	  medida.descripcion UnidadMedida, sum.nombre medicamento, via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento"  , dev."cantidadDevuelta" FROM admisiones_ingresos ing INNER JOIN farmacia_farmacia far ON (far."ingresoPaciente"= ing.id) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN	enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id")  INNER JOIN	enfermeria_enfermeria enf ON (enf.id = enfdet.enfermeria_id and enf.historia_id is null)  INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = ing.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id") LEFT JOIN enfermeria_enfermeriadevoluciondetalle dev ON (dev."enfermeriaRecibe_id" = recibe.id ) WHERE ing.id=' + "'" + str(ingresoId.id) + "' ORDER BY 5,6"
    else:
            detalle = 'SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, hist.folio folio,   fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis, recibe."cantidadDispensada" cantidad, 	  medida.descripcion UnidadMedida, sum.nombre medicamento, via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento"  , dev."cantidadDevuelta" FROM admisiones_ingresos ing INNER JOIN clinico_historia hist ON (hist."tipoDoc_id" = ing."tipoDoc_id" AND hist.documento_id=ing.documento_id AND hist."consecAdmision" = ing.consec) INNER JOIN farmacia_farmacia far ON (far.historia_id= hist.id) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN	enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN	enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id") INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = ing.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id") LEFT JOIN enfermeria_enfermeriadevoluciondetalle dev ON (dev."enfermeriaRecibe_id" = recibe.id )	WHERE ing.id=' + "'" + str(triageId.id) + "' UNION " + ' SELECT recibe.id id, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, 0 folio,  fardet."consecutivoMedicamento" consecutivoMedicamento, recibe."dosisCantidad" dosis,  recibe."cantidadDispensada" cantidad, 	  medida.descripcion UnidadMedida, sum.nombre medicamento, via.nombre via , frec.descripcion frecuencia, enfdet."diasTratamiento" , dev."cantidadDevuelta" FROM admisiones_ingresos ing INNER JOIN farmacia_farmacia far ON (far."ingresoPaciente"= ing.id) INNER JOIN farmacia_farmaciadetalle fardet ON (fardet.farmacia_id = far.id) INNER JOIN enfermeria_enfermeriarecibe recibe ON (recibe."farmaciaDetalle_id" = fardet.id) INNER JOIN	enfermeria_enfermeriadetalle enfdet ON (enfdet.id = recibe."enfermeriaDetalle_id") INNER JOIN	enfermeria_enfermeria enf ON (enf.id = enfdet.enfermeria_id and enf.historia_id is null) INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") LEFT JOIN clinico_frecuenciasaplicacion frec ON (frec.id = enfdet."frecuencia_id") INNER JOIN usuarios_usuarios usu ON (usu.id = ing.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = usu."tipoDoc_id")	LEFT JOIN enfermeria_enfermeriadevoluciondetalle dev ON (dev."enfermeriaRecibe_id" = recibe.id ) WHERE ing.id=' + "'" + str(triageId.id) + "' ORDER BY 5,6"



    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc, documento, paciente, folio,  consecutivoMedicamento, dosis, cantidad,  UnidadMedida, medicamento, via, frecuencia, diasTratamiento ,cantidadDevuelta in curx.fetchall():
            devolucionEnfermeria.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id, 'tipoDoc': tipoDoc, 'Documento': documento, 'paciente': paciente,
                 'folio': folio,   'consecutivoMedicamento': consecutivoMedicamento, 'dosis':dosis,   'cantidad': cantidad, 'UnidadMedida': UnidadMedida,
                   'medicamento': medicamento,'via':via, 'frecuencia':frecuencia, 'diasTratamiento':diasTratamiento,'cantidadDevuelta':cantidadDevuelta}})

    miConexionx.close()
    print("devolucionEnfermeria = " , devolucionEnfermeria)


    serialized1 = json.dumps(devolucionEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataConsultaDevolucionesEnfermeria(request, data):
    print("Entre Load_dataConsultaDevolucionesEnfermeria")

    context = {}
    d = json.loads(data)

    sede = d['sede']
    print ("sede =", sede)

    fechaRegistro = datetime.datetime.now()


    año_actual = fechaRegistro.year  # Puedes cambiar este valor
    fechaRegistro = date(año_actual, 1, 1)

    print(fechaRegistro)


    devolucionesConsultaEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    detalle = 'select dev.id, dev."fechaRegistro" fechaRegistro ,servDevuelve.nombre servicioDevuelve,plantaDevuelve.nombre usuarioDevuelve,servRecibe.nombre servicioRecibe,plantaRecibe.nombre usuarioRecibe FROM enfermeria_enfermeriadevolucion dev INNER JOIN sitios_serviciosadministrativos servDevuelve ON (servDevuelve.id = dev."serviciosAdministrativosDevuelve_id") LEFT JOIN 	sitios_serviciosadministrativos servRecibe ON (servRecibe.id = dev."serviciosAdministrativosRecibe_id" ) INNER JOIN planta_planta plantaDevuelve  ON (plantaDevuelve.id = dev."usuarioDevuelve_id") LEFT JOIN planta_planta plantaRecibe ON (plantaRecibe.id = dev."usuarioRecibe_id") WHERE dev."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND  dev."fechaRegistro" >=' + "'" + str(fechaRegistro) + "'" + ' order by dev.id'

    print(detalle)

    curx.execute(detalle)

    for id, fechaRegistro, servicioDevuelve, usuarioDevuelve, servicioRecibe,  usuarioRecibe in curx.fetchall():
            devolucionesConsultaEnfermeria.append({"model": "enfermeria.devoluciones", "pk": id, "fields":
                {'id': id, 'fechaRegistro': fechaRegistro, 'servicioDevuelve': servicioDevuelve, 'usuarioDevuelve': usuarioDevuelve,
                 'servicioRecibe': servicioRecibe,   'usuarioRecibe': usuarioRecibe}})

    miConexionx.close()
    print("devolucionesConsultaEnfermeria = " , devolucionesConsultaEnfermeria)


    serialized1 = json.dumps(devolucionesConsultaEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataConsultaDevolucionesDetalleEnfermeria(request, data):
    print("Entre Load_dataConsultaDevolucionesDetalleEnfermeria")

    context = {}
    d = json.loads(data)

    devolucionEnfermeriaId = d['devolucionEnfermeriaId']

    print ("devolucionEnfermeriaId =", devolucionEnfermeriaId)

    ConsultaDevolucionesDetalleEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT devdet.id id,	sum.nombre medicamento,recibe."dosisCantidad" dosis, medida.descripcion unidadMedida, via.nombre via ,  recibe."cantidadDispensada" cantidad, devdet."cantidadDevuelta"	 cantidadDevuelta , devdet.observaciones observaciones 	FROM enfermeria_enfermeriadevoluciondetalle devdet INNER JOIN	enfermeria_enfermeriarecibe recibe ON (recibe.id = devdet."enfermeriaRecibe_id") INNER JOIN facturacion_suministros sum ON (sum.id = recibe.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = recibe."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = recibe."dosisUnidad_id") WHERE devdet."enfermeriaDevolucion_id" = ' + "'" + str(devolucionEnfermeriaId) + "'"


    print(detalle)

    curx.execute(detalle)

    for id, medicamento, dosis, unidadMedida, via,  cantidad, cantidadDevuelta, observaciones in curx.fetchall():
            ConsultaDevolucionesDetalleEnfermeria.append({"model": "enfermeria.devolucionesdetalle", "pk": id, "fields":
                {'id': id, 'medicamento': medicamento, 'dosis': dosis, 'unidadMedida': unidadMedida,
                 'via': via,   'cantidad': cantidad, 'cantidadDevuelta':cantidadDevuelta, 'bservaciones':observaciones}})

    miConexionx.close()
    print("ConsultaDevolucionesDetalleEnfermeria = " , ConsultaDevolucionesDetalleEnfermeria)


    serialized1 = json.dumps(ConsultaDevolucionesDetalleEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')



def Load_dataSignosVitalesEnfermeria(request, data):
    print("Entre Load_dataSignosVitalesEnfermeria")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']

    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingresoId = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")



    signosVitalesEnfermeria = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    if (esTriage=='N'):

        detalle = 'SELECT sig.id, sig.fecha, his.folio, sig."frecCardiaca", sig."frecRespiratoria", sig."tensionADiastolica", sig."tensionASistolica", "tensionAMedia", sig.temperatura, sig.saturacion, sig.glucometria, sig.glasgow, sig.apache, pvc, cuna, ic, "glasgowOcular", "glasgowVerbal", "glasgowMotora", sig.observacion, sig."fechaRegistro",  pla.nombre usuarioRegistro FROM clinico_historiasignosvitales sig INNER JOIN clinico_historia his on (his.id = sig.historia_id) INNER JOIN admisiones_ingresos adm on (adm."tipoDoc_id" = his."tipoDoc_id"  and adm.documento_id=his.documento_id and adm.consec=his."consecAdmision") INNER JOIN planta_planta pla on (pla.id= sig."usuarioRegistro_id")	WHERE adm.id = ' + "'" + str(ingresoId.id) + "'"
    else:
        detalle = 'SELECT sig.id, sig.fecha, his.folio, sig."frecCardiaca", sig."frecRespiratoria", sig."tensionADiastolica", sig."tensionASistolica", "tensionAMedia", sig.temperatura, sig.saturacion, sig.glucometria, sig.glasgow, sig.apache, pvc, cuna, ic, "glasgowOcular", "glasgowVerbal", "glasgowMotora", sig.observacion, sig."fechaRegistro",  pla.nombre usuarioRegistro FROM clinico_historiasignosvitales sig INNER JOIN clinico_historia his on (his.id = sig.historia_id) INNER JOIN triage_triage tri on (tri."tipoDoc_id" = his."tipoDoc_id"  and tri.documento_id=his.documento_id and tri.consec=his."consecAdmision") INNER JOIN planta_planta pla on (pla.id= sig."usuarioRegistro_id")	WHERE tri.id = ' + "'" + str(triageId.id) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, fecha, folio, frecCardiaca, frecRespiratoria, tensionADiastolica, tensionASistolica,  tensionAMedia, temperatura, saturacion, glucometria, glasgow, apache, pvc, cuna, ic, glasgowOcular, glasgowVerbal, glasgowMotora, observacion,  fechaRegistro , usuarioRegistro in curx.fetchall():
            signosVitalesEnfermeria.append({"model": "enfermeria.signosvitales", "pk": id, "fields":
                {'id': id, 'fecha':fecha, 'folio':folio, 'frecCardiaca': frecCardiaca, 'frecRespiratoria': frecRespiratoria, 'tensionADiastolica': tensionADiastolica,
                 'tensionAMedia':tensionAMedia,'temperatura': temperatura,'saturacion':saturacion,'glucometria':glucometria,'glasgow':glasgow,'apache':apache,'pvc':pvc, 'cuna':cuna, 'ic':ic, 'glasgowOcular':glasgowOcular,'glasgowVerbal':glasgowVerbal,'glasgowMotora' :glasgowMotora, 'observacion':observacion, 'usuarioRegistro':usuarioRegistro    }})

    miConexionx.close()
    print("signosVitalesEnfermeria = " , signosVitalesEnfermeria)


    serialized1 = json.dumps(signosVitalesEnfermeria, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def GuardaSignosVitalEnfermeria(request):
    print("Entre GuardaSignosVitalEnfermeria")


    username_id = request.POST['username_id']
    print ("username_id =", username_id)
    sede = request.POST['sede']
    print ("sede =", sede)
    ingresoId = request.POST['ingresoId']
    print ("ingresoId =", ingresoId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingreso = Ingresos.objects.get(id=ingresoId)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(id=ingresoId)
            esTriage = 'S'

    finally:
        print("No haga nada")

    #fecha = request.POST['fecha']
    #print ("fecha =", fecha)

    frecCardiaca = request.POST['frecCardiaca']
    print ("frecCardiaca =", frecCardiaca)
    frecRespiratoria = request.POST['frecRespiratoria']
    print ("frecRespiratoria =", frecRespiratoria)
    tensionADiastolica = request.POST['tensionADiastolica']
    print ("tensionADiastolica =", tensionADiastolica)
    tensionASistolica = request.POST['tensionASistolica']
    print ("tensionASistolica =", tensionASistolica)
    tensionAMedia = request.POST['tensionAMedia']
    print ("tensionAMedia =", tensionAMedia)
    temperatura = request.POST['temperatura']
    print ("temperatura =", temperatura)
    saturacion = request.POST['saturacion']
    print ("saturacion =", saturacion)
    glucometria = request.POST['glucometria']
    print ("glucometria =", glucometria)

    glasgow = request.POST['glasgow']
    print ("glasgow =", glasgow)
    apache = request.POST['apache']
    print ("apache =", apache)
    pvc = request.POST['pvc']
    print ("pvc =", pvc)
    cuna = request.POST['cuna']
    print ("cuna =", cuna)
    ic = request.POST['ic']
    print ("ic =", ic)
    glasgowOcular = request.POST['glasgowOcular']
    print ("glasgowOcular =", glasgowOcular)
    glasgowVerbal = request.POST['glasgowVerbal']
    print ("glasgowVerbal =", glasgowVerbal)
    glasgowMotora = request.POST['glasgowMotora']
    print ("glasgowMotora =", glasgowMotora)

    observacion = request.POST['observacion']
    print ("observacion =", observacion)

    serviciosAdministrativos = request.POST['serviciosAdministrativosSig']
    print ("serviciosAdministrativos =", serviciosAdministrativos)

    tiposFolio = TiposFolio.objects.get(nombre='ENFERMERIA')

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    #Crea El signo vital Enfermeria

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        # Primero buscamos el numero del folio nuevo
        if (esTriage=='N'):

            ultimofolio = Historia.objects.all().filter(tipoDoc_id=ingreso.tipoDoc_id).filter(documento_id=ingreso.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))
        else:
            ultimofolio = Historia.objects.all().filter(tipoDoc_id=triageId.tipoDoc_id).filter(documento_id=triageId.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))


        print("ultimo folio = ", ultimofolio)
        print("ultimo folio = ", ultimofolio['maximo'])
        ultimofolio2 = (ultimofolio['maximo']) + 1
        print("ultimo folio2 = ", ultimofolio2)

        # Segundo  INSERT en clinico_historial

        if (esTriage=='N'):
            detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(ingreso.consec) + "','" + str(ultimofolio2) +  "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) +"','" + str(ingreso.documento_id) + "','" + str(ingreso.tipoDoc_id) + "','" + str(username_id)  + "','" + str(tiposFolio.id)  + "','" + str(username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"
        else:
            detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(triageId.consec) + "','" + str(ultimofolio2) +  "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) +"','" + str(triageId.documento_id) + "','" + str(triageId.tipoDoc_id) + "','" + str(username_id)  + "','" + str(tiposFolio.id)  + "','" + str(username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"

        print(detalle)
        resultado = cur3.execute(detalle)
        historiaId = cur3.fetchone()[0]
        print("historiaId = ", historiaId)

        # Segundo  INSERT en clinico_historialdietas

        detalle = 'INSERT INTO clinico_historiasignosvitales ( fecha, "frecCardiaca", "frecRespiratoria", "tensionADiastolica", "tensionASistolica", "tensionAMedia", temperatura, saturacion, glucometria, glasgow, apache, pvc, cuna, ic, "glasgowOcular", "glasgowVerbal", "glasgowMotora", observacion, "fechaRegistro", "estadoReg", historia_id, "usuarioRegistro_id" )  VALUES (' + "'" + str(fechaRegistro) +  "','" + str(frecCardiaca) +"','" + str(frecRespiratoria) + "','" + str(tensionADiastolica) + "','" + str(tensionASistolica) + "','" + str(tensionAMedia) + "','" + str(temperatura) + "','" + str(saturacion) + "','" + str(glucometria) + "','" + str(glasgow) + "','" + str(apache) + "','" + str(pvc) + "','" + str(cuna)  + "','" + str(ic) + "','" + str(glasgowOcular) + "','" + str(glasgowVerbal) + "','" + str(glasgowMotora) + "','" + str(observacion) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(historiaId) +  "','" + str(username_id)   +   "')"
        print(detalle)
        cur3.execute(detalle)
        miConexion3.commit()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Signo Vital Creado!'})

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
