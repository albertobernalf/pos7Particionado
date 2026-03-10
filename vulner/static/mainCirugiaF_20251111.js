console.log('Hola Alberto Hi!')

let dataTable;
let dataTableB;
let dataTableC;
let dataTableD;
let dataTableF;
let dataTableG;
let dataTableH;
let dataTableI;

let dataTableProgramacionCirugiaInitialized = false;
let dataTableSalasCirugiaInitialized = false;
let dataTableSolicitudCirugiaInitialized = false;
let dataTableIngresosCirugiaInitialized = false;
let dataTableDisponibilidadSalaInitialized = false;
let dataTableProcedimientosCirugiaInitialized = false;
let dataTableParticipantesCirugiaInitialized = false;
let dataTableMaterialCirugiaInitialized = false;
let dataTableMaterialInformeCirugiaInitialized = false;
let dataTableProcedimientosInformeCirugiaInitialized = false;
let dataTableParticipantesInformeCirugiaInitialized = false;
let dataTableParticipantesInformeXXCirugiaInitialized = false;
let dataTableMaterialInformeXXCirugiaInitialized = false;

let dataTableHojaDeGastoCirugiaInitialized = false;
let dataTableHojaDeGastoXXCirugiaInitialized = false;


$(document).ready(function() {

	 var $searchInput = $('#ParticipantesInformeCirugia_filter input'); // Reemplaza 'dataTable_filter' con el ID del contenedor de búsqueda

    // Modificar el atributo placeholder
    $searchInput.attr('placeholder', 'Buscar...');



    var table = $('#tablaProgramacionCirugia').DataTable();
    
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


function arrancaCirugia(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsSalasCirugia  ={
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
            scrollY: '475px',
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
                 url:"/load_dataSalasCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <input type='radio' name='miProgramacionCirugia' class='miProgCirugia form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	     btn = btn + " <button class='miEditaProgramacionCirugia btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";


                       return btn;
                    },

	},

                { data: "fields.id"},
                { data: "fields.numero"},
		   { data: "fields.nombre"}, 
                { data: "fields.ubicacion"},
                { data: "fields.servicio"},
                { data: "fields.estado"},
                        ]
            }
	        
		   dataTable = $('#tablaSalasCirugia').DataTable(dataTableOptionsSalasCirugia);


  }

    if (valorTabla == 2)
    {
        let dataTableOptionsProgramacionCirugia  ={
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
            scrollY: '475px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
		{  
                    "targets": 17
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
                 url:"/load_dataProgramacionCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miProgramacionCirugia' class='miProgramacionCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
                    },

	},

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	     btn = btn + " <button class='miEditaProgramacionCirugia btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: green;'  data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";


                       return btn;
                    },

	},



                { data: "fields.id"},
            //    { data: "fields.tipoDoc_id"},
{
			target: 1,
			visible: false
		},
	{
			target: 2,
			visible: false
		},

		  // { data: "fields.tipoNota"}, 
		   { data: "fields.abrev"}, 
                { data: "fields.documento"},
                { data: "fields.paciente"},
          
                { data: "fields.numero"},
                { data: "fields.sala"},
                { data: "fields.cirugias"},

                { data: "fields.inicia"},
		{ data: "fields.horaInicia"},
                { data: "fields.Termina"},
		 { data: "fields.horaTermina"},
		{
		  "render": function ( data, type, row ) {
                	        var btn = '';

		     btn = btn + " <button class='miEditaEstadoProgramacionCirugia btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
		},

     		 { data: "fields.estadoProg"},
		{
		  "render": function ( data, type, row ) {
                	        var btn = '';

		     btn = btn + " <button class='miEditaEstadoCirugia btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
		},

     		 { data: "fields.estadoCirugia"},
                        ]
            }

		dataTable = $('#tablaProgramacionCirugia').DataTable(dataTableOptionsProgramacionCirugia);

  }


    if (valorTabla == 3)
    {
        let dataTableOptionsSolicitudCirugia  ={
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
                    "targets": 30
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
                 url:"/load_dataSolicitudCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miSolicitudCirugia' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miSolicitudCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	     btn = btn + " <button class='miAdicionarProcedimientos btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: green;' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },

	},

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	     btn = btn + " <button class='miAdicionarParticipantes btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: green;' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";


                       return btn;
                    },

	},
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	     btn = btn + " <button class='miAdicionarMaterial btn-primary ' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: green;'  data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";


                       return btn;
                    },

	},
		{ data: "fields.id"},
		{ data: "fields.sede"},
                { data: "fields.cirugia"},
                { data: "fields.tipoDoc"},
                { data: "fields.documento"},
                { data: "fields.paciente"},
                { data: "fields.nacimiento"},
                { data: "fields.genero"},
                { data: "fields.edad"},
                { data: "fields.ingreso"},
                //{ data: "fields.solicita"},
{
			target: 10,
			visible: false
		},
                { data: "fields.cama"},
                { data: "fields.empresa"},
                //{ data: "fields.telefono"},
{
			target: 13,
			visible: false
		},

               // { data: "fields.solicitaSangre"},
{
			target: 14,
			visible: false
		},

 //               { data: "fields.describeSangre"},
{
			target: 15,
			visible: false
		},

               // { data: "fields.cantidadSangre"},
{
			target: 16,
			visible: false
		},

                { data: "fields.solicitaCamaUci"},
                // { data: "fields.solicitaMicroscopio"},
{
			target: 18,
			visible: false
		},

                // { data: "fields.solicitaRx"},
{
			target: 19,
			visible: false
		},

               // { data: "fields.solicitaAutoSutura"},
{
			target: 20,
			visible: false
		},

                // { data: "fields.solicitaOsteosintesis"},
{
			target: 21,
			visible: false
		},

                // { data: "fields.solicitaBiopsia"},
{
			target: 22,
			visible: false
		},

               // { data: "fields.solicitaMalla"},
{
			target: 23,
			visible: false
		},

               // { data: "fields.solicitaOtros"},
{
			target: 24,
			visible: false
		},

		

                { data: "fields.estadoProg"},
                { data: "fields.anestesia"},

                        ]
            }

		dataTable = $('#tablaSolicitudCirugia').DataTable(dataTableOptionsSolicitudCirugia);

  }

    if (valorTabla == 4)
    {
        let dataTableOptionsIngresosCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '150px',
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
                 url:"/load_dataIngresosCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miSolicitudCirugia' class='miSolicitudCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


		{ data: "fields.id"},
                { data: "fields.tipoDoc_id"},
                { data: "fields.documento"},
                { data: "fields.paciente"},
                { data: "fields.consecutivo"},
                { data: "fields.genero"},
                { data: "fields.edad"},
                { data: "fields.nacimiento"},
                { data: "fields.cama"},
                { data: "fields.telefono"},
                { data: "fields.empresa"},
                        ]
            }

		dataTable = $('#tablaIngresosCirugia').DataTable(dataTableOptionsIngresosCirugia);

  }



    if (valorTabla == 5)
    {
        let dataTableOptionsProcedimientosCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
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
                 url:"/load_dataTraerProcedimientosCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miProcedimientoCirugia' class='miSolicitudCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},
		{ data: "fields.id"},              
                { data: "fields.cups_id"},
                { data: "fields.exaNombre"},
                { data: "fields.finalNombre"},
                        ]
            }

		dataTable = $('#tablaProcedimientosCirugia').DataTable(dataTableOptionsProcedimientosCirugia);

  }


    if (valorTabla == 6)
    {
        let dataTableOptionsParticipantesCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
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
                 url:"/load_dataTraerParticipantesCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miParticipanteCirugia' class='miSolicitudCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


		{ data: "fields.id"},
                { data: "fields.cirugiaId"},
                { data: "fields.honNombre"},
                { data: "fields.medicoNombre"},
                { data: "fields.especialidadNombre"},
                { data: "fields.cupsNombre"},

                        ]
            }

		dataTable = $('#tablaParticipantesCirugia').DataTable(dataTableOptionsParticipantesCirugia);

  }

    if (valorTabla == 7)
    {
        let dataTableOptionsDisponibilidadSala  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '150px',
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
                 url:"/load_dataDisponibilidadSala/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miDisponibilidadSala' class='miDisponibilidadSala2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


		/* { data: "fields.prog"}, */
		{ data: "fields.id"},
                { data: "fields.sala"},
                { data: "fields.nombre"},
                { data: "fields.fechaProgramacionInicia"},
                { data: "fields.fechaProgramacionFin"},
                { data: "fields.horaProgramacionInicia"},
                { data: "fields.horaProgramacionFin"},
            /*    { data: "fields.estado"},  */



     {
		         target : 8,
			"sWidth": "1%",
        	           "render": function (data, type, row) {
                console.log ('data = ', data);
                console.log ('type = ', type);
                console.log ('row = ', row);


				if ( row['fields']['estado'] === 'OCUPADO')
                {
                    return '<i class="far fa-dot-circle" style="color:red; " >Ocupado</i>';
					/*  return 'SIN CONVENIO'; */
					}

			    if ( row['fields']['estado'] ==  'LIBRE')
				{
		 return '<i class="far fa-dot-circle" style="color:green" >Libre</i>';
/*
                     return  row['fields']['estado'];
                    return data;
*/
                    }


	                    }
			},









                        ]
            }

		dataTable = $('#tablaDisponibilidadSala').DataTable(dataTableOptionsDisponibilidadSala);

  }

    if (valorTabla == 8)
    {
        let dataTableOptionsMaterialCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
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
                 url:"/load_dataMaterialCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miMaterialCirugia' class='miMaterialCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},
		{ data: "fields.id"},   
		{ data: "fields.cupsNombre"},          
                { data: "fields.suministro_id"},
                { data: "fields.suministro"},
                { data: "fields.tipoSuministro"},
                { data: "fields.cantidad"},
                { data: "fields.valorLiquidacion"},
                        ]
            }

		dataTable = $('#tablaMaterialCirugia').DataTable(dataTableOptionsMaterialCirugia);

  }

    if (valorTabla == 9)
    {
        let dataTableOptionsParticipantesInformeCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '110px',
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
                 url:"/load_dataTraerParticipantesInformeCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miParticipanteInformeCirugia' class='miSolicitudInformeCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


		{ data: "fields.id"},
                { data: "fields.cirugiaId"},
                { data: "fields.honNombre"},
                { data: "fields.medicoNombre"},
                { data: "fields.especialidadNombre"},
                { data: "fields.cupsNombre"},
   {     "render": function ( data, type, row ) {
                        var btn = '';

		  btn = btn + " <button class='btn-primary  deleteParticipanteInformeCirugia' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa-solid fa-trash" style="font-size: 6px;"></i>' + "</button>";
	     
                       return btn;
                    },
            }
 
                        ]
            }

		dataTable = $('#tablaParticipantesInformeCirugia').DataTable(dataTableOptionsParticipantesInformeCirugia);

  }

    if (valorTabla == 10)
    {
        let dataTableOptionsProcedimientosInformeCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '110px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
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
                 url:"/load_dataTraerProcedimientosInformeCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miProcedimientoInformeCirugia' class='miSolicitudInformeCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},
		{ data: "fields.id"},              
		{ data: "fields.cirugia_id"},  
                { data: "fields.cups_id"},
                { data: "fields.exaNombre"},
                { data: "fields.finalNombre"},
                { data: "fields.cruento"},
                { data: "fields.incruento"},
                { data: "fields.regionOperatoria"},
                { data: "fields.viasDeAcceso"},


  {     "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn-primary  deleteProcedimientosInformeCirugia' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa-solid fa-trash" style="font-size: 6px;"></i>' + "</button>";
                       return btn;
                    },
            }
                        ]
            }

		dataTable = $('#tablaProcedimientosInformeCirugia').DataTable(dataTableOptionsProcedimientosInformeCirugia);

  }



    if (valorTabla == 11)
    {
        let dataTableOptionsMaterialInformeCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '110px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3] },
	    { width: '10%', targets: [2,3] },
		{  
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
                 url:"/load_dataMaterialInformeCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miMaterialInformeCirugia' class='miMaterialInformeCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},
		{ data: "fields.id"}, 
		{ data: "fields.cirugia_id"},             
		 { data: "fields.cupsNombre"},

                { data: "fields.suministro_id"},
                { data: "fields.suministro"},
                { data: "fields.tipoSuministro"},
               { data: "fields.cantidad"},
               { data: "fields.valorLiquidacion"},
  	{     "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn-primary deleteMaterialInformeCirugia' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa-solid fa-trash" style="font-size: 6px;"></i>' + "</button>";
                       return btn;
                    },
            }
                        ]
            }

		dataTable = $('#tablaMaterialInformeCirugia').DataTable(dataTableOptionsMaterialInformeCirugia);

  }



    if (valorTabla == 12)
    {
        let dataTableOptionsProcedimientosInformeXXCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
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
                 url:"/load_dataTraerProcedimientosInformeXXCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

		{ data: "fields.id"},              
		{ data: "fields.cirugia_id"},  
                { data: "fields.cups_id"},
                { data: "fields.exaNombre"},
                { data: "fields.finalNombre"},
                { data: "fields.cruento"},
                { data: "fields.incruento"},
                { data: "fields.regionOperatoria"},
                { data: "fields.viasDeAcceso"},
                        ]
            }

		dataTable = $('#tablaProcedimientosInformeXXCirugia').DataTable(dataTableOptionsProcedimientosInformeXXCirugia);

  }


    if (valorTabla == 13)
    {
        let dataTableOptionsMaterialInformeXXCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
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
                 url:"/load_dataMaterialInformeXXCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{ data: "fields.id"}, 
		{ data: "fields.cirugia_id"},             
		 { data: "fields.cupsNombre"},
                { data: "fields.suministro_id"},
                { data: "fields.suministro"},
                { data: "fields.tipoSuministro"},
               { data: "fields.cantidad"},
               { data: "fields.valorLiquidacion"},
                        ]
            }

		dataTable = $('#tablaMaterialInformeXXCirugia').DataTable(dataTableOptionsMaterialInformeXXCirugia);

  }


    if (valorTabla == 14)
    {
        let dataTableOptionsHojaDeGastoCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
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
                 url:"/load_dataHojaDeGastoCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{ data: "fields.id"}, 
		{ data: "fields.cirugia_id"},             
                { data: "fields.suministro_id"},
                { data: "fields.suministro"},
                { data: "fields.tipoSuministro"},
               { data: "fields.cantidad"},
  {     "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn  deleteHojaDeGastoCirugia' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa-solid fa-trash"></i>' + "</button>";
                       return btn;
                    },
            }

                        ]
            }

		dataTable = $('#tablaHojaDeGastoCirugia').DataTable(dataTableOptionsHojaDeGastoCirugia);

  }

    if (valorTabla == 15)
    {
        let dataTableOptionsHojaDeGastoXXCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
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
                 url:"/load_dataHojaDeGastoXXCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{ data: "fields.id"}, 
		{ data: "fields.cirugia_id"},             
                { data: "fields.suministro_id"},
                { data: "fields.suministro"},
                { data: "fields.tipoSuministro"},
               { data: "fields.cantidad"},
  {     "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn  deleteHojaDeGastoCirugia2' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa-solid fa-trash"></i>' + "</button>";
                       return btn;
                    },
            }

                        ]
            }

		dataTable = $('#tablaHojaDeGastoXXCirugia').DataTable(dataTableOptionsHojaDeGastoXXCirugia);

  }

    if (valorTabla == 16)
    {
        let dataTableOptionsParticipantesInformeXXCirugia  ={
	  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '275px',
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
                 url:"/load_dataTraerParticipantesInformeXXCirugia/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	    btn = btn + " <input type='radio' name='miParticipanteInformeXXCirugia' class='miSolicitudInformeXXCirugia2 form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },

	},


		{ data: "fields.id"},
                { data: "fields.cirugiaId"},
                { data: "fields.honNombre"},
                { data: "fields.medicoNombre"},
                { data: "fields.especialidadNombre"},
                { data: "fields.cupsNombre"},
	    {     "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn  deleteParticipanteInformeXXCirugia' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa-solid fa-trash" style="font-size: 12px;"></i>' + "</button>";
                       return btn;
                    },
            }
                        ]
            }

		dataTable = $('#tablaParticipantesInformeXXCirugia').DataTable(dataTableOptionsParticipantesInformeXXCirugia);

  }



}

const initDataTableProgramacionCirugia = async () => {
	if  (dataTableProgramacionCirugiaInitialized)  {
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

        arrancaCirugia(2,data);
	    dataTableProgramacionCirugiaInitialized = true;

        arrancaCirugia(1,data);
	    dataTableSalasCirugiaInitialized = true;

        arrancaCirugia(3,data);
	    dataTableSolicitudCirugiaInitialized = true;


      //  arrancaCirugia(9,data);
      // dataTableProcedimientosInformeCirugiaInitialized= true;

      //  arrancaCirugia(10,data);
      // dataTableParticipantesInformeCirugiaInitialized= true;
      //  arrancaCirugia(11,data);
      //  dataTableMaterialInformeCirugiaInitialized= true;

}


 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableProgramacionCirugia();
	 $('#tablaProgramacionCirugia tbody tr:eq(0) .miSol').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript

});


 /* FIN ONLOAD */




$('#tablaProgramacionCirugia tbody').on('click', '.miProgramacionCirugia2', function() {

		//  alert("ENTRE Programacion Cirugia");

	     var post_id = $(this).data('pk');
      
  });




$('#tablaProgramacionCirugia tbody').on('click', '.miEditaProgramacionCirugia', function() {

		//  alert("ENTRE Editar Programacion Cirugia");

	     var post_id = $(this).data('pk');
	// alert("programacion : " + post_id);
		
 	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	document.getElementById("sedesClinicaProgramacionCirugia_id").value = sede ;

     
	$.ajax({

	        url: "/buscaProgramacionCirugia/",
                data: {'programacionId':post_id,'sede':sede, 'username_id':username_id},
                type: "POST",
                dataType: 'json',
                success: function (info) {
            $('#postFormProgramacionCirugia').trigger("reset");
            $('#post_id').val('');

          
	 // alert("info sala_id = " + info[0].fields.sala_id);
	 //  alert("info fields  = " + info[0].fields);
		
		$('#sala').val(info[0].fields.sala_id);

          //  $('#fechaProgramacionInicia').val(info[0].fields.inicia);
            $('#horaProgramacionInicia').val(info[0].fields.horaInicia);
           // $('#fechaProgramacionTermina').val(info[0].fields.termina);
            $('#horaProgramacionFin').val(info[0].fields.horaTermina);
	    $('#estadoProgramacion').val(info[0].fields.estado_id);
	   $('#programacionId').val(post_id);
		 document.getElementById("fechaProgramacionInicia").value =info[0].fields.inicia;
		 document.getElementById("fechaProgramacionFin").value =   info[0].fields.termina;


            $('#modelHeadingProgramacionCirugia').html("Creacion Programacion de Cirugia");
            $('#crearModelProgramacionCirugia').modal('show');      


	
	username_id = document.getElementById("username_id").value   ;

	
	document.getElementById("usernameProgramacionCirugia_id").value = username_id;

            $('#estadosProgramacionY').val(info[0].fields.estado_id);
            $('#serviciosAdministrativos').val(info[0].fields.serviciosAdministrativos_id);


		// AQUI EL LLENADO DE LOS COMBOS PARTICIPA Y MATERIALES

		// Participantes solicitud e informe

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(info);
                     const $id2 = document.querySelector("#procedParticipantes");

 	      		     $("#procedParticipantes").empty();
				   alert("ya blanquue los medicos");

	                 $.each(dato[procedParticipantes], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });


                     const $id3 = document.querySelector("#procedMateriales");

 	      		     $("#procedMateriales").empty();
				   alert("ya blanquue los procedMateriales");

	                 $.each(dato[procedMateriales], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });


		// fin combo solicitud participa y maeria

		// combos Informe participa y merial

	  var dato = JSON.parse(info);
                     const $id4 = document.querySelector("#procedParticipantesInforme");

 	      		     $("#procedParticipantesInforme").empty();
				   alert("ya blanquue los procedParticipantesInforme");

	                 $.each(dato[procedParticipantes], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id4.appendChild(option);
 	      		      });


                     const $id5 = document.querySelector("#procedMaterialesInforme");

 	      		     $("#procedMaterialesInforme").empty();
				   alert("ya blanquue los procedMaterialesInforme");

	                 $.each(dato[procedMateriales], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id5.appendChild(option);
 	      		      });

		// fin combos informe





		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
	        data = JSON.stringify(data);	

	     arrancaCirugia(7,data);
	    dataTableDisponibilidadSalaInitialized = true;

		// document.getElementById("mensajesExitoModalProgramacion").innerHTML = 'Programacion actualizada Satisfactoriamente !';
				                },
                  error: function (data) {
	   			    	document.getElementById("mensajesErrorProgramacion").value =   data.responseText;

	   	    	}
            });
      
  });


$('#tablaProgramacionCirugia tbody').on('click', '.miEditaEstadoProgramacionCirugia', function() {

		//  alert("A modal EstadoProgramacionCirugia");

	     var post_id = $(this).data('pk');



	$.ajax({

	        url: "/traerEstadoProgramacionCirugia/",
                data: {'programacionId':post_id},
                type: "POST",
                dataType: 'json',
                success: function (info) {


            $('#postFormEstadoProgramacionCirugia').trigger("reset");

	   $('#estadosProgramacionCirugia').val(info[0].estadoProgramacionCirugia_id);

	   	document.getElementById("programacionIdParaEstado").value = post_id;
            $('#modelHeadingEstadoProgramacionCirugia').html("Actualizar estado programacion Cirugia");
            $('#crearModelEstadoProgramacionCirugia').modal('show');      

			                },
                   error: function (data) {
	   			    	document.getElementById("mensajesErrorProgramacion").value =   data.responseText;

	   	    	}
            });

      
  });


function GuardarEstadoProgramacionCirugia()
{
		//  alert("ENTRE Editar Guardar Estado Programacion Cirugia");
	  var programacionId = document.getElementById("programacionIdParaEstado").value;
	  var estadoId = document.getElementById("estadosProgramacionCirugia").value;

	// alert("programacion : " + programacionId );
     
	$.ajax({

	        url: "/guardarEstadoProgramacionCirugia/",
                data: {'programacionId':programacionId,'estadoId':estadoId},
                type: "POST",
                dataType: 'json',
                success: function (info) {

		var data =  {}   ;
	 	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	 	var sede = document.getElementById("sede").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;

	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
            $('#crearModelEstadoProgramacionCirugia').modal('hide');      	
		
	        data = JSON.stringify(data);
	       arrancaCirugia(2,data);
		    dataTableProgramacionCirugiaInitialized = true;

	       arrancaCirugia(3,data);
		    dataTableSolicitudCirugiaInitialized = true;





		//  alert("info = " + info);


			if (info.success == 'False')
			{
			document.getElementById("mensajesError").value = info.Mensajes;
			}
			else
			{
			document.getElementById("mensajes").value = info.Mensajes;
			}

				                },
      			 error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });


}


$('#tablaProgramacionCirugia tbody').on('click', '.miEditaEstadoCirugia', function() {
		// alert("A modal EstadoCirugia");

	     var post_id = $(this).data('pk');



	$.ajax({

	        url: "/traerEstadoCirugia/",
                data: {'programacionId':post_id},
                type: "POST",
                dataType: 'json',
                success: function (info) {

	


            $('#postFormEstadoCirugia').trigger("reset");

	   $('#estadosCirugia').val(info[0].estadoCirugia_id);
	   $('#cirugiaIdParaEstado2').val(info[0].id);

     	    document.getElementById("programacionIdParaEstado2").value = post_id;
            $('#modelHeadingEstadoCirugia').html("Actualizar estado programacion Cirugia");
            $('#crearModelEstadoCirugia').modal('show');      

	
				                },
      		   error: function (data) {
	   			    	document.getElementById("mensajesErrorProgramacion").value =   data.responseText;

	   	    	}
            });


      
  });


function GuardarEstadoCirugia()
{
		// alert("ENTRE Guardar Estado Cirugia");

	  	var cirugiaId = document.getElementById("cirugiaIdParaEstado2").value;
		var estadoId = document.getElementById("estadosCirugia").value;

  	     // alert("programacion : " + post_id);		
    
	$.ajax({

	        url: "/guardarEstadoCirugia/",
                data: {'cirugiaId':cirugiaId,'estadoId':estadoId},
                type: "POST",
                dataType: 'json',
                success: function (info) {

		var data =  {}   ;
	 	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	 	var sede = document.getElementById("sede").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;


	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
            $('#crearModelEstadoCirugia').modal('hide');      
		
	        data = JSON.stringify(data);
	       arrancaCirugia(2,data);
		    dataTableProgramacionCirugiaInitialized = true;
				                },
           error: function (data) {
	   			    	document.getElementById("mensajesErrorProgramacion").value =   data.responseText;

	   	    	}
            });


}
// FIN DE LO NUEVO

// Solicitud Procedimientos


$('#tablaSolicitudCirugia tbody').on('click', '.miAdicionarProcedimientos', function() {

		// alert("ENTRE miAdicionarProcedimientos");

	     var post_id = $(this).data('pk');
	cirugiaIdModalProcedimientos =   post_id;
	// alert("cirugiaIdModalProcedimientos = " +  cirugiaIdModalProcedimientos);
	

            $('#postFormProcedimientosCirugia').trigger("reset");

            $('#modelHeadingProcedimientosCirugia').html("Detalle Procedimientos Cirugia");
            $('#crearModelProcedimientosCirugia').modal('show');
		document.getElementById("cirugiaIdModalProcedimientos").value = cirugiaIdModalProcedimientos ;
		document.getElementById("cirugiaIdModalInformeProcedimientos").value = cirugiaIdModalProcedimientos ;

		username_id = document.getElementById("username_id").value   ;
		// alert("username_id = " + username_id );
		// document.getElementById("username4_id").value = username_id ;
	document.getElementById("usernameProcedimientosCirugia_id").value = username_id;


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
	data['cirugiaId'] = cirugiaIdModalProcedimientos;
 	    data = JSON.stringify(data);

		     arrancaCirugia(5,data);
		     	dataTableProcedimientosCirugiaInitialized = true;
	
      
  });

$('#tablaSolicitudCirugia tbody').on('click', '.miAdicionarParticipantes', function() {

		 

	         var post_id = $(this).data('pk');
		 var  cirugiaIdModalParticipantes =   post_id;
		var cirugiaId = post_id;

alert("ENTRE miAdicionarParticipantes" + cirugiaId);
  
            $('#postFormParticipantesCirugia').trigger("reset");		

// aquip AJAX ESTO ES NUEVO
          $.ajax({
                data: {'cirugiaId':cirugiaId},
	        url: "/buscarProcedimientosParticipantesDeCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	  	    var options = '<option value="=================="></option>';

	alert("llegue con estop = " + JSON.stringify(data2));
	alert("llegue con estop = " + JSON.stringify(data2[0]));

	            const $id4 = document.querySelector("#procedParticipantes");
 	      	$("#procedParticipantes").empty();

	                 $.each(data2, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id4.appendChild(option);
 	      		      });

            $('#modelHeadingParticipantesCirugia').html("Detalle Participantes Cirugia");
            $('#crearModelParticipantesCirugia').modal('show');

		document.getElementById("cirugiaIdModalParticipantes").value = cirugiaIdModalParticipantes ;
		username_id = document.getElementById("username_id").value   ;

		// alert("username_id = " + username_id );
		document.getElementById("usernameParticipantesCirugia_id").value = username_id ;      


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
	data['cirugiaId'] = post_id;
	// alert("voy a cargar tabla con post_id = " + post_id);

 	    data = JSON.stringify(data);

		     arrancaCirugia(6,data);
		     	dataTableParticipantesCirugiaInitialized = true;





                },
         error: function (data) {
	   			    	document.getElementById("mensajesErrorModalParticipantesInformeCirugia").value =   data.responseText;

	   	    	}
            });

// FIN AJAX NUEVO

  });


$('#tablaSolicitudCirugia tbody').on('click', '.miAdicionarMaterial', function() {

		// alert("ENTRE miAdicionarMaterial");

	     var post_id = $(this).data('pk');
	   var cirugiaIdModalMaterial =   post_id;
	// alert("cirugiaIdModalMaterial = " +  cirugiaIdModalMaterial);
		var cirugiaId = post_id;

            $('#postFormMaterialCirugia').trigger("reset");



// aquip AJAX ESTO ES NUEVO
          $.ajax({
                data: {'cirugiaId':cirugiaId},
	        url: "/buscarProcedimientosMaterialesDeCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	  	    var options = '<option value="=================="></option>';

	alert("llegue con estop = " + JSON.stringify(data2));
	alert("llegue con estop = " + JSON.stringify(data2[0]));

	            const $id5 = document.querySelector("#procedMateriales");
 	      	$("#procedMaterialess").empty();

	                 $.each(data2, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id5.appendChild(option);
 	      		      });

            $('#modelHeadingMaterialCirugia').html("Detalle Material Qx");
            $('#crearModelMaterialCirugia').modal('show');
		document.getElementById("cirugiaIdModalMaterial").value = cirugiaIdModalMaterial ;
		username_id = document.getElementById("username_id").value   ;
		 document.getElementById("usernameMaterialCirugia_id").value = username_id  ;
		// alert("username_id = " + username_id );

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
	data['cirugiaId'] = cirugiaIdModalMaterial;
 	    data = JSON.stringify(data);

		     arrancaCirugia(8,data);
		     	dataTableMaterialCirugiaInitialized = true;
	




                },
         error: function (data) {
	   			    	document.getElementById("mensajesErrorModalParticipantesInformeCirugia").value =   data.responseText;

	   	    	}
            });

// FIN AJAX NUEVO


      
  });


$('#tablaProgramacionCirugia tbody').on('click', '.miProgramacionCirugia2', function() {


	     var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
		var programacionId= post_id;
		// alert("ProgramacionId = " + programacionId);
	// Debo hacer un AJAX para traer la cirugia, le envio la programacion

    $.ajax({
                
	        url: "/seleccionProgramacionCirugia/",
		data:{'programacionId':programacionId},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		// alert("data2 = " + data2);
		var cirugiaId = data2;		
    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

	document.getElementById("cirugiaIdModalInformeProcedimientos").value = cirugiaId;
	document.getElementById("cirugiaIdModalProcedimientos").value = cirugiaId;
	// alert("voy a colocar en cirugiaIdModalParticipantesInforme = " + cirugiaId);

	document.getElementById("cirugiaIdModalParticipantes").value = cirugiaId;
	// alert("Y LO LEO = " + document.getElementById("cirugiaIdModalParticipantes").value);
	document.getElementById("cirugiaIdModalParticipantesInforme").value = cirugiaId;

	document.getElementById("cirugiaIdModalAdicionarQx").value = cirugiaId;

	// Aqui llenar la info basica de la programacion Cirugia en la hoja de Informe qx

	var table = $('#tablaProgramacionCirugia').DataTable();  // Inicializa el DataTable jquery 	      
	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato3 documento = " , dato3.documento); 
	        console.log ( "dato3 paciente = " , dato3.paciente); 
	 document.getElementById("tipoDocPaciente").innerHTML = dato3.abrev;
	document.getElementById("docPaciente").innerHTML = dato3.documento;
	document.getElementById("nombrePaciente").innerHTML = dato3.paciente;
	document.getElementById("salaCirugia").innerHTML = dato3.sala;
	document.getElementById("programacionDesdeCirugia").innerHTML = dato3.inicia;
	document.getElementById("programacionDesdeHoraCirugia").innerHTML = dato3.horaInicia;
	document.getElementById("programacionHastaCirugia").innerHTML = dato3.horaInicia;
	document.getElementById("programacionHastaHoraCirugia").innerHTML = dato3.horaTermina;






	// Fin llenado

         var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	data['cirugiaId'] = cirugiaId;
 	data = JSON.stringify(data);

        arrancaCirugia(9,data);
	dataTableProcedimientosInformeCirugiaInitialized= true;

        arrancaCirugia(10,data);

	dataTableParticipantesInformeCirugiaInitialized= true;

        arrancaCirugia(11,data);
	dataTableMaterialInformeCirugiaInitialized= true;
        arrancaCirugia(14,data);
	dataTableHojaDeGastoCirugiaInitialized= true;
		  	
                },
         error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });
	
      
  });

$('#tablaProcedimientosInformeCirugia tbody').on('click', '.deleteProcedimientosInformeCirugia', function() {


		var row = $(this).closest('tr'); // Encuentra la fila
	     var post_id = $(this).data('pk');
		var procedimientoId = post_id;
	var table = $('#tablaProcedimientosInformeCirugia').DataTable();  // Inicializa el DataTable jquery//
	
 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
       console.log("rowindex= " , rowindex);

	    	 dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "la factura es =  = " , dato3.cirugia_id); 
		cirugiaId = dato3.cirugia_id;

		// alert("Seleccion DELETE fila" + post_id);
		// alert("Cirugia : " + cirugiaId );

            $.ajax({
                
	        url: "/borraProcedimientosInformeCirugia/",
		data:{'cirugiaId':cirugiaId,'procedimientoId':procedimientoId},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
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
	data['cirugiaId'] = cirugiaId;
 	    data = JSON.stringify(data);

        arrancaCirugia(10,data);
	dataTableProcedimientosInformeCirugiaInitialized= true;

                },
          error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });


	
      
  });



$('#tablaParticipantesInformeCirugia tbody').on('click', '.deleteParticipanteInformeCirugia', function() {



	     var post_id = $(this).data('pk');
		var participanteId = post_id;

		var table = $('#tablaParticipantesInformeCirugia').DataTable();  // Inicializa el DataTable jquery//
	
		var row = $(this).closest('tr'); // Encuentra la fila
	 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	        console.log("rowindex= " , rowindex);
	  	dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "la factura es =  = " , dato3.cirugiaId); 
		cirugiaId = dato3.cirugiaId;

		// alert("Seleccion DELETE fila" + post_id);
		// alert("Cirugia : " + cirugiaId );


	
            $.ajax({
                
	        url: "/borraParticipanteInformeCirugia/",
		data:{'participanteId': participanteId},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
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
	data['cirugiaId'] = cirugiaId;
 	    data = JSON.stringify(data);

        arrancaCirugia(9,data);
	dataTableParticipantesInformeCirugiaInitialized= true;

                },
    error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });


	
      
  });

$('#tablaMaterialInformeCirugia tbody').on('click', '.deleteMaterialInformeCirugia', function() {


	
	     var post_id = $(this).data('pk');
		var materialId = post_id;
			// alert("Seleccion DELETE fila" + post_id);
	
		var table = $('#tablaMaterialInformeCirugia').DataTable();  // Inicializa el DataTable jquery//
		var row = $(this).closest('tr'); // Encuentra la fila
	 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
	        console.log("rowindex= " , rowindex);
	  	dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "la factura es =  = " , dato3.cirugia_id); 
		cirugiaId = dato3.cirugia_id;

		// alert("Seleccion DELETE fila" + post_id);
		// alert("Cirugia : " + cirugiaId );




            $.ajax({
                
	        url: "/borraMaterialInformeCirugia/",
		data:{'materialId': materialId},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
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
	data['cirugiaId'] = cirugiaId;
 	    data = JSON.stringify(data);

        arrancaCirugia(11,data);
	dataTableMaterialesInformeCirugiaInitialized= true;

                },
  error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });


	
      
  });


$('#tablaHojaDeGastoCirugia tbody').on('click', '.deleteHojaDeGastoCirugia', function() {


		var row = $(this).closest('tr'); // Encuentra la fila
	     var post_id = $(this).data('pk');
		var hojaDeGastoId = post_id;

	var table = $('#tablaHojaDeGastoCirugia').DataTable();  // Inicializa el DataTable jquery//
	
 	var rowindex = table.row(row).data(); // Obtiene los datos de la fila
       console.log("rowindex= " , rowindex);

	    	 dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "la factura es =  = " , dato3.cirugia_id); 
		cirugiaId = dato3.cirugia_id;

		// alert("Seleccion DELETE fila" + post_id);
		// alert("Cirugia : " + cirugiaId );

            $.ajax({
                
	        url: "/borraHojaDeGastoCirugia/",
		data:{'cirugiaId':cirugiaId,'hojaDeGastoId':hojaDeGastoId},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
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
	data['cirugiaId'] = cirugiaId;
 	    data = JSON.stringify(data);

        arrancaCirugia(14,data);
	dataTableHojaDeGastoCirugiaInitialized= true;

                },
  error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });


	
      
  });





$('#tablaIngresosCirugia tbody').on('click', '.miSolicitudCirugia2', function() {


		 var post_id = $(this).data('pk');
		document.getElementById("ingresoId2").value  = post_id;
		username_id = document.getElementById("username_id").value;

		document.getElementById("username3_id").value  = username_id;
		var ingresoId = post_id;

// aqui va el ajax que trae los convenios de paciente a ser seleccionado

            $.ajax({
	        url: "/buscarConveniosCirugiaPaciente/",
		data: {'ingresoId':ingresoId},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		// if (data2.success == true)
		// 	 {
		// 	  document.getElementById("mensajes").value = data2.Mensajes;
		// 	 }
		// 	else
		// 	{
			alert("data2  = " + JSON.stringify(data2));
// 
// 			document.getElementById("mensajesErrorModalProgramacion").value = data2.Mensajes;
// 			return;
// 			}

	  		   var options = '<option value="=================="></option>';

	  		//  var dato = JSON.parse(data2);
				var dato = data2;


                     const $id2 = document.querySelector("#convenioProc");


 	      		     $("#convenioProc").empty();

				   alert("ya blanquue los convenioProc");



	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });



                },
       error: function (data) {
	   			    	document.getElementById("mensajesErrorModalProgramacion").value =   data.responseText;

	   	    	}
            });




// FIN AJAX
		
})





/* ---------------------------------
Para borrar detalle rips
------------------------------------*/





	/*------------------------------------------
        --------------------------------------------
        Create GuardarDetalleRips
        --------------------------------------------
        --------------------------------------------*/

/*------------------------------------------
        --------------------------------------------
        EnvioRips
        --------------------------------------------
        --------------------------------------------*/





function CerrarModalJson()
{

            $('#crearModelRipsJson').modal('hide');
}

function CerrarModalEnvioJson()
{

            $('#crearModelRipsEnvioJson').modal('hide');
}


function ProgramacionCirugia()
{
// alert("VACIO");

}

function SolicitudCirugia()
{	
	// alert("Solicitud");

            $('#post_id').val('');
            $('#postFormSolicitudCirugia').trigger("reset");
            $('#modelHeadingSolicitudCirugia').html("Creacion Solicitud de Cirugia");
	   var sede = document.getElementById("sede").value;
	   document.getElementById("sedesClinica_id").value =  sede;
	   document.getElementById("username3_id").value =  document.getElementById("username_id").value;
	    arrancaCirugia(4,data);
	    dataTableIngresosCirugiaInitialized = true;
		document.getElementById("cirugiaId2").value = post_id
            $('#crearModelSolicitudCirugia').modal('show');      
}



function CrearProgramacionCirugia()
{
	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinica_id").value =  sede;

	// Validaciones de ocupacion
		

            $.ajax({
                data: $('#postFormProgramacionCirugia').serialize(),
	        url: "/crearProgramacionCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		


		if (data2.success == true)
			 {
			  document.getElementById("mensajes").value = data2.Mensajes;
			 }
			else
			{
			alert("data2 ERROR = " + JSON.stringify(data2));

			document.getElementById("mensajesErrorModalProgramacion").value = data2.Mensajes;
			return;
			}



		  
              //    $('#postFormProgramacionCirugia').trigger("reset");
		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
	        data = JSON.stringify(data);
	
	     arrancaCirugia(2,data);
	    dataTableProgramacionCirugiaInitialized = true;

	     arrancaCirugia(1,data);
	    dataTableSalasCirugiaInitialized = true;

 		$('#crearModelProgramacionCirugia').modal('hide');

	document.getElementById("mensajesExitoModalProgramacion").value = data2.Mensajes;
	  
	     arrancaCirugia(7,data);
	    dataTableDisponibilidadSalaInitialized = true;

   arrancaCirugia(3,data);
	    dataTableSolicitudCirugiaInitialized = true;



                },
       error: function (data) {
	   			    	document.getElementById("mensajesErrorModalProgramacion").value =   data.responseText;

	   	    	}
            });


}



function CrearSolicitudCirugia()
{

	// alert("Entre CrearSolicitudCirugia");
	var row = $(this).closest('tr'); // Encuentra la fila

	// alert("row =" +  row);
	console.log("row =",  row);

	var sede = document.getElementById("sede").value;
	// alert("sede = " + sede);

	document.getElementById("sedesClinica_id").value =  sede;
	

            $.ajax({
                data: $('#postFormSolicitudCirugia').serialize(),
	        url: "/crearSolicitudCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormSolicitudCirugia').trigger("reset");
		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
	        data = JSON.stringify(data);

	     arrancaCirugia(2,data);
	    dataTableProgramacionCirugiaInitialized = true;

	     arrancaCirugia(1,data);
	    dataTableSalasCirugiaInitialized = true;

	     arrancaCirugia(3,data);
	    dataTableSolicitudCirugiaInitialized = true;

 		 $('#crearModelSolicitudCirugia').modal('hide');
		 $("#mensajes").html(data2.message);

                },
      error: function (data) {
	   			    	document.getElementById("mensajesErrorModalSolicitud").value =   data.responseText;

	   	    	}
            });


}

function CrearProcedimientosCirugia()
{

	// alert("CrearProcedimientosCirugia");

	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinica_id").value =  sede;
	var cirugiaIdModalProcedimientos  = document.getElementById("cirugiaIdModalProcedimientos").value ;
	var user  = document.getElementById("usernameProcedimientosCirugia_id").value ;

	// alert("user = " + user);


            $.ajax({
                data: $('#postFormProcedimientosCirugia').serialize(),
	        url: "/crearProcedimientosCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormProcedimientosCirugia').trigger("reset");

	document.getElementById("cirugiaIdModalProcedimientos").value  = cirugiaIdModalProcedimientos ;
	document.getElementById("usernameProcedimientosCirugia_id").value = user;


		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] =cirugiaIdModalProcedimientos;
	        data = JSON.stringify(data);
	

	     arrancaCirugia(5,data);
	    dataTableProcedimientosCirugiaInitialized = true;

  
 		// $('#crearModelProcedimientosCirugia').modal('hide');
				
		document.getElementById("mensajesModalProcedimientosCirugia").value = data2.Mensajes;


                },
       error: function (data) {
	   			    	document.getElementById("mensajesErrorModalProcedimientosCirugia").value =   data.responseText;

	   	    	}
            });


}

function CrearParticipantesCirugia()
{
	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinica_id").value =  sede;
	var cirugiaId = document.getElementById("cirugiaIdModalParticipantes").value;
	var user  = document.getElementById("usernameParticipantesCirugia_id").value ;


            $.ajax({
                data: $('#postFormParticipantesCirugia').serialize(),
	        url: "/crearParticipantesCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormParticipantesCirugia').trigger("reset");
	  document.getElementById("cirugiaIdModalParticipantes").value = cirugiaId;
	 document.getElementById("usernameParticipantesCirugia_id").value  = user;

	var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] =cirugiaId;
	        data = JSON.stringify(data);
	 	

	     arrancaCirugia(6,data);
	    dataTableParticipantesCirugiaInitialized = true;
  
	     arrancaCirugia(9,data);
	    dataTableParticipantesCirugiaInitialized = true;


 		 // $('#crearModelParticipantesCirugia').modal('hide');

	document.getElementById("mensajesModalParticipantesCirugia").value = data2.Mensajes;

                },
        error: function (data) {
	   			    	document.getElementById("mensajesErrorModalParticipantesCirugia").value =   data.responseText;

	   	    	}
            });


}

function CrearParticipantesInformeCirugia()
{
	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinicaModalParticipantesInforme_id").value =  sede;
	var cirugiaId = document.getElementById("cirugiaIdModalParticipantesInforme").value;
	var user  = document.getElementById("username_id").value ;
	 document.getElementById("usernameParticipantesInformeCirugia_id").value  = user;

  // OJO AQUI FILTRAR PARA QUE SOLO SE SELCCIONE CIRUJANO HONORARIO MEDICO LOS DEMAS HONORARIO SE DEJA CUPS_ID = NULO


	var tipoHonorarioSeleccionado = document.getElementById("tipoHonorariosInforme").value ;
	var cupsSeleccionado = document.getElementById("cupsParticipantesInforme").value ;

	/* Para obtener el valor */
	var tipoHonorarioSeleccionado = document.getElementById("tipoHonorariosInforme").value;
	// alert(tipoHonorarioSeleccionado);
 
	/* Para obtener el texto */
	var combo = document.getElementById("tipoHonorariosInforme");
	var nombreHonorario = combo.options[combo.selectedIndex].text;
	// alert(nombreHonorario);

	  if ( nombreHonorario != 'CIRUJANO')
		{

		// alert("Entre a blanquear = "  );
		 combo.selectedIndex = 0;
		}

            $.ajax({
                data: $('#postFormParticipantesInformeCirugia').serialize(),
	        url: "/crearParticipantesInformeCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormParticipantesInformeCirugia').trigger("reset");

	  document.getElementById("cirugiaIdModalParticipantesInforme").value = cirugiaId;
	 document.getElementById("usernameParticipantesInformeCirugia_id").value  = user;

	var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = user;
			
		data['cirugiaId'] =cirugiaId;
	        data = JSON.stringify(data);
	 	

	     arrancaCirugia(16,data);
	    dataTableParticipantesInformeXXCirugiaInitialized = true;

	     arrancaCirugia(9,data);
	    dataTableParticipantesInformeXXCirugiaInitialized = true;
  


 		 // $('#crearModelParticipantesCirugia').modal('hide');

		document.getElementById("mensajesModalParticipantesInformeCirugia").value = data2.Mensajes;



                },
        error: function (data) {
	   			    	document.getElementById("mensajesErrorModalParticipantesInformeCirugia").value =   data.responseText;

	   	    	}
            });


}


function AdicionarParticipanteInformeCirugia()
{

	var cirugiaId = document.getElementById("cirugiaIdModalProcedimientos").value ;
        
	var user  = document.getElementById("username_id").value ;

                  $('#postFormParticipantesInformeCirugia').trigger("reset");
document.getElementById("cirugiaIdModalParticipantesInforme").value =	document.getElementById("cirugiaIdModalProcedimientos").value ;
                 var cirugiaId = document.getElementById("cirugiaIdModalParticipantesInforme").value;

   $('#modelHeadingParticipantesInformeCirugia').html("Adicion participante de Cirugia");


          $.ajax({
                data: {'cirugiaId':cirugiaId},
	        url: "/buscarProcedimientosDeCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		
		// alert(" estado nombre cirugia3 = " + data2[0].EstadoNombreCirugia);

		if (data2[0].EstadoNombreCirugia == 'REALIZADA')
				{
				document.getElementById("mensajesError").value = 'No se pueden agregar mas participantes a Cirugia Realizada !'
				return;
				}

			if (data2[0].EstadoNombreCirugia == 'FACTURADA')
				{
				document.getElementById("mensajesError").value = 'No se pueden agregar mas participantes a Cirugia Facturada !'
				return;
				}


	

	    // $('#cupsParticipantesInforme').val(data2);


	  	    var options = '<option value="=================="></option>';

		

	  //          const $id2 = document.querySelector("#cupsParticipantesInforme");
 	  //    	$("#cupsParticipantesInforme").empty();

//	                 $.each(data2, function(key,value) {
  //                                  options +='<option value="' + value.id + '">' + value.nombre + '</option>';
    //                                option = document.createElement("option");
      //                              option.value = value.id;
        //                            option.text = value.nombre;
          //                          $id2.appendChild(option);
 	    //  		      });

alert("llegue con estop = " + JSON.stringify(data2));
alert("llegue con estop = " + JSON.stringify(data2[0]));


	            const $id3 = document.querySelector("#procedParticipantesInforme");
 	      	$("#procedParticipantesInforme").empty();

	                 $.each(data2[0]['ProcedParticipantesInforme'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });


		  
	var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = user;
			
		data['cirugiaId'] =cirugiaId;
	        data = JSON.stringify(data);

	     arrancaCirugia(9,data);
	    dataTableParticipantesInformeCirugiaInitialized = true;


	     arrancaCirugia(16,data);
	    dataTableParticipantesInformeXXCirugiaInitialized = true;

  
 		 $('#crearModelParticipantesInformeCirugia').modal('show');

                },
         error: function (data) {
	   			    	document.getElementById("mensajesErrorModalParticipantesInformeCirugia").value =   data.responseText;

	   	    	}
            });


}



function CrearMaterialCirugia()
{

	// alert("CrearMaterialCirugia");

	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinica_id").value =  sede;
	cirugiaIdModalMaterial  = document.getElementById("cirugiaIdModalMaterial").value ;
	var user  = document.getElementById("usernameMaterialCirugia_id").value ;
        var cantidad = document.getElementById("cantidad").value ;

		if (cantidad =='')
		{
		alert("Suministre Cantidad de material");
		return;
		}

            $.ajax({
                data: $('#postFormMaterialCirugia').serialize(),
	        url: "/crearMaterialCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormMaterialCirugia').trigger("reset");
	   document.getElementById("cirugiaIdModalMaterial").value = cirugiaIdModalMaterial;
	 document.getElementById("usernameMaterialCirugia_id").value =  user;

		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] =cirugiaIdModalMaterial;
	        data = JSON.stringify(data);
	

	     arrancaCirugia(8,data);
	    dataTableMaterialCirugiaInitialized = true;
	  

 		// $('#crearModelMaterialCirugia').modal('hide');
			 document.getElementById("mensajesModalMaterialCirugia").value = data2.Mensajes;



                },
         error: function (data) {
	   			    	document.getElementById("mensajesErrorModalMaterialCirugia").value =   data.responseText;

	   	    	}
            });


}



function AdicionarProcedimientosInformeCirugia() {


		var post_id = document.getElementById("cirugiaIdModalInformeProcedimientos").value ;

	 
    $.ajax({

	        url: "/traerInformacionDeCirugia/",
                data: {'cirugiaId':post_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
	            $('#postFormProcedimientosInformeCirugia').trigger("reset");


			// alert(" data2.estadoCirugia = "+ data2[0]['estadoCirugia']);

			if (data2[0]['estadoCirugia'] == 'REALIZADA')
				{
				document.getElementById("mensajesError").value = 'No se pueden agregar mas procedimientos a Cirugia Realizada !'
				return;
				}

			if (data2[0]['estadoCirugia'] == 'FACTURADA')
				{
				document.getElementById("mensajesError").value = 'No se pueden agregar mas procedimientos a Cirugia Facturada !'
				return;
				}


	            $('#modelHeadingProcedimientosInformeCirugia').html("Detalle Procedimientos Cirugia");
			username_id = document.getElementById("username_id").value   ;


			// document.getElementById("username4_id").value = username_id ;
			document.getElementById("usernameProcedimientosInformeCirugia_id").value = username_id;
			document.getElementById("tipoDocZ").innerHTML = data2[0].tipoDoc;
			document.getElementById("documentoZ").innerHTML = data2[0].documento;
			document.getElementById("pacienteZ").innerHTML = data2[0].paciente;
			document.getElementById("salaZ").innerHTML = data2[0].sala;
			document.getElementById("estadoCirugiaZ").innerHTML = data2[0].estadoCirugia;

	
	            $('#crearModelProcedimientosInformeCirugia').modal('show');
			document.getElementById("cirugiaIdModalInformeProcedimientos").value = document.getElementById("cirugiaIdModalProcedimientos").value;




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
		data['cirugiaId'] = document.getElementById("cirugiaIdModalInformeProcedimientos").value;
	 	    data = JSON.stringify(data);

		     arrancaCirugia(12,data);
		     	dataTableProcedimientosInformeXXCirugiaInitialized = true; 
          

                },
          error: function (data) {
	   			    	document.getElementById("mensajesErrorModalProcedimientosInformeCirugia").value =   data.responseText;

	   	    	}
            });
    
  };


function CrearProcedimientosInformeCirugia()
{

	// alert("CrearProcedimientosInfornmeCirugia");

	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinica_id").value =  sede;
	var cirugiaIdModalInformeProcedimientos  = document.getElementById("cirugiaIdModalInformeProcedimientos").value ;
	var user  = document.getElementById("usernameProcedimientosInformeCirugia_id").value ;

	// alert("user = " + user);


            $.ajax({
                data: $('#postFormProcedimientosInformeCirugia').serialize(),
	        url: "/crearProcedimientosInformeCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormProcedimientosInformeCirugia').trigger("reset");

	document.getElementById("cirugiaIdModalInformeProcedimientos").value  = cirugiaIdModalInformeProcedimientos ;
	document.getElementById("usernameProcedimientosInformeCirugia_id").value = user;


		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] =document.getElementById("cirugiaIdModalInformeProcedimientos").value;
	        data = JSON.stringify(data);
	

	     arrancaCirugia(10,data);
	    dataTableProcedimientosInformeCirugiaInitialized = true;

	  
	     arrancaCirugia(12,data);
	    dataTableProcedimientosInformeXXCirugiaInitialized = true;


 		// $('#crearModelProcedimientosCirugia').modal('hide');

	document.getElementById("mensajesModalProcedimientosInformeCirugia").value = data2.Mensajes;

                },
        error: function (data) {
	   			    	document.getElementById("mensajesErrorModalProcedimientosInformeCirugia").value =   data.responseText;

	   	    	}
            });


}


function AdicionarQx() {


	var cirugiaId = document.getElementById("cirugiaIdModalProcedimientos").value ;
	var sede = document.getElementById("sede").value ;

		// alert("ENTRE miAdicionarQx Cirugia No" + cirugiaId);

            $.ajax({
                data: {'sede':sede, 'cirugiaId':cirugiaId},
	        url: "/buscaAdicionarQx/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

            $('#postFormAdicionarQx').trigger("reset");

	    document.getElementById("cirugiaIdModalAdicionarQx").value = document.getElementById("cirugiaIdModalProcedimientos").value ;
		$('#ingresoQuirofano').val(info[0].fields.ingresoQuirofano);
		// alert("fechainiAnestesia = " + info[0].fields.fechaIniAnestesia);

		$('#fechaIniAnestesia2').val(info[0].fields.fechaIniAnestesia);
		$('#fechaQxIni').val(info[0].fields.fechaQxIni);
		$('#fechaQxFin').val(info[0].fields.fechaQxFin);
		$('#fechaFinAnestesia').val(info[0].fields.fechaFinAnestesia);
		$('#salidaQuirofano').val(info[0].fields.salidaQuirofano);
		$('#ingresoRecuperacion').val(info[0].fields.ingresoRecuperacion);
		$('#salidaRecuperacion').val(info[0].fields.salidaRecuperacion);
		$('#dxPreOperatorio').val(info[0].fields.dxPreOperatorio);
		$('#dxPostOperatorio').val(info[0].fields.dxPostOperatorio);
		$('#impresionDx').val(info[0].fields.impresionDx);
		$('#complicacionesDx').val(info[0].fields.complicacionesDx);
		$('#formaRealizacion').val(info[0].fields.formaRealizacion);
		$('#tejidoPatologia').val(info[0].fields.tejidoPatologia);
		$('#tipoFractura').val(info[0].fields.tipoFractura);
		$('#intensificador').val(info[0].fields.intensificador);
		$('#descripcionQx').val(info[0].fields.descripcionQx);
		$('#hallazgos').val(info[0].fields.hallazgos);
		$('#analisis').val(info[0].fields.analisis);
		$('#planx').val(info[0].fields.planx);
		$('#fechaIniAnestesia2').val(info[0].fields.fechaIniAnestesia);

            $('#modelHeadingAdicionarQx').html("Adicion Qx");
            $('#crearModelAdicionarQx').modal('show');

                },
       error: function (data) {
	   			    	document.getElementById("mensajesErrorModalAdicionarQx").value =   data.responseText;

	   	    	}
            });

   	
	
      
  };


function CrearAdicionQx() {

		// alert("ENTRE CrearAdicionQx");
		// Aqui validacion de fechas. Para Filtrar inconsistyencias

		var ingresoQuirofano = document.getElementById("ingresoQuirofano").value ;
		var fechaIniAnestesia2 = document.getElementById("fechaIniAnestesia2").value ;
		var fechaQxIni = document.getElementById("fechaQxIni").value ;
		var fechaQxIni = document.getElementById("fechaQxIni").value ;
		var fechaQxFin = document.getElementById("fechaQxFin").value ;
		var fechaFinAnestesia = document.getElementById("fechaFinAnestesia").value ;
		var salidaQuirofano = document.getElementById("salidaQuirofano").value ;
		var ingresoRecuperacion = document.getElementById("ingresoRecuperacion").value ;
		var salidaRecuperacion = document.getElementById("salidaRecuperacion").value ;

		if (fechaIniAnestesia2<ingresoQuirofano )
			{
			document.getElementById("cirugiaIdModalAdicionarQx").value = 'Fecha inicio de anestesia No puede ser menor que el ingreso al Quirofano !'
			return;
			}

		if (fechaQxIni<fechaIniAnestesia2 )
			{
			document.getElementById("cirugiaIdModalAdicionarQx").value = 'Fecha inicio Quirurgico No puede ser menor que el inicio de la Anestesia !'
			return;
			}

		if (fechaQxFin<fechaQxIni )
			{
			document.getElementById("cirugiaIdModalAdicionarQx").value = 'Fecha FIn Quirurgico No puede ser menor que la fecha de Inicio Quirurgico!'
			return;
			}

		if (fechaFinAnestesia<fechaQxFin )
			{
			document.getElementById("cirugiaIdModalAdicionarQx").value = 'Fecha Fin de Anestesia No puede ser menor que la fecha de Fin Quirurgico!'
			return;
			}

		if (salidaQuirofano<fechaFinAnestesia )
			{
			document.getElementById("cirugiaIdModalAdicionarQx").value = 'Fecha de salida Quirofano No puede ser menor que la fecha de Fin Anestesia !'
			return;
			}

		if (ingresoRecuperacion<salidaQuirofano )
			{
			document.getElementById("cirugiaIdModalAdicionarQx").value = 'Fecha de Inicio Recuperacion No puede ser menor que la fecha de salida de quirofano !'
			return;
			}

		if (salidaRecuperacion<ingresoRecuperacion )
			{
			document.getElementById("cirugiaIdModalAdicionarQx").value = 'Fecha de Salida de Recuperacion No puede ser menor que la fecha de ingreso a Recuperacion !'
			return;
			}
	



       $.ajax({
                data: $('#postFormAdicionarQx').serialize(),
	        url: "/crearAdicionQx/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormAdicionarQx').trigger("reset");
	    document.getElementById("cirugiaIdModalAdicionarQx").value = document.getElementById("cirugiaIdModalProcedimientos").value ;



		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] = document.getElementById("cirugiaIdModalProcedimientos").value ;

	        data = JSON.stringify(data);
	

	  
	     // arrancaCirugia(12,data);
	     // dataTableProcedimientosInformeXXCirugiaInitialized = true;


            $('#crearModelAdicionarQx').modal('hide');
		    	
		 $("#mensajesModalAdicionarQx").html(data2.message);

                },
        error: function (data) {
	   			    	document.getElementById("mensajesErrorModalAdicionarQx").value =   data.responseText;

	   	    	}
            });

	
        };


function CrearMaterialInformeCirugia()
{

	// alert("CrearMaterialInformeCirugia");

	if (cantidad =='')
		{
		alert("Suministre Cantidad de material");
		return;
		}


	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinicaModalMaterialInforme_id").value =  sede;
	var cirugiaIdModalMaterialInforme  = document.getElementById("cirugiaIdModalMaterialInforme").value ;
	


            $.ajax({
                data: $('#postFormMaterialInformeCirugia').serialize(),
	        url: "/crearMaterialInformeCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormMaterialInformeCirugia').trigger("reset");
	   document.getElementById("cirugiaIdModalMaterialInforme").value = cirugiaIdModalMaterialInforme;
		var user  = document.getElementById("username_id").value ;
	

	 document.getElementById("usernameMaterialInformeCirugia_id").value=user;

		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] =cirugiaIdModalMaterialInforme;
	        data = JSON.stringify(data);
	

	     arrancaCirugia(13,data);
	    dataTableMaterialInformeXXCirugiaInitialized = true;
	  
	    arrancaCirugia(11,data);
	    dataTableMaterialInformeCirugiaInitialized = true;
	  
 		// $('#crearModelMaterialInformeCirugia').modal('hide');

    	document.getElementById("mensajesModalMaterialInformeCirugia").value = data2.Mensajes;


                },
            error: function (data) {
	   			    	document.getElementById("mensajesErrorModalMaterialCirugia").value =   data.responseText;

	   	    	}
            });


}

function AdicionarHojaDeGastoCirugia() {

   	   //  alert("ENTRE AdicionarHojaDeGastoCirugia");




            $('#postFormHojaDeGastoCirugia').trigger("reset");
	    document.getElementById("cirugiaIdModalHojaDeGastoCirugia").value = document.getElementById("cirugiaIdModalHojaDeGastoCirugia").value ;
	    var user  = document.getElementById("username_id").value ;
	    document.getElementById("usernameHojaDeGastoCirugia_id").value = user; 

	    document.getElementById("cirugiaIdModalHojaDeGastoCirugia").value = document.getElementById("cirugiaIdModalProcedimientos").value ;

           $('#modelHeadingHojaDeGastoCirugia').html("Hoja De Gasto Cirugia");
            $('#crearModelHojaDeGastoCirugia').modal('show');		    	
	
      
  };

function AdicionarMaterialInformeCirugia() {

   	     alert("ENTRE AdicionarMaterialInformeCirugia");

            $('#postFormMaterialInformeCirugia').trigger("reset");
	    document.getElementById("cirugiaIdModalMaterialInforme").value = document.getElementById("cirugiaIdModalProcedimientos").value ;
	    var user  = document.getElementById("username_id").value ;

	    document.getElementById("usernameMaterialInformeCirugia_id").value = user;
	
	    cirugiaId = document.getElementById("cirugiaIdModalProcedimientos").value ;

// aqui NUEVO AJAX

	


          $.ajax({
                data: {'cirugiaId':cirugiaId},
	        url: "/buscarProcedimientosMaterialesDeCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	  	    var options = '<option value="=================="></option>';



	            const $id7 = document.querySelector("#procedMaterialesInforme");
 	      	$("#procedMaterialesInforme").empty();

	                 $.each(data2, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id7.appendChild(option);
 	      		      });


            $('#modelHeadingMaterialInformeCirugia').html("Adicion de materiales a Cirugia");
            $('#crearModelMaterialInformeCirugia').modal('show');

		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] =document.getElementById("cirugiaIdModalProcedimientos").value ;
	        data = JSON.stringify(data);
	  
	    arrancaCirugia(13,data);
	    dataTableMaterialInformeXXCirugiaInitialized = true; 

                },
         error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });

// FIN AJAX 	
      
  };






function CrearHojaDeGastoCirugia()
{

	// alert("CrearHojaDeGastoCirugia");

	var sede = document.getElementById("sede").value;

	var user  = document.getElementById("username_id").value ;
	var cirugiaIdModalHojaDeGastoCirugia  = document.getElementById("cirugiaIdModalHojaDeGastoCirugia").value ;

            $.ajax({
                data: $('#postFormHojaDeGastoCirugia').serialize(),
	        url: "/crearHojaDeGastoCirugia/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		  
                  $('#postFormHojaDeGastoCirugia').trigger("reset");

	   document.getElementById("cirugiaIdModalHojaDeGastoCirugia").value = cirugiaIdModalHojaDeGastoCirugia;
	 document.getElementById("usernameHojaDeGastoCirugia_id").value =  user;

		var data =  {}   ;
	        data['username'] = username;
  	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
			
		data['cirugiaId'] =cirugiaIdModalHojaDeGastoCirugia;
	        data = JSON.stringify(data);
	

	     arrancaCirugia(14,data);
	    dataTableHojaDeGastoCirugiaInitialized = true;
	     arrancaCirugia(15,data);
	    dataTableHojaDeGastoXXCirugiaInitialized = true;
	  
	  

 		// $('#crearModelHojaDeGastoCirugia').modal('hide');
		 $("#mensajesModalHojaDeGastoCirugia").html(data2.message);

                },
        error: function (data) {
	   			    	document.getElementById("mensajesErrorModalHojaDeGastoCirugia").value =   data.responseText;

	   	    	}
            });


}

function GenerarLiquidacionCirugia()
{

	// alert("GenerarLiquidacionCirugia");
	var username_id  = document.getElementById("username_id").value ;
	var sede  = document.getElementById("sede").value ;

	var cirugiaId  = document.getElementById("cirugiaIdModalInformeProcedimientos").value ;

            $.ajax({

	        url: "/generarLiquidacionCirugia/",
                data: {'cirugiaId':cirugiaId,'sede':sede, 'username_id':username_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

		if (data2.sucess == 'False')
		{
		 $("#mensajesError").html(data2.Mensajes);
		 return;
		}
		else
		{
		 $("#mensajes").html(data2.Mensajes);

		}

	



                },
     error: function (data) {
	   			    	document.getElementById("mensajesError").value =   data.responseText;

	   	    	}
            });


}

$(document).on('change', '#unitarioLiquidacionInforme', function(event) {

      


       var cantidadInforme =   document.getElementById("cantidadInforme").value;
       var unitarioLiquidacionInforme =   document.getElementById("unitarioLiquidacionInforme").value;
	document.getElementById("valorLiquidacionSolicitud").value = cantidadInforme * unitarioLiquidacionInforme;

});


$(document).on('change', '#unitarioLiquidacionInforme', function(event) {

      


       var cantidad =   document.getElementById("cantidad").value;
       var unitarioLiquidacion =   document.getElementById("unitarioLiquidacion").value;
	document.getElementById("valorLiquidacionSolicitud").value = cantidad * unitarioLiquidacion;

});


