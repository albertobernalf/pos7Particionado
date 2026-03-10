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
#from .forms import historiaForm, historiaExamenesForm
from datetime import datetime
from clinico.models import Historia, HistoriaExamenes, Examenes, TiposExamen, EspecialidadesMedicos, Medicos, Especialidades, TiposFolio, CausasExterna, EstadoExamenes, HistorialAntecedentes, HistorialDiagnosticos, HistorialInterconsultas, EstadosInterconsulta, HistorialIncapacidades,  HistoriaSignosVitales, HistoriaRevisionSistemas, HistoriaMedicamentos , Regimenes
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

import os
import requests
import urllib
from django.http import FileResponse
from io import BytesIO
import io
from django.http import FileResponse


class PDFTriage(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, triageId,  *args, **kwargs):
    #def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.triageId = triageId


    def header(self):
        # Move to the right
        #self.cell(12)

        ## CURSOR PARA LEER ENCABEZADO
        #

        # Line break
        print("entre header")
        self.ln(6)

    def footer(self):
        # Position at 1.5 cm from bottom
        #self.set_y(-15)
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Helvetica', 'B', 8)
        self.cell(18, 10, 'ELABORADO', 0, 0, 'C')

        miConexionii = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        curii = miConexionii.cursor()

        comando = 'SELECT  planta.nombre plantaNombre, planta."tipoDoc_id", planta.documento 	FROM triage_triage tri INNER JOIN planta_planta planta ON (planta.id = tri."usuarioCrea_id") WHERE tri.id = ' + "'" + str(self.triageId) +"'"

        curii.execute(comando)

        print(comando)

        elaboro = []

        for plantaNombre, tipoDoc_id, documento in curii.fetchall():
            elaboro.append(
                {'plantaNombre': plantaNombre, 'tipoDoc_id': tipoDoc_id, 'documento': documento})
        miConexionii.close()

        self.set_line_width(0.4)
        self.rect(10, 280.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto

        self.cell(15, 10, 'Firmado Por:', 0, 0, 'L')
        self.cell(25, 10, '' + str(elaboro[0]['tipoDoc_id']), 0, 0, 'L')
        self.cell(25, 10, '' + str(elaboro[0]['documento']), 0, 0, 'L')
        self.cell(80, 10, '' + str(elaboro[0]['plantaNombre']), 0, 0, 'L')

        self.ln(3)
        self.cell(100, 10, 'Firmado Electronicamente', 0, 0, 'L')
        self.set_font('Helvetica', 'I', 8)
        # Page number
        #self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')




class PDFAtencionInicialUrgencias(FPDF):
    def __init__(self, tipoDocId, documentoId, consec,ingresoId,  *args, **kwargs):
    #def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.ingresoId = ingresoId


    def header(self):
        # Move to the right
        # self.cell(12)

        ## CURSOR PARA LEER ENCABEZADO
        #
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")

        curt = miConexiont.cursor()

        comando = 'select ' + "'" + str('Paciente en trauma') + "'" + ' seInforma, substring(cast(current_Helveticatamp as text),1,10) fecha , substring(cast(current_time as text), 1,5) as time,emp.nombre nombreEmpresa, substring(sed.nit,1,9) nit, substring(sed.nit,9,1) nitVerificacion, sed."codigoHabilitacion" habilita,emp.direccion direccionPrestador, emp.telefono telefonoPrestador, dep.nombre departamentoPrestador, dep."departamentoCodigoDian" codigoDepartamentoPrestador, mun.nombre municipioPrestador FROM facturacion_empresas emp INNER JOIN sitios_sedesclinica sed ON (sed.id=1) INNER JOIN sitios_departamentos dep ON (dep.id=emp.departamento_id) INNER JOIN sitios_municipios mun ON (mun.id = emp.municipio_id) WHERE emp. nombre like (' + "'" + str('%MEDICAL%') + "')"

        curt.execute(comando)
        print(comando)

        historia = []

        for seInforma, fecha, time, nombreEmpresa, nit, nitVerificacion, habilita, direccionPrestador, telefonoPrestador, departamentoPrestador, codigoDepartamentoPrestador, municipioPrestador in curt.fetchall():
            historia.append(
                {'seInforma': seInforma, 'fecha': fecha, 'time': time, 'nombreEmpresa': nombreEmpresa,
                 'nit': nit, 'nitVerificacion': nitVerificacion, 'habilita': habilita,
                 'direccionPrestador': direccionPrestador, 'telefonoPrestador': telefonoPrestador,
                 'departamentoPrestador': departamentoPrestador,
                 'codigoDepartamentoPrestador': codigoDepartamentoPrestador, 'municipioPrestador': municipioPrestador})

        miConexiont.close()

        ## FIN CURSOR

        # Title
        #
        self.ln(4)
        self.set_font('Helvetica', 'B', 7)
        self.cell(180, 10, 'ANEXO TECNICO No. 2345678', 0, 0, 'C')
        self.ln(1)
        self.cell(180, 10, 'INFORME DE LA ATENCION INICIAL DE URGENCIAS: ', 0, 0, 'C')
        self.set_font('Helvetica', '', 7)

        # Define el ancho de línea
        self.set_line_width(0.4)
        # Dibuja el borde
        self.rect(5.0, 18.0, 200.0, 185.0)  # Coordenadas x, y, ancho, alto
        self.ln(3)
        # Logo
        self.image('C:/EntornosPython/Pos7Particionado/vulner/static/img/MedicalFinal.jpg', 7, 19, 11, 11)
        # Arial bold 15
        self.set_font('Helvetica', 'B', 7)
        self.ln(3)
        self.cell(180, 10, 'MINISTERIO DE LA PROTECCION SOCIAL: ', 0, 0, 'C')
        self.ln(3)
        self.cell(180, 10, 'INFORME DE LA ATENCION INICIAL DE URGENCIAS: ', 0, 0, 'C')
        self.ln(6)
        self.set_font('Helvetica', 'B', 7)
        self.cell(80, 10, 'INFORMACION DEL PRESTADOR: ', 0, 0, 'L')

        self.cell(45, 10, 'NUMERO DE ATENCION: ', 0, 0, 'L')
        self.set_font('Helvetica', '', 7)
        self.set_line_width(0.3)
        #self.rect(135.0, 29.0, 13.0, 3.0)  # Coordenadas x, y, ancho, alto

        #self.cell(15, 10, '527733', 0, 0, 'L')
        self.cell(15, 10, str(self.ingresoId), 0, 0, 'L')
        self.set_font('Helvetica', 'B', 7)
        self.cell(10, 10, 'Fecha: ', 0, 0, 'L')
        self.set_font('Helvetica', '', 7)
        self.cell(25, 10, historia[0]['fecha'], 0, 0, 'L')
        self.set_font('Helvetica', 'B', 7)
        self.cell(10, 10, 'Hora: ', 0, 0, 'L')
        self.set_font('Helvetica', '', 7)
        self.cell(25, 10, historia[0]['time'], 0, 0, 'L')
        self.ln(1)
        self.set_line_width(0.3)
        self.rect(5.0, 36.0, 120.0, 3.0)  # Coordenadas x, y, ancho, alto
        self.cell(120, 10, historia[0]['nombreEmpresa'], 0, 0, 'L')
        self.rect(130.0, 36.0, 70.0, 3.0)  # Coordenadas x, y, ancho, alto
        self.cell(25, 10, 'Nit: ', 0, 0, 'L')
        self.cell(25, 10, 'X', 0, 0, 'L')
        self.cell(20, 10, historia[0]['nit'], 0, 0, 'L')
        self.rect(200.0, 36.0, 5.0, 3.0)  # Coordenadas x, y, ancho, alto
        self.cell(20, 10, historia[0]['nitVerificacion'], 0, 0, 'L')
        self.cell(25, 10, 'CC', 0, 0, 'L')
        self.cell(25, 10, 'Numero', 0, 0, 'L')
        self.cell(25, 10, 'DV', 0, 0, 'L')
        self.ln(3)
        self.set_line_width(0.3)
        #self.rect(5.0, 39.0, 200.0, 6.0)  # Coordenadas x, y, ancho, alto

        self.cell(25, 10, 'Codigo:', 0, 0, 'L')
        self.cell(25, 10, historia[0]['habilita'], 0, 0, 'L')
        self.cell(25, 10, 'Direccion Prestador:', 0, 0, 'L')
        self.cell(25, 10, historia[0]['direccionPrestador'], 0, 0, 'L')
        self.ln(3)
        self.cell(25, 10, 'Telefono:', 0, 0, 'L')
        self.cell(25, 10, historia[0]['telefonoPrestador'], 0, 0, 'L')
        self.ln(3)
        self.set_line_width(0.3)
        self.rect(5.0, 39.0, 200.0, 15.0)  # Coordenadas x, y, ancho, alto
        self.cell(25, 10, 'Indicativo:', 0, 0, 'L')
        self.cell(25, 10, 'Numero:', 0, 0, 'L')
        self.cell(25, 10, 'Departamento:', 0, 0, 'L')
        self.cell(25, 10, historia[0]['departamentoPrestador'], 0, 0, 'L')
        self.cell(25, 10, historia[0]['codigoDepartamentoPrestador'], 0, 0, 'L')
        self.cell(25, 10, 'Municipio:', 0, 0, 'L')
        self.cell(25, 10, historia[0]['municipioPrestador'], 0, 0, 'L')
        self.ln(3)
        self.cell(85, 10, 'Entidad a ala que se le informa (Pagador):', 0, 0, 'L')
        self.cell(25, 10, historia[0]['seInforma'], 0, 0, 'L')
        self.cell(25, 10, 'Codigo):', 0, 0, 'L')
        self.ln(3)

        # Line break
        self.ln(10)


class PDFHojaAdmision(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, ingresoId,  *args, **kwargs):
    #def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.ingresoId = ingresoId


    def header(self):
        # Move to the right
        # self.cell(12)

        ## CURSOR PARA LEER ENCABEZADO
        #

        # Line break
        self.ln(10)

class PDFManilla(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, ingresoId,  *args, **kwargs):
    #def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.ingresoId = ingresoId


    def header(self):
        # Move to the right
        # self.cell(12)

        ## CURSOR PARA LEER ENCABEZADO
        #

        # Line break
        self.ln(10)



def ImprimirAtencionInicialUrgencias(ingresoId2):
    # Instantiation of inherited class
    print("Entre ImprimirAtencionInicialUrgencias ", ingresoId2)


    #ingresoId = request.POST["ingresoId"]
    print("ingresoId2 = ", ingresoId2)
    ingresoId = ingresoId2

    ingresoPaciente = Ingresos.objects.get(id=ingresoId)
    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    pdf = PDFAtencionInicialUrgencias(tipoDocId, documentoId, consec, ingresoId)
    # pdf = PDFAtencionInicialUrgencias()
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(1)
    linea = 7

    # El propgrama debe preguntar desde que Folio hasta cual Y/O desde que fecha y hasta cual fecha

    # Cursor recorre Laboratorios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    # comando ='SELECT substring(usu.nombre,1,(position(' + "' '" +  ' in usu.nombre))) primerNombre,substring(usu.nombre, position(' + "' '" +  ' in usu.nombre),10) segundoNombre, 0  primerApellido, 0  segundoApellido , usu."tipoDoc_id" tipoDoc ,usu.documento documento , usu."fechaNacio" fechaNacimiento, usu.direccion direccion, usu.telefono telefono,  dep.nombre departamentoPaciente, mun.nombre municipioPaciente FROM clinico_historia his INNER JOIN admisiones_ingresos ing ON (ing."tipoDoc_id"=his."tipoDoc_id" AND ing.documento_id=his.documento_id and ing.consec=his."consecAdmision") INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id"=his."tipoDoc_id" AND usu.id=his.documento_id) INNER JOIN sitios_departamentos dep ON (dep.id=usu.departamentos_id) INNER JOIN sitios_municipios mun ON (mun.id = usu.municipio_id) INNER JOIN clinico_servicios servicios on ( servicios.id=ing."serviciosActual_id") WHERE ing.id = ' + "'" + str(50137) + "'" + ' AND servicios.NOMBRE LIKE (' + "'" + str('%URGENC%') + "')" + ' group by primerNombre, segundoNombre, usu."tipoDoc_id",usu.documento, usu."fechaNacio" , usu.direccion , usu.telefono , dep.nombre , mun.nombre'

    comando = 'SELECT usu."primerNombre"  primerNombre, usu."segundoNombre"  segundoNombre, usu."primerApellido"  primerApellido, usu."segundoApellido" segundoApellido , usu."tipoDoc_id" tipoDoc ,usu.documento documento , usu."fechaNacio" fechaNacimiento, usu.direccion direccion, usu.telefono telefono,  dep.nombre departamentoPaciente, mun.nombre municipioPaciente, regimen.nombre regimen FROM admisiones_ingresos ing INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id"=ing."tipoDoc_id" AND usu.id=ing.documento_id) INNER JOIN sitios_departamentos dep ON (dep.id=usu.departamentos_id) INNER JOIN sitios_municipios mun ON (mun.id = usu.municipio_id) INNER JOIN clinico_servicios servicios on ( servicios.id=ing."serviciosActual_id") LEFT JOIN clinico_regimenes regimen ON (regimen.id = ing.regimen_id) WHERE ing.id = ' + "'" + str(
        ingresoId) + "'" + ' AND servicios.NOMBRE LIKE (' + "'" + str(
        '%URGENC%') + "')" + ' group by usu."primerNombre", usu."segundoNombre", usu."primerApellido", usu."segundoApellido", usu."tipoDoc_id",usu.documento, usu."fechaNacio" , usu.direccion , usu.telefono , dep.nombre , mun.nombre, regimen.nombre'

    curt.execute(comando)

    print(comando)

    atencionUrgencias = []

    for primerNombre, segundoNombre, primerApellido, segundoApellido, tipoDoc, documento, fechaNacimiento, direccion, telefono, departamentoPaciente, municipioPaciente, regimen in curt.fetchall():
        atencionUrgencias.append(
            {'primerNombre': primerNombre, 'segundoNombre': segundoNombre, 'primerApellido': primerApellido,
             'segundoApellido': segundoApellido, 'tipoDoc': tipoDoc, 'documento': documento,
             'fechaNacimiento': fechaNacimiento, 'direccion': direccion, 'telefono': telefono,
             'departamentoPaciente': departamentoPaciente, 'municipioPaciente': municipioPaciente, 'regimen': regimen})
    miConexiont.close()

    tipoDocumento = TiposDocumento.objects.get(id=atencionUrgencias[0]['tipoDoc'])
    regimenes = Regimenes.objects.get(nombre=atencionUrgencias[0]['regimen'])

    print("atencionUrgencias = ", atencionUrgencias)
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 50.0, 200.0, 3.0)  # Coordenadas x, y, ancho, alto

    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(180, 10, 'DATOS DEL PACIENTE:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(3)
    print("pase_1 con data", atencionUrgencias[0]['primerApellido'])
    pdf.set_line_width(0.3)
    pdf.rect(5.0, 58.0, 50.0, 4.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(50, 10, str(atencionUrgencias[0]['primerApellido']), 0, 0, 'L')
    pdf.rect(55.0, 58.0, 50.0, 4.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(50, 10, str(atencionUrgencias[0]['segundoApellido']), 0, 0, 'L')
    pdf.rect(105.0, 58.0, 50.0, 4.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(50, 10, str(atencionUrgencias[0]['primerNombre']), 0, 0, 'L')
    pdf.rect(155.0, 58.0, 50.0, 4.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(50, 10, str(atencionUrgencias[0]['segundoNombre']), 0, 0, 'L')

    pdf.ln(3)
    pdf.cell(50, 10, 'primerApellido', 0, 0, 'L')
    pdf.cell(50, 10, 'segundorApellido', 0, 0, 'L')
    pdf.cell(50, 10, 'primerNombre', 0, 0, 'L')
    pdf.cell(50, 10, 'segundoNombre', 0, 0, 'L')
    pdf.ln(4)
    pdf.cell(25, 10, 'Tipo Documento Identificacion', 0, 0, 'L')
    pdf.ln(3)
    if tipoDocumento.abreviatura == 'RC':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(50, 10, 'Registro Civil', 0, 0, 'L')
    if tipoDocumento.abreviatura == 'PA':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(50, 10, 'Pasaporte', 0, 0, 'L')
    # pdf.rect(100.0, 70.0, 40.0, 4.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(25, 10, str(atencionUrgencias[0]['documento']), 0, 0, 'L')
    if tipoDocumento.abreviatura == 'TI':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, 'Tarjeta de Identidad', 0, 0, 'L')
    if tipoDocumento.abreviatura == 'NN':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(50, 10, 'Adulto sin Identificacion', 0, 0, 'L')
    pdf.cell(25, 10, 'Numero de Documento de Identificacion', 0, 0, 'L')
    pdf.ln(3)
    if tipoDocumento.abreviatura == 'CC':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(50, 10, 'Cedula de ciudadania', 0, 0, 'L')
    if tipoDocumento.abreviatura == 'NN':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(50, 10, 'Menor sin identificacion', 0, 0, 'L')
    pdf.ln(3)
    if tipoDocumento.abreviatura == 'CE':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(120, 10, 'Cedula de extranjeria', 0, 0, 'L')
    pdf.cell(25, 10, 'Fecha de nacimiento', 0, 0, 'L')
    pdf.cell(35, 10, str(atencionUrgencias[0]['fechaNacimiento']), 0, 0, 'L')

    # pdf.cell(25, 14, 'Numero de Documento de Identificacion', 0, 0, 'L')

    # pdf.rect(5.0, 65.0, 200.0, 4.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(3)
    pdf.cell(35, 10, 'Direccion de residencia habitual', 0, 0, 'L')
    pdf.cell(100, 10, str(atencionUrgencias[0]['direccion']), 0, 0, 'L')
    pdf.cell(25, 10, 'Telefono', 0, 0, 'L')
    pdf.cell(25, 10, str(atencionUrgencias[0]['telefono']), 0, 0, 'L')
    # pdf.rect(150.0, 58.0, 58.0, 4.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(3)
    pdf.cell(60, 10, 'Departamento', 0, 0, 'L')
    pdf.cell(25, 10, str(atencionUrgencias[0]['departamentoPaciente']), 0, 0, 'L')
    pdf.cell(25, 10, 'Municipio', 0, 0, 'L')
    pdf.cell(25, 10, str(atencionUrgencias[0]['municipioPaciente']), 0, 0, 'L')
    pdf.ln(3)
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 85.0, 200.0, 10.0)  # Coordenadas x, y, ancho, alto
    pdf.rect(5.0, 95.0, 200.0, 12.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(3)
    pdf.cell(35, 10, 'Cobertura en salud', 0, 0, 'L')
    pdf.ln(3)
    if regimenes.nombre == 'CONTRIBUTIVO':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(35, 10, 'Regimen Contributtivo', 0, 0, 'L')
    if regimenes.nombre == 'SUBSIDIADO':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(35, 10, 'Regimen subsidiado parcial', 0, 0, 'L')
    pdf.cell(65, 10, 'Poblacion pobre No asegurada con sisben', 0, 0, 'L')
    pdf.cell(35, 10, 'Plan adicional en salud', 0, 0, 'L')
    pdf.ln(3)
    if regimenes.nombre == 'SUBSIDIADO':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(35, 10, 'Regimen subsidiado total', 0, 0, 'L')
    pdf.cell(65, 10, 'Poblacion pobre No asegurada sin sisben', 0, 0, 'L')
    pdf.cell(45, 10, 'Desplazado', 0, 0, 'L')
    if (regimenes.nombre != 'SUBSIDIADO' or regimenes.nombre != 'CONTRIBUTIVO' or regimenes.nombre != 'VINCULADO'):
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(35, 10, 'Otro', 0, 0, 'L')
    pdf.ln(3)
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 98.0, 200.0, 3.0)  # Coordenadas x, y, ancho, alto
    pdf.set_font('Helvetica', 'B', 8)

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select ext.id id ,ext.nombre causa from admisiones_ingresos ing inner join clinico_causasexterna ext on (ext.id=ing."causasExterna_id") where ing.id= ' + "'" + str(
        ingresoId) + "'"

    curt.execute(comando)

    print(comando)

    externaUrgencias = []

    for id, causa in curt.fetchall():
        externaUrgencias.append(
            {'id': id, 'causa': causa})
    miConexiont.close()

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select tri.id id ,tri."clasificacionTriage_id" triage from triage_triage tri WHERE tri."tipoDoc_id" = ' + "'" + str(
        tipoDocId) + "'" + ' and tri.documento_id = ' + "'" + str(
        documentoId) + "'" + ' and tri."consecAdmision" = ' + "'" + str(consec) + "'"

    curt.execute(comando)

    print(comando)

    triageUrgencias = []

    for id, triage in curt.fetchall():
        triageUrgencias.append(
            {'id': id, 'triage': triage})

    print("triageUrgencias = ", triageUrgencias)
    miConexiont.close()

    pdf.cell(200, 10, 'INFORMACION DE LA ATENCION', 0, 0, 'C')
    pdf.set_font('Helvetica', '',8)
    pdf.ln(3)

    pdf.rect(5.0, 115.0, 200.0, 14.0)  # Coordenadas x, y, ancho, alto
    pdf.set_font('Helvetica', 'B',8)
    pdf.cell(25, 10, 'Origen de la atencion', 0, 0, 'L')
    pdf.ln(2)
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(3)
    pdf.cell(25, 10, 'Enfermedad General', 0, 0, 'L')
    if externaUrgencias[0]['causa'] == 'ENFERMEDAD GENERAL':
        pdf.cell(34, 10, 'X', 0, 0, 'L')
    if externaUrgencias[0]['causa'] == 'ACCIDENTE DE TRABAJO':
        pdf.cell(34, 10, 'X', 0, 0, 'L')
    pdf.cell(25, 10, 'Accidente de trabajo', 0, 0, 'L')
    if externaUrgencias[0]['causa'] == 'EVENTO CATASTROFICO':
        pdf.cell(27, 34, 'X', 0, 0, 'L')
    pdf.cell(30, 10, 'Evento Catastrofico', 0, 0, 'L')
    if triageUrgencias[0]['triage'] == '1':
        pdf.cell(5, 10, 'X', 0, 0, 'L')
    pdf.cell(40, 10, '', 0, 0, 'L')
    pdf.cell(15, 10, '1. Rojo', 0, 0, 'L')
    pdf.ln(3)

    pdf.cell(25, 10, 'Enfermedad Profesional', 0, 0, 'L')
    if externaUrgencias[0]['causa'] == 'ENFERMEDAD PROFESIONAL':
        pdf.cell(25, 10, 'X', 0, 0, 'L')

    pdf.cell(25, 10, 'Accidente de transito', 0, 0, 'L')
    if externaUrgencias[0]['causa'] == 'ACCIDENTE DE TRANSITO':
        pdf.cell(27, 10, 'X', 0, 0, 'L')

    if externaUrgencias[0]['causa'] == 'OTROS':
        pdf.cell(27, 10, 'X', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(70, 10, 'Otro tipo de accidente', 0, 0, 'L')

    pdf.cell(40, 10, '', 0, 0, 'L')
    pdf.cell(15, 10, '2. Naranja', 0, 0, 'L')
    if triageUrgencias[0]['triage'] == '2':
        pdf.cell(137, 10, 'X', 0, 0, 'L')
    pdf.ln(1)
    pdf.cell(70, 10, '', 0, 0, 'L')
    pdf.cell(40, 10, 'Clasificacion Triage', 0, 0, 'L')
    pdf.cell(10, 10, '3. Amarillo', 0, 0, 'L')
    if triageUrgencias[0]['triage'] == '3':
        pdf.cell(137,10, 'X', 0, 0, 'L')
    pdf.ln(1)
    pdf.cell(120, 10, '', 0, 0, 'L')
    pdf.cell(15, 30, '4. Verde', 0, 0, 'L')
    if triageUrgencias[0]['triage'] == '4':
        pdf.cell(137,10, 'X', 0, 0, 'L')
    pdf.ln(1)
    pdf.cell(120, 10, '', 0, 0, 'L')
    pdf.cell(15, 10, '5. Azul', 0, 0, 'L')
    if triageUrgencias[0]['triage'] == '5':
        pdf.cell(137, 31, 'X', 0, 0, 'L')

    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 105.0, 200.0, 3.0)  # Coordenadas x, y, ancho, alto
    pdf.rect(5.0, 130.0, 200.0, 14.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(3)
    pdf.cell(35, 10, 'Ingreso a Urgencias', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(15, 10, 'Fecha', 0, 0, 'L')
    pdf.cell(10, 10, 'Hora', 0, 0, 'L')
    pdf.cell(35, 10, 'Paciente viene Remitido', 0, 0, 'L')
    pdf.cell(5, 10, 'Si', 0, 0, 'L')
    pdf.cell(35, 10, 'Paciente viene Remitido', 0, 0, 'L')
    pdf.ln(3)
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 107.0, 200.0, 3.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(55, 10, 'Nombre del prestador de servicios que remite:', 0, 0, 'L')
    pdf.cell(5, 10, 'Codigo:', 0, 0, 'L')

    pdf.ln(3)
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 109.0, 200.0, 3.0)  # Coordenadas x, y, ancho, alto
    # pdf.cell(200, 40, 'Motivo de consulta', 0, 0, 'C')
    pdf.set_line_width(0.3)
    pdf.rect(5.0, 112.0, 200.0, 3.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(4)
    pdf.rect(5.0, 147.0, 200.0, 10.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(200, 10, 'Examen Fisico', 0, 0, 'C')
    pdf.ln(2)

    pdf.cell(20, 10, 'Signos Vitales', 0, 0, 'L')
    pdf.cell(5, 10, 'FC', 0, 0, 'L')
    pdf.cell(15, 10, 'FR', 0, 0, 'L')
    pdf.cell(15, 10, 'TA', 0, 0, 'L')
    pdf.cell(15, 10, 'TA', 0, 0, 'L')
    pdf.cell(15, 10, 'Glasgow', 0, 0, 'L')
    pdf.cell(15, 10, 'Temp:', 0, 0, 'L')
    pdf.cell(15, 10, 'Peso:', 0, 0, 'L')
    pdf.ln(3)
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 105.0, 200.0, 20.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(3)

    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 150.0, 200.0, 12.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(35, 10, 'Impresion Diagnostica', 0, 0, 'L')
    pdf.cell(15, 10, 'Codigo', 0, 0, 'L')
    pdf.cell(25, 10, 'Descripcion', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(15, 10, 'Diagnostico Principal', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(15, 10, 'Relacionado 1', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(15, 10, 'Relacionado 2', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(15, 10, 'Relacionado 3', 0, 0, 'L')
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 143.0, 200.0, 8.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(3)
    pdf.rect(5.0, 177.0, 200.0, 9.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(15, 10, 'Destino del paciente', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(2)
    pdf.cell(45, 10, 'Domicilio', 0, 0, 'L')
    pdf.cell(45, 10, 'Internacion', 0, 0, 'L')
    pdf.cell(45, 10, 'ContraRemision', 0, 0, 'L')
    pdf.ln(2)
    pdf.cell(45, 10, 'Observacion', 0, 0, 'L')
    pdf.cell(45, 10, 'Remision', 0, 0, 'L')
    pdf.cell(45, 10, 'Otro', 0, 0, 'L')
    pdf.set_line_width(0.3)
    # pdf.rect(5.0, 125.0, 200.0, 10.0)  # Coordenadas x, y, ancho, alto
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(200, 10, 'INFORMACION DE LA PERSONA QUE INFORMA', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(3)
    pdf.cell(75, 10, 'Nombre de quien informa', 0, 0, 'L')
    pdf.cell(35, 10, 'Telefono', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(35, 10, 'Indicativo', 0, 0, 'L')
    pdf.cell(35, 10, 'Numero', 0, 0, 'L')
    pdf.cell(35, 10, 'Extension', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(35, 10, 'Cargo o Actividad', 0, 0, 'L')
    pdf.cell(35, 10, 'Telefono Celular', 0, 0, 'L')

    # pdf.output('C:/EntornosPython/temporal/temporal/atencionInicialUrgencias.pdf', 'F')

    linea = linea + 3
    pdf.ln(3)

    carpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'AtencionInicialUrgencias.pdf'
    print("archivo =", archivo)

    pdf.output(archivo, 'F')

    try:
        # Intenta abrir el archivo directamente
        #webbrowser.open(archivo)


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

    return JsonResponse({'success': True, 'message': 'Atencion Inicial de Urgencias impresa!'})


def ImprimirHojaAdmision(ingresoId):
    # Instantiation of inherited class

    print("ingresoId = ", ingresoId)

    print("Entre ImprimirHojaAdmision ", ingresoId)
    #ingresoId = request.POST["ingresoId"]

    ingresoPaciente = Ingresos.objects.get(id=ingresoId)
    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    pdf = PDFHojaAdmision(tipoDocId, documentoId, consec, ingresoId)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(1)
    linea = 7

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT ing.id id , to_char(ing."fechaIngreso",' + "'" + str('YYYY-MM-DD') + "')" + ' fechaIngreso, to_char (ing."fechaIngreso" , ' + "'" + str('HH:MM:SS') + "')" + '  horaIngreso, dep.numero cama, serv.nombre servIngreso, ext.nombre causaExterna,ing."numManilla" manilla, usu.nombre nombrePaciente, tipDoc.nombre tipDoc, usu.documento documento, ocupa.nombre ocupacion, estCivil.nombre estadoCivil, regimen.nombre regimen, mun.nombre municipio,  local.nombre localidad,usu.direccion direccion ,usu.telefono telefono, usu.correo correo, diag.nombre diagnostico , to_char(usu."fechaNacio", ' + "'" + str('YYYY-MM-DD')  + "')" + ' nacio, cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad, usu.genero sexo  FROM admisiones_ingresos ing INNER JOIN sitios_dependencias dep ON (dep."tipoDoc_id" = ing."tipoDoc_id" AND dep.documento_id = ing.documento_id AND ing.consec=dep.consec) INNER JOIN clinico_servicios serv ON (serv.id = ing."serviciosIng_id") LEFT JOIN clinico_causasexterna ext ON (ext.id = ing."causasExterna_id") INNER JOIN usuarios_usuarios usu ON (usu.id=ing.documento_id) LEFT JOIN usuarios_tiposdocumento tipDoc ON (tipDoc.id = ing."tipoDoc_id") LEFT JOIN basicas_ocupaciones ocupa ON (ocupa.id = usu.ocupacion_id) LEFT JOIN basicas_estadocivil estCivil ON (estCivil.id = usu."estadoCivil_id") LEFT JOIN clinico_regimenes regimen ON (regimen.id = ing.regimen_id)	LEFT JOIN sitios_municipios mun ON (mun.id=usu.municipio_id)	LEFT JOIN sitios_localidades local ON (local.id=usu.localidad_id) LEFT JOIN clinico_diagnosticos diag ON (diag.id=ing."dxIngreso_id") WHERE ing.id = ' + "'" + str(ingresoId) + "'"

    print(comando)

    curt.execute(comando)

    print(comando)

    hospitalizacion = []

    for id, fechaIngreso, horaIngreso, cama, servIngreso,causaExterna,manilla,nombrePaciente,tipDoc, documento, ocupacion, estadoCivil, regimen, municipio, localidad, direccion, telefono, correo, diagnostico ,nacio, edad, sexo in curt.fetchall():
        hospitalizacion.append(
            {'id':id, 'fechaIngreso': fechaIngreso, 'horaIngreso': horaIngreso,'cama':cama,'servIngreso':servIngreso,'causaExterna':causaExterna,
             'manilla': manilla,'nombrePaciente':nombrePaciente,'tipDoc':tipDoc,'documento':documento,  'ocupacion':ocupacion,'estadoCivil':estadoCivil,
             'regimen':regimen,'municipio':municipio, 'localidad':localidad,'direccion':direccion, 'telefono':telefono,'correo':correo,'diagnostico':diagnostico,
             'nacio':nacio, 'edad':edad,'sexo':sexo
             })

    miConexiont.close()
    print("hospitalizacion = ",hospitalizacion )


    # Define el ancho de línea
    pdf.set_line_width(0.4)
    # Dibuja el borde
    pdf.rect(5.0, 18.0, 200.0, 185.0)  # Coordenadas x, y, ancho, alto
    # Logo
    pdf.image('C:/EntornosPython/Pos7Particionado/vulner/static/img/MedicalFinal.jpg', 7, 19, 11, 11)
    # Arial bold 10
    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(3)
    pdf.cell(200, 10, 'HOJA DE ADMISION DEL PACIENTE', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 7)
    pdf.ln(1)

    pdf.cell(15, 10, 'Admision:', 0, 0, 'L')
    pdf.cell(15, 10, str(hospitalizacion[0]['id']), 0, 0, 'L')

    pdf.ln(3)
    #pdf.rect(5.0, 102.0, 200.0, 30.0)  # Coordenadas x, y, ancho, alto
    pdf.set_font('Helvetica', 'B', 7)
    #pdf.cell(25, 10, 'Admision:', 0, 0, 'L')
    #pdf.ln(3)
    #pdf.rect(200.0, 26, 200.0, 15.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(30, 10, 'Fecha Ingreso:', 0, 0, 'L')
    pdf.cell(15, 10, hospitalizacion[0]['fechaIngreso'], 0, 0, 'L')

    pdf.cell(20, 10, 'Hora Ingreso:', 0, 0, 'L')
    pdf.cell(15, 10, hospitalizacion[0]['horaIngreso'], 0, 0, 'L')
    pdf.cell(20, 10, 'Servicio:', 0, 0, 'L')
    pdf.cell(35, 10, hospitalizacion[0]['servIngreso'], 0, 0, 'L')

    pdf.cell(15, 10, 'Cama:', 0, 0, 'L')
    pdf.cell(25, 10, hospitalizacion[0]['cama'], 0, 0, 'L')
    pdf.ln(3)
    pdf.set_font('Helvetica', '', 8)
    #pdf.rect(200.0, 27, 200.0, 15.0)  # Coordenadas x, y, ancho, alto
    pdf.cell(25, 10, 'Via Ingreso:', 0, 0, 'L')
    pdf.cell(20, 10, 'Causa Externa:', 0, 0, 'L')
    pdf.cell(80, 10, hospitalizacion[0]['causaExterna'], 0, 0, 'L')
    pdf.cell(230, 10, 'Manilla de Identificacion#:', 0, 0, 'L')
    pdf.cell(20, 10, hospitalizacion[0]['manilla'], 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(3)
    #pdf.rect(200.0, 29, 200.0, 50.0)  # Coordenadas x, y, ancho, alto

    pdf.cell(30, 10, 'Apellidos y Nombres:', 0, 0, 'L')
    pdf.cell(100, 10, hospitalizacion[0]['nombrePaciente'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, 'Historia Clinica:', 0, 0, 'L')
    pdf.cell(30, 10, hospitalizacion[0]['tipDoc'], 0, 0, 'L')
    pdf.cell(20, 10, hospitalizacion[0]['documento'], 0, 0, 'L')
    pdf.ln(3)
    pdf.image('C:/EntornosPython/Pos7Particionado/vulner/static/img/CIRUGIAFINAL.JPG', 140, 45, 30, 30)
    pdf.cell(50, 10, 'Fecha de Nacimiento:', 0, 0, 'L')
    pdf.cell(20, 10, hospitalizacion[0]['nacio'], 0, 0, 'L')
    pdf.cell(8, 10, 'Edad:', 0, 0, 'L')
    pdf.cell(5, 10, hospitalizacion[0]['edad'], 0, 0, 'L')
    pdf.cell(8, 10, 'Sexo:', 0, 0, 'L')
    pdf.cell(5, 10, hospitalizacion[0]['sexo'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, 'Ocupacion:', 0, 0, 'L')
    pdf.cell(30, 10, str(hospitalizacion[0]['ocupacion']), 0, 0, 'L')
    pdf.cell(15, 10, 'Estado Civil:', 0, 0, 'L')
    pdf.cell(30, 10, str(hospitalizacion[0]['estadoCivil']), 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(100, 10, 'SEGURIDAD SOCIAL:', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, 'Regimen:', 0, 0, 'L')
    pdf.cell(20, 10, hospitalizacion[0]['regimen'], 0, 0, 'L')
    pdf.cell(50, 10, 'Usuario:', 0, 0, 'L')
    pdf.cell(10, 10, '', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, 'Nivel:', 0, 0, 'L')
    pdf.cell(50, 10, 'Poblacion especial:', 0, 0, 'L')

    ## ENTIDADES RESPONSABLE

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()


    comando = 'SELECT conv.nombre convenio FROM admisiones_ingresos ing LEFT JOIN facturacion_conveniospacienteingresos convPac ON (convPac."tipoDoc_id" = ing."tipoDoc_id" AND convPac.documento_id = ing.documento_id AND convPac."consecAdmision" = ing.consec) LEFT JOIN contratacion_convenios conv ON (conv.id = convPac.convenio_id) WHERE ing.id= ' + "'" + str(ingresoId) + "'"

    curt.execute(comando)

    print(comando)

    entidadesResponsables = []

    for convenio  in curt.fetchall():
        entidadesResponsables.append(
            {'convenio': convenio })

    miConexiont.close()

    pdf.ln(12)
    pdf.cell(50, 10, 'ENTIDADES RESPONSABLES:', 0, 0, 'L')
    pdf.cell(50, 10, '1.-', 0, 0, 'L')
    #pdf.cell(10, 10, entidadesResponsables[0]['convenio'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, '2.-', 0, 0, 'L')
    #pdf.cell(10, 10, entidadesResponsables[0]['convenio'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, '3.-', 0, 0, 'L')
    #pdf.cell(10, 10, entidadesResponsables[0]['convenio'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(50, 10, '4.-', 0, 0, 'L')
    #pdf.cell(10, 10, entidadesResponsables[0]['convenio'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(30, 10, 'Direccion del sitio de vivienda:', 0, 0, 'L')
    pdf.cell(30, 10, hospitalizacion[0]['direccion'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(20, 10, 'Telefono:', 0, 0, 'L')
    pdf.cell(30, 10, hospitalizacion[0]['telefono'], 0, 0, 'L')
    pdf.cell(30, 10, 'Municipio:', 0, 0, 'L')
    pdf.cell(30, 10, hospitalizacion[0]['municipio'], 0, 0, 'L')
    pdf.cell(30, 10, 'Zona:', 0, 0, 'L')
    pdf.cell(30, 10, hospitalizacion[0]['localidad'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(100, 10, 'Localidad:', 0, 0, 'L')
    pdf.cell(30, 10, hospitalizacion[0]['localidad'], 0, 0, 'L')
    pdf.cell(20, 10, 'Correo Electronico:', 0, 0, 'L')
    pdf.cell(30, 10, str(hospitalizacion[0]['correo']), 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(100, 10, 'DATOS DEL ACCIDENTE:', 0, 0, 'L')
    pdf.cell(100, 10, 'Direccion del accidente', 0, 0, 'L')
    pdf.cell(100, 10, 'Municipio del accidente', 0, 0, 'L')
    pdf.cell(100, 10, 'Condiciones del accidentado', 0, 0, 'L')
    pdf.cell(100, 10, 'Descripcion del accidente', 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(30, 10, 'Impresion Dx comentada', 0, 0, 'L')
    pdf.cell(100, 10, hospitalizacion[0]['diagnostico'], 0, 0, 'L')
    pdf.cell(30, 10, 'Servicio solicitado', 0, 0, 'L')
    pdf.ln(2)

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT usuContacto.nombre nombre, usuContacto.direccion direccion,usuContacto.telefono telefono,tiposFamilia.nombre tiposFamilia  FROM admisiones_ingresos ing LEFT JOIN usuarios_usuarioscontacto usuContacto ON (usuContacto.id = ing."contactoResponsable_id") LEFT JOIN basicas_tiposfamilia tiposFamilia ON (tiposFamilia.id = usuContacto."tiposFamilia_id") WHERE ing.id= ' + "'" + str(ingresoId) + "'"
    print(comando)
    curt.execute(comando)


    responsablePaciente = []

    for nombre, direccion, telefono, tiposFamilia in curt.fetchall():
        responsablePaciente.append(
            {'nombre': nombre,'direccion':direccion,'telefono':telefono, 'tiposFamilia':tiposFamilia  })

    miConexiont.close()

    pdf.cell(100, 10, 'Responsable del paciente', 0, 0, 'L')
    #pdf.cell(10, 10, responsablePaciente[0]['nombre'], 0, 0, 'L')
    pdf.cell(100, 10, 'L.D', 0, 0, 'L')
    pdf.cell(100, 10, 'Parentesco', 0, 0, 'L')
    #pdf.cell(10, 10, responsablePaciente[0]['tiposFamilia'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(100, 10, 'Direccion:', 0, 0, 'L')
    #pdf.cell(10, 10, responsablePaciente[0]['direccion'], 0, 0, 'L')
    pdf.cell(100, 10, 'Telefono:', 0, 0, 'L')
    #pdf.cell(10, 10, responsablePaciente[0]['telefono'], 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(100, 10, 'Usuario Capitado:', 0, 0, 'L')
    pdf.cell(100, 10, 'Responsable Admision:', 0, 0, 'L')
    pdf.ln(8)
    #pdf.rect(200.0, 49, 200.0, 100.0)  # Coordenadas x, y, ancho, alto

    pdf.set_font('Helvetica', 'B', 8)


    textoImpresion1 = '(Ley 1438 del 2011 Art. 143 Según Circular externa 0000033 de 2011 del MINISTERIO DE LA PROTECCION SOCIAL y Resolución 1915 del 2008). La informacion aquí registrada del evento catalogado como accidente de transito, es declarada bajo la gravedad de juramento por el usuario: con documento de identificación numero:  quien reside en la dirección:     Barrio:    Municipio de:     en calidad de paciente y/o acudiente del paciente:___________________________ con documento de identificación numero:_______________,   donde resulto afectado por vehiculo automotor en movimiento.: - Mediante la firma de esta declaración, confirma la veracidad y exactitud de las declaraciones que formula y , manifestando que nada ha ocultado ,omitido o alterado y se da por enterado que esta declaración constituye para la Compañía prestadora de servcicios en salud información determinante del siniestro , provocándolo intencionalmente, presentándolo ante el asegurador como ocurrido por causas o en circunstancias distintas a las verdaderas, ocultando la cosa asegurada o aumentando fraudulentamente las pérdidas efectivamente sufridas, incurre en el delito de fraude al seguro establecido en el artículo 470, número 10 del código final.g o en mi representacion __________________________________________ identificado con ___________________   Declaro que la informacion y/o documentacion aportada y consignada en el presente formato es cierta, veraz y verificable; razón por la cual autorizo su posterior verificacion por parte de la aseguradora y de la misma institucion. Teniendo en cuenta el artículo 9 de la Ley 1581 de 2012 “Por la cual se dictan disposiciones generales para la proteccion de datos personales”, autorizo expresamente a la Clínica Medical S.A.S. a divulgar la informacion aqui reposada tanto internamente como a EPS, aseguradoras, entes de control y demas entidades que la requieran y que esten autorizadas para tal fin, siempre y cuando dicha divulgacion este relacionada con los motivos por los cuales recibí tratamiento en esta Institucion prestadora de salud. De igual'

    pdf.multi_cell(w=300, h=3, txt=textoImpresion1, border=0, align='J', fill=False)           
    pdf.ln(4)

    pdf.cell(30, 10, 'Nombre Completo:', 0, 0, 'L')
    pdf.cell(40, 10, hospitalizacion[0]['nombrePaciente'], 0, 0, 'L')

    pdf.ln(4)
    pdf.cell(30, 10, 'Identificacion:',  0, 0, 'L')
    pdf.cell(40, 10, hospitalizacion[0]['documento'], 0, 0, 'L')

    pdf.ln(4)
    pdf.cell(30, 10,'Parentesco:', 0, 0, 'L')
    pdf.cell(40, 10, 'PACIENTE', 0, 0, 'L')

    #pdf.output('C:/EntornosPython/temporal/temporal/hojaAdmision.pdf', 'F')

    linea = linea + 3
    pdf.ln(5)

    #carpeta = 'C:\EntornosPython\Pos7Particionado\vulner\JSONCLINICA\HistoriasClinicas\'
    carpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'HojaAdmision.pdf'
    print("archivo =", archivo)

    pdf.output(archivo, 'F')

    try:
        # Intenta abrir el archivo directamente
        #webbrowser.open(archivo)


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

    return JsonResponse({'success': True, 'message': 'Hoja Admsision impresa!'})


def ImprimirManilla(ingresoId):
    # Instantiation of inherited class

    print("ingresoId = ", ingresoId)

    # ingresoId = request.POST["ingresoId"]

    ingresoPaciente = Ingresos.objects.get(id=ingresoId)
    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")


    curt = miConexiont.cursor()

    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento, usu."primerNombre",usu."segundoNombre",usu."primerApellido", usu."segundoApellido", cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad , usu.genero sexo, ing."fechaIngreso" fechaIngreso FROM admisiones_ingresos ing INNER JOIN usuarios_usuarios usu ON (usu.id=ing.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") WHERE ing.id= ' + "'" + str(
        ingresoId) + "'"
    print(comando)

    curt.execute(comando)

    print(comando)

    manilla = []

    for abrev, documento, primerNombre, segundoNombre, primerApellido, segundoApellido, edad, sexo, fechaIngreso in curt.fetchall():
        manilla.append(
            {'abrev': abrev, 'documento': documento, 'primerNombre': primerNombre, 'segundoNombre': segundoNombre,
             'primerApellido': primerApellido, 'segundoApellido': segundoApellido,
             'edad': edad, 'sexo': sexo, "fechaIngreso": fechaIngreso})

    miConexiont.close()
    print("manilla = ", manilla)

    pdf = PDFManilla(tipoDocId, documentoId, consec, ingresoId)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(1)
    linea = 7


    # Define el ancho de línea
    pdf.set_line_width(0.4)
    # Dibuja el borde
    pdf.rect(5.0, 15.0, 300.0, 30.0)  # Coordenadas x, y, ancho, alto

    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(3)
    pdf.cell(5, 10, 'Nombres:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 7)
    pdf.cell(25, 10, str(manilla[0]['primerNombre']), 0, 0, 'L')
    pdf.cell(25, 10, str(manilla[0]['segundoNombre']), 0, 0, 'L')
    pdf.cell(5, 10, 'Apellidos:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(manilla[0]['primerApellido']), 0, 0, 'L')
    pdf.cell(35, 10, str(manilla[0]['segundoApellido']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(100, 10, 'Riesgo:', 0, 0, 'C')
    pdf.ln(3)
    pdf.cell(15, 10, 'Identificacion:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(15, 10, str(manilla[0]['documento']), 0, 0, 'L')
    pdf.cell(15, 10, str(manilla[0]['edad']), 0, 0, 'L')
    pdf.cell(15, 10, str(manilla[0]['sexo']), 0, 0, 'L')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Fecha Hora de Ingreso:', 0, 0, 'C')
    pdf.cell(15, 10, str(manilla[0]['fechaIngreso']), 0, 0, 'L')
    pdf.ln(3)
    pdf.cell(5, 10, 'Alergias:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)

    carpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'Manilla.pdf'
    print("archivo =", archivo)

    pdf.output(archivo, 'F')

    try:
        # Intenta abrir el archivo directamente
        #webbrowser.open(archivo)


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

    return JsonResponse({'success': True, 'message': 'Manilla impresa!'})




def ImprimirTriage(request):
    # Instantiation of inherited class
    print("Entre imprimirTriage PAILAS")
    triageId = request.POST["triageId"]
    print("triageId = ", triageId)

    ingresoPaciente = Triage.objects.get(id=triageId)
    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)



    print("triageANTES = ")
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",     password="123456")

    curt = miConexiont.cursor()

    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento,usu.nombre nombre,  cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad , usu.genero sexo, tri."fechaSolicita" fechaSolicita , tri.motivo, tri."examenFisico",  tri."frecCardiaca", tri."frecRespiratoria", tri."taSist", tri."taDiast", tri."taMedia",  tri.glasgow, tri.peso, tri.temperatura, tri.estatura, tri.glucometria, tri.saturacion, tri."escalaDolor", cla.nombre triageNombre  FROM triage_triage tri INNER JOIN usuarios_usuarios usu ON (usu.id=tri.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") INNER JOIN clinico_tipostriage cla ON (cla.id= tri."clasificacionTriage_id") WHERE tri.id= ' + "'" + str(triageId) + "'"
    #comando = 'SELECT tipo.abreviatura abrev, usu.documento documento,usu.nombre nombre, usu


    print(comando)
    curt.execute(comando)
    print("triageDESPUES DE EXECUTA ")

    triage = []
    print("triage = ")

    for abrev, documento, nombre, edad, sexo, fechaSolicita, motivo,examenFisico, frecCardiaca,frecRespiratoria, taSist, taDiast, taMedia, glasgow,  peso, temperatura, estatura, glucometria, saturacion, escalaDolor, triageNombre   in curt.fetchall():
        triage.append(
            {'abrev': abrev, 'documento': documento, 'nombre':nombre ,
             'edad': edad, 'sexo': sexo, "fechaSolicita": fechaSolicita,'motivo':motivo,'examenFisico':examenFisico, 'frecCardiaca':frecCardiaca, 'frecRespiratoria':frecRespiratoria,
            'taSist':taSist,'taDiast':taDiast,'taMedia':taMedia,'glasgow':glasgow,'peso':peso, 'temperatura':temperatura, 'estatura':estatura,'glucometria':glucometria, 'saturacion':saturacion,'escalaDolor':escalaDolor,'triageNombre':triageNombre})

    miConexiont.close()


    pdf = PDFTriage(tipoDocId, documentoId, consec, triageId)
    print("triage = ")
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    print("triage antes font= ")
    pdf.set_font('Helvetica', '', 8)
    print("triage SERIF= ")
    pdf.ln(1)
    linea = 7


    # Define el ancho de línea
    pdf.set_line_width(0.4)
    # Dibuja el borde

    pdf.rect(5.0, 15.0, 200.0, 60.0)  # Coordenadas x, y, ancho, alto

    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(4)
    pdf.cell(180, 10, 'TRIAGE:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'FECHA:', 0, 0, 'L')
    print("triage FECHA= ", triage[0]['fechaSolicita'])
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(35, 10, str(triage[0]['fechaSolicita']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(4)
    pdf.cell(10, 10, 'TIPO:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['abrev']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(15, 10, 'DOCUMENTO:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['documento']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(15, 10, 'PACIENTE:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(60 , 10, str(triage[0]['nombre']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(8, 10, 'EDAD:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(10, 10, str(triage[0]['edad']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(8, 10, 'SEXO:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(10, 10, str(triage[0]['sexo']), 0, 0, 'L')
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(15, 10, 'MOTIVO:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.multi_cell(0, 10, str(triage[0]['motivo']), align='J')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(20, 10, 'EXAMEN FISICO:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.multi_cell(0, 10, str(triage[0]['examenFisico']), align='J')
    print("EXA.FISICO = ",triage[0]['examenFisico'] )
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(25, 10, 'FREC.CARDIACA:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['frecCardiaca']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(15, 10, 'FREC.RESPIRATORIA:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['frecRespiratoria']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(15, 10, 'FREC.CARDIACA:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['frecCardiaca']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    print("FREC.CARDIACAe = ")
    pdf.cell(15, 10, 'FREC.RESPIRATORIA:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['frecRespiratoria']), 0, 0, 'L')
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'SISTOLE:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['taSist']), 0, 0, 'L')
    print("TA.SIST = ")
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'DIASTOLE:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['taDiast']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'MEDIA:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['taMedia']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'GLASGOW:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['glasgow']), 0, 0, 'L')
    pdf.ln(4)

    print("triage = ", triageId)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'PESO:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['peso']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'TEMPERATURA:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['temperatura']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'ESTATURA:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['estatura']), 0, 0, 'L')
    print("triageestatura = ", triageId)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'GLASGOW:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['glasgow']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'GLUCOMETRIA:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['glucometria']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'SATURACION:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['saturacion']), 0, 0, 'L')
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(10, 10, 'ESCALADOLOR:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['escalaDolor']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(15, 10, 'TRIAGE:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(25, 10, str(triage[0]['triageNombre']), 0, 0, 'L')
    print("ESCALADORLO ")
    pdf.ln(4)

    carpeta = 'C:/EntornosPython/Pos7Particionado/vulner/JSONCLINICA/HistoriasClinicas/'
    print("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'Triage.pdf'
    print("archivo = ", archivo)

    #pdf.output(archivo, 'F', true)
    print("ya lo cree el  archivo =", archivo)

    try:
        # Intenta abrir el archivo directamente
        #webbrowser.open(archivo)
        buff = BytesIO()
        buff.name = archivo
        pdf.output(archivo, 'F')

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

    return JsonResponse({'success': True, 'message': 'Autorizacion impresa!'})


def ImprimirTriageParametro(triageId):
    # Instantiation of inherited class

    print("triageId = ", triageId)


    ingresoPaciente = Triage.objects.get(id=triageId)
    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")


    curt = miConexiont.cursor()

    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento, usu."primerNombre",usu."segundoNombre",usu."primerApellido", usu."segundoApellido", cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad , usu.genero sexo, ing."fechaIngreso" fechaIngreso FROM admisiones_ingresos ing INNER JOIN usuarios_usuarios usu ON (usu.id=ing.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") WHERE ing.id= ' + "'" + str(
        triageId) + "'"
    print(comando)

    curt.execute(comando)

    print(comando)

    manilla = []

    for abrev, documento, primerNombre, segundoNombre, primerApellido, segundoApellido, edad, sexo, fechaIngreso in curt.fetchall():
        manilla.append(
            {'abrev': abrev, 'documento': documento, 'primerNombre': primerNombre, 'segundoNombre': segundoNombre,
             'primerApellido': primerApellido, 'segundoApellido': segundoApellido,
             'edad': edad, 'sexo': sexo, "fechaIngreso": fechaIngreso})

    miConexiont.close()
    print("manilla = ", manilla)

    pdf = PDFTriage(tipoDocId, documentoId, consec, triageId)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(1)
    linea = 7


    # Define el ancho de línea
    pdf.set_line_width(0.4)
    # Dibuja el borde
    pdf.rect(5.0, 15.0, 200.0, 50.0)  # Coordenadas x, y, ancho, alto

    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(3)
    pdf.cell(100, 10, 'TRIAGE:', 0, 0, 'C')
    pdf.set_font('Helvetica', '', 8)

    carpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'Triage.pdf'
    print("archivo =", archivo)

    pdf.output(archivo, 'F')

    try:
        # Intenta abrir el archivo directamente
        webbrowser.open(archivo)


        #buff = BytesIO()
        #buff.name = archivo
        #Genera el archivo el el servidor

        #pdf.output(archivo, 'F')


        # 2. Abrir el archivo PDF y leerlo
        #with open(archivo, 'rb') as f:
        #    pdf_data = f.read()
        #    # 3. Escribir los datos en el buffer
        #    buff.write(pdf_data)

        #buff.seek(0)

        #return FileResponse(
        #    buff,
        #    as_attachment=True,  # Cambiar a False para verlo en navegador
        #    filename=archivo,
        #    content_type='application/pdf'
        #)
        #return

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

    return JsonResponse({'success': True, 'message': 'Autorizacion impresa!'})


