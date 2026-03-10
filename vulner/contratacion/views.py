from django.shortcuts import render
import json
from django import forms
import cv2
import numpy as np
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Avg, Max, Min

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.http import JsonResponse
import MySQLdb
import pyodbc
import psycopg2
import json 
import datetime
from decimal import Decimal
from contratacion.models import  ConveniosLiquidacionTarifasHonorarios
from tarifarios.models import TarifariosDescripcion


# Create your views here.
def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")

def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 


# Create your views here.
def load_dataConvenios(request, data):
    print ("Entre load_data Convenios")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)
    

    #print("data = ", request.GET('data'))

    convenios = []

   
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()
   
    #detalle = 'select conv.id id, emp.nombre empresa, emp.id empresa_id,  conv.nombre nombreConvenio, conv.descripcion,  conv."vigenciaDesde" vigenciaDesde, conv."vigenciaHasta" vigenciaHasta, conv."tarifariosDescripcionProc_id" tarifariosDescripcionProc_id, des1.descripcion tarifariosDescripcionProc,  conv."tarifariosDescripcionSum_id" tarifariosDescripcionSum_id, des2.descripcion tarifariosDescripcionSum ,  conv."tarifariosDescripcionHono_id" tarifariosDescripcionHono_id, des3.descripcion tarifariosDescripcionHono  from contratacion_convenios conv, facturacion_empresas emp , tarifarios_TarifariosDescripcion des1 , tarifarios_TarifariosDescripcion des2, tarifarios_TarifariosDescripcion des3 WHERE emp.id = conv.empresa_id AND conv."tarifariosDescripcionProc_id" = des1.id AND conv."tarifariosDescripcionSum_id" = des2.id AND conv."tarifariosDescripcionHono_id" = des3.id ORDER BY conv.nombre'
    detalle = '	select conv.id id, emp.nombre empresa, emp.id empresa_id,  conv.nombre nombreConvenio, conv.descripcion,  conv."vigenciaDesde" vigenciaDesde, conv."vigenciaHasta" vigenciaHasta, conv."tarifariosDescripcionProc_id" tarifariosDescripcionProc_id, des1.descripcion tarifariosDescripcionProc,  conv."tarifariosDescripcionSum_id" tarifariosDescripcionSum_id, des2.descripcion tarifariosDescripcionSum ,  conv."tarifariosDescripcionHono_id" tarifariosDescripcionHono_id, des3.nombre tarifariosDescripcionHono from contratacion_convenios conv INNER JOIN facturacion_empresas emp ON (emp.id = conv.empresa_id) LEFT JOIN tarifarios_TarifariosDescripcion des1 ON (des1.id =conv."tarifariosDescripcionProc_id" ) LEFT JOIN tarifarios_TarifariosDescripcion des2 ON (des2.id =conv."tarifariosDescripcionSum_id") LEFT JOIN tarifarios_TarifariosDescripcionhonorarios des3 ON (des3.id =conv."tarifariosDescripcionHono_id") ORDER BY conv.nombre'

    print(detalle)

    curx.execute(detalle)

    for id, empresa, empresa_id,  nombreConvenio, descripcion,  vigenciaDesde, vigenciaHasta, tarifariosDescripcionProc_id, tarifariosDescripcionProc, tarifariosDescripcionSum_id, tarifariosDescripcionSum, tarifariosDescripcionHono_id, tarifariosDescripcionHono  in curx.fetchall():
        convenios.append(
		{"model":"convenios.convenios","pk":id,"fields":
			{'id':id, 'empresa':empresa , 'empresa_id': empresa_id, 'nombreConvenio': nombreConvenio,'descripcion':descripcion, 'vigenciaDesde': vigenciaDesde, 'vigenciaHasta': vigenciaHasta,
             'tarifariosDescripcionProc_id':tarifariosDescripcionProc_id,'tarifariosDescripcionProc':tarifariosDescripcionProc,
             'tarifariosDescripcionSum_id':tarifariosDescripcionSum_id,
             'tarifariosDescripcionSum':tarifariosDescripcionSum,
             'tarifariosDescripcionHono_id':tarifariosDescripcionHono_id, 'tarifariosDescripcionHono':tarifariosDescripcionHono
                         }})

    miConexionx.close()
    print(convenios)
    context['Convenios'] = convenios
    #convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    #convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    #convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    #convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})


    serialized1 = json.dumps(convenios, default=str)


    return HttpResponse(serialized1, content_type='application/json')



def TraerConvenio(request):

    print("Entre TraerConvenios")

    convenioId = request.POST.get('post_id')
    print("convenioId =", convenioId)

    convenio = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    comando = 'select id, nombre nombreConvenio, "vigenciaDesde", "vigenciaHasta", "porcTarifario", "porcSuministros", "valorOxigeno", "porcEsterilizacion", "porcMaterial",hospitalario, urgencias, ambulatorio, "consultaExterna", copago, moderadora, tipofactura, agrupada, "facturacionSuministros", "facturacionCups","cuentaContable", requisitos, "fechaRegistro", "estadoReg", empresa_id, "usuarioRegistro_id", descripcion,"tarifariosDescripcionProc_id", "tarifariosDescripcionHono_id", "tarifariosDescripcionSum_id" , particular FROM contratacion_convenios WHERE id = ' + "'" + str(convenioId) + "'"

    print(comando)
    cur3.execute(comando)

    for id, nombreConvenio, vigenciaDesde, vigenciaHasta, porcTarifario, porcSuministros, valorOxigeno, porcEsterilizacion, porcMaterial,	hospitalario, urgencias, ambulatorio, consultaExterna, copago, moderadora, tipofactura, agrupada, facturacionSuministros, facturacionCups,	cuentaContable, requisitos, fechaRegistro, estadoReg, empresa_id, usuarioRegistro_id, descripcion,tarifariosDescripcionProc_id, tarifariosDescripcionHono_id, tarifariosDescripcionSum_id, particular   in cur3.fetchall():
        convenio.append(
            {"model": "contratacion.convenios", "pk": id, "fields":
                {'id': id, 'nombreConvenio': nombreConvenio, 'vigenciaDesde': vigenciaDesde, 'vigenciaHasta': vigenciaHasta, 'porcTarifario': porcTarifario
                    , 'porcSuministros': porcSuministros, 'valorOxigeno': valorOxigeno, 'porcEsterilizacion': porcEsterilizacion, 'porcMaterial': porcMaterial, 'hospitalario': hospitalario
                    , 'urgencias': urgencias, 'ambulatorio': ambulatorio, 'consultaExterna': consultaExterna, 'copago': copago, 'moderadora': moderadora,
                 'tipofactura': tipofactura,'agrupada': agrupada,'facturacionSuministros': facturacionSuministros,'facturacionCups': facturacionCups,
                 'cuentaContable':cuentaContable, 'requisitos':requisitos ,'fechaRegistro': fechaRegistro, 'estadoReg':estadoReg,
                 'empresa_id':empresa_id ,'usuarioRegistro_id':usuarioRegistro_id ,'descripcion':descripcion, 'tarifariosDescripcionProc_id':tarifariosDescripcionProc_id ,
                 'tarifariosDescripcionHono_id': tarifariosDescripcionHono_id, 'tarifariosDescripcionSum_id':tarifariosDescripcionSum_id ,'particular':particular }})

    miConexion3.close()
    print(convenio)

    serialized1 = json.dumps(convenio, default=str)

    return HttpResponse(serialized1, content_type='application/json')




    return JsonResponse({'success': True, 'Mensaje': 'Tarifario Sabana creado !'})


def EditarGuardarConvenios(request):

    print("Entre EditarGuardarConvenios")

    convenioId = request.POST.get('post_id')
    print("convenioId =", convenioId)

    nombreConvenio = request.POST.get('nombreConvenio')
    print("nombreConvenio =", nombreConvenio)

    vigenciaDesde = request.POST.get('vigenciaDesde')
    print("vigenciaDesde =", vigenciaDesde)

    vigenciaHasta = request.POST.get('vigenciaHasta')
    print("vigenciaHasta =", vigenciaHasta)

    porcTarifario = request.POST.get('porcTarifario')
    print("porcTarifario =", porcTarifario)

    if (porcTarifario==''):
        porcTarifario='null'

    porcSuministros = request.POST.get('porcSuministros')
    print("porcSuministros =", porcSuministros)

    if (porcSuministros==''):
        porcSuministros='null'


    valorOxigeno = request.POST.get('valorOxigeno')
    print("valorOxigeno =", valorOxigeno)

    if (valorOxigeno == ''):
        valorOxigeno = 'null'


    porcEsterilizacion = request.POST.get('porcEsterilizacion')
    print("porcEsterilizacion =", porcEsterilizacion)

    if (porcEsterilizacion == ''):
        porcEsterilizacion = 'null'


    porcMaterial = request.POST.get('porcMaterial')
    print("porcMaterial =", porcMaterial)

    if (porcMaterial == ''):
        porcMaterial = 'null'


    hospitalario = request.POST.get('hospitalario')
    print("hospitalario =", hospitalario)
    urgencias = request.POST.get('urgencias')
    print("urgencias =", urgencias)
    ambulatorio = request.POST.get('ambulatorio')
    print("ambulatorio =", ambulatorio)
    consultaExterna = request.POST.get('consultaExterna')
    print("consultaExterna =", consultaExterna)
    copago = request.POST.get('copago')
    print("copago =", copago)
    moderadora = request.POST.get('moderadora')
    print("moderadora =", moderadora)
    tipofactura = request.POST.get('tipofactura')
    print("tipofactura =", tipofactura)
    facturacionSuministros = request.POST.get('facturacionSuministros')
    print("facturacionSuministros =", facturacionSuministros)
    facturacionCups = request.POST.get('facturacionCups')
    print("facturacionCups =", facturacionCups)
    cuentaContable = request.POST.get('cuentaContable')
    print("cuentaContable =", cuentaContable)
    facturacionCups = request.POST.get('facturacionCups')
    print("facturacionCups =", facturacionCups)
    requisitos = request.POST.get('requisitos')
    print("requisitos =", requisitos)
    empresa_id = request.POST.get('empresa_id')
    print("empresa_id =", empresa_id)
    usuarioRegistro_id = request.POST.get('usuarioRegistro_id')
    print("usuarioRegistro_id =", usuarioRegistro_id)

    tarifariosDescripcionProc_id = request.POST.get('tarifariosDescripcionProc_id')
    print("tarifariosDescripcionProc_id =", tarifariosDescripcionProc_id)

    if (tarifariosDescripcionProc_id == ''):
        tarifariosDescripcionProc_id = 'null'

    tarifariosDescripcionSum_id = request.POST.get('tarifariosDescripcionSum_id')
    print("tarifariosDescripcionSum_id =", tarifariosDescripcionSum_id)

    if (tarifariosDescripcionSum_id == ''):
        tarifariosDescripcionSum_id = 'null'


    tarifariosDescripcionHono_id = request.POST.get('tarifariosDescripcionHono_id')
    print("tarifariosDescripcionHono_id =", tarifariosDescripcionHono_id)
    if (tarifariosDescripcionHono_id == ''):
        tarifariosDescripcionHono_id = 'null'


    descripcion = request.POST.get('descripcion')
    print("descripcion =", descripcion)

    serviciosAdministrativos_id = request.POST.get('serviciosAdministrativos_id')
    print("serviciosAdministrativos_id =", serviciosAdministrativos_id)

    if (serviciosAdministrativos_id == ''):
        serviciosAdministrativos_id = 'null'


    particular = request.POST.get('particular')
    print("particular =", particular)

    estadoReg = 'A'

    #fechaRegistro = datetime.datetime.now()
    fechaRegistro = timezone.now()


    miConexiont = None
    try:

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
        curt = miConexiont.cursor()

        comando = 'UPDATE contratacion_Convenios SET nombre = ' + "'" + str(nombreConvenio) + "'," + '"vigenciaDesde" = ' + "'" + str(vigenciaDesde) + "'," + '"vigenciaHasta" = ' + "'" + str(vigenciaHasta) + "'," + '"porcTarifario" = ' + str(porcTarifario) + "," + '"porcSuministros" = ' + str(porcSuministros) + "," + '"valorOxigeno" = ' + str(valorOxigeno) + "," + '"porcEsterilizacion" = ' + str(porcEsterilizacion) + "," + '"porcMaterial" = ' + str(porcMaterial) + "," + '"hospitalario" = ' + "'" + str(hospitalario) + "'," + '"urgencias" = ' + "'" + str(urgencias) + "'," + '"ambulatorio" = ' + "'" + str(ambulatorio) + "'," + '"consultaExterna" = ' + "'" + str(consultaExterna) + "'," + '"copago" = ' + "'" + str(copago) + "'," + '"moderadora" = ' + "'" + str(moderadora) + "'," + '"tipofactura" = ' + "'" + str(tipofactura) + "'," + '"facturacionSuministros" = ' + "'" + str(facturacionSuministros) + "'," + '"facturacionCups" = ' + "'" + str(facturacionCups) + "'," + '"cuentaContable" = ' + "'" + str(cuentaContable) + "',"  + '"requisitos" = ' + "'" + str(requisitos) + "'," + '"empresa_id" = ' + "'" + str(empresa_id) + "'," + '"usuarioRegistro_id" = ' + "'" + str(usuarioRegistro_id) + "'," + '"tarifariosDescripcionProc_id" = ' + str(tarifariosDescripcionProc_id) + "," + '"tarifariosDescripcionSum_id" = ' + str(tarifariosDescripcionSum_id) + ", descripcion = " + "'" + str(descripcion) + "'," + '"tarifariosDescripcionHono_id" = '  + str(tarifariosDescripcionHono_id)  + ',"serviciosAdministrativos_id"= ' + str(serviciosAdministrativos_id) + ' , particular = ' + "'" + str(particular) + "'  WHERE id = " + "'" + str(convenioId) + "'"

        print(comando)
        curt.execute(comando)

        miConexiont.commit()
        curt.close()
        miConexiont.close()

        return JsonResponse({'success': True, 'Mensajes': 'Convenio Actualizado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexiont.rollback()
        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})


    finally:
        if miConexiont:
            curt.close()
            miConexiont.close()


def CrearGuardarConvenios(request):

    print("Entre CrearGuardarConvenios")

    convenioId = request.POST.get('post_id')
    print("convenioId =", convenioId)

    nombreConvenio = request.POST.get('nombreConvenio')
    print("nombreConvenio =", nombreConvenio)

    vigenciaDesde = request.POST.get('vigenciaDesde')
    print("vigenciaDesde =", vigenciaDesde)

    vigenciaHasta = request.POST.get('vigenciaHasta')
    print("vigenciaHasta =", vigenciaHasta)

    porcTarifario = request.POST.get('porcTarifario')
    print("porcTarifario =", porcTarifario)

    if (porcTarifario==''):
        porcTarifario='null'




    porcSuministros = request.POST.get('porcSuministros')
    print("porcSuministros =", porcSuministros)

    if (porcSuministros==''):
        porcSuministros='null'


    valorOxigeno = request.POST.get('valorOxigeno')
    print("valorOxigeno =", valorOxigeno)

    if (valorOxigeno == ''):
        valorOxigeno = 'null'


    porcEsterilizacion = request.POST.get('porcEsterilizacion')
    print("porcEsterilizacion =", porcEsterilizacion)

    if (porcEsterilizacion == ''):
        porcEsterilizacion = 'null'


    porcMaterial = request.POST.get('porcMaterial')
    print("porcMaterial =", porcMaterial)

    if (porcMaterial == ''):
        porcMaterial = 'null'


    hospitalario = request.POST.get('hospitalario')
    print("hospitalario =", hospitalario)
    urgencias = request.POST.get('urgencias')
    print("urgencias =", urgencias)
    ambulatorio = request.POST.get('ambulatorio')
    print("ambulatorio =", ambulatorio)
    consultaExterna = request.POST.get('consultaExterna')
    print("consultaExterna =", consultaExterna)
    copago = request.POST.get('copago')
    print("copago =", copago)
    moderadora = request.POST.get('moderadora')
    print("moderadora =", moderadora)
    agrupada = request.POST.get('agrupada')
    print("agrupada =", agrupada)

    tipofactura = request.POST.get('tipofactura')
    print("tipofactura =", tipofactura)
    facturacionSuministros = request.POST.get('facturacionSuministros')
    print("facturacionSuministros =", facturacionSuministros)
    facturacionCups = request.POST.get('facturacionCups')
    print("facturacionCups =", facturacionCups)
    cuentaContable = request.POST.get('cuentaContable')
    print("cuentaContable =", cuentaContable)
    facturacionCups = request.POST.get('facturacionCups')
    print("facturacionCups =", facturacionCups)
    requisitos = request.POST.get('requisitos')
    print("requisitos =", requisitos)
    empresa_id = request.POST.get('empresa_id')
    print("empresa_id =", empresa_id)
    usuarioRegistro_id = request.POST.get('usuarioRegistro_id')
    print("usuarioRegistro_id =", usuarioRegistro_id)

    tarifariosDescripcionProc_id = request.POST.get('tarifariosDescripcionProc_id')
    print("tarifariosDescripcionProc_id =", tarifariosDescripcionProc_id)

    if (tarifariosDescripcionProc_id == ''):
        tarifariosDescripcionProc_id = 'null'

    tarifariosDescripcionSum_id = request.POST.get('tarifariosDescripcionSum_id')
    print("tarifariosDescripcionSum_id =", tarifariosDescripcionSum_id)

    if (tarifariosDescripcionSum_id == ''):
        tarifariosDescripcionSum_id = 'null'

    serviciosAdministrativos_id = request.POST.get('serviciosAdministrativos_id')
    print("serviciosAdministrativos_id =", serviciosAdministrativos_id)

    if (serviciosAdministrativos_id == ''):
        serviciosAdministrativos_id = 'null'

    tarifariosDescripcionHono_id = request.POST.get('tarifariosDescripcionHono_id')
    print("tarifariosDescripcionHono_id =", tarifariosDescripcionHono_id)
    if (tarifariosDescripcionHono_id == ''):
        tarifariosDescripcionHono_id = 'null'


    descripcion = request.POST.get('descripcion')
    print("descripcion =", descripcion)

    particular = request.POST.get('particular')
    print("particular =", particular)


    estadoReg = 'A'

    #fechaRegistro = datetime.datetime.now()
    fechaRegistro = timezone.now()

    print ("voy a crear un Convenio")

    miConexiont = None
    try:


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
        curt = miConexiont.cursor()

        comando = 'INSERT INTO contratacion_Convenios (nombre, "vigenciaDesde", "vigenciaHasta", "porcTarifario", "porcSuministros", "valorOxigeno", "porcEsterilizacion", "porcMaterial", hospitalario, urgencias, ambulatorio, "consultaExterna", copago, moderadora, tipofactura, agrupada, "facturacionSuministros", "facturacionCups", "cuentaContable", requisitos, "fechaRegistro", "estadoReg", empresa_id, "usuarioRegistro_id", descripcion, "tarifariosDescripcionProc_id", "tarifariosDescripcionHono_id", "tarifariosDescripcionSum_id", "serviciosAdministrativos_id", particular) VALUES (' + "'" + str(nombreConvenio) + "'," + "'" + str(vigenciaDesde) + "','" + str(vigenciaHasta) + "'," + str(porcTarifario) + "," + str(porcSuministros) + "," + str(valorOxigeno) + "," + str(porcEsterilizacion) + "," + str(porcMaterial) + "," + "'" + str(hospitalario) + "'," + "'" + str(urgencias) + "'," + "'" + str(ambulatorio) + "'," + "'" + str(consultaExterna) + "'," + "'" + str(copago) + "'," + "'" + str(moderadora) + "'," + "'" + str(tipofactura) + "','" + str(agrupada) + "'," + "'" + str(facturacionSuministros) + "'," + "'" + str(facturacionCups) + "'," + "'" + str(cuentaContable) + "','"  + str(requisitos)   + "'," + "'" +  str(fechaRegistro) + "'," + "'" +  str(estadoReg) + "','" + str(empresa_id) + "',"  + str(usuarioRegistro_id) + ",'" + str(descripcion) + "',"   + str(tarifariosDescripcionProc_id) + "," + str(tarifariosDescripcionHono_id)  +  "," + str(tarifariosDescripcionSum_id) + ",'"  + str(serviciosAdministrativos_id) + "','" + str(particular) + "'" + ')'

        print(comando)
        curt.execute(comando)

        miConexiont.commit()
        curt.close()
        miConexiont.close()

        return JsonResponse({'success': True, 'Mensajes': 'Convenio Creada satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexiont:
            print("Entro ha hacer el Rollback")
            miConexiont.rollback()
        message_error= str(error)
        return JsonResponse({'success': False, 'Mensajes': message_error})


    finally:
        if miConexiont:
            curt.close()
            miConexiont.close()


def PostConsultaConvenios(request):
    print ("Entre PostConsultaConvenios ")

    Post_id = request.POST["post_id"]

    print("id = ", Post_id)
    llave = Post_id.split('-')
    print ("llave = " ,llave)
    print ("primero=" ,llave[0])

    context = {}

    # Combo Empresas

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.129", database="vulner", port="5432", user="postgres", password="pass123")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM facturacion_empresas c"

    curt.execute(comando)
    print(comando)

    empresas = []

    for id, nombre in curt.fetchall():
        empresas.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(empresas)

    context['Empresas'] = empresas

    # Fin combo empresas

    # Combo sEmpresas

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM facturacion_empresas c"

    curt.execute(comando)
    print(comando)

    sempresas = []

    for id, nombre in curt.fetchall():
        sempresas.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(sempresas)

    context['Sempresas'] = sempresas

    # Fin combo sempresas



    # Combo Tipos Tarifa

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM tarifarios_TiposTarifa c"

    curt.execute(comando)
    print(comando)

    tiposTarifa = []

    for id, nombre in curt.fetchall():
        tiposTarifa.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposTarifa)

    context['TiposTarifa'] = tiposTarifa

    # Fin combo Tipos Tarifa

    # Combo Tipos Honorarios

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM tarifarios_TiposHonorarios c"

    curt.execute(comando)
    print(comando)

    honorarios = []

    for id, nombre in curt.fetchall():
        honorarios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(honorarios)

    context['Honorarios'] = honorarios
    # Fin combo Tipos Honorarios



    # Combo Cups

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
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

    context['Cups'] = cups

    # Fin combo Cups


    # Combo Suministras

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    #comando = 'SELECT c.id id, c.nombre||' + "' '" +  '||c.cums nombre FROM facturacion_suministros c order by c.nombre'
    comando = 'SELECT c.id id, c.nombre nombre FROM facturacion_suministros c order by c.nombre'

    curt.execute(comando)
    print(comando)

    suministras = []

    suministras.append({'id': '', 'nombre': ''})

    for id,  nombre in curt.fetchall():
        suministras.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    print(suministras)

    context['Suministras'] = suministras

    # Fin combo suministras


    # Combo Conceptos

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id, c.nombre nombre FROM facturacion_conceptos c order by c.nombre'

    curt.execute(comando)
    print(comando)

    conceptos = []

    conceptos.append({'id': '', 'nombre': ''})

    for id,  nombre in curt.fetchall():
        conceptos.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    print(conceptos)

    context['Conceptos'] = conceptos

    # Fin combo conceptos

    # Combo Conceptosa

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT c.id id, c.nombre nombre FROM facturacion_conceptos c order by c.nombre'

    curt.execute(comando)
    print(comando)

    conceptosa = []

    conceptos.append({'id': '', 'nombre': ''})

    for id,  nombre in curt.fetchall():
        conceptosa.append({'id': id,  'nombre': nombre})

    miConexiont.close()
    print(conceptosa)

    context['Conceptosa'] = conceptosa

    # Fin combo conceptos


    if request.method == 'POST':

        # Abro Conexion

        conveniosD = []

    
        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        curx = miConexionx.cursor()
   
        detalle = 'select conv.id id,conv.nombre nombre, conv."vigenciaDesde" vigenciaDesde, conv."vigenciaHasta" vigenciaHasta, conv.empresa_id  empresa,   "porcTarifario",  "porcSuministros",  "valorOxigeno" ,  "porcEsterilizacion",  "porcMaterial" ,  hospitalario ,  urgencias ,  ambulatorio ,  "consultaExterna" ,  copago ,  moderadora ,   tipofactura ,  agrupada ,  "facturacionSuministros" ,  "facturacionCups" ,  "cuentaContable" ,  requisitos  from contratacion_convenios conv, facturacion_empresas emp WHERE emp.id = conv.empresa_id and  conv.id = ' + "'" + str(Post_id) + "'"

        print(detalle)

        curx.execute(detalle)

        for id, nombre, vigenciaDesde, vigenciaHasta, empresa,  porcTarifario,  porcSuministros,  valorOxigeno ,  porcEsterilizacion,  porcMaterial ,  hospitalario ,  urgencias ,  ambulatorio ,  consultaExterna ,  copago ,  moderadora ,   tipofactura ,  agrupada ,  facturacionSuministros ,  facturacionCups ,  cuentaContable ,  requisitos   in curx.fetchall():
           conveniosD.append(
		{"model":"convenios.convenios","pk":id,"fields":
			{'id':id, 'nombre': nombre, 'vigenciaDesde': vigenciaDesde, 'vigenciaHasta': vigenciaHasta, 'empresa': empresa,
          
             'porcTarifario': porcTarifario, 'porcSuministros': porcSuministros,
             'valorOxigeno': valorOxigeno,
             'porcEsterilizacion': porcEsterilizacion,
             'porcMaterial': porcMaterial,
             'hospitalario': hospitalario,
             'urgencias': urgencias,
             'ambulatorio': ambulatorio,
             'consultaExterna': consultaExterna,
             'copago': copago,
             'moderadora': moderadora,
             'tipofactura': tipofactura,
             'agrupada': agrupada,
             'facturacionSuministros': facturacionSuministros,
             'facturacionCups': facturacionCups,
             'cuentaContable': cuentaContable,
             'requisitos': requisitos }})

        miConexionx.close()
        print(conveniosD)

        # Cierro Conexion

        print ("Prueba convenioNombre" , conveniosD[0]['fields']['nombre'])


        return JsonResponse({'pk':conveniosD[0]['pk'], 'id':conveniosD[0]['pk'], 'nombre':conveniosD[0]['fields']['nombre'],'vigenciaDesde':conveniosD[0]['fields']['vigenciaDesde'],
                             'vigenciaHasta':conveniosD[0]['fields']['vigenciaHasta'],  'empresa': conveniosD[0]['fields']['empresa'],
                             'porcTarifario':conveniosD[0]['fields']['porcTarifario'] ,    'porcSuministros':conveniosD[0]['fields']['porcSuministros'],
                             'valorOxigeno': conveniosD[0]['fields']['valorOxigeno'],
                             'porcEsterilizacion': conveniosD[0]['fields']['porcEsterilizacion'],
                             'porcMaterial': conveniosD[0]['fields']['porcMaterial'],
                             'hospitalario': conveniosD[0]['fields']['hospitalario'],
                             'urgencias': conveniosD[0]['fields']['urgencias'],
                             'ambulatorio': conveniosD[0]['fields']['ambulatorio'],
                             'consultaExterna': conveniosD[0]['fields']['consultaExterna'],
                             'copago': conveniosD[0]['fields']['copago'],
                             'moderadora': conveniosD[0]['fields']['moderadora'],
                             'tipofactura': conveniosD[0]['fields']['tipofactura'],
                             'agrupada': conveniosD[0]['fields']['agrupada'],
                             'facturacionSuministros': conveniosD[0]['fields']['facturacionSuministros'],
                             'facturacionCups': conveniosD[0]['fields']['facturacionCups'],
                             'cuentaContable': conveniosD[0]['fields']['cuentaContable'],
                             'requisitos': conveniosD[0]['fields']['requisitos'], 'Empresas': empresas, 'TiposTarifa':tiposTarifa, 'Conceptos': conceptos, 'Cups':cups, 'Suministras':suministras, 'Sempresas':sempresas, 'Honorarios':honorarios
                             })

    else:
        return JsonResponse({'errors':'Something went wrong!'})


# Create your views here.
def load_dataConveniosProcedimientos(request, data):
    print ("Entre load_data Conveniosrocedimientos")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)

    convenioId = d['valor']
    

    #print("data = ", request.GET('data'))

    convenios = []
    
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()
   
    detalle = 'select convProc.id procId, conv.id id, convProc."codigoHomologado" codigoHomologado, convProc.valor valor,  convProc.cups_id cupsId ,exa.nombre cupsNombre, tipostar.nombre tarifa FROM contratacion_convenios conv , contratacion_conveniosprocedimientos convProc, tarifarios_tipostarifa tipostar, clinico_examenes exa WHERE conv.id = convProc.convenio_id and convProc."tipoTarifa_id" = tipostar.id and convProc.cups_id = exa.id and conv.id = ' + "'" + str(convenioId) + "'"

    print(detalle)

    curx.execute(detalle)

    conveniosP = []

    for procId , id, codigoHomologado, valor,  cupsId ,cupsNombre,tarifa in curx.fetchall():
            conveniosP.append(
                {"model": "conveniosP.conveniosP", "pk": procId, "fields":
                  {"procId":procId, "id": id,
                     "codigoHomologado": codigoHomologado,
                     "valor": valor,
                     "cupsId": cupsId, "cupsNombre": cupsNombre,
                     "tarifa": tarifa }})

    miConexionx.close()
    print(conveniosP)

    context['ConveniosP'] = conveniosP


    serialized1 = json.dumps(conveniosP, default=decimal_serializer)


    return HttpResponse(serialized1, content_type='application/json')




def GuardarConveniosProcedimientos( request):

    if request.method == 'POST':

        codigoHomologado = request.POST["codigoHomologado"]
        tiposTarifa = request.POST["tiposTarifa"]
        #nombreTiposTarifa = request.POST["nombreTiposTarifa"]
        cups = request.POST["xcups"]
        #nombreCups = request.POST["nombreCups"]
        valor = request.POST["valor"]
        convenioId = request.POST["convenioId"]
        conceptos = request.POST["xconceptos"]
     
        if tiposTarifa == '':
           tiposTarifa="null"

        if cups == '':
            cups ="null"


        estadoReg= 'A'
        username_id = request.POST["username_id"]
        fechaRegistro = timezone.now()
        #fechaRegistro = datetime.datetime.now()

     

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        curt = miConexiont.cursor()
        comando = 'INSERT INTO contratacion_conveniosprocedimientos ("codigoHomologado", valor, "fechaRegistro", "estadoReg", convenio_id, cups_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) values (' + "'" + str(codigoHomologado) + "'," + "'" + str(valor) + "'," + "'" + str(fechaRegistro) +"'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + "'" + str(cups) + "'," + "'" + str(tiposTarifa) + "'," + "'" + str(username_id) + "',"  + str(conceptos) + ")"

        print(comando)

        try:
            curt.execute(comando)
        except (Exception, psycopg2.DatabaseError) as error:

            print("Error = " ,error)
            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})

            #return JsonResponse({'success': True, 'Mensajes': 'Registro ya existe ¡'})

        miConexiont.commit()
        curt.close()
        miConexiont.close()

        return JsonResponse({'success': True, 'Mensajes': 'Tarifa de convenio Creada satisfactoriamente!'})



def GuardarConvenio( request):

    print ("Entre Guardar Convenio")	

    if request.method == 'POST':

        convenioId=request.POST["convenioId"]
        nombre = request.POST["nombre"]
        empresa=request.POST["empresa"]
        vigenciaDesde=request.POST["vigenciaDesde"]
        vigenciaHasta=request.POST["vigenciaHasta"]

        porcTarifario=request.POST["porcTarifario"]
        porcSuministros=request.POST["porcSuministros"]
        valorOxigeno=request.POST["valorOxigeno"]
        porcEsterilizacion=request.POST["porcEsterilizacion"]
        porcMaterial=request.POST["porcMaterial"]
        hospitalario=request.POST["hospitalario"]
        urgencias=request.POST["urgencias"]
        consultaExterna=request.POST["consultaExterna"]
        copago=request.POST["copago"]
        moderadora=request.POST["moderadora"]
        tipoFactura=request.POST["tipoFactura"]
        agrupada=request.POST["agrupada"]
        facturacionSuministros=request.POST["facturacionSuministros"]
        facturacionCups=request.POST["facturacionCups"]
        cuentaContable=request.POST["cuentaContable"]
        requisitos=request.POST["requisitos"]

        if vigenciaDesde == '':
            vigenciaDesde="0001-01-01 00:00:00"

        if vigenciaHasta == '':
            vigenciaHasta="0001-01-01 00:00:00"

        if porcTarifario == '':
            porcTarifario=0

        if porcSuministros == '':
            porcSuministros=0

        if valorOxigeno == '':
            valorOxigeno=0

        if porcEsterilizacion == '':
            porcEsterilizacion=0

        if porcMaterial == '':
            porcMaterial=0


        estadoReg= 'A'
        username_id = request.POST["username_id"]

        #fechaRegistro = datetime.datetime.now()
        fechaRegistro = timezone.now()

        #ultId = Convenios.objects.all().aggregate(maximo=Coalesce(Max('id'), 0 ))
        #ultId1 = (ultId['maximo']) + 1

        miConexiont = None
        try:

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
            curt = miConexiont.cursor()
            comando = 'INSERT INTO contratacion_convenios (nombre,empresa_id,"vigenciaDesde","vigenciaHasta","porcTarifario", "porcSuministros", "valorOxigeno", "porcEsterilizacion", "porcMaterial",hospitalario, urgencias,"consultaExterna",copago, moderadora, "tipofactura",agrupada,"facturacionSuministros","facturacionCups", "cuentaContable", requisitos,"fechaRegistro","estadoReg","usuarioRegistro_id") VALUES (' + "'" + str(nombre) + "'," + "'" + str(empresa) + "'," + "'" + str(vigenciaDesde) + "'," + "'" + str(vigenciaHasta) + "',"  +  str(porcTarifario) + "," + str(porcSuministros) + "," + str(valorOxigeno) + "," + str(porcEsterilizacion) + ","  + str(porcMaterial) + "," + "'" + str(hospitalario) + "'," + "'" + str(urgencias) + "'," + "'" + str(consultaExterna) + "'," + "'" + str(copago) + "'," + "'" + str(moderadora) + "'," + "'" + str(tipoFactura) + "'," + "'" + str(agrupada) + "'," + "'" + str(facturacionSuministros) + "'," + "'" + str(facturacionCups) + "'," + "'" + str(cuentaContable) + "'," + "'" + str(requisitos) + "'," + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(username_id) + "')"
            print(comando)

            curt.execute(comando)
            miConexiont.commit()
            curt.close()
            miConexiont.close()

            return JsonResponse({'success': True, 'Mensajes': 'Convenio Creado satisfactoriamente!'})

        except psycopg2.DatabaseError as error:

            print ("Entre por rollback" , error)

            if miConexiont:
                print("Entro ha hacer el Rollback")
                miConexiont.rollback()

            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})

        finally:

            if miConexiont:
                curt.close()
                miConexiont.close()



def GuardarConvenio1( request):

    print ("Entre Guardar Convenio1")	

    if request.method == 'POST':

        convenioId=request.POST["convenioId"]
        print("convenioId = " , convenioId)
        nombre=request.POST["nombre"]
        empresa=request.POST["empresa"]
        vigenciaDesde=request.POST["vigenciaDesde"]
        vigenciaHasta=request.POST["vigenciaHasta"]
        porcTarifario=request.POST["porcTarifario"]
        porcSuministros=request.POST["porcSuministros"]
        valorOxigeno=request.POST["valorOxigeno"]
        porcEsterilizacion=request.POST["porcEsterilizacion"]
        porcMaterial=request.POST["porcMaterial"]
        hospitalario=request.POST["hospitalario"]
        urgencias=request.POST["urgencias"]
        consultaExterna=request.POST["consultaExterna"]
        copago=request.POST["copago"]
        moderadora=request.POST["moderadora"]
        tipoFactura=request.POST["tipoFactura"]
        agrupada=request.POST["agrupada"]
        facturacionSuministros=request.POST["facturacionSuministros"]
        facturacionCups=request.POST["facturacionCups"]
        cuentaContable=request.POST["cuentaContable"]
        requisitos=request.POST["requisitos"]

        if vigenciaDesde == '':
            vigenciaDesde="0001-01-01 00:00:00"

        if vigenciaHasta == '':
            vigenciaHasta="0001-01-01 00:00:00"

        if vigenciaDesde == '':
            vigenciaDesde="0001-01-01 00:00:00"

        if vigenciaHasta == '':
            vigenciaHasta="0001-01-01 00:00:00"

        if porcTarifario == '':
            porcTarifario=0

        if porcSuministros == '':
            porcSuministros=0

        if valorOxigeno == '':
            valorOxigeno=0

        if porcEsterilizacion == '':
            porcEsterilizacion=0

        if porcMaterial == '':
            porcMaterial=0


        estadoReg= 'A'
        username_id = request.POST["username_id"]
        #fechaRegistro = datetime.datetime.now()
        fechaRegistro = timezone.now()

        miConexiont = None
        try:

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
            curt = miConexiont.cursor()

            #comando = 'UPDATE contratacion_convenios (nombre,empresa_id,"vigenciaDesde","vigenciaHasta",tarifa, "porcTarifario", "porcSuministros", "valorOxigeno", "porcEsterilizacion", "porcMaterial",hospitalario, urgencias,"consultaExterna",copago, moderadora, "tipoFactura",agrupada,"facturacionSuministros","facturacionCups", "cuentaContable", requisitos,"fechaRegistro",estadoReg,"usuarioRegistro_id") VALUES (' + "'" + str(nombre) + "'," + "'" + str(empresa) + "'," + "'" + str(vigenciaDesde) + "'," + "'" + str(vigenciaHasta) + "'," + "'" + str(tarifa) + "'," + "'" + str(porcTarifario) + "'," + "'" + str(porcSuministros) + "'," + "'" + str(valorOxigeno) + "'," + "'" + str(porcEsterilizacion) + "'," + "'" + str(porcMaterial) + "'," + "'" + str(hospitalario) + "'," + "'" + str(urgencias) + "'," + "'" + str(consultaExterna) + "'," + "'" + str(copago) + "'," + "'" + str(moderadora) + "'," + "'" + str(tipoFactura) + "'," + "'" + str(agrupada) + "'," + "'" + str(acturacionSuministros) + "'," + "'" + str(facturacionCups) + "'," + "'" + str(cuentaContable) + "'," + "'" + str(requisitos) + "'," + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(username_id) + "'"
            comando = 'UPDATE contratacion_convenios set nombre = ' + "'" + str(nombre) + "', empresa_id = " + str(empresa) + ","  + '"vigenciaDesde" = ' + "'" + str(vigenciaDesde) + "'," + '"vigenciaHasta" = ' + "'" + str(vigenciaHasta) + "'," + '"porcTarifario" = ' + str(porcTarifario) + "," + '"porcSuministros" = ' + str(porcSuministros) + "," + '"valorOxigeno" = ' + str(valorOxigeno) + "," + '"porcEsterilizacion" = ' + str(porcEsterilizacion) + "," + 'hospitalario = ' + "'" + str(hospitalario) + "'," + 'urgencias = ' + "'" + str(urgencias) + "'," + '"consultaExterna" = ' + "'" + str(consultaExterna) + "'," + 'copago = ' + "'" + str(copago) + "'," + 'moderadora = ' + "'" + str(moderadora) + "'," + 'agrupada = ' + "'" + str(agrupada) + "'," + '"facturacionSuministros" = ' + "'" + str(facturacionSuministros) + "'," + '"facturacionCups" = ' + "'" + str(facturacionCups) + "'," + '"cuentaContable" = ' + "'" + str(cuentaContable) + "'," + 'requisitos = ' + "'" + str(requisitos) + "'," + '"fechaRegistro" = ' + "'" + str(fechaRegistro) + "'," + '"estadoReg" = ' + "'" + str(estadoReg) + "'," + '"usuarioRegistro_id" = ' + "'" + str(username_id) + "'" + ' WHERE id = ' + "'" + str(convenioId) + "'"


            print(comando)
            curt.execute(comando)
            miConexiont.commit()
            curt.close()
            miConexiont.close()

            return JsonResponse({'success': True, 'Mensajes': 'Convenio Creado satisfactoriamente!'})

        except psycopg2.DatabaseError as error:
            print ("Entre por rollback" , error)
            if miConexiont:
                print("Entro ha hacer el Rollback")
                miConexiont.rollback()
            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})

        finally:
            if miConexiont:
                curt.close()
                miConexiont.close()


def GrabarTarifa( request):

    print ("Entre Grabar Tarifa")


    if request.method == 'POST':

        convenioId=request.POST["convenioId1"]
        print("convenioId = " , convenioId)
        tiposTarifa=request.POST["tiposTarifa"]
        print("tiposTarifa = ", tiposTarifa)
        conceptos=request.POST["conceptos"]
        print("conceptos = ", conceptos)
        porcentage=request.POST["porcentage"]
        print("porcentage = ", porcentage)
        valorVariacion=request.POST["valorVariacion"]
        print("valorVariacion = ", valorVariacion)
        estadoReg= 'A'
        username_id = request.POST["username_id"]
        fechaRegistro = datetime.datetime.now()

        accion = request.POST["accion"]

        miConexion3 = None
        try:


                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
                curt = miConexiont.cursor()

                if (accion == 'Crear' and porcentage != 0 and conceptos == '' and valorVariacion == '0' ):
                    print("Entre1")
                    comando = 'INSERT INTO contratacion_conveniosProcedimientos ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,cups_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast("codigoCups_id" as numeric), '  + str(tiposTarifa) + "," + "'" +  str(username_id) + "'" +  ', concepto_id from tarifarios_tarifas where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


                if (accion == 'Crear' and porcentage != 0 and conceptos != '' and valorVariacion == '0'):
                    print("Entre2")
                    comando = 'INSERT INTO contratacion_conveniosProcedimientos ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,cups_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast("codigoCups_id" as numeric), ' +"'"  + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id from tarifarios_tarifas where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"


                if (accion == 'Crear' and porcentage == '0'  and conceptos == '' and valorVariacion != '0'):
                    print("Entre3")
                    comando = 'INSERT INTO contratacion_conveniosProcedimientos ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,cups_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round( ' + "'" + str(valorVariacion) + "')" + ' subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) +  "'," + ' cast("codigoCups_id" as numeric), '   +"'" + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id from tarifarios_tarifas where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


                if (accion == 'Crear' and porcentage == '0'  and conceptos != '' and valorVariacion !='0'):
                    print("Entre4")
                    comando = 'INSERT INTO contratacion_conveniosProcedimientos ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,cups_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round( ' + "'" + str(valorVariacion) + "')" + ' subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast("codigoCups_id" as numeric), '  +"'"  + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id from tarifarios_tarifas where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"


                if (accion == 'Borrar' and conceptos == '' and valorVariacion == '0' ):
                    print("Entre11")
                    comando = 'DELETE FROM contratacion_conveniosProcedimientos  where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


                if (accion == 'Borrar' and conceptos != '' and valorVariacion == '0'):
                    print("Entre12")
                    comando = 'DELETE FROM contratacion_conveniosProcedimientos where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"


                if (accion == 'Borrar' and conceptos == '' and valorVariacion != '0'):
                    print("Entre13")
                    comando = 'DELETE FROM contratacion_conveniosProcedimientos where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' and valor = " + "'" + str(valorVariacion) + "'"


                if (accion == 'Borrar' and conceptos != '' and valorVariacion !='0'):
                    print("Entre14")
                    comando = 'DELETE FROM contratacion_conveniosProcedimientos where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "' AND valor = " + "'" +str(valorVariacion) + "'"


                print(comando)

                curt.execute(comando)

                miConexiont.commit()
                curt.close()
                miConexiont.close()


                if (accion == 'Crear'):
                    return JsonResponse({'success': True, 'Mensajes': 'Tarifas de convenio actualizadas satisfactoriamente!'})

                if (accion == 'Borrar'):
                    return JsonResponse({'success': True, 'Mensages': 'Registros borrados satisfactoriamente!'})

        except psycopg2.DatabaseError as error:
            print ("Entre por rollback" , error)
            if miConexiont:
                print("Entro ha hacer el Rollback")
                miConexiont.rollback()
            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})

        finally:
            if miConexiont:
                curt.close()
                miConexiont.close()



def DeleteConveniosProcedimientos(request):

    print ("Entre DeleteConveniosProcedimientos" )

    try:
        with transaction.atomic():

            id = request.POST["post_id"]
            print ("el id es = ", id)

            post = ConveniosProcedimientos.objects.get(id=id)
            post.delete()

            return JsonResponse({'success': True, 'Mensajes': 'Registro Borrado !'})

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)
        return JsonResponse({'success': False, 'Mensajes': e})

# Create your views here.
def load_dataConveniosSuministros(request, data):
    print ("Entre load_data ConveniosSuministros")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)

    convenioId = d['valor']
    

    #print("data = ", request.GET('data'))

    conveniosS = []

    
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()
   
    detalle = 'select convSum.id sumId, conv.id id, convSum."codigoHomologado" codigoHomologado, convSum.valor valor,  convSum.suministro_id suministroId ,exa.nombre suministroNombre, tipostar.nombre tarifa FROM contratacion_convenios conv , contratacion_conveniossuministros convSum, tarifarios_tipostarifa tipostar, facturacion_suministros exa WHERE conv.id = convSum.convenio_id and convSum."tipoTarifa_id" = tipostar.id and convSum.suministro_id = exa.id and conv.id = ' + "'" + str(convenioId) + "'"

    print(detalle)

    curx.execute(detalle)

    conveniosS = []

    for sumId , id, codigoHomologado, valor,  suministroId ,suministroNombre,tarifa in curx.fetchall():
            conveniosS.append(
                {"model": "conveniosS.conveniosS", "pk": sumId, "fields":
                  {"sumId":sumId, "id": id,
                     "codigoHomologado": codigoHomologado,
                     "valor": valor,
                     "suministroId": suministroId, "suministroNombre": suministroNombre,
                     "tarifa": tarifa }})

    miConexionx.close()
    print(conveniosS)

    context['ConveniosS'] = conveniosS


    serialized1 = json.dumps(conveniosS, default=decimal_serializer)


    return HttpResponse(serialized1, content_type='application/json')


def GuardarConveniosSuministros( request):

    if request.method == 'POST':

        codigoHomologado = request.POST["codigoHomologado"]
        tiposTarifa = request.POST["tiposTarifa"]
        suministro = request.POST["sum"]
        valor = request.POST["valor"]
        convenioId = request.POST["convenioId"]
        conceptos = request.POST["conceptos"]
     
        if tiposTarifa == '':
           tiposTarifa="null"

        if suministro == '':
            cups ="null"


        estadoReg= 'A'
        username_id = request.POST["username_id"]
        fechaRegistro = datetime.datetime.now()

        miConexion3 = None
        try:

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
            curt = miConexiont.cursor()
            comando = 'INSERT INTO contratacion_conveniossuministros ("codigoHomologado", valor, "fechaRegistro", "estadoReg", convenio_id, suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) values (' + "'" + str(codigoHomologado) + "'," + "'" + str(valor) + "'," + "'" + str(fechaRegistro) +"'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + "'" + str(suministro) + "'," + "'" + str(tiposTarifa) + "'," + "'" + str(username_id) + "',"  + str(conceptos) + ")"
            print(comando)
            curt.execute(comando)

            miConexiont.commit()
            curt.close()
            miConexiont.close()

            return JsonResponse({'success': True, 'Mensajes': 'Tarifa de convenio suministro Creada satisfactoriamente!'})

        except psycopg2.DatabaseError as error:
            print ("Entre por rollback" , error)
            if miConexiont:
                print("Entro ha hacer el Rollback")
                miConexiont.rollback()
            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})
        

        finally:
            if miConexiont:
                curt.close()
                miConexiont.close()



def GrabarSuministro( request):

    print ("Entre Grabar Suministro")


    if request.method == 'POST':

        convenioId=request.POST["convenioId1"]
        print("convenioId = " , convenioId)
        tiposTarifa=request.POST["tiposTarifa"]
        print("tiposTarifa = ", tiposTarifa)
        conceptos=request.POST["conceptos"]
        print("conceptos = ", conceptos)
        porcentage=request.POST["porcentage"]
        print("porcentage = ", porcentage)
        valorVariacion=request.POST["valorVariacion"]
        print("valorVariacion = ", valorVariacion)
        estadoReg= 'A'
        username_id = request.POST["username_id"]
        fechaRegistro = timezone.now()
        #fechaRegistro = datetime.datetime.now()

        accion = request.POST["accion"]

        miConexion3 = None
        try:

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
                curt = miConexiont.cursor()

                if (accion == 'Crear' and porcentage != 0 and conceptos == '' and valorVariacion == '0' ):
                    print("Entre1")
                    comando = 'INSERT INTO contratacion_conveniosSuministros ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), '  + str(tiposTarifa) + "," + "'" +  str(username_id) + "'" +  ', concepto_id from tarifarios_tarifassuministros where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


                if (accion == 'Crear' and porcentage != 0 and conceptos != '' and valorVariacion == '0'):
                    print("Entre2")
                    comando = 'INSERT INTO contratacion_conveniosSuministros ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), ' +"'"  + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id from tarifarios_tarifassuministros where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"


                if (accion == 'Crear' and porcentage == '0'  and conceptos == '' and valorVariacion != '0'):
                    print("Entre3")
                    comando = 'INSERT INTO contratacion_conveniosSuministros ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round( ' + "'" + str(valorVariacion) + "')" + ' subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) +  "'," + ' cast(suministro_id as numeric), '   +"'" + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id from tarifarios_tarifassuministros where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


                if (accion == 'Crear' and porcentage == '0'  and conceptos != '' and valorVariacion !='0'):
                    print("Entre4")
                    comando = 'INSERT INTO contratacion_conveniosSuministros ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round( ' + "'" + str(valorVariacion) + "')" + ' subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), '  +"'"  + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id from tarifarios_tarifassuministros where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"


                if (accion == 'Borrar' and conceptos == '' and valorVariacion == '0' ):
                    print("Entre11")
                    comando = 'DELETE FROM contratacion_conveniosSuministros  where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


                if (accion == 'Borrar' and conceptos != '' and valorVariacion == '0'):
                    print("Entre12")
                    comando = 'DELETE FROM contratacion_conveniosSuministros where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"


                if (accion == 'Borrar' and conceptos == '' and valorVariacion != '0'):
                    print("Entre13")
                    comando = 'DELETE FROM contratacion_conveniosSuministros where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' and valor = " + "'" + str(valorVariacion) + "'"


                if (accion == 'Borrar' and conceptos != '' and valorVariacion !='0'):
                    print("Entre14")
                    comando = 'DELETE FROM contratacion_conveniosSuministros where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "' AND valor = " + "'" +str(valorVariacion) + "'"


                print(comando)

                curt.execute(comando)
                miConexiont.commit()
                curt.close()
                miConexiont.close()


                if (accion == 'Crear'):
                    return JsonResponse({'success': True, 'Mensajes': 'Tarifas de convenio suministros actualizadas satisfactoriamente!'})

                if (accion == 'Borrar'):
                    return JsonResponse({'success': True, 'Mensajes': 'Registros borrados satisfactoriamente!'})

        except psycopg2.DatabaseError as error:
            print ("Entre por rollback" , error)
            if miConexiont:
                print("Entro ha hacer el Rollback")
                miConexiont.rollback()
            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})


        finally:
            if miConexiont:
                curt.close()
                miConexiont.close()



def DeleteConveniosSuministros(request):

    print ("Entre DeleteConveniosSuministros" )


    id = request.POST["post_id"]
    print ("el id es = ", id)

    post = ConveniosSuministros.objects.get(id=id)
    post.delete()

    return JsonResponse({'success': True, 'message': 'Registro Borrado !'})


def DeleteConveniosHonorarios(request):

    print ("Entre DeleteConveniosHonorarios" )


    id = request.POST["post_id"]
    print ("el id es = ", id)
    try:
        with transaction.atomic():
            post = ConveniosLiquidacionTarifasHonorarios.objects.get(id=id)
            post.delete()

            return JsonResponse({'success': True, 'Mensajes': 'Registro Borrado !'})
    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)
        message_error= str(e)
        return JsonResponse({'success': False, 'Mensajes': e})


def GrabarHonorarios( request):

    print ("Entre Grabar Honorarios")


    if request.method == 'POST':

        convenioId=request.POST["convenioId1"]
        print("convenioId = " , convenioId)
        tiposTarifa=request.POST["tiposTarifa"]
        print("tiposTarifa = ", tiposTarifa)
        conceptos=request.POST["conceptos"]
        print("conceptos = ", conceptos)
        porcentage=request.POST["porcentage"]
        print("porcentage = ", porcentage)
        valorVariacion=request.POST["valorVariacion"]
        print("valorVariacion = ", valorVariacion)
        honorarios=request.POST["honorarios"]
        print("honorarios = ", honorarios)
        cups=request.POST["cups"]
        print("cups = ", cups)

        estadoReg= 'A'
        username_id = request.POST["username_id"]
        fechaRegistro = timezone.now()
        #fechaRegistro = datetime.datetime.now()

        accion = request.POST["accion"]


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        curt = miConexiont.cursor()

        if (accion == 'Crear' and porcentage != 0 and conceptos == '' and valorVariacion == '0' and honorarios == '' and cups == ''):
            print("Entre1")
            comando = 'INSERT INTO contratacion_ConveniosLiquidacionTarifasHonorarios ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id , "tipoHonorario_id", cups_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), '  + str(tiposTarifa) + "," + "'" +  str(username_id) + "'" +  ', concepto_id , "tipoHonorario_id", "codigoCups_id"  from tarifarios_LiquidacionTarifasHonorarios where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


        if (accion == 'Crear' and porcentage != 0 and conceptos == '' and valorVariacion == '0' and honorarios != '' and cups == ''):
            print("Entre1UNO")
            comando = 'INSERT INTO contratacion_ConveniosLiquidacionTarifasHonorarios ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id, "tipoHonorario_id" , cups_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), '  + str(tiposTarifa) + "," + "'" +  str(username_id) + "'" +  ', concepto_id  , "tipoHonorario_id", "codigoCups_id" from tarifarios_LiquidacionTarifasHonorarios where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'" + ' AND "tipoHonorario_id" = ' + honorarios

        if (accion == 'Crear' and porcentage != 0 and conceptos == '' and valorVariacion == '0' and honorarios != '' and cups != ''):
                print("Entre1DOS")
                comando = 'INSERT INTO contratacion_ConveniosLiquidacionTarifasHonorarios ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id, "tipoHonorario_id" , cups_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), ' + str(tiposTarifa) + "," + "'" + str(username_id) + "'" + ', concepto_id  , "tipoHonorario_id", "codigoCups_id" from tarifarios_LiquidacionTarifasHonorarios where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'" + ' AND "tipoHonorario_id" = ' + honorarios + ' AND "codigoCups_id" = ' + cups

            ## VERIFICAR ESTEP DE ABAJO

        if (accion == 'Crear' and porcentage != 0 and conceptos != '' and valorVariacion == '0'):
                print("Entre2")
                comando = 'INSERT INTO contratacion_ConveniosLiquidacionTarifasHonorarios ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id) select "codigoHomologado", round((+"valor" +"valor"*' + str(porcentage) + '/100)) subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), ' + "'" + str(tiposTarifa) + "'," + "'" + str(username_id) + "'" + ', concepto_id from tarifarios_LiquidacionTarifasHonorarios where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"

                ## es decir por valor
        if (accion == 'Crear' and porcentage == '0'  and conceptos == '' and valorVariacion != '0' and honorarios == '' and cups == ''):
            print("Entre3")
            comando = 'INSERT INTO contratacion_ConveniosLiquidacionTarifasHonorarios ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id, "tipoHonorario_id", cups_id) select "codigoHomologado", round( ' + "'" + str(valorVariacion) + "')" + ' subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) +  "'," + ' cast(suministro_id as numeric), '   +"'" + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id , "tipoHonorario_id", "codigoCups_id"  from tarifarios_LiquidacionTarifasHonorarios where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


        if (accion == 'Crear' and porcentage == '0'  and conceptos != '' and valorVariacion !='0' and honorarios == '' and cups == ''):
            print("Entre4")
            comando = 'INSERT INTO contratacion_ConveniosLiquidacionTarifasHonorarios ("codigoHomologado", valor,  "fechaRegistro", "estadoReg",convenio_id,suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id, "tipoHonorario_id", cups_id) select "codigoHomologado", round( ' + "'" + str(valorVariacion) + "')" + ' subido  ,' + "'" + str(fechaRegistro) + "'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + ' cast(suministro_id as numeric), '  +"'"  + str(tiposTarifa)  + "'," + "'" + str(username_id) + "'" + ', concepto_id , "tipoHonorario_id", "codigoCups_id"  from tarifarios_LiquidacionTarifasHonorarios where "tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"

        if (accion == 'Borrar' and conceptos == '' and valorVariacion == '0' and honorarios == '' and cups == ''):
            print("Entre11")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios  where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "'"


        if (accion == 'Borrar' and conceptos != '' and valorVariacion == '0' and honorarios == '' and cups == ''):
            print("Entre12")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'"

        if (accion == 'Borrar' and conceptos != '' and valorVariacion == '0' and honorarios != '' and cups == ''):
            print("Entre122")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'" + ' AND "tipoHonorario_id" = ' + honorarios


        if (accion == 'Borrar' and conceptos != '' and valorVariacion == '0' and honorarios != '' and cups != ''):
            print("Entre123")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'" + ' AND "tipoHonorario_id" = ' + honorarios + ' AND cups_id = ' + cups

        if (accion == 'Borrar' and conceptos == '' and valorVariacion != '0' and honorarios == '' and cups == ''):
            print("Entre13")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' and valor = " + "'" + str(valorVariacion) + "'"


        if (accion == 'Borrar' and conceptos == '' and valorVariacion != '0' and honorarios != '' and cups == ''):
            print("Entre133")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'" + ' AND "tipoHonorario_id" = ' + honorarios


        if (accion == 'Borrar' and conceptos == '' and valorVariacion != '0' and honorarios != '' and cups != ''):
            print("Entre135")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'" + ' AND "tipoHonorario_id" = ' + honorarios + ' AND cups_id = ' + cups

        if (accion == 'Borrar' and conceptos != '' and valorVariacion !='0' and honorarios != '' and cups != ''):
            print("Entre14")
            comando = 'DELETE FROM contratacion_ConveniosLiquidacionTarifasHonorarios where convenio_id =  ' + "'" + str(convenioId) + "' AND " + '"tipoTarifa_id" = ' + "'" + str(tiposTarifa) + "' AND concepto_id =" + "'" + str(conceptos) + "'" + ' AND "tipoHonorario_id" = ' + honorarios + ' AND cups_id = ' + cups + ' AND concepto_id = "' + conceptos



        try:

            curt.execute(comando)

        except (Exception, psycopg2.DatabaseError) as error:
        	print("Error = " ,error)
        	message_error= str(error)
        	return JsonResponse({'success': False, 'Mensajes': message_error})

        miConexiont.commit()
        miConexiont.close()


        if (accion == 'Crear'):
	        return JsonResponse({'success': True, 'Mensajes': 'Tarifas de convenio suministros actualizadas satisfactoriamente!'})

        if (accion == 'Borrar'):
	        return JsonResponse({'success': True, 'Mensajes': 'Registros borrados satisfactoriamente!'})


# Create your views here.
def load_dataConveniosHonorarios(request, data):
    print ("Entre load_data ConveniosHonorarios")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)

    convenioId = d['valor']
    

    #print("data = ", request.GET('data'))

    conveniosS = []

    
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()
   
    detalle = 'select convHon.id sumId, conv.id id, convHon."codigoHomologado" codigoHomologado, convHon.valor valor,  convHon.suministro_id suministroId ,exa.nombre suministroNombre, tipostar.nombre tarifa FROM contratacion_convenios conv , contratacion_ConveniosLiquidacionTarifasHonorarios convHon, tarifarios_tipostarifa tipostar, facturacion_suministros exa WHERE conv.id = convHon.convenio_id and convHon."tipoTarifa_id" = tipostar.id and convHon.suministro_id = exa.id and conv.id = ' + "'" + str(convenioId) + "'"

    print(detalle)

    curx.execute(detalle)

    conveniosH = []

    for sumId , id, codigoHomologado, valor,  suministroId ,suministroNombre,tarifa in curx.fetchall():
            conveniosH.append(
                {"model": "conveniosS.conveniosS", "pk": sumId, "fields":
                  {"sumId":sumId, "id": id,
                     "codigoHomologado": codigoHomologado,
                     "valor": valor,
                     "suministroId": suministroId, "suministroNombre": suministroNombre,
                     "tarifa": tarifa }})

    miConexionx.close()
    print(conveniosH)

    context['ConveniosH'] = conveniosH


    serialized1 = json.dumps(conveniosH, default=decimal_serializer)


    return HttpResponse(serialized1, content_type='application/json')


def GuardarConveniosHonorarios( request):

    if request.method == 'POST':

        codigoHomologado = request.POST["lcodHomologado"]
        tiposTarifa = request.POST["ltiposTarifa"]
        honorarios = request.POST["llhonorarios"]
        cups = request.POST["llcups"]
        suministro = request.POST["lsum"]
        valor = request.POST["lvalor"]
        conceptos = request.POST["lconceptos"]
        convenioId = request.POST["convenioId"]
        conceptos = request.POST["conceptos"]
        conceptos = request.POST["conceptos"]
        conceptos = request.POST["conceptos"]

     
        if tiposTarifa == '':
           tiposTarifa="null"

        if suministro == '':
            cups ="null"


        estadoReg= 'A'
        username_id = request.POST["username_id"]
        fechaRegistro = timezone.now()
        #fechaRegistro = datetime.datetime.now()

     

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        curt = miConexiont.cursor()
        comando = 'INSERT INTO contratacion_ConveniosLiquidacionTarifasHonorarios ("codigoHomologado", valor, "fechaRegistro", "estadoReg", convenio_id, suministro_id, "tipoTarifa_id", "usuarioRegistro_id", concepto_id, "tipoHonorario_id", cups_id) values (' + "'" + str(codigoHomologado) + "'," + "'" + str(valor) + "'," + "'" + str(fechaRegistro) +"'," + "'" + str(estadoReg) + "'," + "'" + str(convenioId) + "'," + "'" + str(suministro) + "'," + "'" + str(tiposTarifa) + "'," + "'" + str(username_id) + "',"  + str(conceptos) + "," + honorarios + "," + cups + ")"

        print(comando)


        try:
            curt.execute(comando)
        except (Exception, psycopg2.DatabaseError) as error:

            print("Error = " ,error)
            message_error= str(error)
            return JsonResponse({'success': False, 'Mensajes': message_error})

        miConexiont.commit()
        miConexiont.close()

        return JsonResponse({'success': True, 'Mensajes': 'Tarifa Honorario Creada satisfactoriamente!'})


def Load_dataTarifariosProcedimientos1(request, data):
    print ("Entre load_data TarifariosProcedimientos1")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    tarifariosDescripcionProc_id = d['tarifariosDescripcionProc_id']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)
    

    #print("data = ", request.GET('data'))

    entidadColumna = TarifariosDescripcion.objects.get(id=tarifariosDescripcionProc_id)

    tarifariosProcedimientos = []


    
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()


    #detalle = 'select tarproc.id id, tiptar.nombre tipoTarifa, exa."codigoCups" cups, tarproc."codigoHomologado" codigoHomologado, exa.nombre exaNombre, tarproc."colValorBase", tarproc."colValor1", tarproc."colValor2" , tarproc."colValor3"	, tarproc."colValor4"	, tarproc."colValor5"	, tarproc."colValor6"	, tarproc."colValor7"	, tarproc."colValor8"	, tarproc."colValor9" , tarproc."colValor10"from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes, tarifarios_tarifariosprocedimientos tarproc, clinico_examenes exa , contratacion_convenios conv where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id" and tarproc."tiposTarifa_id" = tiptar.id and exa.id = tarproc."codigoCups_id" and tardes.id =' + "'" + str(tarifariosDescripcionProc_id) + "'" + ' and conv."tarifariosDescripcionProc_id" = tardes.id'
    detalle = 'select tarproc.id id, tiptar.nombre tipoTarifa, exa."codigoCups" cups, tarproc."codigoHomologado" codigoHomologado, exa.nombre exaNombre, tarproc."' + str(entidadColumna.columna) + '" valorColumna' +  ' from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes, tarifarios_tarifariosprocedimientos tarproc, clinico_examenes exa , contratacion_convenios conv where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id" and tarproc."tiposTarifa_id" = tiptar.id and exa.id = tarproc."codigoCups_id" and tardes.id =' + "'" + str(tarifariosDescripcionProc_id) + "'" + ' and conv."tarifariosDescripcionProc_id" = tardes.id'


    print(detalle)

    curx.execute(detalle)

    for id, tipoTarifa, cups, codigoHomologado, exanombre, valorColumna  in curx.fetchall():
        tarifariosProcedimientos.append(
		{"model":"tarifarios.tarifariosProcedimientos","pk":id,"fields":
			{'id':id, 'tipoTarifa':tipoTarifa, 'cups':cups, 'codigoHomologado':codigoHomologado, 'exaNombre':exanombre, 'valorColumna':valorColumna}})

    miConexionx.close()
    print(tarifariosProcedimientos)
    #context['Convenios'] = convenios
    #convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    #convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    #convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    #convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})


    serialized1 = json.dumps(tarifariosProcedimientos, default=str)


    return HttpResponse(serialized1, content_type='application/json')



def Load_datatarifariosDescripcionProcedimientos1(request, data):
    print ("Entre load_datatarifariosDescripcionProcedimientos1")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)
    


    tarifariosDescripcionProcedimientos = []


    
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()
   
    detalle = 'select tiptar.id  id,tarprod.nombre tipo, tiptar.nombre tipoTarifa, tardes.columna columna, tardes.descripcion descripcion from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id"  and tarprod.nombre like ('  + "'%PROCE%')" + '  order by tarprod.nombre '

    print(detalle)

    curx.execute(detalle)

    for id, tipo, tipoTarifa, columna, descripcion in curx.fetchall():
        tarifariosDescripcionProcedimientos.append(
		{"model":"tarifarios.tarifariosDescripcion","pk":id,"fields":
			{'id':id, 'tipo': tipo, 'tipoTarifa': tipoTarifa, 'columna': columna, 'descripcion':descripcion }})

    miConexionx.close()
    print(tarifariosDescripcionProcedimientos)
    #context['Convenios'] = convenios
    #convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    #convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    #convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    #convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})


    serialized1 = json.dumps(tarifariosDescripcionProcedimientos, default=str)


    return HttpResponse(serialized1, content_type='application/json')


def Load_dataTarifariosSuministros1(request, data):
    print("Entre load_data TarifariosSuministros1")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    tiposTarifa = d['tiposTarifa_id']

    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)
    print("tiposTarifa:", tiposTarifa)

    tarifariosDescripcionSum_id = d['tarifariosDescripcionSum_id']
    entidadColumna = TarifariosDescripcion.objects.get(id=tarifariosDescripcionSum_id)

    # print("data = ", request.GET('data'))

    tarifariosSuministros = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    #detalle = 'select tarsum.id id, tiptar.nombre tipoTarifa, exa.cums cums, tarsum."codigoHomologado" codigoHomologado, exa.nombre exaNombre, tarsum."colValorBase", tarsum."colValor1", tarsum."colValor2" , tarsum."colValor3"	, tarsum."colValor4"	, tarsum."colValor5"	, tarsum."colValor6"	, tarsum."colValor7"	, tarsum."colValor8"	, tarsum."colValor9" , tarsum."colValor10" from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes, tarifarios_tarifariossuministros tarsum, facturacion_suministros exa where tiptar.id = tardes."tiposTarifa_id" and tarsum."tiposTarifa_id" = tiptar.id and tardes.columna=' + "'" + str('colValorBase') + "'" + ' and exa.id = tarsum."codigoCum_id" and tarsum."tiposTarifa_id" =' + "'" + str(tiposTarifa) + "'" + ' and tarprod.id = tiptar."tiposTarifaProducto_id"'
    detalle = 'select tarsum.id id, tiptar.nombre tipoTarifa, sum.cums cums, tarsum."codigoHomologado" codigoHomologado, sum.nombre exaNombre, tarsum."' + str(entidadColumna.columna) + '" valorColumna' +  ' from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes, tarifarios_tarifariossuministros tarsum, facturacion_suministros sum , contratacion_convenios conv where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id" and tarsum."tiposTarifa_id" = tiptar.id and sum.id = tarsum."codigoCum_id" and tardes.id =' + "'" + str(tarifariosDescripcionSum_id) + "'" + ' and conv."tarifariosDescripcionSum_id" = tardes.id'

    print(detalle)

    curx.execute(detalle)

    for id, tipoTarifa, cums, codigoHomologado, exanombre, valorColumna  in curx.fetchall():
        tarifariosSuministros.append(
            {"model": "tarifarios.tarifariosSuministros", "pk": id, "fields":
                {'id': id, 'tipoTarifa': tipoTarifa, 'cums': cums, 'codigoHomologado': codigoHomologado,
                 'exaNombre': exanombre, 'valorColumna': valorColumna
                 }})

    miConexionx.close()
    print(tarifariosSuministros)
    # context['Convenios'] = convenios
    # convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    # convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    # convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    # convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})

    serialized1 = json.dumps(tarifariosSuministros, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_datatarifariosDescripcionSuministros1(request, data):
    print("Entre load_datatarifariosDescripcionSuministros")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    print("sede:", sede)
    print("username:", username)
    print("username_id:", username_id)

    tarifariosDescripcionSuministros = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select tiptar.id  id,tarprod.nombre tipo, tiptar.nombre tipoTarifa, tardes.columna columna, tardes.descripcion descripcion from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id"  and tarprod.nombre like (' + "'%SUMINI%')" + '  order by tarprod.nombre '

    print(detalle)

    curx.execute(detalle)

    for id, tipo, tipoTarifa, columna, descripcion in curx.fetchall():
        tarifariosDescripcionSuministros.append(
            {"model": "tarifarios.tarifariosDescripcion", "pk": id, "fields":
                {'id': id, 'tipo': tipo, 'tipoTarifa': tipoTarifa, 'columna': columna, 'descripcion': descripcion}})

    miConexionx.close()
    print(tarifariosDescripcionSuministros)
    # context['Convenios'] = convenios
    # convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    # convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    # convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    # convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})

    serialized1 = json.dumps(tarifariosDescripcionSuministros, default=str)

    return HttpResponse(serialized1, content_type='application/json')



