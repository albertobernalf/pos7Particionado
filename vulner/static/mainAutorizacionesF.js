console.log('Hola Alberto Hi!')


let dataTable;
let dataTableB;
let dataTableAutorizacionesInitialized = false;
let dataTableAutorizacionesDetalleInitialized = false;


function arrancaAutorizaciones(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptions  ={
  
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
                 url:"/load_dataAutorizaciones/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{

 "render": function ( data, type, row ) {
                        var btn = '';
             btn = btn + " <input type='radio' name='miAutorizacion' class='miAutorizacion form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },
                 },
        {
		"render": function ( data, type, row ) {
                        var btn = '';

	 	 btn = btn + " <button class='ImprimirAutorizacion btn-primary ' data-pk='" + row.pk + "'>" + '<i class=""fa-duotone fa-solid fa-print""></i>' + "</button>";

                       return btn;
		}
                   },

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
	        dataTable = $('#tablaAutorizaciones').DataTable(dataTableOptions);

       // 	$('#tablaAutorizaciones tbody tr:eq(0) .miAutorizacion').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript



  }

    if (valorTabla == 2)
    {

        let dataTableOptionsAutorizacionesDetalle  ={

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
                      btn = btn + " <button class='miAutorizacionDetalle btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa fa-pencil"></i>' + "</button>";
                       return btn;
                    },
                    "targets":12
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
                 url:"/load_dataAutorizacionesDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
                { data: "fields.tipoTipoExamen"},
                { data: "fields.id"},
                { data: "fields.tipoExamen"},
                { data: "fields.examenId"},
                { data: "fields.examen"},
                { data: "fields.cantidadSolicitada"},
                { data: "fields.cantidadAutorizada"},
                { data: "fields.valorSolicitado"},
                { data: "fields.valorAutorizado"},
                { data: "fields.autorizado"},
                { data: "fields.mipres"},
                { data: "fields.usuarioRegistro_id"},
                     ]
            }

            if  (dataTableAutorizacionesDetalleInitialized)  {

		            dataTableB = $("#tablaAutorizacionesDetalle").dataTable().fnDestroy();

                    }

                dataTableB = $('#tablaAutorizacionesDetalle').DataTable(dataTableOptionsAutorizacionesDetalle);

	            dataTableAutorizacionesDetalleInitialized  = true;
      }

}
	
const initDataTableAutorizaciones = async () => {
	if  (dataTableAutorizacionesInitialized)  {
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

        arrancaAutorizaciones(1,data);
	    dataTableAutorizacionesInitialized = true;
}


 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableAutorizaciones();
	 $('#tablaAutorizaciones tbody tr:eq(0) .miAutorizacion').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript


});


 /* FIN ONLOAD */



 $('#tablaAutorizaciones tbody').on('click', '.miAutorizacion', function() {

        var post_id = $(this).data('pk');
        var autorizacionId = post_id;
	    var row = $(this).closest('tr'); // Encuentra la fila

	    var data =  {}   ;
	    var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	document.getElementById("autorizacionId").value = autorizacionId ;

        var data =  {}   ;
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
        data['autorizacionId'] = autorizacionId;
    	data = JSON.stringify(data);

        arrancaAutorizaciones(2,data);


  });


 $('#tablaAutorizacionesDetalle tbody').on('click', '.miAutorizacionDetalle', function() {

        var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila


	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

	 document.getElementById("autorizacionDetalleId").value = post_id;


	var autorizacionDetalleId = post_id; 

	$.ajax({

	        url: "/leerDetalleAutorizacion/",
                data: {'autorizacionDetalleId':autorizacionDetalleId},
                type: "POST",
                dataType: 'json',
                success: function (info) {

		alert("regrese " + JSON.stringify(info));
		
				

				$('#tipoTipoExamen').val(info[0].fields.tipoTipoExamen);
 				$('#estadoAutorizacion').val(info[0].fields.estadoAutorizacion_id);

				 $('#tipNombre').val(info[0].fields.tipNombre);
				 $('#exaNombre').val(info[0].fields.exaNombre);
 			
				
  		        	$('#numeroAutorizacion').val(info[0].fields.numeroAutorizacion);
        	       	$('#examenes_id').val(info[0].fields.examenes_id);
	                $('#cantidadSolicitada').val(info[0].fields.cantidadSolicitada);
	                $('#cantidadAutorizada').val(info[0].fields.cantidadAutorizada);
	                $('#valorSolicitado').val(info[0].fields.valorSolicitado);
	                $('#valorAutorizado').val(info[0].fields.valorAutorizado);
	                $('#fechaRegistro').val(info[0].fields.fechaRegistro);
	                $('#tipoExamen').val(info[0].fields.tipoExamen);
	                $('#usuarioRegistro2_id').val(info[0].fields.usuarioRegistro_id);
			$('#Aconvenios').val(info[0].fields.convenio_id);
			$('#mipres').val(info[0].fields.mipres);



         	   $('#modelHeadingAutorizacionesDetalle').html("Detalle Autorizaciones");
 		 $('#crearModelAutorizacionesDetalle').modal('show');


                },
     	   	        error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
			        },
            });

  });



function ActualizarAut()
{



            $.ajax({
                data: $('#postFormAutorizacionesDetalle').serialize(),
	        url: "/actualizarAutorizacionDetalle/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {
		   $("#mensajes").html(data2.Mensaje);
                  $('#postFormAutorizacionesDetalle').trigger("reset");

		

	    	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        	var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	        var username_id = document.getElementById("username_id").value;
		var autorizacionId = document.getElementById("autorizacionId").value;


		var data =  {}   ;
	        data['username'] = username;
	       	data['sedeSeleccionada'] = sedeSeleccionada;
	       	data['nombreSede'] = nombreSede;
	      	data['sede'] = sede;
	        data['username_id'] = username_id;
		   data['autorizacionId'] = autorizacionId;	
       		data = JSON.stringify(data);
	        arrancaAutorizaciones(1,data);
	    dataTableAutorizacionesDetalleInitialized = true;


	        arrancaAutorizaciones(2,data);
	    dataTableAutorizacionesDetalleInitialized = true;
	
	

 		 $('#crearModelAutorizacionesDetalle').modal('hide');

                },
      	   	        error: function(data){
		       		document.getElementById("mensajesErrorAutorizacionesDetalle").innerHTML =  data.responseText;
			        },
            });


}




function CerrarModalJson()
{

            $('#crearModelRipsJson').modal('hide');
}

        $('body').on('click', '.ImprimirAutorizacion', function () {

	          var post_id = $(this).data('pk');
		var row = $(this).closest('tr'); // Encuentra la fila

		 alert("ImprimirAutorizacion entre pk = " + post_id);

	var autorizacionId = post_id;

	alert("voy ajax imprimir " + autorizacionId);

$.ajax({
    url: '/imprimirAut/',
   data : {autorizacionId:autorizacionId},
    method: 'POST',
    xhrFields: {
        responseType: 'blob' // Importante: interpreta la respuesta como binario
    },
    success: function (data) {
	alert("llegue");


        var blob = new Blob([data], { type: 'application/pdf' });
        var link = window.URL.createObjectURL(blob);
        window.open(link, '_blank'); // Abre el PDF en nueva pestaña [11]
    },
    error: function (error) {
      document.getElementById("mensajesError").value =  data.responseText
    }
});

       });
