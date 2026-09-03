import json
from django import forms

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
from facturacion.models import Liquidacion, LiquidacionDetalle, Suministros, TiposSuministro, Empresas
#from contratacion.models import Procedimientos
from usuarios.models import Usuarios, TiposDocumento
from cartera.models  import Pagos
from autorizaciones.models import Autorizaciones,AutorizacionesDetalle, EstadosAutorizacion
from contratacion.models import Convenios
from cirugia.models import EstadosCirugias, EstadosProgramacion, ProgramacionCirugias
from tarifarios.models import TarifariosDescripcion, TarifariosProcedimientos, TarifariosSuministros
from clinico.forms import  IncapacidadesForm, HistorialDiagnosticosCabezoteForm, HistoriaSignosVitalesForm, Historia
from autorizaciones.models import Autorizaciones
from django.db.models import Avg, Max, Min , Sum
from usuarios.models import Usuarios, TiposDocumento
from admisiones.models import Ingresos
from farmacia.models import Farmacia, FarmaciaDetalle, FarmaciaEstados
from enfermeria.models import Enfermeria, EnfermeriaDetalle
from facturacion.models import ConveniosPacienteIngresos
from tarifarios.models import TiposHonorarios
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
import cgi

import os
import requests
import urllib
from django.http import FileResponse
from io import BytesIO
import io

class PDFConsentimientoInformado(FPDF):

    def __init__(self, tipoDocId, documentoId, consec, ingresoId2, flag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.ingresoId = ingresoId2
        self.flag = flag

    def header(self):
        # Logo
        print ("Entre encabezados reporte despacho")
        self.image('C:/EntornosPython/pos7Particionado/vulner/static/img/MedicalFinal.jpg', 180 ,20, 10 , 10)
        # Arial bold 15
        self.set_font('Helvetica', 'B', 7)

        # Move to the right
        # self.cell(12)
        print("voy a convenio")
        convenioId = ConveniosPacienteIngresos.objects.filter(tipoDoc_id=self.tipoDocId, documento_id=self.documentoId, consecAdmision=self.consec).aggregate(Max('convenio_id'))
        print("convenioId = ", convenioId['convenio_id__max'])
        convenio = convenioId['convenio_id__max']

        ## CURSOR PARA LEER ENCABEZADO
        #
        miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")

        curt = miConexiont.cursor()

        if (self.flag=='ADMISION'):

            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, u.documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str(
                'M') + "'" + ' then ' + "'" + str('Masculino') + "'" + ' when genero= ' + "'" + str(
                'F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, age("fechaNacio" ) edad,   reg.nombre regimen, convenio.nombre convenio , serv.nombre servicio, cast(now() as text) fecha from admisiones_ingresos adm INNER JOIN 	usuarios_usuarios u ON (u."tipoDoc_id" = adm."tipoDoc_id" and u.id = adm.documento_id) INNER JOIN usuarios_tiposDocumento tip ON (tip.id = u."tipoDoc_id") LEFT JOIN facturacion_conveniospacienteingresos  convIngreso ON (convIngreso."tipoDoc_id" = adm."tipoDoc_id" and convIngreso.documento_id = adm.documento_id and convIngreso."consecAdmision" = adm.consec) LEFT JOIN contratacion_convenios convenio ON (convenio.id = convIngreso.convenio_id AND convenio.id = ' + "'" + str(convenio) + "')" +  ' LEFT JOIN facturacion_empresas EMP on (emp.id =convenio.empresa_id ) LEFT JOIN clinico_regimenes reg ON (reg.id=emp.regimen_id) INNER JOIN sitios_serviciosSedes serv ON (serv.id = adm."serviciosActual_id")	 WHERE adm."tipoDoc_id" = ' + "'" + str(
                self.tipoDocId) + "'" + ' AND adm.documento_id= ' + "'" + str(
                self.documentoId) + "'" + ' AND adm.consec = ' + "'" + str(
                self.consec) + "'"
        else:

            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, u.documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str(
                'M') + "'" + ' then ' + "'" + str('Masculino') + "'" + ' when genero= ' + "'" + str(
                'F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, age("fechaNacio" ) edad,   reg.nombre regimen, convenio.nombre convenio , serv.nombre servicio, cast(now() as text) fecha from triage_triage tri INNER JOIN 	usuarios_usuarios u ON (u."tipoDoc_id" = tri."tipoDoc_id" and u.id = tri.documento_id) INNER JOIN usuarios_tiposDocumento tip ON (tip.id = u."tipoDoc_id") LEFT JOIN facturacion_conveniospacienteingresos  convIngreso ON (convIngreso."tipoDoc_id" = tri."tipoDoc_id" and convIngreso.documento_id = tri.documento_id and convIngreso."consecAdmision" = tri.consec) LEFT JOIN contratacion_convenios convenio ON (convenio.id = convIngreso.convenio_id AND convenio.id = ' + "'" + str(convenio) + "')" +  ' LEFT JOIN facturacion_empresas EMP on (emp.id =convenio.empresa_id ) LEFT JOIN clinico_regimenes reg ON (reg.id=emp.regimen_id) INNER JOIN sitios_serviciosSedes serv ON (serv.id = tri."serviciosSedes_id") WHERE tri."tipoDoc_id" = ' + "'" + str(
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
        print ("A imprimir pues")
        self.rect(10.0, 10.0, 195.0, 270.0)  # Coordenadas x, y, ancho, alto
        self.ln(5)
        print ("A imprimir pues1")
        self.set_font('Helvetica', 'B', 7)
        self.cell(50, 10, 'CLINICA MEDICAL', 0, 0, 'C')
        self.ln(5)
        print ("A imprimir pues2")
        self.cell(50, 10, 'CONSENTIMIENTO INFORMADO', 0, 0, 'C')
        self.ln(5)
        print ("A imprimir pues3")
        #pdf.cell(50, 10, '1. DATOS DEL PACIENTE', 0, 0, 'C')
        self.ln(5)
        #self.set_line_width(0.5)
        print ("A imprimir pues4")
        self.rect(10.0, 10.0, 195.0, 28)  # Coordenadas x, y, ancho, alto
        print ("ya comence A imprimir pues")
        self.set_font('Helvetica', 'B', 8)
        self.cell(25, 10, 'PACIENTE: ', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)

        self.cell(35, 10, historia[0]['tipnombre'], 0, 0, 'L')
        self.cell(20, 10, historia[0]['documentoPaciente'], 0, 0, 'L')
        self.cell(25, 10, historia[0]['nombre'], 0, 0, 'L')
        self.ln(5)
        self.set_font('Helvetica', 'B', 8)
        self.cell(25, 10, 'EDAD:', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)
        self.cell(50, 10, str(historia[0]['edad']), 0, 0, 'L')
        self.set_font('Helvetica', 'B', 8)
        self.cell(30, 10, 'GENERO:', 0, 0, 'L')
        self.set_font('Helvetica', '', 7)
        self.cell(50, 10, historia[0]['genero'], 0, 0, 'L')
        self.ln(5)
        self.set_font('Helvetica', 'B', 8)
        self.cell(25, 10, 'REGIMEN:', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)
        self.cell(50, 10, str(historia[0]['regimen']), 0, 0, 'L')
        self.ln(5)
        self.set_font('Helvetica', 'B', 8)
        self.cell(25, 10, 'CONVENIO:', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)
        self.cell(25, 10, str(historia[0]['convenio']), 0, 0, 'L')
        self.ln(5)
        self.set_font('Helvetica', 'B', 8)
        self.cell(25, 10, 'SERVICIO:', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)
        self.cell(25, 10, str(historia[0]['servicio']), 0, 0, 'L')
        self.ln(5)
        self.set_font('Helvetica', 'B', 8)
        self.cell(25, 10, 'FECHA:', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)
        self.cell(25, 10, historia[0]['fecha'], 0, 0, 'L')

        # Line break
        self.ln(3)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-30)
        # Arial italic 8
        self.set_font('Helvetica', 'B', 8)

        print("Etre footer consentimiento informado:")

        #miConexionii = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
        #                               password="123456")
        #curii = miConexionii.cursor()
        #comando = 'SELECT disp.despacho_id despacho, desp."usuarioEntrega_id" codEntrega , desp."usuarioRecibe_id" codRecibe, pla1.nombre entrega, pla2.nombre recibe  FROM farmacia_farmaciadespachos desp inner join farmacia_farmaciadespachosdispensa disp on (disp.despacho_id = desp.id) inner join planta_planta pla1 on (pla1.id= desp."usuarioEntrega_id") inner join planta_planta pla2 on (pla2.id= desp."usuarioRecibe_id") where desp.id = ' + "'" + str(self.despachoId) + "'"

        #curii.execute(comando)

        #print(comando)

        #registro = []

        #for depacho, codEntrega, codRecibe, entrega, recibe in curii.fetchall():
        #    registro.append(
        #        {'depacho': depacho, 'codEntrega': codEntrega, 'codRecibe': codRecibe, 'entrega': entrega,'recibe':recibe })
        #miConexionii.close()

        #self.set_line_width(0.4)
        #self.rect(10, 265.0, 195.0, 15.0)  # Coordenadas x, y, ancho, alto

        #self.set_font('Helvetica', 'B', 8)
        #pdf.cell(20, 10, '5. FIRMAS', 0, 0, 'L')
        #print('registro =', registro)
        #self.set_font('Helvetica', '', 8)
        #self.ln(6)
        #pdf.cell(20, 10, 'Firma del Paciente (o Representante Legal):', 0, 0, 'L')
        #self.ln(3)
        #self.cell(25, 1, '' + str(registro[0]['paciente']), 0, 0, 'L')
        #self.ln(5)
        #self.set_font('Helvetica', 'B', 8)
        #pdf.cell(20, 10, 'Nombre del Representante', 0, 0, 'L')
        #self.set_font('Helvetica', 'B', 8)
        #self.cell(25, 1, '' + str(registro[0]['nombreRepresentanteLegal']), 0, 0, 'L')
        #self.ln(5)
        #self.set_font('Helvetica', 'B', 8)
        #pdf.cell(20, 10, 'Documento del Representante', 0, 0, 'L')
        #self.set_font('Helvetica', 'B', 8)
        #self.cell(25, 1, '' + str(registro[0]['documentoRepresentanteLegal']), 0, 0, 'L')
        #self.ln(5)
        #self.set_font('Helvetica', 'B', 8)
        #pdf.cell(10, 10, 'Fecha Hora', 0, 0, 'L')
        #self.set_font('Helvetica', 'B', 8)
        #self.cell(25, 1, '' + str(registro[0]['fechaHora']), 0, 0, 'L')
        #self.ln(5)
        #self.set_font('Helvetica', 'B', 8)
        #pdf.cell(20, 10, 'Firma del Médico', 0, 0, 'L')
        #self.ln(5)
        #self.set_font('Helvetica', 'B', 8)
        #self.cell(25, 1, '' + str(registro[0]['firmaMedico']), 0, 0, 'L')
        #self.ln(5)
        #self.set_font('Helvetica', 'B', 8)
        #pdf.cell(20, 10, 'Nombre del Médico', 0, 0, 'L')
        #self.set_font('Helvetica', 'B', 8)
        #self.cell(25, 1, '' + str(registro[0]['nombreMedico']), 0, 0, 'L')

        #self.ln(5)
        #self.set_font('Helvetica', 'B', 8)
        #pdf.cell(20, 10, 'Registro Profesional (Matrícula)', 0, 0, 'L')
        #self.set_font('Helvetica', 'B', 8)
        #self.cell(25, 1, '' + str(registro[0]['registroProfesinal']), 0, 0, 'L')
        print ("chao footer")
        # Page number

        self.cell(150, 1, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def ImprimirConsentimientoInformado(request):
    # Instantiation of inherited class
    print("Entre consentimientoInformado")

    programacionId = request.POST["programacionId"]
    print("programacionId = ", programacionId)
    programacion = ProgramacionCirugias.objects.get(id=programacionId)
    print ("programacion tipoDoc_id= " , programacion.tipoDoc_id)
    print("programacion codumento_id= ", programacion.documento_id)
    print("programacion consecAdmision= ", programacion.consecAdmision)


    if (programacion.consecAdmision == 0):
        print("es triage")
        flag='TRIAGE'
        triageId = Triage.objects.get(tipoDoc_id=programacion.tipoDoc_id, documento_id=programacion.documento_id, consec=programacion.consecAdmision)
        pacienteId = Usuarios.objects.get(id=triageId.documento_id)

        print("documentoPaciente = ", pacienteId.documento)

    else:
        print("es admision")
        flag='ADMISION'
        ingresoId = Ingresos.objects.get(tipoDoc_id=programacion.tipoDoc_id, documento_id=programacion.documento_id, consec=programacion.consecAdmision)
        print ("paso_1")
        pacienteId = Usuarios.objects.get(id=ingresoId.documento_id)
        print("paso_2", pacienteId  )
        print("paso_2", pacienteId.tipoDoc_id  )

    tipoDocId = TiposDocumento.objects.get(id=pacienteId.tipoDoc_id)
    print("tipoDocId = ", tipoDocId)

    # Datos de la empresa

   
    datosEmpresa = Empresas.objects.get(nombre='CLINICA MEDICAL S.A.S')
    print ("datosEmpresa =" , datosEmpresa)
    # Fin Datos de la empresa

    ## Datos del paciente

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")


    curt = miConexiont.cursor()

    if (flag!='TRIAGE'):

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
    print("datosPersonales ULT= ", datosPersonales)

    #  Fin datos paciente

    ## Datos DE LA SOLICITUD
    #  Fin datos de quien solicita

    tipoDocId=tipoDocId.id
    print("tipoDocId", tipoDocId)
    documentoId = ingresoId.documento_id
    print("documentoId",documentoId )
    consec = ingresoId.consec
    print("consec", consec)
    ingresoId2 = ingresoId.id
    print("ingresoId",ingresoId2 )

    pdf = PDFConsentimientoInformado(tipoDocId,documentoId, consec, ingresoId2, flag)
    print("comenzamos")

    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    print("hata aqui llegamos")
    pdf.add_page()
    print("de aui no pasa")
    pdf.set_font('Helvetica', 'B', 8)
    linea = 7

    print("Ya encabezados")
    # Cursor Lee los datos de la Cirugia
    nombreCirujanoId = TiposHonorarios.objects.get(nombre='CIRUJANO')

    miConexiont = psycopg2.connect(host="192.168.133.128", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()


    comando ='select exa.nombre nombreExamen, pla.nombre nombreMedico from cirugia_cirugias cir inner join cirugia_cirugiasprocedimientos cirProc ON (cirProc.cirugia_id = cir.id) inner join cirugia_cirugiasparticipantes cirPart ON (cirPart.cirugia_id = cir.id  and cirPart."cirugiaProcedimiento_id" = cirProc.id ) inner join clinico_examenes exa on (exa.id = cirProc.cups_id ) inner join tarifarios_tiposhonorarios hon on (hon.id = cirPart."tipoHonorarios_id") inner join clinico_medicos med on (med.id = cirPart.medico_id) inner join planta_planta pla on (pla.id=med.planta_id) WHERE cir.id= ' + "'" + str(programacion.cirugia_id) + "'" +' and hon.nombre =' + "'" + str(nombreCirujanoId.nombre) + "'"
    print(comando)
    curt.execute(comando)


    medico = []

    for nombreExamen, nombreMedico  in curt.fetchall():
        medico.append({'nombreExamen': nombreExamen, 'nombreMedico':nombreMedico})

    print("antes de cerrar conexion")
    miConexiont.close()

    print("medico = ", medico)

    if (medico != []):
        print ("entrre medico")
        linea = linea + 2
        pdf.ln(5)
        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(120, 10, 'CONSENTIMIENTO INFORMADO', 0, 0, 'C')
        pdf.set_font('Helvetica', '', 8)
        pdf.ln(5)

    for l in range(0, len(medico)):

        print ("entre medico len")

        pdf.cell(10, 10, '2. INFORMACION DEL PROCEDIMIENTO', 0, 0, 'L')
        print("pase len_1")
        pdf.cell(10, 10, 'Nombre del Procedimiento/Tratamiento', 0, 0, 'L')
        pdf.cell(25, 1, '' + str(medico[0]['nombreExamen']), 0, 0, 'L')
        pdf.ln(5)  
        pdf.cell(10, 10, 'Médico Tratante', 0, 0, 'L')
        pdf.cell(25, 1, '' + str(medico[0]['nombreMedico']), 0, 0, 'L') 
        pdf.cell(10, 10, 'Propósito y Descripción', 0, 0, 'L') 
        pdf.ln(5)
        print("pase len_2")
        pdf.cell(10, 10, '3. RIESGOS Y BENEFICIOS', 0, 0, 'L')
        pdf.cell(10, 10, 'Beneficios Esperados', 0, 0, 'L')
        pdf.ln(5)  
        print("pase len_3")
        pdf.cell(10, 10, 'Riesgos Comunes/Específicos', 0, 0, 'L')
        pdf.cell(10, 10, 'Alternativas', 0, 0, 'L')
        pdf.ln(5)  
        print("pase len_4")
        pdf.cell(10, 10, '4. DECLARACION DEL PROCEDIMIENTO', 0, 0, 'L')
        textoConsentimiento = 'He leído (o me han leído) este documento, he comprendido la información y he tenido la oportunidad de hacer preguntas. Entiendo que la medicina no es una ciencia exacta y no se me han garantizado resultados. Entiendo que puedo revocar este consentimiento en cualquier momento antes del procedimiento. Autorizo la realización de procedimientos adicionales necesarios si surge una emergencia.'
        print("pase len_5")
        pdf.multi_cell(w=0, h=4, txt=textoConsentimiento , border=0, align='J', fill=False)

        pdf.ln(6)

    carpeta = 'C:\\EntornosPython\\pos7Particionado\\vulner\\JSONCLINICA\\Consentimientos\\'
    print ("carpeta = ", carpeta)

    archivote = carpeta + '' + str('Consentimiento_') + str(pacienteId.documento) + '_' + str(consec) + '.pdf'

    print ("archivote =" , archivote)

    try:
        # Intenta abrir el archivo directamente
        print("archivo LISTO ANTES DE ABRIR=", archivote)

        buff = BytesIO()
        buff.name = archivote
        #Genera el archivo el el servidor

        pdf.output(archivote, 'F')

        print("archivo LISTO =", archivote)
        #webbrowser.open(archivote)

        # 2. Abrir el archivo PDF y leerlo

        print("voy a leer")
        with open(archivote, 'rb') as f:
            pdf_data = f.read()
            # 3. Escribir los datos en el buffer
            buff.write(pdf_data)

        buff.seek(0)

        print("voy a responder")

        return FileResponse(
            buff,
            as_attachment=False,  # Cambiar a False para verlo en navegador
            filename=archivote,
            content_type='application/pdf'
        )


    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivote}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

    return JsonResponse({'success': True, 'Mensajes': 'Consentimiento Informado impreso!'})

