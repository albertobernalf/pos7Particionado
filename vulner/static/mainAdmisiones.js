
console.log('Hola Alberto Hi!')
var datavta;

var x=0
var  folio_final =0

const form = document.getElementById('formHistoria')

const form2 = document.getElementById('formClinicos')
console.log(form)
console.log(form2)
let dataTable;
let dataTableB;
let dataTableC;
let dataTableAdmisionesInitialized = false;
let dataTableAdmisionesConvenios = false;
let dataTableAbonosAdmisionesInitialized =false;
let dataTableAbonosAutorizacionesInitialized =false;
let dataTableCensoInitialized =false;
let dataTableHabitacionesInitialized =false;


$(document).ready(function() {
    var table = $('#tablaDatos').DataTable();
    
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

function arrancaAdmisiones(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsAdmisiones  ={

 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",

//  dom: 'Bfrtilp',
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
	// text: '<i class="bi bi-file-earmark-excel-fill"></i> Exportar Excel',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success btn-sm',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger btn-sm',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info btn-sm',
    },
  ],
	autoWidth: false,
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '450px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
             "rowClass": function( row, data, index ) {
      return 'my-row-class';
    },

 // select: {
  //          style: 'single' // o 'multi'
  //      },

            columnDefs: [
            { width: '1%', targets: [0,1] },
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6,7,8,9,10], // índice de la columna que quieres evitar que haga wrap

		    },
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
                 url:"/load_dataAdmisiones/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

              btn = btn + " <input type='radio'  name='ingresoId' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miIngresoId form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

		{
			"render": function ( data, type, row ) {
                        var btn = '';

	        btn = btn + " <button class='miEditaAdmision btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
		}
                    },

		{
		"render": function ( data, type, row ) {
                        var btn = '';

	  btn = btn + " <button class='ImprimirHojaAdmision btn-primary ' data-pk='" + row.pk + "'>" + '<i class=""fa-duotone fa-solid fa-print""></i>' + "</button>";

                       return btn;
		}
                   },
		{
		"render": function ( data, type, row ) {
                        var btn = '';

	  btn = btn + " <button class='ImprimirAtencionInicialUrgencias btn-primary ' data-pk='" + row.pk + "'>" + '<i class=""fa-duotone fa-solid fa-print""></i>' + "</button>";

                       return btn;
		}
                   },

		{
		"render": function ( data, type, row ) {
                        var btn = '';

	  btn = btn + " <button class='ImprimirManilla btn-primary ' data-pk='" + row.pk + "'>" + '<i class=""fa-duotone fa-solid fa-print""></i>' + "</button>";

                       return btn;
		}
                   },


                 { data: "fields.id"},
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


            ] //,
	 //initComplete: function(settings, json) {
            // Selecciona la primera fila (índice 0)
      //      table.row(':eq(0)'{ page: 'current' }).select();

            // Alternativa: Si no usas la extensión 'select'// busca el checkbox y márcalo manualmente:
            // table.row(0).node().querySelector('input[type="checkbox"]').checked = true;
       // }

             }

	        dataTable = $('#tablaDatos').DataTable(dataTableOptionsAdmisiones);
       // dataTable.row(0).node().querySelector('input[name="ingresoId"]').checked = true;
        // dataTable.row(0).document.querySelector('input[name=".miIngresoId"]').checked = true;

        //	$('#tablaDatos tbody tr:eq(0) .miIngresoId').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript



  }

      if (valorTabla == 2)
    {
        let dataTableOptionsConvenios  ={
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
		{     "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostConvenios' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa fa-trash"></i>' + "</button>";
                       return btn;
                    },

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
                 url:"/load_dataConvenioAdmisiones/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
                 { data: "fields.id"},
                { data: "fields.nombreDocumento"},
                { data: "fields.nombre"},
                { data: "fields.consec"},
                { data: "fields.convenio"},
            ]
             }

	        dataTable = $('#tablaConveniosAdmisiones').DataTable(dataTableOptionsConvenios);

  }

      if (valorTabla == 3)
    {
        let dataTableOptionsAbonosAdmisiones  ={

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
		{ className: 'centered', targets: [0, 1, 2] },
	    { width: '10%', targets: [2] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostAbonos' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa fa-trash"></i>' + "</button>";
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
                 url:"/load_dataAbonosAdmisiones/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		 { data: "fields.id"},
	  /*                { data: "fields.tipoPago"}, */
		{
			target: 0,
			visible: false
		},

                { data: "fields.nombreTipoPago"},
	/*	{ data: "fields.formaPago"}, */
			{
			target: 2,
			visible: false
		},
                { data: "fields.nombreFormaPago"},
                { data: "fields.valor"},
                { data: "fields.descripcion"},
		{ data: "fields.estadoReg"},
            ]
             }

	        dataTable = $('#tablaAbonosAdmisiones').DataTable(dataTableOptionsAbonosAdmisiones);
  }

    if (valorTabla == 4)
    {
        let dataTableOptionsAutorizaciones  ={
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",

//  dom: 'Bfrtilp',
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
	// text: '<i class="bi bi-file-earmark-excel-fill"></i> Exportar Excel',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success btn-sm',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger btn-sm',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info btn-sm',
    },
  ],
	
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '360px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6,7,8], // índice de la columna que quieres evitar que haga wrap
		      className: 'nowrap-column'
		    },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                      return btn;
                    },
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
                 url:"/load_dataAutorizacionesAdmisiones/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
  {
		"render": function ( data, type, row ) {
                        var btn = '';

	 	 btn = btn + " <button class='ImprimirAutorizacion btn-primary ' data-pk='" + row.pk + "'>" + '<i class=""fa-duotone fa-solid fa-print""></i>' + "</button>";

                       return btn;
		}
                   },
                 { data: "fields.id"},
                 { data: "fields.fechaSolicitud" }, 
                { data: "fields.numeroAutorizacion"},
                { data: "fields.fechaAutorizacion"},
                { data: "fields.estado"},
                { data: "fields.empresa"},
                { data: "fields.examen"},
                { data: "fields.cums"},
                { data: "fields.valorAutorizado"},
	       { data: "fields.autDetalle"}, 
                { data: "fields.nombreSuministro"},
	        { data: "fields.nombreExamen"},

            ]
             }

	        dataTable = $('#tablaAutorizaciones').DataTable(dataTableOptionsAutorizaciones);

  }

    if (valorTabla == 5)
    {
        let dataTableOptionsCenso  ={
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",

//  dom: 'Bfrtilp',
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
	// text: '<i class="bi bi-file-earmark-excel-fill"></i> Exportar Excel',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success btn-sm',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger btn-sm',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info btn-sm',
    },
  ],
	
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '360px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6,7,8], // índice de la columna que quieres evitar que haga wrap
		      className: 'nowrap-column'
		    },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                      return btn;
                    },
                    "targets": 9
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
                 url:"/load_dataCensoAdmisiones/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
                 { data: "fields.sede"},
                 { data: "fields.servicio" }, 
                { data: "fields.subservicio"},
                { data: "fields.nombre"},
                { data: "fields.tipoDoc"},
                { data: "fields.Documento"},
                { data: "fields.paciente"},
                { data: "fields.ocupa"},
                { data: "fields.accion"},

            ]
             }

	        dataTable = $('#tablaCenso').DataTable(dataTableOptionsCenso);

  }

    if (valorTabla == 6)
    {
        let dataTableOptionsHabitaciones  ={
 dom: "<'row mb-0'<'col-sm-6'f><'col-sm-4'><'col-sm-2'B>>" + // B = Botones a la izquierda, f = filtro a la derecha
            "<'row'<'col-sm-12'tr>>" +
             "<'row mt-0'<'col-sm-5'i><'col-sm-7'p>>",

//  dom: 'Bfrtilp',
  buttons: [
    {
      extend: 'excelHtml5',
      text: '<i class="fas fa-file-excel"></i> ',
	// text: '<i class="bi bi-file-earmark-excel-fill"></i> Exportar Excel',
      titleAttr: 'Exportar a Excel',
      className: 'btn btn-success btn-sm',
    },
    {
      extend: 'pdfHtml5',
      text: '<i class="fas fa-file-pdf"></i> ',
      titleAttr: 'Exportar a PDF',
      className: 'btn btn-danger btn-sm',
    },
    {
      extend: 'print',
      text: '<i class="fa fa-print"></i> ',
      titleAttr: 'Imprimir',
      className: 'btn btn-info btn-sm',
    },
  ],
	
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '360px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6,7,8], // índice de la columna que quieres evitar que haga wrap
		      className: 'nowrap-column'
		    },
		{     "render": function ( data, type, row ) {
                        var btn = '';
                      return btn;
                    },
                    "targets": 9
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
                 url:"/load_dataHabitacionesAdmisiones/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
                 { data: "fields.sede"},
                 { data: "fields.servicio" }, 
                { data: "fields.subservicio"},
                { data: "fields.numero"},
                { data: "fields.accion"},
                { data: "fields.fecha"},
                { data: "fields.tipoDoc"},
                { data: "fields.Documento"},
                { data: "fields.paciente"},



            ]
             }

	        dataTable = $('#tablaHabitaciones').DataTable(dataTableOptionsHabitaciones);

  }



}


const initDataTableAdmisiones = async () => {
	if  (dataTableAdmisionesInitialized)  {
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



         var valor = $('input[name="ingresoId"]:checked').val();



	 var sede = document.getElementById("sede").value;


	 document.getElementById("ingresoIdGlobal").value = valor;
	 document.getElementById("ingresoId22").value = valor;

	 document.getElementById("ingresoId1").value = valor;
	 document.getElementById("ingresoId2").value = valor;
	 document.getElementById("ingresoId4").value = valor;
	 document.getElementById("ingresoId5").value = valor;
	 document.getElementById("ingresoId6").value = valor;
	 // document.getElementById("ingresoIdF").value = valor;

         // var sede = document.getElementById("sede1").value;
	//  var ingresoId= document.getElementById("ingresoId1").value;



          data['sede'] = sede;
        

 	    data = JSON.stringify(data);

        arrancaAdmisiones(1,data);
	    dataTableAdmisionesInitialized = true;



        arrancaAdmisiones(5,data);
	    dataTableCensoInitialized = true;

	marcarRegistroInicial();
          $('input[name="ingresoId"]').prop('checked', true);

        // arrancaAdmisiones(6,data);
	//    dataTableHabitacionesInitialized = true;


}

 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableAdmisiones();
	 //$('#tablaDatos tbody tr:eq(0) .miIngresoId').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript
	
});


 /* FIN ONLOAD */


    	/*------------------------------------------
        --------------------------------------------
        Click to Button
        --------------------------------------------
        --------------------------------------------*/
        $('#createNewPost').click(function () {

		
            $('#saveBtnCrearConvenio').val("Create Post");
            $('#post_id').val('');
            $('#postFormCrearConvenio').trigger("reset");
            $('#modelHeading').html("Creacion convenios en admision");
//		var ingresos = $('input[name="ingresoId"]:checked').val();
		ingresoId1 = document.getElementById("ingresoId1").value
	   
	    document.getElementById("ingresoId2").value = ingresoId1;

            $('#crearConvenioModel').modal('show');
        });

	/*--------------------------------------------
        Click to Edit Button
        --------------------------------------------
        --------------------------------------------*/
        $('body').on('click', '.editPost', function () {

          var post_id = $(this).data('pk');
        //  alert("pk1 = " + $(this).data('pk'));

      	$.ajax({
	           url: '/creacionHc/postConsultaHcli/',
	            data : {post_id:post_id},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {
                       // alert("Regrese");
                       // alert("respuesta="  + data);

			 $('#pk').val(data.pk);
        	        $('#tipoDocId').val(data.tipoDocId);
                	$('#nombreTipoDoc').val(data.nombreTipoDoc);
	                $('#documentoId').val(data.documentoId);
	                $('#documento').val(data.documento);
	                $('#consec').val(data.consec);


                    },
	   	        error: function(data){
		       		document.getElementById("mensajesErrorAbonos").value =  data.responseText
			        },
      });
        });



    	/*------------------------------------------
        --------------------------------------------
        Click to Button
        --------------------------------------------
        --------------------------------------------*/
        $('#createNewPostAbonos').click(function () {

	    var ingresoId= document.getElementById("ingresoId1").value;
	    document.getElementById("ingresoId2").value = ingresoId;
       // alert("ingresoId" + ingresoId);

	    if (ingresoId=='undefined')
		{
		// alert("Debe seleccionar Ingreso");
		return;
		}

        // Tiene que hace run ajax para leer los convenios del paciente

		   $.ajax({
	           url: '/buscaConveniosAbonoAdmision/' ,
	            data : {'ingresoId':ingresoId},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data2) {
	  		// alert("llegue con : " + JSON.stringify(data2));

			if (data2 == '')
				{
				// alert("Debe crear un Convenio");
				document.getElementById("mensajesErrorAbonos").value = 'Debe crear un Convenio';
				return;
				}

	  	    var options = '<option value="=================="></option>';
	  		//var dato = JSON.parse(data2);
            const $id2 = document.querySelector("#convenioPaciente");
 	      	$("#convenioPaciente").empty();
			// alert("voy a llenar combo conveniospaciente");
	                 $.each(data2, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

            $('#saveBtnCrearAbonos').val("Create Post");
            $('#post_id').val('');
            $('#postFormCrearAbonos').trigger("reset");
            $('#modelHeading').html("Creacion Abonos en admision");
            $('#crearAbonosModel').modal('show');
                    },
	   		                error: function(data){
		       		document.getElementById("mensajesErrorAbonos").value =  data.responseText
			        },
      });
        });

        /*------------------------------------------
        --------------------------------------------
        Print Error Msg
        --------------------------------------------
        --------------------------------------------*/
        function printErrorMsg(msg) {
            $('.error-msg').find('ul').html('');
            $('.error-msg').css('display','block');
            $.each( msg, function( key, value ) {
                $(".error-msg").find("ul").append('<li>'+value+'</li>');
            });
        }

        /*------------------------------------------
        --------------------------------------------
        Create Post Code
        --------------------------------------------
        --------------------------------------------*/
        $('#saveBtnCrearConvenio').click(function (e) {
            e.preventDefault();
            $(this).html('Sending..');

            $.ajax({
                data: $('#postFormCrearConvenio').serialize(),

		  url: '/guardaConvenioAdmision/',
                type: "POST",
                dataType: 'json',
                success: function (data) {

			if (data.success==true)
			{
			document.getElementById("mensajes").value = data.Mensaje;
			}

		    $('#crearConvenioModel').modal('hide');
                    $('#postFormCrearConvenio').trigger("reset");

	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
		        var username = document.getElementById("username").value;
		        var nombreSede = document.getElementById("nombreSede").value;
		    	var sede = document.getElementById("sede").value;
		        var username_id = document.getElementById("username_id").value;
		        var ingresoId  = document.getElementById("ingresoId22").value;
		         var data =  {}   ;
		        data['username'] = username;
		        data['sedeSeleccionada'] = sedeSeleccionada;
		        data['nombreSede'] = nombreSede;
		        data['sede'] = sede;
		        data['username_id'] = username_id;   
			data['ingresoId'] = ingresoId;
			
          		 data = JSON.stringify(data);

        		arrancaAdmisiones(2,data);
	 		   dataTableConveniosAdmisionesInitialized = true;

                },


	   		    error: function (data) {
	
				document.getElementById("mensajesErrorModalConvenio").value =  data.responseText;

		  var table = $('#tablaConveniosAdmisiones').DataTable(); // accede de nuevo a la DataTable.
	          table.ajax.reload();

	   	    	}
            });
        });

        /*------------------------------------------
        --------------------------------------------
        Create Post Code Abonos
        --------------------------------------------
        --------------------------------------------*/
        $('#saveBtnCrearAbonos').click(function (e) {
            e.preventDefault();
            $(this).html('Sending..');

            $.ajax({
                data: $('#postFormCrearAbonos').serialize(),

		  url: "/guardaAbonosAdmision/",
                type: "POST",
                dataType: 'json',
                success: function (data) {

			if (data.success==true)
			{
			document.getElementById("mensajes").value = data.Mensaje;
			}

                    $('#crearAbonosModel').modal('hide');
                    $('#postFormCrearAbonos').trigger("reset");
		  	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
		        var username = document.getElementById("username").value;
		        var nombreSede = document.getElementById("nombreSede").value;
		    	var sede = document.getElementById("sede").value;
		        var username_id = document.getElementById("username_id").value;
		        var ingresoId  = document.getElementById("ingresoId22").value;
		         var data =  {}   ;
		        data['username'] = username;
		        data['sedeSeleccionada'] = sedeSeleccionada;
		        data['nombreSede'] = nombreSede;
		        data['sede'] = sede;
		        data['username_id'] = username_id;   
			data['ingresoId'] = ingresoId;
			
          		 data = JSON.stringify(data);

			arrancaAdmisiones(3,data);
		        dataTableAbonosAdmisionesInitialized = true;


                },
                error: function (data) {

		      
			document.getElementById("mensajesErrorAbonos").value =   data.responseText;

		  var tableA = $('#tablaAbonosAdmisiones').DataTable(); // accede de nuevo a la DataTable.
	          tableA.ajax.reload();
                }
            });
        });


/*------------------------------------------
        --------------------------------------------
        Delete Post Code
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostConvenios",function(){
            var current_object = $(this);
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');


		   $.ajax({
	           url: '/postDeleteConveniosAdmision/' ,
	            data : {'id':id},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {
				
				document.getElementById("mensajes").valueL =   data['Mensaje'];
			

			            var table = $('#tablaConveniosAdmisiones').DataTable(); // accede de nuevo a la DataTable.
		                table.ajax.reload();
                    },
	   		    error: function (data) {
    

				document.getElementById("mensajesErrorModalUsuario").value =  data.responseText;

	   	    	}


	           });
	});


/*------------------------------------------
        --------------------------------------------
        Delete Post Code Abonos
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostAbonos",function(){
            var current_object = $(this);
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');


		   $.ajax({
	           url: '/postDeleteAbonosAdmision/' ,
	            data : {'id':id},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {

			if (data.success==false)
			{
		document.getElementById("mensajesError").value =   data.Mensajes;
			}
			else
			{
		document.getElementById("mensajes").value =   data.Mensajes;	
			}



			            var table = $('#tablaConveniosAdmisiones').DataTable(); // accede de nuevo a la DataTable.
		                table.ajax.reload();
                    },
	   		    error: function (data) {
		  

				document.getElementById("mensajesErrorModalUsuario").value =  data.JresponseText;

	   	    	}


	           });
	});
	const get = document.getElementById('dispara');




$('#tablaDatos tbody').on('change', '.miIngresoId', function() {


    var row = $(this).closest('tr'); // Encuentra la fila
	    var valor=   $(this).val()

	  var table = $('#tablaDatos').DataTable();  // Inicializa el DataTable jquery
        var rowindex = table.row(row).data(); // Obtiene los datos de la fila

	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);

		var ingresoId = dato3.id;  // jquery
		var valor = ingresoId;


           document.getElementById("mensajes").innerText="";
           document.getElementById("tipoDocx").value="";
           document.getElementById("documentox").value="";
           document.getElementById("pacientex").value="";
           document.getElementById("consecx").value="";
           document.getElementById("servicioActual").value="";
           document.getElementById("subServicioActual").value="";
           document.getElementById("dependenciaActual").value="";
           document.getElementById("fechaOcupacion").value="";
           document.getElementById("servicioCambio").value="";
           document.getElementById("subServicioCambio").value="";
           document.getElementById("dependenciaCambio").value="";

           document.getElementById("ingresoIdGlobal").value = valor;
     	   document.getElementById("ingresoId22").value = valor;
	       document.getElementById("ingresoId1").value = valor;
	       document.getElementById("ingresoId2").value = valor;

	        document.getElementById("ingresoId4").value = valor;
	        document.getElementById("ingresoId5").value = valor;
	          document.getElementById("ingresoId6").value = valor;
        //    document.getElementById("ingresoIdF").value = valor;

	       var data =  {}   ;
     	   var sede = document.getElementById("sede").value;   
           data['sede'] = sede;
           data['ingresoId'] = ingresoId;

           data = JSON.stringify(data);

	       arrancaAdmisiones(2,data);
	    dataTableAdmisionesConveniosInitialized = true;

         arrancaAdmisiones(3,data);
	    dataTableAbonosAdmisionesInitialized = true;

	// alert("voy a cargar autorizaciones");

         arrancaAdmisiones(4,data);
	    dataTableAutorizacionesInitialized = true;
	// alert("YA PASE  autorizaciones");

         arrancaAdmisiones(6,data);
	    dataTableHabitacionesInitialized = true;

	$.ajax({
		type: 'POST',
    		url: '/cambioServicio/',
		data: {'valor' : valor, 'sede': sede},
		dataType : 'json',
		success: function (cambioServicio) {

		 $('#tipoDocx').val(cambioServicio['Usuarios'].tipoDoc);
		 $('#documentox').val(cambioServicio['Usuarios'].documento);
		 $('#pacientex').val(cambioServicio['Usuarios'].paciente);
		 $('#consecx').val(cambioServicio['Usuarios'].consec);
		$('#servicioActual').val(cambioServicio['DependenciasActual'].servicio);
		$('#subServicioActual').val(cambioServicio['DependenciasActual'].subServicio);
		$('#dependenciaActual').val(cambioServicio['DependenciasActual'].depNombre);
		$('#fechaOcupacion').val(cambioServicio['DependenciasActual'].ocupacion);
		 $('#servicioCambio').val(cambioServicio['Servicios']);
		 $('#subServicioCambio').val(cambioServicio['SubServicios']);
		 $('#dependenciaCambio').val(cambioServicio['DependenciasActual'].habitaciones);

		 $('#convTipoDoc').val(cambioServicio['Usuarios'].tipoDoc);
		 $('#convNumdoc').val(cambioServicio['Usuarios'].documento);
		$('#convPaciente').val(cambioServicio['Usuarios'].paciente);		
		 $('#convConsec').val(cambioServicio['Usuarios'].consec);

		$('#convTipoDocA').val(cambioServicio['Usuarios'].tipoDoc);
		 $('#convNumdocA').val(cambioServicio['Usuarios'].documento);
		 $('#convPacienteA').val(cambioServicio['Usuarios'].paciente);
		 $('#convConsecA').val(cambioServicio['Usuarios'].consec);

		 $('#responsablesC').val(cambioServicio['Usuarios'].responsable);
		  $('#acompananteC').val(cambioServicio['Usuarios'].acompanante);


                     // Desde aquip FURIPS
		  $('#fechaRadicado').val(cambioServicio['Furips'].fechaRadicado);
		  $('#numeroRadicacion').val(cambioServicio['Furips'].numeroRadicacion);
		  $('#numeroFactura').val(cambioServicio['Furips'].numeroFactura);
		  $('#primerNombreVictima').val(cambioServicio['Furips'].primerNombreVictima);
		  $('#segundoNombreVictima').val(cambioServicio['Furips'].segundoNombreVictima);
		  $('#primerApellidoVictima').val(cambioServicio['Furips'].primerApellidoVictima);
		$('#segundoApellidoVictima').val(cambioServicio['Furips'].segundoApellidoVictima);
		  $('#tipoDocVictima').val(cambioServicio['Furips'].tipoDocVictima);


                     // Hasta Aqui FURIPS


                    },
	   		    error: function (data) {
		 
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	});

           // Fin cambio de servicio

	// Sera que aquip le colocamos el ajax de los FURIPS

	// FIN ajax de furips

});



function CierraModal()
{

            $('#usuariosModal').modal('hide');
}

function CierraModalActualiza()
{
        
            $('#modalActualizaAdmision').modal('hide');
        
}


function AUsuario()
{

	var envios = new FormData();


	var tipoDoc = document.getElementById("tipoDoc1").value;


	var documento = document.getElementById("documento1").value;
		var busDocumentoSel = document.getElementById("busDocumentoSel").value;
   var nombre = document.getElementById("nombre1").value;
   var primerNombre = document.getElementById("primerNombre").value;
   var segundoNombre = document.getElementById("segundoNombre").value;
   var primerApellido = document.getElementById("primerApellido").value;
   var segundoApellido = document.getElementById("segundoApellido").value;


  // alert("Documento = " +  documento);

	var genero = document.getElementById("genero").value;
	var pais = document.getElementById("pais").value;
	var departamentos = document.getElementById("departamentos").value;
	var ciudades = document.getElementById("ciudades").value;


	var direccion = document.getElementById("direccion").value;

	var telefono = document.getElementById("telefono").value;
	var contacto = document.getElementById("contacto").value;
	var municipio = document.getElementById("municipios").value;
	var localidad = document.getElementById("localidades").value;
	var estadoCivil = document.getElementById("estadoCivil").value;
	var ocupacion = document.getElementById("ocupaciones").value;
	var correo = document.getElementById("correo").value;
	var fechaNacio = document.getElementById("fechaNacioU").value;

	var centrosc = document.getElementById("centrosc").value;
	var tiposUsuario = document.getElementById("tiposUsuario").value;
	var centrosC_id = document.getElementById("centrosc").value;
	var ripsZonaTerritorial = document.getElementById("ripsZonaTerritorial").value;

	// alert("ripsZonaTerritorial = " + ripsZonaTerritorial);


if (genero =='')
		{

		document.getElementById("mensajesErrorModalUsuario").valueL = 'Suministre Genero';
		return;
		}

				if (fechaNacio =='')
		{

		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Fecha nacimiento';
		return;
		}



		if (pais =='')
		{

		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Pais';
        return;
		}



	if (departamentos =='')
		{

		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Departamento';
        return;
		}

			if (municipio =='')
		{

		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Municipio';
		return;
		}

			if (localidad =='')
		{

		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Localidad';
		return;
		}



		if (ciudades =='')
		{
		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Ciudad';
		return;
		}
		if (direccion =='')
		{
		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Direccion';
		return;
		}
		if (telefono =='')
		{
		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Telefono';
		return;
		}
		if (estadoCivil =='')
		{
		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Estado Civil';
		return;
		}

			if (centrosC_id =='')
		{
		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Centro de donde viene el paciente';
		return;
		}



		if (tiposUsuario =='')
		{
		document.getElementById("mensajesErrorModalUsuario").value = 'Suministre Tipo Usuario';
		return;
		}


	$.ajax({
		type: 'POST',
    	url: '/guardarUsuariosModal/',
		data: {'tipoDoc':tipoDoc,
		        'documento':documento,
		        'nombre':nombre,
                        'primerNombre':primerNombre,
			'segundoNombre':segundoNombre,
			'primerApellido':primerApellido,
			'segundoApellido':segundoApellido,
		        'genero':genero,
		        'fechaNacio':fechaNacio,
		         'pais':pais,
		          'departamentos':departamentos,
		          'ciudades':ciudades,
		          'direccion':direccion,
		          'telefono':telefono,
		          'contacto':contacto,
		           "centrosC_id":centrosC_id,
		            'tiposUsuario':tiposUsuario,
		            'municipios':municipio,
		            'localidades':localidad,
		            'estadoCivil':estadoCivil,
		            'ocupaciones':ocupacion,
		            'correo':correo,
			    'ripsZonaTerritorial':ripsZonaTerritorial},

		success: function (respuesta) {

			$('#usuariosModal').modal('hide');
 
	                $('#mensajes').html(respuesta.Mensaje);



                    },
	   		    error: function (sata) {
  
				document.getElementById("mensajesErrorModalUsuario").value = data.responseText;

	   	    	}
	});
};


// Aqui combos para Cambio de servicio

$(document).on('change', '#servicioCambio', function(event) {

    
    var serv =   $(this).val()
	// alert (" Entre cambio Servicio" + serv);
    var sede =  document.getElementById("sede").value;


        $.ajax({
	           url: '/buscarSubServicios',
	            data : {serv:serv, sede:sede},
	           type: 'GET',
	           dataType : 'json',
	  		success: function (respuesta) {
                       //  alert("Regrese");

	  		   var options = '<option value="=================="></option>';
	  		  var dato = JSON.parse(respuesta);
                     const $id2 = document.querySelector("#subServicioCambio");
 	      		     $("#subServicioCambio").empty();
				// alert("voy a llenar subservicio");
	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });
                    },
	   		    error: function (data) {
			
	   			  	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	     });
});



$(document).on('change', '#subServicioCambio', function(event) {
   //  alert (" Entre cambio Habitacion Servicio");
       var select = document.getElementById("servicioCambio"); /*Obtener el SELECT */
       var serv = select.options[select.selectedIndex].value; /* Obtener el valor */
       var subServ =   $(this).val()
    //   alert("voy a enviar este servicio   = " + serv);
      //  alert("voy a enviar este Subservicio   = " + subServ);
       var sede =  document.getElementById("sede").value;

        $.ajax({
	           url: '/buscarHabitaciones',
		    data : {serv:serv, sede:sede, subServ:subServ, Exc:'S'},
	           type: 'GET',
	           dataType : 'json',
	  		success: function (respuesta) {
	  		   var options = '<option value="=================="></option>';
	  		  var dato = JSON.parse(respuesta);
                     const $id2 = document.querySelector("#dependenciaCambio");
 	      		     $("#dependenciaCambio").empty();
			
	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });
                    },
	   		    error: function (data) {
     		
	   			   	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	     });
});

// Fin combios cambios de Servicio


// Aqui la Grabacion del Cambio de Servicio



// Fin grabacion Cambio de Servicio

///// Aqui la para buscar Usuario  Admisiones ////

$(document).on('change', '#busDocumentoSel', function(event) {

  //      alert("Entre cambio Modal usuarios");

	var envios = new FormData();


   eldocu = document.getElementById("busDocumentoSel").value;
  // alert( "Este es el nro del documento : " + eldocu);
   	var busDocumentoSel = document.getElementById("busDocumentoSel").value;
    // alert("Documento = " +  eldocu);
    //  alert("OtorDocumento = " +  busDocumentoSel);
	 var select = document.getElementById("tipoDoc"); /*Obtener el SELECT */
       var tipoDoc = select.options[select.selectedIndex].value; /* Obtener el valor */
	var documento = document.getElementById("busDocumentoSel").value;

    //  alert("Envio a la MOdal Tipo Doc = " + tipoDoc);
    //  alert("Envio a la MOdal documento = " + documento);

	$.ajax({
		type: 'POST',
    	url: '/findOneUsuario/',
		data: {'tipoDoc':tipoDoc,'documento':documento},
		success: function (Usuarios) {

	//		 alert("entre DATOS MODAL y el nombre es = " + Usuarios.tipoDoc_id + " " +  Usuarios.documento);

                $('#tipoDoc1').val(Usuarios.tipoDoc_id);
		$('#tipoDoc').val(Usuarios.tipoDoc_id);
				$('#documento').val(Usuarios.documento);

				$('#nombre1').val(Usuarios.nombre);

				$('#genero').val(Usuarios.genero);
				$('#departamentos').val(Usuarios.departamento);
				$('#municipios').val(Usuarios.municipio);
				$('#localidades').val(Usuarios.localidad);
				$('#ciudades').val(Usuarios.ciudad);

				$('#direccion').val(Usuarios.direccion);
				$('#telefono').val(Usuarios.telefono);
				$('#contacto').val(Usuarios.contacto);
				$('#estadoCivil').val(Usuarios.estadoCivil);
				$('#ocupaciones').val(Usuarios.ocupacion);
				$('#correo').val(Usuarios.correo);


				$('#centrosc').val(Usuarios.centrosc_id);
				$('#tiposUsuario').val(Usuarios.tiposUsuario_id);

				 $('#usuariosModal').modal({show:true});
			//	 $('#usuariosModal').modal().hide();

                    },
	   		    error: function (data) {
	   
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	});

});


//  FIN

///// Aqui la para buscar Usuario Triage ////

$(document).on('change', '#busDocumentoSelTriage', function(event) {

    //    alert("Entre cambio Modal usuarios Triage");

	var envios = new FormData();

	 var select = document.getElementById("tipoDocTriage"); /*Obtener el SELECT */
    var tipoDoc = select.options[select.selectedIndex].value; /* Obtener el valor */

   documento = document.getElementById("busDocumentoSelTriage").value;
   //  alert( "Este es el documento : " + tipoDoc +  " " + documento);

    //  alert("Envio a la MOdal Tipo Doc = " + tipoDoc);
    //  alert("Envio a la MOdal documento = " + documento);


	$.ajax({
		type: 'POST',
    	url: '/findOneUsuarioTriage/',
		data: {'tipoDoc':tipoDoc,'documento':documento},
		success: function (Usuarios) {

			 //  alert("entre DATOS MODAL y el nombre es = " + Usuarios.tipoDoc_id + " " +  Usuarios.documento);

                $('#tipoDoc').val(Usuarios.tipoDoc_id);
		$('#tipoDoc').val(Usuarios.tipoDoc_id);
				$('#documento').val(Usuarios.documento);

				$('#nombre1').val(Usuarios.nombre);

				$('#genero').val(Usuarios.genero);
				$('#departamentos').val(Usuarios.departamento);
				$('#municipios').val(Usuarios.municipio);
				$('#localidades').val(Usuarios.localidad);
				$('#ciudades').val(Usuarios.ciudad);

				$('#direccion').val(Usuarios.direccion);
				$('#telefono').val(Usuarios.telefono);
				$('#contacto').val(Usuarios.contacto);
				$('#estadoCivil').val(Usuarios.estadoCivil);
				$('#ocupaciones').val(Usuarios.ocupacion);
				$('#correo').val(Usuarios.correo);


				$('#centrosc').val(Usuarios.centrosc_id);
				$('#tiposUsuario').val(Usuarios.tiposUsuario_id);

				 $('#usuariosModalTriage').modal({show:true});
			//	 $('#usuariosModal').modal().hide();
                    },
	   		    error: function (data) {
			
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	});

});


// Aqui usuario para triage

function findOneUsuarioTriage()
{

	var envios = new FormData();

   eldocu = document.getElementById("busDocumentoSelTriage").value;
    // alert( "Este es el nro del documento : " + eldocu);
   	var busDocumentoSelTriage = document.getElementById("busDocumentoSeltriage").value;
     // alert("Documento = " +  eldocu);
    //  alert("OtorDocumento = " +  busDocumentoSelTriage);


	 var select = document.getElementById("tipoDoc"); /*Obtener el SELECT */
       var tipoDoc = select.options[select.selectedIndex].value; /* Obtener el valor */
	var documento = document.getElementById("busDocumentoSelTriage").value;

    //  alert("Envio a la MOdal Tipo Doc = " + tipoDoc);
    //  alert("Envio a la MOdal documento = " + documento);


	$.ajax({
		type: 'POST',
    	url: '/findOneUsuario/',
		data: {'tipoDoc':tipoDoc,'documento':documento},
		success: function (Usuarios) {

			 //  alert("entre DATOS MODAL y el nombre es = " + Usuarios.tipoDoc_id + " " +  Usuarios.documento);

                $('#tipoDoc1').val(Usuarios.tipoDoc_id);
				$('#documento').val(Usuarios.documento);

				$('#nombre1').val(Usuarios.nombre);

				$('#genero').val(Usuarios.genero);
				$('#departamentos').val(Usuarios.departamento);
				$('#municipios').val(Usuarios.municipio);
				$('#localidades').val(Usuarios.localidad);
				$('#ciudades').val(Usuarios.ciudad);

				$('#direccion').val(Usuarios.direccion);
				$('#telefono').val(Usuarios.telefono);
				$('#contacto').val(Usuarios.contacto);
				$('#estadoCivil').val(Usuarios.estadoCivil);
				$('#ocupaciones').val(Usuarios.ocupacion);
				$('#correo').val(Usuarios.correo);
				$('#centrosc').val(Usuarios.centrosc_id);
				$('#tiposUsuario').val(Usuarios.tiposUsuario_id);

				 $('#usuariosModalTriage').modal({show:true});
			//	 $('#usuariosModal').modal().hide();

                    },
	   		    error: function (data) {
		       

	document.getElementById("mensajesError").value =  data.responseText;


	   	    	}
	});
};


$(document).on('change', '#busDocumentoSel22', function(event) {

     var select = document.getElementById("tipoDoc22"); /*Obtener el SELECT */
       var tipoDoc = select.options[select.selectedIndex].value; /* Obtener el valor */


	var documento = document.getElementById("busDocumentoSel22").value;

   // alert("Envio TIPOdOC = " + tipoDoc);
  //  alert("Envio a la MOdal documento = " + documento);


	$.ajax({
		type: 'POST',
    	url: '/findOneUsuario/',
		data: {'tipoDoc':tipoDoc,'documento':documento},
		success: function (Usuarios) {

			// alert("entre DATOS MODAL y el nombre es = " + Usuarios.tipoDoc_id + " " +  Usuarios.documento);

               if ( Usuarios.tipoDoc_id == null)
				{

				$('#tipoDoc1').val(tipoDoc);
				$('#documento1').val(documento);
				}
			     else
 				{
                                $('#tipoDoc1').val(Usuarios.tipoDoc_id);
				$('#documento1').val(Usuarios.documento);
				}
				$('#nombre1').val(Usuarios.nombre);
				$('#genero').val(Usuarios.genero);
				//$('#fechaNacioU').val(Usuarios.fechaNacio);
				 // alert("fecha = " + Usuarios.fechaNacio);

				document.getElementById("fechaNacioU").value = Usuarios.fechaNacio;

				$('#pais').val(Usuarios.pais_id);
				$('#departamentos').val(Usuarios.departamento);
				$('#municipios').val(Usuarios.municipio);
				$('#localidades').val(Usuarios.localidad);
				$('#ciudades').val(Usuarios.ciudad);
				$('#direccion').val(Usuarios.direccion);
				$('#telefono').val(Usuarios.telefono);
				$('#contacto').val(Usuarios.contacto);
				$('#estadoCivil').val(Usuarios.estadoCivil);
				$('#ocupaciones').val(Usuarios.ocupacion);
				$('#correo').val(Usuarios.correo);
				$('#centrosc').val(Usuarios.centrosc_id);
				$('#tiposUsuario').val(Usuarios.tiposUsuario_id);

			 document.getElementById('nombre1').focus();

				$('#usuariosModal').modal('show');



                    },
	   		    error: function (data) {
		
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	});
});




function findOneUsuario1()
{

	var envios = new FormData();

   eldocu = document.getElementById("busDocumentoSel").value;
    // alert( "Este es el nro del documento : " + eldocu);


   	var busDocumentoSel = document.getElementById("busDocumentoSel").value;
    //  alert("Documento = " +  eldocu);
   //   alert("OtorDocumento = " +  busDocumentoSel);

   var select = document.getElementById("tipoDoc"); /*Obtener el SELECT */

       var tipoDoc = select.options[select.selectedIndex].value; /* Obtener el valor */


	var documento = document.getElementById("busDocumentoSel").value;

    //  alert("Envio a la MOdal Tipo Doc = " + tipoDoc);
     // alert("Envio a la MOdal documento = " + documento);


	$.ajax({
		type: 'POST',
    	url: '/findOneUsuario/',
		data: {'tipoDoc':tipoDoc,'documento':documento},
		success: function (Usuarios) {

			 //  alert("entre DATOS MODAL y el nombre es = " + Usuarios.tipoDoc_id + " " +  Usuarios.documento);

                $('#tipoDoc1').val(Usuarios.tipoDoc_id);
				$('#documento').val(Usuarios.documento);
				$('#nombre1').val(Usuarios.nombre);
				$('#genero').val(Usuarios.genero);
				$('#departamentos').val(Usuarios.departamento);
				$('#municipios').val(Usuarios.municipio);
				$('#localidades').val(Usuarios.localidad);
				$('#ciudades').val(Usuarios.ciudad);

				$('#direccion').val(Usuarios.direccion);
				$('#telefono').val(Usuarios.telefono);
				$('#contacto').val(Usuarios.contacto);
				$('#estadoCivil').val(Usuarios.estadoCivil);
				$('#ocupaciones').val(Usuarios.ocupacion);
				$('#correo').val(Usuarios.correo);


				$('#centrosc').val(Usuarios.centrosc_id);
				$('#tiposUsuario').val(Usuarios.tiposUsuario_id);

				 $('#usuariosModal').modal({show:true});
			//	 $('#usuariosModal').modal().hide();

                    },
	   		    error: function (data) {
        
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	});
};



$('#tablaDatos tbody').on('click', '.miEditaAdmision', function() {



    var row = $(this).closest('tr'); // Encuentra la fila
	   
	  var table = $('#tablaDatos').DataTable();  // Inicializa el DataTable jquery
        var rowindex = table.row(row).data(); // Obtiene los datos de la fila

	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);

		var ingresoId = dato3.id;  // jquery


	document.getElementById("ingresoIdActualizar").value = dato3.id;

      var rowIndex = $(this).parent().index('#tablaDatos tbody tr');
      var tdIndex = $(this).index('#tablaDatos tbody tr:eq('+rowIndex+') td');


      tipoDoc=$(this).parents("tr").find("td").eq(0).html();
      documento=$(this).parents("tr").find("td").eq(1).html();
      consec=$(this).parents("tr").find("td").eq(3).html();
      var sede = document.getElementById("sede").value;


      $.ajax({
		type: 'POST',
      	url: '/encuentraAdmisionModal/',
      	data: {'ingresoId':ingresoId, 'sede':sede},
		success: function (Usuarios) {

 // alert("llegue diagMedico = " + Usuarios.diagMedico);
 // alert("llegue medicoIngreso = " + Usuarios.medicoIngreso);


			  var options = '<option value="=================="></option>';


                          const $id1 = document.querySelector("#tipoDoc");
	     		  $("#tipoDoc").empty();

	                 $.each(Usuarios['TipoDoc'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id1.appendChild(option);
 	      		      });

		            $('#tipoDoc').val(Usuarios.tipoDoc);
       			    $('#busDocumentoSel').val(Usuarios.documento);
       			  $('#paciente').val(Usuarios.paciente);
       			      			    $('#empresaE').val(Usuarios.empresa);
      			    $('#busServicio2').val(Usuarios.servicioNombreIng);
      			    $('#busSubServicio2').val(Usuarios.subServicioNombreIng);



   			    $('#dependenciasIngreso').val(Usuarios.dependenciasIngreso);
    			    $('#busEspecialidadP').val(Usuarios.espMedico);

    			    $('#dxIngresoPX').val(Usuarios.dxIngreso);
    			    $('#viasIngresoP').val(Usuarios.viasIngreso);
    			    $('#causasExternaP').val(Usuarios.causasExterna);
    			    $('#regimenesP').val(Usuarios.regimenes);
    			    $('#tiposCotizanteP').val(Usuarios.cotizante);
    			    $('#remitidoP').val(Usuarios.remitido);
    			    $('#numManillaP').val(Usuarios.numManilla);

    			    $('#medicoIngresoPPX').val(Usuarios.medicoIngreso); 	

    			    $('#responsablesP').val(Usuarios.responsable); 	
    			    $('#acompanantesP').val(Usuarios.acompanante); 	
			$('#ipsP').val(Usuarios.ips); 	


  		  $('#tiposCotizanteP').val(Usuarios.cotizante);
  		  $('#ripsCausaMotivoAtencionX').val(Usuarios.ripsCausaMotivoAtencion);
  		  $('#ripsGrupoServiciosX').val(Usuarios.ripsGrupoServicios);
  		  $('#ripsmodalidadGrupoServicioTecSalX').val(Usuarios.ripsmodalidadGrupoServicioTecSal);
  		  $('#ripsmodalidadGrupoServicioTecSalX').val(Usuarios.ripsmodalidadGrupoServicioTecSal);
  		  $('#ripsCondicionDestinoUsuarioEgresoX').val(Usuarios.ripsCondicionDestinoUsuarioEgreso);
  		  $('#ripsViaIngresoServicioSaludX').val(Usuarios.ripsViaIngresoServicioSalud);
  		  $('#ripsDestinoUsuarioEgresoRecienNacidoX').val(Usuarios.ripsDestinoUsuarioEgresoRecienNacidoX);
		  $('#ripsServiciosIngX').val(Usuarios.ripsServiciosIng);



  		   $('#modalActualizaAdmision').modal('show');	

    		



                    },
	   		    error: function (data) {
		       
	document.getElementById("mensajesError").value = data.responseText;
	   	    	}
	});


});

$('.eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal Usuarios");
			 // alert("Entre carga MODAL");

			$.get(href, function(Usuarios,status)
			 {
			 //  alert("entre DATOS MODAL y el nombre es = ");


                $('#tipoDoc').val(Usuarios.tipoDoc_id);
				$('#documento').val(Usuarios.documento);

				 // alert(Usuarios.nombre);

				$('#nombre').val(Usuarios.nombre);
				$('#genero').val(Usuarios.genero);
				$('#direccion').val(Usuarios.direccion);
				$('#telefono').val(Usuarios.telefono);
				$('#contacto').val(Usuarios.contacto);
				$('#centrosc').val(Usuarios.centrosc_id);
				$('#tiposUsuario').val(Usuarios.tiposUsuario_id);

				});

			 $('#usuariosModal').modal({show:true});

			  });




$(document).on('change', '#pais', function(event) {

       var Pais =   $(this).val()
	 // alert("entre Pais");


        $.ajax({
	           url: '/buscarPaises/',
	            data : {Pais:Pais},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id78 = document.querySelector("#departamentos");


 	      		     $("#departamentos").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id78.appendChild(option);
 	      		      });


                    },
	   		    error: function (data) {
	

	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });

});


$(document).on('change', '#departamentos', function(event) {




       var Departamento =   $(this).val()


        $.ajax({
	           url: '/buscarCiudades/',
	            data : {Departamento:Departamento},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id7 = document.querySelector("#ciudades");


 	      		     $("#ciudades").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id7.appendChild(option);
 	      		      });





                    },
	   		    error: function (data) {
		

	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}

	     });

// AJAX DE MUNICIPIOS



$.ajax({
	           url: '/buscarMunicipios/',
	            data : {Departamento:Departamento},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {
			 // alert("regrese de buscar municipios " + respuesta );

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id3 = document.querySelector("#municipios");


 	      		     $("#municipios").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });





                    },
	   		    error: function (data) {
      		

	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });

// aclara las localidades

     $("#localidades").empty();

});





$(document).on('change', '#departamentosViejo', function(event) {

        //  alert("Entre cambio Departamento");


       var Departamento =   $(this).val()

       //  alert("Departamento = " + Departamento);

        $.ajax({
	           url: '/buscarCiudades/',
	            data : {Departamento:Departamento},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#ciudades");


 	      		     $("#ciudades").empty();

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });


                    },
	   		    error: function (data) {
		      

	   			  	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });
});






$(document).on('change', '#busEspecialidad', function(event) {

        //  alert("Entre cambio especialdiad");


       var Esp =   $(this).val()

	 // alert("especialidad Nro = " + Esp);


        var Sede =  document.getElementById("Sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];
	 // alert("Sede = " + Sede);



        $.ajax({
	           url: '/buscarEspecialidadesMedicos',
	            data : {Esp:Esp, Sede:Sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#medicoIngresoPP");


 	      		     $("#medicoIngresoPP").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
	   		    error: function (data) {


	   			 	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });
});



$(document).on('change', '#busEspecialidadP', function(event) {

        //  alert("Entre cambio busEspecialidadP");


       var Esp =   $(this).val()

	 // alert("especialidad Nro = " + Esp);


        var Sede =  document.getElementById("Sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];
	 // alert("Sede = " + Sede);



        $.ajax({
	           url: '/buscarEspecialidadesMedicos',
	            data : {Esp:Esp, Sede:Sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#medicoIngresoPPX");


 	      		     $("#medicoIngresoPPX").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });


                    },
	   		    error: function (data) {


	   			 	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });
});





$(document).on('change', '#tiposAntecedente', function(event) {


       var select = document.getElementById("tiposAntecedente"); /*Obtener el SELECT */
       var TiposAntecedente = select.options[select .selectedIndex].value; /* Obtener el valor */
     //  var Antecedentes =   $(this).val()

       // var Sede =  document.getElementById("Sede").value;
       //  alert("Entre Tipos Antecedente");

        $.ajax({
	           url: '/buscarAntecedentes',
	            data : {TiposAntecedente:TiposAntecedente},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#antecedentes");


      		     $("#antecedentes").empty();

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
		 error: function (data) {
    

				document.getElementById("mensajesError").value =  data.responseText;

	   	    	}            
	     });
});




$(document).on('change', '#busServicio', function(event) {



       var Serv =   $(this).val()

        var Sede =  document.getElementById("Sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];



        $.ajax({
	           url: '/buscarSubServicios',
	            data : {Serv:Serv, Sede:Sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#busSubServicio");


 	      		     $("#busSubServicio").empty();

				 // alert("voy a llenar subservicio");
	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

							 // alert("ya llene subservicio");



                    },
	   		    error: function (data) {
      
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });
});


$(document).on('change', '#busServicioT', function(event) {



       var Serv =   $(this).val()

      //   alert("Entre para llamar a buscarServiciosTriage : " + Serv)

        var Sede =  document.getElementById("Sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];



        $.ajax({
	           url: '/buscarSubServiciosTriage',
	            data : {Serv:Serv, Sede:Sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#busSubServicioT");


 	      		     $("#busSubServicioT").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
	   		    error: function (data) {

	   			    	document.getElementById("value").value =  data.responseText;

	   	    	}

	     });
});



$(document).on('change', '#busSubServicio', function(event) {


       var select = document.getElementById("busSubServicio"); /*Obtener el SELECT */
       var serv = select.options[select.selectedIndex].value; /* Obtener el valor */
       var subServ =   $(this).val()

        var sede =  document.getElementById("sede").value;
        //  alert("voy a enviar este servicio parea la busqueda de habitaciones  = " + serv);


        $.ajax({
	           url: '/buscarHabitaciones',
	            data : {serv:serv, sede:sede, subServ:subServ, Exc:'N'},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);

                     const $id2 = document.querySelector("#busHabitacion");
 	      		     $("#busHabitacion").empty();

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
	   		    error: function (data) {

	document.getElementById("mensajesError").value =  data.JsonResponse.errodata.responseText;

	   	    	}

	     });
});



$(document).on('change', '#busSubServicioT', function(event) {

        //  alert("Entre a busSubServicioT");

        var select = document.getElementById("busServicioT"); /*Obtener el SELECT */
        // var Serv = select.options[select.selectedIndex].value; /* Obtener el valor */
       // var Serv = document.getElementById("busServicioT").value;

	var Serv = $("#busSubServicioT").val();



       //   alert("Entre para llamar a buscar Nuevo ServiciosTriage : " + Serv);

        var SubServ =   $(this).val()

        var Sede =  document.getElementById("Sede").value;


       //   alert("Entre para llamar a buscar SubServiciosTriage : " + SubServ);
      //    alert("Entre para llamar a buscar Sede : " + Sede);

        $.ajax({
	           url: '/buscarHabitacionesTriage',
	            data : {Serv:Serv, Sede:Sede, SubServ:SubServ, Exc:'S'},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  	 // 	alert("Me devuelvo pos satisfactorio habitaciones");


	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);

                     const $id2 = document.querySelector("#dependenciasT");

 	      		     $("#dependenciasT").empty();

                  //    alert("ya borre ahora a escribir depedencias" + dato);

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
	   		    error: function (data) {


	   				document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });
});







$(document).on('change', '#busServicio22', function(event) {



       var serv =   $(this).val()
	alert("codigo del servivio a buscar VERIFICAR" + serv);


        var sede =  document.getElementById("Sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];



        $.ajax({
	           url: '/buscarSubServicios',
	            data : {serv:serv, sede:sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {
				// alert("DE REGRESO");


	  		   var options = '<option value="=================="></option>';
	  		  var dato = JSON.parse(respuesta);
		//	alert("esto devuelve = " + dato);

                     const $id21 = document.querySelector("#busSubServicio22");
 	      		     $("#busSubServicio22").empty();

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id21.appendChild(option);
 	      		      });





                    },
	   		    error: function (data) {
     

	   			  	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });
});


$(document).on('change', '#busSubServicio22', function(event) {

        alert("Entre a cambiar el subservicio");

       var select = document.getElementById("busServicio22"); /*Obtener el SELECT */
       var serv = select.options[select.selectedIndex].value; /* Obtener el valor */
       var subServ =   $(this).val()

        var sede =  document.getElementById("sede").value;


        $.ajax({
	           url: '/buscarHabitaciones',
	            data : {serv:serv, sede:sede, subServ:subServ, Exc:'S'},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#dependenciasIngreso22");


 	      		     $("#dependenciasIngreso22").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });





                    },
	   		    error: function (data) {
   

	   			document.getElementById("mensajesError").value =  data.responseText;

	   	    	}

	     });
});






// Para la ventana Moddal

 $('.eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			console.log("Entre Ventana Modal");

			$.get(href, function(UsuariosHc,status)
			 {
			 //  alert("entre");


                $('#username').val(UsuariosHc.username);
				$('#password').val(UsuariosHc.password);

				}
			);

			 $('#exampleModal').modal({show:true});

			  });




// FUnciones para Modales



function abrir_modal(url)
        {
            //  alert ("Entre NModal_0000000000000000000000000001");
            $('#modalActualizaAdmision').load(url, function()
            {
            //  alert ("Entre NModal_001");
            $(this).modal({

                backdrop: 'static',
                keyboard: false
            })
            //  alert ("Entre NModal_003");

            $('#tipoDoc').val("1");
	    	$('#documento').val("33333333333333333333");



            $(this).modal('show');
            });
            return false;
        }

function cerrar_modal()
        {
      
        $('#modalActualizaAdmision').modal('hide');
return false;
        }


function findOneAdmision(tipoDoc,Documento,consec, sede)
{

	var envios = new FormData();


	//var select = document.getElementById("tipoDoc");
    //var tipoDoc = select.options[select.selectedIndex].value;
	//var documento = document.getElementById("busDocumentoSel").value;


    //  alert("Envio a la MOdal documento = " + documento);

	$.ajax({
		type: 'POST',
    	url: '/encuentraAdmisionModal/',
		data: {'tipoDoc':tipoDoc,'documento':documento,'consec':consec, 'sede':sede},
		success: function (Usuarios) {

			 //  alert("entre DATOS MODAL de admision y el nombre es = " + Usuarios.tipoDoc + " " +  Usuarios.documento);

	           		
				$('#documento').val(Usuarios.documento);
				$('#busServicio2').val(Usuarios.servicioNombreIng);
				$('#busSubServicio2').val(Usuarios.busSubServicio2);
				$('#dependenciasIngreso').val(Usuarios.dependenciasIngreso);
				$('#tipoDoc').val(Usuarios.tipoDoc);
				$('#viasIngreso').val(Usuarios.viasIngreso);
				$('#causasExterna').val(Usuarios.causasExterna);
				$('#regimenes').val(Usuarios.regimenes);
				$('#cotizante').val(Usuarios.cotizante);
				$('#remitido').val(Usuarios.remitido);
				$('#ips').val(Usuarios.ips);

				$('#numManilla').val(Usuarios.numManilla);
				$('#dxIngresoPX').val(Usuarios.dxIngreso);
				$('#paciente').val(Usuarios.paciente);
				$('#ingreso').val(Usuarios.ingreso);
				$('#salida').val(Usuarios.salida);
				$('#medicoIngresoPPX').val(Usuarios.medicoIngreso);
				$('#espMedico').val(Usuarios.espMedico);
				$('#diagMedico').val(Usuarios.diagMedico);


				 $('#modalActualizaAdmision').modal({show:true});
         //  alert("data = " + JSON.stringify(data)); // data
		         //    alert(data.status); // the status code   
		           //  alert(data.JsonResponse['error']); // the message
                    },
	   		    error: function (data) {
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	});
};




function guardaCambioServicio()
{

	
	var tipoDocx = document.getElementById("tipoDocx").value;
	var documentox = document.getElementById("documentox").value;
	var pacientex = document.getElementById("pacientex").value;
	var consecx = document.getElementById("consecx").value;
	var sede= document.getElementById("sede").value;

	var fechaOcupacion = document.getElementById("fechaOcupacion").value;
    var servicioActual = document.getElementById("servicioActual").value;
    var subServicioActual = document.getElementById("subServicioActual").value;
    var dependenciaActual = document.getElementById("dependenciaActual").value;

	var select = document.getElementById("servicioCambio");
    var servicioCambio = select.options[select.selectedIndex].value;
 // alert("servicio cambio = " +  servicioCambio);

	var select = document.getElementById("subServicioCambio");
    var subServicioCambio = select.options[select.selectedIndex].value;
	var select = document.getElementById("dependenciaCambio");
    var dependenciaCambio = select.options[select.selectedIndex].value;


	var username = document.getElementById("username").value;
	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	var numReporte = document.getElementById("numreporte").value;
	var grupo = document.getElementById("grupo").value;
	var subGrupo = document.getElementById("subGrupo").value;
	var sede = document.getElementById("sede").value;
	var documento = document.getElementById("documento").value;
	var nombreSede = document.getElementById("nombreSede").value;
	var profesional = document.getElementById("profesional").value;
	var permisosGrales = document.getElementById("permisosGrales").value;
	var escogeModulo = document.getElementById("escogeModulo").value;
	var username_id = document.getElementById("username_id").value;
	var permisosDetalle = document.getElementById("permisosDetalle").value;

	
    //  alert("Envio:  " + documentox);

	$.ajax({
		type: 'POST',
    		url: '/guardaCambioServicio/',
		data: {'tipoDocx':tipoDocx,
			'documentox':documentox,
			'consecx':consecx,
             'pacientex':pacientex,
			 'sede':sede,
			 'fechaOcupacion':fechaOcupacion,
			 'servicioActual':servicioActual,
			 'subServicioActual':subServicioActual,
			 'dependenciaActual':dependenciaActual,
			 'servicioCambio':servicioCambio,
			 'subServicioCambio':subServicioCambio,
			 'dependenciaCambio':dependenciaCambio,
			 'username':username,
			 'sedeSeleccionada':sedeSeleccionada,
			 'numReporte':numReporte,
			 'grupo':grupo,
 			 'subGrupo':subGrupo,
             'nombreSede':nombreSede,
			 'profesional':profesional,
			 'permisosGrales':permisosGrales,
			 'escogeModulo':escogeModulo,
			 'username_id':username_id,
			 'permisosDetalle':permisosDetalle},

		success: function (CambioServicio) {

			if (CambioServicio.success == true)
				{
			$('#mensajes').val(CambioServicio.Mensaje);
				}
		

			 //  alert("DE REGRESO CON CambioServicio = " + CambioServicio);
			 //  alert("DE REGRESO CON CambioServicio Doc = " + CambioServicio.Documentox);
			 //  alert("FECHA OCUPACION = " + CambioServicio.FechaOcupacion);

	                       $('#tipoDocx').val(CambioServicio.TipoDocx);
				$('#documentoc').val(CambioServicio.Documentox);
				$('#pacientex').val(CambioServicio.Pacientex);
				$('#servicioActual').val(CambioServicio.ServicioActual);
				$('#subServicioActual').val(CambioServicio.SubServicioActual);
				$('#dependenciaActual').val(CambioServicio.DependenciaActual);
				$('#fechaOcupacion').val(CambioServicio.FechaOcupacion);
		
	  		  var options = '<option value="=================="></option>';
                          const $id2 = document.querySelector("#servicioCambio");
	     		  $("#servicioCambio").empty();

	                 $.each(CambioServicio['Servicios'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

			  var options = '<option value="=================="></option>';	  	
                          const $id3 = document.querySelector("#subServicioCambio");
	     		  $("#subServicioCambio").empty();

	                 $.each(CambioServicio['SubServicios'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });

			  var options = '<option value="=================="></option>';	  	
                          const $id4 = document.querySelector("#dependenciaCambio");
	     		  $("#dependenciaCambio").empty();

	                 $.each(CambioServicio['Habitaciones'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id4.appendChild(option);
 	      		      });
			
					
                     document.getElementById("mensajes").innerText=CambioServicio.Mensaje;
var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;


    	var ingresoId = document.getElementById("ingresoId1").value;

         var data =  {}   ;
         data['username'] = username;
         data['sedeSeleccionada'] = sedeSeleccionada;
         data['nombreSede'] = nombreSede;
         data['sede'] = sede;
         data['username_id'] = username_id;
	 data['ingresoId'] = ingresoId;
	 data = JSON.stringify(data);
	

         arrancaAdmisiones(5,data);
         dataTableCensoInitialized = true;

         arrancaAdmisiones(6,data);
	 dataTableHabitacionesInitialized = true;




                    },
		 error: function (data) {
  

				document.getElementById("mensajesError").value =  data.responseText;

	   	    	}            
	});
};



const article = document.querySelector('article');
// Print the selected target
article.addEventListener('click', event => {
    // alert("click en article" + event.target);
});



 function tableActions() {
   var table = initTableConvenios();
   var tableA = initTableAbonos();

    // perform API operations with `table`
    // ...
}

$(document).on('click', '#Convenios', function(event) {
  // alert("pique en article Convenios");
});

        /*------------------------------------------
        --------------------------------------------
        Create Post Code Crea Responsable
        --------------------------------------------
        --------------------------------------------*/
        $('#guardaResponsable1').click(function (e) {
            e.preventDefault();
            $(this).html('Sending..');

	     // var ingresoId = $('input[name="ingresoId"]:checked').val();
	      var ingresoId = document.getElementById("ingresoId1").value;
	       // alert("ingreso = " + ingresoId);

	     var selectx = document.getElementById("responsablesC");
              var responsable = selectx.options[selectx.selectedIndex].value;

            $.ajax({
                data: {'ingresoId':ingresoId,'responsable':responsable},
        	  url: "/guardarResponsableAdmision/",
                type: "POST",
                dataType: 'json',
                success: function (data) {

			if (data.success == true)
			 {
			  $("#mensajes").html(data.Mensaje);
			 }


                },
		 error: function (data) {


				document.getElementById("mensajesError").valueL =  data.responseText;

	   	    	}            
});
        });



        /*------------------------------------------
        --------------------------------------------
        Create Post Code Crea Acompanante
        --------------------------------------------
        --------------------------------------------*/
        $('#guardaAcompanante1').click(function (e) {
            e.preventDefault();
            $(this).html('Sending..');

      var ingresoId = document.getElementById("ingresoId1").value;
	      //  alert("ingreso = " + ingresoId);


	     var selectx = document.getElementById("acompananteC");
              var acompanante = selectx.options[selectx.selectedIndex].value;

            $.ajax({
                data: {'ingresoId':ingresoId,'acompanante':acompanante},
        	  url: "/guardarAcompananteAdmision/",
                type: "POST",
                dataType: 'json',
                success: function (data) {
			if (data.success == true)
				{
					  $("#mensajes").html(data.Mensaje);
				}

                },
		 error: function (data) {



				document.getElementById("mensajesError").value = data.responseText;

	   	    	}

            });
        });


$(document).on('click', '#Furips', function(event) {

	 // alert("Entre FURIPS");


  var sede = document.getElementById("sede").value; 
//  var valor = document.getElementById("ingresoIdF").value;
var valor = $('input[name="ingresoId"]:checked').val();
	var numeroRadicacion = document.getElementById("numeroRadicacion").value; 
	var numeroFactura = document.getElementById("numeroFactura").value;
	var primerNombreVictima = document.getElementById("primerNombreVictima").value;
	var primerApellidoVictima = document.getElementById("primerApellidoVictima").value;
	var fechaRadicado  = document.getElementById("fechaRadicado").value; 


	 // alert("La fila selecionada es el id = " + valor);
	 // alert("numeroradicacion = " + numeroRadicacion);


     
	$.ajax({
		type: 'POST',
    	url: '/guardaFurips/',
		data: {'sede':sede,
			'ingresoId':valor,
			'numeroRadicacion':numeroRadicacion,
			'numeroFactura':numeroFactura,
			'primerNombreVictima':primerNombreVictima,
			'primerApellidoVictima':primerApellidoVictima,
			'fechaRadicado':fechaRadicado
			},

		dataType : 'json',
		success: function (furips) {

                  //  alert("llegue Guarda FURIPS = " + furips);

		 $('#convConsecA').val(cambioServicio['Usuarios'].consec);
		 $('#responsablesC').val(cambioServicio['Usuarios'].responsable);
		  $('#acompananteC').val(cambioServicio['Usuarios'].acompanante);
		 $("#mensajes").html(" !  Registro Actualizado !");

                    },
			 error: function (data) {


				document.getElementById("mensajesError").value =  data.responseText;

	   	    	}	});

           // Fin FURPS


})

function actualizaAdmision()
{



	var empresa = document.getElementById("empresaE").value;
	var busEspecialidad = document.getElementById("busEspecialidadP").value;
	var medicoIngreso = document.getElementById("medicoIngresoPPX").value;
	var sede= document.getElementById("sede").value;

	var viasIngreso = document.getElementById("viasIngresoP").value;
    var causasExterna = document.getElementById("causasExternaP").value;
    var regimenes = document.getElementById("regimenesP").value;
    var tiposCotizante = document.getElementById("tiposCotizanteP").value;
    var acompanantes = document.getElementById("acompanantesP").value;
    var dxIngreso = document.getElementById("dxIngresoPX").value;
    var responsables = document.getElementById("responsablesP").value;
    var remitido = document.getElementById("remitidoP").value;
    var ips = document.getElementById("ipsP").value;
    var numManilla = document.getElementById("numManillaP").value;
    var ingresoId = document.getElementById("ingresoIdActualizar").value;
	


	var username = document.getElementById("username").value;
	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	var numReporte = document.getElementById("numreporte").value;
	var grupo = document.getElementById("grupo").value;
	var subGrupo = document.getElementById("subGrupo").value;
	var sede = document.getElementById("sede").value;
	var documento = document.getElementById("documento").value;
	var nombreSede = document.getElementById("nombreSede").value;
	var profesional = document.getElementById("profesional").value;
	var permisosGrales = document.getElementById("permisosGrales").value;
	var escogeModulo = document.getElementById("escogeModulo").value;
	var username_id = document.getElementById("username_id").value;
	var permisosDetalle = document.getElementById("permisosDetalle").value;

	// RIPS

	var ripsDestinoUsuarioEgresoRecienNacido = document.getElementById("ripsDestinoUsuarioEgresoRecienNacidoX").value;
	var ripsEdadGestacional = document.getElementById("ripsEdadGestacionalX").value;
	var ripsNumConsultasCPrenatal = document.getElementById("ripsNumConsultasCPrenatalX").value;
	var ripsPesoRecienNacido = document.getElementById("ripsPesoRecienNacidoX").value;
	var ripsRecienNacido = document.getElementById("ripsRecienNacidoX").value;
	var ripsCausaMotivoAtencion = document.getElementById("ripsCausaMotivoAtencionX").value;
	var ripsCondicionDestinoUsuarioEgreso = document.getElementById("ripsCondicionDestinoUsuarioEgresoX").value;
	var ripsGrupoServicios = document.getElementById("ripsGrupoServiciosX").value;
	var ripsViaIngresoServicioSalud = document.getElementById("ripsViaIngresoServicioSaludX").value;
	var ripsmodalidadGrupoServicioTecSal = document.getElementById("ripsmodalidadGrupoServicioTecSalX").value;
	var ripsFinalidadConsulta = document.getElementById("ripsFinalidadConsultaX").value;
	var ripsServiciosIng = document.getElementById("ripsServiciosIng").value;


	$.ajax({
		type: 'POST',
    		url: '/actualizaAdmision/',
		data: {'ingresoId':ingresoId,
			'numManilla':numManilla,
			'ips':ips,
             'remitido':remitido,
			 'sede':sede,
			 'responsables':responsables,
			 'acompanantes':acompanantes,
			 'responsables':responsables,
			 'tiposCotizante':tiposCotizante,
			 'causasExterna':causasExterna,
			 'regimenes':regimenes,
			 'viasIngreso':viasIngreso,
			 'dxIngreso':dxIngreso,
			 'medicoIngreso':medicoIngreso,
			 'busEspecialidad':busEspecialidad,
			 'empresa':empresa,
			 'username':username,
			 'sedeSeleccionada':sedeSeleccionada,
			 'numReporte':numReporte,
			 'grupo':grupo,
 			 'subGrupo':subGrupo,
		         'nombreSede':nombreSede,
			 'profesional':profesional,
			 'permisosGrales':permisosGrales,
			 'escogeModulo':escogeModulo,
			 'username_id':username_id,
			 'permisosDetalle':permisosDetalle,
			 'ripsDestinoUsuarioEgresoRecienNacido':ripsDestinoUsuarioEgresoRecienNacido,
			 'ripsEdadGestacional':ripsEdadGestacional,
			 'ripsNumConsultasCPrenatal':ripsNumConsultasCPrenatal,
			 'ripsPesoRecienNacido':ripsPesoRecienNacido,
			 'ripsRecienNacido':ripsRecienNacido,
			 'ripsCausaMotivoAtencion':ripsCausaMotivoAtencion,
			 'ripsCondicionDestinoUsuarioEgreso':ripsCondicionDestinoUsuarioEgreso,
			 'ripsGrupoServicios':ripsGrupoServicios,
			 'ripsViaIngresoServicioSalud':ripsViaIngresoServicioSalud,
			 'ripsmodalidadGrupoServicioTecSal':ripsmodalidadGrupoServicioTecSal,
			 'ripsFinalidadConsulta':ripsFinalidadConsulta,
			 'ripsServiciosIng':ripsServiciosIng},


		success: function (data2) {

                     document.getElementById("mensajes").innerText=data2.Mensaje;

			 $('#modalActualizaAdmision').modal('hide');
		      var data =  {}   ;
     			   var sede = document.getElementById("sede").value;   
       			    data['sede'] = sede;


		           data = JSON.stringify(data);

	       arrancaAdmisiones(1,data);
	    dataTableAdmisionesInitialized = true;

                    },
		 error: function (data) {
     
					document.getElementById("mensajesError").value =  data.responseText;


	   	    	}            
	});
};

function CrearAdm()
{

	 // alert("CrearAdmisionDef a poner foco");
			 document.getElementById('empresaC').focus();

	};




$('#tablaDatos tbody').on('click', '.ImprimirHojaAdmision', function() {

	 // alert ("Entre ImprimirHojaAdmision ");

	     var post_id = $(this).data('pk');
	 // alert ("post_id = " + post_id);
	var ingresoId = post_id;


$.ajax({
    url: '/imprimirHojaAdmision/',
  data : {ingresoId:ingresoId},



    method: 'POST',
    xhrFields: {
        responseType: 'blob' // Importante: interpreta la respuesta como binario
    },
    success: function (data) {


        var blob = new Blob([data], { type: 'application/pdf' });
        var link = window.URL.createObjectURL(blob);
        window.open(link, '_blank'); // Abre el PDF en nueva pestaña [11]
    },
    error: function (error) {
      document.getElementById("mensajesError").value =  data.responseText
    }
});


    });

$('#tablaDatos tbody').on('click', '.ImprimirManilla', function() {

	 // alert ("Entre ImprimirManilla ");

	     var post_id = $(this).data('pk');
	 // alert ("post_id = " + post_id);
	var ingresoId = post_id;

$.ajax({
    url: '/imprimirManillaAdmision/',
 data : {ingresoId:ingresoId},
    method: 'POST',
    xhrFields: {
        responseType: 'blob' // Importante: interpreta la respuesta como binario
    },
    success: function (data) {
	// alert("de regreso");

        var blob = new Blob([data], { type: 'application/pdf' });
        var link = window.URL.createObjectURL(blob);
        window.open(link, '_blank'); // Abre el PDF en nueva pestaña [11]
    },
    error: function (error) {
      document.getElementById("mensajesError").value =  data.responseText
    }
});
    });




$('#tablaDatos tbody').on('click', '.ImprimirAtencionInicialUrgencias', function() {

	 // alert ("Entre ImprimirAtencionInicialUrgencias ");

	     var post_id = $(this).data('pk');
	 // alert ("post_id = " + post_id);
	var ingresoId = post_id;

$.ajax({
    url: '/imprimirAtencionUrgencias/',
 data : {ingresoId:ingresoId},
    method: 'POST',
    xhrFields: {
        responseType: 'blob' // Importante: interpreta la respuesta como binario
    },
    success: function (data) {


        var blob = new Blob([data], { type: 'application/pdf' });
        var link = window.URL.createObjectURL(blob);
        window.open(link, '_blank'); // Abre el PDF en nueva pestaña [11]
    },
    error: function (error) {
      document.getElementById("mensajesError").value =  data.responseText
    }
});

    });

$(document).on('change', '#municipios', function(event) {



       var Municipio =   $(this).val()





        $.ajax({
	           url: '/buscarLocalidades/',
	            data : {Municipio:Municipio},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id7 = document.querySelector("#localidades");


 	      		     $("#localidades").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id7.appendChild(option);
 	      		      });





                    },
	   		    error: function (data) {
    

	document.getElementById("mensajesError").value = data.responseText;

	   	    	}

	     });
     });


    $('body').on('click', '.ImprimirAutorizacion', function () {

	          var post_id = $(this).data('pk');
		var row = $(this).closest('tr'); // Encuentra la fila

		 //  alert("ImprimirAutorizacion desd admisiones = " + post_id);

	var autorizacionId = post_id;

$.ajax({
    url: '/imprimirAutorizacionesAdm/',
 data : {autorizacionId:autorizacionId},
    method: 'POST',
    xhrFields: {
        responseType: 'blob' // Importante: interpreta la respuesta como binario
    },
    success: function (data) {
        var blob = new Blob([data], { type: 'application/pdf' });
        var link = window.URL.createObjectURL(blob);
        window.open(link, '_blank'); // Abre el PDF en nueva pestaña [11]
    },
    error: function (error) {
      document.getElementById("mensajesError").value =  data.responseText
    }
});
        });

$(document).on('change', '#empresaC', function(event) {

       var select = document.getElementById("empresaC"); /*Obtener el SELECT */
       var empresaId  = select.options[select.selectedIndex].value; /* Obtener el valor */

	 // alert("Entre para llamar a buscarConvenios de Empresa : " + empresaId)

        $.ajax({
	           url: '/buscarConvenioEmpresa',
	            data : {empresaId:empresaId},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#conveniosC");


 	      		     $("#conveniosC").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });
                    },
                    error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}

	     });
});



function marcarRegistroInicial()
{
$('#tablaDatos tbody tr:eq(0) input[type="radio"]').prop('checked', true);
  $('input[name="ingresoId"]').prop('checked', true);
}


function ActivarFurips()
        {
             // alert ("Entre Activar furips");
 $('#modalFurips').modal('show');

        }

function RefrescarPantalla() {

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
        arrancaAdmisiones(1,data);
	dataTableAdmisionesInitialized = true;


	$.ajax({url:'/indicadores/',
			data: {'Sede':sede},
			type: 'POST',
			dataType: 'json',
	  			success: function (respuesta) {
					// alert("indicadores = " + JSON.stringify(respuesta));

					if (respuesta.nombre == 'HOSPITALIZACION')
					{
					document.getElementById("hosp").innerHTML = respuesta.total;
					}

					if (respuesta.nombre == 'TRIAGE')
					{
					document.getElementById("tria").innerHTML = respuesta.total;
					}

					if (respuesta.nombre == 'URGENCIAS')
					{
					document.getElementById("urg").innerHTML = respuesta.total;
					}

					if (respuesta.nombre == 'AMBULATORIO')
					{
					document.getElementById("amb").innerHTML = respuesta.total;
					}
                    },
	   		    error: function (data) {   		
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
	     });



}

