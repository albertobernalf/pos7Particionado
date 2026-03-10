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
let dataTableGlosasDetalleRipsInitialized = false;
let dataTableGlosasTotalesDetalleInitialized = false;
let dataTableGlosasTransaccionInitialized = false;
let dataTableGlosasUsuariosInitialized = false;
let dataTableGlosasProcedimientosInitialized = false;
let dataTableGlosasHospitalizacionInitialized = false;
let dataTableGlosasMedicamentosInitialized = false;
let dataTableGlosasUrgenciasInitialized = false;
let dataTableGlosasAdicionarInitialized = false;
let dataTableNotasCreditoInitialized = false;
let dataTableNotasCreditoDetalleInitialized = false;
let dataTableNotasCreditoDetalleRipsInitialized = false;



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
                { data: "fields.totalSoportado"},
                { data: "fields.totalAceptado"},
                { data: "fields.totalGlosa"},
                { data: "fields.totalNotasCredito"},
                { data: "fields.observaciones"},
                { data: "fields.fechaRegistro"},
                { data: "fields.estadoReg"},
                { data: "fields.usuarioRegistro_id"},
		 { data: "fields.fechaRespuesta"},
		 { data: "fields.tipoGlosa_id"},
		 { data: "fields.nombreTipoGlosa"},
		  { data: "fields.usuarioRecepcion_id"},
                { data: "fields.usuarioRespuesta_id"},              
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
                    "targets": 6
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
                          btn = btn + " <input type='radio' name='glosaDetalle' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miGlosaDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },
		},
		{ data: "fields.id"},
                { data: "fields.factura_id"},

                { data: "fields.valorGlosa"},
                { data: "fields.valorAceptado"},
                { data: "fields.valorNotasCredito"},
                { data: "fields.valorSoportado"},

		{
		"render": function ( data, type, row ) {
                        var btn = '';
		 btn = btn + " <button class='miBorrarGlosaDetalle btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: red;'  data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
		},


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

       let dataTableOptionsGlosasDetalleRips  ={
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
            scrollY: '225px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },

		{   
                    "targets": 11
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
                 url:"/load_tablaGlosasDetalleRips/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='glosasDetalleRips'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miGlosasDetalleRips form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},

                { data: "fields.tipo"},
                { data: "fields.id"},
                { data: "fields.consec"},
                { data: "fields.itemFactura"},
                { data: "fields.codigo"},
                { data: "fields.nombre"},
                { data: "fields.vrServicio"},
                { data: "fields.valorGlosa"},
                { data: "fields.valorSoportado"},
                { data: "fields.valorAceptado"},
                { data: "fields.valorNotasCredito"},

	{
		"render": function ( data, type, row ) {
                        var btn = '';
		 btn = btn + " <button class='miBorrarGlosasDetalleRips btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: red;'  data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
		},


       ]
            }
	        dataTable = $('#tablaGlosasDetalleRips').DataTable(dataTableOptionsGlosasDetalleRips);
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


    if (valorTabla == 10)
    {
        let dataTableOptionsGlosasAdicionar  ={
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
            scrollY: '100px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },

		{   
                    "targets": 11
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
                 url:"/load_dataGlosasAdicionar/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='glosaAdicionar'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miGlosaAdicionar form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},


                { data: "fields.id"},
              
                { data: "fields.fechaRecepcion"},
                { data: "fields.saldoFactura"},
		  { data: "fields.totalGlosa"},
                { data: "fields.totalAceptado"},
                { data: "fields.totalNotasCredito"},
                { data: "fields.totalSoportado"},
		{ data: "fields.nombreConvenio"},
		 { data: "fields.fechaRespuesta"},
		 { data: "fields.tipoGlosa_id"},
		 { data: "fields.nombreTipoGlosa"},  
       ]
            }
	        dataTable = $('#tablaGlosasAdicionar').DataTable(dataTableOptionsGlosasAdicionar);




  }


    if (valorTabla == 11)
    {
        let dataTableOptionsGlosasTotalesDetalle  ={
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
                 url:"/load_tablaGlosasTotalesDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
"render": function ( data, type, row ) {
                        var btn = '';
                          btn = btn + " <input type='radio' name='glosaTotalDetalle' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miGlosaTotalDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

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
                { data: "fields.valorAceptado"},
                { data: "fields.valorNotasCredito"},
                { data: "fields.valorSoportado2"},

                     ]
            }

            if  (dataTableGlosasTotalesDetalleInitialized)  {

		            dataTableH = $("#tablaGlosasTotalesDetalle").dataTable().fnDestroy();

                    }

                dataTableD = $('#tablaGlosasTotalesDetalle').DataTable(dataTableOptionsGlosasTotalesDetalle);

	            dataTableGlosasTotalesDetalleInitialized  = true;

      }

    if (valorTabla == 12)
    {
        let dataTableOptionsNotasCredito  ={
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
                    "targets": 7
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
                 url:"/load_dataNotasCredito/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='notaCredito'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miNotaCredito form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},
                { data: "fields.id"},
		 { data: "fields.serviciosAdministrativos_id"},
                { data: "fields.fechaNota"},
                { data: "fields.valorNota"},
                { data: "fields.fechaRegistro"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.descripcion"},
{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='miEditaNotaCredito'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miEditaNotaCredito form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},
       ]
            }
	        dataTable = $('#tablaNotasCredito').DataTable(dataTableOptionsNotasCredito);

  }

    if (valorTabla == 13)
    {
        let dataTableOptionsNotasCreditoDetalle  ={
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
                    "targets": 11
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
                 url:"/load_dataNotasCreditoDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='notaCreditoDetalle'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miNotaCreditoDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},
                { data: "fields.id"},
		 { data: "fields.notaCredito"},
                { data: "fields.factura_id"},
                { data: "fields.valorNota"},
                { data: "fields.nombreTipoNota"},
                { data: "fields.fechaRegistro"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.totalFactura"},
                { data: "fields.totalGlosas"},
                { data: "fields.totalNotasCredito"},
                { data: "fields.saldoFactura"},

       ]
            }
	        dataTable = $('#tablaNotasCreditoDetalle').DataTable(dataTableOptionsNotasCreditoDetalle);

  }


    if (valorTabla == 14)
    {
        let dataTableOptionsNotasCreditoDetalleRips  ={
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
            scrollY: '225px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },

		{   
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
                 url:"/load_dataNotasCreditoDetalleRips/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='notaCreditoDetalleRips'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miNotaCreditoDetalleRips form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},

                { data: "fields.tipo"},
                { data: "fields.id"},
                { data: "fields.consec"},
                { data: "fields.itemFactura"},
                { data: "fields.codigo"},
                { data: "fields.nombre"},
                { data: "fields.vrServicio"},
                { data: "fields.valorNota"},
	{
		"render": function ( data, type, row ) {
                        var btn = '';
		 btn = btn + " <button class='miBorrarNotaCreditoDetalleRips btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: red;'  data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
		},


       ]
            }
	        dataTable = $('#tablaNotasCreditoDetalleRips').DataTable(dataTableOptionsNotasCreditoDetalleRips);

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
         arrancaGlosas(11,data);
	 dataTableGlosasTotalesInitialized = true;
         arrancaGlosas(12,data);
	 dataTableNotasCreditoInitialized = true;


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

	// AQUI tengo que colocar los datosde la Glosa en el Formulario de General y demas

	document.getElementById("post_idGlo").innerHTML =dato3.id;
	document.getElementById("factura_idGlo").innerHTML = dato3.factura_id;
	document.getElementById("facturaAdicionar_id").value = dato3.factura_id;
	//document.getElementById("convenio_idGlo").value = dato3.convenio_id;
	//document.getElementById("convenioAdicionar_id").value = dato3.convenio_id;
	document.getElementById("tipoGlosa_idGlo").value = dato3.tipoGlosa_id;
	document.getElementById("estadoRadicacion_idGlo").value = dato3.estadoRadicacion_id;
	document.getElementById("estadoRecepcion_idGlo").value = dato3.estadoRecepcion_id;

  });



 $('#tablaGlosasAdicionar tbody').on('click', '.miGlosaAdicionar', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila

        var data =  {}   ;
	alert("post_id = " + post_id);

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

	var table = $('#tablaGlosasAdicionar').DataTable();  // Inicializa el DataTable jquery 	      

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


	// AQUI tengo que colocar los datosde la Glosa en el Formulario de General y demas

	document.getElementById("post_idGlo").innerHTML =post_id;
	document.getElementById("factura_idGlo").innerHTML = dato3.factura_id;
	// document.getElementById("fechaRecepcionGlo").innerHTML = dato3.fechaRecepcion;
	// document.getElementById("valorGlosaGlo").innerHTML = dato3.valorGlosa;
	//document.getElementById("estadoRegGlo").innerHTML = dato3.estadoReg;
	//document.getElementById("totalSoportadoGlo").innerHTML= dato3.totalSoportado;
	//document.getElementById("totalAceptadoGlo").innerHTML = dato3.totalAceptado;

	//document.getElementById("totalGlosaGlo").innerHTML= dato3.totalGlosa;
	//document.getElementById("totalNotasCreditoGlo").innerHTML = dato3.totalNotasCredito;


	//document.getElementById("saldoFacturaGlo").innerHTML = dato3.saldoFactura;
	// document.getElementById("observacionesGlo").innerHTML = dato3.observaciones;

	document.getElementById("convenio_idGlo").value = dato3.convenio_id;
	//document.getElementById("fechaRegistroGlo").innerHTML = dato3.fechaRegistro;
	//document.getElementById("usuarioRegistro_idGlo").innerHTML = dato3.usuarioRegistro_id;
	//document.getElementById("fechaRespuestaGlo").innerHTML = dato3.fechaRespuesta;
	document.getElementById("tipoGlosa_idGlo").value = dato3.tipoGlosa_id;
	//document.getElementById("usuarioRecepcion_idGlo").innerHTML = dato3.usuarioRecepcion_id;
	//document.getElementById("usuarioRespuesta_idGlo").innerHTML = dato3.usuarioRespuesta_id;
	document.getElementById("estadoRadicacion_idGlo").value = dato3.estadoRadicacion_id;
	document.getElementById("estadoRecepcion_idGlo").value = dato3.estadoRecepcion_id;

        	arrancaGlosas(10,data);
	    dataTableGlosasAdicionarInitialized  = true;

	    arrancaGlosas(1,data);
	    dataTableGlosasTransaccionInitialized = true;

	        arrancaGlosas(2,data);
	    dataTableGlosasDetalleInitialized = true;

//	        arrancaGlosas(4,data);
//	    dataTableGlosasInitialized = true;

//	        arrancaGlosas(5,data);
//	    dataTableGlosasUsuariosInitialized = true;

//        	arrancaGlosas(7,data);
//	    dataTableGlosasHospitalizacion = true;

//        	arrancaGlosas(8,data);
//	    dataTableGlosasMedicamentos = true;

//        	arrancaGlosas(6,data);
//	    dataTableGlosasProcedimientos = true;

  });


 $('#tablaGlosasDetalle tbody').on('click', '.miGlosaDetalle', function() {

	alert("Entre glosas detalle ");

        var data =  {}   ;
       // post_id = document.getElementById("post_idGlo").innerHTML;
	var table = $('#tablaGlosasDetalle').DataTable();  // Inicializa el DataTable jquery
var row = $(this).closest('tr'); // Encuentra la fila
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila

	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
    console.log("dato3 de glosasdetalleRips = ", dato3);
    var post_id = dato3.id
    var facturaId = dato3.factura_id

	alert("post_id = " + post_id);

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
    data['facturaId'] = facturaId;
	data['glosaId'] = post_id;

        data = JSON.stringify(data);

        arrancaGlosas(3,data);
        dataTableGlosasDetalleRipsInitialized = true;

  });


 $('#tablaGlosasDetalleRips tbody').on('click', '.miGlosaDetalleRips', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	alert("Entre glosas detalle RIPS");

	var table = $('#tablaGlosasDetalleRips').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
        console.log("dato3 de glosasdetalleRips = ", dato3);



     $.ajax({
		   data: {'tipo':dato3.tipo, 'id':dato3.id},
	        url: "/consultaGlosasDetalleRips/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

	$('#postFormGlosasDetalle').trigger("reset");

	alert("info[0] = " + JSON.stringify(info[0]) );


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



 $('#tablaGlosasDetalle tbody').on('click', '.miBorrarGlosaDetalle', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	alert("entre a borrar" + post_id);



	var table = $('#tablaGlosasDetalle').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
        console.log("dato3 de glosasdetalle = ", dato3);
	var ripsId = dato3.id;
	var glosaId = dato3.glosaId;
	alert("ripsId = " + ripsId);
	alert("glosaId = " + glosaId);
	facturaId = document.getElementById("factura_idGlo").innerHTML;

     $.ajax({
		   data: {'ripsId':ripsId, 'detGloId':dato3.detGloId,'glosaId':glosaId},
	        url: "/borraGlosasDetalle/",
                type: "POST",
                dataType: 'json',
                success: function (info) {


        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

	var facturaId = dato3.factura_id;

	var data =  {}   ;

        data['username'] = username;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['sedesClinica_id'] = sede;
	data['facturaId'] = facturaId
	data['glosaId'] = glosaId;
        data = JSON.stringify(data);

	    arrancaGlosas(10,data);
	    dataTableGlosasAdicionarInitialized  = true;

	        arrancaGlosas(2,data);
	    dataTableGlosasDetalleInitialized = true;

                },
              error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
                }
            });

  });



 $('#tablaNotasCreditoDetalleRips tbody').on('click', '.miBorrarNotaCreditoDetalleRips', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	alert("entre a borrar Notas Credito detalle rips" + post_id);

        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;


	var table = $('#tablaNotasCreditoDetalleRips').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
        console.log("dato3 de glosasdetalle = ", dato3);
        var ripsId = dato3.id;
        var detCreRipsId = dato3.detCreRipsId;
	var valorNota = dato3.valorNota;
	if (valorNota==null)
		{
		alert("Nulo");
		valorNota=0
		}

     $.ajax({
		   data: {'ripsId':ripsId, 'detCreRipsId':dato3.detCreRipsId,'valorNota':valorNota},
	        url: "/borraNotasCreditoDetalleRips/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

	var facturaId = dato3.factura_id;

	var data =  {}   ;

        data['username'] = username;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['sedesClinica_id'] = sede;
	var username_id = document.getElementById("notaCreditoDetalleId").value;

	data['notaCreditoDetalle'] = notaCreditoDetalleId

        data = JSON.stringify(data);

	    arrancaGlosas(14,data);
	    dataTableNotasCreditoDetalleRipsInitialized  = true;

                },
              error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
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
		var facturaId =	document.getElementById("factura_idGlo").innerHTML;
		data['facturaId'] = facturaId;
		data['glosaId'] = post_idGlo;


	        data = JSON.stringify(data);

			 arrancaGlosas(1,data);
			    dataTableGlosasInitialized = true;


//        	arrancaGlosas(7,data);
//	    dataTableGlosasHospitalizacion = true;

			 arrancaGlosas(2,data);
			    dataTableGlosasDetalleInitialized = true;

			 arrancaGlosas(10,data);
			    dataTableGlosasAdicionarInitialized = true;


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

		var facturaId = document.getElementById("factura_idGlo").innerHTML;
		data['facturaId'] = document.getElementById("factura_idGlo").innerHTML;

	        data = JSON.stringify(data);
	
  	
			 arrancaGlosas(1,data);
			    dataTableGlosasInitialized = true;

        //	arrancaGlosas(7,data);
	 //    dataTableGlosasHospitalizacion = true;
	 //		 arrancaGlosas(8,data);
	 //		    dataTableGlosasMedicamentosInitialized = true;



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

function NotasCredito()
{
    
	
	
            $('#post_id').val('');
            $('#postFormCrearNotasCredito').trigger("reset");
            $('#modelHeadingMotasCredito').html("Creacion NotasCredito");
            $('#crearModelNotasCredito').modal('show');
        
}



function GlosasAdicionar()
{
    
            $('#post_id').val('');
            $('#postFormCrearGlosasAdicionar').trigger("reset");
            $('#modelHeadingGlosas').html("Creacion Glosas  Factura");
            $('#crearModelGlosasAdicionar').modal('show');
        
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
	        var totalGlosa = document.getElementById("totalGlosa").value;
	        var estadoRecepcion_id = document.getElementById("estadoRecepcion_id").value;
	        var usuarioRegistro_id = document.getElementById("usuarioRegistro_id").value;
	        var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativos_id").value;


            $.ajax({
                data: {'serviciosAdministrativos_id':serviciosAdministrativos_id, 'convenio_id':convenio_id,'sedesClinica_id':sedesClinica_id, 'fechaRecepcion':fechaRecepcion, 'observaciones':observaciones,'factura_id':factura_id,  'fechaRespuesta':fechaRespuesta, 'tipoGlosa_id':tipoGlosa_id, 'totalGlosa':totalGlosa, 'estadoRecepcion_id':estadoRecepcion_id, 'usuarioRegistro_id':usuarioRegistro_id },
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

		var facturaId = document.getElementById("factura_idGlo").innerHTML;
		data['facturaId'] = document.getElementById("factura_idGlo").value;

	        data = JSON.stringify(data);
	
  	
			 arrancaGlosas(1,data);
			    dataTableGlosasInitialized = true;

//        	arrancaGlosas(7,data);
//	    dataTableGlosasHospitalizacion = true;

//			 arrancaGlosas(8,data);
//			    dataTableGlosasMedicamentosInitialized = true;
		            $('#crearModelGlosas').modal('hide');


		document.getElementById("mensajesError").value = data2.Mensajes;

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalGlosas").value =   data.responseText;
                }
            });


}



function CrearNotasCredito()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;
		alert("Entre Guardar NC");

        
	        var sedesClinica_id = document.getElementById("sedesClinica_id").value;
	        var fechaNota = document.getElementById("fechaNota").value;
	        var valorNota = document.getElementById("valorNotaNC").value;
	        var descripcion = document.getElementById("descripcionNc").value;
	        var usuarioRegistro_id = document.getElementById("usuarioRegistro_id").value;
	        var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativosNC_id").value;


            $.ajax({
                data: {'serviciosAdministrativos_id':serviciosAdministrativos_id, 'sedesClinica_id':sedesClinica_id, 'fechaNota':fechaNota, 'valorNota':valorNota , 'usuarioRegistro_id':usuarioRegistro_id,'descripcion':descripcion },
	        url: "/guardaNotasCredito/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

			if (data2.success == false )
				{
				document.getElementById("mensajesErrorModalNotasCredito").value = data2.Mensajes
					return ;
				}

		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

	        data = JSON.stringify(data);
		
			 arrancaGlosas(12,data);
			    dataTableNotasCReditoInitialized = true;

		            $('#crearModelNotasCredito').modal('hide');

                },
              error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
                }
            });


}


function CrearNotasCreditoDetalle()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;
		
      
	        var sedesClinica_id = document.getElementById("sedesClinica_id").value;
	        var tipoNotaCredito = document.getElementById("tipoNotaCredito").value;
	        var notaCredito = document.getElementById("notaCreditoId").value;
	        var factura = document.getElementById("facturaDetalle").value;
	        var valorNota = document.getElementById("valorNotaDetalle").value;

		alert("Entre Guardar tipo Nota credito detalle " +  tipoNotaCredito );

            $.ajax({
                data: {'sedesClinica_id':sedesClinica_id, 'notaCredito':notaCredito, 'tipoNotaCredito':tipoNotaCredito, 'valorNota':valorNota ,'factura':factura,  'username_id':username_id },
	        url: "/guardaNotasCreditoDetalle/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

			if (data2.success == false )
				{
				document.getElementById("mensajesError").value = data2.Mensajes
					return ;
				}

		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;
		data['notaCredito'] = notaCredito;

	        data = JSON.stringify(data);
		
			 arrancaGlosas(12,data);
			    dataTableNotasCReditoInitialized = true;


			 arrancaGlosas(13,data);
			    dataTableNotasCreditoInitialized = true;


                },
              error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
                }
            });


}


function CrearGlosasAdicionar()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;
		alert("Entre Guardar Glosas Adicionar ");      

	        var sedesClinica_id = document.getElementById("sedesClinicaAdicionar_id").value;
	        var observaciones = document.getElementById("observacionesAdicionar").value;
	        var factura_id = document.getElementById("facturaAdicionar_id").value;
	        //var tipoGlosa_id = document.getElementById("tipoGlosaAdicionar_id").value;
	        var totalGlosa = document.getElementById("totalGlosaAdicionar").value;
	        // var estadoRecepcion_id = document.getElementById("estadoRecepcionAdicionar_id").value;
	        var usuarioRegistro_id = document.getElementById("usuarioRegistroAdicionar_id").value;
		var glosaId = document.getElementById("post_idGlo").innerHTML;

            $.ajax({
                data: {'glosaId':glosaId, 'sedesClinica_id':sedesClinica_id,  'observaciones':observaciones,'factura_id':factura_id, 'totalGlosa':totalGlosa,  'usuarioRegistro_id':usuarioRegistro_id ,'factura_id':factura_id},
	        url: "/guardaGlosasAdicionar/",
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
		data['glosaId'] = glosaId;
		var facturaId = document.getElementById("facturaAdicionar_id").value;
		data['facturaId'] = document.getElementById("facturaAdicionar_id").value;

	        data = JSON.stringify(data);
	
  		 arrancaGlosas(2,data);
			    dataTableGlosasDetalleInitialized = true;

		            $('#crearModelGlosasAdicionar').modal('hide');


		document.getElementById("mensajes").value = data2.Mensajes;

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalGlosasAdicionar").value =   data.responseText;
                }
            });


}

 $('#tablaNotasCredito tbody').on('click', '.miNotaCredito', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila

	alert("selecciono Nota # " + post_id );

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
	var sedesClinica_id = sede;
	data['sedesClinica_id'] = sede
        var notaCredito = post_id;
	data['notaCredito'] = notaCredito
	        data = JSON.stringify(data);


	document.getElementById("notaCreditoId").value = notaCredito ;

        	arrancaGlosas(13,data);
	    dataTableNotasCreditoDetalleInitialized = true;


  });


 $('#tablaNotasCreditoDetalle tbody').on('click', '.miNotaCreditoDetalle', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila

	alert("selecciono Nota Detalle # " + post_id );

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
	var sedesClinica_id = sede;
	data['sedesClinica_id'] = sede
        var notaCreditoDetalle = post_id;
	data['notaCreditoDetalle'] = notaCreditoDetalle
	data = JSON.stringify(data);

	// document.getElementById("notaCreditoId").value = notaCredito ;
	document.getElementById("notaCreditoDetalleId").value = post_id;

        	arrancaGlosas(14,data);
	    dataTableNotasCreditoDetalleRipsInitialized = true;


  });

 $('#tablaNotasCreditoDetalleRips tbody').on('click', '.miNotaCreditoDetalleRips', function() {

       var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	alert("Entre NC detalleRips = " + post_id);


	var table = $('#tablaNotasCreditoDetalleRips').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
        console.log("dato3 de tablaNotasCreditoDetalleRips = ", dato3);
	alert("tipo = " + dato3.tipo);
	alert("detCreId = " + dato3.detCreId);



     $.ajax({
		   data: {'tipo':dato3.tipo, 'id':dato3.id, 'detCreId':dato3.detCreId, 'itemFactura':dato3.itemFactura},
	        url: "/consultaNotasCreditoDetalleRips/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

	$('#postFormNotasCreditoDetalleRips').trigger("reset");

	alert("info[0] = " + JSON.stringify(info[0]) );


  	//$('#post_idGloDet').val(info[0].fields.id);
	document.getElementById("tipoNotasCreditoDetalleRips").innerHTML = info[0].fields.tipo; 
	document.getElementById("itemFacturaNotasCreditoDetalleRips").innerHTML = info[0].fields.itemFactura;
  	document.getElementById("codigoNotasCreditoDetalleRips").innerHTML = info[0].fields.codigo;
	document.getElementById("nombreNotasCreditoDetalleRips").innerHTML = info[0].fields.nombre;
	document.getElementById("vrServicioNotasCreditoDetalleRips").innerHTML = info[0].fields.vrServicio;
	document.getElementById("post_idNotasCreditoDetalle").value = info[0].fields.detCreId;

  	$('#valorNotaNotasCreditoDetalleRips').val(info[0].fields.valorNota);
  	$('#post_idRipsId').val(info[0].fields.id);

		 $('#crearModelNotasCreditoDetalleRips').modal('show');
                },
              error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
                }
            });



  });


function GuardarNotasCreditoDetalleRips()
{

		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var username_id = document.getElementById("username_id").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	    	var post_id = document.getElementById("post_idRipsId").value;
		var notasCreditoDetalle = document.getElementById("post_idNotasCreditoDetalle").value;
		var itemFactura = document.getElementById("itemFacturaNotasCreditoDetalleRips").innerHTML;
		var vrServicio = document.getElementById("vrServicioNotasCreditoDetalleRips").innerHTML;
		var valorNota = document.getElementById("valorNotaNotasCreditoDetalleRips").value;
		var tipo = document.getElementById("tipoNotasCreditoDetalleRips").innerHTML;

		

		var notasCreditoDetalle = document.getElementById("notaCreditoDetalleId").value;
		alert("notasCreditoDetalle = " +  notasCreditoDetalle);


            $.ajax({
                data: {'post_id':post_id, 'notasCreditoDetalle':notasCreditoDetalle,'itemFactura':itemFactura, 'vrServicio':vrServicio, 'valorNota':valorNota,'tipo':tipo ,'username_id':username_id},
	        url: "/guardarNotasCreditoDetalleRips/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {


			if (data2.success == false )
				{
		
				document.getElementById("mensajesErrorNotasCreditoDetalleRips").value = data2.Mensajes

					return ;
				}
	
				if (data2.success  == true )
				{


				 $('#postFormGlosasDetalle').trigger("reset");




		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

		var facturaId = dato3.factura_id;  // jquery
		data['notaCreditoDetalle'] = notasCreditoDetalle;

	        data = JSON.stringify(data);
			 arrancaGlosas(14,data);
			    dataTableNotasCreditoDetalleRipsInitialized = true;

 		 $('#crearModelNotasCreditoDetalleRips').modal('hide');
		document.getElementById("mensajes").value = data2.Mensajes

				}	// Cierra el if		

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorNotasCreditoDetalleRips").value =   data.responseText;
                }
            });


}
