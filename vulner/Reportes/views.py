from django.shortcuts import render

import psycopg2
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from datetime import datetime
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.db.models.functions import Cast, Coalesce
import numpy  as np
import openpyxl
import  xlwt
import csv
from django.utils.encoding import smart_str
from datetime import datetime
import math

## De Reporteador

import csv as aliascsv
from django.views.generic import ListView, CreateView, TemplateView, View
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet , ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from django.core import serializers
from io import StringIO
from io import BytesIO
import itertools
from random import randint
from statistics import mean
#from datascience import *
from reportlab.platypus import *
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from django.conf import settings
import os
from datetime import datetime
from datetime import date
from reportlab.lib.fonts import addMapping
from reportlab.lib.colors import (
black,
purple,
white,
yellow
)

## Fin Reporteador



# Create your views here.

def menuAcceso(request):
    print ("Ingreso al Menu")
    context = {}

    # Sedes
    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexion.cursor()
    comando = 'SELECT ltrim(codreg_sede), nom_sede FROM public."Administracion_imhotep_sedesreportes" where estadoReg=' +  "'A'"
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede':codreg_sede, 'nom_sede' : nom_sede})
    miConexion.close()

    context['Sedes'] = sedes



    return render(request, "accesoPrincipalAngular.html", context)


def validaAccesoR(request):

    print ("Entre ValidacionR")
    context = {}

    # Sedes
    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexion.cursor()
    comando = 'SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes" where estadoReg=' +  "'A'"
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})
    miConexion.close()

    context['Sedes'] = sedes
    print ("Aqui estan las sedes")
    print (context['Sedes'])

    username = request.POST["username"]

    contrasena = request.POST["password"]

    sedeSeleccionada   = request.POST["seleccion2"]
    print ("sedeSeleccionada = " , sedeSeleccionada)
    print("username = ", username)
    print ("contrasena = ", contrasena)

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada


    # Consigo Nombre de la sede

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexion.cursor()
    #comando = "SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes" WHERE codreg_sede = '" + sedeSeleccionada + "'"
    comando = 'SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes" where estadoReg=' + "'A'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for codreg_sede, nom_sede in cur.fetchall():
        nombreSede.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

    miConexion.close()

    context['NombreSede'] = nombreSede

    # Validacion Usuario existente

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    comando = "SELECT  cod_usuario,   nom_usuario, clave_usuario  FROM imhotep_usuarios WHERE activo='S' and cod_Usuario = '" + username + "'"
    cur.execute(comando)
    print(comando)

    nombreUsuario = []

    for cod_usuario, nom_usuario, clave_usuario in cur.fetchall():
        nombreUsuario.append({'cod_usuario': cod_usuario, 'nom_usuario': nom_usuario, 'clave_usuario' : clave_usuario})

    miConexion.close()

    context['NombreUsuario'] = nombreUsuario

    print ("Asi quedo el nombre del usuario", nombreUsuario)


    if nombreUsuario == []:

        context['Error'] = "Personal invalido y/o No Activo ! "
        print("Entre por personal No encontrado")

        return render(request, "accesoPrincipalAngular.html", context)

    else:
        # Valido contraseña
        if nombreUsuario[0]['clave_usuario'] != contrasena:
            context['Error'] = "Contraseña invalida ! "
            return render(request, "accesoPrincipalAngular.html", context)

        else:
            pass

            # Valido Permiso de ejecucion en la Sede seleccinada
            #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
            miConexion.set_client_encoding('LATIN1')
            cur = miConexion.cursor()
            cur.execute("set client_encoding='LATIN1';")


            comando = 'select usuarios.cod_usuario  as usuario from public."Administracion_mae_repusuarios" usuarios, public."Administracion_imhotep_sedesreportes" sedes where  usuarios.estadoReg =  ' + "'" + 'A' +  "'" + ' and  usuarios.cod_usuario = ' + "'" + username + "'" + ' and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = '  + "'"  + sedeSeleccionada + "'"
            print(comando)
            cur.execute(comando)


            permitido = []

            for usuario in cur.fetchall():
                permitido.append({'usuario': usuario})

            miConexion.close()

            if permitido == []:

                context['Error'] = "Usuario no tiene autorizacion para la sede seleccionada y/o Reportes no asignados ! "
                return render(request, "accesoPrincipalAngular.html", context)

            else:

                print("Paso Autenticacion")

            # Le doy la informacion de los reportes a los que tiene acceso
                #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

            miConexion.set_client_encoding('LATIN1')
            cur = miConexion.cursor()
            cur.execute("set client_encoding='LATIN1';")

            #comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = '  + "'"  + sedeSeleccionada + "'"
            #comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = ' + "'" + sedeSeleccionada + "'" + ' AND usuarios.estadoReg=' +  "'A'"
            comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados ,reportes.mae_gruporeportes_id grupo ,reportes.mae_subgruporeportes_id subgrupo , grupos.nom_grupo nombreGrupo, subgrupos.nom_subgrupo nombreSubgrupo from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes ,public."Administracion_mae_gruporeportes" grupos,public."Administracion_mae_subgruporeportes" subgrupos   where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and grupos.id = reportes.mae_gruporeportes_id and subgrupos.id = reportes.mae_subgruporeportes_id  and sedes.codreg_sede = ' + "'" + sedeSeleccionada + "'" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A'"

            print(comando)
            cur.execute(comando)

            reportesUsuario = []

            for numreporte, usuario, reporte, cuerpo_sql, descripcion, encabezados, grupo, subgrupo, nombreGrupo, nombreSubGrupo in cur.fetchall():
                reportesUsuario.append(
                    {'numreporte': numreporte, 'usuario': usuario, 'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
                     'descripcion': descripcion, 'encabezados':encabezados , 'grupo': grupo, 'subgrupo': subgrupo, 'nombreGrupo': nombreGrupo, 'nombreSubGrupo': nombreSubGrupo    })

            miConexion.close()
            context['ReportesUsuario'] = reportesUsuario



            # Envio los grupos
            #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
            cur = miConexion.cursor()
            comando = 'select  id , grupos.nom_grupo nombreGrupo, grupos.logo logo  from public."Administracion_mae_gruporeportes" grupos order by grupos.id'

            print(comando)
            cur.execute(comando)

            grupos = []

            for id, nombreGrupo, logo in cur.fetchall():
                grupos.append(
                    {'id': id, 'nombreGrupo': nombreGrupo , 'logo':logo})

            miConexion.close()
            context['Grupos'] = grupos


            print("pase0")




    return render(request, "Reportes/PantallaGruposAngular.html", context)



def salir(request):
    print("Voy a salir")

    context = {}
    # Sedes
    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexion.cursor()

    comando = 'SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes"'
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})
    miConexion.close()

    context['Sedes'] = sedes
    print("Aqui estan las sedes")
    print(context['Sedes'])

    return render(request, "accesoPrincipalAngular.html", context)



Story = []
numReporte = 0
nombreReporte = ""
lasColumnas = []
columnas = 0


class Reporte1PdfView(TemplateView):
    print("Entre Reporte1")
    template_name = 'Reportes/ParametrosAngular2.html'
    desdeFecha = '2022-01-01'
    hastaFecha = '2022-01-31'


    def stylesheet():
        styles = {
        "default": ParagraphStyle(
            "default",
            fontName="Times-Roman",
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName="Times-Roman",
            bulletFontSize=10,
            bulletIndent=0,
            textColor=black,
            backColor=None,
            #wordWrap=None,
            wordWrap='LTR',
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,  # "uppercase" | "lowercase" |                 None
            endDots=None,
            splitLongWords=1,
        )}


        return styles


    def myFirstPage(self, canvas, doc):

        global numReporte
        print("Mi primera Pagina")
        canvas.saveState()
        print("Paso canvas")
        canvas.setFont("Helvetica-Bold",9)
        print("Paso canvas1")

        print("Numero de reportes = ", numReporte)

        # cabezote
        #logotipo = "C:\\FONDOCM.jpg"
        logotipo = "{% static '/img/medical1.jpg' %}"

        #imagen = Image(logotipo, 0.6 * inch, 0.6 * inch)

        #imagen.hAlign = 'LEFT'

        fecha = date.today()
        format = fecha.strftime('%d / %m / %Y')
        print(fecha)
        print(format)
        canvas.drawImage( "C:\EntornosPython\pos7Particionado/vulner\static\img/medical1.jpg", 40, 715, width=50,
                     height=50)
        canvas.drawString(250, 750, "CLINICA MEDICAL")
        canvas.drawString(250, 735, 'NIT: 8305077188')
        canvas.drawString(100, 720, "INFORME: ")
        canvas.drawString(150, 720, nombreReporte)
        canvas.drawString(320, 720, "Fecha:")
        canvas.drawString(360, 720, str(format))
        canvas.drawString(520, 720, "Pág: %d " % (doc.page))


        #canvas.drawString(520, 715, "de %d " % (doc.pageCount))

        # Trae Cabezote
        # Ejemplo Tituolo del reporte conexion a BAse de datos, etc

        texto1 = '_________________________________________________________________________________________________________________'
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(30, 670, texto1)

        sonColumnas = range(0, columnas)
        factor = 30

        for i in sonColumnas:
            canvas.drawString(factor, 675, lasColumnas[i])
            factor = factor + 55

        texto1 = '_________________________________________________________________________________________________________________'
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(30, 690, texto1)

        # Fin Cabezote
        pageinfo = "Ejemplo Platypus"
        # canvas.drawString(inch, 0.75 * inch, "Página %d " % (doc.page))
        print ("A restaurar canvas")
        canvas.drawString(200, 20,  "Dirección CALLE 36 SUR 77 33 KENNEDY, BOGOTA")
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        print("Entre myLaterPages")

        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 9)
        desdeFecha = '2022-01-01'
        hastaFecha = '2022-01-01'

        print(desdeFecha)
        print(hastaFecha)

        # Inserto codigo desde cabezote
        #logotipo = "C:\\FONDOCM.jpg"
        logotipo = "{% static '/img/medical1.jpg' %}"
        imagen = Image(logotipo, 0.6 * inch, 0.6 * inch)
        imagen.hAlign = 'LEFT'

        fecha = date.today()
        format = fecha.strftime('%d / %m / %Y')
        print(fecha)
        print(format)
        canvas.drawImage(  "C:\EntornosPython\pos7Particionado/vulner\static\img/medical1.jpg", 40, 715, width=50,
                 height=50)
        canvas.drawString(250, 750, "CLINICA MEDICAL")
        canvas.drawString(250, 735, 'NIT: 8305077188')
        canvas.drawString(100, 720, "INFORME: ")
        canvas.drawString(150, 720, nombreReporte)
        canvas.drawString(320, 720, "Fecha:")
        canvas.drawString(360, 720, str(format))
        canvas.drawString(520, 720, "Pág: %d " % (doc.page))
        #canvas.drawString(520, 715, "de %d " % (doc.pageCount))



        # Trae Cabezote
        # Ejemplo Tituolo del reporte conexion a BAse de datos, etc



        texto1 = '_________________________________________________________________________________________________________________'
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(30, 670, texto1)

        sonColumnas = range(0, columnas)
        factor = 30

        for i in sonColumnas:
            canvas.drawString(factor, 675, lasColumnas[i])
            factor = factor + 55

        texto1 = '_________________________________________________________________________________________________________________'
        canvas.setFont('Helvetica-Bold', 9)
        canvas.drawString(30, 690, texto1)

        # Fin Cabezote
        pageinfo = "Ejemplo Platypus"
        canvas.drawString(200, 20, "Dirección CALLE 36 SUR 77 33 KENNEDY, BOGOTA")
        # canvas.drawString(inch, 0.75 * inch, "Página %d " % (doc.page))
        canvas.restoreState()


    def cabezote(self, doc, y, Story, tipodoc, documento, folio, headline_mayor, headline_mayor1, headline_mayor2,
             headline_mayor3, headline_mayor33, headline_mayor4, subtitle_tipoevol, subtitle_atencion,
             subtitle_cabezote, subtitle_nacimiento, lineas):
        localcabezote = 0
        print("Entre Cabezote Folio , Linea  ")
        return localcabezote


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi gran Template'
        print("POR QUI PASE")
        print("USERNAME = ",  context )
        username =   context['username']
        sedeSeleccionada = context['sedeSeleccionada']
        numreporte = context["numreporte"]
        grupo = context["grupo"]
        sede= sedeSeleccionada
        subGrupo = context["subGrupo"]

        print("Esta es mi Sede seleccionada =", sedeSeleccionada)


        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NumReporte'] = numReporte
        context["Grupo"] = grupo
        context["SubGrupo"] = subGrupo

        print ("grupo = ", grupo)
        print("Subgrupo = ", subGrupo)

        # Le doy la informacion del Reportes seleccionado
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        #comando = 'select  reportes.id numreporte, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados, reportes.excel excel, reportes.pdf pdf, reportes.csv csv, reportes.grilla from public."Administracion_mae_reportes" reportes where cast(reportes.id as text)  = cast(' + str(numreporte) + ' as text)'
        comando = 'select  reportes.id numreporte, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados, reportes.excel excel, reportes.pdf pdf,reportes.csv as csv,reportes.grilla from public."Administracion_mae_reportes" reportes where cast(reportes.id as text)  = cast(' + str(
            numreporte) + ' as text)'


        cur.execute("set client_encoding='LATIN1';")

        print(comando)
        cur.execute(comando)

        reporteSeleccionado = []

        for numreporte,  reporte, cuerpo_sql, descripcion, encabezados, excel, pdf, csv , grilla  in cur.fetchall():
            reporteSeleccionado.append(
                {'numreporte': numreporte,  'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
                 'descripcion': descripcion, 'encabezados':encabezados, 'excel':excel, 'pdf':pdf, 'csv':csv, 'grilla':grilla})

        miConexion.close()

        print("pase0")

        context['ReporteSeleccionado'] = reporteSeleccionado

        global nombreReporte
        nombreReporte = reporteSeleccionado[0]['reporte']
        print ("El nombre del reporte es : ", nombreReporte)

        # Le doy la informacion de los Parametros del Reporte seleccionado
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        cur = miConexion.cursor()

        comando = 'select   param.parametro parametro,param.parametro_texto param_texto, tiposcampo.nombre param_tipocampo from public."Administracion_mae_reportes" as reportes ,public."Administracion_mae_repparametros" as param, public."Administracion_mae_tiposcampo" tiposcampo where reportes.id = param.mae_reportes_id and tiposcampo.id = param.mae_tiposcampo_id and cast(reportes.id as text)  = cast(' + str(numreporte) + ' as text)' + ' ORDER BY param.parametro'

        print(comando)
        cur.execute(comando)

        parametrosSeleccionado = []

        for parametro, param_texto, param_tipocampo in cur.fetchall():
            parametrosSeleccionado.append(
                {'parametro': parametro, 'param_texto': param_texto,'param_tipocampo': param_tipocampo})

        miConexion.close()

        print("pase0")

        context['ParametrosSeleccionado'] = parametrosSeleccionado

        print("devuelvo1 = ", context['ReporteSeleccionado'])
        print("devuelvo2 = ", context['ParametrosSeleccionado'])


        # Le doy la informacion de los reportes a los que tiene acceso
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()

        #comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id  and sedes.codreg_sede = ltrim(' + "'" + str(sedeSeleccionada) + "')" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A'"
        # comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = ' + "'" + sedeSeleccionada + "'" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A'"

        comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,public."Administracion_mae_reportes" as reportes , sitios_sedesClinica sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id  and sedes.id = ' + "'" + str(sede) + "'" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A'" + ' AND reportes.mae_gruporeportes_id= ' + str(grupo) + ' AND reportes.mae_subgruporeportes_id = ' + str(subGrupo)

        print(comando)
        print("pase01")
        cur.execute(comando)

        reportesUsuario = []

        for numreporte, usuario, reporte, cuerpo_sql, descripcion, encabezados in cur.fetchall():
            reportesUsuario.append(
                {'numreporte': numreporte, 'usuario': usuario, 'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
                 'descripcion': descripcion, 'encabezados': encabezados})

        miConexion.close()

        print("Ojo reenvio estas opciones del menu = ", reportesUsuario)

        context['ReportesUsuario'] = reportesUsuario

        # Validacion Usuario existente
        #
        #miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
        #                           password="123456")
        #cur = miConexion.cursor()
        #comando = "SELECT cod_usuario, nom_usuario, clave_usuario  FROM imhotep_usuarios WHERE cod_Usuario = '" + username + "'"
        #cur.execute(comando)
        #print(comando)

        #nombreUsuario = []

        #for cod_usuario, nom_usuario, clave_usuario in cur.fetchall():
        #    nombreUsuario.append(
        #        {'cod_usuario': cod_usuario, 'nom_usuario': nom_usuario, 'clave_usuario': clave_usuario})

        #miConexion.close()

        #context['NombreUsuario'] = nombreUsuario

        #print("Asi quedo el nombre del usuario", nombreUsuario)

        # Envio los grupos
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

        cur = miConexion.cursor()
        comando = 'select  id , grupos.nom_grupo nombreGrupo , grupos.logo logo from public."Administracion_mae_gruporeportes" grupos order by grupos.id'

        print(comando)
        cur.execute(comando)

        grupos = []

        for id, nombreGrupo , logo in cur.fetchall():
            grupos.append(
                {'id': id, 'nombreGrupo': nombreGrupo , 'logo': logo})

        miConexion.close()
        context['Grupos'] = grupos

        # Envio los Subgrupos
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

        cur = miConexion.cursor()
        comando = 'select  id , subgrupos.nom_subgrupo nombreSubGrupo , subgrupos.logo logo from public."Administracion_mae_subgruporeportes" subgrupos where subgrupos.mae_gruporeportes_id= ' + str(grupo) + ' AND subgrupos.estadoReg=' + "'A'"

        print(comando)
        cur.execute(comando)

        subGrupos = []

        for id, nombreSubGrupo , logo  in cur.fetchall():
            subGrupos.append(
                {'id': id, 'nombreSubGrupo': nombreSubGrupo ,'logo':logo})

        miConexion.close()
        context['SubGrupos'] = subGrupos

        # Consigo Nombre de la sede
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

        cur = miConexion.cursor()
        comando = "SELECT id codreg_sede, nombre nom_sede FROM sitios_sedesClinica WHERE id = '" + sede + "'"
        cur.execute(comando)
        print(comando)

        nombreSede = []

        for codreg_sede, nom_sede in cur.fetchall():
            nombreSede.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

        miConexion.close()

        context['NombreSede'] = nombreSede

        return context



    def post(self, request, *args, **kwargs):
        print ("Comenzamos a generar el Informe")
        #  Arrancamos
        # Story = []
        global Story
        global numReporte
        context = {}
        cuerpo_sql = request.POST.get('cuerpoSql', False)
        encabezados = request.POST.get('encabezados', False)
        tipoArchivo = request.POST.get('tipoArchivo', False)
        numReporte = request.POST.get('numReporte', False)
        username = request.POST["username"]
        sedeSeleccionada = ""
        sedeSeleccionada = request.POST["sedeSeleccionada"]
        nombreReporte = request.POST["nombreReporte"]

        grupo = request.POST.get('grupo', False)
        subGrupo = request.POST.get('subGrupo', False)

        print("encabezados = ", encabezados)
        print("numReporte = ", numReporte)
        print("tipoArchivo = ", tipoArchivo)
        print("username = ", username)
        print("sedeSeleccionada =", sedeSeleccionada)
        sede=sedeSeleccionada
        context['username'] = username
        context['sedeSeleccionada'] = sedeSeleccionada

        context['Grupo'] = grupo
        context['SubGrupo'] = subGrupo


        # Le doy la informacion del Reportes seleccionado
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        #comando = 'select  reportes.id numreporte, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados, reportes.excel excel, reportes.pdf pdf, reportes.csv csv, reportes.grilla from public."Administracion_mae_reportes" reportes where cast(reportes.id as text)  = cast(' + str(numreporte) + ' as text)'
        comando = 'select  reportes.id numreporte, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados, reportes.excel excel, reportes.pdf pdf,reportes.csv as csv,reportes.grilla from public."Administracion_mae_reportes" reportes where cast(reportes.id as text)  = cast(' + str(
            numReporte) + ' as text)'
        cur.execute("set client_encoding='LATIN1';")

        print(comando)
        cur.execute(comando)

        reporteSeleccionado = []

        for numreporte,  reporte, cuerpo_sql, descripcion, encabezados, excel, pdf, csv , grilla  in cur.fetchall():
            reporteSeleccionado.append(
                {'numreporte': numreporte,  'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
                 'descripcion': descripcion, 'encabezados':encabezados, 'excel':excel, 'pdf':pdf, 'csv':csv, 'grilla':grilla})

        miConexion.close()

        print("pase0")

        context['ReporteSeleccionado'] = reporteSeleccionado

        # Consigo Numero de Parametros del reporte
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        cur = miConexion.cursor()
        comando = 'SELECT rep.id numeroreporte, count(*) numeroParametros FROM public."Administracion_mae_reportes" rep,   public."Administracion_mae_repparametros" parametros WHERE parametros.mae_reportes_id = rep.id and  rep.id =' + str(numReporte) + ' group by rep.id'
        print(comando)
        cur.execute(comando)

        numeroDeParametros = []

        for numeroreporte, numeroParametros in cur.fetchall():
            numeroDeParametros.append({'numeroreporte': numeroreporte, 'numeroParametros': numeroParametros})

        miConexion.close()

        hayParametros = 0

        if numeroDeParametros != []:
            print("numeroDeParametros =", numeroDeParametros)

            hayParametros = numeroDeParametros[0]['numeroParametros']
            hayParametros = hayParametros + 1

        print ("hayParametros =", hayParametros)

        ##  nuevo codigo
        #####################
        parametros = []
        x = range(1, hayParametros)
        # t=  range (1, hayParametros - 1)

        parametrosSeleccionado = request.POST.get('parametrosSeleccionado', False)

        print("parametrosSeleccionado NUEVO", parametrosSeleccionado)

        parametrosSeleccionado1 = []

        print("parametrosSeleccionado = a ", parametrosSeleccionado)

        if parametrosSeleccionado == False:

            print("No hay parametros selccionados")
            for i in x:
                comodin = str(i)

                valor = request.POST.get(comodin, False)
                print("valor del parametro = ", valor)
                parametros.append(valor)

        print("parametros = ", parametros)
        c = '?'
        total = len(parametros)
        print("numero de parametros =", total)

        t = range(1, total + 1)

        # Aqui se crea un nuevo parametros 1
        parametros1 = []

        for i in t:
            parametros1.append({"campo": i, 'valor': parametros[i - 1]})

        print("parametros1 ya de devuelta = ", parametros1)

        ## vamos a guardar el valor de los parametros en el context
        context['Parametros1'] = parametros1
        context['Parametros'] = parametros

        if parametrosSeleccionado != False:

            print("parametrosSeleccionado Final queda : ", parametrosSeleccionado)
            for i in x:
                comodin = str(i)
                valor = request.POST.get(comodin, False)
                print("valor del parametro = ", valor)
                parametros.append(valor)

            total = len(parametros)
            print("numero de parametros =", total)
            t = range(1, total + 1)

            for i in t:
                print("Matriz parametros = ", parametros[i - 1])
                dato = "'" + parametros[i - 1] + "'"
                cuerpo_sql = cuerpo_sql.replace("?", dato, 1)

        if parametrosSeleccionado == False:
            for i in t:
                print("Matriz parametros = ", parametros[i - 1])
                dato = "'" + parametros[i - 1] + "'"
                cuerpo_sql = cuerpo_sql.replace("?", dato, 1)

        print("CuerpoSQl_Final = ", cuerpo_sql)

        #desdeFecha = request.POST.get('DesdeFecha', False)
        #hastaFecha = request.POST.get('HastaFecha', False)

        # Aqui hace la pregunta si es excel o pdf



        # Story = [Spacer(0, 20)]
        buff = io.BytesIO()
        # doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=26,   leftMargin=32, topMargin=72, bottomMargin=18)
        doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=26, leftMargin=32, topMargin=120, bottomMargin=20)

        styles = getSampleStyleSheet()
        styleBH = styles["Normal"]
        styleBH.align = 'CENTER'
        styleBH.fontSize = 6

        estilos = getSampleStyleSheet()
        headline_mayor = estilos["Heading1"]
        headline_mayor.alignment = TA_LEFT
        headline_mayor.leading = 8
        headline_mayor.fontSize = 10
        headline_mayor.fontName = "Helvetica-Bold"
        headline_mayor.spaceAfter = 0
        headline_mayor.spaceBefore = 0

        headline_mayor1 = estilos["Heading5"]
        headline_mayor1.alignment = TA_LEFT
        headline_mayor1.leading = 6
        headline_mayor1.fontSize = 8
        headline_mayor1.fontName = "Helvetica-Bold"
        headline_mayor1.spaceAfter = 0
        headline_mayor1.spaceBefore = 0

        headline_mayor2 = estilos["Heading5"]
        headline_mayor2.alignment = TA_LEFT
        headline_mayor2.leading = 7
        headline_mayor2.fontSize = 8
        headline_mayor2.fontName = "Helvetica-Bold"
        headline_mayor2.spaceAfter = 0
        headline_mayor2.spaceBefore = 0

        headline_mayor3 = estilos["Heading5"]
        headline_mayor3.alignment = TA_CENTER
        headline_mayor3.leading = 8
        headline_mayor3.fontSize = 10
        headline_mayor3.fontName = "Helvetica-Bold"
        headline_mayor3.spaceAfter = 0
        headline_mayor3.spaceBefore = 0

        headline_mayor33 = estilos["Heading5"]
        headline_mayor33.alignment = TA_CENTER
        headline_mayor33.leading = 3
        headline_mayor33.fontSize = 10
        headline_mayor33.fontName = "Helvetica-Bold"
        headline_mayor33.spaceAfter = 0
        headline_mayor33.spaceBefore = 0

        headline_mayor4 = estilos["Heading5"]
        headline_mayor4.alignment = TA_CENTER
        # headline_mayor4.leftIndent= 10
        headline_mayor4.leading = 7
        headline_mayor4.fontSize = 9
        headline_mayor4.fontName = "Helvetica-Bold"
        headline_mayor4.spaceAfter = 0
        headline_mayor4.spaceBefore = 0

        subtitle_tipoevol = estilos["Heading2"]
        subtitle_tipoevol.leading = 9  # estaba15
        subtitle_tipoevol.fontSize = 8
        subtitle_tipoevol.fontName = "Times-Roman"
        subtitle_tipoevol.spaceAfter = 0
        subtitle_tipoevol.spaceBefore = 0
        subtitle_tipoevol.alignment = TA_LEFT
        subtitle_tipoevol.wordWrap = 'LTR'

        # subtitle_atencion = estilos["Heading3"]
        # subtitle_atencion.leading =9
        # subtitle_atencion.fontSize = 8
        # subtitle_atencion.fontName = "Times-Roman"
        # subtitle_atencion.spaceAfter = 0
        # subtitle_atencion.spaceBefore = 0
        # subtitle_atencion.alignment = TA_LEFT

        subtitle_atencion = estilos["Heading3"]
        subtitle_atencion.leading = 9
        subtitle_atencion.fontSize = 8
        subtitle_atencion.fontName = "courier-bold"
        subtitle_atencion.spaceAfter = 0
        subtitle_atencion.spaceBefore = 0
        subtitle_atencion.alignment = TA_LEFT
        # Tahoma ,, courier

        subtitle_cabezote = estilos["Heading4"]
        subtitle_cabezote.leading = 7
        subtitle_cabezote.fontSize = 8
        subtitle_cabezote.fontName = "Times-Roman"
        subtitle_cabezote.spaceAfter = 0
        subtitle_cabezote.spaceBefore = 0
        subtitle_cabezote.alignment = TA_LEFT

        subtitle_nacimiento = estilos["Heading6"]
        subtitle_nacimiento.leading = 7
        subtitle_nacimiento.fontSize = 8
        subtitle_nacimiento.fontName = "Times-Roman"
        subtitle_nacimiento.spaceAfter = 0
        subtitle_nacimiento.spaceBefore = 0
        subtitle_nacimiento.alignment = TA_LEFT

        estilos.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
        estilos1 = getSampleStyleSheet()
        estilos1.add(ParagraphStyle(name='Justify_left', alignment=TA_LEFT))
        estilos2 = getSampleStyleSheet()
        estilos2.add(ParagraphStyle(name='Justify_right', alignment=TA_RIGHT))
        response    = HttpResponse(content_type='application/pdf')
        print("Creo Archivo")


        #response = HttpResponse(content_type="application/pdf")

        nombreReporteFinal = nombreReporte + ".pdf"
        response['Content-Disposition'] = 'attachment; filename= '  + nombreReporteFinal

        #response['Content-Disposition'] = 'attachment; filename="' + tipodoc + ' ' + documento + '.pdf"'

        ## Aqui va la impresion de todo el reporte
        ##
        ##


        ## Genero el Reporte Dinamico
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

        miConexion.set_client_encoding('LATIN1')

        cur = miConexion.cursor()

        cur.execute("set client_encoding='LATIN1';")
        print(cur.execute("show server_encoding;"))

        # Aqui se arregla Cuerpo_sql, con los parametros y los valores introducidos por el Usuario


        cur.execute(cuerpo_sql)
        print("Esto lo ejecuto = ", cuerpo_sql)
        rows = cur.fetchall()

        #Story.append(Spacer(1, 3))
        #print ("Este es el listado de Registros " , rows)

        # ExtraigoCuento cuantas columnas hay
        global columnas
        columnas = encabezados.count(',')
        columnas = columnas + 1

        print ("El numero de columnas del reporte son :",  columnas)

        # Extraigo el valor de los encabezados

        t = ","
        #encabezado = "codreg_sede, nom_sede, codreg_ips, direccion, telefono, departamento"
        #columnas = 6

        posicioncoma=0
        initial = encabezados
        global lasColumnas
        lasColumnas = []


        for i in range(columnas):

            posicioncoma =  initial.find(t)
            #print("Posicion coma = ", posicioncoma)
            lasColumnas.append(initial[0:(posicioncoma)])
            initial = initial[(posicioncoma +1) : len(encabezados)]
            #print("initial = ", initial)

        print("Estas son las Columnas :",    lasColumnas)



        if (tipoArchivo == "csv"):

            response = HttpResponse(content_type='text/csv')

            nombreReporteFinal = nombreReporte + ".csv"
            response['Content-Disposition'] = 'attachment; filename= ' + nombreReporteFinal

            myFile = open(nombreReporteFinal, 'w')

            with myFile:
                writer = aliascsv.writer(response, myFile)

            response.write(u'\ufeff'.encode('utf8'))


            # write column headers in sheet
            titulos = ""

            for col_num in range(len(lasColumnas)):
                titulos = titulos +   lasColumnas[col_num] + ","

            writer.writerow([
                smart_str(titulos),
            ])

            row_num = 0

            if rows == []:
                pass
            else:

                for row in rows:
                    row_num = row_num + 1
                    campo= ""
                    campoTot= ""

                    for col in range(len(lasColumnas)):
                        campo = row[col]

                        campoTot = campoTot  + str(campo) + ","

                    writer.writerow([        smart_str(campoTot),     ])

        if (tipoArchivo == "grilla"):

            ## Copio desde aquip lo nuevo

            context['ParametrosSeleccionado'] = parametros1
            numreporteSalvado = numreporte
            print (" Numreporte queda en = ", numreporteSalvado)
            # insert esto

            # Le doy la informacion de los reportes a los que tiene acceso
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

            miConexion.set_client_encoding('LATIN1')
            cur = miConexion.cursor()
            cur.execute("set client_encoding='LATIN1';")
            # comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = '  + "'"  + sedeSeleccionada + "'"
            # comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = ' + "'" + sedeSeleccionada + "'" + ' AND usuarios.estadoReg=' +  "'A'"
            comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados ,reportes.mae_gruporeportes_id grupo ,reportes.mae_subgruporeportes_id subgrupo , grupos.nom_grupo nombreGrupo, subgrupos.nom_subgrupo nombreSubgrupo from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , sitios_sedesClinica sedes ,public."Administracion_mae_gruporeportes" grupos,public."Administracion_mae_subgruporeportes" subgrupos   where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and grupos.id = reportes.mae_gruporeportes_id and grupos.id = ' + "'" + grupo + "'" + ' and subgrupos.id = reportes.mae_subgruporeportes_id  AND subgrupos.id = ' + "'" + subGrupo + "'" + ' and sedes.id = ' + "'" + sede + "'" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A'"

            print(comando)
            cur.execute(comando)

            reportesUsuario = []

            for numreporte, usuario, reporte, cuerpo_sql, descripcion, encabezados, grupo, subgrupo, nombreGrupo, nombreSubGrupo in cur.fetchall():
                reportesUsuario.append(
                    {'numreporte': numreporte, 'usuario': usuario, 'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
                     'descripcion': descripcion, 'encabezados': encabezados, 'grupo': grupo, 'subgrupo': subgrupo,
                     'nombreGrupo': nombreGrupo, 'nombreSubGrupo': nombreSubGrupo})

            miConexion.close()
            context['ReportesUsuario'] = reportesUsuario


            ## fin insetro esto
            ## insetto esto de los parametros

            # Le doy la informacion de los Parametros del Reporte seleccionado
            #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

            cur = miConexion.cursor()

            comando = 'select   param.parametro parametro,param.parametro_texto param_texto, tiposcampo.nombre param_tipocampo from public."Administracion_mae_reportes" as reportes ,public."Administracion_mae_repparametros" as param, public."Administracion_mae_tiposcampo" tiposcampo where reportes.id = param.mae_reportes_id and tiposcampo.id = param.mae_tiposcampo_id and cast(reportes.id as text)  = cast(' + str(numreporteSalvado) + ' as text)' + ' ORDER BY param.parametro'

            print(comando)
            cur.execute(comando)

            parametrosSeleccionado = []

            for parametro, param_texto, param_tipocampo in cur.fetchall():
                parametrosSeleccionado.append(
                    {'parametro': parametro, 'param_texto': param_texto, 'param_tipocampo': param_tipocampo})

            miConexion.close()

            print("pase0")

            context['ParametrosSeleccionado'] = parametrosSeleccionado

            print("ParametrosSeleccionado quedo  = ",parametrosSeleccionado )

            ## Fin inserto esto d elos parametros

            # Validacion Usuario existente
            #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

            cur = miConexion.cursor()
            comando = "SELECT documento cod_usuario, nombre nom_usuario, contrasena clave_usuario  FROM planta_planta WHERE documento = '" + username + "'"
            cur.execute(comando)
            print(comando)

            nombreUsuario = []

            for cod_usuario, nom_usuario, clave_usuario in cur.fetchall():
                nombreUsuario.append(
                    {'cod_usuario': cod_usuario, 'nom_usuario': nom_usuario, 'clave_usuario': clave_usuario})

            miConexion.close()

            context['NombreUsuario'] = nombreUsuario

            print("Asi quedo el nombre del usuario", nombreUsuario)

            ## Hasta Aqui copie lo nuevo

            grilla_data = []

            subir= {}
            x = range(0, len(lasColumnas))

            for row in rows:
               subir = {}
               for j in x:

                   subir[lasColumnas[j].lstrip()] = str(row[j])

               grilla_data.append(subir)

            #print (grilla_data)

            sonColumnas = range(0, len(lasColumnas))

            context['Grilla'] = rows # grilla_data
            context['LasColumnas'] = lasColumnas
            context['NumeroColumnas'] = sonColumnas
            context['Username'] = username
            context['SedeSeleccionada'] = sedeSeleccionada


            # Envio los grupos
            #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
            cur = miConexion.cursor()
            comando = 'select  id , grupos.nom_grupo nombreGrupo from public."Administracion_mae_gruporeportes" grupos'

            print(comando)
            cur.execute(comando)

            grupos = []

            for id, nombreGrupo in cur.fetchall():
                grupos.append(
                    {'id': id, 'nombreGrupo': nombreGrupo})

            miConexion.close()
            context['Grupos'] = grupos

            # Envio los Subgrupos
            #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
            cur = miConexion.cursor()
            comando = 'select  id , subgrupos.nom_subgrupo nombreSubGrupo from public."Administracion_mae_subgruporeportes" subgrupos where subgrupos.mae_gruporeportes_id= ' + str(
                grupo)

            print(comando)
            cur.execute(comando)

            subGrupos = []

            for id, nombreSubGrupo in cur.fetchall():
                subGrupos.append(
                    {'id': id, 'nombreSubGrupo': nombreSubGrupo})

            miConexion.close()
            context['SubGrupos'] = subGrupos

            # Consigo Nombre de la sede
            #
            miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

            cur = miConexion.cursor()
            comando = "SELECT id codreg_sede, nombre nom_sede FROM sitios_sedesClinica WHERE id = '" + sedeSeleccionada + "'"
            cur.execute(comando)
            print(comando)

            nombreSede = []

            for codreg_sede, nom_sede in cur.fetchall():
                nombreSede.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

            miConexion.close()

            context['NombreSede'] = nombreSede

            return render(request, "Reportes/PantallaGrillaAngular.html", context)

        if (tipoArchivo == "excel"):

            response = HttpResponse(content_type="application/ms-excel")
            nombreReporteFinal = nombreReporte + ".xls"
            response['Content-Disposition'] = 'attachment; filename=' + nombreReporteFinal

            # creating workbook
            wb = xlwt.Workbook(encoding='utf-8')

            # adding sheet
            #Info0 = wb.add_sheet("Info0")

            styles = dict(
                bold='font: bold 1',
                italic='font: italic 1',
                # Wrap text in the cell
                wrap_bold='font: bold 1; align: wrap 1;',
                # White text on a blue background
                reversed='pattern: pattern solid, fore_color blue; font: color white;',
                # Light orange checkered background
                light_orange_bg='pattern: pattern fine_dots, fore_color white, back_color orange;',
                # Heavy borders
                bordered='border: top thick, right thick, bottom thick, left thick;',
                # 16 pt red text
                big_red='font: height 260, color blue;',

                # 16 pt red text
                normal='font: height 260, color black;',
            )

           # for idx, k in enumerate(sorted(styles)):
           #     style = xlwt.easyxf(styles[k])
           #     ws.write(idx, 0, k)
           #     ws.write(idx, 1, styles[k], style)


            # Sheet header, first row
            row_num = 0

            # Encabezados del Reporte

            #font_style = xlwt.XFStyle()
            # headers are bold
            #font_style.font.bold = True

            #row_num = 1

            #Info0.write(row_num, 0, "CLINICA MEDICAL", font_style)
            #row_num = row_num + 1
            #Info0.write(row_num, 0, 'NIT: 8305077188', font_style)
            #row_num = row_num + 1
            #Info0.write(row_num, 0, "INFORME: ", font_style)
            #Info0.write(row_num, 1, nombreReporte, font_style)
            #Info0.write(row_num, 3, "FECHA: ", font_style)
            #fechaActual = datetime.today().strftime('%Y-%m-%d %H:%M')
            #print("Fecha Actual = ", fechaActual)
            #Info0.write(row_num, 4, fechaActual, font_style)

            #row_num = row_num + 2

            # write column headers in sheet
            #for col_num in range(len(lasColumnas)):
            #    style = xlwt.easyxf(styles['big_red'])
            #    #ws.write(idx, 1, styles[k], style)
            #    Info0.write(row_num, col_num, lasColumnas[col_num], style)

            #row_num = row_num + 1

            # Sheet body, remaining rows
            #font_style = xlwt.XFStyle()
            #font_style.font.bold = True

            # get your data, from database or from a text file...
            global Info0
            if rows == []:
                A1=0
                Info0 = wb.add_sheet("Info0")
            else:
                style = xlwt.easyxf(styles['normal'])

                # Practicamente desde aquio se comienza a imprimir el reporte

                print("ESte es el tamaño de que ? " , len(rows))

                numeroHojas = math.trunc(len(rows)/60000)

                if numeroHojas == 0:
                    numeroHojas = 1
                else:
                     if (numeroHojas % numeroHojas != 1):
                          numeroHojas = numeroHojas + 1



                print("El Numero de Hojas =  ", math.trunc(numeroHojas))

                x = range(0, (numeroHojas))

                nombreDeHojas = []
                Info = "Info"

                resultado = 0

                n = range(1, numeroHojas + 1)

                for hoj in n:
                    if (hoj == 1):

                        print("Entre a crear la Primera Info0")

                        Info0 = wb.add_sheet("Info0")
                    if (hoj == 2):
                        global Info1
                        Info1 = wb.add_sheet("Info1")
                    if (hoj == 3):
                        global Info2
                        Info2 = wb.add_sheet("Info2")
                    if (hoj == 4):
                        global Info3
                        Info3 = wb.add_sheet("Info3")
                    if (hoj == 5):
                        global Info4
                        Info4 = wb.add_sheet("Info4")
                    if (hoj == 6):
                        global Info5
                        Info5 = wb.add_sheet("Info5")
                    if (hoj == 7):
                        global Info6
                        Info6 = wb.add_sheet("Info6")
                    if (hoj == 8):
                        global Info7
                        Info7 = wb.add_sheet("Info7")
                    if (hoj == 9):
                        global Info8
                        Info8 = wb.add_sheet("Info8")
                    if (hoj == 10):
                        global Info9
                        Info9 = wb.add_sheet("Info9")
                    if (hoj == 11):
                        global Info10
                        Info10 = wb.add_sheet("Info10")
                    if (hoj == 12):
                        global Info11
                        Info11 = wb.add_sheet("Info11")
                    if (hoj == 13):
                        global Info12
                        Info12 = wb.add_sheet("Info12")
                    if (hoj == 14):
                        global Info13
                        Info13 = wb.add_sheet("Info13")
                    if (hoj == 15):
                        global Info14
                        Info14 = wb.add_sheet("Info14")
                    if (hoj == 16):
                        global Info15
                        Info15 = wb.add_sheet("Info15")
                    if (hoj == 17):
                        global Info16
                        Info16 = wb.add_sheet("Info16")
                    if (hoj == 18):
                        global Info17
                        Info17 = wb.add_sheet("Info17")
                    if (hoj == 19):
                        global Info18
                        Info18 = wb.add_sheet("Info18")
                    if (hoj == 20):
                        global Info19
                        Info19 = wb.add_sheet("Info19")

                if numeroHojas <= 1:
                        desde=0
                        hasta=len(rows)

                if numeroHojas > 1:
                        desde = 0
                        hasta = 60000
                        # Aqui debe crear las hojas que va a Utilizar

                for z in x:
                    # Aqui impresion de titulos,

                    if (z==0):
                        print("Aqui el error")
                        resultado = titulosCab(Info0)
                    if (z==1):
                        resultado = titulosCab(Info1)
                    if (z==2):
                        titulosCab(Info2)
                    if (z==3):
                        titulosCab(Info3)
                    if (z==4):
                        titulosCab(Info4)
                    if (z==5):
                        titulosCab(Info5)
                    if (z==6):
                        titulosCab(Info6)
                    if (z==7):
                        titulosCab(Info7)
                    if (z==8):
                        titulosCab(Info8)
                    if (z==10):
                        titulosCab(Info10)
                    if (z==11):
                        titulosCab(Info11)
                    if (z==12):
                        titulosCab(Info12)
                    if (z==13):
                        titulosCab(Info13)
                    if (z==14):
                        titulosCab(Info14)
                    if (z==15):
                        titulosCab(Info15)
                    if (z==16):
                        titulosCab(Info16)
                    if (z==17):
                        titulosCab(Info17)
                    if (z==18):
                        titulosCab(Info18)
                    if (z==19):
                        titulosCab(Info19)


                    for i in range(desde, hasta):

                        for j in range(0, len(rows[i])):
                            if z==0:
                                Info0.write(i+8, j, str(rows[i][j]), style)
                            if z==1:
                                Info1.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==2:
                                Info2.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==3:
                                Info3.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==4:
                                Info4.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==5:
                                Info5.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==6:
                                Info6.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==7:
                                Info7.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==8:
                                Info8.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==9:
                                Info9.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==10:
                                Info10.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==11:
                                Info11.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==12:
                                Info12.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==13:
                                Info13.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==14:
                                Info14.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==15:
                                Info15.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==16:
                                Info16.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==17:
                                Info17.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==18:
                                Info18.write(i-desde+8, j, str(rows[i][j]), style)
                            if z==19:
                                Info19.write(i-desde+8, j, str(rows[i][j]), style)


                    desde = hasta
                    if (z == (numeroHojas-2)):
                        hasta = len(rows)
                        print ("Hasta de Control = " , hasta)
                        print("z =  ", z)
                    else:
                        hasta = hasta + 60000
                        print("Hasta Normal = ", hasta)
                        print("z =  ", z)


                #for row in rows:
                #    row_num = row_num + 1
                #    print ("fila : ", row)


                #    for col in range(len(lasColumnas)):

                #       campo = row[col]
                #        print("fila= ", row_num)
                #        print("columna= ", col)
                #        print ("campo= ", campo)
                #        ws.write(row_num, col, campo, style)



        if (tipoArchivo=='pdf'):

            # Genera el pdf


            if rows == []:

                tbl_data4 = ['  ']
                print ("Entre por No registros PDF")
                tbl1 = Table(tbl_data4, colWidths =[10 * cm, 1.6 * cm, 1.4  * cm, 1  * cm, 4.6  * cm, 1 * cm])

                Story.append(tbl1)
                Story.append(Spacer(1, 3))

            else:
                print("Entre por SI HAY  registros PDF")
                # Aqui Rutina de Impresion de Titulos

                comienzo = 0
                mascara = ""
                print ("Aqui va el listado de Registros")

                for row in rows:
                    tbl_data3 = []
                    tbl_data2 = []
                    tbl_data1 = []
                    longitudes = []
                    longitudesFinal = []
                    longitudesFinal1 = {}
                    longitudesFinal1['formato'] = ""
                    Ancho = 0
                    calculo = 0
                    son = ""
                    print("fila : ", row)
                    print ("columnas = ", columnas)

                    m = range(0, columnas)

                    for i in m:
                            print("la variable i = ", i)
                            print("columna longitud = ", len(str(row[i])))
                            longitudes.append(len(str(row[i])))
                            Ancho = Ancho + int(len(str(row[i])))

                    print ("Total Ancho Columnas =", Ancho)

                    for i in m:
                            tbl_data1 = Paragraph(str(row[i]), subtitle_tipoevol),
                            tbl_data2.append(tbl_data1)
                            calculo = round(longitudes[i] * 19 / Ancho,2)

                            if calculo < 1:
                                calculo = 1
                            son = son + str(calculo) + " * cm, "
                            #longitudesFinal1['formato'] = longitudesFinal1['formato'] + str(calculo) + " * cm, "

                    longitudesFinal.append(son.replace("'",''))
                    #longitudesFinal1['formato']  = son

                    son = '[' + son + ']'
                    son.replace("'", ' ')
                    print('son = ', son)
                    print("longitud Final = ", longitudesFinal)
                    print("longitud Final Otro = ", longitudesFinal[0])

                    print ("tbl_data2 = ", tbl_data2)
                    tbl_data3.append(tbl_data2)
                    print("tbl_data3 = ", tbl_data3)

                    #tbl1 = Table(tbl_data3, colWidths=[3.5 * cm, 2   * cm, 8    * cm, 2    * cm, 3    * cm, 0.5  * cm])
                    #floats = list(map(float, longitudesFinal1['formato']))


                    tbl1 = Table(tbl_data3, colWidths=None)
                    #tbl1 = Table(tbl_data3, colWidths=floats)

                    Story.append(tbl1)
                    Story.append(Spacer(1, 3))

        miConexion.close()


        # Le doy la informacion de los reportes a los que tiene acceso
        #
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")
        comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,public."Administracion_mae_reportes" as reportes , sitios_sedesClinica sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id and sedes.id = ' + "'" + str(sede) + "'" + ' AND reportes.estadoReg=' + "'A'"

        print(comando)
        cur.execute(comando)

        reportesUsuario = []

        for numreporte, usuario, reporte, cuerpo_sql, descripcion, encabezados in cur.fetchall():
            reportesUsuario.append(
                {'numreporte': numreporte, 'usuario': usuario, 'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
                 'descripcion': descripcion, 'encabezados': encabezados})

        miConexion.close()

        print("pase0")

        context['ReportesUsuario'] = reportesUsuario


        if (tipoArchivo == "excel"):
            print("vOY DE REGRESO CON EL eXCEL")
            wb.save(response)
            print("vOY DE REGRESO CON EL eXCEL1")
            return response

        if (tipoArchivo == "pdf"):
            print("Voy a generar el reporte")
            doc.build(Story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
            response.write(buff.getvalue())
            buff.close()

            return response

        if (tipoArchivo == "csv"):

            return response


def titulosCab(RecibeInfo):

        print("Entre Rutina de impresion")

        row_num = 0

        styles = dict(
            bold='font: bold 1',
            italic='font: italic 1',
            # Wrap text in the cell
            wrap_bold='font: bold 1; align: wrap 1;',
            # White text on a blue background
            reversed='pattern: pattern solid, fore_color blue; font: color white;',
            # Light orange checkered background
            light_orange_bg='pattern: pattern fine_dots, fore_color white, back_color orange;',
            # Heavy borders
            bordered='border: top thick, right thick, bottom thick, left thick;',
            # 16 pt red text
            big_red='font: height 260, color blue;',

            # 16 pt red text
            normal='font: height 260, color black;',
        )

        row_num = 1

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        RecibeInfo.write(row_num, 0, "CLINICA MEDICAL", font_style)
        row_num = row_num + 1
        RecibeInfo.write(row_num, 0, 'NIT: 8305077188', font_style)
        row_num = row_num + 1
        RecibeInfo.write(row_num, 0, "INFORME: ", font_style)
        RecibeInfo.write(row_num, 1, nombreReporte, font_style)
        RecibeInfo.write(row_num, 3, "FECHA: ", font_style)
        fechaActual = datetime.today().strftime('%Y-%m-%d %H:%M')
        print("Fecha Actual = ", fechaActual)
        RecibeInfo.write(row_num, 4, fechaActual, font_style)

        row_num = row_num + 2

        # write column headers in sheet
        for col_num in range(len(lasColumnas)):
            style = xlwt.easyxf(styles['big_red'])
            # ws.write(idx, 1, styles[k], style)
            RecibeInfo.write(row_num, col_num, lasColumnas[col_num], style)
        row_num = row_num + 1
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        return 0


def pantallaSubgrupos(request, username, sedeSeleccionada, grupo):
    print ("Entre Pantala Subgrupos")

    context = {}


    print("username = ", username)
    print("sedeSeleccionada = ", sedeSeleccionada)
    print("grupo = ", grupo)

    sede = sedeSeleccionada
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['Grupo'] = grupo

    # Consigo Nombre de la sede

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id codreg_sede, nombre nom_sede FROM sitios_sedesClinica WHERE id = '" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for codreg_sede, nom_sede in cur.fetchall():
        nombreSede.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

    miConexion.close()

    context['NombreSede'] = nombreSede


    # Le doy la informacion de los reportes a los que tiene acceso

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    miConexion.set_client_encoding('LATIN1')

    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")
    # comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = '  + "'"  + sedeSeleccionada + "'"
    # comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes  where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and sedes.codreg_sede = ' + "'" + sedeSeleccionada + "'" + ' AND usuarios.estadoReg=' +  "'A'"
    comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados ,reportes.mae_gruporeportes_id grupo ,reportes.mae_subgruporeportes_id subgrupo , grupos.nom_grupo nombreGrupo, subgrupos.nom_subgrupo nombreSubgrupo from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , public."Administracion_imhotep_sedesreportes" sedes ,public."Administracion_mae_gruporeportes" grupos,public."Administracion_mae_subgruporeportes" subgrupos   where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and grupos.id = reportes.mae_gruporeportes_id and grupos.id = '   + "'" + grupo + "'" + ' and subgrupos.id = reportes.mae_subgruporeportes_id  and sedes.codreg_sede = ' + "'" + sedeSeleccionada + "'" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A'"

    print(comando)
    cur.execute(comando)

    reportesUsuario = []

    for numreporte, usuario, reporte, cuerpo_sql, descripcion, encabezados, grupo, subgrupo, nombreGrupo, nombreSubGrupo in cur.fetchall():
        reportesUsuario.append(
            {'numreporte': numreporte, 'usuario': usuario, 'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
             'descripcion': descripcion, 'encabezados': encabezados, 'grupo': grupo, 'subgrupo': subgrupo,
             'nombreGrupo': nombreGrupo, 'nombreSubGrupo': nombreSubGrupo})

    miConexion.close()
    context['ReportesUsuario'] = reportesUsuario

    # Envio Nombre de Grupo Seleccionado

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = 'select  grupos.id id, grupos.nom_grupo nombreGrupo from public."Administracion_mae_gruporeportes" grupos where grupos.id =' + "'" + str(
        grupo) + "'"

    print(comando)
    cur.execute(comando)

    nombreGrupoSeleccionado = []

    for id, nombreGrupo in cur.fetchall():
        nombreGrupoSeleccionado.append({'id': id, 'nombreGrupo': nombreGrupo})

    miConexion.close()
    context['NombreGrupoSeleccionado'] = nombreGrupoSeleccionado


    # Envio los grupos

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = 'select  id , grupos.nom_grupo nombreGrupo, grupos.logo logo from public."Administracion_mae_gruporeportes" grupos order by grupos.id'

    print(comando)
    cur.execute(comando)

    grupos = []

    for id, nombreGrupo, logo in cur.fetchall():
        grupos.append(
            {'id': id, 'nombreGrupo': nombreGrupo , 'logo': logo})

    miConexion.close()
    context['Grupos'] = grupos

    # Envio los Subgrupos

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cur = miConexion.cursor()
    comando = 'select  id , subgrupos.nom_subgrupo nombreSubGrupo , subgrupos.logo logo  from public."Administracion_mae_subgruporeportes" subgrupos where subgrupos.mae_gruporeportes_id= ' + str(grupo) + ' AND subgrupos.estadoReg=' + "'A'"

    print(comando)
    cur.execute(comando)

    subGrupos = []

    for id, nombreSubGrupo , logo in cur.fetchall():
        subGrupos.append(
            {'id': id, 'nombreSubGrupo': nombreSubGrupo , 'logo': logo})

    miConexion.close()
    context['SubGrupos'] = subGrupos



    print("pase0")

    return render(request, "Reportes/PantallaSubGrupos.html", context)

def combo(request, username, sedeSeleccionada, grupo, subGrupo):

    context = {}

    print ("Entre Combo")
    print("username = ", username)
    print("sedeSeleccionada = ", sedeSeleccionada)
    print("grupo = ", grupo)
    print("subgrupo = ", subGrupo)

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['Grupo'] = grupo
    context['SubGrupo'] = subGrupo
    subgrupo = subGrupo
    sede=sedeSeleccionada
    # Envio los grupos

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = 'select  id , grupos.nom_grupo nombreGrupo , grupos.logo logo from public."Administracion_mae_gruporeportes" grupos order by grupos.id'

    print(comando)
    cur.execute(comando)

    grupos = []

    for id, nombreGrupo , logo in cur.fetchall():
        grupos.append(
            {'id': id, 'nombreGrupo': nombreGrupo , 'logo': logo})

    miConexion.close()
    context['Grupos'] = grupos

    # Envio los Subgrupos

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = 'select  id , subgrupos.nom_subgrupo nombreSubGrupo , subgrupos.logo logo from public."Administracion_mae_subgruporeportes" subgrupos where subgrupos.mae_gruporeportes_id= ' + str(
        grupo)

    print(comando)
    cur.execute(comando)

    subGrupos = []

    for id, nombreSubGrupo, logo in cur.fetchall():
        subGrupos.append(
            {'id': id, 'nombreSubGrupo': nombreSubGrupo , 'logo': logo})

    miConexion.close()
    context['SubGrupos'] = subGrupos

    # Consigo Nombre de la sede

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = "SELECT id codreg_sede, nombre nom_sede FROM sitios_sedesClinica  WHERE id = '" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for codreg_sede, nom_sede in cur.fetchall():
        nombreSede.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

    miConexion.close()

    context['NombreSede'] = nombreSede

    # Le doy la informacion de los reportes a los que tiene acceso

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")
    comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados ,reportes.mae_gruporeportes_id grupo ,reportes.mae_subgruporeportes_id subgrupo , grupos.nom_grupo nombreGrupo, subgrupos.nom_subgrupo nombreSubgrupo from public."Administracion_mae_repusuarios" as usuarios,  public."Administracion_mae_reportes" as reportes , sitios_sedesClinica sedes ,public."Administracion_mae_gruporeportes" grupos,public."Administracion_mae_subgruporeportes" subgrupos   where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and grupos.id = reportes.mae_gruporeportes_id and grupos.id = ' + "'" + grupo + "'" + ' and subgrupos.id = reportes.mae_subgruporeportes_id  AND subgrupos.id = '  + "'" + subGrupo + "'" + ' and sedes.id = ' + "'" + sede + "'" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A' ORDER BY reportes.id ASC"

    print(comando)
    cur.execute(comando)

    reportesUsuario = []

    for numreporte, usuario, reporte, cuerpo_sql, descripcion, encabezados, grupo, subgrupo, nombreGrupo, nombreSubGrupo in cur.fetchall():
        reportesUsuario.append(
            {'numreporte': numreporte, 'usuario': usuario, 'reporte': reporte, 'cuerpo_sql': cuerpo_sql,
             'descripcion': descripcion, 'encabezados': encabezados, 'grupo': grupo, 'subgrupo': subgrupo,
             'nombreGrupo': nombreGrupo, 'nombreSubGrupo': nombreSubGrupo})

    miConexion.close()
    context['ReportesUsuario'] = reportesUsuario

    print (" reportesUsuario =", reportesUsuario)

    ## RUTINA AVERIGUAR EL PRIMER ID DEL REPOTE PARA COLOCARLO EN LA VARIABLE numreporte

    ## context['numreporte'] = 24

    if reportesUsuario == []:
        context['numreporte'] = ""
    else:
        context['numreporte'] = reportesUsuario[0]['numreporte']

    print (" numreporte =", reportesUsuario[0]['numreporte'])

    ## FIN RUTINA AVERIGUAR EL PRIMER ID DEL REPOTE PARA COLOCARLO EN LA VARIABLE numreporte


    # Envio Nombre de SubGrupo Seleccionado

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = 'select  id , subgrupos.nom_subgrupo nombreSubGrupo  from public."Administracion_mae_subgruporeportes" subgrupos where subgrupos.id = ' + str(
        subgrupo) + ' AND subgrupos.mae_gruporeportes_id= ' + str(
        grupo)

    print(comando)
    cur.execute(comando)

    nombreSubGrupoSeleccionado = []

    for id, nombreSubGrupo in cur.fetchall():
        nombreSubGrupoSeleccionado.append({'id': id, 'nombreSubGrupo': nombreSubGrupo})

    miConexion.close()
    context['NombreSubGrupoSeleccionado'] = nombreSubGrupoSeleccionado

    #return render(request, "Reportes/combo.html", context)
    return render(request, "Reportes/ParametrosAngular2.html", context)


def emergenteGrupos(request, username, sedeSeleccionada, grupo):
    # Le doy la informacion de los reportes a los que tiene acceso

    context = {}

    # Sedes
    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = 'SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes" where estadoReg=' + "'A'"
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})
    miConexion.close()

    context['Sedes'] = sedes
    print("Aqui estan las sedes")
    print(context['Sedes'])

    print("username = ", username)

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada

    # Consigo Nombre de la sede

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    # comando = "SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes" WHERE codreg_sede = '" + sedeSeleccionada + "'"
    comando = 'SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes" where estadoReg=' + "'A'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for codreg_sede, nom_sede in cur.fetchall():
        nombreSede.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

    miConexion.close()

    context['NombreSede'] = nombreSede

    # Envio los grupos

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")

    cur = miConexion.cursor()
    comando = 'select  id , grupos.nom_grupo nombreGrupo , grupos.logo logo from public."Administracion_mae_gruporeportes" grupos order by grupos.id'

    print(comando)
    cur.execute(comando)

    grupos = []

    for id, nombreGrupo, logo in cur.fetchall():
        grupos.append(
            {'id': id, 'nombreGrupo': nombreGrupo, 'logo': logo})

    miConexion.close()
    context['Grupos'] = grupos

    print("pase0")

    return render(request, "Reportes/pantallaGruposAngular.html", context)

