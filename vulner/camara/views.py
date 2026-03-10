from django.shortcuts import render

# Create your views here.

import numpy as np
import cv2
import uuid
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import os
import speech_recognition as sr
import time
import json
import pyttsx3
import MySQLdb
import pyodbc



def camara(request):
    print("Entre Camara")
    cap= cv2.VideoCapture(0)

  #  while(True):
    ret , frame = cap.read()

    if ret:
            archivo=request.GET["nombre"]
            nombre_foto = archivo + ".jpg"
            cv2.imshow('Visor Familia Camacho', frame)
         #   cv2.imwrite( nombre_foto, frame)
            path = 'c:/EntornosPython/practica8/vulner/vulner/usuarios/static/usuarios'
            cv2.imwrite(os.path.join(path, nombre_foto), frame)
            datos = {"nombre": nombre_foto, "mensaje": " Fotografia tomada correctamente "}

            print("Foto tomada correctamente con el nombre {}".format(nombre_foto))
    else:
        datos = {"nombre": nombre_foto, "mensaje": "Error al acceder a la cámara"}
        print("Error al acceder a la cámara")



 #       if cv2.waitKey(1) & 0xFF == ord('q'):
 #           break
    print("chao")
    cap.release()
    cv2.destroyAllWindows()

    return HttpResponse(json.dumps(datos))

def menu(request):
    print("Ingreso a menu")
    return render(request, "home1.html")


def admHospProvisional(request,Documento, Perfil, Sede, NombreSede, Servicio):
    print("admHospProvisional")
    print(Documento)
    context = {}
    context['Documento'] = Documento
    context['Perfil'] = Perfil
    context['Sede'] = Sede
    context['NombreSede'] = NombreSede
    context['Servicio'] = Servicio




    return render(request, "admisiones/panelHospAdmisiones.html", context)

def acceso(request):
    print("Ingreso a acceso")
    return render(request, "home.html")





def accesoEspecialidadMedico(request, documento):
    print("Ingreso a acceso")
    print ("el medico es")
    print (documento)

    miConexion = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=CMKSISTEPC07\MEDICALL;DATABASE=vulnerable ;UID=sa;pwd=75AAbb??')
    cur = miConexion.cursor()
    comando = "select e.id id ,e.nombre nombre from clinico_especialidadesmedicos c, clinico_especialidades e , planta_planta p where p.documento = '" + documento + "' AND c.id_medico_id=p.id and c.id_especialidad_id=e.id"
    cur.execute(comando)
    print(comando)

    perfiles = []
    context = {}

    for id, nombre in cur.fetchall():
        perfiles.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(perfiles)

    context['Perfiles'] = perfiles
    context['documento'] = documento

    return render(request, "accesoEspecialidadMedico.html", context)






def contrasena(request, documento):

    print("Entre cambio contrasena")
    print(documento)








def reconocerAudio(request):
    print ("Entre a Reconocer audio")
    r = sr.Recognizer()
    print(sr.Microphone.list_microphone_names())

    with sr.Microphone(device_index=0) as source:  # use the default microphone as the audio source
        print("Speak Please")

        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)  # listen for the first phrase and extract it into audio data
        print ("pase")
    try:
            print("No haga nada")
            # print("You said " + r.recognize_google(audio , language = 'en-IN', show_all = True))  # recognize speech using Google Speech Recognition
            #text = r.recognize_google(audio, language = 'es-CO', show_all = True )
            text = r.recognize_google(audio,language = 'es-CO', show_all=True)
            print('You said: {}'.format(text))
            frutas = text.keys()
            print(frutas)

            for info in frutas.keys():
                print(info)



    except LookupError:  # speech is unintelligible
               print("Could not understand audio")

    return render(request, "home.html")


def leeAudio(request):
    print("Entre a leer audio")

    r = sr.Recognizer()
    with sr.WavFile("test.wav") as source:  # use "test.wav" as the audio source
     audio = r.record(source)  # extract audio data from the file

    try:
      print("Transcription: " + r.recognize_google(audio))  # recognize speech using Google Speech Recognition
    except LookupError:  # speech is unintelligible
      print("Could not understand audio")

    return render(request, "home.html")

def reproduceAudio(request):

    print ("Entre al Audio")
    engine = pyttsx3.init()
    engine.setProperty("rate",150)
    texto = request.GET["nombre"]
    engine.say(texto)
    engine.runAndWait()

    return redirect('/menu/')





