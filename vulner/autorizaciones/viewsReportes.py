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
from clinico.forms import  IncapacidadesForm, HistorialDiagnosticosCabezoteForm, HistoriaSignosVitalesForm, Historia
from autorizaciones.models import Autorizaciones
from django.db.models import Avg, Max, Min , Sum
from usuarios.models import Usuarios, TiposDocumento
from admisiones.models import Ingresos
from farmacia.models import Farmacia, FarmaciaDetalle, FarmaciaEstados
from enfermeria.models import Enfermeria, EnfermeriaDetalle
from facturacion.models import ConveniosPacienteIngresos

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


def ImprimirAut(request):
    # Instantiation of inherited class

    autorizacion = request.POST["autorizacionId"]
    autorizacionId = Autorizaciones.objects.get(id=autorizacion)
    historia = Historia.objects.get(id=autorizacion.historia_id)
  
    if (historia.consec == 0):
        flag='TRIAGE'
        triageId = Triage.objects.get(tipoDoc_id=historia.tipoDoc_id, documento_id=historia.documento_id, consec=historia.consecAdmision)
        pacienteId = Usuarios.objects.get(id=triageId.documento_id)

        print("documentoPaciente = ", pacienteId.documento)

    else:
        flag='INGRESO'
        ingresoId = Ingresos.objects.get(tipoDoc_id=historia.tipoDoc_id, documento_id=historia.documento_id, consec=historia.consecAdmision)
        pacienteId = Usuarios.objects.get(id=ingresoId.documento_id)
        ingresoId = ingreso.id


    print("autorizacionId = ", autorizacionId)
    print("ingresoId = ", ingresoId)

    tipoDocId = TiposDocumentos.objects.get(id=pacienteId.tipoDoc_id)
    print("tipoDocId = ", tipoDocId)

    # Datos de la empresa

   
    datosEmpresa = Empresas.objects.get(nombre='CLINICA MEDICAL S.A.S')

    # Fin Datos de la empresa

    ## Datos del paciente

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")


    curt = miConexiont.cursor()

    if (flag=='TRIAGE'):

	    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento, usu."primerNombre",usu."segundoNombre",usu."primerApellido", usu."segundoApellido", cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad , usu.genero sexo, ing."fechaIngreso" fechaIngreso FROM admisiones_ingresos ing INNER JOIN usuarios_usuarios usu ON (usu.id=ing.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") WHERE ing.id= ' + "'" + str(
        		ingresoId.id) + "'"
    else:
	    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento, usu."primerNombre",usu."segundoNombre",usu."primerApellido", usu."segundoApellido", cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad , usu.genero sexo, tri."fechaSolicitud" fechaIngreso FROM triage_triage tri INNER JOIN usuarios_usuarios usu ON (usu.id=tri.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") WHERE tri.id= ' + "'" + str(
        		triageId.id) + "'"

    print(comando)

    curt.execute(comando)

    datosPersonales = []

    for abrev, documento, primerNombre, segundoNombre, primerApellido, segundoApellido, edad, sexo, fechaIngreso in curt.fetchall():
        datosPersonales.append(
            {'abrev': abrev, 'documento': documento, 'primerNombre': primerNombre, 'segundoNombre': segundoNombre,
             'primerApellido': primerApellido, 'segundoApellido': segundoApellido,
             'edad': edad, 'sexo': sexo, "fechaIngreso": fechaIngreso})

    miConexiont.close()
    print("datosPersonales = ", datosPersonales)

    #  Fin datos paciente

    ## Datos DE LA SOLICITUD


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")


    curt = miConexiont.cursor()
    comando = 'SELECT autDet.cums_id,autdet.examenes_id,sum.nombre nombreInsumo, exa.nombre nompreProc, exa."codigoCups", sum.cums cums, autDet."cantidadSolicitada" FROM autorizaciones_autorizaciones aut INNER JOIN autorizaciones_autorizacionesdetalle autDet ON (autDet.autorizaciones_id=aut.id) WHERE aut.id = ' +"'" + str(autorizacionId.id) + "'"

    print(comando)

    curt.execute(comando)

    datosSolicitud = []

    for cums_id, examenes_id, nombreInsumo, nompreProc, codigoCups, cums, edad, sexo, fechaIngreso in curt.fetchall():
        datosSolicitud.append(
            {'cums_id': cums_id, 'examenes_id': examenes_id, 'nombreInsumo': nombreInsumo, ' nompreProc':  nompreProc,
             'codigoCups': codigoCups, 'cums': cums,
             'cantidadSolicitada': cantidadSolicitada})

    miConexiont.close()
    print("datosSolicitud = ", datosSolicitud)


    #  Fin datos de la solicitud

    ## Datos de quien solicita

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")


    curt = miConexiont.cursor()
    comando = 'SELECT pla.nombre, pla.telefono, pla.celular,  esp.nombre especialidad, 	med."registroMedico" FROM clinico_historia hist clinico_especialidadesmedicos espMed ON (espMed.id=hist."especialidadesMedicos_id" ) INNER JOIN planta_planta pla ON (pla.id=espMed.planta_id) INNER JOIN clinico_medicos med ON (med.planta_id=pla.id) INNER JOIN clinico_especialidades esp ON (esp.id=espMed.especialidades_id) WHERE hist =' + "'" + str(historia.id) + "'"

    print(comando)

    curt.execute(comando)

    datosDeQuienSolicita = []

    for nombre, telefono, celular, especialidad, registroMedico in curt.fetchall():
        datosDeQuienSolicita.append(
            {'nombre': nombre, 'telefono': telefono, 'celular': celular, 'especialidad': especialidad,
             'registroMedico': registroMedico})

    miConexiont.close()
    print("datosDeQuienSolicita = ", datosDeQuienSolicita)


    #  Fin datos de quien solicita



    # Datos personales paciente

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")


    curt = miConexiont.cursor()

    if (flag=='TRIAGE'):

	    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento, usu."primerNombre",usu."segundoNombre",usu."primerApellido", usu."segundoApellido", cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad , usu.genero sexo, ing."fechaIngreso" fechaIngreso FROM admisiones_ingresos ing INNER JOIN usuarios_usuarios usu ON (usu.id=ing.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") WHERE ing.id= ' + "'" + str(
        		ingresoId.id) + "'"
    else:
	    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento, usu."primerNombre",usu."segundoNombre",usu."primerApellido", usu."segundoApellido", cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text)   edad , usu.genero sexo, tri."fechaSolicitud" fechaIngreso FROM triage_triage tri INNER JOIN usuarios_usuarios usu ON (usu.id=tri.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id") WHERE tri.id= ' + "'" + str(
        		triageId.id) + "'"


    print(comando)

    curt.execute(comando)

    print(comando)

    datosPersonales = []

    for abrev, documento, primerNombre, segundoNombre, primerApellido, segundoApellido, edad, sexo, fechaIngreso in curt.fetchall():
        datosPersonales.append(
            {'abrev': abrev, 'documento': documento, 'primerNombre': primerNombre, 'segundoNombre': segundoNombre,
             'primerApellido': primerApellido, 'segundoApellido': segundoApellido,
             'edad': edad, 'sexo': sexo, "fechaIngreso": fechaIngreso})

    miConexiont.close()
    print("datosPersonales = ", datosPersonales)

    #  Fin datos personales paciente


    #pdf = PDFAutorizacion(tipoDocId, documentoId, consec, ingresoId)
    #pdf.alias_nb_pages()
    #pdf.set_margins(left=10, top=5, right=5)
    ##pdf.add_page()
    pdf.set_font('Times', '', 8)
    pdf.ln(1)



    # Define el ancho de línea
    pdf.set_line_width(0.4)
    # Dibuja el borde
    pdf.rect(5.0, 15.0, 200.0, 50.0)  # Coordenadas x, y, ancho, alto

    pdf.set_font('Times', 'B', 9)
    pdf.ln(3)
    pdf.cell(100, 30, 'AUTORIZACION:', 0, 0, 'C')
    pdf.cell(30, 30, 'cuarta linea', 0, 0, 'C')
    pdf.set_font('Times', '', 7)

    carpeta = 'C:\EntornosPython\Pos7Particionado/vulner/JSONCLINICA\HistoriasClinicas/'
    print("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'Autorizacion.pdf'
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

    return JsonResponse({'success': True, 'message': 'Autorizacion impresa!'})



