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
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
# import onnx as onnx
# import onnxruntime as ort
import pyttsx3

import speech_recognition as sr
from django.core.serializers import serialize
from django.db.models.functions import Cast, Coalesce
from django.db.models import Avg, Max, Min
#from .forms import historiaForm, historiaExamenesForm
from datetime import datetime
from clinico.models import Historia, HistoriaExamenes, Examenes, TiposExamen, EspecialidadesMedicos, Medicos, Especialidades, TiposFolio, CausasExterna, EstadoExamenes, HistorialAntecedentes, HistorialDiagnosticos, HistorialInterconsultas, EstadosInterconsulta, HistorialIncapacidades,  HistoriaSignosVitales, HistoriaRevisionSistemas, HistoriaMedicamentos, Regimenes
from sitios.models import Dependencias
from planta.models import Planta
from facturacion.models import Liquidacion, LiquidacionDetalle, Suministros, TiposSuministro, Conceptos
#from contratacion.models import Procedimientos
from usuarios.models import Usuarios, TiposDocumento
from cartera.models  import Pagos
from autorizaciones.models import Autorizaciones,AutorizacionesDetalle, EstadosAutorizacion
from contratacion.models import Convenios
from cirugia.models import EstadosCirugias, EstadosProgramacion
from tarifarios.models import TarifariosDescripcion, TarifariosProcedimientos, TarifariosSuministros, TiposHonorarios
from clinico.forms import  IncapacidadesForm, HistorialDiagnosticosCabezoteForm, HistoriaSignosVitalesForm
from django.db.models import Avg, Max, Min , Sum
from usuarios.models import Usuarios, TiposDocumento
from admisiones.models import Ingresos
from farmacia.models import Farmacia, FarmaciaDetalle, FarmaciaEstados
from enfermeria.models import Enfermeria, EnfermeriaDetalle
from facturacion.models import ConveniosPacienteIngresos, Facturacion
from basicas.models import Parametros
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
from django.utils import timezone
from tarifarios.models import TarifariosDescripcionHonorarios

import os
import requests
import urllib
from django.http import FileResponse
from io import BytesIO
import io
from django.http import FileResponse




class PDFFacturacion(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, ingresoId, factura, flag, *args, **kwargs):
    #def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.ingresoId = ingresoId
        self.factura = factura
        self.flag = flag

    def header(self):

        ## CURSOR PARA EMPRESA
        #
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")

        curt = miConexiont.cursor()

        comando = 'select ' + "'" + str('Paciente en trauma') + "'" + ' seInforma, substring(cast(current_timestamp as text),1,10) fecha , substring(cast(current_time as text), 1,5) as time,emp.nombre nombreEmpresa, substring(sed.nit,1,9) nit, substring(sed.nit,9,1) nitVerificacion, sed."codigoHabilitacion" habilita,emp.direccion direccionPrestador, emp.telefono telefonoPrestador, dep.nombre departamentoPrestador, dep."departamentoCodigoDian" codigoDepartamentoPrestador, mun.nombre municipioPrestador FROM facturacion_empresas emp INNER JOIN sitios_sedesclinica sed ON (sed.id=1) INNER JOIN sitios_departamentos dep ON (dep.id=emp.departamento_id) INNER JOIN sitios_municipios mun ON (mun.id = emp.municipio_id) WHERE emp. nombre like (' + "'" + str('%MEDICAL%') + "')"

        print(comando)
        curt.execute(comando)


        empresa = []

        for seInforma, fecha, time, nombreEmpresa, nit, nitVerificacion, habilita, direccionPrestador, telefonoPrestador, departamentoPrestador, codigoDepartamentoPrestador, municipioPrestador in curt.fetchall():
            empresa.append(
                {'seInforma': seInforma, 'fecha': fecha, 'time': time, 'nombreEmpresa': nombreEmpresa,
                 'nit': nit, 'nitVerificacion': nitVerificacion, 'habilita': habilita,
                 'direccionPrestador': direccionPrestador, 'telefonoPrestador': telefonoPrestador,
                 'departamentoPrestador': departamentoPrestador,
                 'codigoDepartamentoPrestador': codigoDepartamentoPrestador, 'municipioPrestador': municipioPrestador})

        print("empresa =", empresa)

        miConexiont.close()

        print("voy por peunta FLAG")
        if (self.flag=='F'):

            factura = Facturacion.objects.get(id=self.factura)

        else:

            factura = Liquidacion.objects.get(id=self.factura)

        ## FIN CURSOR


        if (self.flag=='F'):
            print("voy por codigoqr", factura.codigoQr)

            self.image(factura.codigoQr, 180, 5, 20, 10)

        else:
            print("nada de codigoqr")
            #self.image(factura.codigoQr, 180, 5, 20, 10)
            pass

        print("voy por tirulos")


        self.ln(4)
        self.set_font('helvetica', 'B', 8)
        self.cell(180, 10, empresa[0]['nombreEmpresa'], 0, 0, 'C')
        self.ln(3)
        self.cell(77, 10, '', 0, 0, 'L')
        self.cell(10, 10, 'N.I.T: ', 0, 0, 'C')
        self.cell(13, 10, empresa[0]['nit'], 0, 0, 'L')
        self.cell(20, 10, empresa[0]['nitVerificacion'], 0, 0, 'L')

        self.ln(3)
        self.cell(60, 10, '', 0, 0, 'L')
        self.cell(30, 10, empresa[0]['direccionPrestador'], 0, 0, 'C')
        self.cell(5, 10, 'Tel:', 0, 0, 'L')
        self.cell(25, 10, empresa[0]['telefonoPrestador'], 0, 0, 'C')
        self.set_font('helvetica', '', 8)
        # Define el ancho de línea
        self.set_line_width(0.4)
        # Dibuja el borde

        self.rect(5.0, 24.0, 200.0, 230.0)  # Coordenadas x, y, ancho, alto el cudro mas grande
        self.ln(3)
        # Logo
        self.image('C:/EntornosPython/Pos7Particionado/vulner/static/img/MedicalFinal.jpg', 7, 5, 30, 17)
        # Arial bold 15
        self.set_font('helvetica', 'B', 8)
        self.ln(3)
        #self.cell(120, 10, 'Cufe : 6b7dd1910792ec82b16f5a30d83da5c8f10895b42e3a685a8ee0f0edfc9e32e087576ba23525a50091a6eeb5bd9a9c5e ', 0, 0, 'L')
        self.cell(7, 13,'Cufe : ', 0, 0, 'L')

        print("voy pr el CUFE")

        if (self.flag=='F'):

            self.cell(120, 10, str(factura.cufeDefinitivo), 0, 0, 'L')
        else:
            pass

        print("PASE CUFE")

        self.ln(5)
        self.set_font('helvetica', 'B', 8)
        if (self.flag=='F'):

            self.cell(60, 10, 'FACTURA ELECTRONICA DE VENTA:', 0, 0, 'L')

        else:

            self.cell(60, 10, 'PREFATURA:', 0, 0, 'L')


        self.cell(25, 10, str(self.factura), 0, 0, 'L')
        self.cell(20, 10, '', 0, 0, 'L')
        parametro1 = Parametros.objects.get(nombre='Factura_1')
        self.cell(60, 10, str(parametro1.parametro1), 0, 0, 'L')
        #self.cell(70, 10, 'AUTORETENEDOR EN RENTA RESOLUCION 151 DEL 14-01-2016', 0, 0, 'L')
        self.ln(3)
        self.set_font('helvetica', '', 8)
        self.cell(95, 10, '', 0, 0, 'L')
        parametro2 = Parametros.objects.get(nombre='Factura_2')
        self.cell(50, 10, str(parametro2.parametro1), 0, 0, 'L')
        #self.cell(50, 10, 'Gran Contribuyente Res. 0012220 de 26-12-2022 - Actividad económica 8610', 0, 0, 'L')
        self.ln(3)
        self.cell(10, 10, '', 0, 0, 'L')
        self.ln(3)
        fechaExpedicion = datetime.datetime.now()
        self.set_font('helvetica', 'B', 8)
        self.cell(35, 10, 'Fecha de Expedición:', 0, 0, 'L')
        self.cell(40, 10, str(fechaExpedicion), 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        self.set_font('helvetica', 'B', 8)
        self.cell(95, 10, 'Fecha de Vencimiento (Cartera):', 0, 0, 'L')
        #self.cell(30, 10, 'Pagina 1 de 4', 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        self.cell(30, 10, 'Pagina ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        self.ln(3)
        self.cell(30, 10, '', 0, 0, 'C')
        parametro3 = Parametros.objects.get(nombre='Factura_3')
        self.cell(130, 10, str(parametro3.parametro1), 0, 0, 'C')
        #self.cell(100, 10, 'Favor NO efectuar retención de Industria y Comercio e IVA - Somos agentes retenedores de IVA', 0, 0, 'L')
        self.ln(3)
        self.cell(30, 10, '', 0, 0, 'L')
        parametro4 = Parametros.objects.get(nombre='Factura_4')
        self.cell(130, 10, str(parametro4.parametro1), 0, 0, 'C')
        #self.cell(100, 10, 'Resolución DIAN # 18764069407849 del 22/04/2024 al 22/10/2025 de la CME342.410,00 a la CME500.000,00', 0, 0, 'L')
        self.set_line_width(0.4)
        # Dibuja el borde
        self.rect(5.0,62.0, 200.0, 7.0)  # Coordenadas x, y, ancho, alto
        self.ln(3)
        print("voy cusor paciente")

        ## CURSOR PARA PACIENTE
        #
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        curt = miConexiont.cursor()

        if (self.flag=='F'):

            #comando = 'SELECT ing.id ingreso , usu.nombre, usu."primerNombre"  primerNombre, usu."segundoNombre"  segundoNombre, usu."primerApellido"  primerApellido, usu."segundoApellido" segundoApellido , tipos.abreviatura abreviatura ,usu.documento documento , round(cast(cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text) as numeric)/365,0)   edad, ing."fechaIngreso" fechaIngreso, usu.direccion direccion, usu.telefono telefono,  ing."fechaSalida" fechaSalida, dep.nombre departamentoPaciente, mun.nombre municipioPaciente, ing.factura, emp.nombre nombreEmpresa, emp.documento nit 	FROM admisiones_ingresos ing  INNER JOIN facturacion_facturacion fac ON (fac."tipoDoc_id" = ing."tipoDoc_id" AND fac.documento_id=ing.documento_id AND fac."consecAdmision" = ing.consec) INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id"=ing."tipoDoc_id" AND usu.id=ing.documento_id)  INNER JOIN sitios_departamentos dep ON (dep.id=usu.departamentos_id) INNER JOIN sitios_municipios mun ON (mun.id = usu.municipio_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=ing."tipoDoc_id") INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN facturacion_empresas emp ON (emp.id=conv.empresa_id) WHERE ing.id = ' + "'" + str(self.ingresoId) + "'"
            print ("self.factura=" , self.factura)
            comando = 'SELECT ing.id ingreso , usu.nombre, usu."primerNombre"  primerNombre, usu."segundoNombre"  segundoNombre, usu."primerApellido"  primerApellido, usu."segundoApellido" segundoApellido , tipos.abreviatura abreviatura ,usu.documento documento , round(cast(cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text) as numeric)/365,0)   edad, ing."fechaIngreso" fechaIngreso, usu.direccion direccion, usu.telefono telefono,  ing."fechaSalida" fechaSalida, dep.nombre departamentoPaciente, mun.nombre municipioPaciente, convIng.convenio_id, emp.nombre nombreEmpresa, emp.documento nit 	FROM admisiones_ingresos ing  INNER JOIN facturacion_facturacion fac ON (fac.id= ' + "'" + str(self.factura) + "' AND " + '        fac."tipoDoc_id" = ing."tipoDoc_id" AND fac.documento_id=ing.documento_id AND fac."consecAdmision" = ing.consec) INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id"=ing."tipoDoc_id" AND usu.id=ing.documento_id)  INNER JOIN sitios_departamentos dep ON (dep.id=usu.departamentos_id) INNER JOIN sitios_municipios mun ON (mun.id = usu.municipio_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=ing."tipoDoc_id") INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN facturacion_empresas emp ON (emp.id=conv.empresa_id) INNER JOIN facturacion_conveniospacienteingresos convIng ON (convIng.factura_id=' + "'" + str(self.factura) + "'" + ') WHERE ing.id = ' + "'" + str(self.ingresoId) + "'"

        else:
            print("self.factura=", self.factura)

            #comando = 'SELECT ing.id ingreso , usu.nombre, usu."primerNombre"  primerNombre, usu."segundoNombre"  segundoNombre, usu."primerApellido"  primerApellido, usu."segundoApellido" segundoApellido , tipos.abreviatura abreviatura ,usu.documento documento , round(cast(cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text) as numeric)/365,0)   edad, ing."fechaIngreso" fechaIngreso, usu.direccion direccion, usu.telefono telefono,  ing."fechaSalida" fechaSalida, dep.nombre departamentoPaciente, mun.nombre municipioPaciente, ing.factura, emp.nombre nombreEmpresa, emp.documento nit 	FROM admisiones_ingresos ing  INNER JOIN facturacion_liquidacion fac ON (fac."tipoDoc_id" = ing."tipoDoc_id" AND fac.documento_id=ing.documento_id AND fac."consecAdmision" = ing.consec) INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id"=ing."tipoDoc_id" AND usu.id=ing.documento_id)  INNER JOIN sitios_departamentos dep ON (dep.id=usu.departamentos_id) INNER JOIN sitios_municipios mun ON (mun.id = usu.municipio_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=ing."tipoDoc_id") INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN facturacion_empresas emp ON (emp.id=conv.empresa_id) WHERE ing.id = ' + "'" + str(self.ingresoId) + "'"
            comando = 'SELECT ing.id ingreso , usu.nombre, usu."primerNombre"  primerNombre, usu."segundoNombre"  segundoNombre, usu."primerApellido"  primerApellido, usu."segundoApellido" segundoApellido , tipos.abreviatura abreviatura ,usu.documento documento , round(cast(cast((cast(now() as date)  - cast(usu."fechaNacio" as date)) as text) as numeric)/365,0)   edad, ing."fechaIngreso" fechaIngreso, usu.direccion direccion, usu.telefono telefono,  ing."fechaSalida" fechaSalida, dep.nombre departamentoPaciente, mun.nombre municipioPaciente, convIng.convenio_id, emp.nombre nombreEmpresa, emp.documento nit 	FROM admisiones_ingresos ing  INNER JOIN facturacion_liquidacion fac ON (fac.id= ' + "'" + str(self.factura) + "' AND " + ' fac."tipoDoc_id" = ing."tipoDoc_id" AND fac.documento_id=ing.documento_id AND fac."consecAdmision" = ing.consec) INNER JOIN usuarios_usuarios usu ON (usu."tipoDoc_id"=ing."tipoDoc_id" AND usu.id=ing.documento_id)  INNER JOIN sitios_departamentos dep ON (dep.id=usu.departamentos_id) INNER JOIN sitios_municipios mun ON (mun.id = usu.municipio_id) INNER JOIN usuarios_tiposdocumento tipos ON (tipos.id=ing."tipoDoc_id") INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN facturacion_empresas emp ON (emp.id=conv.empresa_id) INNER JOIN facturacion_conveniospacienteingresos convIng ON (convIng."tipoDoc_id" = ing."tipoDoc_id" AND convIng.documento_id=ing.documento_id AND convIng."consecAdmision" = ing.consec and convIng.convenio_id= conv.id )  WHERE ing.id = ' + "'" + str(self.ingresoId) + "'"

        print(comando)
        curt.execute(comando)



        paciente = []

        for ingreso, nombre,primerNombre, segundoNombre, primerApellido, segundoApellido, abreviatura,  documento, edad, fechaIngreso, direccion, telefono,fechaSalida , departamentoPaciente, municipioPaciente, factura, nombreEmpresa, nit in curt.fetchall():
          paciente.append(
            {'ingreso':ingreso,'nombre':nombre,  'primerNombre': primerNombre, 'segundoNombre': segundoNombre, 'primerApellido': primerApellido,
             'segundoApellido': segundoApellido, 'abreviatura': abreviatura, 'documento': documento,'edad':edad,
             'fechaIngreso': fechaIngreso, 'direccion': direccion, 'telefono': telefono,'fechaSalida':fechaSalida,
             'departamentoPaciente': departamentoPaciente, 'municipioPaciente': municipioPaciente, 'factura':factura,'nombreEmpresa':nombreEmpresa, 'nit':nit})

        miConexiont.close()

        print("PACIENTE = " , paciente)

        ## FIN CURSOR
        self.set_font('helvetica', 'B', 8)
        self.cell(30, 10, 'Nombre del Paciente:', 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        self.cell(100, 10, paciente[0]['nombre'], 0, 0, 'L')
        self.set_font('helvetica', 'B', 8)
        self.cell(15, 10, 'Admision:', 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        self.cell(15, 10, str(paciente[0]['ingreso']), 0, 0, 'L')
        self.ln(3)
        self.set_font('helvetica', 'B', 8)
        self.cell(30, 10, 'Identificación:', 0, 0, 'L')
        self.set_font('helvetica', '', 8)
        self.cell(5, 10, paciente[0]['abreviatura'], 0, 0, 'L')
        self.cell(50, 10, paciente[0]['documento'], 0, 0, 'L')
        self.set_font('helvetica', 'B', 8)
        self.cell(17, 10, 'Edad:', 0, 0, 'L')
        self.cell(25, 10, str(paciente[0]['edad']), 0, 0, 'L')
        self.cell(20, 10, 'Fec. Ingreso:', 0, 0, 'L')
        self.cell(20, 10, str(paciente[0]['fechaIngreso']), 0, 0, 'L')
        self.ln(3)
        self.cell(30, 10, 'Dirección:', 0, 0, 'L')
        self.cell(55, 10, paciente[0]['direccion'], 0, 0, 'L')
        self.cell(17, 10, 'Teléfono:', 0, 0, 'L')
        self.cell(25, 10, paciente[0]['telefono'], 0, 0, 'L')
        self.cell(20, 10, 'Fec. Egreso:', 0, 0, 'L')
        self.cell(20, 10, str(paciente[0]['fechaSalida']), 0, 0, 'L')
        self.ln(3)
        self.cell(30, 10, 'Municipio:', 0, 0, 'L')
        self.cell(50, 10, paciente[0]['municipioPaciente'], 0, 0, 'L')
        self.ln(3)
        self.cell(30, 10, 'Responsable:', 0, 0, 'L')
        self.cell(55, 10, paciente[0]['nombreEmpresa'], 0, 0, 'L')
        self.cell(17, 10, 'Nit:', 0, 0, 'L')
        self.cell(15, 10, paciente[0]['nit'], 0, 0, 'L')
        self.ln(3)
        self.set_line_width(0.4)

        print("de SALIDA EN titulos")

        # Dibuja el borde
        #self.rect(5.0,64.0, 200.0, 5.0)  # Coordenadas x, y, ancho, alto
        self.ln(3)
        self.cell(10, 10, 'CUPS', 0, 0, 'L')
        self.cell(20, 10, 'Cod.Tarifa', 0, 0, 'L')
        self.cell(120, 10, 'Descripcion', 0, 0, 'L')
        self.cell(12, 10, 'Cantidad', 0, 0, 'L')
        self.cell(20, 10, 'Vr.Unidad', 0, 0, 'L')
        self.cell(15, 10, 'Vr.Total', 0, 0, 'L')
        self.ln(5)
        self.cell(30, 10, 'Detallado de la Factura', 0, 0, 'L')
        self.ln(3)
        self.set_line_width(0.4)
        # Dibuja el borde
        #self.rect(5.0, 74.0, 200.0, 192.5)  # Coordenadas x, y, ancho, alto

class PDFPazYSalvo(FPDF):
    def __init__(self, tipoDocId, documentoId, consec, ingresoId1,  *args, **kwargs):
    #def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipoDocId = tipoDocId
        self.documentoId = documentoId
        self.consec = consec
        self.ingresoId = ingresoId1


    def header(self):
        # Move to the right
        # self.cell(12)

        ## CURSOR PARA LEER ENCABEZADO
        #

        # Line break
        print("Entre clas paz y salvo")
        self.ln(6)


def ImprimirFactura(request):


    # Instantiation of inherited class
    ingresoId1 = request.POST["ingresoId"]
    print ("Entre ImprimirFactura")

    llave = ingresoId1.split('-')
    print("llave = ", llave)
    print("primero=", llave[0])
    #print("segundo = ", llave[1])
    #print("tercero o convenio  = ", llave[2])
    factura=llave[0]

    print("factura = ", factura)
    facturaPaciente= Facturacion.objects.get(id=factura)

    # ingresoId = request.POST["ingresoId"]

    ingresoPaciente = Ingresos.objects.get(tipoDoc_id=facturaPaciente.tipoDoc_id, documento_id=facturaPaciente.documento_id, consec=facturaPaciente.consecAdmision)
    ingresoId=ingresoPaciente.id
    print("ingresoId = ", ingresoId)
    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    #fechaRegistro = timezone.now()
    fechaRegistro = timezone.now()

    tipoCirujano = TiposHonorarios.objects.get(nombre='CIRUJANO')
    tipoAnestesiologo = TiposHonorarios.objects.get(nombre='ANESTESIOLOGO')
    tipoAyudante = TiposHonorarios.objects.get(nombre='AYUDANTE')
    tipoDerechosSala = TiposHonorarios.objects.get(nombre='DERECHOS DE SALA')
    tipoMateriales = TiposHonorarios.objects.get(nombre='MATERIAL QX')

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
    print("voy fpdpf = ")

    pdf = PDFFacturacion(tipoDocId, documentoId, consec, ingresoId, factura ,'F',format="letter")
    print("vuelvofpdpf = ")
    #pdf.alias_nb_pages()
    print("que paso?? = ")
    pdf.set_margins(left=10, top=5, right=5)
    print("que paso?? = ")
    pdf.add_page()
    print("que paso?? = ")
    pdf.set_font('helvetica', 'B', 8)
    print("que paso?? = ")
    pdf.ln(1)

    print("que paso??xxxx = ")
    conceptoMedicamentos= Conceptos.objects.get(nombre='MEDICAMENTOS')
    print("volvi pdfp1")
    conceptoProcedimientosNoQx= Conceptos.objects.get(nombre='PROCEDIMIENTOS NO QX')
    conceptoProcedimientosQx= Conceptos.objects.get(nombre='PROCEDIMIENTOS QX')
    print("volvi pdfp2")
    honorarioSalas = TiposHonorarios.objects.get(nombre='DERECHOS DE SALA')
    print("volvi pdfp3")

    conceptoInsumosMedicos = Conceptos.objects.get(nombre='INSUMOS MEDICOS')
    print("volvi pdfp4")
    conceptoMaterialQx = Conceptos.objects.get(nombre='MATERIAL QX Y/O MATERIAL ESPEC')

    print("volvi pdfp5")

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    #comando = 'SELECT id, nombre nombreConcepto from facturacion_conceptos '
    comando = 'SELECT distinct con.id, con.nombre nombreConcepto from facturacion_conceptos con INNER JOIN clinico_examenes exa ON (exa.concepto_id = con.id) where exa.id in (select facdet.examen_id from facturacion_facturaciondetalle facdet where facdet.facturacion_id = ' + "'" + str(factura) + "')" + ' union SELECT distinct con.id, con.nombre nombreConcepto from facturacion_conceptos con INNER JOIN facturacion_suministros sum ON (sum.concepto_id = con.id) where sum.id in (select facdet.cums_id from facturacion_facturaciondetalle facdet where facdet.facturacion_id = ' + "'" + str(factura) + "')" + ' order by 1 asc '

    curt.execute(comando)

    print(comando)
    lineaConcepto=1
    conceptos = []
    subTotal=0;
    lineaDetalle=1

    contratacionConvenio = Convenios.objects.get(id=facturaPaciente.convenio_id)
    tarifariosHonorarios = TarifariosDescripcionHonorarios.objects.get(id=contratacionConvenio.tarifariosDescripcionHono_id)

    liquidaHonorarios=''

    if (tarifariosHonorarios.nombre=='ISS 2001'):
        liquidaHonorarios='ISS'

    if (tarifariosHonorarios.nombre == 'SOAT 2004'):
        liquidaHonorarios = 'SOAT'

    if (tarifariosHonorarios.nombre == 'PARTICULAR'):
        liquidaHonorarios = 'PARTICULAR'


    for id, nombreConcepto in curt.fetchall():
        conceptos.append(
            {'id': id, 'nombreConcepto': nombreConcepto})

        #pdf.cell(40, 26 + lineaConcepto, str(conceptos[0]['nombreConcepto']), 0, 0, 'C')
        pdf.ln(3)
        if (nombreConcepto != 'HONORARIOS'):

            pdf.set_font('helvetica', 'B', 8)
            pdf.cell(200, 10, str('___________________________________________________________________________________________________________________________'), 0, 0, 'L')
            pdf.ln(3)
            pdf.cell(200, 10, str(nombreConcepto), 0, 0, 'C')
            pdf.ln(1)
            pdf.cell(200, 10, str('___________________________________________________________________________________________________________________________'), 0, 0, 'L')
            pdf.set_font('helvetica', '', 8)
            pdf.ln(4)


        ## AQUI VIENE EL CURSOR DEL DETALLE DE LA FACTURA

        miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cury = miConexiony.cursor()

        print("Factura =", factura)
        print("Voy en concepto =", id)
        print("concepto medicamentos =" ,conceptoMedicamentos.id)


        if (id == conceptoProcedimientosNoQx.id):
            print ("Procedimiento Noqx")
            #comando = 'select exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, detFac.cantidad cantidad, detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + " AND exa.concepto_id = " +"'" + str(id) + "'" + ' ORDER BY exa."codigoCups"'
            pass


        if (id == conceptoProcedimientosQx.id):
            print ("Procedimiento qx")
            #comando = 'select exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, detFac.cantidad cantidad, detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + " AND exa.concepto_id = " +"'" + str(id) + "'" + ' ORDER BY exa."codigoCups"'
            pass

        if (id == conceptoInsumosMedicos.id):

            #comando = 'select sum.cums cups,tarSum."codigoHomologado" homologado, sum.nombre  descripcion, detFac.cantidad cantidad, 	detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionSum_id") LEFT JOIN tarifarios_tarifariossuministros tarSum ON (tarSum."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarSum."codigoCum_id" = detFac.cums_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" +   ' AND sum.concepto_id = ' + "'" + str(id) + "'" + ' ORDER BY sum.cums'
            comando = 'select sum.cums cups, ' + "' '" + ' homologado, sum.nombre  descripcion, detFac.cantidad cantidad,detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND sum.concepto_id = ' + "'" + str(conceptoInsumosMedicos.id) + "' ORDER BY sum.cums"
            print("entre iNSUMOS MEDICOS")



        if (id ==conceptoMaterialQx.id):

            #comando = 'select sum.cums cups,tarSum."codigoHomologado" homologado, sum.nombre  descripcion, detFac.cantidad cantidad, 	detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionSum_id") LEFT JOIN tarifarios_tarifariossuministros tarSum ON (tarSum."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarSum."codigoCum_id" = detFac.cums_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" +   ' AND sum.concepto_id = ' + "'" + str(id) + "'" + ' ORDER BY sum.cums'
            comando = 'select sum.cums cups, ' + "' '" + ' homologado, sum.nombre  descripcion, detFac.cantidad cantidad,detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND sum.concepto_id = ' + "'" + str(conceptoMaterialQx.id) + "' ORDER BY sum.cums"
            print("entre iNSUMOS MEDICOS")

        if (id == conceptoMedicamentos.id):

            comando = 'select sum.cums cups,tarSum."codigoHomologado" homologado, sum.nombre  descripcion, detFac.cantidad cantidad, 	detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionSum_id") LEFT JOIN tarifarios_tarifariossuministros tarSum ON (tarSum."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarSum."codigoCum_id" = detFac.cums_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" +   ' AND sum.concepto_id = ' + "'" + str(id) + "'" + ' ORDER BY sum.cums'
            print("entre Medicamentos")

        if (id != conceptoMedicamentos.id and id != conceptoProcedimientosQx.id and id != conceptoInsumosMedicos.id and id != conceptoMaterialQx.id):

            comando = 'select exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, detFac.cantidad cantidad, detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + " AND exa.concepto_id = " +"'" + str(id) + "'" + ' ORDER BY exa."codigoCups"'
            print ("entre proced Normales")

        print ("comando DE datos Facturacion Detalle", comando)
        cury.execute(comando)

        print("SIGO CON  concepto =", id)

        detalleFacturacion = []
        lineaDetalle = 1
        salvoConcepto = id

        ## Aqui comienza el detalle de cada item del concepto en cuestion
        if (id != conceptoProcedimientosQx.id):


            for cups, homologado, descripcion, cantidad, valorUnitario, valorTotal in cury.fetchall():
                detalleFacturacion.append(
                    {'cups': cups, 'homologado': homologado,'descripcion':descripcion, 'cantidad':cantidad,'valorUnitario':valorUnitario, 'valorTotal':valorTotal })

                print ("voy a imprimir concepto =" , id)
                if (len(descripcion) > 65):
	                pdf.ln(3)

                pdf.cell(15, 10, str(cups), 0, 0, 'L')
                if (homologado=='NoNe'):
                    homologado=''

                pdf.cell(15, 10, str(homologado), 0, 0, 'L')
                #pdf.cell(85, 10, str(descripcion), 0, 0, 'L')
                #pdf.multi_cell(w=100, h=10, txt=str(descripcion),  align='J')
                #pdf.multi_cell(w=85, h=3, txt=str(descripcion), align='L' )

                if (len(descripcion) < 65):
                     pdf.cell(120, 10, str(descripcion), 0, 0, 'L')

                else:
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.multi_cell(w=120, h=3, txt=str(descripcion), align='L' )
                    pdf.set_xy(x + 120, y)


                pdf.cell(15, 10, str(cantidad), 0, 0, 'L')
                pdf.cell(18, 10 , str(valorUnitario), 0, 0, 'L')
                pdf.cell(25, 10 , str(valorTotal), 0, 0, 'L')

                subTotal = subTotal + float(valorTotal)


                pdf.ln(3)
                lineaDetalle = lineaDetalle + 2
                #pdf.rect(5.0, 26 + lineaConcepto + lineaDetalle, 200.0, 0)  # Coordenadas x, y, ancho, alto

        else:

	        ## Por aqui es un Procedimiento Qx Detalle
            print ("Entre a liquidar cirugias con honorrios =" , liquidaHonorarios)

            if (liquidaHonorarios=='ISS'):
                liquidacionTotalesProc = []
                print("Entre a liquidar ISS cirugias ")
                comando = 'select exa.id idCups, exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, 1 cantidad,sum(detFac."valorUnitario") valorUnitario, sum(detFac."valorTotal") valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado = ' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac."tipoHonorario_id" is not null group by exa.id,  exa."codigoCups", tarProc."codigoHomologado",exa.nombre ORDER BY 2,1'
                print("COMANDO =", comando)
                cury.execute(comando)

                for idCups, cups, homologado, descripcion, cantidad, valorUnitario, valorTotal in cury.fetchall():


                    pdf.set_font('helvetica', 'B', 8)
                    print ("voy a comenzar a imprimir el total del procediento =" , id)
                    print("cups = ", cups)
                    print("idCups = ", idCups)
                    print("id = ", id)

                    subTotal = subTotal + float(valorTotal)

                    pdf.cell(15, 10, str(cups), 0, 0, 'L')
                    if (homologado == 'NoNe'):
                        homologado = ''

                    pdf.cell(15, 10, str(homologado), 0, 0, 'L')
                    pdf.cell(85, 10, str(descripcion), 0, 0, 'L')
                    pdf.cell(30, 10, str(cantidad), 0, 0, 'L')
                    pdf.cell(30, 10, str(valorUnitario), 0, 0, 'L')
                    pdf.cell(30, 10, str(valorTotal), 0, 0, 'L')
                    pdf.ln(4)
                    pdf.set_font('helvetica', '', 8)
                    # Ahora barro un CURSOR CON EL DETALLE DE LOS HONORARIOS

                    comando = 'select tipHono.id idHonorario,(select ' + "'" + str('Cod:') + "'" + '||' + "' '||" + ' tarIss."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoCirujano.id) + "'" + ' group by tarIss."homologado",exa.nombre) CIRUJANO, (select ' + "'" + str('Cod:') + "'||' '||" + 'tarIss."homologado" ||' + "'" + " $ '||" + ' sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) 	INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) 	INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoAnestesiologo.id) + "'" + ' group by tarIss."homologado",exa.nombre) ANESTESIOLOGO, (select ' + "'" + str('Cod:') + "'" + "||' '||" + 'tarIss."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id)  INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoAyudante.id) + "'" + ' group by tarIss."homologado",exa.nombre) AYUDANTE,	(select ' + "'" + str('Cod:') + "'" + "||' '||" + ' detFac."codigoHomologado" ||' + "' $ '||" + ' sum(detFac."valorTotal") 	FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and detFac."tipoHonorario_id" = ' + "'" + str(tipoDerechosSala.id) + "'" + ' GROUP BY   detFac."codigoHomologado",exa.nombre) SALAS  ,(select ' + "'" + str('Cod:') + "'||' '||" + ' detFac."codigoHomologado" ||' + "'" + str('$') + "'||" + ' sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablamaterialsuturacuracion tarMat ON (tarMat."tipoHonorario_id" = detFac."tipoHonorario_id" and tarMat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" +  str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarMat."tipoHonorario_id" = ' + "'" + str(tipoMateriales.id) + "'" + ' GROUP BY detFac."codigoHomologado",exa.nombre) MATERIALES  FROM tarifarios_tiposhonorarios tipHono WHERE tipHono.nombre in (' + "'" + str('CIRUJANO') + "')" + ' ORDER BY tipHono.id'

                    print ("COMANDO =" , comando)
                    cury.execute(comando)

                    pdf.cell(40, 10, 'HonorariosMedicos', 0, 0, 'L')
                    pdf.cell(40, 10, 'Anestesiologo', 0, 0, 'L')
                    pdf.cell(40, 10, 'Ayudantia', 0, 0, 'L')
                    pdf.cell(40, 10, 'Derechos de Sala', 0, 0, 'L')
                    pdf.cell(40, 10, 'Materiales', 0, 0, 'L')

                    pdf.ln(4)

                    print("voy a comenzar a imprimir LOS HONORARIOS DEPROCEDIMIENTO EN CUESTION")

                    for id, CIRUJANO, ANESTESIOLOGO, AYUDANTE, SALAS, MATERIALES in cury.fetchall():

                        if (SALAS == None):
                            SALAS = 0
                        if (AYUDANTE == None):
                            AYUDANTE = 0
                        if (ANESTESIOLOGO == None):
                            ANESTESIOLOGO = 0
                        if (CIRUJANO == None):
                            CIRUJANO = 0

                        if (MATERIALES == None):
                            MATERIALES = 0


                        pdf.cell(40, 10, str(CIRUJANO), 0, 0, 'L')
                        pdf.cell(40, 10, str(ANESTESIOLOGO), 0, 0, 'L')
                        pdf.cell(40, 10, str(AYUDANTE), 0, 0, 'L')
                        pdf.cell(40, 10, str(SALAS), 0, 0, 'L')
                        pdf.cell(40, 10, str(MATERIALES), 0, 0, 'L')

                        pdf.ln(4)

            if (liquidaHonorarios == 'SOAT'):

                liquidacionTotalesProc = []
                print("Entre a liquidar Cirugias SOAT")
                comando = 'select exa.id idCups, exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, 1 cantidad,sum(detFac."valorUnitario") valorUnitario, sum(detFac."valorTotal") valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado = ' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac."tipoHonorario_id" is not null group by exa.id,  exa."codigoCups", tarProc."codigoHomologado",exa.nombre ORDER BY 2,1'
                print("COMANDO =", comando)
                cury.execute(comando)

                for idCups, cups, homologado, descripcion, cantidad, valorUnitario, valorTotal in cury.fetchall():

                    print("voy a comenzar a imprimir el total del procediento =", id)
                    print("cups = ", cups)
                    print("idCups = ", idCups)
                    print("id = ", id)

                    subTotal = subTotal + float(valorTotal)
                    pdf.set_font('helvetica', 'B', 8)

                    pdf.cell(15, 10, str(cups), 0, 0, 'L')

                    if (homologado=='NoNe'):
                    	homologado=''

                    pdf.cell(15, 10, str(homologado), 0, 0, 'L')
                    pdf.cell(85, 10, str(descripcion), 0, 0, 'L')
                    pdf.cell(30, 10, str(cantidad), 0, 0, 'L')
                    pdf.cell(30, 10, str(valorUnitario), 0, 0, 'L')
                    pdf.cell(30, 10, str(valorTotal), 0, 0, 'L')
                    pdf.ln(4)
                    pdf.set_font('helvetica', '', 8)

                    # Ahora barro un CURSOR CON EL DETALLE DE LOS HONORARIOS

                    comando = 'select tipHono.id idHonorario,(select ' + "'" + str('Cod:') + "'" + '||' + "' '||" + ' tarSoat."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoCirujano.id) + "'" + ' group by tarSoat."homologado",exa.nombre) CIRUJANO, (select ' + "'" + str('Cod:') + "'||' '||" + 'tarSoat."homologado" ||' + "'" + " $ '||" + ' sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) 	INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoAnestesiologo.id) + "'" + ' group by tarSoat."homologado",exa.nombre) ANESTESIOLOGO, (select ' + "'" + str('Cod:') + "'" + "||' '||" + 'tarSoat."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id)  INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoAyudante.id) + "'" + ' group by tarSoat."homologado",exa.nombre) AYUDANTE,	(select ' + "'" + str('Cod:') + "'" + "||' '||" + ' detFac."codigoHomologado" ||' + "' $ '||" + ' sum(detFac."valorTotal") 	FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and detFac."tipoHonorario_id" = ' + "'" + str(tipoDerechosSala.id) + "'" + ' GROUP BY   detFac."codigoHomologado",exa.nombre) SALAS   ,(select ' + "'" + str('Cod:') + "'||' '||" + ' detFac."codigoHomologado" ||' + "'" + str('$') + "'||" + ' sum(detFac."valorTotal") FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablamaterialsuturacuracion tarMat ON (tarMat."tipoHonorario_id" = detFac."tipoHonorario_id" and tarMat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" +  str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarMat."tipoHonorario_id" = ' + "'" + str(tipoMateriales.id) + "'" + ' GROUP BY detFac."codigoHomologado",exa.nombre) MATERIALES FROM tarifarios_tiposhonorarios tipHono WHERE tipHono.nombre in (' + "'" + str('CIRUJANO') + "')" + ' ORDER BY tipHono.id'

                    print("COMANDO =", comando)
                    cury.execute(comando)

                    pdf.cell(40, 10, 'HonorariosMedicos', 0, 0, 'L')
                    pdf.cell(40, 10, 'Anestesiologo', 0, 0, 'L')
                    pdf.cell(40, 10, 'Ayudantia', 0, 0, 'L')
                    pdf.cell(40, 10, 'Derechos de Sala', 0, 0, 'L')
                    pdf.cell(40, 10, 'Materiales', 0, 0, 'L')

                    pdf.ln(4)

                    print("voy a comenzar a imprimir LOS HONORARIOS DEPROCEDIMIENTO EN CUESTION")

                    for id, CIRUJANO, ANESTESIOLOGO, AYUDANTE, SALAS, MATERIALES  in cury.fetchall():

                        if (SALAS == None):
                            SALAS = 0
                        if (AYUDANTE == None):
                            AYUDANTE = 0
                        if (ANESTESIOLOGO == None):
                            ANESTESIOLOGO = 0
                        if (CIRUJANO == None):
                            CIRUJANO = 0

                        if (MATERIALES == None):
                            MATERIALES = 0


                        pdf.cell(40, 10 + lineaDetalle, str(CIRUJANO), 0, 0, 'L')
                        pdf.cell(40, 10, str(ANESTESIOLOGO), 0, 0, 'L')
                        pdf.cell(40, 10, str(AYUDANTE), 0, 0, 'L')
                        pdf.cell(40, 10, str(SALAS), 0, 0, 'L')
                        pdf.cell(40, 10, str(MATERIALES), 0, 0, 'L')

                        pdf.ln(4)

            if (liquidaHonorarios == 'PARTICULAR'):
                pass

        ## FIN CURSOR DETALLE FACTURA

        pdf.ln(4)
        miConexiony.close()

        if (nombreConcepto != 'HONORARIOS'):

            pdf.cell(145, 10, ' ' , 0, 0, 'L')
            pdf.cell(30, 10, 'SubTotal ' , 0, 0, 'L')
            pdf.cell(30, 0, str(subTotal), 0, 0, 'L')
            pdf.ln(2)

        subTotal=0

    miConexiont.close()

    pdf.ln(8)


    miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cury = miConexiony.cursor()

    comando = 'SELECT "totalFactura" , ("totalRecibido"  - anticipos) abonos, anticipos, ' + "'" + str('0') + "'" + ' descuentos, "valorApagar" , "valorAPagarLetras" , planta.nombre usuario FROM facturacion_facturacion fac INNER JOIN planta_planta planta ON (planta.id="usuarioRegistro_id")   WHERE fac.id= ' + "'" + str(factura) + "'"


    cury.execute(comando)

    factura = []
    lineaDetalle=lineaDetalle +2

    for totalFactura, abonos, anticipos, descuentos, valorApagar, valorAPagarLetras, usuario in cury.fetchall():
        factura.append(
            {'totalFactura': totalFactura, 'abonos': abonos, 'anticipos': anticipos, 'descuentos': descuentos,
             'valorApagar': valorApagar,'valorAPagarLetras':valorAPagarLetras,'usuario':usuario})

    pdf.set_line_width(0.4)
    # Dibuja el borde
    #pdf.rect(5.0, 90.0, 200.0, 25)  # Coordenadas x, y, ancho, alto

    ## Aquip totales
    pdf.set_font('helvetica', 'B', 8)
    pdf.ln(4)
    pdf.cell(152, 10, 'Valor en letras', 0, 0, 'L')
    pdf.cell(30, 10, 'SubTotal Cargos:', 0, 0, 'L')
    pdf.cell(30, 10 , str(totalFactura), 0, 0, 'L')
    pdf.ln(3)

    pdf.cell(152, 10 , str(valorAPagarLetras), 0, 0, 'L')
    pdf.cell(30, 10, 'Abonos o Cuota:', 0, 0, 'L')
    pdf.cell(30, 10 , str(abonos), 0, 0, 'L')
    pdf.ln(3)

    pdf.cell(152, 10 , str(''), 0, 0, 'L')
    pdf.cell(30, 10, 'Anticipos:', 0, 0, 'L')
    pdf.cell(30, 10 , str(anticipos), 0, 0, 'L')

    pdf.ln(3)

    pdf.cell(152, 10 , str(''), 0, 0, 'L')
    pdf.cell(30, 10, 'Descuentos:', 0, 0, 'L')
    pdf.cell(30, 10 , str(descuentos), 0, 0, 'L')

    pdf.ln(3)

    pdf.cell(152, 10 , str(''), 0, 0, 'L')
    pdf.cell(30, 10, 'Valor a Pagar:', 0, 0, 'L')
    pdf.cell(30, 10 , str(valorApagar), 0, 0, 'L')

    pdf.ln(12)

    pdf.cell(40, 10, 'Facturado por:', 0, 0, 'L')
    pdf.cell(100, 10, str(usuario), 0, 0, 'L')
    pdf.cell(40, 10, 'Firma del Paciente o Reponsable:', 0, 0, 'L')

    pdf.ln(3)
    pdf.cell(40, 10, str(''), 0, 0, 'L')
    pdf.cell(40, 10, 'Facturador(a):', 0, 0, 'L')

    pdf.ln(8)
    pdf.cell(40, 10, 'Fecha de impresion:', 0, 0, 'L')
    pdf.cell(150, 10, str(fechaRegistro), 0, 0, 'L')

    miConexiont.close()

    print ("po aqui voy")

    carpeta = 'C:/EntornosPython/Pos7Particionado/vulner/JSONCLINICA/Facturas/PDF/'
    print("carpeta_ult = ", carpeta)

    archivo = carpeta + '' + 'Factura_' + str(facturaPaciente.id) + '.pdf'
    print("archivo_ult =", archivo)

    try:
        # Intenta abrir el archivo directamente

        buff = BytesIO()
        buff.name = archivo
        # Genera el archivo el el servidor

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

    # hasta aquip


    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': False, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')

    print("Por aqui me voy_2")


    return JsonResponse({'success': True, 'message': 'Factura impresa!'})



def ImprimirLiquidacion(request):

    # Instantiation of inherited class
    # Toco adaptar todo desde la Factura a la Liquidacion
    ingresoId1 = request.POST["ingresoId"]
    print ("Entre ImprimirLiquidacion", ingresoId1)

    llave = ingresoId1.split('-')
    print("llave = ", llave)
    print("primero=", llave[0])
    numeroIngreso = llave[1].strip()
    convenioId2= llave[2]
    print("numeroIngreso = ", numeroIngreso)
    print("convenioId2  = ", convenioId2)
    #Variable factura es el id de la liquidacion
    ingresoPac = Ingresos.objects.get(id=numeroIngreso)
    facturaPaciente= Liquidacion.objects.get(tipoDoc_id=ingresoPac.tipoDoc_id, documento_id=ingresoPac.documento_id, consecAdmision=ingresoPac.consec, convenio_id=convenioId2)
    factura=facturaPaciente.id

    print("factura = ", factura)

    ingresoPaciente = Ingresos.objects.get(tipoDoc_id=facturaPaciente.tipoDoc_id, documento_id=facturaPaciente.documento_id, consec=facturaPaciente.consecAdmision)
    ingresoId=ingresoPaciente.id
    print("ingresoId = ", ingresoId)
    tipoDocId = ingresoPaciente.tipoDoc_id
    print("tipoDocId = ", tipoDocId)
    documentoId = ingresoPaciente.documento_id
    print("documentoId = ", documentoId)
    consec = ingresoPaciente.consec
    print("consec = ", consec)
    pacienteId = Usuarios.objects.get(id=documentoId)
    print("documentoPaciente = ", pacienteId.documento)

    #fechaRegistro = timezone.now()
    fechaRegistro = timezone.now()

    tipoCirujano = TiposHonorarios.objects.get(nombre='CIRUJANO')
    tipoAnestesiologo = TiposHonorarios.objects.get(nombre='ANESTESIOLOGO')
    tipoAyudante = TiposHonorarios.objects.get(nombre='AYUDANTE')
    tipoDerechosSala = TiposHonorarios.objects.get(nombre='DERECHOS DE SALA')
    tipoMateriales = TiposHonorarios.objects.get(nombre='MATERIAL QX')


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

    pdf = PDFFacturacion(tipoDocId, documentoId, consec, ingresoId, factura , 'L' ,format="letter")
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('helvetica', '', 8)
    pdf.ln(1)
    linea = 7

    conceptoMedicamentos= Conceptos.objects.get(nombre='MEDICAMENTOS')
    conceptoProcedimientosNoQx= Conceptos.objects.get(nombre='PROCEDIMIENTOS NO QX')
    conceptoProcedimientosQx= Conceptos.objects.get(nombre='PROCEDIMIENTOS QX')
    honorarioSalas = TiposHonorarios.objects.get(nombre='DERECHOS DE SALA')
    conceptoInsumosMedicos = Conceptos.objects.get(nombre='INSUMOS MEDICOS')
    conceptoMaterialQx = Conceptos.objects.get(nombre='MATERIAL QX Y/O MATERIAL ESPEC')

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    #comando = 'SELECT id, nombre nombreConcepto from facturacion_conceptos '
    comando = 'SELECT distinct con.id, con.nombre nombreConcepto from facturacion_conceptos con INNER JOIN clinico_examenes exa ON (exa.concepto_id = con.id) where exa.id in (select facdet.examen_id from facturacion_liquidaciondetalle facdet where facdet.liquidacion_id = ' + "'" + str(factura) + "')" + ' union SELECT distinct con.id, con.nombre nombreConcepto from facturacion_conceptos con INNER JOIN facturacion_suministros sum ON (sum.concepto_id = con.id) where sum.id in (select facdet.cums_id from facturacion_liquidaciondetalle facdet where facdet.liquidacion_id = ' + "'" + str(factura) + "')" + ' order by 1 asc '

    curt.execute(comando)

    print(comando)
    lineaConcepto=1
    conceptos = []
    subTotal=0;
    lineaDetalle=1

    contratacionConvenio = Convenios.objects.get(id=facturaPaciente.convenio_id)
    tarifariosHonorarios = TarifariosDescripcionHonorarios.objects.get(id=contratacionConvenio.tarifariosDescripcionHono_id)

    liquidaHonorarios=''

    if (tarifariosHonorarios.nombre=='ISS 2001'):
        liquidaHonorarios='ISS'

    if (tarifariosHonorarios.nombre == 'SOAT 2004'):
        liquidaHonorarios = 'SOAT'

    if (tarifariosHonorarios.nombre == 'PARTICULAR'):
        liquidaHonorarios = 'PARTICULAR'


    for id, nombreConcepto in curt.fetchall():
        conceptos.append(
            {'id': id, 'nombreConcepto': nombreConcepto})

        #pdf.ln(1)

        if (nombreConcepto != 'HONORARIOS'):

            pdf.set_font('helvetica', 'B', 8)
            pdf.cell(200, 10, str('___________________________________________________________________________________________________________________________'), 0, 0, 'L')
            pdf.ln(3)
            pdf.cell(200, 10, str(nombreConcepto), 0, 0, 'C')
            pdf.ln(1)
            pdf.cell(200, 10, str('___________________________________________________________________________________________________________________________'), 0, 0, 'L')
            pdf.set_font('helvetica', '', 8)

            pdf.ln(4)

        ## AQUI VIENE EL CURSOR DEL DETALLE DE LA FACTURA

        miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cury = miConexiony.cursor()

        print("Factura =", factura)
        print("Voy en concepto =", id)
        print("concepto medicamentos =" ,conceptoMedicamentos.id)

        if (id == conceptoProcedimientosNoQx.id):
            print ("Procedimiento Noqx")
            #comando = 'select exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, detFac.cantidad cantidad, detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_facturaciondetalle detFac INNER JOIN facturacion_facturacion fac ON (fac.id=detFac.facturacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.facturacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + " AND exa.concepto_id = " +"'" + str(id) + "'" + ' ORDER BY exa."codigoCups"'
            pass


        if (id == conceptoProcedimientosQx.id):
            print ("Procedimiento qx")
            #comando = 'select exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, detFac.cantidad cantidad, detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + " AND exa.concepto_id = " +"'" + str(id) + "'" + ' ORDER BY exa."codigoCups"'
            pass

        if (id == conceptoInsumosMedicos.id):

            #comando = 'select sum.cums cups,tarSum."codigoHomologado" homologado, sum.nombre  descripcion, detFac.cantidad cantidad, 	detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionSum_id") LEFT JOIN tarifarios_tarifariossuministros tarSum ON (tarSum."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarSum."codigoCum_id" = detFac.cums_id ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" +   ' AND sum.concepto_id = ' + "'" + str(id) + "'" + ' ORDER BY sum.cums'
            comando = 'select sum.cums cups, ' + "' '" + ' homologado, sum.nombre  descripcion, detFac.cantidad cantidad,detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND sum.concepto_id = ' + "'" + str(conceptoInsumosMedicos.id) + "' ORDER BY sum.cums"
            print("entre iNSUMOS MEDICOS")


        if (id ==conceptoMaterialQx.id):

            #comando = 'select sum.cums cups,tarSum."codigoHomologado" homologado, sum.nombre  descripcion, detFac.cantidad cantidad, 	detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionSum_id") LEFT JOIN tarifarios_tarifariossuministros tarSum ON (tarSum."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarSum."codigoCum_id" = detFac.cums_id ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" +   ' AND sum.concepto_id = ' + "'" + str(id) + "'" + ' ORDER BY sum.cums'
            comando = 'select sum.cums cups, ' + "' '" + ' homologado, sum.nombre  descripcion, detFac.cantidad cantidad,detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND sum.concepto_id = ' + "'" + str(conceptoMaterialQx.id) + "' ORDER BY sum.cums"
            print("entre iNSUMOS MEDICOS")

        if (id == conceptoMedicamentos.id):

            comando = 'select sum.cums cups,tarSum."codigoHomologado" homologado, sum.nombre  descripcion, detFac.cantidad cantidad, 	detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionSum_id") LEFT JOIN tarifarios_tarifariossuministros tarSum ON (tarSum."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarSum."codigoCum_id" = detFac.cums_id ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" +   ' AND sum.concepto_id = ' + "'" + str(id) + "'" + ' ORDER BY sum.cums'
            print("entre Medicamentos")

        if (id != conceptoMedicamentos.id and id != conceptoProcedimientosQx.id and id != conceptoInsumosMedicos.id and id != conceptoMaterialQx.id):

            comando = 'select exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, detFac.cantidad cantidad, detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + " AND exa.concepto_id = " +"'" + str(id) + "'" + ' ORDER BY exa."codigoCups"'
            print ("entre proced Normales")

        print ("comando DE datos Facturacion Detalle", comando)
        cury.execute(comando)

        print("SIGO CON  concepto =", id)

        detalleFacturacion = []
        lineaDetalle = 1
        salvoConcepto = id

        ## Aqui comienza el detalle de cada item del concepto en cuestion
        #
        pdf.set_font('helvetica', '', 8)
        if (id != conceptoProcedimientosQx.id):

            for cups, homologado, descripcion, cantidad, valorUnitario, valorTotal in cury.fetchall():
                detalleFacturacion.append(
                    {'cups': cups, 'homologado': homologado,'descripcion':descripcion, 'cantidad':cantidad,'valorUnitario':valorUnitario, 'valorTotal':valorTotal })

                print ("voy a imprimir concepto =" , id)

                if (len(descripcion) > 65):
	                pdf.ln(3)

                pdf.cell(15, 10 , str(cups), 0, 0, 'L')

                if (homologado=='NoNe'):
                    homologado=''

                pdf.cell(15, 10, str(homologado), 0, 0, 'L')
                #pdf.cell(85, 10, str(descripcion), 0, 0, 'L')
                #pdf.multi_cell(w=100, h=10, txt=str(descripcion),  align='J')

                if (len(descripcion) < 65):
                     pdf.cell(120, 10, str(descripcion), 0, 0, 'L')
                else:
                    x = pdf.get_x()
                    y = pdf.get_y()
                    pdf.multi_cell(w=120, h=3, txt=str(descripcion), align='L' )
                    pdf.set_xy(x + 120, y)

                pdf.cell(15, 10 , str(cantidad), 0, 0, 'L')
                pdf.cell(18, 10 , str(valorUnitario), 0, 0, 'L')
                pdf.cell(25, 10 , str(valorTotal), 0, 0, 'L')

                subTotal = subTotal + float(valorTotal)

                #lineaDetalle=lineaDetalle +1

                pdf.ln(3)

                #pdf.rect(5.0, 26 + lineaConcepto + lineaDetalle, 200.0, 0)  # Coordenadas x, y, ancho, alto

        else:

	        ## Por aqui es un Procedimiento Qx Detalle
            print ("Entre a liquidar cirugias con honorrios =" , liquidaHonorarios)

            if (liquidaHonorarios=='ISS'):
                liquidacionTotalesProc = []
                print("Entre a liquidar ISS cirugias ")
                comando = 'select exa.id idCups, exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, 1 cantidad,sum(detFac."valorUnitario") valorUnitario, sum(detFac."valorTotal") valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" +  ' AND (detfac.anulado = ' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac."tipoHonorario_id" is not null group by exa.id,  exa."codigoCups", tarProc."codigoHomologado",exa.nombre ORDER BY 2,1'
                print("COMANDO =", comando)
                cury.execute(comando)

                for idCups, cups, homologado, descripcion, cantidad, valorUnitario, valorTotal in cury.fetchall():

                    pdf.set_font('helvetica', 'B', 8)
                    print ("voy a comenzar a imprimir el total del procediento =" , id)
                    print("cups = ", cups)
                    print("idCups = ", idCups)
                    print("id = ", id)

                    subTotal = subTotal + float(valorTotal)

                    pdf.cell(15, 10 , str(cups), 0, 0, 'L')

                    if (homologado == 'NoNe'):
                        homologado = ''

                    pdf.cell(15, 10 , str(homologado), 0, 0, 'L')
                    pdf.cell(85, 10 , str(descripcion), 0, 0, 'L')
                    pdf.cell(30, 10 , str(cantidad), 0, 0, 'L')
                    pdf.cell(30, 10 , str(valorUnitario), 0, 0, 'L')
                    pdf.cell(30, 10 , str(valorTotal), 0, 0, 'L')
                    pdf.ln(4)
                    pdf.set_font('helvetica', '', 8)

                    # Ahora barro un CURSOR CON EL DETALLE DE LOS HONORARIOS

                    #comando = 'select tipHono.id idHonorario,(select ' + "'" + str('Cod:') + "'" + '||' + "' '||" + ' tarIss."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoCirujano.id) + "'" + ' group by tarIss."homologado",exa.nombre) CIRUJANO, (select ' + "'" + str('Cod:') + "'||' '||" + 'tarIss."homologado" ||' + "'" + " $ '||" + ' sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) 	INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) 	INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoAnestesiologo.id) + "'" + ' group by tarIss."homologado",exa.nombre) ANESTESIOLOGO, (select ' + "'" + str('Cod:') + "'" + "||' '||" + 'tarIss."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id)  INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoAyudante.id) + "'" + ' group by tarIss."homologado",exa.nombre) AYUDANTE,	(select ' + "'" + str('Cod:') + "'" + "||' '||" + ' detFac."codigoHomologado" ||' + "' $ '||" + ' sum(detFac."valorTotal") 	FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablasalasdecirugiaiss tarSala ON (tarSala."tipoHonorario_id" = detFac."tipoHonorario_id" ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSala."tipoHonorario_id" = ' + "'" + str(tipoDerechosSala.id) + "'" + ' GROUP BY   detFac."codigoHomologado",exa.nombre) SALAS FROM tarifarios_tiposhonorarios tipHono WHERE tipHono.nombre in (' + "'" + str('CIRUJANO') + "')" + ' ORDER BY tipHono.id'
                    comando = 'select tipHono.id idHonorario,(select ' + "'" + str('Cod:') + "'" + '||' + "' '||" + ' tarIss."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoCirujano.id) + "'" + ' group by tarIss."homologado",exa.nombre) CIRUJANO, (select ' + "'" + str('Cod:') + "'||' '||" + 'tarIss."homologado" ||' + "'" + " $ '||" + ' sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) 	INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) 	INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoAnestesiologo.id) + "'" + ' group by tarIss."homologado",exa.nombre) ANESTESIOLOGO, (select ' + "'" + str('Cod:') + "'" + "||' '||" + 'tarIss."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id)  INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariosiss tarIss ON (tarIss."tiposHonorarios_id" = detFac."tipoHonorario_id" ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarIss."tiposHonorarios_id" = ' + "'" + str(tipoAyudante.id) + "'" + ' group by tarIss."homologado",exa.nombre) AYUDANTE,	(select ' + "'" + str('Cod:') + "'" + "||' '||" + ' detFac."codigoHomologado" ||' + "' $ '||" + ' sum(detFac."valorTotal") 	FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and detFac."tipoHonorario_id" = ' + "'" + str(tipoDerechosSala.id) + "'" + ' GROUP BY   detFac."codigoHomologado",exa.nombre) SALAS ,(select ' + "'" + str('Cod:') + "'||' '||" + ' detFac."codigoHomologado" ||' + "'" + str('$') + "'||" + ' sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablamaterialsuturacuracion tarMat ON (tarMat."tipoHonorario_id" = detFac."tipoHonorario_id" and tarMat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" +  str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarMat."tipoHonorario_id" = ' + "'" + str(tipoMateriales.id) + "'" + ' GROUP BY detFac."codigoHomologado",exa.nombre) MATERIALES  FROM tarifarios_tiposhonorarios tipHono WHERE tipHono.nombre in (' + "'" + str('CIRUJANO') + "')" + ' ORDER BY tipHono.id'


                    print ("COMANDO =" , comando)
                    cury.execute(comando)

                    pdf.cell(40, 10, 'HonorariosMedicos', 0, 0, 'L')
                    pdf.cell(40, 10, 'Anestesiologo', 0, 0, 'L')
                    pdf.cell(40, 10, 'Ayudantia', 0, 0, 'L')
                    pdf.cell(40, 10, 'Derechos de Sala', 0, 0, 'L')
                    pdf.cell(40, 10, 'Materiales', 0, 0, 'L')
                    pdf.ln(4)

                    print("voy a comenzar a imprimir LOS HONORARIOS DEPROCEDIMIENTO EN CUESTION")

                    for id, CIRUJANO, ANESTESIOLOGO, AYUDANTE, SALAS , MATERIALES in cury.fetchall():

                        if (SALAS == None):
                            SALAS = 0
                        if (AYUDANTE == None):
                            AYUDANTE = 0
                        if (ANESTESIOLOGO == None):
                            ANESTESIOLOGO = 0
                        if (CIRUJANO == None):
                            CIRUJANO = 0

                        if (MATERIALES == None):
                            MATERIALES = 0

                        pdf.cell(40, 10, str(CIRUJANO), 0, 0, 'L')
                        pdf.cell(40, 10, str(ANESTESIOLOGO), 0, 0, 'L')
                        pdf.cell(40, 10, str(AYUDANTE), 0, 0, 'L')
                        pdf.cell(40, 10, str(SALAS), 0, 0, 'L')
                        pdf.cell(40, 10, str(MATERIALES), 0, 0, 'L')


                        pdf.ln(4)

            if (liquidaHonorarios == 'SOAT'):

                liquidacionTotalesProc = []
                print("Entre a liquidar Cirugias SOAT")
                comando = 'select exa.id idCups, exa."codigoCups" cups,tarProc."codigoHomologado" homologado, exa.nombre  descripcion, 1 cantidad,sum(detFac."valorUnitario") valorUnitario, sum(detFac."valorTotal") valorTotal FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionProc_id") LEFT JOIN tarifarios_tarifariosprocedimientos tarProc ON (tarProc."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarProc."codigoCups_id" = detFac.examen_id ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado = ' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac."tipoHonorario_id" is not null group by exa.id,  exa."codigoCups", tarProc."codigoHomologado",exa.nombre ORDER BY 2,1'
                print("COMANDO =", comando)
                cury.execute(comando)

                for idCups, cups, homologado, descripcion, cantidad, valorUnitario, valorTotal in cury.fetchall():

                    print("voy a comenzar a imprimir el total del procediento =", id)
                    print("cups = ", cups)
                    print("idCups = ", idCups)
                    print("id = ", id)

                    subTotal = subTotal + float(valorTotal)
                    pdf.set_font('helvetica', 'B', 8)
                    pdf.cell(15, 10, str(cups), 0, 0, 'L')

                    if (homologado == 'NoNe'):
                        homologado = ''

                    pdf.cell(15, 10, str(homologado), 0, 0, 'L')
                    pdf.cell(85, 10, str(descripcion), 0, 0, 'L')
                    pdf.cell(30, 10, str(cantidad), 0, 0, 'L')
                    pdf.cell(30, 10, str(valorUnitario), 0, 0, 'L')
                    pdf.cell(30, 10, str(valorTotal), 0, 0, 'L')
                    pdf.ln(4)
                    pdf.set_font('helvetica', '', 8)

                    # Ahora barro un CURSOR CON EL DETALLE DE LOS HONORARIOS

                    #comando = 'select tipHono.id idHonorario,(select ' + "'" + str('Cod:') + "'" + '||' + "' '||" + ' tarSoat."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoCirujano.id) + "'" + ' group by tarSoat."homologado",exa.nombre) CIRUJANO, (select ' + "'" + str('Cod:') + "'||' '||" + 'tarSoat."homologado" ||' + "'" + " $ '||" + ' sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) 	INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoAnestesiologo.id) + "'" + ' group by tarSoat."homologado",exa.nombre) ANESTESIOLOGO, (select ' + "'" + str('Cod:') + "'" + "||' '||" + 'tarSoat."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id)  INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoAyudante.id) + "'" + ' group by tarSoat."homologado",exa.nombre) AYUDANTE,	(select ' + "'" + str('Cod:') + "'" + "||' '||" + ' detFac."codigoHomologado" ||' + "' $ '||" + ' sum(detFac."valorTotal") 	FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablasalasdecirugia tarSala ON (tarSala."tipoHonorario_id" = detFac."tipoHonorario_id" and tarSala."grupoQx_id" = exa."grupoQx_id"  )    where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSala."tipoHonorario_id" = ' + "'" + str(tipoDerechosSala.id) + "'" + ' GROUP BY   detFac."codigoHomologado",exa.nombre) SALAS FROM tarifarios_tiposhonorarios tipHono WHERE tipHono.nombre in (' + "'" + str('CIRUJANO') + "')" + ' ORDER BY tipHono.id'
                    comando = 'select tipHono.id idHonorario,(select ' + "'" + str('Cod:') + "'" + '||' + "' '||" + ' tarSoat."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)  INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoCirujano.id) + "'" + ' group by tarSoat."homologado",exa.nombre) CIRUJANO, (select ' + "'" + str('Cod:') + "'||' '||" + 'tarSoat."homologado" ||' + "'" + " $ '||" + ' sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) 	INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoAnestesiologo.id) + "'" + ' group by tarSoat."homologado",exa.nombre) ANESTESIOLOGO, (select ' + "'" + str('Cod:') + "'" + "||' '||" + 'tarSoat."homologado" ||' + "' $ '||" + 'sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id)  INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablahonorariossoat tarSoat ON (tarSoat."tiposHonorarios_id" = detFac."tipoHonorario_id" and tarSoat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + ' AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarSoat."tiposHonorarios_id" = ' + "'" + str(tipoAyudante.id) + "'" + ' group by tarSoat."homologado",exa.nombre) AYUDANTE,	(select ' + "'" + str('Cod:') + "'" + "||' '||" + ' detFac."codigoHomologado" ||' + "' $ '||" + ' sum(detFac."valorTotal") 	FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id)   where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" + str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and detFac."tipoHonorario_id" = ' + "'" + str(tipoDerechosSala.id) + "'" + ' GROUP BY   detFac."codigoHomologado",exa.nombre) SALAS ,(select ' + "'" + str('Cod:') + "'||' '||" + ' detFac."codigoHomologado" ||' + "'" + str('$') + "'||" + ' sum(detFac."valorTotal") FROM facturacion_liquidaciondetalle detFac INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) INNER JOIN clinico_examenes exa on (exa.id=detFac.examen_id) INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) INNER JOIN tarifarios_tablamaterialsuturacuracion tarMat ON (tarMat."tipoHonorario_id" = detFac."tipoHonorario_id" and tarMat."grupoQx_id" = exa."grupoQx_id"  ) where detfac.liquidacion_id= ' + "'" + str(factura) + "'" + ' AND (detfac.anulado =' + "'" + str('N') + "'" + ' or detfac.anulado=' + "'" + str('R') + "')" + '  AND exa.concepto_id = ' + "'" +  str(salvoConcepto) + "'" + ' and detFac.examen_id= ' + "'" + str(idCups) + "'" + ' and tarMat."tipoHonorario_id" = ' + "'" + str(tipoMateriales.id) + "'" + ' GROUP BY detFac."codigoHomologado",exa.nombre) MATERIALES  FROM tarifarios_tiposhonorarios tipHono WHERE tipHono.nombre in (' + "'" + str('CIRUJANO') + "')" + ' ORDER BY tipHono.id'

                    print("COMANDO =", comando)
                    cury.execute(comando)

                    pdf.cell(40, 10, 'HonorariosMedicos', 0, 0, 'L')
                    pdf.cell(40, 10, 'Anestesiologo', 0, 0, 'L')
                    pdf.cell(40, 10, 'Ayudantia', 0, 0, 'L')
                    pdf.cell(40, 10, 'Derechos de Sala', 0, 0, 'L')
                    pdf.cell(40, 10, 'Materiales', 0, 0, 'L')
                    pdf.ln(4)

                    print("voy a comenzar a imprimir LOS HONORARIOS DEPROCEDIMIENTO EN CUESTION")

                    for id, CIRUJANO, ANESTESIOLOGO, AYUDANTE, SALAS , MATERIALES in cury.fetchall():

                        if (SALAS == None):
                            SALAS = 0
                        if (AYUDANTE == None):
                            AYUDANTE = 0
                        if (ANESTESIOLOGO == None):
                            ANESTESIOLOGO = 0
                        if (CIRUJANO == None):
                            CIRUJANO = 0

                        if (MATERIALES == None):
                            MATERIALES = 0


                        pdf.cell(40, 10, str(CIRUJANO), 0, 0, 'L')
                        pdf.cell(40, 10, str(ANESTESIOLOGO), 0, 0, 'L')
                        pdf.cell(40, 10, str(AYUDANTE), 0, 0, 'L')
                        pdf.cell(40, 10, str(SALAS), 0, 0, 'L')
                        pdf.cell(40, 10, str(MATERIALES), 0, 0, 'L')

                        pdf.ln(4)

            if (liquidaHonorarios == 'PARTICULAR'):
                pass



        ## FIN CURSOR DETALLE FACTURA

        pdf.ln(4)


        miConexiony.close()
        if (nombreConcepto != 'HONORARIOS'):

            pdf.cell(150, 10 , ' ' , 0, 0, 'L')
            pdf.cell(30, 10  , 'SubTotal ' , 0, 0, 'L')
            pdf.cell(35, 10 , str(subTotal), 0, 0, 'L')
            pdf.ln(2)
        subTotal=0

    miConexiont.close()

    pdf.ln(8)


    miConexiony = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    cury = miConexiony.cursor()

    comando = 'SELECT "totalLiquidacion" , ("totalRecibido"  - anticipos) abonos, anticipos, ' + "'" + str('0') + "'" + ' descuentos, "valorApagar" , ' + "' '" + '  valorAPagarLetras , planta.nombre usuario FROM facturacion_liquidacion fac INNER JOIN planta_planta planta ON (planta.id="usuarioRegistro_id")   WHERE fac.id= ' + "'" + str(factura) + "'"


    cury.execute(comando)

    factura = []
    lineaDetalle=lineaDetalle +2

    for totalFactura, abonos, anticipos, descuentos, valorApagar, valorAPagarLetras, usuario in cury.fetchall():
        factura.append(
            {'totalFactura': totalFactura, 'abonos': abonos, 'anticipos': anticipos, 'descuentos': descuentos,
             'valorApagar': valorApagar,'valorAPagarLetras':valorAPagarLetras,'usuario':usuario})

    pdf.set_line_width(0.4)
    # Dibuja el borde
    #pdf.rect(5.0, 90.0, 200.0, 25)  # Coordenadas x, y, ancho, alto

    ## Aquip totales
    pdf.set_font('helvetica', 'B', 8)
    pdf.ln(4)
    pdf.cell(152, 10, 'Valor en letras', 0, 0, 'L')
    pdf.cell(30, 10, 'SubTotal Cargos:', 0, 0, 'L')
    pdf.cell(30, 10 , str(totalFactura), 0, 0, 'L')
    pdf.ln(3)

    pdf.cell(152, 10 , str(valorAPagarLetras), 0, 0, 'L')
    pdf.cell(30, 10, 'Abonos o Cuota:', 0, 0, 'L')
    pdf.cell(30, 10 , str(abonos), 0, 0, 'L')
    pdf.ln(3)

    pdf.cell(152, 10 , str(''), 0, 0, 'L')
    pdf.cell(30, 10, 'Anticipos:', 0, 0, 'L')
    pdf.cell(30, 10 , str(anticipos), 0, 0, 'L')

    pdf.ln(3)

    pdf.cell(152, 10 , str(''), 0, 0, 'L')
    pdf.cell(30, 10, 'Descuentos:', 0, 0, 'L')
    pdf.cell(30, 10 , str(descuentos), 0, 0, 'L')

    pdf.ln(3)

    pdf.cell(152, 10 , str(''), 0, 0, 'L')
    pdf.cell(30, 10, 'Valor a Pagar:', 0, 0, 'L')
    pdf.cell(30, 10 , str(valorApagar), 0, 0, 'L')

    pdf.ln(12)

    pdf.cell(40, 10, 'Facturado por:', 0, 0, 'L')
    pdf.cell(100, 10, str(usuario), 0, 0, 'L')
    pdf.cell(40, 10, 'Firma del Paciente o Reponsable:', 0, 0, 'L')

    pdf.ln(3)
    pdf.cell(40, 10, str(''), 0, 0, 'L')
    pdf.cell(40, 10, 'Facturador(a):', 0, 0, 'L')

    pdf.ln(8)
    pdf.cell(40, 10, 'Fecha de impresion:', 0, 0, 'L')
    pdf.cell(150, 10, str(fechaRegistro), 0, 0, 'L')

    miConexiont.close()

    carpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\Facturas\\PDF\\'
    print("carpeta_ulti = ", carpeta)

    #archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'Liquida.pdf'
    archivo = carpeta + '' + 'Liquida_' + str(facturaPaciente.id) + '.pdf'
    print("archivo_ulti =", archivo)

    print ("aqui voy_0")

    try:

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

        # Intenta abrir el archivo directamente

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        datosMensaje = {'success': False, 'Mensaje': 'Cerrar Archivo cargado en browser'}
        json_data = json.dumps(datosMensaje, default=str)
        return HttpResponse(json_data, content_type='application/json')


    print ("aqui voy_4")

    return JsonResponse({'success': True, 'message': 'Factura impresa!'})

def ImprimirPazYSalvo(request):

    print("Entre imprimirPazYSalvo")

    # Instantiation of inherited class
    ingresoId1 = request.POST["ingresoId"]
    print("ingresoId1 = ", ingresoId1)

    llave = ingresoId1.split('-')
    print("llave = ", llave)
    print("primero=", llave[0])
    numeroIngreso = llave[1].strip()
    convenioId2= llave[2]
    print("numeroIngreso = ", numeroIngreso)
    print("convenioId2  = ", convenioId2)
    #Variable factura es el id de la liquidacion
    ingresoPac = Ingresos.objects.get(id=numeroIngreso)
    facturaPaciente= Liquidacion.objects.get(tipoDoc_id=ingresoPac.tipoDoc_id, documento_id=ingresoPac.documento_id, consecAdmision=ingresoPac.consec, convenio_id=convenioId2)
    factura=facturaPaciente.id

    ingresoPaciente = Ingresos.objects.get(id=numeroIngreso)
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

    comando = 'SELECT tipo.abreviatura abrev, usu.documento documento, usu.nombre nombre, ing."fechaIngreso", ing."fechaSalida" fechaSalida,	conv.nombre asegurador, regimen.nombre regimen, tiposCotizante.nombre tiposCotizante, tiposUsuario.nombre tiposUsuario, ' + "'" + str('Paciente') + "'" + ' parentesco  FROM admisiones_ingresos ing INNER JOIN usuarios_usuarios usu ON (usu.id=ing.documento_id) INNER JOIN usuarios_tiposdocumento tipo ON (tipo.id = usu."tipoDoc_id")  LEFT JOIN clinico_regimenes regimen ON (regimen.id=ing.regimen_id) LEFT JOIN clinico_tiposcotizante tiposCotizante ON (tiposCotizante.id=ing."tiposCotizante_id") LEFT JOIN usuarios_tiposusuario tiposUsuario ON (tiposUsuario.id = usu."tiposUsuario_id") LEFT JOIN contratacion_convenios conv on (conv.id=1) WHERE ing.id= ' + "'" + str(numeroIngreso)  +"'"
    print(comando)

    curt.execute(comando)

    print(comando)

    pazYSalvo = []

    for abrev, documento, nombre, fechaIngreso, fechaSalida, asegurador, regimen, tiposCotizante, tiposUsuario, parentesco in curt.fetchall():
        pazYSalvo.append(
            {'abrev': abrev, 'documento': documento, 'nombre':nombre,'fechaIngreso':fechaIngreso, 'fechasalida':fechaSalida, 
             'asegurador': asegurador, 'regimen': regimen,
             'tiposCotizante': tiposCotizante, 'tiposUsuario': tiposUsuario,'parentesco':parentesco})

    miConexiont.close()
    print("oazYSalvo = ", pazYSalvo)

    pdf = PDFPazYSalvo(tipoDocId, documentoId, consec, ingresoId1)
    pdf.alias_nb_pages()
    pdf.set_margins(left=10, top=5, right=5)
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(4)

    # Define el ancho de línea
    pdf.set_line_width(0.4)
    # Dibuja el borde
    pdf.rect(7.0, 15.0, 190.0, 47.0)  # Coordenadas x, y, ancho, alto

    print ("aqui toy01")

    pdf.set_font('Helvetica', 'B', 8)
    print ("aqui toy011")
    pdf.cell(200, 10, 'PAZ Y SALVO ADMINISTRATIVO:', 0, 0, 'C')
    print ("aqui toy01111")
    pdf.set_font('Helvetica', 'B', 8)
    pdf.ln(3)
    pdf.cell(200, 10, str(pazYSalvo[0]['nombre']), 0, 0, 'C')
    print ("aqui toy02")
    pdf.set_font('Helvetica', '', 8)
    pdf.ln(6)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Identificacion:', 0, 0, 'L')
    print("aqui toy10")
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['abrev']), 0, 0, 'L')
    pdf.cell(30, 10, str(pazYSalvo[0]['documento']), 0, 0, 'L')
    print ("aqui toy12")
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Admision:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(numeroIngreso), 0, 0, 'L')
    print("aqui toy12")
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Asegurador:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['asegurador']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Regimen:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['regimen']), 0, 0, 'L')
    pdf.ln(3)
    print("aqui toy20")
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Usuario:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['tiposCotizante']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Nivel:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    #pdf.cell(30, 10, str(pazYSalvo[0]['nivel']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'poblacion Esp:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['tiposUsuario']), 0, 0, 'L')
    pdf.ln(3)
    print("aqui toy31")
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Fecha de ingreso:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(60, 10, str(pazYSalvo[0]['fechaIngreso']), 0, 0, 'L')
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(40, 10, 'Fecha de Egreso:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    print("aqui toy311")
    #pdf.cell(30, 10, str(pazYSalvo[0]['fechaSalida']), 0, 0, 'L')
    print("aqui to312")
    pdf.ln(15)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Nombre Completo:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['nombre']), 0, 0, 'L')
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Identificacion:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['abrev']), 0, 0, 'L')
    pdf.cell(30, 10, str(pazYSalvo[0]['documento']), 0, 0, 'L')
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(30, 10, 'Parentesco:', 0, 0, 'L')
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(30, 10, str(pazYSalvo[0]['parentesco']), 0, 0, 'L')

    pdf.ln(10)

    texto = 'Este documento certifica que el paciente se encuentra a paz y salvo en pagos y/o documentos exigidos para la adecuada prestación del servicio. ES VÁLIDO PARA LA SALIDA'
    pdf.multi_cell(w=180, h=3, txt=str(texto), align='C')
    print("ya imprimi el footer")


    carpeta = 'C:\\EntornosPython\\Pos7Particionado\\vulner\\JSONCLINICA\\HistoriasClinicas\\'
    print("carpeta = ", carpeta)

    archivo = carpeta + '' + str(pacienteId.documento) + '_' + 'PazYsalvo.pdf'
    print("archivo =", archivo)

    try:
        # Intenta abrir el archivo directamente
        pdf.output(archivo, "F")
        print("archivo LISTO =", archivo)
        #webbrowser.open(archivo)

        buff = BytesIO()
        buff.name = archivo
        #Genera el archivo el el servidor

        # 2. Abrir el archivo PDF y leerlo

        print("voy a leer")
        with open(archivo, 'rb') as f:
            pdf_data = f.read()
            # 3. Escribir los datos en el buffer
            buff.write(pdf_data)

        buff.seek(0)

        print("voy a responder")

        return FileResponse(
            buff,
            as_attachment=False,  # Cambiar a False para verlo en navegador
            filename=archivo,
            content_type='application/pdf'
        )


    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {archivo}")
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")

    return JsonResponse({'success': True, 'message': 'Paz y salvo impreso!'})


