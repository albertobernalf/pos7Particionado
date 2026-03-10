from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, CreateView, TemplateView, View
import pygame.mixer
from pygame.mixer import Sound

#from signal import pause

# Create your views here.

from gpiozero import LED, Button

from time import sleep

led = LED(17)


class manejoLuz(TemplateView):
        print("Entre luzHabitacion")
        template_name = 'luzHabitacion.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Mi Inicio'

            context['info'] = ""
            context['infoA'] = ""

            return context

        def post(self, request, *args, **kwargs):
            print("Entre POST manejoLuz")

            luz = request.POST.get('luz');

            print(luz)
            context = {}

            if (luz == 'E'):
                led.on()
                context['info'] = "Encendido"
                context['infoA'] = ""

            if (luz == 'A'):
                led.off()
                context['infoA'] = "Apagado"
                context['info'] = ""


            return render(request, "luzHabitacion.html", context)


class ambienteMusical(TemplateView):
    print("Entre ambienteMusical")
    template_name = 'ambienteMusical.html'

    def get_context_data(self, **kwargs):


        boton1 = Button(3)

        context = super().get_context_data(**kwargs)
        context['title'] = 'Mi Inicio'

        context['info1'] = ""
        context['info2'] = ""
        context['info3'] = ""
        pygame.init()
        pygame.mixer.init()

        return context

    def post(self, request, *args, **kwargs):
        print("Entre POST manejoLuz")

        musica = request.POST.get('musica');

        print(musica)
        context = {}

        if (musica == 'M1'):
            print("Entre Suena boton1)")
            pygame.init()
            pygame.mixer.init()

            boton1 = Sound("/home/pi/EntornosPython/vulne/lib/python3.7/site-packages/pygame/examples/data/car_door.wav")
            print("Voy a sonar")

            pygame.mixer.music.load('/home/pi/EntornosPython/vulne/lib/python3.7/site-packages/pygame/examples/data/car_door.wav')
            pygame.mixer.music.play()
            sonido_fondo = pygame.mixer.Sound("/home/pi/EntornosPython/vulne/lib/python3.7/site-packages/pygame/examples/data/car_door.wav")
            pygame.mixer.Sound.play(sonido_fondo, -1)



            #while pygame.mixer.music.get_busy() == True:
               # continue





            #pygame.mixer.music.play(loops=-1)


            boton1.play()
            print ("ya sone")
            context['info1'] = "Musica_1"
            context['info2'] = ""
            context['info3'] = ""

        if (musica == 'M2'):

            context['info1'] = ""
            context['info2'] = "Musica_2"
            context['info3'] = ""

        if (musica == 'M3'):

             context['info1'] = ""
             context['info2'] = ""
             context['info3'] = "Musica_3"

        return render(request, "ambienteMusical.html", context)