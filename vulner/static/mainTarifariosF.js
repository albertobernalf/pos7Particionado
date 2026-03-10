console.log('Hola Alberto Hi!')


let dataTable;
let dataTableB;
let dataTableC;
let dataTableTarifariosProcedimientosInitialized = false;
let dataTableTarifariosSuministrosInitialized = false;
let dataTableTarifariosDescripcionProcedimientosInitialized = false;
let dataTableTarifariosDescripcionSuministrosInitialized = false;



function arrancaTarifarios(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsProcedimientos  ={
 
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
            scrollY: '125px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
	    { width: '10%', targets: [9,15] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
             btn = btn + " <input type='radio' name='miProcedimientos' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miProcedimientos form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

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
                 url:"/load_dataTarifariosProcedimientos/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
                { data: "fields.id"},
                { data: "fields.tipoTarifa"},
                { data: "fields.cups"},
                { data: "fields.codigoHomologado"},
                { data: "fields.exaNombre"},
                { data: "fields.colValorBase"},
                { data: "fields.colValor1"},
                { data: "fields.colValor2"},
                { data: "fields.colValor3"},
                { data: "fields.colValor4"},
                { data: "fields.colValor5"},
                { data: "fields.colValor6"},
                { data: "fields.colValor7"},
                { data: "fields.colValor8"},
                { data: "fields.colValor9"},
                { data: "fields.colValor10"},
            ]
            }
	        dataTable = $('#tablaTarifariosProcedimientos').DataTable(dataTableOptionsProcedimientos);


  }

    if (valorTabla == 2)
    {

        let dataTableOptionsSuministros  ={

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
		{     "render": function ( data, type, row ) {
                        var btn = '';
                      btn = btn + " <button class='miSuministro btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa fa-pencil"></i>' + "</button>";
                       return btn;
                    },
                    "targets":18
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
                 url:"/load_datatarifariosSuministros/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	          { data: "fields.id"},
                { data: "fields.codigoHomologado"},
                { data: "fields.tiposTarifa_id"},
                { data: "fields.codigoCum_id"},
                { data: "fields.concepto_id"},
                { data: "fields.colValor1"},
                { data: "fields.colValor2"},
                { data: "fields.colValor3"},
                { data: "fields.colValor4"},
                { data: "fields.colValor5"},
                { data: "fields.colValor6"},
                { data: "fields.colValor7"},
                { data: "fields.colValor8"},
                { data: "fields.colValor9"},
                { data: "fields.colValor10"},
                { data: "fields.usuarioRegistro_id"},
                { data: "fields.fechaRegistro"},
                { data: "fields.estadoReg"},
                     ]
            }

            if  (dataTableTarifariosSuministrosInitialized)  {

		            dataTableB = $("#tablaTarifariosSuministros").dataTable().fnDestroy();

                    }

                dataTableB = $('#tablaTarifariosSuministros').DataTable(dataTableOptionsSumnistros);

	            dataTableTarifariosSuministrosInitialized  = true;
      }


    if (valorTabla == 3)
    {
        let dataTableOptionsHonorarios  ={

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
	    { width: '10%', targets: [9,15] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
             btn = btn + " <input type='radio' name='miHonorarios' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miHonorarios form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


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
                 url:"/load_dataTarifariosHonorarios/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
                { data: "fields.id"},
                { data: "fields.sedesClinica_id"},

                { data: "fields.paciente"},
                { data: "fields.folio"},
                { data: "fields.fechaSolicitud"},

                { data: "fields.numeroAutorizacion"},
                { data: "fields.fechaAutorizacion"},
                { data: "fields.medico"},
                { data: "fields.observaciones"},
                { data: "fields.estadoAutorizacion"},
                { data: "fields.numeroSolicitud"},
                { data: "fields.fechaVigencia"},
                { data: "fields.empresa_id"},
                { data: "fields.empresaNombre"},
                { data: "fields.plantaOrdena_id"},
                { data: "fields.usuarioRegistro_id"},
            ]
            }
	        dataTable = $('#tablaTarifariosHonorarios').DataTable(dataTableOptionsHonorarios);


  }

    if (valorTabla == 4)
    {

        let dataTableOptionsDescripcionProcedimientos  ={
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '120px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
 			 btn = btn + " <input type='radio' name='miDescripcionProcedimiento' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miDescripcionProcedimiento form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
          		   btn = btn + " <button class='miAplicarProcedimientos btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
                    "targets":6
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
                 url:"/load_datatarifariosDescripcionProcedimientos/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	          { data: "fields.id"},
	          { data: "fields.tipTarId"},
                { data: "fields.tipo"},
                { data: "fields.tipoTarifa"},
                { data: "fields.columna"},
                { data: "fields.descripcion"},
                     ]
            }

            if  (dataTableTarifariosDescripcionProcedimientosInitialized)  {

		            dataTableB = $("#tablaTarifariosDescripcionProcedimientos").dataTable().fnDestroy();

                    }

                dataTableC = $('#tablaTarifariosDescripcionProcedimientos').DataTable(dataTableOptionsDescripcionProcedimientos);

	            dataTableTarifariosDescripcionProcedimientosInitialized  = true;
      }




    if (valorTabla == 5)
    {
        let dataTableOptionsSuministros  ={

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
            scrollY: '125px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
	    { width: '10%', targets: [2,3] },
	    { width: '10%', targets: [9,15] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
             btn = btn + " <input type='radio' name='miSuministros' class='miSuministros style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

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
                 url:"/load_dataTarifariosSuministros/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
                { data: "fields.id"},
                { data: "fields.tipoTarifa"},
                { data: "fields.cums"},
                { data: "fields.codigoHomologado"},
                { data: "fields.exaNombre"},
                { data: "fields.colValorBase"},
                { data: "fields.colValor1"},
                { data: "fields.colValor2"},
                { data: "fields.colValor3"},
                { data: "fields.colValor4"},
                { data: "fields.colValor5"},
                { data: "fields.colValor6"},
                { data: "fields.colValor7"},
                { data: "fields.colValor8"},
                { data: "fields.colValor9"},
                { data: "fields.colValor10"},
            ]
            }
	        dataTable = $('#tablaTarifariosSuministros').DataTable(dataTableOptionsSuministros);


  }


    if (valorTabla == 6)
    {

        let dataTableOptionsDescripcionSuministros  ={
  lengthMenu: [2, 4, 15],
           processing: true,
            serverSide: false,
            scrollY: '120px',
	    scrollX: true,
	    scrollCollapse: true,
            paging:false,
            columnDefs: [
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{     "render": function ( data, type, row ) {
                        var btn = '';
 			 btn = btn + " <input type='radio' name='miDescripcionSuministro' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miDescripcionSuministro form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
          		   btn = btn + " <button class='miAplicarSuministro btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";

                       return btn;
                    },
                    "targets":5
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
                 url:"/load_datatarifariosDescripcionSuministros/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
	          { data: "fields.id"},
                { data: "fields.tipo"},
                { data: "fields.tipoTarifa"},
                { data: "fields.columna"},
                { data: "fields.descripcion"},
                     ]
            }

            if  (dataTableTarifariosDescripcionSuministrosInitialized)  {

		            dataTableB = $("#tablaTarifariosDescripcionSuministros").dataTable().fnDestroy();

                    }

                dataTableC = $('#tablaTarifariosDescripcionSuministros').DataTable(dataTableOptionsDescripcionSuministros);

	            dataTableTarifariosDescripcionSuministrosInitialized  = true;
      }








}
	
const initDataTableTarifariosDescripcionProcedimientos = async () => {
	if  (dataTableTarifariosDescripcionProcedimientosInitialized)  {
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
	tiposTarifa_id = 1
        data['tiposTarifa_id'] = tiposTarifa_id;
        data['tiposTarifaSuministros_id'] = 8;

 	    data = JSON.stringify(data);

        arrancaTarifarios(4,data);
	    dataTableTarifariosDescripcionProcedimientosInitialized = true;

        arrancaTarifarios(1,data);
	    dataTableTarifariosProcedimientosInitialized = true;



   		 arrancaTarifarios(5,data);
	
	    dataTableTarifariosSuministrosInitialized = true;

     		  arrancaTarifarios(6,data);
	    dataTableTarifariosDescripcionSuministrosInitialized = true;

}


 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableTarifariosDescripcionProcedimientos();
	 $('#tablaTarifariosDescripcionProcedimientos tbody tr:eq(0) .miProcedimientos').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript


});


 /* FIN ONLOAD */



 $('#tablaTarifariosProcedimientos tbody').on('click', '.miProcedimientos', function() {

        var post_id = $(this).data('pk');
        var row = $(this).closest('tr'); // Encuentra la fila

	alert("Ingrese Modal Editar Procedimiento" + post_id);


        var username_id = document.getElementById("username_id").value;

            $.ajax({

	        url: "/traerTarifarioProcedimientos/",
	    	data: {'post_id': post_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

                  alert("llegue con data = " + data2[0]);

	        alert("llegue con id = " + data2[0].fields.id);

	    $('#post_id').val('');
            $('#postFormEditarTarifarioProcedimientos').trigger("reset");
            $('#modelHeadingEditarTarifarioProcedimientos').html("Editar Tarifario Procedimientos");

  		 $('#postEditar1_id').val(data2[0].fields.id);
 		 $('#codigoHomologadoEditar').val(data2[0].fields.codigoHomologado);
 		 $('#colValorBaseEditar').val(data2[0].fields.colValorBase);
 		 $('#colValor1Editar').val(data2[0].fields.colValor1);
 		 $('#colValor2Editar').val(data2[0].fields.colValor2);
 		 $('#colValor3Editar').val(data2[0].fields.colValor3);
 		 $('#colValor4Editar').val(data2[0].fields.colValor4);
 		 $('#colValor5Editar').val(data2[0].fields.colValor5);
 		 $('#colValor6Editar').val(data2[0].fields.colValor6);
 		 $('#colValor7Editar').val(data2[0].fields.colValor7);
 		 $('#colValor8Editar').val(data2[0].fields.colValor8);
 		 $('#colValor9Editar').val(data2[0].fields.colValor9);
 		 $('#colValor10Editar').val(data2[0].fields.colValor10);
		$('#codigoCupsU').val(data2[0].fields.codigoCups);
		$('#exaNombre').val(data2[0].fields.exaNombre);
		$('#tiposTarifaU').val(data2[0].fields.tiposTarifa_id);


            $('#crearModelEditarTarifarioProcedimientos').modal('show');


		   $("#mensajes").html(data2.message);
                         },
               error: function (request, status, error) {
	   			    $("#mensajes").html(" !  Reproduccion  con error !");
	   	    	}
            });


  });




$('#tablaTarifariosDescripcionProcedimientos tbody').on('click', '.miAplicarProcedimientos', function() {

        alert(" Entre miAplicarProcedimientos ");

        var post_id = $(this).data('pk');
	    var row = $(this).closest('tr'); // Encuentra la fila

	    var table = $('#tablaTarifariosDescripcionProcedimientos').DataTable();  // Inicializa el DataTable jquery

	    var rowindex = table.row(row).data(); // Obtiene los datos de la fila


	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato3 columna = " , dato3.columna);
	        console.log ( "dato3  descripcion = " , dato3.descripcion);
	        console.log ( "dato3 = tipoTarifa " , dato3.tipoTarifa);
            $('#postFormAplicarTarifario').trigger("reset");

	        $('#post_id').val(dato3.columna);
	         $('#columnaAplicar').val(dato3.columna);
	          $('#descripcionTarifario').val(dato3.descripcion);
	           $('#tiposTarifaTarifario_id').val(dato3.tipoTarifa);
		  $('#post_idProcedimientosDesc').val(dato3.id);


            $('#modelHeadingAplicarTarifario').html("Aplicar Tarifarios");
            $('#crearModelAplicarTarifario').modal('show');

  });

$('#tablaTarifariosDescripcionProcedimientos tbody').on('click', '.miDescripcionProcedimiento', function() {


       		 var post_id = $(this).data('pk');

	alert ("selecciono id descripcionProc: " + post_id);

	    var row = $(this).closest('tr'); // Encuentra la fila
	    var table = $('#tablaTarifariosDescripcionProcedimientos').DataTable();  // Inicializa el DataTable jquery

	    var rowindex = table.row(row).data(); // Obtiene los datos de la fila


	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato3 columna = " , dato3.columna);
	        console.log ( "dato3  descripcion = " , dato3.descripcion);
	        console.log ( "dato3 = tipoTarifa " , dato3.id);


	    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;

		document.getElementById("post_idProcedimientosDesc").value = post_id;


		alert("este dato = " + document.getElementById("post_idProcedimientosDesc").value);

	         var data =  {}   ;
	        data['username'] = username;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['username_id'] = username_id;
	        data['tiposTarifa_id'] = dato3.id;

 		data = JSON.stringify(data);
  

        arrancaTarifarios(1,data);
	    dataTableTarifariosProcedimientosInitialized = true;

  });




function CerrarModalJson()
{

            $('#crearModelRipsJson').modal('hide');
}

function CrearItemTarifario()
{
	alert("Ingrese crear Item Tarifario");


	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
    	var username_id = document.getElementById("username_id").value;

 	var codigoHomologadoItem = document.getElementById("codigoHomologadoItem").value;
 	var tiposTarifaItem_id = document.getElementById("tiposTarifaItem_id").value;
 	var codigoCupsItem_id = document.getElementById("codigoCupsItem_id").value;

 	var colValorBaseItem = document.getElementById("colValorBaseItem").value;
 	var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativosX").value;



        var username_id = document.getElementById("username_id").value;

            $.ajax({

	        url: "/crearItemTarifario/",

	    	data: {'codigoHomologadoItem':codigoHomologadoItem , 'tiposTarifaItem_id' :tiposTarifaItem_id, 'codigoCupsItem_id' : codigoCupsItem_id, 'colValorBaseItem':colValorBaseItem, 'username_id': username_id,'serviciosAdministrativos_id':serviciosAdministrativos_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifaItem_id;
	        data = JSON.stringify(data);

     	 arrancaTarifarios(1,data);
	    dataTableTarifariosProcedimientosInitialized = true;



		document.getElementById("mensajesError").innerHTML = data2.message;

		$('#codigoHomologadoItem').val('');
		$('#colValorBaseItem').val('0');
		$('#codigoCupsItem_id').val('');




                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });



}

function AplicarTarifario()
{

	

	var post_id = document.getElementById("post_id").value ;
	var tiposTarifaTarifario_id = document.getElementById("tiposTarifaTarifario_id").value ;
	var porcentaje = document.getElementById("porcentaje").value ;
	var post_idProcedimientosDesc = document.getElementById("post_idProcedimientosDesc").value ;
	var descripcionTarifario = document.getElementById("descripcionTarifario").value ;

alert("Ingrese Grabar Item Tarifario e la descripcion :" + post_id);

	var porcentaje = document.getElementById("porcentaje").value ;
	var valorAplicar = document.getElementById("valorAplicar").value ;
	var columnaAplicar = document.getElementById("columnaAplicar").value ;
	var codigoCups_id = document.getElementById("codigoCups_id").value ;
	var codigoCupsHasta_id = document.getElementById("codigoCupsHasta_id").value ;

	var serviciosAdministrativosO = document.getElementById("serviciosAdministrativosO_id").value ;


	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	alert("serviciosAdministrativosO = " +  serviciosAdministrativosO);

            $.ajax({

	        url: "/aplicarTarifas/",
		data: {'post_id' : post_id, 'tiposTarifaTarifario_id':tiposTarifaTarifario_id, 'porcentaje':porcentaje,'valorAplicar':valorAplicar,
		'columnaAplicar':columnaAplicar,'codigoCupsHasta_id':codigoCupsHasta_id,'codigoCups_id':codigoCups_id,'serviciosAdministrativosO':serviciosAdministrativosO ,'post_idProcedimientosDesc':post_idProcedimientosDesc,'descripcionTarifario':descripcionTarifario},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifaTarifario_id;
	        data = JSON.stringify(data);

		document.getElementById("mensajesError").innerHTML = data2.message;

		    	  $('#crearModelAplicarTarifario').modal('hide');
    
        arrancaTarifarios(4,data);
	    dataTableTarifariosDescripcionProcedimientosInitialized = true;

                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

}

function ModalDescripcionProcedimiento()
{

	alert("Ingrese Modal Descripcion Procedimiento");

	    $('#post_id').val('');
            $('#postFormDescripcionProcedimientos').trigger("reset");
            $('#modelHeadingDescripcionProcedimientos').html("Descripcion Procedimientos");
            $('#crearModelDescripcionProcedimientos').modal('show');

}


function GuardarDescripcionProcedimientos()
{
	alert("Ingrese GuardarDescripcionProcedimientos");

	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var tiposTarifa_id = document.getElementById("tiposTarifa_id").value;
        var columna = document.getElementById("columna").value;
        var descripcion = document.getElementById("descripcion").value;
        var serviciosAdministrativos = document.getElementById("serviciosAdministrativos").value;



            $.ajax({

	        url: "/guardarDescripcionProcedimientos/",
		    data: {'tiposTarifa_id':tiposTarifa_id,'columna':columna, 'descripcion':descripcion,'serviciosAdministrativos':serviciosAdministrativos},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
	        data = JSON.stringify(data);

     		  arrancaTarifarios(4,data);
	    dataTableTarifariosDescripcionProcedimientosInitialized = true;
	

		document.getElementById("mensajesError").innerHTML = data2.message;
 	  $('#crearModelDescripcionProcedimientos').modal('hide');


                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

}

function ModalCrearTarifarioProcedimientos()
{

	alert("Ingrese Modal Descripcion Procedimiento");

	    $('#post_id').val('');
            $('#postFormCrearTarifarioProcedimientos').trigger("reset");
            $('#modelHeadingCrearTarifarioProcedimientos').html("Crear Tarifario sabana Procedimientos");
            $('#crearModelCrearTarifarioProcedimientos').modal('show');

}



function CrearTarifarioProcedimientos()
{

	alert("Ingrese CrearTarifarioProcedimientos");
	    var post_id = $(this).data('pk');


	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var username_id = document.getElementById("username2_id").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var tiposTarifa1_id = document.getElementById("tiposTarifa1_id").value;
	var usuarioRegistro_id = document.getElementById("usuarioRegistro_id").value;
	var serviciosAdministrativosC_id = document.getElementById("serviciosAdministrativosC").value;

	var rutaArchivo = document.getElementById("rutaArchivo").value;

	    alert( "este es eltiposTarifa1_id QUE VOY A CREAR  =" + tiposTarifa1_id) ;


            $.ajax({

	        url: "/crearTarifarioProcedimientos/",
    		data: {'tiposTarifa_id':tiposTarifa1_id,'username_id':username_id,'serviciosAdministrativosC_id':serviciosAdministrativosC_id ,'rutaArchivo':rutaArchivo},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifa1_id;
	        data = JSON.stringify(data);

     		  arrancaTarifarios(4,data);
	    dataTableTarifariosDescripcionProcedimientosInitialized = true;
	
     		  arrancaTarifarios(1,data);
	    dataTableTarifariosProcedimientosInitialized = true;




		document.getElementById("mensajesError").innerHTML = data2.message;
 	  $('#crearModelCrearTarifarioProcedimientos').modal('hide');


                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

} 

function GuardarEditarTarifarioProcedimientos()
{



	var post_id = document.getElementById("postEditar1_id").value;

	// alert("Entre GuardarEditarTarifarioProcedimientos" +  post_id);


	var username_id = document.getElementById("username_id").value;
	var codigoHomologadoEditar = document.getElementById("codigoHomologadoEditar").value;
	var colValorBaseEditar = document.getElementById("colValorBaseEditar").value;
	var colValor1Editar = document.getElementById("colValor1Editar").value;
	var colValor2Editar = document.getElementById("colValor2Editar").value;
	var colValor3Editar = document.getElementById("colValor3Editar").value;
	var colValor4Editar = document.getElementById("colValor4Editar").value;
	var colValor5Editar = document.getElementById("colValor5Editar").value;
	var colValor6Editar = document.getElementById("colValor6Editar").value;
	var colValor7Editar = document.getElementById("colValor7Editar").value;
	var colValor8Editar = document.getElementById("colValor8Editar").value;
	var colValor9Editar = document.getElementById("colValor9Editar").value;
	var colValor10Editar = document.getElementById("colValor10Editar").value;
	var tiposTarifaU = document.getElementById("tiposTarifaU").value;

            $.ajax({

	        url: "/guardarEditarTarifarioProcedimientos/",
    		data: {'post_id':post_id, 'codigoHomologadoEditar':codigoHomologadoEditar,'colValorBaseEditar':colValorBaseEditar,
				'colValor1Editar':colValor1Editar,'colValor2Editar':colValor2Editar,'colValor3Editar':colValor3Editar,'colValor4Editar':colValor4Editar,
				'colValor5Editar':colValor5Editar,'colValor6Editar':colValor6Editar,'colValor7Editar':colValor7Editar,'colValor8Editar':colValor8Editar,
				'colValor9Editar':colValor9Editar,'colValor10Editar':colValor10Editar,'username_id':username_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifaU;
	        data = JSON.stringify(data);

     		  arrancaTarifarios(4,data);
	    dataTableTarifariosDescripcionProcedimientosInitialized = true;
     		  arrancaTarifarios(1,data);
	    dataTableTarifariosProcedimientosInitialized = true;
	    dataTableTarifariosProcedimientosInitialized = true;


		document.getElementById("mensajesError").innerHTML = data2.message;
 	  $('#crearModelEditarTarifarioProcedimientos').modal('hide');

                         },
               error: function (request, status, error) {
			document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

}

function ModalCrearTarifarioSuministros()
{

	alert("Ingrese Modal Descripcion Suministros");

	    $('#post_id').val('');
            $('#postFormCrearTarifarioSuministros').trigger("reset");
            $('#modelHeadingCrearTarifarioSuministros').html("Crear Tarifario sabana Suministros");
            $('#crearModelCrearTarifarioSuministros').modal('show');

}


function CrearTarifarioSuministros()
{

	alert("Ingrese CrearTarifarioSuministros");
	    var post_id = $(this).data('pk');

	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var username_id = document.getElementById("username2_id").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var tiposTarifa_id = document.getElementById("tiposTarifaSuministros2_id").value;
	var usuarioRegistro_id = document.getElementById("usuarioRegistro_id").value;
	var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativosY").value;


	var rutaArchivo = document.getElementById("rutaArchivoSuministros").value;

	    alert( "este es eltiposTarifa1_id QUE VOY A CREAR  =" + tiposTarifa1_id) ;


            $.ajax({

	        url: "/crearTarifarioSuministros/",
    		data: {'tiposTarifa_id':tiposTarifa_id,'username_id':username_id,'serviciosAdministrativos_id':serviciosAdministrativos_id, 'rutaArchivoSuministros':rutaArchivo},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifa_id;
	        data = JSON.stringify(data);

     		  arrancaTarifarios(6,data);
	    dataTableTarifariosDescripcionSuministrosInitialized = true;
	
     		  arrancaTarifarios(5,data);
	    dataTableTarifariosSuministrosInitialized = true;



		
		document.getElementById("mensajesError").innerHTML = data2.message;
 	  $('#crearModelCrearTarifarioSuministros').modal('hide');


                         },
               error: function (request, status, error) {
			document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

} 

function ModalDescripcionSuministros()
{

	alert("Ingrese Modal Descripcion Suministros");

	    $('#post_id').val('');
            $('#postFormDescripcionSuministros').trigger("reset");
            $('#modelHeadingDescripcionSuministros').html("Descripcion Suministros");
            $('#crearModelDescripcionSuministros').modal('show');

}

function GuardarDescripcionSuministros()
{
	alert("Ingrese GuardarDescripcionSuministros");

	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var tiposTarifa_id = document.getElementById("tiposTarifaSuministros1_id").value;
        var columna = document.getElementById("columna").value;
        var descripcion = document.getElementById("descripcionSuministros").value;
        var serviciosAdministrativosS = document.getElementById("serviciosAdministrativosS").value;



            $.ajax({

	        url: "/guardarDescripcionSuministros/",
		data: {'tiposTarifa_id':tiposTarifa_id,'columna':columna, 'descripcion':descripcion,'serviciosAdministrativosS':serviciosAdministrativosS},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifa_id;
	        data = JSON.stringify(data);

		alert ("Regrese de guardar descripcion suministro");


     		  arrancaTarifarios(6,data);
	    dataTableTarifariosDescripcionSuministrosInitialized = true;
	
     		  arrancaTarifarios(5,data);
	    dataTableTarifariosSuministrosInitialized = true;



		document.getElementById("mensajesError").innerHTML = data2.message;
 	  $('#crearModelDescripcionSuministros').modal('hide');


                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

}


$('#tablaTarifariosDescripcionSuministros tbody').on('click', '.miAplicarSuministro', function() {

        alert(" Entre miAplicarSuministros ");

        var post_id = $(this).data('pk');
	    var row = $(this).closest('tr'); // Encuentra la fila

	    var table = $('#tablaTarifariosDescripcionSuministros').DataTable();  // Inicializa el DataTable jquery

	    var rowindex = table.row(row).data(); // Obtiene los datos de la fila


	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato3 columna = " , dato3.columna);
	        console.log ( "dato3  descripcion = " , dato3.descripcion);
	        console.log ( "dato3 = tipoTarifa " , dato3.tipoTarifa);
            $('#postFormAplicarTarifarioSuministros').trigger("reset");

	        $('#post_id').val(dato3.columna);
	         $('#columnaAplicarSuministros').val(dato3.columna);
	          $('#descripcionTarifarioSuministros').val(dato3.descripcion);
	           $('#tiposTarifaTarifarioSuministros_id').val(dato3.tipoTarifa);


            $('#modelHeadingAplicarTarifarioSuministros').html("Aplicar Tarifarios Suministros");
            $('#crearModelAplicarTarifarioSuministros').modal('show');

  });

$('#tablaTarifariosDescripcionSuministros tbody').on('click', '.miDescripcionSuministro', function() {

	alert("Entre descripcon suministro");


        var post_id = $(this).data('pk');
	    var row = $(this).closest('tr'); // Encuentra la fila
	    var table = $('#tablaTarifariosDescripcionSuministros').DataTable();  // Inicializa el DataTable jquery

	    var rowindex = table.row(row).data(); // Obtiene los datos de la fila


	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato3 columna = " , dato3.columna);
	        console.log ( "dato3  descripcion = " , dato3.descripcion);
	        console.log ( "dato3 = tipoTarifa " , dato3.id);


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
	        data['tiposTarifa_id'] = dato3.id;

 		data = JSON.stringify(data);

        arrancaTarifarios(5,data);
	    dataTableTarifariosSuministrosInitialized = true;

  });



function AplicarTarifarioSuministros()
{
	alert("Ingrese Grabar Tarifario Suministros");


	var post_id = document.getElementById("post_id").value ;
	var tiposTarifaTarifario_id = document.getElementById("tiposTarifaTarifarioSuministros_id").value ;

	var porcentaje = document.getElementById("porcentajeSuministros").value ;
	var valorAplicar = document.getElementById("valorAplicarSuministros").value ;
	var columnaAplicar = document.getElementById("columnaAplicarSuministros").value ;
	var codigoCums_id = document.getElementById("codigoCums_id").value ;
	var codigoCumsHasta_id = document.getElementById("codigoCumsHasta_id").value ;


	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;


            $.ajax({

	        url: "/aplicarTarifasSuministros/",
		data: {'post_id' : post_id, 'tiposTarifaTarifario_id':tiposTarifaTarifario_id, 'porcentaje':porcentaje,'valorAplicar':valorAplicar,
		'columnaAplicar':columnaAplicar,'codigoCumsHasta_id':codigoCumsHasta_id,'codigoCums_id':codigoCums_id },
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifaTarifario_id;
	        data = JSON.stringify(data);



		   $("#mensajes").html(data2.message);
		document.getElementById("mensajesError").innerHTML = data2.message;

		    	  $('#crearModelAplicarTarifario').modal('hide');


                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

}

function CrearItemTarifarioSuministros()
{
	alert("Ingrese crear Item Tarifario Suministros");


	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
    	var username_id = document.getElementById("username_id").value;

 	var codigoHomologadoItem = document.getElementById("codigoHomologadoItemSuministros").value;
 	var tiposTarifaItem_id = document.getElementById("tiposTarifaItemSuministros_id").value;
 	var codigoCumsItem_id = document.getElementById("codigoCumsItem_id").value;

 	var colValorBaseItem = document.getElementById("colValorBaseItemSuministros").value;
 	var serviciosAdministrativos_id = document.getElementById("serviciosAdministrativosIt_id").value;



        var username_id = document.getElementById("username_id").value;

            $.ajax({

	        url: "/crearItemTarifarioSuministros/",

	    	data: {'codigoHomologadoItem':codigoHomologadoItem , 'tiposTarifaItem_id' :tiposTarifaItem_id, 
			'codigoCumsItem_id' : codigoCumsItem_id, 'colValorBaseItem':colValorBaseItem, 'username_id': username_id,'serviciosAdministrativos_id':serviciosAdministrativos_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifaItem_id;
	        data = JSON.stringify(data);

     	 arrancaTarifarios(5,data);
	    dataTableTarifariosProcedimientosInitialized = true;


		   $("#mensajes").html(data2.message);

		$('#codigoHomologadoItemSuministros').val('');
		$('#colValorBaseItemSuministros').val('0');
		$('#codigoCupsItemSuministros_id').val('');




                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });



}


 $('#tablaTarifariosSuministros tbody').on('click', '.miSuministros', function() {

        var post_id = $(this).data('pk');
        var row = $(this).closest('tr'); // Encuentra la fila

	alert("Ingrese Modal Editar Suministro" + post_id);


        var username_id = document.getElementById("username_id").value;

            $.ajax({

	        url: "/traerTarifarioSuministros/",
	    	data: {'post_id': post_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {

                  alert("llegue con data = " + data2[0]);

	        alert("llegue con id = " + data2[0].fields.id);

	    $('#post_id').val('');
            $('#postFormEditarTarifarioSuministros').trigger("reset");
            $('#modelHeadingEditarTarifarioSuministros').html("Editar Tarifario Suministros");

  		 $('#postEditar1_id').val(data2[0].fields.id);
 		 $('#codigoHomologadoEditarSuministros').val(data2[0].fields.codigoHomologado);
 		 $('#colValorBaseEditarSuministros').val(data2[0].fields.colValorBase);
 		 $('#colValor1EditarSuministros').val(data2[0].fields.colValor1);
 		 $('#colValor2EditarSuministros').val(data2[0].fields.colValor2);
 		 $('#colValor3EditarSuministros').val(data2[0].fields.colValor3);
 		 $('#colValor4EditarSuministros').val(data2[0].fields.colValor4);
 		 $('#colValor5EditarSuministros').val(data2[0].fields.colValor5);
 		 $('#colValor6EditarSuministros').val(data2[0].fields.colValor6);
 		 $('#colValor7EditarSuministros').val(data2[0].fields.colValor7);
 		 $('#colValor8EditarSuministros').val(data2[0].fields.colValor8);
 		 $('#colValor9EditarSuministros').val(data2[0].fields.colValor9);
 		 $('#colValor10EditarSuministros').val(data2[0].fields.colValor10);
		$('#codigoCumsUSuministros').val(data2[0].fields.codigoCums);
		$('#exaNombreSuministros').val(data2[0].fields.exaNombre);
		$('#tiposTarifaUSuministros').val(data2[0].fields.tiposTarifa_id);


            $('#crearModelEditarTarifarioSuministros').modal('show');


		   $("#mensajes").html(data2.message);
			document.getElementById("mensajesError").innerHTML = data2.message;
                         },
               error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });


  });


function GuardarEditarTarifarioSuministros()
{
	alert("Entre GuardarEditarTarifarioSuministros");


	var post_id = document.getElementById("postEditar1_id").value;
	var username_id = document.getElementById("username_id").value;
	var codigoHomologadoEditar = document.getElementById("codigoHomologadoEditarSuministros").value;
	var colValorBaseEditar = document.getElementById("colValorBaseEditarSuministros").value;
	var colValor1Editar = document.getElementById("colValor1EditarSuministros").value;
	var colValor2Editar = document.getElementById("colValor2EditarSuministros").value;
	var colValor3Editar = document.getElementById("colValor3EditarSuministros").value;
	var colValor4Editar = document.getElementById("colValor4EditarSuministros").value;
	var colValor5Editar = document.getElementById("colValor5EditarSuministros").value;
	var colValor6Editar = document.getElementById("colValor6EditarSuministros").value;
	var colValor7Editar = document.getElementById("colValor7EditarSuministros").value;
	var colValor8Editar = document.getElementById("colValor8EditarSuministros").value;
	var colValor9Editar = document.getElementById("colValor9EditarSuministros").value;
	var colValor10Editar = document.getElementById("colValor10EditarSuministros").value;
	var tiposTarifaU = document.getElementById("tiposTarifaUSuministros").value;

            $.ajax({

	        url: "/guardarEditarTarifarioSuministros/",
    		data: {'post_id':post_id, 'codigoHomologadoEditar':codigoHomologadoEditar,'colValorBaseEditar':colValorBaseEditar,
				'colValor1Editar':colValor1Editar,'colValor2Editar':colValor2Editar,'colValor3Editar':colValor3Editar,'colValor4Editar':colValor4Editar,
				'colValor5Editar':colValor5Editar,'colValor6Editar':colValor6Editar,'colValor7Editar':colValor7Editar,'colValor8Editar':colValor8Editar,
				'colValor9Editar':colValor9Editar,'colValor10Editar':colValor10Editar,'username_id':username_id},
                type: "POST",
                dataType: 'json',
                success: function (data2) {
	
		var data =  {}   ;
	        data['username'] = username;
	       data['sedeSeleccionada'] = sedeSeleccionada;
	       data['nombreSede'] = nombreSede;
	      data['sede'] = sede;
	        data['username_id'] = username_id;
		 data['tiposTarifa_id'] = tiposTarifaU;
	        data = JSON.stringify(data);


     		  arrancaTarifarios(6,data);
	    dataTableTarifariosDescripcionSuministrosInitialized = true;
     		  arrancaTarifarios(5,data);
	    dataTableTarifariosSuministrosInitialized = true;


		   $("#mensajes").html(data2.message);
 	  $('#crearModelEditarTarifarioSuministros').modal('hide');

                         },
               error: function (request, status, error) {
			document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
            });

}

