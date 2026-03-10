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
#from datetime import datetime
import datetime
from datetime import date, timedelta
import time
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
#from clinico import viewsReportes
from clinico.viewsReportes import ImprimirOrdenLaboratorio, ImprimirOrdenIncapacidad, ImprimirOrdenRadiologia, ImprimirOrdenTerapia, ImprimirOrdenMedicamentos, ImprimirOrdenDeControl
from django.db import transaction
import traceback
from django.db import transaction, IntegrityError
from django.utils import timezone

# Create your views here.

def prueba(request):
    return render(request, "index.html")


def resMotivoInvidente(request):
    print("Entre a Reconocer audio Motivo Consulta")
    r = sr.Recognizer()
    print(sr.Microphone.list_microphone_names())

    with sr.Microphone(device_index=0) as source:  # use the default microphone as the audio source
        print("Por Favor cuenteme :")

        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)  # listen for the first phrase and extract it into audio data
        print("pase")
    try:
        print("No haga nada")
        # print("You said " + r.recognize_google(audio , language = 'en-IN', show_all = True))  # recognize speech using Google Speech Recognition
        # text = r.recognize_google(audio, language = 'es-CO', show_all = True )
        text = r.recognize_google(audio, language='es-CO', show_all=True)
        #  jsonToPython = json.loads(format(text))
        print('You said: {}'.format(text))


    except LookupError:  # speech is unintelligible
        print("Could not understand audio")

    # return render(request, "home.html")

    datos = {"Respuesta": format(text)}
    print(datos)

    return HttpResponse(json.dumps(datos))

class Form:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"Form: {self.data}"


def motivoInvidente(request):
    print("Entre al Moivo invidente Audio")
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    texto = request.GET["nombre"]
    engine.say(texto)
    engine.runAndWait()

    return redirect('/menu/')



def motivoSeñas(request):
    print("Entre Reproduce SeÃ±as")
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    texto = step_5_camera()
    print("De devuelta el texto es : ")
    print(texto)

    #  texto = request.GET["nombre"]
    engine.say(texto)
    engine.runAndWait()

    datos = {"mensaje": texto}
    print(datos)

    return HttpResponse(json.dumps(datos))

    return redirect('/menu/')


def subjetivoSeñas(request):
    print("Entre Reproduce SubjetivoSeñas")
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    texto = step_5_camera()
    print("De devuelta el texto es : ")
    print(texto)

    #  texto = request.GET["nombre"]
    engine.say(texto)
    engine.runAndWait()

    datos = {"mensaje": texto}
    print(datos)

    return HttpResponse(json.dumps(datos))

    return redirect('/menu/')


def step_5_camera():
    print("Entree a Camara")
    onnx_file = 'C:\\EntornosPython\\vulne\\vulnerable\\signlanguage.onnx'
    onnx_model = onnx.load(onnx_file)
    onnx.checker.check_model(onnx_model)
    print('The model is checked!')

    # constants
    index_to_letter = list('ABCDEFGHIKLMNOPQRSTUVWXY')
    mean = 0.485 * 255.
    std = 0.229 * 255.
    print("Adentro1")
    # create runnable session with exported model
    ort_session = ort.InferenceSession(onnx_file)
    print("Adentro11")
    cap = cv2.VideoCapture(0)
    mensaje = []
    print("Adentro2")

    # while True:
    for t in range(15):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # preprocess data
        frame = center_crop(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        x = cv2.resize(frame, (28, 28))
        x = (x - mean) / std

        x = x.reshape(1, 1, 28, 28).astype(np.float32)
        y = ort_session.run(None, {'input': x})[0]

        index = np.argmax(y, axis=1)
        letter = index_to_letter[int(index)]

        mensaje.append(letter)
        print("las letras son: %s", mensaje)

        cv2.putText(frame, letter, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), thickness=2)
        cv2.imshow("Sign Language Translator", frame)
        print("Adentro3")
        #  if cv2.waitKey(1) & 0xFF == ord('q'):
        #  break

    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()

    print("El mensaje Final es : ")

    resultado = ''

    for x in range(0, len(mensaje)):
        resultado = resultado + mensaje[x]

    return (resultado)


def center_crop(frame):
    h, w, _ = frame.shape
    start = abs(h - w) // 2
    if h > w:
        return frame[start: start + w]
    return frame[:, start: start + h]


def crearHistoriaClinica(request):
    print("Entre crearHistoriaClinica y el request es :", request.method)
    print("Entre crearHistoriaClinica y el request AJAX es  :",  request.is_ajax)
    # form = historiaForm(request.POST)

    if request.method == 'POST':


        if request.is_ajax and request.method == "POST":


            print("Entre Ajax POST")

            sede = request.POST["sede"]
            print("sede = ", sede)

            tipoDoc = request.POST["tipoDocPaciente"]
            print("tipoDoc = ", tipoDoc)
            documento = request.POST["documentoPaciente"]
            print("documento = ", documento)
            ingresoPaciente = request.POST["ingresoPaciente"]
            print("ingresoPaciente = ", ingresoPaciente)
   

            tiposFolio = request.POST["tiposFolioEscogido"]
            print("tiposFolioEscogido = ", tiposFolio)
            mipres = request.POST["mipres"]
            print ("mipres = " , mipres)

            ordenMedicaLab = request.POST["ordenMedicaLab"]
            print ("ordenMedicaLab = " , ordenMedicaLab)

            ordenMedicaRad = request.POST["ordenMedicaRad"]
            print ("ordenMedicaLRad = " , ordenMedicaRad)

            ordenMedicaTer = request.POST["ordenMedicaTer"]
            print ("ordenMedicaTer = " , ordenMedicaTer)

            ordenMedicaMed = request.POST["ordenMedicaMed"]
            print ("ordenMedicaLab = " , ordenMedicaLab)

            ordenMedicaOxi = request.POST["ordenMedicaOxi"]
            print ("ordenMedicaOxi = " , ordenMedicaOxi)

            ordenMedicaInt = request.POST["ordenMedicaInt"]
            print ("ordenMedicaInt = " , ordenMedicaInt)

            ordenDeControl = request.POST["ordenDeControl"]
            print ("ordenDeControl = " , ordenDeControl)


            dxComplicacion = request.POST["dxComplicacion"]
            print ("dxComplicacion = " , dxComplicacion)

            print ("tiposfolios Seleccionado = " , tiposFolio)
            #dependenciasRealizado = request.POST["dependenciasRealizado"]
            serviciosAdministrativos = request.POST["serviciosAdministrativos"]
            print("serviciosAdministrativos", serviciosAdministrativos)

            if (serviciosAdministrativos==''):
                serviciosAdministrativos="null"

            causasExterna = request.POST["causasExterna"]
            print("causasExterna", causasExterna)
            espMedico = request.POST["espMedico"]
            print("espMedico seleccionado",espMedico)

            # Aqui consigo el codigo de la especialidad

            especialidadId = EspecialidadesMedicos.objects.get(id=espMedico)
            print("Especialidad = ", especialidadId.especialidades_id)

            plantados = request.POST["planta"]
            print("plantaDos = ", plantados)

            plantaId = Planta.objects.get(documento=plantados.strip(), sedesClinica_id=sede)
            print("plantaId =", plantaId.id)

            medicoId = Medicos.objects.get(planta_id= plantaId.id)
            print ("medicoId = ", medicoId.id)

            tipoDocId = TiposDocumento.objects.get(nombre=tipoDoc)
            print("tipoDocId =", tipoDocId)
            documentoId = Usuarios.objects.get(tipoDoc_id=tipoDocId.id, documento=documento)
            print("documentoId =", documentoId)

	        # Aqui se consigue el ingreso del paciente
            tipoAdmision=''
            try:
                with transaction.atomic():
                    ingresosPaciente = Ingresos.objects.get(tipoDoc_id=tipoDocId.id, documento_id=documentoId.id,  consec=ingresoPaciente)
                    print(" ingresosPaciente = ", ingresosPaciente)
                    tipoAdmision='ADMISION'

            except Exception as e:
                # Aquí ya se hizo rollback automáticamente
                print("Se hizo rollback INGRESO por:", e)
                ingresosPaciente = Triage.objects.get(tipoDoc_id=tipoDocId.id, documento_id=documentoId.id,  consec=ingresoPaciente)
                print(" ingresosPaciente = ", ingresosPaciente.id)
                tipoAdmision = 'TRIAGE'

                #return HttpResponse(json.dumps(data))

                    #return JsonResponse({'success': False, 'Mensaje': e})
                    # raise Exception("¡Ha ocurrido un error ENVIADO DESDE DJANGO!")
            finally:
                print("Finally")


            print("ingresosPaciente = ", ingresosPaciente.id)
            print("tipoAdmision = ", tipoAdmision)

            motivo = request.POST["motivo"]
            objetivo = request.POST["objetivo"]
            subjetivo = request.POST["subjetivo"]
            analisis = request.POST["analisis"]
            plan = request.POST["plan"]
            tratamiento = request.POST["tratamiento"]
            print("tratamiento =", tratamiento)
            tipoIng = request.POST["tipoIng"]
            usuarioRegistro = plantaId.id

            #fechaRegistro = dnow


            fechaRegistro = timezone.now()

            estadoReg = "A"
            print("estadoRegistro =", estadoReg)
            # Busca el folio a asignar
            # Primero el id del paciente:
            # Se recogen los datos Clinicos
            antibioticos = request.POST["antibioticos"]
            print("antibioticos =", antibioticos)

            apache2 = request.POST["apache2"]
            print("apache2 =", apache2)
            monitoreo = request.POST["monitoreo"]
            print("monitoreo =", monitoreo)
            movilidadLimitada = request.POST["movilidadLimitada"]
            print("movilidadLimitada =", movilidadLimitada)
            nauseas = request.POST["nauseas"]
            print("nauseas =", nauseas)
            llenadoCapilar = request.POST["llenadoCapilar"]
            print("llenadoCapilar =", llenadoCapilar)
            neurologia = request.POST["neurologia"]
            print("neurologia =", neurologia)
            irritacion = request.POST["irritacion"]
            pulsos = request.POST["pulsos"]
            print("pulsos =", pulsos)

            retiroPuntos = request.POST["retiroPuntos"]
            print("retiroPuntos =", retiroPuntos)
            inmovilizacion = request.POST["inmovilizacion"]
            print("inmovilizacion =", inmovilizacion)
            notaAclaratoria = request.POST["notaAclaratoria"]
            print("notaAclaratoria =", notaAclaratoria)
            fecNotaAclaratoria = request.POST["fecNotaAclaratoria"]
            print("fecNotaAclaratoria =", fecNotaAclaratoria)
            if (fecNotaAclaratoria== ''):
                fecNotaAclaratoria='0001-01-01 00:00:00'


            #fecNotaAclaratoria = request.POST["fecNotaAclaratoria"]
            #print("fecNotaAclaratoria =", fecNotaAclaratoria)
            examenFisico = request.POST["examenFisico"]
            print("examenFisico =", examenFisico)
            noQx1 = request.POST["noQx1"]
            print("noQx1 =", noQx1)
            observaciones = request.POST["observaciones"]
            print("observaciones =", observaciones)
            riesgoHemodinamico = request.POST["riesgoHemodinamico"]
            print("riesgoHemodinamico =", riesgoHemodinamico)
            #riesgoVentilatorio = request.POST["riesgoVentilatorio"]
            #print("riesgoVentilatorio =", riesgoVentilatorio)
            riesgos = request.POST["riesgos"]
            print("riesgos =", riesgos)
            trombocitopenia = request.POST["trombocitopenia"]
            print("trombocitopenia =", trombocitopenia)
            hipotension = request.POST["hipotension"]
            print("hipotension =", hipotension)
            indiceMortalidad = request.POST["indiceMortalidad"]
            print("indiceMortalidad =", indiceMortalidad)
            ingestaAlcohol = request.POST["ingestaAlcohol"]
            print("ingestaAlcohol =", ingestaAlcohol)
            tratamiento = request.POST["tratamiento"]
            print("tratamiento =", tratamiento)
            inmovilizacionObservaciones = request.POST["inmovilizacionObservaciones"]
            print("inmovilizacionObservaciones =", inmovilizacionObservaciones)
            justificacion = request.POST["justificacion"]
            print("justificacion =", justificacion)
            leucopenia = request.POST["leucopenia"]
            print("leucopenia =", leucopenia)
            manejoQx = request.POST["manejoQx"]
            print("manejoQx =", manejoQx)


            tipoDocId = TiposDocumento.objects.get(nombre=tipoDoc)
            print("tipoDocId =", tipoDocId)
            documentoId = Usuarios.objects.get(tipoDoc_id=tipoDocId.id, documento=documento)
            print("documentoId =", documentoId)

            #ultimofolio = Historia.objects.all().filter(tipoDoc_id=tipoDoc).filter(documento_id=idPacienteFinal['id']).aggregate(maximo=Coalesce(Max('folio'), 0))
            ultimofolio = Historia.objects.all().filter(tipoDoc_id=tipoDocId.id).filter(documento_id=documentoId.id).aggregate(maximo=Coalesce(Max('folio'), 0 ))

            salidaClinica = request.POST['salidaClinica']
            tiposSalidas = request.POST['tiposSalidas']

            print("salidaClinica =", salidaClinica)

            if salidaClinica=='on':
                salidaClinica='S'
            else:
                salidaClinica='N'

            print("salidaClinicaFinal =", salidaClinica)
	

            ##########################################


            print("ultimo folio = ", ultimofolio)
            print("ultimo folio = ", ultimofolio['maximo'])
            ultimofolio2 = (ultimofolio['maximo']) + 1
            print("ultimo folio2 = ", ultimofolio2)

            print ("documento= ", documento)
            print("tipoDoc = ", tipoDoc)
            print ("consec admisione = ", ingresoPaciente)
            print("folio = ", ultimofolio2)
            #print("fecha = ", fecha)
            print("tiposFolio = ", tiposFolio)
            print("causas externa=", causasExterna)
            print("espemedico = ", espMedico)
            print("planta = ", plantados)

            print("usuarioRegistro = ", usuarioRegistro)

            diagnosticos = request.POST["diagnosticos"]

            print("diagnosticos = ", diagnosticos)

            if (causasExterna == ''):

                print("Entre GRAVES campos vacios")
                data = {'Mensaje': 'Favor suministrar Causa externa Obligatorio'}
                return HttpResponse(json.dumps(data))


            jsonDDiagnosticos = json.loads(diagnosticos)
            elementosDiagnosticos = len (jsonDDiagnosticos)
            print ("elementosDiagnosticos = ", elementosDiagnosticos )



            if (elementosDiagnosticos== 1):

                print("Entre GRAVES campos vacios")
                data = {'Mensaje': 'Favor suministrar diagnostico Obligatorios!'}
                return HttpResponse(json.dumps(data))


            else:

                # Grabacion Historia

                print ("VOY A GRABAR DEFINITIVAMENTE LA HISTORIA CLINICA")

                # Inicio grabacion Historia Clinica

                miConexiont = None
                try:

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres", password="123456")
                            curt = miConexiont.cursor()

                            comando = 'INSERT INTO clinico_Historia ("sedesClinica_id", "tipoDoc_id" , documento_id , "consecAdmision", folio ,fecha , "tiposFolio_id" ,"causasExterna_id" , "serviciosAdministrativos_id" , especialidades_id ,planta_id, motivo , subjetivo,objetivo, analisis ,plann, tratamiento ,                apache2, antibioticos, monitoreo, "movilidadLimitada", nauseas, "llenadoCapilar", neurologia, irritacion, pulsos, "retiroPuntos",             inmovilizacion, "notaAclaratoria", "fecNotaAclaratoria", "examenFisico", "noQx", observaciones, "riesgoHemodinamico", riesgos, trombocitopenia, hipotension, "indiceMortalidad", "ingestaAlcohol", "inmovilizacionObservaciones", justificacion, leucopenia, "manejoQx", "fechaRegistro", "usuarioRegistro_id", "estadoReg" , mipres,"ordenMedicaLab","ordenMedicaRad","ordenMedicaTer","ordenMedicaMed","ordenMedicaOxi","ordenMedicaInt", "especialidadesMedicos_id", "ordenDeControl")  VALUES(' + "'" + str(sede) + "',"  + "'" +  str(tipoDocId.id) + "','" + str(documentoId.id) + "','" + str(ingresoPaciente) + "','" + str(ultimofolio2) + "','" + str(fechaRegistro) + "','"  +  str(tiposFolio) + "','" + str(causasExterna) + "'," + str(serviciosAdministrativos) + ",'" + str(especialidadId.especialidades_id) + "','" + str(plantaId.id) + "','" + str(motivo) + "','" + str(subjetivo) + "','" + str(objetivo) + "','" + str(analisis) + "','" + str(plan) + "','" + str(tratamiento)  + "','" + str(apache2) + "','" + str(antibioticos) + "','" + str(monitoreo) + "','"  + str(movilidadLimitada) + "','" + str(nauseas) + "','"  + str(llenadoCapilar) + "','" + str(neurologia) + "','"  + str(irritacion) + "','"  + str(pulsos) + "','" + str(retiroPuntos) + "','" + str(inmovilizacion) + "','" + str(notaAclaratoria) + "','"  + str(fecNotaAclaratoria) + "','" + str(examenFisico) +  "','" + str(noQx1) + "','" + str(observaciones) + "','" + str(riesgoHemodinamico) + "','" + str(riesgos) + "','" + str(trombocitopenia) + "','" + str(hipotension) + "','"  + str(indiceMortalidad) + "','" + str(ingestaAlcohol) + "','" + str(inmovilizacionObservaciones) + "','" + str(justificacion) + "','" + str(leucopenia) + "','" + str(manejoQx) + "','"  + str(fechaRegistro) + "','" + str(usuarioRegistro) + "','" + str(estadoReg) + "','" + str(mipres) + "'" +  ",'" + str(ordenMedicaLab) + "'" +  ",'" + str(ordenMedicaRad) + "'" +  ",'" + str(ordenMedicaTer) + "'"  +  ",'" + str(ordenMedicaMed) + "'"   +  ",'" + str(ordenMedicaOxi) + "'" +  ",'" + str(ordenMedicaInt) + "'," + "'" + str(espMedico) + "','" + str(ordenDeControl)  + "'"  +  ") RETURNING id ;"

                            ## fin tentativo insert

                            print(comando)
                            resultado = curt.execute(comando)

                            historiaId = curt.fetchone()[0]
                            print("resultado = " , resultado)

                            print ("historiaId Final = ", historiaId)

                            miConexiont.commit()

                            #print("historiaid = ", historiaId)
                            #historiaIdU = Historia.objects.all().aggregate(maximo=Coalesce(Max('id'), 0))
                            #historiaId = (historiaIdU['maximo']) + 0
                            print("1 record inserted, ID:", historiaId)

                            curt.close()
                            miConexiont.close()

                            print("El id del la hsitoria INSERTADA es ", historiaId)

                            # Fingrabacion Historia Clinica

                            print("Historia No : ", historiaId)
                            jsonHistoria = {'id': historiaId}

                except psycopg2.DatabaseError as error:
                      print("Entre por rollback", error)
                      if miConexiont:
                           print("Entro ha hacer el Rollback")
                           miConexiont.rollback()

                      data = {'Mensaje': error}

                      return HttpResponse(json.dumps(data))


                finally:
                    if miConexiont:
                        curt.close()
                        miConexiont.close()



                convenioParticular = Convenios.objects.get(particular='S')
                print ("convenioParticular =", convenioParticular)

                # Fin Grabacion Historia
		
		# Aqui rutina busca Convenio del Paciente

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",        password="123456")
                curt = miConexiont.cursor()

                comando = 'SELECT min(p.convenio_id) id FROM facturacion_conveniospacienteingresos p WHERE "tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "'" + ' AND documento_id = ' + "'" + str(documentoId.id) + "'" + ' AND "consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND convenio_id != " + "'" + str(convenioParticular.id) + "'"

                curt.execute(comando)

                print(comando)

                convenio = []

                for id in curt.fetchall():
                      convenio.append({'id': id})

                miConexiont.close()
                print("convenioId = ", convenio[0])

                convenioId = convenio[0]['id']
                convenioId = str(convenioId)
                print ("convenioId = ", convenioId)

                convenioId = convenioId.replace("(",' ')
                convenioId = convenioId.replace(")", ' ')
                convenioId = convenioId.replace(",", ' ')
                print("convenioId = ", convenioId)
                print("Tamalo de convenioId =", len(convenioId))
                
                convenioId = convenioId.strip()

                print("sin espacioos convenioId =", convenioId)


                if convenioId.strip()=='None':
                   #convenioId=0
                   convenioId= convenioParticular.id
                   ## Aqui si no hay convenio particular creado en facturacion_conveniospacioenteingreso anton crearlo

                   try:
                       with transaction.atomic():

                           conveniospacienteingresos = ConveniosPacienteIngresos.objects.get(tipoDoc_id=tipoDocId.id,documento_id=documentoId.id,                                                                         consecAdmision=ingresoPaciente, convenio_id=convenioParticular.id)

                   except Exception as e:
                       # Aquí ya se hizo rollback automáticamente
                       print("Se hizo rollback por:", e)
                       print("ppor aqui se le crea el convenio Particular al paciente")

                       grabo88 = ConveniosPacienteIngresos(
                           tipoDoc_id=tipoDocId.id,
                           documento_id=documentoId.id,
                           consecAdmision=ingresoPaciente,
                           convenio_id=convenioParticular.id,
                           fechaRegistro = fechaRegistro,
                           usuarioRegistro_id = usuarioRegistro,
                           estadoReg = estadoReg
                       )
                       grabo88.save()
                       grabo88.id
                       print("yA grabe", grabo88.id)

                   finally:
                       print("Cleanup operations or final logging.")


                   print ("Entre a MODIFICAR convenioID")

                print("ULTIMO valor de convenioId= ", convenioId)

	        # Fin Rutina busca convenio del paciente

                # Validacion si existe o No existe CABEZOTE

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",   password="123456")

                curt = miConexiont.cursor()
                comando = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + "'" + str(
                    tipoDocId.id) + "' AND documento_id = " + "'" + str(
                    documentoId.id) + "'" + ' AND "consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND convenio_id = '" + str(convenioId) + "'"
                curt.execute(comando)

                cabezoteLiquidacion = []

                for id in curt.fetchall():
                    cabezoteLiquidacion.append({'id': id})

                print ("CABEZOTE DE LIQUIDACION = ", cabezoteLiquidacion);

                miConexiont.close()
                if (cabezoteLiquidacion == []):
                    # Si no existe liquidacion CABEZOTE se debe crear con los totales, abonos, anticipos, procedimiento, suministros etc
                    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                   user="postgres", password="123456")
                    curt = miConexiont.cursor()
                    comando = 'INSERT INTO facturacion_liquidacion ("sedesClinica_id", "tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos") VALUES (' + "'" + str(sede) + "'," +  "'" + str(
                        tipoDocId.id) + "','" + str(documentoId.id) + "','" + str(ingresoPaciente) + "','" + str(
                        fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(
                        estadoReg) + "'," + str(convenioId) + ',' + "'" + str(usuarioRegistro) + "',0) RETURNING id "
                    curt.execute(comando)
                    liquidacionId = curt.fetchone()[0]

                    print("resultado liquidacionId = " , liquidacionId)

                    miConexiont.commit()
                    miConexiont.close()
                    #liquidacionU = Liquidacion.objects.all().aggregate(maximo=Coalesce(Max('id'), 0))
                    #liquidacionId = (liquidacionU['maximo']) + 0
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

                # Aqui RUTINA busca consecutivo de liquidacion

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",        password="123456")
                curt = miConexiont.cursor()

                comando = 'SELECT (max(p.consecutivo) + 1) cons FROM facturacion_liquidaciondetalle p WHERE liquidacion_id = ' + liquidacionId

                curt.execute(comando)

                print(comando)

                consecLiquidacion = []

                for cons in curt.fetchall():
                      consecLiquidacion.append({'cons': cons})

                miConexiont.close()
                print("consecLiquidacion = ", consecLiquidacion[0])

                consecLiquidacion = consecLiquidacion[0]['cons']
                consecLiquidacion = str(consecLiquidacion)
                print ("consecLiquidacion = ", consecLiquidacion)

                consecLiquidacion = consecLiquidacion.replace("(",' ')
                consecLiquidacion = consecLiquidacion.replace(")", ' ')
                consecLiquidacion = consecLiquidacion.replace(",", ' ')

                if consecLiquidacion.strip()=='None':
                    print ("consecLiquidacion = ",  consecLiquidacion)
                    consecLiquidacion=1

	        # Fin RUTINA busca consecutivo de liquidacion
		
		    # RUTINA encuentra columna de dondel LEER la tarifa.
                #

                try:
                    with transaction.atomic():

                        contratacion = Convenios.objects.get(id=convenioId)

                        print("OJOO contratacion.tarifariosDescripcionProc_id = " , contratacion.tarifariosDescripcionProc_id)

                        columnaALeer = TarifariosDescripcion.objects.get(id=contratacion.tarifariosDescripcionProc_id)
                        columnaALeerPropia  = columnaALeer.columna

                except Exception as e:
                    # Aquí ya se hizo rollback automáticamente
                    print("Se hizo rollback de Convenio TarifarioDescripcion por:", e)
                    error_data = {
                        'type': type(e).__name__,
                        'message': str(e),
                        'traceback': traceback.format_exc()
                    }
                    columnaALeerPropia =''
                    #response = JsonResponse({"error": 'No hay definicion Convenio TarifarioDescripcion'})
                    #response.status_code = 403 # To announce that the user isn't allowed to publish
                    #Sreturn response

                    #raise error_data

                finally:
                    print("Finally")

                print ("Columna a leer = ", columnaALeerPropia)

                autorizacionId=0

                #Grabacion Laboratorios
            #
                laboratorios = request.POST["laboratorios"]
                print("laboratorios =", laboratorios)
                ## Rutina leer el JSON de laboratorios en python primero
                consecutivo=0
                jsonLaboratorios = json.loads(laboratorios)

                conteoLab=0

                for key in jsonLaboratorios:

                    print("key = " ,key)
                    queda= key
                    tiposExamen_Id = key["tiposExamen_Id"]
                    print ("tiposExamen_Id", tiposExamen_Id)
                    cups = key["cups"].strip()
                    print("cups ", cups )
                    cantidad = key["cantidad"]
                    print("cantidad", cantidad)
                    observa = key["observa"]
                    print("observa", observa)
                    estadoExamenes_id = "1"

                    if cups != "":
                        consecutivo = consecutivo + 1
                        #codigoCupsId = Examenes.objects.get(codigoCups=cups)

                        a = HistoriaExamenes(tiposExamen_id= tiposExamen_Id ,codigoCups =  cups,consecutivo=consecutivo, cantidad = cantidad, observaciones=observa,estadoReg='A' , estadoExamenes_id= estadoExamenes_id, anulado="N", historia_id=historiaId, usuaroRegistra_id=usuarioRegistro, consecutivoLiquidacion=consecLiquidacion)
                        a.save()
                        conteoLab = conteoLab + 1

                        ## Desde Aqui rutina de Facturacion
                        #
                        codigoCupsId = Examenes.objects.filter(codigoCups=cups)
                        print ("codigoCupsId", codigoCupsId[0].id)

                        miConexion3 = None
                        try:
                            if (columnaALeerPropia != ''):

                                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",   user="postgres", password="123456")

                                curt = miConexiont.cursor()
                                comando = 'SELECT conv.convenio_id id ,exa."codigoCups" cups, proc."' + str(columnaALeer.columna) + '"' + ' valor FROM facturacion_conveniospacienteingresos conv, tarifarios_tarifariosdescripcion des, tarifarios_tarifariosprocedimientos proc, clinico_examenes exa, contratacion_convenios conv1 , tarifarios_tipostarifa tiptar WHERE conv."tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "'" + ' AND conv.documento_id = ' + "'" + str(documentoId.id) + "'" + ' AND conv."consecAdmision" = ' + "'" + str(ingresoPaciente) + "'" + ' AND conv.convenio_id = conv1.id AND des.id = conv1."tarifariosDescripcionProc_id" AND proc."codigoCups_id" = exa.id  And exa.id = ' + "'" + str(codigoCupsId[0].id) + "'" + ' AND des."tiposTarifa_id" = tiptar.id and proc."tiposTarifa_id" = tiptar.id'
                                print("comando = ", comando)
                                curt.execute(comando)

                                convenioValor = []

                                for id, cups,tarifaValor   in curt.fetchall():
         	                               convenioValor.append({'id': id, 'cups':cups, 'valor':tarifaValor})

                                miConexiont.close()
                            else:
                                convenioValor = []

                            print("columnaALeer.columna", columnaALeerPropia)
                            print("convenioValor = ", convenioValor)
                            print("convenioValor[0].cups = ", convenioValor[0]['cups'])


                            # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones

                            #print("el cups :", cups)

                            #print ("autorizacion para el CUPS es ", codigoCupsId[0].requiereAutorizacion)

                            # Aqui saca valores pata tarifas

                            if convenioValor != []:

                                print ("Cups = "  , convenioValor[0]['cups'])
                                tarifaValor = convenioValor[0]['valor']
                                tarifaValor = str(tarifaValor)
                                print("tarifaValor = ", tarifaValor)
                                tarifaValor = tarifaValor.replace("None", ' ')
                                tarifaValor = tarifaValor.replace("(", ' ')
                                tarifaValor = tarifaValor.replace(")", ' ')
                                tarifaValor = tarifaValor.replace(",", ' ')
                                tarifaValor = tarifaValor.replace(" ", '')
                                print ("tarifaValor = ", tarifaValor)
                            else:
                                tarifaValor=0


                            if tarifaValor == '':
                                print ("Entre cambiar tarufa Valor" ,  tarifaValor)
                                tarifaValor=0

                        except psycopg2.DatabaseError as error:
                            print("Entre por rollback", error)
                            if miConexion3:
                                print("Entro ha hacer el Rollback")
                                miConexion3.rollback()
                                tarifaValor = 0

                        finally:
                            if miConexion3:
                                cur3.close()
                                miConexion3.close()

                        TotalTarifa = float(tarifaValor) * float(cantidad)

                        if (codigoCupsId[0].requiereAutorizacion == 'S'):

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                            curt = miConexiont.cursor()
                            comando = 'SELECT aut.id id FROM autorizaciones_autorizaciones  aut, clinico_historia historia WHERE  aut.historia_id = historia.id AND historia."tipoDoc_id" = ' + "'" +  str(tipoDocId.id) + "' AND historia.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND historia."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND aut.historia_id = " + "'" + str(historiaId) + "'"


                            curt.execute(comando)
			    
                            hayAut = []

                            for id in curt.fetchall():
                                hayAut.append({'id': id})

                            miConexiont.close()

                            estadoAutorizacionId = EstadosAutorizacion.objects.get(nombre='PENDIENTE')

                            if hayAut != '':


                                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                                curt = miConexiont.cursor()
                                comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id , convenio_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" +  str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ', conv.id FROM facturacion_conveniospacienteingresos convIngreso,  contratacion_convenios conv WHERE conv.id = ' + "'" + str(convenioId) + "'" + ' AND conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" +  str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = " + "'" + str(convenioValor[0]['id']) + "'" + ' RETURNING id'

                                print ("comando ", comando)

                                curt.execute(comando)
                                autorizacionId = curt.fetchone()[0]
                                miConexiont.commit()

                                miConexiont.close()

                                #autorizacionIdU = Autorizaciones.objects.all().filter(historia_id=historiaId).aggregate(maximo=Coalesce(Max('id'), 0))
                                #autorizacionId = (autorizacionIdU['maximo']) + 0
			
                            else:

                                autorizacionId = hayAut[0]['id']

                            print ("Autorizacion Final = ", autorizacionId)

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",   user="postgres", password="123456")

                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id", "valorSolicitado")  VALUES (' + "'" + str(estadoAutorizacionId.id) + "'," + "'" + str(cantidad) + "'" + ' ,0, now(),' + "'" + str('A') + "','"  + str(autorizacionId) + "','" + str(usuarioRegistro)  + "'," +  "'"  + str(codigoCupsId[0].id) + "',null, " + "'" + str(tiposExamen_Id) + "'," + "'" + str(TotalTarifa)  + "'" +  ')'

                            print ("comando=", comando)

                            curt.execute(comando)
                            miConexiont.commit()

                            miConexiont.close()



                            # Fin tema Autorizaciones

                    # Aqui Rutina FACTURACION crea en liquidaciondetalle el registro con la tarifa, con campo cups y convenio
                    #

                        if (codigoCupsId[0].requiereAutorizacion == 'N'):

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",                                       password="123456")
                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia_id,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro") VALUES (' + "'" +  str(consecLiquidacion)  + "','" + str(fechaRegistro) + "','" + str(cantidad) + "','"  + str(tarifaValor) + "','" + str(TotalTarifa)  + "',null,'"  +  str(fechaRegistro) + "','" +  str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(codigoCupsId[0].id) + "','" + str(usuarioRegistro) + "'," + liquidacionId + ",'SISTEMA')"
                            print("comando de insercio" , comando)
                            curt.execute(comando)
                            miConexiont.commit()
                            miConexiont.close()

                            consecLiquidacion = int(consecLiquidacion) + 1


	            # Fin rutina Facturacion

		# Rutina Impresion Ordenes de Laboratorio
                print ("tamaño matriz laboratorios", len(laboratorios[0]))

                if conteoLab >= 1:
                    print("Encontre ordenes de laboratrio")
                    print("Encontre ordenes de laboratrio")
                    ingresoId2=ingresosPaciente.id
                    ImprimirOrdenLaboratorio(ingresoId2, historiaId, convenioId, tipoAdmision)
                else:
                    print("No Encontre ordenes de laboratrio")
                    print("No Encontre ordenes de laboratrio")

                # Fin Grabacion Laboratorios

                # Grabacion Radiologia


                radiologia = request.POST["radiologia"]
                print("radiologia =", radiologia)

                ## Rutina leer el JSON de laboratorios en python primero
                consecutivo = 0
                jsonRadiologia = json.loads(radiologia)
                conteoRad=0

                for key1 in jsonRadiologia:

                     print("key1 = ", key1)
                     queda = key1
                     tiposExamen_Id = key1["tiposExamen_Id"]
                     print("tiposExamen_Id", tiposExamen_Id)
                     cups = key1["cups"].strip()
                     print("cups = ", cups)
                     cantidad = key1["cantidad"]
                     print("cantidad", cantidad)
                     observa = key1["observa"]
                     print("observa", observa)
                     estadoExamenes_id = "1"

                     if cups != "":
                        consecutivo = consecutivo + 1
                         #codigoCups = Examenes.objects.get(nombre=nombreRx)
                        b = HistoriaExamenes(tiposExamen_id=tiposExamen_Id, codigoCups=cups,
                                              cantidad=cantidad, consecutivo=consecutivo, observaciones=observa, estadoReg='A',
                                              estadoExamenes_id=estadoExamenes_id, anulado="N",
                                              historia_id=historiaId, usuaroRegistra_id=usuarioRegistro , consecutivoLiquidacion=consecLiquidacion)
                        b.save()
                        conteoRad=conteoRad + 1

                        # Rutiva busca en convenio el valor de la tarifa CUPS

                        codigoCupsId = Examenes.objects.filter(codigoCups=cups)
                        print("codigoCupsId", codigoCupsId[0].id)
                        print("liquidacionId = ", liquidacionId)

                        miConexion3 = None
                        try:
                            if (columnaALeerPropia != ''):

                                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                               user="postgres", password="123456")

                                curt = miConexiont.cursor()
                                comando = 'SELECT conv.convenio_id id ,exa."codigoCups" cups, proc."' + str(
                                    columnaALeer.columna) + '"' + ' valor FROM facturacion_conveniospacienteingresos conv, tarifarios_tarifariosdescripcion des, tarifarios_tarifariosprocedimientos proc, clinico_examenes exa, contratacion_convenios conv1 , tarifarios_tipostarifa tiptar WHERE conv."tipoDoc_id" = ' + "'" + str(
                                    tipoDocId.id) + "'" + ' AND conv.documento_id = ' + "'" + str(
                                    documentoId.id) + "'" + ' AND conv."consecAdmision" = ' + "'" + str(
                                    ingresoPaciente) + "'" + ' AND conv.convenio_id = conv1.id AND des.id = conv1."tarifariosDescripcionProc_id" AND proc."codigoCups_id" = exa.id  And exa.id = ' + "'" + str(
                                    codigoCupsId[
                                        0].id) + "'" + ' AND des."tiposTarifa_id" = tiptar.id and proc."tiposTarifa_id" = tiptar.id'
                                print("comando = ", comando)
                                curt.execute(comando)

                                convenioValor = []

                                for id, cups, tarifaValor in curt.fetchall():
                                    convenioValor.append({'id': id, 'cups': cups, 'valor': tarifaValor})

                                miConexiont.close()
                            else:
                                convenioValor = []

                            print("columnaALeer.columna", columnaALeerPropia)
                            print("convenioValor = ", convenioValor)
                            print("codigoCupsId[0].id = ", codigoCupsId[0].id)

                            # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones

                            print("el cups :", cups)

                            print("autorizacion para el CUPS es ", codigoCupsId[0].requiereAutorizacion)

                            # Aqui saca valores pata tarifas

                            if convenioValor != []:

                                print("Cups = ", convenioValor[0]['cups'])
                                tarifaValor = convenioValor[0]['valor']
                                tarifaValor = str(tarifaValor)
                                print("tarifaValor = ", tarifaValor)
                                tarifaValor = tarifaValor.replace("None", ' ')
                                tarifaValor = tarifaValor.replace("(", ' ')
                                tarifaValor = tarifaValor.replace(")", ' ')
                                tarifaValor = tarifaValor.replace(",", ' ')
                                tarifaValor = tarifaValor.replace(" ", '')
                                print("tarifaValor = ", tarifaValor)
                            else:
                                tarifaValor = 0

                            if tarifaValor == '':
                                print("Entre cambiar tarufa Valor", tarifaValor)
                                tarifaValor = 0

                        except psycopg2.DatabaseError as error:
                            print("Entre por rollback", error)
                            if miConexion3:
                                print("Entro ha hacer el Rollback")
                                miConexion3.rollback()
                                tarifaValor = 0

                        finally:
                            if miConexion3:
                                cur3.close()
                                miConexion3.close()

                        TotalTarifa = float(tarifaValor) * float(cantidad)

                        # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones

                        print("el cups :", cups)

                        if (codigoCupsId[0].requiereAutorizacion == 'S'):

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                            curt = miConexiont.cursor()
                            comando = 'SELECT aut.id id FROM autorizaciones_autorizaciones  aut, clinico_historia historia WHERE  aut.historia_id = historia.id AND historia."tipoDoc_id" = ' + "'" + str(
                                tipoDocId.id) + "' AND historia.documento_id = " + "'" + str(
                                documentoId.id) + "'" + ' AND historia."consecAdmision" = ' + "'" + str(
                                ingresoPaciente) + "' AND aut.historia_id = " + "'" + str(historiaId) + "'"

                            curt.execute(comando)
                            hayAut = []

                            for id in curt.fetchall():
                                hayAut.append({'id': id})

                            miConexiont.close()

                            estadoAutorizacionId = EstadosAutorizacion.objects.get(nombre='PENDIENTE')

                            hayAut = str(hayAut[0]['id'])
                            hayAut = hayAut.replace("None", ' ')
                            hayAut = hayAut.replace("(", ' ')
                            hayAut = hayAut.replace(")", ' ')
                            hayAut = hayAut.replace(",", ' ')
                            hayAut = hayAut.replace(" ", '')
                            print("hayAut = ", hayAut)



                            if hayAut == '':
                                print ("ENTRE CREAR AUTORIZACION ")
                                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                               user="postgres", password="123456")

                                curt = miConexiont.cursor()
                                #comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" +  str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ' FROM facturacion_conveniospacienteingresos convIngreso, contratacion_conveniosprocedimientos proc, contratacion_convenios conv WHERE conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" +  str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = proc.convenio_id AND proc.cups_id = " + "'" +  str(codigoCupsId[0].id) + "' RETURNING id"
                                comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id, convenio_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" + str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ', conv.id FROM facturacion_conveniospacienteingresos convIngreso,  contratacion_convenios conv WHERE conv.id = ' + "'" + str(convenioId) + "'" + ' AND conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = " + "'" + str(convenioValor[0]['id']) + "'" + ' RETURNING id'

                                curt.execute(comando)
                                autorizacionId = curt.fetchone()[0]
                                miConexiont.commit()
                                miConexiont.close()

                                #autorizacionIdU = Autorizaciones.objects.all().filter(
                                #    historia_id=historia.id).aggregate(maximo=Coalesce(Max('id'), 0))
                                #autorizacionId = (autorizacionIdU['maximo']) + 0

                            else:

                                autorizacionId = hayAut

                            print("Autorizacion Final = ", autorizacionId)

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id","valorSolicitado")  VALUES (' + "'" + str(estadoAutorizacionId.id) + "'," + "'" + str(cantidad) + "'" + ' ,0, now(),' + "'" + str('A') + "','"  + str(autorizacionId) + "','" + str(usuarioRegistro)  + "'," +  "'"  + str(codigoCupsId[0].id) + "',null,'" + str(tiposExamen_Id) + "','" + str(tarifaValor) + "')"
                            curt.execute(comando)
                            miConexiont.commit()
                            miConexiont.close()

                            # Fin tema Autorizaciones


                    # Aqui Rutina FACTURACION crea en liquidaciondetalle el registro con la tarifa, con campo cups y convenio
                    
                        if (codigoCupsId[0].requiereAutorizacion == 'N'):

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",                                       password="123456")
                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia_id,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro") VALUES (' + "'" +  str(consecLiquidacion)  + "','" + str(fechaRegistro) + "','" + str(cantidad) + "','"  + str(tarifaValor) + "','" + str(TotalTarifa)  + "',null,'" +  str(fechaRegistro) + "','" +  str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(codigoCupsId[0].id) + "','" + str(usuarioRegistro) + "'," + liquidacionId + ",'SISTEMA')"
                            curt.execute(comando)
                            miConexiont.commit()
                            miConexiont.close()

                            consecLiquidacion = int(consecLiquidacion) + 1


	            # Fin rutina Facturacion

                     ## Fin
                print("tamaño matriz radiologia", len(radiologia[0]))

                if conteoRad >=  1:
                    print("Encontre ordenes de radiologia")
                    print("Encontre ordenes de radiologia")
                    ingresoId2 = ingresosPaciente.id
                    ImprimirOrdenRadiologia(ingresoId2, historiaId, convenioId, tipoAdmision)
                else:
                    print("No Encontre ordenes de radiologia")
                    print("No Encontre ordenes de radiologia")


                # Fin Grabacion Radiologia

                     # Grabacion Terapias

                terapias = request.POST["terapias"]
                print("terapias =", terapias)

                ## Rutina leer el JSON de laboratorios en python primero
                consecutivo = 0
                jsonTerapias = json.loads(terapias)
                conteoTer=0

                for key2 in jsonTerapias:

                   print("key2 = ", key2)
                   queda = key2
                   tiposExamen_Id = key2["tiposExamen_Id"]
                   print("tiposExamen_Id", tiposExamen_Id)
                   cups = key2["cups"].strip()
                   print("cups = ", cups)
                   cantidad = key2["cantidad"]
                   print("cantidad", cantidad)
                   observa = key2["observa"]
                   print("observa", observa)
                   estadoExamenes_id = "1"

                   if cups != "":
                        consecutivo = consecutivo + 1
                          #codigoCups = Examenes.objects.get(nombre=nombreTerapias)
                        c = HistoriaExamenes(tiposExamen_id=tiposExamen_Id, codigoCups=cups,
                                               cantidad=cantidad, consecutivo=consecutivo, observaciones=observa,
                                               estadoReg='A',
                                               estadoExamenes_id=estadoExamenes_id, anulado="N",
                                                historia_id=historiaId, usuaroRegistra_id=usuarioRegistro, consecutivoLiquidacion=consecLiquidacion)
                        c.save()
                        conteoTer=conteoTer + 1

			## Desde Aqui rutina de Facturacion
                          #
                        codigoCupsId = Examenes.objects.filter(codigoCups=cups)
                        print("codigoCupsId", codigoCupsId[0].id)

                        # Rutiva busca en convenio el valor de la tarifa CUPS
                        print("liquidacionId = ", liquidacionId)
                        print ("cups no id = ",cups)

                        miConexion3 = None
                        try:
                            if (columnaALeerPropia != ''):

                                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                               user="postgres", password="123456")

                                curt = miConexiont.cursor()
                                comando = 'SELECT conv.convenio_id id ,exa."codigoCups" cups, proc."' + str(
                                    columnaALeer.columna) + '"' + ' valor FROM facturacion_conveniospacienteingresos conv, tarifarios_tarifariosdescripcion des, tarifarios_tarifariosprocedimientos proc, clinico_examenes exa, contratacion_convenios conv1 , tarifarios_tipostarifa tiptar WHERE conv."tipoDoc_id" = ' + "'" + str(
                                    tipoDocId.id) + "'" + ' AND conv.documento_id = ' + "'" + str(
                                    documentoId.id) + "'" + ' AND conv."consecAdmision" = ' + "'" + str(
                                    ingresoPaciente) + "'" + ' AND conv.convenio_id = conv1.id AND des.id = conv1."tarifariosDescripcionProc_id" AND proc."codigoCups_id" = exa.id  And exa.id = ' + "'" + str(
                                    codigoCupsId[
                                        0].id) + "'" + ' AND des."tiposTarifa_id" = tiptar.id and proc."tiposTarifa_id" = tiptar.id'
                                print("comando = ", comando)
                                curt.execute(comando)

                                convenioValor = []

                                for id, cups, tarifaValor in curt.fetchall():
                                    convenioValor.append({'id': id, 'cups': cups, 'valor': tarifaValor})

                                miConexiont.close()
                            else:
                                convenioValor = []

                            print("columnaALeer.columna", columnaALeerPropia)
                            print("convenioValor = ", convenioValor)
                            print("codigoCupsId[0].id = ", codigoCupsId[0].id)

                            # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones

                            print("el cups :", cups)

                            print("autorizacion para el CUPS es ", codigoCupsId[0].requiereAutorizacion)

                            # Aqui saca valores pata tarifas

                            if convenioValor != []:

                                print("Cups = ", convenioValor[0]['cups'])
                                tarifaValor = convenioValor[0]['valor']
                                tarifaValor = str(tarifaValor)
                                print("tarifaValor = ", tarifaValor)
                                tarifaValor = tarifaValor.replace("None", ' ')
                                tarifaValor = tarifaValor.replace("(", ' ')
                                tarifaValor = tarifaValor.replace(")", ' ')
                                tarifaValor = tarifaValor.replace(",", ' ')
                                tarifaValor = tarifaValor.replace(" ", '')
                                print("tarifaValor = ", tarifaValor)
                            else:
                                tarifaValor = 0

                            if tarifaValor == '':
                                print("Entre cambiar tarufa Valor", tarifaValor)
                                tarifaValor = 0

                        except psycopg2.DatabaseError as error:
                            print("Entre por rollback", error)
                            if miConexion3:
                                print("Entro ha hacer el Rollback")
                                miConexion3.rollback()
                                tarifaValor = 0

                        finally:
                            if miConexion3:
                                cur3.close()
                                miConexion3.close()


                        TotalTarifa = float(tarifaValor) * float(cantidad)

                        # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones

                        print("el cups :", cups)


                        if (codigoCupsId[0].requiereAutorizacion == 'S'):

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                            curt = miConexiont.cursor()
                            comando = 'SELECT aut.id id FROM autorizaciones_autorizaciones  aut, clinico_historia historia WHERE  aut.historia_id = historia.id AND historia."tipoDoc_id" = ' + "'" + str(
                                tipoDocId.id) + "' AND historia.documento_id = " + "'" + str(
                                documentoId.id) + "'" + ' AND historia."consecAdmision" = ' + "'" + str(
                                ingresoPaciente) + "' AND aut.historia_id = " + "'" + str(historiaId) + "'"

                            curt.execute(comando)
                            hayAut = []

                            for id in curt.fetchall():
                                hayAut.append({'id': id})

                            miConexiont.close()

                            estadoAutorizacionId = EstadosAutorizacion.objects.get(nombre='PENDIENTE')


                            hayAut = str(hayAut[0]['id'])
                            hayAut = hayAut.replace("None", ' ')
                            hayAut = hayAut.replace("(", ' ')
                            hayAut = hayAut.replace(")", ' ')
                            hayAut = hayAut.replace(",", ' ')
                            hayAut = hayAut.replace(" ", '')
                            print("hayAut = ", hayAut)

                            if hayAut == '':
                                print ("Entre Autorizaciones detalle")

                                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                               user="postgres", password="123456")

                                curt = miConexiont.cursor()
                                #comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" +  str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ' FROM facturacion_conveniospacienteingresos convIngreso, contratacion_conveniosprocedimientos proc, contratacion_convenios conv WHERE conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" +  str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = proc.convenio_id AND proc.cups_id = " + "'" +  str(codigoCupsId[0].id) + "' RETURNING id"
                                comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id, convenio_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" + str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ' , conv.id FROM facturacion_conveniospacienteingresos convIngreso,  contratacion_convenios conv WHERE conv.id = ' + "'" + str(convenioId) + "'" + ' AND conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = " + "'" + str(convenioValor[0]['id']) + "'" + ' RETURNING id'
                                print("comando " , comando)
                                curt.execute(comando)
                                autorizacionId = curt.fetchone()[0]
                                miConexiont.commit()
                                miConexiont.close()

                                #autorizacionIdU = Autorizaciones.objects.all().filter(
                                #    historia_id=historia.id).aggregate(maximo=Coalesce(Max('id'), 0))
                                #autorizacionId = (autorizacionIdU['maximo']) + 0

                            else:

                                autorizacionId = hayAut

                            print("Autorizacion Final = ", autorizacionId)

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id","valorSolicitado")  VALUES (' + "'" + str(estadoAutorizacionId.id) + "'," + "'" + str(cantidad) + "'" + ' ,0, now(),' + "'" + str('A') + "','"  + str(autorizacionId) + "','" + str(usuarioRegistro)  + "'," +  "'"  + str(codigoCupsId[0].id) + "',null,'" + str(tiposExamen_Id) + "','" + str(tarifaValor) + "')"
                            print("comando autdetalle = ", comando)
                            curt.execute(comando)
                            miConexiont.commit()
                            miConexiont.close()

                            # Fin tema Autorizaciones




                    # Aqui Rutina FACTURACION crea en liquidaciondetalle el registro con la tarifa, con campo cups y convenio
                    #
                        print("autorizacion = ", codigoCupsId[0].requiereAutorizacion)

                        if (codigoCupsId[0].requiereAutorizacion == 'N'):
                            print("Entre a guardar liquidaciondetalle")

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",                                       password="123456")
                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia_id,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro") VALUES (' + "'" +  str(consecLiquidacion)  + "','" + str(fechaRegistro) + "','" + str(cantidad) + "','"  + str(tarifaValor) + "','" + str(TotalTarifa)  + "',null,'" +  str(fechaRegistro) + "','" +  str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(codigoCupsId[0].id) + "','" + str(usuarioRegistro) + "'," + liquidacionId + ",'SISTEMA')"
                            curt.execute(comando)
                            miConexiont.commit()
                            miConexiont.close()

                            consecLiquidacion = int(consecLiquidacion) + 1


	            # Fin rutina Facturacion

                         ## Fin
                # Rutina Impresion Ordenes de Laboratorio
                print("tamaño matriz terapias", len(terapias[0]))

                if conteoTer >= 1:
                    print("Encontre ordenes de terapias")
                    print("Encontre ordenes de terapias")
                    ingresoId2 = ingresosPaciente.id
                    ImprimirOrdenTerapia(ingresoId2, historiaId, convenioId, tipoAdmision)
                else:
                    print("No Encontre ordenes de terapias")
                    print("No Encontre ordenes de terapias")



                   # Fin Grabacion Terapias

                     # Grabacion noQx

                noQx = request.POST["noQx"]
                print("noQx =", noQx)

                ## Rutina leer el JSON de laboratorios en python primero
                consecutivo = 0
                jsonNoQx = json.loads(noQx)

                for key3 in jsonNoQx:

                   print("key2 = ", key3)
                   queda = key3
                   tiposExamen_Id = key3["tiposExamen_Id"]
                   print("tiposExamen_Id", tiposExamen_Id)
                   cups = key3["cups"].strip()
                   print("cups = ", cups)
                   cantidad = key3["cantidad"]
                   print("cantidad", cantidad)
                   observa = key3["observa"]
                   print("observa", observa)
                   estadoExamenes_id = "1"

                   if cups != "":
                          consecutivo = consecutivo + 1
                          #codigoCups = Examenes.objects.get(nombre=nombreTerapias)
                          c = HistoriaExamenes(tiposExamen_id=tiposExamen_Id, codigoCups=cups,
                                               cantidad=cantidad, consecutivo=consecutivo, observaciones=observa,
                                               estadoReg='A',
                                               estadoExamenes_id=estadoExamenes_id, anulado="N",
                                                historia_id=historiaId, usuaroRegistra_id=usuarioRegistro, consecutivoLiquidacion=consecLiquidacion)
                          c.save()


                          ## Desde Aqui rutina de Facturacion
                        #
                          codigoCupsId = Examenes.objects.filter(codigoCups=cups)
                          print ("codigoCupsId", codigoCupsId[0].id)

                          miConexion3 = None
                          try:
                              if (columnaALeerPropia != ''):

                                  miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                                 user="postgres", password="123456")

                                  curt = miConexiont.cursor()
                                  comando = 'SELECT conv.convenio_id id ,exa."codigoCups" cups, proc."' + str(
                                      columnaALeer.columna) + '"' + ' valor FROM facturacion_conveniospacienteingresos conv, tarifarios_tarifariosdescripcion des, tarifarios_tarifariosprocedimientos proc, clinico_examenes exa, contratacion_convenios conv1 , tarifarios_tipostarifa tiptar WHERE conv."tipoDoc_id" = ' + "'" + str(
                                      tipoDocId.id) + "'" + ' AND conv.documento_id = ' + "'" + str(
                                      documentoId.id) + "'" + ' AND conv."consecAdmision" = ' + "'" + str(
                                      ingresoPaciente) + "'" + ' AND conv.convenio_id = conv1.id AND des.id = conv1."tarifariosDescripcionProc_id" AND proc."codigoCups_id" = exa.id  And exa.id = ' + "'" + str(
                                      codigoCupsId[
                                          0].id) + "'" + ' AND des."tiposTarifa_id" = tiptar.id and proc."tiposTarifa_id" = tiptar.id'
                                  print("comando = ", comando)
                                  curt.execute(comando)

                                  convenioValor = []

                                  for id, cups, tarifaValor in curt.fetchall():
                                      convenioValor.append({'id': id, 'cups': cups, 'valor': tarifaValor})

                                  miConexiont.close()
                              else:
                                  convenioValor = []

                              print("columnaALeer.columna", columnaALeerPropia)
                              print("convenioValor = ", convenioValor)
                              print("codigoCupsId[0].id = ", codigoCupsId[0].id)

                              # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones

                              print("el cups :", cups)

                              print("autorizacion para el CUPS es ", codigoCupsId[0].requiereAutorizacion)

                              # Aqui saca valores pata tarifas

                              if convenioValor != []:

                                  print("Cups = ", convenioValor[0]['cups'])
                                  tarifaValor = convenioValor[0]['valor']
                                  tarifaValor = str(tarifaValor)
                                  print("tarifaValor = ", tarifaValor)
                                  tarifaValor = tarifaValor.replace("None", ' ')
                                  tarifaValor = tarifaValor.replace("(", ' ')
                                  tarifaValor = tarifaValor.replace(")", ' ')
                                  tarifaValor = tarifaValor.replace(",", ' ')
                                  tarifaValor = tarifaValor.replace(" ", '')
                                  print("tarifaValor = ", tarifaValor)
                              else:
                                  tarifaValor = 0

                              if tarifaValor == '':
                                  print("Entre cambiar tarufa Valor", tarifaValor)
                                  tarifaValor = 0

                          except psycopg2.DatabaseError as error:
                              print("Entre por rollback", error)
                              if miConexion3:
                                  print("Entro ha hacer el Rollback")
                                  miConexion3.rollback()
                                  tarifaValor = 0

                          finally:
                              if miConexion3:
                                  cur3.close()
                                  miConexion3.close()


                          TotalTarifa = float(tarifaValor) * float(cantidad)

                          # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones

                          print("el cups :", cups)
                          print("Requiere autorizacion :", codigoCupsId[0].requiereAutorizacion)

                          if (codigoCupsId[0].requiereAutorizacion == 'S'):

                              miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                             user="postgres", password="123456")

                              curt = miConexiont.cursor()
                              comando = 'SELECT aut.id id FROM autorizaciones_autorizaciones  aut, clinico_historia historia WHERE  aut.historia_id = historia.id AND historia."tipoDoc_id" = ' + "'" + str(
                                  tipoDocId.id) + "' AND historia.documento_id = " + "'" + str(
                                  documentoId.id) + "'" + ' AND historia."consecAdmision" = ' + "'" + str(
                                  ingresoPaciente) + "' AND aut.historia_id = " + "'" + str(historiaId) + "'"

                              curt.execute(comando)
                              hayAut = []

                              for id in curt.fetchall():
                                  hayAut.append({'id': id})

                              miConexiont.close()
                              estadoAutorizacionId = EstadosAutorizacion.objects.get(nombre='PENDIENTE')

                              hayAut = str(hayAut[0]['id'])
                              hayAut = hayAut.replace("None", ' ')
                              hayAut = hayAut.replace("(", ' ')
                              hayAut = hayAut.replace(")", ' ')
                              hayAut = hayAut.replace(",", ' ')
                              hayAut = hayAut.replace(" ", '')
                              print("hayAut = ", hayAut)


                              if hayAut == '':

                                  miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                                 user="postgres", password="123456")

                                  curt = miConexiont.cursor()
                                  comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id, convenio_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" + str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ', conv.id FROM facturacion_conveniospacienteingresos convIngreso,  contratacion_convenios conv WHERE conv.id = ' + "'" + str(convenioId) + "'" + ' AND conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = " + "'" + str(convenioValor[0]['id']) + "'" + ' RETURNING id'

                                  curt.execute(comando)
                                  autorizacionId = curt.fetchone()[0]
                                  miConexiont.commit()
                                  miConexiont.close()

                                  #autorizacionIdU = Autorizaciones.objects.all().filter(
                                  #    historia_id=historia.id).aggregate(maximo=Coalesce(Max('id'), 0))
                                  #autorizacionId = (autorizacionIdU['maximo']) + 0

                              else:

                                  autorizacionId = hayAut[0]

                              print("Autorizacion Final = ", autorizacionId)

                              miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                             user="postgres", password="123456")

                              curt = miConexiont.cursor()
                              comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAitorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "examenes_id", cums_id, "tiposExamen_id","valorSolicitado")  VALUES (' + "'" + str(
                                  estadoAutorizacionId.id) + "'," + "'" + str(cantidad) + "'" + ' ,0, now(),' + "'" + str(
                                  'A') + "','" + str(autorizacionId) + "','" + str(usuarioRegistro) + "'," + "'" + str(
                                  codigoCupsId[0].id) + "',null," + "'" + str(tiposExamen_Id) + "','" + str(tarifaValor) + "')"

                              curt.execute(comando)

                              miConexiont.close()

                              # Fin tema Autorizaciones

                          # Aqui Rutina FACTURACION crea en liquidaciondetalle el registro con la tarifa, con campo cups y convenio
                      #
                          if (codigoCupsId[0].requiereAutorizacion == 'N'):

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",                                       password="123456")
                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia,"fechaCrea", "fechaRegistro", "estadoRegistro", "examen_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro") VALUES (' + "'" +  str(consecLiquidacion)  + "','" + str(fechaRegistro) + "','" + str(cantidad) + "','"  + str(tarifaValor) + "','" + str(TotalTarifa)  + "','" + str('N') + "','" +  str(fechaRegistro) + "','" +  str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(codigoCupsId[0].id) + "','" + str(usuarioRegistro) + "'," + liquidacionId + ",'SISTEMA')"
                            curt.execute(comando)
                            miConexiont.commit()
                            miConexiont.close()

                            consecLiquidacion = int(consecLiquidacion) + 1

    	              # Fin rutina Facturacion

                          print("tipoExamen =", key3["tiposExamen_Id"])
                          print("cups =", key3["cups"])
                          print("cantidad =", key3["cantidad"])
                          print("observaciones =", key3["observa"])

                         ## Fin

                     # Fin Grabacion noQx

                     # Grabacion Antecedentes

                antecedentes = request.POST["antecedentes"]
                print("antecedentes =", antecedentes)

                ## Rutina leer el JSON de laboratorios en python primero
                jsonAntecedentes = json.loads(antecedentes)

                for key4 in jsonAntecedentes:

                   print("key4 = ", key4)
                   queda = key4
                   id = key4["id"].strip()
                   print("id = ", id)
                   tipo = key4["tipo"]
                   print("tipo", tipo)
                   descripcion = key4["descripcion"]

                   estadoExamenes_id = "1"

                   if tipo != "":


                          d = HistorialAntecedentes(descripcion=descripcion, fechaRegistro=fechaRegistro,
                                               tiposAntecedente_id=id,
                                               estadoReg='A', historia_id=historiaId, usuarioRegistro_id=usuarioRegistro)
                          d.save()

                          print("id =", key4["id"])
                          print("tipo =", key4["tipo"])
                          print("descripcion =", key4["descripcion"])


                         ## Fin

                     # Fin Grabacion Antecedentes

                     # Grabacion Diagnosticos

                diagnosticos = request.POST["diagnosticos"]
                print("diagnosticos =", diagnosticos)

                ## Rutina leer el JSON de Diagnosticos en python primero
                consecutivo=0
                jsonDiagnosticos = json.loads(diagnosticos)

                for key5 in jsonDiagnosticos:

                   print("key5 = ", key5)
                   queda = key5

                   diagnosticoId = key5["diagnosticos"]
                   print("diagnosticoId", diagnosticoId)
                   tiposDiagnosticoId = key5["tiposDiagnosticos"]
                   print("tiposDiagnosticoId", tiposDiagnosticoId)
                   observa = key5["observa"]

                   if salidaClinica=='S':
                       diagnosticoIdSalida = diagnosticoId


                   if diagnosticoId != "":
                          consecutivo = consecutivo + 1
                          e = HistorialDiagnosticos(observaciones=observa, diagnosticos_id=diagnosticoId,tiposDiagnostico_id=tiposDiagnosticoId,
                                        estadoReg='A', historia_id=historiaId, consecutivo=consecutivo)
                          e.save()

                         ## Fin

                     # Fin Grabacion Diagnosticos

                # Antecedentes

                ## Rutina leer el JSON de laboratorios en python primero

                jsonAntecedentes = json.loads(antecedentes)

                for key4 in jsonAntecedentes:

                   print("key4 = ", key4)
                   queda = key4
                   id = key4["id"].strip()
                   print("id = ", id)
                   tipo = key4["tipo"]
                   print("tipo", tipo)
                   descripcion = key4["descripcion"]

                   estadoExamenes_id = "1"

                   if tipo != "":


                          d = HistorialAntecedentes(descripcion=descripcion, fechaRegistro=fechaRegistro,
                                               tiposAntecedente_id=id,
                                               estadoReg='A', historia_id=historiaId, usuarioRegistro_id=usuarioRegistro)
                          d.save()

                          print("id =", key4["id"])
                          print("tipo =", key4["tipo"])
                          print("descripcion =", key4["descripcion"])


                         ## Fin

                     # Fin Grabacion Antecedentes

                   # Grabacion Interconsultas

                interconsultas = request.POST["interconsultas"]
                print("interconsultas =", interconsultas)

                ## Rutina leer el JSON de laboratorios en python primero

                jsonInterconsultas = json.loads(interconsultas)

                for key6 in jsonInterconsultas:

                    print("key6 = ", key6)
                    queda = key6

                    diagnosticoId = key6["diagnosticos"]
                    print("diagnosticoId", diagnosticoId)

                    especialidadConsultadaId = key6["especialidadConsultada"]
                    print("especialidadConsultadaId", especialidadConsultadaId)

                    medicoConsultadoId = key6["medicoConsultado"]
                    print("medicoConsultadoId", medicoConsultadoId)

                    tiposInterconsultaId = key6["tiposInterconsulta"]
                    print("tiposInterconsultaId", tiposInterconsultaId)

                    especialidadConsultadaId = key6["especialidadConsultada"]
                    print("especialidadConsultaId", especialidadConsultadaId)


                    tiposInterconsultaId = key6["tiposInterconsulta"]
                    print("tiposInterconsultaId", tiposInterconsultaId)

                    descripcionConsulta = key6["descripcion"]

                    estado = EstadosInterconsulta.objects.get(nombre='PENDIENTE')
                    print ("estadoInterconsulta", estado.id)

                    if medicoConsultadoId != "":

                        f = HistorialInterconsultas(descripcionConsulta=descripcionConsulta, diagnosticos_id=diagnosticoId,
                                                  especialidadConsultada_id=especialidadConsultadaId,medicoConsultado_id=medicoConsultadoId,
                                           especialidadConsulta_id=espMedico, medicoConsulta_id=medicoId.id,
                                                  historia_id=historiaId, tipoInterconsulta_id=tiposInterconsultaId,estadosInterconsulta_id=estado.id)
                        f.save()

                    ## Fin



                    # Fin Grabacion Interconsultas

                        # Grabacion incapacidades

                incapForm = request.POST['incapacidades']

                 #incapForm = incapacidades(request.POST)
                print("incapForm= ", incapForm )


                print("voy a validar incapacidad")

                jsonIncapacidades = json.loads(incapForm)

                for key7 in jsonIncapacidades:

                    tiposIncapacidad=key7["tiposIncapacidad"]
                    diagnosticosIncapacidad=key7["diagnosticosIncapacidad"]
                    desdeFecha=key7["desdeFecha"]
                    hastaFecha=key7["hastaFecha"]
                    #desdeFecha = datetime.datetime.strptime(desdeFecha, "YYYY-MM-DD")
                    #hastaFecha = datetime.datetime.strptime(hastaFecha, "YYYY-MM-DD")
                    desdeFecha = fechaRegistro
                    hastaFecha = fechaRegistro
                    print("desdeFecha =" , desdeFecha)
                    numDias=key7["numDias"]
                    descripcion=key7["descripcion"]

                    print("voy a guardar incapacidad")

                    if tiposIncapacidad != "":
                        print("voy a guardar incapacidad")
                        g = HistorialIncapacidades(tiposIncapacidad_id=tiposIncapacidad, diagnosticosIncapacidad_id=diagnosticosIncapacidad,
                                          descripcion=descripcion,desdeFecha=desdeFecha,  hastaFecha=hastaFecha, numDias=numDias,  historia_id=historiaId,estadoReg='A', fechaRegistro=fechaRegistro)
                        g.save()
                        print("ya guarde incapacidad")


                print("Longitud de incapaciddaes = " , len(incapForm[0]))

                if len(incapForm[0]) > 1:

                    print("Entre imprimir incapacidad")
                    ingresoId2=ingresosPaciente.id
                    ImprimirOrdenIncapacidad(ingresoId2, historiaId)


                # Fin Grabacion incapacidades


            # Grabacion signos

                signosForm = request.POST['signos']
                print("signosForm= ", signosForm )
                print("voy a validar signos")
                jsonSignos = json.loads(signosForm)

                for key8 in jsonSignos:

                    fecha=key8["fecha"]
                    frecCardiaca=key8["frecCardiaca"]
                    frecRespiratoria=key8["frecRespiratoria"]
                    tensionADiastolica=key8["tensionADiastolica"]
                    tensionASistolica=key8["tensionASistolica"]
                    temperatura=key8["temperatura"]
                    saturacion = key8["saturacion"]
                    glucometria = key8["glucometria"]
                    glasgow = key8["apache"]
                    pvc = key8["pvc"]
                    ic = key8["ic"]
                    cuna = key8["cuna"]
                    glasgowOcular = key8["glasgowOcular"]
                    glasgowVerbal = key8["glasgowVerbal"]
                    glasgowMotora = key8["glasgowMotora"]

                    print ("VOY A GRABAR")

                    if fecha != "":
                        h = HistoriaSignosVitales(fecha=fecha, frecCardiaca=frecCardiaca,
                                       frecRespiratoria=frecRespiratoria,  tensionADiastolica=tensionADiastolica, tensionASistolica=tensionASistolica,
                                          temperatura=temperatura,saturacion=saturacion,glucometria=glucometria,glasgow=glasgow,pvc=pvc,ic=ic,cuna=cuna,
                                          glasgowOcular=glasgowOcular,glasgowVerbal=glasgowVerbal,glasgowMotora=glasgowMotora,
                                          historia_id=historiaId,estadoReg='A', fechaRegistro=dnow  ,usuarioRegistro_id=plantaId.id )
                        h.save()


                # Fin Grabacion signos

               # Grabacion Revision Sistemas

                revisionSistemas = request.POST['revisionSistemas']
                print("revisionSistemas =", revisionSistemas)

                print("voy a validar revisionSistemas")

                jsonRevisionSistemas = json.loads(revisionSistemas)

                for key9 in jsonRevisionSistemas:

                    revisionSistemas=key9["revisionSistemas"]
                    observa=key9["observa"]

                    if revisionSistemas != "":
                        h = HistoriaRevisionSistemas(observacion=observa, revisionSistemas_id= revisionSistemas,
                                          historia_id=historiaId,usuarioRegistro_id=usuarioRegistro  , estadoReg='A', fechaRegistro=fechaRegistro )
                        h.save()


                # Fin Grabacion Revision Sistemas


               # Grabacion Formulacion

                formulacion = request.POST["formulacion"]
                print("Longitud de formulacion ANTES DE = ", len(formulacion[0]))
                print("voy a validar Medicamentos =", formulacion)

                jsonFormulacion = json.loads(formulacion)

                print("voy para el FOR")

                print("voy a validar JSONMedicamentos =", jsonFormulacion)

                consecutivo = 1

                # Consigue el esato de Farmacia SOLICITUD

                estadoFarmaciaSolicitud = FarmaciaEstados.objects.get(nombre='SOLICITUD')

                print("estadoFarmaciaSolicitud", estadoFarmaciaSolicitud)
                conteoMed=0

                for key in jsonFormulacion:

                    medicamentos = key["medicamentos"]
                    print("medicamentos=", medicamentos)

                    dosis = key["dosis"]
                    print("dosis=", dosis)
                    uMedidaDosis = key["uMedidaDosis"]
                    print("uMedidaDosis=", uMedidaDosis)
                    frecuencia = key["frecuencia"]
                    print("frecuencia=", frecuencia)
                    vias = key["vias"]
                    print("vias =", vias )
                    viasAdministracion = key["viasAdministracion"]
                    print("viasAdministracion =", viasAdministracion )
                    cantidadMedicamento = key["cantidadMedicamento"]
                    print("cantidadMedicamento=", cantidadMedicamento)
                    diasTratamiento = key["diasTratamiento"]
                    print("diasTratamiento=", diasTratamiento)

                    if medicamentos != "":
                        conteoMed=conteoMed+1
                        i = HistoriaMedicamentos(dosisCantidad=dosis, suministro_id= medicamentos,frecuencia_id=frecuencia,dosisUnidad_id=uMedidaDosis,  
                                                   viaAdministracion_id = vias,  cantidadOrdenada= cantidadMedicamento, diasTratamiento= diasTratamiento,
                                          historia_id=historiaId,usuarioRegistro_id=usuarioRegistro  , estadoReg='A', fechaRegistro=fechaRegistro , consecutivoLiquidacion=0, consecutivoMedicamento=consecutivo)
                        i.save()


                        print("Esto grabe de Medicamentos : ", i.id);

                        # Aqui rutina Actualizar totales de CABEZOTE de liquidacion. Primero por ORM calcula totales
                        # OJOOO ESTA RUTINA se debe hacer desde DISPENSACION NDE FARMAICA.
                        # POR EL MOMNETO DESDE AQUIP

                        print("medicamentos = ", medicamentos)

                        medicamentosId = Suministros.objects.get(id=medicamentos)
                        print("medicamentosId total", medicamentosId)
                        print("medicamentosId", medicamentosId.id)
                        print("requiereAutorizacion", medicamentosId.requiereAutorizacion)

                        tiposSuministroId = TiposSuministro.objects.get(nombre='MEDICAMENTOS')

                        # Aqui logica para crear el cabezote de Farmacia y Enfermeria

                        if (consecutivo == 1 and medicamentosId.requiereAutorizacion == 'N'):

                            # Aqui Gaurdar FARMACIA

                            f = Farmacia(historia_id=historiaId , serviciosAdministrativos_id =serviciosAdministrativos , tipoOrigen_id = '1', tipoMovimiento_id = '1' , fechaRegistro =fechaRegistro  , usuarioRegistro_id  =  usuarioRegistro, estadoReg = 'A' , sedesClinica_id = sede,  estado_id= estadoFarmaciaSolicitud.id, ingresoPaciente_id=ingresosPaciente.id)
                            f.save()

                            # Aqui Guardar ENFERMERIA

                            e = Enfermeria(historia_id=historiaId , serviciosAdministrativos_id =serviciosAdministrativos , tipoOrigen_id = '1', tipoMovimiento_id = '1' , fechaRegistro =fechaRegistro  , usuarioRegistro_id  =  usuarioRegistro, estadoReg = 'A' , sedesClinica_id = sede , ingresoPaciente_id=ingresosPaciente.id)
                            e.save()

                        if (medicamentosId.requiereAutorizacion == 'N'):

                            # Aqui Guardar FARMACIA DETALLE
                            #
                            fd = FarmaciaDetalle(farmacia_id=f.id , historiaMedicamentos_id = i.id , suministro_id = medicamentos ,  dosisCantidad = dosis,  dosisUnidad_id =uMedidaDosis ,viaAdministracion_id = vias , cantidadOrdenada=cantidadMedicamento  , fechaRegistro =fechaRegistro ,  usuarioRegistro_id  =  usuarioRegistro, estadoReg = 'A', consecutivoMedicamento=consecutivo)
                            fd.save()

                            # Aqui Guardar ENFERMERIA DETALLE

                            er = EnfermeriaDetalle(enfermeria_id=e.id , historiaMedicamentos_id = i.id , farmaciaDetalle_id = fd.id, suministro_id = medicamentos ,  dosisCantidad = dosis,  dosisUnidad_id =uMedidaDosis ,viaAdministracion_id = vias ,  cantidadOrdenada=cantidadMedicamento  ,fechaRegistro =fechaRegistro ,  usuarioRegistro_id  =  usuarioRegistro, estadoReg = 'A', frecuencia_id=frecuencia, diasTratamiento=diasTratamiento)
                            er.save()

                        consecutivo = consecutivo + 1


                        # Fin Grabacion Formulacion


                        ## Desde Aqui rutina de Facturacion
                        #
                     
                        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                       user="postgres", password="123456")
                        curt = miConexiont.cursor()
                        #comando = 'SELECT convIngreso.convenio_id convenio ,sum.suministro_id sum, sum.valor tarifaValor FROM facturacion_conveniospacienteingresos convIngreso, contratacion_conveniossuministros sum WHERE convIngreso."tipoDoc_id" = ' + "'" +  str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND convIngreso.convenio_id = sum.convenio_id AND sum.suministro_id = " + "'" +  str(medicamentos) + "'"
                        comando = 'SELECT conv.convenio_id id ,exa.cums cums, sum."' + str(columnaALeer.columna) + '"' + ' tarifaValor FROM facturacion_conveniospacienteingresos conv, tarifarios_tarifariosdescripcion des, tarifarios_tarifariossuministros sum, facturacion_suministros exa, contratacion_convenios conv1 , tarifarios_tipostarifa tiptar WHERE conv."tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "'" + ' AND conv.documento_id = ' + "'" + str(documentoId.id) + "'" + ' AND conv."consecAdmision" = ' + "'" + str(ingresoPaciente) + "'" + ' AND conv.convenio_id = conv1.id AND des.id = conv1."tarifariosDescripcionSum_id" AND sum."codigoCum_id" = exa.id  And exa.id = ' + "'" + str(medicamentos) + "'" + ' AND des."tiposTarifa_id" = tiptar.id and sum."tiposTarifa_id" = tiptar.id'

                        print ("comando =" , comando)

                        curt.execute(comando)

                        convenioValor = []

                        for id, sum,tarifaValor   in curt.fetchall():
                            convenioValor.append({'id': id, 'sum':sum, 'valor':tarifaValor})

                        miConexiont.close()

                        if (convenioValor != []):

                            print("convenioValor[0]['valor'] = ", convenioValor[0]['valor'])
                            print("convenioValor[0]['sum'] = ", convenioValor[0]['sum'])

                        # Aqui analiza si es necesario que caiga en la tabla de Autorizaciones


                        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                        curt = miConexiont.cursor()

                        if (medicamentosId.requiereAutorizacion == 'S'):

                            comando = 'SELECT aut.id id FROM autorizaciones_autorizaciones  aut, clinico_historia historia WHERE  aut.historia_id = historia.id AND historia."tipoDoc_id" = ' + "'" + str(
                                tipoDocId.id) + "' AND historia.documento_id = " + "'" + str(
                                documentoId.id) + "'" + ' AND historia."consecAdmision" = ' + "'" + str(
                                ingresoPaciente) + "' AND aut.historia_id = " + "'" + str(historiaId) + "'"

                            curt.execute(comando)
                            hayAut = []

                            for id in curt.fetchall():
                                hayAut.append({'id': id})


                            estadoAutorizacionId = EstadosAutorizacion.objects.get(nombre='PENDIENTE')

                            hayAut = str(hayAut[0]['id'])
                            hayAut = hayAut.replace("None", ' ')
                            hayAut = hayAut.replace("(", ' ')
                            hayAut = hayAut.replace(")", ' ')
                            hayAut = hayAut.replace(",", ' ')
                            hayAut = hayAut.replace(" ", '')
                            print("hayAut = ", hayAut)

                            if hayAut == '':


                                #comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" +  str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ' FROM facturacion_conveniospacienteingresos convIngreso, contratacion_conveniosprocedimientos proc, contratacion_convenios conv WHERE conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" +  str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = proc.convenio_id AND proc.cups_id = " + "'" +  str(medicamentos) + "' RETURNING id"
                                comando = 'INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id, convenio_id )  SELECT ' + "'" + str(estadoAutorizacionId.id) + "'" + ', now(), now(), ' + "'" + str('A') + "'" + ', conv.empresa_id,  ' + "'" + str(plantaId.id) + "','" + str(sede) + "','" + str(usuarioRegistro) + "'," + "'" + str(historiaId) + "'" + ', conv.id FROM facturacion_conveniospacienteingresos convIngreso,  contratacion_convenios conv WHERE conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = ' + "'" + str(tipoDocId.id) + "' AND convIngreso.documento_id = " + "'" + str(documentoId.id) + "'" + ' AND convIngreso."consecAdmision" = ' + "'" + str(ingresoPaciente) + "' AND conv.id = " + "'" + str(convenioValor[0]['id']) + "'" + ' RETURNING id'
                                print("comando " , comando)
                                curt.execute(comando)
                                autorizacionId = curt.fetchone()[0]
                                miConexiont.commit()

                                #autorizacionIdU = Autorizaciones.objects.all().filter(historia_id=historiaId).aggregate(maximo=Coalesce(Max('id'), 0))
                                #autorizacionId = (autorizacionIdU['maximo']) + 0

                            else:
                                autorizacionId = hayAut

                            print("Autorizacion Final = ", autorizacionId)

                            miConexiont.close()

                            miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")

                            curt = miConexiont.cursor()
                            comando = 'INSERT INTO autorizaciones_autorizacionesdetalle ("estadoAutorizacion_id", "cantidadSolicitada", "cantidadAutorizada", "fechaRegistro", "estadoReg", autorizaciones_id, "usuarioRegistro_id", "tipoSuministro_id", cums_id,"historiaMedicamentos_id")  VALUES (' + "'" + str(estadoAutorizacionId.id) + "'," + "'" + str(cantidadMedicamento) + "'" + ' ,0, now(),' + "'" + str('A') + "','"  + str(autorizacionId) + "','" + str(usuarioRegistro)  + "','" + str(tiposSuministroId.id) + "','" + str(medicamentos) + "','" + str(i.id) + "')"


                            curt.execute(comando)
                            miConexiont.commit()
                            miConexiont.close()

                            # Fin tema Autorizaciones

                        if (convenioValor != []):

                            print ("Sum = "  , convenioValor[0]['sum'])
                            tarifaValor = convenioValor[0]['valor']
                            tarifaValor = str(tarifaValor)
                            print("tarifaValor = ", tarifaValor)
                            tarifaValor = tarifaValor.replace("None", ' ')
                            tarifaValor = tarifaValor.replace("(", ' ')
                            tarifaValor = tarifaValor.replace(")", ' ')
                            tarifaValor = tarifaValor.replace(",", ' ')
                            tarifaValor = tarifaValor.replace(" ", '')
                            print ("tarifaValor = ", tarifaValor)

                        else:
                            tarifaValor=0

                        if tarifaValor == None:
                            tarifaValor=0


                        TotalTarifa = float(tarifaValor) * float(cantidadMedicamento)
                        print("consecLiquidacion LISTO= ", consecLiquidacion)

                    # Aqui Rutina FACTURACION crea en liquidaciondetalle el registro con la tarifa, con campo cups y convenio
                    #

                        if (medicamentosId.requiereAutorizacion == 'N'):
                            pass

                            #miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",                                       password="123456")
                            #curt = miConexiont.cursor()
                            # Aqui INSERT A FARMACIA

                            #comando = 'INSERT INTO facturacion_liquidaciondetalle (consecutivo,fecha, cantidad, "valorUnitario", "valorTotal",cirugia,"fechaCrea", "fechaRegistro", "estadoRegistro", "cums_id",  "usuarioRegistro_id", liquidacion_id, "tipoRegistro", "historiaMedicamento_id") VALUES (' + "'" +  str(consecLiquidacion)  + "','" + str(fechaRegistro) + "','" + str(cantidadMedicamento) + "','"  + str(tarifaValor) + "','" + str(TotalTarifa)  + "','" + str('N') + "','" +  str(fechaRegistro) + "','" +  str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(medicamentos) + "','" + str(usuarioRegistro) + "'," + liquidacionId + ",'SISTEMA',"  + "'" + str(i.id) + "'" + ')'
                            #print("comando " , comando)

                            #curt.execute(comando)
                            #miConexiont.commit()
                            #miConexiont.close()

                            #consecLiquidacion = int(consecLiquidacion) + 1


	            # Fin rutina Facturacion


                if conteoMed >= 1:
                   print("Entre imprimir Medicamentos")
                   ingresoId2 = ingresosPaciente.id
                   ImprimirOrdenMedicamentos(ingresoId2, historiaId, convenioId, tipoAdmision)



                    #
                ## Vamops a actualizar los totales de la Liquidacion:
                #
                totalSuministros = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(examen_id = None).exclude(estadoRegistro='N').aggregate(totalS=Coalesce(Sum('valorTotal'), 0))
                totalSuministros = (totalSuministros['totalS']) + 0
                print("totalSuministros", totalSuministros)
                totalProcedimientos = LiquidacionDetalle.objects.all().filter(liquidacion_id=liquidacionId).filter(cums_id = None).exclude(estadoRegistro='N').aggregate(totalP=Coalesce(Sum('valorTotal'), 0))
                totalProcedimientos = (totalProcedimientos['totalP']) + 0
                print("totalProcedimientos", totalProcedimientos)
                registroPago = Liquidacion.objects.get(id=liquidacionId)

		    # Continua Aqui

                totalCopagos = Pagos.objects.all().filter(tipoDoc_id=tipoDocId.id).filter(documento_id=documentoId.id).filter(consec=ingresoPaciente).filter(formaPago_id=4).exclude(estadoReg='N').aggregate(totalC=Coalesce(Sum('valor'), 0))
                totalCopagos = (totalCopagos['totalC']) + 0
                print("totalCopagos", totalCopagos)
                totalCuotaModeradora = Pagos.objects.all().filter(tipoDoc_id=tipoDocId.id).filter(documento_id=documentoId.id).filter(consec=ingresoPaciente).filter(formaPago_id=3).exclude(estadoReg='N').aggregate(totalM=Coalesce(Sum('valor'), 0))
                totalCuotaModeradora = (totalCuotaModeradora['totalM']) + 0
                print("totalCuotaModeradora", totalCuotaModeradora)
                totalAnticipos = Pagos.objects.all().filter(tipoDoc_id=tipoDocId.id).filter(documento_id=documentoId.id).filter(consec=ingresoPaciente).filter(formaPago_id=1).exclude(estadoReg='N').aggregate(Anticipos=Coalesce(Sum('valor'), 0))
                totalAnticipos = (totalAnticipos['Anticipos']) + 0
                print("totalAnticipos", totalAnticipos)
                totalAbonos = Pagos.objects.all().filter(tipoDoc_id=tipoDocId.id).filter(documento_id=documentoId.id).filter(consec=ingresoPaciente).filter(formaPago_id=2).exclude(estadoReg='N').aggregate(totalAb=Coalesce(Sum('valor'), 0))
                totalAbonos = (totalAbonos['totalAb']) + 0
                #totalAbonos = totalCopagos + totalAnticipos + totalCuotaModeradora
                print("totalAbonos", totalAbonos)

                totalRecibido = totalCopagos + totalCuotaModeradora + totalAnticipos + totalAbonos
                totalApagar = totalSuministros + totalProcedimientos - totalRecibido
                totalLiquidacion = totalSuministros + totalProcedimientos
                print("totalLiquidacion", totalLiquidacion)
                print("totalAPagar", totalApagar)

                # Rutina Guarda en cabezote los totales

                print ("Voy a grabar el cabezote")
                print ("liquidacionId = ", liquidacionId)

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",                                       password="123456")
                curt = miConexiont.cursor()
                comando = 'UPDATE facturacion_liquidacion SET "totalSuministros" = ' +  "'" +  str(totalSuministros) + "'" + ',"totalProcedimientos" = ' + "'" +  str(totalProcedimientos) + "'"  + ', "totalCopagos" = ' + "'" +  str(totalCopagos) + "'"  + ' , "totalCuotaModeradora" = ' + "'" +  str(totalCuotaModeradora) + "'" + ', anticipos = ' + "'" +  str(totalAnticipos) + "'"  + ' ,"totalAbonos" = ' + "'" + str(totalAbonos) + "'" + ', "totalLiquidacion" = ' + "'" + str(totalLiquidacion) + "'" + ', "valorApagar" = ' + "'" + str(totalApagar) + "'"   + ', "totalRecibido" = ' + "'" + str(totalRecibido) + "'"  + ' WHERE id =' + str(liquidacionId)
                print("COMANDO = " , comando)
                curt.execute(comando)
                miConexiont.commit()
                miConexiont.close()


                ## SALIDA CLINICA
                #
                if (salidaClinica=='S'):

                    miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",    password="123456")
                    cur3 = miConexion3.cursor()
                    comando = 'UPDATE admisiones_ingresos SET "salidaClinica" = ' + "'" + str(salidaClinica) + "'" + ', "dxSalida_id" = ' + "'" + str(diagnosticoIdSalida) + "'" + ', "medicoSalida_id" = ' + "'" + str(plantaId.id) + "'" + ', "especialidadesMedicosSalida_id" = ' + "'" + str(espMedico) + "'" +  ',"serviciosSalida_id" = "serviciosActual_id"  ' + ', "salidaMotivo_id" = ' + "'" + str(tiposSalidas) + "'," + ' "dxComplicacion_id" = ' + "'" + str(dxComplicacion) + "'" +  ' WHERE "tipoDoc_id" =  ' + "'" + str(tipoDocId.id) + "' and documento_id = " + "'" + str(documentoId.id) + "' AND consec = " + "'" + str(ingresoPaciente) + "'"
                    print(comando)
                    cur3.execute(comando)
                    miConexion3.commit()
                    miConexion3.close()

                # Aqui RUTINA CREA Solicitud - Programacion de Cirugia. Ojo hacer filtro por si si o no la cirugia. No es todo mundo

                #postFormCirugiaClinica = request.POST.get("postFormCirugiaClinica")


                cBoxCirugia =   request.POST['cBoxCirugia']
                print("cBoxCirugia =", cBoxCirugia)

                print("cBoxCirugia =", cBoxCirugia)


                if cBoxCirugia == 'true':

                        serviciosAdministrativos = request.POST.get("serviciosAdministrativos")
                        print("serviciosAdministrativos =", serviciosAdministrativos)

                        solicitaSangre = request.POST["solicitaSangre"]
                        print("solicitaSangre =", solicitaSangre)

                        describeSangre = request.POST["describeSangre"]
                        print("describeSangre =", describeSangre)

                        cantidadSangre = request.POST["cantidadSangre"]
                        print("cantidadSangre =", cantidadSangre)

                        solicitaCamaUci = request.POST["solicitaCamaUci"]
                        print("solicitaCamaUci =", solicitaCamaUci)

                        solicitaMicroscopio = request.POST["solicitaMicroscopio"]
                        print("olicitaMicroscopio =", solicitaMicroscopio)

                        solicitaCamaUci = request.POST["solicitaCamaUci"]
                        print("solicitaCamaUci =", solicitaCamaUci)

                        solicitaRx = request.POST["solicitaRx"]
                        print("solicitaRx =", solicitaRx)

                        solicitaCamaUci = request.POST["solicitaCamaUci"]
                        print("solicitaCamaUci =", solicitaCamaUci)

                        solicitaOsteosintesis = request.POST["solicitaOsteosintesis"]
                        print("solicitaOsteosintesis =", solicitaOsteosintesis)
                        solicitaBiopsia = request.POST["solicitaBiopsia"]
                        print("solicitaBiopsia =", solicitaBiopsia)
                        solicitaMalla = request.POST["solicitaMalla"]
                        print("solicitaMalla =", solicitaMalla)
                        solicitaOtros = request.POST["solicitaOtros"]
                        print("solicitaOtros =", solicitaOtros)

                        anestesia = request.POST["anestesia"]
                        print("anestesia =", anestesia)
                        sedesClinica_id = request.POST["sede"]
                        print("sedesClinica_id =", sedesClinica_id)

                        username = request.POST["usuarioRegistro"]
                        print("username =", username)

                        solicitaHospitalizacion = request.POST["solicitaHospitalizacion"]
                        print("solicitaHospitalizacion =", solicitaHospitalizacion)
                        solicitaAyudante = request.POST["solicitaAyudante"]
                        print("solicitaAyudante =", solicitaAyudante)
                        solicitaTiempoQx = request.POST["solicitaTiempoQx"]
                        print("solicitaTiempoQx =", solicitaTiempoQx)

                        solicitaTipoQx = request.POST["solicitaTipoQx"]
                        print("solicitatipoQx =", solicitaTipoQx)
                        solicitaAnestesia = request.POST["solicitaAnestesia"]
                        print("solicitaAnestesia =", solicitaAnestesia)
                        solicitaOtros = request.POST["solicitaOtros"]
                        print("solicitaOtros =", solicitaOtros)
                        tiempoMaxQx = request.POST["tiempoMaxQx"]
                        print("tiempoMaxQx =", tiempoMaxQx)
                        solicitaAutoSutura = request.POST["solicitaAutoSutura"]
                        print("solicitaAutoSutura =", solicitaAutoSutura)

                        solicitaSoporte = request.POST["solicitaSoporte"]
                        print("solicitaSoporte =", solicitaSoporte)

                        describeOtros = request.POST["describeOtros"]
                        print("describeOtros =", describeOtros)

                        #especialidadX = request.POST["especialidadX"]
                        #print("especialidadX =", especialidadX)

                        tiposCirugia = request.POST["tiposCirugia"]
                        print("tiposCirugia =", tiposCirugia)

                        dxPreQx = request.POST["dxPreQx"]
                        print("dxPreQx =", dxPreQx)

                        dxPrinc = request.POST["dxPrinc"]
                        print("dxPrinc =", dxPrinc)

                        dxRel1 = request.POST["dxRel1"]
                        print("dxRel1 =", dxRel1)

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



                        # especialidadId = EspecialidadesMedicos.objects.get(planta_id=username)

                        estadoCirugia = EstadosCirugias.objects.get(nombre='SIN ASIGNAR')
                        estadoProgramacion = EstadosProgramacion.objects.get(nombre='Solicitud')
                        # estadoSala = EstadosSalas.objetcs.get(nombre='OCUPADA')
                        estadoReg = 'A'
                        fechaRegistro = timezone.now()

                        fechaSolicita = datetime.datetime.now()

                        tipoDocCirugia =  request.POST["tipoDocCirugia"]
                        print("tipoDocCirugia =", tipoDocCirugia)
                        documentoCirugia  = request.POST["documentoCirugia"]
                        print("documentoCirugia =", documentoCirugia)
                        consecutivoIngresoCirugia = request.POST["consecutivoIngresoCirugia"]
                        print("consecutivoIngresoCirugia =", consecutivoIngresoCirugia)

                        # Aqui buscar el ingreso del paciente
                        documento_id = Usuarios.objects.get(tipoDoc_id=tipoDocCirugia, documento=documentoCirugia)
                        registroIngreso = Ingresos.objects.get(tipoDoc_id=tipoDocCirugia, documento_id=documento_id.id,
                                                               consec=consecutivoIngresoCirugia)

                        miConexion3 = None
                        try:

                            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432",
                                                           user="postgres", password="123456")
                            cur3 = miConexion3.cursor()

                            comando = 'INSERT INTO cirugia_cirugias ("consecAdmision", "fechaSolicita", "solicitaHospitalizacion", "solicitaAyudante", "solicitaTiempoQx",  "solicitaAnestesia", "solicitaSangre", "describeSangre", "cantidadSangre", "solicitaCamaUci", "solicitaMicroscopio", "solicitaRx", "solicitaAutoSutura", "solicitaOsteosintesis",  "solicitaBiopsia", "solicitaMalla", "solicitaOtros", "describeOtros", "tiempoMaxQx", "fechaRegistro", "estadoReg", anestesia_id, documento_id,  "dxPreQx_id", "dxPrinc_id", "dxRel1_id", especialidad_id, "sedesClinica_id", "tipoDoc_id", "usuarioRegistro_id", "usuarioSolicita_id", "serviciosAdministrativos_id", "estadoProgramacion_id", "tiposCirugia_id","estadoCirugia_id", historia_id) VALUES (' + "'" + str(
                                registroIngreso.consec) + "','" + str(fechaSolicita) + "','" + str(
                                solicitaHospitalizacion) + "','" + str(solicitaAyudante) + "','" + str(
                                solicitaTiempoQx) + "','" + str(solicitaAnestesia) + "','" + str(solicitaSangre) + "','" + str(
                                describeSangre) + "','" + str(cantidadSangre) + "','" + str(solicitaCamaUci) + "','" + str(
                                solicitaMicroscopio) + "','" + str(solicitaRx) + "','" + str(solicitaAutoSutura) + "','" + str(
                                solicitaOsteosintesis) + "','" + str(solicitaBiopsia) + "','" + str(
                                solicitaMalla) + "','" + str(solicitaOtros) + "','" + str(describeOtros) + "','" + str(
                                tiempoMaxQx) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(
                                anestesia) + "','" + str(registroIngreso.documento_id) + "','" + str(dxPreQx) + "','" + str(
                                dxPrinc) + "','" + str(dxRel1) + "','" + str(espMedico) + "','" + str(
                                sedesClinica_id) + "','" + str(registroIngreso.tipoDoc_id) + "','" + str(
                                username) + "','" + str(username) + "','" + str(serviciosAdministrativos) + "','" + str(
                                estadoProgramacion.id) + "','" + str(tiposCirugia) + "','" + str(estadoCirugia.id) + "','" + str(historiaId) + "')"

                            print(comando)
                            cur3.execute(comando)

                            comando2 = 'INSERT INTO cirugia_programacioncirugias ("consecAdmision", "fechaRegistro", "estadoReg", documento_id, "sedesClinica_id", "tipoDoc_id", "usuarioRegistro_id",  "estadoProgramacion_id") values (' + "'" + str(
                                registroIngreso.consec) + "','" + str(fechaRegistro) + "','" + str(estadoReg) + "','" + str(
                                registroIngreso.documento_id) + "','" + str(sedesClinica_id) + "','" + str(
                                registroIngreso.tipoDoc_id) + "','" + str(username) + "','" + str(estadoProgramacion.id) + "')"

                            print(comando2)
                            cur3.execute(comando2)

                            miConexion3.commit()
                            cur3.close()
                            miConexion3.close()



                        except psycopg2.DatabaseError as error:
                            print("Entre por rollback", error)
                            if miConexion3:
                                print("Entro ha hacer el Rollback")
                                miConexion3.rollback()
                            raise error

                        finally:
                            if miConexion3:
                                cur3.close()
                                miConexion3.close()

                # FIN RUTINA CREA Solicitud - Programacion de Cirugia

                # Imprimir OrdenDeControl
                print("ordenDeControl = ", ordenDeControl)

                if (ordenDeControl != ''):

                    print("Entre imprimir orden de control")
                    ingresoId2=ingresosPaciente.id
                    try:
                        ImprimirOrdenDeControl(ingresoId2, historiaId, convenioId, tipoAdmision)
                    except psycopg2.DatabaseError as error:
                        print("Entre por rollback", error)

                        return JsonResponse({'success': False, 'Mensaje': 'Favor cerrar pdf OrdenDeControl'})

                    finally:
                        print("ok")
                print("Ya grabe el cabezote")

                    #data = {'Mensaje': 'Folio exitoso : ' + str(ultimofolio2)}
                data = {'Mensaje': 'OK'}

                return HttpResponse(json.dumps(data))
                #return HttpResponse(data)
                #return HttpResponse('Folio Creado')


    if request.method == "POST":

        alert("Entre por solo POST falta el context");

        context['Mensaje'] = 'Folio de Historia Clinica guardado !'

        return render(request, 'clinico/panelClinico.html', context);

	
    if request.method == "GET":

        print("Entre por GET Crear Historia Clinica")
        context = {}
        context['title'] = 'Mi gran Template'
        context['historiaForm'] = historiaForm
        context['IncapacidadesForm'] = IncapacidadesForm
        context['HistoriaSignosVitalesForm']  = HistoriaSignosVitalesForm

        Sede = request.GET["sede"]
        sede = request.GET["sede"]
        Username = request.GET["username"]
        Username_id = request.GET["username_id"]
        Profesional = request.GET["profesional"]
        EscogeModulo = request.GET["escogeModulo"]

        NombreSede = request.GET["nombreSede"]
        TipoDocPaciente = request.GET["nombreTipoDoc"]
        DocumentoPaciente = request.GET["documento2"]
        IngresoPaciente = request.GET["consec"]
        EspMedico = request.GET["espMedico"]
        TiposFolioEscogido = request.GET['tiposFolio']
        DocumentoId = request.GET["documentoId"]

        print("especialidad Medico = ", EspMedico)
        print("TipoDocPaciente = ", TipoDocPaciente)
        print("DocumentoPaciente = ", DocumentoPaciente)
        print("IngresoPaciente = ", IngresoPaciente)


        TipoIng = request.GET["tipoIng"]
        print("TipoIng = ", TipoIng )



        print("Sede = ", Sede)

        print("Username = ", Username)

        context['Sede'] = Sede
        context['Username'] = Username
        context['Username_id'] = Username_id
        context['Profesional'] = Profesional
        context['EscogeModulo'] = EscogeModulo

        context['NombreSede'] = NombreSede
        context['TipoDocPaciente'] = TipoDocPaciente
        context['DocumentoPaciente'] = DocumentoPaciente
        context['IngresoPaciente'] = IngresoPaciente
        context['EspMedico'] = EspMedico
        context['TiposFolioEscogido'] = TiposFolioEscogido

        # Combo Tipos Diagnostico

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT t.id id, t.nombre  nombre FROM clinico_tiposDiagnostico t"

        curt.execute(comando)
        print(comando)

        tiposDiagnostico = []
        tiposDiagnostico.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDiagnostico.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDiagnostico)

        context['TiposDiagnostico'] = tiposDiagnostico

        # Fin combo Tipos Diagnostico

        # Combo Diagnostico

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM clinico_diagnosticos p"

        curt.execute(comando)
        print(comando)

        diagnosticos = []
        diagnosticos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            diagnosticos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(diagnosticos)

        context['Diagnosticos'] = diagnosticos

        # Fin combo Diagnosticos

        # Combo Especialidades

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT e.id id, e.nombre  nombre FROM clinico_especialidades e"

        curt.execute(comando)
        print(comando)

        especialidades = []
        especialidades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidades)

        context['Especialidades'] = especialidades

        # Fin combo Especialidades

        # Combo TiposFolio

        #miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
        #                               password="123456")
        #curt = miConexiont.cursor()

        #comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

        #curt.execute(comando)
        #print(comando)

        #tiposFolio = []
        #tiposFolio.append({'id': '', 'nombre': ''})

        #for id, nombre in curt.fetchall():
        #    tiposFolio.append({'id': id, 'nombre': nombre})

        #miConexiont.close()
        #print(tiposFolio)

        #context['TiposFolio'] = tiposFolio

        # Fin combo TiposFolio

        # Combo Laboratorios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT t.id TipoId, e.id id, e.nombre nombre , e."codigoCups" cups FROM clinico_tiposExamen t, clinico_examenes e WHERE t.id = e."TiposExamen_id" and t.nombre = ' + "'" + str(
            'LABORATORIO') + "'"
        curt.execute(comando)
        print(comando)

        laboratorios = []
        laboratorios.append({'TipoId': '', 'id': '', 'nombre': '', 'cups': ''})

        for TipoId, id, nombre, cups in curt.fetchall():
            laboratorios.append({'TipoId': TipoId, 'id': id, 'nombre': nombre, 'cups': cups})

        miConexiont.close()
        print(laboratorios)

        context['Laboratorios'] = laboratorios
        context['TipoExamenLab'] = '1'

        # Fin combo Laboratorios

        # Combo Radiologia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        # comando = "SELECT t.id TipoId, e.id id, e.nombre nombre FROM clinico_tiposExamen t, clinico_examenes e WHERE t.id = e.TiposExamen_id and t.id ='1'"
        comando = 'SELECT t.id TipoId, e.id id, e.nombre nombre , e."codigoCups" cups FROM clinico_tiposExamen t, clinico_examenes e WHERE t.id = e."TiposExamen_id" and t.nombre = ' + "'" + str(
            'RADIOLOGIA') + "'"

        curt.execute(comando)
        print(comando)

        radiologias = []
        radiologias.append({'TipoId': '', 'id': '', 'nombre': '', 'cups': ''})

        for TipoId, id, nombre, cups in curt.fetchall():
            radiologias.append({'TipoId': TipoId, 'id': id, 'nombre': nombre, 'cups': cups})

        miConexiont.close()
        print(radiologias)

        context['Radiologias'] = radiologias
        context['TipoExamenRad'] = '3'

        # Fin combo Radiologia

        # Datos Basicos del Paciente


        print("especialidad Medico = ", EspMedico)
        print("TipoDocPaciente = ", TipoDocPaciente)
        print("DocumentoPaciente = ", DocumentoPaciente)
        print("IngresoPaciente = ", IngresoPaciente)
        print("DocumentoId = ", DocumentoId)


        filaTipoDoc = TiposDocumento.objects.get(nombre=TipoDocPaciente)
        print("id tipodoc = " , filaTipoDoc.id)
        print("nombre tipodoc = ", filaTipoDoc.nombre)

        fila = Usuarios.objects.get(tipoDoc_id=filaTipoDoc.id, documento=DocumentoPaciente)
        print("OJO LOS DATOS DESNORMALIOZADOS")

        print(fila.documento)

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",   password="123456")
        curt = miConexiont.cursor()
        if (TipoIng == 'INGRESO'):
            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str('M') + "'" + ' then ' + "'" + str("Masculino") + "'" + ' when genero= ' + "'" + str('F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, cen.nombre as centro, tu.nombre as tipoUsuario,"fechaNacio", u.direccion direccion, u.telefono telefono from usuarios_usuarios u, usuarios_tiposUsuario tu, sitios_centros cen, usuarios_tiposDocumento tip where tip.id = u."tipoDoc_id"  AND u."tipoDoc_id" = ' +"'" + str(filaTipoDoc.id) + "'" + ' and u.documento = ' + "'" + str(fila.documento) + "'" + ' and u."tiposUsuario_id" = tu.id and u."centrosC_id" = cen.id'
        else:
            comando = 'select  u."tipoDoc_id" , tip.nombre tipnombre, documento documentoPaciente, u.nombre nombre, case when genero = ' + "'" + str('M') + "'" + ' then ' + "'" + str("Masculino") + "'" + ' when genero= ' + "'" + str('F') + "'" + ' then ' + "'" + str('Femenino') + "'" + ' end as genero, cen.nombre as centro, tu.nombre as tipoUsuario,"fechaNacio", u.direccion direccion, u.telefono telefono from usuarios_usuarios u, usuarios_tiposUsuario tu, sitios_centros cen, usuarios_tiposDocumento tip where tip.id = u."tipoDoc_id"  AND u."tipoDoc_id" = ' +"'" + str(filaTipoDoc.id) + "'" + ' and u.documento = ' + "'" + str(fila.documento) + "'" + ' and u."tiposUsuario_id" = tu.id and u."centrosC_id" = cen.id'


        curt.execute(comando)
        print(comando)

        datosPaciente = []

        for tipoDoc_id, tipnombre, documentoPaciente, nombre, genero, centro, tipoUsuario, fechaNacio, direccion, telefono in curt.fetchall():
            datosPaciente.append(
                {'tipoDoc_id': tipoDoc_id, 'tipnombre': tipnombre, 'documentoPaciente': documentoPaciente,
                 'nombre': nombre, 'genero': genero, 'centro': centro, 'tipoUsuario': tipoUsuario, 'fechaNacio': fechaNacio, 'direccion': direccion,'telefono': telefono})

        miConexiont.close()
        print("OJO ESTOS SON LOS DAOS DEL PACIENTE SELECCIONAO")

        print(datosPaciente)

        context['DatosPaciente'] = datosPaciente
        context['TipoIng'] = TipoIng

        # Combo Fin Datos BAsicos paciente

        # Combo DependenciasRealizado

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        # 3 = Consultorios Verificar

        comando = 'SELECT d.id id, d.nombre nombre FROM sitios_dependenciasTipo d '

        curt.execute(comando)
        print(comando)

        dependenciasRealizado = []
        # dependenciasRealizado.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            dependenciasRealizado.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(dependenciasRealizado)

        context['DependenciasRealizado'] = dependenciasRealizado

        # Fin Combo DependenciasRealizado

        # Combo causasExterna

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT d.id id, d.nombre nombre FROM clinico_causasExterna d "
        curt.execute(comando)
        print(comando)

        causasExterna = []
        causasExterna.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            causasExterna.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(causasExterna)

        context['CausasExterna'] = causasExterna

        # Fin Combo causasExterna

        # Combo Tiposantecedentes

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT id,  nombre FROM clinico_tiposAntecedente  "

        curt.execute(comando)
        print(comando)

        tiposAntecedente = []
        tiposAntecedente.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposAntecedente.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposAntecedente)

        context['TiposAntecedente'] = tiposAntecedente

        # Fin Combo Tiposantecedentes


        # Combo Terapias

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        # comando = "SELECT t.id TipoId, e.id id, e.nombre nombre FROM clinico_tiposExamen t, clinico_examenes e WHERE t.id = e.TiposExamen_id and t.id ='3'"
        comando = 'SELECT t.id TipoId, e.id id, e.nombre nombre , e."codigoCups" cups FROM clinico_tiposExamen t, clinico_examenes e WHERE t.id = e."TiposExamen_id" and t.nombre = ' + "'" + str(
            'TERAPIAS') + "'"

        curt.execute(comando)
        print(comando)

        terapias = []
        terapias.append({'TipoId': '', 'id': '', 'nombre': '', 'cups': ''})

        for TipoId, id, nombre, cups in curt.fetchall():
            terapias.append({'TipoId': TipoId, 'id': id, 'nombre': nombre, 'cups': cups})

        miConexiont.close()
        print(terapias)

        context['Terapias'] = terapias
        context['TipoExamenTer'] = '2'

        # Fin combo Terapias

        # Combo No Qx

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT t.id TipoId, e.id id, e.nombre nombre , e."codigoCups" cups FROM clinico_tiposExamen t, clinico_examenes e WHERE t.id = e."TiposExamen_id" and t.nombre = ' + "'" + str(
            'PROCEDIMIENTOS NO QX') + "'"

        curt.execute(comando)
        print(comando)

        noQx = []
        noQx.append({'TipoId': '', 'id': '', 'nombre': '', 'cups': ''})

        for TipoId, id, nombre, cups in curt.fetchall():
            noQx.append({'TipoId': TipoId, 'id': id, 'nombre': nombre, 'cups': cups})

        miConexiont.close()
        print(noQx)

        context['NoQx'] = noQx
        context['TipoExamenProcNoQx'] = '4'

        # Fin combo No Qx

        # Combo Antecedentes

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM clinico_tiposAntecedente e'

        curt.execute(comando)
        print(comando)

        antecedentes = []
        antecedentes.append({'id': '', 'nombre': ''})

        for  id, nombre in curt.fetchall():
            antecedentes.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(antecedentes)

        context['Antecedentes'] = antecedentes

        # Fin combo Antecednetes

        # Combo TipoInterconsulta

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM clinico_tiposInterconsulta e'

        curt.execute(comando)
        print(comando)

        tiposInterconsulta = []
        tiposInterconsulta.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposInterconsulta.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposInterconsulta)

        context['TiposInterconsulta'] = tiposInterconsulta

        # Fin combo TipoInterconsulta

        # Combo Medicos
        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT med.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(
            Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str('MEDICO') + "'" + ' and med.planta_id = p.id'

        curt.execute(comando)
        print(comando)

        medicos = []
        medicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            medicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicos)

        context['Medicos'] = medicos

        # Fin combo Medicos


        # Combo RevisionSistemas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM clinico_RevisionSistemas e'

        curt.execute(comando)
        print(comando)

        revisionSistemas = []
        revisionSistemas.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            revisionSistemas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(revisionSistemas)

        context['RevisionSistemas'] = revisionSistemas

        # Fin combo RevisionSistemas


        # Combo Medicamentos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM facturacion_Suministros e, facturacion_tipossuministro t  where e."tipoSuministro_id" = t.id AND t.nombre = ' + "'" + str('MEDICAMENTOS') + "' ORDER BY e.nombre"

        curt.execute(comando)
        print(comando)

        medicamentos = []
        medicamentos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            medicamentos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(medicamentos)

        context['Medicamentos'] = medicamentos

        # Fin combo medicamentos


       # Combo UMedidaDosis

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.descripcion nombre  FROM clinico_unidadesdemedidadosis e'

        curt.execute(comando)
        print(comando)

        uMedidaDosis= []
        uMedidaDosis.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            uMedidaDosis.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(uMedidaDosis)

        context['UMedidaDosis'] = uMedidaDosis

        # Fin combo UMedidaDosis


       # Combo formaFarma

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM clinico_formasfarmaceuticas e' 

        curt.execute(comando)
        print(comando)

        formaFarma= []
        formaFarma.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            formaFarma.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(formaFarma)

        context['FormaFarma'] = formaFarma

        # Fin combo formaFarma


       # Combo forfrecuencias Farmaceuticas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.descripcion nombre  FROM clinico_frecuenciasaplicacion  e'

        curt.execute(comando)
        print(comando)

        frecuencia= []
        frecuencia.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            frecuencia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(frecuencia)

        context['Frecuencia'] = frecuencia

        # Fin combo frecuencia farmaceuticas

        # Combo Vias Administracion

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM clinico_viasAdministracion c"

        curt.execute(comando)
        print(comando)

        viasAdministracion = []

        for id, nombre in curt.fetchall():
            viasAdministracion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(viasAdministracion)

        context['ViasAdministracion'] = viasAdministracion

        # Fin combo Vias Administracion

        # Combo TiposSalidas


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",   password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT e.id ,e.nombre FROM clinico_TiposSalidas e'
        curt.execute(comando)
        print(comando)

        tiposSalidas = []
        tiposSalidas.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
             tiposSalidas.append({'id': id, 'nombre': nombre})

        miConexiont.close()

        print(tiposSalidas)

        context['TiposSalidas'] = tiposSalidas

        print ("tiposSalidas =", tiposSalidas)

        # FIN Combo TipopsSalidas



        # Combo Dx Complicacion


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",   password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT e.id ,e.nombre FROM clinico_Diagnosticos e'
        curt.execute(comando)
        print(comando)

        dxComplicacion = []
        dxComplicacion.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
             dxComplicacion.append({'id': id, 'nombre': nombre})

        miConexiont.close()

        print(dxComplicacion)

        context['DxComplicacion'] = dxComplicacion

        print ("dxComplicacion =", dxComplicacion)

        # FIN Combo Dx Complicacion



        print ("tiposFolio = " ,TiposFolio)

   	# Combo tiposAnestesia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM  cirugia_tiposanestesia  p"

        curt.execute(comando)
        print(comando)

        tiposAnestesia = []


        for id, nombre in curt.fetchall():
            tiposAnestesia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tiposAnestesia", tiposAnestesia)

        context['TiposAnestesia'] = tiposAnestesia

        # Fin combo tiposAnestesia


   	# Combo tiposCirugia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM  cirugia_tiposcirugia  p"

        curt.execute(comando)
        print(comando)

        tiposCirugia = []


        for id, nombre in curt.fetchall():
            tiposCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tiposCirugia", tiposCirugia)

        context['TiposCirugia'] = tiposCirugia

        # Fin combo tiposCirugia

	# Combo diagnosticos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM  clinico_diagnosticos  p"

        curt.execute(comando)
        print(comando)

        diagnosticosCirugia = []


        for id, nombre in curt.fetchall():
            diagnosticosCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("diagnosticosCirugia", diagnosticosCirugia)

        context['DiagnosticosCirugia'] = diagnosticosCirugia

        # Fin combo diagnosticosCirugia

        # Combo ServiciosAdministrativos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select m.id id, m.nombre||' + "'" + str(' ') + "'||" + ' u.nombre nombre FROM sitios_serviciosAdministrativos m, sitios_ubicaciones u where m.ubicaciones_id= u.id AND m."sedesClinica_id" = ' + str(sede)

        print(comando)
        curt.execute(comando)

        serviciosAdministrativos = []

        for id, nombre in curt.fetchall():
            serviciosAdministrativos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ServiciosAdministrativos = " , serviciosAdministrativos)
        context['ServiciosAdministrativos'] = serviciosAdministrativos

        # Fin Combo ServiciosAdministrativos

        return render(request, 'clinico/navegacionClinicaF.html', context);



def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 



# Create your views here.
def load_dataClinico(request, data):
    print ("Entre load_data Admisiones")

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

    # Combo Indicadores

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()


    comando = 'SELECT ser.nombre nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = sd.id AND dep.disponibilidad = ' + "'" + str('O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = '  + "'" + str('TRIAGE') + "'" + ' group by ser.nombre'

    curt.execute(comando)
    print(comando)

    indicadores = []

    for nombre, total in curt.fetchall():
        indicadores.append({'nombre': nombre, 'total':total})
        if (nombre == 'HOSPITALIZACION' ):
            context['Hospitalizados'] = total
        if (nombre == 'TRIAGE'):
            context['Triage'] = total
        if (nombre == 'URGENCIAS'):
            context['Urgencias'] = total
        if (nombre == 'AMBULATORIO'):
            context['Ambulatorios'] = total

    miConexiont.close()
    print(indicadores)

    context['Indicadores'] = indicadores

    total = len(indicadores)

    print ("total ", total)

    print("YA PASE INDICADORES")

# Fin combo Indicadores



    ingresos = []

    # miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",     password="123456")
    curx = miConexionx.cursor()
   

    detalle = 'SELECT ' + "'" + str("INGRESO") + "'" +  ' tipoIng, i.id'  + "||" +"'" + '-INGRESO' + "'" + ' id, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual, i."salidaClinica" salidaClinica FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = sd.id AND (dep.disponibilidad= ' + "'" + str('O') + "'" + ' OR (dep.disponibilidad = ' + "'" + str('L') + "'" + ' AND ser.id=3)) AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id" UNION SELECT ' + "'"  + str("TRIAGE") + "'" + ' tipoIng, t.id'  + "||" +"'" + '-TRIAGE' + "'" + ' id, tp.nombre tipoDoc,u.documento documento,u.nombre nombre,t.consec consec , t."fechaSolicita" , cast(' + "'" + str('0001-01-01 00:00:00') + "'" + ' as timestamp) fechaSalida,ser.nombre servicioNombreIng, dep.nombre camaNombreIng , ' + "''" + ' dxActual, ' + "' '" + ' salidaClinica FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  ,sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND t."sedesClinica_id" = ' "'" + str(sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str('TRIAGE') + "'"

    print(detalle)

    curx.execute(detalle)

    for tipoIng, id, tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual, salidaClinica in curx.fetchall():
        ingresos.append(
		{"model":"ingresos.ingresos","pk":id,"fields":
			{'tipoIng':tipoIng, 'id':id, 'tipoDoc': tipoDoc, 'documento': documento, 'nombre': nombre, 'consec': consec,
                         'fechaIngreso': fechaIngreso, 'fechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'dxActual': dxActual, 'salidaClinica':salidaClinica}})

    miConexionx.close()
    print(ingresos)
    context['Ingresos'] = ingresos


    serialized1 = json.dumps(ingresos, default=serialize_datetime)

    print ("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')


def PostConsultaHcli(request):
    print ("Entre PostConsultaHcli ")


    Post_id = request.POST["post_id"]

    print("id = ", Post_id)
    llave = Post_id.split('-')
    print ("llave = " ,llave)
    print ("primero=" ,llave[0])
    print("segundo = " ,llave[1])


    if request.method == 'POST':


        # Abro Conexion

        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner6", port="5432", user="postgres",password="123456")
        cur = miConexionx.cursor()

        if (llave[1].strip() == 'INGRESO'):
            comando = 'SELECT i.id id, i."tipoDoc_id" tipoDocId,td.nombre nombreTipoDoc, i.documento_id documentoId, u.documento documento , i.consec consec FROM admisiones_ingresos i, usuarios_usuarios u, usuarios_tiposDocumento td where i.id=' + "'" +  str(llave[0].strip()) + "'" + ' and i."tipoDoc_id" =td.id and i.documento_id=u.id'
        else:
            comando = 'SELECT t.id id, t."tipoDoc_id" tipoDocId,td.nombre nombreTipoDoc, t.documento_id documentoId, u.documento documento , t.consec consec FROM triage_triage t, usuarios_usuarios u, usuarios_tiposDocumento td where t.id=' + "'" + str(llave[0].strip()) + "'" + ' and t."tipoDoc_id" =td.id and t.documento_id=u.id'

        print(comando)

        cur.execute(comando)

        hc = []

        for id, tipoDocId, nombreTipoDoc, documentoId, documento, consec in cur.fetchall():
            hc.append( {"id": id,
                     "tipoDocId": tipoDocId,
                     "nombreTipoDoc": nombreTipoDoc,
                     "documentoId": documentoId, "documento": documento,
                     "consec": consec  })

        miConexionx.close()
        print(hc)

        # Cierro Conexion

        return JsonResponse({'pk':hc[0]['id'],'tipoDocId':hc[0]['tipoDocId'],'nombreTipoDoc':hc[0]['nombreTipoDoc'],
                             'documentoId':hc[0]['documentoId'],  'documento': hc[0]['documento'],
                             'consec': hc[0]['consec']})

    else:
        return JsonResponse({'errors':'Something went wrong!'})