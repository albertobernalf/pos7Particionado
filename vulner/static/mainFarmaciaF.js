console.log('Hola Alberto Hi!')

let dataTable;
let dataTableB;
let dataTableC;
let dataTableD;
let dataTableF;
let dataTableG;
let dataTableH;
let dataTableI;

let dataTablePanelFarmaciaInitialized = false;
let dataTableFarmaciaDespachosInitialized = false;
let dataTableFarmaciaDespachosDispensaInitialized = false;
let dataTableFarmaciaDetalleInitialized = false;
let dataTableFarmaciaDetalleOrdenadosInitialized = false;
let dataTableDespachosFarmaciaDispensaInitialized = false;
let dataTableDespachosFarmaciaInitialized = false;
let dataTableDespachosDetalleFarmaciaInitialized = false;

let dataTableDevolucionesFarmaciaInitialized = false;
let dataTableDevolucionesDetalleFarmaciaInitialized = false;
var controlMed = 0;


$(document).ready(function() {


// aqui van los filtros de busqueda

$('#tablaFormulacion tbody').on('click', 'tr', function () {
    confirm("Desea eliminar LA FILA: ");
       var tableL = $('#tablaFormulacion').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
        //   alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaFormulacion").deleteRow(fila-1);

});


/*------------------------------------------
        --------------------------------------------
        Create Post Code Formulacion
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarFormulacion').click(function (e) {
            e.preventDefault();


   	   if (controlMed == 0)
   	   {
   	   var table10 = $('#tablaFormulacion').DataTable({scrollY: '80px', paging:false,  search:false,  scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlMed=1;
   	   }
   	   else
   	   {
	  var table10 = $('#tablaFormulacion').DataTable();
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
      	   textViasAdministracion = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada
	
	        var cantidadMedicamento =  document.getElementById("cantidadMedicamento").value;
            var farmaciaDetalleId = document.getElementById("farmaciaDetalle").value;

	    table10.row.add([  medicamentos, textMedicamentos, dosis,  textUMedidaDosis, textViasAdministracion, cantidadMedicamento   , farmaciaDetalleId,   '<i class="fa fa-trash"></i>']).draw(false);

        });




});


function arrancaFarmacia(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsPanelFarmacia  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success',
      messageTop: 'Farmacia Ordenes' ,
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger',
      messageTop: 'Farmacia Ordenes' ,
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info',
      messageTop: 'Farmacia Ordenes' ,
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
		    search: "<i class='fa fa-search'></i> Buscar: _INPUT_",
		    //search: 'Buscar:',
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
                 url:"/load_dataFarmacia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miFarmacia' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miSelFarmacia form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

{
	  "render": function ( data, type, row ) {
                        var btn = '';

	     btn = btn + " <button class='miEditaFarmaciaEstadoDespacho btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },

	},


                { data: "fields.id"},
                { data: "fields.tipoDoc"},
		  { data: "fields.documento"},
		  { data: "fields.paciente"},
		  { data: "fields.servicio"},
		  { data: "fields.cama"},

                { data: "fields.origen"},
		   { data: "fields.mov"}, 
                { data: "fields.servicio"},
                { data: "fields.historia"},
		  { data: "fields.estado"},


                        ]
            }
	        
		   dataTable = $('#tablaPanelFarmacia').DataTable(dataTableOptionsPanelFarmacia);


  }


    if (valorTabla == 2)
    {
        let dataTableOptionsFarmaciaDespachos  ={
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
                 url:"/load_dataFarmaciaDespachos/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miFarmaciaDespachos' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miFarmaciaDespachos form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
                { data: "fields.origen"},
		   { data: "fields.mov"}, 
                { data: "fields.servicio"},
                { data: "fields.historia"},
                        ]
            }
	        
		   dataTable = $('#tablaFarmaciaDespachos').DataTable(dataTableOptionsFarmaciaDespachos);


  }



    if (valorTabla == 3)
    {
        let dataTableOptionsFarmaciaDetalle  ={
 dom: "<'row mb-0'<'col-sm-2'B><'col-sm-1'><'col-sm-4'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
	// text: '<i class="bi bi-file-earmark-excel-fill"></i> Exportar Excel',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success btn-sm',
      messageTop: 'Farmacia Ordenes' ,
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger btn-sm',
      messageTop: 'Farmacia Ordenes' ,
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info btn-sm',
      messageTop: 'Farmacia Ordenes' ,
    },
  ],

  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '200px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 6
               }
            ],
	 pageLength: 20,
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
                 url:"/load_dataFarmaciaDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miFarmaciaDetalle2' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miFarmaciaDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
        		{ data: "fields.dosis"},
                { data: "fields.unidadDosis"},
                { data: "fields.suministro"},
                { data: "fields.viaAdministracion"},
                { data: "fields.cantidad"},

                	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='despachado' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='despachado form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


                        ]
            }
	        
		   dataTable = $('#tablaFarmaciaDetalle').DataTable(dataTableOptionsFarmaciaDetalle);


  }

    if (valorTabla == 4)
    {
        let dataTableOptionsFarmaciaDespachosDispensa  ={
//   dom: "<'row mb-1'<'col-sm-2'B><'col-sm-1'><'col-sm-4'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
  //           "<'row'<'col-sm-12'tr>>" +
    //         "<'row mt-0'<'col-sm-7'i><'col-sm-5'p>>",


   dom: "<'row mb-0'<'col-sm-2'B><'col-sm-1'><'col-sm-4'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-4'i><'col-sm-4'p>>",



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
                 url:"/load_dataFarmaciaDespachosDispensa/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miFarmaciaDespachosDispensa2' class='miFarmaciaDespachosDispensa form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
                { data: "fields.despacho"},
	    	   { data: "fields.suministro"},
                { data: "fields.dosis"},
                { data: "fields.unidadDosis"},
                { data: "fields.via"},
                { data: "fields.cantidad"},

                        ]
            }
	        
		   dataTable = $('#tablaFarmaciaDespachosDispensa').DataTable(dataTableOptionsFarmaciaDespachosDispensa);


  }


    if (valorTabla == 5)
    {
        let dataTableOptionsDespachosFarmacia  ={
   dom: "<'row mb-1'<'col-sm-2'B><'col-sm-1'><'col-sm-4'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-7'i><'col-sm-5'p>>",
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
            scrollY: '300px',
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
                 url:"/load_dataDespachosFarmacia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';


		 btn = btn + " <input type='radio' name='miDespachoFarmacia2' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;'  class='miDespachoFarmacia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},
                { data:"fields.id"},
                { data:"fields.despacho"},
	    	{ data:"fields.servEntrega"},
                { data:"fields.entrega"},
                { data:"fields.servRecibe"},
                { data:"fields.recibe"},

                	{
	  "render": function ( data, type, row ) {
                        var btn = '';
		 btn = btn + " <input type='radio' name='miImprimirDesp' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;'  class='miImprimirDespacho form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
	},
                       ]
            }
	        
		   dataTable = $('#tablaDespachosFarmacia').DataTable(dataTableOptionsDespachosFarmacia);


  }


    if (valorTabla == 6)
    {
        let dataTableOptionsDespachosDetalleFarmacia  ={
   dom: "<'row mb-1'<'col-sm-2'B><'col-sm-1'><'col-sm-4'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-7'i><'col-sm-5'p>>",
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
            scrollY: '300px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
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
                 url:"/load_dataDespachosDetalleFarmacia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miDespachoDetalleFarmacia' class='miDespachoDetalleFarmacia form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
              	   { data: "fields.dosis"},
                { data: "fields.unidadMedida"},
                { data: "fields.cantidad"},
                { data: "fields.suministro"},
                        ]
            }
	        
		   dataTable = $('#tablaDespachosDetalleFarmacia').DataTable(dataTableOptionsDespachosDetalleFarmacia);


  }

  

    if (valorTabla == 7)
    {
        let dataTableOptionsDevolucionesFarmacia  ={
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
                 url:"/load_dataDevolucionesFarmacia/" +  data,
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
	{
	  "render": function ( data, type, row ) {
                        var btn = '';
     btn = btn + " <button class='RecibirDevolucion btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";
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
	        
		   dataTable = $('#tablaDevolucionesFarmacia').DataTable(dataTableOptionsDevolucionesFarmacia);


  }


    if (valorTabla == 8)
    {
        let dataTableOptionsDevolucionesDetalleFarmacia  ={
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
                 url:"/load_dataDevolucionesDetalleFarmacia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';
     btn = btn + " <button class='RecibirDevolucionDetalle btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";
                       return btn;
                    },

	},
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
	        
		   dataTable = $('#tablaDevolucionesDetalleFarmacia').DataTable(dataTableOptionsDevolucionesDetalleFarmacia);

  }


    if (valorTabla == 9)
    {
        let dataTableOptionsFarmaciaDetalleOrdenados  ={
 dom: "<'row mb-0'<'col-sm-2'B><'col-sm-1'><'col-sm-4'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
	// text: '<i class="bi bi-file-earmark-excel-fill"></i> Exportar Excel',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success btn-sm',
      messageTop: 'Farmacia Ordenes' ,
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger btn-sm',
      messageTop: 'Farmacia Ordenes' ,
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info btn-sm',
      messageTop: 'Farmacia Ordenes' ,
    },
  ],

  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '200px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
		{
                    "targets": 6
               }
            ],
	 pageLength: 20,
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
                 url:"/load_dataFarmaciaDetalleOrdenados/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miFarmaciaDetalle2Ordenados' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miFarmaciaDetalleOrdenados form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

                { data: "fields.id"},
        		{ data: "fields.dosis"},
                { data: "fields.unidadDosis"},
                { data: "fields.suministro"},
                { data: "fields.viaAdministracion"},
                { data: "fields.cantidad"},

                	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='despachadoOrdenados' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='despachadoOrdenados form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


                        ]
            }

		   dataTable = $('#tablaFarmaciaDetalleOrdenados').DataTable(dataTableOptionsFarmaciaDetalleOrdenados);


  }



}

const initDataTablePanelFarmacia = async () => {
	if  (dataTablePanelFarmaciaInitialized)  {
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

	//  alert("sede = " + sede);

        arrancaFarmacia(1,data);
	    dataTablePanelFarmaciaInitialized = true;

        arrancaFarmacia(5,data);
	dataTableDespachosFarmaciaInitialized = true;


        //arrancaFarmacia(2,data);
	    //dataTableFarmaciaDespachosInitialized = true;

      //  arrancaFarmacia(4,data);
	//    dataTableFarmaciaDespachosDispensaInitialized = true;


       // arrancaFarmacia(7,data);
	 //   dataTableDevolucionesDetalleFarmaciaInitialized = true;


}


 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTablePanelFarmacia();
	 $('#tablaPanelFarmacia tbody tr:eq(0) .miSol').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript

});


 /* FIN ONLOAD */


$('#tablaPanelFarmacia tbody').on('click', '.miSelFarmacia', function() {

		//  alert("ENTRE miSelFarmacia");

	     var post_id = $(this).data('pk');
	farmaciaId =   post_id;
	//  alert("farmaciaId = " +  farmaciaId);

	document.getElementById("farmaciaId").value = farmaciaId;

    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	var farmaciaDetalleId= "";
         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['farmaciaId'] = farmaciaId;
	data['farmaciaDetalleId'] = farmaciaDetalleId;

 	    data = JSON.stringify(data);

     $.ajax({
                data: {'farmaciaId':farmaciaId},
	        url: "/buscaDatosPaciente/",
                type: "POST",
                dataType: 'json',
                success: function (info) {


        document.getElementById("ordenFarmacia").innerHTML =  farmaciaId;
		document.getElementById("nombreTipoDocN").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoN").innerHTML = info[0].fields.documento;
		document.getElementById("paciente").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmision").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicio").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacion").innerHTML = info[0].fields.cama;

        document.getElementById("ordenFarmaciaX").innerHTML =  farmaciaId;
		document.getElementById("nombreTipoDocNX").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoNX").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteX").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionX").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioX").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionX").innerHTML = info[0].fields.cama;


		document.getElementById("nombreTipoDocDev").innerHTML = info[0].fields.nombreTipoDoc;
		document.getElementById("documentoDev").innerHTML = info[0].fields.documento;
		document.getElementById("pacienteDev").innerHTML = info[0].fields.paciente;
		document.getElementById("consecutivoAdmisionDev").innerHTML = info[0].fields.consecutivoAdmision;
		document.getElementById("servicioDev").innerHTML = info[0].fields.servicio;
		document.getElementById("habitacionDev").innerHTML = info[0].fields.cama;



                },
     	        error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },
            });

	     arrancaFarmacia(3,data);
	     dataTableFarmaciaDetalleInitialized = true;

	     arrancaFarmacia(5,data);
	     dataTableDespachosFarmaciaInitialized = true;

	     arrancaFarmacia(9,data);
	     dataTableFarmaciaDetalleOrdenadosInitialized = true;


	    // arrancaFarmacia(7,data);
	    // dataTableDespachosFarmaciaInitialized = true;

     
  });


$('#tablaDevolucionesFarmacia tbody').on('click', '.miConsultaDev', function() {

	//  alert ("A tablaDevolucionesFarmaciaa");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	devolucionFarmaciaId = post_id;

    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	  var username_id = document.getElementById("username_id").value;
 document.getElementById("devolucionFarmaciaId").value = devolucionFarmaciaId;

         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
        data['devolucionFarmaciaId'] = devolucionFarmaciaId;

 	    data = JSON.stringify(data);

	    arrancaFarmacia(8,data);
	    dataTableDevolucionesDetalleFarmaciaInitialized = true;

});

$('#tablaDevolucionesFarmacia tbody').on('click', '.RecibirDevolucion', function() {

	//  alert ("A RecibirDevolucion Farmacia");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	devolucionFarmaciaId = post_id;
	$('#postFormRecibirDevolucionFarmacia').trigger("reset");

	document.getElementById("devolucionNo").innerHTML =devolucionFarmaciaId;
	document.getElementById("solicitudNo").innerHTML =farmaciaId;
	document.getElementById("devolucionFarmaciaId").value = devolucionFarmaciaId;

            $('#modelHeadingRecibirDevolucionFarmacia').html("Recibir Devolucion Farmacia");
            $('#ModalRecibirDevolucionFarmacia').modal('show');  



});

$('#tablaDevolucionesDetalleFarmacia tbody').on('click', '.RecibirDevolucionDetalle', function() {

	//  alert ("A RecibirDevolucion Detalle Farmacia");

	     var post_id = $(this).data('pk');
	//  alert ("post_id = " + post_id);
	devolucionDetalleFarmaciaId = post_id;
	$('#postFormRecibirDevolucionDetalleFarmacia').trigger("reset");
	var row = $(this).closest('tr'); // Encuentra la fila
	var table = $('#tablaDevolucionesDetalleFarmacia').DataTable();  // Inicializa el DataTable jquery//
	
 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
       console.log("rowindex= " , rowindex);

	    	 dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "Cantidad es =  = " , dato3.cantidadDevuelta); 
	
	document.getElementById("devolucionDetalleNo").innerHTML =devolucionDetalleFarmaciaId;
	document.getElementById("solicitudDetalleNo").innerHTML =devolucionFarmaciaId;
	document.getElementById("cantidadDevueltaY").value = dato3.cantidadDevuelta;
	document.getElementById("cantidadDevueltaRecibidaY").value =0;
	


            $('#modelHeadingRecibirDevolucionDetalleFarmacia').html("Recibir Devolucion Detalle Farmacia ");
            $('#ModalRecibirDevolucionDetalleFarmacia').modal('show');  

});






$('#tablaFarmaciaDetalle tbody').on('click', '.miFarmaciaDetalle', function() {

		//  alert("ENTRE tablaFarmaciaDetalle");

	     var post_id = $(this).data('pk');
	farmaciaDetalleId =   post_id;

	document.getElementById("farmaciaDetalle").value = farmaciaDetalleId;
	farmaciaId = document.getElementById("farmaciaId").value ;

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
	data['farmaciaDetalleId'] = farmaciaDetalleId;
	data['farmaciaId'] = farmaciaId;
 	    data = JSON.stringify(data);

	     arrancaFarmacia(4,data);
		     	dataTableFarmaciaDespachosDispensaInitialized = true;


  });


$('#tablaFarmaciaDetalle tbody').on('click', '.despachado', function() {



	     var post_id = $(this).data('pk');
	farmaciaDetalleId =   post_id;

 alert("ENTRE despachado" +  farmaciaDetalleId);
	// document.getElementById("farmaciaDetalle").value = farmaciaDetalleId;
	// farmaciaId = document.getElementById("farmaciaId").value ;

    // Aqui ajax que marca despachado (S) el detalle de farmacia

         $.ajax({
                data: {'farmaciaDetalleId':farmaciaDetalleId },
	        url: "/despachadoFarmaciaDetalle/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

                alert("regrese " + JSON.stringify(info));

		if (info.success == true)
			 {
			  document.getElementById("mensajes").innerHTML = data.Mensaje;
			 }
			else
			{
			document.getElementById("mensajesError").innerHTML = data.Mensaje;
			return;
			}
                },
             	        error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });

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
    	data['farmaciaDetalleId'] = farmaciaDetalleId;
    	data['farmaciaId'] = farmaciaId;
 	    data = JSON.stringify(data);

	     arrancaFarmacia(3,data);
	  	dataTableFarmaciaDetalleInitialized = true;

    document.getElementById("farmaciaDetalle").value = 0;
        	data['farmaciaDetalleId'] = document.getElementById("farmaciaDetalle").value;
 	    data = JSON.stringify(data);

	    arrancaFarmacia(4,data);
	  	dataTableFarmaciaDespachosDispensaInitialized = true;


  });



// Cambia estado despacho implora Modal

$('#tablaPanelFarmacia tbody').on('click', '.miEditaFarmaciaEstadoDespacho', function() {

		//  alert("ENTRE miEditaFarmaciaEstadoDespach");

	     var post_id = $(this).data('pk');
	var farmaciaId =   post_id;
	//  alert("farmaciaId = " +  farmaciaId);

 $('#postFormModalEstadoFarmacia').trigger("reset");

            $('#modelHeadingProgramacionCirugia').html("Actualiza Estado Despacho");
            $('#creaModalEstadoFarmacia').modal('show');     


  });


$('#tablaDespachosFarmacia tbody').on('click', '.miDespachoFarmacia2', function() {

		//  alert("ENTRE tablaDespachosFarmacia VE");

   	        var post_id = $(this).data('pk');

		var despachoId =   post_id;
		//  alert("despacho = " +  despachoId);

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
	data['despachoId'] = despachoId;
	    data = JSON.stringify(data);


		     arrancaFarmacia(6,data);
		     	dataTableDespachosDetalleFarmaciaInitialized = true;

		     arrancaFarmacia(7,data);
		     	dataTableDevolucionesFarmaciaInitialized = true;
   
		     arrancaFarmacia(8,data);
		     	dataTableDevolucionesDetalleFarmaciaInitialized = true;



  });

$('#tablaDespachosFarmacia tbody').on('click', '.miImprimirDespacho', function() {
		  alert("ENTRE miImprimirDespacho ");
	      var post_id = $(this).data('pk');
		var despachoId =   post_id;
		var farmaciaId = document.getElementById("farmaciaId").value;
		alert("voy ajax con farmaciaId = " + farmaciaId);
		alert("voy ajax con despachoId = " + despachoId);

$.ajax({
 	data: {'farmaciaId':farmaciaId, 'despachoId':despachoId},
	url: "/imprimirDespachoFarmacia/",
	method: 'POST',
	xhrFields: {
        	responseType: 'blob' // Importante: interpreta la respuesta como binario
		    },
    success: function (data) {

        var blob = new Blob([data], { type: 'application/pdf' });
        var link = window.URL.createObjectURL(blob);
        window.open(link, '_blank'); // Abre el PDF en nueva pestaña 
    },

    error: function (error) {
      document.getElementById("mensajesError").value =  data.responseText;
    }
});
  });


function CambiaEstadoDespacho()
{

		//  alert("ENTRE miEditaFarmaciaEstadoDespach");
	farmaciaId = document.getElementById("farmaciaId").value ;
	//  alert("farmaciaId = " +  farmaciaId);

	document.getElementById("farmaciaId").value = farmaciaId;
    	var estadoFarmaciaDespacho = document.getElementById("estadoFarmaciaDespacho").value;

     $.ajax({
                data: {'farmaciaId':farmaciaId,'estadoFarmaciaDespacho':estadoFarmaciaDespacho },
	        url: "/cambiaEstadoDespacho/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

		if (info.success == true)
			 {
			  document.getElementById("mensajes").innerHTML = data.Mensaje;
			 }
			else
			{
			document.getElementById("mensajesError").innerHTML = data.Mensaje;
			return;
			}


                },
             	        error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

            });
		   $('#creaModalEstadoFarmacia').modal('hide');  
		     arrancaFarmacia(1,data);
		     	dataTableFarmaciaInitialized = true;

  };



// Medicamentos

function tableActionsFormulacion() {

   var table10 = $('#tablaFormulacion').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '300px',
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
                    "targets": 14
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
	              { visible: true }, //col 1


            ],
    });
}

// FIN MEDICAMENTOS


function AdicionarDespachosDispensa()
{

	// Formulacion
	//  alert("Entre a GRABAR despacho");

     	var username = document.getElementById("username").value;
        var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var farmaciaDetalleId = document.getElementById("farmaciaDetalle").value;
        var servicioAdmonEntrega = document.getElementById("servicioAdmonEntregaF").value;
        var servicioAdmonRecibe = document.getElementById("servicioAdmonRecibeF").value;
        var plantaEntrega = document.getElementById("plantaEntregaF").value;
        var plantaRecibe = document.getElementById("plantaRecibeF").value;
        var farmaciaId = document.getElementById("farmaciaId").value;
	//  alert("plantaRecibe = " + plantaRecibe );


    const table10 = $('#tablaFormulacion').DataTable();
     var datos_tabla10 = table10.rows().data().toArray();

        formulacion=[]


	for(var i= 0; i < datos_tabla10.length; i++) {

	    formulacion.push({
	        "medicamentos"    : datos_tabla10[i][0] ,
	        "dosis"    : datos_tabla10[i][2],
	        "uMedidaDosis"    : datos_tabla10[i][3] ,
	      /*  "vias"    : datos_tabla10[i][4] , */
	        "viasAdministracion"    : datos_tabla10[i][4] ,
	        "cantidadMedicamento"    : datos_tabla10[i][5] ,
	       "farmaciaDetalleId"    : datos_tabla10[i][6] ,

	      });
	   };

	    formulacion  = JSON.stringify(formulacion);

	      alert("Esto envio formulacion = " + formulacion)
    
 	// Fin Formulacion


  $.ajax({
            	   type: 'POST',
 	               url: '/adicionarDespachosDispensa/',
  	               data: { 'username':username, 'sede':sede, 'username_id':username_id,'formulacion':formulacion,
                            'farmaciaDetalleId':farmaciaDetalleId,'servicioAdmonEntrega':servicioAdmonEntrega, 'servicioAdmonRecibe':servicioAdmonRecibe,
                             	   'plantaEntrega':plantaEntrega, 'plantaRecibe':plantaRecibe, 'farmaciaId':farmaciaId},
 	      		success: function (data) {

     			    $("#mensajes").html(data.message);

			document.getElementById("mensajes").innerHTML = data.message;

    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var farmaciaId = document.getElementById("farmaciaId").value;
        var farmaciaDetalleId = document.getElementById("farmaciaDetalle").value;
         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;

	    data['farmaciaId'] = farmaciaId;
	    data['farmaciaDetalleId'] = farmaciaDetalleId;

 	    data = JSON.stringify(data);

        arrancaFarmacia(1,data);
	    dataTableFarmaciaDespachosInitialized = true;

        arrancaFarmacia(4,data);
	dataTableFarmaciaDespachosDispensaInitialized = true;


         arrancaFarmacia(5,data);
	 dataTableDespachosFarmaciaInitialized = true;


        // aqui inicializar tablaFormulacion etc


        var tabla = $('#tablaFormulacion').DataTable();
        tabla.rows().remove().draw();


        /// Aqui inicializar combos

servicioAdmonEntrega.selectedIndex = 0;
plantaEntrega.selectedIndex = 0;
servicioAdmonRecibe.selectedIndex = 0;
plantaRecibe.selectedIndex = 0;


 	      		}, // cierra function sucess
		     	        error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },

 	      	//	}, // cierra error function
  	        });  // cierra ajax


}


function RecibirDevolucionFarmacia()
{

	//  alert("RecibirDevolucionFarmacia");
    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        // var farmaciaId = document.getElementById("farmaciaId").value;
        // var farmaciaDetalleId = document.getElementById("farmaciaDetalle").value;
        var devolucionFarmaciaId = document.getElementById("devolucionNo").innerHTML;
	//  alert("devolucionFarmaciaId = " + devolucionFarmaciaId);

	var servicioRecibeId = document.getElementById("servicioRecibe").value;
	var plantaRecibeId = document.getElementById("plantaRecibe").value;

  $.ajax({
            	   type: 'POST',
 	               url: '/recibirDevolucionFarmacia/',
  	               data: { 'username':username, 'sede':sede, 'username_id':username_id,'devolucionFarmaciaId':devolucionFarmaciaId,
                            'servicioRecibeId':servicioRecibeId,'plantaRecibeId':plantaRecibeId},
 	      		success: function (data) {

		if (data.success == true)
			 {
			  document.getElementById("mensajes").innerHTML = data.Mensaje;
			 }
			else
			{
			document.getElementById("mensajesError").innerHTML = data.Mensaje;
			return;
			}


	       $('#ModalRecibirDevolucionFarmacia').modal('hide');  
	         var data =  {}   ;
	        data['username'] = username;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;

	 	    data = JSON.stringify(data);

	  		   arrancaFarmacia(7,data);
		     	dataTableDevolucionesFarmaciaInitialized = true;
      

 	      		}, // cierra function sucess
 	      		     	        error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },
					 // cierra error function
  	        });  // cierra ajax

}

function RecibirDevolucionDetalleFarmacia()
{

	//  alert("RecibirDevolucionDetalleFarmacia");
    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
        var devolucionFarmaciaId = document.getElementById("devolucionFarmaciaId").value;
        // var farmaciaId = document.getElementById("farmaciaId").value;
        // var farmaciaDetalleId = document.getElementById("farmaciaDetalle").value;
        var devolucionDetalleFarmaciaId = document.getElementById("devolucionDetalleNo").innerHTML;
	//  alert("devolucionDetalleFarmaciaId = " + devolucionDetalleFarmaciaId);

	var cantidadDevueltaRecibida = document.getElementById("cantidadDevueltaRecibidaY").value;


  $.ajax({
            	   type: 'POST',
 	               url: '/recibirDevolucionDetalleFarmacia/',
  	               data: { 'username':username, 'sede':sede, 'username_id':username_id,'devolucionDetalleFarmaciaId':devolucionDetalleFarmaciaId,
                            'cantidadDevueltaRecibida':cantidadDevueltaRecibida},
 	      		success: function (data) {

		if (data.success == true)
			 {
			  document.getElementById("mensajes").innerHTML = data.Mensaje;
			 }
			else
			{
			document.getElementById("mensajesError").innerHTML = data.Mensaje;
			return;
			}



	       $('#ModalRecibirDevolucionDetalleFarmacia').modal('hide');  
	         var data =  {}   ;
	        data['username'] = username;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
	        data['devolucionFarmaciaId'] =devolucionFarmaciaId;

	 	    data = JSON.stringify(data);

	  		   arrancaFarmacia(8,data);
		     	dataTableDevolucionesDetalleFarmaciaInitialized = true;

 	      		}, // cierra function sucess
 	      	     	        error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },
		 // cierra error function
  	        });  // cierra ajax

}
