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
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
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
  autoWidth: false,
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
		    search: "<i class='fa fa-search'></i> Buscar: _INPUT_",
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

       ],
	  initComplete: function(settings, json) {

		var primeraFila = $('#tablaGlosas tbody tr:eq(0) input[type="radio"]').prop('checked', true);
             $(primeraFila).click();
                 primeraFila.addClass('selected');
        }
            }
	        dataTable = $('#tablaGlosas').DataTable(dataTableOptionsGlosas);
  }

    if (valorTabla == 2)
    {
        let dataTableOptionsGlosasDetalle  ={
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
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
  autoWidth: false,
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
		    search: "<i class='fa fa-search'></i> Buscar: _INPUT_",
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


                     ],
	  initComplete: function(settings, json) {

		var primeraFila = $('#tablaGlosasDetalle tbody tr:eq(0) input[type="radio"]').prop('checked', true);
             $(primeraFila).click();
                 primeraFila.addClass('selected');
        }
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
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
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
  autoWidth: false,
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
		    search: "<i class='fa fa-search'></i> Buscar: _INPUT_",
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


    if (valorTabla==12)
    {
        alert ("Entre tabla 12");

        let dataTableOptionsNotasCredito  = {
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
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
  autoWidth: false,
  lengthMenu: [2, 4],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1] },
	    { width: '10%', targets: [2,3] },

		{   
                    "targets": 10
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
		    search: "<i class='fa fa-search'></i> Buscar: _INPUT_",
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
                 url:"/load_dataNotas/" + data,
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
{
		"render": function ( data, type, row ) {
                        var btn = '';
		 btn = btn + " <button class='estadoRecepcion btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: red;'  data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
		},
    	     {
		"render": function ( data, type, row ) {
                        var btn = '';
		 btn = btn + " <button class='estadoRadicacion btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: red;'  data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
		},
                { data: "fields.id"},
                { data: "fields.fechaNota"},
                { data: "fields.valorNotaTotal"},
                { data: "fields.observaciones"},
                { data: "fields.fechaRegistro"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.estadoReg"},
                { data: "fields.fechaRespuesta"},
                { data: "fields.tiposNota"},
                { data: "fields.ripsEnvioId"},
{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='miEditaNotaCredito'  style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miEditaNotaCredito form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},
       ],
	  initComplete: function(settings, json) {

		var primeraFila = $('#tablaNotas tbody tr:eq(0) input[type="radio"]').prop('checked', true);
             $(primeraFila).click();
                 primeraFila.addClass('selected');
        }
            }
	        dataTable = $('#tablaNotas').DataTable(dataTableOptionsNotasCredito);
  }

    if (valorTabla == 13)
    {
	alert("Entre tabla 13");

        let dataTableOptionsNotasCreditoDetalle  ={
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
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
		    search: "<i class='fa fa-search'></i> Buscar: _INPUT_",
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
		{ data: "fields.notaCreditoId"},
                { data: "fields.factura_id"},
                { data: "fields.valorNotaTotal"},
                { data: "fields.fechaRegistro"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.totalFactura"},
                { data: "fields.valorApagar"},
                { data: "fields.totalNotasCredito"},
                { data: "fields.totalOtrasNotasCredito"},
                { data: "fields.saldoFactura"},
       ],
	  initComplete: function(settings, json) {

		var primeraFila = $('#tablaNotasCreditoDetalle tbody tr:eq(0) input[type="radio"]').prop('checked', true);
             $(primeraFila).click();
                 primeraFila.addClass('selected');
        }
            }
	        dataTable = $('#tablaNotasCreditoDetalle').DataTable(dataTableOptionsNotasCreditoDetalle);
  }


    if (valorTabla == 14)
    {
        let dataTableOptionsNotasCreditoDetalleRips  ={
  dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
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
		    search: "<i class='fa fa-search'></i> Buscar: _INPUT_",
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

	 alert("a cargar NC");
         arrancaGlosas(12,data);
	 dataTableNotasCreditoInitialized = true;
	 alert("ya cargue NC");

         arrancaGlosas(1,data);
	 dataTableGlosasInitialized = true;

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

	   // arrancaGlosas(1,data);
	   // dataTableGlosasTransaccionInitialized = true;

	        arrancaGlosas(2,data);
	    dataTableGlosasDetalleInitialized = true;

	     //   arrancaGlosas(3,data);
	    // dataTableGlosasDetalleRipsInitialized = true;

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



$('#tablaNotas tbody').on('click', '.miNotaCredito', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	alert("Entre mi notaCredito");

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

	var table = $('#tablaNotas').DataTable();  // Inicializa el DataTable jquery 	      

  	        var rowindex = table.row(row).data(); // Obtiene los datos de la fila


	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato10 notaCredito_id = " , dato3.id); 

		data['notaCreditoId'] = dato3.id;

	        data = JSON.stringify(data);
		alert("a cargar notas credito detalle");

	        arrancaGlosas(13,data);
	        dataTableNotaCreditoDetalleInitialized = true;

		alert("LISTO notas credito detalle");

	        arrancaGlosas(14,data);
    	        dataTableNotaCreditoDetalleRipsInitialized = true;

	// AQUI tengo que colocar los datosde la Nota Credito en el Formulario de General y demas

	  document.getElementById("postNotasCredito_id").innerHTML =dato3.id;
	  document.getElementById("estadoRadicacionNotasCredito").innerHTML =dato3.estadoRadicacion;
	  document.getElementById("estadoRecepcionNotasCredito").innerHTML = dato3.estadoRecepcion;
	  document.getElementById("tiposNotasCredito").innerHTML = dato3.tiposNota;



  });




 $('#tablaGlosasDetalle tbody').on('click', '.miGlosaDetalle', function() {

	alert("Entre glosas detalle ");

        var data =  {}   ;
       
	var table = $('#tablaGlosasDetalle').DataTable();  // Inicializa el DataTable jquery
var row = $(this).closest('tr'); // Encuentra la fila
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila

	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
    console.log("dato3 de glosasdetalleRips = ", dato3);
    var post_id = dato3.id
      document.getElementById("post_idGloDet").innerHTML =  post_id;
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
	post_id = document.getElementById("post_idGlo").innerHTML;
	post_idGloDet = document.getElementById("post_idGloDet").innerHTML;
	data['glosaId'] = post_id;
	data['gloDetId'] = post_idGloDet;
        data = JSON.stringify(data);

        arrancaGlosas(3,data);
        dataTableGlosasDetalleRipsInitialized = true;

  });


 $('#tablaGlosasDetalleRips tbody').on('click', '.miGlosasDetalleRips', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	alert("Entre glosas detalle RIPS");

	var table = $('#tablaGlosasDetalleRips').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
        console.log("dato3 de glosasdetalleRips = ", dato3);
         

     $.ajax({
		   data: {'tipo':dato3.tipo, 'id':dato3.id,'detGloId':dato3.detGloId},
	        url: "/consultaGlosasDetalleRips/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

	$('#postFormGlosasDetalleRips').trigger("reset");

	alert("info[0] = " + JSON.stringify(info[0]) );


  	$('#post_idGloDet').val(info[0].fields.id);
	document.getElementById("tipoGloDetRips").innerHTML = info[0].fields.tipo; 
	document.getElementById("glosaGloDetRips").innerHTML = document.getElementById("post_idGloDet").value;
	document.getElementById("itemFacturaGloDetRips").innerHTML = info[0].fields.itemFactura;
  	document.getElementById("codigoGloDetRips").innerHTML = info[0].fields.codigo;
	document.getElementById("nombreGloDetRips").innerHTML = info[0].fields.nombre;
	document.getElementById("vrServicioGloDetRips").innerHTML = info[0].fields.vrServicio;
  	$('#consecutivoGloDetRips').val(info[0].fields.consecutivo);
  	$('#valorGlosadoGloDetRips').val(info[0].fields.valorGlosa);
  	$('#vAceptadoGloDetRips').val(info[0].fields.valorAceptado);
  	$('#valorSoportadoGloDetRips').val(info[0].fields.valorSoportado);
  	$('#motivoGlosa_idGloDetRips').val(info[0].fields.motivoGlosa_id);
  	$('#notasCreditoGlosaGloDetRips').val(info[0].fields.valorNotasCredito);
  	$('#observacionesGloDetRips').val(info[0].fields.observaciones);

		if (info.success == false )
				{
		
				document.getElementById("mensajesErrorGlosasDetalleModalRips").value = info.Mensajes;
				document.getElementById("mensajesGlosasDetalleModalRips").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajesErrorGlosasDetalleModalRips").value = '';
				document.getElementById("mensajesGlosasDetalleModalRips").value = info.Mensajes;

				}


		 $('#crearModelGlosasDetalleRips').modal('show');
                },
              error: function (data) {	      
			document.getElementById("mensajesErrorGlosasDetalleModalRips").value =   data.responseText;
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


				if (info.success == false )
				{
		
				document.getElementById("mensajesError").value = info.Mensajes;
				document.getElementById("mensajes").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajes").value = info.Mensajes;
				document.getElementById("mensajesError").value = '';

				}


                },
              error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
                }
            });

  });



$('#tablaGlosasDetalleRips tbody').on('click', '.miBorrarGlosasDetalleRips', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	alert("entre a borrar miBorrarGlosaDetalleRips" + post_id);



	var table = $('#tablaGlosasDetalleRips').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	dato1 = Object.values(rowindex);
	dato3 = dato1[2];
        console.log("dato3 de glosasdetalle = ", dato3);
	var detGloRipsId = dato3.gloDetRips;
	alert("detGloRipsId = " + detGloRipsId);
	var detGloId = dato3.detGloId;
        alert("detGloId = " + detGloId);
	var glosaId = dato3.glosaId;
         alert("glosaId = " + glosaId);

	var ripsId = dato3.id;
        alert("ripsId = " + ripsId);

     $.ajax({
		   data: {'detGloRipsId':detGloRipsId, 'detGloId':detGloId,'glosaId':glosaId, 'ripsId':ripsId},
	        url: "/borraGlosasDetalleRips/",
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
	data['gloDetId'] = detGloId;
        data = JSON.stringify(data);

	        arrancaGlosas(1,data);
	    dataTableGlosasInitialized = true;

	        arrancaGlosas(2,data);
	    dataTableGlosasDetalleInitialized = true;
	    arrancaGlosas(3,data);
	    dataTableGlosasDetalleRipsInitialized  = true;

				if (info.success == false )
				{
		
				document.getElementById("mensajesError").value = info.Mensajes;
				document.getElementById("mensajes").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajes").value = info.Mensajes;
				document.getElementById("mensajesError").value = '';

				}

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
        var notasCreditoDetalleId = dato3.detCreId;
        var notasCreditoRipsDetalleId = dato3.detCreRipsId;

	var valorNota = dato3.valorNota;
	if (valorNota==null)
		{
		alert("Nulo");
		valorNota=0
		}

     $.ajax({
		   data: {'ripsId':ripsId, 'notasCreditoDetalleId':notasCreditoDetalleId,'notasCreditoRipsDetalleId':notasCreditoRipsDetalleId,  'valorNota':valorNota},
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


	data['notaCreditoDetalle'] = notasCreditoDetalleId

        data = JSON.stringify(data);


	    arrancaGlosas(14,data);
	    dataTableNotasCreditoDetalleRipsInitialized  = true;


				if (info.success == false )
				{
		
				document.getElementById("mensajesError").value = info.Mensajes;
				document.getElementById("mensajes").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajes").value = info.Mensajes;
				document.getElementById("mensajesError").value = '';

				}


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
		
				document.getElementById("mensajesErrorDetalleModal").value = data2.Mensajes;
				document.getElementById("mensajesDetalleModal").value = '';

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


function GuardarGlosasDetalleRips()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var username_id = document.getElementById("username_id").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
		
		var post_idGloDet = document.getElementById("post_idGloDet").innerHTML;
		var post_idGlo = document.getElementById("post_idGlo").innerHTML;

	    	var post_idGloDetRips = document.getElementById("post_idGloDetRips").innerHTML;
	    	var tipoGloDetRips = document.getElementById("tipoGloDetRips").innerHTML;
	        var glosaGloDetRips = document.getElementById("glosaGloDetRips").innerHTML;
	        var motivoGlosa_idGloDetRips = document.getElementById("motivoGlosa_idGloDetRips").value;
	        var valorGlosadoGloDetRips = document.getElementById("valorGlosadoGloDetRips").value;
		var itemFacturaGloDetRips = document.getElementById("itemFacturaGloDetRips").innerHTML;

	        var observacionesGloDetRips = document.getElementById("observacionesGloDetRips").value;
	        var vAceptadoGloDetRips = document.getElementById("vAceptadoGloDetRips").value;
	        var valorSoportadoGloDetRips = document.getElementById("valorSoportadoGloDetRips").value;
	        var notasCreditoGlosaGloDetRips = document.getElementById("notasCreditoGlosaGloDetRips").value;
	        var vrServicioGloDetRips = document.getElementById("vrServicioGloDetRips").innerHTML;


            $.ajax({
                data: {'post_idGloDet':post_idGloDet, 'post_idGloDetRips':post_idGloDetRips, 'tipoGloDetRips':tipoGloDetRips,'glosaGloDetRips':glosaGloDetRips, 'motivoGlosa_idGloDetRips':motivoGlosa_idGloDetRips, 'valorGlosadoGloDetRips':valorGlosadoGloDetRips,'vAceptadoGloDetRips':vAceptadoGloDetRips,  'valorSoportadoGloDetRips':valorSoportadoGloDetRips, 'notasCreditoGlosaGloDetRips':notasCreditoGlosaGloDetRips,   'vrServicioGloDetRips':vrServicioGloDetRips,'username_id':username_id ,'itemFacturaGloDetRips':itemFacturaGloDetRips,'observacionesGloDetRips':observacionesGloDetRips },
	        url: "/guardarGlosasDetalleRips/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

				alert("regrese con = " + JSON.stringify(data2));

			if (data2.success == false )
				{ 
			alert ("Entre false");
		
				document.getElementById("mensajesErrorGlosasDetalleModalRips").value = data2.Mensajes;
				document.getElementById("mensajesGlosasDetalleModalRips").value = '';

					return ;
				}
	
				if (data2.success  == true )
				{


				 $('#postFormGlosasDetalle').trigger("reset");


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
		var facturaId =	document.getElementById("factura_idGlo").innerHTML;


		data['glosaId'] = post_idGlo;
		data['facturaId'] = facturaId;
		data['gloDetId'] = post_idGloDet;

		alert("voya a cargat con glosaId + " +  post_idGlo);
		alert("voya a cargat con facturaId + " +  facturaId);



	        data = JSON.stringify(data);

			 arrancaGlosas(2,data);
			    dataTableGlosasDetalleInitialized = true;

			 arrancaGlosas(3,data);
			    dataTableGlosasDetalleRipsInitialized = true;


 		 $('#crearModelGlosasDetalleRips').modal('hide');


				}	// Cierra el if		

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorGlosasDetalleModalRips").value =   data.responseText;
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

				if (data2.success == false )
				{
		
				document.getElementById("mensajesError").value = data2.Mensajes;
				document.getElementById("mensajes").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajes").value = data2.Mensajes;
				document.getElementById("mensajesError").value = '';

				}




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
    
	
	    var nada='';
            $('#post_id').val('');
            $('#postFormCrearNotasCredito').trigger("reset");
            $('#modelHeadingMotasCredito').html("Creacion NotasCredito");
            $.ajax({
                data: {'nada':nada},
	        url: "/traerCodigoTipoNota/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
			alert("esto trae" + JSON.stringify(data2));
		
		document.getElementById("tipoNotasCredito_id").value =   data2[0]['fields'].id;
	
                },
              error: function (data) {	      
			document.getElementById("mensajesError").value =   data.responseText;
                }
            });



            $('#crearModelNotasCredito').modal('show');
        
}



function GlosasAdicionar()
{
    
            $('#post_id').val('');
            $('#postFormGlosasAdicionar').trigger("reset");
            $('#modelHeadingGlosas').html("Creacion Glosas  Factura");
		alert("voy a abrir");
            $('#crearModelGlosasAdicionar').modal('show');
		alert("ya abri");
        
}

function NotasCreditoDetalleAdicionar()
{
    
            $('#post_id').val('');
            $('#postFormNotasCreditoDetalleAdicionar').trigger("reset");
            $('#modelHeadingGlosas').html("Creacion Notas Credito  Factura");
		alert("voy a abrir");
            $('#crearNotasCreditoDetalleAdicionar').modal('show');
		alert("ya abri");
        
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
     
	
	        var sedesClinica_id = document.getElementById("sedesClinica_id").value;
	        var fechaRecepcion = document.getElementById("fechaRecepcion").value;
	        var observaciones = document.getElementById("observaciones").value;
	        var fechaRespuesta = document.getElementById("fechaRespuesta").value;
	        var tipoGlosa_id = document.getElementById("tipoGlosa_id").value;
	        var totalGlosa = document.getElementById("totalGlosa").value;
	        var estadoRecepcion_id = document.getElementById("estadoRecepcion_id").value;
	        var usuarioRegistro_id = document.getElementById("usuarioRegistro_id").value;
	        var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativos_id").value;

            $.ajax({
                data: {'serviciosAdministrativos_id':serviciosAdministrativos_id, 'sedesClinica_id':sedesClinica_id, 'fechaRecepcion':fechaRecepcion, 'observaciones':observaciones, 'fechaRespuesta':fechaRespuesta, 'tipoGlosa_id':tipoGlosa_id, 'totalGlosa':totalGlosa, 'estadoRecepcion_id':estadoRecepcion_id, 'usuarioRegistro_id':usuarioRegistro_id },
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

	        data = JSON.stringify(data);
  	
			 arrancaGlosas(1,data);
			    dataTableGlosasInitialized = true;

		            $('#crearModelGlosas').modal('hide');

				if (data2.success == false )
				{
		
				document.getElementById("mensajesError").value = data2.Mensajes;
				document.getElementById("mensajes").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajes").value = data2.Mensajes;
				document.getElementById("mensajesError").value = '';

				}

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalGlosas").value =   data.responseText;
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


				if (data2.success == false )
				{
		
				document.getElementById("mensajesError").value = data2.Mensajes;
				document.getElementById("mensajes").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajes").value = data2.Mensajes;
				document.getElementById("mensajesError").value = '';

				}


                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalGlosasAdicionar").value =   data.responseText;
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
		alert("Entre GuardarNotas Credito");
     
	
	        var sedesClinica_id = document.getElementById("sedesClinica_id").value;
	        var fechaRecepcion = document.getElementById("fechaRecepcionNotasCredito").value;
	        var observaciones = document.getElementById("observacionesNotasCredito").value;
	        var fechaRespuesta = document.getElementById("fechaRespuestaNotasCredito").value;
	        var tipoNotasCredito = document.getElementById("tipoNotasCredito_id").value;
	        var totalNotasCredito = document.getElementById("totalNotasCredito").value;
	        var estadoRecepcionNotasCredito_id = document.getElementById("estadoRecepcionNotasCredito_id").value;
	        var usuarioRegistro_id = document.getElementById("usuarioRegistro_id").value;
	        var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativosNotasCredito_id").value;

            $.ajax({
                data: {'serviciosAdministrativos_id':serviciosAdministrativos_id, 'sedesClinica_id':sedesClinica_id, 'fechaRecepcion':fechaRecepcion, 'observaciones':observaciones, 'fechaRespuesta':fechaRespuesta, 'tipoNotasCredito':tipoNotasCredito, 'totalNotasCredito':totalNotasCredito, 'estadoRecepcionNotasCredito_id':estadoRecepcionNotasCredito_id, 'usuarioRegistro_id':usuarioRegistro_id },
	        url: "/guardaNotasCredito/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

				if (data2.success == false )
				{
		
				document.getElementById("mensajesErrorModalNotasCredito").value = data2.Mensajes;
				document.getElementById("mensajesModalNotasCredito").value = '';
					return ;
				}
				else
				{
				document.getElementById("mensajes").value = data2.Mensajes;
				document.getElementById("mensajesError").value = '';

				}

                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalNotasCredito").value =   data.responseText;
                }
            });

		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

	        data = JSON.stringify(data);
  	
			 arrancaGlosas(12,data);
			    dataTableNotasCreditoInitialized = true;

		            $('#crearModelNotasCredito').modal('hide');
}



function CrearNotasCreditoDetalleAdicionar()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;
		alert("Entre Guardar CrearDetalleNotasCreditoAdicionar");      

	        var sedesClinica_id = document.getElementById("sedesClinica_id").value;
	        var observaciones = document.getElementById("observacionesNotasCreditoDetalleAdicionar").value;
	        var factura_id = document.getElementById("facturaNotasCreditoDetalleAdicionar_id").value;
	        var totalNotasCreditoDetalleAdicionar = document.getElementById("totalNotasCreditoDetalleAdicionar").value;
	        var usuarioRegistro_id = document.getElementById("usuarioRegistroNotasCreditoDetalleAdicionar_id").value;
		var notaCreditoId = document.getElementById("postNotasCredito_id").innerHTML;

            $.ajax({
                data: {'notaCreditoId':notaCreditoId, 'sedesClinica_id':sedesClinica_id,  'observaciones':observaciones,'factura_id':factura_id, 'totalNotasCreditoDetalleAdicionar':totalNotasCreditoDetalleAdicionar,  'usuarioRegistro_id':usuarioRegistro_id },
	        url: "/guardaNotasCreditoDetalleAdicionar/",
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
		data['notaCreditoId'] = notaCreditoId;
		var facturaId = document.getElementById("facturaAdicionar_id").value;
		data['facturaId'] = factura_id;

	        data = JSON.stringify(data);
	
  		 	arrancaGlosas(13,data);
			    dataTableNotasCreditoDetalleInitialized = true;

  		 	arrancaGlosas(14,data);
			    dataTableNotasCreditoDetalleRipsInitialized = true;

				if (data2.success == false )
				{	
				document.getElementById("mensajesErrorModalDetalleNotasCreditoAdicionar").value = data2.Mensajes;
				document.getElementById("mensajesModalDetalleNotasCreditoAdicionar").value = '';
				return ;
				}
				else
				{
				document.getElementById("mensajes").value = data2.Mensajes;
				document.getElementById("mensajesError").value = '';
				}
		      $('#crearNotasCreditoDetalleAdicionar').modal('hide');
                },
              error: function (data) {	      
			document.getElementById("mensajesErrorModalDetalleNotasCreditoAdicionar").value =   data.responseText;
                }
            });
}

 $('#tablaNotasCreditoDetalle tbody').on('click', '.miNotaCreditoDetalle', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila

	alert("selecciono miNotaCreditoDetalle # " + post_id );

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

	// document.getElementById("notaCreditoDetalleId").value = post_id;

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

	alert("info[0] = " + JSON.stringify(info[0]));
        console.log("OJO Traigo esto " , JSON.stringify(info[0]));

	document.getElementById("tipoNotasCreditoDetalleRips").innerHTML = info[0].fields.tipo; 
	document.getElementById("itemFacturaNotasCreditoDetalleRips").innerHTML = info[0].fields.itemFactura;
  	document.getElementById("codigoNotasCreditoDetalleRips").innerHTML = info[0].fields.codigo;
	document.getElementById("nombreNotasCreditoDetalleRips").innerHTML = info[0].fields.nombre;
	document.getElementById("vrServicioNotasCreditoDetalleRips").innerHTML = info[0].fields.vrServicio;
	document.getElementById("NotasCreditoDetalleId").innerHTML = info[0].fields.detCreId;
	document.getElementById("post_idNotasCreditoRips").value = info[0].fields.id;

  	$('#valorNotasCreditoDetalleRips').val(info[0].fields.valorNota);

		alert("voy a mostrar la modal rips");

		 $('#crearModelNotasCreditoDetalleRips').modal('show');

		alert("YA MOSTRE r la modal rips");
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

	    	var post_id = document.getElementById("post_idNotasCreditoRips").value;
		var notasCreditoDetalle = document.getElementById("NotasCreditoDetalleId").innerHTML;
		var itemFactura = document.getElementById("itemFacturaNotasCreditoDetalleRips").innerHTML;
		var vrServicio = document.getElementById("vrServicioNotasCreditoDetalleRips").innerHTML;
		var valorNota = document.getElementById("valorNotasCreditoDetalleRips").value;
		var tipoRips = document.getElementById("tipoNotasCreditoDetalleRips").innerHTML;
		alert("envio TIPORIPS = " + tipoRips);
		alert("post_id  o RIPSID = " + post_id);

            $.ajax({
                data: {'ripsId':post_id, 'notasCreditoDetalle':notasCreditoDetalle,'itemFactura':itemFactura, 'vrServicio':vrServicio, 'valorNota':valorNota,'username_id':username_id, 'tipoRips':tipoRips},
	        url: "/guardarNotasCreditoDetalleRips/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {


			if (data2.success == false )
				{
		
				document.getElementById("mensajesErrorNotasCreditoDetalleRips").value = data2.Mensajes;
				document.getElementById("mensajesNotasCreditoDetalleRips").value = " ";
					return ;
				}
	
				if (data2.success  == true )
				{


				 $('#postFormNotasCreditoDetalleRips').trigger("reset");


		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

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
