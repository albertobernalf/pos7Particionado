from django.shortcuts import render
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
from django.http import JsonResponse
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
from clinico.models import Servicios, EspecialidadesMedicos, TiposFolio, Historia, Examenes, TiposExamen, HistorialCirugias
from rips.models import RipsTransaccion, RipsUsuarios, RipsEnvios, RipsDetalle, RipsTiposNotas
from tarifarios.models import TiposTarifa, TiposTarifaProducto, TiposHonorarios, TarifariosDescripcionHonorarios ,MinimosLegales, TiposHonorarios
import io
import pandas as pd
from cirugia.models import EstadosCirugias, EstadosSalas, EstadosProgramacion, ProgramacionCirugias, Cirugias, ProgramacionCirugias, ViasDeAcceso
from contratacion.models import Convenios
from django.db.models import Min, Max, Avg
from django.db.models import F
from django.db import transaction, IntegrityError
from django.utils import timezone
from contratacion.models import  ConveniosLiquidacionTarifasHonorarios
from tarifarios.models import TarifariosDescripcion , TiposHonorarios
from cirugia import viewsReportes
from autorizaciones.models import EstadosAutorizacion

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
    estadoConDescripcionQx = EstadosCirugias.objects.get(nombre='CON DESCRIPCION QX')



    programacionCirugias = []

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT prog.id id,  u."tipoDoc_id" tipoDoc_id ,tipdoc.abreviatura abrev, u.documento documento, i.consec consecutivo, u.nombre paciente,estprog.nombre estadoProg,sala.numero, sala.nombre sala, prog."fechaProgramacionInicia" inicia, prog."horaProgramacionInicia" horaInicia, prog."fechaProgramacionFin" Termina, prog."horaProgramacionFin" horaTermina ,(SELECT exa.nombre FROM cirugia_cirugias cir LEFT JOIN cirugia_cirugiasprocedimientos cirproc on (cirproc.cirugia_id = cir.id) INNER JOIN clinico_examenes exa on (exa.id = cirproc.cups_id) WHERE cir."tipoDoc_id" = prog."tipoDoc_id" and cir.documento_id = prog.documento_id  and cir."consecAdmision" = prog."consecAdmision" limit 1) cirugias , estcir.nombre estadoCirugia FROM cirugia_programacioncirugias prog INNER JOIN sitios_sedesclinica sed	on (sed.id = prog."sedesClinica_id") INNER JOIN admisiones_ingresos i ON (i."tipoDoc_id" =prog."tipoDoc_id" AND i.documento_id =  prog.documento_id AND i.consec= prog."consecAdmision" )  INNER JOIN cirugia_cirugias cir ON (cir."tipoDoc_id" =prog."tipoDoc_id" AND cir.documento_id =  prog.documento_id AND cir."consecAdmision" = prog."consecAdmision"  AND cir.id = prog.cirugia_id)  INNER JOIN cirugia_estadoscirugias estcir ON (estcir.id = cir."estadoCirugia_id" AND  estcir.id IN ( ' + "'" + str(estadoCirugiaPendiente.id) + "','" + str(estadoCirugiaConfirmada.id) + "','" + str(estadoCirugiaRealizada.id)  + "','" + str(estadoConDescripcionQx.id) + "'))" + '  INNER JOIN usuarios_usuarios u ON (u.id = i.documento_id ) INNER JOIN usuarios_tiposdocumento tipdoc ON (tipdoc.id =  u."tipoDoc_id") INNER JOIN cirugia_estadosprogramacion estprog ON (estprog.id = prog."estadoProgramacion_id" AND estprog.nombre != '  + "'" + str(estadoProgramacionRealizada.nombre) + "'" + ' ) LEFT JOIN sitios_salas sala ON (sala.id =prog.sala_id )  WHERE sed.id = ' + "'" + str(sede) +  "'"  + ' order by sala.numero'

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


def Load_dataDisponibilidadSalasCirugia(request, data):
    print("Entre Load_dataDisponibilidadSalasCirugia")

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

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT sal.id id, sal.numero numero, sal.nombre nombre, tipsal.nombre tipoSala, est.nombre estado, dispo.fecha, dispo."desdeHora", dispo."hastaHora" FROM sitios_salas sal, cirugia_estadossalas est, sitios_tiposSalas tipSal, sitios_disponibilidadsalas dispo WHERE sal."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND sal."tipoSala_id" = tipsal.id AND sal."estadoSala_id" = est.id AND sal.id=dispo.salas_id ORDER BY sal.numero, tipsal.nombre'

    print(detalle)

    curx.execute(detalle)

    for id, numero, nombre, tipoSala, estado, fecha, desdeHora, hastaHora  in curx.fetchall():
        salasCirugia.append(
            {"model": "sitios.salas", "pk": id, "fields":
                {'id': id, 'numero': numero, 'nombre': nombre, 'tipoSala': tipoSala,
                 'estado': estado,'fecha':fecha, 'desdeHora':desdeHora, 'hastaHora':hastaHora }})

    miConexionx.close()
    print(salasCirugia)

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

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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
    registroCirugia = Cirugias.objects.get(id=registroProgramacion.cirugia_id,   tipoDoc_id=registroProgramacion.tipoDoc_id, documento_id=registroProgramacion.documento_id, consecAdmision = registroProgramacion.consecAdmision)


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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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
    print("fecha_actual", fecha_actual)
    fecha_actual = fecha_actual + timedelta(days =-1)
    print("fecha_actual", fecha_actual)
    fecha_hoyM = fecha_actual.strftime("%Y-%m-%d")
    print("fecha_hoyM a WORK:", fecha_hoy)
    dias_a_revisar = 5


    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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
    print("Convenio = ", cirugiaId2.convenio_id)

    finalidad = request.POST.get('finalidad')
    print("finalidad =", finalidad)

    cups = request.POST["cupsProc"]
    print ("cups =", cups)

    sede = request.POST["sedesClinicaModalProcedimientos_id"]
    print ("sede =", sede)

    username_id = request.POST['usernameProcedimientosCirugia_id']
    print ("username_id =", username_id)


    estadoReg = 'A'

    fechaRegistro = timezone.now()

    estadoAutorizacionId = EstadosAutorizacion.objects.get(nombre='PENDIENTE')
    print ("paso_00")	
    ingresoId = Ingresos.objects.get(tipoDoc_id = cirugiaId2.tipoDoc_id, documento_id = cirugiaId2.documento_id , consec = cirugiaId2.consecAdmision )
    
    print ("paso_01")	
    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        print ("paso_02")	
        comando = 'INSERT INTO cirugia_cirugiasprocedimientos (finalidad_id, "fechaRegistro", "estadoReg", cirugia_id, cups_id, "usuarioRegistro_id") VALUES (' + "'" + str(finalidad) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(cups) + "','" + str(username_id) + "')"

        print(comando)
        cur3.execute(comando)

        # Aui la rutina para mirar si va o no a autorizaciones

        requiereAutorizacion = Examenes.objects.get(id=cups)

        if (requiereAutorizacion.requiereAutorizacion == 'S'):

            # crea cabezote de autorizaciones
            print("Entre requiere autorizacion") 

            comando = 'INSERT INTO autorizaciones_autorizaciones ("fechaSolicitud","estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id , convenio_id , ingreso_id,observaciones)  VALUES ( now(), ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "','" +  str(ingresoId.empresa_id) + "','" + str(username_id) + "','" + str(sede) + "','" + str(username_id) + "',null," + "'" + str(cirugiaId2.convenio_id) + "','"  + str(ingresoId.id) + "','" + str('AUTORIZACION DE CIRUGIA') +  "') RETURNING id;"
            print(comando)
            cur3.execute(comando)
            autorizacionId = cur3.fetchone()[0]

            # crea detalle de autorizacionesdetalle

            tiposExamenId = TiposExamen.objects.get(nombre='PROCEDIMIENTOS QX')


            comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id", "valorSolicitado", mipres, cirugia_id)  VALUES (' + "'" + str(estadoAutorizacionId.id) + "'," + "'" + str('1') + "'" + ' ,0, now(),' + "'" + str('A') + "','" + str(autorizacionId) + "','" + str(username_id) + "'," + "'" + str(cups) + "',null, " + "'" + str(tiposExamenId.id) + "'" + ",0 , null,'" + str(cirugiaId) + "');"
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
    cirugiaId2 = Cirugias.objects.get(id=cirugiaId)
    finalidad = request.POST.get('finalidadInforme')
    print("finalidad =", finalidad)
    print("convenio = " , cirugiaId2.convenio_id)
    sede = request.POST.get('sedesClinicaModalInformeProcedimientos_id')
    print ("sede =", sede)

    cups = request.POST["cupsInforme"]
    print ("cups =", cups)

    username_id = request.POST['usernameProcedimientosInformeCirugia_id']
    print ("username_id =", username_id)

    if 'cruento' in request.POST:
        cruento = 'S'
    else:
        cruento = 'N'

    if 'incruento' in request.POST:
        incruento = 'S'
    else:
        incruento = 'N'

    #cruento = request.POST['cruento']
    print ("cruento =", cruento)

    #incruento = request.POST['incruento']
    print ("incruento =", incruento)

    regionesOperatorias = request.POST['regionesOperatorias']
    print ("regionesOperatorias =", regionesOperatorias)

    viasDeAcceso = request.POST['viasDeAcceso']


    if (viasDeAcceso==""):
        viasDeAcceso='null'
    print ("viasDeAcceso =", viasDeAcceso)

    estadoReg = 'A'
    fechaRegistro = timezone.now()


    estadoAutorizacionId = EstadosAutorizacion.objects.get(nombre='PENDIENTE')
    print ("paso_00")	
    ingresoId = Ingresos.objects.get(tipoDoc_id = cirugiaId2.tipoDoc_id, documento_id = cirugiaId2.documento_id , consec = cirugiaId2.consecAdmision )
    
    print ("empresa_id ", ingresoId.empresa_id)	


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO cirugia_cirugiasprocedimientos (finalidad_id, "fechaRegistro", "estadoReg", cirugia_id, cups_id, "usuarioRegistro_id", cruento, incruento , "regionOperatoria_id", "viasDeAcceso_id") VALUES (' + "'" + str(finalidad) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(cirugiaId) + "','"  + str(cups) + "','" + str(username_id) + "','" + str(cruento) + "','" + str(incruento) + "','" + str(regionesOperatorias)   + "',"  + str(viasDeAcceso) + ")"

        print(comando)
        cur3.execute(comando)

        # Aui la rutina para mirar si va o no a autorizaciones

        requiereAutorizacion = Examenes.objects.get(id=cups)

        if (requiereAutorizacion.requiereAutorizacion == 'S'):

            # crea cabezote de autorizaciones
            print("Entre requiere autorizacion") 

            comando = 'INSERT INTO autorizaciones_autorizaciones ("fechaSolicitud","estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id , convenio_id , ingreso_id,observaciones)  VALUES ( now(), '  + str(estadoAutorizacionId.id) + ', now(), now(), ' + "'" + str('A') + "'," +  str(ingresoId.empresa_id) + "," + str(username_id) + ",'" + str(sede) + "','" + str(username_id) + "',null," + str(cirugiaId2.convenio_id) + ","  + str(ingresoId.id) + ",'" + str('AUTORIZACION DE CIRUGIA') + "'" +  ') RETURNING id;'
            print(comando)
            cur3.execute(comando)
            autorizacionId = cur3.fetchone()[0]

            # crea detalle de autorizacionesdetalle

            tiposExamenId = TiposExamen.objects.get(nombre='PROCEDIMIENTOS QX')


            comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id", "valorSolicitado", mipres, cirugia_id)  VALUES (' + "'" + str(estadoAutorizacionId.id) + "'," + "'" + str('1') + "'" + ' ,0, now(),' + "'" + str('A') + "','" + str(autorizacionId) + "','" + str(username_id) + "'," + "'" + str(cups) + "',null, " + "'" + str(tiposExamenId.id) + "'" + ",0 , null,'" + str(cirugiaId) + "');"
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    detalle = 'SELECT prog.id id,  u."tipoDoc_id" tipoDoc_id , u.documento documento, i.consec consecutivo, u.nombre paciente,estprog.id estado_id, estprog.nombre estadoProg,sala.id sala_id, sala.nombre sala, prog."fechaProgramacionInicia" inicia, prog."horaProgramacionInicia" horaInicia, prog."fechaProgramacionFin" termina, prog."horaProgramacionFin" horaTermina , prog."serviciosAdministrativos_id" serviciosAdministrativos_id, cir.convenio_id FROM cirugia_programacioncirugias prog INNER JOIN cirugia_cirugias cir ON (cir.id=prog.cirugia_id ) INNER JOIN sitios_sedesclinica sed	on (sed.id = prog."sedesClinica_id") INNER JOIN admisiones_ingresos i ON (i."tipoDoc_id" =prog."tipoDoc_id" AND i.documento_id =  prog.documento_id AND i.consec= prog."consecAdmision" ) INNER JOIN usuarios_usuarios u ON (u.id = i.documento_id ) INNER JOIN cirugia_estadosprogramacion estprog ON (estprog.id = prog."estadoProgramacion_id" ) LEFT JOIN sitios_salas sala ON (sala.id =prog.sala_id )  WHERE sed.id = ' + "'" + str(sede) + "' AND prog.id = " + "'" + str(programacionId) + "'"

    print(detalle)

    cur3.execute(detalle)

    for id, tipoDoc_id, documento, consecutivo, paciente, estado_id, estadoProg, sala_id, sala, inicia, horaInicia, termina, horaTermina , serviciosAdministrativos_id, convenio_id in cur3.fetchall():
        programacionCirugia.append(
            {"model": "cirugia.programcioncirugias", "pk": id, "fields":
                {'id': id, 'tipoDoc_id': tipoDoc_id, 'documento': documento, 'consecutivo': consecutivo,
                 'paciente': paciente, 'estado_id':estado_id, 'estadoProg': estadoProg, 'sala_id': sala_id, 'sala': sala,
                 'inicia': inicia, 'horaInicia': horaInicia,
                 'termina': termina, 'horaTermina': horaTermina,'serviciosAdministrativos_id':serviciosAdministrativos_id,'convenio_id':convenio_id
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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
    cirugiaId2 = request.POST.get('cirugiaId')
    print("cirugiaId2 =", cirugiaId2)

    cirugiaId = Cirugias.objects.get(id=cirugiaId2) 
    print("pase_01")   
    cirugiaRealizada = EstadosCirugias.objects.get(nombre='REALIZADA')
    print("pase_02")
    cirugiaFacturada = EstadosCirugias.objects.get(nombre='FACTURADA')

    print ("cirugiaId.estadoCirugia_id = ",cirugiaId.estadoCirugia_id )

    if (cirugiaId.estadoCirugia_id == cirugiaRealizada or cirugiaId.estadoCirugia_id == cirugiaFacturada):

	    return JsonResponse({'success': False, 'Mensajes': 'Procedimiento no se puede cancelar en cirugias REALIZADA y/o FACTURADAS!'})

    print("pase el if")

    miConexion3 = None
    try:


        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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


        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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


        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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
    tiposFolio = TiposFolio.objects.get(nombre='MEDICO')

    username_id = request.POST.get('usernameModalAdicionarQx_id')
    print("username_id = " , username_id );

    ciruIdd = Cirugias.objects.get(id=cirugiaId)
    print("ciruIdd =", ciruIdd.id)
    estadoConfirmadaId = EstadosCirugias.objects.get(nombre='CONFIRMADA')
    print(" estadoConfirmadaId = ", estadoConfirmadaId)

    ingresoQuirofano = request.POST.get('ingresoQuirofano')
    print("ingresoQuirofano", ingresoQuirofano)
    horaIngresoQuirofano =  ingresoQuirofano[11:19]
    print("horaIngresoQuirofano", horaIngresoQuirofano)
    print ("año = ", int(ingresoQuirofano[0:4]))
    print("mes = ", ingresoQuirofano[6:7])
    print("dia = ", ingresoQuirofano[8:10])


    ingresoQuirofano =  datetime.date(int(ingresoQuirofano[0:4]), int(ingresoQuirofano[6:7]), int(ingresoQuirofano[8:10]))
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
    serviciosAdministrativos = request.POST.get('serviciosAdministrativos')


    if (serviciosAdministrativos==None):
        serviciosAdministrativos='null'
    print(" serviciosAdministrativos =" , serviciosAdministrativos)
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

    sede = request.POST.get('sedesClinicaModalAdicionarQx_id')
    print("sede =", sede)

    estadoCirugiaId = ciruIdd.estadoCirugia_id
    estadoRealizadaId = EstadosCirugias.objects.get(nombre='REALIZADA')
    print(" estadoRealizadaId = ", estadoRealizadaId.id)

    estadoDescripcionQxId = EstadosCirugias.objects.get(nombre='CON DESCRIPCION QX')
    print(" estadoDescripcionQxId = ", estadoDescripcionQxId.id)

    estadoReg = 'A'
    fechaRegistro = timezone.now()


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

            miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()

            detalle = 'UPDATE cirugia_Cirugias SET "ingresoQuirofano" =  ' + "'" + str(ingresoQuirofano) + "'," + '"horaIngresoQuirofano" = ' + "'" + str(horaIngresoQuirofano) + "'," + '  "salidaQuirofano" =  ' + "'" + str(salidaQuirofano) + "'," + '"horaSalidaQuirofano" = ' + "'" + str(horaSalidaQuirofano)  + "'," + '"fechaIniAnestesia" = ' + "'" + str(fechaIniAnestesia) + "'," + '"HoraIniAnestesia" = ' + "'" + str(horaIniAnestesia) + "',"  + '"fechaQxInicial" = ' + "'" + str(fechaQxIni) + "'," + '"horaQxInicial" = ' + "'" + str(horaQxIni) + "'," + '"fechaQxFinal" = ' + "'" + str(fechaQxFin) + "'," + '"horaQxFinal" = ' + "'" + str(horaQxFin) + "'," + '"fechaFinAnestesia" = ' + "'" + str(fechaFinAnestesia) + "'," + '"horaFinAnestesia" = ' + "'" + str(horaFinAnestesia) + "'," + '"ingresoRecuperacion" = ' + "'" + str(ingresoRecuperacion) + "'," + '"horaIngresoRecuperacion" = ' + "'" + str(horaIngresoRecuperacion) + "'," + '"salidaRecuperacion" = ' + "'" + str(salidaRecuperacion) + "'," + '"horaSalidaRecuperacion" = ' + "'" + str(horaSalidaRecuperacion) + "'," + '"dxPreQx_id" = ' + str(dxPreOperatorio) + ","   + '"dxPostQx_id" = ' +  str(dxPostOperatorio) + ","  + '"impresionDx_id" = ' + str(impresionDx) + "," + '"dxComplicacion_id" = ' + str(complicacionesDx) + "," + '"formaRealiza" = ' + "'" + str(formaRealizacion) + "'," + '"patologia" = ' + "'" + str(tejidoPatologia) + "'," + '"tipofractura" = ' + "'" + str(tipoFractura) + "'," + '"intensificador" = ' + "'" + str(intensificador) + "'," + '"descripcionQx" = ' + "'" + str(descripcionQx) + "'," + '"hallazgos" = ' + "'" + str(hallazgos) + "'," + '"analisis" = ' + "'" + str(analisis) + "'," + '"planx" = ' + "'" + str(planx) + "'," + '"estadoCirugia_id" = ' + "'" + str(estadoDescripcionQxId.id) + "'" + ' Where id = ' + "'" + str(cirugiaId) + "'"

            print(detalle)
            cur3.execute(detalle)

            print("estadoConfirmadaId.id = ", estadoConfirmadaId.id)
            print("ciruIdd.estadoCirugia_id = ", ciruIdd.estadoCirugia_id)
            print("ingreso documento_id = ", ingreso.documento_id)
            print("ingreso tipoDoc_id = ", ingreso.tipoDoc_id)
            print("ingreso consec = " , ingreso.consec)

            ##OPS aqi hay problema si se reversan los estados mas de una ez
            # mejor hacer un query u orm que cuente en clinico_historialcruiias <1 para n crear folios nuevo

            folios = HistorialCirugias.objects.filter(cirugia_id=cirugiaId).count()

            print("folios = " , folios)
            if folios > 1:
                # Lanza la excepción 404 al navegador
                abort(404, description="Paciente ya registrado")
    
                #return JsonResponse({'success': False, 'Mensajes': 'No hay cirugias registradas!'})

            print("folios = " , folios)

            if (folios==0 and (float(ciruIdd.estadoCirugia_id)==float(estadoConfirmadaId.id) or float(ciruIdd.estadoCirugia_id)==float(estadoRealizadaId.id) or float(ciruIdd.estadoCirugia_id)==float(estadoDescripcionQxId.id))):  # Hay que crear folio

                print("Pase filtro para cfear historialciruias")

                ## Desde aqui INSERT FOLIO

                # Primero buscamos el numero del folio nuevo

                print ("Entre a crear folio")

                if (esTriage == 'N'):

                    ultimofolio = Historia.objects.all().filter(tipoDoc_id=ingreso.tipoDoc_id).filter(documento_id=ingreso.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))
                    historiaAnterior = Historia.objects.all().get(tipoDoc_id=ingreso.tipoDoc_id,documento_id=ingreso.documento_id, consecAdmision = ingreso.consec, folio=ultimoFolio-1)
                    diagnosticoAnterior=HistorialDiagnosticos.objects.filter(historia_id=historialAnterior.id).aggregate(maximo=Coalesce(Max('diagnostico_id'), 0))
                else:
                    ultimofolio = Historia.objects.all().filter(tipoDoc_id=triageId.tipoDoc_id).filter(documento_id=triageId.documento_id).aggregate(maximo=Coalesce(Max('folio'), 0))
                    historiaAnterior = Historia.objects.all().get(tipoDoc_id=triageId.tipoDoc_id,documento_id=triageId.documento_id, consecAdmision = triageId.consec, folio=ultimoFolio-1)
                    diagnosticoAnterior=HistorialDiagnosticos.objectsfilter(historia_id=historialAnterior.id).aggregate(maximo=Coalesce(Max('diagnostico_id'), 0))

                print("ultimo folio = ", ultimofolio)
                print("ultimo folio = ", ultimofolio['maximo'])
                ultimofolio2 = (ultimofolio['maximo']) + 1
                print("ultimo folio2 = ", ultimofolio2)

                print("diagnosticoAnterior= ", diagnosticoAnterior)
                diagnosticoAnterior2 = (diagnosticoAnterior['maximo']) + 1
                print("diagnosticoAnterior2 = ", diagnosticoAnterior2)


                # Segundo  INSERT en clinico_historial
                print("esTriage =" , esTriage)

                # Busca la causa Externa ultima y El ultimo Dx

                

                if (esTriage == 'N'):
                    print("Entre ingreso=")

                    detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id", causaExterna_id ) VALUES (' + "'" + str(ingreso.consec) + "'," + str(ultimofolio2) + ",'" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(ingreso.documento_id) + "," + str(ingreso.tipoDoc_id) + ",'" + str(username_id) + "'," + str(tiposFolio.id) + ",'" + str(username_id) + "'," + str(sede) + "," +  str(serviciosAdministrativos) + ",'" + str(historiaAnterior.causaExterna_id) + "') RETURNING id;"

                    print(detalle)
                else:

                    print("tRIAGE")
                    detalle = 'INSERT INTO clinico_historia ("consecAdmision", folio, fecha, "fechaRegistro", "estadoReg", documento_id, "tipoDoc_id" , planta_id, "tiposFolio_id" , "usuarioRegistro_id", "sedesClinica_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(triageId.consec) + "'," + str(ultimofolio2) + ",'" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(triageId.documento_id) + "," + str(triageId.tipoDoc_id) + ",'" + str(username_id) + "'," + str(tiposFolio.id) + ",'" + str(username_id) + "','" + str(sede) + "'," + str(serviciosAdministrativos) + ") RETURNING id;"

                print(detalle)
                resultado = cur3.execute(detalle)
                historiaId = cur3.fetchone()[0]
                print("historiaId = ", historiaId)

                detalle = 'INSERT INTO clinico_historialDiagnosticos (historia_id, diagnostico_id, "estadoReg", "fechaRegistro") Values(' + "'" + str(historiaId)  + "','" + str(diagnosticoAnterior2) + "','" + str(estadoReg) + "','" + str(fechaRegistro) + "')"
                print(detalle)
                resultado = cur3.execute(detalle)


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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
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


        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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
    registroCirugia = Cirugias.objects.get(tipoDoc_id=registroProgramacion.tipoDoc_id, documento_id=registroProgramacion.documento_id, consecAdmision = registroProgramacion.consecAdmision, id=registroProgramacion.cirugia_id)

    serialized1 = json.dumps(registroCirugia.id, default=str)
    print("de regreso") 
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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
    if (registroHonorarioCirujano==None or registroHonorarioCirujano=='None'):
       print ("Entre resultado None CIRUJANO")
       return JsonResponse({'success': False, 'Mensajes': 'Tipo Honorario CIRUJANO. Registro No existente !'})

    registroHonorarioAnestesiologo = TiposHonorarios.objects.get(nombre='ANESTESIOLOGO')
    if (registroHonorarioAnestesiologo==None or registroHonorarioAnestesiologo=='None'):
       print ("Entre resultado None Tipo Honorario ANESTESIOLOGO")
       return JsonResponse({'success': False, 'Mensajes': 'Tipo Honorario ANESTESIOLOGO. Registro No existente !'})
 
    registroHonorarioAyudante = TiposHonorarios.objects.get(nombre='AYUDANTE')
    if (registroHonorarioAyudante==None or registroHonorarioAyudante=='None'):
       print ("Entre resultado None Tipo Honorario AYUDANTE")
       return JsonResponse({'success': False, 'Mensajes': 'Tipo Honorario AYUDANTE. Registro No existente !'})
     
    #registroHonorarioPerfisionista = TiposHonorarios.objects.get(nombre='PERFUSIONISTA')
    print ("aqui01")
    registroDerechosSala = TiposHonorarios.objects.get(nombre='DERECHOS DE SALA')
    if (registroDerechosSala==None or registroDerechosSala=='None'):
       print ("Entre resultado None Honorario Derechos de Sala")
       return JsonResponse({'success': False, 'Mensajes': 'Honorario Derechos de Sala . Registro No existente !'})


    viaDeAccesoMismaId = ViasDeAcceso.objects.get(nombre='MISMA VIA') 
    viaDeAccesoDiferenteId = ViasDeAcceso.objects.get(nombre='DIFERENTE VIA') 

    viaDeAccesoMisma = viaDeAccesoMismaId.id
    viaDeAccesoDiferente = viaDeAccesoDiferenteId.id

    registroMateriales = TiposHonorarios.objects.get(nombre='MATERIALES DE SUTURA Y CURACION QX')
    print ("aqui02")
    if (registroMateriales==None or registroMateriales=='None'):
       print ("Entre resultado None Honorario Materiales de sutura y curacion Qx")
       return JsonResponse({'success': False, 'Mensajes': 'Honorario Materiales de sutura y curacion Qx . Registro No existente !'})

    # Busco datos de la cirugia relacionado,
    registroCirugia = Cirugias.objects.get(id=cirugiaId)
    print ("aqui03")
    #AQui valido si es estado de la cirugia es apta para liquidar 

    estadoConfirmada = EstadosCirugias.objects.get(nombre='CONFIRMADA')
    if (estadoConfirmada==None or estadoConfirmada=='None'):
       print ("Entre resultado None No EXISTE estado Confirmada")
       return JsonResponse({'success': False, 'Mensajes': 'No EXISTE estado Confirmada . Registro No existente !'})

    estadoRealizada = EstadosCirugias.objects.get(nombre='REALIZADA')
    if (estadoRealizada==None or estadoRealizada=='None'):
       print ("Entre resultado None No EXISTE estado Realizada")
       return JsonResponse({'success': False, 'Mensajes': 'No EXISTE estado Realizada . Registro No existente !'})

    estadoConDescripcionQx = EstadosCirugias.objects.get(nombre='CON DESCRIPCION QX')
    if (estadoConDescripcionQx==None or estadoConDescripcionQx=='None'):
       print ("Entre resultado None No EXISTE estado Con DescripcionQx")
       return JsonResponse({'success': False, 'Mensajes': 'No EXISTE estadoConDescripcionQx . Registro No existente !'})

    print(" registroCirugia.estadoCirugia_id = ", registroCirugia.estadoCirugia_id);
    print("estadoRealizada.id = ", estadoRealizada.id);

    if (registroCirugia.estadoCirugia_id != estadoRealizada.id and  registroCirugia.estadoCirugia_id != estadoConDescripcionQx.id ):

           return JsonResponse({'success': False, 'Mensajes': 'Cirugia de paciente No esta REALIZADA !'})


    registroConvenio = registroCirugia.convenio_id
    print("registroConvenio = ", registroConvenio)

    # Busco cual es Liquiacion de Honorarios de paciente
    #registroConvenio = registroConvenio.objects.get(tipoDoc_id=registroCirugia.tipoDoc_id, documento_id=registroCirugia.documento_id,consecAdmision=registroCirugia.consecAdmision)

    #Busco la forma de liquidacion

    registroliquidacion = Convenios.objects.get(id=registroConvenio)

    print("registroliquidacion = ", registroliquidacion)
    print("registroliquidacion.tarifariosDescripcionHono_id = ", registroliquidacion.tarifariosDescripcionHono_id)

    # Busco Tipo de liquidacion Honorario. O sea como voy a liquidar el honorario

    registroliquidacionHonorario = TarifariosDescripcionHonorarios.objects.get(id=registroliquidacion.tarifariosDescripcionHono_id)

    if (registroliquidacionHonorario.id == 1):   # ISS 2001

        print("Entre a liquidar ISS")
        # Validacion si existe o No existe CABEZOTE

        miConexion3 = None
        try:
            print("Entre por liquiacion ISS")
            miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()

            comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + "'" + str(
                registroCirugia.tipoDoc_id) + "' AND documento_id = " + "'" + str(
                registroCirugia.documento_id) + "'" + ' AND "consecAdmision" = ' + "'" + str(
                registroCirugia.consecAdmision) + "' AND convenio_id = " + str(registroCirugia.convenio_id)
            print("comando = ", comando)

            cur3.execute(comando)

            cabezoteLiquidacion = []

            for id in cur3.fetchall():
                cabezoteLiquidacion.append({'id': id})

            print("CABEZOTE DE LIQUIDACION = ", cabezoteLiquidacion);

            if (cabezoteLiquidacion == []):

                comando = 'INSERT INTO facturacion_liquidacion ("sedesClinica_id", "tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos") VALUES (' + "'" + str(
                    sede) + "'," + "'" + str(registroCirugia.tipoDoc_id) + "','" + str(
                    registroCirugia.documento_id) + "','" + str(
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

            comando = 'DELETE FROM facturacion_liquidaciondetalle p WHERE liquidacion_id = ' +  str(liquidacionId) + " AND cirugia_id = " + str(cirugiaId) + ";"
            print("comando = ", comando)

            cur3.execute(comando)
            print("Acabo de borrar la liquidacion")

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

            # Consigo informacion para trabajar

            suministroMaterial = TiposSuministro.objects.get(nombre='MATERIAL QX')
            if (suministroMaterial==None or suministroMaterial=='None'):
               print ("Entre resultado None No EXISTE Tipo Suministro MATERIAL QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Suministro MATERIAL QX . Registro No existente !'})

            suministroMaterialQx=suministroMaterial.id
            suministroSutura = TiposSuministro.objects.get(nombre='MATERIAL DE SUTURA Y CURACION QX')
            if (suministroSutura==None or suministroSutura=='None'):
               print ("Entre resultado None No EXISTE Tipo SuministroMATERIAL DE SUTURA Y CURACION QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Suministro MATERIAL DE SUTURA Y CURACION QX . Registro No existente !'})

            suministroSuturaQx=suministroSutura.id

            honorarioMaterial = TiposHonorarios.objects.get(nombre='MATERIAL QX')
            if (honorarioMaterial==None or honorarioMaterial=='None'):
               print ("Entre resultado None No EXISTE Tipo Honorario MATERIAL QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Honorario MATERIAL QX . Registro No existente !'})


            honorarioMaterialQx = honorarioMaterial.id

            honorarioSuministroSutura = TiposHonorarios.objects.get(nombre='MATERIALES DE SUTURA Y CURACION QX')
            if (honorarioSuministroSutura==None or honorarioSuministroSutura=='None'):
               print ("Entre resultado None No EXISTE Tipo Honorario MATERIALES DE SUTURA Y CURACION QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Honorario MATERIALES DE SUTURA Y CURACION QX . Registro No existente !'})

 
            honorarioSuministroSuturaQx = honorarioSuministroSutura.id
            conceptoMaterialQxMaterialEspec = Conceptos.objects.get(nombre='MATERIAL QX Y/O MATERIAL ESPEC')

            if (conceptoMaterialQxMaterialEspec==None or conceptoMaterialQxMaterialEspec=='None'):
               print ("Entre resultado None No EXISTE Tipo Concepto MATERIAL QX Y/O MATERIAL ESPEC")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Concepto MATERIAL QX Y/O MATERIAL ESPEC . Registro No existente !'})


            # Consigue procedimientos a facturar

            print("Entre por liquiacion ISS")

            detalle = 'SELECT cirProc.cups_id cups, mipres, "autorizacionDetalle_id" , exa."cantidadUvr", cirProc."viasDeAcceso_id" viasDeAcceso  FROM cirugia_cirugiasprocedimientos cirProc LEFT JOIN clinico_examenes exa on (exa.id = cirProc.cups_id) WHERE cirugia_id = ' + "'" + str(cirugiaId) + "' ORDER BY " + ' exa."cantidadUvr", "codigoCups"'

            print(detalle)

            cupsLiquidacion = []

            cur3.execute(detalle)

            for cups, mipres, autorizacionDetalle_id, cantidaUvr, viasDeAcceso in cur3.fetchall():
                cupsLiquidacion.append({'cups':cups,'mipres':mipres, 'autorizacionDetalle_id':autorizacionDetalle_id,'cantidaUvr':cantidaUvr,'viasDeAcceso':viasDeAcceso})

            print("cups =" , cupsLiquidacion)

            print("Voy a liquidar los materiales quirurgicos sutura y curacion segun procedimiento del ISS en tabla del ISS")

            pasada=0
            ## DESDE AQUI CADA PROCEDIMIENTO

            print("paso_Procedimientos")
            procedimientoAnterior=""
            cantidadUvr2Anterior=""
            viasDeAccesoAnterior=""
            materialesAnterior=""
 
            for procedimiento1 in cupsLiquidacion:

                pasada = pasada +1

                procedimiento = str(procedimiento1['cups'])
                procedimiento = procedimiento.replace("(", ' ')
                procedimiento = procedimiento.replace(")", ' ')
                procedimiento = procedimiento.replace(",", ' ')
                print("procedimiento por el FORSEGUNDO = " ,procedimiento)
                procedimiento =procedimiento.strip()
                #procedimientoAnterior = procedimiento

                mipres = str(procedimiento1['mipres'])
                mipres = mipres.replace("(", ' ')
                mipres = mipres.replace(")", ' ')
                mipres = mipres.replace(",", ' ')
                print("mipres por el FORSEGUNDO = " ,mipres)
                mipres =mipres.strip()

                procedimientoId=Examenes.objects.get(id=procedimiento)
                print("concepto_id =", procedimientoId.concepto_id)


                autorizacionDetalle_id = str(procedimiento1['autorizacionDetalle_id'])
                autorizacionDetalle_id = autorizacionDetalle_id.replace(")", ' ')
                autorizacionDetalle_id = autorizacionDetalle_id.replace(",", ' ')
                print("autorizacionDetalle_id por el FORSEGUNDO = " ,autorizacionDetalle_id)
                autorizacionDetalle_id =autorizacionDetalle_id.strip()


                cantidaUvr2 = str(procedimiento1['cantidaUvr'])
                cantidaUvr2 = cantidaUvr2.replace(")", ' ')
                cantidaUvr2 = cantidaUvr2.replace(",", ' ')
                #cantidadUvr2Anterior= cantidadUvr2
                #cantidaUvr2 = cantidaUvr2.strip()
                print("cantidaUvr2 = ", cantidaUvr2)


                viasDeAcceso = str(procedimiento1['viasDeAcceso'])
                viasDeAcceso = viasDeAcceso.replace("(", ' ')
                viasDeAcceso = viasDeAcceso.replace(")", ' ')
                viasDeAcceso = viasDeAcceso.replace(",", ' ')
                print("viasDeAcceso por el FORSEGUNDO = " ,viasDeAcceso)
                viasDeAcceso =viasDeAcceso.strip()
                #viasDeAccesoAnterior = viasDeAcceso

                if (viasDeAcceso==None or viasDeAcceso=='None'):
                   viasDeAcceso=0.0


                if (autorizacionDetalle_id=='None'):

                    autorizacionDetalle_id='null'

                limite = 170
                print("que paso")
  
                if (float(cantidaUvr2) > float(limite)):
                    print("Entre uvr > 170")

                    # AQUI RUTINA SUBE HONORARIOS SUTURA Y CURACION DE CIRUGIA POR PROCEDIMIENTO
                    # de procedimientos > 170 uvr es decir de acuerdo a cinsumo Hoja de gasto

                    # Esta es la parte Procedimientos >= 170 UVR sí son facturables y se podrán cobrar de acuerdo al consumo demostrado en la hoja de gasto quirúrgico. Excepto el oxígeno, agentes y gases anestésicos.

                    detalle = 'select matqx.suministro_id suministro, sum.nombre nomSuministro , tipos.nombre tipo ,	matqx."valorLiquidacion" valorLiquidacionMat , tiposHonor.id honorario from cirugia_cirugiasmaterialqx matqx, facturacion_suministros sum, facturacion_tipossuministro tipos ,tarifarios_tiposhonorarios tiposHonor	where matqx.cirugia_id= ' + "'" + str(
                        cirugiaId) + "'" + ' and matqx.suministro_id = sum.id and sum."tipoSuministro_id" = tipos.id  AND tipos."tiposHonorarios_id" in ( ' + "'" + str(
                        honorarioMaterialQx) + "','" + str(
                        honorarioSuministroSuturaQx) + "')" + '  AND  matqx."hojaDeGasto" = ' + "'" + str(
                        'N') + "'" + ' and tiposHonor.id = tipos."tiposHonorarios_id" '

                    materialesQx = []

                    print(detalle)
                    cur3.execute(detalle)
                    cur3.fetchone() # Supongamos que devuelve None


                    for suministro, nomSuministro, tipo, valorLiquidacionMat, honorario in cur3.fetchall():
                        materialesQx.append({'suministro': suministro, 'nomSuministro': nomSuministro, 'tipo': tipo,
                                             'valorLiquidacionMat': valorLiquidacionMat, 'honorario': honorario})

                    print("materialesQx = ", materialesQx)

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

                        materialesAnterior = valorLiquidacionMat

                        if (viasDeAcceso == viaDeAccesoMismaId.id or  viasDeAcceso == viaDeAccesoDiferenteId.id): 
                            valorLiquidacionMat = valorLiquidacionMat * 50/100
                            print ("Entre vias de Acceso al 50% de valorLiquidacionMat")

                        honorario = str(matQx['honorario'])
                        honorario = honorario.replace("(", ' ')
                        honorario = honorario.replace(")", ' ')
                        honorario = honorario.replace(",", ' ')

                        suministroId = Suministros.objects.get(id=suministro)
                        # conceptoId=suministroId.concepto_id
                        print("conceptoId= ", suministroId.concepto_id)

                        consecLiquidacion = int(consecLiquidacion) + 1


                        comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "cums_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado, concepto_id) VALUES (' + "'" + str(
                            consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(
                            valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(
                            fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(suministro) + "','" + str(
                            username_id) + "'," + liquidacionId + ",'MANUAL','" + str(honorario) + "','" + str(
                            cirugiaId) + "','N','" + str(suministroId.concepto_id) + "')"
                        print("comando ", comando)
                        cur3.execute(comando)

                        # En teoria hasta aqui Materiales de sutura  ISS de acuerdo al procedimiento
                        #

                    # FIN  Esta es la parte Procedimientos >= 170 UVR sí son facturables y se podrán cobrar de acuerdo al consumo demostrado en la hoja de gasto quirúrgico. Excepto el oxígeno, agentes y gases anestésicos.

                else:

                    # AQUI RUTINA SUBE HONORARIOS SUTURA Y CURACION DE CIRUGIA POR PROCEDIMIENTO
                    # de procedimientos < 170 uvr es decir van por tabla del ISS
                    print("Entre uvr <= 170")
                    detalle = 'select matIss.homologado homologado1 , matIss.valor valorLiquidacionMat1 FROM clinico_examenes exa INNER JOIN tarifarios_tablamaterialsuturacuracioniss matIss on (matIss."desdeUvr" <= exa."cantidadUvr" AND matIss."hastaUvr" >= exa."cantidadUvr") INNER JOIN sitios_tipossalas tipsal ON (tipsal.id =matIss."tiposSala_id") INNER JOIN cirugia_cirugias cir on (cir.id = ' + "'" + str(cirugiaId) + "')" + ' INNER JOIN sitios_salas sal ON (sal.id=cir.sala_id and sal."tipoSala_id" = tipsal.id)  WHERE exa.id = ' + str(procedimiento) + " and " + ' matIss."tipoHonorario_id" = ' + str(honorarioSuministroSutura.id)

                    materialesQx = []

                    print(detalle)
                    cur3.execute(detalle)
                    #resultado = cur3.fetchone() # Supongamos que devuelve None

                    for homologado1,valorLiquidacionMat1 in cur3.fetchall():
                        materialesQx.append({'homologado1':homologado1, 'valorLiquidacionMat1': valorLiquidacionMat1})

                        print("materialesQx = ", materialesQx)

                        if (materialesQx == []):
                          #raise Exception("El registro no existe en la base de datos")
                          print ("Entre resultado=None")
                          return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Iss tarifarios_tablamaterialsuturacuracioniss. Registro No existente !'})

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

                        materialesAnterior = valorLiquidacionMat

                        if (viasDeAcceso == viaDeAccesoMismaId.id or  viasDeAcceso == viaDeAccesoDiferenteId.id): 

                            valorLiquidacionMat = valorLiquidacionMat * 50/100
                            print("Entre valorLiquidacionMat al 50% = ", valorLiquidacionMat)


                        comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,examen_id,"codigoHomologado", concepto_id) VALUES (' + "'" + str(
                            consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(
                            valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(
                            fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA','"+  str(honorarioSuministroSuturaQx) + "','"  + str(cirugiaId) + "','N'," + "'" + str(procedimiento)  + "','" + str(homologado)  + "','" + str(conceptoMaterialQxMaterialEspec.id) + "')"
                        print("comando ", comando)
                        cur3.execute(comando)

                # En teoria hasta aqui Materiales de sutura  ISS de acuerdo al procedimiento
                # fin rutina sube HONORARIO MATERIAL QX

                # consigue La cantidad de uvr del procedimiento. BUENO NO IMPORTA ESTA REPETIDO PARA NO CAMBIAR
                # TODO EL CODIHO HASTA ABAJO

                detalle = 'SELECT "cantidadUvr" cantidadUvr FROM clinico_examenes WHERE id = ' + "'" + str(procedimiento) + "'"

                cantidadUvrProced = []

                cur3.execute(detalle)

                #resultado = cur3.fetchone() # Supongamos que devuelve None

                for cantidadUvr in cur3.fetchall():

                    cantidadUvrProced.append({'cantidadUvr': cantidadUvr })

                for cantidadUvrProced in cantidadUvrProced[0]['cantidadUvr']:

                    cantidadUvrProced = cantidadUvrProced

                print("cantidadUvrProced =" , cantidadUvrProced)

                if (cantidadUvrProced == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Procedimiento cantidad Uvr. Registro No existente !'})


                # consigo valor De 1 Uver a pagar al cirujano

                detalle = 'SELECT homologado, "valorUvr" valorUvrCirujano FROM tarifarios_tablahonorariosiss WHERE id = ' + "'" + str(registroHonorarioCirujano.id) + "'"

                valorUvrCirujanoProced = []

                cur3.execute(detalle)

                #resultado = cur3.fetchone() # Supongamos que devuelve None


                for homologado, valorUvrCirujano in cur3.fetchall():
                    valorUvrCirujanoProced.append({'homologado':homologado,'valorUvrCirujano': valorUvrCirujano })

                    print("valorUvrCirujanoProced =" , valorUvrCirujanoProced[0]['valorUvrCirujano'])
                    valorUvrCirujanoProced = valorUvrCirujanoProced[0]['valorUvrCirujano']
                #for valorUvrCirujanoProced in valorUvrCirujanoProced[0]['valorUvrCirujano']:
                    print("valorUvrCirujanoProced1" , valorUvrCirujanoProced)

                    if (valorUvrCirujanoProced == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Iss tablahonorariosiss Cirujano. Registro No existente !'})

                    print ("procedimiento = ",procedimiento )
                    print ("viasDeAcceso = ",viasDeAcceso )
                    print ("viaDeAccesoMismaId.id = ",viaDeAccesoMismaId.id )
                    print ("viaDeAccesoDiferenteId.id = ",viaDeAccesoDiferenteId.id )

                    if (float(viasDeAcceso) == float(viaDeAccesoMismaId.id) or  float(viasDeAcceso) == float(viaDeAccesoDiferenteId.id)): 

                        liquidaCirujano= float(valorUvrCirujanoProced) * float(cantidadUvrProced) * 75/100
                        print ("liquidaCirujano AL 75% =",liquidaCirujano )
                        homologadoCirujano = homologado			

                    else:
                        liquidaCirujano= float(valorUvrCirujanoProced) * float(cantidadUvrProced)
                        print ("liquidaCirujano =",liquidaCirujano )
                        homologadoCirujano = homologado			


                # En teoria hasta aqui tengo el valor del Cirujano ISS de acuerdo al procedimiento

                # Aqui liquidacion de honorarios Anestesiologo

                # consigo valor De 1 Uver a pagar al Anestesiologo

                detalle = 'SELECT homologado, "valorUvr" valorUvrAnestesiologo FROM tarifarios_tablahonorariosiss WHERE id = ' + "'" + str(registroHonorarioAnestesiologo.id) + "'"

                valorUvrAnestesiologoProced = []

                cur3.execute(detalle)

                #resultado = cur3.fetchone() # Supongamos que devuelve None

                for homologado, valorUvrAnestesiologo in cur3.fetchall():
                    valorUvrAnestesiologoProced.append({'homologado':homologado,'valorUvrAnestesiologo': valorUvrAnestesiologo })

                    print("valorUvrAnestesiologoProced =" , valorUvrAnestesiologoProced[0]['valorUvrAnestesiologo'])

                    if (valorUvrAnestesiologoProced == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Iss tablahonorariosiss Anestesiologo. Registro No existente !'})


                    print("valorUvrAnestesiologoProced = " ,valorUvrAnestesiologoProced)
                    valorUvrAnestesiologoProced = valorUvrAnestesiologoProced[0]['valorUvrAnestesiologo']

                    print ("procedimiento = ",procedimiento )
                    print ("viasDeAcceso = ",viasDeAcceso )
                    print ("viaDeAccesoMismaId.id = ",viaDeAccesoMismaId.id )
                    print ("viaDeAccesoDiferenteId.id = ",viaDeAccesoDiferenteId.id )


                    if (float(viasDeAcceso) == float(viaDeAccesoMismaId.id) or  float(viasDeAcceso) == float(viaDeAccesoDiferenteId.id)): 

                        liquidaAnestesiologo= float(valorUvrAnestesiologoProced) * float(cantidadUvrProced) * 75/100

                        print ("liquidaAnestesiologo AL 75% =",liquidaAnestesiologo )
                        homologadoAnestesiologo = homologado			

                    else:

                       liquidaAnestesiologo= float(valorUvrAnestesiologoProced) * float(cantidadUvrProced)
                       print("liquidaAnestesiologo =", liquidaAnestesiologo)
                       homologadoAnestesiologo = homologado			

                # En teoria hasta aqui honorariosAnestesiologo ISS de acuerdo al procedimiento

                # Aqui liquidacion de honorarios Ayudante

                # consigo valor De 1 Uver a pagar al Ayudante

                detalle = 'SELECT homologado,"valorUvr" valorUvrAyudante FROM tarifarios_tablahonorariosiss WHERE id = ' + "'" + str(registroHonorarioAyudante.id) + "'"

                valorUvrAyudanteProced = []

                cur3.execute(detalle)

                #resultado = cur3.fetchone() # Supongamos que devuelve None


                for homologado,valorUvrAyudante in cur3.fetchall():
                    valorUvrAyudanteProced.append(
                        {'homologado':homologado, 'valorUvrAyudante': valorUvrAyudante })

                    print("valorUvrAyudanteProced =" , valorUvrAyudanteProced[0]['valorUvrAyudante'])

                #for valorUvrAyudanteProced in valorUvrAyudanteProced[0]['valorUvrAyudante']:
                    print(valorUvrAyudanteProced)
                    valorUvrAyudanteProced = valorUvrAyudanteProced[0]['valorUvrAyudante']

                    if (valorUvrAyudanteProced == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Iss tablahonorariosiss Ayudante. Registro No existente !'})

                    print ("procedimiento = ",procedimiento )
                    print ("viasDeAcceso = ",viasDeAcceso )
                    print ("viaDeAccesoMismaId.id = ",viaDeAccesoMismaId.id )
                    print ("viaDeAccesoDiferenteId.id = ",viaDeAccesoDiferenteId.id )



                    if (float(viasDeAcceso) == float(viaDeAccesoMismaId.id) or  float(viasDeAcceso) == float(viaDeAccesoDiferenteId.id)): 

                        liquidaAyudante= float(valorUvrAyudanteProced) * float(cantidadUvrProced) * 75/100

                        print ("liquidaAyudante AL 75% =",liquidaAyudante )
                        homologadoAyudante = homologado			

                    else:

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
                print("paso_1 Cirujano  con concepto_id: ", procedimientoId.concepto_id)
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal","estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id , anulado, "codigoHomologado", mipres, "autorizacionDetalle_id", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaCirujano) + "','" + str(liquidaCirujano) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioCirujano.id)  + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoCirujano)  + "','" + str(mipres) + "'," + str(autorizacionDetalle_id) + ",'" + str(procedimientoId.concepto_id) + "')"
                print("comando ", comando)
                cur3.execute(comando)
                # Anestesiologo
                print("paso_2 Anestesiologo")
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro","fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado, "codigoHomologado", mipres, "autorizacionDetalle_id", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAnestesiologo) + "','" + str(liquidaAnestesiologo) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAnestesiologo.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAnestesiologo) + "','" + str(mipres) + "'," + str(autorizacionDetalle_id) + ",'" + str(procedimientoId.concepto_id) + "')"
                print("comando ", comando)
                cur3.execute(comando)
			
                # Ayudante
                consecLiquidacion= int(consecLiquidacion) + 1
                print("paso_2 Ayudante")
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",  "estadoRegistro", "fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado, "codigoHomologado", mipres, "autorizacionDetalle_id", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAyudante) + "','" + str(liquidaAyudante) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) +  "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAyudante.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAyudante) + "','" + str(mipres) + "'," + str(autorizacionDetalle_id) + ",'" + str(procedimientoId.concepto_id) + "')"
                print("comando ", comando)
                cur3.execute(comando)
                print("paso_1 Ayudante")
                print("ANTES DE pasada = ", pasada)

                # LIQUIDACION SALAS DE CIRUGIA

                print ("Entre pasada = ", pasada)

                ## Luego ir a tabla tarifarios_tablaSalasdecirugiaiss para sacar el valor
                #
                detalle = 'SELECT tarifa.homologado homologado,tarifa.valor valor FROM cirugia_cirugias cir, sitios_tipossalas tipsal, tarifarios_tablaSalasdecirugiaiss tarifa, sitios_salas sala WHERE cir.id = ' + "'" + str(cirugiaId) + "'" + ' AND cir.sala_id = sala.id and sala."tipoSala_id" = tipsal.id and tarifa."tiposSala_id" = tipsal.id and ' + "'" + str(cantidadUvrProced) + "'" + ' between tarifa."desdeUvr" AND tarifa."hastaUvr"'
                valorSala = []
                print(detalle)
                cur3.execute(detalle)

                resultado = cur3.fetchone() # Supongamos que devuelve None



                for homologado, valor in cur3.fetchall():
                    valorSala.append({'homologado':homologado, 'valor': valor})

                    #valorSala = valorSala[0]

                    liquidaValorSala = valor
                    liquidaValorHomologado = homologado
                    print("liquidaValorSala = ", liquidaValorSala)
                    print("liquidaValorHomologado = ", liquidaValorHomologado)

                    if (valorSala == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Iss Salas de Cirugia. Registro No existente !'})


                    if (viasDeAcceso == viaDeAccesoMismaId.id or  viasDeAcceso == viaDeAccesoDiferenteId.id): 

                         liquidaValorSala=liquidaValorSala * 50/100
                         print ("liquidaValorSalaAL 50% =",liquidaValorSala )

                # Salas
                #
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,"codigoHomologado", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaValorSala) + "','" + str(liquidaValorSala) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro)  + "','" + str(procedimiento)  + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroDerechosSala.id)+ "'," +  "'" + str(cirugiaId) + "','N','" + str(liquidaValorHomologado) +  "','" + str(procedimientoId.concepto_id) + "')"
                print("comando", comando)
                cur3.execute(comando)

                # En teoria aqui cambia al procedimiento que sigue

                print("ya paso el procedimiento = ", procedimiento)

                procedimientoAnterior = procedimiento
                #cantidadUvr2Anterior= cantidadUvr2
                print("cantidadUvr2Anterior = ", cantidadUvr2Anterior)
                viasDeAccesoAnterior = viasDeAcceso
                print("con via de acceso = ", viasDeAccesoAnterior)

                # En teoria hasta aqui Salas de CIRUGIA  ISS de acuerdo al procedimiento

            # Fin INSERT liquidaciones

            print("voy a guardar")
	
            miConexion3.commit()
            cur3.close()
            miConexion3.close()

            #return JsonResponse({'success': True, 'Mensajes': 'Liquidacion Honorarios Iss cargada a cuenta Paciente Verificar valores !'})

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
            miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()


            # Consigue procedimientos a facturar


            #detalle = 'SELECT cups_id cups FROM cirugia_cirugiasprocedimientos WHERE cirugia_id = ' + "'" + str(cirugiaId) + "'"
            detalle = 'SELECT cirProc.cups_id cups, mipres, "autorizacionDetalle_id" , exa."grupoQx_id"  FROM cirugia_cirugiasprocedimientos cirProc LEFT JOIN clinico_examenes exa on (exa.id = cirProc.cups_id) WHERE cirugia_id = ' + "'" + str(cirugiaId) + "'"

            print(detalle)

            cupsLiquidacion = []

            cur3.execute(detalle)

            for cups, mipres, autorizacionDetalle_id, grupoQx_id in cur3.fetchall():
                cupsLiquidacion.append({'cups':cups,'mipres':mipres, 'autorizacionDetalle_id':autorizacionDetalle_id,'grupoQx_id':grupoQx_id})

            print("cups =" , cupsLiquidacion)

            # Validacion si existe o No existe CABEZOTE

            comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + "'" + str(registroCirugia.tipoDoc_id) + "' AND documento_id = " + "'" + str(registroCirugia.documento_id) + "'" + ' AND "consecAdmision" = ' + "'" + str(registroCirugia.consecAdmision) + "' AND convenio_id = " + str(registroCirugia.convenio_id)
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

            print("consecLiquidacionIni = ", consecLiquidacion[0])

            consecLiquidacion = consecLiquidacion[0]['cons']
            consecLiquidacion = str(consecLiquidacion)
            print("consecLiquidacionAnt = ", consecLiquidacion)

            consecLiquidacion = consecLiquidacion.replace("(", ' ')
            consecLiquidacion = consecLiquidacion.replace(")", ' ')
            consecLiquidacion = consecLiquidacion.replace(",", ' ')

            if consecLiquidacion.strip() == 'None':
                print("consecLiquidacionFinal = ", consecLiquidacion)
                consecLiquidacion = 0

	    # Busco Tipos de honorarios,
            #registroHonorarioCirujano = TiposHonorarios.objects.get(nombre='CIRUJANO')
            #print("Pase_001")
            #registroHonorarioAnestesiologo = TiposHonorarios.objects.get(nombre='ANESTESIOLOGO')
            #print("Pase_002")
            #registroHonorarioAyudante = TiposHonorarios.objects.get(nombre='AYUDANTE')
            #print("Pase_003")
            #registroDerechosSala = TiposHonorarios.objects.get(nombre='DERECHOS DE SALA')
            #print("Pase_004")
            #registroMateriales = TiposHonorarios.objects.get(nombre='MATERIALES DE SUTURA Y CURACION QX')

            # Consigo informacion para trabajar

            suministroMaterial = TiposSuministro.objects.get(nombre='MATERIAL QX')
            if (suministroMaterial==None or suministroMaterial=='None'):
               print ("Entre resultado None No EXISTE Tipo Suministro MATERIAL QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Suministro MATERIAL QX . Registro No existente !'})

            suministroMaterialQx=suministroMaterial.id
            suministroSutura = TiposSuministro.objects.get(nombre='MATERIAL DE SUTURA Y CURACION QX')
            if (suministroSutura==None or suministroSutura=='None'):
               print ("Entre resultado None No EXISTE Tipo SuministroMATERIAL DE SUTURA Y CURACION QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Suministro MATERIAL DE SUTURA Y CURACION QX . Registro No existente !'})

            suministroSuturaQx=suministroSutura.id

            honorarioMaterial = TiposHonorarios.objects.get(nombre='MATERIAL QX')
            if (honorarioMaterial==None or honorarioMaterial=='None'):
               print ("Entre resultado None No EXISTE Tipo Honorario MATERIAL QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Honorario MATERIAL QX . Registro No existente !'})


            honorarioMaterialQx = honorarioMaterial.id

            honorarioSuministroSutura = TiposHonorarios.objects.get(nombre='MATERIALES DE SUTURA Y CURACION QX')
            if (honorarioSuministroSutura==None or honorarioSuministroSutura=='None'):
               print ("Entre resultado None No EXISTE Tipo Honorario MATERIALES DE SUTURA Y CURACION QX")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Tipo Honorario MATERIALES DE SUTURA Y CURACION QX . Registro No existente !'})

 
            honorarioSuministroSuturaQx = honorarioSuministroSutura.id
            conceptoMaterialQxMaterialEspec = Conceptos.objects.get(nombre='MATERIAL QX Y/O MATERIAL ESPEC')

            if (conceptoMaterialQxMaterialEspec==None or conceptoMaterialQxMaterialEspec=='None'):
               print ("Entre resultado None No EXISTE Tipo Concepto MATERIAL QX Y/O MATERIAL ESPEC")
               return JsonResponse({'success': False, 'Mensajes': 'No EXISTE Concepto MATERIAL QX Y/O MATERIAL ESPEC . Registro No existente !'})


            # Consigue procedimientos a facturar

            pasada=0

            print("A cargar proedimientos")

            for procedimiento1 in cupsLiquidacion:

                pasada = pasada +1

                procedimiento = str(procedimiento1['cups'])
                procedimiento = procedimiento.replace("(", ' ')
                procedimiento = procedimiento.replace(")", ' ')
                procedimiento = procedimiento.replace(",", ' ')
                print("procedimiento por el FORSEGUNDO = " ,procedimiento)
                procedimiento =procedimiento.strip()

                mipres = str(procedimiento1['mipres'])
                mipres = mipres.replace("(", ' ')
                mipres = mipres.replace(")", ' ')
                mipres = mipres.replace(",", ' ')
                print("mipres por el FORSEGUNDO = " ,mipres)
                mipres =mipres.strip()

                procedimientoId=Examenes.objects.get(id=procedimiento)
                print("concepto_id =", procedimientoId.concepto_id)

                autorizacionDetalle_id = str(procedimiento1['autorizacionDetalle_id'])
                autorizacionDetalle_id = autorizacionDetalle_id.replace(")", ' ')
                autorizacionDetalle_id = autorizacionDetalle_id.replace(",", ' ')
                print("autorizacionDetalle_id por el FORSEGUNDO = " ,autorizacionDetalle_id)
                autorizacionDetalle_id =autorizacionDetalle_id.strip()


                grupoQx_id2 = str(procedimiento1['grupoQx_id'])
                grupoQx_id2 = grupoQx_id2.replace(")", ' ')
                grupoQx_id2 = grupoQx_id2.replace(",", ' ')

                print("grupoQx_id2 = ", grupoQx_id2)

                if (autorizacionDetalle_id=='None'):

                    autorizacionDetalle_id='null'

                # DESDE AQUI LIQUIDACION MATERIAL QX SOAT 
 
                limite = 13
                print("que paso")

                if (grupoQx_id2==None or grupoQx_id2=='None'):

                   print ("EntreGrupo Qx Nulo")
                   return JsonResponse({'success': False, 'Mensajes': 'Grupo quirurgico NULO !'})

  
                if (float(grupoQx_id2) > float(limite)):
                    print("Entre grupoQx_id2 > 23")

                    # AQUI RUTINA SUBE HONORARIOS SUTURA Y CURACION DE CIRUGIA POR PROCEDIMIENTO
                    # de procedimientos > 13 uvr es decir de acuerdo a consumo Hoja de gasto

                    # Esta es la parte grupoQx Procedimientos > 13 UVR sí son facturables y se podrán cobrar de acuerdo al consumo demostrado en la hoja de gasto quirúrgico. Excepto el oxígeno, agentes y gases anestésicos.

                    detalle = 'select matqx.suministro_id suministro, sum.nombre nomSuministro , tipos.nombre tipo ,	matqx."valorLiquidacion" valorLiquidacionMat , tiposHonor.id honorario from cirugia_cirugiasmaterialqx matqx, facturacion_suministros sum, facturacion_tipossuministro tipos ,tarifarios_tiposhonorarios tiposHonor	where matqx.cirugia_id= ' + "'" + str(
                        cirugiaId) + "'" + ' and matqx.suministro_id = sum.id and sum."tipoSuministro_id" = tipos.id  AND tipos."tiposHonorarios_id" in ( ' + "'" + str(
                        honorarioMaterialQx) + "','" + str(
                        honorarioSuministroSuturaQx) + "')" + '  AND  matqx."hojaDeGasto" = ' + "'" + str(
                        'N') + "'" + ' and tiposHonor.id = tipos."tiposHonorarios_id" '

                    materialesQx = []

                    print(detalle)
                    cur3.execute(detalle)


                    for suministro, nomSuministro, tipo, valorLiquidacionMat, honorario in cur3.fetchall():
                        materialesQx.append({'suministro': suministro, 'nomSuministro': nomSuministro, 'tipo': tipo,
                                             'valorLiquidacionMat': valorLiquidacionMat, 'honorario': honorario})

                    if (materialesQx == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Soat Suministro,TipoSuministro,TipoHonorario. Registro No existente !'})

                    print("materialesQx = ", materialesQx)

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

                        honorario = str(matQx['honorario'])
                        honorario = honorario.replace("(", ' ')
                        honorario = honorario.replace(")", ' ')
                        honorario = honorario.replace(",", ' ')

                        suministroId = Suministros.objects.get(id=suministro)
                        # conceptoId=suministroId.concepto_id
                        print("conceptoId= ", suministroId.concepto_id)

                        consecLiquidacion = int(consecLiquidacion) + 1
                        comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "cums_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado, concepto_id) VALUES (' + "'" + str(
                            consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(
                            valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(
                            fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(suministro) + "','" + str(
                            username_id) + "'," + liquidacionId + ",'MANUAL','" + str(honorario) + "','" + str(
                            cirugiaId) + "','N','" + str(suministroId.concepto_id) + "')"
                        print("comando ", comando)
                        cur3.execute(comando)

                        # En teoria hasta aqui Materiales de sutura  ISS de acuerdo al procedimiento
                        #

                    # FIN  Esta es la parte Procedimientos >= 170 UVR sí son facturables y se podrán cobrar de acuerdo al consumo demostrado en la hoja de gasto quirúrgico. Excepto el oxígeno, agentes y gases anestésicos.

                else:

                    # AQUI RUTINA SUBE HONORARIOS SUTURA Y CURACION DE CIRUGIA POR PROCEDIMIENTO
                    # de procedimientos grupo_qx  < 13 es decir van por tabla del SOAT
                    print("Entre grupo_qx  < 13")
                    detalle = 'select matIss.homologado homologado1 , matIss.valor valorLiquidacionMat1 FROM clinico_examenes exa INNER JOIN tarifarios_tablamaterialsuturacuracionSoat matSoat on (matSoat."desdeGrupoQx_id" <= exa."grupoQx_idr" AND matSoat."hastaGrupoQx_id" >= exa."grupoQx_id") INNER JOIN sitios_tipossalas tipsal ON (tipsal.id =matSoat."tiposSala_id") INNER JOIN cirugia_cirugias cir on (cir.id = ' + "'" + str(cirugiaId) + "')" + ' INNER JOIN sitios_salas sal ON (sal.id=cir.sala_id and sal."tipoSala_id" = tipsal.id)  WHERE exa.id = ' + str(procedimiento) + " and " + ' matSoat."tipoHonorario_id" = ' + str(honorarioSuministroSutura.id)

                    materialesQx = []

                    print(detalle)
                    cur3.execute(detalle)
  
                    #resultado = cur3.fetchone() # Supongamos que devuelve None

 
                    for homologado1,valorLiquidacionMat1 in cur3.fetchall():
                        materialesQx.append({'homologado1':homologado1, 'valorLiquidacionMat1': valorLiquidacionMat1})

                        print("materialesQx = ", materialesQx)

                        if (materialesQx == []):
                          #raise Exception("El registro no existe en la base de datos")
                          print ("Entre resultado=None")
                          return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Soat tablamaterialsuturacuracionSoat . Registro No existente !'})


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

                        comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,examen_id,"codigoHomologado", concepto_id) VALUES (' + "'" + str(
                            consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(
                            valorLiquidacionMat) + "','" + str(valorLiquidacionMat) + "','" + str('A') + "','" + str(
                            fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA','"+  str(honorarioSuministroSuturaQx) + "','"  + str(cirugiaId) + "','N'," + "'" + str(procedimiento)  + "','" + str(homologado)  + "','" + str(conceptoMaterialQxMaterialEspec.id) + "')"
                        print("comando ", comando)
                        cur3.execute(comando)

                # En teoria hasta aqui Materiales de sutura  ISS de acuerdo al procedimiento
                # fin rutina sube HONORARIO MATERIAL QX

                # consigue La cantidad de uvr del procedimiento. BUENO NO IMPORTA ESTA REPETIDO PARA NO CAMBIAR
                # TODO EL CODIHO HASTA ABAJO

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

                encuentroGupoId = Examenes.objects.get(id=procedimiento)
                grupoQx=encuentroGupoId.grupoQx_id

                if (grupoQx=='None' or grupoQx=='' or grupoQx==None):
                      #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Soat Grupo Qx Procedimiento . Registro No existente !'})
 
                #detalle = 'SELECT "grupoQx_id" grupa FROM clinico_examenes WHERE id = ' + str(procedimiento)
                #print("detalle = ", detalle)

                #datosQx=[]

                #cur3.execute(detalle)

                #resultado = cur3.fetchone() # Supongamos que devuelve None

                #if (resultado=='None' or resultado=='' or resultado==None):
                #      #raise Exception("El registro no existe en la base de datos")
                #       print ("Entre resultado=None")
                #       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Soat Grupo Qx Procedimiento . Registro No existente !'})
 
                print("Ejecute comando")

                #for grupa in cur3.fetchall():
                #    print("en el FOR grupo = ", grupo)
                #    datosQx.append({'grupa':grupa})
                #   print("en el FOR grupo = ", grupo)

                #print("pase datosQx")
                #print("datosQx =" , datosQx)

                #grupoQx = datosQx[0][grupa]

                print("grupoQx =" , grupoQx)

                # consigo la tarifa del honorario SOAT a pagar al cirujano

                detalle = 'SELECT homologado homologado ,  smldv * ' + str(minimo/30)  + ' valor FROM tarifarios_tablahonorariossoat WHERE "grupoQx_id" = ' + str(grupoQx) + ' AND "tiposHonorarios_id" = ' + "'" + str(registroHonorarioCirujano.id)  + "';"

                #detalle = 'SELECT homologado FROM tarifarios_tablahonorariossoat WHERE "grupoQx_id" = ' + "'" + str(grupoQx) + "' " 

                valorCirujanoProced = []

                print("detalle Honorario=", detalle)

                cur3.execute(detalle)


                for homologado, valor in cur3.fetchall():
                    valorCirujanoProced.append({'homologado':homologado, 'valor': valor})
                    print("valorCirujanoProced =" , valorCirujanoProced)
                    liquidaCirujano = float(valor)
                    homologadoCirujano = homologado

                if (valorCirujanoProced == []):
                    # raise Exception("El registro no existe en la base de datos")
                    print("Entre resultado=None")
                    return JsonResponse({'success': False,
                                         'Mensajes': 'Verificar parametrizacion Soat tablahonorariossoat Cirujano . Registro No existente !'})

                if valorCirujanoProced == []:
                    liquidaCirujano = 0

                if homologadoCirujano == None:
                    homologadoCirujano = ''

                # En teoria hasta aqui tengo el valor del Cirujano ISS de acuerdo al procedimiento


                # Aqui liquidacion de honorarios Anestesiologo

                # consigo valor a pagar al Anestesiologo


                detalle = 'SELECT homologado, "smldv" * ' + "'" + str(minimo/30) + "'" + ' valorAnestesiologo FROM tarifarios_tablahonorariossoat WHERE "grupoQx_id" = ' + "'" + str(grupoQx) + "' AND " + '"tiposHonorarios_id" = ' + "'" + str(registroHonorarioAnestesiologo.id)  + "'"

                valorAnestesiologoProced = []
                print("detalle Anestesiologo=", detalle)

                cur3.execute(detalle)

                for homologado, valorAnestesiologo in cur3.fetchall():
                    valorAnestesiologoProced.append({'homologado':homologado, 'valorAnestesiologo': valorAnestesiologo })
                    liquidaAnestesiologo= float(valorAnestesiologo)
                    homologadoAnestesiologo = homologado

                if (valorAnestesiologoProced == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Soat tablahonorariossoat Anestesiologo . Registro No existente !'})

                if valorAnestesiologoProced == []:
                    liquidaAnestesiologo = 0

                if homologadoAnestesiologo == '':
                    homologadoAnestesiologo = ''

                # En teoria hasta aqui honorariosAnestesiologo ISS de acuerdo al procedimiento

                # Aqui liquidacion de honorarios Ayudante

                # consigo valor a pagar al Ayudante

                detalle = 'SELECT homologado, "smldv" * ' + "'" + str(minimo/30) + "'" + ' valorAyudante FROM tarifarios_tablahonorariossoat WHERE "grupoQx_id" = ' + "'" + str(grupoQx) + "' AND " + '"tiposHonorarios_id" = ' + "'" + str(registroHonorarioAyudante.id)  + "'"

                valorAyudanteProced = []
                print("detalle Ayudante", detalle)
                cur3.execute(detalle)

                for homologado, valorAyudante in cur3.fetchall():
                    valorAyudanteProced.append(
                        {'homologado':homologado, 'valorAyudante': valorAyudante })
                    liquidaAyudante= float(valorAyudante)
                    homologadoAyudante= homologado


                if (valorAyudanteProced == []):
                       #raise Exception("El registro no existe en la base de datos")
                       print ("Entre resultado=None")
                       return JsonResponse({'success': False, 'Mensajes': 'Verificar parametrizacion Soat tablahonorariossoat Ayudante . Registro No existente !'})

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
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal","estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id , anulado, "codigoHomologado", mipres, "autorizacionDetalle_id", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaCirujano) + "','" + str(liquidaCirujano) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioCirujano.id)  + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoCirujano) + "','" + str(mipres) + "'," + str(autorizacionDetalle_id) + ",'" + str(procedimientoId.concepto_id) + "')"
                print("comando ", comando)
                cur3.execute(comando)
                # Anestesiologo
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro","fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,  "codigoHomologado" , mipres, "autorizacionDetalle_id", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAnestesiologo) + "','" + str(liquidaAnestesiologo) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) + "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAnestesiologo.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAnestesiologo) + "','" + str(mipres) + "'," + str(autorizacionDetalle_id) + ",'" + str(procedimientoId.concepto_id) + "')"
                print("comando ", comando)
                cur3.execute(comando)

                # Ayudante
                consecLiquidacion= int(consecLiquidacion) + 1

                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",  "estadoRegistro", "fechaCrea", "fechaRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,  "codigoHomologado", mipres, "autorizacionDetalle_id", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaAyudante) + "','" + str(liquidaAyudante) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro) +  "','" + str(procedimiento) + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroHonorarioAyudante.id) + "'," +  "'" + str(cirugiaId) + "','N','" + str(homologadoAyudante) + "','" + str(mipres) + "'," + str(autorizacionDetalle_id) + ",'" + str(procedimientoId.concepto_id) + "')"
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
                print("detalle salas soat", detalle)
                cur3.execute(detalle)

                for homologado, valor in cur3.fetchall():
                    valorSala.append({'homologado':homologado, 'valor': valor})

                    liquidaValorSala = valor
                    liquidaValorHomologado = homologado

                if (valorSala == []):
                  #raise Exception("El registro no existe en la base de datos")
                  print ("Entre resultado=None")
                  return JsonResponse({'success': False, 'Mensajes': 'Verificar tabla Soat Salas de cirugia. Registro No existente !'})

                if valorSala == []:
                    liquidaValorSala = 0

                if liquidaValorHomologado == None:
                    liquidaValorHomologado = ''

                # Salas
                #
                consecLiquidacion= int(consecLiquidacion) + 1
                comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal", "estadoRegistro", "fechaCrea", "fechaRegistro",  "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "tipoHonorario_id", cirugia_id, anulado,  "codigoHomologado", concepto_id) VALUES (' + "'" + str(consecLiquidacion) + "','" + str(fechaRegistro) + "','" + str('1') + "','" + str(liquidaValorSala) + "','" + str(liquidaValorSala) + "','" + str('A') + "','" + str(fechaRegistro) + "','" + str(fechaRegistro)  + "','" + str(procedimiento)  + "','" + str(username_id) + "'," + liquidacionId + ",'SISTEMA'," + "'" + str(registroDerechosSala.id)+ "'," +  "'" + str(cirugiaId) + "','N','" + str(liquidaValorHomologado) + "','" + str(procedimientoId.concepto_id) + "')"
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
            miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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
    print ("Voy a generar totales")

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
    print("liquidacionId = ", liquidacionId)

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' + "'" + str(totalSuministros) + "'" + ',"totalProcedimientos" = ' + "'" + str(totalProcedimientos) + "'"  + ', "totalCopagos" = ' + "'"  + str(totalCopagos) + "'" + ' , "totalCuotaModeradora" = ' + "'"  + str(totalCuotaModeradora) + "'"  + ', anticipos = ' + "'" + str(totalAnticipos) + "'" + ' ,"totalAbonos" = ' + "'" + str(totalAbonos) + "'"  + ', "totalLiquidacion" = ' + "'" + str(totalLiquidacion) + "'" + ', "valorApagar" = ' + "'"  + str(totalApagar) + "'" + ', "totalRecibido" = ' + "'" + str(totalRecibido) + "'" + ' WHERE id =' + str(liquidacionId)
        print("comando = ", comando)
        cur3.execute(comando)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        print("Me devuelvo")

        return JsonResponse({'success': True, 'Mensajes': 'Cargos de honorarios trasladados a cuenta Paciente!'})

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
    #cupsParticipantesInforme.append({'id': '', 'nombre': ''})


     # Combo procedParticipantes

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    #comando = 'SELECT p."cirugiaProcedimiento_id" id,exa.nombre nombre FROM cirugia_cirugiasparticipantes p INNER JOIN cirugia_cirugiasprocedimientos cirProc ON (cirProc.id=p."cirugiaProcedimiento_id") INNER JOIN clinico_examenes exa on (exa.id= cirProc.cups_id) where p.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    comando = 'SELECT cirProc.id id,exa.nombre nombre FROM  cirugia_cirugiasprocedimientos cirProc LEFT JOIN cirugia_cirugiasparticipantes cirPart ON (cirPart.cirugia_id = cirProc.cirugia_id AND cirPart."cirugiaProcedimiento_id" = cirProc.id) LEFT JOIN clinico_examenes exa on (exa.id= cirProc.cups_id) where cirProc.cirugia_id = ' + "'" + str(cirugiaId) + "'"
    print(comando)
    curt.execute(comando)


    procedParticipantesInforme = []

    for id, nombre in curt.fetchall():
        procedParticipantesInforme.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print("procedParticipantesInforme", procedParticipantesInforme)


    # Fin combo procedParticipantes


    estadoCirugia = Cirugias.objects.get(id=cirugiaId)
    estadoNombreCirugia = EstadosCirugias.objects.get(id=estadoCirugia.estadoCirugia_id)

    print ("estadoNombreCirugia = " , estadoNombreCirugia.nombre )

    #procedParticipantesInforme[0]['EstadoNombreCirugia'] = estadoNombreCirugia.nombre
    #procedParticipantesInforme[0]['ProcedParticipantesInforme'] = procedParticipantesInforme

    serialized1 = json.dumps(procedParticipantesInforme, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def BuscarProcedimientosParticipantesDeCirugia(request):
    print("Entre BuscarProcedimientosParticipantesDeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)


    # Combo procedParticipantes

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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


    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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

    miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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


def CrearConveniosDeCirugia(request):
    print("Entre CrearConveniosDeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)

    convenioId = request.POST.get('convenioId')
    print("convenioId =", convenioId)

    estadoReg = 'A'

    fechaRegistro = timezone.now()

    print("paso_01")
    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432",
                                       user="postgres", password="123456")
        cur3 = miConexion3.cursor()

        print("paso_02")
        comando = 'UPDATE cirugia_cirugias SET convenio_id = ' + "'" + str(convenioId) + "' WHERE id = " + "'" + str(cirugiaId) + "'"
        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Conveio actualizado en Cirugia!'})


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


def BuscarConveniosDeCirugia(request):
    print("Entre BuscarConveniosDeCirugia")

    cirugiaId = request.POST.get('cirugiaId')
    print("cirugiaId =", cirugiaId)

    estadoReg = 'A'

    fechaRegistro = timezone.now()

    print("paso_01")
    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432",
                                       user="postgres", password="123456")
        cur3 = miConexion3.cursor()

        print("paso_02")
        detalle = 'select conv.id, conv.nombre FROM  cirugia_cirugias cir INNER JOIN facturacion_conveniospacienteingresos convIng  ON (convIng."tipoDoc_id" = cir."tipoDoc_id" And convIng.documento_id= cir.documento_id  AND convIng."consecAdmision" = cir."consecAdmision") LEFT JOIN contratacion_convenios conv ON (conv.id=convIng.convenio_id)  WHERE cir.id = ' + "'" + str(cirugiaId) + "'"

        conveniosDeCirugia = []

        print(detalle)

        cur3.execute(detalle)

        for id, nombre in cur3.fetchall():
            conveniosDeCirugia.append(
                {'id': id, 'nombre': nombre})

        miConexion3.close()
        print(conveniosDeCirugia)

        serialized1 = json.dumps(conveniosDeCirugia, default=str)

        return HttpResponse(serialized1, content_type='application/json')



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




def Load_dataDisponibilidadSalas2(request, data):

    print("Entre Load_dataDisponibilidadSalas2")

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
    print("fecha_actual", fecha_actual)
    fecha_actual = fecha_actual + timedelta(days =-1)
    print("fecha_actual", fecha_actual)
    fecha_hoyM = fecha_actual.strftime("%Y-%m-%d")
    print("fecha_hoyM a WORK:", fecha_hoy)
    dias_a_revisar = 5


    miConexionx = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
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




def CrearDisponibilidadSalasCirugia(request):

    print ("Entre crearDisponibilidadSalasCirugia" )

    username_id = request.POST["ModalDisponibilidadSalasCirugiaUsername_id"]
    print ("username_id =", username_id)

    sede = request.POST["sedesClinicaModalDisponibilidadSalasCirugia"]
    print ("sede=", sede)


    disponibilidadSalasCirugia = request.POST["disponibilidadSalasCirugia"]
    print ("disponibilidadSalasCirugia=", disponibilidadSalasCirugia)

  
    desdeHora = request.POST["desdeHora"]
    print ("desdeHora =", desdeHora)

    hastaHora = request.POST["hastaHora"]
    print ("hastaHora =", hastaHora)

    fechaDisponibilidad = request.POST["fechaDisponibilidad"]
    print ("fechaDisponibilidad =", fechaDisponibilidad)

    estadoReg = 'A'
    fechaRegistro = timezone.now()

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO sitios_disponibilidadsalas ("desdeHora", "hastaHora", "estadoReg", salas_id, "estadoDisponibilidad" , fecha) VALUES (' + "'" + str(desdeHora) + "','" + str(hastaHora) + "','" + str(estadoReg) + "'," + str(disponibilidadSalasCirugia) + ",'A','"  + str(fechaDisponibilidad) + "');"

        print(comando)
        cur3.execute(comando)


        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Disponibilidad en Sala Actualizado satisfactoriamente!'})


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
