from django.shortcuts import render
import MySQLdb
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from .forms import crearAdmisionForm
from admisiones.models import Ingresos
from django.db.models import Max
from django.db.models.functions import Cast, Coalesce
import pyodbc
import psycopg2
from datetime import datetime
from decimal import Decimal
from django.db.models import Avg, Max, Min, Sum
import pytz
import tzlocal
# import datetime as dt
from admisiones.models import Ingresos, Furips
from admisiones.forms import furipsForm
from sitios.models import  HistorialDependencias, Dependencias, ServiciosSedes, SubServiciosSedes
from usuarios.models import Usuarios, TiposDocumento
from planta.models import Planta
from facturacion.models import ConveniosPacienteIngresos, Liquidacion, LiquidacionDetalle
from rips.models import  RipsDestinoEgreso
from cartera.models import FormasPagos, PagosFacturas, Pagos, TiposPagos, Caja
from autorizaciones.models import EstadosAutorizacion, Autorizaciones, AutorizacionesDetalle
import datetime
from django.utils import timezone
from clinico.models import Servicios,EspecialidadesMedicos, Medicos
from django.db import transaction, IntegrityError
from django.db.models import Q
from admisiones.viewsReportes import ImprimirAtencionUrgencias, ImprimirHojaAdmision, ImpresionManilla
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.db.models import F
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.db.models import F
from tarifarios.models import TiposHonorarios


# Create your views here.

def menuAcceso(request):
    print("Ingreso a acceso")

    #miConexion = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)
    context = {}
    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    return render(request, "inicio/accesoPrincipal1.html", context)

def validaAcceso(request):
    print("Hola Entre a validar el acceso Principal")

    context = {}
    username = request.POST["username"].strip()
    print("username = ", username)
    contrase = request.POST["password"]
    print("contrasena=", contrase)
    sede = request.POST["seleccion2"]
    Sede = sede
    print("Sede Mayuscula = ", Sede)
    print(contrase)
    print("sede= ", sede)
    context = {}
    context['Documento'] = username
    context['Username'] = username
    context['Sede'] = sede

    # Variables que tengo en context : Documento, Perfil , Sede,   sedes ,NombreSede

    print (context['Documento'])

    # Consigo la sede Nombre

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id, nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for id, nombre  in cur.fetchall():
        nombreSede.append({'id':id , 'nombre' : nombre})

    miConexion.close()
    print("ESTA ES EL NOMBRE DE LA SEDE :")
    print (nombreSede[0]['nombre'])

    context['NombreSede'] =  nombreSede[0]['nombre']

    # esta consulta por que se pierde de otras pantallas

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    miConexion0 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur0 = miConexion0.cursor()
    comando = 'select p.id  Username_id , p.nombre profesional , p."sedesClinica_id" , p.contrasena contrasena from planta_planta p where p.documento = ' + "'"  + username + "'" + ' AND p."sedesClinica_id" = ' + "'" + str(sede) + "'"
    cur0.execute(comando)
    print(comando)
    planta = []
    profesional = ''

    for Username_id, profesional, sedesClinica_id , contrasena in cur0.fetchall():
        planta.append({'Username_id': Username_id, 'profesional': profesional, 'sedesClinica_id': sedesClinica_id, 'contrasena':contrasena})
        context['Username_id'] = Username_id
        profesional = profesional

    context['Profesional'] = profesional
    print ("Profesional = ", context['Profesional'] )
    miConexion0.close()
    print("planta =", planta)

    if planta == []:

        context['Error'] = "Personal invalido ! "
        print("Entre por personal No encontrado")
        return render(request, "inicio/accesoPrincipal1.html", context)

    else:

        miConexion1 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        cur1 = miConexion1.cursor()
        comando = "select p.contrasena contrasenax from planta_planta p where p.documento ='" + username + "'" + " AND contrasena = '" + contrasena +"'"
        cur1.execute(comando)

        plantaContrasena = []

        for contrasenax in cur1.fetchall():
            plantaContrasena.append({'contrasenax': contrasenax})

        print ("plantaContrasena[0]['contrasenax'] = ", plantaContrasena[0]['contrasenax'])
        contrasenax = str(plantaContrasena[0]['contrasenax'])
        contrasenax = contrasenax.replace("(", ' ')
        contrasenax = contrasenax.replace(")", ' ')
        contrasenax = contrasenax.replace("'", ' ')
        contrasenax = contrasenax.replace(",", ' ')
        contrasenax=contrasenax.strip()
        print ("contrasenax = ", contrasenax)
        print("contrase = ", contrase)

        if (contrasenax != contrase.strip()):
	        #if plantaContrasena == []:
            #miConexion1.close()
            print("Entre contraseña invalida")
            context['Error'] = "Contraseña invalida ! "
            return render(request, "inicio/accesoPrincipal1.html", context)
        else:
            print("OJOOO CONTRASENA ok")
            #Aqui ya se valido username y contraseña OK

            miConexion2 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
            cur2 = miConexion2.cursor()
            comando =  'select perfcli.id perfil1 from seguridad_perfilesgralusu gral, sitios_sedesClinica sedes, seguridad_perfilesclinica perfcli, planta_planta planta where planta."sedesClinica_id" = sedes.id and planta.id=gral."plantaId_id" and perfcli.id = gral."perfilesClinicaId_id" and sedes.id = ' + "'" +  str(sede) + "'" +   ' AND  planta.documento = ' + "'" + str(username) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"
            print(comando)
            cur2.execute(comando)

            perfil = []

            for perfil1 in cur2.fetchall():
                perfil.append({'perfil1': perfil1})
                
            print ("OJOOO esto es perfil", perfil)
            miConexion2.close()

            if perfil == []:

                print ("Entre Perfil No autorizado para la sede!")
                context['Error'] = "Perfil No autorizado para la sede! "
                return render(request, "inicio/accesoPrincipal1.html", context)

            else:

                # Combo Modulos

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
                curt = miConexiont.cursor()

                comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

                curt.execute(comando)
                print(comando)

                modulos = []

                for id, nombre, nomenclatura, logo in curt.fetchall():
                    modulos.append({'id': id, 'nombre': nombre,'nomenclatura':nomenclatura, 'logo':logo})

                miConexiont.close()
                print(modulos)

                context['Modulos'] = modulos

                # Fin combo Modulos

                # Combo PermisosGrales

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
                curt = miConexiont.cursor()

                comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(username) + "'" + ' and planta."sedesClinica_id" =' + "'" + str(sede) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

                curt.execute(comando)
                print(comando)

                permisosGrales = []

                for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
                    permisosGrales.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo,'modulo_id':modulo_id, 'modulo_nombre':modulo_nombre })

                miConexiont.close()
                print(permisosGrales)

                context['PermisosGrales'] = permisosGrales

                # Fin Combo PermisosGrales

                # Combo PermisosDetalle

                miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
                curt = miConexiont.cursor()

                comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'"  + username + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

                curt.execute(comando)
                print(comando)

                permisosDetalle = []

                for id, nombre, nomenclatura, logo , nombreOpcion , nombreElemento in curt.fetchall():
                    permisosDetalle.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion':nombreOpcion, 'nombreElemento':nombreElemento})

                miConexiont.close()
                print(permisosDetalle)

                context['PermisosDetalle'] = permisosDetalle

                # Fin Combo PermisosDetalle

                print (perfil[0])

    return render(request, "inicio/PantallaPrincipal.html", context)


def escogeAcceso(request, Sede, Username, Profesional, Documento, NombreSede, escogeModulo ):
    print ("Entre Escoge Acceso")

    username = Username
    username = username.strip()
    sede = Sede
    profesional = Profesional
    documento = Documento
    nombreSede = NombreSede
    escogeModulo = escogeModulo

    print("username = ", username)
    print("sede= ", sede)
    print("escogeModulo= ", escogeModulo)
    print("documento= ", documento)
    print("nombreSede= ", nombreSede)
    print("profesional= ", profesional)

    ## username_id
    usernameLlave = Planta.objects.get(documento=username.strip() , sedesClinica_id=sede)
    username_id= usernameLlave.id

    # Combo PermisosGrales

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(username) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

    curt.execute(comando)
    print(comando)

    permisosGrales = []

    for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
        permisosGrales.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
             'modulo_nombre': modulo_nombre})

    miConexiont.close()
    print(permisosGrales)

    # Fin Combo PermisosGrales

    print("permisosGrales= ", permisosGrales)

    context = {}
    context['PermisosGrales'] = permisosGrales
    context['Documento'] = documento
    context['Username'] = username
    context['Profesional'] = profesional
    context['Sede'] = sede
    context['PermisosGrales'] = permisosGrales
    context['NombreSede'] = nombreSede
    context['EscogeModulo'] = escogeModulo
    context['Username_id'] = username_id

    # aqui la manada de combos organizarlo segun necesidades

    # Combo ServiciosAdministrativos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
    comando = 'select m.id id, m.nombre||' + "'" + str(' ') + "'||" + ' u.nombre nombre FROM sitios_serviciosAdministrativos m, sitios_ubicaciones u where m.ubicaciones_id= u.id AND m."sedesClinica_id" = ' + str(sede)

    print(comando)
    curt.execute(comando)


    serviciosAdministrativos = []

    for id, nombre in curt.fetchall():
        serviciosAdministrativos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(serviciosAdministrativos)
    context['ServiciosAdministrativos'] = serviciosAdministrativos

    # Fin Combo ServiciosAdministrativos


    # Combo de Servicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT sed.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id AND ser.nombre != ' + "'" + str('TRIAGE') + "'"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed.id = sub."serviciosSedes_id"'
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios

    # Fin combo SubServicios

    # Combo TiposDOc

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc

    # Combo Habitaciones

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
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

    # Combo EspecialidadesMedicos


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' + "'" + str(username) + "' AND " + 'em."sedesClinica_id" = ' + "'" + str(sede) + "'"
    curt.execute(comando)
    print(comando)

    especialidadesMedicos = []
    especialidadesMedicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidadesMedicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidadesMedicos)

    context['EspecialidadesMedicos'] = especialidadesMedicos

    # Fin combo EspecialidadesMedicos



    # Combo Medicos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT med.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str('MEDICO') + "'" + ' and med.planta_id = p.id'

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

    # Combo TiposFolio


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

    curt.execute(comando)
    print(comando)

    tiposFolio = []
    tiposFolio.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposFolio.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposFolio)

    context['TiposFolio'] = tiposFolio

    # Fin combo TiposFolio

    # Combo TiposUsuario

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

    curt.execute(comando)
    print(comando)

    tiposUsuario = []
    tiposUsuario.append({'id': '', 'nombre': ''})


    for id, nombre in curt.fetchall():
        tiposUsuario.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposUsuario)

    context['TiposUsuario'] = tiposUsuario

    # Fin combo Tipos Usuario

    # Combo TiposDocumento

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

    curt.execute(comando)
    print(comando)

    tiposDocumento = []
    # tiposDocumento.append({'id': '', 'nombre': ''})

    tiposDocumento.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDocumento.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['TiposDocumento'] = tiposDocumento

    # Fin combo TiposDocumento

    # Combo Centros


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

    curt.execute(comando)
    print(comando)

    centros = []
    centros.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        centros.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['Centros'] = centros

    # Fin combo Centros

    # Combo Diagnosticos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT p.id id, p.nombre||' + "' '||" + 'cie10  nombre FROM clinico_diagnosticos p order by p.nombre'

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

    # Combo Pais

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_paises d ORDER BY d.nombre"

    curt.execute(comando)
    print(comando)

    pais = []

    for id, nombre in curt.fetchall():
        pais.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(pais)

    context['Pais'] = pais

    # Fin combo Pais

    # Combo Departamentos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d ORDER by d.nombre"

    curt.execute(comando)
    print(comando)

    departamentos = []
    departamentos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        departamentos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(departamentos)

    context['Departamentos'] = departamentos

    # Fin combo Departamentos

    # Combo Ciudades

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

    curt.execute(comando)
    print(comando)

    ciudades = []

    for id, nombre in curt.fetchall():
        ciudades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ciudades)

    context['Ciudades'] = ciudades

    # Fin combo Ciudades

    # Combo Modulos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

    curt.execute(comando)
    print(comando)

    modulos = []

    for id, nombre, nomenclatura, logo in curt.fetchall():
        modulos.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo})

    miConexiont.close()
    print(modulos)

    context['Modulos'] = modulos

    # Fin combo Modulos

    # Combo PermisosGrales

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
    comando =   'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
        username) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

    curt.execute(comando)
    print(comando)

    permisosGrales = []

    for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
        permisosGrales.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
             'modulo_nombre': modulo_nombre})

    miConexiont.close()
    print(permisosGrales)

    context['PermisosGrales'] = permisosGrales

    # Fin Combo PermisosGrales

    # Combo PermisosDetalle

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'" + username + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

    curt.execute(comando)
    print(comando)

    permisosDetalle = []

    for id, nombre, nomenclatura, logo, nombreOpcion, nombreElemento in curt.fetchall():
        permisosDetalle.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion': nombreOpcion,
             'nombreElemento': nombreElemento})

    miConexiont.close()
    print(permisosDetalle)

    context['PermisosDetalle'] = permisosDetalle

    # Fin Combo PermisosDetalle

    ## Hasta aquo FIN contexto para todas las Pantallas


    # Combo Vias Ingreso

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_viasingreso c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    viasIngreso = []
    viasIngreso.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        viasIngreso.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(viasIngreso)

    context['ViasIngreso'] = viasIngreso

    # Fin combo vias Ingreso

    # Combo Causas Externa

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_causasExterna c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    causasExterna = []

    for id, nombre in curt.fetchall():
        causasExterna.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(causasExterna)

    context['CausasExterna'] = causasExterna

    # Fin combo causasExterna

    # Combo Regimenes

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_regimenes c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    regimenes = []
    regimenes.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        regimenes.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(regimenes)

    context['Regimenes'] = regimenes

    # Fin combo regimenes


    # Combo Tipos Cotizante

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_tiposcotizante c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    tiposCotizante = []

    for id, nombre in curt.fetchall():
        tiposCotizante.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposCotizante)

    context['TiposCotizante'] = tiposCotizante

    # Fin combo tiposCotizante

    # Combo municipios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM sitios_municipios c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    municipios = []
    municipios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        municipios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(municipios)

    context['Municipios'] = municipios

    # Fin combo municipios

    # Combo localidades

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM sitios_localidades c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    localidades = []

    for id, nombre in curt.fetchall():
        localidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(localidades)

    context['Localidades'] = localidades

    # Fin combo localidades


    # Combo estadoCivil

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM basicas_estadocivil c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    estadoCivil = []
    estadoCivil.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        estadoCivil.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(estadoCivil)

    context['EstadoCivil'] = estadoCivil

    # Fin combo estadoCivil


    # Combo ocupaciones

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM basicas_ocupaciones c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    ocupaciones = []
    ocupaciones.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        ocupaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ocupaciones)

    context['Ocupaciones'] = ocupaciones

    # Fin combo ocupaciones


    # Combo ips

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_ips c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    ips = []
    ips.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        ips.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ips)

    context['Ips'] = ips

    # Fin combo ips

    # Combo Empresas

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM facturacion_empresas c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    empresas = []
    empresas.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        empresas.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(empresas)

    context['Empresas'] = empresas

    # Fin combo empresas



    # Combo ripstipousuario

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM RIPS_ripstipousuario c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    ripstipousuario = []

    for id, nombre in curt.fetchall():
        ripstipousuario.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ripstipousuario)

    context['RipsTipoUsuario'] = ripstipousuario

    # Fin combo ripstipousuario


    # Combo ripsZonaTerritorial

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM rips_ripsZonaTerritorial c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    ripsZonaTerritorial = []

    for id, nombre in curt.fetchall():
        ripsZonaTerritorial.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ripsZonaTerritorial)

    context['RipsZonaTerritorial'] = ripsZonaTerritorial

    # Fin combo RipsZonaTerritorial



    # Combo ripsFinalidadConsulta

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id,c.codigo id,c.nombre nombre FROM RIPS_ripsFinalidadConsulta c ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    ripsFinalidadConsulta= []

    for id, codigo, nombre in curt.fetchall():
        ripsFinalidadConsulta.append({'id': id, 'codigo':codigo, 'nombre': nombre})

    miConexiont.close()
    print(ripsFinalidadConsulta)

    context['RipsFinalidadConsulta'] = ripsFinalidadConsulta

    # Fin combo ripsFinalidadConsulta

    ## fin manada de combis


   # Aqui ya vienen las validaciones de permisos de acceso

    if (escogeModulo == 'ADMISIONES'):
        print ("ENTRE ADMISIONES 4")
        print("escogeModulo = ", escogeModulo)

        # Combo Acompanantes

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT c.id id,c.nombre nombre FROM usuarios_usuarioscontacto c, basicas_tiposcontacto t where  c."tiposContacto_id" = t.id and t.nombre like (' + "'" + str(
            '%ACOMPA%') + "')"

        curt.execute(comando)
        print(comando)

        acompanantes = []
        acompanantes.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            acompanantes.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(acompanantes)

        context['Acompanantes'] = acompanantes

        # Fin combo Acompanantes

        # Combo responsables

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT c.id id,c.nombre nombre FROM usuarios_usuarioscontacto c, basicas_tiposcontacto t where  c."tiposContacto_id" = t.id and t.nombre like (' + "'" + str(
            '%RESPONSA%') + "')"

        curt.execute(comando)
        print(comando)

        responsables = []
        responsables.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            responsables.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(responsables)

        context['Responsables'] = responsables

        # Fin combo responsables

        # Combo Convenios


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM contratacion_convenios p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        convenios = []

        for id, nombre in curt.fetchall():
            convenios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("convenios", convenios)

        context['Convenios'] = convenios

        # Fin combo Convenios


        # Combo Empresas


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM facturacion_empresas p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        empresas = []

        for id, nombre in curt.fetchall():
            empresas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("empresas", empresas)

        context['Empresas'] = empresas

        # Fin combo Empresas




        # Combo TiposPagos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM cartera_tipospagos p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        tiposPagos = []

        for id, nombre in curt.fetchall():
            tiposPagos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tiposPagos", tiposPagos)

        context['TiposPagos'] = tiposPagos

        # Fin combo tiposPagos


        # Combo FormasPagos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM cartera_formaspagos p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        formasPagos = []

        for id, nombre in curt.fetchall():
            formasPagos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("formasPagos", formasPagos)

        context['FormasPagos'] = formasPagos

        # Fin combo tiposPagos


        # Combo ripsServiciosIng

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_RipsServicios  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsServiciosIng = []
        ripsServiciosIng.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsServiciosIng.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsServiciosIng", ripsServiciosIng)

        context['RipsServiciosIng'] = ripsServiciosIng

        # Fin combo ripsServiciosIng

        # Combo ripsmodalidadGrupoServicioTecSal

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_RipsModalidadAtencion   p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsmodalidadGrupoServicioTecSal = []
        ripsmodalidadGrupoServicioTecSal.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            ripsmodalidadGrupoServicioTecSal.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsmodalidadGrupoServicioTecSal", ripsmodalidadGrupoServicioTecSal)

        context['RipsmodalidadGrupoServicioTecSal'] = ripsmodalidadGrupoServicioTecSal

        # Fin combo ripsmodalidadGrupoServicioTecSal

        # Combo ripsViaIngresoServicioSalud

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsviasingresosalud  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsViaIngresoServicioSalud = []
        ripsViaIngresoServicioSalud.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsViaIngresoServicioSalud.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsViaIngresoServicioSalud", ripsViaIngresoServicioSalud)

        context['RipsViaIngresoServicioSalud'] = ripsViaIngresoServicioSalud

        # Fin combo ripsViaIngresoServicioSalud

        # Combo ripsGrupoServicios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsGrupoServicios  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsGrupoServicios = []
        ripsGrupoServicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsGrupoServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsGrupoServicios", ripsGrupoServicios)

        context['RipsGrupoServicios'] = ripsGrupoServicios

        # Fin combo ripsGrupoServicios

        # Combo ripsCondicionDestinoUsuarioEgreso

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsdestinoegreso  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsCondicionDestinoUsuarioEgreso = []
        ripsCondicionDestinoUsuarioEgreso.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsCondicionDestinoUsuarioEgreso.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsCondicionDestinoUsuarioEgreso", ripsCondicionDestinoUsuarioEgreso)

        context['RipsCondicionDestinoUsuarioEgreso'] = ripsCondicionDestinoUsuarioEgreso

        # Fin combo ripsCondicionDestinoUsuarioEgreso

        # Combo ripsCausaMotivoAtencion

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripscausaexterna  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsCausaMotivoAtencion = []
        ripsCausaMotivoAtencion.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsCausaMotivoAtencion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsCausaMotivoAtencion", ripsCausaMotivoAtencion)

        context['RipsCausaMotivoAtencion'] = ripsCausaMotivoAtencion

        # Fin combo ripsCausaMotivoAtencion

        # Combo ripsDestinoUsuarioEgresoRecienNacido

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsdestinoegreso  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsDestinoUsuarioEgresoRecienNacido = []
        ripsDestinoUsuarioEgresoRecienNacido.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsDestinoUsuarioEgresoRecienNacido.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsDestinoUsuarioEgresoRecienNacido", ripsDestinoUsuarioEgresoRecienNacido)

        context['RipsDestinoUsuarioEgresoRecienNacido'] = ripsDestinoUsuarioEgresoRecienNacido

        # Fin combo ripsDestinoUsuarioEgresoRecienNacido


        ## Aqui contexto para solo admisiones


        ## Para los froms FURIPS

        context['FuripsForm'] = furipsForm

        # Combo Indicadores

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        print ("Listo voy a RENDERIZAR LA PAGINA")

        ## FIN CONTEXTO solo Admisiones



        return render(request, "admisiones/panelAdmisiones.html", context)

    if (escogeModulo == 'HISTORIA CLINICA'):
        print ("WENTRE PERMSISO HISTORIA CLINICA")
        ## Aqui contexto para solo Historia Clinica


        print("username = ", username)
        username = username.lstrip()

        ingresos = []

        # miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curx = miConexionx.cursor()

        detalle = 'SELECT i.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
            Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null'
        print(detalle)

        curx.execute(detalle)

        for id,tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'id':id, 'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        #username = username.lstrip()

        print ("username = ", username)

        documento_llave = Planta.objects.get(documento=username, sedesClinica_id=sede)

        print("el id del dopcumento = ", documento_llave.id)


        # Combo TiposSalidas


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",   password="123456")
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


        # Combo Enfermedades


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",   password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT e.id ,e.nombre FROM clinico_Enfermedades e ORDER BY e.nombre'
        curt.execute(comando)
        print(comando)

        enfermedades = []
        enfermedades.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
             enfermedades.append({'id': id, 'nombre': nombre})

        miConexiont.close()

        print(enfermedades)

        context['Enfermedades'] = enfermedades

        print ("enfermedades =", enfermedades)

        # FIN Combo enfermedades




        # Combo Dx Complicacion


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",   password="123456")
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


   	# Combo tiposAnestesia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "' '||" + 'cie10  nombre FROM  clinico_diagnosticos  p'

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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        # Combo Indicadores

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT ser.nombre nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
            sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = sd.id AND dep.disponibilidad = ' + "'" + str(
            'O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str(
            'N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(
            sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str(
            'TRIAGE') + "'" + ' group by ser.nombre'

        curt.execute(comando)
        print(comando)

        indicadores = []

        for nombre, total in curt.fetchall():
            indicadores.append({'nombre': nombre, 'total': total})
            if (nombre == 'HOSPITALIZACION'):
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

        print("total ", total)

        print("YA PASE INDICADORES")

        # Fin combo Indicadores

        # Fin Combo ServiciosAdministrativos



        # Combo EspecialidadesMedicosInterconsultas


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT e.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND  em."sedesClinica_id" = ' + "'" + str(sede) + "' GROUP BY  e.id ,e.nombre"
        curt.execute(comando)
        print(comando)

        especialidadesMedicosInterConsultas = []
        especialidadesMedicosInterConsultas.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            especialidadesMedicosInterConsultas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidadesMedicosInterConsultas)

        context['EspecialidadesMedicosInterConsultas'] = especialidadesMedicosInterConsultas

        # Fin combo EspecialidadesMedicosInterconsultas



        ## FIN CONTEXTO
        return render(request, "clinico/panelClinico2F.html", context)

    if (escogeModulo == 'TRIAGE'):
        print ("WENTRE PERMSISO TRIAGE")
        ## Aqui contexto para solo Triage

        # Combo de Servicios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT sed.id id ,sed.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
            sede) + "'" + ' AND sed."servicios_id" = ser.id AND ser.nombre = ' + "'" + str('TRIAGE') + "'"
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo de SubServicios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        #comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id"'
        comando = 'SELECT sub.id id ,sub.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(Sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sub."serviciosSedes_id" = sed.id AND ser.nombre = ' + "'" + str('TRIAGE') + "'"
        curt.execute(comando)
        print(comando)

        subServicios = []
        subServicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            subServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(subServicios)

        context['SubServicios'] = subServicios

        # Fin combo SubServicios

        # Combo de TiposTriage

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT id, nombre FROM clinico_tipostriage order by id'
        curt.execute(comando)
        print(comando)

        tiposTriage = []
        tiposTriage.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposTriage.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposTriage)

        context['TiposTriage'] = tiposTriage

        # Fin combo TiposTriage



        # Combo ripsServiciosIng


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_RipsServicios  p"

        curt.execute(comando)
        print(comando)

        ripsServiciosIng = []

        for id, nombre in curt.fetchall():
            ripsServiciosIng.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsServiciosIng", ripsServiciosIng)

        context['RipsServiciosIng'] = ripsServiciosIng

        # Fin combo ripsServiciosIng

        # Combo ripsmodalidadGrupoServicioTecSal


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_RipsModalidadAtencion   p"

        curt.execute(comando)
        print(comando)

        ripsmodalidadGrupoServicioTecSal = []

        for id, nombre in curt.fetchall():
            ripsmodalidadGrupoServicioTecSal.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsmodalidadGrupoServicioTecSal", ripsmodalidadGrupoServicioTecSal)

        context['RipsmodalidadGrupoServicioTecSal'] = ripsmodalidadGrupoServicioTecSal

        # Fin combo ripsmodalidadGrupoServicioTecSal

        # Combo ripsViaIngresoServicioSalud


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsviasingresosalud  p"

        curt.execute(comando)
        print(comando)

        ripsViaIngresoServicioSalud = []

        for id, nombre in curt.fetchall():
            ripsViaIngresoServicioSalud.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsViaIngresoServicioSalud", ripsViaIngresoServicioSalud)

        context['RipsViaIngresoServicioSalud'] = ripsViaIngresoServicioSalud

        # Fin combo ripsViaIngresoServicioSalud

        # Combo ripsGrupoServicios


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsGrupoServicios  p"

        curt.execute(comando)
        print(comando)

        ripsGrupoServicios = []

        for id, nombre in curt.fetchall():
            ripsGrupoServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsGrupoServicios", ripsGrupoServicios)

        context['RipsGrupoServicios'] = ripsGrupoServicios

        # Fin combo ripsGrupoServicios

        # Combo ripsCondicionDestinoUsuarioEgreso

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsdestinoegreso  p"

        curt.execute(comando)
        print(comando)

        ripsCondicionDestinoUsuarioEgreso = []

        for id, nombre in curt.fetchall():
            ripsCondicionDestinoUsuarioEgreso.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsCondicionDestinoUsuarioEgreso", ripsCondicionDestinoUsuarioEgreso)

        context['RipsCondicionDestinoUsuarioEgreso'] = ripsCondicionDestinoUsuarioEgreso

        # Fin combo ripsCondicionDestinoUsuarioEgreso

        # Combo ripsCausaMotivoAtencion


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripscausaexterna  p"

        curt.execute(comando)
        print(comando)

        ripsCausaMotivoAtencion = []

        for id, nombre in curt.fetchall():
            ripsCausaMotivoAtencion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsCausaMotivoAtencion", ripsCausaMotivoAtencion)

        context['RipsCausaMotivoAtencion'] = ripsCausaMotivoAtencion

        # Fin combo ripsCausaMotivoAtencion

        # Combo ripsDestinoUsuarioEgresoRecienNacido


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsdestinoegreso  p"

        curt.execute(comando)
        print(comando)

        ripsDestinoUsuarioEgresoRecienNacido = []

        for id, nombre in curt.fetchall():
            ripsDestinoUsuarioEgresoRecienNacido.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsDestinoUsuarioEgresoRecienNacido", ripsDestinoUsuarioEgresoRecienNacido)

        context['RipsDestinoUsuarioEgresoRecienNacido'] = ripsDestinoUsuarioEgresoRecienNacido

        # Fin combo ripsDestinoUsuarioEgresoRecienNacido

        # Combo Empresas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM facturacion_empresas c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        empresas = []
        empresas.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            empresas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(empresas)

        context['Empresas'] = empresas

        # Fin combo empresas

        # Combo ServiciosAdministrativos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select m.id id, m.nombre||' + "'" + str(' ') + "'||" + ' u.nombre nombre FROM sitios_serviciosAdministrativos m, sitios_ubicaciones u where m.ubicaciones_id= u.id AND m."sedesClinica_id" = ' + str(sede)

        print(comando)
        curt.execute(comando)

        serviciosAdministrativos = []

        serviciosAdministrativos.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            serviciosAdministrativos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ServiciosAdministrativos = " , serviciosAdministrativos)
        context['ServiciosAdministrativos'] = serviciosAdministrativos

        triage1 = []

        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curx = miConexionx.cursor()

        #comando = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , t.consec consec , dep.nombre camaNombre,t."fechaSolicita" solicita,t.motivo motivo, t."clasificacionTriage_id" triage FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  ,sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND t."sedesClinica_id" =' + "'" + str(Sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND t."serviciosSedes_id" = sd.id AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and t."tipoDoc_id" = u."tipoDoc_id" and  u.id = t."documento_id"'
        comando = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , t.consec consec , dep.nombre camaNombre,t."fechaSolicita" solicita,t.motivo motivo, t."clasificacionTriage_id" triage FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  ,sitios_serviciosSedes sd, clinico_servicios ser  WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND t."sedesClinica_id" =' + "'" + str(Sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and t."tipoDoc_id" = u."tipoDoc_id" and  u.id = t."documento_id"  and ser.id = sd.servicios_id and dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str('TRIAGE') + "'"
        print(comando)

        curx.execute(comando)

        for tipoDoc, documento, nombre, consec, camaNombre, solicita, motivo, triage in curx.fetchall():
            triage1.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,'camaNombre': camaNombre, 'solicita': solicita,
                             'motivo': motivo, 'triage': triage})

        miConexionx.close()
        print(triage1)
        context['Triage'] = triage1

        context['PermisoTriage'] = 'True'
        context['PermisoCrearTriage'] = 'True'

        ## FIN CONTEXTO
        return render(request, "triage/panelTriage.html", context)

    if (escogeModulo == 'AUTORIZACIONES'):
        print ("ENTRE PERMSISO AUTORIZACIONES")
        ## Aqui contexto para solo Triage

   	# Combo estadosautorizacion

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM  autorizaciones_estadosautorizacion  p"

        curt.execute(comando)
        print(comando)

        estadosAutorizacion = []


        for id, nombre in curt.fetchall():
            estadosAutorizacion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("EstadosAutorizacion", estadosAutorizacion)

        context['EstadosAutorizacion'] = estadosAutorizacion

        # Fin combo estadosAutorizacion

        # Combo Convenios


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM contratacion_convenios p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        convenios = []

        for id, nombre in curt.fetchall():
            convenios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("convenios", convenios)

        context['Convenios'] = convenios

        # Fin combo Convenios



        ## FIN CONTEXTO
        return render(request, "autorizaciones/panelAutorizacionesF.html", context)

    if (escogeModulo == 'FACTURACION'):
        print("ENTRE PERMSISO FACTURACION")
        ## Aqui contexto para solo Facturacion

        ## FIN CONTEXTO

        # Combo Indicadores

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

   	# Combo estado envio dian

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM  facturacion_estadoEnvioDian  p"

        curt.execute(comando)
        print(comando)

        estadoEnvioDian = []


        for id, nombre in curt.fetchall():
            estadoEnvioDian.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("estadoEnvioDian", estadoEnvioDian)

        context['EstadoEnvioDian'] = estadoEnvioDian

        # Fin combo estadoEnvioDian


        return render(request, "facturacion/panelFacturacionF.html", context)


    if (escogeModulo == 'CIRUGIA'):
        print("ENTRE PERMSISO CIRUGIA")
        ## Aqui contexto para solo Facturacion

        ## FIN CONTEXTO

   	# Combo salas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM  sitios_salas  p"

        curt.execute(comando)
        print(comando)

        salasCirugia = []


        for id, nombre in curt.fetchall():
            salasCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("salasCirugia", salasCirugia)

        context['SalasCirugia'] = salasCirugia

        # Fin combo salas


   	# Combo tiposAnestesia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "' '||" + 'cie10  nombre FROM  clinico_diagnosticos  p'

        curt.execute(comando)
        print(comando)

        diagnosticosCirugia = []


        for id, nombre in curt.fetchall():
            diagnosticosCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("diagnosticosCirugia", diagnosticosCirugia)

        context['DiagnosticosCirugia'] = diagnosticosCirugia

        # Fin combo diagnosticosCirugia

	# Combo especialidadesCirugia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM  clinico_especialidades  p"

        curt.execute(comando)
        print(comando)

        especialidadesCirugia = []


        for id, nombre in curt.fetchall():
            especialidadesCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("especialidadesCirugia", especialidadesCirugia)

        context['EspecialidadesCirugia'] = especialidadesCirugia

        # Fin combo especialidadesCirugia

	# Combo cupsCirugia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "' '||" + '"codigoCups" nombre FROM  clinico_examenes  p ORDER BY nombre'

        curt.execute(comando)
        print(comando)

        cupsCirugia = []


        for id, nombre in curt.fetchall():
            cupsCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("cupsCirugia", cupsCirugia)

        context['CupsCirugia'] = cupsCirugia

        # Fin combo cupsCirugia

	# Combo finalidadCirugia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre nombre FROM  cirugia_finalidadcirugia  p ORDER BY nombre"

        curt.execute(comando)
        print(comando)

        finalidadCirugia = []


        for id, nombre in curt.fetchall():
            finalidadCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("finalidadCirugia", finalidadCirugia)

        context['FinalidadCirugia'] = finalidadCirugia

        # Fin combo finalidadCirugia


	# Combo tiposHonorarios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre nombre FROM  tarifarios_tiposHonorarios  p ORDER BY nombre"

        curt.execute(comando)
        print(comando)

        tiposHonorarios = []


        for id, nombre in curt.fetchall():
            tiposHonorarios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tiposHonorarios", tiposHonorarios)

        context['TiposHonorarios'] = tiposHonorarios

        # Fin combo tiposHonorarios

	# Combo EspecialidadesMedicos


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' + "'" + str(username) + "' AND " + 'em."sedesClinica_id" = ' + "'" + str(sede) + "'"
        curt.execute(comando)
        print(comando)

        especialidadesMedicos = []
        especialidadesMedicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
          especialidadesMedicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidadesMedicos)

        context['EspecialidadesMedicos'] = especialidadesMedicos

        # Fin combo EspecialidadesMedicos

	# Combo EspecialidadesMedicosCirugia


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT em.id ,pl.nombre||'+ "'" + str(' ') + "'" +  '||e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id  AND em."sedesClinica_id" = ' + "'" + str(sede) + "'"
        curt.execute(comando)
        print(comando)

        especialidadesMedicosCirugia = []
        especialidadesMedicosCirugia.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
          especialidadesMedicosCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidadesMedicosCirugia)

        context['EspecialidadesMedicosCirugia'] = especialidadesMedicosCirugia

        # Fin combo especialidadesMedicosCirugia



        # Combo suministrosCirugia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "' '||" + ' p.cums nombre FROM  facturacion_suministros  p ORDER BY nombre'

        curt.execute(comando)
        print(comando)

        suministrosCirugia = []

        for id, nombre in curt.fetchall():
            suministrosCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("suministrosCirugia", suministrosCirugia)

        context['SuministrosCirugia'] = suministrosCirugia

        # Fin combo SUMINISTROS CIRUGIA

        honorarioMaterialQx = TiposHonorarios.objects.get(nombre='MATERIAL QX')

	# Combo ProcedimientosCirugia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "' '||" + '"codigoCups" nombre FROM  clinico_examenes  p WHERE p."tipoHonorario_id" = ' + "'" + str(honorarioMaterialQx.id) + "'" + ' ORDER BY nombre'

        curt.execute(comando)
        print(comando)

        procedimientosCirugia = []


        for id, nombre in curt.fetchall():
            procedimientosCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("procedimientosCirugia", procedimientosCirugia)

        context['ProcedimientosCirugia'] = procedimientosCirugia

        # Fin combo ProcedimientosCirugia




        # Combo estadosCirugia

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre nombre FROM  cirugia_estadoscirugias  p ORDER BY nombre"

        curt.execute(comando)
        print(comando)

        estadosCirugia = []

        for id, nombre in curt.fetchall():
            estadosCirugia.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("estadosCirugia", estadosCirugia)

        context['EstadosCirugia'] = estadosCirugia

        # Fin combo estadosCirugia


        # Combo estadosProgramacion

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre nombre FROM  cirugia_estadosprogramacion p ORDER BY nombre"

        curt.execute(comando)
        print(comando)

        estadosProgramacion = []

        for id, nombre in curt.fetchall():
            estadosProgramacion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("estadosProgramacion", estadosProgramacion)

        context['EstadosProgramacion'] = estadosProgramacion

        # Fin combo estadosProgramacion


        # Combo regionesOperatorias

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.region nombre FROM  cirugia_regionesOperatorias  p ORDER BY p.region"

        curt.execute(comando)
        print(comando)

        regionesOperatorias = []


        for id, nombre in curt.fetchall():
            regionesOperatorias.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("regionesOperatorias", regionesOperatorias)

        context['RegionesOperatorias'] = regionesOperatorias

        # Fin combo regionesOperatorias

	# Combo viasDeAcceso

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre nombre FROM  cirugia_viasDeAcceso  p ORDER BY nombre"

        curt.execute(comando)
        print(comando)

        viasDeAcceso = []


        for id, nombre in curt.fetchall():
            viasDeAcceso.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("viasDeAcceso", viasDeAcceso)

        context['ViasDeAcceso'] = viasDeAcceso

        # Fin combo vias de acceso


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre nombre FROM  sitios_serviciosadministrativos  p ORDER BY nombre"

        curt.execute(comando)
        print(comando)


        serviciosAdministrativos = []

        serviciosAdministrativos.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            serviciosAdministrativos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ServiciosAdministrativos = " , serviciosAdministrativos)
        context['ServiciosAdministrativos'] = serviciosAdministrativos



        return render(request, "cirugia/panelCirugiaF.html", context)


    if (escogeModulo == 'CONTRATACION'):
        print("ENTRE PERMSISO FACTURACION")
        ## Aqui contexto para solo Facturacion


        # Combo Empresas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM facturacion_empresas c"

        curt.execute(comando)
        print(comando)

        empresas = []

        for id, nombre in curt.fetchall():
            empresas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(empresas)

        context['Empresas'] = empresas

    # Combo tarifariosDescripcionProc

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT des.id id, des.descripcion  nombre FROM  tarifarios_tarifariosDescripcion  des , tarifarios_tipostarifa tiptar, tarifarios_tipostarifaproducto tipprod WHERE des."tiposTarifa_id" = tiptar.id AND tiptar."tiposTarifaProducto_id" = tipprod.id AND tipprod.nombre like (' + "'%" + str('PROCEDIMIENTO') +"%')"

        curt.execute(comando)
        print(comando)

        tarifariosDescripcionProc = []
        tarifariosDescripcionProc.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tarifariosDescripcionProc.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tarifariosDescripcionProc", tarifariosDescripcionProc)

        context['TarifariosDescripcionProc'] = tarifariosDescripcionProc

        # Fin combo tarifariosDescripcionProc

 	# Combo tarifariosDescripcionSum

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT des.id id, des.descripcion  nombre FROM  tarifarios_tarifariosDescripcion  des , tarifarios_tipostarifa tiptar, tarifarios_tipostarifaproducto tipprod WHERE des."tiposTarifa_id" = tiptar.id AND tiptar."tiposTarifaProducto_id" = tipprod.id AND tipprod.nombre like (' + "'%" + str('SUMINISTRO') +"%')"

        curt.execute(comando)
        print(comando)

        tarifariosDescripcionSum = []

        tarifariosDescripcionSum.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tarifariosDescripcionSum.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tarifariosDescripcionSum", tarifariosDescripcionSum)

        context['TarifariosDescripcionSum'] = tarifariosDescripcionSum

        # Fin combo tarifariosDescripcionSum


 	# Combo tarifariosDescripcionHonorarios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT des.id id, des.nombre  nombre FROM  tarifarios_tarifariosDescripcionHonorarios  des ORDER By des.nombre'

        curt.execute(comando)
        print(comando)

        tarifariosDescripcionHonorarios = []
        tarifariosDescripcionHonorarios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tarifariosDescripcionHonorarios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tarifariosDescripcionHonorarios", tarifariosDescripcionHonorarios)

        context['TarifariosDescripcionHonorarios'] = tarifariosDescripcionHonorarios

        # Fin combo tarifariosDescripcionHonoracion

        ## FIN CONTEXTO

        return render(request, "contratacion/panelConveniosF.html", context)


    if (escogeModulo == 'APOYO TERAPEUTICO'):
        print("ENTRE PERMSISO APOYO TERAPEUTICO")
        ## Aqui contexto para solo Triage

        ## FIN CONTEXTO
        return render(request, "apoyoTerapeutico/panelApoyoTerapeutico.html", context)


    if (escogeModulo == 'TARIFAS'):
        print("ENTRE PERMSISO TARIFAS")
        ## Aqui contexto para solo Tarifarios

   	# Combo TiposTarifa Suministros

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre  nombre FROM  tarifarios_tipostarifa  p where p."tiposTarifaProducto_id" in (select id from tarifarios_tipostarifaProducto where nombre like (' + "'" + str('%SUMIN%')  + "'))"
        print(comando)
        curt.execute(comando)


        tiposTarifaSuministros = []


        for id, nombre in curt.fetchall():
            tiposTarifaSuministros.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("tiposTarifaSuministros", tiposTarifaSuministros)

        context['TiposTarifaSuministros'] = tiposTarifaSuministros

        # Fin combo TiposTarifa Suministros



   	# Combo TiposTarifa

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre  nombre FROM  tarifarios_tipostarifa  p where p."tiposTarifaProducto_id" in (select id from tarifarios_tipostarifaProducto where nombre like (' + "'" + str('%PROCED%')  + "'))"
        print(comando)
        curt.execute(comando)


        tiposTarifa = []


        for id, nombre in curt.fetchall():
            tiposTarifa.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("TiposTarifa", tiposTarifa)

        context['TiposTarifa'] = tiposTarifa

        # Fin combo TiposTarifa

   	# Combo Cups

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "'" + str(' ') + "'" + '||p."codigoCups"  nombre FROM  clinico_examenes  p ORDER BY p.id '
        print(comando)
        curt.execute(comando)


        cups = []

        cups.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            cups.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("Cups", cups)

        context['Cups'] = cups

        # Fin combo Cups


   	# Combo Cums

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "'" + str(' ') + "'"  +' ||p.cums  nombre FROM  facturacion_suministros  p ORDER BY p.id '
        print(comando)
        curt.execute(comando)


        cums = []

        cums.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            cums.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("cums", cums)

        context['Cums'] = cums

        # Fin combo Cums





   	# Combo Conceptos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre  nombre FROM  facturacion_conceptos p'
        print(comando)
        curt.execute(comando)


        conceptos = []


        for id, nombre in curt.fetchall():
            conceptos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("conceptos", conceptos)

        context['Conceptos'] = conceptos

        # Fin combo Conceptos



        ## FIN CONTEXTO
        return render(request, "tarifarios/PanelTarifariosF.html", context)


    if (escogeModulo == 'RIPS'):
        print("ENTRE PERMSISO RIPS")
        ## Aqui contexto para solo Rips

        # Combo RipsTiposNotas


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_RipsTiposNotas  p "

        curt.execute(comando)
        print(comando)

        ripsTiposNotas = []

        for id, nombre in curt.fetchall():
            ripsTiposNotas .append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsTiposNotas ", ripsTiposNotas )

        context['RipsTiposNotas'] = ripsTiposNotas 

        # Fin combo ripsTiposNotas 


        ## FIN CONTEXTO
        return render(request, "rips/PanelRipsF.html", context)


    if (escogeModulo == 'GLOSAS'):
        print("ENTRE PERMSISO GLOSAS")



        # Combo Tipos Notas Credito

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM cartera_tiposnotascredito c ORDER BY nombre asc "

        curt.execute(comando)
        print(comando)

        tiposNotasCredito = []

        for id, nombre in curt.fetchall():
            tiposNotasCredito.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposNotasCredito)

        context['TiposNotasCredito'] = tiposNotasCredito

        # Fin combo tiposNotasCredito



        # Combo Convenios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM contratacion_convenios c"

        curt.execute(comando)
        print(comando)

        convenios = []

        for id, nombre in curt.fetchall():
            convenios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(convenios)

        context['Convenios'] = convenios

        # Fin combo convenios

        # Combo Tipos Glosas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM cartera_tiposglosas c "

        curt.execute(comando)
        print(comando)

        tiposGlosas = []

        for id, nombre in curt.fetchall():
            tiposGlosas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposGlosas)

        context['TiposGlosas'] = tiposGlosas

        # Fin combo Tipos Glosas

        # Combo Motivos Glosas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM cartera_motivosglosas c "

        curt.execute(comando)
        print(comando)

        motivosGlosas = []

        for id, nombre in curt.fetchall():
            motivosGlosas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(motivosGlosas)

        context['MotivosGlosas'] = motivosGlosas

        # Fin combo motivos Glosas


        # Combo Estados Glosas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM cartera_estadosglosas c WHERE c.tipo= 'RECEPCION'"

        curt.execute(comando)
        print(comando)

        estadosRecepcion = []

        for id, nombre in curt.fetchall():
            estadosRecepcion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(estadosRecepcion)

        context['EstadosRecepcion'] = estadosRecepcion

        # Fin combo Estado Glosas recepcion


        # Combo Estados Glosas Radicacion

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM cartera_estadosglosas c WHERE c.tipo= 'RADICACION'"

        curt.execute(comando)
        print(comando)

        estadosRadicacion = []

        for id, nombre in curt.fetchall():
            estadosRadicacion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(estadosRadicacion)

        context['EstadosRadicacion'] = estadosRadicacion

        # Fin combo Estado Glosas estadosRadicacion


        return render(request, "cartera/PanelGlosasFU.html", context)


    if (escogeModulo == 'CARTERA'):
        print("ENTRE PERMISO CARTERA")

        # Combo Convenios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM contratacion_convenios c"

        curt.execute(comando)
        print(comando)

        convenios = []

        for id, nombre in curt.fetchall():
            convenios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(convenios)

        context['Convenios'] = convenios

        # Fin combo convenios


        # Combo UsuarioEntrega

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM planta_planta c WHERE " + ' "sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND  c."estadoReg" = ' + "'" + str('A') + "' AND " + ' "esCajero" = ' + "'" + str('S') + "'"

        curt.execute(comando)
        print(comando)

        usuarioEntrega = []

        for id, nombre in curt.fetchall():
            usuarioEntrega.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(usuarioEntrega)

        context['UsuarioEntrega'] = usuarioEntrega

        # Fin combo UsuarioEntrega

        # Combo UsuarioRecibe

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM planta_planta c WHERE " + ' "sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND  c."estadoReg" = ' + "'" + str('A') + "' AND " + ' "esCajero" = ' + "'" + str('S') + "'"

        curt.execute(comando)
        print(comando)

        usuarioRecibe = []

        for id, nombre in curt.fetchall():
            usuarioRecibe.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(usuarioRecibe)

        context['UsuarioRecibe'] = usuarioRecibe

        # Fin combo usuarioRecibe


        # Combo UsuarioSuperviza

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM planta_planta c WHERE " + ' "sedesClinica_id" =  ' + "'" + str(sede) + "'" + ' AND  c."estadoReg" = ' + "'" + str('A') + "' AND " + ' "esCajero" = ' + "'" + str('S') + "'"

        curt.execute(comando)
        print(comando)

        usuarioSuperviza = []

        for id, nombre in curt.fetchall():
            usuarioSuperviza.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(usuarioSuperviza)

        context['UsuarioSuperviza'] = usuarioSuperviza

        # Fin combo UsuarioSuperviza

        # Combo ServiciosAdministrativos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
        comando = 'select m.id id, m.nombre||' + "'" + str(
            ' ') + "'||" + ' u.nombre nombre FROM sitios_serviciosAdministrativos m, sitios_ubicaciones u where m.ubicaciones_id= u.id AND m."sedesClinica_id" = ' + str(
            sede)

        print(comando)
        curt.execute(comando)

        serviciosAdministrativos = []

        for id, nombre in curt.fetchall():
            serviciosAdministrativos.append({'id': id, 'nombre': nombre})

        miConexiont.close()

        print(serviciosAdministrativos)
        context['ServiciosAdministrativos'] = serviciosAdministrativos

        # Fin Combo ServiciosAdministrativos

        # Combo Empresas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM facturacion_empresas c"

        curt.execute(comando)
        print(comando)

        empresas = []

        for id, nombre in curt.fetchall():
            empresas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(empresas)

        context['Empresas'] = empresas

        # Fin combo empresas

        # Combo FormasPagos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM cartera_formaspagos c"

        curt.execute(comando)
        print(comando)

        formasPagos = []

        for id, nombre in curt.fetchall():
            formasPagos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(formasPagos)

        context['FormasPagos'] = formasPagos

        # Fin combo formasPagos

        # Combo TiposPagos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM cartera_tipospagos c"

        curt.execute(comando)
        print(comando)

        tiposPagos = []

        for id, nombre in curt.fetchall():
            tiposPagos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposPagos)

        context['TiposPagos'] = tiposPagos

        # Fin combo tiposPagos




        return render(request, "cartera/PanelCarteraF.html", context)


    if (escogeModulo == 'ENFERMERIA'):
        print("ENTRE PERMSISO ENFERMERIA")
        ## Aqui contexto para solo ENFERMERIA

        # Combo ServiciosAdministrativos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select m.id id, m.nombre||' + "'" + str(' ') + "'||" + ' u.nombre nombre FROM sitios_serviciosAdministrativos m, sitios_ubicaciones u where m.ubicaciones_id= u.id AND m."sedesClinica_id" = ' + str(sede)

        print(comando)
        curt.execute(comando)

        serviciosAdministrativos = []

        serviciosAdministrativos.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            serviciosAdministrativos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ServiciosAdministrativos = " , serviciosAdministrativos)
        context['ServiciosAdministrativos'] = serviciosAdministrativos

        # Fin Combo ServiciosAdministrativos

        # Combo EnfermeriaTipoOrigen

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select o.id id, o.nombre nombre FROM enfermeria_enfermeriaTipoOrigen o'

        print(comando)
        curt.execute(comando)

        enfermeriaTipoOrigen = []

        enfermeriaTipoOrigen.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            enfermeriaTipoOrigen.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("enfermeriaTipoOrigen  = " , enfermeriaTipoOrigen )
        context['EnfermeriaTipoOrigen'] = enfermeriaTipoOrigen 

        # Fin Combo enfermeriaTipoOrigen 


        # Combo EnfermeriaTipoMovimiento

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select o.id id, o.nombre nombre FROM enfermeria_enfermeriaTipoMovimiento o'

        print(comando)
        curt.execute(comando)

        enfermeriaTipoMovimiento = []

        enfermeriaTipoMovimiento.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            enfermeriaTipoMovimiento.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("enfermeriaTipoMovimiento  = " , enfermeriaTipoMovimiento )
        context['EnfermeriaTipoMovimiento'] = enfermeriaTipoMovimiento

        # Fin Combo enfermeriaTipoMovimiento 

        # Combo Medicamentos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

        # Combo Vias Administracion

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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


       # Combo PlantaUsuarios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM planta_planta e WHERE e."sedesClinica_id" = ' + "'" + str(sede) + "'"

        curt.execute(comando)
        print(comando)

        plantaUsuarios= []
        plantaUsuarios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            plantaUsuarios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(plantaUsuarios)

        context['PlantaUsuarios'] = plantaUsuarios

        # Fin combo PlantaUsuarios

       # Combo TipoDietas

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM clinico_tipodietas e'

        curt.execute(comando)
        print(comando)

        tipoDietas= []
        tipoDietas.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tipoDietas.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tipoDietas)

        context['TipoDietas'] = tipoDietas

        # Fin combo tipoDietas



        ## FIN CONTEXTO
        return render(request, "enfermeria/PanelEnfermeriaF.html", context)


    if (escogeModulo == 'FARMACIA'):
        print("ENTRE PERMSISO FARMACIA")
        ## Aqui contexto para solo FARMACIA
        # Combo ServiciosAdministrativos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select m.id id, m.nombre||' + "'" + str(' ') + "'||" + ' u.nombre nombre FROM sitios_serviciosAdministrativos m, sitios_ubicaciones u where m.ubicaciones_id= u.id AND m."sedesClinica_id" = ' + str(sede)

        print(comando)
        curt.execute(comando)

        serviciosAdministrativos = []

        serviciosAdministrativos.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            serviciosAdministrativos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ServiciosAdministrativos = " , serviciosAdministrativos)
        context['ServiciosAdministrativos'] = serviciosAdministrativos

        # Fin Combo ServiciosAdministrativos

        # Combo Medicamentos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre||' + "' '||" + ' e.cums nombre  FROM facturacion_Suministros e, facturacion_tipossuministro t  where e."tipoSuministro_id" = t.id AND t.nombre = ' + "'" + str('MEDICAMENTOS') + "' ORDER BY e.nombre"

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

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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

       # Combo PlantaUsuarios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM planta_planta e WHERE e."sedesClinica_id" = ' + "'" + str(sede) + "'"

        curt.execute(comando)
        print(comando)

        plantaUsuarios= []
        plantaUsuarios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            plantaUsuarios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(plantaUsuarios)

        context['PlantaUsuarios'] = plantaUsuarios

        # Fin combo PlantaUsuarios

       # Combo Estados Farmacia
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM farmacia_farmaciaestados e'

        curt.execute(comando)
        print(comando)

        farmaciaEstados= []
      

        for id, nombre in curt.fetchall():
            farmaciaEstados.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(farmaciaEstados)

        context['FarmaciaEstados'] = farmaciaEstados

        # Fin combo farmaciaEstados

       # Combo Estados Farmacia Limitados
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT e.id id, e.nombre nombre  FROM farmacia_farmaciaestados e WHERE E.nombre like (' + "'" + str('%DESPA%') + "')"

        curt.execute(comando)
        print(comando)

        farmaciaEstadosLimitados= []
      

        for id, nombre in curt.fetchall():
            farmaciaEstadosLimitados.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(farmaciaEstadosLimitados)

        context['FarmaciaEstadosLimitados'] = farmaciaEstadosLimitados

        # Fin combo farmaciaEstadosLimitados



        # Combo Vias Administracion

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
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


        ## FIN CONTEXTO
        return render(request, "farmacia/PanelFarmaciaF.html", context)

    if (escogeModulo == 'REPORTES'):
        print("ENTRE PERMSISO REPORTES")
        ## Aqui contexto
        print ("Entre Validacion Reporteador")

        # Sedes

        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",
                                      user="postgres", password="123456")
        cur = miConexion.cursor()
        comando = "SELECT id  codreg_sede ,nombre nom_sede  FROM sitios_sedesClinica"
        cur.execute(comando)
        print(comando)
        context = {}
        sedes = []

        for codreg_sede, nom_sede in cur.fetchall():
            sedes.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

        miConexion.close()
        print(sedes)

        context['Sedes'] = sedes

        print ("Aqui estan las sedes")
        print (context['Sedes'])

        sedeSeleccionada   = sede
        print ("sedeSeleccionada = " , sedeSeleccionada)
        print("username = ", username)

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = profesional

        print ("Asi quedo el nombre del usuario", profesional)

        # Valido Permiso de ejecucion en la Sede seleccinada

        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",
                                      user="postgres",
                                      password="123456")
        cur = miConexion.cursor()

        comando = 'select usuarios.cod_usuario  as usuario from "Administracion_mae_repusuarios" usuarios, sitios_sedesClinica sedes where  usuarios.estadoReg =  ' + "'" + 'A' +  "'" + ' and  usuarios.cod_usuario = ' + "'" + username + "'" + ' and usuarios.cod_sede_id = sedes.id and sedes.id = '  + "'"  + sedeSeleccionada + "'"
        print(comando)
        cur.execute(comando)


        permitido = []

        for usuario in cur.fetchall():
            permitido.append({'usuario': usuario})

        miConexion.close()

        if permitido == []:

            context['Error'] = "Usuario no tiene autorizacion para la sede seleccionada y/o Reportes no asignados ! "
            return render(request, "inicio/accesoPrincipal1.html", context)

        else:

            print("Paso Autenticacion")

        # Le doy la informacion de los reportes a los que tiene acceso

        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",
                                      user="postgres",
                                      password="123456")
        cur = miConexion.cursor()
        #cur.execute("set client_encoding='LATIN1';")

        comando = 'select  reportes.id numreporte, usuarios.cod_usuario usuario, reportes.nom_reporte reporte,reportes.cuerpo_sql, reportes.descripcion descripcion , reportes.encabezados encabezados ,reportes.mae_gruporeportes_id grupo ,reportes.mae_subgruporeportes_id subgrupo , grupos.nom_grupo nombreGrupo, subgrupos.nom_subgrupo nombreSubgrupo from "Administracion_mae_repusuarios" as usuarios,  "Administracion_mae_reportes" as reportes , sitios_sedesClinica sedes , "Administracion_mae_gruporeportes" grupos, "Administracion_mae_subgruporeportes" subgrupos   where usuarios.cod_Usuario = ' + "'" + username + "'" + ' and  usuarios.mae_reportes_id = reportes.id  and usuarios.cod_sede_id = sedes.id and grupos.id = reportes.mae_gruporeportes_id and subgrupos.id = reportes.mae_subgruporeportes_id  and sedes.id = ' + "'" + sede + "'" + ' AND usuarios.estadoReg=' + "'A'" + ' AND reportes.estadoReg=' + "'A'"

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
        miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432",
                                      user="postgres",
                                      password="123456")
        cur = miConexion.cursor()
        comando = 'select  id , grupos.nom_grupo nombreGrupo, grupos.logo logo  from "Administracion_mae_gruporeportes" grupos order by grupos.id'

        print(comando)
        cur.execute(comando)

        grupos = []

        for id, nombreGrupo, logo in cur.fetchall():
            grupos.append(
                {'id': id, 'nombreGrupo': nombreGrupo , 'logo':logo})

        miConexion.close()
        context['Grupos'] = grupos
        print("pase0")

    return render(request, "Reportes/PantallaGrupos.html", context)


    return render(request, "panelVacio.html", context)




    return render(request, "panelVacio.html", context)



def retornarAdmision(request, Sede, Perfil, Username, Username_id, NombreSede):


    print ("Entre Retornar Admision")
    #Sede = request.POST["Sede"]
    print ("Sede = ", Sede)
    Sede = Sede.lstrip()
    sede = Sede
    #Perfil = request.POST["Perfil"]
    print ("Perfil = ",Perfil)
    Perfil = Perfil.lstrip()
    print("Perfil = ", Perfil)

    print ("Nombre dede = ", NombreSede)
    username = Username

    context = {}

    context['Sede'] = Sede
    context['Username'] = Username
    context['Username_id'] = Username_id
    context['NombreSede'] = NombreSede


    # Consigo la sede Nombre


    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []

    for nombre in cur.fetchall():
        nombreSedes.append({'nombre': nombre})

    miConexion.close()
    print(nombreSedes)
    nombresede1 = nombreSedes[0]

    context['NombreSede'] = nombresede1

    # esta consulta por que se pierde de otras pantallas


    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    ingresos = []


    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
        Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null'
    print(detalle)

    curx.execute(detalle)

    for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
        ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                         'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'DxActual': dxActual})

    miConexionx.close()
    print(ingresos)
    context['Ingresos'] = ingresos

    # Combo de Servicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed.sedesClinica_id ='" + str(
        sede) + "' AND sed.servicios_id = ser.id"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed.sedesClinica_id ='" + str(
        Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id"
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios

    # Fin combo SubServicios


    # Combo TiposDOc

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc

    # Combo Habitaciones

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()
    comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
    curt.execute(comando)
    print(comando)

    habitaciones = []

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
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

    # Combo Medicos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT p.id id, p.nombre  nombre FROM planta_planta p , planta_perfilesplanta perf WHERE perf.sedesClinica_id = '" + str(
        Sede) + "' AND perf.tiposPlanta_id = 1 and p.id = perf.planta_id"

    curt.execute(comando)
    print(comando)

    medicos = []
    medicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        medicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicos)

    context['Medicos'] = medicos
    context['Perfil'] = Perfil


    # Combo Vias Ingreso


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_viasingreso c"

    curt.execute(comando)
    print(comando)

    viasIngreso = []

    for id, nombre in curt.fetchall():
        viasIngreso.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(viasIngreso)

    context['ViasIngreso'] = viasIngreso

    # Fin combo vias Ingreso

    # Combo Causas Externa

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_causasExterna c"

    curt.execute(comando)
    print(comando)

    causasExterna = []

    for id, nombre in curt.fetchall():
        causasExterna.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(causasExterna)

    context['CausasExterna'] = causasExterna

    # Fin combo causasExterna

    # Combo Regimenes


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_regimenes c"

    curt.execute(comando)
    print(comando)

    regimenes = []

    for id, nombre in curt.fetchall():
        regimenes.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(regimenes)

    context['Regimenes'] = regimenes

    # Fin combo regimenes


    # Combo Tipos Cotizante


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_tiposcotizante c"

    curt.execute(comando)
    print(comando)

    tiposCotizante = []

    for id, nombre in curt.fetchall():
        tiposCotizante.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposCotizante)

    context['TiposCotizante'] = tiposCotizante

    # Fin combo tiposCotizante


    # Combo municipios


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM sitios_municipios c"

    curt.execute(comando)
    print(comando)

    municipios = []

    for id, nombre in curt.fetchall():
        municipios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(municipios)

    context['Municipios'] = municipios

    # Fin combo municipios

    # Combo localidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM sitios_localidades c"

    curt.execute(comando)
    print(comando)

    localidades = []

    for id, nombre in curt.fetchall():
        localidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(localidades)

    context['Localidades'] = localidades

    # Fin combo localidades


    # Combo estadoCivil


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM basicas_estadocivil c"

    curt.execute(comando)
    print(comando)

    estadoCivil = []

    for id, nombre in curt.fetchall():
        estadoCivil.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(estadoCivil)

    context['EstadoCivil'] = estadoCivil

    # Fin combo estadoCivil


    # Combo ocupaciones

    # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM basicas_ocupaciones c"

    curt.execute(comando)
    print(comando)

    ocupaciones = []

    for id, nombre in curt.fetchall():
        ocupaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ocupaciones)

    context['Ocupaciones'] = ocupaciones

    # Fin combo ocupaciones




    # Fin combo Medicos

    if (Perfil == 1):
        return render(request, "menuMedico.html", context)
    if (Perfil == 2):
        return render(request, "menuEnfermero.html", context)
    if (Perfil == 3):
        return render(request, "menuAuxiliar.html", context)
    if (Perfil == 4):
        return render(request, "citasMedicas/menuCitasMedicas.html", context)
    if (Perfil == 5):
        return render(request, "facturacion/menuFacturacion.html", context)
    if (Perfil == 6):
        print ("Entre por dende ERA")
        return render(request, "admisiones/panelAdmisiones.html", context)

    return render(request, "admisiones/panelAdmisiones.html", context)


def RetornarMen(request, Sede, Username,  Documento, NombreSede, Profesional):

    print("Voy a RETORNAR AL MENU")

    context = {}
    username = Username.strip()

    documento = Documento
    sede = Sede
    nombreSede = NombreSede
    profesional = Profesional


    username = Username
    username = username.strip()
    print(username)
    print(sede)
    print(nombreSede)
    print(profesional)
    print(username)


    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    context['Documento'] = username
    context['Username'] = username
    context['Sede'] = sede
    context['NombreSede'] = nombreSede
    context['Profesional'] = profesional

    # Combo PermisosGrales

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(username) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

    curt.execute(comando)
    print("CONSULTA PERMISOS GENERALES = " ,comando)

    permisosGrales = []

    for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
        permisosGrales.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
             'modulo_nombre': modulo_nombre})

    miConexiont.close()
    print(permisosGrales)

    context['PermisosGrales'] = permisosGrales

    # Fin Combo PermisosGrales

    # Combo PermisosDetalle

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'" + username + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

    curt.execute(comando)
    print(comando)

    permisosDetalle = []

    for id, nombre, nomenclatura, logo, nombreOpcion, nombreElemento in curt.fetchall():
        permisosDetalle.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion': nombreOpcion,
             'nombreElemento': nombreElemento})

    miConexiont.close()
    print(permisosDetalle)

    context['PermisosDetalle'] = permisosDetalle

    # Fin Combo PermisosDetalle

    # Consigo la sede Nombre

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id, nombre   FROM sitios_sedesClinica WHERE id ='" + sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for id, nombre  in cur.fetchall():
        nombreSede.append({'id':id , 'nombre' : nombre})

    miConexion.close()
    print("ESTA ES EL NOMBRE DE LA SEDE :")
    print (nombreSede[0]['nombre'])
    #
    context['NombreSede'] =  nombreSede[0]['nombre']

    # esta consulta por que se pierde de otras pantallas

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT id ,nombre FROM sitios_sedesClinica"
    cur.execute(comando)
    print(comando)

    sedes = []

    for id, nombre in cur.fetchall():
        sedes.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(sedes)

    context['Sedes'] = sedes

    miConexion0 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur0 = miConexion0.cursor()
    comando = 'select p.id  Username_id , p.nombre profesional , p."sedesClinica_id" , p.contrasena contrasena from planta_planta p where p.documento = ' + "'"  + username + "'" + ' AND p."sedesClinica_id" = ' + "'" + str(sede) + "'"
    cur0.execute(comando)
    print(comando)
    planta = []
    profesional = ''

    for Username_id, profesional, sedesClinica_id , contrasena in cur0.fetchall():
        planta.append({'Username_id': Username_id, 'profesional': profesional, 'sedesClinica_id': sedesClinica_id, 'contrasena':contrasena})
        context['Username_id'] = Username_id
        profesional = profesional

    context['Profesional'] = profesional
    print ("Profesional = ", context['Profesional'] )
    miConexion0.close()

    # Combo Modulos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

    curt.execute(comando)
    print(comando)

    modulos = []

    for id, nombre, nomenclatura, logo in curt.fetchall():
        modulos.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo})

    miConexiont.close()
    print(modulos)

    context['Modulos'] = modulos

    # Fin combo Modulos

    print ("Voy de Regreso Context = ", context)

    return render(request, "inicio/PantallaPrincipal.html", context)


def validaPassword(request, username, contrasenaAnt,contrasenaNueva,contrasenaNueva2):
    print("Entre ValidaPassword" )
    username = request.POST["username"]
    contrasenaAnt = request.POST["contrasenaAnt"]
    contrasenaNueva = request.POST["contrasenaNueva"]
    contrasenaNueva2 = request.POST["contrasenaNueva2"]

    print(username)
    print(contrasenaAnt)
    print(contrasenaNueva)
    print(contrasenaNueva2)
    context = {}

    if (contrasenaNueva2 != contrasenaNueva):
        dato = "No coinciden las contraseñas ! "
        context['Error'] = "No coincideln las contraseñas ! "
        print(context)

        return HttpResponse(dato)



    miConexion1 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur1 = miConexion1.cursor()
    comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
    print(comando)
    cur1.execute(comando)

    UsuariosHc = []

    for documento, contrasena in cur1.fetchall():
        UsuariosHc = {'username': documento, 'contrasena': contrasena}

    miConexion1.close()
    print(UsuariosHc)

    if UsuariosHc == []:

        dato = "Personal invalido ! "
        context['Error'] = "Personal invalido ! "
        print(context)

        return HttpResponse(dato)
        #return render(request, "accesoPrincipal1.html", context)

    else:
        miConexion1 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "' AND contrasena = '" + str(contrasenaAnt) + "'"
        print(comando)
        cur1.execute(comando)

        ContrasenaHc = []
        for documento, contrasena in cur1.fetchall():
            ContrasenaHc = {'username': documento, 'contrasena': contrasena}
        miConexion1.close()

        if ContrasenaHc == []:
            dato = "Contraseña Invalida ! "
            context['Error'] = "Contraseña Invalida ! "
            print(context)

            return HttpResponse(dato)

        else:

            miConexion1 =psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
            cur1 = miConexion1.cursor()
            comando = "UPDATE planta_planta SET contrasena = '" +  str(contrasenaNueva) + "' WHERE documento = '" + str(username) + "'"
            print(comando)
            cur1.execute(comando)
            miConexion1.commit()
            miConexion1.close()
            context['Error'] = "Contraseña Actualizada ! "
            dato = "Contraseña Actualizada !"
            print(context)
            #return HttpResponse(context, safe=False)
            return HttpResponse(dato)
            #return render(request, "accesoPrincipal1.html", context)


    #return JsonResponse(UsuariosHc, safe=False)

def Modal(request, username, password):

        print("Entre a Modal")
        print(username)
        print(password)


        miConexion1 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        cur1 = miConexion1.cursor()
        comando = "SELECT documento,contrasena FROM planta_planta WHERE documento = '" + str(username) + "'"
        print(comando)
        cur1.execute(comando)

        UsuariosHc = {}

        for documento, contrasena in cur1.fetchall():
            UsuariosHc = {'username': documento, 'contrasena': contrasena}

        miConexion1.close()
        print(UsuariosHc)
        return JsonResponse(UsuariosHc, safe=False)
        # return HttpResponse(UsuariosHc)



def buscarAdmision(request):
    context = {}

    ## ULTIMOS AJUSTES

    print("Entre Buscar Admision" )
    BusTipoDoc = request.POST["busTipoDoc"]
    BusDocumento = request.POST["busDocumento"]
    BusHabitacion = request.POST["busHabitacion"]
    BusDesde = request.POST["busDesde"]
    BusHasta = request.POST["busHasta"]
    BusEspecialidad = request.POST["busEspecialidad"]
    print ("Especialidad = ", BusEspecialidad )
    BusMedico = request.POST["busMedico"]
    BusServicio = request.POST["busServicio"]
    BusSubServicio = request.POST["busSubServicio"]
    BusPaciente = request.POST["busPaciente"]
    #Perfil = request.POST['Perfil']

    Sede = request.POST["sede"]
    sede = request.POST["sede"]
    context['Sede'] = Sede

    # Consigo la sede Nombre

    miConexion = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur = miConexion.cursor()
    comando = "SELECT nombre   FROM sitios_sedesClinica WHERE id ='" + Sede + "'"
    cur.execute(comando)
    print(comando)

    nombreSedes = []

    for nombre in cur.fetchall():
        nombreSedes.append({'nombre': nombre})

    miConexion.close()
    print(nombreSedes)
    nombresede1 = nombreSedes[0]

    context['NombreSede'] = nombresede1

    username = request.POST["username"]
    context['Username'] = username
    print("Sede  = ", Sede)
    print("BusHabitacion= ", BusHabitacion)
    print("BusTipoDoc=", BusTipoDoc)
    print("BusDocumento=" , BusDocumento)
    print("BusDesde=", BusDesde)
    print("BusHasta=", BusHasta)
    print("La sede es = " , Sede)
    print("El busServicio = ", BusServicio)
    print("El busSubServicio = ", BusSubServicio)
    print("El busEspecialidad = ", BusEspecialidad)
    print("El busSMedico = ", BusMedico)
    print("El busSMedico = ", BusPaciente)

    ## Combos para Contexto

    # aqui la manada de combos organizarlo segun necesidades

    ingresos = []


    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()


    detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null'
    print(detalle)

    curx.execute(detalle)

    for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
        ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                         'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                         'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                         'DxActual': dxActual})

    miConexionx.close()
    print(ingresos)
    context['Ingresos'] = ingresos

    # Combo de Servicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id'
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id"'
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios

    # Fin combo SubServicios

    # Combo TiposDOc

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
    curt.execute(comando)
    print(comando)

    tiposDoc = []
    tiposDoc.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDoc.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDoc)

    context['TiposDoc'] = tiposDoc

    # Fin combo TiposDOc

    # Combo Habitaciones

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    context['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    # Combo Especialidades

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = "SELECT id ,nombre FROM clinico_Especialidades"
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

    # Combo EspecialidadesMedicos


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' + "'" + str(username) + "' AND " + 'em."sedesClinica_id" = ' + "'" + str(sede) + "'"
    curt.execute(comando)
    print(comando)

    especialidadesMedicos = []
    especialidadesMedicos.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        especialidadesMedicos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(especialidadesMedicos)

    context['EspecialidadesMedicos'] = especialidadesMedicos

    # Fin combo EspecialidadesMedicos
    # Combo Medicos

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT p.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str('MEDICO') + "'" + ' and med.planta_id = p.id'

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

    # Combo TiposFolio


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

    curt.execute(comando)
    print(comando)

    tiposFolio = []
    tiposFolio.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposFolio.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposFolio)

    context['TiposFolio'] = tiposFolio

    # Fin combo TiposFolio

    # Combo TiposUsuario


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

    curt.execute(comando)
    print(comando)

    tiposUsuario = []
    # tiposUsuario.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposUsuario.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposUsuario)

    context['TiposUsuario'] = tiposUsuario

    # Fin combo Tipos Usuario

    # Combo TiposDocumento


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p"

    curt.execute(comando)
    print(comando)

    tiposDocumento = []
    tiposDocumento.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        tiposDocumento.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['TiposDocumento'] = tiposDocumento

    # Fin combo TiposDocumento

    # Combo Centros


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p"

    curt.execute(comando)
    print(comando)

    centros = []
    centros.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        centros.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposDocumento)

    context['Centros'] = centros

    # Fin combo Centros

    # Combo Diagnosticos


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT p.id id, p.nombre||' + "' '||" + 'cie10  nombre FROM clinico_diagnosticos p'

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

    # Combo Departamentos


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d"

    curt.execute(comando)
    print(comando)

    departamentos = []
    # tiposDocumento.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        departamentos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(departamentos)

    context['Departamentos'] = departamentos

    # Fin combo Departamentos

    # Combo Ciudades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

    curt.execute(comando)
    print(comando)

    ciudades = []

    for id, nombre in curt.fetchall():
        ciudades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ciudades)

    context['Ciudades'] = ciudades

    # Fin combo Ciudades

    # Combo Modulos


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

    curt.execute(comando)
    print(comando)

    modulos = []

    for id, nombre, nomenclatura, logo in curt.fetchall():
        modulos.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo})

    miConexiont.close()
    print(modulos)

    context['Modulos'] = modulos

    # Fin combo Modulos

    # Combo PermisosGrales

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()


    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
        username) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

    curt.execute(comando)
    print(comando)

    permisosGrales = []

    for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
        permisosGrales.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
             'modulo_nombre': modulo_nombre})

    miConexiont.close()
    print(permisosGrales)

    context['PermisosGrales'] = permisosGrales

    # Fin Combo PermisosGrales

    # Combo PermisosDetalle

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'" + username + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

    curt.execute(comando)
    print(comando)

    permisosDetalle = []

    for id, nombre, nomenclatura, logo, nombreOpcion, nombreElemento in curt.fetchall():
        permisosDetalle.append(
            {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion': nombreOpcion,
             'nombreElemento': nombreElemento})

    miConexiont.close()
    print(permisosDetalle)

    context['PermisosDetalle'] = permisosDetalle

    # Fin Combo PermisosDetalle

    # Combo Vias Ingreso


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_viasingreso c"

    curt.execute(comando)
    print(comando)

    viasIngreso = []

    for id, nombre in curt.fetchall():
        viasIngreso.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(viasIngreso)

    context['ViasIngreso'] = viasIngreso

    # Fin combo vias Ingreso

    # Combo Causas Externa


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_causasExterna c"

    curt.execute(comando)
    print(comando)

    causasExterna = []

    for id, nombre in curt.fetchall():
        causasExterna.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(causasExterna)

    context['CausasExterna'] = causasExterna

    # Fin combo causasExterna

    # Combo Regimenes


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_regimenes c"

    curt.execute(comando)
    print(comando)

    regimenes = []

    for id, nombre in curt.fetchall():
        regimenes.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(regimenes)

    context['Regimenes'] = regimenes

    # Fin combo regimenes


    # Combo Tipos Cotizante


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM clinico_tiposcotizante c"

    curt.execute(comando)
    print(comando)

    tiposCotizante = []

    for id, nombre in curt.fetchall():
        tiposCotizante.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(tiposCotizante)

    context['TiposCotizante'] = tiposCotizante

    # Fin combo tiposCotizante

    # Combo municipios


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM sitios_municipios c"

    curt.execute(comando)
    print(comando)

    municipios = []

    for id, nombre in curt.fetchall():
        municipios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(municipios)

    context['Municipios'] = municipios

    # Fin combo municipios

    # Combo localidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM sitios_localidades c"

    curt.execute(comando)
    print(comando)

    localidades = []

    for id, nombre in curt.fetchall():
        localidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(localidades)

    context['Localidades'] = localidades

    # Fin combo localidades


    # Combo estadoCivil


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM basicas_estadocivil c"

    curt.execute(comando)
    print(comando)

    estadoCivil = []

    for id, nombre in curt.fetchall():
        estadoCivil.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(estadoCivil)

    context['EstadoCivil'] = estadoCivil

    # Fin combo estadoCivil


    # Combo ocupaciones


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id,c.nombre nombre FROM basicas_ocupaciones c"

    curt.execute(comando)
    print(comando)

    ocupaciones = []

    for id, nombre in curt.fetchall():
        ocupaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ocupaciones)

    context['Ocupaciones'] = ocupaciones

    # Fin combo ocupaciones

    ## fin manada de combis

    ## Fin Combos para contexto


    miConexion1 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur1 = miConexion1.cursor()

    detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd , sitios_subServiciosSedes sub  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and sd."sedesClinica_id" = sub."sedesClinica_id" and  sub."sedesClinica_id" =  i."sedesClinica_id"   and  sub."sedesClinica_id" = dep."sedesClinica_id" and dep.id = i."dependenciasActual_id"  and dep."subServiciosSedes_id" = sub.id  and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
        Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosIng_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null'


    print(detalle)

    desdeTiempo = BusDesde[11:16]
    hastaTiempo = BusHasta[11:16]
    desdeFecha = BusDesde[0:10]
    hastaFecha = BusHasta[0:10]

    print ("desdeTiempo = ", desdeTiempo)
    print("desdeTiempo = " ,hastaTiempo)

    print (" desde fecha = " , desdeFecha)
    print("hasta  = ", hastaFecha)


    if BusServicio != "":
      detalle = detalle + " AND  ser.id = '" + str(BusServicio) + "'"
    print(detalle)

    if BusSubServicio != "":
      detalle = detalle + " AND  sub.id = '" + str(BusSubServicio) + "'"
    print(detalle)


    if BusDesde != "":
        detalle = detalle +  ' AND i."fechaIngreso" >= ' + "'" + str(desdeFecha) +   " " + str(desdeTiempo)  + ":00" + "'"
        print (detalle)

    if BusHasta != "":
        detalle = detalle + ' AND i."fechaIngreso" <=  ' + "'"  + str(hastaFecha) +  " " + str(hastaTiempo) + ":00" +"'"
        print(detalle)

    if BusHabitacion != "":
        detalle = detalle + " AND dep.id = '" + str(BusHabitacion) + "'"
        print(detalle)

    if BusTipoDoc != "":
        detalle = detalle + ' AND i."tipoDoc_id"= ' + "'" +  str(BusTipoDoc) + "'"
        print(detalle)

    if BusDocumento != "":
        detalle = detalle + " AND u.documento= '" + str(BusDocumento) + "'"
        print(detalle)

    if BusPaciente != "":
        detalle = detalle + " AND u.nombre like '%" + str(BusPaciente) + "%'"
        print(detalle)

    if BusMedico != "":
        detalle = detalle + ' AND i."medicoActual_id" = ' + "'"   + str(BusMedico) + "'"
        print(detalle)


    if BusEspecialidad != "":
        detalle = detalle + ' AND i."dxIngreso_id" = ' + "'" +  str(BusEspecialidad) + "'"
        print(detalle)


    cur1.execute(detalle)

    ingresos = []

    for tipoDoc, documento_id, nombre , consec, fechaIngreso,  fechaSalida, servicioNombreIng, camaNombreIng, dxActual  in cur1.fetchall():
        ingresos.append ({'tipoDoc' : tipoDoc, 'Documento': documento_id, 'Nombre': nombre , 'Consec': consec, 'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida, 'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng, 'DxActual': dxActual})

    miConexion1.close()


    print(ingresos)
    context['Ingresos'] = ingresos

    return render(request, "admisiones/panelAdmisiones.html", context)

def buscarServicios(request):
    context = {}
    Sede = request.GET["Sede"]
    print("Entre buscar  servicio =", Serv)
    print("Sede = ", Sede)
    # Combo de Servicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT sed.id id ,sed.nombre nombre FROM  sitios_serviciosSedes sed Where sed."sedesClinica_id" =' + "'" + str(Sede) + "'"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    context['Servicios'] = servicios

    context['Sede'] = Sede

    return JsonResponse(json.dumps(servicios), safe=False)



def buscarSubServicios(request):
    context = {}
    Serv = request.GET["serv"]
    Sede = request.GET["sede"]
    print ("Entre buscar  Subservicios PLAS del servicio  =",Serv)
    print ("Sede = ", Sede)

    # Combo de SubServicios

    miConexiont =psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    #comando = 'SELECT sub.id id ,sub.nombre nombre FROM sitios_serviciosSedes sed ,sitios_subserviciossedes sub , clinico_servicios serv Where sed."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' and sed."sedesClinica_id" = sub."sedesClinica_id" and sed.id = sub."serviciosSedes_id"  and serv.id = ' + "'" + str(Serv) + "'" + ' and sub."serviciosSedes_id" = sed.id and serv.id = sed.servicios_id'
    comando = 'SELECT sub.id id ,sub.nombre nombre FROM sitios_serviciosSedes sed ,sitios_subserviciossedes sub , clinico_servicios serv Where sed."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' and sed."sedesClinica_id" = sub."sedesClinica_id" and sed.id = sub."serviciosSedes_id"  and sed.id = ' + "'" + str(Serv) + "'" + ' and sub."serviciosSedes_id" = sed.id and serv.id = sed.servicios_id'
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)

    context['SubServicios'] = subServicios


    context['Sede'] = Sede


    return JsonResponse(json.dumps(subServicios), safe=False)

def buscarPaises(request):
    context = {}
    Pais = request.GET["Pais"]

    print ("Entre buscar  deptos del Pais    =",Pais)


    # Combo de Medicos Especialidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_paises d, sitios_departamentos c WHERE c.pais_id = d.id and d.id = '" + str(Pais) + "' ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    deptos = []

    for id, nombre in curt.fetchall():
        deptos.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(deptos)


    context['Departamentos'] = deptos


    return JsonResponse(json.dumps(deptos), safe=False)


def buscarCiudades(request):
    context = {}
    Departamento = request.GET["Departamento"]

    print ("Entre buscar  Ciudades del Depto  =",Departamento)


    # Combo de Medicos Especialidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_departamentos d, sitios_ciudades c WHERE c.departamentos_id = d.id and d.id = '" + str(Departamento) + "' ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    ciudades = []

    for id, nombre in curt.fetchall():
        ciudades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(ciudades)


    context['Ciudades'] = ciudades


    return JsonResponse(json.dumps(ciudades), safe=False)


def buscarEspecialidadesMedicos(request):
    context = {}
    Esp = request.GET["Esp"]
    Sede = request.GET["Sede"]
    print ("Entre buscar  Especialidad =",Esp)
    print ("Sede = ", Sede)

    # Combo de Medicos Especialidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()


    comando = 'SELECT m.id id, pla.nombre nombre from clinico_medicos m, clinico_Especialidadesmedicos medesp,clinico_especialidades esp,sitios_sedesclinica sed,  planta_planta pla where  pla.id=medesp.planta_id and  medesp.especialidades_id = esp.id and m.planta_id = pla.id and  esp.id = ' + "'" + str(
        Esp) + "'" + ' and esp.id=medesp.especialidades_id and pla."sedesClinica_id" = sed.id and pla.id = medesp.planta_id and pla."sedesClinica_id"=' + "'" + str(
        Sede) + "'" + ' order by pla.nombre'

    curt.execute(comando)
    print(comando)

    medicosEspecialidades = []


    for id, nombre in curt.fetchall():
        medicosEspecialidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(medicosEspecialidades)

    context['MedicosEspecialidades'] = medicosEspecialidades

    context['Sede'] = Sede

    return JsonResponse(json.dumps(medicosEspecialidades), safe=False)



def buscarHabitaciones(request):


    context = {}
    Exc = request.GET["Exc"]
    print ("Excluir = ", Exc)
    Serv = request.GET["serv"]
    SubServ = request.GET["subServ"]
    Sede = request.GET["sede"]
    print ("Entre buscar  servicio =",Serv)
    print("Entre buscar Subservicio =", SubServ)
    print ("Sede = ", Sede)


    # Busco la habitaciones de un Servicio


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    if Exc == 'N':

      comando = "SELECT dep.id id ,dep.numero nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub , sitios_dependencias dep  Where sed.sedesClinica_id ='" + str(
        Sede) + "' AND sed.servicios_id = ser.id and  sed.sedesClinica_id = sub.sedesClinica_id and sed.servicios_id =sub.servicios_id and  dep.sedesClinica_id=sed.sedesClinica_id and dep.servicios_id = sub.servicios_id and dep.subServicios_id =sub.id  and dep.subServicios_id = '" +str(SubServ) + "'" + ' and dep.disponibilidad = ' + "'" + 'L' + "'"

    else:

       comando = 'SELECT dep.id id ,dep.numero nombre   FROM sitios_serviciosSedes sed,  sitios_subserviciossedes sub , sitios_dependencias dep ,  sitios_dependenciasTipo tip   Where sed."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND sed."sedesClinica_id" = sub."sedesClinica_id" and sub."serviciosSedes_id" = sed.id and dep."sedesClinica_id"=sed."sedesClinica_id" and dep."serviciosSedes_id"= sed.id and dep."subServiciosSedes_id" = sub.id and dep."subServiciosSedes_id" = ' + "'" + str(SubServ) + "'" + ' and dep.disponibilidad = ' + "'" + 'L' +  "'" + ' and tip.id=dep."dependenciasTipo_id" and tip.nombre = ' + "'" + str('HABITACIONES') + "'"
    curt.execute(comando)
    print(comando)

    Habitaciones =[]

    for id, nombre in curt.fetchall():
        Habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(Habitaciones)
    context['Habitaciones'] = Habitaciones

    context['Sede'] = Sede



    return JsonResponse(json.dumps(Habitaciones), safe=False)

# aqui nuevo codigo cvrear admision DEF


def crearAdmisionDef(request):

    print("Entre a Craer Admision definitiva")

    if request.method == 'POST':
        print("EntrePost Graba Admision Def")
        data = {}
        context = {}

        #sedesClinica = request.POST['sedesClinica']
        sedesClinica = request.POST['Sede']
        Sede = request.POST['Sede']
        sede = request.POST['Sede']
        context['Sede'] = Sede

        NombreSede = request.POST['nombreSede']
        nombreSede = request.POST['nombreSede']

        print("Sedes Clinica = ", sedesClinica)
        print ("Sede = ",Sede)


        username = request.POST["username"].strip()
        print(" Username = " , username)
        context['Username'] = username



        Profesional = request.POST["profesional"]
        print(" Profesional = " , Profesional)
        context['Profesional'] = Profesional

        empresa = request.POST["empresaC"]
        print(" empresa = ", empresa)

        convenio = request.POST["conveniosC"]
        print(" convenio = ", convenio)

        serviciosAdministrativos = request.POST["serviciosAdministrativos"]
        print(" serviciosAdministrativos = ", serviciosAdministrativos)



        Username_id = request.POST["username_id"]
        print("Username_id = ", Username_id)
        context['Username_id'] = Username_id

        busServicio2 = request.POST["busServicio22"]
        print(" busServicio2 = ", busServicio2)
        context['BusServicio2'] = busServicio2

        tipoDoc = request.POST['tipoDoc22']
        documento = request.POST['busDocumentoSel22'].strip()
        print("tipoDoc = ", tipoDoc)
        print("documento = ", documento)

        # Consigo el Id del Paciente Documento

        DocumentoId = Usuarios.objects.get(tipoDoc_id=tipoDoc,   documento=documento.strip())
        idPacienteFinal = DocumentoId.id

        print("idPacienteFinal", idPacienteFinal)

        consec = Ingresos.objects.all().filter(tipoDoc_id=tipoDoc).filter(documento_id=idPacienteFinal).aggregate(maximo=Coalesce(Max('consec'), 0))
        print("ultimo Ingreso = ", consec)
        consecAdmision = (consec['maximo'] + 1)
        print("ultimo ingreso = ", consecAdmision)


        fechaRegistro = timezone.now()


        fechaIngreso = fechaRegistro
        print("fechaIngreso = ", fechaIngreso)

        #fechaSalida = "0001-01-01 00:00:00"

        factura = 0
        numcita = 0
        dependenciasIngreso = request.POST['dependenciasIngreso22']
        print("dependenciasIngreso =", dependenciasIngreso)
        #dependenciasActual = dependenciasIngreso
        dependenciasSalida = ""
        dxIngreso = request.POST['dxIngreso']
        print("dxIngreso =", dxIngreso)
        dxActual = dxIngreso
        dxSalida = ""
        estadoSalida = "1"

        medicoIngreso = request.POST['medicoIngresoPP']
        print("medicoIngreso =", medicoIngreso)
        medicoActual = medicoIngreso
        medicoSalida = ""
        salidaClinica = "N"
        salidaDefinitiva = "N"

        especialidadesMedicosP = request.POST['busEspecialidad']
        medicoIngresoId = Medicos.objects.get(id=medicoIngreso)
        especialidadesMedicosQ = EspecialidadesMedicos.objects.get(planta_id=medicoIngresoId.planta_id, especialidades_id = especialidadesMedicosP)
        especialidadesMedicos = especialidadesMedicosQ.id

        especialidadesMedicosSalida = ""
        especialidadesMedicosActual = especialidadesMedicos


        usuarioRegistro = Username_id

        print("usuarioRegistro =", usuarioRegistro)

        if 'checkAutorizacionHospitalizacion' in request.POST:

           checkAutorizacionHospitalizacion = 'S'

        else:

           checkAutorizacionHospitalizacion = 'N'

        fechaRegistro = fechaIngreso

        estadoReg = "A"
        print("estadoRegistro =", estadoReg)

        data[0] = "Ha ocurrido un error"

        # VAmos a guardar la Admision

        # Consigo ID de Documento

        documento_llave = Usuarios.objects.get(tipoDoc_id=tipoDoc,   documento=documento.strip())
        print("el id del dopcumento = ", documento_llave.id)

        usernameId = Planta.objects.get(documento=username, sedesClinica_id=sede)
        print("el id del planta = ", usernameId.id)

        viasIngreso   = request.POST["viasIngreso"]
        context['ViasIngreso'] = viasIngreso
        causasExterna = request.POST["causasExterna"]
        context['CausasExterna'] = causasExterna
        regimenes = request.POST["regimenes"]
        context['Regimenes'] = regimenes
        tiposCotizante = request.POST["tiposCotizante"]
        context['TiposCotizante'] = tiposCotizante
        ipsRemite = request.POST["ips"]
        numManilla = request.POST["numManilla"]
        remitido = request.POST["remitido"]
        #print("empresaId= ", empresaId)
        print("numManilla = ", numManilla)
        print("ipsRemite = ", ipsRemite)
        print("remitido = ", remitido)

        # DATOS DE RIPS
        ripsServiciosIng = request.POST['ripsServiciosIng']
        ripsmodalidadGrupoServicioTecSal = request.POST['ripsmodalidadGrupoServicioTecSal']
        ripsViaIngresoServicioSalud = request.POST['ripsViaIngresoServicioSalud']
        ripsGrupoServicios = request.POST['ripsGrupoServicios']
        ripsCondicionDestinoUsuarioEgreso = request.POST['ripsCondicionDestinoUsuarioEgreso']
        ripsCausaMotivoAtencion = request.POST['ripsCausaMotivoAtencion']
        ripsRecienNacido = request.POST["ripsRecienNacido"]
        ripsPesoRecienNacido = request.POST["ripsPesoRecienNacido"]
        ripsNumConsultasCPrenatal = request.POST["ripsNumConsultasCPrenatal"]
        ripsEdadGestacional = request.POST["ripsEdadGestacional"]
        ripsDestinoUsuarioEgresoRecienNacido = request.POST['ripsDestinoUsuarioEgresoRecienNacido']
        ripsFinalidadConsulta = request.POST['ripsFinalidadConsulta']
        print("ripsFinalidadConsulta", ripsFinalidadConsulta)

        ripsDestinoUsu1 = RipsDestinoEgreso.objects.get(id= ripsDestinoUsuarioEgresoRecienNacido)

        ## DESDE AQUIP TRANSACCIONALIDAD

        try:
            with transaction.atomic():
                grabo = Ingresos(
                                 sedesClinica_id=Sede,
                                 tipoDoc_id=tipoDoc,
                                 documento_id=documento_llave.id,
                                 consec=consecAdmision,
                                 fechaIngreso=fechaIngreso,
                                 empresa_id=empresa,
                                 #fechaSalida=NULL,
                                 factura=factura,
                                 numcita=numcita,
                                 serviciosAdministrativos_id=serviciosAdministrativos,
                                 serviciosIng_id=  busServicio2,
                                 dependenciasIngreso_id=dependenciasIngreso,
                                 dxIngreso_id=dxIngreso,
                                 medicoIngreso_id=medicoIngreso,
                                 especialidadesMedicosIngreso_id=especialidadesMedicos,
                                 serviciosActual_id=busServicio2,
                                 dependenciasActual_id=dependenciasIngreso,
                                 dxActual_id = dxIngreso,
                                 medicoActual_id=medicoIngreso,
                                 especialidadesMedicosActual_id=especialidadesMedicos,
                                 #dependenciasSalida_id = dependenciasSalida,
                                 #dxSalida_id = dxSalida,
                                 #medicoSalida_id=medicoSalida,
                                 #especialidadesMedicosSalida_id="",
                                 #estadoSalida_id = estadoSalida,
                                 ViasIngreso_id=viasIngreso,
                                 causasExterna_id=causasExterna,
                                 regimen_id=regimenes,
                                 tiposCotizante_id=tiposCotizante,
                                 #empresa_id=empresaId,
                                 ipsRemite_id=ipsRemite,
                                 numManilla=numManilla,
                                 #contactoAcompañante_id=contactoAcompanante,
                                 #contactoResponsable_id=contactoResponsable,
                                 remitido=remitido,
                                 #salidaClinica=salidaClinica,
                                 #salidaDefinitiva=salidaDefinitiva,
                                 ripsServiciosIng_id = ripsServiciosIng,
                                 ripsServiciosActual_id=ripsServiciosIng,
                                 ripsmodalidadGrupoServicioTecSal_id = ripsmodalidadGrupoServicioTecSal,
                                 ripsViaIngresoServicioSalud_id = ripsViaIngresoServicioSalud,
                                 ripsGrupoServicios_id = ripsGrupoServicios,
                                 ripsCondicionDestinoUsuarioEgreso_id = ripsCondicionDestinoUsuarioEgreso,
                                 ripsCausaMotivoAtencion_id = ripsCausaMotivoAtencion,
                                 ripsRecienNacido = ripsRecienNacido,
                                 ripsPesoRecienNacido = ripsPesoRecienNacido,
                                 ripsNumConsultasCPrenatal = ripsNumConsultasCPrenatal,
                                 ripsEdadGestacional = ripsEdadGestacional,
                                 ripsDestinoUsuarioEgresoRecienNacido =ripsDestinoUsu1,
                                 ripsFinalidadConsulta_id = ripsFinalidadConsulta,
                                 fechaRegistro=fechaRegistro,
                                 usuarioRegistro_id=usernameId.id,
                                 estadoReg=estadoReg,
                )
                print("Voy a guardar la INFO")

                grabo.save()
                print("yA grabe 2", grabo.id)
                grabo.id
                print("yA grabe" , grabo.id)

                # Grabo Dependencias

                print("Voy a guardar dependencias OJO ESTO ES UN UPDATE")
                # ejemplo
                grabo4 =  Dependencias.objects.filter(id = dependenciasIngreso).update(tipoDoc_id=tipoDoc, documento_id=documento_llave.id, consec=consecAdmision, disponibilidad='O',fechaRegistro=fechaRegistro, fechaOcupacion= fechaRegistro)

                print("Grabe HISTPRICO DEPENDENCIAS")

                # Grabo Dependencia Historico

                print("Voy a guardar HISTORICO dependencias ")

                grabo2 = HistorialDependencias(
                    tipoDoc_id=tipoDoc,
                    documento_id=documento_llave.id,
                    consec=consecAdmision,
                    dependencias_id=dependenciasIngreso,
                    disponibilidad='O',
                    fechaRegistro=fechaRegistro,
                    usuarioRegistro_id=usernameId.id,
                    fechaOcupacion=fechaRegistro,
                    estadoReg=estadoReg

                )
                grabo2.save()
                print("yA grabe dependencias historico", grabo2.id)

                grabo88 = ConveniosPacienteIngresos(
                          tipoDoc_id=tipoDoc,
                          documento_id=documento_llave.id,
                          consecAdmision=consecAdmision,
                          convenio_id=convenio,
                          fechaRegistro = fechaRegistro,
                          usuarioRegistro_id = usernameId.id,
                          estadoReg = estadoReg
                       )
                grabo88.save()
                grabo88.id
                print("yA grabe pacientes ingresos", grabo88.id)
                print("Grabe HISTORICO DEPENDENCIAS")


                # Aqui rutina de radiar autorizacion de hospitalizacion y/o ambulatorios
                #
                estadosAutorizacion = EstadosAutorizacion.objects.get(nombre='PENDIENTE')

                if (checkAutorizacionHospitalizacion=='S'):

                    grabo99 = Autorizaciones(fechaSolicitud=fechaRegistro,
                              fechaModifica=fechaRegistro,
                              estadoReg = estadoReg,
                              convenio_id=convenio,
                              empresa_id = empresa ,
                              estadoAutorizacion_id= estadosAutorizacion.id,
                              plantaOrdena_id=usernameId.id,
                              sedesClinica_id=Sede,
                              serviciosAdministrativos_id = serviciosAdministrativos,
                              fechaRegistro = fechaRegistro,
                              usuarioRegistro_id = usernameId.id,
                              observaciones='AUTORIZACION HOSPITALARIA',			  
                              ingreso_id= grabo.id,
                           )
                    grabo99.save()
                    grabo99.id
                    print("yA grabe Autorizaciones", grabo99.id)


                    grabo77 = AutorizacionesDetalle(
                              cantidadSolicitada=1,
                              estadoAutorizacion_id= estadosAutorizacion.id,
                              fechaRegistro = fechaRegistro,
                              estadoReg = estadoReg,
                              autorizaciones_id = grabo99.id,
                              usuarioRegistro_id = usernameId.id
                           )
                    grabo77.save()
                    grabo77.id
                    print("yA grabe Autorizaciones detalle", grabo77.id)

                    grabo101 = Ingresos.objects.filter(id=grabo.id).update(autorizacionesHospitalDetalle_id=grabo77.id)

                else:
                    pass


        except Exception as e:
            # Aquí ya se hizo rollback automáticamente
            print("Se hizo rollback por:", e)
            datosMensaje = {'success': False, 'Mensaje': e}
            json_data = json.dumps(datosMensaje, default=str)
            return HttpResponse(json_data, content_type='application/json')




        # HASTA AQUIP TRANSACCIONALIDAD

        # Aqui reporte de inicial URGENCIAS, pero ojo se suspende porque tiene que tener TRIAGE

        #servicioUrgencias = Servicios.objects.get(id=busServicio2)


        #if servicioUrgencias.nombre == 'URGENCIAS':
        #    print("Entre imprimir inicial UREGNCIAS")
        #    ingresoId2 = grabo.id
        #    ImprimirAtencionInicialUrgencias(ingresoId2)

        # Aqui reporte de Hoja de Admision

        servicioHospitalizacion = ServiciosSedes.objects.get(id=busServicio2)


        if servicioHospitalizacion.nombre == 'HOSPITALIZACION':
            print("Entre imprimir Hoja de admision paciente")
            ingresoId2 = grabo.id
            ImprimirHojaAdmision(ingresoId2)

        # RUTINA ARMADO CONTEXT
        #
        #
        ingresos = []

        miConexionx =  psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        curx = miConexionx.cursor()

        detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
            Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and  i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null'

        print(detalle)

        curx.execute(detalle)

        for tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        ## ojo desde aquip


        # Combo PermisosGrales

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
        comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
            username) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

        curt.execute(comando)
        print(comando)

        permisosGrales = []

        for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
            permisosGrales.append(
                {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
                 'modulo_nombre': modulo_nombre})

        miConexiont.close()
        print(permisosGrales)

        # Fin Combo PermisosGrales
        print("permisosGrales= ", permisosGrales)

        context = {}
        context['PermisosGrales'] = permisosGrales
        context['Documento'] = documento
        context['Username'] = username
        context['Profesional'] = Profesional
        context['Sede'] = Sede
        context['PermisosGrales'] = permisosGrales
        context['NombreSede'] = NombreSede
        context['NombreSede'] = nombreSede

        # Combo Accesos usuario

        #miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
        #                               password="123456")
        #curt = miConexiont.cursor()

        # comando = "select opc.id id_opc, opc.perfilesClinicaId_id id_perfilesClinica,opc.modulosElementosDefId_id id_elmentosDef, elem_nombre, elem.url url ,modelem.nombre nombreElemento from seguridad_perfilesusu usu, seguridad_perfilesclinicaopciones opc, planta_planta planta, seguridad_moduloselementosdef elem, seguridad_moduloselementos modelem where usu.estadoReg = 'A' and usu.plantaId_id =  planta.id and planta.documento = '" + str(username) + "' and opc.id = usu.perfilesclinicaOpcionesId_id and elem.id =opc.modulosElementosDefId_id and modelem.id = opc.modulosElementosDefId_id "
        #comando = 'select opc.id id_opc, opc."perfilesClinicaId_id" id_perfilesClinica,opc."modulosElementosDefId_id" id_elmentosDef,modulos.nombre nombre_modulo ,elem.nombre nombre_defelemento , elem.url url ,modelem.nombre nombreElemento from seguridad_perfilesusu usu, seguridad_perfilesclinicaopciones opc, planta_planta planta, seguridad_moduloselementosdef elem, seguridad_moduloselementos modelem , seguridad_perfilesclinica perfcli, seguridad_perfilesgralusu gralusu, seguridad_modulos modulos, sitios_sedesClinica  sedes where gralusu."perfilesClinicaId_id" = perfcli.id and usu."plantaId_id" = gralusu."plantaId_id" and usu."plantaId_id" =  planta.id and usu."estadoReg" = ' + "'" + 'A' + "'" + ' and  opc.id = usu."perfilesClinicaOpcionesId_id" and elem.id =opc."modulosElementosDefId_id" and modulos.id = perfcli."modulosId_id" and elem."modulosId_id" = perfcli."modulosId_id"  and sedes.id = planta."sedesClinica_id"  and planta.documento =  ' + "'"  + '19465673' + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

        #curt.execute(comando)
        #print(comando)

        #accesosUsuario = []

        #for id_opc, id_perfilesClinica, id_elmentosDef, nombre_modulo, nombre_defelemento, url, nombreElemento in curt.fetchall():
        #    accesosUsuario.append(
        #        {'id_opc': id_opc, 'id_perfilesClinica': id_perfilesClinica, 'id_elmentosDef': id_elmentosDef,
        #         'nombre_modulo': nombre_modulo, 'nombre_defelemento': nombre_defelemento, 'url': url,
        #         'nombreElemento': nombreElemento})

        #miConexiont.close()
        #print(accesosUsuario)

        #context['AccesosUsuario '] = accesosUsuario

        # Fin Accesos usuario

        # aqui la manada de combos organizarlo segun necesidades

        ingresos = []


        miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curx = miConexionx.cursor()
        #detalle = 'SELECT  tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
        #    Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null'
        detalle = 'SELECT i.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , i."fechaSalida", ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and ser.nombre != ' + "'" + str('TRIAGE') + "'" + ' AND dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"'

        print(detalle)

        curx.execute(detalle)

        for id, tipoDoc, documento, nombre, consec, fechaIngreso, fechaSalida, servicioNombreIng, camaNombreIng, dxActual in curx.fetchall():
            ingresos.append({'id':id, 'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre, 'Consec': consec,
                             'FechaIngreso': fechaIngreso, 'FechaSalida': fechaSalida,
                             'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                             'DxActual': dxActual})

        miConexionx.close()
        print(ingresos)
        context['Ingresos'] = ingresos

        # Combo de Servicios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
            sede) + "'" + ' AND sed."servicios_id" = ser.id'
        curt.execute(comando)
        print(comando)

        servicios = []
        servicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            servicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(servicios)

        context['Servicios'] = servicios

        # Fin combo servicios

        # Combo de SubServicios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(
            sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id"'
        curt.execute(comando)
        print(comando)

        subServicios = []
        subServicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            subServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(subServicios)

        context['SubServicios'] = subServicios

        # Fin combo SubServicios

        # Combo TiposDOc

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM usuarios_TiposDocumento "
        curt.execute(comando)
        print(comando)

        tiposDoc = []
        # tiposDoc.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDoc.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDoc)

        context['TiposDoc'] = tiposDoc

        # Fin combo TiposDOc

        # Combo Habitaciones

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = ' SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip where dep."sedesClinica_id" = ' + "'" + str(
            Sede) + "'" + ' AND tip.nombre=' + "'" + str(
            'HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id'
        curt.execute(comando)
        print(comando)

        habitaciones = []
        habitaciones.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            habitaciones.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(habitaciones)

        context['Habitaciones'] = habitaciones

        # Fin combo Habitaciones

        # Combo Especialidades

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()
        comando = "SELECT id ,nombre FROM clinico_Especialidades"
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

       # Combo EspecialidadesMedicos


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT em.id ,e.nombre FROM clinico_Especialidades e, clinico_EspecialidadesMedicos em,planta_planta pl  where em."especialidades_id" = e.id and em."planta_id" = pl.id AND pl.documento = ' + "'" + str(username) + "' AND " + 'em."sedesClinica_id" = ' + "'" + str(sede) + "'"
        curt.execute(comando)
        print(comando)

        especialidadesMedicos = []
        especialidadesMedicos.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
           especialidadesMedicos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(especialidadesMedicos)

        context['EspecialidadesMedicos'] = especialidadesMedicos

        # Fin combo EspecialidadesMedicos
        # Combo Medicos

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre nombre FROM planta_planta p,clinico_medicos med, planta_tiposPlanta tp WHERE p."sedesClinica_id" = ' + "'" + str(
            Sede) + "'" + ' and p."tiposPlanta_id" = tp.id and tp.nombre = ' + "'" + str(
            'MEDICO') + "'" + ' and med.planta_id = p.id'

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

        # Combo TiposFolio


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT e.id id, e.nombre nombre FROM clinico_tiposFolio e"

        curt.execute(comando)
        print(comando)

        tiposFolio = []
        tiposFolio.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposFolio.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposFolio)

        context['TiposFolio'] = tiposFolio

        # Fin combo TiposFolio

        # Combo TiposUsuario


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposusuario p"

        curt.execute(comando)
        print(comando)

        tiposUsuario = []
        # tiposUsuario.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposUsuario.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposUsuario)

        context['TiposUsuario'] = tiposUsuario

        # Fin combo Tipos Usuario

        # Combo TiposDocumento


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM usuarios_tiposDocumento p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        tiposDocumento = []
        # tiposDocumento.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            tiposDocumento.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDocumento)

        context['TiposDocumento'] = tiposDocumento

        # Fin combo TiposDocumento

        # Combo ips

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM clinico_ips c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        ips = []
        ips.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ips.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(ips)

        context['Ips'] = ips

        # Fin combo ips


        # Combo Centros

        # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM sitios_centros p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        centros = []

        for id, nombre in curt.fetchall():
            centros.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposDocumento)

        context['Centros'] = centros

        # Fin combo Centros

        # Combo Diagnosticos


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.id id, p.nombre||' + "' '||" + 'cie10  nombre FROM clinico_diagnosticos p ORDER BY p.nombre'

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

        # Combo Departamentos


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT d.id id, d.nombre  nombre FROM sitios_departamentos d ORDER BY d.nombre"

        curt.execute(comando)
        print(comando)

        departamentos = []
        # tiposDocumento.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            departamentos.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(departamentos)

        context['Departamentos'] = departamentos

        # Fin combo Departamentos

        # Combo Ciudades


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id, c.nombre  nombre FROM sitios_ciudades c"

        curt.execute(comando)
        print(comando)

        ciudades = []

        for id, nombre in curt.fetchall():
            ciudades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(ciudades)

        context['Ciudades'] = ciudades

        # Fin combo Ciudades

        # Combo Modulos


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre, c.nomenclatura nomenclatura, c.logo logo FROM seguridad_modulos c"

        curt.execute(comando)
        print(comando)

        modulos = []

        for id, nombre, nomenclatura, logo in curt.fetchall():
            modulos.append({'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo})

        miConexiont.close()
        print(modulos)

        context['Modulos'] = modulos

        # Fin combo Modulos

        # Combo PermisosGrales

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        # comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + username + "'" + ' and  perfcli."sedesClinica_id" = ' + "'" + str(Sede) + "'"
        comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo ,perfcli."modulosId_id" modulo_id , m.nombre modulo_nombre from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli where planta.id = gral."plantaId_id" and  gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and planta.documento =' + "'" + str(
            username) + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

        curt.execute(comando)
        print(comando)

        permisosGrales = []

        for id, nombre, nomenclatura, logo, modulo_id, modulo_nombre in curt.fetchall():
            permisosGrales.append(
                {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'modulo_id': modulo_id,
                 'modulo_nombre': modulo_nombre})

        miConexiont.close()
        print(permisosGrales)

        context['PermisosGrales'] = permisosGrales

        # Fin Combo PermisosGrales

        # Combo PermisosDetalle

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'select m.id id, m.nombre nombre , m.nomenclatura nomenclatura, m.logo logo, modeledef.nombre nombreOpcion ,elemen.nombre nombreElemento from seguridad_modulos m, seguridad_perfilesgralusu gral, planta_planta planta, seguridad_perfilesclinica perfcli, seguridad_perfilesclinicaopciones perfopc, seguridad_perfilesusu perfdet, seguridad_moduloselementosdef modeledef, seguridad_moduloselementos elemen where planta.id= 1 and  planta.id = gral."plantaId_id" and gral."perfilesClinicaId_id" = perfcli.id and perfcli."modulosId_id" = m.id and gral.id = perfdet."plantaId_id" and perfdet."perfilesClinicaOpcionesId_id" = perfopc.id and perfopc."perfilesClinicaId_id" =perfcli.id and  perfopc."modulosElementosDefId_id" = modeledef.id and elemen.id = modeledef."modulosElementosId_id"  and planta.documento = ' + "'" + username + "'" + ' AND gral."plantaId_id"=planta.id AND planta."sedesClinica_id"=' + "'" + str(sede) + "'"

        curt.execute(comando)
        print(comando)

        permisosDetalle = []

        for id, nombre, nomenclatura, logo, nombreOpcion, nombreElemento in curt.fetchall():
            permisosDetalle.append(
                {'id': id, 'nombre': nombre, 'nomenclatura': nomenclatura, 'logo': logo, 'nombreOpcion': nombreOpcion,
                 'nombreElemento': nombreElemento})

        miConexiont.close()
        print(permisosDetalle)

        context['PermisosDetalle'] = permisosDetalle

        # Fin Combo PermisosDetalle

        # Combo Vias Ingreso


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM clinico_viasingreso c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        viasIngreso = []

        for id, nombre in curt.fetchall():
            viasIngreso.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(viasIngreso)

        context['ViasIngreso'] = viasIngreso

        # Fin combo vias Ingreso

        # Combo Causas Externa


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM clinico_causasExterna c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        causasExterna = []

        for id, nombre in curt.fetchall():
            causasExterna.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(causasExterna)

        context['CausasExterna'] = causasExterna

        # Fin combo causasExterna

        # Combo Regimenes


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM clinico_regimenes c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        regimenes = []

        for id, nombre in curt.fetchall():
            regimenes.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(regimenes)

        context['Regimenes'] = regimenes

        # Fin combo regimenes

        # Combo Tipos Cotizante


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM clinico_tiposcotizante c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        tiposCotizante = []

        for id, nombre in curt.fetchall():
            tiposCotizante.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(tiposCotizante)

        context['TiposCotizante'] = tiposCotizante

        # Fin combo tiposCotizante

        # Combo municipios


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM sitios_municipios c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        municipios = []

        for id, nombre in curt.fetchall():
            municipios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(municipios)

        context['Municipios'] = municipios

        # Fin combo municipios

        # Combo localidades

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM sitios_localidades c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        localidades = []

        for id, nombre in curt.fetchall():
            localidades.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(localidades)

        context['Localidades'] = localidades

        # Fin combo localidades

        # Combo estadoCivil

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM basicas_estadocivil c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        estadoCivil = []

        for id, nombre in curt.fetchall():
            estadoCivil.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(estadoCivil)

        context['EstadoCivil'] = estadoCivil

        # Fin combo estadoCivil

        # Combo ocupaciones

        # iConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id id,c.nombre nombre FROM basicas_ocupaciones c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        ocupaciones = []

        for id, nombre in curt.fetchall():
            ocupaciones.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print(ocupaciones)

        context['Ocupaciones'] = ocupaciones


        # Combo Convenios


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM contratacion_convenios p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        convenios = []

        for id, nombre in curt.fetchall():
            convenios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("convenios", convenios)

        context['Convenios'] = convenios

        # Fin combo Convenios

        # Combo ripsServiciosIng

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_RipsServicios  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsServiciosIng = []
        ripsServiciosIng.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsServiciosIng.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsServiciosIng", ripsServiciosIng)

        context['RipsServiciosIng'] = ripsServiciosIng

        # Fin combo ripsServiciosIng

        # Combo ripsmodalidadGrupoServicioTecSal

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_RipsModalidadAtencion   p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsmodalidadGrupoServicioTecSal = []
        ripsmodalidadGrupoServicioTecSal.append({'id': '', 'nombre': ''})


        for id, nombre in curt.fetchall():
            ripsmodalidadGrupoServicioTecSal.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsmodalidadGrupoServicioTecSal", ripsmodalidadGrupoServicioTecSal)

        context['RipsmodalidadGrupoServicioTecSal'] = ripsmodalidadGrupoServicioTecSal

        # Fin combo ripsmodalidadGrupoServicioTecSal

        # Combo ripsViaIngresoServicioSalud

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsviasingresosalud  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsViaIngresoServicioSalud = []
        ripsViaIngresoServicioSalud.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsViaIngresoServicioSalud.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsViaIngresoServicioSalud", ripsViaIngresoServicioSalud)

        context['RipsViaIngresoServicioSalud'] = ripsViaIngresoServicioSalud

        # Fin combo ripsViaIngresoServicioSalud

        # Combo ripsGrupoServicios

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsGrupoServicios  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsGrupoServicios = []
        ripsGrupoServicios.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsGrupoServicios.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsGrupoServicios", ripsGrupoServicios)

        context['RipsGrupoServicios'] = ripsGrupoServicios

        # Fin combo ripsGrupoServicios

        # Combo ripsCondicionDestinoUsuarioEgreso

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsdestinoegreso  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsCondicionDestinoUsuarioEgreso = []
        ripsCondicionDestinoUsuarioEgreso.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsCondicionDestinoUsuarioEgreso.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsCondicionDestinoUsuarioEgreso", ripsCondicionDestinoUsuarioEgreso)

        context['RipsCondicionDestinoUsuarioEgreso'] = ripsCondicionDestinoUsuarioEgreso

        # Fin combo ripsCondicionDestinoUsuarioEgreso

        # Combo ripsCausaMotivoAtencion

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripscausaexterna  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsCausaMotivoAtencion = []
        ripsCausaMotivoAtencion.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsCausaMotivoAtencion.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsCausaMotivoAtencion", ripsCausaMotivoAtencion)

        context['RipsCausaMotivoAtencion'] = ripsCausaMotivoAtencion

        # Fin combo ripsCausaMotivoAtencion

        # Combo ripsDestinoUsuarioEgresoRecienNacido

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT p.id id, p.nombre  nombre FROM rips_ripsdestinoegreso  p ORDER BY p.nombre"

        curt.execute(comando)
        print(comando)

        ripsDestinoUsuarioEgresoRecienNacido = []
        ripsDestinoUsuarioEgresoRecienNacido.append({'id': '', 'nombre': ''})

        for id, nombre in curt.fetchall():
            ripsDestinoUsuarioEgresoRecienNacido.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("ripsDestinoUsuarioEgresoRecienNacido", ripsDestinoUsuarioEgresoRecienNacido)

        context['RipsDestinoUsuarioEgresoRecienNacido'] = ripsDestinoUsuarioEgresoRecienNacido

        # Fin combo ripsDestinoUsuarioEgresoRecienNacido

        # Combo ripsFinalidadConsulta

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = "SELECT c.id,c.codigo id,c.nombre nombre FROM RIPS_ripsFinalidadConsulta c ORDER BY c.nombre"

        curt.execute(comando)
        print(comando)

        ripsFinalidadConsulta = []

        for id, codigo, nombre in curt.fetchall():
            ripsFinalidadConsulta.append({'id': id, 'codigo': codigo, 'nombre': nombre})

        miConexiont.close()
        print(ripsFinalidadConsulta)

        context['RipsFinalidadConsulta'] = ripsFinalidadConsulta

        # Fin combo ripsFinalidadConsulta

        # Combo Indicadores

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT ser.nombre nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
            sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + str(
            'O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str(
            'N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(
            sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str(
            'TRIAGE') + "'" + ' group by ser.nombre'

        curt.execute(comando)
        print(comando)

        indicadores = []

        for nombre, total in curt.fetchall():
            indicadores.append({'nombre': nombre, 'total': total})
            if (nombre == 'HOSPITALIZACION'):
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

        print("total ", total)

        print("YA PASE INDICADORES")

    # Fin combo Indicadores


    # FIN RUTINA ARMADO CONTEXT


    return render(request, "admisiones/panelAdmisiones.html", context)



# fin nuevo mcodigo crear admison DEF



def crearResponsables(request):
    print("Entre crear Responsables")
    pass


def UsuariosModal(request):
        print("Entre a buscar Usuario para la Modal")

        tipoDoc = request.POST['tipoDoc']
        documento = request.POST['documento']

        print ("documento = " , documento)
        print("tipodoc = " ,tipoDoc)

        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        curt = miConexiont.cursor()
        comando = 'SELECT usu.nombre, usu.documento, usu.genero, usu."fechaNacio" fechaNacio, usu.pais_id pais_id,  usu.departamentos_id, usu.ciudades_id, usu.direccion, usu.telefono, usu.contacto, usu."centrosC_id", usu."tipoDoc_id", usu."tiposUsuario_id", usu.municipio_id municipio, usu.localidad_id localidad, usu."estadoCivil_id" estadoCivil , usu.ocupacion_id ocupacion, correo correo  FROM usuarios_usuarios usu WHERE usu."tipoDoc_id" = ' + "'"  + str(tipoDoc) + "'" + ' AND usu.documento = ' + "'" + str(documento) + "'"
        print(comando)
        curt.execute(comando)

        Usuarios = {}

        for nombre, documento, genero, fechaNacio, pais_id,  departamentos_id, ciudades_id, direccion, telefono, contacto, centrosc_id, tipoDoc_id, tiposUsuario_id, municipio, localidad, estadoCivil, ocupacion, correo  in curt.fetchall():
            Usuarios = {'nombre': nombre, 'documento': documento, 'genero': genero, 'fechaNacio': fechaNacio , 'pais_id' : pais_id,  'departamento' : departamentos_id, 'ciudad': ciudades_id,  'direccion':  direccion, 'telefono' :telefono, 'contacto': contacto, 'centrosc_id':centrosc_id, 'tipoDoc_id':tipoDoc_id,'tiposUsuario_id':tiposUsuario_id,
                        'municipio':municipio, 'localidad':localidad, 'estadoCivil':estadoCivil, 'ocupacion':ocupacion,'correo':correo}

        miConexiont.close()
        print(Usuarios)

        if Usuarios == '[]':
            datos = {'Mensaje' : 'Usuario No existe'}
            return JsonResponse(datos, safe=False)
        else:
            return JsonResponse(Usuarios, safe=False)




def guardarUsuariosModal(request):
    print("Entre a grabar Usuarios Modal")
    tipoDoc_id = request.POST["tipoDoc"]

    documento = request.POST["documento"]
    nombre = request.POST["nombre"]
    print("DOCUMENTO = " ,documento)
    print(nombre)
    primerNombre = request.POST["primerNombre"]
    segundoNombre = request.POST["segundoNombre"]
    primerApellido = request.POST["primerApellido"]
    segundoApellido = request.POST["segundoApellido"]

    genero = request.POST["genero"]
    pais = request.POST["pais"]
    departamento = request.POST["departamentos"]
    ciudad = request.POST["ciudades"]
    fechaNacio = request.POST["fechaNacio"]

    print ("departamento = ", departamento)
    print("ciudad = ", ciudad)
    if (fechaNacio == ''):
         fechaNacio='0001-01-01 00:00:01'
    print("fechaNacio = ", fechaNacio)
    direccion = request.POST["direccion"]
    telefono = request.POST["telefono"]
    contacto = request.POST["contacto"]
    centrosc_id = request.POST["centrosC_id"]
    #quemado por el momento mientras encuentor que pasa
    tiposUsuario_id = request.POST["tiposUsuario"]
    print("DIRECCION = ", direccion)
    print("telefono = ", telefono)
    print("contacto = ", contacto)
    print("centrosc_id = ", centrosc_id)
    municipio  = request.POST['municipios']
    localidad  = request.POST['localidades']
    estadoCivil  = request.POST['estadoCivil']
    ocupaciones  = request.POST['ocupaciones']
    ripsZonaTerritorial  = request.POST['ripsZonaTerritorial']


    if ripsZonaTerritorial == '':
        ripsZonaTerritorial="null"

    if estadoCivil == '':
           estadoCivil="null"

    if pais == '':
           pais="null"


    if ciudad == '':
           ciudad="null"



    if tiposUsuario_id == '':
           tiposUsuario_id="null"


    if tiposUsuario_id == '':
           tiposUsuario_id="null"

    if centrosc_id == '':
           centrosc_id="null"

    if ocupaciones == '':
           ocupaciones="null"

    if primerNombre == '':
           primerNombre="null"
    if segundoNombre == '':
           segundoNombre="null"
    if primerApellido == '':
           primerApellido="null"
    if segundoApellido == '':
           segundoApellido="null"

    ocupacion = request.POST['ocupaciones']
    correo = request.POST["correo"]

    correo = request.POST["correo"]



    print(documento)
    print(tipoDoc_id)


    miConexion11 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    cur11 = miConexion11.cursor()
    comando = 'SELECT usu.id, usu."tipoDoc_id", usu.documento FROM usuarios_usuarios usu WHERE usu."tipoDoc_id" = ' + "'" + str(tipoDoc_id) + "'" + ' AND usu.documento = ' + "'" + str(documento) + "'"

    print(comando)
    cur11.execute(comando)

    Usuarios = []

    for id, tipoDoc_id, documento in cur11.fetchall():
        Usuarios.append({'id': id, 'tipoDoc_id': tipoDoc_id, 'documento': documento})

    miConexion11.close()

    fechaRegistro = timezone.now()

    print ("Usuarios = ", Usuarios)


    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            cur3 = miConexion3.cursor()

            if Usuarios == []:

                 print("Entre a crear")
                 comando = 'insert into usuarios_usuarios (nombre, documento, genero, "fechaNacio", pais_id,  departamentos_id, ciudades_id, direccion, telefono, contacto, "centrosC_id", "tipoDoc_id", "tiposUsuario_id", municipio_id, localidad_id, "estadoCivil_id", ocupacion_id, correo ,"fechaRegistro", "estadoReg","primerNombre","segundoNombre","primerApellido", "segundoApellido", "ripsZonaTerritorial_id") values (' + "'" + str(nombre) + "'" + ' , ' + "'" + str(documento) + "'" + ', ' + "'" + str(genero) + "'" + '  , ' + "'" + str(fechaNacio) + "'" +  ', ' + "'" + str(pais) + "'" + ', ' + "'" + str(departamento) + "'" +  '  , ' + "'" +  str(ciudad) + "'" + '  , ' + "'" +  str(direccion) + "'" + ', ' + "'" + str(telefono) + "'" + ', ' + "'" + str(contacto) + "'" + ', ' +  str(centrosc_id) +  ', ' + "'" + str(tipoDoc_id) + "'" + ', ' + str(tiposUsuario_id) + " , " + "'" + str(municipio) + "'" +   ', ' + "'" + str(localidad) + "'" + ", " + str(estadoCivil)  + ", " + str(ocupaciones) + ", " + "'" + str(correo) + "', " +  "'"  + str(fechaRegistro) + "'"  +  ", 'A'"  + ",'" + str(primerNombre) + "','" + str(segundoNombre)  +  "','" + str(primerApellido) + "','" + str(segundoApellido)  + "','" + str(ripsZonaTerritorial) + "')"
                 print(comando)

            else:
                print("Entre a actualizar")
                comando = 'update usuarios_usuarios set nombre = ' "'" + str(nombre) +  "'"  + ',ciudades_id = ' + "'" + str(ciudad) + "'"  +    ', direccion  = ' + "'" +  str(direccion) + "'"  + ', pais_id = ' + "'" + str(pais) + "'"     + ', departamentos_id = ' + "'" + str(departamento) + "'" + ', genero = ' + "'" + str(genero) + "'"  + ', "fechaNacio" = ' + "'" + str(fechaNacio) + "'"   + ', telefono= ' + "'" + str(telefono) + "'" +  ', contacto= ' + "'" +  str(contacto) + "'" +  ', "centrosC_id"= ' + str(centrosc_id)  + ', "tiposUsuario_id" = ' + str(tiposUsuario_id) + ","   + ' municipio_id = ' + "'" + str(municipio) + "'" +  ', localidad_id = ' + "'" + str(localidad) + "'" + ', "estadoCivil_id"= '  + str(estadoCivil)  + ', ocupacion_id = ' + str(ocupaciones)  + ', correo = ' + "'" + str(correo) + "'" + ', "primerNombre" = ' + "'" + str(primerNombre) + "'," + '"segundoNombre" = ' + "'" + str(segundoNombre) + "'," + '"primerApellido"= ' + "'" + str(primerApellido) + "'," + '"segundoApellido" = ' + "'" + str(segundoApellido)  +"'," + '"ripsZonaTerritorial_id" = ' + "'" + str(ripsZonaTerritorial)  +  "'"  + ' WHERE "tipoDoc_id" = ' + str(tipoDoc_id) + ' AND documento = ' + "'" + str(documento) + "'"
                print(comando)

            cur3.execute(comando)
            miConexion3.commit()
            cur3.close()

            if Usuarios == []:
                return JsonResponse({'success': True, 'Mensaje': 'Paciente Creado !'})
            else:
                return JsonResponse({'success': True, 'Mensaje': 'Paciente Actualizado !'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()
        return JsonResponse({'success': False, 'Mensaje': error})



    finally:
        print("Finally")
        if miConexion3:
            miConexion3.close()
            print("Cerre conexion")



def encuentraAdmisionModal(request):

        ingresoId = request.POST["ingresoId"]
        sede = request.POST["sede"]

        Ingreso = Ingresos.objects.get(id=ingresoId)

        print("Entre a buscar una Admision Modal")
        print("documento = ", Ingreso.documento_id)
        print("tipodoc = ", Ingreso.tipoDoc_id)
        print("consecutivoAdmision = ", Ingreso.consec)
        print("Sede = ", sede)


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT tp.nombre tipoDoc,  u.documento documento, u.nombre  paciente , i.consec consec , i."fechaIngreso" ingreso , i."fechaSalida" salida, ser.nombre servicioNombreIng,subserv.nombre subServicioNombreIng, dep.nombre dependenciasIngreso ,i."medicoIngreso_id" medicoIngreso, i."especialidadesMedicosIngreso_id" espMedico, diag1.nombre diagMedico, i."ViasIngreso_id" viasIngreso, i."causasExterna_id" causasExterna,i.regimen_id regimenes ,i."tiposCotizante_id"  cotizante,i.remitido remitido,i."ipsRemite_id" ips ,i."numManilla" numManilla, i."dxIngreso_id" dxIngreso, "contactoResponsable_id" responsable, "contactoAcompañante_id" acompanante , i.empresa_id empresa  , i."ripsCausaMotivoAtencion_id" ripsCausaMotivoAtencion , "ripsGrupoServicios_id" ripsGrupoServicios, i."ripsmodalidadGrupoServicioTecSal_id" ripsmodalidadGrupoServicioTecSal  , i."ripsViaIngresoServicioSalud_id" ripsViaIngresoServicioSalud , i."ripsServiciosIng_id" ripsServiciosIng, i."ripsCondicionDestinoUsuarioEgreso_id" ripsCondicionDestinoUsuarioEgreso, i."ripsViaIngresoServicioSalud_id" ripsViaIngresoServicioSalud ,i."ripsDestinoUsuarioEgresoRecienNacido_id" ripsDestinoUsuarioEgresoRecienNacido  FROM admisiones_ingresos i inner join usuarios_usuarios u on (u."tipoDoc_id" = i."tipoDoc_id" and u.id = i."documento_id" ) inner join sitios_dependencias dep on (dep."sedesClinica_id" = i."sedesClinica_id" and dep."tipoDoc_id" =  i."tipoDoc_id" and dep.documento_id =i."documento_id"  and dep.consec = i.consec) inner join usuarios_tiposDocumento tp on (tp.id = u."tipoDoc_id") inner join sitios_dependenciastipo deptip on (deptip.id = dep."dependenciasTipo_id") inner join sitios_subserviciossedes subServ ON (subserv.id = dep."subServiciosSedes_id") inner join sitios_serviciosSedes sd on (sd."sedesClinica_id" = i."sedesClinica_id") inner join clinico_servicios ser  on (ser.id = sd.servicios_id  and ser.id = i."serviciosIng_id" ) left join clinico_especialidades esp1 on (esp1.id = i."especialidadesMedicosIngreso_id" ) left join clinico_diagnosticos diag1 on (diag1.id = i."dxIngreso_id") left join clinico_medicos med1 on (med1.id =i."medicoIngreso_id") left join planta_planta pla on (pla.id =i."medicoIngreso_id")  left join clinico_viasIngreso vias on (vias.id = i."ViasIngreso_id") left join clinico_causasExterna cexterna on (cexterna.id = i."causasExterna_id") inner join clinico_regimenes reg on (reg.id = i.regimen_id) inner join clinico_tiposcotizante cot on (cot.id = i."tiposCotizante_id") left  join clinico_ips ips on (ips.id =i."ipsRemite_id") WHERE i."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' and u."tipoDoc_id" = ' + "'" + str(Ingreso.tipoDoc_id) + "'" + ' and u.id = ' + "'" + str(Ingreso.documento_id) + "'" + ' and i.consec= ' + "'" + str(Ingreso.consec) + "'" + ' and i."fechaSalida" is null'

        print(comando)
        curt.execute(comando)

        Usuarios = {}

        for tipoDoc,  documento,paciente ,consec ,  ingreso , salida, servicioNombreIng,subServicioNombreIng, dependenciasIngreso , medicoIngreso, espMedico, diagMedico, viasIngreso, causasExterna,regimenes, cotizante, remitido,ips , numManilla, dxIngreso,responsable, acompanante, empresa, ripsCausaMotivoAtencion ,ripsGrupoServicios, ripsmodalidadGrupoServicioTecSal, ripsViaIngresoServicioSalud , ripsServiciosIng , ripsCondicionDestinoUsuarioEgreso , ripsViaIngresoServicioSalud, ripsDestinoUsuarioEgresoRecienNacido  in curt.fetchall():
            Usuarios = {'tipoDoc': tipoDoc, 'documento': documento, 'paciente': paciente, 'ingreso': ingreso,
                        'salida': salida, 'servicioNombreIng': servicioNombreIng, 'subServicioNombreIng':subServicioNombreIng, 'dependenciasIngreso': dependenciasIngreso,
                        'medicoIngreso': medicoIngreso, 'espMedico': espMedico, 'diagMedico': diagMedico,
                        'viasIngreso': viasIngreso, 'causasExterna': causasExterna,
                        'regimenes': regimenes, 'cotizante': cotizante, 'remitido': remitido,
                        'ips': ips, 'numManilla': numManilla, 'dxIngreso':dxIngreso,'responsable':responsable, 'acompanante':acompanante,'empresa':empresa,'ripsCausaMotivoAtencion':ripsCausaMotivoAtencion, 'ripsGrupoServicios' : ripsGrupoServicios   , 'ripsmodalidadGrupoServicioTecSal':ripsmodalidadGrupoServicioTecSal , 'ripsViaIngresoServicioSalud':ripsViaIngresoServicioSalud, 'ripsServiciosIng':ripsServiciosIng,'ripsCondicionDestinoUsuarioEgreso':ripsCondicionDestinoUsuarioEgreso,
                        'ripsViaIngresoServicioSalud':ripsViaIngresoServicioSalud,'ripsDestinoUsuarioEgresoRecienNacido':ripsDestinoUsuarioEgresoRecienNacido}

        miConexiont.close()
        print(Usuarios)


        if Usuarios == '[]':
            datos = {'Mensaje': 'Usuario No existe'}
            return JsonResponse(datos, safe=False)
        else:
            datos = {'Mensaje': 'Usuario SIII existe'}
            return JsonResponse(Usuarios, safe=False)


def cambioServicio(request):

    print("Entre a buscar una Cambio Servicio  Modal")
    sede = request.POST['sede']
    print("sede = ", sede)
    ingreso = request.POST['valor']
    print("ingreso = ", ingreso)

    datos  = Ingresos.objects.get(id=ingreso)
    datosTip = TiposDocumento.objects.get(nombre=datos.tipoDoc)

    datosDoc = Usuarios.objects.get(nombre=datos.documento)
  

    tipoDocPaciente  =  datosTip.id
    documentoPaciente = datosDoc.id
    consecutivo = datos.consec
    print("datos Tipo doc = ", datosTip.id)
    print("datos  documento = ", datosDoc.id)
    print("datos  consecutivo= ", datos.consec)


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT i."tipoDoc_id" tipoDocId, tp.nombre tipoDoc,  i.documento_id documentoId, u.documento documento, u.nombre  paciente , i.consec consec , i."fechaIngreso" ingreso , i."fechaSalida" salida, ser.nombre servicioNombreIng, dep.nombre dependenciasIngreso ,pla.nombre medicoIngreso, esp1.nombre espMedico,diag1.nombre diagMedico,vias.nombre viasIngreso, cexterna.nombre causasExterna,reg.nombre regimenes ,cot.nombre cotizante,i.remitido remitido,ips.nombre ips ,i."numManilla" numManilla, diag1.nombre dxIngreso, i."contactoResponsable_id" responsable, i."contactoAcompañante_id"  acompanante FROM admisiones_ingresos i inner join usuarios_usuarios u on (u."tipoDoc_id" = i."tipoDoc_id" and u.id = i."documento_id" ) inner join sitios_dependencias dep on (dep."sedesClinica_id" = i."sedesClinica_id" and dep."tipoDoc_id" =  i."tipoDoc_id" and dep.documento_id =i."documento_id"  and dep.consec = i.consec) inner join usuarios_tiposDocumento tp on (tp.id = u."tipoDoc_id") inner join sitios_dependenciastipo deptip on (deptip.id = dep."dependenciasTipo_id") inner join sitios_serviciosSedes sd on (sd."sedesClinica_id" = i."sedesClinica_id") inner join clinico_servicios ser  on (ser.id = sd.servicios_id  and ser.id = i."serviciosIng_id" ) left join clinico_especialidades esp1 on (esp1.id = i."especialidadesMedicosIngreso_id" ) left join clinico_diagnosticos diag1 on (diag1.id = i."dxIngreso_id")  left join clinico_medicos med1 on (med1.id =i."medicoIngreso_id"  ) left join planta_planta pla on (pla.id = med1.planta_id)   inner join clinico_viasIngreso vias on (vias.id = i."ViasIngreso_id") left join clinico_causasExterna cexterna on (cexterna.id = i."causasExterna_id") inner join clinico_regimenes reg on (reg.id = i.regimen_id) inner join clinico_tiposcotizante cot on (cot.id = i."tiposCotizante_id") left  join clinico_ips ips on (ips.id =i."ipsRemite_id") WHERE i.id = ' + "'" + str(ingreso) + "'"

    print(comando)
    curt.execute(comando)

    usuarios = {}

    for tipoDocId, tipoDoc, documentoId, documento, paciente, consec, ingreso, salida, servicioNombreIng, dependenciasIngreso, medicoIngreso, espMedico, diagMedico, viasIngreso, causasExterna, regimenes, cotizante, remitido, ips, numManilla, dxIngreso, responsable, acompanante in curt.fetchall():
        usuarios = {'tipoDocId':tipoDocId, 'tipoDoc': tipoDoc, 'documentoId':documentoId, 'documento': documento, 'paciente': paciente, 'consec':consec, 'ingreso': ingreso,
                    'salida': salida, 'servicioNombreIng': servicioNombreIng,
                    'dependenciasIngreso': dependenciasIngreso,
                    'medicoIngreso': medicoIngreso, 'espMedico': espMedico, 'diagMedico': diagMedico,
                    'viasIngreso': viasIngreso, 'causasExterna': causasExterna,
                    'regimenes': regimenes, 'cotizante': cotizante, 'remitido': remitido,
                    'ips': ips, 'numManilla': numManilla, 'dxIngreso': dxIngreso, 'responsable':responsable, 'acompanante':acompanante}

    miConexiont.close()
    print(usuarios)

    cambioServicio = {}
    cambioServicio['Usuarios'] = usuarios

    dependenciasActual = {}

    # Ahora llevamos la dependencia Actual

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",                   password="123456")
    curt = miConexiont.cursor()

    comando = 'select dep.id id , dep.numero numero , dep.nombre depNombre, sd.nombre servicio, sub.nombre subServicio,   dep."tipoDoc_id" tipoDocId, dep.documento_id documentoId, dep."fechaRegistro" fechaRegistro, dep.disponibilidad dispo,dep.consec consec ,dep."fechaOcupacion" ocupacion from sitios_dependencias dep, sitios_serviciosSedes sd, sitios_subServiciosSedes sub where dep."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' and dep."tipoDoc_id"=' + "'" + str(datosTip.id) + "'" + ' and dep.documento_id=' + "'" + str(datosDoc.id) + "'" + ' and dep.consec = ' + str(datos.consec) + '  and dep.disponibilidad = ' + "'" + str('O') + "'" + ' and sub."serviciosSedes_id" = sd.id and sd.id=dep."serviciosSedes_id" and sub.id= dep."subServiciosSedes_id"'

    print(comando)
    curt.execute(comando)

    for id, numero, depNombre, servicio, subServicio, tipoDocId, documentoId, fechaRegistro, dispo, consec, ocupacion in curt.fetchall():
        dependenciasActual = {'id': id, 'numero': numero, 'depNombre': depNombre, 'servicio': servicio,
                    'subServicio': subServicio,
                    'tipoDocId': tipoDocId, 'documentoId': documentoId,
                    'fechaRegistro': fechaRegistro,'dispo':dispo, 'consec':consec,'ocupacion':ocupacion   }

    miConexiont.close()

    cambioServicio['DependenciasActual'] = dependenciasActual
    


    # Combo de Servicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id AND ser.nombre in ( ' + "'" + str('HOSPITALIZACION') + "','" + str('URGENCIAS') + "')"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    cambioServicio['Servicios'] = servicios

    # Fin combo servicios

    # Combo de SubServicios

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id" AND ser.nombre in ( ' + "'" + str('HOSPITALIZACION') + "','" + str('URGENCIAS') + "')"
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)


    cambioServicio['SubServicios'] = subServicios

    # Fin combo SubServicios


    # Combo Habitaciones

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip , sitios_serviciosSedes sd, clinico_servicios ser where dep."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id AND dep.disponibilidad = ' + "'" + str('L') + "'" + ' AND sd.id=dep."serviciosSedes_id" AND ser.id = sd."servicios_id" and ser.nombre in (' + "'" + str('HOSPITALIZACION') + "'," + "'" + str('URGENCIAS') + "')"
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    cambioServicio['Habitaciones'] = habitaciones

    # Aqui FURIPS Leer el id y enviar un Furips form por aqui a ver que pasa

    tipoDocPaciente  =  datosTip.id
    documentoPaciente = datosDoc.id
    consecutivo = datos.consec


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT "consecVictima",  "numeroFactura" ,  "fechaRadicado" ,  "lugarRecogeVictima" ,  "eventoDescripcion" ,  "direccionEvento" ,  "fechaEvento" ,  "documentoInvolucrado" ,  "tipoVehiculo" ,  codigoaseguradora ,   "numeroPlacaTranporto" ,  "fechaIniPoliza" ,  "fechaFinPoliza" ,  "codigoInscripcion" ,  "codigoInscripcionRecibe" ,  "documentoPropietario" , "numeroRadicadoAnterior" ,  "direccionPropietario" ,  "primerApellidoInvolucrado" ,  "cobroExcedentePoliza" ,   "numeroRadicacion" ,  "direccionInvolucrado" ,  "placaVehiculo" ,  "primerApellidoPropietario" ,  "marcaVehiculo" ,  "primerApellidoVictima" ,  "numeroPoliza" ,  "fechaRegistro" ,  "estadoReg" ,   "documentoProfesionalAtendio_id" ,  "dxPrincEgreso_id" ,  "dxPrincIngreso_id" ,  "dxRel1Egreso_id" ,  "dxRel1Ingreso_id" ,  "dxRel2Egreso_id" ,  "dxRel2Ingreso_id" ,  "evento_id" ,  "localidadEvento_id" ,  "municipioEvento_id" ,  "municipioPropietario_id" ,"sedesClinica_id" ,"tipoDocVictima_id" ,  "tipoDocPropietario_id" ,"usuarioCrea_id",  "amparoReclamaAFosygaGastos" ,  "amparoReclamaAFosygaQx" ,  "amparoReclamaFacturadoGastos" , "amparoReclamaFacturadoQx" ,  "certificacionEgreso" ,  "certificacionIngreso" ,  "condicionAccidentado" ,  "departamentoEvento_id" ,  "departamentoInvolucrado_id" ,  "departamentoPropietario_id" ,  "documentoVictima_id" ,  estado,  "fechaAceptacion" ,  "fechaRemision" ,  "intervencionAutoridad" ,  "localidadInvolucrado_id" ,  "localidadPropietario_id" ,  "municipioInvolucrado_id" ,  "prestadorRecibe_id" ,  "prestadorRemite_id" ,  "primerNombreInvolucrado" ,  "primerNombrePropietario" ,  "primerNombreVictima" ,  "profesionalRecibe" ,  "profesionalRemite_id" ,  "segundoApellidoInvolucrado" ,  "segundoApellidoPropietario" ,  "segundoApellidoVictima" ,  "segundoNombreInvolucrado" ,  "segundoNombrePropietario" ,  "segundoNombreVictima" ,  "tipoDocInvolucrado_id" ,  "tipoDocProfesionalAtendio_id" ,  "tipoReferencia" ,  "tipoServicioVehiculo" ,  "tipoTransporteTransporto" ,  "trasportoVictimaDesde" ,  "trasportoVictimaHasta",   "zonaEvento" ,  consec ,  "documento_id" ,  "tipoDoc_id" FROM admisiones_furips where documento_id = ' + "'" + str(tipoDocPaciente) + "'" + ' AND "tipoDoc_id" = ' + "'" + str(documentoPaciente) + "'" + '  AND consec = ' +"'" + str(consecutivo) + "'"


    curt.execute(comando)
    print(comando)

    furips = []
    furips.append({'id': '', 'nombre': ''})

    for  consecVictima,  numeroFactura ,  fechaRadicado ,  lugarRecogeVictima ,  eventoDescripcion ,  direccionEvento ,  fechaEvento ,  documentoInvolucrado ,  tipoVehiculo ,  codigoAseguradora ,  numeroPlacaTranporto ,  fechaIniPoliza ,  fechaFinPoliza ,  codigoInscripcion ,  codigoInscripcionRecibe ,  documentoPropietario , numeroRadicadoAnterior ,  direccionPropietario ,  primerApellidoInvolucrado ,  cobroExcedentePoliza ,  numeroRadicacion ,  direccionInvolucrado ,  placaVehiculo ,  primerApellidoPropietario ,  marcaVehiculo ,  primerApellidoVictima ,  numeroPoliza ,  fechaRegistro ,  estadoReg ,  documentoProfesionalAtendio_id ,  dxPrincEgreso_id ,  dxPrincIngreso_id ,  dxRel1Egreso_id ,  dxRel1Ingreso_id ,  dxRel2Egreso_id ,  dxRel2Ingreso_id ,  evento_id ,  localidadEvento_id ,  municipioEvento_id ,  municipioPropietario_id ,  sedesClinica_id ,  tipoDocVictima_id ,  tipoDocPropietario_id ,  usuarioCrea_id ,  amparoReclamaAFosygaGastos ,  amparoReclamaAFosygaQx ,  amparoReclamaFacturadoGastos ,  amparoReclamaFacturadoQx ,  certificacionEgreso ,  certificacionIngreso ,  condicionAccidentado ,  departamentoEvento_id ,  departamentoInvolucrado_id ,  departamentoPropietario_id ,  documentoVictima_id ,  estado,  fechaAceptacion ,  fechaRemision ,  intervencionAutoridad ,  localidadInvolucrado_id ,  localidadPropietario_id ,  municipioInvolucrado_id ,  prestadorRecibe_id ,  prestadorRemite_id ,  primerNombreInvolucrado ,  primerNombrePropietario ,  primerNombreVictima ,  profesionalRecibe ,  profesionalRemite_id ,  segundoApellidoInvolucrado ,  segundoApellidoPropietario ,  segundoApellidoVictima ,  segundoNombreInvolucrado ,  segundoNombrePropietario ,  segundoNombreVictima ,  tipoDocInvolucrado_id ,  tipoDocProfesionalAtendio_id ,  tipoReferencia ,  tipoServicioVehiculo ,  tipoTransporteTransporto ,  trasportoVictimaDesde ,  trasportoVictimaHasta,  zonaEvento ,  consec ,  documento_id ,  tipoDoc_id  in curt.fetchall():
        furips.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(furips)

    cambioServicio['Furips'] = furips


    # FIN FURIPS

    # Fin combo Habitaciones

    if cambioServicio == '[]':
        datos = {'Mensaje': 'Usuario No existe'}
        return JsonResponse(cambioServicio, safe=False)
    else:
        datos = {'Mensaje': 'Usuario SIII existe'}
        return JsonResponse(cambioServicio, safe=False)



def guardaCambioServicio(request):
    print ("entre guardaCambioServicio")
    CambioServicio = {}
   
    tipoDoc = request.POST['tipoDocx']
    documento = request.POST["documentox"]
    consec = request.POST["consecx"]
    pacientex = request.POST["pacientex"]
    print("tipoDoc  = ", tipoDoc)
    print ("documento = ", documento )
    print("consec = ", consec )
    servicioFin = request.POST["servicioCambio"]
    subServicioFin = request.POST["subServicioCambio"]
    dependenciaFin = request.POST["dependenciaCambio"]
    print("dependenciaFin = ", dependenciaFin)

    fechaOcupacion = datetime.datetime.now()
    fechaRegistro = timezone.now()

    CambioServicio['TipoDocx'] = tipoDoc
    CambioServicio['Documentox'] = documento
    CambioServicio['Consecx'] = consec
    CambioServicio['Pacientex'] = pacientex
    #CambioServicio['ServicioCambio'] = servicioFin
    #CambioServicio['SubServicioCambio'] = subServicioFin
    #CambioServicio['DependenciaCambio'] = dependenciaFin


    username_id = request.POST["username_id"]
    print("servicioFin = ", servicioFin )
    print("subServicioFin = ", subServicioFin )
    print("fechaOcupacion = ", fechaOcupacion)
    print("username_id = ", username_id)
    CambioServicio['Username_id'] = username_id


    # Aqui consigo el servicio Actual

    servicioFinId = ServiciosSedes.objects.get(id=servicioFin)
    print("servicioFinId = ", servicioFinId.id)
    tipoDocId = TiposDocumento.objects.get(nombre=tipoDoc)
    print("el id del tipo del  documento es : ", tipoDocId.id)

    documentoId = Usuarios.objects.get(documento=documento, tipoDoc_id=tipoDocId.id)
    print("el id del documento es : ", documentoId.id)

    try:
        with transaction.atomic():

            dependenciaActualId = Dependencias.objects.get(documento_id=documentoId.id, tipoDoc_id=tipoDocId.id, consec=consec)
            print("el id del dependenciaActualId es : ", dependenciaActualId.id)

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)
        return JsonResponse({'success': False, 'Mensaje': e})


    dependenciaFinalId = Dependencias.objects.get(serviciosSedes_id=servicioFin , subServiciosSedes_id=subServicioFin , id=dependenciaFin)
    print("el id del dependenciaFinalId es : ", dependenciaFinalId.id)
    ingresoActualId = Ingresos.objects.get(documento_id=documentoId.id , tipoDoc_id=tipoDocId.id , consec=consec)
    print("el id del ingresoFinalId es : ", ingresoActualId.id)


    sede = request.POST['sede'] 
    sedeSeleccionada = request.POST['sedeSeleccionada'] 
    numReporte = request.POST['numReporte'] 
    grupo = request.POST['sede']
    subGrupo = request.POST['subGrupo'] 
    nombreSede = request.POST['nombreSede'] 
    profesional = request.POST['profesional'] 
    permisosGrales = request.POST['permisosGrales'] 
    escogeModulo = request.POST['escogeModulo'] 
    permisosDetalle = request.POST['permisosDetalle'] 

    CambioServicio['Sede'] = sede
    CambioServicio['SedeSeleccionada'] = sedeSeleccionada
    CambioServicio['NumReporte'] = numReporte
    CambioServicio['Grupo'] = grupo
    CambioServicio['SubGrupo'] = subGrupo
    CambioServicio['NombreSede'] = nombreSede
    CambioServicio['Profesional'] = profesional
    CambioServicio['PermisosGrales'] = permisosGrales
    CambioServicio['EscogeModulo'] = escogeModulo
    CambioServicio['PermisosDetalle'] = permisosDetalle



    # Combo de Servicios
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT ser.id id ,ser.nombre nombre FROM sitios_serviciosSedes sed, clinico_servicios ser Where sed."sedesClinica_id" =' + "'" + str(
        sede) + "'" + ' AND sed."servicios_id" = ser.id AND ser.nombre in ( ' + "'" + str('HOSPITALIZACION') + "','" + str('URGENCIAS') + "')"
    curt.execute(comando)
    print(comando)

    servicios = []
    servicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        servicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(servicios)

    CambioServicio['Servicios'] = servicios

    # Fin combo servicios


    # Combo de SubServicios
    # miConexiont = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()
    comando = 'SELECT sub.id id ,sub.nombre nombre  FROM sitios_serviciosSedes sed, clinico_servicios ser  , sitios_subserviciossedes sub Where sed."sedesClinica_id" =' + "'" + str(sede) + "'" + ' AND sed."servicios_id" = ser.id and  sed."sedesClinica_id" = sub."sedesClinica_id" and sed."servicios_id" = sub."serviciosSedes_id" AND ser.nombre in ( ' + "'" + str('HOSPITALIZACION') + "','" + str('URGENCIAS') + "')"
    curt.execute(comando)
    print(comando)

    subServicios = []
    subServicios.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        subServicios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(subServicios)


    CambioServicio['SubServicios'] = subServicios

    # Fin combo SubServicios


    # Combo Habitaciones

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT dep.id ,dep.nombre FROM sitios_dependencias dep, sitios_dependenciasTipo tip , sitios_serviciosSedes sd, clinico_servicios ser where dep."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND tip.nombre=' + "'" + str('HABITACIONES') + "'" + ' and dep."dependenciasTipo_id" = tip.id AND dep.disponibilidad = ' + "'" + str('L') + "'" + ' AND sd.id=dep."serviciosSedes_id" AND ser.id = sd."servicios_id" and ser.nombre in (' + "'" + str('HOSPITALIZACION') + "'," + "'" + str('URGENCIAS') + "')"
    curt.execute(comando)
    print(comando)

    habitaciones = []
    habitaciones.append({'id': '', 'nombre': ''})

    for id, nombre in curt.fetchall():
        habitaciones.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(habitaciones)

    CambioServicio['Habitaciones'] = habitaciones

    # Fin combo Habitaciones

    CambioServicio['Mensaje'] = 'Cambio de servicio realizado'

    servicioFinalId = ServiciosSedes.objects.get(id=servicioFin)
    subServicioFinalId = SubServiciosSedes.objects.get(id=subServicioFin)
    dependenciaFinalId = Dependencias.objects.get(id=dependenciaFin)

    ## OJO NO CONFUNDIR ESTE PEDAZO DE CODIGO DE ABAJO CON LO DE ARRIBA SE SOBREESCRIBE
	
    CambioServicio['ServicioActual'] = servicioFinalId.nombre
    CambioServicio['SubServicioActual'] = subServicioFinalId.nombre
    CambioServicio['DependenciaActual'] = dependenciaFinalId.nombre
    CambioServicio['FechaOcupacion'] = fechaOcupacion

    try:
        with transaction.atomic():
            # Actualiza la dependecia Actual

            print("Aqui actualiza  : ",  dependenciaActualId.id);


            #Aqui libera la que tenia ocupada creo

            grabo01 = Dependencias.objects.filter(id=dependenciaActualId.id).update(tipoDoc_id='', documento_id='',
                                                                                    consec=0, disponibilidad="L",
                                                                                    fechaRegistro=fechaRegistro,
                                                                                    fechaLiberacion=None,
                                                                                    fechaOcupacion=None)
            print("pase YA grabo01", grabo01)

            # Actualiza la dependencia Nueva

            print("Aqui Error  : ",  dependenciaFinalId.id);
            print ("tipoDocId.id = ",tipoDocId.id)
            print("documentoId.id = ", documentoId.id )
            print("consec =", consec )


            #Aqui Ocupa la nueva cama

            grabo02 = Dependencias.objects.filter(id=dependenciaFinalId.id).update(tipoDoc_id=tipoDocId.id,
                                                                                   documento_id=documentoId.id,
                                                                                   consec=consec, disponibilidad="O",
                                                                                   fechaRegistro=fechaRegistro,
                                                                                   fechaOcupacion=fechaRegistro,
                                                                                   fechaLiberacion=None)
            print("pase grabo02", grabo02)
            # Inserta en dependeciasHistoricos

            # Actualiza la admision en Ingresos

            grabo03 = Ingresos.objects.filter(id=ingresoActualId.id).update(dependenciasActual_id=dependenciaFinalId.id,
                                                                            serviciosActual_id=servicioFinalId.servicios_id)
            print("pase grabo03", grabo03)

            # Registro PRIMERO el historico de dependencia LA QUE LIBERO


            grabo07 = HistorialDependencias(
                tipoDoc_id=tipoDocId.id,
                documento_id=documentoId.id,
                consec=consec,
                dependencias_id=dependenciaActualId.id,
                disponibilidad='L',
                fechaRegistro=fechaRegistro,
                usuarioRegistro_id=username_id,
                fechaLiberacion=fechaRegistro,
                fechaOcupacion=None,
                estadoReg='A'
            )
            grabo07.save()
            print("yA grabe dependencias historico la que libere", grabo07.id)



            # Registro el historico la nueva dependencia si es un INSERT

            grabo05 = HistorialDependencias(
                tipoDoc_id=tipoDocId.id,
                documento_id=documentoId.id,
                consec=consec,
                dependencias_id=dependenciaFinalId.id,
                disponibilidad='O',
                fechaRegistro=fechaRegistro,
                usuarioRegistro_id=username_id,
                #fechaLiberacion=fechaRegistro,
                fechaOcupacion=fechaRegistro,
                estadoReg='A'
            )
            grabo05.save()
            print("yA grabe dependencias historico", grabo05.id)

            CambioServicio['success'] = True
            CambioServicio['Mensaje'] = 'Traslado realizado correctamente !'

            return JsonResponse(CambioServicio, safe=False)


    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)
        return JsonResponse({'success': False, 'Mensaje': e})




	

def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime):
        return obj.isoformat() 
    raise TypeError("Type not serializable") 


def serialize_datetime1(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")



# Create your views here.
def load_dataConvenioAdmisiones(request, data):
    print ("Entre  load_dataConvenioAdmisiones")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']
    sede = d['sede']

    print ("sede:", sede)
    print ("ingresoId:", ingresoId)



    conveniosPacienteIngresos = []


    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",     password="123456")
    curx = miConexionx.cursor()
   
    detalle = 'SELECT conv.id id,i."tipoDoc_id" tipoDocId , i.documento_id documentoId ,u.documento documento,u.nombre nombre,i.consec consec , contra.nombre convenio, tipdoc.nombre nombreDocumento FROM admisiones_ingresos i, usuarios_usuarios u, facturacion_conveniosPacienteIngresos conv , contratacion_convenios contra , usuarios_tiposdocumento tipdoc WHERE i.id = ' + "'" + str(ingresoId) + "'" + ' and i.documento_id = u.id and i."tipoDoc_id" = conv."tipoDoc_id" and i.documento_id  = conv.documento_id and i.consec = conv."consecAdmision" and contra.id = conv.convenio_id AND tipdoc.id = i."tipoDoc_id"'

    print(detalle)

    curx.execute(detalle)

    for  id, tipoDocId, documentoId, documento, nombre, consec, convenio, nombreDocumento in curx.fetchall():
        conveniosPacienteIngresos.append(
		{"model":"conveniosPacienteIngresos.conveniosPacienteIngresos","pk":id,"fields":
			{'id':id, 'tipoDocId': tipoDocId, 'documentoId': documentoId, 'documento':documento , 'nombre': nombre, 'consec': consec, 'convenio':convenio, 'nombreDocumento':nombreDocumento}})

    miConexionx.close()
    print(conveniosPacienteIngresos )
    context['ConveniosPacienteIngresos '] = conveniosPacienteIngresos

    serialized1 = json.dumps(conveniosPacienteIngresos , default=serialize_datetime)

    print ("Envio = ", serialized1 )

    return HttpResponse(serialized1, content_type='application/json')


def load_dataAbonosAdmisiones(request, data):
    print("Entre  load_dataAbonosAdmisiones")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']
    sede = d['sede']

    print("sede:", sede)
    print("ingresoId:", ingresoId)

    # print("data = ", request.GET('data'))

    abonos  = []

    # miConexionx = MySQLdb.connect(host='CMKSISTEPC07', user='sa', passwd='75AAbb??', db='vulnerable')
    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'SELECT pag.id id , i."tipoDoc_id" tipoDoc , i.documento_id documentoId ,u.documento documento,u.nombre nombre,i.consec consec , tipdoc.nombre nombreDocumento , cast(date(pag.fecha) as text)  fecha, pag."tipoPago_id" tipoPago , tip.nombre nombreTipoPago, pag."formaPago_id" formaPago, forma.nombre nombreFormaPago, pag.valor valor, pag.descripcion descripcion , pag."estadoReg" estadoReg FROM admisiones_ingresos i, cartera_pagos pag ,usuarios_usuarios u ,usuarios_tiposdocumento tipdoc, cartera_tiposPagos tip, cartera_formasPagos forma WHERE i.id = ' + "'" + str(ingresoId) + "'" + ' and i.documento_id = u.id and i."tipoDoc_id" = pag."tipoDoc_id" and i.documento_id  = pag.documento_id and  i.consec = pag.consec AND tipdoc.id = i."tipoDoc_id" and pag."tipoPago_id" = tip.id and pag."formaPago_id" = forma.id'
    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc, documentoId, documento, nombre, consec, nombreDocumento , fecha, tipoPago, nombreTipoPago, formaPago, nombreFormaPago,  valor, descripcion , estadoReg in curx.fetchall():
        abonos.append(
            {"model": "cartera_pagos.cartera_pagos", "pk": id, "fields":
                {'id': id, 'tipoDoc': tipoDoc, 'documentoId': documentoId, 'nombre':nombre,'consec':consec,  'nombreDocumento': nombreDocumento,
                 'fecha': fecha, 'tipoPago': tipoPago, 'nombreTipoPago': nombreTipoPago,'formaPago': formaPago, 'nombreFormaPago':nombreFormaPago, 'valor':valor, 'descripcion':descripcion, 'estadoReg':estadoReg}})

    miConexionx.close()
    print(abonos)
    context['Abonos '] = abonos

    serialized2 = json.dumps(abonos,  default=decimal_serializer)


    print("Envio = ", serialized2)

    return HttpResponse(serialized2, content_type='application/json')



def GuardaConvenioAdmision(request):

    print ("Entre GuardaConvenioAdmision" )

    ingresoId = request.POST["ingresoId2"]

    sede = request.POST["sede2"]
    convenio = request.POST["convenio"]
    username_id = request.POST["username33_id"]
    print ("ingresoId = ", ingresoId)
    print("sede = ", sede)
    print("convenio = ", convenio)
    print("username_id = ", username_id)

    fechaRegistro = timezone.now()

    registroId = Ingresos.objects.get(id=ingresoId)
    estadoReg='A'
    print  ("registroId documento =" , registroId.documento_id)

    ## falta usuarioRegistro_id

    ## Desde Aquip Transaccionalidad


    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            cur3 = miConexion3.cursor()

            comando1 = 'insert into facturacion_ConveniosPacienteIngresos ("consecAdmision", "fechaRegistro",  convenio_id, documento_id, "tipoDoc_id" , "usuarioRegistro_id" ,"estadoReg", anulado ) values (' + "'" + str(registroId.consec) + "'" + ' , ' + "'" + str(fechaRegistro) + "'" + ', ' + "'" + str(convenio) + "'" + '  , ' + "'" + str(registroId.documento_id) + "'" + ', ' + "'" + str(registroId.tipoDoc_id) + "'," + "'" + str("1") + "'," + "'" + str("A") + "','N');"
            print(comando1)
            cur3.execute(comando1)

            try:
                with transaction.atomic():
                    existeLiquidacion = Liquidacion.objects.get(tipoDoc_id=registroId.tipoDoc_id, documento_id=registroId.documento_id, consecAdmision=registroId.consec, convenio_id = convenio)
                    hayLiquidacion=existeLiquidacion.id
                    print("hayLiquidacion DENTRO DEL WITH=", hayLiquidacion)

            except Exception as e:
                # Aquí No existe
                print("Noexiste:", e)
                hayLiquidacion = 0

            finally:
                print("No haga nada")

            print ("hayLiquidacion =", hayLiquidacion )

            if (hayLiquidacion==0):


                print ("Entre por hayliquidacion= 0, O sea creo liquidacion ")
                comando2 = 'INSERT INTO facturacion_liquidacion ("sedesClinica_id", "tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos",anulado) VALUES (' + "'" + str(sede) + "'," +  "'" + str(registroId.tipoDoc_id) + "','" + str(registroId.documento_id) + "','" + str(registroId.consec) + "','" + str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(convenio) + ',' + "'" + str(username_id) + "',0,'N') RETURNING id "

            else:
                comando2 = 'UPDATE facturacion_Liquidacion SET convenio_id = ' + "'" + str(convenio) + "' WHERE id =" + str(hayLiquidacion)

            print("comando1= ", comando1)
            print("comando2= ", comando2)

            cur3.execute(comando2)
            miConexion3.commit()
            cur3.close()
            datos = {'success': True, 'Mensaje': 'Convenio Actualizado satisfactoriamente!'}
            return JsonResponse(datos, safe=False)

            #return JsonResponse({'success': True, 'Mensaje': 'Convenio Actualizado satisfactoriamente!'})


    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        return JsonResponse({'success': False, 'Mensaje': error})

    finally:
        if miConexion3:
            miConexion3.close()



def GuardaAbonosAdmision(request):

    print ("Entre GuardaAbonosAdmision" )

    ingresoId = request.POST["ingresoId22"]
    sede = request.POST["sede22"]
    ingresos = Ingresos.objects.get(id=ingresoId)

    sede = request.POST["sede22"]
    username_id = request.POST["username22_id"]
    tipoPago = request.POST["tipoPago"]
    formaPago = request.POST["formaPago"]

    formaAnticipo = FormasPagos.objects.get(nombre='ANTICIPO')
    formaAbono = FormasPagos.objects.get(nombre='ABONO')
    print ("formaAbono = " , formaAbono)
    formaModeradora= FormasPagos.objects.get(nombre='CUOTA MODERADORA')
    formaCopago= FormasPagos.objects.get(nombre='COPAGO')
    tipoPagoId= TiposPagos.objects.get(id=tipoPago)

    valor = request.POST['valorAbono']
    descripcion = request.POST['descripcionAbono']
    print ("ingresoId = ", ingresoId)
    print("sede = ", sede)
    print("formaPago = ", formaPago)
    convenioPaciente = request.POST['convenioPaciente']
    print ("convenioPaciente = ", convenioPaciente)

    serviciosAdministrativos = request.POST['serviciosAdministrativosPagos']
    print ("serviciosAdministrativos = ", serviciosAdministrativos)


    estadoReg = 'A'
    fechaRegistro = timezone.now()

    registroId = Ingresos.objects.get(id=ingresoId)
    print  ("registroId documento =" , registroId.documento_id)

    ## falta usuarioRegistro_id

    ## Aqui busco el registro en cartera_caja si lo hay o si no hat que crear uno nuevo

    pailas = 0
    cajaEsteId=0

    try:
        with transaction.atomic():
            cajaId = Caja.objects.get(fecha=fechaRegistro, usuarioEntrega_id=username_id)
            cajaEsteId= cajaId.id

    except ObjectDoesNotExist:
        print("no ya informacion")
        pailas=0
        cajaEsteId=0

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por PRONO SE HACE NADA:", e)
        pailas=1
        envioMensaje=e
        #return JsonResponse({'success': False, 'Mensaje': e})

    finally:

        if (pailas==1):

            return JsonResponse({'success': False, 'Mensaje': envioMensaje})
        else:
            print("No haga nada")


    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        cur3 = miConexion3.cursor()

    	## AQui RUTINA Actualiza lo generado por el CAJERO
        if (cajaEsteId>0):

            if (tipoPagoId.nombre == 'EFECTIVO'):
                comando2 = 'UPDATE cartera_caja SET "totalEfectivoEsperado" = "totalEfectivoEsperado" + ' + "'" + str(valor) + "'" + ' WHERE id = ' + "'" + str(cajaEsteId) + "'"
                print ("acabo de actulizar con valor = ", valor)
            if (tipoPagoId.nombre == 'TARJETA DEBITO'):
                comando2 = 'UPDATE cartera_caja SET "totalTarjetasDebitoEsperado" = "totalTarjetasDebitoEsperado" + ' + "'" + str(valor) + "'" + ' WHERE id = ' + "'" + str(cajaEsteId) + "'"

            if (tipoPagoId.nombre == 'TARJETA CREDITO'):
                comando2 = 'UPDATE cartera_caja SET "totalTarjetasCreditoEsperado" = "totalTarjetasCreditoEsperado" + ' + "'" + str(valor) + "'" + ' WHERE id = ' + "'" + str(cajaEsteId) + "'"

            if (tipoPagoId.nombre == 'CHEQUE'):
                comando2 = 'UPDATE cartera_caja SET "totalChequesEsperado" = "totalChequesEsperado" + ' + "'" + str(valor) + "'" + ' WHERE id = ' + "'" + str(cajaEsteId) + "'"

            print("comando2 =" , comando2)
            resultado = cur3.execute(comando2)

        if (cajaEsteId == 0):

            if (tipoPagoId.nombre == 'EFECTIVO'):
                comando2 = 'INSERT INTO cartera_caja (fecha, "totalEfectivo", "totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", total, "fechaRegistro", "estadoReg", "serviciosAdministrativos_id", "usuarioEntrega_id", "usuarioRecibe_id", "usuarioRegistro_id", "usuarioSuperviza_id", "estadoCaja", "sedesClinica_id", "totalChequesEsperado", "totalEfectivoEsperado", "totalEsperado", "totalTarjetasCreditoEsperado", "totalTarjetasDebitoEsperado", anulado) VALUES (' + "'" + str(fechaRegistro) + "',0,0,0,0,0," + "'" + str(fechaRegistro) + "','A',null"  + "," + "'" + str(username_id) + "',null,"  + "'" + str(username_id) + "',null,'A','"  + str(sede)  + "',0,'" + str(valor) + "','" + str(valor) + "',0,0,'N') RETURNING id"

            if (tipoPagoId.nombre == 'TARJETA DEBITO'):
                comando2 = 'INSERT INTO cartera_caja (fecha, "totalEfectivo", "totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", total, "fechaRegistro", "estadoReg", "serviciosAdministrativos_id", "usuarioEntrega_id", "usuarioRecibe_id", "usuarioRegistro_id", "usuarioSuperviza_id", "estadoCaja", "sedesClinica_id", "totalChequesEsperado", "totalEfectivoEsperado", "totalEsperado", "totalTarjetasCreditoEsperado", "totalTarjetasDebitoEsperado", anulado) VALUES (' + "'" + str(fechaRegistro) + "',0,0,0,0,0," + "'" + str(fechaRegistro) + "','A'," + "'" + str(serviciosAdministrativos) + "'," + "'" + str(username_id) + "',null,"  + "'" + str(username_id) + "',null,'A',"  + "'" + str(sede)  + "',0,0,'" + str(valor) + "',0,'"  + str(valor) + "','N') RETURNING id"

            if (tipoPagoId.nombre == 'TARJETA CREDITO'):
                comando2 = 'INSERT INTO cartera_caja (fecha, "totalEfectivo", "totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", total, "fechaRegistro", "estadoReg", "serviciosAdministrativos_id", "usuarioEntrega_id", "usuarioRecibe_id", "usuarioRegistro_id", "usuarioSuperviza_id", "estadoCaja", "sedesClinica_id", "totalChequesEsperado", "totalEfectivoEsperado", "totalEsperado", "totalTarjetasCreditoEsperado", "totalTarjetasDebitoEsperado", anulado) VALUES (' + "'" + str(fechaRegistro) + "',0,0,0,0,0," + "'" + str(fechaRegistro) + "','A'," + "'" + str(serviciosAdministrativos) + "'," + "'" + str(username_id) + "',null,"  + "'" + str(username_id) + "',null,'A','"  + str(sede)  + "',0,0,'"  + str(valor) + "','"  + str(valor) + "',0,'N') RETURNING id"

            if (tipoPagoId.nombre == 'CHEQUE'):
                comando2 = 'INSERT INTO cartera_caja (fecha, "totalEfectivo", "totalTarjetasDebito", "totalTarjetasCredito", "totalCheques", total, "fechaRegistro", "estadoReg", "serviciosAdministrativos_id", "usuarioEntrega_id", "usuarioRecibe_id", "usuarioRegistro_id", "usuarioSuperviza_id", "estadoCaja", "sedesClinica_id", "totalChequesEsperado", "totalEfectivoEsperado", "totalEsperado", "totalTarjetasCreditoEsperado", "totalTarjetasDebitoEsperado", anulado) VALUES (' + "'" + str(fechaRegistro) + "',0,0,0,0,0," + "'" + str(fechaRegistro) + "','A'," + "'" + str(serviciosAdministrativos) + "'," + "'" + str(username_id) + "',null,"  + "'" + str(username_id) + "',null,'A','"  + str(sede)  + "','" + str(valor) + "'0,'" + str(valor) + "',0,0,'N') RETURNING id"

            print("comando2 =" , comando2)
            resultado = cur3.execute(comando2)
            cajaEsteId = cur3.fetchone()[0]

        print("Aqui vony cajaEsteId = ", cajaEsteId )

        comando = 'insert into cartera_Pagos ("fecha", "tipoDoc_id" , documento_id, consec,  "tipoPago_id" , "formaPago_id", valor, descripcion ,"fechaRegistro","estadoReg",saldo, "totalAplicado", "valorEnCurso", convenio_id, "serviciosAdministrativos_id" , anulado, "sedesClinica_id" , caja_id ) values (' + "'" + str(
            fechaRegistro) + "'," + "'" + str(registroId.tipoDoc_id) + "'" + ' , ' + "'" + str(
            registroId.documento_id) + "'" + ', ' + "'" + str(registroId.consec) + "'" + '  , ' + "'" + str(
            tipoPago) + "'" + '  , ' + "'" + str(formaPago) + "'" + ', ' + "'" + str(valor) + "'," + "'" + str(
            descripcion) + "','" + str(fechaRegistro) + "','" + str("A") + "','" + str(
            valor) + "'," + ' 0 , 0, ' + "'" + str(convenioPaciente) + "','" + str(
            serviciosAdministrativos) + "','N','" + str(sede) + "' ,'" + str(cajaEsteId) + "')"

        cur3.execute(comando)

        ## Aqui actualiza el total registro d caja esperado

        comandox = 'UPDATE cartera_caja SET "totalEsperado" = "totalEfectivoEsperado" + "totalTarjetasDebitoEsperado" + "totalTarjetasCreditoEsperado" + "totalChequesEsperado"  WHERE id = ' + "'" + str(cajaEsteId) + "'"
        cur3.execute(comandox)


        ## Aqui rutina crea cabezote si no existe. Actualiza totales a la liquidacion

        comando1 = 'SELECT id FROM facturacion_liquidacion WHERE "tipoDoc_id" = ' + str(registroId.tipoDoc_id) + ' AND documento_id = ' + str(registroId.documento_id) + ' AND "consecAdmision" = ' + "'" +  str(registroId.consec) + "' AND convenio_id = " + "'" + str(convenioPaciente) + "'"

        print("comando1 = " , comando1)

        resultado = cur3.execute(comando1)
        print("resultado = ", resultado)


        cabezoteLiquidacion = []

        for id in cur3.fetchall():
            cabezoteLiquidacion.append({'id': id})

        print("cabezoteLiquidacion = ", cabezoteLiquidacion)




        if (cabezoteLiquidacion == []):
            print("OJOOOOOO ENTRE AL CABEZOTE LIQUIDACION DEL ABONO NUEVO")
            comando2 = 'INSERT INTO facturacion_liquidacion ("tipoDoc_id", documento_id, "consecAdmision", fecha, "totalCopagos", "totalCuotaModeradora", "totalProcedimientos" , "totalSuministros" , "totalLiquidacion", "valorApagar", anticipos, "fechaRegistro", "estadoRegistro", convenio_id,  "usuarioRegistro_id", "totalAbonos" , "totalRecibido" , "sedesClinica_id", anulado ) VALUES (' + str(registroId.tipoDoc_id) + ',' + str(registroId.documento_id) + ',' + str(registroId.consec) + ',' + "'" + str(fechaRegistro) + "'," + '0,0,0,0,0,0,0,' + "'" + str(fechaRegistro) + "','" + str(estadoReg) + "'," + str(convenioPaciente) + ',' + "'" + str(username_id) + "',0,0," + "'" + str(sede) + "','A') RETURNING id"
            resultado = cur3.execute(comando2)
            liquidacionId = cur3.fetchone()[0]

        else:

            liquidacionId = cabezoteLiquidacion[0]['id']
            liquidacionId = str(liquidacionId)
            liquidacionId = liquidacionId.replace("(", ' ')
            liquidacionId = liquidacionId.replace(")", ' ')
            liquidacionId = liquidacionId.replace(",", ' ')

        print("liquidacionId = ", liquidacionId)

        miConexion3.commit()
        cur3.close()
        miConexion3.close()

        return JsonResponse({'success': True, 'Mensaje': 'Abono Creado satisfactoriamente!'})


    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        #print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensaje': error})

    finally:
        if miConexion3:
            cur3.close()
            miConexion3.close()




def PostDeleteConveniosAdmision(request):

    print ("Entre PostDeleteConveniosAdmision" )
    print ("PostDeleteConveniosAdmision" )

    id = request.POST["id"]
    print ("el id es = ", id)
    # Aqui Filtramos que se borre el convenio que no tenga registros en liquidaciondetalle

    convenio = ConveniosPacienteIngresos.objects.get(id=id)
    print("convenio_id = ", convenio.convenio_id)

    cantidadRegistros=0
    try:
      with transaction.atomic():

        registrosFacturacion = Liquidacion.objects.get(tipoDoc_id=convenio.tipoDoc_id, documento_id=convenio.documento_id, consecAdmision=convenio.consecAdmision, convenio_id=convenio.convenio_id)
        print("liquidacion = ", registrosFacturacion.id)
        cantidadRegistros = LiquidacionDetalle.objects.filter(liquidacion_id=registrosFacturacion.id).exclude(estadoRegistro='N').count()
        print("Cantidad Registros liquidacion Detalle = ", cantidadRegistros)

        if (cantidadRegistros>=1):
            return JsonResponse({'success': False, 'Mensaje': 'Convenio con registros de liqudacion Activos No es posible borrarlo!'})

    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)
        return JsonResponse({'success': False, 'Mensaje':  e})

    finally:
        print("Cleanup operations or final logging.")


    #miConexion3 = None

    try:
      with transaction.atomic():	

        ## Borra cabezote de Facturacion

        post2 = LiquidacionDetalle.objects.filter(liquidacion_id=registrosFacturacion.id)
        post2.delete()


        ## Borra cabezote de Facturacion
        post1 = Liquidacion.objects.get(id=registrosFacturacion.id)
        post1.delete()

        post = ConveniosPacienteIngresos.objects.get(id=id)
        post.delete()

        return JsonResponse({'success': True, 'Mensaje': 'Convenio borrado!'})


    except Exception as e:
        # Aquí ya se hizo rollback automáticamente
        print("Se hizo rollback por:", e)

    finally:
        print("Cleanup operations or final logging.")


    # Aqui Fin Manejo Transaccionalidad


def PostDeleteAbonosAdmision(request):

    print ("Entre PostDeleteAbonosFacturacion" )

    id = request.POST["id"]
    print ("el id es = ", id)

    pagos = Pagos.objects.get(id=id)

    liquidacion = Liquidacion.objects.get(tipoDoc_id=pagos.tipoDoc_id, documento_id = pagos.documento_id, consecAdmision=pagos.consec)
    liquidacionId = liquidacion.id
    print("liquidacionId =" , liquidacionId)

    ## Se debe verificar antes que no haya valor aplicado en PagosFacturas

    valorAMirar=0

    try:
        with transaction.atomic():

            valorSaldo = PagosFacturas.objects.get(pago_id=id, estadoReg='A', anulado='N')
            print ("Saldo = ", valorSaldo.saldo)
            valorAMirar = valorSaldo.saldo

    except Exception as e:

        print("Se hizo rollback por NO SE HACE NADA :", e)
        valorAMirar = 0

    finally:
        print("Cleanup operations or final logging.")


    if (valorAMirar > 0):

        return JsonResponse({'success': False, 'Mensaje': 'No se puede anular Abono con Facturas relacionadas!'})

        # Aqui Manejo Transaccionalidad

    formaAnticipo = FormasPagos.objects.get(nombre='ANTICIPO')
    formaAbono = FormasPagos.objects.get(nombre='ABONO')
    print ("formaAbono = " , formaAbono)
    formaModeradora= FormasPagos.objects.get(nombre='CUOTA MODERADORA')
    formaCopago= FormasPagos.objects.get(nombre='COPAGO')

    formaPago=pagos.formaPago

    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
            cur3 = miConexion3.cursor()
            comando = 'UPDATE cartera_Pagos SET "estadoReg" = ' + "'" + str('N') + "', anulado= 'S' WHERE id =  " + id
            print("comando = ", comando)
            cur3.execute(comando)

            ## AQUI RUTUNA ACTUALIZA CABEZOTE DE LIQUIDACION

            miConexion3.commit()
            cur3.close()
            miConexion3.close()

            ##FIN ACTUALIZA CABEZOTES
            return JsonResponse({'success': True, 'Mensaje': 'Abono Cancelado!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()
        #print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensaje': error})

    finally:
            if miConexion3:
                miConexion3.close()


    # Aqui Fin Manejo Transaccionalidad


def GuardarResponsableAdmision(request):

    print ("Entre GuardaConvenioAdmision" )

    ingresoId = request.POST["ingresoId"]
    responsable = request.POST["responsable"]
    print ("ingresoId = ", ingresoId)
    print("responsable  = ", responsable )

    registroId = Ingresos.objects.get(id=ingresoId)
    print  ("registroId documento =" , registroId.documento_id)

    # Aqui Manejo Transaccionalidad

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        cur3 = miConexion3.cursor()
        comando = 'UPDATE admisiones_ingresos set "contactoResponsable_id" = ' + "'" + str(responsable) + "' WHERE id = " + "'" + str(ingresoId) + "'"
        print("comando = ", comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()

        return JsonResponse({'success': True, 'Mensaje': 'Responsable Actualizado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        #print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensaje': error})

    finally:
        if miConexion3:
            miConexion3.close()


    # Aqui Fin Manejo Transaccionalidad



def GuardarAcompananteAdmision(request):

    print ("Entre GuardaAcompananteAdmision" )

    ingresoId = request.POST["ingresoId"]
    acompanante = request.POST["acompanante"]
    print ("ingresoId = ", ingresoId)
    print("acompanante  = ", acompanante )

    registroId = Ingresos.objects.get(id=ingresoId)
    print  ("registroId documento =" , registroId.documento_id)

    # Aqui Manejo Transaccionalidad

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        cur3 = miConexion3.cursor()
        comando = 'UPDATE admisiones_ingresos set "contactoAcompañante_id" = ' + "'" + str(acompanante) + "' WHERE id = " + "'" + str(ingresoId) + "'"
        print("comando = ", comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()

        return JsonResponse({'success': True, 'Mensaje': 'Acompañante Actualizado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()
        #print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensaje': error})

    finally:
        if miConexion3:
            miConexion3.close()


    # Aqui Fin Manejo Transaccionalidad


def GuardaFurips(request):

    print ("Entre GuardaFurips" )

    ingresoId = request.POST["ingresoId"]
    sede = request.POST["sede"]
    print ("ingresoId = ", ingresoId)
    print("sede = ", sede)
    fechaRegistro = timezone.now()
    registroId = Ingresos.objects.get(id=ingresoId)
    print  ("registroId documento =" , registroId.documento_id)

    primerApellidoVictima = request.POST["primerApellidoVictima"]
    print("primerApellidoVictima = ", primerApellidoVictima)


    numeroRadicacion = request.POST["numeroRadicacion"]
    print ("numeroRadicacion = ", numeroRadicacion)
    fechaRadicado = request.POST["fechaRadicado"]
    print ("fechaRadicado = ", fechaRadicado)
    numeroFactura = request.POST["numeroFactura"]
    print ("numeroFactura = ", numeroFactura)
    primerNombreVictima = request.POST["primerNombreVictima"]
    print ("primerNombreVictima = ", primerNombreVictima)

    # Aqui Manejo Transaccionalidad

    miConexion3 = None
    try:

        miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
        cur3 = miConexion3.cursor()
        comando = 'insert into admisiones_furips (documento_id,  "tipoDoc_id" , consec , "numeroRadicacion", "fechaRadicado" , "primerNombreVictima", "primerApellidoVictima" , "fechaRegistro" ,"estadoReg") values (' + "'" + str(registroId.documento_id) + "'," + "'" + str(registroId.tipoDoc_id) + "'," + "'" + str(registroId.consec) + "'" + ' , ' + "'" + str(numeroRadicacion) + "'" + '  , ' + "'" + str(fechaRadicado) + "'" + ', ' + "'" + str(primerNombreVictima) + "'," + "'" + str(primerApellidoVictima) + "','" + str(fechaRegistro) + "'," + "'" + str("A") + "');"
        print("comando = ", comando)
        cur3.execute(comando)
        miConexion3.commit()
        cur3.close()

        return JsonResponse({'success': True,  'Mensaje':'Furips Actualizado satisfactoriamente!'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()
        #print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensaje': error})

    finally:
        if miConexion3:
            miConexion3.close()


    # Aqui Fin Manejo Transaccionalidad


def load_dataAdmisiones(request, data):
    print("Entre load_data Admisiones")

    context = {}
    d = json.loads(data)

    Sede = d['sede']
    print("sede = ", Sede)

    ingresos = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    #detalle = 'SELECT i.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , ser.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual, (select count(*)  from facturacion_conveniospacienteingresos conv where conv."tipoDoc_id" = i."tipoDoc_id" and conv.documento_id=i.documento_id  and conv."consecAdmision"=i.consec) numConvenios,(select count(*)  from cartera_pagos pag where pag."tipoDoc_id" = i."tipoDoc_id" and pag.documento_id=i.documento_id  and pag.consec=i.consec) numPagos, empresa.nombre Empresa  FROM admisiones_ingresos i, usuarios_usuarios u, facturacion_empresas empresa , sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and empresa.id = i.empresa_id AND sd.servicios_id  = ser.id and  i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
    #        Sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = ser.id AND dep.disponibilidad = ' + "'" + 'O' + "'" + ' AND i."salidaDefinitiva" = ' + "'" + 'N' + "'" + ' and tp.id = u."tipoDoc_id" and i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and ser.nombre != ' + "'" + str('TRIAGE') + "'" + ' AND dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"'
    detalle = 'SELECT i.id id, tp.nombre tipoDoc,  u.documento documento, u.nombre  nombre , i.consec consec , i."fechaIngreso" , sd.nombre servicioNombreIng, dep.nombre camaNombreIng , diag.nombre dxActual, (select count(*)  from facturacion_conveniospacienteingresos conv where conv."tipoDoc_id" = i."tipoDoc_id" and conv.documento_id=i.documento_id  and conv."consecAdmision"=i.consec) numConvenios,	(select count(*)  from cartera_pagos pag where pag."tipoDoc_id" = i."tipoDoc_id" and pag.documento_id=i.documento_id  and pag.consec=i.consec) numPagos,	empresa.nombre Empresa, date_part(' + "'" + str('YEAR') + "'" + ' ,  AGE(CURRENT_DATE , U."fechaNacio")) edad, i."salidaClinica" salidaClinica FROM admisiones_ingresos i inner join usuarios_usuarios u on ( u."tipoDoc_id" = i."tipoDoc_id"  and u.id = i."documento_id" ) left join facturacion_empresas empresa on (empresa.id = i.empresa_id) inner join sitios_dependencias dep on (dep.id = i."dependenciasActual_id" and dep."sedesClinica_id" =  i."sedesClinica_id" AND dep.disponibilidad = ' + "'" + str('O') + "')"  + ' inner join sitios_serviciosSedes sd on (sd."sedesClinica_id" = i."sedesClinica_id" and sd.id= dep."serviciosSedes_id" and sd.id  = i."serviciosActual_id")  inner join clinico_servicios ser on (ser.id = sd.servicios_id and ser.nombre != ' + "'" + str('TRIAGE') + "')" + ' inner join usuarios_tiposDocumento tp on (tp.id = u."tipoDoc_id") inner join sitios_dependenciastipo deptip on ( deptip.id = dep."dependenciasTipo_id") left join  clinico_Diagnosticos diag on (diag.id = i."dxActual_id")  WHERE  i."sedesClinica_id" = ' + "'" + str(Sede) + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str('N') + "'" + ' AND i."fechaSalida" is null '
    print(detalle)

    curx.execute(detalle)

    for id, tipoDoc, documento, nombre, consec, fechaIngreso,  servicioNombreIng, camaNombreIng, dxActual, numConvenios, numPagos, Empresa , edad, salidaClinica in curx.fetchall():
            ingresos.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id': id, 'tipoDoc': tipoDoc, 'Documento': documento, 'Nombre': nombre,
                 'Consec': consec, 'FechaIngreso': fechaIngreso,   'servicioNombreIng': servicioNombreIng, 'camaNombreIng': camaNombreIng,
                   'DxActual': dxActual,'numConvenios':numConvenios,'numPagos':numPagos, 'Empresa':Empresa,'edad':edad, 'salidaClinica': salidaClinica}})

    miConexionx.close()
    print("ingresos = " , ingresos)
    context['Ingresos'] = ingresos


    serialized1 = json.dumps(ingresos, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def BuscaConveniosAbonoAdmision(request):

        print("Entre a buscar una Admision Modal")
        ingresoId = request.POST["ingresoId"]

        print("ingresoId = ", ingresoId)

        registroId = Ingresos.objects.get(id=ingresoId)

        # Combo Convenios Pacienmte


        miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
        curt = miConexiont.cursor()

        comando = 'SELECT p.convenio_id id, conv.nombre  nombre FROM facturacion_conveniospacienteingresos p , contratacion_convenios conv where conv.id = p.convenio_id AND  p."tipoDoc_id"  = '  + "'" +str(registroId.tipoDoc_id) + "' AND documento_id = " + "'" + str(registroId.documento_id) + "' AND " + '"consecAdmision" =' +"'" + str(registroId.consec) + "'"

        curt.execute(comando)
        print(comando)

        conveniosPaciente = []


        for id, nombre in curt.fetchall():
            conveniosPaciente.append({'id': id, 'nombre': nombre})

        miConexiont.close()
        print("conveniosPaciente", conveniosPaciente)

        # Fin combo Convenios

        serialized1 = json.dumps(conveniosPaciente, default=str)

        return HttpResponse(serialized1, content_type='application/json')


def Load_dataAutorizacionesAdmisiones(request, data):
    print("Entre  load_dataAutorizaciones")

    context = {}
    d = json.loads(data)

    ingresoId = d['ingresoId']
    sede = d['sede']

    print("sede:", sede)
    print("ingresoId:", ingresoId)


    RegistroId =  Ingresos.objects.get(id=ingresoId)

    autorizaciones = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curx = miConexionx.cursor()

    detalle = 'select aut.id id,  aut."fechaSolicitud" fechaSolicitud ,aut."numeroAutorizacion" numeroAutorizacion,aut."fechaAutorizacion" fechaAutorizacion, est.nombre estado, emp.nombre empresa,det.examenes_id examen ,det.cums_id cums, det."valorAutorizado" valorAutorizado, det."numeroAutorizacion" autDetalle, sum.nombre nombreSuministro, exa.nombre nombreExamen from autorizaciones_autorizaciones aut  inner join clinico_historia his on (his.id = aut.historia_id)  left join autorizaciones_autorizacionesdetalle det on (det.autorizaciones_id = aut.id)	inner join autorizaciones_estadosautorizacion est on (est.id = aut."estadoAutorizacion_id" ) left join facturacion_empresas emp on (emp.id = aut.empresa_id) left join facturacion_suministros sum on (sum.id=det.cums_id) left join clinico_examenes exa on (exa.id = det.examenes_id) WHERE his."tipoDoc_id" = ' + "'" + str(RegistroId.tipoDoc_id) + "' AND his.documento_id =" + "'" + str(RegistroId.documento_id) + "'" + ' AND his."consecAdmision" = ' +"'" + str(RegistroId.consec) + "'"

    print(detalle)

    curx.execute(detalle)

    for id, fechaSolicitud ,numeroAutorizacion,fechaAutorizacion,estado,empresa,examen,cums,valorAutorizado,autDetalle,nombreSuministro,nombreExamen in curx.fetchall():
        autorizaciones.append(
            {"model": "autorizaciones.autorizaciones", "pk": id, "fields":
                {'id': id, 'fechaSolicitud': fechaSolicitud, 'numeroAutorizacion': numeroAutorizacion, 'fechaAutorizacion': fechaAutorizacion, 'estado': estado,
                 'empresa': empresa, 'examen': examen, 'cums': cums,'valorAutorizado':valorAutorizado,'autDetalle':autDetalle,'nombreSuministro':nombreSuministro, 'nombreExamen':nombreExamen }})

    miConexionx.close()
    print("autorizaciones =  OJOOOOOOOOOOOOO ", autorizaciones)

    serialized1 = json.dumps(autorizaciones, default=str)

    print("Envio = ", serialized1)

    return HttpResponse(serialized1, content_type='application/json')


def ActualizaAdmision(request):
    print("entre ActualizaAdmision")

    ingresoId = request.POST['ingresoId']
    numManilla = request.POST["numManilla"]
    ips = request.POST["ips"]
    if ips=='':
        ips='null'

    remitido = request.POST["remitido"]
    print("ingresoId  = ", ingresoId)

    responsables = request.POST["responsables"]

    if responsables=='':
        responsables='null'

    acompanantes = request.POST["acompanantes"]

    if acompanantes=='':
        acompanantes='null'

    dxIngreso = request.POST["dxIngreso"]

    if dxIngreso=='':
        dxIngreso='null'



    tiposCotizante = request.POST["tiposCotizante"]
    if tiposCotizante=='':
        tiposCotizante='null'


    fechaRegistro = timezone.now()
    causasExterna = request.POST["causasExterna"]
    if causasExterna=='':
        causasExterna='null'

    regimenes = request.POST["regimenes"]
    if regimenes=='':
        regimenes='null'

    viasIngreso = request.POST["viasIngreso"]
    if viasIngreso=='':
        viasIngreso='null'


    medicoIngreso = request.POST["medicoIngreso"]
    if medicoIngreso=='':
        medicoIngreso='null'


    busEspecialidad = request.POST["busEspecialidad"]
    if busEspecialidad=='':
        busEspecialidad='null'



    empresa = request.POST["empresa"]
    if empresa=='':
        empresa='null'


    username_id = request.POST["username_id"]

    sede = request.POST['sede']
    sedeSeleccionada = request.POST['sedeSeleccionada']
    numReporte = request.POST['numReporte']
    grupo = request.POST['sede']
    subGrupo = request.POST['subGrupo']
    nombreSede = request.POST['nombreSede']
    profesional = request.POST['profesional']
    permisosGrales = request.POST['permisosGrales']
    escogeModulo = request.POST['escogeModulo']
    permisosDetalle = request.POST['permisosDetalle']


    ripsDestinoUsuarioEgresoRecienNacido = request.POST['ripsDestinoUsuarioEgresoRecienNacido']
    ripsEdadGestacional = request.POST['ripsEdadGestacional']
    ripsNumConsultasCPrenatal = request.POST['ripsNumConsultasCPrenatal']
    ripsPesoRecienNacido = request.POST['ripsPesoRecienNacido']
    ripsRecienNacido = request.POST['ripsRecienNacido']
    ripsCausaMotivoAtencion = request.POST['ripsCausaMotivoAtencion']
    ripsCondicionDestinoUsuarioEgreso = request.POST['ripsCondicionDestinoUsuarioEgreso']
    ripsGrupoServicios = request.POST['ripsGrupoServicios']
    ripsViaIngresoServicioSalud = request.POST['ripsViaIngresoServicioSalud']
    ripsmodalidadGrupoServicioTecSal = request.POST['ripsmodalidadGrupoServicioTecSal']
    ripsFinalidadConsulta = request.POST['ripsFinalidadConsulta']
    ripsServiciosIng = request.POST['ripsServiciosIng']


    if ripsDestinoUsuarioEgresoRecienNacido=='':
        ripsDestinoUsuarioEgresoRecienNacido='null'
    if ripsEdadGestacional=='':
        ripsEdadGestacional='null'
    if ripsNumConsultasCPrenatal=='':
        ripsNumConsultasCPrenatal='null'
    if ripsPesoRecienNacido=='':
        ripsPesoRecienNacido='null'
    if ripsRecienNacido=='':
        ripsRecienNacido='null'
    if ripsCausaMotivoAtencion=='':
        ripsCausaMotivoAtencion='null'
    if ripsCondicionDestinoUsuarioEgreso=='':
        ripsCondicionDestinoUsuarioEgreso='null'
    if ripsGrupoServicios=='':
        ripsGrupoServicios='null'
    if ripsViaIngresoServicioSalud=='':
        ripsViaIngresoServicioSalud='null'
    if ripsmodalidadGrupoServicioTecSal=='':
        ripsmodalidadGrupoServicioTecSal='null'
    if ripsFinalidadConsulta=='':
        ripsFinalidadConsulta='null'
    if ripsServiciosIng=='':
        ripsServiciosIng='null'


    ## Gauardo laActualizacion

    miConexion3 = None
    try:

            miConexion3 = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",  password="123456")
            cur3 = miConexion3.cursor()
            comando = 'UPDATE ADMISIONES_INGRESOS SET "numManilla" = ' + "'" + str(numManilla) + "'," + ' "ipsRemite_id" =    ' + str(ips) + "," +  ' "contactoResponsable_id" = ' + str(responsables) + "," +  '"contactoAcompañante_id" = ' + str(acompanantes) + "," + '"tiposCotizante_id" = ' + str(tiposCotizante) + "," +  '"causasExterna_id" =   ' + "'" + str(causasExterna) + "'," +  'regimen_id = ' + str(regimenes) + "," +   '"ViasIngreso_id" = ' + str(viasIngreso) + "," + '"medicoIngreso_id" = ' + str(medicoIngreso) + "," +  ' "especialidadesMedicosIngreso_id" = ' + str(busEspecialidad) + "," + 'empresa_id = '  + str(empresa)  + "," +  ' "ripsDestinoUsuarioEgresoRecienNacido_id" = ' + str(ripsDestinoUsuarioEgresoRecienNacido) +  "," +  ' "ripsEdadGestacional" = ' + str(ripsEdadGestacional) + "," +  ' "ripsNumConsultasCPrenatal" = ' + str(ripsNumConsultasCPrenatal) + "," +  ' "ripsPesoRecienNacido" = ' + str(ripsPesoRecienNacido) + "," +  ' "ripsRecienNacido" = ' + str(ripsRecienNacido) + "," +  ' "ripsCausaMotivoAtencion_id" = ' + str(ripsCausaMotivoAtencion) + "," +  ' "ripsCondicionDestinoUsuarioEgreso_id" = ' + str(ripsCondicionDestinoUsuarioEgreso) + "," +  ' "ripsGrupoServicios_id" = ' + str(ripsGrupoServicios) + "," +  ' "ripsViaIngresoServicioSalud_id" = ' + str(ripsViaIngresoServicioSalud) +  "," +  ' "ripsmodalidadGrupoServicioTecSal_id" = ' + str(ripsmodalidadGrupoServicioTecSal) + "," +  ' "ripsFinalidadConsulta_id" = ' + str(ripsFinalidadConsulta) +  "," +  ' "ripsServiciosIng_id" = ' + str(ripsServiciosIng)   + "," + '"dxIngreso_id" = ' + str(dxIngreso)  +  ' WHERE id = ' + "'" + str(ingresoId) + "'"
            print(comando)

            cur3.execute(comando)
            miConexion3.commit()
            cur3.close()

            return JsonResponse({'success': True, 'Mensaje': 'Ingreso Actualizado !'})

    except psycopg2.DatabaseError as error:
        print ("Entre por rollback" , error)
        if miConexion3:
            print("Entro ha hacer el Rollback")
            miConexion3.rollback()

        #print ("Voy a hacer el jsonresponde")
        return JsonResponse({'success': False, 'Mensaje': error})

    finally:
        print("Finally")
        if miConexion3:
            miConexion3.close()
            print("Cerre conexion")



def Load_dataCensoAdmisiones(request, data):
    print("Entre load_data Admisiones")

    context = {}
    d = json.loads(data)

    sede = d['sede']
    print("sede = ", sede)

    censo = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    detalle = 'select dep.id id,sed.nombre sede, serv.nombre servicio, subserv.nombre subservicio, dep.nombre nombre, tp.nombre tipoDoc ,u.documento documento,  u.nombre paciente, dep."fechaOcupacion" ocupa,  dep.disponibilidad accion FROM sitios_dependencias dep, usuarios_usuarios u, usuarios_tiposdocumento tp,sitios_sedesclinica sed, sitios_serviciossedes serv, sitios_subserviciossedes subserv WHERE dep."sedesClinica_id" = ' + "'" + str(sede) + "'" + ' AND sed.id=dep."sedesClinica_id" AND sed.id = serv."sedesClinica_id" AND sed.id = subserv."sedesClinica_id" AND  dep."serviciosSedes_id" = serv.id and dep."subServiciosSedes_id" = subserv.id AND dep."tipoDoc_id" = u."tipoDoc_id" and dep.documento_id = u.id and u."tipoDoc_id" = tp.id and dep.disponibilidad = ' + "'" + str('O') + "'" + ' ORDER By dep.numero, dep."fechaOcupacion"'
    print(detalle)

    curx.execute(detalle)

    for id,sede, servicio,subservicio, nombre, tipoDoc,  documento, paciente, ocupa, accion in curx.fetchall():
            censo.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id':id,'sede': sede, 'servicio':servicio, 'subservicio':subservicio, 'nombre':nombre, 'tipoDoc': tipoDoc, 'Documento': documento, 'paciente': paciente,
                 'ocupa': ocupa, 'accion': accion}})

    miConexionx.close()
    print("censo = " , censo)
    context['censo'] = censo


    serialized1 = json.dumps(censo, default=str)

    return HttpResponse(serialized1, content_type='application/json')


def Load_dataHabitacionesAdmisiones(request, data):
    print("Entre load_data Admisiones")

    context = {}
    d = json.loads(data)

    sede = d['sede']
    print("sede = ", sede)
    ingresoId = d['ingresoId']
    print("ingresoId = ", ingresoId)

    ingreso = Ingresos.objects.get(id=ingresoId)

    habitaciones = []

    miConexionx = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                       password="123456")
    curx = miConexionx.cursor()

    #detalle = 'select dep.id id,sed.nombre, serv.nombre, subserv.nombre, dep.numero numero,   case when his.disponibilidad = ' + "'" + str('L') + "'" + ' then ' + "'" + str('Libera') + "'" + ' else ' + "'" + str('Ocupa') + "'" + ' end accion,  case when his.disponibilidad =' + "'" + str('O') + "'" + ' then  his."fechaOcupacion" else  his."fechaLiberacion" end  fecha, tp.nombre tipoDoc 	,	u.documento documento, 	u.nombre paciente FROM sitios_dependencias dep, usuarios_usuarios u, usuarios_tiposdocumento tp,sitios_sedesclinica sed, 	sitios_serviciossedes serv, sitios_subserviciossedes subserv, sitios_historialdependencias his WHERE his.dependencias_id = dep.id AND dep."sedesClinica_id"  = ' + "'" + str(sede) + "'" + ' AND sed.id=dep."sedesClinica_id" AND sed.id = serv."sedesClinica_id" AND sed.id = subserv."sedesClinica_id" AND dep."serviciosSedes_id" = serv.id and dep."subServiciosSedes_id" = subserv.id AND dep."tipoDoc_id" = u."tipoDoc_id" and dep.documento_id = u.id and u."tipoDoc_id" = tp.id  ORDER By dep.numero, dep."fechaOcupacion"'
    detalle = 'select dep.id id,sed.nombre, serv.nombre, subserv.nombre, dep.numero numero,  case when his.disponibilidad = ' + "'" + str('L') + "'" + ' then ' + "'" + str('Libera') + "'" + ' else ' + "'" + str('Ocupa') + "'" + ' end accion, 	case when his.disponibilidad =' + "'" + str('O') + "'" + ' then  his."fechaOcupacion" else  his."fechaLiberacion" end fecha, tp.nombre tipoDoc 	,	u.documento documento, 	u.nombre paciente  	FROM  sitios_dependencias dep, usuarios_usuarios u, usuarios_tiposdocumento tp,sitios_sedesclinica sed, sitios_serviciossedes serv, sitios_subserviciossedes subserv, sitios_historialdependencias his WHERE	his.dependencias_id = dep.id AND dep."sedesClinica_id"  = ' + "'" + str(sede) + "'" + ' AND sed.id=dep."sedesClinica_id" AND sed.id = serv."sedesClinica_id" and  sed.id = subserv."sedesClinica_id" AND dep."serviciosSedes_id" =  serv.id and dep."subServiciosSedes_id" = subserv.id AND his."tipoDoc_id" = u."tipoDoc_id" and his.documento_id = u.id and u."tipoDoc_id" = tp.id  and his."tipoDoc_id" =' + "'" + str(ingreso.tipoDoc_id) + "'" + ' AND his.documento_id = ' + "'" + str(ingreso.documento_id) + "'" + ' ORDER By  his.id,his."fechaOcupacion", dep.numero'
    print(detalle)

    curx.execute(detalle)

    for id,sede, servicio,subservicio, numero, accion, fecha    , tipoDoc,  documento, paciente in curx.fetchall():
            habitaciones.append({"model": "ingresos.ingresos", "pk": id, "fields":
                {'id':id,'sede': sede, 'servicio':servicio, 'subservicio':subservicio, 'numero':numero, 'accion':accion, 'fecha':fecha, 'tipoDoc': tipoDoc, 'Documento': documento, 'paciente': paciente }})

    miConexionx.close()
    print("habitaciones = " , habitaciones)


    serialized1 = json.dumps(habitaciones, default=str)

    return HttpResponse(serialized1, content_type='application/json')

def buscarMunicipios(request):
    context = {}
    Departamento = request.GET["Departamento"]

    print ("Entre buscar  Municipio del Depto  =",Departamento)


    # Combo de Medicos Especialidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_departamentos d, sitios_municipios c WHERE c.departamento_id = d.id and d.id = '" + str(Departamento) + "' ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    municipios = []

    for id, nombre in curt.fetchall():
        municipios.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(municipios)


    context['Municipios'] = municipios


    return JsonResponse(json.dumps(municipios), safe=False)

def buscarLocalidades(request):
    context = {}
    municipio = request.GET["Municipio"]

    print ("Entre buscar  Localidades  de la municipio  =",municipio)


    # Combo de Medicos Especialidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = "SELECT c.id id, c.nombre  nombre FROM sitios_municipios d, sitios_localidades c WHERE c.municipio_id = d.id and d.id = '" + str(municipio) + "' ORDER BY c.nombre"

    curt.execute(comando)
    print(comando)

    localidades = []

    for id, nombre in curt.fetchall():
        localidades.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(localidades)


    context['Localidades'] = localidades


    return JsonResponse(json.dumps(localidades), safe=False)


def buscarConvenioEmpresa(request):
    context = {}
    empresaId = request.GET["empresaId"]

    print ("Entre buscar  Convenios de la empresa  =", empresaId)


    # Combo de Medicos Especialidades


    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres", password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT d.id id, d.nombre  nombre FROM contratacion_convenios d, facturacion_empresas c WHERE d.empresa_id = c.id AND c.id = ' + "'" + str(empresaId) + "'" + ' ORDER BY d.nombre '

    curt.execute(comando)
    print(comando)

    conveniosEmpresas = []

    for id, nombre in curt.fetchall():
        conveniosEmpresas.append({'id': id, 'nombre': nombre})

    miConexiont.close()
    print(conveniosEmpresas)


    context['ConveniosEmpresas'] = conveniosEmpresas


    return JsonResponse(json.dumps(conveniosEmpresas), safe=False)


def Indicadores(request):

    sede = request.POST["sede"]

    print ("Entre buscar  Convenios de la empresa  =", empresaId)

    # Combo Indicadores

    miConexiont = psycopg2.connect(host="192.168.79.133", database="vulner7Particionado", port="5432", user="postgres",
                                   password="123456")
    curt = miConexiont.cursor()

    comando = 'SELECT ser.nombre nombre, count(*) total FROM admisiones_ingresos i, usuarios_usuarios u, sitios_dependencias dep , clinico_servicios ser ,usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , clinico_Diagnosticos diag , sitios_serviciosSedes sd  WHERE sd."sedesClinica_id" = i."sedesClinica_id"  and sd.servicios_id  = ser.id and i."sedesClinica_id" = dep."sedesClinica_id" AND i."sedesClinica_id" = ' + "'" + str(
        sede) + "'" + ' AND  deptip.id = dep."dependenciasTipo_id" and i."serviciosActual_id" = sd.id AND dep.disponibilidad = ' + "'" + str(
        'O') + "'" + ' AND i."salidaDefinitiva" = ' + "'" + str(
        'N') + "'" + ' and tp.id = u."tipoDoc_id" and  i."tipoDoc_id" = u."tipoDoc_id" and u.id = i."documento_id" and diag.id = i."dxActual_id" and i."fechaSalida" is null and dep."serviciosSedes_id" = sd.id and dep.id = i."dependenciasActual_id"  group by ser.nombre UNION SELECT ser.nombre, count(*) total FROM triage_triage t, usuarios_usuarios u, sitios_dependencias dep , usuarios_tiposDocumento tp , sitios_dependenciastipo deptip  , sitios_serviciosSedes sd, clinico_servicios ser WHERE sd."sedesClinica_id" = t."sedesClinica_id"  and t."sedesClinica_id" = dep."sedesClinica_id" AND  t."sedesClinica_id" =  ' + "'" + str(
        sede) + "'" + ' AND dep."sedesClinica_id" =  sd."sedesClinica_id" AND dep.id = t.dependencias_id AND  t."serviciosSedes_id" = sd.id  AND deptip.id = dep."dependenciasTipo_id" and  tp.id = u."tipoDoc_id" and  t."tipoDoc_id" = u."tipoDoc_id" and u.id = t."documento_id"  and ser.id = sd.servicios_id and  dep."serviciosSedes_id" = sd.id and t."serviciosSedes_id" = sd.id and dep."tipoDoc_id" = t."tipoDoc_id" and  t."consecAdmision" = 0 and dep."documento_id" = t."documento_id" and ser.nombre = ' + "'" + str(
        'TRIAGE') + "'" + ' group by ser.nombre'

    curt.execute(comando)
    print(comando)

    indicadores = []

    for nombre, total in curt.fetchall():
        indicadores.append({'nombre': nombre, 'total': total})

    miConexiont.close()
    print(indicadores)

    print("YA PASE INDICADORES", indicadores)

    # Fin combo Indicadores

    return JsonResponse(json.dumps(indicadores), safe=False)


