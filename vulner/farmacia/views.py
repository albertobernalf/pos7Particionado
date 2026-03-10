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
import json
import datetime
from django.utils import timezone
from datetime import date, timedelta
import time
from decimal import Decimal
from admisiones.models import Ingresos
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle, Conceptos, Suministros
from tarifarios.models import TarifariosDescripcion
from clinico.models import Servicios, EspecialidadesMedicos, Historia, HistoriaMedicamentos
from farmacia.models import FarmaciaEstados, Farmacia, FarmaciaDetalle
import io
import pandas as pd
from cirugia.models import EstadosCirugias, EstadosSalas, EstadosProgramacion, ProgramacionCirugias, Cirugias, ProgramacionCirugias
from clinico.models import UnidadesDeMedidaDosis, ViasAdministracion
from enfermeria.models import EnfermeriaDetalle
from contratacion.models import Convenios
from cartera.models import Pagos
from django.db.models import Min, Max, Avg
from django.db.models import F
from django.db import transaction, IntegrityError
from autorizaciones.models import EstadosAutorizacion
from farmacia.viewsReportes import ImprimirDespacho

# Create your views here.


def Load_dataFarmacia(request, data):
    print("Entre Load_dataFarmacia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    despachado = FarmaciaEstados.objects.get(nombre='DESPACHADO')


    farmacia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select far.id id,origen.nombre origen, mov.nombre mov , serv.nombre servicio, far.historia_id historia,far."ingresoPaciente" ingreso, est.nombre estado, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, servicios.nombre servicio, dep.nombre cama FROM farmacia_farmacia far INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id =  far."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id= far."tipoMovimiento_id") LEFT JOIN sitios_serviciosadministrativos serv ON (serv.id = far."serviciosAdministrativos_id") INNER JOIN farmacia_farmaciaEstados est ON (est.id=far.estado_id) INNER JOIN clinico_historia hist ON (hist.id = far.historia_id) INNER JOIN admisiones_ingresos adm ON (adm."tipoDoc_id" = hist."tipoDoc_id"  AND adm.documento_id = hist.documento_id AND adm.consec = hist."consecAdmision") INNER JOIN usuarios_usuarios usu ON (usu.id = adm.documento_id ) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = adm."tipoDoc_id")	 INNER JOIN sitios_dependencias dep ON (dep.id=adm."dependenciasActual_id")  INNER JOIN sitios_serviciossedes servicios ON servicios.id=adm."serviciosActual_id"  WHERE far."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND far.estado_id <> ' + "'" + str('0') + "' and adm.documento_id in (select dep.documento_id from sitios_dependencias dep where dep.documento_id=adm.documento_id and dep.disponibilidad= " + "'" + str('O') + "')"  + ' UNION  select far.id id,origen.nombre origen, mov.nombre mov , serv.nombre servicio, far.historia_id historia,far."ingresoPaciente" ingreso, est.nombre estado, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, servicios.nombre servicio, dep.nombre cama FROM farmacia_farmacia far INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id =  far."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id= far."tipoMovimiento_id") INNER JOIN sitios_serviciosadministrativos serv ON (serv.id = far."serviciosAdministrativos_id") INNER JOIN farmacia_farmaciaEstados est ON (est.id=far.estado_id) INNER JOIN admisiones_ingresos adm ON (adm.id= far."ingresoPaciente") INNER JOIN usuarios_usuarios usu ON (usu.id = adm.documento_id ) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = adm."tipoDoc_id") INNER JOIN sitios_dependencias dep ON (dep.id=adm."dependenciasActual_id")  INNER JOIN sitios_serviciossedes servicios ON servicios.id=adm."serviciosActual_id" WHERE far."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' and far.estado_id <> ' + "'" + str('0') + "'" + ' and adm.documento_id in (select dep.documento_id from sitios_dependencias dep where dep.documento_id=adm.documento_id and dep.disponibilidad= ' + "'" + str('O') + "')" + ' UNION select far.id id,origen.nombre origen, mov.nombre mov , serv.nombre servicio, far.historia_id historia,far."ingresoPaciente" ingreso, est.nombre estado, tipos.nombre tipoDoc, usu.documento documento, usu.nombre paciente, servicios.nombre servicio, ' + "'" + str('triage') + "'" + ' cama FROM farmacia_farmacia far INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id =  far."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id= far."tipoMovimiento_id")  INNER JOIN sitios_serviciosadministrativos serv ON (serv.id = far."serviciosAdministrativos_id") INNER JOIN farmacia_farmaciaEstados est ON (est.id=far.estado_id) INNER JOIN clinico_historia hist ON (hist.id = far.historia_id) INNER JOIN triage_triage tri ON (tri."tipoDoc_id" = hist."tipoDoc_id"  AND tri.documento_id = hist.documento_id AND tri.consec = hist."consecAdmision" and tri."consecAdmision"=0) INNER JOIN usuarios_usuarios usu ON (usu.id = tri.documento_id ) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id = tri."tipoDoc_id")  INNER JOIN sitios_serviciossedes servicios ON servicios.id=tri."serviciosSedes_id"'  +  ' WHERE far."sedesClinica_id" = ' + "'" + str(sede) + "'" + '  and far.estado_id <> ' + "'" + str('0') + "' and tri.documento_id in (select dep.documento_id from sitios_dependencias dep where dep.documento_id=tri.documento_id and dep.disponibilidad=" + "'" + str('O') + "')" + ' ORDER BY 6 desc'

    print(detalle)

    curx.execute(detalle)

    for id, origen, mov, servicio, historia, ingreso, estado, tipoDoc, documento,paciente, servicio,cama  in curx.fetchall():
        farmacia.append(
            {"model": "farmacia.farmacia", "pk": id, "fields":
                {'id': id, 'origen': origen, 'mov':mov, 'servicio': servicio, 'historia': historia ,'ingreso':ingreso, 'estado':estado,'tipoDoc':tipoDoc,'documento':documento, 'paciente':paciente, 'servicio':servicio, 'cama':cama }})

    miConexionx.close()
    print(farmacia)

    serialized1 = json.dumps(farmacia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataFarmaciaDetalle(request, data):
    print("Entre Load_dataFarmaciaDetalle")

    context = {}
    envioDatos = {}

    d = json.loads(data)

    farmaciaId = d['farmaciaId']

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    # Combo Datos Paciente

    datosPaciente = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select usu.id id,  hist."tipoDoc_id" tipoDoc, tipos.nombre nombreTipoDoc, usu.documento documento, usu.nombre paciente, hist."consecAdmision" consecutivoAdmision, serv.nombre servicio, dep.numero cama FROM farmacia_farmacia far INNER JOIN clinico_historia hist ON (hist.id = far.historia_id) INNER JOIN usuarios_usuarios usu ON (usu.id=hist.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=hist."tipoDoc_id") INNER JOIN admisiones_ingresos ingreso ON (ingreso."tipoDoc_id" =hist."tipoDoc_id" and ingreso.documento_id=hist.documento_id and ingreso.consec = hist."consecAdmision")  INNER Join sitios_dependencias dep on (dep.id=ingreso."dependenciasActual_id") INNER Join sitios_serviciossedes serv on (serv.id=ingreso."serviciosActual_id") where far.id= ' + "'" + str(farmaciaId) + "'"
    print(detalle)

    curx.execute(detalle)

    for id,tipoDoc,nombreTipoDoc, documento, paciente ,consecutivoAdmision, servicio, cama  in curx.fetchall():
        datosPaciente.append(
            {"model": "famacia.farmaciaDetalle1", "pk": id, "fields":
                {'id':id, 'tipoDoc': tipoDoc, 'nombreTipoDoc':nombreTipoDoc, 'documento': documento,'paciente':paciente,'consecutivoAdmision':consecutivoAdmision ,'servicio':servicio, 'cama':cama}})

    miConexionx.close()
    print(datosPaciente)


    # Fin Combo


    farmaciaDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select  det.id id,estados.nombre estadoNombre ,origen.nombre origenNombre, mov.nombre movNombre, sum.nombre || cums  suministro, 	det."dosisCantidad" dosis, dosis.descripcion unidadDosis,   vias.nombre via,	det."cantidadOrdenada" cantidad,  via.nombre viaAdministracion , det.despachado despachado FROM farmacia_farmacia far INNER JOIN farmacia_farmaciadetalle det ON (det.farmacia_id = far.id) LEFT JOIN farmacia_farmaciaestados estados  ON (estados.id = far.estado_id) INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id = far."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id = far."tipoOrigen_id") INNER JOIN facturacion_suministros sum ON (sum.id= det.suministro_id) INNER JOIN clinico_viasadministracion vias ON (vias.id= det."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis dosis ON (dosis.id= det."dosisUnidad_id") INNER JOIN clinico_viasadministracion via ON (via.id= det."viaAdministracion_id")  where far.id ='  + "'" + str(farmaciaId) + "' AND det.despachado = 'N' ORDER BY det.id"
    print(detalle)

    curx.execute(detalle)

    for id,estadoNombre, origenNombre,movNombre,suministro, dosis, unidadDosis, via, cantidad , viaAdministracion , despachado in curx.fetchall():
        farmaciaDetalle.append(
            {"model": "famacia.farmaciaDetalle", "pk": id, "fields":
                {'id': id, 'estadoNombre':estadoNombre, 'origenNombre': origenNombre ,'movNombre':movNombre,'suministro':suministro,'dosis':dosis ,'unidadDosis':unidadDosis ,'cantidad':cantidad , 'viaAdministracion':viaAdministracion, 'despachado':despachado}})

    miConexionx.close()
    print(farmaciaDetalle)

    envioDatos['datosPaciente'] = datosPaciente
    envioDatos['farmaciaDetalle'] = farmaciaDetalle

    print("envioDatos = " , envioDatos)

    serialized1 = json.dumps(farmaciaDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataFarmaciaDespachos(request, data):
    print("Entre Load_dataFarmaciaDespachos")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    farmaciaDetalleId = d['farmaciaDetalleId']
    farmaciaId = d['farmaciaId']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("farmaciaDetalleId:", farmaciaDetalleId)

    farmaciaDespachos = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select dispensa.id id, dispensa.despacho_id despacho , sum.nombre suministro, 	dispensa."dosisCantidad" dosis, dosis.descripcion unidadDosis,   vias.nombre via,	dispensa."cantidadOrdenada" cantidad FROM farmacia_farmaciadespachosdispensa dispensa INNER JOIN farmacia_farmaciaDetalle detalle ON (detalle.id = dispensa."farmaciaDetalle_id") INNER JOIN facturacion_suministros sum ON (sum.id= dispensa.suministro_id) INNER JOIN clinico_viasadministracion vias ON (vias.id= dispensa."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis dosis ON (dosis.id= dispensa."dosisUnidad_id") WHERE detalle.FARMACIA_ID=' + "'" + str(farmaciaId) + "' ORDER BY dispensa.id"

    print(detalle)

    curx.execute(detalle)

    for id,despacho, suministro, dosis, unidadDosis, via, cantidad in curx.fetchall():
        farmaciaDespachos.append(
            {"model": "famacia.farmaciadespachos", "pk": id, "fields":
                {'id': id, 'despacho':despacho, 'suministro': suministro ,'unidadDosis':unidadDosis, 'via':via, 'cantidad':cantidad  }})

    miConexionx.close()
    print(farmaciaDespachos)

    serialized1 = json.dumps(farmaciaDespachos, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataFarmaciaDespachosDispensa(request, data):
    print("Entre Load_dataFarmaciaDespachosDispensa")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    farmaciaDetalleId = d['farmaciaDetalleId']
    print("farmaciaDetalleId:", farmaciaDetalleId)
    farmaciaId = d['farmaciaId']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)


    farmaciaDespachosDispensa = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select dispensa.id id, dispensa.despacho_id despacho , sum.nombre||' + "' '||" + ' sum.cums suministro, 	dispensa."dosisCantidad" dosis, dosis.descripcion unidadDosis,   vias.nombre via,	dispensa."cantidadOrdenada" cantidad FROM farmacia_farmaciadespachosdispensa dispensa INNER JOIN farmacia_farmaciaDetalle detalle ON (detalle.id = dispensa."farmaciaDetalle_id" ) INNER JOIN facturacion_suministros sum ON (sum.id= dispensa.suministro_id) INNER JOIN clinico_viasadministracion vias ON (vias.id= dispensa."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis dosis ON (dosis.id= dispensa."dosisUnidad_id") WHERE detalle.farmacia_id =' + "'" + str(farmaciaId) + "'" + ' AND detalle.id = ' + "'" + str(farmaciaDetalleId) + "' ORDER BY dispensa.id"

    print(detalle)

    curx.execute(detalle)

    for id,despacho, suministro, dosis, unidadDosis, via, cantidad in curx.fetchall():
        farmaciaDespachosDispensa.append(
            {"model": "famacia.farmaciadespachosDispensa", "pk": id, "fields":
                {'id': id, 'despacho':despacho, 'suministro': suministro ,'dosis':dosis, 'unidadDosis':unidadDosis, 'via':via, 'cantidad':cantidad  }})

    miConexionx.close()
    print(farmaciaDespachosDispensa)

    serialized1 = json.dumps(farmaciaDespachosDispensa, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def BuscaDatosPaciente(request):
    print("Entre BuscaDatosPaciente")


    farmaciaId = request.POST['farmaciaId']
    print ("farmaciaId =", farmaciaId)
    hist = Farmacia.objects.get(id=farmaciaId)
    esTriage = Historia.objects.get(id=hist.historia_id)
    print("estriage =" , esTriage.consecAdmision)


    # Combo Datos Paciente

    datosPaciente = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    if (esTriage.consecAdmision !=0):

        detalle = 'select usu.id id,  hist."tipoDoc_id" tipoDoc, tipos.nombre nombreTipoDoc, usu.documento documento, usu.nombre paciente, hist."consecAdmision" consecutivoAdmision, serv.nombre servicio, dep.numero cama FROM farmacia_farmacia far INNER JOIN clinico_historia hist ON (hist.id = far.historia_id) INNER JOIN usuarios_usuarios usu ON (usu.id=hist.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=hist."tipoDoc_id") INNER JOIN admisiones_ingresos ingreso ON (ingreso."tipoDoc_id" =hist."tipoDoc_id" and ingreso.documento_id=hist.documento_id and ingreso.consec = hist."consecAdmision")  INNER Join sitios_dependencias dep on (dep.id=ingreso."dependenciasActual_id") INNER Join sitios_serviciossedes serv on (serv.id=ingreso."serviciosActual_id") where far.id= ' + "'" + str(farmaciaId) + "'"
    else:
        print("Entre TRIAGE")
        detalle = 'select usu.id id,  hist."tipoDoc_id" tipoDoc, tipos.nombre nombreTipoDoc, usu.documento documento, usu.nombre paciente, hist."consecAdmision" consecutivoAdmision, serv.nombre servicio, ' + "'" + str('TRIAGE') + "'" + ' cama FROM farmacia_farmacia far INNER JOIN clinico_historia hist ON (hist.id = far.historia_id) INNER JOIN usuarios_usuarios usu ON (usu.id=hist.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=hist."tipoDoc_id") INNER JOIN triage_triage tri ON (tri."tipoDoc_id" =hist."tipoDoc_id" and tri.documento_id=hist.documento_id and tri.consec = hist."consecAdmision")  INNER Join sitios_serviciossedes serv on (serv.id = tri."serviciosSedes_id") where far.id= ' + "'" + str(farmaciaId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id,tipoDoc,nombreTipoDoc, documento, paciente ,consecutivoAdmision, servicio, cama  in curx.fetchall():
        datosPaciente.append(
            {"model": "datosPaciente", "pk": id, "fields":
                {'id':id, 'tipoDoc': tipoDoc, 'nombreTipoDoc':nombreTipoDoc, 'documento': documento,'paciente':paciente,'consecutivoAdmision':consecutivoAdmision ,'servicio':servicio, 'cama':cama}})

    miConexionx.close()
    print(datosPaciente)

    # Fin Combo

    serialized1 = json.dumps(datosPaciente, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def AdicionarDespachosDispensa(request):

    print("Entre AdicionarDespachosDispensa")

    context = {}

    username = request.POST['username']
    sede = request.POST['sede']
    username_id = request.POST['username_id']
    farmaciaId = request.POST['farmaciaId']
    farmaciaDetalleId = request.POST['farmaciaDetalleId']
    print("farmaciaDetalleId = ", farmaciaDetalleId)

    servicioAdmonEntrega = request.POST['servicioAdmonEntrega']
    print("servicioAdmonEntrega:", servicioAdmonEntrega)
    servicioAdmonRecibe = request.POST['servicioAdmonRecibe']
    print("servicioAdmonRecibe:", servicioAdmonRecibe)
    plantaEntrega = request.POST['plantaEntrega']
    print("plantaEntrega:", plantaEntrega)

    plantaRecibe = request.POST['plantaRecibe']
    print("plantaRecibe:", plantaRecibe)

    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("farmaciaDetalleId:", farmaciaDetalleId)

    parcialDespachado = FarmaciaEstados.objects.get(nombre='PARCIALMENTE DESPACHADO')

    # Desde aqui

    # Busco la Historia
    farmacia = Farmacia.objects.get(id=farmaciaId)
    print("FARMACIA = ", farmacia.historia_id)

    if (farmacia.historia_id != ''):
        print ("Entre SOLICITUD DE MEDICAMENTOS")
        historia = Historia.objects.get(id=farmacia.historia_id)
        tipoDocId = historia.tipoDoc_id
        documentoId= historia.documento_id
        ingresoPaciente = historia.consecAdmision

    else:
        print ("Entre PEDIDO ENFERMERIA")
        ingre = Ingresos.objects.get(id=farmacia.ingresoPaciente)
        tipoDocId = ingre.tipoDoc_id
        documentoId= ingre.documento_id
        ingresoPaciente = ingre.consec



    print("tipoDocId:", tipoDocId)
    print("documentoId:", documentoId)
    print("ingresoPaciente:", ingresoPaciente)

    # Guarda en FarmaciaDespachos

    # Guarda en FarmaciaDespachosDispensa

    # Grabacion Formulacion

    formulacion = request.POST['formulacion']

    print("voy a validar Medicamentos =", formulacion)

    jsonFormulacion = json.loads(formulacion)

    print("voy para el FOR")

    print("voy a validar JSONMedicamentos =", jsonFormulacion)
    medicamentos= ""
    estadoReg = 'A'

    fechaRegistro = timezone.now()

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()
        # Primero creamos el despacho

        comando = 'INSERT INTO farmacia_farmaciadespachos ("fechaRegistro", "estadoReg",farmacia_id, "serviciosAdministrativosEntrega_id","usuarioEntrega_id", "usuarioRegistro_id","serviciosAdministrativosRecibe_id" , "usuarioRecibe_id") VALUES (' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(farmaciaId) + ",'" + str(servicioAdmonEntrega) + "','" + str(plantaEntrega) + "','" + str(username_id) + "','" +  str(servicioAdmonRecibe) + "','" +  str(plantaRecibe) + "') RETURNING id ;"
        print(comando)

        resultado = cur3.execute(comando)
        despachoId = cur3.fetchone()[0]

        print ("despachoId = ", despachoId)

        comando = 'UPDATE farmacia_farmacia SET estado_id = ' + "'" + str(parcialDespachado.id) + "' WHERE id = '" + str(farmaciaId) + "'"
        print(comando)

        cur3.execute(comando)

        ##############################################
        ##############################################
        ## DESDE AQUI CABEZOTE LIQUIDACION
        ## El UNICO PROBLEMA ES SI OPRIME DISMENSAR Y NMO VA NINGUN DESPACHO OJO CONTROLAR ESTO CON JAVASCRIPT EN EL MANI
        # Aqui rutina busca Convenio del Paciente

        convenioParticular = Convenios.objects.get(particular='S')
        print("convenioParticular =", convenioParticular)

        #comando = 'SELECT min(p.convenio_id) id FROM facturacion_conveniospacienteingresos p WHERE "tipoDoc_id" = ' + "'" + str(tipoDocId) + "'" + ' AND documento_id = ' + "'" + str(documentoId) + "'" + ' AND "consecAdmision" = ' + "'" + str(ingresoPaciente) + "'"
        comando = 'SELECT min(p.convenio_id) id FROM facturacion_conveniospacienteingresos p WHERE "tipoDoc_id" = ' + "'" + str(tipoDocId) + "'" + ' AND documento_id = ' + "'" + str(documentoId) + "'" + ' AND "consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND convenio_id != " + "'" + str(convenioParticular.id) + "'"
        cur3.execute(comando)

        print(comando)

        convenio = []

        for id in cur3.fetchall():
            convenio.append({'id': id})

        print("convenioId = ", convenio[0])

        convenioId = convenio[0]['id']
        convenioId = str(convenioId)
        print("convenioId = ", convenioId)

        convenioId = convenioId.replace("(", ' ')
        convenioId = convenioId.replace(")", ' ')
        convenioId = convenioId.replace(",", ' ')
        print("convenioId = ", convenioId)
        print("Tamalo de convenioId =", len(convenioId))

        convenioId = convenioId.strip()

        print("sin espacioos convenioId =", convenioId)

        if convenioId.strip() == 'None':
            convenioId = convenioParticular.id
            print("Entre a MODIFICAR convenioID")

            try:
                with transaction.atomic():

                    conveniospacienteingresos = ConveniosPacienteIngresos.objects.get(tipoDoc_id=tipoDocId,documento_id=documentoId, consecAdmision=ingresoPaciente, convenio_id=convenioParticular.id)

            except Exception as e:
                # Aquí ya se hizo rollback automáticamente
                print("Se hizo rollback por:", e)
                print("ppor aqui se le crea el convenio Particular al paciente")

                grabo88 = ConveniosPacienteIngresos(
                    tipoDoc_id=tipoDocId,
                    documento_id=documentoId,
                    consecAdmision=ingresoPaciente,
                    convenio_id=convenioParticular.id,
                    fechaRegistro=fechaRegistro,
                    usuarioRegistro_id=username_id,
                    estadoReg=estadoReg
                )
                grabo88.save()
                grabo88.id
                print("yA grabe", grabo88.id)

            finally:
                print("Cleanup operations or final logging.")


        print("ULTIMO valor de convenioId= ", convenioId)

        # Fin Rutina busca convenio del paciente

        # Validacion si existe o No existe CABEZOTE

        comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + "'" + str(tipoDocId) + "' AND documento_id = " + "'" + str(documentoId) + "'" + ' AND "consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND convenio_id = '" + str(convenioId) + "'"
        cur3.execute(comando)

        cabezoteLiquidacion = []

        for id in cur3.fetchall():
            cabezoteLiquidacion.append({'id': id})

        print("CABEZOTE DE LIQUIDACION = ", cabezoteLiquidacion);


        if (cabezoteLiquidacion == []):
            # Si no existe liquidacion CABEZOTE se debe crear con los totales, abonos, anticipos, procedimiento, suministros etc
            comando = 'INSERT INTO facturacion_liquidacion ("sedesClinica_id", "tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos", anulado) VALUES (' + "'" + str(sede) + "'," + "'" + str(tipoDocId) + "','" + str(documentoId) + "','" + str(ingresoPaciente) + "','" + str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(convenioId) + ',' + "'" + str(username_id) + "',0,'N') RETURNING id "
            cur3.execute(comando)
            liquidacionId = cur3.fetchone()[0]

            print("resultado liquidacionId = ", liquidacionId)

            # liquidacionU = Liquidacion.objects.all().aggregate(maximo=Coalesce(Max('id'), 0))
            # liquidacionId = (liquidacionU['maximo']) + 0
        else:
            liquidacionId = cabezoteLiquidacion[0]['id']
            liquidacionId = str(liquidacionId)
            print("liquidacionId = ", liquidacionId)

        liquidacionId = str(liquidacionId)
        liquidacionId = liquidacionId.replace("(", ' ')
        liquidacionId = liquidacionId.replace(")", ' ')
        liquidacionId = liquidacionId.replace(",", ' ')

        # Fin validacion de Liquidacion cabezote

        # Rutiva busca en convenio el valor de la tarifa CUPS
        print("liquidacionId = ", liquidacionId)

        # Aqui RUTINA busca consecutivo de liquidacion

        comando = 'SELECT (max(p.consecutivo) + 1) cons FROM facturacion_liquidaciondetalle p WHERE liquidacion_id = ' + liquidacionId

        cur3.execute(comando)

        print(comando)

        consecLiquidacion = []

        for cons in cur3.fetchall():
            consecLiquidacion.append({'cons': cons})

        print("consecLiquidacion = ", consecLiquidacion[0])

        consecLiquidacion = consecLiquidacion[0]['cons']
        consecLiquidacion = str(consecLiquidacion)
        print("consecLiquidacion = ", consecLiquidacion)

        consecLiquidacion = consecLiquidacion.replace("(", ' ')
        consecLiquidacion = consecLiquidacion.replace(")", ' ')
        consecLiquidacion = consecLiquidacion.replace(",", ' ')

        if consecLiquidacion.strip() == 'None':
            print("consecLiquidacion = ", consecLiquidacion)
            consecLiquidacion = 1

        # Fin RUTINA busca consecutivo de liquidacion

        # RUTINA encuentra columna de dondel LEER la tarifa.
        #
        try:
            with transaction.atomic():

                contratacion = Convenios.objects.get(id=convenioId)

                print("OJOO contratacion.tarifariosDescripcionProc_id = ", contratacion.tarifariosDescripcionSum_id)

                columnaALeer = TarifariosDescripcion.objects.get(id=contratacion.tarifariosDescripcionSum_id)
                columnaALeerPropia = columnaALeer.columna

        except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback de Convenio TarifarioDescripcion por:", e)
            error_data = {
                'type': type(e).__name__,
                'message': str(e),
                'traceback': traceback.format_exc()
            }
            columnaALeerPropia = ''

        finally:
            print("Finally")

        print("Columna a leer = ", columnaALeerPropia)

        ## FIN CABEZOTE DE LIQUIDACION
        #############################################
        ###############################################

        # Segundo creamos la dispensacion del despacho
        item = 0

        ## Aqui crear RUTINA para validar si hay algun medicamento que van a despachar que requeira Autorizacion y devolver e indicar al usuario

        ## Miercoles aqui deberia haber una rutina que lo envie a Autorizaciones No cree ?

        flagNoRequiereAut = 'N'
        autPendiente = EstadosAutorizacion.objects.get(nombre='PENDIENTE')


        for key in jsonFormulacion:

            if key["medicamentos"] != '':
                item = item +1
                print("Estoy recorriendo el jsonFormulacion")

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

                farmaciaDetalleId = key["farmaciaDetalleId"].strip()
                print("farmaciaDetalleId=", farmaciaDetalleId)


                #diasTratamiento = key["diasTratamiento"]
                #print("diasTratamiento=", diasTratamiento)

                #AQUI DEBO FILTRAR SI REQUIERE AUTORIZACION ENVIARLA A AUTORIZACIONES Y NO DESPACHAR
                ##Nop esta rutina PAILAS se queda enun loop indefinido de requiereautoriacion
                #no va

                requiereAut = Suministros.objects.get(id=medicamentos)
                print("requiereAut = " , requiereAut.requiereAutorizacion)

                ##FIN RUTINA ENVIO A AUTORIZACIONES Y DEBE SEQUIR CON EL SIGTE ITEM

                #if (requiereAut.requiereAutorizacion== 'S'):

                #    if (flagNoRequiereAut=='N'):
                        # Crea la Autorizacion
                #        comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id , convenio_id )  SELECT ' + "'" + str(autPendiente.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(username_id) + "','" + str(sede) + "','" + str(username_id) + "'," + "'" + str(historia.id) + "'" + ', conv.id FROM facturacion_conveniospacienteingresos convIngreso,  contratacion_convenios conv WHERE conv.id = ' + "'" + str(convenioId) + "'" + ' AND conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" + str(tipoDocId) + "' AND convIngreso.documento_id = " + "'" + str(documentoId) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = " + "'" + str(convenioId) + "'" + ' RETURNING id'

                #        cur3.execute(comando)
                #        autorizacionId = cur3.fetchone()[0]
                #        flagNoRequiereAut='S'

                #    else:
                        #Crea la autorizacionDetalle
                #        comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id", "valorSolicitado")  VALUES (' + "'" + str(autPendiente.id) + "'," + "'" + str(cantidadMedicamento) + "'" + ' ,0, now(),' + "'" + str('A') + "','" + str(autorizacionId) + "','" + str(username_id) + "'," + "'" + str(medicamentos) + "',null, " + "null," + "'" + str('0') + "'" + ')'

                #        print("comando=", comando)
                #        cur3.execute(comando)

                    # no lo carga al despacho
                 #   continue

                # Busco historialMediamentos

                farmaciaDetalle = FarmaciaDetalle.objects.get(id=farmaciaDetalleId)

                if (farmacia.historia_id == None):
                    historiaMedicamentos = 'null'
                else:
                    historiaMedicamentos = HistoriaMedicamentos.objects.get(id=farmaciaDetalle.historiaMedicamentos_id)


                comando = 'INSERT INTO farmacia_farmaciadespachosdispensa ("dosisCantidad","cantidadOrdenada","fechaRegistro", "estadoReg",despacho_id, "dosisUnidad_id", "farmaciaDetalle_id", "suministro_id","usuarioRegistro_id", "viaAdministracion_id")  VALUES ( ' + "'" + str(dosis) + "','" + str(cantidadMedicamento) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(despachoId) + "','" + str(MedidaDosis.id) + "','" + str(farmaciaDetalleId) + "','" + str(medicamentos) + "','" + str(username_id) + "','" + str(vias.id) +  "') RETURNING id"

                print(comando)
                resultado = cur3.execute(comando)

                farmaciaDespachosDispensaId = cur3.fetchone()[0]

                # Tercero creamos lo que Enfermeria recibe
                print("farmaciaDetalleId =", farmaciaDetalleId)

                enfermeriaDetalleId = EnfermeriaDetalle.objects.get(farmaciaDetalle_id=farmaciaDetalleId)
                #print("vias =", vias)

                comando = 'INSERT INTO enfermeria_enfermeriarecibe ("dosisCantidad","cantidadDispensada","fechaRegistro", "estadoReg", "dosisUnidad_id", "enfermeriaDetalle_id", "suministro_id","usuarioRegistro_id", "viaAdministracion_id",despachos_id, "farmaciaDetalle_id", "farmaciaDespachosDispensa_id",anulado)  VALUES ( ' + "'" + str(dosis) + "','" + str(cantidadMedicamento) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(MedidaDosis.id) + "','" + str(enfermeriaDetalleId.id) + "','" + str(medicamentos) + "','" + str(username_id) + "','" + str(vias.id) + "','"  + str(despachoId) + "','"  + str(farmaciaDetalleId) + "','" + str(farmaciaDespachosDispensaId) +  "','N')"
                print(comando)
                cur3.execute(comando)

                # Cuarto cargamos a la cuenta del paciente


                ## Desde Aqui rutina de Facturacion Para Medicamentos
                #

                miConexiont = None
                try:
                    if (columnaALeerPropia != ''):

                        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",
                                                       user="postgres", password="123456")

                        curt = miConexiont.cursor()
                        # comando = 'SELECT conv.convenio_id id ,exa."codigoCups" cups, proc."' + str(columnaALeer.columna) + '"' + ' valor FROM facturacion_conveniospacienteingresos conv, tarifarios_tarifariosdescripcion des, tarifarios_tarifariosprocedimientos proc, clinico_examenes exa, contratacion_convenios conv1 , tarifarios_tipostarifa tiptar WHERE conv."tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "'" + ' AND conv.documento_id = ' + "'" + str(documentoId.id) + "'" + ' AND conv."consecAdmision" = ' + "'" + str(ingresoPaciente) + "'" + ' AND conv.convenio_id = conv1.id AND des.id = conv1."tarifariosDescripcionProc_id" AND proc."codigoCups_id" = exa.id  And exa.id = ' + "'" + str(codigoCupsId[0].id) + "'" + ' AND des."tiposTarifa_id" = tiptar.id and proc."tiposTarifa_id" = tiptar.id'
                        comando = 'SELECT conv.convenio_id id ,exa.cums cums, sum."' + str(columnaALeer.columna) + '"' + ' tarifaValor FROM facturacion_conveniospacienteingresos conv, tarifarios_tarifariosdescripcion des, tarifarios_tarifariossuministros sum, facturacion_suministros exa, contratacion_convenios conv1 , tarifarios_tipostarifa tiptar WHERE conv."tipoDoc_id" = ' + "'" + str(tipoDocId) + "'" + ' AND conv.documento_id = ' + "'" + str(documentoId) + "'" + ' AND conv."consecAdmision" = ' + "'" + str(ingresoPaciente) + "'" + ' AND conv.convenio_id = conv1.id AND des.id = conv1."tarifariosDescripcionSum_id" AND sum."codigoCum_id" = exa.id  And exa.id = ' + "'" + str(medicamentos) + "'" + ' AND des."tiposTarifa_id" = tiptar.id and sum."tiposTarifa_id" = tiptar.id'

                        print("comando = ", comando)
                        curt.execute(comando)

                        convenioValor = []

                        for id, sum, tarifaValor in curt.fetchall():
                            convenioValor.append({'id': id, 'sum': sum, 'valor': tarifaValor})

                        miConexiont.close()
                    else:
                        convenioValor = []

                    print("columnaALeer.columna", columnaALeerPropia)
                    print("convenioValor = ", convenioValor)
                    #print("convenioValor[0].sum = ", convenioValor[0].sum)


                except psycopg2.DatabaseError as error:
                    print("Entre por rollback", error)
                    if miConexiont:
                        print("Entro ha hacer el Rollback")
                        miConexiont.rollback()
                        tarifaValor = 0

                finally:
                    if miConexiont:
                        curt.close()
                        miConexiont.close()

                if (convenioValor != []):

                    print("Sum = ", convenioValor[0]['sum'])
                    tarifaValor = convenioValor[0]['valor']
                    tarifaValor = str(tarifaValor)
                    print("tarifaValor = ", tarifaValor)
                    tarifaValor = tarifaValor.replace("None", ' ')
                    tarifaValor = tarifaValor.replace("(", ' ')
                    tarifaValor = tarifaValor.replace(")", ' ')
                    tarifaValor = tarifaValor.replace(",", ' ')
                    tarifaValor = tarifaValor.replace(" ", '')
                    print("tarifaValor = ", tarifaValor)

                else:
                    tarifaValor = 0

                if tarifaValor == '':
                    print("Entre cambiar tarufa Valor", tarifaValor)
                    tarifaValor = 0

                TotalTarifa = float(tarifaValor) * float(cantidadMedicamento)
                print("consecLiquidacion LISTO= ", consecLiquidacion)

                # Aqui Rutina FACTURACION crea en liquidaciondetalle el registro con la tarifa, con campo cups y convenio
                #

                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia_id,"fechaCrea", "fechaRegistro", "estadoRegistro", "cums_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "historiaMedicamento_id",anulado) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str(cantidadMedicamento) + "','" + str(tarifaValor) + "','" + str(TotalTarifa) + "',null,'" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(medicamentos) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + str(historiaMedicamentos.id)  + ",'N')"
                print("comando ", comando)

                cur3.execute(comando)

                consecLiquidacion = int(consecLiquidacion) + 1


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        ## FIN rutina de Facturacion Para Medicamentos Total

        ## OJOOOO
        ## AQUI FALTA UN except




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


    ## Vamops a actualizar los totales de la Liquidacion:

    totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(examen_id=None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
    totalSuministros = (totalSuministros['totalS']) + 0
    print("totalSuministros", totalSuministros)
    totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(cums_id=None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
    totalProcedimientos = (totalProcedimientos['totalP']) + 0
    print("totalProcedimientos", totalProcedimientos)
    registroPago = Liquidacion.objects.get(id=liquidacionId)

    # Continua Aqui

    totalCopagos = Pagos.objects.all().filter(tipoDoc_id=tipoDocId).filter(documento_id=documentoId).filter(consec=ingresoPaciente).filter(formaPago_id=4).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalC=Coalesce(Sum('valorEnCurso'), 0))
    totalCopagos = (totalCopagos['totalC']) + 0
    print("totalCopagos", totalCopagos)
    totalCuotaModeradora = Pagos.objects.all().filter(tipoDoc_id=tipoDocId).filter(documento_id=documentoId).filter(consec=ingresoPaciente).filter(formaPago_id=3).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalM=Coalesce(Sum('valorEnCurso'), 0))
    totalCuotaModeradora = (totalCuotaModeradora['totalM']) + 0
    print("totalCuotaModeradora", totalCuotaModeradora)
    totalAnticipos = Pagos.objects.all().filter(tipoDoc_id=tipoDocId).filter(documento_id=documentoId).filter(consec=ingresoPaciente).filter(formaPago_id=1).exclude(estadoReg='I').exclude(anulado='S').aggregate(Anticipos=Coalesce(Sum('valorEnCurso'), 0))
    totalAnticipos = (totalAnticipos['Anticipos']) + 0
    print("totalAnticipos", totalAnticipos)
    totalAbonos = Pagos.objects.all().filter(tipoDoc_id=tipoDocId).filter(documento_id=documentoId).filter(consec=ingresoPaciente).filter(formaPago_id=2).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalAb=Coalesce(Sum('valorEnCurso'), 0))
    totalAbonos = (totalAbonos['totalAb']) + 0
    # totalAbonos = totalCopagos + totalAnticipos + totalCuotaModeradora
    print("totalAbonos", totalAbonos)

    totalRecibido = totalCopagos + totalCuotaModeradora + totalAnticipos + totalAbonos
    totalApagar = totalSuministros + totalProcedimientos - totalRecibido
    totalLiquidacion = totalSuministros + totalProcedimientos
    print("totalLiquidacion", totalLiquidacion)
    print("totalAPagar", totalApagar)

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",
                                       user="postgres", password="123456")
        cur3 = miConexion3.cursor()
        # Primero creamos el despacho

        comando = 'INSERT INTO farmacia_farmaciadespachos ("fechaRegistro", "estadoReg",farmacia_id, "serviciosAdministrativosEntrega_id","usuarioEntrega_id", "usuarioRegistro_id","serviciosAdministrativosRecibe_id" , "usuarioRecibe_id") VALUES (' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(farmaciaId) + ",'" + str(servicioAdmonEntrega) + "','" + str(plantaEntrega) + "','" + str(username_id) + "','" +  str(servicioAdmonRecibe) + "','" +  str(plantaRecibe) + "') RETURNING id ;"
        print(comando)
        # Rutina Guarda en cabezote los totales

        print("Voy a grabar el cabezote")

        comando = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + "'" + str(totalSuministros) + "'" + ',"totalProcedimientos" = ' + "'" + str(totalProcedimientos) + "'"  + ', "totalCopagos" = ' + "'"  + str(totalCopagos) + "'" + ' , "totalCuotaModeradora" = ' + "'"  + str(totalCuotaModeradora) + "'"  + ', anticipos = ' + "'" + str(totalAnticipos) + "'" + ' ,"totalAbonos" = ' + "'" + str(totalAbonos) + "'"  + ', "totalLiquidacion" = ' + "'" + str(totalLiquidacion) + "'" + ', "valorApagar" = ' + "'"  + str(totalApagar) + "'" + ', "totalRecibido" = ' + "'" + str(totalRecibido) + "'" + ' WHERE id =' + str(liquidacionId)
        cur3.execute(comando)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        # Por ultimo imprime el Despacho

        print("Entre imprimir despacho salida", despachoId)
        ImprimirDespacho(farmaciaId, despachoId)

        print("Ya imprimi orden de control")

        return JsonResponse({'success': True, 'Mensajes': 'Despacho creado satisfactoriamente!' })

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


    # Creo eso es todop


def CambiaEstadoDespacho(request):
    print("Entre CambiaEstadoDespacho")

    farmaciaId = request.POST['farmaciaId']
    print ("farmaciaId =", farmaciaId)

    estadoFarmaciaDespacho = request.POST['estadoFarmaciaDespacho']
    print ("estadoFarmaciaDespacho =", estadoFarmaciaDespacho)


    #Actualiza estado despacho
    estadoDespachado = FarmaciaEstados.objects.get(nombre='DESPACHADO')

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'UPDATE farmacia_farmacia SET estado_id = ' + "'" + str(estadoFarmaciaDespacho) + "' WHERE id = " + "'"  + str(farmaciaId) + "'"
        print(detalle)
        cur3.execute(detalle)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Despacho actualizado !'})

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


def Load_dataDespachosFarmacia(request, data):
    print("Entre Load_dataDespachosFarmacia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    farmaciaId = d['farmaciaId']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)


    fechaRegistro = timezone.now()
    haceUnMes = fechaRegistro - datetime.timedelta(days=90)
    print(" haceUnMes = ", haceUnMes)



    año_actual = fechaRegistro.year  # Puedes cambiar este valor
    #fechaRegistro = date(año_actual, 1, 1)

    print(fechaRegistro)

    despachosFarmacia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    #detalle = 'select desp.id id, desp.id despacho,serv1.nombre servEntrega ,  pla1.nombre entrega , serv2.nombre servRecibe, pla2.nombre recibe FROM farmacia_farmaciadespachos desp INNER JOIN farmacia_farmacia far ON (far.id = desp.farmacia_id and far."sedesClinica_id" = ' + "'" + str(sede) + "'" + ')  LEFT JOIN sitios_serviciosadministrativos serv1 ON (serv1.id = desp."serviciosAdministrativosEntrega_id") LEFT JOIN sitios_serviciosadministrativos serv2 ON (serv2.id = desp."serviciosAdministrativosRecibe_id") LEFT JOIN planta_planta pla1 ON (pla1.id = desp."usuarioEntrega_id") LEFT JOIN planta_planta pla2 ON (pla2.id = desp."usuarioRecibe_id") WHERE desp."fechaRegistro" >= ' + "'" + str(haceUnMes) + "'"
    detalle = 'select desp.id id, desp.id despacho,serv1.nombre servEntrega ,  pla1.nombre entrega , serv2.nombre servRecibe, pla2.nombre recibe FROM farmacia_farmaciadespachos desp INNER JOIN farmacia_farmacia far ON (far.id = desp.farmacia_id and far."sedesClinica_id" = ' + "'" + str(sede) + "'" + ')  LEFT JOIN sitios_serviciosadministrativos serv1 ON (serv1.id = desp."serviciosAdministrativosEntrega_id") LEFT JOIN sitios_serviciosadministrativos serv2 ON (serv2.id = desp."serviciosAdministrativosRecibe_id") LEFT JOIN planta_planta pla1 ON (pla1.id = desp."usuarioEntrega_id") LEFT JOIN planta_planta pla2 ON (pla2.id = desp."usuarioRecibe_id") WHERE desp.farmacia_id = ' + "'" + str(farmaciaId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, despacho, servEntrega, entrega, servRecibe, recibe  in curx.fetchall():
        despachosFarmacia.append(
            {"model": "farmacia.farmaciaDespachos", "pk": id, "fields":
                {'id': id, 'despacho': despacho, 'servEntrega':servEntrega, 'entrega': entrega, 'servRecibe': servRecibe ,'recibe':recibe  }})

    miConexionx.close()
    print(despachosFarmacia)

    serialized1 = json.dumps(despachosFarmacia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataDespachosDetalleFarmacia(request, data):
    print("Entre Load_dataDespachosDetalleFarmacia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    despachoId = d['despachoId']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    fechaRegistro = datetime.datetime.now()
    fechaRegistro = timezone.now()

    despachosDetalleFarmacia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select disp.id id ,disp."dosisCantidad" dosis, med.descripcion  unidadMedida, disp."cantidadOrdenada" cantidad , sum.nombre suministro FROM farmacia_farmaciadespachos desp INNER JOIN farmacia_farmaciadespachosdispensa disp ON (disp.despacho_id = desp.id) LEFT JOIN sitios_serviciosadministrativos serv1 ON (serv1.id = desp."serviciosAdministrativosEntrega_id") LEFT JOIN sitios_serviciosadministrativos serv2 ON (serv2.id = desp."serviciosAdministrativosRecibe_id") LEFT JOIN planta_planta pla1 ON (pla1.id = desp."usuarioEntrega_id") LEFT JOIN planta_planta pla2 ON (pla2.id = desp."usuarioRecibe_id") INNER JOIN clinico_unidadesdemedidadosis med ON (med.id = disp."dosisUnidad_id") INNER JOIN facturacion_suministros sum ON (sum.id = disp.suministro_id) WHERE disp.despacho_id = ' + "'" + str(despachoId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, dosis, unidadMedida, cantidad, suministro  in curx.fetchall():
        despachosDetalleFarmacia.append(
            {"model": "farmacia.farmaciaDespachosDetalle", "pk": id, "fields":
                {'id': id, 'dosis': dosis, 'unidadMedida':unidadMedida, 'cantidad': cantidad, 'suministro': suministro}})

    miConexionx.close()
    print(despachosDetalleFarmacia)

    serialized1 = json.dumps(despachosDetalleFarmacia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataDevolucionesFarmacia(request, data):
    print("Entre Load_dataDevolucionesFarmacia")

    context = {}
    d = json.loads(data)

    despachoId = d['despachoId']
    print("despachoId =" , despachoId)

    fechaRegistro = timezone.now()


    año_actual = fechaRegistro.year  # Puedes cambiar este valor
    fechaRegistro = date(año_actual, 1, 1)

    print(fechaRegistro)

    devolucionesFarmacia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    #detalle = 'select dev.id, dev."fechaRegistro" fechaRegistro ,servDevuelve.nombre servicioDevuelve,plantaDevuelve.nombre usuarioDevuelve,servRecibe.nombre servicioRecibe,plantaRecibe.nombre usuarioRecibe FROM farmacia_farmaciadevolucion dev INNER JOIN sitios_serviciosadministrativos servDevuelve ON (servDevuelve.id = dev."serviciosAdministrativosDevuelve_id") LEFT JOIN 	sitios_serviciosadministrativos servRecibe ON (servRecibe.id = dev."serviciosAdministrativosRecibe_id" ) INNER JOIN planta_planta plantaDevuelve  ON (plantaDevuelve.id = dev."usuarioDevuelve_id") LEFT JOIN planta_planta plantaRecibe ON (plantaRecibe.id = dev."usuarioRecibe_id") WHERE dev."fechaRegistro" >=' + "'" + str(fechaRegistro) + "'" + ' order by dev.id'
    detalle = 'select dev.id, dev."fechaRegistro" fechaRegistro ,servDevuelve.nombre servicioDevuelve,plantaDevuelve.nombre usuarioDevuelve, servRecibe.nombre servicioRecibe,plantaRecibe.nombre usuarioRecibe FROM farmacia_farmaciadevolucion dev INNER JOIN farmacia_farmaciadevoluciondetalle devDetalle ON (devDetalle."farmaciaDevolucion_id" = dev.id) INNER JOIN farmacia_farmaciadespachosdispensa dispensa ON (dispensa.id = devDetalle."farmaciaDespachosDispensa_id") INNER JOIN farmacia_farmaciadespachos despacho ON (despacho.id = dispensa.despacho_id  ) INNER JOIN sitios_serviciosadministrativos servDevuelve ON (servDevuelve.id = dev."serviciosAdministrativosDevuelve_id") LEFT JOIN 	sitios_serviciosadministrativos servRecibe ON (servRecibe.id = dev."serviciosAdministrativosRecibe_id" ) INNER JOIN planta_planta plantaDevuelve  ON (plantaDevuelve.id = dev."usuarioDevuelve_id")  LEFT JOIN planta_planta plantaRecibe ON (plantaRecibe.id = dev."usuarioRecibe_id") WHERE  despacho.id=' + "'" + str(despachoId) + "'	order by dev.id"

    print(detalle)

    curx.execute(detalle)

    for id, fechaRegistro, servicioDevuelve, usuarioDevuelve, servicioRecibe,  usuarioRecibe in curx.fetchall():
            devolucionesFarmacia.append({"model": "farmacia.devoluciones", "pk": id, "fields":
                {'id': id, 'fechaRegistro': fechaRegistro, 'servicioDevuelve': servicioDevuelve, 'usuarioDevuelve': usuarioDevuelve,
                 'servicioRecibe': servicioRecibe,   'usuarioRecibe': usuarioRecibe}})

    miConexionx.close()
    print("devolucionesFarmacia = " , devolucionesFarmacia)


    serialized1 = json.dumps(devolucionesFarmacia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataDevolucionesDetalleFarmacia(request, data):
    print("Entre Load_dataDevolucionesDetalleFarmacia")

    context = {}
    d = json.loads(data)

    devolucionFarmaciaId = d['devolucionFarmaciaId']

    print ("devolucionFarmaciaId =", devolucionFarmaciaId)

    devolucionesDetalleFarmacia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT devdet.id id,	sum.nombre medicamento,dispensa."dosisCantidad" dosis, medida.descripcion unidadMedida, via.nombre via , dispensa."cantidadOrdenada" cantidad, devdet."cantidadDevuelta"	 cantidadDevuelta , devdet.observaciones observaciones FROM farmacia_farmaciadevoluciondetalle devdet INNER JOIN	farmacia_farmaciadespachosdispensa dispensa ON (dispensa.id = devdet."farmaciaDespachosDispensa_id") INNER JOIN facturacion_suministros sum ON (sum.id = dispensa.suministro_id) INNER JOIN clinico_viasadministracion via ON (via.id = dispensa."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis medida ON (medida.id = dispensa."dosisUnidad_id") WHERE devdet."farmaciaDevolucion_id" = ' + "'" + str(devolucionFarmaciaId) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, medicamento, dosis, unidadMedida, via,  cantidad, cantidadDevuelta, observaciones in curx.fetchall():
            devolucionesDetalleFarmacia.append({"model": "farmacia.devolucionesdetalle", "pk": id, "fields":
                {'id': id, 'medicamento': medicamento, 'dosis': dosis, 'unidadMedida': unidadMedida,
                 'via': via,   'cantidad': cantidad, 'cantidadDevuelta':cantidadDevuelta, 'bservaciones':observaciones}})

    miConexionx.close()
    print("devolucionesDetalleFarmacia = " , devolucionesDetalleFarmacia)


    serialized1 = json.dumps(devolucionesDetalleFarmacia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def RecibirDevolucionFarmacia(request):
    print("Entre RecibirDevolucionFarmacia")

    username_id = request.POST['username_id']
    print ("username_id =", username_id)
    sede = request.POST['sede']
    print ("sede =", sede)
    devolucionFarmaciaId = request.POST['devolucionFarmaciaId']
    print ("devolucionFarmaciaId =", devolucionFarmaciaId)
    servicioRecibeId = request.POST['servicioRecibeId']
    print ("servicioRecibeId =", servicioRecibeId)
    plantaRecibeId = request.POST['plantaRecibeId']
    print ("plantaRecibeId =", plantaRecibeId)

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'UPDATE farmacia_farmaciadevolucion SET "serviciosAdministrativosRecibe_id" = ' + "'" + str(servicioRecibeId) + "'," + ' "usuarioRecibe_id" = ' + "'" + str(plantaRecibeId) + "'" + ' WHERE id = ' + "'" + str(devolucionFarmaciaId) + "'"
        print(detalle)

        cur3.execute(detalle)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Recibida Devolucion Actualizada!'})

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



def RecibirDevolucionDetalleFarmacia(request):
    print("Entre RecibirDevolucionDetalleFarmacia")

    username_id = request.POST['username_id']
    print ("username_id =", username_id)
    sede = request.POST['sede']
    print ("sede =", sede)
    devolucionDetalleFarmaciaId = request.POST['devolucionDetalleFarmaciaId']
    print ("devolucionDetalleFarmaciaId =", devolucionDetalleFarmaciaId)
    cantidadDevueltaRecibida = request.POST['cantidadDevueltaRecibida']
    print ("cantidadDevueltaRecibida =", cantidadDevueltaRecibida)


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'UPDATE farmacia_farmaciadevoluciondetalle SET "cantidadDevueltaRecibida" = ' + "'" + str(cantidadDevueltaRecibida) + "'" + ' WHERE id = ' + "'" + str(devolucionDetalleFarmaciaId) + "'"
        print(detalle)

        cur3.execute(detalle)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Recibida Devolucion Detalle Actualizada!'})

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


def DespachadoFarmaciaDetalle(request):
    print("Entre DespachadoFarmaciaDetalle")

    farmaciaDetalleId = request.POST['farmaciaDetalleId']
    print ("farmaciaDetalleId =", farmaciaDetalleId)


    farmaciaDetalle = FarmaciaDetalle.objects.filter(id=farmaciaDetalleId)
    farmacia = FarmaciaDetalle.objects.filter(farmacia_id=farmaciaDetalle.farmacia_id)
    pendientes = FarmaciaDetalle.objects.filter(farmacia_id=farmaciaDetalle.farmacia_id, despachado='N').count()
    estadosFarmacia = FarmaciaEstados.objects.get(nombre='DESPACHADO')

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'UPDATE farmacia_farmaciadetalle SET despachado = ' + "'" + str('S') + "'" + ' WHERE id = ' + str(farmaciaDetalleId)
        print(detalle)
        cur3.execute(detalle)

        if (pendientes == 0):
                detalle = 'UPDATE farmacia_farmacia SET despachado = ' + "'" + str(estadosFarmacia.id) + "'" + ' WHERE id = ' + str(farmacia.id)
                print(detalle)
                cur3.execute(detalle)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Item de Farmacia Despachado!'})

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




def Load_dataFarmaciaDetalleOrdenados(request, data):
    print("Entre Load_dataFarmaciaDetalleOrdenados")

    context = {}
    envioDatos = {}

    d = json.loads(data)

    farmaciaId = d['farmaciaId']

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    # Combo Datos Paciente

    datosPaciente = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select usu.id id,  hist."tipoDoc_id" tipoDoc, tipos.nombre nombreTipoDoc, usu.documento documento, usu.nombre paciente, hist."consecAdmision" consecutivoAdmision, serv.nombre servicio, dep.numero cama FROM farmacia_farmacia far INNER JOIN clinico_historia hist ON (hist.id = far.historia_id) INNER JOIN usuarios_usuarios usu ON (usu.id=hist.documento_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=hist."tipoDoc_id") INNER JOIN admisiones_ingresos ingreso ON (ingreso."tipoDoc_id" =hist."tipoDoc_id" and ingreso.documento_id=hist.documento_id and ingreso.consec = hist."consecAdmision")  INNER Join sitios_dependencias dep on (dep.id=ingreso."dependenciasActual_id") INNER Join sitios_serviciossedes serv on (serv.id=ingreso."serviciosActual_id") where far.id= ' + "'" + str(farmaciaId) + "'"
    print(detalle)

    curx.execute(detalle)

    for id,tipoDoc,nombreTipoDoc, documento, paciente ,consecutivoAdmision, servicio, cama  in curx.fetchall():
        datosPaciente.append(
            {"model": "famacia.farmaciaDetalle1", "pk": id, "fields":
                {'id':id, 'tipoDoc': tipoDoc, 'nombreTipoDoc':nombreTipoDoc, 'documento': documento,'paciente':paciente,'consecutivoAdmision':consecutivoAdmision ,'servicio':servicio, 'cama':cama}})

    miConexionx.close()
    print(datosPaciente)


    # Fin Combo


    farmaciaDetalle = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select  det.id id,estados.nombre estadoNombre ,origen.nombre origenNombre, mov.nombre movNombre, sum.nombre || cums  suministro, 	det."dosisCantidad" dosis, dosis.descripcion unidadDosis,   vias.nombre via,	det."cantidadOrdenada" cantidad,  via.nombre viaAdministracion , det.despachado despachado FROM farmacia_farmacia far INNER JOIN farmacia_farmaciadetalle det ON (det.farmacia_id = far.id) LEFT JOIN farmacia_farmaciaestados estados  ON (estados.id = far.estado_id) INNER JOIN enfermeria_enfermeriatipoorigen origen ON (origen.id = far."tipoOrigen_id") INNER JOIN enfermeria_enfermeriatipomovimiento mov ON (mov.id = far."tipoOrigen_id") INNER JOIN facturacion_suministros sum ON (sum.id= det.suministro_id) INNER JOIN clinico_viasadministracion vias ON (vias.id= det."viaAdministracion_id") INNER JOIN clinico_unidadesdemedidadosis dosis ON (dosis.id= det."dosisUnidad_id") INNER JOIN clinico_viasadministracion via ON (via.id= det."viaAdministracion_id")  where far.id ='  + "'" + str(farmaciaId) + "' ORDER BY det.id"
    print(detalle)

    curx.execute(detalle)

    for id,estadoNombre, origenNombre,movNombre,suministro, dosis, unidadDosis, via, cantidad , viaAdministracion , despachado in curx.fetchall():
        farmaciaDetalle.append(
            {"model": "famacia.farmaciaDetalle", "pk": id, "fields":
                {'id': id, 'estadoNombre':estadoNombre, 'origenNombre': origenNombre ,'movNombre':movNombre,'suministro':suministro,'dosis':dosis ,'unidadDosis':unidadDosis ,'cantidad':cantidad , 'viaAdministracion':viaAdministracion, 'despachado':despachado}})

    miConexionx.close()
    print(farmaciaDetalle)

    envioDatos['datosPaciente'] = datosPaciente
    envioDatos['farmaciaDetalle'] = farmaciaDetalle

    print("envioDatos = " , envioDatos)

    serialized1 = json.dumps(farmaciaDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')
