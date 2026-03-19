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
#from datetime import date
#from datetime import timezone

import time
from datetime import date, timedelta
import time
from decimal import Decimal
from admisiones.models import Ingresos
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle, Conceptos, Suministros , TiposSuministro
from cartera.models import TiposPagos, FormasPagos, Pagos, PagosFacturas, Glosas
from triage.models import Triage
from clinico.models import Servicios, EspecialidadesMedicos, TiposFolio, Historia
from rips.models import RipsTransaccion, RipsUsuarios, RipsEnvios, RipsDetalle, RipsTiposNotas
from tarifarios.models import TiposTarifa, TiposTarifaProducto, TiposHonorarios, TarifariosDescripcionHonorarios ,MinimosLegales
import io
import pandas as pd
from cirugia.models import EstadosCirugias, EstadosSalas, EstadosProgramacion, ProgramacionCirugias, Cirugias, ProgramacionCirugias
from contratacion.models import Convenios
from django.db.models import Min, Max, Avg
from django.db.models import F
from django.db import transaction, IntegrityError
from django.utils import timezone
from contratacion.models import  ConveniosLiquidacionTarifasHonorarios
from tarifarios.models import TarifariosDescripcion , TiposHonorarios
from cirugia import viewsReportes


# Create your views here.


def Load_dataProgramacionCirugia(request, data):
    print("Entre Load_dataProgramacionCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    estadoProgramacion = EstadosProgramacion.objects.get(nombre='Solicitud')
    estadoProgramacionRealizada = EstadosProgramacion.objects.get(nombre='Realizada')
    #estadoCirugiaSinAsignar = EstadosCirugias.objects.get(nombre='SIN ASIGNAR')
    estadoCirugiaPendiente = EstadosCirugias.objects.get(nombre='PENDIENTE')
    estadoCirugiaConfirmada = EstadosCirugias.objects.get(nombre='CONFIRMADA')
    estadoCirugiaRealizada = EstadosCirugias.objects.get(nombre='REALIZADA')



    programacionCirugias = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT prog.id id,  u."tipoDoc_id" tipoDoc_id ,tipdoc.abreviatura abrev, u.documento documento, i.consec consecutivo, u.nombre paciente,estprog.nombre estadoProg,sala.numero, sala.nombre sala, prog."fechaProgramacionInicia" inicia, prog."horaProgramacionInicia" horaInicia, prog."fechaProgramacionFin" Termina, prog."horaProgramacionFin" horaTermina ,(SELECT exa.nombre FROM cirugia_cirugias cir LEFT JOIN cirugia_cirugiasprocedimientos cirproc on (cirproc.cirugia_id = cir.id) INNER JOIN clinico_examenes exa on (exa.id = cirproc.cups_id) WHERE cir."tipoDoc_id" = prog."tipoDoc_id" and cir.documento_id = prog.documento_id  and cir."consecAdmision" = prog."consecAdmision" limit 1) cirugias , estcir.nombre estadoCirugia FROM cirugia_programacioncirugias prog INNER JOIN sitios_sedesclinica sed	on (sed.id = prog."sedesClinica_id") INNER JOIN admisiones_ingresos i ON (i."tipoDoc_id" =prog."tipoDoc_id" AND i.documento_id =  prog.documento_id AND i.consec= prog."consecAdmision" )  LEFT JOIN cirugia_cirugias cir ON (cir."tipoDoc_id" =prog."tipoDoc_id" AND cir.documento_id =  prog.documento_id AND cir."consecAdmision" = prog."consecAdmision" )  INNER JOIN cirugia_estadoscirugias estcir ON (estcir.id = cir."estadoCirugia_id" AND  estcir.id IN ( ' + "'" + str(estadoCirugiaPendiente.id) + "','" + str(estadoCirugiaConfirmada.id) + "','" + str(estadoCirugiaRealizada.id)  + "'))" + '  INNER JOIN usuarios_usuarios u ON (u.id = i.documento_id ) INNER JOIN usuarios_tiposdocumento tipdoc ON (tipdoc.id =  u."tipoDoc_id") INNER JOIN cirugia_estadosprogramacion estprog ON (estprog.id = prog."estadoProgramacion_id" AND estprog.nombre != '  + "'" + str(estadoProgramacionRealizada.nombre) + "'" + ' ) LEFT JOIN sitios_salas sala ON (sala.id =prog.sala_id )  WHERE sed.id = ' + "'" + str(sede) +  "'"  + ' order by sala.numero'

    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc_id, abrev, documento, consecutivo, paciente, estadoProg, numero, sala, inicia, horaInicia, Termina, horaTermina , cirugias, estadoCirugia in curx.fetchall():
        programacionCirugias.append(
            {"model": "cirugia.programcioncirugias", "pk": id, "fields":
                {'id': id, 'tipoDoc_id': tipoDoc_id, 'abrev':abrev, 'documento': documento, 'consecutivo': consecutivo,
                 'paciente': paciente, 'estadoProg': estadoProg, 'numero': numero, 'sala': sala,
                 'inicia': inicia, 'horaInicia': horaInicia,
                 'Termina': Termina, 'horaTermina': horaTermina,'cirugias':cirugias,'estadoCirugia':estadoCirugia
                 }})

    miConexionx.close()
    print(programacionCirugias)
    # context['Convenios'] = convenios
    # convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    # convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    # convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    # convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})

    serialized1 = json.dumps(programacionCirugias, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataSalasCirugia(request, data):
    print("Entre Load_dataSalasCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    # print("data = ", request.GET('data'))

    salasCirugia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT sal.id id, sal.numero numero, sal.nombre nombre, ubi.nombre ubicacion, serv.nombre servicio, est.nombre estado FROM sitios_salas sal, sitios_ubicaciones ubi, cirugia_estadossalas est, sitios_serviciosadministrativos serv WHERE sal."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND sal."serviciosAdministrativos_id" = serv.id AND ubi.id = serv.ubicaciones_id AND sal."estadoSala_id" = est.id ORDER BY sal.numero'

    print(detalle)

    curx.execute(detalle)

    for id, numero, nombre, ubicacion, servicio, estado  in curx.fetchall():
        salasCirugia.append(
            {"model": "sitios.salas", "pk": id, "fields":
                {'id': id, 'numero': numero, 'nombre': nombre, 'ubicacion': ubicacion,
                 'servicio': servicio, 'estado': estado    }})

    miConexionx.close()
    print(salasCirugia)
    # context['Convenios'] = convenios
    # convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    # convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    # convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    # convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})

    serialized1 = json.dumps(salasCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataDispoSalasCirugia(request, data):
    print("Entre Load_dataDispoSalasCirugia")

    context = {}
    d = json.loads(data)


    sede = d['sede']
    print("sede:", sede)
    salaId = d['salaId']
    print("salaId:", salaId)


    disponibilidadSalasCirugia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT sal.id id, sal.nombre nombre, dispoSala.fecha , dispoSala."desdeHora", dispoSala."hastaHora", dispoSala."estadoDisponibilidad"  FROM sitios_salas sal,  sitios_disponibilidadSalas dispoSala WHERE sal."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND sal.id = dispoSala.salas_id AND sal.id = ' + "'" + str(salaId) + "'" + ' ORDER BY sal.numero'

    print(detalle)

    curx.execute(detalle)

    for id, nombre, fecha, desdeHora, hastaHora , estadoDisponibilidad  in curx.fetchall():
        disponibilidadSalasCirugia.append(
            {"model": "sitios.disponibilidadSalas", "pk": id, "fields":
                {'id': id,  'nombre': nombre, 'fecha': fecha,
                 'desdeHora':desdeHora, 'hastaHora':hastaHora, 'estadoDisponibilidad':estadoDisponibilidad}})

    print("disponibilidad= " , disponibilidadSalasCirugia)
    miConexionx.close()


    serialized1 = json.dumps(disponibilidadSalasCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')




def CrearProgramacionCirugia(request):

    print ("Entre CrearProgramacionCirugia" )

    programacionId = request.POST["programacionId"]
    print ("programacionId =", programacionId)

    registroProgramacion = ProgramacionCirugias.objects.get(id=programacionId)
    registroCirugia = Cirugias.objects.get(tipoDoc_id=registroProgramacion.tipoDoc_id, documento_id=registroProgramacion.documento_id, consecAdmision = registroProgramacion.consecAdmision)


    serviciosAdministrativos = request.POST.get('serviciosAdministrativos')
    print ("serviciosAdministrativos =", serviciosAdministrativos)

    sala = request.POST["sala"]
    print ("sala =", sala)

    fechaProgramacionInicia = request.POST["fechaProgramacionInicia"]
    print ("fechaProgramacionInicia =", fechaProgramacionInicia)

    horaProgramacionInicia = request.POST["horaProgramacionInicia"]
    print ("horaProgramacionInicia =", horaProgramacionInicia)

    fechaProgramacionFin = request.POST["fechaProgramacionFin"]
    print ("fechaProgramacionFin =", fechaProgramacionFin)

    horaProgramacionFin = request.POST["horaProgramacionFin"]
    print ("horaProgramacionFin =", horaProgramacionFin)


    sedesClinica_id = request.POST["sedesClinicaProgramacionCirugia_id"]
    print("sedesClinica_id =", sedesClinica_id)

    username_id = request.POST["usernameProgramacionCirugia_id"]
    print("username_id =", username_id)

    estadosProgramacionY = request.POST["estadosProgramacionY"]
    print("estadosProgramacionY =", estadosProgramacionY)


    estadoProgramacion = EstadosProgramacion.objects.get(nombre='Programada')
    estadoCirugia = EstadosCirugias.objects.get(nombre='PENDIENTE')
    estadoSala = EstadosSalas.objects.get(nombre='OCUPADA')

    conveniosProg = request.POST["conveniosProg"]
    print("conveniosProg =", conveniosProg)


    estadoReg = 'A'
    fechaRegistro = timezone.now()

    # Aqui validar si las feca-hora de la sala a solicitar estan ocupadas si si enviar excepcion

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        horarioSala = []
        #comando0 = 'SELECT count(*) id FROM cirugia_programacioncirugias cir where cir.id != ' + "'" + str(programacionId) + "'" +  ' AND sala_id =  ' + "'" + str(sala) + "'" + ' AND cir."fechaProgramacionInicia" =  date(' + "'" + str(fechaProgramacionInicia) + "')" + ' AND (cir."horaProgramacionInicia"  BETWEEN  ' + "'" + str(horaProgramacionInicia) + "'" + ' and ' + "'" + str(horaProgramacionFin) + "'" + ' OR cir."horaProgramacionFin"  BETWEEN ' + "'" + str(horaProgramacionInicia) + "' AND " + "'" + str(horaProgramacionFin) + "')"
        comando0 = 'SELECT count(*) id FROM cirugia_programacioncirugias cir where cir.id != ' + "'" + str(programacionId) + "'" +  ' AND sala_id =  ' + "'" + str(sala) + "'" + ' AND cir."fechaProgramacionInicia" =  date(' + "'" + str(fechaProgramacionInicia) + "')" + ' AND (cir."horaProgramacionInicia"  > ' + "'" + str(horaProgramacionInicia) + "'" + ' and  cir."horaProgramacionInicia" < ' + "'" + str(horaProgramacionFin) + "'" + ' OR cir."horaProgramacionFin"  > ' + "'" + str(horaProgramacionInicia) + "'" + ' AND  cir."horaProgramacionFin" < ' + "'" + str(horaProgramacionFin) + "')"

        print(comando0)
        cur3.execute(comando0)

        for id in cur3.fetchall():
            horarioSala.append({'id': id})

        print ("horarioSala = ", horarioSala[0]['id'])

        horarioSala = str(horarioSala[0]['id'])
        horarioSala = horarioSala.replace(")", ' ')
        horarioSala = horarioSala.replace("(", ' ')
        horarioSala = horarioSala.replace(",", ' ')

        print ("horarioSala2 = ", horarioSala)


        if (float(horarioSala) > 0):
            print ("Entre muchos horarioss")

            miConexion3.rollback()

            return JsonResponse({'success': False, 'Mensajes': 'sala de Cirugia con horario ocupado!'})


        comando = 'UPDATE cirugia_programacioncirugias SET "horaProgramacionFin" = ' + "'" + str(horaProgramacionFin) + "'," +   '"fechaRegistro" = ' + "'" + str(fechaRegistro) + "'," + '"estadoReg" = ' + "'" + str(estadoReg) + "'," + '"sedesClinica_id" = ' + "'" + str(sedesClinica_id) + "'," + '"usuarioRegistro_id" = ' + "'" + str(username_id) + "'," + '"fechaProgramacionFin" = ' + "'" + str(fechaProgramacionFin)  + "'," + '"fechaProgramacionInicia" = ' + "'" + str(fechaProgramacionInicia)  + "'," + '"horaProgramacionInicia" = ' + "'" + str(horaProgramacionInicia) + "', sala_id = '" + str(sala) + "'," + '"estadoProgramacion_id" = ' + "'" + str(estadosProgramacionY) + "'," + '"serviciosAdministrativos_id" = ' + "'" + str(serviciosAdministrativos) + "'" + ' WHERE id = '  + "'"  + str(programacionId) + "'"

        print(comando)
        cur3.execute(comando)

        comando1 = 'UPDATE cirugia_cirugias SET "fechaProg" = ' + "'" + str(fechaProgramacionInicia)   + "'," + '"HoraProg" = ' + "'" + str(horaProgramacionInicia)  +  "', sala_id = " + str(sala) + "," + '"estadoProgramacion_id" = ' + "'" + str(estadosProgramacionY) + "'," + '"estadoCirugia_id" = '  + str(estadoCirugia.id) + ", convenio_id = " + "'" + str(conveniosProg) + "'" + ' WHERE id = ' + "'"  + str(registroCirugia.id) + "'"

        print(comando1)
        cur3.execute(comando1)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Programacion Actualizada satisfactoriamente!'})


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


def Load_dataSolicitudCirugia(request, data):
    print("Entre Load_dataSolicitudnCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    # print("data = ", request.GET('data'))

    estadoProgramacion = EstadosProgramacion.objects.get(nombre='Solicitud')
    #estadoCirugiaSinAsignar = EstadosCirugias.objects.get(nombre='SIN ASIGNAR')
    estadoCirugiaPendiente = EstadosCirugias.objects.get(nombre='PENDIENTE')
    estadoCirugiaConfirmada = EstadosCirugias.objects.get(nombre='CONFIRMADA')


    solicitudCirugias = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT cir.id id, i."sedesClinica_id" sede, u."tipoDoc_id" tipoDoc_id, u.documento documento, u.nombre paciente , i.consec consecutivo, u."fechaNacio" nacimiento,u.genero genero, age(u."fechaNacio") edad, i.id ingreso, cir."fechaSolicita" solicita, dep.nombre cama,emp.nombre empresa	, u.telefono telefono, cir."solicitaSangre" solicitaSangre, cir."describeSangre" describeSangre, "cantidadSangre","solicitaCamaUci",cir."solicitaMicroscopio","solicitaRx","solicitaAutoSutura","solicitaOsteosintesis",	"solicitaBiopsia", cir."solicitaMalla" solicitaMalla, cir."solicitaOtros" solicitaOtros, estcir.nombre estadoCir,tiposAnes.nombre anestesia FROM admisiones_ingresos i INNER JOIN  usuarios_usuarios u ON ( u."tipoDoc_id" = i."tipoDoc_id" and  u.id = i.documento_id ) INNER JOIN  cirugia_cirugias cir ON (cir."sedesClinica_id" = i."sedesClinica_id" and cir."tipoDoc_id"=i."tipoDoc_id" AND cir.documento_id = i.documento_id AND cir."consecAdmision"= i.consec) INNER JOIN sitios_dependencias dep ON (dep.id =  i."dependenciasActual_id") LEFT JOIN  facturacion_empresas emp ON (emp.id = i.empresa_id ) LEFT JOIN  sitios_serviciosadministrativos serv ON (serv.id = cir."serviciosAdministrativos_id" ) LEFT JOIN  cirugia_estadoscirugias estcir ON (estcir.id = cir."estadoCirugia_id" ) LEFT JOIN  cirugia_tiposanestesia tiposAnes ON (tiposAnes.id = cir.anestesia_id ) LEFT JOIN  cirugia_tiposcirugia tiposCiru ON (tiposCiru.id = cir."tiposCirugia_id") WHERE i."sedesClinica_id" = ' + "'" + str(sede) + "' AND " + 'cir."estadoCirugia_id" IN ( ' + "'" + str(estadoCirugiaPendiente.id) + "','" + str(estadoCirugiaConfirmada.id) + "')"

    print(detalle)

    curx.execute(detalle)

    for id, sede, tipoDoc_id, documento,  paciente, consecutivo, nacimiento, genero, edad, ingreso, solicita, cama, empresa, telefono, solicitaSangre, describeSangre, cantidadSangre, solicitaCamaUci, solicitaMicroscopio,solicitaRx,solicitaAutoSutura, solicitaOsteosintesis, solicitaBiopsia, solicitaMalla,solicitaOtros, estadoCir, anestesia  in curx.fetchall():
        solicitudCirugias.append(
            {"model": "cirugia.cirugia", "pk": id, "fields":
                {'id': id, 'sede':sede, 'tipoDoc_id': tipoDoc_id, 'documento': documento,
                 'paciente': paciente, 'consecutivo': consecutivo, 'nacimiento': nacimiento, 'genero': genero, 'edad': edad,
                 'ingreso': ingreso, 'solicita': solicita,'cama':cama,
                 'empresa': empresa, 'telefono': telefono, 'solicitaSangre': solicitaSangre, 'describeSangre': describeSangre,
                 'cantidadSangre': cantidadSangre, 'solicitaCamaUci': solicitaCamaUci,'solicitaMicroscopio':solicitaMicroscopio,'solicitaRx':solicitaRx,
                 'solicitaAutoSutura':solicitaAutoSutura, 'solicitaOsteosintesis':solicitaOsteosintesis,'solicitaBiopsia':solicitaBiopsia,'solicitaMalla':solicitaMalla,
                 'solicitaOtros':solicitaOtros  ,'estadoCir':estadoCir,'anestesia':anestesia
                 }})

    miConexionx.close()
    print(solicitudCirugias)
    #solicitudCirugias['ingresosCirugia'] = ingresosCirugia

    serialized1 = json.dumps(solicitudCirugias, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataIngresosCirugia(request, data):
    print("Entre Load_dataIngresosCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    # print("data = ", request.GET('data'))

    estadoProgramacionRealizada = EstadosProgramacion.objects.get(nombre='Realizada')

    ingresosCirugia = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    #detalle = 'SELECT i.id id,i."tipoDoc_id" tipoDoc_id, u.documento documento,u.nombre paciente, i.consec consecutivo, u.genero, age(u."fechaNacio") edad, u."fechaNacio" nacimiento, dep.nombre cama, u.telefono telefono, emp.nombre empresa FROM admisiones_ingresos i INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" =  i."tipoDoc_id" AND u.id =  i.documento_id) LEFT JOIN sitios_dependencias dep ON (dep."sedesClinica_id" = i."sedesClinica_id" AND dep.id = i."dependenciasActual_id") LEFT JOIN facturacion_empresas emp	 ON (emp.id = i.empresa_id )  INNER JOIN sitios_serviciossedes servsed ON (servsed.id = dep."serviciosSedes_id") INNER JOIN clinico_servicios serv ON (serv.id = servsed.servicios_id AND (serv.nombre = ' + "'" + str('HOSPITALIZACION') + "' OR serv.nombre = " + "'" + str('URGENCIAS') + "' OR serv.nombre = '" + str('AMBULATORIO') + "'))" + ' where i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND i."fechaSalida"  is null ' + ' AND (i."tipoDoc_id", i.documento_id, i.consec) not in (select cirx."tipoDoc_id", cirx.documento_id, cirx."consecAdmision" FROM cirugia_cirugias cirx WHERE cirx."tipoDoc_id" = i."tipoDoc_id" AND cirx.documento_id = i.documento_id AND cirx."consecAdmision" = i.consec AND cirx."estadoProgramacion_id" = ' + "'" + str(estadoProgramacionRealizada.id) + "'" + ') ORDER BY i."dependenciasActual_id"'
    detalle = 'SELECT i.id id,i."tipoDoc_id" tipoDoc_id, u.documento documento,u.nombre paciente, i.consec consecutivo, u.genero, age(u."fechaNacio") edad, u."fechaNacio" nacimiento, dep.nombre cama, u.telefono telefono, emp.nombre empresa FROM admisiones_ingresos i INNER JOIN usuarios_usuarios u ON (u."tipoDoc_id" =  i."tipoDoc_id" AND u.id =  i.documento_id) LEFT JOIN sitios_dependencias dep ON (dep."sedesClinica_id" = i."sedesClinica_id" AND dep.id = i."dependenciasActual_id") LEFT JOIN facturacion_empresas emp	 ON (emp.id = i.empresa_id )  INNER JOIN sitios_serviciossedes servsed ON (servsed.id = dep."serviciosSedes_id") INNER JOIN clinico_servicios serv ON (serv.id = servsed.servicios_id AND (serv.nombre = ' + "'" + str('HOSPITALIZACION') + "' OR serv.nombre = " + "'" + str('URGENCIAS') + "' OR serv.nombre = '" + str('AMBULATORIO') + "'))" + ' where i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND i."fechaSalida"  is null '
    print(detalle)

    curx.execute(detalle)

    for  id,tipoDoc_id, documento,  paciente, consecutivo,  genero, edad, nacimiento,  cama,telefono, empresa  in curx.fetchall():

        ingresosCirugia.append(
            {"model": "admisiones.ingresos", "pk": id, "fields":
                {'id': id,  'tipoDoc_id': tipoDoc_id, 'documento': documento, 'paciente': paciente, 'consecutivo': consecutivo, 'genero': genero, 'edad': edad,
                  'nacimiento': nacimiento, 'cama': cama, 'telefono': telefono, 'empresa': empresa        }})

    miConexionx.close()
    print(ingresosCirugia)

    serialized1 = json.dumps(ingresosCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataDisponibilidadSalas(request, data):

    print("Entre Load_dataDisponibilidadSalas")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']
    print ("aqui voy_01")

    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    fecha_hoy = timezone.now()
    fecha_actual = timezone.now()
    print("fecha_actual1", fecha_actual)
    fecha_actual = fecha_actual + timedelta(days =-1)
    print("fecha_actual2", fecha_actual)
    fecha_hoyM = fecha_actual.strftime("%Y-%m-%d")
    print("fecha_hoyM a WORK:", fecha_hoy)
    dias_a_revisar = 5


    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    comando1 = 'SELECT id, id salaId , nombre nombreSala FROM sitios_salas WHERE "sedesClinica_id"  = ' + "'" + str(sede) + "' ORDER BY id"
    print("comando1 = ", comando1)
    curx.execute(comando1)

    salas = []
    disponibilidadAprobada = []

    fecha_futura = fecha_hoyM

    for id, salaId, nombreSala in curx.fetchall():
        salas.append(
            {"model": "sitios.salas", "pk": id, "fields":
                {'id':id, 'salaId': salaId, 'nombreSala': nombreSala}})

        primeraIteracionDia = 'S'
        print("COMIENZO CON LA SALA No ", salaId)
        print ("primeraIteracionDia:" , primeraIteracionDia)

        for i in range(dias_a_revisar + 1):


            print("en la fecha  ", fecha_futura)
            fecha_actual = fecha_actual + timedelta(days= +1)
            fecha_futura = fecha_actual
            fecha_futura = fecha_futura.strftime("%Y-%m-%d")
            primeraIteracion = 'S'
            print("Comienzo en el dia ", fecha_futura)

            comando2 = 'SELECT dispoSalas.id id , dispoSalas.id dispoId , dispoSalas.fecha, dispoSalas."desdeHora", dispoSalas."hastaHora", dispoSalas."estadoDisponibilidad" FROM sitios_disponibilidadsalas dispoSalas, sitios_salas salas WHERE salas.id = ' + "'" + str(salaId) + "' AND  salas.id = dispoSalas.salas_id  AND disposalas.fecha = " + "'" + str(fecha_futura) + "'" + ' ORDER BY "desdeHora", "hastaHora"'
            print("comando salas disponibilidad = ", comando2)
            curx.execute(comando2)

            salasDisponibilidad = []

            for id, dispoId , fecha, desdeHora, hastaHora, estadoDisponibilidad in curx.fetchall():
                salasDisponibilidad.append({"model": "sitios.disponibilidadsalas", "pk": id, "fields": {'id': id, 'dispoId': dispoId ,'fecha': fecha,'desdeHora':desdeHora, 'hastaHora':hastaHora, 'estadoDisponibilidad':estadoDisponibilidad}})

                print ("Paso por salasDisponibilidad[] ", salasDisponibilidad)

                if (salasDisponibilidad == '[]'):

                    primeraIteracion = 'X'
                    print ("voy en dia y SALTO", fecha_futura)

                else:
                    print("Ensa al", salaId)
                    print("Encontre disponibildad",fecha_futura)

                    comando3 = 'SELECT prog.id,  prog."fechaProgramacionInicia" fechaProgramacionInicia, prog."fechaProgramacionFin" fechaProgramacionFin,	prog."horaProgramacionInicia" horaProgramacionInicia, prog."horaProgramacionFin" horaProgramacionFin , usu.nombre nombrePaciente FROM cirugia_programacioncirugias prog INNER JOIN usuarios_usuarios usu ON (usu.id = prog.documento_id ) WHERE prog.sala_id = ' + "'" + str(salaId) + "'" + ' AND prog."fechaProgramacionInicia" = ' + "'" + str(fecha_futura) + "' ORDER BY " + ' prog."horaProgramacionInicia" '
                    print("comando programaciondisponibilidad = ", comando3)

                    curx.execute(comando3)
                    disponibilidadCirugia = []
                    print("comando programaciondisponibilidad CONFIRMADO_1 = ")

                    totalCirugiasDia=0
                    totalCirugiasDia = ProgramacionCirugias.objects.filter(sala_id=salaId, fechaProgramacionInicia=fecha_futura).count()

                    print("Total cirugias del dia ", totalCirugiasDia);

                    if (totalCirugiasDia == 0):

                        disponibilidadAprobada.append(
                            {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                {'id': id, 'salaId': salaId, 'nombreSala': nombreSala,
                                 'fechaProgramacionInicia': fecha_futura, 'fechaProgramacionFin': fecha_futura,
                                 'horaProgramacionInicia': desdeHora,
                                 'horaProgramacionFin': hastaHora, 'nombrePaciente': '', 'estado': 'DISPONIBLE'}})


                    else:
	
                        for  id,  fechaProgramacionInicia, fechaProgramacionFin,  horaProgramacionInicia, horaProgramacionFin , nombrePaciente in curx.fetchall():
                                print("comando programaciondisponibilidad CONFIRMADO_1.5 = ")
                                disponibilidadCirugia.append({"model": "cirgugia.disponibilidadCirugia", "pk": id, "fields": {'id':id, 'fechaProgramacionInicia': fechaProgramacionInicia, 'fechaProgramacionFin': fechaProgramacionFin, 'horaProgramacionInicia': horaProgramacionInicia,'horaProgramacionFin': horaProgramacionFin,'nombrePaciente':nombrePaciente}})
                                print("comando programaciondisponibilidad CONFIRMADO_2 = ")
                                print("paso por disponibilidadCirugia =" , disponibilidadCirugia)

                                if (disponibilidadCirugia=='[]'):

                                    print ("Es un dia sin programacion o sea sala libre")

                                    disponibilidadAprobada.append(
                                                 {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                                 {'id':id, 'salaId':salaId,'nombreSala':nombreSala, 'fechaProgramacionInicia': fecha_futura, 'fechaProgramacionFin': fecha_futura, 'horaProgramacionInicia': desdeHora,
                                                 'horaProgramacionFin': hastaHora,'nombrePaciente':'','estado':'DISPONIBLE'}})


                                    primeraIteracion = 'X'

                                else:

                                    if (primeraIteracionDia == 'S'):

                                        print ("entre primera iteracion")
                                        print("desdeHora:" , desdeHora)
                                        print("horaProgramacionInicia:", horaProgramacionInicia)

                                        if (desdeHora < horaProgramacionInicia):
                                            print("entre desdeHora <  horaProgramacionInicia")
                                            # Hueco DISPONIBLE
                                            disponibilidadAprobada.append(
                                                        {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                                        {'id':id, 'salaId':salaId,'nombreSala':nombreSala, 'fechaProgramacionInicia': fecha_futura, 'fechaProgramacionFin': fecha_futura, 'horaProgramacionInicia': desdeHora,
                                                         'horaProgramacionFin': horaProgramacionInicia,'nombrePaciente':'','estado':'DISPONIBLE'}})
                                            #Ahora si la cirugia AGENDADA
                                            disponibilidadAprobada.append(
                                                        {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                                        {'id':id, 'salaId':salaId, 'nombreSala':nombreSala,'fechaProgramacionInicia': fechaProgramacionInicia, 'fechaProgramacionFin': fechaProgramacionFin, 'horaProgramacionInicia': horaProgramacionInicia,
                                                         'horaProgramacionFin': horaProgramacionFin ,'nombrePaciente':nombrePaciente,'estado':'OCUPADA'}})



                                            print("primeraIteracionDia = ", primeraIteracionDia)
                                            print("disponibilidadAprobada = ", disponibilidadAprobada)

                                        if (desdeHora == horaProgramacionInicia):
                                            # Ahora si la cirugia AGENDADA
                                            disponibilidadAprobada.append(
                                                        {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                                        {'id':id, 'salaId':salaId, 'nombreSala':nombreSala, 'fechaProgramacionInicia': fechaProgramacionInicia, 'fechaProgramacionFin': fechaProgramacionFin, 'horaProgramacionInicia': horaProgramacionInicia,
                                                         'horaProgramacionFin': horaProgramacionFin,'nombrePaciente':nombrePaciente,'estado':'OCUPADA'}})


                                        primeraIteracionDia == 'N'
                                        fechaProgramacionIniciaAnterior = fechaProgramacionInicia
                                        fechaProgramacionFinAnterior = fechaProgramacionFin
                                        horaProgramacionIniciaAnterior = horaProgramacionInicia
                                        horaProgramacionFinAnterior = horaProgramacionFin

                                    else:
                                        # Por aqui No es primera iteracion
                                        print ("entre primeraIteracion = N")
                                        print("entre : horaProgramacionFinAnterior", horaProgramacionFinAnterior)
                                        print("entre : horaProgramacionInicia", horaProgramacionInicia)

                                        if (horaProgramacionFinAnterior < horaProgramacionInicia):
                                            # Hueco DISPONIBLE
                                            print ("entre MENOR ")

                                            disponibilidadAprobada.append(
                                                        {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                                        {'id':id,  'salaId':salaId, 'nombreSala':nombreSala,'fechaProgramacionInicia': fecha_futura, 'fechaProgramacionFin': fecha_futura, 'horaProgramacionInicia': horaProgramacionFinAnterior,
                                                         'horaProgramacionFin': horaProgramacionInicia,'nombrePaciente':'','estado':'DISPONIBLE'}})
                                            # Ahora si la cirugia AGENDADA
                                            disponibilidadAprobada.append(
                                                        {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                                        {'id':id, 'salaId':salaId, 'nombreSala':nombreSala,'fechaProgramacionInicia': fechaProgramacionInicia, 'fechaProgramacionFin': fechaProgramacionFin, 'horaProgramacionInicia': horaProgramacionInicia,
                                                         'horaProgramacionFin': horaProgramacionFin ,'nombrePaciente':nombrePaciente,'estado':'OCUPADA'}})


                                        if (horaProgramacionFinAnterior == horaProgramacionInicia):

                                            #Ahora si la cirugia AGENDADA
                                            disponibilidadAprobada.append(
                                                        {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                                        {'id':id,  'salaId':salaId,'nombreSala':nombreSala, 'fechaProgramacionInicia': fechaProgramacionInicia, 'fechaProgramacionFin': fechaProgramacionFin, 'horaProgramacionInicia': horaProgramacionInicia,
                                                         'horaProgramacionFin': horaProgramacionFin ,'nombrePaciente':nombrePaciente,'estado':'OCUPADA'}})

                                        fechaProgramacionIniciaAnterior = fechaProgramacionInicia
                                        fechaProgramacionFinAnterior = fechaProgramacionFin
                                        horaProgramacionIniciaAnterior = horaProgramacionInicia
                                        horaProgramacionFinAnterior = horaProgramacionFin

                                ##for BARRO LA PROGRAMACION PARA ESE DIA
                                primeraIteracion = 'S'

                                if (hastaHora > horaProgramacionFin):
                                    disponibilidadAprobada.append(
                                    {"model": "cirugia.programacionAprobada", "pk": id, "fields":
                                    {'id': id, 'salaId': salaId, 'nombreSala': nombreSala,
                                     'fechaProgramacionInicia': fechaProgramacionInicia,
                                     'fechaProgramacionFin': fechaProgramacionFin,
                                     'horaProgramacionInicia': horaProgramacionFinAnterior,
                                     'horaProgramacionFin': hastaHora, 'nombrePaciente': '', 'estado': 'DISPONIBLE'}})


                #FOR PARA ESTE DIA QUE DISPONIBILIDAD HAY EN ESA SALA
                #  fin cambia 1 dia

            primeraIteracion = 'S'



        #FIN FOR  1 SALA

        print ("un dia con i = ", i)

        fecha_actual = timezone.now()
        #fecha_actual = datetime.now()
        fecha_actual = fecha_actual + timedelta(days = -1)
        primeraIteracion = 'S'
        # fecha_hoy = fecha_actual.strftime("%Y-%m-%d")
        fecha_futura = fecha_actual.strftime("%Y-%m-%d")


    #FIn acxabo todas las salas
    #
    fecha_actual = timezone.now()
    #fecha_actual = datetime.now()
    fecha_actual = fecha_actual + timedelta(days = -1)

    primeraIteracion = 'S'
    #fecha_hoy = fecha_actual.strftime("%Y-%m-%d")
    fecha_futura = fecha_actual.strftime("%Y-%m-%d")

    print("sali me regreso con " , disponibilidadAprobada)

    miConexionx.close()
    print(disponibilidadAprobada)

    serialized1 = json.dumps(disponibilidadAprobada, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def CrearSolicitudCirugia(request):

    print ("Entre CrearSolicitudCirugia" )

    serviciosAdministrativos = request.POST.get("serviciosAdministrativosI")
    print ("serviciosAdministrativos =", serviciosAdministrativos)

    if 'solicitaSangre' in request.POST:
        solicitaSangre = 'S'
    else:
        solicitaSangre = 'N'

    print ("solicitaSangre =", solicitaSangre)

    describeSangre = request.POST["describeSangre"]
    print ("describeSangre =", describeSangre)

    cantidadSangre = request.POST["cantidadSangre"]
    print ("cantidadSangre =", cantidadSangre)

    if 'solicitaCamaUci' in request.POST:
        solicitaCamaUci = 'S'
    else:
        solicitaCamaUci = 'N'


    print ("solicitaCamaUci =", solicitaCamaUci)

    if 'solicitaMicroscopio' in request.POST:
        solicitaMicroscopio = 'S'
    else:
        solicitaMicroscopio = 'N'

    print ("solicitaMicroscopio =", solicitaMicroscopio)

    if 'solicitaRx' in request.POST:
        solicitaRx = 'S'
    else:
        solicitaRx = 'N'

    print ("solicitaRx =", solicitaRx)

    if 'solicitaOsteosintesis' in request.POST:
        solicitaOsteosintesis = 'S'
    else:
        solicitaOsteosintesis = 'N'

    print ("solicitaOsteosintesis =", solicitaOsteosintesis)

    if 'solicitaBiopsia' in request.POST:
        solicitaBiopsia = 'S'
    else:
        solicitaBiopsia = 'N'

    print ("solicitaBiopsia =", solicitaBiopsia)

    if 'solicitaMalla' in request.POST:
        solicitaMalla = 'S'
    else:
        solicitaMalla = 'N'

    print ("solicitaMalla =", solicitaMalla)

    if 'solicitaOtros' in request.POST:
        solicitaOtros = 'S'
    else:
        solicitaOtros = 'N'
    print ("solicitaOtros =", solicitaOtros)


    if 'solicitaAnestesia' in request.POST:
        solicitaAnestesia = 'S'
    else:
        solicitaAnestesia = 'N'
    print ("solicitaAnestesia =", solicitaAnestesia)

    anestesia = request.POST["anestesia"]
    print("anestesia =", anestesia)


    print ("anestesia =", anestesia)
    sedesClinica_id = request.POST["sedesClinica_id"]
    print("sedesClinica_id =", sedesClinica_id)

    username = request.POST["username3_id"]
    print("username =", username)

    if 'solicitaHospitalizacion' in request.POST:

       solicitaHospitalizacion = 'S'
    else:
        solicitaHospitalizacion = 'N'

    print ("solicitaHospitalizacion =", solicitaHospitalizacion)

    if 'solicitaAyudante' in request.POST:
        solicitaAyudante = 'S'
    else:
        solicitaAyudante = 'N'


    print ("solicitaAyudante =", solicitaAyudante)
    if 'solicitaTiempoQx' in request.POST:
        solicitaTiempoQx = 'S'
    else:
        solicitaTiempoQx = 'N'

    print ("solicitaTiempoQx =", solicitaTiempoQx)
    if 'solicitaTipoQx' in request.POST:
        solicitaTipoQx = 'S'
    else:
        solicitaTipoQx= 'N'

    print ("solicitatipoQx =", solicitaTipoQx)

    tiempoMaxQx = request.POST["tiempoMaxQx"]
    print ("tiempoMaxQx =", tiempoMaxQx)

    if 'solicitaAutoSutura' in request.POST:
        solicitaAutoSutura = 'S'
    else:
        solicitaAutoSutura= 'N'

    
    if 'solicitaSoporte' in request.POST:
        solicitaSoporte = 'S'
    else:
        solicitaSoporte= 'N'

    print ("solicitaSoporte =", solicitaSoporte)
    describeOtros = request.POST["describeOtros"]
    print ("describeOtros =", describeOtros)

    especialidadX = request.POST["especialidadX"]
    print("especialidadX =", especialidadX)

    tiposCirugia = request.POST["tiposCirugia"]
    print ("tiposCirugia =", tiposCirugia)

    dxPreQx = request.POST["dxPreQx"]
    print ("dxPreQx =", dxPreQx)

    dxPrinc = request.POST["dxPrinc"]
    print ("dxPrinc =", dxPrinc)

    dxRel1 = request.POST["dxRel1"]
    print ("dxRel1 =", dxRel1)

    dxRel2 = request.POST["dxRel2"]
    print ("dxRel2 =", dxRel2)

    dxPostQx = "null"
    dxRel3 = 'null'

    if dxPreQx == '':
        dxPreQx = "null"

    if dxPostQx == '':
        dxPostQx = "null"

    if dxPrinc == '':
        dxPrinc = "null"
    if dxRel1 == '':
        dxRel1 = "null"
    if dxRel2 == '':
        dxRel2 = "null"


    convenioProc = request.POST["convenioProc"]
    print ("convenioProc =", convenioProc)


    #especialidadId = EspecialidadesMedicos.objects.get(planta_id=username)

    estadoCirugia = EstadosCirugias.objects.get(nombre='PENDIENTE')
    estadoProgramacion = EstadosProgramacion.objects.get(nombre='Solicitud')
    #estadoSala = EstadosSalas.objetcs.get(nombre='OCUPADA')
    estadoReg = 'A'
    fechaRegistro = timezone.now()
    fechaSolicita = fechaRegistro

    ingresoId = request.POST["ingresoId2"]
    print("ingresoId =", ingresoId)

    registroIngreso = Ingresos.objects.get(id=ingresoId)

    print("A INSERTAR")

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugias ("consecAdmision", "fechaSolicita", "solicitaHospitalizacion", "solicitaAyudante", "solicitaTiempoQx",  "solicitaAnestesia", "solicitaSangre", "describeSangre", "cantidadSangre", "solicitaCamaUci", "solicitaMicroscopio", "solicitaRx", "solicitaAutoSutura", "solicitaOsteosintesis",  "solicitaBiopsia", "solicitaMalla", "solicitaOtros", "describeOtros", "tiempoMaxQx", "fechaRegistro", "estadoReg", anestesia_id, documento_id,  "dxPreQx_id", "dxPrinc_id", "dxRel1_id", especialidad_id, "sedesClinica_id", "tipoDoc_id", "usuarioRegistro_id", "usuarioSolicita_id", "serviciosAdministrativos_id", "estadoProgramacion_id", "tiposCirugia_id","estadoCirugia_id", anulado, convenio_id) VALUES (' + "'" + str(registroIngreso.consec) + "','" + str(fechaSolicita) + "','" + str(solicitaHospitalizacion) + "','" + str(solicitaAyudante) + "','" + str(solicitaTiempoQx) + "','"  + str(solicitaAnestesia) + "','" + str(solicitaSangre) + "','" + str(describeSangre) + "','" + str(cantidadSangre) + "','" + str(solicitaCamaUci) + "','" + str(solicitaMicroscopio) + "','" + str(solicitaRx) + "','" + str(solicitaAutoSutura) + "','" + str(solicitaOsteosintesis) + "','"  + str(solicitaBiopsia) + "','" + str(solicitaMalla) + "','" + str(solicitaOtros) + "','" + str(describeOtros) + "','" + str(tiempoMaxQx) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(anestesia) + "," + str(registroIngreso.documento_id) + "," + str(dxPreQx) + "," + str(dxPrinc) + "," + str(dxRel1) + "," + str(especialidadX) + "," + str(sedesClinica_id) + "," + str(registroIngreso.tipoDoc_id) + "," + str(username) + "," + str(username) + "," + str(serviciosAdministrativos) + "," + str(estadoProgramacion.id) + ",'" + str(tiposCirugia) + "'," + str(estadoCirugia.id) + ",'N','" + str(convenioProc) + "') RETURNING id"
        #comando = 'INSERT INTO cirugia_cirugias ("consecAdmision", "fechaSolicita", "solicitaHospitalizacion", "solicitaAyudante", "solicitaTiempoQx") VALUES (' + "'" + str(registroIngreso.consec) + "','" + str(fechaSolicita) + "','" + str(solicitaHospitalizacion) + "','" + str(solicitaAyudante) + "','" + str(solicitaTiempoQx) + "') RETURNING id"
        #comando = 'INSERT INTO cirugia_cirugias ("consecAdmision", "fechaSolicita", "solicitaHospitalizacion", "solicitaAyudante", "solicitaTiempoQx",  "solicitaAnestesia", "solicitaSangre", "describeSangre", "cantidadSangre", "solicitaCamaUci"  ) VALUES (' + "'" + str(registroIngreso.consec) + "','" + str(fechaSolicita) + "','" + str(solicitaHospitalizacion) + "','" + str(solicitaAyudante) + "','" + str(solicitaTiempoQx) + "','"  + str(solicitaAnestesia) + "','" + str(solicitaSangre) + "','" + str(describeSangre) + "','" + str(cantidadSangre) + "','" + str(solicitaCamaUci) + "') RETURNING id"

        print("comando = " , comando)



        resultado = cur3.execute(comando)

        cirugiaId = cur3.fetchone()[0]

        comando2 = 'INSERT INTO cirugia_programacioncirugias ("consecAdmision", "fechaRegistro", "estadoReg", documento_id, "sedesClinica_id", "tipoDoc_id", "usuarioRegistro_id",  "estadoProgramacion_id", cirugia_id) values (' + "'" + str(registroIngreso.consec) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(registroIngreso.documento_id) + "','" + str(sedesClinica_id) + "','" + str(registroIngreso.tipoDoc_id) + "','" + str(username) + "','" + str(estadoProgramacion.id) + "','" + str(cirugiaId)  + "')"

        print(comando2)
        cur3.execute(comando2)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Solicitud Actualizada satisfactoriamente!'})


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

def Load_dataTraerProcedimientosCirugia(request, data):
    print("Entre Load_dataTraerProcedimientosCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    procedimientosCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    #comando = 'select cirproc.id id, cirproc.cirugia_id cirugiaId, cirproc.cups_id cups_id, exa.nombre exaNombre, final.nombre finalNombre FROM cirugia_cirugiasprocedimientos cirproc, clinico_examenes exa, cirugia_finalidadcirugia final WHERE cirproc.cirugia_id = ' + "'" + str(cirugiaId) + "'" + ' and cirproc.cups_id = exa.id and final.id = cirproc.finalidad_id'
    comando = 'select cirproc.id id, cirproc.cups_id cups_id, exa.nombre exaNombre, final.nombre finalNombre FROM cirugia_cirugiasprocedimientos cirproc INNER JOIN clinico_examenes exa ON ( exa.id = cirproc.cups_id) LEFT JOIN cirugia_finalidadcirugia final ON (final.id = cirproc.finalidad_id) WHERE cirproc.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id,  cups_id, exaNombre, finalNombre  in cur3.fetchall():
        procedimientosCirugia.append(
            {"model": "cirugia.procedimientos", "pk": id, "fields":
                {'id': id,  'cups_id': cups_id, 'exaNombre': exaNombre, 'finalNombre': finalNombre      }})

    miConexion3.close()
    print(procedimientosCirugia)

    serialized1 = json.dumps(procedimientosCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataTraerProcedimientosInformeCirugia(request, data):
    print("Entre Load_dataTraerProcedimientosInformeCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    procedimientosCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    comando = 'select cirproc.id id, cirproc.cirugia_id cirugia_id, cirproc.cups_id cups_id, exa.nombre exaNombre, final.nombre finalNombre, cirproc.cruento, cirproc.incruento, reg.region  regionOperatoria, vias.nombre viasDeAcceso FROM cirugia_cirugiasprocedimientos cirproc INNER JOIN clinico_examenes exa ON ( exa.id = cirproc.cups_id) LEFT JOIN cirugia_regionesoperatorias reg ON (reg.id = cirproc."regionOperatoria_id") LEFT JOIN cirugia_viasdeacceso vias ON (vias.id = cirproc."viasDeAcceso_id") LEFT JOIN cirugia_finalidadcirugia final ON (final.id = cirproc.finalidad_id) WHERE cirproc.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id, cirugia_id,  cups_id, exaNombre, finalNombre , cruento, incruento, regionOperatoria, viasDeAcceso  in cur3.fetchall():
        procedimientosCirugia.append(
            {"model": "cirugia.procedimientos", "pk": id, "fields":
                {'id': id, 'cirugia_id':cirugia_id,  'cups_id': cups_id, 'exaNombre': exaNombre, 'finalNombre': finalNombre ,'cruento':cruento, 'incruento':incruento,
                 'regionOperatoria':regionOperatoria,'viasDeAcceso':viasDeAcceso }})

    miConexion3.close()
    print(procedimientosCirugia)

    serialized1 = json.dumps(procedimientosCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataTraerProcedimientosInformeXXCirugia(request, data):
    print("Entre Load_dataTraerProcedimientosInformeXXCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    procedimientosCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    comando = 'select cirproc.id id, cirproc.cirugia_id cirugia_id, cirproc.cups_id cups_id, exa.nombre exaNombre, final.nombre finalNombre , cirproc.cruento, cirproc.incruento, reg.region  regionOperatoria, vias.nombre viasDeAcceso  FROM cirugia_cirugiasprocedimientos cirproc INNER JOIN clinico_examenes exa ON ( exa.id = cirproc.cups_id)  LEFT JOIN cirugia_regionesoperatorias reg ON (reg.id = cirproc."regionOperatoria_id") LEFT JOIN cirugia_viasdeacceso vias ON (vias.id = cirproc."viasDeAcceso_id")  LEFT JOIN cirugia_finalidadcirugia final ON (final.id = cirproc.finalidad_id) WHERE cirproc.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id, cirugia_id,  cups_id, exaNombre, finalNombre, cruento, incruento , regionOperatoria, viasDeAcceso in cur3.fetchall():
        procedimientosCirugia.append(
            {"model": "cirugia.procedimientos", "pk": id, "fields":
                {'id': id, 'cirugia_id':cirugia_id,  'cups_id': cups_id, 'exaNombre': exaNombre, 'finalNombre': finalNombre  ,'cruento':cruento, 'incruento':incruento,
                 'regionOperatoria':regionOperatoria,'viasDeAcceso':viasDeAcceso    }})

    miConexion3.close()
    print(procedimientosCirugia)

    serialized1 = json.dumps(procedimientosCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataTraerParticipantesCirugia(request, data):
    print("Entre Load_dataTraerParticipantesCirugia")

    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']


    cirugiaId =  d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    participantesCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    #comando = 'select cirpart.id id, cirpart.cirugia_id cirugiaId, hon.nombre honNombre, med.nombre medicoNombre, esp.nombre especialidadNombre , exa.nombre cupsNombre FROM cirugia_cirugiasparticipantes cirpart inner join tarifarios_tiposhonorarios hon ON (hon.id = cirpart."tipoHonorarios_id") inner join clinico_especialidadesmedicos med ON ( med.id = cirpart.medico_id ) inner join clinico_especialidades esp ON (esp.id =med.especialidades_id  ) left join clinico_examenes exa ON (exa.id = cirpart."cirugiaProcedimiento_id") WHERE cirpart.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    comando = 'select cirpart.id id, cirpart.cirugia_id cirugiaId, hon.nombre honNombre, med.nombre medicoNombre, esp.nombre especialidadNombre , exa.nombre cupsNombre FROM cirugia_cirugiasparticipantes cirpart inner join tarifarios_tiposhonorarios hon ON (hon.id = cirpart."tipoHonorarios_id") inner join clinico_especialidadesmedicos med ON ( med.id = cirpart.medico_id ) inner join clinico_especialidades esp ON (esp.id =med.especialidades_id  ) inner join cirugia_cirugiasprocedimientos cirProc ON (cirProc.id =  cirpart."cirugiaProcedimiento_id" )   left join clinico_examenes exa ON (exa.id = cirProc.cups_id)  WHERE cirpart.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id, cirugiaId, honNombre, medicoNombre, especialidadNombre , cupsNombre in cur3.fetchall():
        participantesCirugia.append(
            {"model": "cirugia.procedimientos", "pk": id, "fields":
                {'id': id, 'cirugiaId': cirugiaId, 'honNombre': honNombre, 'medicoNombre': medicoNombre, 'especialidadNombre': especialidadNombre,'cupsNombre':cupsNombre      }})

    miConexion3.close()
    print(participantesCirugia)

    serialized1 = json.dumps(participantesCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def Load_dataTraerParticipantesInformeCirugia(request, data):
    print("Entre Load_dataTraerParticipantesInformeCirugia")

    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']


    cirugiaId =  d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    participantesCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    comando = 'select cirpart.id id, cirpart.cirugia_id cirugiaId, hon.nombre honNombre, med.nombre medicoNombre, esp.nombre especialidadNombre , exa.nombre cupsNombre FROM cirugia_cirugiasparticipantes cirpart inner join tarifarios_tiposhonorarios hon ON (hon.id = cirpart."tipoHonorarios_id") inner join clinico_especialidadesmedicos med ON ( med.id = cirpart.medico_id ) inner join clinico_especialidades esp ON (esp.id =med.especialidades_id  ) inner join cirugia_cirugiasprocedimientos cirProc ON (cirProc.id =  cirpart."cirugiaProcedimiento_id" )   left join clinico_examenes exa ON (exa.id = cirProc.cups_id)  WHERE cirpart.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id, cirugiaId, honNombre, medicoNombre, especialidadNombre , cupsNombre in cur3.fetchall():
        participantesCirugia.append(
            {"model": "cirugia.procedimientos", "pk": id, "fields":
                {'id': id, 'cirugiaId': cirugiaId, 'honNombre': honNombre, 'medicoNombre': medicoNombre, 'especialidadNombre': especialidadNombre ,'cupsNombre':cupsNombre     }})

    miConexion3.close()
    print(participantesCirugia)

    serialized1 = json.dumps(participantesCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataTraerParticipantesInformeXXCirugia(request, data):
    print("Entre Load_dataTraerParticipantesXXInformeCirugia")

    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']


    cirugiaId =  d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    participantesCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    comando = 'select cirpart.id id, cirpart.cirugia_id cirugiaId, hon.nombre honNombre, med.nombre medicoNombre, esp.nombre especialidadNombre , exa.nombre cupsNombre FROM cirugia_cirugiasparticipantes cirpart, tarifarios_tiposhonorarios hon, clinico_especialidadesmedicos med, clinico_especialidades esp , clinico_examenes exa ,	cirugia_cirugiasprocedimientos cirProc WHERE cirpart.cirugia_id = ' + "'" + str(cirugiaId) + "'" + ' and cirpart."tipoHonorarios_id" = hon.id  and cirpart.medico_id = med.id and med.especialidades_id = esp.id AND cirpart."cirugiaProcedimiento_id" = cirProc.id AND cirProc.cups_id = exa.id'

    print(comando)
    cur3.execute(comando)

    for id, cirugiaId, honNombre, medicoNombre, especialidadNombre, cupsNombre  in cur3.fetchall():
        participantesCirugia.append(
            {"model": "cirugia.procedimientos", "pk": id, "fields":
                {'id': id, 'cirugiaId': cirugiaId, 'honNombre': honNombre, 'medicoNombre': medicoNombre, 'especialidadNombre': especialidadNombre , 'cupsNombre':cupsNombre     }})

    miConexion3.close()
    print(participantesCirugia)

    serialized1 = json.dumps(participantesCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataMaterialCirugia(request, data):
    print("Entre Load_dataMaterialCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    materialCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    comando = 'select cirmaterial.id id, cirmaterial.suministro_id suministro_id, suministros.nombre suministro , cirmaterial."hojaDeGasto" hojaDeGasto , tipo.nombre tipoSuministro , cirmaterial.unitario unitario , cirmaterial.cantidad cantidad , cirmaterial."valorLiquidacion" valorLiquidacion, exa.nombre cupsNombre FROM cirugia_cirugiasMaterialQx cirmaterial INNER JOIN cirugia_cirugiasprocedimientos cirProc ON ( cirProc.id = cirmaterial."cirugiaProcedimiento_id") LEFT JOIN facturacion_suministros suministros ON ( suministros.id = cirmaterial.suministro_id) LEFT JOIN facturacion_tipossuministro tipo ON (tipo.id = suministros."tipoSuministro_id") LEFT JOIN clinico_examenes exa ON ( exa.id = cirProc.cups_id)  WHERE cirmaterial.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id,  suministro_id, suministro , hojaDeGasto, tipoSuministro, unitario,cantidad , valorLiquidacion, cupsNombre in cur3.fetchall():
        materialCirugia.append(
            {"model": "cirugia.cirugiasMaterialQx", "pk": id, "fields":
                {'id': id,  'suministro_id': suministro_id, 'suministro': suministro, 'hojaDeGasto':hojaDeGasto,'tipoSuministro': tipoSuministro , 'unitario':unitario ,'cantidad':cantidad  ,'valorLiquidacion':valorLiquidacion  ,'cupsNombre':cupsNombre }})

    miConexion3.close()
    print(materialCirugia)

    serialized1 = json.dumps(materialCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataMaterialInformeCirugia(request, data):
    print("Entre Load_dataMaterialInformeCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    materialCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    comando = 'select cirmaterial.id id, cirmaterial.cirugia_id cirugia_id, cirmaterial.suministro_id suministro_id, suministros.nombre suministro ,cirmaterial."hojaDeGasto" hojaDeGasto , tipo.nombre tipoSuministro ,cirmaterial.unitario unitario , cirmaterial.cantidad cantidad , cirmaterial."valorLiquidacion" , exa.nombre cupsNombre FROM cirugia_cirugiasMaterialQx cirmaterial INNER JOIN cirugia_cirugiasprocedimientos cirProc ON ( cirProc.id = cirmaterial."cirugiaProcedimiento_id")  LEFT JOIN facturacion_suministros suministros ON ( suministros.id = cirmaterial.suministro_id) LEFT JOIN facturacion_tipossuministro tipo ON (tipo.id = suministros."tipoSuministro_id") LEFT JOIN clinico_examenes exa ON ( exa.id = cirProc.cups_id)  WHERE cirmaterial.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id,  cirugia_id, suministro_id, suministro ,hojaDeGasto , tipoSuministro, unitario,cantidad , valorLiquidacion, cupsNombre in cur3.fetchall():
        materialCirugia.append(
            {"model": "cirugia.cirugiasMaterialQx", "pk": id, "fields":
                {'id': id, 'cirugia_id':cirugia_id ,  'suministro_id': suministro_id, 'suministro': suministro, 'hojaDeGasto':hojaDeGasto, 'tipoSuministro': tipoSuministro, 'unitario':unitario ,'cantidad':cantidad ,'valorLiquidacion':valorLiquidacion ,'cupsNombre':cupsNombre   }})

    miConexion3.close()
    print(materialCirugia)

    serialized1 = json.dumps(materialCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataMaterialInformeXXCirugia(request, data):
    print("Entre Load_dataMaterialInformeXXCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    materialCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    comando = 'select cirmaterial.id id, cirmaterial.cirugia_id cirugia_id, cirmaterial.suministro_id suministro_id, suministros.nombre suministro , cirmaterial."hojaDeGasto" hojaDeGasto , tipo.nombre tipoSuministro , cirmaterial.unitario unitario, cirmaterial.cantidad cantidad , cirmaterial."valorLiquidacion" valorLiquidacion ,exa.nombre cupsNombre FROM cirugia_cirugiasMaterialQx cirmaterial INNER JOIN cirugia_cirugiasprocedimientos cirProc ON ( cirProc.id = cirmaterial."cirugiaProcedimiento_id") LEFT JOIN facturacion_suministros suministros ON ( suministros.id = cirmaterial.suministro_id) INNER JOIN facturacion_tipossuministro tipo ON (tipo.id = suministros."tipoSuministro_id") LEFT JOIN clinico_examenes exa ON ( exa.id = cirProc.cups_id)  WHERE cirmaterial.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id,  cirugia_id, suministro_id, suministro , hojaDeGasto , tipoSuministro, unitario, cantidad, valorLiquidacion, cupsNombre  in cur3.fetchall():
        materialCirugia.append(
            {"model": "cirugia.cirugiasMaterialQx", "pk": id, "fields":
                {'id': id, 'cirugia_id':cirugia_id ,  'suministro_id': suministro_id, 'suministro': suministro, 'hojaDeGasto':hojaDeGasto,'tipoSuministro': tipoSuministro, 'unitario':unitario ,'cantidad':cantidad, 'valorLiquidacion':valorLiquidacion ,'cupsNombre':cupsNombre    }})

    miConexion3.close()
    print(materialCirugia)

    serialized1 = json.dumps(materialCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')




def CrearProcedimientosCirugia(request):

    print ("Entre CrearProcedimientosCirugia" )

    cirugiaId = request.POST.get('cirugiaIdModalProcedimientos')
    print ("cirugiaId =", cirugiaId)

    cirugiaId2 = Cirugias.objects.get(id=cirugiaId)
    finalidad = request.POST.get('finalidad')
    print("finalidad =", finalidad)

    cups = request.POST["cups"]
    print ("cups =", cups)

    username_id = request.POST['usernameProcedimientosCirugia_id']
    print ("username_id =", username_id)


    estadoReg = 'A'

    fechaRegistro = timezone.now()

    estadoAutorizacionId = EstadoAutorizacion.objects.get(nombre='PENDIENTE')
    ingresoId = Ingresos.objects.get(tipoDoc_id = cirugiaId2.tipoDoc_id, documento_id = cirugiaId2.documento_id , consec = cirugiaId2.consecAdmision )

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugiasprocedimientos (finalidad_id, "fechaRegistro", "estadoReg", cirugia_id, cups_id, "usuarioRegistro_id") VALUES (' + "'" + str(finalidad) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(cups) + "','" + str(username_id) + "')"

        print(comando)
        cur3.execute(comando)

        # Aui la rutina para mirar si va o no a autorizaciones

        requiereAutorizacion = Examenes.objects.get(id=cups)

        if (requiereAutorizacion.requiereAutorizacion == 'S'):

            # crea cabezote de autorizaciones

            #comando = 'INSERT INTO autorizaciones_autorizaciones () VALUES () RETURNING id;'
            comando = 'INSERT INTO autorizaciones_autorizaciones ("fechaSolicitud","estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id , convenio_id , ingreso_id)  VALUES ( now(), ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" + str(sede) + "','" + str(username_id) + "'," + "'" + str('0') + "'" + ',' + "'" + str(cirugiaId2.convenio_id) + "',,"  + str(ingresoId.consec) + "' RETURNING id"
            print(comando)
            cur3.execute(comando)
            autorizacionId = cur3.fetchone()[0]

            # crea detalle de autorizacionesdetalle

            tiposExamenId = TiposExamen.objects.get(nombre='PROCEDIMIENTOS QX')

            #comando = 'INSERT INTO autorizaciones_autorizacionesdetalle () VALUES () RETURNING id;'
            comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id", "valorSolicitado", mipres)  VALUES (' + "'" + str(estadoAutorizacionId.id) + "'," + "'" + str('1') + "'" + ' ,0, now(),' + "'" + str('A') + "','" + str(autorizacionId) + "','" + str(username_id) + "'," + "'" + str(cups) + "',null, " + "'" + str(tiposExamenId.id) + "'," + "',0 , null)"
            print(comando)
            cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Procedimiento Actualizado satisfactoriamente!'})


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


def CrearProcedimientosInformeCirugia(request):

    print ("Entre CrearProcedimientosInformeCirugia" )

    cirugiaId = request.POST.get('cirugiaIdModalInformeProcedimientos')
    print ("cirugiaId =", cirugiaId)

    finalidad = request.POST.get('finalidadInforme')
    print("finalidad =", finalidad)

    cups = request.POST["cupsInforme"]
    print ("cups =", cups)

    username_id = request.POST['usernameProcedimientosInformeCirugia_id']
    print ("username_id =", username_id)

    cruento = request.POST['cruento']
    print ("cruento =", cruento)

    incruento = request.POST['incruento']
    print ("incruento =", incruento)

    regionesOperatorias = request.POST['regionesOperatorias']
    print ("regionesOperatorias =", regionesOperatorias)

    viasDeAcceso = request.POST['viasDeAcceso']
    print ("viasDeAcceso =", viasDeAcceso)


    estadoReg = 'A'
    fechaRegistro = timezone.now()



    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugiasprocedimientos (finalidad_id, "fechaRegistro", "estadoReg", cirugia_id, cups_id, "usuarioRegistro_id", cruento, incruento , "regionOperatoria_id", "viasDeAcceso_id") VALUES (' + "'" + str(finalidad) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(cups) + "','" + str(username_id) + "','" + str(cruento) + "','" + str(incruento) + "','" + str(regionesOperatorias)   + "','"  + str(viasDeAcceso) + "')"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Procedimiento Actualizado satisfactoriamente!'})


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


def CrearParticipantesInformeCirugia(request):

    print ("Entre CrearParticipantesInformeCirugia" )

    cirugiaId = request.POST.get('cirugiaIdModalParticipantesInforme')
    print ("cirugiaId =", cirugiaId)

    finalidadId = request.POST.get('finalidadParticipantesInformeCirugia')
    print("finalidadId =", finalidadId)

    medico = request.POST["medicoInforme"]
    print ("medico =", medico)

    procedParticipantesInforme = request.POST["procedParticipantesInforme"]
    print ("procedParticipantesInforme =", procedParticipantesInforme)

    if procedParticipantesInforme == '':
        procedParticipantesInforme = "null"


    username_id = request.POST["usernameParticipantesInformeCirugia_id"]
    print("username_id =", username_id)

    tipoHonorarios = request.POST["tipoHonorariosInforme"]
    print("tipoHonorarios =", tipoHonorarios)


    estadoReg = 'A'
    fechaRegistro = timezone.now()



    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugiasparticipantes (finalidad_id, "fechaRegistro", "estadoReg", cirugia_id, "tipoHonorarios_id", "usuarioRegistro_id", medico_id,"cirugiaProcedimiento_id") VALUES (' + "'" + str(finalidadId) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(tipoHonorarios) + "','" + str(username_id) + "','" + str(medico) +  "','" + str(procedParticipantesInforme) + "')"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Participante Actualizado satisfactoriamente!'})


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


def CrearParticipantesCirugia(request):

    print ("Entre CrearParticipantesCirugia" )

    cirugiaId = request.POST.get('cirugiaIdModalParticipantes')
    print ("cirugiaId =", cirugiaId)

    finalidadId = request.POST.get('finalidadParticipantesCirugia')
    print("finalidadId =", finalidadId)

    medico = request.POST["medico"]
    print ("medico =", medico)

    procedParticipantes = request.POST["procedParticipantes"]
    print ("procedParticipantes =", procedParticipantes)


    username_id = request.POST["usernameParticipantesCirugia_id"]
    print("username_id =", username_id)

    tipoHonorarios = request.POST["tipoHonorarios"]
    print("tipoHonorarios =", tipoHonorarios)

    estadoReg = 'A'
    fechaRegistro = timezone.now()



    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugiasparticipantes (finalidad_id, "fechaRegistro", "estadoReg", cirugia_id, "tipoHonorarios_id", "usuarioRegistro_id", medico_id, "cirugiaProcedimiento_id") VALUES (' + "'" + str(finalidadId) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(tipoHonorarios) + "','" + str(username_id) + "','" + str(medico) + "','" + str(procedParticipantes) + "')"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Participante Actualizado satisfactoriamente!'})


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


def BuscaProgramacionCirugia(request):
    print("Entre BuscaProgramacionCirugia")

    programacionId = request.POST.get('programacionId')
    print("programacionId =", programacionId)

    programacionId2 = ProgramacionCirugias.objects.get(id=programacionId)
    cirugiaId = programacionId2.cirugia_id

    sede = request.POST.get('sede')
    print("sede =", sede)
    print("cirugiaId =", cirugiaId)

    # Combo estadosProgramacion

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre nombre FROM  cirugia_estadosprogramacion p where nombre in ( " + "'" + str('Programada') + "','" + str('Cancelada')  + "')" + ' ORDER BY nombre'

    curt.execute(comando)
    print(comando)

    estadosProgramacion = []

    for id, nombre in curt.fetchall():
        estadosProgramacion.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("estadosProgramacion", estadosProgramacion)


    # Fin combo estadosProgramacion

    # Combo convenios paciente

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    #comando = "SELECT p.id id, p.nombre nombre FROM  cirugia_estadosprogramacion p where nombre in ( " + "'" + str('Programada') + "','" + str('Cancelada')  + "')" + ' ORDER BY nombre'
    comando = 'select conv.id, conv.nombre FROM cirugia_programacioncirugias prog LEFT JOIN facturacion_conveniospacienteingresos convIngreso ON (convIngreso."tipoDoc_id"= prog."tipoDoc_id" AND convIngreso.documento_id=prog.documento_id AND convIngreso."consecAdmision" = prog."consecAdmision") LEFT JOIN contratacion_convenios conv ON (conv.id = convIngreso.convenio_id) where prog.id = ' + "'" + str(programacionId) + "'"

    curt.execute(comando)
    print(comando)

    conveniosPaciente = []

    for id, nombre in curt.fetchall():
        conveniosPaciente.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("ConveniosPaciente", conveniosPaciente)


    # Fin combo estadosProgramacion


    # Combo procedParticipantes

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT p."cirugiaProcedimiento_id" id,exa.nombre nombre FROM cirugia_cirugiasparticipantes p INNER JOIN cirugia_cirugiasprocedimientos cirProc ON (cirProc.id=p."cirugiaProcedimiento_id") INNER JOIN clinico_examenes exa on (exa.id= cirProc.cups_id) where p.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    print(comando)
    curt.execute(comando)


    procedParticipantes = []

    for id, nombre in curt.fetchall():
        procedParticipantes.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("procedParticipantes", procedParticipantes)


    # Fin combo procedParticipantes


    # Fin combo estadosProgramacion

    # Combo procedMateriales

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT p."cirugiaProcedimiento_id" id,sum.nombre nombre FROM cirugia_cirugiasMaterialqx p INNER JOIN cirugia_cirugiasprocedimientos cirMat ON (cirMat.id=p."cirugiaProcedimiento_id") INNER JOIN facturacion_suministros sum on (sum.id= p.suministro_id) where p.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    print(comando)
    curt.execute(comando)


    procedMateriales = []

    for id, nombre in curt.fetchall():
        procedMateriales.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("procedMateriales", procedMateriales)


    # Fin combo procedParticipantes

    programacionCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    detalle = 'SELECT prog.id id,  u."tipoDoc_id" tipoDoc_id , u.documento documento, i.consec consecutivo, u.nombre paciente,estprog.id estado_id, estprog.nombre estadoProg,sala.id sala_id, sala.nombre sala, prog."fechaProgramacionInicia" inicia, prog."horaProgramacionInicia" horaInicia, prog."fechaProgramacionFin" termina, prog."horaProgramacionFin" horaTermina , prog."serviciosAdministrativos_id" serviciosAdministrativos_id FROM cirugia_programacioncirugias prog INNER JOIN sitios_sedesclinica sed	on (sed.id = prog."sedesClinica_id") INNER JOIN admisiones_ingresos i ON (i."tipoDoc_id" =prog."tipoDoc_id" AND i.documento_id =  prog.documento_id AND i.consec= prog."consecAdmision" ) INNER JOIN usuarios_usuarios u ON (u.id = i.documento_id ) INNER JOIN cirugia_estadosprogramacion estprog ON (estprog.id = prog."estadoProgramacion_id" ) LEFT JOIN sitios_salas sala ON (sala.id =prog.sala_id )  WHERE sed.id = ' + "'" + str(sede) + "' AND prog.id = " + "'" + str(programacionId) + "'"

    print(detalle)

    cur3.execute(detalle)

    for id, tipoDoc_id, documento, consecutivo, paciente, estado_id, estadoProg, sala_id, sala, inicia, horaInicia, termina, horaTermina , serviciosAdministrativos_id in cur3.fetchall():
        programacionCirugia.append(
            {"model": "cirugia.programcioncirugias", "pk": id, "fields":
                {'id': id, 'tipoDoc_id': tipoDoc_id, 'documento': documento, 'consecutivo': consecutivo,
                 'paciente': paciente, 'estado_id':estado_id, 'estadoProg': estadoProg, 'sala_id': sala_id, 'sala': sala,
                 'inicia': inicia, 'horaInicia': horaInicia,
                 'termina': termina, 'horaTermina': horaTermina,'serviciosAdministrativos_id':serviciosAdministrativos_id
                 }})


    miConexion3.close()
    print(programacionCirugia)

    programacionCirugia[0]['estadosProgramacion'] = estadosProgramacion
    programacionCirugia[0]['ProcedParticipantes'] = procedParticipantes
    programacionCirugia[0]['ProcedMateriales'] = procedMateriales
    programacionCirugia[0]['ConveniosPaciente'] = conveniosPaciente
    print(programacionCirugia)

    serialized1 = json.dumps(programacionCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def CrearMaterialCirugia(request):

    print ("Entre CrearMaterialCirugia", request )

    cirugiaId = request.POST.get('cirugiaIdModalMaterial')
    print ("cirugiaId =", cirugiaId)

    suministro = request.POST["suministro"]
    print ("suministro =", suministro)

    if 'hojaDeGastoInforme' in request.POST:
        hojaDeGasto = 'S'
    else:
        hojaDeGasto = 'N'


    print ("hojaDeGasto =", hojaDeGasto)

    procedMateriales = request.POST["procedMateriales"]
    print ("procedMateriales =", procedMateriales)

    username_id = request.POST["usernameMaterialCirugia_id"]
    print ("username_id =", username_id)

    cantidad = request.POST["cantidad"]
    print ("cantidad =", cantidad)

    unitario = request.POST["unitarioLiquidacion"]
    print ("unitario =", unitario)

    valorLiquidacion = request.POST["valorLiquidacionSolicitud"]
    print ("valorLiquidacion =", valorLiquidacion)

    estadoReg = 'A'
    fechaRegistro = timezone.now()


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugiasmaterialQx (cantidad, "fechaRegistro", "estadoReg", cirugia_id, suministro_id, "usuarioRegistro_id","cirugiaProcedimiento_id", unitario,"valorLiquidacion", "hojaDeGasto") VALUES (' + "'" + str(cantidad) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(suministro) + "','" + str(username_id)  + "','" + str(procedMateriales) + "','" + str(unitario) + "','" + str(valorLiquidacion) + "','" + str(hojaDeGasto) +  "')"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Material Actualizado satisfactoriamente!'})


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


def CrearMaterialInformeCirugia(request):

    print ("Entre CrearMaterialInformeCirugia" )

    cirugiaId = request.POST.get('cirugiaIdModalMaterialInforme')
    print ("cirugiaId =", cirugiaId)

    suministro = request.POST["suministroInforme"]
    print ("suministro =", suministro)

    if 'hojaDeGastoInforme' in request.POST:
        hojaDeGasto = 'S'
    else:
        hojaDeGasto = 'N'

    #hojaDeGasto = request.POST['hojaDeGastoInforme']

    print ("hojaDeGasto =", hojaDeGasto)

    username_id = request.POST["usernameMaterialInformeCirugia_id"]
    print ("username_id =", username_id)

    cantidad = request.POST["cantidadInforme"]
    print ("cantidad =", cantidad)

    unitario = request.POST["unitarioLiquidacionInforme"]
    print ("unitario =", unitario)

    valorLiquidacion = request.POST["valorLiquidacionInforme"]
    print ("valorLiquidacion =", valorLiquidacion)

    procedMaterialesInforme = request.POST["procedMaterialesInforme"]
    print ("procedMaterialesInforme =", procedMaterialesInforme)

    estadoReg = 'A'
    fechaRegistro = timezone.now()

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugiasmaterialQx (cantidad, "fechaRegistro", "estadoReg", cirugia_id, suministro_id, "usuarioRegistro_id", "valorLiquidacion", "cirugiaProcedimiento_id", unitario, "hojaDeGasto") VALUES (' + "'" + str(cantidad) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(suministro) + "','" + str(username_id) + "','" +  str(valorLiquidacion) + "','" + str(procedMaterialesInforme) + "','" + str(unitario) +   "','"  + str(hojaDeGasto) + "')"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Material Actualizado satisfactoriamente!'})


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



def BorraProcedimientosInformeCirugia(request):
    print("Entre BorraProcedimientosInformeCirugia")


    procedimientoId = request.POST.get('procedimientoId')
    print("procedimientoId =", procedimientoId)


    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'DELETE FROM cirugia_cirugiasprocedimientos Where id = ' + "'" + str(procedimientoId) + "'"

        print(detalle)
        cur3.execute(detalle)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Procedimiento cancelado!'})

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


def BorraParticipanteInformeCirugia(request):
    print("Entre BorraParticipanteInformeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)

    participanteId = request.POST.get('participanteId')
    print("participanteId =", participanteId)


    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'DELETE FROM cirugia_cirugiasparticipantes Where id = ' + "'" + str(participanteId) + "'"

        print(detalle)
        cur3.execute(detalle)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Participante cancelado!'})

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

def BorraMaterialInformeCirugia(request):
    print("Entre BorraMaterialInformeCirugia")


    materialId = request.POST.get('materialId')
    print("materialId =", materialId)


    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'DELETE FROM cirugia_CirugiasMaterialQx Where id = ' + "'" + str(materialId) + "'"

        print(detalle)
        cur3.execute(detalle)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Material cancelado!'})

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

def CrearAdicionQx(request):
    print("Entre CrearAdicionQx")


    cirugiaId = request.POST.get('cirugiaIdModalAdicionarQx')

    ciruIdd = Cirugias.objects.get(id=cirugiaId)
    print("ciruIdd =", ciruIdd.id)
    estadoConfirmadaId = EstadosCirugias.objects.get(nombre='REALIZADA')
    print(" estadoConfirmadaId = ", estadoConfirmadaId)

    ingresoQuirofano = request.POST.get('ingresoQuirofano')
    print("ingresoQuirofano", ingresoQuirofano)
    horaIngresoQuirofano =  ingresoQuirofano[11:19]
    print("horaIngresoQuirofano", horaIngresoQuirofano)
    print ("año = ", int(ingresoQuirofano[0:4]))
    print("mes = ", ingresoQuirofano[6:7])
    print("dia = ", ingresoQuirofano[9:11])


    ingresoQuirofano =  datetime.date(int(ingresoQuirofano[0:4]), int(ingresoQuirofano[6:7]), int(ingresoQuirofano[9:11]))
    print("ingresoQuirofano Formulado", ingresoQuirofano)


    fechaIniAnestesia = request.POST.get('fechaIniAnestesia2')
    horaIniAnestesia = fechaIniAnestesia[11:19]
    fechaIniAnestesia =  datetime.date(int(fechaIniAnestesia[0:4]), int(fechaIniAnestesia[5:7]), int(fechaIniAnestesia[8:11]))


    fechaQxIni = request.POST.get('fechaQxIni')
    horaQxIni = fechaQxIni[11:19]
    fechaQxIni =  datetime.date(int(fechaQxIni[0:4]), int(fechaQxIni[5:7]), int(fechaQxIni[8:11]))


    fechaQxFin = request.POST.get('fechaQxFin')
    horaQxFin = fechaQxFin[11:19]
    fechaQxFin =  datetime.date(int(fechaQxFin[0:4]), int(fechaQxFin[5:7]), int(fechaQxFin[8:11]))


    fechaFinAnestesia = request.POST.get('fechaFinAnestesia')
    horaFinAnestesia = fechaFinAnestesia[11:19]
    fechaFinAnestesia = datetime.date(int(fechaFinAnestesia[0:4]), int(fechaFinAnestesia[5:7]), int(fechaFinAnestesia[8:11]))


    ingresoQuirofano = request.POST.get('ingresoQuirofano')
    horaIngresoQuirofano = ingresoQuirofano[11:19]
    ingresoQuirofano = datetime.date(int(ingresoQuirofano[0:4]), int(ingresoQuirofano[5:7]), int(ingresoQuirofano[8:11]))


    #tiempoTotal = request.POST.get('tiempoTotal')
    #tiempoAnestesicoTotal = request.POST.get('tiempoAnestesicoTotal')
    #tiempoTotalEnSala = request.POST.get('tiempoTotalEnSala')
    ingresoRecuperacion = request.POST.get('ingresoRecuperacion')
    horaIngresoRecuperacion = ingresoRecuperacion[11:19]
    ingresoRecuperacion = datetime.date(int(ingresoRecuperacion[0:4]), int(ingresoRecuperacion[5:7]), int(ingresoRecuperacion[8:11]))


    salidaRecuperacion = request.POST.get('salidaRecuperacion')
    horaSalidaRecuperacion = salidaRecuperacion[11:19]
    salidaRecuperacion = datetime.date(int(salidaRecuperacion[0:4]), int(salidaRecuperacion[5:7]), int(salidaRecuperacion[8:11]))

    salidaQuirofano = request.POST.get('salidaQuirofano')
    horaSalidaQuirofano = salidaQuirofano[11:19]
    salidaQuirofano = datetime.date(int(salidaQuirofano[0:4]), int(salidaQuirofano[5:7]), int(salidaQuirofano[8:11]))

    #tiempoTotalRecuperacion = request.POST.get('tiempoTotalRecuperacion')

    dxPreOperatorio = request.POST.get('dxPreOperatorio')
    dxPostOperatorio = request.POST.get('dxPostOperatorio')
    impresionDx = request.POST.get('impresionDx')
    complicacionesDx = request.POST.get('complicacionesDx')

    print("antes complicacionesDx =" , complicacionesDx)
    print("ANTES dxPreOperatorio =", dxPreOperatorio)
    print("ANTES dxPostOperatorio =", dxPostOperatorio)

    if impresionDx == None:

           impresionDx='null'

    if complicacionesDx == None:

           complicacionesDx='null'

    if dxPreOperatorio == None:
           dxPreOperatorio='null'

    if dxPostOperatorio == None:
           dxPostOperatorio='null'

    print("complicacionesDx =" , complicacionesDx)
    print("dxPreOperatorio =", dxPreOperatorio)
    print("dxPostOperatorio =", dxPostOperatorio)

    formaRealizacion = request.POST.get('formaRealizacion')
    tejidoPatologia = request.POST.get('tejidoPatologia')
    tipoFractura = request.POST.get('tipoFractura')
    intensificador = request.POST.get('intensificador')

    descripcionQx = request.POST.get('descripcionQx')
    hallazgos = request.POST.get('hallazgos')
    analisis = request.POST.get('analisis')
    planx = request.POST.get('planx')

    sede = request.POST.get('cirugiaIdModalAdicionarQx')
    print("sede =", sede)

    estadoCirugiaId = EstadosCirugias.objects.get(nombre="REALIZADA")
    estadoRealizadaId = EstadosCirugias.objects.get(nombre='REALIZADA')
    print(" estadoRealizadaId = ", estadoRealizadaId)

    esTriage='N'
    try:
        with transaction.atomic():

           ingreso = Ingresos.objects.get(tipoDoc_id=ciruIdd.tipoDoc_id, documento_id=ciruIdd.documento_id, consec = ciruIdd.consecAdmision)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(tipoDoc_id=ciruIdd.tipoDoc_id, documento_id=ciruIdd.documento_id, consecAdmision = ciruIdd.consecAdmision)
            esTriage = 'S'

    finally:
        print("No haga nada")


    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()

            detalle = 'UPDATE cirugia_Cirugias SET "ingresoQuirofano" =  ' + "'" + str(ingresoQuirofano) + "'," + '"horaIngresoQuirofano" = ' + "'" + str(horaIngresoQuirofano) + "'," + '  "salidaQuirofano" =  ' + "'" + str(salidaQuirofano) + "'," + '"horaSalidaQuirofano" = ' + "'" + str(horaSalidaQuirofano)  + "'," + '"fechaIniAnestesia" = ' + "'" + str(fechaIniAnestesia) + "'," + '"HoraIniAnestesia" = ' + "'" + str(horaIniAnestesia) + "',"  + '"fechaQxInicial" = ' + "'" + str(fechaQxIni) + "'," + '"horaQxInicial" = ' + "'" + str(horaQxIni) + "'," + '"fechaQxFinal" = ' + "'" + str(fechaQxFin) + "'," + '"horaQxFinal" = ' + "'" + str(horaQxFin) + "'," + '"fechaFinAnestesia" = ' + "'" + str(fechaFinAnestesia) + "'," + '"horaFinAnestesia" = ' + "'" + str(horaFinAnestesia) + "'," + '"ingresoRecuperacion" = ' + "'" + str(ingresoRecuperacion) + "'," + '"horaIngresoRecuperacion" = ' + "'" + str(horaIngresoRecuperacion) + "'," + '"salidaRecuperacion" = ' + "'" + str(salidaRecuperacion) + "'," + '"horaSalidaRecuperacion" = ' + "'" + str(horaSalidaRecuperacion) + "'," + '"dxPreQx_id" = ' + str(dxPreOperatorio) + ","   + '"dxPostQx_id" = ' +  str(dxPostOperatorio) + ","  + '"impresionDx_id" = ' + str(impresionDx) + "," + '"dxComplicacion_id" = ' + str(complicacionesDx) + "," + '"formaRealiza" = ' + "'" + str(formaRealizacion) + "'," + '"patologia" = ' + "'" + str(tejidoPatologia) + "'," + '"tipofractura" = ' + "'" + str(tipoFractura) + "'," + '"intensificador" = ' + "'" + str(intensificador) + "'," + '"descripcionQx" = ' + "'" + str(descripcionQx) + "'," + '"hallazgos" = ' + "'" + str(hallazgos) + "'," + '"analisis" = ' + "'" + str(analisis) + "'," + '"planx" = ' + "'" + str(planx) + "'," + '"estadoCirugia_id" = ' + "'" + str(estadoCirugiaId.id) + "'" + ' Where id = ' + "'" + str(cirugiaId) + "'"

            print(detalle)
            cur3.execute(detalle)

            print("estadoConfirmadaId.id = ", estadoConfirmadaId.id)
            print("ciruIdd.estadoCirugia_id = ", ciruIdd.estadoCirugia_id)

            ##OPS aqi hay problema si se reversan los estados mas de una ez
            # mejor hacer un query u orm que cuente en clinico_historialcruiias <1 para n crear folios nuevo

            if (float(ciruIdd.estadoCirugia_id) != float(estadoConfirmadaId.id)):  # Hay que crear folio

                print("Pase pñrimer filtroio")

                if (float(ciruIdd.estadoCirugia_id) != float(estadoConfirmadaId.id)):

                    ## Desde aqui INSERT FOLIO

                    # Primero buscamos el numero del folio nuevo

                    print ("Entre a crear folio")

                    if (esTriage == 'N'):

                        ultimofolio = Historia.objects.all().filter(tipoDoc_id=ingreso.tipoDoc_id).filter(documento_id=ingreso.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))
                    else:
                        ultimofolio = Historia.objects.all().filter(tipoDoc_id=triageId.tipoDoc_id).filter(documento_id=triageId.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))

                    print("ultimo folio = ", ultimofolio)
                    print("ultimo folio = ", ultimofolio['maximo'])
                    ultimofolio2 = (ultimofolio['maximo']) + 1
                    print("ultimo folio2 = ", ultimofolio2)

                    # Segundo  INSERT en clinico_historial

                    if (esTriage == 'N'):

                        detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(
                            ingreso.consec) + "','" + str(ultimofolio2) + "','" + str(fechaRegistro) + "','" + str(
                            fechaRegistro) + "','" + str(estadoReg) + "','" + str(ingreso.documento_id) + "','" + str(
                            ingreso.tipoDoc_id) + "','" + str(username_id) + "','" + str(tiposFolio.id) + "','" + str(
                            username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"
                    else:
                        detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(
                            triageId.consec) + "','" + str(ultimofolio2) + "','" + str(fechaRegistro) + "','" + str(
                            fechaRegistro) + "','" + str(estadoReg) + "','" + str(triageId.documento_id) + "','" + str(
                            triageId.tipoDoc_id) + "','" + str(username_id) + "','" + str(tiposFolio.id) + "','" + str(
                            username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"

                    print(detalle)
                    resultado = cur3.execute(detalle)
                    historiaId = cur3.fetchone()[0]
                    print("historiaId = ", historiaId)

                    detalle = 'INSERT INTO clinico_historialcirugias ("estadoReg",cirugia_id, historia_id, "usuarioRegistro_id")  VALUES (' + "'A','" + str(cirugiaId) + "','" + str(historiaId) + "','" + str(username_id) + "')"
                    print(detalle)
                    cur3.execute(detalle)

            print("poraqui salgo")

            miConexion3.commit()
            cur3.close()
            miConexion3.close()

            return JsonResponse({'success': True, 'Mensajes': 'Cirugia Actualizada!'})


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


def Load_dataHojaDeGastoCirugia(request, data):
    print("Entre Load_dataHojaDeGastoCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    hojaDeGastoCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    comando = 'select cirmaterial.id id, cirmaterial.cirugia_id cirugia_id, cirmaterial.suministro_id suministro_id, suministros.nombre suministro , tipo.nombre tipoSuministro , cirmaterial.cantidad cantidad FROM cirugia_hojasdegastos cirmaterial INNER JOIN facturacion_suministros suministros ON ( suministros.id = cirmaterial.suministro_id) INNER JOIN facturacion_tipossuministro tipo ON (tipo.id = suministros."tipoSuministro_id") WHERE cirmaterial.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id,  cirugia_id, suministro_id, suministro , tipoSuministro, cantidad  in cur3.fetchall():
        hojaDeGastoCirugia.append(
            {"model": "cirugia.jojadegasto", "pk": id, "fields":
                {'id': id, 'cirugia_id':cirugia_id ,  'suministro_id': suministro_id, 'suministro': suministro, 'tipoSuministro': tipoSuministro ,'cantidad':cantidad     }})

    miConexion3.close()
    print(hojaDeGastoCirugia)

    serialized1 = json.dumps(hojaDeGastoCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataHojaDeGastoXXCirugia(request, data):
    print("Entre Load_dataHojaDeGastoXXCirugia")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    cirugiaId = d['cirugiaId']
    print("cirugiaId =", cirugiaId)

    hojaDeGastoCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    comando = 'select cirmaterial.id id, cirmaterial.cirugia_id cirugia_id, cirmaterial.suministro_id suministro_id, suministros.nombre suministro , tipo.nombre tipoSuministro , cirmaterial.cantidad cantidad FROM cirugia_hojasdegastos cirmaterial INNER JOIN facturacion_suministros suministros ON ( suministros.id = cirmaterial.suministro_id) INNER JOIN facturacion_tipossuministro tipo ON (tipo.id = suministros."tipoSuministro_id") WHERE cirmaterial.cirugia_id = ' + "'" + str(cirugiaId) + "'"

    print(comando)
    cur3.execute(comando)

    for id,  cirugia_id, suministro_id, suministro , tipoSuministro, cantidad  in cur3.fetchall():
        hojaDeGastoCirugia.append(
            {"model": "cirugia.jojadegastoXX", "pk": id, "fields":
                {'id': id, 'cirugia_id':cirugia_id ,  'suministro_id': suministro_id, 'suministro': suministro, 'tipoSuministro': tipoSuministro ,'cantidad':cantidad     }})

    miConexion3.close()
    print(hojaDeGastoCirugia)

    serialized1 = json.dumps(hojaDeGastoCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def CrearHojaDeGastoCirugia(request):

    print ("Entre CrearHojaDeGastoCirugia" )

    cirugiaId = request.POST.get('cirugiaIdModalHojaDeGastoCirugia')
    print ("cirugiaId =", cirugiaId)

    suministro = request.POST["suministroHojaDeGasto"]
    print ("suministro =", suministro)

    username_id = request.POST["usernameHojaDeGastoCirugia_id"]
    print ("username_id =", username_id)

    cantidad = request.POST["cantidadHojaDeGasto"]
    print ("cantidad =", cantidad)



    estadoReg = 'A'
    fechaRegistro = timezone.now()



    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_hojasdegastos (cantidad, "fechaRegistro", "estadoReg", cirugia_id, suministro_id, "usuarioRegistro_id") VALUES (' + "'" + str(cantidad) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(suministro) + "','" + str(username_id) + "')"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Hoja De Gastos  Actualizado satisfactoriamente!'})


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

def BorraHojaDeGastoCirugia(request):
    print("Entre BorraHojadeGastoCirugia")


    hojaDeGastoId = request.POST.get('hojaDeGastoId')
    print("materialId =", hojaDeGastoId)


    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'DELETE FROM cirugia_hojasdegastos Where id = ' + "'" + str(hojaDeGastoId) + "'"

        print(detalle)
        cur3.execute(detalle)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Hoja de Gasto cancelado!'})

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


def BuscaAdicionarQx(request):
    print("Entre BuscaAdicionarQx")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)
    sede = request.POST.get('sede')
    print("sede =", sede)

    adicionarQx = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    detalle = 'SELECT cir.id, cir."ingresoQuirofano"||' + "'" +  str(' ' ) + "'" +   '||cir."horaIngresoQuirofano" ingresoQuirofano,cir."fechaIniAnestesia"||' + "'" +  str(' ' ) + "'" +  '||cir."HoraIniAnestesia" fechaIniAnestesia,cir."fechaQxInicial"||' + "'" +  str(' ' ) + "'" +  '||cir."horaQxInicial" fechaQxIni,cir."fechaQxFinal"||' + "'" +  str(' ' ) + "'" +  '||cir."horaQxFinal" fechaQxFin, cir."fechaFinAnestesia"||' + "'" +  str(' ' ) + "'" +  '||cir."horaFinAnestesia" fechaFinAnestesia, cir."salidaQuirofano"||' + "'" +  str(' ' ) + "'" +   '||cir."horaSalidaQuirofano" salidaQuirofano , cir."ingresoRecuperacion"||' + "'" +  str(' ' ) + "'" +   '||cir."horaIngresoRecuperacion" ingresoRecuperacion, cir."salidaRecuperacion"||' + "'" +  str(' ' ) + "'" +   '||cir."horaSalidaRecuperacion" salidaRecuperacion ,"dxPreQx_id" dxPreOperatorio, "dxPostQx_id" dxPostOperatorio, "impresionDx_id" impresionDx, "dxComplicacion_id" complicacionesDx,"formaRealiza" formaRealizacion,patologia tejidoPatologia, "tipofractura" tipoFractura, intensificador intensificador,"descripcionQx" descripcionQx, hallazgos hallazgos, analisis analisis, planx planx FROM cirugia_cirugias cir WHERE id = ' + "'" + str(cirugiaId) + "'"

    print(detalle)

    cur3.execute(detalle)

    for id, ingresoQuirofano,fechaIniAnestesia,fechaQxIni,fechaQxFin,fechaFinAnestesia,salidaQuirofano,ingresoRecuperacion,salidaRecuperacion,	dxPreOperatorio,dxPostOperatorio,impresionDx,complicacionesDx,formaRealizacion,tejidoPatologia,tipoFractura,intensificador,	descripcionQx,	hallazgos,analisis,planx  in cur3.fetchall():
        adicionarQx.append(
            {"model": "cirugia.programcioncirugias", "pk": id, "fields":
                {'id': id, 'ingresoQuirofano': ingresoQuirofano, 'fechaIniAnestesia': fechaIniAnestesia, 'fechaQxIni': fechaQxIni,
                 'fechaQxFin': fechaQxFin, 'fechaFinAnestesia':fechaFinAnestesia, 'salidaQuirofano': salidaQuirofano, 'ingresoRecuperacion': ingresoRecuperacion, 'salidaRecuperacion': salidaRecuperacion,
                 'dxPreOperatorio': dxPreOperatorio, 'dxPostOperatorio': dxPostOperatorio,
                 'impresionDx': impresionDx, 'complicacionesDx': complicacionesDx,'formaRealizacion':formaRealizacion, 'tejidoPatologia':tejidoPatologia, 'tipoFractura':tipoFractura,'intensificador':intensificador, 'descripcionQx':descripcionQx, 'hallazgos':hallazgos, 'analisis':analisis, 'planx':planx
                 }})


    miConexion3.close()
    print(adicionarQx)

    serialized1 = json.dumps(adicionarQx, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def SeleccionProgramacionCirugia(request):
    print("Entre SeleccionProgramacionCirugia")

    programacionId = request.POST.get('programacionId')
    print("programacionId =", programacionId)

    registroProgramacion = ProgramacionCirugias.objects.get(id=programacionId)
    registroCirugia = Cirugias.objects.get(tipoDoc_id=registroProgramacion.tipoDoc_id, documento_id=registroProgramacion.documento_id, consecAdmision = registroProgramacion.consecAdmision)

    serialized1 = json.dumps(registroCirugia.id, default=str)

    return HttpResponse(serialized1, content_type='application/json')



def GuardarEstadoProgramacionCirugia(request):
    print("Entre GuardarEstadoProgramacionCirugia")

    programacionId = request.POST.get('programacionId')
    print("programacionId =", programacionId)

    estadoId = request.POST.get('estadoId')
    print("estadoId =", estadoId)

    estadoCancelado = EstadosProgramacion.objects.get(nombre='Cancelada')
    print("estadoCancelado = " , estadoCancelado.id )

    programacionEstadoAnterior = ProgramacionCirugias.objects.get(id=programacionId)

    print("programacionEstadoAnterior_1 = ", programacionEstadoAnterior.id)

    cirugiaId = Cirugias.objects.get(tipoDoc_id =programacionEstadoAnterior.tipoDoc_id, documento_id=programacionEstadoAnterior.documento_id , consecAdmision = programacionEstadoAnterior.consecAdmision)

    print ("programacionEstadoAnterior = " , programacionEstadoAnterior.estadoProgramacion_id)

    if (programacionEstadoAnterior.estadoProgramacion_id == estadoCancelado.id):
        print ("Entre a NO PERMITIR GUARDAR=")
        return JsonResponse({'success': False, 'message': 'Estado Programacion Cancelado no se puede Actualizar!'})


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'UPDATE cirugia_programacioncirugias set  "estadoProgramacion_id" = ' + "'" + str(estadoId) + "'" + ' WHERE id = ' + "'" + str(programacionId) + "'"

        print(detalle)

        cur3.execute(detalle)

        detalle1 = 'UPDATE cirugia_cirugias set  "estadoProgramacion_id" = ' + "'" + str(estadoId) + "'" + ' WHERE id = ' + "'" + str(cirugiaId.id) + "'"

        print(detalle1)

        cur3.execute(detalle1)



        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Estado Programacion Actualizado!'})

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


def GuardarEstadoCirugia(request):
    print("Entre GuardarEstadonCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)

    estadoId = request.POST.get('estadoId')
    print("estadoId =", estadoId)

    username_id = request.POST.get('username_id')
    print("username_id =", username_id)

    estadoConfirmadaId = EstadosCirugias.objects.get(nombre='REALIZADA')
    print(" estadoConfirmadaId = ", estadoConfirmadaId)

    ciruIdd = Cirugias.objects.get(id=cirugiaId)
    print("ciruIdd =", ciruIdd.id)

    print("ciruIdd.tipoDoc_Id =", ciruIdd.tipoDoc_id)


    serviciosAdministrativos = ciruIdd.serviciosAdministrativos_id
    print(" serviciosAdministrativos = ", serviciosAdministrativos)

    tiposFolio = TiposFolio.objects.get(nombre='CIRUGIA')
    print(" tiposFolio = ", tiposFolio.id)

    estadoReg='A'
    fechaRegistro = timezone.now()

    sede = request.POST['sede']
    print ("sede =", sede)


    esTriage='N'
    try:
        with transaction.atomic():

           #ingreso = Ingresos.objects.get(id=ingresoId.id)
           ingreso = Ingresos.objects.get(tipoDoc_id=ciruIdd.tipoDoc_id, documento_id=ciruIdd.documento_id, consec = ciruIdd.consecAdmision)
           print ("ingresoId =", ingreso)

    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por PRONO SE HACE NADA:", e)
            triageId = Triage.objects.get(tipoDoc_id=ciruIdd.tipoDoc_id, documento_id=ciruIdd.documento_id, consecAdmision = ciruIdd.consecAdmision)
            esTriage = 'S'

    finally:
        print("No haga nada")



    estadoReg = 'A'
    fechaRegistro = timezone.now()

    # Busco la cirugia relacionado, esperando que no hayan ms de una cirugia. OPS
    #registroProgramacion = ProgramacionCirugias.objects.get(id=programacionId)
    #registroCirugia = Cirugias.objects.get(tipoDoc_id=registroProgramacion.tipoDoc_id, documento_id=registroProgramacion.documento_id, consecAdmision=registroProgramacion.consecAdmision)


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        detalle = 'UPDATE cirugia_cirugias set  "estadoCirugia_id" = ' + "'" + str(estadoId) + "'" + ' WHERE id = ' + "'" + str(cirugiaId) + "'"

        print(detalle)

        cur3.execute(detalle)

        print("estadoId = " , estadoId)
        print("estadoConfirmadaId.id = ", estadoConfirmadaId.id)
        print("ciruIdd.estadoCirugia_id = ", ciruIdd.estadoCirugia_id)

        if (float(estadoId) == float(estadoConfirmadaId.id)):  # Hay que crear folio

            print("Pase pñrimer filtroio")

            if (float(ciruIdd.estadoCirugia_id) != float(estadoConfirmadaId.id)):

                ## Desde aqui INSERT FOLIO

                # Primero buscamos el numero del folio nuevo

                print ("Entre a crear folio")

                if (esTriage == 'N'):

                    ultimofolio = Historia.objects.all().filter(tipoDoc_id=ingreso.tipoDoc_id).filter(documento_id=ingreso.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))
                else:
                    ultimofolio = Historia.objects.all().filter(tipoDoc_id=triageId.tipoDoc_id).filter(documento_id=triageId.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))


                print("ultimo folio = ", ultimofolio)
                print("ultimo folio = ", ultimofolio['maximo'])
                ultimofolio2 = (ultimofolio['maximo']) + 1
                print("ultimo folio2 = ", ultimofolio2)

                # Segundo  INSERT en clinico_historial

                if (esTriage == 'N'):

                    detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(
                        ingreso.consec) + "','" + str(ultimofolio2) + "','" + str(fechaRegistro) + "','" + str(
                        fechaRegistro) + "','" + str(estadoReg) + "','" + str(ingreso.documento_id) + "','" + str(
                        ingreso.tipoDoc_id) + "','" + str(username_id) + "','" + str(tiposFolio.id) + "','" + str(
                        username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"
                else:
                    detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(
                        triageId.consec) + "','" + str(ultimofolio2) + "','" + str(fechaRegistro) + "','" + str(
                        fechaRegistro) + "','" + str(estadoReg) + "','" + str(triageId.documento_id) + "','" + str(
                        triageId.tipoDoc_id) + "','" + str(username_id) + "','" + str(tiposFolio.id) + "','" + str(
                        username_id) + "','" + str(sede) + "','" + str(serviciosAdministrativos) + "') RETURNING id"

                print(detalle)
                resultado = cur3.execute(detalle)
                historiaId = cur3.fetchone()[0]
                print("historiaId = ", historiaId)

                detalle = 'INSERT INTO clinico_historialcirugias ("estadoReg",cirugia_id, historia_id, "usuarioRegistro_id")  VALUES (' + "'A','" + str(cirugiaId) + "','" + str(historiaId) + "','" + str(username_id) + "')"
                print(detalle)
                cur3.execute(detalle)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Estado Cirugia Actualizado!'})

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


def GenerarLiquidacionCirugia(request):
    print("Entre GenerarLiquidacionCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)
    username_id = request.POST.get('username_id')
    print("username_id =", username_id)
    sede = request.POST.get('sede')
    print("sede =", sede)

    estadoReg='A'
    fechaRegistro = timezone.now()


    # Busco Tipos de honorarios,
    registroHonorarioCirujano = TiposHonorarios.objects.get(nombre='CIRUJANO')
    registroHonorarioAnestesiologo = TiposHonorarios.objects.get(nombre='ANESTESIOLOGO')
    registroHonorarioAyudante = TiposHonorarios.objects.get(nombre='AYUDANTE')
    #registroHonorarioPerfisionista = TiposHonorarios.objects.get(nombre='PERFUSIONISTA')
    registroDerechosSala = TiposHonorarios.objects.get(nombre='DERECHOS DE SALA')
    registroMateriales = TiposHonorarios.objects.get(nombre='MATERIALES DE SUTURA Y CURACIO')

    # Busco datos de la cirugia relacionado,
    registroCirugia = Cirugias.objects.get(id=cirugiaId)

    #AQui valido si es estado de la cirugia es apta para liquidar 

    estadoConfirmada = EstadosCirugias.objects.get(nombre='CONFIRMADA')
    estadoRealizada = EstadosCirugias.objects.get(nombre='REALIZADA')

    if (registroCirugia.estadoCirugia_id != estadoRealizada.id):

           return JsonResponse({'success': False, 'Mensajes': 'Cirugia de paciente No esta REALIZADA !'})


    registroConvenio = registroCirugia.convenio_id
    print("registroConvenio =", registroConvenio)
    # Busco convenio del paciente

    #miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
    #                               password="123456")
    #cur3 = miConexion3.cursor()

    #detalle = 'SELECT min(convenio_id) convenioId FROM facturacion_ConveniosPacienteIngresos WHERE "tipoDoc_id" = ' + "'" + str(registroCirugia.tipoDoc_id) + "' AND documento_id = '"  +  str(registroCirugia.documento_id) + "' AND " + '"consecAdmision" = ' + "'" + str(registroCirugia.consecAdmision) + "'"

    #print(detalle)

    #registroConvenio = []

    #cur3.execute(detalle)

    #for convenioId in cur3.fetchall():
    #    registroConvenio.append({'convenioId': convenioId})


    #print("registroConvenio =" , registroConvenio[0])
    #print("registroConvenio =" , registroConvenio[0]['convenioId'])


    #cur3.close()

    #registroConvenio = str(registroConvenio[0]['convenioId'])
    #registroConvenio = registroConvenio.replace("(", ' ')
    #registroConvenio = registroConvenio.replace(")", ' ')
    #registroConvenio = registroConvenio.replace(",", ' ')

    #registroConvenio = ConveniosPacienteIngresos.objects.annotate(convenioMinimo=Min('convenio_id')).filter(tipoDoc_id=registroCirugia.tipoDoc_id, documento_id=registroCirugia.documento_id,consecAdmision=registroCirugia.consecAdmision,convenio_id=F('convenioMinimo'))
    #registroConvenio = ConveniosPacienteIngresos.objects.filter(tipoDoc_id=registroCirugia.tipoDoc_id, documento_id=registroCirugia.documento_id,consecAdmision=registroCirugia.consecAdmision).annotate(convenioMinimo=Min('convenio_id')).filter(convenio_id=F('convenioMinimo'))
    print("registroConvenio =" , registroConvenio)


    # Busco cual es Liquiacion de Honorarios de paciente
    #registroConvenio = registroConvenio.objects.get(tipoDoc_id=registroCirugia.tipoDoc_id, documento_id=registroCirugia.documento_id,consecAdmision=registroCirugia.consecAdmision)

    #Busco la forma de liquidacion

    registroliquidacion = Convenios.objects.get(id=registroConvenio)

    print("registroliquidacion = ", registroliquidacion)
    print("registroliquidacion.tarifariosDescripcionHono_id = ", registroliquidacion.tarifariosDescripcionHono_id)

    # Busco Tipo de liquidacion Honorario. O sea como voy a liquidar el honorario

    registroliquidacionHonorario = TarifariosDescripcionHonorarios.objects.get(id=registroliquidacion.tarifariosDescripcionHono_id)

    if (registroliquidacionHonorario.id == 1):   # ISS 2001

        # Consigue procedimientos a facturar

        miConexion3 = None
        try:
            print("Entre por liquiacion ISS")
            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()


            detalle = 'SELECT cups_id cups FROM cirugia_cirugiasprocedimientos WHERE cirugia_id = ' + "'" + str(cirugiaId) + "'"

            print(detalle)

            cupsLiquidacion = []

            cur3.execute(detalle)

            for cups in cur3.fetchall():
                cupsLiquidacion.append({'cups':cups})


            print("cups =" , cupsLiquidacion)

            # Validacion si existe o No existe CABEZOTE

            comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + "'" + str(registroCirugia.tipoDoc_id) + "' AND documento_id = " + "'" + str(registroCirugia.documento_id) + "'" + ' AND "consecAdmision" = ' + "'" + str(registroCirugia.consecAdmision) + "'"
            cur3.execute(comando)

            cabezoteLiquidacion = []

            for id in cur3.fetchall():
                cabezoteLiquidacion.append({'id': id})

            print("CABEZOTE DE LIQUIDACION = ", cabezoteLiquidacion);

            if (cabezoteLiquidacion == []):

                comando = 'INSERT INTO facturacion_liquidacion ("sedesClinica_id", "tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos") VALUES (' + "'" + str(
                    sede) + "'," + "'" + str(registroCirugia.tipoDoc_id) + "','" + str(registroCirugia.documento_id) + "','" + str(
                    registroCirugia.consecAdmision) + "','" + str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(
                    fechaRegistro) + "','" + str(estadoReg) + "'," + str(
                    registroConvenio.convenio_id) + ',' + "'" + str(username_id) + "',0) RETURNING id "
                cur3.execute(comando)
                liquidacionId = curt.fetchone()[0]

                print("resultado liquidacionId = ", liquidacionId)

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

            # Primero que todo borrar lo ya liquidado , para volver a hacer una nueva liquidacion

            comando = 'DELETE FROM facturacion_liquidaciondetalle p WHERE liquidacion_id = ' + "'" + str(liquidacionId) + "' AND cirugia_id = " + "'" + str(cirugiaId) + "'"

            cur3.execute(comando)

            # Aqui RUTINA busca consecutivo de liquidacion


            comando = 'SELECT (max(p.consecutivo)) cons FROM facturacion_liquidaciondetalle p WHERE liquidacion_id = ' + liquidacionId

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
                consecLiquidacion = 0


            # Aqui liquidacion de Materiales INSUMOS MEDICOS. No Materiales Quirugicos van a la cuenta
            # uN SOLO INGESO PR TODOS LOS MATERIALES QUE NO SEN MATERIAL QX
            # esto d earriba no esta bien EXPLICADO

            suministroMaterial = TiposSuministro.objects.get(nombre='MATERIAL QX')
            suministroMaterialQx=suministroMaterial.id
            honorarioMaterial = TiposHonorarios.objects.get(nombre='MATERIAL QX')
            honorarioMaterialqX = honorarioMaterial.id


            detalle = 'select matqx.suministro_id suministro, sum.nombre nomSuministro , tipos.nombre tipo ,matqx."valorLiquidacion" valorLiquidacionMat from cirugia_cirugiasmaterialqx matqx, facturacion_suministros sum, facturacion_tipossuministro tipos where matqx.cirugia_id= ' + "'" + str(cirugiaId) + "'" + ' and matqx.suministro_id = sum.id and sum."tipoSuministro_id" = tipos.id  AND tipos.id != ' + "'" + str(suministroMaterialQx) + "' AND " + 'matqx."hojaDeGasto" = ' + "'" + str('N') + "'"


            materialesQx = []

            print(detalle)
            cur3.execute(detalle)

            for suministro, nomSuministro, tipo, valorLiquidacionMat  in cur3.fetchall():
                materialesQx.append({'suministro': suministro, 'nomSuministro':nomSuministro, 'tipo':tipo, 'valorLiquidacionMat':valorLiquidacionMat})

            print("materialesQx = " , materialesQx)

            # Materialde sutura y conexion

            for matQx in materialesQx:

                suministro = str(matQx['suministro'])
                suministro = suministro.replace("(", ' ')
                suministro = suministro.replace(")", ' ')
                suministro = suministro.replace(",", ' ')

                valorLiquidacionMat = str(matQx['valorLiquidacionMat'])
                valorLiquidacionMat = valorLiquidacionMat.replace("(", ' ')
                valorLiquidacionMat = valorLiquidacionMat.replace(")", ' ')
                valorLiquidacionMat = valorLiquidacionMat.replace(",", ' ')

                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "cums_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro)  + "','" + str(suministro) + "','" + str(username_id) + "'," + liquidacionId + ",'MANUAL'," + "null," +  "'" + str(cirugiaId) + "','N')"
                print ("comando ", comando)
                cur3.execute(comando)

                # En teoria hasta aqui Materiales de sutura  ISS de acuerdo al procedimiento
                #

            pasada=0
            ## DESDE AQUI CADA PROCEDIMIENTO

            print("paso_Procedikientos")

            for procedimiento1 in cupsLiquidacion:

                pasada = pasada +1

                procedimiento = str(procedimiento1['cups'])
                procedimiento = procedimiento.replace("(", ' ')
                procedimiento = procedimiento.replace(")", ' ')
                procedimiento = procedimiento.replace(",", ' ')
                print("procedimiento por el FORSEGUNDO = " ,procedimiento)
                procedimiento =procedimiento.strip()

                ## Aqui rutina para subir la tarifa del procedimiento como tal a Liquidaciondetalle
                # RUTINA encuentra columna de dondel LEER la tarifa.
                #
                #try:
                #    with transaction.atomic():

                 #       contratacion = Convenios.objects.get(id=registroConvenio)

                  #      print("OJOO contratacion.tarifariosDescripcionProc_id = ", contratacion.tarifariosDescripcionProc_id)

                  #      columnaALeer = TarifariosDescripcion.objects.get(id=contratacion.tarifariosDescripcionProc_id)
                  #      columnaALeerPropia = columnaALeer.columna

                #except Exception as e:
                    # Aquí ya se hizo rollback automáticamente
                    #print("Se hizo rollback de Convenio TarifarioDescripcion por:", e)
                    #error_data = {
                    #    'type': type(e).__name__,
                    #    'message': str(e),
                    #    'traceback': traceback.format_exc()
                    #}
                    #columnaALeerPropia = ''

                #finally:
                 #   print("Finally")

               # print("Columna a leer = ", columnaALeerPropia)
               # FIN RUTINA encuentra columna de dondel LEER la tarifa.

                ## Desde Aqui rutina de Facturacion Para Procedimientos
                #

               # Fin rutina Facturacion Procedimientos detalle

            # AQUI RUTINA SUBE HONORARIO MATERIALES DE CIRUGIA POR PROCEDIMIENTO

                #detalle = 'select sum(matqx."valorLiquidacion") valorLiquidacionMat  from cirugia_cirugiasmaterialqx matqx, facturacion_suministros sum, facturacion_tipossuministro tipos  , cirugia_cirugiasprocedimientos cirProc where matqx.cirugia_id= ' + "'" + str(cirugiaId) + "'" + ' and matqx.suministro_id = sum.id and sum."tipoSuministro_id" = tipos.id  AND tipos.id = ' + "'" + str(suministroMaterialQx) + "'" + 'and cirProc.id = matqx."cirugiaProcedimiento_id" and cirProc.cups_id= ' + "'" + str(procedimiento) + "'"

                detalle = 'select matIss.homologado homologado1 , matIss.valor valorLiquidacionMat1 FROM clinico_examenes exa INNER JOIN tarifarios_tablamaterialsuturacuracioniss matIss on (matIss."desdeUvr" <= exa."cantidadUvr" AND matIss."hastaUvr" >= exa."cantidadUvr") INNER JOIN sitios_tipossalas tipsal ON (tipsal.id =matIss."tiposSala_id") INNER JOIN cirugia_cirugias cir on (cir.id = ' + "'" + str(cirugiaId) + "')" + ' INNER JOIN sitios_salas sal ON (sal.id=cir.sala_id and sal."tipoSala_id" = tipsal.id)  WHERE exa.id = ' + "'" + str(procedimiento) + "'"

                materialesQx = []

                print(detalle)
                cur3.execute(detalle)

                for homologado1,valorLiquidacionMat1 in cur3.fetchall():
                    materialesQx.append({'homologado1':homologado1, 'valorLiquidacionMat1': valorLiquidacionMat1})

                    print("materialesQx = ", materialesQx)

                    # Materialde sutura y conexion

                    valorLiquidacionMat = valorLiquidacionMat1
                    print ("valorLiquidacionMat =", valorLiquidacionMat)
                    homologado = homologado1
                    print ("homologado =", homologado)

                    if (homologado=='None'):
                        homologado=''

                    print("valorLiquidacionMat =" , valorLiquidacionMat)

                    if (valorLiquidacionMat==None):
                        print ("Entre None")
                        valorLiquidacionMat=0
                        

                    print("valorLiquidacionMat FINAL =", valorLiquidacionMat)

                    consecLiquidacion = int(consecLiquidacion) + 1

                    comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,examen_id,"codigoHomologado") VALUES (' + "'" + str(
                        consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(
                        valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(
                        fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA','"+  str(honorarioMaterial.id) + "','"  + str(cirugiaId) + "','N'," + "'" + str(procedimiento)  + "','" + str(homologado) + "')"
                    print("comando ", comando)
                    cur3.execute(comando)

                # En teoria hasta aqui Materiales de sutura  ISS de acuerdo al procedimiento
                # fin rutina sube HONORARIO MATERIAL QX

                ## Fin rutina para subir la tarifa del procedimiento como tal a Liquidaciondetalle

                # consigue La cantidad de uvr del procedimiento

                detalle = 'SELECT "cantidadUvr" cantidadUvr FROM clinico_examenes WHERE id = ' + "'" + str(procedimiento) + "'"

                cantidadUvrProced = []

                cur3.execute(detalle)

                for cantidadUvr in cur3.fetchall():

                    cantidadUvrProced.append({'cantidadUvr': cantidadUvr })

                for cantidadUvrProced in cantidadUvrProced[0]['cantidadUvr']:

                    cantidadUvrProced = cantidadUvrProced

                print("cantidadUvrProced =" , cantidadUvrProced)

                # consigo valor De 1 Uver a pagar al cirujano

                detalle = 'SELECT homologado, "valorUvr" valorUvrCirujano FROM tarifarios_tablahonorariosiss WHERE id = ' + "'" + str(registroHonorarioCirujano.id) + "'"

                valorUvrCirujanoProced = []

                cur3.execute(detalle)

                for homologado, valorUvrCirujano in cur3.fetchall():
                    valorUvrCirujanoProced.append({'homologado':homologado,'valorUvrCirujano': valorUvrCirujano })

                    print("valorUvrCirujanoProced =" , valorUvrCirujanoProced[0]['valorUvrCirujano'])
                    valorUvrCirujanoProced = valorUvrCirujanoProced[0]['valorUvrCirujano']
                #for valorUvrCirujanoProced in valorUvrCirujanoProced[0]['valorUvrCirujano']:
                    print("valorUvrCirujanoProced1" , valorUvrCirujanoProced)

                    liquidaCirujano= float(valorUvrCirujanoProced) * float(cantidadUvrProced)
                    print ("liquidaCirujano =",liquidaCirujano )
                    homologadoCirujano = homologado			

                # En teoria hasta aqui tengo el valor del Cirujano ISS de acuerdo al procedimiento

                # Aqui liquidacion de honorarios Anestesiologo

                # consigo valor De 1 Uver a pagar al Anestesiologo

                detalle = 'SELECT homologado, "valorUvr" valorUvrAnestesiologo FROM tarifarios_tablahonorariosiss WHERE id = ' + "'" + str(registroHonorarioAnestesiologo.id) + "'"

                valorUvrAnestesiologoProced = []

                cur3.execute(detalle)

                for homologado, valorUvrAnestesiologo in cur3.fetchall():
                    valorUvrAnestesiologoProced.append({'homologado':homologado,'valorUvrAnestesiologo': valorUvrAnestesiologo })

                    print("valorUvrAnestesiologoProced =" , valorUvrAnestesiologoProced[0]['valorUvrAnestesiologo'])

                #for valorUvrAnestesiologoProced in valorUvrAnestesiologoProced[0]['valorUvrAnestesiologo']:
                    print("valorUvrAnestesiologoProced = " ,valorUvrAnestesiologoProced)
                    valorUvrAnestesiologoProced = valorUvrAnestesiologoProced[0]['valorUvrAnestesiologo']
                    liquidaAnestesiologo= float(valorUvrAnestesiologoProced) * float(cantidadUvrProced)
                    print("liquidaAnestesiologo =", liquidaAnestesiologo)
                    homologadoAnestesiologo = homologado			

                # En teoria hasta aqui honorariosAnestesiologo ISS de acuerdo al procedimiento

                # Aqui liquidacion de honorarios Ayudante

                # consigo valor De 1 Uver a pagar al Ayudante

                detalle = 'SELECT homologado,"valorUvr" valorUvrAyudante FROM tarifarios_tablahonorariosiss WHERE id = ' + "'" + str(registroHonorarioAyudante.id) + "'"

                valorUvrAyudanteProced = []

                cur3.execute(detalle)

                for homologado,valorUvrAyudante in cur3.fetchall():
                    valorUvrAyudanteProced.append(
                        {'homologado':homologado, 'valorUvrAyudante': valorUvrAyudante })

                    print("valorUvrAyudanteProced =" , valorUvrAyudanteProced[0]['valorUvrAyudante'])

                #for valorUvrAyudanteProced in valorUvrAyudanteProced[0]['valorUvrAyudante']:
                    print(valorUvrAyudanteProced)
                    valorUvrAyudanteProced = valorUvrAyudanteProced[0]['valorUvrAyudante']
                    liquidaAyudante= float(valorUvrAyudanteProced) * float(cantidadUvrProced)
                    print("liquidaAyudante =", liquidaAyudante)
                    homologadoAyudante = homologado

                # En teoria hasta aqui honorarios Ayudante ISS de acuerdo al procedimiento

                # Aqui INSERT a la tabla lioquidaciones de los valores liquidados para un procedimiento

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
                print("consecLiquidacion = ", consecLiquidacion)

                if consecLiquidacion.strip() == 'None':
                    print("consecLiquidacion = ", consecLiquidacion)
                    consecLiquidacion = 1

                # Fin RUTINA busca consecutivo de liquidacion
                # Cirujano
                print("paso_1")
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal","estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id , anulado, "codigoHomologado") VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaCirujano) + "','" + str(liquidaCirujano) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioCirujano.id)  + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoCirujano) + "')"
                print("comando ", comando)
                cur3.execute(comando)
                # Anestesiologo
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro","fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado, "codigoHomologado") VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAnestesiologo) + "','" + str(liquidaAnestesiologo) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAnestesiologo.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAnestesiologo) + "')"
                print("comando ", comando)
                cur3.execute(comando)

                # Ayudante
                consecLiquidacion= int(consecLiquidacion) + 1
                print("paso_2")
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",  "estadoRegistro", "fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado, "codigoHomologado") VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAyudante) + "','" + str(liquidaAyudante) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) +  "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAyudante.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAyudante) + "')"
                print("comando ", comando)
                cur3.execute(comando)

                print("ANTES DE pasada = ", pasada)

                # Aqui liquidacion de Salas de CIRUGIA

                print ("Entre pasada = ", pasada)

                ## Luego ir a tabla tarifarios_tablaSalasdecirugiaiss para sacar el valor
                #
                detalle = 'SELECT tarifa.homologado homologado,tarifa.valor valor FROM cirugia_cirugias cir, sitios_tipossalas tipsal, tarifarios_tablaSalasdecirugiaiss tarifa, sitios_salas sala WHERE cir.id = ' + "'" + str(cirugiaId) + "'" + ' AND cir.sala_id = sala.id and sala."tipoSala_id" = tipsal.id and tarifa."tiposSala_id" = tipsal.id and ' + "'" + str(cantidadUvrProced) + "'" + ' between tarifa."desdeUvr" AND tarifa."hastaUvr"'
                valorSala = []
                print(detalle)
                cur3.execute(detalle)

                for homologado, valor in cur3.fetchall():
                    valorSala.append({'homologado':homologado, 'valor': valor})

                    #valorSala = valorSala[0]

                    liquidaValorSala = valor
                    liquidaValorHomologado = homologado
                    print("liquidaValorSala = ", liquidaValorSala)
                    print("liquidaValorHomologado = ", liquidaValorHomologado)

                # Salas
                #
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,"codigoHomologado") VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaValorSala) + "','" + str(liquidaValorSala) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro)  + "','" + str(procedimiento)  + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroDerechosSala.id)+ "'," +  "'" + str(cirugiaId) + "','N','" + str(liquidaValorHomologado) +  "')"
                print("comando", comando)
                cur3.execute(comando)

                # En teoria hasta aqui Salas de CIRUGIA  ISS de acuerdo al procedimiento

            # Fin INSERT liquidaciones


            miConexion3.commit()
            cur3.close()
            miConexion3.close()

            # return JsonResponse({'success': True, 'Mensajes': 'Liquidacion Honorarios Iss cargada a cuenta Paciente Verificar valores !'})

        except NotFoundError:
            # Code to handle the FileNotFoundError
            print("Registro No encontrado")


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



    if (registroliquidacionHonorario.id == 2):   # SOAT 2004

        # Consigue procedimientos a facturar

        miConexion3 = None
        try:
            print("Entre por liquiacion SOAT")
            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()


            detalle = 'SELECT cups_id cups FROM cirugia_cirugiasprocedimientos WHERE cirugia_id = ' + "'" + str(cirugiaId) + "'"

            print(detalle)

            cupsLiquidacion = []

            cur3.execute(detalle)

            for cups in cur3.fetchall():
                cupsLiquidacion.append({'cups':cups})


            print("cups =" , cupsLiquidacion)

            # Validacion si existe o No existe CABEZOTE

            comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + "'" + str(registroCirugia.tipoDoc_id) + "' AND documento_id = " + "'" + str(registroCirugia.documento_id) + "'" + ' AND "consecAdmision" = ' + "'" + str(registroCirugia.consecAdmision) + "'"
            cur3.execute(comando)

            cabezoteLiquidacion = []

            for id in cur3.fetchall():
                cabezoteLiquidacion.append({'id': id})

            print("CABEZOTE DE LIQUIDACION = ", cabezoteLiquidacion);

            if (cabezoteLiquidacion == []):

                comando = 'INSERT INTO facturacion_liquidacion ("sedesClinica_id", "tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos") VALUES (' + "'" + str(
                    sede) + "'," + "'" + str(registroCirugia.tipoDoc_id) + "','" + str(registroCirugia.documento_id) + "','" + str(
                    registroCirugia.consecAdmision) + "','" + str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(
                    fechaRegistro) + "','" + str(estadoReg) + "'," + str(
                    registroConvenio.convenio_id) + ',' + "'" + str(username_id) + "',0) RETURNING id "
                cur3.execute(comando)
                liquidacionId = curt.fetchone()[0]

                print("resultado liquidacionId = ", liquidacionId)

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

            # Primero que todo borrar lo ya liquidado , para volver a hacer una nueva liquidacion

            comando = 'DELETE FROM facturacion_liquidaciondetalle p WHERE liquidacion_id = ' + "'" + str(liquidacionId) + "' AND cirugia_id = " + "'" + str(cirugiaId) + "'"

            cur3.execute(comando)

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
                consecLiquidacion = 0

            suministroMaterial = TiposSuministro.objects.get(nombre='MATERIAL QX')
            suministroMaterialQx=suministroMaterial.id
            honorarioMaterial = TiposHonorarios.objects.get(nombre='MATERIAL QX')
            honorarioMaterialqX = honorarioMaterial.id


            # Aqui liquidacion de Materiales INSUMOS MEDICOS NO MATERIAL QX 

            detalle = 'select matqx.suministro_id suministro, sum.nombre nomSuministro , tipos.nombre tipo ,matqx.cantidad cantidad, matqx."valorLiquidacion" valorLiquidacionMat from cirugia_cirugiasmaterialqx matqx, facturacion_suministros sum, facturacion_tipossuministro tipos where matqx.cirugia_id= ' + "'" + str(cirugiaId) + "'" + ' and matqx.suministro_id = sum.id and sum."tipoSuministro_id" = tipos.id AND tipos.id != ' + "'" + str(suministroMaterialQx) + "'"

            materialesQx = []

            print(detalle)
            cur3.execute(detalle)

            for suministro, nomSuministro, tipo, cantidad, valorLiquidacionMat  in cur3.fetchall():
                materialesQx.append({'suministro': suministro, 'nomSuministro':nomSuministro, 'tipo':tipo, 'cantidad' :cantidad, 'valorLiquidacionMat':valorLiquidacionMat})

            print("materialesQx = " , materialesQx)


            # Materialde sutura y conexion

            for matQx in materialesQx:

                suministro = str(matQx['suministro'])
                suministro = suministro.replace("(", ' ')
                suministro = suministro.replace(")", ' ')
                suministro = suministro.replace(",", ' ')

                valorLiquidacionMat = str(matQx['valorLiquidacionMat'])
                valorLiquidacionMat = valorLiquidacionMat.replace("(", ' ')
                valorLiquidacionMat = valorLiquidacionMat.replace(")", ' ')
                valorLiquidacionMat = valorLiquidacionMat.replace(",", ' ')

                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "cums_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str(cantidad) + "','" + str(valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro)  + "','" + str(suministro) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(honorarioMaterialqX) +  "'," +  "'" + str(cirugiaId) + "','N')"
                print ("comando ", comando)
                cur3.execute(comando)

                # En teoria hasta aqui Materiales SOAT de acuerdo al procedimiento
                #

            pasada=0


            for procedimiento1 in cupsLiquidacion:

                pasada = pasada +1

                procedimiento = str(procedimiento1['cups'])
                procedimiento = procedimiento.replace("(", ' ')
                procedimiento = procedimiento.replace(")", ' ')
                procedimiento = procedimiento.replace(",", ' ')
                print("procedimiento por el FORSEGUNDO = " ,procedimiento)
                procedimiento =procedimiento.strip()

            # AQUI RUTINA SUBE HONORARIO MATERIALES DE CIRUGIA POR PROCEDIMIENTO

                detalle = 'select sum(matqx."valorLiquidacion") valorLiquidacionMat  from cirugia_cirugiasmaterialqx matqx, facturacion_suministros sum, facturacion_tipossuministro tipos  , cirugia_cirugiasprocedimientos cirProc where matqx.cirugia_id= ' + "'" + str(cirugiaId) + "'" + ' and matqx.suministro_id = sum.id and sum."tipoSuministro_id" = tipos.id  AND tipos.id = ' + "'" + str(suministroMaterialQx) + "'" + 'and cirProc.id = matqx."cirugiaProcedimiento_id" and cirProc.cups_id= ' + "'" + str(procedimiento) + "'"
                #detalle = 'select matSoat.homologado homologado1 , matSoat.smldv valorLiquidacionMat1 FROM clinico_examenes exa INNER JOIN tarifarios_tablamaterialsuturacuracion matSoat on (matSoat."grupoQx_id" <= exa."cantidadUvr" AND matIss."hastaUvr" >= exa."cantidadUvr") INNER JOIN 	sitios_tipossalas tipsal ON (tipsal.id =matIss."tiposSala_id" and tipsal.id = ' + "'" + str(registroCirugia.sala_id) + "'" + ' ) WHERE exa.id = ' + "'" + str(procedimiento) + "'"

                detalle = 'select matSoat.homologado homologado1 , matSoat.smldv * minLeg.valor/30 valorLiquidacionMat1 FROM clinico_examenes exa INNER JOIN tarifarios_tablamaterialsuturacuracion matSoat on (matSoat."grupoQx_id" = exa."grupoQx_id") INNER JOIN 	tarifarios_minimoslegales minLeg ON (minLeg.id =matSoat."minimosLegales_id") WHERE exa.id = ' + "'" + str(procedimiento) + "'"

                materialesQx = []

                print(detalle)
                cur3.execute(detalle)

                for homologado1 ,valorLiquidacionMat in cur3.fetchall():
                    materialesQx.append({'homologado1':homologado1, 'valorLiquidacionMat': valorLiquidacionMat})

                    print("materialesQx = ", materialesQx)

                # Materialde sutura y conexion

                    valorLiquidacionMat = valorLiquidacionMat
                    print ("valorLiquidacionMat =", valorLiquidacionMat)

                    homologado = homologado1
                    print ("homologado =", homologado)

                    if (homologado==None):
                        homologado=0

                    if (valorLiquidacionMat==None):
                        print ("Entre None")
                        valorLiquidacionMat=0

                    print("valorLiquidacionMat FINAL =", valorLiquidacionMat)
                    print("homologado FINAL =", homologado)

                    consecLiquidacion = int(consecLiquidacion) + 1

                    comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,examen_id,  "codigoHomologado") VALUES (' + "'" + str(
                        consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(
                        valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(
                        fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA','"+  str(honorarioMaterial.id) + "','"  + str(cirugiaId) + "','N'," + "'" + str(procedimiento)  + "','" + str(homologado) + "')"
                    print("comando ", comando)
                    cur3.execute(comando)

                # En teoria hasta aqui Materiales de sutura  ISS de acuerdo al procedimiento
                # fin rutina sube HONORARIO MATERIAL QX

                # consigue año de programacion de cirugia
                #
                progCiru = Cirugias.objects.get(id=cirugiaId)
                fecha = progCiru.fechaProg
                print("fecha = ", fecha)
                año = fecha.year

                print("año = ", año)
 
                # consigue el salario minimo Legal
                #
                minimo = MinimosLegales.objects.get(año=año)
                print("minimo = ", minimo.valor)

                minimo = minimo.valor
                print("minimo = ", minimo)

                # consigue Grupo de procedimiento

                detalle = 'SELECT "grupoQx_id" grupoQx FROM clinico_examenes WHERE id = ' + "'" + str(procedimiento) + "'"

                grupoQx1 = []

                cur3.execute(detalle)

                for grupoQx  in cur3.fetchall():

                    grupoQx1.append({'grupoQx': grupoQx })

                for grupoQx1 in grupoQx1[0]['grupoQx']:

                    grupoQx = grupoQx1

                print("grupoQx =" , grupoQx)

                # consigo la tarifa del honorario SOAT a pagar al cirujano

                detalle = 'SELECT homologado,  "smldv" * ' + "'" + str(minimo/30) + "'" + ' valorCirujano FROM tarifarios_tablahonorariossoat WHERE "grupoQx_id" = ' + "'" + str(grupoQx) + "' AND " + '"tiposHonorarios_id" = ' + "'" + str(registroHonorarioCirujano.id)  + "'"

                valorCirujanoProced = []

                cur3.execute(detalle)


                for homologado, valorCirujano in cur3.fetchall():
                    valorCirujanoProced.append({'homologado':homologado, 'valorCirujano': valorCirujano })
                    print("valorCirujanoProced =" , valorCirujanoProced)
                    liquidaCirujano = float(valorCirujano)
                    homologadoCirujano = homologado

                if valorCirujanoProced == []:
                    liquidaCirujano = 0

                if homologadoCirujano == None:
                    homologadoCirujano = ''

                # En teoria hasta aqui tengo el valor del Cirujano ISS de acuerdo al procedimiento


                # Aqui liquidacion de honorarios Anestesiologo

                # consigo valor a pagar al Anestesiologo


                detalle = 'SELECT homologado, "smldv" * ' + "'" + str(minimo/30) + "'" + ' valorAnestesiologo FROM tarifarios_tablahonorariossoat WHERE "grupoQx_id" = ' + "'" + str(grupoQx) + "' AND " + '"tiposHonorarios_id" = ' + "'" + str(registroHonorarioAnestesiologo.id)  + "'"

                valorAnestesiologoProced = []

                cur3.execute(detalle)

                for homologado, valorAnestesiologo in cur3.fetchall():
                    valorAnestesiologoProced.append({'homologado':homologado, 'valorAnestesiologo': valorAnestesiologo })
                    liquidaAnestesiologo= float(valorAnestesiologo)
                    homologadoAnestesiologo = homologado

                if valorAnestesiologoProced == []:
                    liquidaAnestesiologo = 0

                if homologadoAnestesiologo == '':
                    homologadoAnestesiologo = ''

                # En teoria hasta aqui honorariosAnestesiologo ISS de acuerdo al procedimiento

                # Aqui liquidacion de honorarios Ayudante

                # consigo valor a pagar al Ayudante

                detalle = 'SELECT homologado, "smldv" * ' + "'" + str(minimo/30) + "'" + ' valorAyudante FROM tarifarios_tablahonorariossoat WHERE "grupoQx_id" = ' + "'" + str(grupoQx) + "' AND " + '"tiposHonorarios_id" = ' + "'" + str(registroHonorarioAyudante.id)  + "'"

                valorAyudanteProced = []

                cur3.execute(detalle)

                for homologado, valorAyudante in cur3.fetchall():
                    valorAyudanteProced.append(
                        {'homologado':homologado, 'valorAyudante': valorAyudante })
                    liquidaAyudante= float(valorAyudante)
                    homologadoAyudante= homologado

                if valorAyudanteProced == []:
                    liquidaAyudante= 0

                if homologadoAyudante == None:
                        homologadoAyudante = ''


                print("liquidaAyudante =", liquidaAyudante)

                # En teoria hasta aqui honorarios Ayudante ISS de acuerdo al procedimiento

                # Aqui INSERT a la tabla lioquidaciones de los valores liquidados para un procedimiento

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
                print("consecLiquidacion = ", consecLiquidacion)

                if consecLiquidacion.strip() == 'None':
                    print("consecLiquidacion = ", consecLiquidacion)
                    consecLiquidacion = 1

                # Fin RUTINA busca consecutivo de liquidacion
                # Cirujano
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal","estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id , anulado, "codigoHomologado") VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaCirujano) + "','" + str(liquidaCirujano) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioCirujano.id)  + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAyudante) + "')"
                print("comando ", comando)
                cur3.execute(comando)
                # Anestesiologo
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro","fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,  "codigoHomologado" ) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAnestesiologo) + "','" + str(liquidaAnestesiologo) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAnestesiologo.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAnestesiologo) + "')"
                print("comando ", comando)
                cur3.execute(comando)

                # Ayudante
                consecLiquidacion= int(consecLiquidacion) + 1

                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",  "estadoRegistro", "fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,  "codigoHomologado") VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAyudante) + "','" + str(liquidaAyudante) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) +  "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAyudante.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAyudante) + "')"
                print("comando ", comando)
                cur3.execute(comando)

                print("ANTES DE pasada = ", pasada)

                # Aqui liquidacion de Salas de CIRUGIA

                print ("Entre pasada = ", pasada)

                ## Luego ir a tabla tarifarios_tablaSalasdecirugiaiss para sacar el valor
                #
                #
                detalle = 'SELECT tarifa.homologado homologado, tarifa.smldv * ' + "'" + str(minimo/30) + "'" + ' valor FROM cirugia_cirugias cir,  tarifarios_tablaSalasdecirugia tarifa WHERE cir.id = ' + "'" + str(cirugiaId) + "'" + ' AND  "grupoQx_id" =  ' + "'" + str(grupoQx) + "'"

                valorSala = []
                print(detalle)
                cur3.execute(detalle)

                for homologado, valor in cur3.fetchall():
                    valorSala.append({'homologado':homologado, 'valor': valor})

                    liquidaValorSala = valor
                    liquidaValorHomologado = homologado


                if valorSala == []:
                    liquidaValorSala = 0

                if liquidaValorHomologado == None:
                    liquidaValorHomologado = ''

                # Salas
                #
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,  "codigoHomologado") VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaValorSala) + "','" + str(liquidaValorSala) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro)  + "','" + str(procedimiento)  + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroDerechosSala.id)+ "'," +  "'" + str(cirugiaId) + "','N','" + str(liquidaValorHomologado) + "')"
                print("comando", comando)
                cur3.execute(comando)

                # En teoria hasta aqui Salas de CIRUGIA  SOAT de acuerdo al procedimiento

            # Fin INSERT liquidaciones


            miConexion3.commit()
            cur3.close()
            miConexion3.close()

            #return JsonResponse({'success': True, 'Mensajes': 'Liquidacion Honorarios Soat cargada a cuenta Paciente Verificar valores !'})

        except psycopg2.Error as e:

            print(f"Database error: {e}")


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



    if (registroliquidacionHonorario.id == 3):  # PARTICULAR

        miConexion3 = None
        try:
            print("Entre por liquiacion PARTICULAR")
            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()

            # Fin RUTINA busca consecutivo de liquidacion
            # Cirujano
            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str('0') + "','" + str('0') + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioCirujano.id) + "'," +  "'" + str(cirugiaId) + "','N')"
            cur3.execute(comando)
            # Anestesiologo
            consecLiquidacion = consecLiquidacion + 1
            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str('0') + "','" + str('0') + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAnestesiologo.id) + "'," +  "'" + str(cirugiaId) + "','N')"
            cur3.execute(comando)

            # Ayudante
            consecLiquidacion = consecLiquidacion + 1
            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str('0') + "','" + str('0') + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAyudante.id) + "'," +  "'" + str(cirugiaId) + "','N')"
            cur3.execute(comando)

            # Salas
            consecLiquidacion = consecLiquidacion + 1

            # Materialde sutura y conexion
            consecLiquidacion = consecLiquidacion + 1

            # Fin INSERT liquidaciones

            miConexion3.commit()
            cur3.close()
            miConexion3.close()

            #return JsonResponse({'success': True, 'Mensajes': 'Liquidacion Honorarios Particular cargada a cuenta Paciente Verificar valores !'})

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



    ##Aqui RUTINA QUE ACTUALIZE TOTALES
        ## Vamops a actualizar los totales de la Liquidacion:
        #
    totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(examen_id=None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
    totalSuministros = (totalSuministros['totalS']) + 0
    print("totalSuministros", totalSuministros)
    totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(cums_id=None).exclude(estadoRegistro='I').exclude(anulado='S').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
    totalProcedimientos = (totalProcedimientos['totalP']) + 0
    print("totalProcedimientos", totalProcedimientos)
    registroPago = Liquidacion.objects.get(id=liquidacionId)

    # Continua Aqui

    totalCopagos = Pagos.objects.all().filter(tipoDoc_id=registroCirugia.tipoDoc_id).filter(documento_id=registroCirugia.documento_id).filter(consec=registroCirugia.consecAdmision).filter(formaPago_id=4).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalC=Coalesce(Sum('valorEnCurso'), 0))
    totalCopagos = (totalCopagos['totalC']) + 0
    print("totalCopagos", totalCopagos)
    totalCuotaModeradora = Pagos.objects.all().filter(tipoDoc_id=registroCirugia.tipoDoc_id).filter(documento_id=registroCirugia.documento_id).filter(consec=registroCirugia.consecAdmision).filter(formaPago_id=3).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalM=Coalesce(Sum('valorEnCurso'), 0))
    totalCuotaModeradora = (totalCuotaModeradora['totalM']) + 0
    print("totalCuotaModeradora", totalCuotaModeradora)
    totalAnticipos = Pagos.objects.all().filter(tipoDoc_id=registroCirugia.tipoDoc_id).filter(documento_id=registroCirugia.documento_id).filter(consec=registroCirugia.consecAdmision).filter(formaPago_id=1).exclude(estadoReg='I').exclude(anulado='S').aggregate(Anticipos=Coalesce(Sum('valorEnCurso'), 0))
    totalAnticipos = (totalAnticipos['Anticipos']) + 0
    print("totalAnticipos", totalAnticipos)
    totalAbonos = Pagos.objects.all().filter(tipoDoc_id=registroCirugia.tipoDoc_id).filter(documento_id=registroCirugia.documento_id).filter(consec=registroCirugia.consecAdmision).filter(formaPago_id=2).exclude(estadoReg='I').exclude(anulado='S').aggregate(totalAb=Coalesce(Sum('valorEnCurso'), 0))
    totalAbonos = (totalAbonos['totalAb']) + 0
    # totalAbonos = totalCopagos + totalAnticipos + totalCuotaModeradora
    print("totalAbonos", totalAbonos)

    totalRecibido = totalCopagos + totalCuotaModeradora + totalAnticipos + totalAbonos
    totalApagar = float(totalSuministros) + float(totalProcedimientos) - float(totalRecibido)
    totalLiquidacion = float(totalSuministros) + float(totalProcedimientos)
    print("totalLiquidacion", totalLiquidacion)
    print("totalAPagar", totalApagar)

    # Rutina Guarda en cabezote los totales

    print("Voy a grabar el cabezote")

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + "'" + str(totalSuministros) + "'" + ',"totalProcedimientos" = ' + "'" + str(totalProcedimientos) + "'"  + ', "totalCopagos" = ' + "'"  + str(totalCopagos) + "'" + ' , "totalCuotaModeradora" = ' + "'"  + str(totalCuotaModeradora) + "'"  + ', anticipos = ' + "'" + str(totalAnticipos) + "'" + ' ,"totalAbonos" = ' + "'" + str(totalAbonos) + "'"  + ', "totalLiquidacion" = ' + "'" + str(totalLiquidacion) + "'" + ', "valorApagar" = ' + "'"  + str(totalApagar) + "'" + ', "totalRecibido" = ' + "'" + str(totalRecibido) + "'" + ' WHERE id =' + str(liquidacionId)
        cur3.execute(comando)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Cargos de honoracios trasladados a cuenta Paciente!'})

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


        ## FIN rutina de Facturacion Para Medicamentos Total


    ##Fin rutina actualiza totales


def BuscarProcedimientosDeCirugia(request):
    print("Entre buscarProcedimientosDeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)

    cupsParticipantesInforme = []
    cupsParticipantesInforme.append({'id': '', 'nombre': ''})


    # Combo procedParticipantes

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT p."cirugiaProcedimiento_id" id,exa.nombre nombre FROM cirugia_cirugiasparticipantes p INNER JOIN cirugia_cirugiasprocedimientos cirProc ON (cirProc.id=p."cirugiaProcedimiento_id") INNER JOIN clinico_examenes exa on (exa.id= cirProc.cups_id) where p.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    print(comando)
    curt.execute(comando)


    procedParticipantesInforme = []

    for id, nombre in curt.fetchall():
        procedParticipantesInforme.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("procedParticipantesInforme", procedParticipantesInforme)


    # Fin combo procedParticipantes



    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    detalle = 'SELECT exa.id id, exa.nombre nombre FROM cirugia_cirugiasprocedimientos cirproc, clinico_examenes exa WHERE cirproc.cirugia_id = ' + "'" + str(cirugiaId) + "'" + ' AND exa.id = cirproc.cups_id'

    print(detalle)

    cur3.execute(detalle)

    for id, nombre  in cur3.fetchall():
        cupsParticipantesInforme.append(
            {'id': id, 'nombre': nombre})


    miConexion3.close()
    print(cupsParticipantesInforme)

    estadoCirugia = Cirugias.objects.get(id=cirugiaId)
    estadoNombreCirugia = EstadosCirugias.objects.get(id=estadoCirugia.estadoCirugia_id)

    print ("estadoNombreCirugia = " , estadoNombreCirugia.nombre )

    cupsParticipantesInforme[0]['EstadoNombreCirugia'] = estadoNombreCirugia.nombre
    cupsParticipantesInforme[0]['ProcedParticipantesInforme'] = procedParticipantesInforme

    serialized1 = json.dumps(cupsParticipantesInforme, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def BuscarProcedimientosParticipantesDeCirugia(request):
    print("Entre BuscarProcedimientosParticipantesDeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)


    # Combo procedParticipantes

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    #comando = 'SELECT p."cirugiaProcedimiento_id" id,exa.nombre nombre FROM cirugia_cirugiasparticipantes p INNER JOIN cirugia_cirugiasprocedimientos cirProc ON (cirProc.id=p."cirugiaProcedimiento_id") INNER JOIN clinico_examenes exa on (exa.id= cirProc.cups_id) where p.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    comando = 'SELECT cirProc.id id,exa.nombre nombre FROM  cirugia_cirugiasprocedimientos cirProc LEFT JOIN cirugia_cirugiasparticipantes cirPart ON (cirPart.cirugia_id = cirProc.cirugia_id AND cirPart."cirugiaProcedimiento_id" = cirProc.id) LEFT JOIN clinico_examenes exa on (exa.id= cirProc.cups_id) where cirProc.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    print(comando)
    curt.execute(comando)


    procedParticipantes = []

    for id, nombre in curt.fetchall():
        procedParticipantes.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("procedParticipantes", procedParticipantes)


    serialized1 = json.dumps(procedParticipantes, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def BuscarProcedimientosMaterialesDeCirugia(request):
    print("Entre BuscarProcedimientosMaterialesDeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)

    # Combo procedParticipantes

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT cirProc.id id,exa.nombre nombre FROM  cirugia_cirugiasprocedimientos cirProc LEFT JOIN clinico_examenes exa on (exa.id= cirProc.cups_id) where cirProc.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    print(comando)
    curt.execute(comando)


    procedMaterialesInforme = []

    for id, nombre in curt.fetchall():
        procedMaterialesInforme.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("procedMaterialesInforme", procedMaterialesInforme)


    serialized1 = json.dumps(procedMaterialesInforme, default=str)

    return HttpResponse(serialized1, content_type='application/json')




def TraerInformacionDeCirugia(request):
    print("Entre TraerInformacionDeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)

    informacionDeCirugia = []


    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    detalle = 'select cir.id id, est.nombre estadoCirugia, tipo.nombre tipoDoc, usu.documento documento , usu.nombre paciente, sala.nombre sala FROM cirugia_cirugias cir INNER JOIN cirugia_estadoscirugias est ON (est.id = cir."estadoCirugia_id") INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id" = cir."tipoDoc_id" AND usu.id = cir.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") LEFT JOIN sitios_salas sala ON (sala.id = cir.sala_id) WHERE cir.id = ' + "'" + str(cirugiaId) + "'"
    print(detalle)

    cur3.execute(detalle)

    for id, estadoCirugia, tipoDoc, documento, paciente, sala  in cur3.fetchall():
        informacionDeCirugia.append(
            {'id': id, 'estadoCirugia':estadoCirugia, 'tipoDoc': tipoDoc,'documento':documento,'paciente':paciente, 'sala':sala  })


    miConexion3.close()
    print(informacionDeCirugia)

    serialized1 = json.dumps(informacionDeCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def TraerEstadoCirugia(request):
    print("Entre TraerEstadoCirugia")

    programacionId = request.POST.get('programacionId')
    print("programacionId =", programacionId)

    registroProgramacion = ProgramacionCirugias.objects.get(id=programacionId)



    registroCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()


    detalle = 'select cir.id id, est.id  estadoCirugia_id ,est.nombre estadoCirugia, tipo.nombre tipoDoc, usu.documento documento , usu.nombre paciente, sala.nombre sala FROM cirugia_cirugias cir INNER JOIN cirugia_estadoscirugias est ON (est.id = cir."estadoCirugia_id") INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id" = cir."tipoDoc_id" AND usu.id = cir.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") LEFT JOIN sitios_salas sala ON (sala.id = cir.sala_id)' + ' WHERE cir."tipoDoc_id" = ' + "'" + str(registroProgramacion.tipoDoc_id) + "' AND cir.documento_id = '" + str(registroProgramacion.documento_id) + "'"+  ' AND cir."consecAdmision" = ' + "'"  + str(registroProgramacion.consecAdmision) + "'"
    print(detalle)

    cur3.execute(detalle)

    for id, estadoCirugia_id, estadoCirugia, tipoDoc, documento, paciente, sala in cur3.fetchall():
        registroCirugia.append(
            {'id': id, 'estadoCirugia_id':estadoCirugia_id, 'estadoCirugia': estadoCirugia, 'tipoDoc': tipoDoc, 'documento': documento, 'paciente': paciente,
             'sala': sala})

    miConexion3.close()
    print(registroCirugia)

    #registroCirugia = Cirugias.objects.get(tipoDoc_id=registroProgramacion.tipoDoc_id, documento_id=registroProgramacion.documento_id, consecAdmision = registroProgramacion.consecAdmision)

    serialized1 = json.dumps(registroCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def TraerEstadoProgramacionCirugia(request):
    print("Entre TraerEstadoProgramacionCirugia")

    programacionId = request.POST.get('programacionId')
    print("programacionId =", programacionId)

    registroProgramacionCirugia = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    detalle = 'select prog.id id, est.id  estadoProgramacionCirugia_id ,est.nombre estadoProgramacionCirugia, sala.nombre sala FROM cirugia_programacioncirugias prog INNER JOIN cirugia_estadosprogramacion est ON (est.id = prog."estadoProgramacion_id")  LEFT JOIN sitios_salas sala ON (sala.id = prog.sala_id)' + ' WHERE prog.id = ' + "'" + str(programacionId) + "'"
    print(detalle)

    cur3.execute(detalle)

    for id, estadoProgramacionCirugia_id, estadoProgramacionCirugia , sala in cur3.fetchall():
        registroProgramacionCirugia.append(
            {'id': id, 'estadoProgramacionCirugia_id':estadoProgramacionCirugia_id, 'estadoProgramacionCirugia': estadoProgramacionCirugia, 'sala': sala})

    miConexion3.close()
    print(registroProgramacionCirugia)

    #registroCirugia = Cirugias.objects.get(tipoDoc_id=registroProgramacion.tipoDoc_id, documento_id=registroProgramacion.documento_id, consecAdmision = registroProgramacion.consecAdmision)

    serialized1 = json.dumps(registroProgramacionCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def BuscarConveniosCirugiaPaciente(request):
    print("Entre buscarConveniosCirugiaPaciente")

    ingresoId = request.POST.get('ingresoId')
    print("ingresoId =", ingresoId)

    registroIngreso = Ingresos.objects.get(id=ingresoId)

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    detalle = 'SELECT c.id id, c.nombre nombre FROM  contratacion_convenios c ,facturacion_conveniospacienteingresos p	where p."tipoDoc_id" = ' + "'" + str(registroIngreso.tipoDoc_id) + "'" + ' AND p.documento_id = ' + "'" + str(registroIngreso.documento_id)  + "'" + ' AND p."consecAdmision" =  ' + "'" + str(registroIngreso.consec)  + "'" + ' AND  c.id=p.convenio_id'

    conveniosPacienteCirugia = []

    print(detalle)

    cur3.execute(detalle)

    for id, nombre in cur3.fetchall():
        conveniosPacienteCirugia.append(
            {'id': id, 'nombre':nombre})

    miConexion3.close()
    print(conveniosPacienteCirugia)

    serialized1 = json.dumps(conveniosPacienteCirugia, default=str)

    return HttpResponse(serialized1, content_type='application/json')

