# Create your views here.
from django.shortcuts import render
import json
from django import forms
import cv2
import numpy as np
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.utils import timezone
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
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle, Facturacion, FacturacionDetalle, Conceptos
from cartera.models import TiposPagos, FormasPagos, Pagos, PagosFacturas, Glosas
from triage.models import Triage
from clinico.models import Servicios
from rips.models import RipsTransaccion, RipsUsuarios, RipsEnvios, RipsDetalle, RipsTiposNotas
from tarifarios.models import TiposTarifa, TiposTarifaProducto
import pickle
import io
import pandas as pd
from django.db import transaction, DatabaseError


def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")




def Load_dataTarifariosProcedimientos(request, data):
    print ("Entre load_data TarifariosProcedimientos")

    context = {}
    d = json.loads(data)

    username = d['username']
    sede = d['sede']
    username_id = d['username_id']

    nombreSede = d['nombreSede']
    tiposTarifa = d['tiposTarifa_id']
    print ("sede:", sede)
    print ("username:", username)
    print ("username_id:", username_id)
    

    #print("data = ", request.GET('data'))

    tarifariosProcedimientos = []


    
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()
   
    #detalle = 'select id, "codigoHomologado", "colValorBase", "colValor1", "colValor2", "colValor3", "colValor4", "colValor5", "colValor6", "colValor7", "colValor8", "colValor9", "colValor10", "fechaRegistro", "estadoReg", "codigoCups_id", concepto_id, "tiposTarifa_id", "usuarioRegistro_id" from tarifarios_tarifariosprocedimientos'
    detalle = 'select tarproc.id id, tiptar.nombre tipoTarifa, exa."codigoCups" cups, tarproc."codigoHomologado" codigoHomologado, exa.nombre exaNombre, tarproc."colValorBase", tarproc."colValor1", tarproc."colValor2" , tarproc."colValor3"	, tarproc."colValor4"	, tarproc."colValor5"	, tarproc."colValor6"	, tarproc."colValor7"	, tarproc."colValor8"	, tarproc."colValor9" , tarproc."colValor10" from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes, tarifarios_tarifariosprocedimientos tarproc, clinico_examenes exa where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id" and tarproc."tiposTarifa_id" = tiptar.id and tardes.columna=' + "'" + str('colValorBase') + "'" + ' and exa.id = tarproc."codigoCups_id" and tarproc."tiposTarifa_id" =' + "'" + str(tiposTarifa) + "'"


    print(detalle)

    curx.execute(detalle)

    for id, tipoTarifa, cups, codigoHomologado, exanombre, colValorBase, colValor1, colValor2, colValor3, colValor4, colValor5, colValor6, colValor7, colValor8, colValor9, colValor10  in curx.fetchall():
        tarifariosProcedimientos.append(
		{"model":"tarifarios.tarifariosProcedimientos","pk":id,"fields":
			{'id':id, 'tipoTarifa':tipoTarifa, 'cups':cups, 'codigoHomologado': codigoHomologado, 'exaNombre':exanombre, 'colValorBase': colValorBase, 'colValor1': colValor1, 'colValor2': colValor2,'colValor3': colValor3,'colValor4': colValor4,
			'colValor5': colValor5,'colValor6': colValor6,'colValor7': colValor7,'colValor8': colValor8,'colValor9': colValor9,'colValor10': colValor10
                         }})

    miConexionx.close()
    print(tarifariosProcedimientos)
    #context['Convenios'] = convenios
    #convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    #convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    #convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    #convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})


    serialized1 = json.dumps(tarifariosProcedimientos, default=str)


    return HttpResponse(serialized1, content_type='application/json')



def Load_datatarifariosDescripcionProcedimientos(request, data):
    print ("Entre load_datatarifariosDescripcionProcedimientos")

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
   
    detalle = 'select tardes.id id, tiptar.id  tipTarId,tarprod.nombre tipo, tiptar.nombre tipoTarifa, tardes.columna columna, tardes.descripcion descripcion from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id"  and tarprod.nombre like ('  + "'%PROCE%')" + '  order by tarprod.nombre '

    print(detalle)

    curx.execute(detalle)

    for id, tipo, tipTarId, tipoTarifa, columna, descripcion in curx.fetchall():
        tarifariosDescripcionProcedimientos.append(
		{"model":"tarifarios.tarifariosDescripcion","pk":id,"fields":
			{'id':id, 'tipTarId':tipTarId, 'tipo': tipo, 'tipoTarifa': tipoTarifa, 'columna': columna, 'descripcion':descripcion }})

    miConexionx.close()
    print(tarifariosDescripcionProcedimientos)
    #context['Convenios'] = convenios
    #convenios.append({"model":"empresas.empresas","pk":id,"fields":{'Empresas':empresas}})
    #convenios.append({"model":"tiposTarifa.tiposTarifa","pk":id,"fields":{'TiposTarifa':tiposTarifa}})
    #convenios.append({"model":"cups.cups","pk":id,"fields":{'Cups':cups}})
    #convenios.append({"model":"conceptos.conceptos","pk":id,"fields":{'Conceptos':conceptos}})


    serialized1 = json.dumps(tarifariosDescripcionProcedimientos, default=str)


    return HttpResponse(serialized1, content_type='application/json')


def GuardarDescripcionProcedimientos(request):

    print ("Entre GuardarDescripcionProcedimientos" )

    tiposTarifa_id = request.POST.get('tiposTarifa_id')
    print ("tiposTarifa_id =", tiposTarifa_id)

    columna = request.POST["columna"]
    print ("columna =", columna)

    descripcion = request.POST["descripcion"]
    print ("descripcion =", descripcion)

    serviciosAdministrativos = request.POST["serviciosAdministrativos"]
    print ("serviciosAdministrativos =", serviciosAdministrativos)

    if serviciosAdministrativos == '':
        serviciosAdministrativos = "null"


    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO tarifarios_tarifariosDescripcion (columna, descripcion, "fechaRegistro", "estadoReg", "tiposTarifa_id","serviciosAdministrativos_id") VALUES (' + "'" + str(columna) + "'," +   "'" + str(descripcion) + "',"  "'" + str(fechaRegistro) + "',"  "'" + str(estadoReg) + "',"  "'" + str(tiposTarifa_id) + "'," + str(serviciosAdministrativos) + ")"

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Tarifario Descripcon Procedimientos Actualizado!'})

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

def CrearTarifarioProcedimientos(request):

    print ("Entre CrearTarifarioProcedimientos" )

    tiposTarifa_id = request.POST.get('tiposTarifa_id')
    print ("tiposTarifa_id =", tiposTarifa_id)

    username_id = request.POST.get('username_id')
    print ("username_id =", username_id)
    serviciosAdministrativos_id = request.POST.get('serviciosAdministrativosC_id')
    print ("serviciosAdministrativos_id =", serviciosAdministrativos_id)

    if serviciosAdministrativos_id == '':
        serviciosAdministrativos_id = "null"

    rutaArchivo = request.POST.get('rutaArchivo')
    print ("rutaArchivo =", rutaArchivo)

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    conceptoId =  Conceptos.objects.get(nombre='PROCEDIMIENTOS NO QX')
    productoId = TiposTarifaProducto.objects.get(nombre='PROCEDIMIENTOS')
    descripcion = TiposTarifa.objects.get(id=tiposTarifa_id ,tiposTarifaProducto_id=productoId.id)

    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()

            comando = 'INSERT INTO tarifarios_tarifariosDescripcion (columna, descripcion, "fechaRegistro", "estadoReg", "tiposTarifa_id","serviciosAdministrativos_id") VALUES (' + "'" + str(
                'colValorBase') + "'," + "'" + str(descripcion.nombre) + "',"  "'" + str(fechaRegistro) + "',"  "'" + str(
                estadoReg) + "','" + str(descripcion.id) + "'," + str(serviciosAdministrativos_id) + ')'

            print(comando)
            cur3.execute(comando)


            # Aqui Rutina carga archivo Excel

            #archivo_excel = 'c:\\Entornospython\\Pos7Particionado\\vulner\\JSONCLINICA\\CargaProcedimientos\\datos1.xlsx'
            #archivo_excel = rutaArchivo + '\\particular.xlsx'
	    ## Va con en xlsx
            archivo_excel = rutaArchivo 

            df = pd.read_excel(archivo_excel)

            print("ya lei el dataframe")

            # Crear una sentencia INSERT (ajustar según la estructura de la tabla)

            #try:
            for index, row in df.iterrows():
                    query = 'INSERT INTO tarifarios_tarifariosprocedimientos ("codigoHomologado", "colValorBase", "fechaRegistro", "estadoReg"  ,"codigoCups_id"  ,    "tiposTarifa_id" ,"serviciosAdministrativos_id" ) VALUES (%s, %s,  %s, %s, %s, %s, %s)'
                    valores = (row["codigoHomologado"], row["colValorBase"], row["fechaRegistro"],row["estadoReg"], row["codigoCups_id"] ,   row["tiposTarifa_id"], row["serviciosAdministrativos_id"] )
                    cur3.execute(query, valores)
                    print("pase")

            # Cerrar la conexión
            print("voy a GUARDAR")
            miConexion3.commit()
            cur3.close()
            miConexion3.close()
            return JsonResponse({'success': True, 'Mensajes': 'Tarifario Sabana creado !'})

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


def CrearItemTarifario(request):

    print ("Entre Crear Item Tarifario" )

    codigoHomologadoItem = request.POST.get('codigoHomologadoItem')
    print ("codigoHomologadoItem =", codigoHomologadoItem)

    tiposTarifaItem_id = request.POST.get('tiposTarifaItem_id')
    print ("tiposTarifaItem_id =", tiposTarifaItem_id)

    codigoCupsItem_id = request.POST.get('codigoCupsItem_id')
    print ("codigoCupsItem_id =", codigoCupsItem_id)

    if (codigoCupsItem_id ==''):
        codigoCupsItem_id='null'


    conceptoId = Conceptos.objects.get(nombre='PROCEDIMIENTOS')

    colValorBaseItem = request.POST.get('colValorBaseItem')
    print ("colValorBaseItem =", colValorBaseItem)

    if (colValorBaseItem ==''):
        colValorBaseItem='null'


    username_id = request.POST.get('username_id')
    print ("username_id =", username_id)

    serviciosAdministrativos_id = request.POST.get('serviciosAdministrativos_id')
    print ("serviciosAdministrativos_id =", serviciosAdministrativos_id)

    if (serviciosAdministrativos_id ==''):
        serviciosAdministrativos_id='null'



    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    conceptoId =  Conceptos.objects.get(nombre='PROCEDIMIENTOS')

    miConexion3 = None
    try:
        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO tarifarios_tarifariosprocedimientos ("codigoHomologado", "colValorBase", "fechaRegistro", "estadoReg", "codigoCups_id", concepto_id , "tiposTarifa_id", "usuarioRegistro_id","serviciosAdministrativos_id") VALUES ( ' + "'" + str(codigoHomologadoItem) + "'," + str( colValorBaseItem) + ","  + "'" + str( fechaRegistro) + "'," + "'" + str( estadoReg) + "'," + "'" + str( codigoCupsItem_id) + "'," + "'" + str( conceptoId.id) + "',"  + "'" + str( tiposTarifaItem_id) + "'," + "'" + str( username_id) + "'," + str(serviciosAdministrativos_id) + ")"

        print(comando)

        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()
        return JsonResponse({'success': True, 'Mensajes': 'Item Tarifario creado !'})

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


def AplicarTarifas(request):

    print ("Entre AplicarTarifas" )

    post_id = request.POST.get('post_idProcedimientosDesc')
    print ("post_id =", post_id)

    tiposTarifaTarifario_id = request.POST.get('tiposTarifaTarifario_id')
    print ("tiposTarifaTarifario_id =", tiposTarifaTarifario_id)

    descripcionTarifario = request.POST.get('descripcionTarifario')
    print ("descripcionTarifario =", descripcionTarifario)

    tiposTarifaProducto = TiposTarifaProducto.objects.get(nombre='PROCEDIMIENTOS')

    tipoTarifario = TiposTarifa.objects.get(nombre=tiposTarifaTarifario_id , tiposTarifaProducto_id = tiposTarifaProducto.id)

    porcentaje = request.POST.get('porcentaje')
    print ("porcentaje =", porcentaje)

    valorAplicar = request.POST.get('valorAplicar')
    print ("valorAplicar =", valorAplicar)

    columnaAplicar = request.POST.get('columnaAplicar')
    print ("columnaAplicar =", columnaAplicar)

    serviciosAdministrativosO = request.POST.get('serviciosAdministrativosO')
    print ("serviciosAdministrativosO =", serviciosAdministrativosO)

    if (serviciosAdministrativosO ==''):
        serviciosAdministrativosO='null'

    codigoCups_id = request.POST.get('codigoCups_id')
    print ("codigoCups_id =", codigoCups_id)

    if (codigoCups_id ==''):
        codigoCups_id='null'

    if (valorAplicar == ''):
        valorAplicar = 'null'

    if (porcentaje == ''):
        porcentaje = 'null'

    codigoCupsHasta_id = request.POST.get('codigoCupsHasta_id')
    print ("codigoCupsHasta_id =", codigoCupsHasta_id)

    if (codigoCupsHasta_id == ''):
        codigoCupsHasta_id='null'

    print ("Comenzamos_1")

    estadoReg = 'A'
    print("Comenzamos_2")
    fechaRegistro = timezone.now()

    #conceptoId =  Conceptos.objects.get(nombre='PROCEDIMIENTOS')

    print ("Comenzamos_3")

    if (codigoCups_id != '' and codigoCupsHasta_id != '' and porcentaje !='' ):
        print("Entre porcentaje a Rango de CUPS")
        comando = 'UPDATE tarifarios_tarifariosprocedimientos SET ' + '"' + str(columnaAplicar) + '"'  + ' = "colValorBase" +  "colValorBase" * ' + str(porcentaje) + '/100 WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "'" + ' AND "codigoCups_id" >= ' + "'" + str(codigoCups_id) + "' AND "  + ' "codigoCups_id" <= ' + "'" + str(codigoCupsHasta_id) + "'"

    print ("Comenzamos_4")
    if (codigoCups_id != '' and codigoCupsHasta_id != '' and valorAplicar != ''):
        print("Entre Valor a aplicar  en rango de cups")
        comando = 'UPDATE tarifarios_tarifariosprocedimientos SET ' + '"' + str(columnaAplicar) + '"'  + ' = ' + "'" + str(valorAplicar) + "'"  + '  WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "' AND " + '"codigoCups_id" >= ' + "'" + str(codigoCups_id) + "' AND "  + ' "codigoCups_id" <= ' + "'" + str(codigoCupsHasta_id) + "'"
    print ("Comenzamos_5")
    if ( codigoCups_id == '' and codigoCupsHasta_id == '' and porcentaje != ''):

	    print ("Entre porcentaje Solito")
	    comando = 'UPDATE tarifarios_tarifariosprocedimientos SET ' + '"' + str(columnaAplicar) + '"'  + ' = "colValorBase" +  "colValorBase" * ' + str(porcentaje) + '/100 WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "'"

    print ("Comenzamos_6")
    if (codigoCups_id == '' and codigoCupsHasta_id == '' and valorAplicar != ''):

	    print ("Entre valor a Aplicar Solito");

	    comando = 'UPDATE tarifarios_tarifariosprocedimientos SET ' + '"' + str(columnaAplicar) + '"'  + ' = ' + "'" + str(valorAplicar) + "'" + ',"serviciosAdministrativosO" = ' + str(serviciosAdministrativosO) +  '  WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "'"

    print ("Comenzamos_7")

    miConexion3 = None
    try:
        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",
                                       user="postgres", password="123456")
        cur3 = miConexion3.cursor()

        if ( codigoCups_id == 'null' and codigoCupsHasta_id == 'null' and porcentaje == 'null' and valorAplicar == 'null'):

            print ("no hace nada")


        else:
            print("por aqui nop")
            print(comando)
            cur3.execute(comando)

        print ("a gardar")
        detalle ='UPDATE tarifarios_tarifariosdescripcion set descripcion = ' + "'" + str(descripcionTarifario) + "'," + '"serviciosAdministrativos_id" = ' + "'" + str(serviciosAdministrativosO) + "' wHERE id = " + str(post_id)
        print("detalle = ", detalle)
        cur3.execute(detalle)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Tarifario Sabana creado !'})

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


def GuardarEditarTarifarioProcedimientos(request):

    print ("Entre GuardarEditarTarifarioProcedimientos" )

    post_id = request.POST.get('post_id')
    print ("post_id =", post_id)

    username_id = request.POST.get('username_id')
    print ("username_id =", username_id)

    codigoHomologadoEditar = request.POST.get('codigoHomologadoEditar')
    print ("codigoHomologadoEditar =", codigoHomologadoEditar)

    if (codigoHomologadoEditar == ''):
        codigoHomologadoEditar='null'

    colValorBaseEditar = request.POST.get('colValorBaseEditar')
    print ("colValorBaseEditar =", colValorBaseEditar)

    if (colValorBaseEditar == ''):
        colValorBaseEditar='null'


    colValor1Editar = request.POST.get('colValor1Editar')
    print ("colValor1Editar =", colValor1Editar)

    if (colValor1Editar == ''):
        colValor1Editar='null'

    colValor2Editar = request.POST.get('colValor2Editar')
    print ("colValor2Editar =", colValor2Editar)

    colValor3Editar = request.POST.get('colValor3Editar')
    print ("colValor3Editar =", colValor3Editar)

    colValor4Editar = request.POST.get('colValor4Editar')
    print ("colValor4Editar =", colValor4Editar)

    colValor5Editar = request.POST.get('colValor5Editar')
    print ("colValor5Editar =", colValor5Editar)

    colValor6Editar = request.POST.get('colValor6Editar')
    print ("colValor6Editar =", colValor6Editar)

    colValor7Editar = request.POST.get('colValor7Editar')
    print ("colValor7Editar =", colValor7Editar)

    colValor8Editar = request.POST.get('colValor8Editar')
    print ("colValor8Editar =", colValor8Editar)

    colValor9Editar = request.POST.get('colValor9Editar')
    print ("colValor9Editar =", colValor9Editar)

    colValor10Editar = request.POST.get('colValor10Editar')
    print ("colValor10Editar =", colValor10Editar)

    if (colValor2Editar == ''):
        colValor2Editar='null'

    if (colValor3Editar == ''):
        colValor3Editar='null'

    if (colValor4Editar == ''):
        colValor4Editar='null'

    if (colValor5Editar == ''):
        colValor5Editar='null'

    if (colValor6Editar == ''):
        colValor6Editar='null'

    if (colValor7Editar == ''):
        colValor7Editar='null'

    if (colValor8Editar == ''):
        colValor8Editar='null'

    if (colValor9Editar == ''):
        colValor9Editar='null'

    if (colValor10Editar == ''):
        colValor10Editar='null'

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    conceptoId =  Conceptos.objects.get(nombre='PROCEDIMIENTOS')


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE tarifarios_tarifariosprocedimientos SET "codigoHomologado" =' + "'" + str(codigoHomologadoEditar ) + "'" +  ', "colValorBase" =' + str(colValorBaseEditar ) + ',"colValor1" =' + str(colValor1Editar ) + "," + '"colValor2" =' + str(colValor2Editar )  + ', "colValor3" ='  + str(colValor3Editar )  + ',"colValor4" =' + str(colValor4Editar )  + ',"colValor5" =' + str(colValor5Editar )  + ',"colValor6" =' + str(colValor6Editar ) + ',"colValor7" =' + str(colValor7Editar ) + ',"colValor8" =' + str(colValor8Editar )  + ',"colValor9" =' + str(colValor9Editar )  + ',"colValor10" =' + str(colValor10Editar )  + ',"usuarioRegistro_id" =' + "'" + str(username_id ) + "'" + '  WHERE id=  ' + "'" + str(post_id) + "'"

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Tarifario Actualizado !'})

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



def TraerTarifarioProcedimientos(request):
    print("Entre TraerTarifarioProcedimientos")

    post_id = request.POST.get('post_id')
    print("post_id =", post_id)

    tarifariosProcedimientosDetalle = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    comando = 'select proc.id, "codigoHomologado", "colValorBase", "colValor1", "colValor2", "colValor3", "colValor4", "colValor5", "colValor6", "colValor7", "colValor8", "colValor9", "colValor10", proc."fechaRegistro", proc."estadoReg", "codigoCups_id", exa.nombre exaNombre, exa."codigoCups" codigoCups, proc.concepto_id, "tiposTarifa_id", proc."usuarioRegistro_id" FROM tarifarios_tarifariosprocedimientos proc, clinico_examenes exa WHERE proc.id = ' + "'" + str(post_id) + "'" + ' and exa.id = "codigoCups_id" '

    print(comando)
    cur3.execute(comando)

    for id, codigoHomologado, colValorBase, colValor1, colValor2 , colValor3, colValor4, colValor5, colValor6 , colValor7 ,colValor8,colValor9, colValor10 ,fechaRegistro , estadoReg , codigoCups_id, exaNombre, codigoCups,  concepto_id, tiposTarifa_id, usuarioRegistro_id  in cur3.fetchall():
        tarifariosProcedimientosDetalle.append(
            {"model": "tarifarios.tarifariosProcedimientos", "pk": id, "fields":
                {'id': id, 'codigoHomologado': codigoHomologado, 'colValorBase': colValorBase, 'colValor1': colValor1, 'colValor2': colValor2
                    , 'colValor3': colValor3, 'colValor4': colValor4, 'colValor5': colValor5, 'colValor6': colValor6, 'colValor7': colValor7
                    , 'colValor8': colValor8, 'colValor9': colValor9, 'colValor10': colValor10, 'fechaRegistro': fechaRegistro, 'estadoReg': estadoReg,
                 'codigoCups_id': codigoCups_id,'exaNombre':exaNombre, 'codigoCups':codigoCups,    'concepto_id': concepto_id,'tiposTarifa_id': tiposTarifa_id,'usuarioRegistro_id': usuarioRegistro_id,

                 }})

    miConexion3.close()
    print(tarifariosProcedimientosDetalle)

    serialized1 = json.dumps(tarifariosProcedimientosDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')




    return JsonResponse({'success': True, 'message': 'Tarifario Sabana creado !'})


def Load_dataTarifariosSuministros(request, data):
    print("Entre load_data TarifariosSuministros")

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


    # print("data = ", request.GET('data'))

    tarifariosSuministros = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'select tarsum.id id, tiptar.nombre tipoTarifa, exa.cums cums, tarsum."codigoHomologado" codigoHomologado, exa.nombre exaNombre, tarsum."colValorBase", tarsum."colValor1", tarsum."colValor2" , tarsum."colValor3"	, tarsum."colValor4"	, tarsum."colValor5"	, tarsum."colValor6"	, tarsum."colValor7"	, tarsum."colValor8"	, tarsum."colValor9" , tarsum."colValor10" from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes, tarifarios_tarifariossuministros tarsum, facturacion_suministros exa where tiptar.id = tardes."tiposTarifa_id" and tarsum."tiposTarifa_id" = tiptar.id and tardes.columna=' + "'" + str('colValorBase') + "'" + ' and exa.id = tarsum."codigoCum_id" and tarsum."tiposTarifa_id" =' + "'" + str(tiposTarifa) + "'" + ' and tarprod.id = tiptar."tiposTarifaProducto_id"'

    print(detalle)

    curx.execute(detalle)

    for id, tipoTarifa, cums, codigoHomologado, exanombre, colValorBase, colValor1, colValor2, colValor3, colValor4, colValor5, colValor6, colValor7, colValor8, colValor9, colValor10 in curx.fetchall():
        tarifariosSuministros.append(
            {"model": "tarifarios.tarifariosSuministros", "pk": id, "fields":
                {'id': id, 'tipoTarifa': tipoTarifa, 'cums': cums, 'codigoHomologado': codigoHomologado,
                 'exaNombre': exanombre, 'colValorBase': colValorBase, 'colValor1': colValor1, 'colValor2': colValor2,
                 'colValor3': colValor3, 'colValor4': colValor4,
                 'colValor5': colValor5, 'colValor6': colValor6, 'colValor7': colValor7, 'colValor8': colValor8,
                 'colValor9': colValor9, 'colValor10': colValor10
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


def Load_datatarifariosDescripcionSuministros(request, data):
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

def CrearTarifarioSuministros(request):

    print ("Entre CrearTarifariSuministros" )

    tiposTarifa_id = request.POST.get('tiposTarifa_id')
    print ("tiposTarifa_id =", tiposTarifa_id)

    serviciosAdministrativos_id = request.POST.get('serviciosAdministrativos_id')
    print ("serviciosAdministrativos_id =", serviciosAdministrativos_id)

    if (serviciosAdministrativos_id == ''):
        serviciosAdministrativos_id = 'null'

    rutaArchivo = request.POST.get('rutaArchivoSuministros')
    print ("rutaArchivo =", rutaArchivo)

    username_id = request.POST.get('username_id')
    print ("username_id =", username_id)

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    productoId = TiposTarifaProducto.objects.get(nombre='SUMINISTROS')
    print("productpId = ",productoId )
    print("productpId.id = ", productoId.id)
    descripcion = TiposTarifa.objects.get(id=tiposTarifa_id ,tiposTarifaProducto_id=productoId.id)
    print("descripcion = ", descripcion)

    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cur3 = miConexion3.cursor()

            comando = 'INSERT INTO tarifarios_tarifariosDescripcion (columna, descripcion, "fechaRegistro", "estadoReg", "tiposTarifa_id","serviciosAdministrativos_id") VALUES (' + "'" + str(
                'colValorBase') + "'," + "'" + str(descripcion.nombre) + "',"  "'" + str(fechaRegistro) + "',"  "'" + str(
                estadoReg) + "',"  "'" + str(descripcion.id) + "'," + str(serviciosAdministrativos_id) + ")"

            print(comando)
            cur3.execute(comando)
            # Aqui Rutina carga archivo Excel

            #archivo_excel = 'c:\\Entornospython\\Pos7ParticionadoLienzo\\vulner\\JSONCLINICA\\CargaSuministros\\particular.xlsx'
            #df = pd.read_excel(archivo_excel)

            archivo_excel = rutaArchivo
            df = pd.read_excel(archivo_excel)

            print ("Ya cargue dataFrame")
            # Crear una sentencia INSERT (ajustar según la estructura de la tabla)

            #try:

            print("Voy a leer la data:")
            for index, row in df.iterrows():
                    query = 'INSERT INTO tarifarios_tarifariossuministros ("codigoHomologado", "colValorBase", "fechaRegistro", "estadoReg"  ,"codigoCum_id"  ,  "tiposTarifa_id"  ) VALUES (%s, %s, %s, %s, %s, %s)'
                    valores = (row["codigoHomologado"], row["colValorBase"], row["fechaRegistro"],row["estadoReg"], row["codigoCum_id"] ,   row["tiposTarifa_id"] )
                    cur3.execute(query, valores)

            #except DatabaseError as e:
            #    transaction.rollback()

            # Guardar y Cerrar la conexión
            miConexion3.commit()
            cur3.close()
            miConexion3.close()
            return JsonResponse({'success': True, 'Mensajes': 'Tarifario Sabana Suministros creado !'})


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


def Load_datatarifariosDescripcionSuministros(request, data):
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

    detalle = 'select tiptar.id  id,tarprod.nombre tipo, tiptar.nombre tipoTarifa, tardes.columna columna, tardes.descripcion descripcion from tarifarios_tipostarifaProducto tarprod, tarifarios_tipostarifa tiptar, tarifarios_TarifariosDescripcion tardes where tarprod.id = tiptar."tiposTarifaProducto_id" and tiptar.id = tardes."tiposTarifa_id"  and tarprod.nombre like (' + "'%SUMI%')" + '  order by tarprod.nombre '

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

def GuardarDescripcionSuministros(request):

    print ("Entre GuardarDescripcionuministros" )

    tiposTarifa_id = request.POST.get('tiposTarifa_id')
    print ("tiposTarifa_id =", tiposTarifa_id)

    columna = request.POST["columna"]
    print ("columna =", columna)

    descripcion = request.POST["descripcion"]
    print ("descripcion =", descripcion)

    serviciosAdministrativos_id = request.POST["serviciosAdministrativosS"]
    print ("serviciosAdministrativos_id =", serviciosAdministrativos_id)


    if serviciosAdministrativos_id == '':
        serviciosAdministrativos_id = "null"


    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()


    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
    cur3 = miConexion3.cursor()

    comando = 'INSERT INTO tarifarios_tarifariosDescripcion (columna, descripcion, "fechaRegistro", "estadoReg", "tiposTarifa_id", "serviciosAdministrativos_id" ) VALUES (' + "'" + str(columna) + "'," +   "'" + str(descripcion) + "',"  "'" + str(fechaRegistro) + "',"  "'" + str(estadoReg) + "',"  "'" + str(tiposTarifa_id) + "'," + str(serviciosAdministrativos_id)  + "')"

    print(comando)
    cur3.execute(comando)
    miConexion3.commit()
    miConexion3.close()

    return JsonResponse({'success': True, 'message': 'Tarifario Descripcon Suministros Actualizado!'})


def AplicarTarifasSuministros(request):

    print ("Entre AplicarTarifas Suministros" )

    post_id = request.POST.get('post_id')
    print ("post_id =", post_id)

    tiposTarifaTarifario_id = request.POST.get('tiposTarifaTarifario_id')
    print ("tiposTarifaTarifario_id =", tiposTarifaTarifario_id)

    tiposTarifaProducto = TiposTarifaProducto.objects.get(nombre='SUMINISTROS')

    tipoTarifario = TiposTarifa.objects.get(nombre=tiposTarifaTarifario_id , tiposTarifaProducto_id = tiposTarifaProducto.id)

    porcentaje = request.POST.get('porcentaje')
    print ("porcentaje =", porcentaje)

    valorAplicar = request.POST.get('valorAplicar')
    print ("valorAplicar =", valorAplicar)

    columnaAplicar = request.POST.get('columnaAplicar')
    print ("columnaAplicar =", columnaAplicar)

    codigoCums_id = request.POST.get('codigoCums_id')
    print ("codigoCums_id =", codigoCums_id)

    if (codigoCums_id ==''):
        pass
        #codigoCums_id='null'

    codigoCumsHasta_id = request.POST.get('codigoCumsHasta_id')
    print ("codigoCumsHasta_id =", codigoCumsHasta_id)

    if (codigoCumsHasta_id ==''):
        pass
        #codigoCumsHasta_id='null'

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    conceptoId =  Conceptos.objects.get(nombre='MEDICAMENTOS')


    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            cur3 = miConexion3.cursor()

            print ("Comenzamos")

            if (codigoCums_id != '' and codigoCumsHasta_id != '' and porcentaje !='' ):

                print("Entre porcentaje a Rango de CUMS")
                comando = 'UPDATE tarifarios_tarifariossuministros SET ' + '"' + str(columnaAplicar) + '"'  + ' = "colValorBase" +  "colValorBase" * ' + str(porcentaje) + '/100 WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "'" + ' AND "codigoCum_id" >= ' + str(codigoCums_id) + " AND "  + ' "codigoCum_id" <= ' +  str(codigoCumsHasta_id)
            if (codigoCums_id != '' and codigoCumsHasta_id != '' and valorAplicar != ''):

                print("Entre Valor a aplicar  en rango de cums")
                comando = 'UPDATE tarifarios_tarifariossuministros SET ' + '"' + str(columnaAplicar) + '"'  + ' = ' + "'" + str(valorAplicar) + "'"  + '  WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "' AND " + '"codigoCum_id" >= ' + str(codigoCums_id) + " AND "  + ' "codigoCum_id" <= '  + str(codigoCumsHasta_id)

            if ( codigoCums_id == '' and codigoCumsHasta_id == '' and porcentaje != ''):

                print ("Entre porcentaje Solito")
                comando = 'UPDATE tarifarios_tarifariossuministros SET ' + '"' + str(columnaAplicar) + '"'  + ' = "colValorBase" +  "colValorBase" * ' + str(porcentaje) + '/100 WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "'"


            if (codigoCums_id == '' and codigoCumsHasta_id == '' and valorAplicar != ''):

                print ("Entre valor a Aplicar Solito");

                comando = 'UPDATE tarifarios_tarifariossuministros SET ' + '"' + str(columnaAplicar) + '"'  + ' = ' + "'" + str(valorAplicar) + "'"  + '  WHERE "tiposTarifa_id" = ' + "'" + str(tipoTarifario.id) + "'"

            print(comando)
            cur3.execute(comando)

            return JsonResponse({'success': True, 'Mensajes': 'Tarifario Suministro Actualizado !'})

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


def CrearItemTarifarioSuministros(request):

    print ("Entre Crear Item Tarifario Suministros" )

    codigoHomologadoItem = request.POST.get('codigoHomologadoItem')
    print ("codigoHomologadoItem =", codigoHomologadoItem)

    tiposTarifaItem_id = request.POST.get('tiposTarifaItem_id')
    print ("tiposTarifaItem_id =", tiposTarifaItem_id)

    codigoCumsItem_id = request.POST.get('codigoCumsItem_id')
    print ("codigoCumsItem_id =", codigoCumsItem_id)

    conceptoId = Conceptos.objects.get(nombre='MEDICAMENTOS')

    colValorBaseItem = request.POST.get('colValorBaseItem')
    print ("colValorBaseItem =", colValorBaseItem)

    username_id = request.POST.get('username_id')
    print ("username_id =", username_id)

    serviciosAdministrativos_id = request.POST.get('serviciosAdministrativos_id')
    print ("serviciosAdministrativos_id =", serviciosAdministrativos_id)

    if (serviciosAdministrativos_id == ''):
        serviciosAdministrativos_id = 'null'



    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    conceptoId =  Conceptos.objects.get(nombre='PROCEDIMIENTOS')

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'INSERT INTO tarifarios_tarifariossuministros ("codigoHomologado", "colValorBase", "fechaRegistro", "estadoReg", "codigoCum_id", concepto_id , "tiposTarifa_id", "usuarioRegistro_id","serviciosAdministrativos_id") VALUES ( ' + "'" + str(codigoHomologadoItem) + "'," + "'" + str( colValorBaseItem) + "',"  + "'" + str( fechaRegistro) + "'," + "'" + str( estadoReg) + "'," + "'" + str( codigoCumsItem_id) + "'," + "'" + str( conceptoId.id) + "',"  + "'" + str( tiposTarifaItem_id) + "'," + "'" + str( username_id) + "'," + str(serviciosAdministrativos_id)   + ")"

        print(comando)

        #try:
        cur3.execute(comando)
        #except psycopg2.Error as e:
            # get error code
            #error = e.pgcode
            #print ("Entre Error Base de datos" ,  error)
            #transaction.rollback()
            #miConexion3.close()
            #message_error= str(error)
            #return JsonResponse({'success': False, 'Mensajes': message_error})
            #return JsonResponse({'success': True, 'message': 'Tarifa Suministro existente !'})

        miConexion3.commit()
        cur3.close()
        miConexion3.close()



        return JsonResponse({'success': True, 'Mensajes': 'Item Tarifario Suministro creado !'})

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

def GuardarEditarTarifarioSuministros(request):

    print ("Entre GuardarEditarTarifarioSuministros" )

    post_id = request.POST.get('post_id')
    print ("post_id =", post_id)

    username_id = request.POST.get('username_id')
    print ("username_id =", username_id)

    codigoHomologadoEditar = request.POST.get('codigoHomologadoEditar')
    print ("codigoHomologadoEditar =", codigoHomologadoEditar)

    if (codigoHomologadoEditar == ''):
        codigoHomologadoEditar='null'

    colValorBaseEditar = request.POST.get('colValorBaseEditar')
    print ("colValorBaseEditar =", colValorBaseEditar)

    if (colValorBaseEditar == ''):
        colValorBaseEditar='null'


    colValor1Editar = request.POST.get('colValor1Editar')
    print ("colValor1Editar =", colValor1Editar)

    if (colValor1Editar == ''):
        colValor1Editar='null'

    colValor2Editar = request.POST.get('colValor2Editar')
    print ("colValor2Editar =", colValor2Editar)

    colValor3Editar = request.POST.get('colValor3Editar')
    print ("colValor3Editar =", colValor3Editar)

    colValor4Editar = request.POST.get('colValor4Editar')
    print ("colValor4Editar =", colValor4Editar)

    colValor5Editar = request.POST.get('colValor5Editar')
    print ("colValor5Editar =", colValor5Editar)

    colValor6Editar = request.POST.get('colValor6Editar')
    print ("colValor6Editar =", colValor6Editar)

    colValor7Editar = request.POST.get('colValor7Editar')
    print ("colValor7Editar =", colValor7Editar)

    colValor8Editar = request.POST.get('colValor8Editar')
    print ("colValor8Editar =", colValor8Editar)

    colValor9Editar = request.POST.get('colValor9Editar')
    print ("colValor9Editar =", colValor9Editar)

    colValor10Editar = request.POST.get('colValor10Editar')
    print ("colValor10Editar =", colValor10Editar)

    if (colValor2Editar == ''):
        colValor2Editar='null'

    if (colValor3Editar == ''):
        colValor3Editar='null'

    if (colValor4Editar == ''):
        colValor4Editar='null'

    if (colValor5Editar == ''):
        colValor5Editar='null'

    if (colValor6Editar == ''):
        colValor6Editar='null'

    if (colValor7Editar == ''):
        colValor7Editar='null'

    if (colValor8Editar == ''):
        colValor8Editar='null'

    if (colValor9Editar == ''):
        colValor9Editar='null'

    if (colValor10Editar == ''):
        colValor10Editar='null'

    estadoReg = 'A'
    fechaRegistro = datetime.datetime.now()

    conceptoId =  Conceptos.objects.get(nombre='PROCEDIMIENTOS')

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
        cur3 = miConexion3.cursor()

        comando = 'UPDATE tarifarios_tarifariossuministros SET "codigoHomologado" =' + str(codigoHomologadoEditar ) +  ', "colValorBase" =' + str(colValorBaseEditar ) + ',"colValor1" =' + str(colValor1Editar ) + "," + '"colValor2" =' + str(colValor2Editar )  + ', "colValor3" ='  + str(colValor3Editar )  + ',"colValor4" =' + str(colValor4Editar )  + ',"colValor5" =' + str(colValor5Editar )  + ',"colValor6" =' + str(colValor6Editar ) + ',"colValor7" =' + str(colValor7Editar ) + ',"colValor8" =' + str(colValor8Editar )  + ',"colValor9" =' + str(colValor9Editar )  + ',"colValor10" =' + str(colValor10Editar )  + ',"usuarioRegistro_id" =' + "'" + str(username_id ) + "'" + '  WHERE id=  ' + "'" + str(post_id) + "'"

        print(comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensajes': 'Tarifario Actualizado !'})

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

def TraerTarifarioSuministros(request):
    print("Entre TraerTarifarioSuministros")

    post_id = request.POST.get('post_id')
    print("post_id =", post_id)

    tarifariosSuministrosDetalle = []

    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur3 = miConexion3.cursor()

    comando = 'select sum.id, "codigoHomologado", "colValorBase", "colValor1", "colValor2", "colValor3", "colValor4", "colValor5", "colValor6", "colValor7", "colValor8", "colValor9", "colValor10", sum."fechaRegistro", sum."estadoReg", "codigoCum_id", exa.nombre exaNombre, exa.cums codigoCums, sum.concepto_id, "tiposTarifa_id", sum."usuarioRegistro_id" FROM tarifarios_tarifariossuministros sum, facturacion_suministros exa WHERE sum.id = ' + "'" + str(post_id) + "'" + ' and exa.id = "codigoCum_id" '

    print(comando)
    cur3.execute(comando)

    for id, codigoHomologado, colValorBase, colValor1, colValor2 , colValor3, colValor4, colValor5, colValor6 , colValor7 ,colValor8,colValor9, colValor10 ,fechaRegistro , estadoReg , codigoCums_id, exaNombre, codigoCums,  concepto_id, tiposTarifa_id, usuarioRegistro_id  in cur3.fetchall():
        tarifariosSuministrosDetalle.append(
            {"model": "tarifarios.tarifariosSuministros", "pk": id, "fields":
                {'id': id, 'codigoHomologado': codigoHomologado, 'colValorBase': colValorBase, 'colValor1': colValor1, 'colValor2': colValor2
                    , 'colValor3': colValor3, 'colValor4': colValor4, 'colValor5': colValor5, 'colValor6': colValor6, 'colValor7': colValor7
                    , 'colValor8': colValor8, 'colValor9': colValor9, 'colValor10': colValor10, 'fechaRegistro': fechaRegistro, 'estadoReg': estadoReg,
                 'codigoCums_id': codigoCums_id,'exaNombre':exaNombre, 'codigoCums':codigoCums,    'concepto_id': concepto_id,'tiposTarifa_id': tiposTarifa_id,'usuarioRegistro_id': usuarioRegistro_id,

                 }})

    miConexion3.close()
    print(tarifariosSuministrosDetalle)

    serialized1 = json.dumps(tarifariosSuministrosDetalle, default=str)

    return HttpResponse(serialized1, content_type='application/json')
