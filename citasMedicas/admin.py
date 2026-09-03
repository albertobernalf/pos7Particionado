from django.contrib import admin

# Register your models here.

from citasMedicas.models import Calendario,TiposCitasMedicas, TiposAtencion, EstadosCitasMedicas, EstadosConsultorios, EstadosProgramacionCitasMedicas, Consultorios, AgendasMedicas, AgendasMedicasProgramacion, EstadoRestriccionAgendas, AgendasMedicasRestriccionProgramacion,  CitasMedicas, CitasMedicasDetalle , CronologiaCitasMedicas


@admin.register(Calendario)
class calendario(admin.ModelAdmin):

   list_display = ("id", "sedesClinica", "fechaDia","nombre")
   search_fields = ("id", "sedesClinica__nombre",  "fechaDia","nombre")
   # Filtrar
   list_filter = ("id", "sedesClinica",   "fechaDia","nombre")


@admin.register(TiposCitasMedicas)
class tiposCitasMedicas(admin.ModelAdmin):
   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")


@admin.register(TiposAtencion)
class tiposAtencion(admin.ModelAdmin):
   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")

@admin.register(EstadosCitasMedicas)
class estadosCitasMedicas(admin.ModelAdmin):
   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")

@admin.register(EstadosConsultorios)
class estadosConsultorios(admin.ModelAdmin):
   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")

@admin.register(EstadosProgramacionCitasMedicas)
class estadosProgramacionCitasMedicas(admin.ModelAdmin):
   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")

@admin.register(Consultorios)
class consultorios(admin.ModelAdmin):
   list_display = ("id", "sedesClinica", "dependencia", "consultorio", "nombre","dia","estadosConsultorios")
   search_fields = ("id", "sedesClinica__nombre", "dependencia", "consultorio", "nombre","dia","estadosConsultorios")
   # Filtrar
   list_filter = ("id", "sedesClinica", "dependencia", "consultorio", "nombre","dia","estadosConsultorios")

@admin.register(AgendasMedicas)
class agendasMedicas(admin.ModelAdmin):
   list_display = ("id", "sedesClinica", "especialidad", "especialidadesMedicos", "estadoAgenda")
   search_fields = ("id", "sedesClinica", "especialidad", "especialidadesMedicos", "estadoAgenda")
   # Filtrar
   list_filter = ("id", "sedesClinica", "especialidad", "especialidadesMedicos", "estadoAgenda")


@admin.register(AgendasMedicasProgramacion)
class agendasMedicasProgramacion(admin.ModelAdmin):
   list_display = ("id", "sedesClinica", "agendaMedica", "consultorio", "atiendeDesde","atiendeHasta","desDeHoraDeAlmuerzo","hastaHoraDeAlmuerzo","duracionCita","estadosProgramacioncitasMedicas")
   search_fields = ("id", "sedesClinica__NOMBRE", "agendaMedica", "consultorio", "atiendeDesde","atiendeHasta","desDeHoraDeAlmuerzo","hastaHoraDeAlmuerzo","duracionCita","estadosProgramacioncitasMedicas__nombre")
   # Filtrar
   list_filter = ("id", "sedesClinica", "agendaMedica", "consultorio", "atiendeDesde","atiendeHasta","desDeHoraDeAlmuerzo","hastaHoraDeAlmuerzo","duracionCita","estadosProgramacioncitasMedicas")



@admin.register(EstadoRestriccionAgendas)
class estadoRestriccionAgendas(admin.ModelAdmin):
   list_display = ("id", "nombre")
   search_fields = ("id", "nombre")
   # Filtrar
   list_filter = ("id", "nombre")

@admin.register(AgendasMedicasRestriccionProgramacion)
class agendasMedicasRestriccionProgramacion(admin.ModelAdmin):
   list_display = ("id", "sedesClinica","agendasMedicasProgramacion","noAtiendeDesde","noAatiendeHasta","estadoRestriccionAgendas")
   search_fields = ("id", "sedesClinica__nombre","agendasMedicasProgramacion","noAtiendeDesde","noAatiendeHasta","estadoRestriccionAgendas")
   # Filtrar
   list_filter = ("id", "sedesClinica","agendasMedicasProgramacion","noAtiendeDesde","noAatiendeHasta","estadoRestriccionAgendas")

@admin.register(CitasMedicas)
class citasMedicas(admin.ModelAdmin):
   list_display = ("id", "sedesClinica","agendasMedicasProgramacion","admision","soatAccidente","furips","fechaReserva","fechaSolicitada","fechaAtencion")
   search_fields = ("id", "sedesClinica__nombre","agendasMedicasProgramacion","admision","soatAccidente","furips","fechaReserva","fechaSolicitada","fechaAtencion")
   # Filtrar
   list_filter = ("id", "sedesClinica","agendasMedicasProgramacion","admision","soatAccidente","furips","fechaReserva","fechaSolicitada","fechaAtencion")


@admin.register(CitasMedicasDetalle)
class citasMedicasDetalle(admin.ModelAdmin):
   list_display = ("id", "citasMedicas" )
   search_fields = ("id", "citasMedicas")
   # Filtrar
   list_filter = ("id", "citasMedicas")

@admin.register(CronologiaCitasMedicas)
class cronologiaCitasMedicas(admin.ModelAdmin):
   list_display = ("id", "citasMedicas","estadosCitasMedicas")
   search_fields = ("id", "citasMedicas","estadosCitasMedicas")
   # Filtrar
   list_filter = ("id", "citasMedicas","estadosCitasMedicas")

