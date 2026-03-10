
console.log('Hola Alberto Hi!')
let dataTable;
let dataTableB;
let dataTableC;
let dataTableApoyoTerapeuticoInitialized = false;
let dataTableDetalleApoyoTerapeuticoInitialized = false;
let dataTableTerapeuticoConsultaInitialized = false;
let dataTableRasgosInitialized =false;
let dataTableRasgosConsultaInitialized =false;



$('.editPostar').on('click',function(event)
{
 	 alert("Entre a editPostt"); 
	 var post_id = $(this).data('pk');
          alert("pk1 = " + $(this).data('pk'));
});

$(document).ready(function() {
    var table = $('#tablaApoyoTerapeutico').DataTable();
    
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


function arrancaApoyoTerapeutico(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsApoyoTerapeutico  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",


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
            columnDefs: [
            { width: '1%', targets: [0,1] },
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6,7] // índice de la columna que quieres evitar que haga wrap

		    },
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
                 url:"/load_dataApoyoTerapeutico/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

                         btn = btn + " <input type='radio'  class='form-check-input editPostApoyoTerapeutico' data-pk='" + row.pk + "'>" + "</input>";

                       return btn;
                    }

	},
                { data: "fields.id"},
                { data: "fields.tipoDoc"},
                { data: "fields.documento"},
                { data: "fields.nombre"},
                { data: "fields.consec"},
                { data: "fields.fechaExamen"},
                { data: "fields.tipoExamen"},
	            { data: "fields.examen"},
                { data: "fields.estadoExamen"},
                { data: "fields.cantidad"},
                { data: "fields.folio"},


            ]
             }

	        dataTable = $('#tablaApoyoTerapeutico').DataTable(dataTableOptionsApoyoTerapeutico);

    
  }

    if (valorTabla == 2)
    {
        let dataTableOptionsRasgosConsulta  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",


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
            columnDefs: [
            { width: '1%', targets: [0,1] },
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6] // índice de la columna que quieres evitar que haga wrap

		    },
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
                 url:"/load_dataRasgosConsulta/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

			btn = btn + " <button class='btn btn-danger deletePostRasgos' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa fa-trash"></i>' + "</button>";

                       return btn;
                    }

	},
  		{ data: "fields.codigoCups"},
                { data: "fields.nombreRasgo"},
                { data: "fields.unidad"},
                { data: "fields.minimo"},
                { data: "fields.maximo"},
                { data: "fields.valorResultado"},
		{ data: "fields.observa"},
            ]
             }

	        dataTable = $('#tablaRasgosConsulta').DataTable(dataTableOptionsRasgosConsulta);

    
  }

    if (valorTabla == 3)
    {
        let dataTableOptionsTerapeuticoConsulta  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",


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
            columnDefs: [
            { width: '1%', targets: [0,1] },
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6] // índice de la columna que quieres evitar que haga wrap

		    },
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
                 url:"/load_dataTerapeuticoConsulta/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

	            btn = btn + " <input type='radio'  class='form-check-input editPostTerapeuticoConsulta' data-pk='" + row.pk + "'>" + "</input>";

                       return btn;
                    }

	},
  		       { data: "fields.id"},
                { data: "fields.tipoDoc"},
                { data: "fields.documento"},
                { data: "fields.nombre"},
                { data: "fields.consec"},
                { data: "fields.fechaExamen"},
                { data: "fields.tipoExamen"},
	            { data: "fields.examen"},
                { data: "fields.estadoExamen"},
                { data: "fields.cantidad"},
                { data: "fields.folio"},
            ]
             }

	        dataTable = $('#tablaTerapeuticoConsulta').DataTable(dataTableOptionsTerapeuticoConsulta);

    
  }

    if (valorTabla == 4)
    {
        let dataTableOptionsRasgos  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",


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
            columnDefs: [
            { width: '1%', targets: [0,1] },
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6] // índice de la columna que quieres evitar que haga wrap

		    },
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
                 url:"/load_dataRasgos/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

			btn = btn + " <button class='btn btn-danger deletePostRasgos' data-action='post/" + row.pk + "/delete' data-pk='" + row.pk + "'>" + '<i class="fa fa-trash"></i>' + "</button>";

                       return btn;
                    }

	},
  	
                { data: "fields.codigoCups"},
                { data: "fields.nombreRasgo"},
                { data: "fields.unidad"},
                { data: "fields.minimo"},
                { data: "fields.maximo"},
                { data: "fields.valorResultado"},
		{ data: "fields.observa"},
            ]
             }

	        dataTable = $('#tablaRasgos').DataTable(dataTableOptionsRasgos);

    
  }

    if (valorTabla == 5)
    {
        let dataTableOptionsDetalleApoyoTerapeutico  ={
   dom: "<'row mb-1'<'col-sm-3'B><'col-sm-3'><'col-sm-6'f>>" + // B = Botones a la izquierda, f = filtro a la derecha
             "<'row'<'col-sm-12'tr>>" +
             "<'row mt-3'<'col-sm-5'i><'col-sm-7'p>>",


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
            columnDefs: [
            { width: '1%', targets: [0,1] },
		{ className: 'centered', targets: [0, 1, 2, 3, 4, 5] },
		{   targets: [5,6,7] // índice de la columna que quieres evitar que haga wrap

		    },
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
                 url:"/load_dataDetalleApoyoTerapeutico/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

	{
	  "render": function ( data, type, row ) {
                        var btn = '';

                         btn = btn + " <input type='radio'  class='form-check-input editPostDetalleApoyoTerapeutico' data-pk='" + row.pk + "'>" + "</input>";

                       return btn;
                    }

	},
                { data: "fields.id"},
                { data: "fields.tipoDoc"},
                { data: "fields.documento"},
                { data: "fields.nombre"},
                { data: "fields.consec"},
                { data: "fields.fechaExamen"},
                { data: "fields.tipoExamen"},
	            { data: "fields.examen"},
                { data: "fields.estadoExamen"},
                { data: "fields.cantidad"},
                { data: "fields.folio"},


            ]
             }

	        dataTable = $('#tablaDetalleApoyoTerapeutico').DataTable(dataTableOptionsDetalleApoyoTerapeutico);

    
  }


}

const initDataTableApoyoTerapeutico = async () => {
	if  (dataTableApoyoTerapeuticoInitialized)  {
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


	 var sede = document.getElementById("sede").value;

          data['sede'] = sede;
        

 	    data = JSON.stringify(data);

	alert("Voy a cargar la tabla");

        arrancaApoyoTerapeutico(1,data);
	    dataTableApoyoTerapeuticoInitialized = true;

}

 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableApoyoTerapeutico();


});


 /* FIN ONLOAD */

	/*------------------------------------------
        --------------------------------------------
        Delete Post Code Rasgos
        --------------------------------------------
        --------------------------------------------*/

        $("body").on("click",".deletePostRasgos",function(){
            var current_object = $(this);
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');

       var data =  {}   ;

		 data['username'] = username;
        	 data['sedeSeleccionada'] = sedeSeleccionada;
	         data['nombreSede'] = nombreSede;
	         data['sede'] = sede;
		 data['username_id'] = username_id;
	         data['valor'] = examId;

		  data = JSON.stringify(data);


		   $.ajax({
	           url: '/postDeleteExamenesRasgos/' ,
	            data : {'id':id},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {

	             		  arrancaApoyoTerapeutico(2,data);
	    dataTableRasgosConsultaInitialized = true;

		  arrancaApoyoTerapeutico(4,data);
	    dataTableRasgosInitialized = true;



		  $("#mensajes").html(" ! Registro Borrado !");
		document.getElementById("mensajes").innerHTML = '! Registro Borrado !';
	

                    },
	   		    error: function (request, status, error) {
			document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
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









	/*--------------------------------------------
        Click to Edit Button
        --------------------------------------------
        --------------------------------------------*/
        $('body').on('click', '.editPostApoyoTerapeutico', function () {
   
          var post_id = $(this).data('pk');
         // alert("post_id= " + post_id);

         var tipoExamenId = document.getElementById("tipoExamenId").innerHTML;
         var tipoExamen = document.getElementById("tipoExamen").innerHTML;
         var CupsId = document.getElementById("CupsId").innerHTML;
         var nombreExamen = document.getElementById("nombreExamen").innerHTML;
         var cantidad = document.getElementById("cantidad").innerHTML;
	     var observaciones = document.getElementById("observaciones").innerHTML;
         var estadoExamen = document.getElementById("estadoExamen").value;
         var folio = document.getElementById("tipoExamenId").value;
         var interpretacion1 = document.getElementById("interpretacion1").value;
         var medicoInterpretacion1 = document.getElementById("medicoInterpretacion1").value;
         var interpretacion2 = document.getElementById("interpretacion2").value;
	     var medicoInterpretacion2 = document.getElementById("medicoInterpretacion2").value;
         var medicoReporte = document.getElementById("medicoReporte").value;
         var rutaImagen = document.getElementById("rutaImagen").value;
         var rutaVideo = document.getElementById("rutaVideo").value;
         var username_id = document.getElementById("username_id").value;	
         var sede = document.getElementById("sede").value;



	$.ajax({
	           url: '/postConsultaApoyoTerapeutico/',
	            data : {post_id:post_id,
			   tipoExamenId:tipoExamenId,
			   tipoExamen:tipoExamen,
			   CupsId:CupsId,
			   nombreExamen:nombreExamen,
			   cantidad:cantidad,
               observaciones:observaciones,
			   estadoExamen:estadoExamen,
			   folio:folio,
			   interpretacion1:interpretacion1,
			   medicoInterpretacion1:medicoInterpretacion1,
			   interpretacion2:interpretacion2,
			   medicoInterpretacion2:medicoInterpretacion2,
               medicoReporte:medicoReporte,
   			   rutaImagen:rutaImagen,
			   rutaVideo:rutaVideo,
			   sede:sede	
			},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {
                       // alert("Regrese");

                    //  alert("dataResultado3="  + data[0]['ResultadoApoyoTerapeutico']); // este es el Registro
                    //   alert("dataResultado5="  + data[0]['ResultadoApoyoTerapeutico'][0].tipoExamenId);
                    //     alert("RasgosClinicos="  + data[1]['RasgosClinicos']);  // esye es el combo

		//               alert("data[2].MedicoInterpretacion1="  + data[2]['MedicoInterpretacion1'][1]['nombre']);  // esye es el combo
                 //              alert("MedicoInterpretacion2="  + data[3]['MedicoInterpretacion2'][1]['nombre']);  // esye es el combo
                  //                alert("MedicoReporte="  + data[4]['MedicoReporte'][1]['nombre']);  // esye es el combo
	//		alert("dependenciasRealizado1 = " + data[0]['ResultadoApoyoTerapeutico'][0]);
	//		alert("dependenciasRealizado2 = " + data[0]['ResultadoApoyoTerapeutico'][0].dependencias);
			

	  		  // var dato = JSON.parse(respuesta);
			 $('#pk').val(data.pk);
	       	        // $('#tipoDocPaci').val(data[7]['Paciente'][0]['tipoDoc']);
			document.getElementById("tipoDocPaci").innerHTML = data[7]['Paciente'][0]['tipoDoc'];
			document.getElementById("documentoPaci").innerHTML = data[7]['Paciente'][0]['documento'];
			document.getElementById("nombrePaciente").innerHTML = data[7]['Paciente'][0]['nombre'];
			document.getElementById("tipoExamenId").innerHTML = data[0]['ResultadoApoyoTerapeutico'][0]['tipoExamenId'];
			document.getElementById("tipoExamen").innerHTML = data[0]['ResultadoApoyoTerapeutico'][0]['tipoExamen'];
			document.getElementById("CupsId").innerHTML = data[0]['ResultadoApoyoTerapeutico'][0]['CupsId'];
			document.getElementById("nombreExamen").innerHTML = data[0]['ResultadoApoyoTerapeutico'][0]['nombreExamen'];
			document.getElementById("cantidad").innerHTML = data[0]['ResultadoApoyoTerapeutico'][0]['cantidad'];
			document.getElementById("observaciones").innerHTML = data[0]['ResultadoApoyoTerapeutico'][0]['observaciones'];
		


	       	        //$('#documentoPaci').val(data[7]['Paciente'][0]['documento']);
	       	        // $('#nombrePaciente').val(data[7]['Paciente'][0]['nombre']);

	       	        //$('#tipoExamenId').val(data[0]['ResultadoApoyoTerapeutico'][0].tipoExamenId);
        	       	//$('#tipoExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].tipoExamen);
	                //$('#CupsId').val(data[0]['ResultadoApoyoTerapeutico'][0].CupsId);
	                //$('#nombreExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].nombreExamen);
	                //$('#cantidad').val(data[0]['ResultadoApoyoTerapeutico'][0].cantidad);

	                //$('#observaciones').val(data[0]['ResultadoApoyoTerapeutico'][0].observaciones);
	                $('#estadoExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].estado);
	                $('#folio').val(data[0]['ResultadoApoyoTerapeutico'][0].folio);
	                $('#interpretacion1').val(data[0]['ResultadoApoyoTerapeutico'][0].interpretacion1);
	                // $('#medicoInterpretacion1').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion1);

	                $('#interpretacion2').val(data[0]['ResultadoApoyoTerapeutico'][0].interpretacion2);
	                // $('#medicoInterpretacion2').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion2);
	                // $('#medicoReporte').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoReporte);
	                $('#rutaImagen').val(data[0]['ResultadoApoyoTerapeutico'][0].rutaImagen);
	                $('#rutaVideo').val(data[0]['ResultadoApoyoTerapeutico'][0].rutaVideo);
		//		alert("medicointerpretacion1 = " + data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion1);


			 $('#ingresoIdA').val(data[4]['MedicoReporte']);
			 $('#examId').val(data[0]['ResultadoApoyoTerapeutico'][0].examId);
			

           	  		   var options = '<option value="=================="></option>';

                     const $id2 = document.querySelector("#rasgosClinicos");
 	      		     $("#rasgosClinicos").empty();

	                 $.each(data[1]['RasgosClinicos'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });


                     const $id3 = document.querySelector("#medicoInterpretacion1");
 	      		     $("#medicoInterpretacion1").empty();

	                 $.each(data[2]['MedicoInterpretacion1'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });



                     const $id4 = document.querySelector("#medicoInterpretacion2");
 	      		     $("#medicoInterpretacion2").empty();

	                 $.each(data[3]['MedicoInterpretacion2'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id4.appendChild(option);
 	      		      });


                     const $id5 = document.querySelector("#medicoReporte");
 	      		     $("#medicoReporte").empty();

	                 $.each(data[4]['MedicoReporte'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id5.appendChild(option);
 	      		      });
		

                     // const $id6 = document.querySelector("#serviciosAdministrativos");
 	      	//	     $("#serviciosAdministrativos").empty();



	               //  $.each(data[5]['ServiciosAdministrativos'], function(key,value) {
                       //             options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                       //             option = document.createElement("option");
                       //             option.value = value.id;
                       //             option.text = value.nombre;
                        //            $id6.appendChild(option);
 	      		//      });




	         const $id7 = document.querySelector("#estadoExamen");
 	      		     $("#estadoExamen").empty();

	                 $.each(data[6]['EstadosExamenes'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id7.appendChild(option);
 	      		      });

			
	                 $('#medicoInterpretacion1').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion1_id);
	                 $('#medicoInterpretacion2').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion2_id);


	                 $('#medicoReporte').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoReporte_id);
			  $('#serviciosAdministrativos').val(data[0]['ResultadoApoyoTerapeutico'][0].serviciosAdministrativos);
 			 $('#estadoExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].estado);


  var data =  {}   ;

         var username_id = document.getElementById("username_id").value;
         var sede = document.getElementById("sede").value;
         var nombreSede = document.getElementById("nombreSede").value;

	     data['username'] = username;
         data['sedeSeleccionada'] = sedeSeleccionada;
         data['nombreSede'] = nombreSede;
         data['sede'] = sede;
	     data['username_id'] = username_id;
         data['valor'] = post_id;	

	  data = JSON.stringify(data);



	//	  arrancaApoyoTerapeutico(2,data);
	//    dataTableRasgosConsultaInitialized = true;

   		  arrancaApoyoTerapeutico(3,data);
	    dataTableTerapeuticoConsultaInitialized = true;

		  arrancaApoyoTerapeutico(4,data);
	    dataTableRasgosInitialized = true;

		  arrancaApoyoTerapeutico(5,data);
	    dataTableDetalleApoyoTerapeuticoInitialized = true;


                  },
	   		    error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
	     });

        });


/*** DESDE AQUI CONSULTA DE RESPUESTAS ***/


	/*--------------------------------------------
        Click to Edit Button
        --------------------------------------------
        --------------------------------------------*/
        $('body').on('click', '.editPostTerapeuticoConsulta', function () {
          alert ("Entre boton Apoyo Terapeutico Consulta");
	
          var post_id = $(this).data('pk');
          alert("pk1 = " + $(this).data('pk'));

         var tipoExamenId = document.getElementById("ztipoExamenId").value;
         var tipoExamen = document.getElementById("ztipoExamen").value;
         var CupsId = document.getElementById("zCupsId").value;
         var nombreExamen = document.getElementById("znombreExamen").value;
         var cantidad = document.getElementById("zcantidad").value;
	 var observaciones = document.getElementById("zobservaciones").value;
         var estadoExamen = document.getElementById("zestadoExamen").value;
         var folio = document.getElementById("ztipoExamenId").value;
         var interpretacion1 = document.getElementById("zinterpretacion1").value;
         var medicoInterpretacion1 = document.getElementById("zmedicoInterpretacion1").value;
         var interpretacion2 = document.getElementById("zinterpretacion2").value;
	 var medicoInterpretacion2 = document.getElementById("zmedicoInterpretacion2").value;
         var medicoReporte = document.getElementById("zmedicoReporte").value;
         var rutaImagen = document.getElementById("zrutaImagen").value;
         var rutaVideo = document.getElementById("zrutaVideo").value;
         var username_id = document.getElementById("username_id").value;
	   var username_id = document.getElementById("username_id").value;
         var sede = document.getElementById("sede").value;
         var nombreSede = document.getElementById("nombreSede").value;

	alert("aqui voy");

        var data2 =  {}   ;

    	 data2['username'] = username;
         data2['sedeSeleccionada'] = sedeSeleccionada;
         data2['nombreSede'] = nombreSede;
         data2['sede'] = sede;
	     data2['username_id'] = username_id;
         data2['valor'] = post_id;

	  data3 = JSON.stringify(data2);

	$.ajax({
	           url: '/postConsultaApoyoTerapeuticoConsulta/',
	            data : {post_id:post_id,
			   tipoExamenId:tipoExamenId,
			   tipoExamen:tipoExamen,
			   CupsId:CupsId,
			   nombreExamen:nombreExamen,
			   cantidad:cantidad,
                           observaciones:observaciones,
			   estadoExamen:estadoExamen,
			   folio:folio,
			   interpretacion1:interpretacion1,
			   medicoInterpretacion1:medicoInterpretacion1,
			   interpretacion2:interpretacion2,
			   medicoInterpretacion2:medicoInterpretacion2,
                           medicoReporte:medicoReporte,
   			   rutaImagen:rutaImagen,
			   rutaVideo:rutaVideo,
			    sede:sede
},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {
                        alert("Regrese");

                      alert("dataResultado3="  + data[0]['ResultadoApoyoTerapeutico']); // este es el Registro
                       alert("dataResultado5="  + data[0]['ResultadoApoyoTerapeutico'][0].tipoExamenId);
                         alert("RasgosClinicosz="  + data[1]['RasgosClinicosz']);  // esye es el combo

                            alert("data[2].MedicoInterpretacion1="  + data[2]['MedicoInterpretacion1'][1]['nombre']);  // esye es el combo
                               alert("MedicoInterpretacion2="  + data[3]['MedicoInterpretacion2'][1]['nombre']);  // esye es el combo
                                  alert("MedicoReporte="  + data[4]['MedicoReporte'][1]['nombre']);  // esye es el combo
			alert("serviciosAdministrativos1 = " + data[0]['ResultadoApoyoTerapeutico'][0]);
			alert("serviciosAdministrativos = " + data[0]['ResultadoApoyoTerapeutico'][0].serviciosAdministrativos);
			

	  		  // var dato = JSON.parse(respuesta);
			 $('#pk').val(data.pk);
	       	        $('#ztipoExamenId').val(data[0]['ResultadoApoyoTerapeutico'][0].tipoExamenId);
        	       	$('#ztipoExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].tipoExamen);
	                $('#zCupsId').val(data[0]['ResultadoApoyoTerapeutico'][0].CupsId);
	                $('#znombreExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].nombreExamen);
	                $('#zcantidad').val(data[0]['ResultadoApoyoTerapeutico'][0].cantidad);
	                $('#zobservaciones').val(data[0]['ResultadoApoyoTerapeutico'][0].observaciones);
	                $('#zestadoExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].estado);
	                $('#zfolio').val(data[0]['ResultadoApoyoTerapeutico'][0].folio);
	                $('#zinterpretacion1').val(data[0]['ResultadoApoyoTerapeutico'][0].interpretacion1);
	                $('#zmedicoInterpretacion1').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion1);
	                $('#zinterpretacion2').val(data[0]['ResultadoApoyoTerapeutico'][0].interpretacion2);
	                $('#zmedicoInterpretacion2').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion2);
	                $('#zmedicoReporte').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoReporte);
	                $('#zrutaImagen').val(data[0]['ResultadoApoyoTerapeutico'][0].rutaImagen);
	                $('#zrutaVideo').val(data[0]['ResultadoApoyoTerapeutico'][0].rutaVideo);
			

			 $('#zingresoIdA').val(data[4]['MedicoReporte']);
			 $('#zexamId').val(data[0]['ResultadoApoyoTerapeutico'][0].examId);
			

           	  		   var options = '<option value="=================="></option>';


                   //  const $id2 = document.querySelector("#zrasgosClinicos");
 	      		//     $("#zrasgosClinicos").empty();

	               //  $.each(data[1]['RasgosClinicosz'], function(key,value) {
                        //            options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                        //            option = document.createElement("option");
                        //            option.value = value.id;
                        //            option.text = value.nombre;
                        //            $id2.appendChild(option);
 	      		//      });


                     const $id3 = document.querySelector("#zmedicoInterpretacion1");
 	      		     $("#zmedicoInterpretacion1").empty();

	                 $.each(data[2]['MedicoInterpretacion1'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });



                     const $id4 = document.querySelector("#zmedicoInterpretacion2");
 	      		     $("#zmedicoInterpretacion2").empty();

	                 $.each(data[3]['MedicoInterpretacion2'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id4.appendChild(option);
 	      		      });



                     const $id5 = document.querySelector("#zmedicoReporte");
 	      		     $("#zmedicoReporte").empty();

	                 $.each(data[4]['MedicoReporte'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id5.appendChild(option);
 	      		      });



                     const $id6 = document.querySelector("#zdependenciasRealizado");
 	      		     $("#zdependenciasRealizado").empty();

	                 $.each(data[5]['DependenciasRealizado'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id6.appendChild(option);
 	      		      });

	         const $id7 = document.querySelector("#zestadoExamen");
 	      		     $("#zestadoExamen").empty();

	                 $.each(data[6]['EstadosExamenes'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id7.appendChild(option);
 	      		      });

		
	                 $('#zmedicoInterpretacion1').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion1);
	                 $('#zmedicoInterpretacion2').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoInterpretacion2);
	                 $('#zmedicoReporte').val(data[0]['ResultadoApoyoTerapeutico'][0].medicoReporte);
			  $('#zdependenciasRealizado').val(data[0]['ResultadoApoyoTerapeutico'][0].zserviciosAdministrativos);
 			 $('#zestadoExamen').val(data[0]['ResultadoApoyoTerapeutico'][0].estado);

		  arrancaApoyoTerapeutico(2,data3);
	    dataTableRasgosConsultaInitialized = true;

                  },
	   		    error: function (request, status, error) {
		document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
	     });

        });


/**** HASTA AQUI  ***/




    	/*------------------------------------------
        --------------------------------------------
        Click to Button
        --------------------------------------------
        --------------------------------------------*/
        $('#createNewResultadoRasgo').click(function () {

 	alert("Entre a crear un rasgo");
 
	  var valor = document.getElementById("valor").value;
	  var observa = document.getElementById("observa").value;
	  var rasgo = document.getElementById("rasgosClinicos").value;
	  var selectRasgo = document.getElementById("rasgo"); 
	  var examId = document.getElementById("examId").value;

	 $.ajax({
	           url: '/guardarResultadoRasgo/',
	            data : {
			'examId':examId,
  			'rasgo':rasgo,
			'valor':valor,
                        'observa':observa
			},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {
                        alert("Regrese");
                        alert("respuesta="  + data);


		document.getElementById("mensajesError").innerHTML = 'Registro Creado ! ';


                    },
	   		    error: function (request, status, error) {
document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
	     });

		
	        var data =  {}   ;

		 data['username'] = username;
        	 data['sedeSeleccionada'] = sedeSeleccionada;
	         data['nombreSede'] = nombreSede;
	         data['sede'] = sede;
		 data['username_id'] = username_id;
	         data['valor'] = examId;	

		  data = JSON.stringify(data);

       		  arrancaApoyoTerapeutico(2,data);
	    dataTableRasgosConsultaInitialized = true;

   		  arrancaApoyoTerapeutico(3,data);
	    dataTableTerapeuticoConsultaInitialized = true;

		  arrancaApoyoTerapeutico(4,data);
	    dataTableRasgosInitialized = true;


	           $("#mensajes").html(" ! Registro Guardado !");
  		
        });







function tableActionsApoyoTerapeutico() {
   var table = initTableApoyoTerapeutico();

    // perform API operations with `table`
    // ...
}

function tableActionsRasgos() {
   var tableR = initTableRasgos();

    // perform API operations with `table`
    // ...
}


$('#tablaApoyoTerapeutico tbody').on('click', 'tr', function () {
    // var data = table.row( this ).data();
    // alert( 'You clicked on '+data[0]+'\'s row' );
} );



function clickEvent() {
  var $ = jQuery;
  console.log("Acabo de entrar en clickEvent");

  // $('input[name="ingresoId"]').prop('checked', true);
  // var valor = $('input[name="ingresoId"]:checked').val();

   var sede = document.getElementById("sede").value;
   table = $("#tablaRasgos").dataTable().fnDestroy();
   initTableRasgos(data);

   $.ajax({
	type : 'POST',
        url  : '//',
        data : {'valor' : valor, 'sede':sede},
        success: function(cambioRasgos) {
             alert("llegue cambio rasgos");
	},
  error: function (request, status, error) {
document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
         })

}

function guardarResultado() {
          alert ("Entre GUARDAR resultado");
	 var tipoExamenId = document.getElementById("tipoExamenId").value;
         var tipoExamen = document.getElementById("tipoExamen").value;
         var examId = document.getElementById("examId").value;
	 var observaciones = document.getElementById("observaciones").value;
         var interpretacion1 = document.getElementById("interpretacion1").value;
         var medicoInterpretacion1 = document.getElementById("medicoInterpretacion1").value;
         var interpretacion2 = document.getElementById("interpretacion2").value;
	 var medicoInterpretacion2 = document.getElementById("medicoInterpretacion2").value;
         var medicoReporte = document.getElementById("medicoReporte").value;
         var rutaImagen = document.getElementById("rutaImagen").value;
         var rutaVideo = document.getElementById("rutaVideo").value;
	 //var dependenciasRealizado = document.getElementById("dependenciasRealizado").value;
	 var username_id = document.getElementById("username_id").value;	
	 var estadoExamen = document.getElementById("estadoExamen").value;
	 var serviciosAdministrativos = document.getElementById("serviciosAdministrativos").value;



	 $.ajax({
	           url: '/guardarResultado/',
	            data : {
			examId:examId,
  			observaciones:observaciones,
			interpretacion1:interpretacion1,
                        medicoInterpretacion1:medicoInterpretacion1,
			interpretacion2:interpretacion2,
                        medicoInterpretacion2:medicoInterpretacion2,
			medicoReporte:medicoReporte,
                        rutaImagen:rutaImagen,
			rutaVideo:rutaVideo,
                        usuarioToma: username_id ,
			estadoExamen:estadoExamen,
			serviciosAdministrativos:serviciosAdministrativos,
			},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {
                        alert("Regrese");
                        alert("respuesta="  + data);

	               // $('#mensajes').val('! Registro Actualizado !');
			  $("#mensajes").html(" ! Registro Actualizado !");
			  window.location.reload();
			  $("#mensajes").html(" ! Registro Actualizado !");

                    },
	   		    error: function (request, status, error) {
document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
	     });

}