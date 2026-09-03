#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView,UpdateView,DeleteView)

from .models import Furips

class FuripsList(ListView):
    model = Furips


class FuripsDetail(DetailView):
    model = Furips


class FuripsCreation(CreateView):
    model = Furips
    success_url = reverse_lazy('furips:list')
    fields = ['id', 'sedesClinica', 'tipoDoc' , 'documento',  'consec'    , 'fechaRadicado' , 'numeroRadicacion' ,'numeroRadicadoAnterior' , 'numeroFactura' , 'primerNombreVictima' ,
    'segundoNombreVictima' , 'primerApellidoVictima' , 'segundoApellidoVictima' , 'tipoDocVictima',
    'documentoVictima', 'consecVictima', 'condicionAccidentado', 'evento', 'direccionEvento',  'departamentoEvento' ,'municipioEvento', 'localidadEvento' ,
    'zonaEvento', 'fechaEvento', 'eventoDescripcion', 'estado' ,'marcaVehiculo','placaVehiculo' ,'tipoServicioVehiculo' ,'tipoVehiculo', 'codigoaseguradora',
    'numeroPoliza','fechaIniPoliza', 'fechaFinPoliza ','intervencionAutoridad','cobroExcedentePoliza', 'primerNombrePropietario', 'segundoNombrePropietario',
    'primerApellidoPropietario', 'segundoApellidoPropietario', 'tipoDocPropietario', 'documentoPropietario', 'departamentoPropietario', 'municipioPropietario',
    'localidadPropietario', 'direccionPropietario', 'primerNombreInvolucrado', 'segundoNombreInvolucrado', 'primerApellidoInvolucrado','segundoApellidoInvolucrado',
    'tipoDocInvolucrado', 'documentoInvolucrado','departamentoInvolucrado','municipioInvolucrado', 'localidadInvolucrado', 'direccionInvolucrado', 'tipoReferencia',
    'fechaRemision', 'prestadorRemite', 'codigoInscripcion', 'profesionalRemite', 'fechaAceptacion', 'prestadorRecibe', 'codigoInscripcionRecibe', 'profesionalRecibe',
    'numeroPlacaTranporto', 'trasportoVictimaDesde', 'trasportoVictimaHasta', 'tipoTransporteTransporto', 'lugarRecogeVictima', 'certificacionIngreso',
    'certificacionEgreso', 'dxPrincIngreso', 'dxRel1Ingreso', 'dxRel2Ingreso','dxPrincEgreso','dxRel1Egreso', 'dxRel2Egreso', 'tipoDocProfesionalAtendio', 'documentoProfesionalAtendio', 'amparoReclamaFacturadoQx',
    'amparoReclamaAFosygaQx', 'amparoReclamaFacturadoGastos', 'amparoReclamaAFosygaGastos']


class FuripsUpdate(UpdateView):
    model = Furips
    success_url = reverse_lazy('furips:list')
    fields = ['id', 'sedesClinica', 'tipoDoc' , 'documento',  'consec'    , 'fechaRadicado' , 'numeroRadicacion' ,'numeroRadicadoAnterior' , 'numeroFactura' , 'primerNombreVictima' ,
    'segundoNombreVictima' , 'primerApellidoVictima' , 'segundoApellidoVictima' , 'tipoDocVictima',
    'documentoVictima', 'consecVictima', 'condicionAccidentado', 'evento', 'direccionEvento',  'departamentoEvento' ,'municipioEvento', 'localidadEvento' ,
    'zonaEvento', 'fechaEvento', 'eventoDescripcion', 'estado' ,'marcaVehiculo','placaVehiculo' ,'tipoServicioVehiculo' ,'tipoVehiculo', 'codigoaseguradora',
    'numeroPoliza','fechaIniPoliza', 'fechaFinPoliza ','intervencionAutoridad','cobroExcedentePoliza', 'primerNombrePropietario', 'segundoNombrePropietario',
    'primerApellidoPropietario', 'segundoApellidoPropietario', 'tipoDocPropietario', 'documentoPropietario', 'departamentoPropietario', 'municipioPropietario',
    'localidadPropietario', 'direccionPropietario', 'primerNombreInvolucrado', 'segundoNombreInvolucrado', 'primerApellidoInvolucrado','segundoApellidoInvolucrado',
    'tipoDocInvolucrado', 'documentoInvolucrado','departamentoInvolucrado','municipioInvolucrado', 'localidadInvolucrado', 'direccionInvolucrado', 'tipoReferencia',
    'fechaRemision', 'prestadorRemite', 'codigoInscripcion', 'profesionalRemite', 'fechaAceptacion', 'prestadorRecibe', 'codigoInscripcionRecibe', 'profesionalRecibe',
    'numeroPlacaTranporto', 'trasportoVictimaDesde', 'trasportoVictimaHasta', 'tipoTransporteTransporto', 'lugarRecogeVictima', 'certificacionIngreso',
    'certificacionEgreso', 'dxPrincIngreso', 'dxRel1Ingreso', 'dxRel2Ingreso','dxPrincEgreso','dxRel1Egreso', 'dxRel2Egreso', 'tipoDocProfesionalAtendio', 'documentoProfesionalAtendio', 'amparoReclamaFacturadoQx',
    'amparoReclamaAFosygaQx', 'amparoReclamaFacturadoGastos', 'amparoReclamaAFosygaGastos']


class FuripsDelete(DeleteView):
    model = Furips
    success_url = reverse_lazy('furips:list')
    reverse_lazy('furips:list')
    fields = ['id', 'sedesClinica', 'tipoDoc' , 'documento',  'consec'    , 'fechaRadicado' , 'numeroRadicacion' ,'numeroRadicadoAnterior' , 'numeroFactura' , 'primerNombreVictima' ,
    'segundoNombreVictima' , 'primerApellidoVictima' , 'segundoApellidoVictima' , 'tipoDocVictima',
    'documentoVictima', 'consecVictima', 'condicionAccidentado', 'evento', 'direccionEvento',  'departamentoEvento' ,'municipioEvento', 'localidadEvento' ,
    'zonaEvento', 'fechaEvento', 'eventoDescripcion', 'estado' ,'marcaVehiculo','placaVehiculo' ,'tipoServicioVehiculo' ,'tipoVehiculo', 'codigoaseguradora',
    'numeroPoliza','fechaIniPoliza', 'fechaFinPoliza ','intervencionAutoridad','cobroExcedentePoliza', 'primerNombrePropietario', 'segundoNombrePropietario',
    'primerApellidoPropietario', 'segundoApellidoPropietario', 'tipoDocPropietario', 'documentoPropietario', 'departamentoPropietario', 'municipioPropietario',
    'localidadPropietario', 'direccionPropietario', 'primerNombreInvolucrado', 'segundoNombreInvolucrado', 'primerApellidoInvolucrado','segundoApellidoInvolucrado',
    'tipoDocInvolucrado', 'documentoInvolucrado','departamentoInvolucrado','municipioInvolucrado', 'localidadInvolucrado', 'direccionInvolucrado', 'tipoReferencia',
    'fechaRemision', 'prestadorRemite', 'codigoInscripcion', 'profesionalRemite', 'fechaAceptacion', 'prestadorRecibe', 'codigoInscripcionRecibe', 'profesionalRecibe',
    'numeroPlacaTranporto', 'trasportoVictimaDesde', 'trasportoVictimaHasta', 'tipoTransporteTransporto', 'lugarRecogeVictima', 'certificacionIngreso',
    'certificacionEgreso', 'dxPrincIngreso', 'dxRel1Ingreso', 'dxRel2Ingreso','dxPrincEgreso','dxRel1Egreso', 'dxRel2Egreso', 'tipoDocProfesionalAtendio', 'documentoProfesionalAtendio', 'amparoReclamaFacturadoQx',
    'amparoReclamaAFosygaQx', 'amparoReclamaFacturadoGastos', 'amparoReclamaAFosygaGastos']

