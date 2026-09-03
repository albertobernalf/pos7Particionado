console.log('Hola Alberto Hi!')

let dataTable;
let dataTableA;
let dataTableB;
let dataTableC;
let dataTableD;
let dataTableF;
let dataTableG;
let dataTableH;

let dataTableGlosasInitialized = false;
let dataTableGlosasDetalleInitialized = false;
let dataTableGlosasTransaccionInitialized = false;
let dataTableGlosasUsuariosInitialized = false;
let dataTableGlosasProcedimientosInitialized = false;
let dataTableGlosasHospitalizacionInitialized = false;
let dataTableGlosasMedicamentosInitialized = false;
let dataTableGlosasUrgenciasInitialized = false;


$(document).ready(function() {
    var table = $('#tablaGlosas').DataTable();
    
       $('#search').on('keyup', function() {
        var searchValue = this.value.split(' '); // Supongamos que los términos de búsqueda están separados por espacios
        
        // Aplica la búsqueda en diferentes columnas
        table
            .columns([3]) // Filtra en la primera columna
            .search(searchValue[0]) // Primer término de búsqueda
            .draw();

	  table
            .columns([9]) // Filtra en la segunda columna
            .search(searchValue[1]) // Segundo término de búsqueda
            .draw();


        
        table
            .columns([14]) // Filtra en la segunda columna
            .search(searchValue[1]) // Segundo término de búsqueda
            .draw();
    });
});


function arrancaGlosas(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsGlosas  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },

		{   
                    "targets": 25
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},


           ajax: {
                 url:"/load_dataGlosas/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='glosa'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miGlosa form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},

                { data: "fields.id"},
                { data: "fields.fechaRecepcion"},
                { data: "fields.saldoFactura"},
                { data: "fields.totalSoportado"},
                { data: "fields.totalAceptado"},
                { data: "fields.totalGlosa"},
                { data: "fields.totalNotasCredito"},

                { data: "fields.observaciones"},
                { data: "fields.fechaRegistro"},
                { data: "fields.estadoReg"},
		{ data: "fields.convenio_id"},
		{ data: "fields.nombreConvenio"},
                { data: "fields.usuarioRegistro_id"},
		 { data: "fields.factura_id"},
		 { data: "fields.fechaRespuesta"},
		 { data: "fields.tipoGlosa_id"},
		 { data: "fields.nombreTipoGlosa"},
		  { data: "fields.usuarioRecepcion_id"},
                { data: "fields.usuarioRespuesta_id"},    
                { data: "fields.valorGlosa"},    
                { data: "fields.estadoRadicacion_id"},    
                { data: "fields.estadoRecepcion_id"},    
                { data: "fields.estadoGlosaRecepcion"},    
                { data: "fields.sedesClinica_id"},    
                { data: "fields.ripsEnvio_id"},    

       ]
            }
	        dataTable = $('#tablaGlosas').DataTable(dataTableOptionsGlosas);




  }

    if (valorTabla == 2)
    {
        let dataTableOptionsGlosasDetalle  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '230px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     
                    "targets": 12
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},
           ajax: {
                 url:"/load_tablaGlosasDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
"render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' name='glosaDetalle' class='miGlosaDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
		},

		 { data: "fields.tipo"},
		 { data: "fields.id"},
             	 { data: "fields.consec"},
                { data: "fields.itemFactura"},
                { data: "fields.codigo"},
                { data: "fields.nombre"},
                { data: "fields.glosaNombre"},
	      { data: "fields.vrServicio"},
                { data: "fields.valorGlosa"},
                { data: "fields.valorSoportado2"},
                { data: "fields.valorAceptado"},
                { data: "fields.valorNotasCredito"},



                     ]
            }

            if  (dataTableGlosasDetalleInitialized)  {

		            dataTableH = $("#tablaGlosasDetalle").dataTable().fnDestroy();

                    }

                dataTableD = $('#tablaGlosasDetalle').DataTable(dataTableOptionsGlosasDetalle);

	            dataTableGlosasDetalleInitialized  = true;




      }


// la tres

    if (valorTabla == 3)
    {

      }


// la cuatro

    if (valorTabla == 4)
    {

        let dataTableOptionsGlosasTransaccion  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' class='miTransaccion form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
                    "targets": 8
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},
           ajax: {
                 url:"/load_tablaGlosasTransaccion/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	 { data: "fields.id"},
             	 { data: "fields.id"},
                { data: "fields.numDocumentoIdObligado"},
                { data: "fields.numNota"},
                { data: "fields.fechaRegistro"},
                { data: "fields.tipoNota_id"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.ripsEnvio_id"},
                { data: "fields.sedesClinica_id"},
                     ]
            }

            if  (dataTableGlosasTransaccionInitialized)  {

		            dataTableD = $("#tablaGlosasTransaccion").dataTable().fnDestroy();

                    }

                dataTableD = $('#tablaGlosasTransaccion').DataTable(dataTableOptionsGlosasTransaccion);

	            dataTableGlosasTransaccionInitialized  = true;
      }



// la cinco

    if (valorTabla == 5)
    {

        let dataTableOptionsGlosasUsuarios  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' class='miUsuarios form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
                    "targets": 16
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},
           ajax: {
                 url:"/load_tablaGlosasUsuarios/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	 { data: "fields.id"},
             	 { data: "fields.id"},
                { data: "fields.tipoDocumentoIdentificacion"},
                { data: "fields.tipoUsuario"},
                { data: "fields.fechaNacimiento"},
                { data: "fields.codSexo"},
                { data: "fields.codZonaTerritorialResidencia"},
                { data: "fields.incapacidad"},
                { data: "fields.consecutivo"},
                { data: "fields.fechaRegistro"},
                { data: "fields.codMunicipioResidencia_id"},
                { data: "fields.codPaisOrigen_id"},
                { data: "fields.codPaisResidencia_id"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.numDocumentoIdentificacion"},
                { data: "fields.ripsDetalle_id"},
                { data: "fields.ripsTransaccion_id"},

                     ]
            }

            if  (dataTableGlosasUsuariosInitialized)  {

		            dataTableE = $("#tablaGlosasUsuarios").dataTable().fnDestroy();

                    }

                dataTableE = $('#tablaGlosasUsuarios').DataTable(dataTableOptionsGlosasUsuarios);

	            dataTableGlosasUsuariosInitialized  = true;
      }


// la seis

    if (valorTabla == 6)
    {

        let dataTableOptionsGlosasProcedimientos  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' class='miProcedimientos form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
                    "targets": 23
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},
           ajax: {
                 url:"/load_tablaGlosasProcedimientos/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	 { data: "fields.id"},
              	 { data: "fields.id"},
                { data: "fields.codPrestador"},
                { data: "fields.fechaInicioAtencion"},
                { data: "fields.idMIPRES"},
                { data: "fields.numAutorizacion"},
                { data: "fields.numDocumentoIdentificacion"},
                { data: "fields.vrServicio"},
                { data: "fields.valorPagoModerador"},
                { data: "fields.consecutivo"},
                { data: "fields.codComplicacion_id"},
                { data: "fields.codDiagnosticoPrincipal_id"},
                { data: "fields.codDiagnosticoRelacionado_id"},
                { data: "fields.codProcedimiento_id"},
                { data: "fields.codServicio_id"},
                { data: "fields.conceptoRecaudo_id"},
                { data: "fields.finalidadTecnologiaSalud_id"},
                { data: "fields.grupoServicios_id"},
                { data: "fields.modalidadGrupoServicioTecSal_id"},
                { data: "fields.tipoDocumentoIdentificacion_id"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.viaIngresoServicioSalud_id"},
                { data: "fields.ripsDetalle_id"},
                { data: "fields.tipoPagoModerador_id"},



                     ]
            }

            if  (dataTableGlosasProcedimientosInitialized)  {

		            dataTableF = $("#tablaGlosasProcedimientos").dataTable().fnDestroy();

                    }

                dataTableF = $('#tablaGlosasProcedimientos').DataTable(dataTableOptionsGlosasProcedimientos);

	            dataTableGlosasProcedimientosInitialized  = true;
      }



// la siete

    if (valorTabla == 7)
    {

        let dataTableOptionsGlosasHospitalizacion  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' class='miHospitalizacion form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
                    "targets": 20
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},
           ajax: {
                 url:"/load_tablaGlosasHospitalizacion/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
  	 { data: "fields.id"},
                { data: "fields.codPrestador"},
                { data: "fields.fechaInicioAtencion"},
                { data: "fields.numAutorizacion"},
                { data: "fields.fechaEgreso"},
                { data: "fields.consecutivo"},
                { data: "fields.fechaRegistro"},
                { data: "fields.causaMotivoAtencion_id"},
                { data: "fields.codComplicacion_id"},
                { data: "fields.codDiagnosticoCausaMuerte_id"},
                { data: "fields.codDiagnosticoPrincipal_id"},
                { data: "fields.codDiagnosticoPrincipalE_id"},
                { data: "fields.codDiagnosticoRelacionadoE1_id"},
                { data: "fields.codDiagnosticoRelacionadoE2_id"},
                { data: "fields.codDiagnosticoRelacionadoE3_id"},
                { data: "fields.condicionDestinoUsuarioEgreso_id"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.viaIngresoServicioSalud_id"},
                { data: "fields.ripsDetalle_id_id"},
                { data: "fields.ripsTipos_id"},

                     ]
            }

            if  (dataTableGlosasHospitalizacionInitialized)  {

		            dataTableG = $("#tablaGlosasHospitalizacion").dataTable().fnDestroy();

                    }

                dataTableG = $('#tablaGlosasHospitalizacion').DataTable(dataTableOptionsGlosasHospitalizacion);

	            dataTableGlosasHospitalizacionInitialized  = true;
      }



// la ocho

    if (valorTabla == 8)
    {

        let dataTableOptionsGlosasMedicamentos  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' class='miMedicamentos form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
                    "targets": 22
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},
           ajax: {
                 url:"/load_tablaGlosasMedicamentos/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		 { data: "fields.id"},
	 	  { data: "fields.itemFactura"},
	  { data: "fields.nomTecnologiaSalud"},
	  { data: "fields.idMIPRES"},
	  { data: "fields.cums"},
	  { data: "fields.concentracionMedicamento"},
	  { data: "fields.cantidadMedicamento"},
  	 { data: "fields.vrUnitMedicamento"},
	  { data: "fields.vrServicio"},
	  { data: "fields.consecutivo"},
	  { data: "fields.tipoMedicamento_id"},
	  { data: "fields.unidadMedida_id"},
	  { data: "fields.cantidadGlosada"},
	  { data: "fields.cantidadAceptada"},
	  { data: "fields.cantidadSoportado"},
	  { data: "fields.valorGlosado"},
	  { data: "fields.vAceptado"},
	  { data: "fields.valorSoportado"},
	  { data: "fields.motivoGlosa_id"},
	  { data: "fields.notasCreditoGlosa"},
	  { data: "fields.notasCreditoOtras"},
	  { data: "fields.notasDebito"},

                     ]
            }

            if  (dataTableGlosasMedicamentosInitialized)  {

		            dataTableH = $("#tablaGlosasMedicamentos").dataTable().fnDestroy();

                    }

                dataTableH = $('#tablaGlosasMedicamentos').DataTable(dataTableOptionsGlosasMedicamentos);

	            dataTableGlosassMedicamentosInitialized  = true;
      }

// la nueve

    if (valorTabla == 9)
    {

        let dataTableOptionsGlosasUrgencias  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
    },
  ],
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' class='miUrgencias form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
                    "targets": 16
               }
            ],
	 pageLength: 3,
	  destroy: true,
	  language: {
		    processing: 'Procesando...',
		    lengthMenu: 'Mostrar _MENU_ registros',
		    zeroRecords: 'No se encontraron resultados',
		    emptyTable: 'Ningún dato disponible en esta tabla',
		    infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
		    infoFiltered: '(filtrado de un total de _MAX_ registros)',
		    search: 'Buscar:',
		    infoThousands: ',',
		    loadingRecords: 'Cargando...',
		    paginate: {
			      first: 'Primero',
			      last: 'Último',
			      next: 'Siguiente',
			      previous: 'Anterior',
		    }
			},
           ajax: {
                 url:"/load_tablaGlosasUrgencias/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	 { data: "fields.id"},
                { data: "fields.codPrestador"},
                { data: "fields.fechaInicioAtencion"},
                { data: "fields.fechaEgreso"},
                { data: "fields.consecutivo"},
                { data: "fields.fechaRegistro"},
                { data: "fields.causaMotivoAtencion_id"},
                { data: "fields.codDiagnosticoCausaMuerte_id"},
                { data: "fields.codDiagnosticoPrincipal_id"},
                { data: "fields.codDiagnosticoPrincipalE_id"},
                { data: "fields.codDiagnosticoRelacionadoE1_id"},
                { data: "fields.codDiagnosticoRelacionadoE2_id"},
                { data: "fields.codDiagnosticoRelacionadoE3_id"},
                { data: "fields.condicionDestinoUsuarioEgreso_id"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.ripsDetalle_id"},
                { data: "fields.ripsTipos_id"},

                     ]
            }

            if  (dataTableGlosasUrgenciasInitialized)  {

		            dataTableG = $("#tablaGlosasUrgencias").dataTable().fnDestroy();

                    }

                dataTableG = $('#tablaGlosasUrgencias').DataTable(dataTableOptionsGlosasUrgencias);

	            dataTableGlosasUrgenciasInitialized  = true;
      }





}

const initDataTableGlosas = async () => {
	if  (dataTableGlosasInitialized)  {
		dataTable.destroy();

}
    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	sedesClinica_id = sede;
	data['sedesClinica_id'] = sedesClinica_id
	data['facturaId'] = 1

        data = JSON.stringify(data);

         arrancaGlosas(1,data);
	 dataTableGlosasInitialized = true;
         arrancaGlosas(4,data);
         dataTableGlosasTransaccionInitialized = true;
	 arrancaGlosas(5,data);
	 dataTableGlosasUsuariosInitialized = true;
         arrancaGlosas(6,data);
	 dataTableGlosasProcedimientosInitialized = true;
         arrancaGlosas(7,data);
	 dataTableGlosasHospitalizacionInitialized = true;
         arrancaGlosas(8,data);
	 dataTableGlosasMedicamentosInitialized = true;
         arrancaGlosas(9,data);
	 dataTableGlosasUrgenciasInitialized = true;


}

 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableGlosas();
	 

});


 /* FIN ONLOAD */


 $('#tablaGlosas tbody').on('click', '.miGlosa', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila


        var data =  {}   ;

 	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	sedesClinica_id = sede;
	data['sedesClinica_id'] = sedesClinica_id

	var table = $('#tablaGlosas').DataTable();  // Inicializa el DataTable jquery 	      

  	        var rowindex = table.row(row).data(); // Obtiene los datos de la fila


	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato10 factura_id = " , dato3.factura_id); 

		var facturaId = dato3.factura_id;  // jquery
		var glosaId = dato3.id;

		data['facturaId'] = facturaId
		data['glosaId'] = glosaId;


	        data = JSON.stringify(data);

		// document.getElementById("facturaId").value = facturaId ;


	    arrancaGlosas(1,data);
	    dataTableGlosasTransaccionInitialized = true;

	        arrancaGlosas(2,data);
	    dataTableGlosasDetalleInitialized = true;


	        arrancaGlosas(4,data);
	    dataTableGlosasInitialized = true;

	        arrancaGlosas(5,data);
	    dataTableGlosasUsuariosInitialized = true;

        	arrancaGlosas(7,data);
	    dataTableGlosasHospitalizacion = true;

        	arrancaGlosas(8,data);
	    dataTableGlosasMedicamentos = true;

	// AQUI tengo que colocar los datosde la Glosa en el Formulario de General y demas

	document.getElementById("post_idGlo").innerHTML =post_id;
	document.getElementById("factura_idGlo").innerHTML = dato3.factura_id;
	document.getElementById("fechaRecepcionGlo").innerHTML = dato3.fechaRecepcion;
	document.getElementById("valorGlosaGlo").innerHTML = dato3.valorGlosa;
	document.getElementById("estadoRegGlo").innerHTML = dato3.estadoReg;
	document.getElementById("totalSoportadoGlo").innerHTML= dato3.totalSoportado;
	document.getElementById("totalAceptadoGlo").innerHTML = dato3.totalAceptado;

	document.getElementById("totalGlosaGlo").innerHTML= dato3.totalGlosa;
	document.getElementById("totalNotasCreditoGlo").innerHTML = dato3.totalNotasCredito;


	document.getElementById("saldoFacturaGlo").innerHTML = dato3.saldoFactura;
	document.getElementById("observacionesGlo").innerHTML = dato3.observaciones;

	document.getElementById("convenio_idGlo").value = dato3.convenio_id;
	document.getElementById("fechaRegistroGlo").innerHTML = dato3.fechaRegistro;
	document.getElementById("usuarioRegistro_idGlo").innerHTML = dato3.usuarioRegistro_id;
	document.getElementById("fechaRespuestaGlo").innerHTML = dato3.fechaRespuesta;
	document.getElementById("tipoGlosa_idGlo").value = dato3.tipoGlosa_id;
	document.getElementById("usuarioRecepcion_idGlo").innerHTML = dato3.usuarioRecepcion_id;
	document.getElementById("usuarioRespuesta_idGlo").innerHTML = dato3.usuarioRespuesta_id;


	document.getElementById("estadoRadicacion_idGlo").value = dato3.estadoRadicacion_id;
	document.getElementById("estadoRecepcion_idGlo").value = dato3.estadoRecepcion_id;


        	arrancaGlosas(6,data);
	    dataTableGlosasProcedimientos = true;


  });



 $('#tablaGlosasDetalle tbody').on('click', '.miGlosaDetalle', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila


	var table = $('#tablaGlosasDetalle').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
        console.log("dato3 de glosasdetalle = ", dato3);



     $.ajax({
		   data: {'tipo':dato3.tipo, 'id':dato3.id},
	        url: "/consultaGlosasDetalle/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

	$('#postFormGlosasDetalle').trigger("reset");

	alert("info[0] = " + info[0] );


  	$('#post_idGloDet').val(info[0].fields.id);
	document.getElementById("tipoGloDet").innerHTML = info[0].fields.tipo; 
	document.getElementById("glosaGloDet").innerHTML = document.getElementById("post_idGloDet").value;
	document.getElementById("itemFacturaGloDet").innerHTML = info[0].fields.itemFactura;
  	document.getElementById("codigoGloDet").innerHTML = info[0].fields.codigo;
	document.getElementById("nombreGloDet").innerHTML = info[0].fields.nombre;
	document.getElementById("vrServicioGloDet").innerHTML = info[0].fields.vrServicio;
  	$('#consecutivoGloDet').val(info[0].fields.consecutivo);
  	$('#valorGlosadoGloDet').val(info[0].fields.valorGlosa);
  	$('#vAceptadoGloDet').val(info[0].fields.valorAceptado);
  	$('#valorSoportadoGloDet').val(info[0].fields.valorSoportado);
  	$('#motivoGlosa_idGloDet').val(info[0].fields.motivoGlosa_id);
  	$('#notasCreditoGlosaGloDet').val(info[0].fields.valorNotasCredito);

		 $('#crearModelGlosasDetalle').modal('show');
                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalGlosasDetalle").value =   data.responseText;
                }
            });

  });



function GuardarGlosasDetalle()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var username_id = document.getElementById("username_id").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;


	    	var post_idGlo = document.getElementById("post_idGlo").innerHTML;
	    	var tipoGloDet = document.getElementById("tipoGloDet").innerHTML;
	        var glosaGloDet = document.getElementById("glosaGloDet").innerHTML;
	        var post_idGloDet = document.getElementById("post_idGloDet").innerHTML;
	        var motivoGlosa_idGloDet = document.getElementById("motivoGlosa_idGloDet").value;
	        var valorGlosadoGloDet = document.getElementById("valorGlosadoGloDet").value;
		var itemFacturaGloDet = document.getElementById("itemFacturaGloDet").innerHTML;

	        var observacionesGloDet = document.getElementById("observacionesGloDet").value;
	        var vAceptadoGloDet = document.getElementById("vAceptadoGloDet").value;
	        var valorGlosadoGloDet = document.getElementById("valorGlosadoGloDet").value;
	        var valorSoportadoGloDet = document.getElementById("valorSoportadoGloDet").value;
	        var notasCreditoGlosaGloDet = document.getElementById("notasCreditoGlosaGloDet").value;
	        var vrServicioGloDet = document.getElementById("vrServicioGloDet").innerHTML;


            $.ajax({
                data: {'post_idGlo':post_idGlo, 'tipoGloDet':tipoGloDet,'glosaGloDet':glosaGloDet,'post_idGloDet':post_idGloDet, 'motivoGlosa_idGloDet':motivoGlosa_idGloDet, 'valorGlosadoGloDet':valorGlosadoGloDet,'vAceptadoGloDet':vAceptadoGloDet, 'valorGlosadoGloDet':valorGlosadoGloDet, 'valorSoportadoGloDet':valorSoportadoGloDet, 'notasCreditoGlosaGloDet':notasCreditoGlosaGloDet,   'vrServicioGloDet':vrServicioGloDet,'username_id':username_id ,'itemFacturaGloDet':itemFacturaGloDet,'observacionesGloDet':observacionesGloDet },
	        url: "/guardarGlosasDetalle/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {


			if (data2.success == false )
				{
		
				document.getElementById("mensajesErrorDetalleModal").value = data2.Mensajes

					return ;
				}
	
				if (data2.success  == true )
				{


				 $('#postFormGlosasDetalle').trigger("reset");


			// filtrodata = JSON.stringify(data2['Data']);
	

			// filtrodata = filtrodata.replace ('[','');
			// filtrodata = filtrodata.replace (']','');
			// filtro = JSON.parse(filtrodata);



		// document.getElementById("valorGlosaGlo").innerHTML = filtro.fields.valorGlosa;
		// document.getElementById("totalSoportadoGlo").innerHTML = filtro.fields.totalSoportado;
		// document.getElementById("totalAceptadoGlo").innerHTML = filtro.fields.totalAceptado;
		// document.getElementById("saldoFacturaGlo").innerHTML = filtro.fields.saldoFactura;
		// document.getElementById("tipoGlosa_idGlo").value = filtro.fields.tipoGlosa_id;
		// document.getElementById("estadoRadicacion_idGlo").value = filtro.fields.estadoRadicacion_id;
		// document.getElementById("estadoRecepcion_idGlo").value = filtro.fields.estadoRecepcion_id;

		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

		var facturaId = dato3.factura_id;  // jquery
		data['facturaId'] = document.getElementById("factura_idGlo").innerHTML;
		data['glosaId'] = post_idGlo;


	        data = JSON.stringify(data);

			 arrancaGlosas(1,data);
			    dataTableGlosasInitialized = true;


        	arrancaGlosas(7,data);
	    dataTableGlosasHospitalizacion = true;

			 arrancaGlosas(2,data);
			    dataTableGlosasDetalleInitialized = true;

 		 $('#crearModelGlosasDetalle').modal('hide');


				}	// Cierra el if		

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalGlosasDetalle").value =   data.responseText;
                }
            });


}


function GuardaGlosasEstados()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;
		alert("Entre Guardar Glosas Estado");

	        var post_idGlo = document.getElementById("post_idGlo").innerHTML;
	        var tipoGlosa_idGlo = document.getElementById("tipoGlosa_idGlo").value;
	        var estadoRadicacion_idGlo = document.getElementById("estadoRadicacion_idGlo").value;
	        var estadoRecepcion_idGlo = document.getElementById("estadoRecepcion_idGlo").value;
	        var sedesClinica_idGlo = document.getElementById("sedesClinica_idGlo").innerHTML;




            $.ajax({
                data: {'post_idGlo':post_idGlo,'tipoGlosa_idGlo':tipoGlosa_idGlo,'estadoRadicacion_idGlo':estadoRadicacion_idGlo, 'estadoRecepcion_idGlo':estadoRecepcion_idGlo, 'sedesClinica_idGlo':sedesClinica_idGlo  },
	        url: "/guardaGlosasEstados/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {


		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

		var facturaId = document.getElementById("factura_idGlo").value;
		data['facturaId'] = document.getElementById("factura_idGlo").value;

	        data = JSON.stringify(data);
	
  		 if  (dataTableGlosasInitialized)  {
		            dataTableC = $("#tablaGlosas").dataTable().fnDestroy();
                    }

			 arrancaGlosas(1,data);
			    dataTableGlosasInitialized = true;

        	arrancaGlosas(7,data);
	    dataTableGlosasHospitalizacion = true;
			 arrancaGlosas(8,data);
			    dataTableGlosasMedicamentosInitialized = true;



		document.getElementById("mensajesError").value = data2.Mensajes;
                },
            error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
                }
            });


}



/*------------------------------------------
        --------------------------------------------
        ModalGlosas
        --------------------------------------------
        --------------------------------------------*/

function ModalGlosas()
{
    
	
	
            $('#post_id').val('');
            $('#postFormCrearEnviosRips').trigger("reset");
            $('#modelHeadingEnviosRips').html("Creacion Envios Rips");
var now = new Date();

    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today = now.getFullYear()+"-"+(month)+"-"+(day) ;

 document.getElementById("fechaRecepcion").value = today;
 document.getElementById("fechaRecepcionGlo").value = today;


            $('#crearModelEnviosRips').modal('show');
        
}

function Glosas()
{
    
	
	
            $('#post_id').val('');
            $('#postFormCrearGlosas').trigger("reset");
            $('#modelHeadingGlosas').html("Creacion Glosas");
            $('#crearModelGlosas').modal('show');
        
}



function CerrarModalJson()
{

            $('#crearModelRipsJson').modal('hide');
}


function CrearGlosas()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;
		alert("Entre Guardar Glosas Estado");

	        
		var convenio_id = document.getElementById("convenio_id").value;
	        var sedesClinica_id = document.getElementById("sedesClinica_id").value;
	        var fechaRecepcion = document.getElementById("fechaRecepcion").value;
	        var observaciones = document.getElementById("observaciones").value;
	        var factura_id = document.getElementById("factura_id").value;
	        var fechaRespuesta = document.getElementById("fechaRespuesta").value;
	        var tipoGlosa_id = document.getElementById("tipoGlosa_id").value;
	        var valorGlosa = document.getElementById("valorGlosa").value;
	        var estadoRecepcion_id = document.getElementById("estadoRecepcion_id").value;
	        var usuarioRegistro_id = document.getElementById("usuarioRegistro_id").value;
	        var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativos_id").value;


            $.ajax({
                data: {'serviciosAdministrativos_id':serviciosAdministrativos_id, 'convenio_id':convenio_id,'sedesClinica_id':sedesClinica_id, 'fechaRecepcion':fechaRecepcion, 'observaciones':observaciones,'factura_id':factura_id,  'fechaRespuesta':fechaRespuesta, 'tipoGlosa_id':tipoGlosa_id, 'valorGlosa':valorGlosa, 'estadoRecepcion_id':estadoRecepcion_id, 'usuarioRegistro_id':usuarioRegistro_id },
	        url: "/guardaGlosas/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {


		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

		var facturaId = document.getElementById("factura_idGlo").value;
		data['facturaId'] = document.getElementById("factura_idGlo").value;

	        data = JSON.stringify(data);
	
  		 if  (dataTableGlosasInitialized)  {
		            dataTableC = $("#tablaGlosas").dataTable().fnDestroy();
                    }

			 arrancaGlosas(1,data);
			    dataTableGlosasInitialized = true;

        	arrancaGlosas(7,data);
	    dataTableGlosasHospitalizacion = true;

			 arrancaGlosas(8,data);
			    dataTableGlosasMedicamentosInitialized = true;
		            $('#crearModelGlosas').modal('hide');


		document.getElementById("mensajesError").value = data2.Mensajes;

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalGlosas").value =   data.responseText;
                }
            });


}



