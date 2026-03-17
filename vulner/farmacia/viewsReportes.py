import json
from django import forms
import cv2
import numpy as np
from fpdf import FPDF
from PyPDF2 import PdfReader
import webbrowser
import psycopg2
import json
import datetime
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.utils.timezone import now
from django.db.models import Avg, Max, Min
from datetime import datetime
from django.db.models import Avg, Max, Min , Sum
from farmacia.models import Farmacia, FarmaciaDetalle, FarmaciaEstados
from enfermeria.models import Enfermeria, EnfermeriaDetalle
from admisiones.models import Ingresos
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.http import JsonResponse
import pyodbc
import psycopg2
import json
import datetime
import cgi
from django.db import transaction
import os
from django.http import FileResponse
from io import BytesIO
import io



class PDFDespacho(FPDF):
    def __init__(self, tipoDocId,documentoId, consec, farmaciaId, despachoId, tipoAdmision,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.farmaciaId = farmaciaId
        self.despachoId = despachoId
        self.tipoAdmision = tipoAdmision


    def header(self):
        # Logo
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 180 ,20, 10 , 10)
        # Arial bold 15
        self.set_font('Sans Serif', 'B', 7)

        # Move to the right
        # self.cell(12)

        convenioId = ConveniosPacienteIngresos.objects.filter(tipoDoc_id=self.tipoDocId, documento_id=self.documentoId,
                                                              consecAdmision=self.consec).aggregate(Max('convenio_id'))

        print("convenioId = ", convenioId['convenio_id__max'])
        convenio = convenioId['convenio_id__max']

        ## CURSOR PARA LEER ENCABEZADO
        #
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")

        curt = miConexiont.cursor()

        if (self.tipoAdmision=='ADMISION'):

            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, u.documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str(
                'M') + "'" + ' then ' + "'" + str('Masculino') + "'" + ' when genero= ' + "'" + str(
                'F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, cast((date_part(' + "'" + str(
                'year') + "'" + ', now()) - date_part(' + "'" + str(
                'year') + "'" + ', u."fechaNacio" )) as text) edad,   reg.nombre regimen, convenio.nombre convenio , serv.nombre servicio, cast(now() as text) fecha from admisiones_ingresos adm INNER JOIN 	usuarios_usuarios u ON (u."tipoDoc_id" = adm."tipoDoc_id" and u.id = adm.documento_id) INNER JOIN usuarios_tiposDocumento tip ON (tip.id = u."tipoDoc_id") LEFT JOIN facturacion_conveniospacienteingresos  convIngreso ON (convIngreso."tipoDoc_id" = adm."tipoDoc_id" and convIngreso.documento_id = adm.documento_id and convIngreso."consecAdmision" = adm.consec) LEFT JOIN contratacion_convenios convenio ON (convenio.id = convIngreso.convenio_id AND convenio.id = ' + "'" + str(convenio) + "')" +  ' LEFT JOIN facturacion_empresas EMP on (emp.id =convenio.empresa_id ) LEFT JOIN clinico_regimenes reg ON (reg.id=emp.regimen_id) INNER JOIN sitios_serviciosSedes serv ON (serv.id = adm."serviciosActual_id")	 WHERE adm."tipoDoc_id" = ' + "'" + str(
                self.tipoDocId) + "'" + ' AND adm.documento_id= ' + "'" + str(
                self.documentoId) + "'" + ' AND adm.consec = ' + "'" + str(
                self.consec) + "'"
        else:

            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, u.documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str(
                'M') + "'" + ' then ' + "'" + str('Masculino') + "'" + ' when genero= ' + "'" + str(
                'F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, cast((date_part(' + "'" + str(
                'year') + "'" + ', now()) - date_part(' + "'" + str(
                'year') + "'" + ', u."fechaNacio" )) as text) edad,   reg.nombre regimen, convenio.nombre convenio , serv.nombre servicio, cast(now() as text) fecha from triage_triage tri INNER JOIN 	usuarios_usuarios u ON (u."tipoDoc_id" = tri."tipoDoc_id" and u.id = tri.documento_id) INNER JOIN usuarios_tiposDocumento tip ON (tip.id = u."tipoDoc_id") LEFT JOIN facturacion_conveniospacienteingresos  convIngreso ON (convIngreso."tipoDoc_id" = tri."tipoDoc_id" and convIngreso.documento_id = tri.documento_id and convIngreso."consecAdmision" = tri.consec) LEFT JOIN contratacion_convenios convenio ON (convenio.id = convIngreso.convenio_id AND convenio.id = ' + "'" + str(convenio) + "')" +  ' LEFT JOIN facturacion_empresas EMP on (emp.id =convenio.empresa_id ) LEFT JOIN clinico_regimenes reg ON (reg.id=emp.regimen_id) INNER JOIN sitios_serviciosSedes serv ON (serv.id = tri."serviciosSedes_id") WHERE tri."tipoDoc_id" = ' + "'" + str(
                self.tipoDocId) + "'" + ' AND tri.documento_id= ' + "'" + str(
                self.documentoId) + "'" + ' AND tri.consec = ' + "'" + str(
                self.consec) + "'"

        curt.execute(comando)
        print(comando)

        historia = []

        for tipoDoc_id, tipnombre, documentoPaciente, nombre, genero, edad, regimen, convenio, servicio, fecha in curt.fetchall():
            historia.append(
                {'tipoDoc_id': tipoDoc_id, 'tipnombre': tipnombre, 'documentoPaciente': documentoPaciente,
                 'nombre': nombre, 'genero': genero, 'edad': edad, 'regimen': regimen, 'convenio': convenio,
                 'servicio': servicio, 'fecha': fecha})

        miConexiont.close()

        ## FIN CURSOR
        # Define el ancho de línea
        self.set_line_width(0.4)
        # Dibuja el borde

        self.rect(10.0, 15.0, 195.0, 265.0)  # Coordenadas x, y, ancho, alto
        self.ln(3)
        self.set_font('Sans Serif', 'B', 7)
        self.cell(195, 10, 'CLINICA MEDICAL', 0, 0, 'C')
        self.ln(3)
        self.cell(195, 10, 'DESPACHO', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Sans Serif', 'B', 8)
        self.cell(25, 10, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)

        self.cell(25, 10, historia[0]['tipnombre'], 0, 0, 'L')
        self.cell(25, 10, historia[0]['documentoPaciente'], 0, 0, 'L')
        self.cell(25, 10, historia[0]['nombre'], 0, 0, 'L')
        self.ln(1)
        self.set_font('Sans Serif', 'B', 8)
        self.cell(25, 10, 'EDAD:', 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)
        self.cell(50, 10, historia[0]['edad'], 0, 0, 'L')
        self.set_font('Sans Serif', 'B', 8)
        self.cell(25, 10, 'GENERO:', 0, 0, 'L')
        self.set_font('Sans Serif', '', 7)
        self.cell(50, 10, historia[0]['genero'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Sans Serif', 'B', 8)
        self.cell(25, 10, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)
        self.cell(50, 10, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Sans Serif', 'B', 8)
        self.cell(25, 10, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)
        self.cell(25, 10, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Sans Serif', 'B', 8)
        self.cell(25, 10, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)
        self.cell(25, 10, str(historia[0]['servicio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Sans Serif', 'B', 8)
        self.cell(25, 10, 'FECHA:', 0, 0, 'L')
        self.cell(25, 10, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(7)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Sans Serif', 'B', 8)
        #self.cell(180, 10, 'MEDICO ORDENA', 0, 0, 'C')
        self.ln(4)

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curii = miConexionii.cursor()
        #comando = 'SELECT  medicos."registroMedico", planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento FROM clinico_historia his INNER JOIN planta_planta planta ON (planta.id = his."usuarioRegistro_id")	INNER JOIN clinico_medicos medicos ON (medicos.planta_id = his."usuarioRegistro_id") WHERE his.id = ' + "'" + str(self.historiaId) + "'" + ' group by "registroMedico", plantaNombre, planta."tipoDoc_id", documento'
        comando = 'SELECT disp.despacho_id despacho, desp."usuarioEntrega_id" codEntrega , desp."usuarioRecibe_id" codRecibe, pla1.nombre entrega, pla2.nombre recibe  FROM farmacia_farmaciadespachos desp inner join farmacia_farmaciadespachosdispensa disp on (disp.despacho_id = desp.id) inner join planta_planta pla1 on (pla1.id= desp."usuarioEntrega_id") inner join planta_planta pla2 on (pla2.id= desp."usuarioRecibe_id") where disp."farmaciaDetalle_id" = ' + "'" + str(detalleFarmaciaId) + "'" + ' and disp.id = (select max(disp1.id) from  farmacia_farmaciadespachosdispensa disp1 where disp1."farmaciaDetalle_id" = disp."farmaciaDetalle_id")'

        curii.execute(comando)

        print(comando)

        registro = []

        for depacho, codEntrega, codRecibe, entrega, recibe in curii.fetchall():
            registro.append(
                {'depacho': depacho, 'codEntrega': codEntrega, 'codRecibe': codRecibe, 'entrega': entrega,'recibe':recibe })
        miConexionii.close()

        self.set_line_width(0.4)
        self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto

        self.set_font('Sans Serif', 'B', 8)
        print('registro =', registro)
        self.cell(15, 10, 'Entrega Por:', 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)
        self.cell(25, 10, '' + str(registro[0]['entrega']), 0, 0, 'L')


        self.ln(2)
        self.set_font('Sans Serif', 'B', 8)
        self.cell(100, 10, 'Recibe', 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)
        self.cell(25, 10, '' + str(registro[0]['recibe']), 0, 0, 'L')
        self.set_font('Sans Serif', '', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def ImprimirDespacho(request, farmaciaId, despachoId):

    # Instantiation of inherited class

    print("Entre ImprimirDespacho " , farmaciaId)

    farmaciaId = request.POST['farmaciaId']
    print("farmaciaId =", farmaciaId)

    despachoId = request.POST['despachoId']
    print("despachoId =", despachoId)

    farmacia = Farmacia.objects.get(id=farmaciaId)
    historia = Historia.objects.get(id=farmacia.historia_id)

    print("historia =", historia)
    print("farmacia =", farmacia)

    #farmaciaDetalle = FarmaciaDetalle.objects.filter(farmaciaDetalle_id=farmaciaDetalleId).first

    try:
        with transaction.atomic():
            ingresoPaciente = Ingresos.objects.get(tipoDoc_id=historia.tipoDoc_id, documento_id = historia.documento_id, consec=historia.consecAdmision )
            print(" ingresosPaciente = ", ingresoPaciente.id)
            tipoAdmision='ADMISION'

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback INGRESO por:", e)
        ingresoPaciente = Triage.objects.get(tipoDoc_id=historia.tipoDoc_id, documento_id=historia.documento_id,consec=historia.consecAdmision)
        print(" ingresosPaciente = ", ingresoPaciente.id)
        tipoAdmision = 'TRIAGE'

    finally:
        print("Finally")


    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec =  ingresoPaciente.consec
    print ("consec = ",consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    pdf = PDFDespacho(tipoDocId,documentoId, consec, farmaciaId, despachoId, tipoAdmision)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Sans Serif', '', 8)
    pdf.ln(7)
    linea = 7

    # Cursor Lee el despacho

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    #comando = 'select h."ordenDeControl" orden from clinico_historia h where h.id = ' + "'" + str(historiaId) + "'"
    comando = 'select disp.id item, desp.id despacho, disp."dosisCantidad" dosis, disp."dosisUnidad_id" dosisUnidad, med.descripcion descripcion, disp."cantidadOrdenada" cantidad , disp.suministro_id cums , sum.nombre suministro from farmacia_farmaciadetalle fardet INNER JOIN farmacia_farmaciadespachos desp ON (desp.farmacia_id = fardet.farmacia_id ) inner join farmacia_farmaciadespachosdispensa disp on (disp."farmaciaDetalle_id" = fardet.id and disp.despacho_id = desp.id) 	inner join clinico_unidadesdemedidadosis med on (med.id = disp."dosisUnidad_id") inner join facturacion_suministros sum on (sum.id =  disp.suministro_id) where fardet.farmacia_id = ' + "'" + str(farmaciaId) + "'" + ' and desp.id = ' + "'" + str(despachoId) + "'"


    curt.execute(comando)

    print(comando)

    despacho = []

    for item, despacho, dosis, dosisUnidad, descripcion, cantidad,  cums, suministro  in curt.fetchall():
        despacho.append(
            {'item': item, 'despacho':despacho, 'dosis':dosis, 'dosisUnidad':dosisUnidad,'descripcion':descripcion,'cantidad':cantidad,'cums':cums,'suministro':suministro  })
    miConexiont.close()

    print("despacho = ", despacho)
    print("matriz despacho = ", len(despacho))

    if (despacho != []):
        linea = linea + 2
        pdf.ln(2)
        pdf.set_font('Sans Serif', 'B', 8)
        pdf.cell(180, 10, 'DESPACHO', 0, 0, 'C')
        pdf.set_font('Sans Serif', '', 8)
        pdf.ln(4)

    for l in range(0, len(despacho)):
        self.cell(25, 10, despacho[0]['despacho'], 0, 0, 'L')
        self.cell(25, 10, despacho[0]['item'], 0, 0, 'L')
        self.cell(25, 10, despacho[0]['dosis'], 0, 0, 'L')
        self.cell(25, 10, despacho[0]['dosisUnidad'], 0, 0, 'L')
        self.cell(25, 10, despacho[0]['descripcion'], 0, 0, 'L')
        self.cell(25, 10, despacho[0]['cums'], 0, 0, 'L')
        suministro=str(despacho[0 + l]['suministro'])
        pdf.multi_cell(w=0, h=3, txt=suministro, border=0, align='J', fill=False)
        self.cell(25, 10, despacho[0]['cantidad'], 0, 0, 'L')
        pdf.ln(4)

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\Despachos\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + str(fdespachoId) + '_' + 'Despacho.pdf'

    print ("archivo =" , archivo)

    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')

        buff = BytesIO()
        buff.name = archivo
        #Genera el archivo el el servidor

        pdf.output(archivo, 'F')


        # 2. Abrir el archivo PDF y leerlo
        with open(archivo, 'rb') as f:
            pdf_data = f.read()
            # 3. Escribir los datos en el buffer
            buff.write(pdf_data)

        buff.seek(0)

        return FileResponse(
            buff,
            as_attachment=True,  # Cambiar a False para verlo en navegador
            filename=archivo,
            content_type='application/pdf'
        )


    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': True, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        #return HttpResponse(json_data, content_type='application/json')


    return JsonResponse({'success': True, 'message': 'Orden De COntrol impresa!'})