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

# import onnx as onnx
# import onnxruntime as ort
import pyttsx3
import speech_recognition as sr
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.utils.timezone import now
from django.db.models import Avg, Max, Min
from .forms import historiaForm, historiaExamenesForm
from datetime import datetime
from clinico.models import Historia, HistoriaExamenes, Examenes, TiposExamen, EspecialidadesMedicos, Medicos, Especialidades, TiposFolio, CausasExterna, EstadoExamenes, HistorialAntecedentes, HistorialDiagnosticos, HistorialInterconsultas, EstadosInterconsulta, HistorialIncapacidades,  HistoriaSignosVitales, HistoriaRevisionSistemas, HistoriaMedicamentos
from sitios.models import Dependencias
from planta.models import Planta
from facturacion.models import Liquidacion, LiquidacionDetalle, Suministros, TiposSuministro
#from contratacion.models import Procedimientos
from usuarios.models import Usuarios, TiposDocumento
from cartera.models  import Pagos
from autorizaciones.models import Autorizaciones,AutorizacionesDetalle, EstadosAutorizacion
from contratacion.models import Convenios
from cirugia.models import EstadosCirugias, EstadosProgramacion
from tarifarios.models import TarifariosDescripcion, TarifariosProcedimientos, TarifariosSuministros
from clinico.forms import  IncapacidadesForm, HistorialDiagnosticosCabezoteForm, HistoriaSignosVitalesForm
from django.db.models import Avg, Max, Min , Sum
from usuarios.models import Usuarios, TiposDocumento
from admisiones.models import Ingresos
from farmacia.models import Farmacia, FarmaciaDetalle, FarmaciaEstados
from enfermeria.models import Enfermeria, EnfermeriaDetalle
from facturacion.models import ConveniosPacienteIngresos
from triage.models import Triage
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
import cgi
from django.db import transaction

import os
from django.http import FileResponse
from io import BytesIO
import io


class PDF(FPDF):
    def __init__(self, tipoDocId,documentoId, consec, esTriage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.esTriage = esTriage
        print("Entre a la def de la clase")


    def header(self):
        # Logo
        print("Entre al HEADER")
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 170 ,15, 10 , 5)
        # Arial bold 15
        self.set_font('Times', 'B', 7)

        # Move to the right
        #self.cell(12)


        convenioId = ConveniosPacienteIngresos.objects.filter(tipoDoc_id=self.tipoDocId,documento_id=self.documentoId,consecAdmision=self.consec).aggregate(Max('convenio_id'))

        print("convenioId = ", convenioId['convenio_id__max'])
        convenio = convenioId['convenio_id__max']

	    ## CURSOR PARA LEER ENCABEZADO
        #
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",   password="123456")

        curt = miConexiont.cursor()

        if (self.esTriage == 'N'):

            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, u.documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str('M') + "'" + ' then ' + "'" + str('Masculino') + "'" + ' when genero= ' + "'" + str('F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, cast((date_part(' + "'" + str('year') + "'" + ', now()) - date_part(' + "'" + str('year') + "'" + ', u."fechaNacio" )) as text) edad,   reg.nombre regimen, convenio.nombre convenio , serv.nombre servicio, cast(now() as text) fecha from admisiones_ingresos adm INNER JOIN 	usuarios_usuarios u ON (u."tipoDoc_id" = adm."tipoDoc_id" and u.id = adm.documento_id) INNER JOIN usuarios_tiposDocumento tip ON (tip.id = u."tipoDoc_id") INNER JOIN facturacion_conveniospacienteingresos  convIngreso ON (convIngreso."tipoDoc_id" = adm."tipoDoc_id" and convIngreso.documento_id = adm.documento_id and convIngreso."consecAdmision" = adm.consec) INNER JOIN contratacion_convenios convenio ON (convenio.id = convIngreso.convenio_id) INNER JOIN facturacion_empresas EMP on (emp.id =convenio.empresa_id ) LEFT JOIN clinico_regimenes reg ON (reg.id=emp.regimen_id) INNER JOIN sitios_serviciossedes serv ON (serv.id = adm."serviciosActual_id")	 WHERE adm."tipoDoc_id" = ' + "'" + str(self.tipoDocId) + "'" + ' AND adm.documento_id= ' + "'" + str(self.documentoId) + "'" + ' AND adm.consec = '  + "'" +str(self.consec) + "'" + ' and convenio.id = ' + "'" + str(convenio) + "'"
        else:
            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, u.documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str('M') + "'" + ' then ' + "'" + str('Masculino') + "'" + ' when genero= ' + "'" + str('F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, cast((date_part(' + "'" + str('year') + "'" + ', now()) - date_part(' + "'" + str('year') + "'" + ', u."fechaNacio" )) as text) edad,   reg.nombre regimen, convenio.nombre convenio , serv.nombre servicio, cast(now() as text) fecha from triage_triage tri INNER JOIN 	usuarios_usuarios u ON (u."tipoDoc_id" = tri."tipoDoc_id" and u.id = tri.documento_id) INNER JOIN usuarios_tiposDocumento tip ON (tip.id = u."tipoDoc_id") INNER JOIN facturacion_conveniospacienteingresos  convIngreso ON (convIngreso."tipoDoc_id" = tri."tipoDoc_id" and convIngreso.documento_id = tri.documento_id and convIngreso."consecAdmision" = tri.consec) INNER JOIN contratacion_convenios convenio ON (convenio.id = convIngreso.convenio_id) INNER JOIN facturacion_empresas EMP on (emp.id =convenio.empresa_id ) LEFT JOIN clinico_regimenes reg ON (reg.id=emp.regimen_id) INNER JOIN sitios_serviciossedes serv ON (serv.id = tri."serviciosSedes_id")	 WHERE tri."tipoDoc_id" = ' + "'" + str(self.tipoDocId) + "'" + ' AND tri.documento_id= ' + "'" + str(self.documentoId) + "'" + ' AND tri.consec = '  + "'" +str(self.consec) + "'" + ' and convenio.id = ' + "'" + str(convenio) + "'"
            print("Entre es triage")

        curt.execute(comando)
        print(comando)

        historia = []

        for tipoDoc_id, tipnombre, documentoPaciente, nombre, genero, edad, regimen, convenio, servicio, fecha  in curt.fetchall():
            historia.append(
                {'tipoDoc_id': tipoDoc_id, 'tipnombre': tipnombre, 'documentoPaciente': documentoPaciente,
                 'nombre': nombre, 'genero': genero, 'edad': edad, 'regimen': regimen, 'convenio': convenio, 'servicio': servicio,'fecha':fecha})

        miConexiont.close()

	## FIN CURSOR

        # Title
        #
        self.ln(2)
        self.cell(195, 1, 'CLINICA MEDICAL',  0, 0, 'C')
        self.ln(3)
        self.cell(195, 1, 'HISTORIA CLINICA', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.4)
        self.rect(10.0, 15.0, 195.0, 270.0)  # Coordenadas x, y, ancho, alto

        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Times', 'B', 7)
        self.cell(25, 11, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Times', '', 7)

        self.cell(25, 11, str(historia[0]['tipnombre']), 0, 0, 'L')
        self.cell(25, 11, str(historia[0]['documentoPaciente']), 0, 0, 'L')
        self.cell(25, 11, str(historia[0]['nombre']), 0, 0, 'L')
        self.ln(1)
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'EDAD:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, str(historia[0]['edad']), 0, 0, 'L')
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'GENERO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, str(historia[0]['genero']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 18, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 18, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 20, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 20, historia[0]['convenio'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 21, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 21, historia[0]['servicio'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 23, 'FECHA:', 0, 0, 'L')
        self.cell(25, 23, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(14)


    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        # Position at 3 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Times', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


class PDFOrdenIncapacidad(FPDF):
    def __init__(self, tipoDocId, documentoId, consec,historiaId ,  convenioId, tipoAdmision, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.historiaId = historiaId
        self.convenioId = convenioId
        self.tipoAdmision = tipoAdmision


    def header(self):
        # Logo
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 170 ,15, 10 , 5)
        # Arial bold 15
        self.set_font('Times', 'B', 7)

        # Move to the right
        # self.cell(12)

        #convenioId = Convenios.objects.filter(id=self.liquidacionId)

        print("convenioId = ", self.convenioId)
        convenio = self.convenioId

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
        self.rect(10.0, 15.0, 195.0, 260.0)  # Coordenadas x, y, ancho, alto
        self.ln(3)
        self.cell(195, 1, 'CLINICA MEDICAL',  0, 0, 'C')
        self.ln(3)
        self.cell(195, 1, 'INCAPACIDAD', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Times', 'B', 7)
        self.cell(25, 10, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Times', '', 7)

        self.cell(25, 10, str(historia[0]['tipnombre']), 0, 0, 'L')
        self.cell(25, 10, str(historia[0]['documentoPaciente']), 0, 0, 'L')
        self.cell(25, 10, str(historia[0]['nombre']), 0, 0, 'L')
        self.ln(1)
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'EDAD:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['edad'], 0, 0, 'L')
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'GENERO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['genero'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 18, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 18, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 20, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 20, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 21, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 21, str(historia[0]['servicio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 23, 'FECHA:', 0, 0, 'L')
        self.cell(25, 23, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(14)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        #self.set_y(-15)
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Times', 'B', 7)
        self.cell(180, 5, 'MEDICO ORDENA', 0, 0, 'C')
        self.ln(4)

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curii = miConexionii.cursor()

        comando = 'SELECT medicos."registroMedico", planta.nombre plantaNombre, usu."tipoDoc_id", usu.documento 	FROM clinico_historialincapacidades inca 	INNER JOIN clinico_historia historia ON (historia.id=inca.historia_id) 	INNER JOIN clinico_TiposIncapacidad tipo  ON (tipo.id = inca."tiposIncapacidad_id") INNER JOIN clinico_Diagnosticos diag ON (diag.id = inca."diagnosticosIncapacidad_id") INNER JOIN planta_planta planta ON (planta.id = historia."usuarioRegistro_id") INNER JOIN clinico_medicos medicos ON (medicos.planta_id = historia."usuarioRegistro_id") INNER JOIN usuarios_usuarios usu ON (usu.id = historia."usuarioRegistro_id")	WHERE inca.historia_id = ' + "'" + str(self.historiaId) +"'"

        curii.execute(comando)

        print(comando)

        incapacidadesI = []

        for registroMedico, plantaNombre, tipoDoc_id, documento in curii.fetchall():
            incapacidadesI.append(
                {'registroMedico': registroMedico, 'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id, 'documento': documento})
        miConexionii.close()

        self.set_line_width(0.4)
        self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto

        self.cell(15, 7, 'Firmado Por:', 0, 0, 'L')
        self.cell(25, 7, '' + str(incapacidadesI[0]['tipoDoc_id']), 0, 0, 'L')
        self.cell(25, 7, '' + str(incapacidadesI[0]['documento']), 0, 0, 'L')
        self.cell(80, 7, '' + str(incapacidadesI[0]['plantaNombre']), 0, 0, 'L')
        self.cell(50, 7, 'Registro Medico:' + str(incapacidadesI[0]['registroMedico']), 0, 0, 'L')

        self.ln(2)
        self.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')
        self.set_font('Times', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

class PDFOrdenLaboratorio(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, historiaId, convenioId, tipoAdmision, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.historiaId = historiaId
        self.convenioId = convenioId
        self.tipoAdmision = tipoAdmision

    def header(self):
        # Logo
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 180 ,20, 10 , 10)
        # Arial bold 15
        self.set_font('Times', 'B', 7)

        # Move to the right
        # self.cell(12)

        convenio=self.convenioId

        print("ULTIMO valor de convenioId= ", convenio)

        ## pRIMERO AVERIGUAMOS SI ES UN TRIAGE UNA ADMISION

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
        self.cell(195, 1, 'CLINICA MEDICAL', 0, 0, 'C')
        self.ln(3)
        self.cell(195, 1, 'LABORATORIOS', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Times', 'B', 7)
        self.cell(25, 11, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Times', '', 7)

        self.cell(25, 11, historia[0]['tipnombre'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['documentoPaciente'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['nombre'], 0, 0, 'L')
        self.ln(1)
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'EDAD:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['edad'], 0, 0, 'L')
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'GENERO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, str(historia[0]['genero']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 18, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        print("regimen = ", historia[0]['regimen'])

        self.cell(50, 18, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 20, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 20, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 21, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 21, historia[0]['servicio'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 23, 'FECHA:', 0, 0, 'L')
        self.cell(25, 23, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(14)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Times', 'B', 7)
        self.cell(180, 5, 'MEDICO ORDENA', 0, 0, 'C')
        self.ln(4)

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curii = miConexionii.cursor()
        comando = 'SELECT  medicos."registroMedico", planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento FROM clinico_historiaexamenes exa INNER JOIN clinico_historia historia ON (historia.id=exa.historia_id) INNER JOIN planta_planta planta ON (planta.id = historia."usuarioRegistro_id")	INNER JOIN clinico_medicos medicos ON (medicos.planta_id = historia."usuarioRegistro_id") WHERE exa.historia_id = ' + "'" + str(self.historiaId) + "'" + ' group by "registroMedico", plantaNombre, planta."tipoDoc_id", documento'

        curii.execute(comando)

        print(comando)

        registro = []

        for registroMedico, plantaNombre, tipoDoc_id, documento in curii.fetchall():
            registro.append(
                {'registroMedico': registroMedico, 'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id, 'documento': documento})
        miConexionii.close()

        self.set_line_width(0.4)
        self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto

        print('registro =', registro)
        self.cell(15, 7, 'Firmado Por:', 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['tipoDoc_id']), 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['documento']), 0, 0, 'L')
        self.cell(80, 7, '' + str(registro[0]['plantaNombre']), 0, 0, 'L')
        self.cell(50, 7, 'Registro Medico:' + str(registro[0]['registroMedico']), 0, 0, 'L')

        self.ln(2)
        self.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')
        self.set_font('Times', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


class PDFOrdenTerapia(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, historiaId, convenioId, tipoAdmision, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.historiaId = historiaId
        self.convenioId = convenioId
        self.tipoAdmision = tipoAdmision

    def header(self):
        # Logo
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 180 ,20, 10 , 10)
        # Arial bold 15
        self.set_font('Times', 'B', 7)

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
        self.cell(195, 1, 'CLINICA MEDICAL', 0, 0, 'C')
        self.ln(3)
        self.cell(195, 1, 'TERAPIAS', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Times', 'B', 7)
        self.cell(25, 11, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Times', '', 7)

        self.cell(25, 11, historia[0]['tipnombre'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['documentoPaciente'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['nombre'], 0, 0, 'L')
        self.ln(1)
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'EDAD:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['edad'], 0, 0, 'L')
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'GENERO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, str(historia[0]['genero']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 18, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 18, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 20, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 20, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 21, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 21, historia[0]['servicio'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 23, 'FECHA:', 0, 0, 'L')
        self.cell(25, 23, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(14)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Times', 'B', 7)
        self.cell(180, 5, 'MEDICO ORDENA', 0, 0, 'C')
        self.ln(4)

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curii = miConexionii.cursor()
        comando = 'SELECT  medicos."registroMedico", planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento FROM clinico_historiaexamenes exa INNER JOIN clinico_historia historia ON (historia.id=exa.historia_id) INNER JOIN planta_planta planta ON (planta.id = historia."usuarioRegistro_id")	INNER JOIN clinico_medicos medicos ON (medicos.planta_id = historia."usuarioRegistro_id") WHERE exa.historia_id = ' + "'" + str(self.historiaId) + "'" + ' group by "registroMedico", plantaNombre, planta."tipoDoc_id", documento'

        curii.execute(comando)

        print(comando)

        registro = []

        for registroMedico, plantaNombre, tipoDoc_id, documento in curii.fetchall():
            registro.append(
                {'registroMedico': registroMedico, 'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id, 'documento': documento})
        miConexionii.close()

        self.set_line_width(0.4)
        self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto


        print('registro =', registro)
        self.cell(15, 7, 'Firmado Por:', 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['tipoDoc_id']), 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['documento']), 0, 0, 'L')
        self.cell(80, 7, '' + str(registro[0]['plantaNombre']), 0, 0, 'L')
        self.cell(50, 7, 'Registro Medico:' + str(registro[0]['registroMedico']), 0, 0, 'L')

        self.ln(2)
        self.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')
        self.set_font('Times', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


class PDFOrdenRadiologia(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, historiaId, convenioId, tipoAdmision, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.historiaId = historiaId
        self.convenioId = convenioId
        self.tipoAdmision = tipoAdmision

    def header(self):
        # Logo
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 180 ,20, 10 , 10)
        # Arial bold 15
        self.set_font('Times', 'B', 7)

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
        self.cell(195, 1, 'CLINICA MEDICAL', 0, 0, 'C')
        self.ln(3)
        self.cell(195, 1, 'RADIOLOGIA', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Times', 'B', 7)
        self.cell(25, 11, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Times', '', 7)

        self.cell(25, 11, historia[0]['tipnombre'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['documentoPaciente'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['nombre'], 0, 0, 'L')
        self.ln(1)
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'EDAD:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['edad'], 0, 0, 'L')
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'GENERO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['genero'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 18, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 18, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 20, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 20, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 21, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 21, str(historia[0]['servicio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 23, 'FECHA:', 0, 0, 'L')
        self.cell(25, 23, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(14)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Times', 'B', 7)
        self.cell(180, 5, 'MEDICO ORDENA', 0, 0, 'C')
        self.ln(4)

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curii = miConexionii.cursor()
        comando = 'SELECT  medicos."registroMedico", planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento FROM clinico_historiaexamenes exa INNER JOIN clinico_historia historia ON (historia.id=exa.historia_id) INNER JOIN planta_planta planta ON (planta.id = historia."usuarioRegistro_id")	INNER JOIN clinico_medicos medicos ON (medicos.planta_id = historia."usuarioRegistro_id") WHERE exa.historia_id = ' + "'" + str(self.historiaId) + "'" + ' group by "registroMedico", plantaNombre, planta."tipoDoc_id", documento'

        curii.execute(comando)

        print(comando)

        registro = []

        for registroMedico, plantaNombre, tipoDoc_id, documento in curii.fetchall():
            registro.append(
                {'registroMedico': registroMedico, 'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id, 'documento': documento})
        miConexionii.close()

        self.set_line_width(0.4)
        self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto

        print('registro =', registro)
        self.cell(15, 7, 'Firmado Por:', 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['tipoDoc_id']), 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['documento']), 0, 0, 'L')
        self.cell(80, 7, '' + str(registro[0]['plantaNombre']), 0, 0, 'L')
        self.cell(50, 7, 'Registro Medico:' + str(registro[0]['registroMedico']), 0, 0, 'L')

        self.ln(2)
        self.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')
        self.set_font('Times', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')



class PDFOrdenMedicamentos(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, historiaId, convenioId, tipoAdmision, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.historiaId = historiaId
        self.convenioId = convenioId
        self.tipoAdmision = tipoAdmision

    def header(self):
        # Logo
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 180 ,20, 10 , 10)
        # Arial bold 15
        self.set_font('Times', 'B', 7)

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
        self.cell(195, 1, 'CLINICA MEDICAL', 0, 0, 'C')
        self.ln(3)
        self.cell(195, 1, 'FORMULACION MEDICAMENTOS', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Times', 'B', 7)
        self.cell(25, 11, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Times', '', 7)

        self.cell(25, 11, historia[0]['tipnombre'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['documentoPaciente'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['nombre'], 0, 0, 'L')
        self.ln(1)
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'EDAD:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['edad'], 0, 0, 'L')
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'GENERO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['genero'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 18, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 18, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 20, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 20, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 21, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 21, str(historia[0]['servicio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 23, 'FECHA:', 0, 0, 'L')
        self.cell(25, 23, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(14)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Times', 'B', 7)
        self.cell(180, 5, 'MEDICO ORDENA', 0, 0, 'C')
        self.ln(4)

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curii = miConexionii.cursor()

        comando = 'SELECT  medicos."registroMedico", planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento FROM clinico_historiamedicamentos med INNER JOIN clinico_historia historia ON (historia.id=med.historia_id) INNER JOIN planta_planta planta ON (planta.id = historia."usuarioRegistro_id")	INNER JOIN clinico_medicos medicos ON (medicos.planta_id = historia."usuarioRegistro_id") WHERE med.historia_id = ' + "'" + str(self.historiaId) + "'" + ' group by "registroMedico", plantaNombre, planta."tipoDoc_id", documento'

        curii.execute(comando)

        print(comando)

        registro = []

        for registroMedico, plantaNombre, tipoDoc_id, documento in curii.fetchall():
            registro.append(
                {'registroMedico': registroMedico, 'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id, 'documento': documento})
        miConexionii.close()
        self.set_line_width(0.4)
        self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto


        print('registro =', registro)
        self.cell(15, 7, 'Firmado Por:', 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['tipoDoc_id']), 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['documento']), 0, 0, 'L')
        self.cell(80, 7, '' + str(registro[0]['plantaNombre']), 0, 0, 'L')
        self.cell(50, 7, 'Registro Medico:' + str(registro[0]['registroMedico']), 0, 0, 'L')

        self.ln(2)
        self.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')
        self.set_font('Times', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


class PDFOrdenDeControl(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, historiaId, convenioId, tipoAdmision, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.historiaId = historiaId
        self.convenioId = convenioId
        self.tipoAdmision = tipoAdmision

    def header(self):
        # Logo
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 180 ,20, 10 , 10)
        # Arial bold 15
        self.set_font('Times', 'B', 7)

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
        self.cell(195, 1, 'CLINICA MEDICAL', 0, 0, 'C')
        self.ln(3)
        self.cell(195, 1, 'ORDEN DE CONTROL', 0, 0, 'C')
        self.ln(2)
        self.set_line_width(0.5)
        self.rect(10.0, 15.0, 195.0, 20)  # Coordenadas x, y, ancho, alto

        self.set_font('Times', 'B', 7)
        self.cell(25, 11, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Times', '', 7)

        self.cell(25, 11, historia[0]['tipnombre'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['documentoPaciente'], 0, 0, 'L')
        self.cell(25, 11, historia[0]['nombre'], 0, 0, 'L')
        self.ln(1)
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'EDAD:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['edad'], 0, 0, 'L')
        self.set_font('Times', 'B', 7)
        self.cell(25, 16, 'GENERO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 16, historia[0]['genero'], 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 18, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(50, 18, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 20, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 20, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 21, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Times', '', 7)
        self.cell(25, 21, str(historia[0]['servicio']), 0, 0, 'L')
        self.ln(2)
        self.set_font('Times', 'B', 7)
        self.cell(25, 23, 'FECHA:', 0, 0, 'L')
        self.cell(25, 23, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(14)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Times', 'B', 7)
        self.cell(180, 5, 'MEDICO ORDENA', 0, 0, 'C')
        self.ln(4)

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curii = miConexionii.cursor()
        comando = 'SELECT  medicos."registroMedico", planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento FROM clinico_historia his INNER JOIN planta_planta planta ON (planta.id = his."usuarioRegistro_id")	INNER JOIN clinico_medicos medicos ON (medicos.planta_id = his."usuarioRegistro_id") WHERE his.id = ' + "'" + str(self.historiaId) + "'" + ' group by "registroMedico", plantaNombre, planta."tipoDoc_id", documento'

        curii.execute(comando)

        print(comando)

        registro = []

        for registroMedico, plantaNombre, tipoDoc_id, documento in curii.fetchall():
            registro.append(
                {'registroMedico': registroMedico, 'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id, 'documento': documento})
        miConexionii.close()

        self.set_line_width(0.4)
        self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto

        print('registro =', registro)
        self.cell(15, 7, 'Firmado Por:', 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['tipoDoc_id']), 0, 0, 'L')
        self.cell(25, 7, '' + str(registro[0]['documento']), 0, 0, 'L')
        self.cell(80, 7, '' + str(registro[0]['plantaNombre']), 0, 0, 'L')
        self.cell(50, 7, 'Registro Medico:' + str(registro[0]['registroMedico']), 0, 0, 'L')

        self.ln(2)
        self.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')
        self.set_font('Times', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def ImprimirHistoriaClinica(request):
    # Instantiation of inherited class
    print("Entre ImprimirHistoriaClinica ")

    ingresoId = request.POST["ingresoId"]
    #print("ingresoId = ", ingresoId)

    print("ingresoId = ", ingresoId)
    llave = ingresoId.split('-')
    print("llave = ", llave)
    print("primero=", llave[0])
    print("segundo = ", llave[1])

    estriage='N'
    if (llave[1] == 'INGRESO'):
        ingresoPaciente = Ingresos.objects.get(id=llave[0])
        estriage='N'

    if (llave[1] == 'TRIAGE'):
        ingresoPaciente = Triage.objects.get(id=llave[0])
        estriage='S'

    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)

    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)

    consec =  ingresoPaciente.consec
    print ("consec = ",consec)

    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    pdf = PDF(tipoDocId,documentoId, consec, estriage)

    pdf.add_page()

    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    print("LISTO 1.5")
    pdf.set_font('Times', '', 8)
    print("LISTO 2")
    pdf.ln(5)
    linea = 5
    totalFolios = 20

    print ("LISTO 3")

    # El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

    # Cursor recorre Folios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select  h.id HistoriaId, h.folio folioId, h.fecha fechaFolio, tip.nombre tipoFolio from clinico_historia h left join clinico_tiposfolio tip ON (tip.id = h."tiposFolio_id" ) where h.documento_id = ' + "'" + str(documentoId) + "'" + ' order by h.id'
    curt.execute(comando)
    #print(comando)

    folios = []

    for HistoriaId, folioId, fechaFolio, tipoFolio in curt.fetchall():
        folios.append(
            {'HistoriaId': HistoriaId, 'folioId': folioId, 'fechaFolio': fechaFolio, 'tipoFolio': tipoFolio})
    miConexiont.close()

    for i in range(0, len(folios)):

        pdf.set_line_width(0.3)
        #pdf.rect(10.0, 43.0, 195.0, 5)  # Coordenadas x, y, ancho, alto


        pdf.cell(1, 1,
                 '_________________________________________________________________________________________________________________________________________',
                 0, 0, 'L')
        pdf.cell(20, 7, 'Folio No ' + str(folios[0 + i]['folioId']), 0, 0, 'L')
        pdf.cell(80, 7, 'Fecha: ' + str(folios[0 + i]['fechaFolio']), 0, 0, 'L')
        pdf.cell(25, 7, 'Tipo Folio: ' + str(folios[0 + i]['tipoFolio']), 0, 0, 'L')

        print("linea = ", linea)
        linea = linea + 1
        pdf.ln(1)
        pdf.cell(1, 10,
                 '_________________________________________________________________________________________________________________________________________',
                 0, 0, 'L')

        linea = linea + 7
        pdf.ln(8)

        # Cursor recorre basicos Historia Clinica

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select  h.motivo motivo, h.subjetivo subjetivo, h.objetivo objetivo, h.analisis analisis, h.plann plan, cau.nombre causasExterna    from clinico_historia h LEFT JOIN clinico_causasexterna cau ON (cau.id = h."causasExterna_id" )  where h.id = ' + str(folios[0 + i]['HistoriaId'])

        curt.execute(comando)

        #print(comando)

        historia = []

        for motivo, subjetivo, objetivo, analisis, plan, causasExterna in curt.fetchall():
            historia.append(
                {'motivo': motivo, 'subjetivo': subjetivo, 'objetivo': objetivo, 'analisis': analisis, 'plan': plan,
                 'causasExterna': causasExterna})
        miConexiont.close()

        print("historia = ", historia)
        print("matriz historia = ", len(historia))

        for l in range(0, len(historia)):
            plan = str(historia[0 + l]['plan'])
            analisis = str(historia[0 + l]['analisis'])
            motivo =  str(historia[0 + l]['motivo'])
            pdf.cell(15, 1, 'Motivo:', '', 0, 0, 'L')
            pdf.multi_cell(w=0, h=4, txt=motivo , border=0, align='J',fill=False)
            #pdf.cell(250, 1, 'Motivo ' + str(historia[0 + l]['motivo']), 0, 0, 'L')
            pdf.ln(3)
            subjetivo =  str(historia[0 + l]['subjetivo'])
            pdf.cell(15, 1, 'Subjetivo:', '', 0, 0, 'L')
            pdf.multi_cell(w=0, h=4, txt=subjetivo , border=0, align='J',fill=False)
            #pdf.cell(250, 1, 'Subjetivo: ' + str(historia[0 + l]['subjetivo']), 0, 0, 'L')
            pdf.ln(3)
            objetivo =  str(historia[0 + l]['objetivo'])
            pdf.multi_cell(w=0, h=4, txt=objetivo , border=0, align='J',fill=False)
            #pdf.cell(250, 1, 'Objetivo: ' + str(historia[0 + l]['objetivo']), 0, 0, 'L')
            pdf.ln(3)
            pdf.cell(15, 1, 'Analisis:', '', 0, 0, 'L')
            pdf.multi_cell(w=0, h=4, txt=analisis, border=0, align='J', fill=False)
            #pdf.cell(250, 1, 'Analisis: ' + str(historia[0 + l]['analisis']), 0, 0, 'L')
            pdf.ln(3)
            pdf.cell(15,1,'Plan:','',0,0,'L')
            pdf.multi_cell(w=0, h=4, txt=plan,border=0, align='J',fill=False)
            #pdf.cell(250, 1, 'Plan: ' + str(historia[0 + l]['plan']), 0, 0, 'L')
            pdf.ln(3)
            pdf.cell(30, 1, 'CausasExterna: ' + str(historia[0 + l]['causasExterna']), 0, 0, 'L')
            linea = linea + 5
            pdf.ln(5)

            # Cursor recorre Historia Clinica ( flags de heridas , nota aclaratoria etc)

            miConexionh = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curh = miConexionh.cursor()

            comando = 'select historia.antibioticos, historia.apache2,historia."examenFisico", historia.hipotension,historia."ingestaAlcohol", 	historia.irritacion, historia.justificacion, historia.leucopenia, historia."llenadoCapilar", historia.monitoreo, 	historia."movilidadLimitada",historia.nauseas, historia.neurologia, historia."notaAclaratoria", historia.pulsos, historia."retiroPuntos", 	historia."riesgoHemodinamico", historia."riesgoVentilatorio", historia.riesgos, historia."textoNotaAclaratoria", 	historia.tratamiento, historia."trombocitopenia", historia.vomito FROm clinico_historia historia WHERE historia.id = ' + str(
                folios[0 + i]['HistoriaId']) + ' AND historia.apache2 != 0'
            curh.execute(comando)

            #print(comando)

            rasgosHistoria = []

            for antibioticos, apache2, examenFisico, hipotension, ingestaAlcohol, irritacion, justificacion, leucopenia, llenadoCapilar, monitoreo, movilidadLimitada, nauseas, neurologia, notaAclaratoria, pulsos, retiroPuntos, riesgoHemodinamico, riesgoVentilatorio, riesgos, textoNotaAclaratoria, tratamiento, trombocitopenia, vomito in curh.fetchall():
                rasgosHistoria.append(
                    {'antibioticos': antibioticos, 'apache2': apache2, 'examenFisico': examenFisico,
                     'hipotension': hipotension,
                     'ingestaAlcohol': ingestaAlcohol, 'irritacion': irritacion, 'justificacion': justificacion,
                     'leucopenia': leucopenia,
                     'llenadoCapilar': llenadoCapilar, 'monitoreo': monitoreo, 'movilidadLimitada': movilidadLimitada,
                     'nauseas': nauseas,
                     'neurologia': neurologia, 'notaAclaratoria': notaAclaratoria, 'pulsos': pulsos,
                     'retiroPuntos': retiroPuntos,
                     'riesgoHemodinamico': riesgoHemodinamico, 'riesgoVentilatorio': riesgoVentilatorio,
                     'riesgos': riesgos, 'textoNotaAclaratoria': textoNotaAclaratoria,
                     'tratamiento': tratamiento, 'trombocitopenia': trombocitopenia, 'vomito': vomito})
            miConexionh.close()
            print("rasgosHistoria = ", rasgosHistoria)
            print("matriz rasgosHistoria = ", len(rasgosHistoria))

            if (rasgosHistoria != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'RASGOS HISTORIA', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(rasgosHistoria)):
                pdf.cell(20, 1, 'Antibioticos ' + str(rasgosHistoria[0 + l]['antibioticos']), 0, 0, 'L')
                pdf.cell(20, 1, 'Apache2: ' + str(rasgosHistoria[0 + l]['apache2']), 0, 0, 'L')
                pdf.cell(100, 1, 'ExamenFisico: ' + str(rasgosHistoria[0 + l]['examenFisico']), 0, 0, 'L')
                pdf.cell(20, 1, 'Hipotension: ' + str(rasgosHistoria[0 + l]['hipotension']), 0, 0, 'L')
                pdf.cell(20, 1, 'IngestaAlcohol: ' + str(rasgosHistoria[0 + l]['ingestaAlcohol']), 0, 0, 'L')
                linea = linea + 4
                pdf.ln(4)

                pdf.cell(20, 1, 'Irritacion: ' + str(rasgosHistoria[0 + l]['irritacion']), 0, 0, 'L')
                pdf.cell(100, 1, 'Justificacion: ' + str(rasgosHistoria[0 + l]['justificacion']), 0, 0, 'L')
                pdf.cell(20, 1, 'Leucopenia: ' + str(rasgosHistoria[0 + l]['leucopenia']), 0, 0, 'L')
                pdf.cell(20, 1, 'LlenadoCapilar: ' + str(rasgosHistoria[0 + l]['llenadoCapilar']), 0, 0, 'L')
                pdf.cell(20, 1, 'Monitoreo: ' + str(rasgosHistoria[0 + l]['monitoreo']), 0, 0, 'L')
                linea = linea + 4
                pdf.ln(4)

                pdf.cell(100, 1, 'MovilidadLimitada: ' + str(rasgosHistoria[0 + l]['movilidadLimitada']), 0, 0, 'L')
                pdf.cell(20, 1, 'Neurologia: ' + str(rasgosHistoria[0 + l]['neurologia']), 0, 0, 'L')
                pdf.cell(2, 1, 'NotaAclaratoria: ' + str(rasgosHistoria[0 + l]['notaAclaratoria']), 0, 0, 'L')
                linea = linea + 4
                pdf.ln(4)
                pdf.cell(20, 1, 'Pulsos: ' + str(rasgosHistoria[0 + l]['pulsos']), 0, 0, 'L')
                pdf.cell(20, 1, 'RetiroPuntos: ' + str(rasgosHistoria[0 + l]['retiroPuntos']), 0, 0, 'L')
                pdf.cell(50, 1, 'RiesgoHemodinamico: ' + str(rasgosHistoria[0 + l]['riesgoHemodinamico']), 0, 0, 'L')
                pdf.cell(100, 1, 'Riesgos: ' + str(rasgosHistoria[0 + l]['riesgos']), 0, 0, 'L')
                linea = linea + 4
                pdf.ln(4)
                pdf.cell(500, 1, 'NotaAclaratoria: ' + str(rasgosHistoria[0 + l]['textoNotaAclaratoria']), 0, 0, 'L')
                pdf.cell(100, 1, 'Tratamiento: ' + str(rasgosHistoria[0 + l]['tratamiento']), 0, 0, 'L')
                pdf.cell(20, 1, 'Trombocitopenia: ' + str(rasgosHistoria[0 + l]['trombocitopenia']), 0, 0, 'L')
                pdf.cell(20, 1, 'Vomito: ' + str(rasgosHistoria[0 + l]['vomito']), 0, 0, 'L')

                linea = linea + 3
                pdf.ln(3)

            # Cursor recorre Revision x Sistemas

            miConexionr = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curr = miConexionr.cursor()

            comando = 'SELECT revision.nombre sistema, hist.observacion observacion FROM clinico_historiarevisionsistemas hist INNER JOIN clinico_revisionsistemas revision  ON (revision.id = hist."revisionSistemas_id") WHERE hist.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            curr.execute(comando)

            #print(comando)

            revisionSistemas = []

            for sistema, observacion in curr.fetchall():
                revisionSistemas.append(
                    {'sistema': sistema, 'observacion': observacion})
            miConexionr.close()

            print("revisionSistemas = ", revisionSistemas)
            print("matriz revisionSistemas = ", len(revisionSistemas))

            if (revisionSistemas != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'REVISION POR SISTEMAS', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(revisionSistemas)):

                sistema =  str(revisionSistemas[0 + l]['sistema'])
                pdf.multi_cell(w=0, h=4, txt=sistema , border=0, align='J',fill=False)
                #pdf.cell(50, 1, 'Sistema ' + str(revisionSistemas[0 + l]['sistema']), 0, 0, 'L')
                observacion =  str(revisionSistemas[0 + l]['observacion'])
                pdf.multi_cell(w=0, h=4, txt=observacion , border=0, align='J',fill=False)
                #pdf.cell(100, 1, 'Observacion: ' + str(revisionSistemas[0 + l]['observacion']), 0, 0, 'L')

                linea = linea + 3
                pdf.ln(3)

            # Cursor recorre Antecedentes

            miConexiond = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curd = miConexiond.cursor()

            comando = 'SELECT antecedente.nombre antecedente, histAntecedente.descripcion descripcion FROM clinico_historialantecedentes histAntecedente INNER JOIN clinico_tiposantecedente antecedente  ON (antecedente.id = histAntecedente."tiposAntecedente_id") WHERE histAntecedente.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            curd.execute(comando)

            print(comando)

            antecedentes = []

            for antecedente, descripcion in curd.fetchall():
                antecedentes.append(
                    {'antecedente': antecedente, 'descripcion': descripcion})
            miConexiond.close()

            print("antecedentes = ", antecedentes)
            print("matriz antecedentes = ", len(antecedentes))

            if (antecedentes != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'ANTECEDENTES', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(antecedentes)):
                pdf.cell(50, 1, 'antecedente ' + str(antecedentes[0 + l]['antecedente']), 0, 0, 'L')
                descripcion =  str(antecedentes[0 + l]['descripcion'])
                pdf.multi_cell(w=0, h=4, txt=descripcion , border=0, align='J',fill=False)
                #pdf.cell(100, 1, 'Descripcion: ' + str(antecedentes[0 + l]['descripcion']), 0, 0, 'L')

                linea = linea + 3
                pdf.ln(3)

            # Cursor recorre Signos vitales

            miConexione = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cure = miConexione.cursor()

            comando = 'SELECT to_char(signos.fecha, ' + "'" + str(
                'YYYY-MM-DD HH:MM') + "') fecha" + ' ,signos."frecCardiaca", signos."frecRespiratoria", signos."tensionADiastolica", signos."tensionASistolica", 	signos."tensionAMedia", signos.temperatura, signos.saturacion, signos.glucometria, signos.glasgow, signos.apache, signos.pvc, 	signos.cuna, signos.ic, signos."glasgowOcular", signos."glasgowVerbal", signos."glasgowMotora", signos.observacion FROM clinico_historiasignosvitales  signos WHERE signos.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            cure.execute(comando)

            #print(comando)

            signosVitales = []

            for fecha, frecCardiaca, frecRespiratoria, tensionADiastolica, tensionASistolica, tensionAMedia, temperatura, saturacion, glucometria, glasgow, apache, pvc, cuna, ic, glasgowOcular, glasgowVerbal, glasgowMotora, observacion in cure.fetchall():
                signosVitales.append(
                    {'fecha': fecha, 'frecCardiaca': frecCardiaca, 'frecRespiratoria': frecRespiratoria,
                     'tensionADiastolica': tensionADiastolica, 'tensionASistolica': tensionASistolica,
                     'tensionAMedia': tensionAMedia, 'temperatura': temperatura, 'saturacion': saturacion,
                     'glucometria': glucometria, 'glasgow': glasgow, 'apache': apache, 'pvc': pvc, 'cuna': cuna,
                     'ic': ic, 'glasgowOcular': glasgowOcular, 'glasgowVerbal': glasgowVerbal,
                     'glasgowMotora': glasgowMotora, 'observacion': observacion})
            miConexione.close()

            print("signosVitales = ", signosVitales)
            print("matriz signosVitales = ", len(signosVitales))

            if (signosVitales != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'SIGNOS VITALES', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(signosVitales)):
                pdf.cell(30, 1, 'Fecha ' + str(signosVitales[0 + l]['fecha']), 0, 0, 'L')
                pdf.cell(30, 1, 'FrecCardiaca: ' + str(signosVitales[0 + l]['frecCardiaca']), 0, 0, 'L')
                pdf.cell(30, 1, 'FrecRespiratoria ' + str(signosVitales[0 + l]['frecRespiratoria']), 0, 0, 'L')
                pdf.cell(30, 1, 'TensionADiastolica ' + str(signosVitales[0 + l]['tensionADiastolica']), 0, 0, 'L')
                pdf.cell(30, 1, 'Tempreatura ' + str(signosVitales[0 + l]['temperatura']), 0, 0, 'L')
                pdf.cell(30, 1, 'Saturacion ' + str(signosVitales[0 + l]['saturacion']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)
                pdf.cell(30, 1, 'Glucometria ' + str(signosVitales[0 + l]['glucometria']), 0, 0, 'L')
                pdf.cell(30, 1, 'Glasgow ' + str(signosVitales[0 + l]['glasgow']), 0, 0, 'L')
                pdf.cell(30, 1, 'apache ' + str(signosVitales[0 + l]['apache']), 0, 0, 'L')
                pdf.cell(30, 1, 'pvc ' + str(signosVitales[0 + l]['pvc']), 0, 0, 'L')
                pdf.cell(30, 1, 'Cuna ' + str(signosVitales[0 + l]['cuna']), 0, 0, 'L')
                pdf.cell(30, 1, 'Ic ' + str(signosVitales[0 + l]['ic']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)
                pdf.cell(30, 1, 'GlasgowOcular ' + str(signosVitales[0 + l]['glasgowOcular']), 0, 0, 'L')
                pdf.cell(30, 1, 'GlasgowVerbal ' + str(signosVitales[0 + l]['glasgowVerbal']), 0, 0, 'L')
                pdf.cell(30, 1, 'GlasgowMotora ' + str(signosVitales[0 + l]['glasgowMotora']), 0, 0, 'L')
                pdf.cell(30, 1, 'Observacion ' + str(signosVitales[0 + l]['observacion']), 0, 0, 'L')

                linea = linea + 3
                pdf.ln(3)

            # Cursor recorre Notas de Enfermeria

            miConexione = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            cure = miConexione.cursor()

            comando = 'SELECT to_char(notas."fechaRegistro", ' + "'" + str(
                'YYYY-MM-DD HH:MM') + "') fecha" + ' ,notas.observaciones nota  FROM clinico_historialnotasenfermeria  notas WHERE notas.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            cure.execute(comando)

            #print(comando)

            notasEnfermeria = []

            for fecha, nota in cure.fetchall():
                notasEnfermeria.append(
                    {'fecha': fecha, 'nota': nota})
            miConexione.close()

            print("notasEnfermeria = ", notasEnfermeria)
            print("matriz notasEnfermeria = ", len(notasEnfermeria))

            if (notasEnfermeria != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'NOTAS ENFERMERIA', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(notasEnfermeria)):
                pdf.cell(30, 1, 'Fecha ' + str(notasEnfermeria[0 + l]['fecha']), 0, 0, 'L')
                nota =  str(notasEnfermeria[0 + l]['nota'])
                pdf.multi_cell(w=0, h=4, txt=nota , border=0, align='J',fill=False)
                #pdf.cell(30, 1, '  ' + str(notasEnfermeria[0 + l]['nota']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)

            # Cursor recorre Oxigeno

            # Cursor recorre Recomendaciones

            # Cursor recorre Laboratorios

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curt = miConexiont.cursor()

            comando = 'select h.id id, h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%LABORATO%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            curt.execute(comando)

            #print(comando)

            laboratorios = []

            for id, codigoCups, nombre, cantidad, observaciones in curt.fetchall():
                laboratorios.append(
                    {'id':id, 'codigoCups': codigoCups, 'nombre': nombre, 'cantidad': cantidad, 'observaciones': observaciones})
            miConexiont.close()

            print("laboratorios = ", laboratorios)
            print("matriz laboratorios = ", len(laboratorios))

            if (laboratorios != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'LABORATORIOS', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(laboratorios)):
                pdf.cell(20, 1, 'Cups ' + str(laboratorios[0 + l]['codigoCups']), 0, 0, 'L')
                pdf.cell(100, 1, 'Nombre: ' + str(laboratorios[0 + l]['nombre']), 0, 0, 'L')
                pdf.cell(25, 1, 'Cantidad: ' + str(laboratorios[0 + l]['cantidad']), 0, 0, 'L')
                pdf.cell(25, 1, 'Observacion: ' + str(laboratorios[0 + l]['observaciones']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)

                ## Aqui cabezote del resultado laboratoiro

                miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                               password="123456")
                cury = miConexiony.cursor()
                #comando ='SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", med.nombre medico FROM clinico_historiaexamenes hisExa INNER JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) WHERE hisExa.historia_id = ' + "'" + str(folios[0 + i]['HistoriaId']) + "'"
                comando = 'SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", pla.nombre medicoInterpreta1, hisExa.interpretacion2, hisExa."fechaInterpretacion2", pla.nombre medicoInterpreta2 FROM clinico_historiaexamenes hisExa LEFT JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") LEFT  JOIN  clinico_medicos med2 ON (med2.id = hisExa."medicoInterpretacion2_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) LEFT JOIN planta_planta pla ON (pla.id=med.planta_id) LEFT JOIN planta_planta pla2 ON (pla2.id=med2.planta_id) WHERE hisExa.id = ' + "'" + str(laboratorios[0 + l]['id'])  + "'"

                print(comando)
                cury.execute(comando)

                resultadosCabezoteLab = []

                for interpretacion1, fechaInterpretacion1, medicoInterpreta1, interpretacion2, fechaInterpretacion2, medicoInterpreta2   in cury.fetchall():
                    resultadosCabezoteLab.append(
                        {'interpretacion1': interpretacion1, 'fechaInterpretacion1': fechaInterpretacion1, 'medicoInterpreta1': medicoInterpreta1,
                         'interpretacion2': interpretacion2, 'fechaInterpretacion2': fechaInterpretacion2, 'medicoInterpreta2': medicoInterpreta2
                         })
                miConexiony.close()


                print("Resultados  resultadosCabezoteLab  = ", resultadosCabezoteLab)

                print("matriz Resultados laboratorios = ", len(resultadosCabezoteLab))


                if (resultadosCabezoteLab != []):
                    linea = linea + 2
                    pdf.ln(2)
                    pdf.cell(180, 1, 'Resultados Grales:', 0, 0, 'L')
                    linea = linea + 4
                    pdf.ln(4)

                    for s in range(0, len(resultadosCabezoteLab)):
                        interpretacion1=str(resultadosCabezoteLab[0 + s]['interpretacion1'])
                        pdf.cell(20, 1, 'Interprestacion1:', '', 0, 0, 'L')
                        pdf.multi_cell(w=0, h=4, txt=interpretacion1, border=0, align='J', fill=False)
                        #pdf.cell(120, 1, 'Interpretacion1 ' + str(resultadosCabezoteLab[0 + s]['interpretacion1']), 0, 0, 'L')
                        linea = linea + 3
                        pdf.ln(3)
                        pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteLab[0 + s]['fechaInterpretacion1']), 0, 0, 'L')
                        linea = linea + 3
                        pdf.ln(3)
                        pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteLab[0 + s]['medicoInterpreta1']), 0, 0, 'L')
                        linea = linea + 3
                        pdf.ln(5)
                        interpretacion2=str(resultadosCabezoteLab[0 + s]['interpretacion2'])
                        pdf.multi_cell(w=0, h=4, txt=interpretacion2, border=0, align='J', fill=False)
                        #pdf.cell(120, 1, 'Interpretacion2' + str(resultadosCabezoteLab[0 + s]['interpretacion2']), 0, 0, 'L')
                        linea = linea + 3
                        pdf.ln(3)
                        pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteLab[0 + s]['fechaInterpretacion2']), 0, 0, 'L')
                        linea = linea + 3
                        pdf.ln(3)

                        pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteLab[0 + s]['medicoInterpreta2']), 0, 0, 'L')

                        linea = linea + 4
                        pdf.ln(4)

                    ## Fin cabezote

                # Aquip Resultados del LABORATORIO

                miConexionp = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                               password="123456")
                curp = miConexionp.cursor()

                comando = 'select rasgos.nombre rasgo, rasgos.unidad unidad, rasgos.minimo minimo , rasgos.maximo maximo,histresul.valor valor FROM clinico_historiaresultados histresul INNER JOIN 	clinico_historiaexamenes histExa on (histExa.id=histresul."historiaExamenes_id" and histExa."codigoCups" = ' + "'" + str(
                    laboratorios[0 + l][
                        'codigoCups']) + "'" + ') INNER JOIN clinico_historia historia on (historia.id = histExa.historia_id ) INNER JOIN clinico_examenesrasgos rasgos ON (rasgos.id=histresul."examenesRasgos_id") where historia.id = ' + "'" + str(
                    folios[0 + i]['HistoriaId']) + "'"

                curp.execute(comando)

                #print(comando)

                resultadosLab = []

                for rasgo, unidad, minimo, maximo, valor in curp.fetchall():
                    resultadosLab.append(
                        {'rasgo': rasgo, 'unidad': unidad, 'minimo': minimo, 'maximo': maximo, 'valor': valor})
                miConexionp.close()

                print("Resultados laboratorios = ", resultadosLab)
                print("matriz Resultados laboratorios = ", len(resultadosLab))

                if (resultadosLab != []):
                    linea = linea + 2
                    pdf.ln(2)
                    pdf.cell(180, 1, 'Resultados:', 0, 0, 'L')
                    linea = linea + 4
                    pdf.ln(4)

                for s in range(0, len(resultadosLab)):
                    pdf.cell(70, 1, 'Rasgo ' + str(resultadosLab[0 + s]['rasgo']), 0, 0, 'L')
                    pdf.cell(40, 1, 'Unidad: ' + str(resultadosLab[0 + s]['unidad']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Minimo: ' + str(resultadosLab[0 + s]['minimo']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Maximo: ' + str(resultadosLab[0 + s]['maximo']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Valor: ' + str(resultadosLab[0 + s]['valor']), 0, 0, 'L')
                    linea = linea + 5
                    pdf.ln(5)

                miConexionp.close()

                # Fin impresion de Resultados der Laboratorio

            # Cursor recorre Radiologia

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curt = miConexiont.cursor()

            comando = 'select h.id id ,h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%RAD%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            curt.execute(comando)

            #print(comando)

            radiologia = []

            for id,codigoCups, nombre, cantidad, observaciones in curt.fetchall():
                radiologia.append(
                    {'id':id, 'codigoCups': codigoCups, 'nombre': nombre, 'cantidad': cantidad, 'observaciones': observaciones})
            miConexiont.close()

            print("Radiologia = ", radiologia)
            print("matriz Radiologia = ", len(radiologia))

            if (radiologia != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'RADIOLOGIA', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(radiologia)):
                pdf.cell(20, 1, 'Cups ' + str(radiologia[0 + l]['codigoCups']), 0, 0, 'L')
                pdf.cell(100, 1, 'Nombre: ' + str(radiologia[0 + l]['nombre']), 0, 0, 'L')
                pdf.cell(25, 1, 'Cantidad: ' + str(radiologia[0 + l]['cantidad']), 0, 0, 'L')
                pdf.cell(25, 1, 'Observacion: ' + str(radiologia[0 + l]['observaciones']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)

                ## Aqui cabezote del resultado Radiologia

                miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                               password="123456")
                cury = miConexiony.cursor()
                #comando ='SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", med.nombre medico FROM clinico_historiaexamenes hisExa INNER JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) WHERE hisExa.historia_id = ' + "'" + str(folios[0 + i]['HistoriaId']) + "'"
                comando = 'SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", pla.nombre medicoInterpreta1, hisExa.interpretacion2, hisExa."fechaInterpretacion2", pla.nombre medicoInterpreta2 FROM clinico_historiaexamenes hisExa LEFT JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") LEFT  JOIN  clinico_medicos med2 ON (med2.id = hisExa."medicoInterpretacion2_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) LEFT JOIN planta_planta pla ON (pla.id=med.planta_id) LEFT JOIN planta_planta pla2 ON (pla2.id=med2.planta_id) WHERE hisExa.id = ' + "'" + str(radiologia[0 + l]['id'])  + "'"

                #print(comando)
                cury.execute(comando)

                resultadosCabezoteRad = []

                for interpretacion1, fechaInterpretacion1, medicoInterpreta1, interpretacion2, fechaInterpretacion2, medicoInterpreta2   in cury.fetchall():
                    resultadosCabezoteRad.append(
                        {'interpretacion1': interpretacion1, 'fechaInterpretacion1': fechaInterpretacion1, 'medicoInterpreta1': medicoInterpreta1,
                         'interpretacion2': interpretacion2, 'fechaInterpretacion2': fechaInterpretacion2, 'medicoInterpreta2': medicoInterpreta2
                         })
                miConexiony.close()


                print("Resultados  resultadosCabezoteRad  = ", resultadosCabezoteRad)
                print("matriz Resultados resultadosCabezoteRad = ", len(resultadosCabezoteRad))


                if (resultadosCabezoteRad != []):
                    linea = linea + 2
                    pdf.ln(2)
                    pdf.cell(180, 1, 'Resultados Grales:', 0, 0, 'L')
                    linea = linea + 4
                    pdf.ln(4)

                for s in range(0, len(resultadosCabezoteRad)):
                    interpretacion1 = str(resultadosCabezoteRad[0 + s]['interpretacion1'])
                    pdf.cell(20, 1, 'Interprestacion1:', '', 0, 0, 'L')
                    pdf.multi_cell(w=0, h=4, txt=interpretacion1, border=0, align='J', fill=False)
                    #pdf.cell(120, 1, 'Interpretacion1 ' + str(resultadosCabezoteRad[0 + s]['interpretacion1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteRad[0 + s]['fechaInterpretacion1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteRad[0 + s]['medicoInterpreta1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(5)
                    interpretacion2=str(resultadosCabezoteRad[0 + s]['interpretacion2'])
                    pdf.multi_cell(w=0, h=4, txt=interpretacion2, border=0, align='J', fill=False)
                    #pdf.cell(120, 1, 'Interpretacion2' + str(resultadosCabezoteRad[0 + s]['interpretacion2']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteRad[0 + s]['fechaInterpretacion2']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)

                    pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteRad[0 + s]['medicoInterpreta2']), 0, 0, 'L')

                    linea = linea + 4
                    pdf.ln(4)

                ## Fin cabezote



                # Aquip Resultados del RADIOLOGIA

                miConexiona = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                               password="123456")
                cura = miConexiona.cursor()

                comando = 'select rasgos.nombre rasgo, rasgos.unidad unidad, rasgos.minimo minimo , rasgos.maximo maximo,histresul.valor valor FROM clinico_historiaresultados histresul INNER JOIN 	clinico_historiaexamenes histExa on (histExa.id=histresul."historiaExamenes_id" and histExa."codigoCups" = ' + "'" + str(
                    radiologia[0 + l][
                        'codigoCups']) + "'" + ') INNER JOIN clinico_historia historia on (historia.id = histExa.historia_id ) INNER JOIN clinico_examenesrasgos rasgos ON (rasgos.id=histresul."examenesRasgos_id") where historia.id = ' + "'" + str(
                    folios[0 + i]['HistoriaId']) + "'"

                cura.execute(comando)

                #print(comando)

                resultadosRad = []

                for rasgo, unidad, minimo, maximo, valor in cura.fetchall():
                    resultadosRad.append(
                        {'rasgo': rasgo, 'unidad': unidad, 'minimo': minimo, 'maximo': maximo, 'valor': valor})
                miConexiona.close()

                print("Resultados radiologia = ", resultadosRad)
                print("matriz Resultados laboratorios = ", len(resultadosRad))

                if (resultadosRad != []):
                    linea = linea + 2
                    pdf.ln(2)
                    pdf.cell(180, 1, 'Resultados:', 0, 0, 'L')
                    linea = linea + 4
                    pdf.ln(4)

                for s in range(0, len(resultadosRad)):
                    pdf.cell(70, 1, 'Rasgo ' + str(resultadosRad[0 + s]['rasgo']), 0, 0, 'L')
                    pdf.cell(40, 1, 'Unidad: ' + str(resultadosRad[0 + s]['unidad']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Minimo: ' + str(resultadosRad[0 + s]['minimo']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Maximo: ' + str(resultadosRad[0 + s]['maximo']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Valor: ' + str(resultadosRad[0 + s]['valor']), 0, 0, 'L')
                    linea = linea + 5
                    pdf.ln(5)

                # Fin impresion de Resultados de Radiologia

            # Cursor recorre Terapias

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curt = miConexiont.cursor()

            comando = 'select h.id id , h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%TERAP%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            curt.execute(comando)

            #print(comando)

            terapias = []

            for id,codigoCups, nombre, cantidad, observaciones in curt.fetchall():
                terapias.append(
                    {'id':id, 'codigoCups': codigoCups, 'nombre': nombre, 'cantidad': cantidad, 'observaciones': observaciones})
            miConexiont.close()

            print("terapias = ", terapias)
            print("matriz terapias = ", len(terapias))

            if (terapias != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'TERAPIAS', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(terapias)):
                pdf.cell(20, 1, 'Cups ' + str(terapias[0 + l]['codigoCups']), 0, 0, 'L')
                pdf.cell(100, 1, 'Nombre: ' + str(terapias[0 + l]['nombre']), 0, 0, 'L')
                pdf.cell(25, 1, 'Cantidad: ' + str(terapias[0 + l]['cantidad']), 0, 0, 'L')
                pdf.cell(25, 1, 'Observacion: ' + str(terapias[0 + l]['observaciones']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)


                ## Aqui cabezote del resultado Terapias

                miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                               password="123456")
                cury = miConexiony.cursor()
                #comando ='SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", med.nombre medico FROM clinico_historiaexamenes hisExa INNER JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) WHERE hisExa.historia_id = ' + "'" + str(folios[0 + i]['HistoriaId']) + "'"
                comando = 'SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", pla.nombre medicoInterpreta1, hisExa.interpretacion2, hisExa."fechaInterpretacion2", pla.nombre medicoInterpreta2 FROM clinico_historiaexamenes hisExa LEFT JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") LEFT  JOIN  clinico_medicos med2 ON (med2.id = hisExa."medicoInterpretacion2_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) LEFT JOIN planta_planta pla ON (pla.id=med.planta_id) LEFT JOIN planta_planta pla2 ON (pla2.id=med2.planta_id) WHERE hisExa.id = ' + "'" + str(terapias[0 + l]['id'])  + "'"

                #print(comando)
                cury.execute(comando)

                resultadosCabezoteTer = []

                for interpretacion1, fechaInterpretacion1, medicoInterpreta1, interpretacion2, fechaInterpretacion2, medicoInterpreta2   in cury.fetchall():
                    resultadosCabezoteTer.append(
                        {'interpretacion1': interpretacion1, 'fechaInterpretacion1': fechaInterpretacion1, 'medicoInterpreta1': medicoInterpreta1,
                         'interpretacion2': interpretacion2, 'fechaInterpretacion2': fechaInterpretacion2, 'medicoInterpreta2': medicoInterpreta2
                         })
                miConexiony.close()


                print("Resultados  resultadosCabezoteTer  = ", resultadosCabezoteTer)
                print("matriz Resultados resultadosCabezoteTer = ", len(resultadosCabezoteTer))


                if (resultadosCabezoteTer != []):
                    linea = linea + 2
                    pdf.ln(2)
                    pdf.cell(180, 1, 'Resultados Grales:', 0, 0, 'L')
                    linea = linea + 4
                    pdf.ln(4)

                for s in range(0, len(resultadosCabezoteTer)):
                    interpretacion1=str(resultadosCabezoteTer[0 + s]['interpretacion2'])
                    pdf.multi_cell(w=0, h=4, txt=interpretacion1, border=0, align='J', fill=False)
                    #pdf.cell(120, 1, 'Interpretacion1 ' + str(resultadosCabezoteTer[0 + s]['interpretacion1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteTer[0 + s]['fechaInterpretacion1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteTer[0 + s]['medicoInterpreta1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(5)
                    interpretacion2=str(resultadosCabezoteTer[0 + s]['interpretacion2'])
                    pdf.multi_cell(w=0, h=4, txt=interpretacion2, border=0, align='J', fill=False)
                    #pdf.cell(120, 1, 'Interpretacion2' + str(resultadosCabezoteTer[0 + s]['interpretacion2']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteTer[0 + s]['fechaInterpretacion2']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)

                    pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteTer[0 + s]['medicoInterpreta2']), 0, 0, 'L')

                    linea = linea + 4
                    pdf.ln(4)

                ## Fin cabezote


                # Aquip Resultados del TERAPIAS

                miConexionb = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                               password="123456")
                curb = miConexionb.cursor()

                comando = 'select rasgos.nombre rasgo, rasgos.unidad unidad, rasgos.minimo minimo , rasgos.maximo maximo,histresul.valor valor FROM clinico_historiaresultados histresul INNER JOIN 	clinico_historiaexamenes histExa on (histExa.id=histresul."historiaExamenes_id" and histExa."codigoCups" = ' + "'" + str(
                    terapias[0 + l][
                        'codigoCups']) + "'" + ') INNER JOIN clinico_historia historia on (historia.id = histExa.historia_id ) INNER JOIN clinico_examenesrasgos rasgos ON (rasgos.id=histresul."examenesRasgos_id") where historia.id = ' + "'" + str(
                    folios[0 + i]['HistoriaId']) + "'"

                curb.execute(comando)

                #print(comando)

                resultadosTer = []

                for rasgo, unidad, minimo, maximo, valor in curb.fetchall():
                    resultadosTer.append(
                        {'rasgo': rasgo, 'unidad': unidad, 'minimo': minimo, 'maximo': maximo, 'valor': valor})
                miConexionb.close()

                print("Resultados resultadosTer = ", resultadosTer)
                print("matriz Resultados resultadosTer = ", len(resultadosTer))

                if (resultadosTer != []):
                    linea = linea + 2
                    pdf.ln(2)
                    pdf.cell(180, 1, 'Resultados:', 0, 0, 'L')
                    linea = linea + 4
                    pdf.ln(4)

                for s in range(0, len(resultadosTer)):
                    pdf.cell(70, 1, 'Rasgo ' + str(resultadosTer[0 + s]['rasgo']), 0, 0, 'L')
                    pdf.cell(40, 1, 'Unidad: ' + str(resultadosTer[0 + s]['unidad']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Minimo: ' + str(resultadosTer[0 + s]['minimo']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Maximo: ' + str(resultadosTer[0 + s]['maximo']), 0, 0, 'L')
                    pdf.cell(25, 1, 'Valor: ' + str(resultadosTer[0 + s]['valor']), 0, 0, 'L')
                    linea = linea + 5
                    pdf.ln(5)

                # Fin impresion de Resultados de Terapias

            # Cursor recorre Proc Mo qx

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curt = miConexiont.cursor()

            comando = 'select h.id,h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%NO%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            curt.execute(comando)

            #print(comando)

            noqX = []

            for id,codigoCups, nombre, cantidad, observaciones in curt.fetchall():
                noqX.append(
                    {'id':id, 'codigoCups': codigoCups, 'nombre': nombre, 'cantidad': cantidad, 'observaciones': observaciones})
            miConexiont.close()

            print("noqX = ", noqX)
            print("matriz noqX = ", len(noqX))

            if (noqX != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'PROCEDIMIENTOS NO QX', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(noqX)):
                pdf.cell(20, 1, 'Cups ' + str(noqX[0 + l]['codigoCups']), 0, 0, 'L')
                pdf.cell(100, 1, 'Nombre: ' + str(noqX[0 + l]['nombre']), 0, 0, 'L')
                pdf.cell(25, 1, 'Cantidad: ' + str(noqX[0 + l]['cantidad']), 0, 0, 'L')
                pdf.cell(25, 1, 'Observacion: ' + str(noqX[0 + l]['observaciones']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)

                print ("noQx = ",noqX )
                ## Aqui cabezote del resultado NoQx
                miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                               password="123456")
                cury = miConexiony.cursor()
                #comando ='SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", med.nombre medico FROM clinico_historiaexamenes hisExa INNER JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) WHERE hisExa.historia_id = ' + "'" + str(folios[0 + i]['HistoriaId']) + "'"
                comando = 'SELECT hisExa.interpretacion1, hisExa."fechaInterpretacion1", pla.nombre medicoInterpreta1, hisExa.interpretacion2, hisExa."fechaInterpretacion2", pla.nombre medicoInterpreta2 FROM clinico_historiaexamenes hisExa LEFT JOIN  clinico_medicos med ON (med.id = hisExa."medicoInterpretacion1_id") LEFT  JOIN  clinico_medicos med2 ON (med2.id = hisExa."medicoInterpretacion2_id") INNER JOIN clinico_historia historia on (historia.id = hisExa.historia_id ) LEFT JOIN planta_planta pla ON (pla.id=med.planta_id) LEFT JOIN planta_planta pla2 ON (pla2.id=med2.planta_id) WHERE hisExa.id = ' + "'" + str(noqX[0 + l]['id'])  + "'"

                #print(comando)
                cury.execute(comando)

                resultadosCabezoteNoQx = []

                for interpretacion1, fechaInterpretacion1, medicoInterpreta1, interpretacion2, fechaInterpretacion2, medicoInterpreta2   in cury.fetchall():
                    resultadosCabezoteNoQx.append(
                        {'interpretacion1': interpretacion1, 'fechaInterpretacion1': fechaInterpretacion1, 'medicoInterpreta1': medicoInterpreta1,
                         'interpretacion2': interpretacion2, 'fechaInterpretacion2': fechaInterpretacion2, 'medicoInterpreta2': medicoInterpreta2
                         })
                miConexiony.close()


                print("Resultados  resultadosCabezoteNoQx  = ", resultadosCabezoteNoQx)
                print("matriz Resultados resultadosCabezoteNoQx = ", len(resultadosCabezoteNoQx))


                if (resultadosCabezoteNoQx != []):
                    linea = linea + 2
                    pdf.ln(2)
                    pdf.cell(180, 1, 'Resultados Grales:', 0, 0, 'L')
                    linea = linea + 4
                    pdf.ln(4)

                for s in range(0, len(resultadosCabezoteNoQx)):
                    interpretacion2=str(resultadosCabezoteNoQx[0 + s]['interpretacion2'])
                    pdf.multi_cell(w=0, h=4, txt=interpretacion2, border=0, align='J', fill=False)
                    #pdf.cell(120, 1, 'Interpretacion1 ' + str(resultadosCabezoteNoQx[0 + s]['interpretacion1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteNoQx[0 + s]['fechaInterpretacion1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteNoQx[0 + s]['medicoInterpreta1']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(5)
                    interpretacion2=str(resultadosCabezoteNoQx[0 + s]['interpretacion2'])
                    pdf.multi_cell(w=0, h=4, txt=interpretacion2, border=0, align='J', fill=False)
                    #pdf.cell(120, 1, 'Interpretacion2' + str(resultadosCabezoteNoQx[0 + s]['interpretacion2']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)
                    pdf.cell(20, 2, 'Fecha: ' + str(resultadosCabezoteNoQx[0 + s]['fechaInterpretacion2']), 0, 0, 'L')
                    linea = linea + 3
                    pdf.ln(3)

                    pdf.cell(25, 3, 'Medico: ' + str(resultadosCabezoteNoQx[0 + s]['medicoInterpreta2']), 0, 0, 'L')

                    linea = linea + 4
                    pdf.ln(4)

                ## Fin cabezote


            # Cursor recorre Interconsultas

            miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curx = miConexionx.cursor()

            comando = 'SELECT especialidadesConsulta.nombre especialidadConsulta, plantaConsulta.nombre plantaConsulta, diag.nombre diagnostico,	inter."descripcionConsulta" descripcionConsulta, especialidadesConsultada.nombre especialidadConsultada, plantaConsultada.nombre plantaConsultada,  inter."respuestaConsulta" respuestaConsulta FROM clinico_historialinterconsultas inter INNER JOIN clinico_medicos medicosConsulta on (medicosConsulta.id = inter."medicoConsulta_id") INNER JOIN clinico_medicos medicosConsultado on (medicosConsultado.id = inter."medicoConsultado_id") INNER JOIN clinico_especialidades especialidadesConsulta ON (especialidadesConsulta.id = inter."especialidadConsulta_id" ) INNER JOIN clinico_especialidades especialidadesConsultada ON (especialidadesConsultada.id = inter."especialidadConsultada_id") INNER JOIN planta_planta plantaConsulta ON (plantaConsulta.id = medicosConsulta.planta_id) INNER JOIN planta_planta plantaConsultada ON (plantaConsultada.id = medicosConsultado.planta_id) INNER JOIN clinico_diagnosticos diag ON (diag.id = inter.diagnosticos_id) WHERE inter.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])

            curx.execute(comando)

            print(comando)

            interConsultas = []

            for especialidadConsulta, plantaConsulta, diagnostico, descripcionConsulta, especialidadConsultada, plantaConsultada, respuestaConsulta in curx.fetchall():
                interConsultas.append(
                    {'especialidadConsulta': especialidadConsulta, 'plantaConsulta': plantaConsulta,
                     'diagnostico': diagnostico, 'descripcionConsulta': descripcionConsulta,
                     'especialidadConsultada': especialidadConsultada, 'plantaConsultada': plantaConsultada,
                     'respuestaConsulta': respuestaConsulta})
            miConexionx.close()

            print("interConsultas = ", interConsultas)
            print("matriz interConsultas = ", len(interConsultas))

            if (interConsultas != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'INTERCONSULTAS', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for x in range(0, len(interConsultas)):
                pdf.cell(50, 1, 'Consulta ' + str(interConsultas[0 + x]['especialidadConsulta']), 0, 0, 'L')
                pdf.cell(50, 1, '  ' + str(interConsultas[0 + x]['plantaConsulta']), 0, 0, 'L')
                pdf.cell(50, 1, 'Diagnostico: ' + str(interConsultas[0 + x]['diagnostico']), 0, 0, 'L')
                descripcionConsulta=str(interConsultas[0 + x]['descripcionConsulta'])
                pdf.multi_cell(w=0, h=4, txt=descripcionConsulta, border=0, align='J', fill=False)
		        #pdf.cell(100, 1, 'Descripcion: ' + str(interConsultas[0 + x]['descripcionConsulta']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)
                pdf.cell(50, 1, 'Consultado: ' + str(interConsultas[0 + x]['especialidadConsultada']), 0, 0, 'L')
                pdf.cell(50, 1, '   ' + str(interConsultas[0 + x]['plantaConsultada']), 0, 0, 'L')
                respuestaConsulta=str(interConsultas[0 + x]['respuestaConsulta'])
                pdf.multi_cell(w=0, h=4, txt=respuestaConsulta, border=0, align='J', fill=False)
                #pdf.cell(100, 1, 'Respuesta:' + str(interConsultas[0 + x]['respuestaConsulta']), 0, 0, 'L')

                linea = linea + 1
                pdf.ln(3)

            # Cursor recorre Medicamentos
            print ("ya imprimi INTERCONSULTAS")

            miConexionc = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curc = miConexionc.cursor()

            comando = 'SELECT med."dosisCantidad" dosis,  dosis.descripcion medida, vias.nombre via, sum.nombre suministro, med."cantidadOrdenada" cantidad,  med."diasTratamiento"  diasTratamiento FROM clinico_historiamedicamentos med INNER JOIN clinico_historia historia ON (historia.id = med.historia_id) LEFT JOIN facturacion_suministros  sum ON (sum.id=med.suministro_id) INNER JOIN clinico_viasadministracion vias ON (vias.id = med."viaAdministracion_id") INNER JOIN clinico_UnidadesDeMedidaDosis dosis ON (dosis.id = med."dosisUnidad_id") WHERE historia.id = ' + str(
                folios[0 + i]['HistoriaId'])
            curc.execute(comando)

            #print(comando)

            medicamentos = []

            for dosis, medida, via, suministro, cantidad, diasTratamiento in curc.fetchall():
                medicamentos.append(
                    {'dosis': dosis, 'medida': medida, 'via': via, 'suministro': suministro, 'cantidad': cantidad,
                     'diasTratamiento': diasTratamiento})
            miConexionc.close()

            print("medicamentos = ", medicamentos)
            print("matriz medicamentos = ", len(medicamentos))

            if (medicamentos != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'MEDICAMENTOS', 0, 0, 'C')
                linea = linea + 5
                pdf.ln(5)

            for z in range(0, len(medicamentos)):
                suministro=str(medicamentos[0 + z]['suministro'])
                pdf.multi_cell(w=0, h=4, txt=suministro, border=0, align='J', fill=False)

                #pdf.cell(90, 1, 'Med: ' + str(medicamentos[0 + z]['suministro']), 0, 0, 'L')
                pdf.cell(15, 1, 'Cant: ' + str(medicamentos[0 + z]['cantidad']), 0, 0, 'L')
                pdf.cell(15, 1, 'Dias: ' + str(medicamentos[0 + z]['diasTratamiento']), 0, 0, 'L')
                #linea = linea + 3
                #pdf.ln(3)
                pdf.cell(15, 1, 'Dosis ' + str(medicamentos[0 + z]['dosis']), 0, 0, 'L')
                pdf.cell(15, 1, 'Medida: ' + str(medicamentos[0 + z]['medida']), 0, 0, 'L')
                pdf.cell(25, 1, 'Via: ' + str(medicamentos[0 + z]['via']), 0, 0, 'L')

                linea = linea + 3
                pdf.ln(3)

            # Cursor recorre Cirugias

            # Cursor recorre Enfermeria

            # Cursor recorre Incapacidades

            miConexioni = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curi = miConexioni.cursor()

            comando = 'SELECT tipo.nombre tipo, diag.nombre diagnostico, inca."desdeFecha" desdeFecha, inca."hastaFecha" hastaFecha, inca."numDias" dias, inca.descripcion descripcion FROM clinico_historialincapacidades inca INNER JOIN clinico_TiposIncapacidad tipo  ON (tipo.id = inca."tiposIncapacidad_id") INNER JOIN clinico_Diagnosticos diag ON (diag.id = inca."diagnosticosIncapacidad_id") WHERE inca.historia_id = ' + str(
                folios[0 + i]['HistoriaId'])
            curi.execute(comando)

            #print(comando)

            incapacidades = []

            for tipo, diagnostico, desdeFecha, hastaFecha, dias, descripcion in curi.fetchall():
                incapacidades.append(
                    {'tipo': tipo, 'diagnostico': diagnostico, 'desdeFecha': desdeFecha, 'hastaFecha': hastaFecha,
                     'dias': dias, 'descripcion': descripcion})
            miConexioni.close()

            print("incapacidades = ", incapacidades)
            print("matriz incapacidades = ", len(incapacidades))

            if (incapacidades != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'Incapacidad Medica', 0, 0, 'C')
                linea = linea + 5
                pdf.ln(5)

            for z in range(0, len(incapacidades)):
                pdf.cell(50, 1, 'Tipo: ' + str(incapacidades[0 + z]['tipo']), 0, 0, 'L')
                pdf.cell(100, 1, 'Diagnostico: ' + str(incapacidades[0 + z]['diagnostico']), 0, 0, 'L')
                linea = linea + 3
                pdf.ln(3)
                pdf.cell(25, 1, 'Desde: ' + str(incapacidades[0 + z]['desdeFecha']), 0, 0, 'L')
                pdf.cell(25, 1, 'Hasta ' + str(incapacidades[0 + z]['hastaFecha']), 0, 0, 'L')
                pdf.cell(20, 1, 'Dias: ' + str(incapacidades[0 + z]['dias']), 0, 0, 'L')
                descripcion=str(incapacidades[0 + z]['descripcion'])
                pdf.multi_cell(w=0, h=4, txt=descripcion, border=0, align='J', fill=False)

                #pdf.cell(100, 1, 'Descripcion: ' + str(incapacidades[0 + z]['descripcion']), 0, 0, 'L')

                linea = linea + 3
                pdf.ln(3)

            # Cursor recorre Diagnosticos

            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curt = miConexiont.cursor()

            # comando ='select h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%NO%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + str(folios[0+i]['HistoriaId'])
            comando = 'select tiposdiag.nombre tipoDiag, histdiag.consecutivo consecutivo , diag.nombre nombreDiagnostico, histdiag.observaciones observaciones FROM clinico_historialdiagnosticos histdiag INNER JOIN clinico_tiposdiagnostico tiposdiag ON (tiposdiag.id = histdiag."tiposDiagnostico_id") INNER JOIN clinico_diagnosticos diag ON (diag.id=histdiag.diagnosticos_id) WHERE historia_id =	' + "'" + str(
                folios[0 + i]['HistoriaId']) + "'"

            curt.execute(comando)

            #print(comando)

            diagnosticos = []

            for tipoDiag, consecutivo, nombreDiagnostico, observaciones in curt.fetchall():
                diagnosticos.append(
                    {'tipoDiag': tipoDiag, 'consecutivo': consecutivo, 'nombreDiagnostico': nombreDiagnostico,
                     'observaciones': observaciones})
            miConexiont.close()

            print("diagnosticos = ", diagnosticos)
            print("matriz diagnosticos = ", len(diagnosticos))

            if (diagnosticos != []):
                linea = linea + 2
                pdf.ln(2)
                pdf.cell(180, 1, 'DIAGNOSTICOS', 0, 0, 'C')
                linea = linea + 3
                pdf.ln(4)

            for l in range(0, len(diagnosticos)):
                pdf.cell(30, 1, 'Tipo ' + str(diagnosticos[0 + l]['tipoDiag']), 0, 0, 'L')
                pdf.cell(20, 1, 'Consecutivo: ' + str(diagnosticos[0 + l]['consecutivo']), 0, 0, 'L')

                nombreDiagnostico=str(diagnosticos[0 + l]['nombreDiagnostico'])
                pdf.multi_cell(w=0, h=4, txt=nombreDiagnostico, border=0, align='J', fill=False)


                pdf.cell(100, 1, 'Nombre: ' + str(diagnosticos[0 + l]['nombreDiagnostico']), 0, 0, 'L')
                pdf.cell(100, 1, 'Observaciones: ' + str(diagnosticos[0 + l]['observaciones']), 0, 0, 'L')
                linea = linea + 1
                pdf.ln(3)

            # Aqui viene elmedico que firma el folio
            #
            miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                           password="123456")
            curx = miConexionx.cursor()

            comando = 'SELECT medicos."registroMedico", planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento 	FROM clinico_historia historia INNER JOIN planta_planta planta ON (planta.id = historia."usuarioRegistro_id") INNER JOIN clinico_medicos medicos ON (medicos.planta_id = planta.id) WHERE historia.id = ' + "'" + str(folios[0 + i]['HistoriaId']) + "'"
            curx.execute(comando)

            #print(comando)

            registroMed = []

            for registroMedico, plantaNombre, tipoDoc_id, documento in curx.fetchall():
                registroMed.append(
                    {'registroMedico': registroMedico, 'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id,
                     'documento': documento})
            miConexionx.close()

            pdf.cell(15, 7, 'Firmado Por:', 0, 0, 'L')
            pdf.cell(25, 7, '' + str(registroMed[0]['tipoDoc_id']), 0, 0, 'L')
            pdf.cell(25, 7, '' + str(registroMed[0]['documento']), 0, 0, 'L')
            pdf.cell(80, 7, '' + str(registroMed[0]['plantaNombre']), 0, 0, 'L')
            pdf.cell(50, 7, 'Registro Medico:' + str(registroMed[0]['registroMedico']), 0, 0, 'L')

            linea = linea + 2
            pdf.ln(2)
            pdf.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')

            linea = linea + 5
            pdf.ln(5)

            # self.ln(2)
            # self.cell(100, 9, 'Firmado Electronicamente', 0, 0, 'L')
            # self.set_font('Times', 'I', 8)
            # Page number
            # self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'HistoriaClinica.pdf'
    print ("archivo =" , archivo)

    #pdf.output('C:\EntornosPython\pos7Particionado/vulner/JSONCLINICA\HistoriasClinicas/hClinica.pdf', 'F')


    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')
        #Genera el archivo el el servidor
        #webbrowser.open(archivo)
        buff = BytesIO()
        buff.name = archivo

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
        return HttpResponse(json_data, content_type='application/json')



    return JsonResponse({'success': True, 'message': 'Historia Clinica impresa!'})


def ImprimirOrdenIncapacidad(ingresoId2, historiaId,convenioId , tipoAdmision):
    # Instantiation of inherited class
    print("Entre ImprimirOrdenIncapacidad ")

    ingresoId = ingresoId2

    try:
        with transaction.atomic():
            ingresoPaciente = Ingresos.objects.get(id=ingresoId)
            print(" ingresosPaciente = ", ingresoPaciente.id)
    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback INGRESO por:", e)
        ingresoPaciente = Triage.objects.get(id=ingresoId)
        print(" ingresosPaciente = ", ingresoPaciente.id)
    finally:
        print("Finally")

    #ingresoId = request.POST["ingresoId"]
    #print("ingresoId = ", ingresoId)

    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    pdf = PDFOrdenIncapacidad(tipoDocId,documentoId, consec, historiaId, convenioId, tipoAdmision, format="letter")
    pdf.alias_nb_pages()
    pdf.set_margins(left= 10, top= 5, right= 5 )
    pdf.add_page()
    pdf.set_font('Times', '', 8)
    pdf.ln(7)
    linea = 7

    #El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

           # Cursor recorre Incapacidades

    miConexioni = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",    password="123456")
    curi = miConexioni.cursor()


    comando = 'SELECT tipo.nombre tipo, diag.nombre diagnostico, inca."desdeFecha" desdeFecha, inca."hastaFecha" hastaFecha, inca."numDias" dias, inca.descripcion descripcion FROM clinico_historialincapacidades inca INNER JOIN clinico_TiposIncapacidad tipo  ON (tipo.id = inca."tiposIncapacidad_id") INNER JOIN clinico_Diagnosticos diag ON (diag.id = inca."diagnosticosIncapacidad_id") WHERE inca.historia_id = ' + "'" + str(historiaId) + "'"
    curi.execute(comando)

    print(comando)

    incapacidades = []

    for tipo, diagnostico, desdeFecha, hastaFecha, dias, descripcion in curi.fetchall():
       incapacidades.append(
           {'tipo': tipo, 'diagnostico': diagnostico, 'desdeFecha': desdeFecha, 'hastaFecha': hastaFecha,'dias':dias, 'descripcion':descripcion})
    miConexioni.close()

    print("incapacidades = ", incapacidades)
    print("matriz incapacidades = " , len(incapacidades))

    if (incapacidades != []):

       linea = linea + 2
       pdf.ln(2)
       pdf.set_font('Times', 'B', 8)
       pdf.cell(180, 1, 'Incapacidad Medica' , 0, 0, 'C')
       pdf.set_font('Times', '', 8)
       linea = linea + 5
       pdf.ln(5)


    for z in range(0, len(incapacidades)):

       pdf.cell(150, 1 , 'Diagnostico: ' + str(incapacidades[0 + z]['diagnostico']), 0, 0, 'L')
       linea = linea + 3
       pdf.ln(3)
       pdf.cell(50, 1 , 'Tipo: ' + str(incapacidades[0 + z]['tipo']), 0, 0, 'L')
       linea = linea + 3
       pdf.ln(3)
       pdf.cell(25, 1 , 'Desde: ' + str(incapacidades[0 + z]['desdeFecha']), 0, 0, 'L')
       pdf.cell(25, 1 , 'Hasta: ' + str(incapacidades[0 + z]['hastaFecha']), 0, 0, 'L')
       pdf.cell(20, 1,  'Dias: ' + str(incapacidades[0 + z]['dias']), 0, 0, 'L')

       descripcion=str(incapacidades[0 + z]['descripcion'])
       pdf.multi_cell(w=0, h=4, txt=descripcion, border=0, align='J', fill=False)

       #pdf.cell(100, 1 , 'Observacion: ' + str(incapacidades[0 + z]['descripcion']), 0, 0, 'L')

       linea = linea + 4
       pdf.ln(4)

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + str(historiaId) + 'Incapacidad.pdf'
    print ("archivo =" , archivo)

    #pdf.output('C:\EntornosPython\pos7Particionado/vulner/JSONCLINICA\HistoriasClinicas/hClinica.pdf', 'F')


    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')
        webbrowser.open(archivo)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': True, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')


    return JsonResponse({'success': True, 'message': 'Orden Incapacidad impresa!'})


def ImprimirOrdenTerapia(ingresoId2, historiaId, convenioId, tipoAdmision):
    # Instantiation of inherited class
    print("Entre ImprimirOrdenTerapia " , ingresoId2)
    print("Entre ImprimirOrdenTerapia historiaId ", historiaId)

    ingresoId = ingresoId2

    try:
        with transaction.atomic():
            ingresoPaciente = Ingresos.objects.get(id=ingresoId)
            print(" ingresosPaciente = ", ingresoPaciente.id)
    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback INGRESO por:", e)
        ingresoPaciente = Triage.objects.get(id=ingresoId)
        print(" ingresosPaciente = ", ingresoPaciente.id)
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

    pdf = PDFOrdenTerapia(tipoDocId,documentoId, consec, historiaId, convenioId, tipoAdmision)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Times', '', 8)
    pdf.ln(7)
    linea = 7
    totalFolios = 20

    # El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

    # Cursor recorre Laboratorios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%TERAP%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + "'" + str(historiaId) + "'"

    curt.execute(comando)

    print(comando)

    terapias = []

    for codigoCups, nombre, cantidad, observaciones in curt.fetchall():
        terapias.append(
            {'codigoCups': codigoCups, 'nombre': nombre, 'cantidad': cantidad, 'observaciones': observaciones})
    miConexiont.close()

    print("terapias = ", terapias)
    print("matriz terapias = ", len(terapias))

    if (terapias != []):
        linea = linea + 2
        pdf.ln(2)
        pdf.set_font('Times', 'B', 8)
        pdf.cell(180, 1, 'TERAPIAS', 0, 0, 'C')
        pdf.set_font('Times', '', 8)
        linea = linea + 3
        pdf.ln(4)

    for l in range(0, len(terapias)):
        pdf.cell(20, 1, 'Cups ' + str(terapias[0 + l]['codigoCups']), 0, 0, 'L')
        pdf.cell(100, 1, 'Nombre: ' + str(terapias[0 + l]['nombre']), 0, 0, 'L')
        pdf.cell(25, 1, 'Cantidad: ' + str(terapias[0 + l]['cantidad']), 0, 0, 'L')
        observaciones=str(terapias[0 + l]['observaciones'])
        pdf.multi_cell(w=0, h=4, txt=observaciones, border=0, align='J', fill=False)

        #pdf.cell(25, 1, 'Observacion: ' + str(terapias[0 + l]['observaciones']), 0, 0, 'L')
        linea = linea + 4
        pdf.ln(4)

    print ("POAQUI VOY A CREAR ARCHIVO")
    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + str(historiaId) + 'Terapia.pdf'
    print ("archivo =" , archivo)


    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')
        webbrowser.open(archivo)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': False, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')

    return JsonResponse({'success': True, 'message': 'Orden Terapia impresa!'})

def ImprimirOrdenLaboratorio(ingresoId2, historiaId, convenioId, tipoAdmision):
    # Instantiation of inherited class
    print("Entre ImprimirOrdenLaboratorio " , ingresoId2)
    print("Entre ImprimirOrdenLaboratorio historiaId ", historiaId)

    #ingresoId = request.POST["ingresoId"]
    #print("ingresoId = ", ingresoId)
    ingresoId = ingresoId2

    try:
        with transaction.atomic():
            ingresoPaciente = Ingresos.objects.get(id=ingresoId)
            print(" ingresosPaciente = ", ingresoPaciente.id)
    except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback INGRESO por:", e)
            ingresoPaciente = Triage.objects.get(id=ingresoId)
            print(" ingresosPaciente = ", ingresoPaciente.id)
    finally:
            print("Finally")

    print("ingresosPaciente = ", ingresoPaciente.id)

    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec =  ingresoPaciente.consec
    print ("consec = ",consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    pdf = PDFOrdenLaboratorio(tipoDocId,documentoId, consec, historiaId, convenioId, tipoAdmision)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Times', '', 8)
    pdf.ln(7)
    linea = 7
    totalFolios = 20

    # El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

    # Cursor recorre Laboratorios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%LABORATO%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + "'" + str(historiaId) + "'"

    curt.execute(comando)

    print(comando)

    laboratorios = []

    for codigoCups, nombre, cantidad, observaciones in curt.fetchall():
        laboratorios.append(
            {'codigoCups': codigoCups, 'nombre': nombre, 'cantidad': cantidad, 'observaciones': observaciones})
    miConexiont.close()

    print("laboratorios = ", laboratorios)
    print("matriz laboratorios = ", len(laboratorios))

    if (laboratorios != []):
        linea = linea + 2
        pdf.ln(2)
        pdf.set_font('Times', 'B', 8)
        pdf.cell(180, 1, 'LABORATORIOS', 0, 0, 'C')
        pdf.set_font('Times', '', 8)
        linea = linea + 3
        pdf.ln(4)

    for l in range(0, len(laboratorios)):
        pdf.cell(20, 1, 'Cups ' + str(laboratorios[0 + l]['codigoCups']), 0, 0, 'L')
        pdf.cell(100, 1, 'Nombre: ' + str(laboratorios[0 + l]['nombre']), 0, 0, 'L')
        pdf.cell(25, 1, 'Cantidad: ' + str(laboratorios[0 + l]['cantidad']), 0, 0, 'L')
        observaciones=str(laboratorios[0 + l]['observaciones'])
        pdf.multi_cell(w=0, h=4, txt=observaciones, border=0, align='J', fill=False)
        #pdf.cell(25, 1, 'Observacion: ' + str(laboratorios[0 + l]['observaciones']), 0, 0, 'L')
        linea = linea + 4
        pdf.ln(4)

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + str(historiaId) + 'Laboratorio.pdf'
    nombreArchivo = str(pacienteId.documento) + '_' + str(historiaId) + 'Laboratorio.pdf'
    print ("archivo =" , archivo)

    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')
        print ("ACABE DE VREAR EL ARCHIVO")
        webbrowser.open(archivo)

        #buff = BytesIO()
        #buff.name = archivo
        # Genera el archivo el el servidor

        # 2. Abrir el archivo PDF y leerlo
        #with open(archivo, 'rb') as f:
        #    pdf_data = f.read()
            # 3. Escribir los datos en el buffer
        #    buff.write(pdf_data)

        #buff.seek(0)
        print("Voya devolver el buff o Archivo binario")

        #return buff

        return nombreArchivo

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': True, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')


    return JsonResponse({'success': True, 'message': 'Orden Laboratorio impresa!'})


def ImprimirOrdenRadiologia(ingresoId2, historiaId, convenioId, tipoAdmision):
    # Instantiation of inherited class
    print("Entre ImprimirOrdenRadiologia " , ingresoId2)
    print("Entre ImprimirOrdenRadiologia historiaId ", historiaId)

    #ingresoId = request.POST["ingresoId"]
    #print("ingresoId = ", ingresoId)
    ingresoId = ingresoId2

    try:
        with transaction.atomic():
            ingresoPaciente = Ingresos.objects.get(id=ingresoId)
            print(" ingresosPaciente = ", ingresoPaciente.id)
    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback INGRESO por:", e)
        ingresoPaciente = Triage.objects.get(id=ingresoId)
        print(" ingresosPaciente = ", ingresoPaciente.id)
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

    pdf = PDFOrdenRadiologia(tipoDocId,documentoId, consec, historiaId, convenioId, tipoAdmision)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Times', '', 8)
    pdf.ln(7)
    linea = 7
    totalFolios = 20

    # El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

    # Cursor recorre Laboratorios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select h."codigoCups" codigoCups, e.nombre nombre, h.cantidad cantidad, h.observaciones observaciones from clinico_historiaexamenes h, clinico_examenes    e, clinico_tiposexamen t  where h."tiposExamen_id" = t.id and t.nombre like(' + "'" + '%RADIOLOG%' + "'" + ') and e."codigoCups" = h."codigoCups" and h.historia_id = ' + "'" + str(historiaId) + "'"

    curt.execute(comando)

    print(comando)

    radiologia = []

    for codigoCups, nombre, cantidad, observaciones in curt.fetchall():
        radiologia.append(
            {'codigoCups': codigoCups, 'nombre': nombre, 'cantidad': cantidad, 'observaciones': observaciones})
    miConexiont.close()

    print("radiologia = ", radiologia)
    print("matriz radiologia = ", len(radiologia))

    if (radiologia != []):
        linea = linea + 2
        pdf.ln(2)
        pdf.set_font('Times', 'B', 8)
        pdf.cell(180, 1, 'RADIOLOGIA', 0, 0, 'C')
        pdf.set_font('Times', '', 8)
        linea = linea + 3
        pdf.ln(4)

    for l in range(0, len(radiologia)):
        pdf.cell(20, 1, 'Cups ' + str(radiologia[0 + l]['codigoCups']), 0, 0, 'L')
        pdf.cell(100, 1, 'Nombre: ' + str(radiologia[0 + l]['nombre']), 0, 0, 'L')
        pdf.cell(25, 1, 'Cantidad: ' + str(radiologia[0 + l]['cantidad']), 0, 0, 'L')
        observaciones=str(radiologia[0 + l]['observaciones'])
        pdf.multi_cell(w=0, h=4, txt=observaciones, border=0, align='J', fill=False)

        #pdf.cell(25, 1, 'Observacion: ' + str(radiologia[0 + l]['observaciones']), 0, 0, 'L')
        linea = linea + 4
        pdf.ln(4)

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento)+ '_' + str(historiaId)  + 'Radiologia.pdf'
    print ("archivo =" , archivo)



    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')
        webbrowser.open(archivo)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': True, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')

    return JsonResponse({'success': True, 'message': 'Orden Laboratorio impresa!'})


def ImprimirOrdenMedicamentos(ingresoId2, historiaId, convenioId, tipoAdmision):
    # Instantiation of inherited class
    print("Entre ImprimirOrdenMedicamentos " , ingresoId2)
    print("Entre ImprimirOrdenMedicamentos historiaId ", historiaId)

    #ingresoId = request.POST["ingresoId"]
    #print("ingresoId = ", ingresoId)
    ingresoId = ingresoId2

    try:
        with transaction.atomic():
            ingresoPaciente = Ingresos.objects.get(id=ingresoId)
            print(" ingresosPaciente = ", ingresoPaciente.id)
    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback INGRESO por:", e)
        ingresoPaciente = Triage.objects.get(id=ingresoId)
        print(" ingresosPaciente = ", ingresoPaciente.id)
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

    pdf = PDFOrdenMedicamentos(tipoDocId,documentoId, consec, historiaId, convenioId, tipoAdmision)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Times', '', 8)
    pdf.ln(7)
    linea = 7
    totalFolios = 20

    # El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

    # Cursor recorre Laboratorios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()


    comando = 'select sum.nombre medicamento,med."dosisCantidad" dosis, undmed.descripcion medida, via.nombre via,frec.descripcion frecuencia, med."cantidadOrdenada" cantidad, med."diasTratamiento" dias from clinico_historiamedicamentos med inner join clinico_historia his on (his.id=med.historia_id) inner join facturacion_suministros sum on (sum.id = med.suministro_id) inner join clinico_viasadministracion via on (via.id = med."viaAdministracion_id") inner join clinico_unidadesdemedidadosis undmed on (undmed.id = med."dosisUnidad_id") inner join clinico_frecuenciasaplicacion frec on (frec.id = med."frecuencia_id") WHERE his.id = ' + "'" + str(historiaId) + "'" + ' order by med."consecutivoMedicamento"'


    curt.execute(comando)

    print(comando)

    medicamentos = []

    for medicamento, dosis, medida, via, frecuencia, cantidad, dias   in curt.fetchall():
        medicamentos.append(
            {'medicamento': medicamento, 'dosis': dosis, 'medida': medida, 'via': via,'frecuencia':frecuencia, 'cantidad':cantidad, 'dias':dias})
    miConexiont.close()

    print("medicamentos = ", medicamentos)
    print("matriz medicamentos = ", len(medicamentos))

    if (medicamentos != []):
        linea = linea + 2
        pdf.ln(2)
        pdf.set_font('Times', 'B', 8)
        pdf.cell(180, 1, 'FORMULACION MEDICAMENTOS', 0, 0, 'C')
        pdf.set_font('Times', '', 8)
        linea = linea + 5
        pdf.ln(5)

    for l in range(0, len(medicamentos)):

        medicamento=str(medicamentos[0 + l]['medicamento'])
        pdf.multi_cell(w=0, h=4, txt=medicamento, border=0, align='J', fill=False)

        #pdf.cell(80, 1, '' + str(medicamentos[0 + l]['medicamento']), 0, 0, 'L')
        pdf.cell(18, 1, 'Dosis: ' + str(medicamentos[0 + l]['dosis']), 0, 0, 'L')
        pdf.cell(10, 1, ' ' + str(medicamentos[0 + l]['medida']), 0, 0, 'L')
        pdf.cell(30, 1, ' ' + str(medicamentos[0 + l]['via']), 0, 0, 'L')
        pdf.cell(25, 1, ' ' + str(medicamentos[0 + l]['frecuencia']), 0, 0, 'L')
        pdf.cell(13, 1, 'Cant: ' + str(medicamentos[0 + l]['cantidad']), 0, 0, 'L')
        pdf.cell(13, 1, 'Dias: ' + str(medicamentos[0 + l]['dias']), 0, 0, 'L')
        linea = linea + 4
        pdf.ln(4)

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + str(historiaId) + 'Medicamentos.pdf'
    print ("archivo =" , archivo)



    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')
        webbrowser.open(archivo)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': True, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')

    return JsonResponse({'success': True, 'message': 'Orden Formulacion de medicamentos impresa!'})



def ImprimirOrdenDeControl(ingresoId2, historiaId, convenioId, tipoAdmision):
    # Instantiation of inherited class
    print("Entre ImprimirOrdenDeControl " , ingresoId2)
    print("Entre ImprimirOrdenDeControl historiaId ", historiaId)

    #ingresoId = request.POST["ingresoId"]
    #print("ingresoId = ", ingresoId)
    ingresoId = ingresoId2

    try:
        with transaction.atomic():
            ingresoPaciente = Ingresos.objects.get(id=ingresoId)
            print(" ingresosPaciente = ", ingresoPaciente.id)
    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback INGRESO por:", e)
        ingresoPaciente = Triage.objects.get(id=ingresoId)
        print(" ingresosPaciente = ", ingresoPaciente.id)
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

    pdf = PDFOrdenDeControl(tipoDocId,documentoId, consec, historiaId, convenioId, tipoAdmision)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Times', '', 8)
    pdf.ln(7)
    linea = 7
    totalFolios = 20

    # El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

    # Cursor Lee orden de control

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select h."ordenDeControl" orden from clinico_historia h where h.id = ' + "'" + str(historiaId) + "'"

    curt.execute(comando)

    print(comando)

    ordenDeControl = []

    for orden in curt.fetchall():
        ordenDeControl.append(
            {'orden': orden})
    miConexiont.close()

    print("ordenDeControl = ", ordenDeControl)
    print("matriz ordenDeControl = ", len(ordenDeControl))

    if (ordenDeControl != []):
        linea = linea + 2
        pdf.ln(2)
        pdf.set_font('Times', 'B', 8)
        pdf.cell(180, 1, 'ORDEN DE CONTROL', 0, 0, 'C')
        pdf.set_font('Times', '', 8)
        linea = linea + 3
        pdf.ln(4)

    for l in range(0, len(ordenDeControl)):
        orden=str(ordenDeControl[0 + l]['orden'])
        pdf.multi_cell(w=0, h=4, txt=orden, border=0, align='J', fill=False)

        #pdf.cell(20, 1, str(ordenDeControl[0 + l]['orden']), 0, 0, 'L')
        linea = linea + 4
        pdf.ln(4)

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print ("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + str(historiaId) + '_' + 'OrdenDeControl.pdf'
    nombreArchivo = str(pacienteId.documento) + '_' + str(historiaId) + '_' + 'OrdenDeControl.pdf'

    print ("archivo =" , archivo)

    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, 'F')
        webbrowser.open(archivo)

        #buff = BytesIO()
        #buff.name = archivo
        # Genera el archivo el el servidor

        # 2. Abrir el archivo PDF y leerlo
        #with open(archivo, 'rb') as f:
        #    pdf_data = f.read()
            # 3. Escribir los datos en el buffer
        #    buff.write(pdf_data)

        #buff.seek(0)
        print ("Voya devolver el buff o Archivo binario")

        #return buff
        #
        return nombreArchivo


        #return JsonResponse({'success': True, 'archivo': buff})
        #return HttpResponse(buff, content_type='application/json')
        #return FileResponse(
        #    buff,
        ##    as_attachment=False,  # Cambiar a False para verlo en navegador
        #    filename=archivo,
        #    content_type='application/pdf'
        #)

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': True, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        #return HttpResponse(json_data, content_type='application/json')


    return JsonResponse({'success': True, 'message': 'Orden De COntrol impresa!','archivo':archivo})
    #return JsonResponse({'success': True,'archivo':archivo})

