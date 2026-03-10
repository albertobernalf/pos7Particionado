console.log('Hola Alberto Hi!')

let dataTable;
let dataTableB;
let dataTableC;
let dataTableD;
let dataTableF;
let dataTableG;
let dataTableH;
let dataTableI;

let dataTablePanelEnfermeriaInitialized = false;
let dataTableMedicamentosEnfermeriaInitialized = false;
let dataTableParaclinicosEnfermeriaEnfermeriaInitialized = false;
let dataTablePedidosEnfermeria = false;
let dataTablePedidosEnfermeriaDetalle = false;
let dataTableTurnosEnfermeria = false;
let dataTablePlaneacionEnfermeria = false;
let dataTableDietaEnfermeria = false;
let dataTableNotasEnfermeria = false;
let dataTableDevolucionEnfermeriaInitialized = false;
let dataTableConsultaDevolucionesEnfermeriaInitialized = false;
let dataTableConsultaDevolucionesDetalleEnfermeriaInitialized = false;
let dataTableSignosVitalesEnfermeriaInitialized = false;

var controlMed = 0;
var controlDev = 0;




$(document).ready(function() {

/*------------------------------------------
        --------------------------------------------
        Create Post Code Formulacion
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarFormulacionEnfermeria').click(function (e) {
            e.preventDefault();


   	   if (controlMed == 0)
   	   {
   	   var table10 = $('#tablaFormulacionEnfermeria').DataTable({scrollY: '80px', paging:false,  search:false,  scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlMed=1;
   	   }
   	   else
   	   {
	  var table10 = $('#tablaFormulacionEnfermeria').DataTable();
   	   }



           var select3 = document.getElementById("medicamentos"); /*Obtener el SELECT */
      	   var medicamentos= select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textMedicamentos = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada

           var dosis =  document.getElementById("dosis").value;

	        var select3 = document.getElementById("uMedidaDosis"); /*Obtener el SELECT */
      	   var uMedidaDosis= select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textUMedidaDosis = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada

	         var select3 = document.getElementById("uMedidaDosis"); /*Obtener el SELECT */
      	   var uMedidaDosis= select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textUMedidaDosis = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada


	         var select3 = document.getElementById("vias"); /*Obtener el SELECT */
      	   var viasAdministracion = select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   var textViasAdministracion = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada
	
	        var cantidadMedicamento =  document.getElementById("cantidadMedicamento").value;

		

	    table10.row.add([ medicamentos, textMedicamentos, dosis,  textUMedidaDosis, textViasAdministracion, cantidadMedicamento   ,  '<i class="fa fa-trash"></i>']).draw(false);

        });



/*------------------------------------------
        --------------------------------------------
        Create Post Code Formulacion Devolucines
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnFormulacionDev').click(function (e) {
            e.preventDefault();

		// alert("entre devolver medicamentos");

   	   if (controlDev == 0)
   	   {
   	   var table11 = $('#tablaFormulacionDevolucion').DataTable({scrollY: '180px', paging:false,  search:false,  scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlMed=1;
   	   }
   	   else
   	   {
	  var table11 = $('#tablaFormulacionDevolucion').DataTable();
   	   }

  	   var enfermeriaRecibeId =  document.getElementById("recibeDevId").value;
	   var textMedicamentos =    document.getElementById("suministroDev").value;
	   var dosis =  document.getElementById("dosisDev").value;
	   var textUMedidaDosis =  document.getElementById("medidaDev").value;
	   var textViasAdministracion =  document.getElementById("viaDev").value;
	   var cantidadMedicamento =  document.getElementById("cantidadDev").value;
	   var observaciones =  document.getElementById("observacionesDev").value;
	

	    table11.row.add([ enfermeriaRecibeId, textMedicamentos, dosis,  textUMedidaDosis, textViasAdministracion, cantidadMedicamento, observaciones,    '<i class="fa fa-trash"></i>']).draw(false);

		 $('#postFormModalDevolverEnfermeria').trigger("reset");
		 $('#ModalDevolverEnfermeria').modal('hide');  


        });

	

// aqui van los filtros de busqueda

});


function arrancaEnfermeria(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsPanelEnfermeria  ={

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
            scrollY: '475px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 14
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
                 url:"/load_dataPanelEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

              btn = btn + " <input type='radio'  name='ingresoEnfermeriaId' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miIngresoEnfermeriaId form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

              /*   { data: "fields.id"}, */
		{
			target: 0,
			visible: true
		},

                 { data: "fields.tipoDoc" }, 
                { data: "fields.Documento"},
                { data: "fields.Nombre"},
                { data: "fields.Consec"},
                { data: "fields.edad"},
                { data: "fields.Empresa"},
                { data: "fields.FechaIngreso"},
                { data: "fields.servicioNombreIng"},
                { data: "fields.camaNombreIng"},
               { data: "fields.salidaClinica"},
		     { data: "fields.DxActual"}, 
                { data: "fields.numConvenios"},
		        { data: "fields.numPagos"},

                        ]
            }
	        
		   dataTable = $('#tablaPanelEnfermeria').DataTable(dataTableOptionsPanelEnfermeria);


  }


    if (valorTabla == 2)
    {
        let dataTableOptionsMedicamentosEnfermeria  ={
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
            scrollY: '250px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
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
                 url:"/load_dataMedicamentosEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

              btn = btn + " <input type='radio'  name='medicamentosId' class='miMedicamentosId form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },

	},
	{
	  "render": function ( data, type, row ) {
                        var btn = '';
     btn = btn + " <button class='Planear btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";
                       return btn;
                    },

	},
           
                 { data: "fields.id"},
		{
			target: 2,
			visible: false
		},
		{
			target: 3,
			visible: false
		},
		{
			target: 4,
			visible: false
		},

		{ data: "fields.despacho"},
                { data: "fields.folio"}, 
                { data: "fields.consecutivoMedicamento"},
                { data: "fields.dosis"},
                { data: "fields.cantidad"},
                { data: "fields.UnidadMedida"},
                { data: "fields.medicamento"},
                { data: "fields.via"},
                { data: "fields.frecuencia"},
                { data: "fields.diasTratamiento"},


                        ]
            }
	        
		   dataTable = $('#tablaMedicamentosEnfermeria').DataTable(dataTableOptionsMedicamentosEnfermeria);


  }


    if (valorTabla == 3)
    {
        let dataTableOptionsParaClinicosEnfermeria  ={
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
            scrollY: '475px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
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
                 url:"/load_dataParaClinicosEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

              btn = btn + " <input type='radio'  name='paraclinicoId' class='paraclinicoId form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                 { data: "fields.id"},
                 { data: "fields.medico" }, 
                { data: "fields.fecha"},
                { data: "fields.folio"},
                { data: "fields.tipo"},
                { data: "fields.consecutivo"},
                { data: "fields.cups"},
                { data: "fields.examen"},
                { data: "fields.cantidad"},


                        ]
            }
	        
		   dataTable = $('#tablaParaClinicosEnfermeria').DataTable(dataTableOptionsParaClinicosEnfermeria);


  }

    if (valorTabla == 4)
    {
        let dataTableOptionsPedidosEnfermeria  ={
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
            scrollY: '75px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
	    "info": false,
		"showNEntries" : false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2,] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 4
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
                 url:"/load_dataPedidosEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miPedidosEnfermeria' class='miPedidosEnfermeria form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },

	},

                { data: "fields.id"},
                { data: "fields.origen"},
		   { data: "fields.mov"}, 
                { data: "fields.servicio"},


                        ]
            }
	        
		   dataTable = $('#tablaPedidosEnfermeria').DataTable(dataTableOptionsPedidosEnfermeria);


  }



    if (valorTabla == 5)
    {
        let dataTableOptionsPedidosEnfermeriaDetalle  ={
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '75px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
	    "info": false,
		"showNEntries" : false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
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
                 url:"/load_dataPedidosEnfermeriaDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miPedidosEnfermeriaDetalle' class='miPedidosEnfermeriaDetale form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
        		{ data: "fields.dosis"},
                { data: "fields.unidadDosis"},
                { data: "fields.suministro"},
                { data: "fields.viaAdministracion"},
                { data: "fields.cantidad"},

                        ]
            }
	        
		   dataTable = $('#tablaPedidosEnfermeriaDetalle').DataTable(dataTableOptionsPedidosEnfermeriaDetalle);


  }



    if (valorTabla == 6)
    {
        let dataTableOptionsTurnosEnfermeria  ={
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
            scrollY: '425px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
	    "info": false,
		"showNEntries" : false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 4
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
                 url:"/load_dataTurnosEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miTurnosEnfermeria' class='miTurnoEnfermeria form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
        		{ data: "fields.servicio"},
                { data: "fields.tipoNombre"},
                { data: "fields.plantaNombre"},
                { data: "fields.horario"},


                        ]
            }
	        
		   dataTable = $('#tablaTurnosEnfermeria').DataTable(dataTableOptionsTurnosEnfermeria);


  }


    if (valorTabla == 7)
    {
        let dataTableOptionsPlaneacionEnfermeria  ={
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
            scrollY: '425px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
	    "info": false,
		"showNEntries" : false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 15
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
                 url:"/load_dataPlaneacionEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miAplicacionEnfermeria' class='miAplicacionEnfermeria form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
        		{ data: "fields.fechaPlanea"},
                { data: "fields.turnoPlanea"},
                { data: "fields.enfermeraPlanea"},
                { data: "fields.cantidadPlaneada"},
                { data: "fields.fechaAplica"},
                { data: "fields.turnoAplica"},
                { data: "fields.enfermeraAplica"},
                { data: "fields.cantidadAplicada"},
                { data: "fields.dosis"},
                { data: "fields.medida"},
                { data: "fields.suministro"},
                { data: "fields.via"},
                { data: "fields.frecuencia"},
                { data: "fields.dias"},

                        ]
            }
	        
		   dataTable = $('#tablaPlaneacionEnfermeria').DataTable(dataTableOptionsPlaneacionEnfermeria);


  }



    if (valorTabla == 8)
    {
        let dataTableOptionsDietasEnfermeria  ={
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
            scrollY: '425px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
	    "info": false,
		"showNEntries" : false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 5
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
                 url:"/load_dataDietasEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miDietaEnfermeria' class='miDietaEnfermeria form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
        		{ data: "fields.consecutivo"},
        		{ data: "fields.folio"},
                { data: "fields.nombreTipoDieta"},
                { data: "fields.observaciones"},
                { data: "fields.profesional"},

                        ]
            }
	        
		   dataTable = $('#tablaDietasEnfermeria').DataTable(dataTableOptionsDietasEnfermeria);


  }


    if (valorTabla == 9)
    {
        let dataTableOptionsNotasEnfermeria  ={
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
            scrollY: '425px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
	    "info": false,
		"showNEntries" : false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, ] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 3
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
                 url:"/load_dataNotasEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miNotaEnfermeria' class='miNotaEnfermeria form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
                { data: "fields.folio"},
                { data: "fields.observaciones"},
                { data: "fields.profesional"},

                        ]
            }
	        
		   dataTable = $('#tablaNotasEnfermeria').DataTable(dataTableOptionsNotasEnfermeria);


  }


    if (valorTabla == 10)
    {
        let dataTableOptionsDevolucionEnfermeria  ={
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
            scrollY: '120px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 13
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
                 url:"/load_dataDevolucionEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';
     btn = btn + " <button class='Devolver btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";
                       return btn;
                    },

	},
           
                 { data: "fields.id"},
		{
			target: 2,
			visible: false
		},
		{
			target: 3,
			visible: false
		},
		{
			target: 4,
			visible: false
		},

                { data: "fields.folio"},
  
                { data: "fields.consecutivoMedicamento"},
                { data: "fields.dosis"},
                { data: "fields.cantidad"},
                { data: "fields.cantidadDevuelta"},
                { data: "fields.UnidadMedida"},
                { data: "fields.medicamento"},
                { data: "fields.via"},
                { data: "fields.frecuencia"},
                { data: "fields.diasTratamiento"},
                        ]
            }
	        
		   dataTable = $('#tablaDevolucionEnfermeria').DataTable(dataTableOptionsDevolucionEnfermeria);


  }



    if (valorTabla == 11)
    {
        let dataTableOptionsConsultaDevolucionesEnfermeria  ={
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
            scrollY: '120px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 5
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
                 url:"/load_dataConsultaDevolucionesEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';
	  btn = btn + " <input type='radio' name='miConsultaDev'  class='miConsultaDev form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},
           
                { data: "fields.id"},
                { data: "fields.fechaRegistro"},
                { data: "fields.servicioDevuelve"},
                { data: "fields.usuarioDevuelve"},
                { data: "fields.servicioRecibe"},
                { data: "fields.usuarioRecibe"},

                        ]
            }
	        
		   dataTable = $('#tablaConsultaDevolucionesEnfermeria').DataTable(dataTableOptionsConsultaDevolucionesEnfermeria);


  }


    if (valorTabla == 12)
    {
        let dataTableOptionsConsultaDevolucionesDetalleEnfermeria  ={
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
            scrollY: '120px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
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
                 url:"/load_dataConsultaDevolucionesDetalleEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		 { data: "fields.id"},
                { data: "fields.medicamento"},
                { data: "fields.dosis"},
                { data: "fields.unidadMedida"},
                { data: "fields.via"},
                { data: "fields.cantidad"},
                { data: "fields.cantidadDevuelta"},
                { data: "fields.observaciones"},
                        ]
            }
	        
		   dataTable = $('#tablaConsultaDevolucionesDetalleEnfermeria').DataTable(dataTableOptionsConsultaDevolucionesDetalleEnfermeria);

  }


    if (valorTabla == 13)
    {
        let dataTableOptionsSignosVitalesEnfermeria  ={
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
            scrollY: '475px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 18
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
                 url:"/load_dataSignosVitalesEnfermeria/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		 { data: "fields.id"},
                { data: "fields.fecha"},
                { data: "fields.folio"},
                { data: "fields.frecCardiaca"},
                { data: "fields.frecRespiratoria"},
                { data: "fields.tensionADiastolica"},
                { data: "fields.tensionSistolica"},
                { data: "fields.tensionAMedia"},
                { data: "fields.temperatura"},
                { data: "fields.saturacion"},
                { data: "fields.tensionAMedia"},
                { data: "fields.glasgow"},
                { data: "fields.apache"},
                { data: "fields.pvc"},
                { data: "fields.cuna"},
                { data: "fields.ic"},
		   { data: "fields.glasgowOcular"},
		   { data: "fields.glasgowVerbal"},
		   { data: "fields.glasgowMotora"},

                        ]
            }
	        
		   dataTable = $('#tablaSignosVitalesEnfermeria').DataTable(dataTableOptionsSignosVitalesEnfermeria);

  }


  
}

const initDataTablePanelEnfermeria = async () => {
	if  (dataTablePanelEnfermeriaInitialized)  {
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
 	    data = JSON.stringify(data);

	// alert("sede = " + sede);

        arrancaEnfermeria(1,data);
	    dataTablePanelEnfermeriaInitialized = true;

        arrancaEnfermeria(6,data);
	    dataTableTurnosEnfermeriaInitialized = true;

}


 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTablePanelEnfermeria();
	 $('#tablaPanelEnfermeria tbody tr:eq(0) .miSol').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript

});


 /* FIN ONLOAD */



$('#tablaPanelEnfermeria tbody').on('click', '.miIngresoEnfermeriaId', function() {

	//  alert ("Seleccione Enfermeria");

        var post_id = $(this).data('pk');
	ingresoId =   post_id;

	document.getElementById("ingresoId").value = ingresoId;

    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var enfermeriaId=0;
	var enfermeriaRecibeId = document.getElementById("enfermeriaRecibeId").value;

         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['ingresoId'] = ingresoId;
	data['enfermeriaId'] = enfermeriaId;
	data['enfermeriaRecibeId'] = enfermeriaRecibeId;
	
 	    data = JSON.stringify(data);

	  $.ajax({
                data: {'ingresoId':ingresoId},
	        url: "/buscaDatosPacienteEnfermeria/",
                type: "POST",
                dataType: 'json',
                success: function (info) {
			
		document.getElementById("nombreTipoDoc").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documento").innerHTML = info[0].fields.documento;
		document.getElementById("paciente").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmision").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicio").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacion").innerHTML = info[0].fields.cama;

		document.getElementById("nombreTipoDocM").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoM").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteM").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionM").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioM").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionM").innerHTML = info[0].fields.cama;


		document.getElementById("nombreTipoDocD").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoD").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteD").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionD").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioD").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionD").innerHTML = info[0].fields.cama;


		document.getElementById("nombreTipoDocN").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoN").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteN").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionN").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioN").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionN").innerHTML = info[0].fields.cama;


		document.getElementById("nombreTipoDocDev").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoDev").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteDev").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionDev").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioDev").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionDev").innerHTML = info[0].fields.cama;


		document.getElementById("nombreTipoDocConsDev").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoConsDev").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteConsDev").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionConsDev").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioConsDev").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionConsDev").innerHTML = info[0].fields.cama;

		document.getElementById("nombreTipoDocSig").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoSig").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteSig").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionSig").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioSig").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionSig").innerHTML = info[0].fields.cama;

		document.getElementById("nombreTipoDocPar").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoPar").innerHTML = info[0].fields.documento;
		document.getElementById("pacientePar").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionPar").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioPar").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionPar").innerHTML = info[0].fields.cama;



                },
         error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },
            });



	     arrancaEnfermeria(2,data);
	     dataTableMedicamentosEnfermeriaInitialized = true;

	     arrancaEnfermeria(3,data);
	     dataTableParaclinicosEnfermeriaEnfermeriaInitialized = true;

	     arrancaEnfermeria(4,data);
	     dataTablePedidosEnfermeriaInitialized = true;

	     arrancaEnfermeria(5,data);
	     dataTablePedidosEnfermeriaDetalleInitialized = true;


	     arrancaEnfermeria(6,data);
	     dataTableTurnossEnfermeriaInitialized = true;


	     arrancaEnfermeria(7,data);
	     dataTablePlaneacionEnfermeriaInitialized = true;
		
	     arrancaEnfermeria(8,data);
	     dataTableDietasEnfermeriaInitialized = true;

	     arrancaEnfermeria(9,data);
	     dataTableNotasEnfermeriaInitialized = true;

	     arrancaEnfermeria(10,data);
	     dataTableDevolucionEnfermeriaInitialized = true;

	    arrancaEnfermeria(11,data);
	    dataTableConsultaDevolucionesEnfermeriaInitialized = true;

	    arrancaEnfermeria(13,data);
	    dataTableSignosVitalesEnfermeriaInitialized = true;

      
  });

$('#tablaConsultaDevolucionesEnfermeria tbody').on('click', '.miConsultaDev', function() {

	//  alert ("A tablaConsultaDevolucionesEnfermeria");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	devolucionEnfermeriaId = post_id;

    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	  var username_id = document.getElementById("username_id").value;
 
         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
        data['devolucionEnfermeriaId'] = devolucionEnfermeriaId;

 	    data = JSON.stringify(data);

	    arrancaEnfermeria(12,data);
	    dataTableConsultaDevolucionesDetalleEnfermeriaInitialized = true;

});



$('#tablaPedidosEnfermeria tbody').on('click', '.miPedidosEnfermeria', function() {

	//  alert ("Seleccione miPedidosEnfermeria");

	     var post_id = $(this).data('pk');
	enfermeriaId =   post_id;

	document.getElementById("enfermeriaId").value = enfermeriaId;

         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['enfermeriaId'] = enfermeriaId;

	 data = JSON.stringify(data);

  	 arrancaEnfermeria(5,data);
	 dataTablePedidosEnfermeriaDetalleInitialized = true;
      
  });



function ModalPedidosEnfermeriaCabezote()
{
	// alert("ENTRE cargar modal CreaPedidosEnfermeriaCabezote");

	 $('#postFormModalCreaPedidosEnfermeria').trigger("reset");

            $('#modelHeadingPedidosEnfermeria').html("Creacon Pedidos Enfermeria");
            $('#creaModalPedidosEnfermeria').modal('show');     



}


function CreaPedidosEnfermeriaCabezote()
{

		// alert("ENTRE CreaPedidosEnfermeriaCabezote");
	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	var ingresoId = document.getElementById("ingresoId").value ;

        var enfermeriaTipoOrigen = document.getElementById("enfermeriaTipoOrigenx").value;
        var enfermeriaTipoMovimiento = document.getElementById("enfermeriaTipoMovimientox").value;
        var servicioEnfermeria = document.getElementById("servicioEnfermeria").value;

	//  alert("username_id: " + username_id );
	// alert("enfermeriaTipoOrigen: " + enfermeriaTipoOrigen );
	//  alert("enfermeriaTipoMovimiento : " + enfermeriaTipoMovimiento  );
		
     $.ajax({

	        url: "/creaPedidosEnfermeriaCabezote/",
                data: {'ingresoId':ingresoId, 'username_id':username_id ,'sede':sede,'enfermeriaTipoOrigen':enfermeriaTipoOrigen,'enfermeriaTipoMovimiento':enfermeriaTipoMovimiento,'servicioEnfermeria':servicioEnfermeria},
                type: "POST",
                dataType: 'json',
                success: function (info) {

		if (info.success=true)
		{
		document.getElementById("mensajes").innerHTML = 'Se actualiza cambio de estado';
		}
		else
		{
		document.getElementById("mensajesError").innerHTML = info.Mensaje
		}


	         var data =  {}   ;
	        data['username'] = username;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
		   data['ingresoId'] = ingresoId;

	    data = JSON.stringify(data);

	        arrancaEnfermeria(4,data);

	        dataTablePedidosEnfermeriaInitialized = true;


                },
               error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });
		   $('#creaModalPedidosEnfermeria').modal('hide');  


}

$('#tablaMedicamentosEnfermeria tbody').on('click', '.miMedicamentosId', function() {

	//  alert ("Sleecion Meicamento");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	var enfermeriaRecibeId = post_id;


	var ingresoId = document.getElementById("ingresoId").value ;



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
	data['ingresoId'] = ingresoId;
	data['enfermeriaRecibeId'] = enfermeriaRecibeId;
	
 	    data = JSON.stringify(data);

	     arrancaEnfermeria(7,data);
	     dataTablePlaneacionEnfermeriaInitialized = true;


});

$('#tablaPlaneacionEnfermeria tbody').on('click', '.miAplicacionEnfermeria', function() {

	//  alert ("A Aplicar Medicamentos");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	var row = $(this).closest('tr'); // Encuentra la fila

	

	var table = $('#tablaPlaneacionEnfermeria').DataTable();  // Inicializa el DataTable jquery//
	
 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
       console.log("rowindex= " , rowindex);

	    	 dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "Suministro es =  = " , dato3.medicamento); 
		document.getElementById("planeacionEnfermeriaId").value = dato3.id;



	// Aquip cargar modal planeacion medicamentos
	 $('#postFormModalPlaneacionEnfermeria').trigger("reset");

            $('#modelHeadingAplicaEnfermeria').html("Creacon Pedidos Enfermeria");
		document.getElementById("dosisA").value =dato3.dosis;
		document.getElementById("medidaA").value = dato3.medida;
		document.getElementById("cantidadA").value = dato3.cantidadPlaneada;
		document.getElementById("suministroA").value = dato3.suministro;
		document.getElementById("viaA").value = dato3.via;
		//  alert("via = " + dato3.via);
		document.getElementById("frecuenciaA").value = dato3.frecuencia;
		document.getElementById("diasTratamientoA").value = dato3.dias;
		document.getElementById("enfermeriaRecibeId").value = post_id;


            $('#ModalAplicacionEnfermeria').modal('show');     



});




$('#tablaMedicamentosEnfermeria tbody').on('click', '.Planear', function() {

	//  alert ("A planear Meidcamentos");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	var row = $(this).closest('tr'); // Encuentra la fila



	var table = $('#tablaMedicamentosEnfermeria').DataTable();  // Inicializa el DataTable jquery//
	
 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
       console.log("rowindex= " , rowindex);

	    	 dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "Suministro es =  = " , dato3.medicamento); 



	// Aquip cargar modal planeacion medicamentos
	 $('#postFormModalPlaneacionEnfermeria').trigger("reset");

            $('#modelHeadingPlaneacionEnfermeria').html("Creacon Pedidos Enfermeria");
		document.getElementById("dosisP").value =dato3.dosis;
		document.getElementById("medidaP").value = dato3.UnidadMedida;
		document.getElementById("cantidadP").value = dato3.cantidad;
		document.getElementById("suministroP").value = dato3.medicamento;
		document.getElementById("viaP").value = dato3.via;
		//  alert("via = " + dato3.via);
		document.getElementById("frecuenciaP").value = dato3.frecuencia;
		document.getElementById("diasTratamientoP").value = dato3.diasTratamiento;
		document.getElementById("numeroPlaneos").value = 0;
		document.getElementById("enfermeriaRecibeId").value = post_id;


            $('#ModalPlaneacionEnfermeria').modal('show');     


  });



$('#tablaDevolucionEnfermeria tbody').on('click', '.Devolver', function() {

	//  alert ("A devolver Meidcamentos");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	var row = $(this).closest('tr'); // Encuentra la fila



	var table = $('#tablaDevolucionEnfermeria').DataTable();  // Inicializa el DataTable jquery//
	
 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
       console.log("rowindex= " , rowindex);

	    	 dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "Suministro es =  = " , dato3.medicamento); 



	// Aquip cargar modal planeacion medicamentos
	 $('#postFormModalDevolvernEnfermeria').trigger("reset");

            $('#modelHeadingDevolvernEnfermeria').html("Devolver a Farmacia");
		document.getElementById("dosisDev").value =dato3.dosis;
		document.getElementById("medidaDev").value = dato3.UnidadMedida;
		document.getElementById("cantidadDev").value = dato3.cantidad;
		document.getElementById("cantidadPura").value = dato3.cantidad;
		document.getElementById("suministroDev").value = dato3.medicamento;
		document.getElementById("viaDev").value = dato3.via;
		//  alert("via = " + dato3.via);
		document.getElementById("frecuenciaDev").value = dato3.frecuencia;
		document.getElementById("diasTratamientoDev").value = dato3.diasTratamiento;
		document.getElementById("numeroPlaneos").value = 0;
		document.getElementById("enfermeriaRecibeId").value = post_id;
		document.getElementById("recibeDevId").value =dato3.id;



            $('#ModalDevolverEnfermeria').modal('show');     


  });



function GuardarPlaneacion() 
{
	//  alert ("A Guardar planeacion medicamentos");

	     var post_id = $(this).data('pk');
	// alert ("post_id = " + post_id);
	var ingresoId = document.getElementById("ingresoId").value ;

   	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

	var enfermeriaRecibeId  = document.getElementById("enfermeriaRecibeId").value;
	var desdePlanea = document.getElementById("desdePlanea").value;

	//  alert(" desdePlanea = " + desdePlanea );


        var numeroPlaneos = document.getElementById("numeroPlaneos").value;
        var frecuenciaP = document.getElementById("frecuenciaP").value;

	var dosisP = document.getElementById("dosisP").value;
	var medidaP = document.getElementById("medidaP").value;
	var suministroP = document.getElementById("suministroP").value;
	var viaP = document.getElementById("viaP").value;
	var diasTratamientoP = document.getElementById("diasTratamientoP").value;
	var cantidadP = document.getElementById("cantidadP").value;

         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['enfermeriaRecibeId'] = enfermeriaRecibeId;
	data['desdePlanea'] = desdePlanea;
	data['numeroPlaneos'] = numeroPlaneos;
	data['frecuenciaP'] = frecuenciaP;
	data['ingresoId'] = ingresoId;

 	    data = JSON.stringify(data);

	  $.ajax({
                data: {'sede':sede,'username_id':username_id, 'enfermeriaRecibeId':enfermeriaRecibeId,'desdePlanea':desdePlanea, 'numeroPlaneos':numeroPlaneos, 'frecuenciaP':frecuenciaP,'dosisP':dosisP, 'medidaP':medidaP, 'suministroP':suministroP, 'viaP':viaP, 'diasTratamientoP':diasTratamientoP, 'cantidadP' : cantidadP },
	        url: "/guardaPlaneacionEnfermeria/",
                type: "POST",
                dataType: 'json',
                success: function (info) {
		if (info.success = true)
		{
		document.getElementById("mensajes").innerHTML =	info.Mensaje;	
		}
		else
		{
		document.getElementById("mensajesError").innerHTML = info.Mensaje;			
		return;
		}

	     arrancaEnfermeria(7,data);
	     dataTablePlaneacionEnfermeriaInitialized = true;

	
	
                },
         error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });

		 $('#postFormModalPlaneacionEnfermeria').trigger("reset");
		 $('#ModalPlaneacionEnfermeria').modal('hide');  




      
  };



function GuardarAplicacion() 
{
	//  alert ("A Guardar Aplicacion medicamentos");

	     var post_id = $(this).data('pk');
	
	var ingresoId = document.getElementById("ingresoId").value ;

		registroAplica =  document.getElementById("planeacionEnfermeriaId").value ;



   	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

	var enfermeriaRecibeId  = document.getElementById("enfermeriaRecibeId").value;
	var fechaAplica = document.getElementById("fechaAplica").value;

	//  alert(" ingresoId= " + ingresoId);
	//  alert("fechaAplica= " + fechaAplica);


	var enfermeriaRecibeId  = document.getElementById("enfermeriaRecibeId").value;




	var dosisA = document.getElementById("dosisA").value;
	var medidaA = document.getElementById("medidaA").value;
	var suministroA = document.getElementById("suministroA").value;
	var viaA = document.getElementById("viaA").value;
	var diasTratamientoA = document.getElementById("diasTratamientoA").value;
	var cantidadA = document.getElementById("cantidadA").value;
        var frecuenciaA = document.getElementById("frecuenciaA").value;

         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['enfermeriaRecibeId'] = enfermeriaRecibeId;
	data['ingresoId'] = ingresoId;

 	    data = JSON.stringify(data);

	  $.ajax({
                data: {'sede':sede,'username_id':username_id,
			'enfermeriaRecibeId':enfermeriaRecibeId,'fechaAplica':fechaAplica,'frecuenciaA':frecuenciaA, 
			'dosisA':dosisA,'medidaA':medidaA,
			 'suministroA':suministroA,'viaA':viaA,'diasTratamientoA':diasTratamientoA,
			 'cantidadA':cantidadA ,'registroAplica':registroAplica },
	        url: "/guardaAplicacionEnfermeria/",
                type: "POST",
                dataType: 'json',
                success: function (info) {
			
		if (info.success = true)
		{
		document.getElementById("mensajes").innerHTML =	info.Mensaje;	
		}
		else
		{
		document.getElementById("mensajesError").innerHTML = info.Mensaje;			
		return;
		}

	
	     arrancaEnfermeria(7,data);
	     dataTablePlaneacionEnfermeriaInitialized = true;

                },
                  error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });

		 $('#postFormModalAplicacionEnfermeria').trigger("reset");
		 $('#ModalAplicacionEnfermeria').modal('hide');  



      
  };





// Medicamentos

function tableActionsFormulacionEnfermeria() {

   var table10 = $('#tablaFormulacionEnfermeria').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '100px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deleteRevisionSistemas' id='borraDiag'>" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 13
               }
            ],
        lengthMenu: [5],
    columns:[
    //"dummy" configuration
        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
	  { visible: false }, //col 4
	  { visible: true }, //col 5
	  { visible: false }, //col 6
	  { visible: true }, //col 7


            ],
    });
}

// FIN MEDICAMENTOS


function GuardarPedido()
{

	// Formulacion
	//  alert("Entre a GRABAR PedidosEnfermeria");

     	var username = document.getElementById("username").value;
        var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var servicioAdmonEnfermeria = document.getElementById("servicioAdmonEnfermeria").value;
        var enfermeriaId = document.getElementById("enfermeriaId").value;


    const table10 = $('#tablaFormulacionEnfermeria').DataTable();
     var datos_tabla10 = table10.rows().data().toArray();

        formulacionEnfermeria=[]

	for(var i= 0; i < datos_tabla10.length; i++) {

	    formulacionEnfermeria.push({
	        "medicamentos"    : datos_tabla10[i][0] ,
	        "dosis"    : datos_tabla10[i][2],
	        "uMedidaDosis"    : datos_tabla10[i][3] ,
	      /*  "vias"    : datos_tabla10[i][4] , */
	        "viasAdministracion"    : datos_tabla10[i][4] ,
	        "cantidadMedicamento"    : datos_tabla10[i][5] ,

	      });
	   };

	    formulacionEnfermeria  = JSON.stringify(formulacionEnfermeria);

	   //  alert("Esto envio formulacionEnfermeri = " + formulacionEnfermeria)
    
 	// Fin Formulacion


  $.ajax({
            	   type: 'POST',
 	               url: '/adicionarFormulacionEnfermeria/',
  	               data: { 'username':username, 'sede':sede, 'username_id':username_id,'formulacionEnfermeria':formulacionEnfermeria,
                            'servicioAdmonEnfermeria':servicioAdmonEnfermeria,'enfermeriaId':enfermeriaId},
 	      		success: function (data) {

			if (info.success = true)
			{
			document.getElementById("mensajes").innerHTML =	info.Mensaje;	
			}
			else
			{
			document.getElementById("mensajesError").innerHTML = info.Mensaje;			
			}


    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var ingresoId = document.getElementById("ingresoId").value;
 
         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['enfermeriaId'] = enfermeriaId;

	    data['ingresoId'] = ingresoId;
 	    data = JSON.stringify(data);

	    arrancaEnfermeria(4,data);
	    dataTablePedidosEnfermeriaInitialized = true;

	    arrancaEnfermeria(5,data);
	    dataTablePedidosEnfermeriaDetalleInitialized = true;

        // aqui inicializar tablaFormulacion etc

        /// Aqui inicializar combos

 document.getElementById("serviciosAdmonEnfermeria").selectedIndex = 0;

	// document.getElementById("serviciosAdministrativosN").selectedIndex = 0;

        var tabla = $('#tablaFormulacionEnfermeria').DataTable();
        tabla.rows().remove().draw();


 	      		}, // cierra function sucess
 	      	         error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },
			 // cierra error function
  	        });  // cierra ajax


}



function GuardarDietas() 
{
	// alert ("A GuardarDietas");

	     var post_id = $(this).data('pk');
	
	var ingresoId = document.getElementById("ingresoId").value ;


   	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

	 var tiposDietasD = document.getElementById("tiposDietasD").value;
	 var observacionesD = document.getElementById("observacionesD").value;
	 var serviciosAdministrativosD = document.getElementById("serviciosAdministrativosD").value;

	//  alert(" ingresoId= " + ingresoId);


         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['ingresoId'] = ingresoId;

 	    data = JSON.stringify(data);

	  $.ajax({
                data: {'sede':sede,'username_id':username_id,'tiposDietasD':tiposDietasD, 'observacionesD':observacionesD, 'ingresoId':ingresoId,'serviciosAdministrativosD':serviciosAdministrativosD},
	        url: "/guardaDietasEnfermeria/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

		if (info.success = true)
		{
		document.getElementById("mensajes").innerHTML =	info.Mensaje;	
		}
		else
		{
		document.getElementById("mensajesError").innerHTML = info.Mensaje;			
		}

	    arrancaEnfermeria(8,data);
	    dataTableDietaEnfermeriaInitialized = true;




    /// Aqui inicializar combos

	 document.getElementById("serviciosAdministrativosD").selectedIndex = 0;
        $("tiposDietasD").prop('selectedIndex', 0);



			document.getElementById("mensajes").innerHTML = 'Error Contacte a su Administrador' + ': ' + info

                },
                   error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });


	     arrancaEnfermeria(8,data);
	     dataTableDietasEnfermeriaInitialized = true;

      
  };




function GuardarNotasEnfermeria() 
{
	//  alert ("A GuardarNotasEnfermeria");

	     var post_id = $(this).data('pk');
	
	var ingresoId = document.getElementById("ingresoId").value ;


   	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;


	 var observacionesN = document.getElementById("observacionesN").value;
	 var serviciosAdministrativosN = document.getElementById("serviciosAdministrativosN").value;

	//  alert(" ingresoId= " + ingresoId);


         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['ingresoId'] = ingresoId;

 	    data = JSON.stringify(data);

	  $.ajax({
                data: {'sede':sede,'username_id':username_id, 'observacionesN':observacionesN, 'ingresoId':ingresoId,'serviciosAdministrativosN':serviciosAdministrativosN},
	        url: "/guardaNotasEnfermeria/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

		if (info.success = true)
		{
		document.getElementById("mensajes").innerHTML =	info.Mensaje;	
		}
		else
		{
		document.getElementById("mensajesError").innerHTML = info.Mensaje;			
		}

		alert("Voy a hacer el REFRESH");


	     arrancaEnfermeria(9,data);
	     dataTableNotasEnfermeriaInitialized = true;



    /// Aqui inicializar combos
	 document.getElementById("serviciosAdministrativosN").selectedIndex = 0;
	document.getElementById("observacionesN").value = '';


                },
              error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });



      
  };


function GuardarDevolucion()
{

	// Formulacion
	//  alert("Entre a GRABAR GuardarDevolucion");

     	var username = document.getElementById("username").value;
        var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var servicioAdmonEnfermeria = document.getElementById("serviciosAdministrativosDev").value;
        var enfermeriaId = document.getElementById("enfermeriaId").value;
        var enfermeriaRecibeId = document.getElementById("recibeDevId").value;


    const table10 = $('#tablaFormulacionDevolucion').DataTable();
     var datos_tabla11 = table10.rows().data().toArray();


        formulacionDevolucion=[]

	for(var i= 0; i < datos_tabla11.length; i++) {

	    formulacionDevolucion.push({
	        "enfermeriaRecibeId"    : datos_tabla11[i][0] ,
	        "medicamentos"    : datos_tabla11[i][1] ,
	        "dosis"    : datos_tabla11[i][2],
	        "uMedidaDosis"    : datos_tabla11[i][3] ,
	        "viasAdministracion"    : datos_tabla11[i][4] ,
	        "cantidadMedicamento"    : datos_tabla11[i][5] ,
	        "observaciones"    : datos_tabla11[i][6] ,

	      });
	   };

	    formulacionDevolucion  = JSON.stringify(formulacionDevolucion);

	   //   alert("Esto envio formulacionDevolucion = " + formulacionDevolucion);
    
 	// Fin Formulacion


  $.ajax({
            	   type: 'POST',
 	               url: '/guardarDevolucionEnfermeria/',
  	               data: { 'username':username, 'sede':sede, 'username_id':username_id,'formulacionDevolucion':formulacionDevolucion,
                            'servicioAdmonEnfermeria':servicioAdmonEnfermeria,'enfermeriaId':enfermeriaId},
 	      		success: function (data) {

		if (data.success = true)
		{
		document.getElementById("mensajes").innerHTML =	info.Mensaje;	
		}
		else
		{
		document.getElementById("mensajesError").innerHTML = info.Mensaje;			
		}

    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var ingresoId = document.getElementById("ingresoId").value;
 
         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;

	    data['ingresoId'] = ingresoId;
 	    data = JSON.stringify(data);

	    arrancaEnfermeria(4,data);
	    dataTablePedidosEnfermeriaInitialized = true;

	    arrancaEnfermeria(5,data);
	    dataTablePedidosEnfermeriaDetalleInitialized = true;

        // aqui inicializar tablaFormulacion etc

        /// Aqui inicializar combos
        // $("servicioAdmonEnfermeriaDev").prop('selectedIndex', 0);
 document.getElementById("servicioAdmonEnfermeriaDev").selectedIndex = 0;

        var tabla = $('#tablaFormulacionDevolucion').DataTable();
        tabla.rows().remove().draw();


 	      		}, // cierra function sucess
 	      	         error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText;
			        },
 // cierra error function
  	        });  // cierra ajax


}

function GuardarSignoVitalEnfermeria() 
{
	//  alert ("A GuardarSignoVital");

	  	
	var ingresoId = document.getElementById("ingresoId").value ;
   	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        //var fecha = document.getElementById("fechaSig").value;
        var frecCardiaca = document.getElementById("frecCardiaca").value;
        var frecRespiratoria = document.getElementById("frecRespiratoria").value;
        var tensionADiastolica = document.getElementById("tensionADiastolica").value;
        var tensionASistolica = document.getElementById("tensionASistolica").value;
        var tensionAMedia = document.getElementById("tensionAMedia").value;
        var temperatura = document.getElementById("temperatura").value;
        var saturacion = document.getElementById("saturacion").value;
        var glucometria = document.getElementById("glucometria").value;
        var glasgow = document.getElementById("glasgow").value;
        var apache = document.getElementById("apache").value;
        var pvc = document.getElementById("pvc").value;
        var cuna = document.getElementById("cuna").value;
        var ic = document.getElementById("ic").value;
        var glasgowOcular = document.getElementById("glasgowOcular").value;
        var glasgowVerbal = document.getElementById("glasgowVerbal").value;
        var glasgowMotora = document.getElementById("glasgowMotora").value;
        var observacion = document.getElementById("observacionSig").value;
        var serviciosAdministrativosSig = document.getElementById("serviciosAdministrativosSig").value;

	//  alert(" ingresoId= " + ingresoId);


         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['ingresoId'] = ingresoId;

 	    data = JSON.stringify(data);

	  $.ajax({
                data: {'sede':sede,'username_id':username_id, 'ingresoId':ingresoId,
         'frecCardiaca':frecCardiaca,	'frecRespiratoria':frecRespiratoria,
	'tensionADiastolica':tensionADiastolica,'tensionASistolica':tensionASistolica,'tensionAMedia':tensionAMedia,
	'temperatura':temperatura,'saturacion':saturacion,'glucometria':glucometria,'glasgow':glasgow,
	'apache':apache,'pvc':pvc,'cuna':cuna,'ic':ic,'glasgowOcular':glasgowOcular,'glasgowVerbal':glasgowVerbal,
	'glasgowMotora':glasgowMotora,'observacion':observacion,'serviciosAdministrativosSig':serviciosAdministrativosSig},
	        url: "/guardaSignosVitalEnfermeria/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

		//  alert ("llegue listop");
document.getElementById("frecCardiaca").value = '';
document.getElementById("frecRespiratoria").value= '';
document.getElementById("tensionADiastolica").value= '';
document.getElementById("tensionASistolica").value= '';
document.getElementById("tensionAMedia").value= '';
document.getElementById("temperatura").value= '';
document.getElementById("saturacion").value= '';
document.getElementById("glucometria").value= '';
document.getElementById("glasgow").value= '';
document.getElementById("apache").value= '';
document.getElementById("pvc").value= '';
document.getElementById("cuna").value= '';
document.getElementById("ic").value= '';
document.getElementById("glasgowOcular").value= '';
document.getElementById("glasgowVerbal").value= '';
document.getElementById("glasgowMotora").value= '';
document.getElementById("observacionSig").value= '';

        /// Aqui inicializar combos

 document.getElementById("serviciosAdministrativosSig").selectedIndex = 0;


	     arrancaEnfermeria(13,data);
	     dataTableSignosVitalesEnfermeriaInitialized = true;

		if (info.success = true)
		{
		document.getElementById("mensajes").innerHTML =	info.Mensaje;	
		}
		else
		{
		document.getElementById("mensajesError").innerHTML = info.Mensaje;			
		}


                },
                 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });

      
  };




