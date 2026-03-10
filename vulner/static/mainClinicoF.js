
console.log('Hola Alberto Hi!')

const form = document.getElementById('formHistoria')
const form2 = document.getElementById('formClinicos')
const FormEvolucionarHistoria = document.getElementById('FormEvolucionarHistoria')

console.log(form)


let dataTable;
let dataTableClinicoInitialized = false;
let dataTableInterConsultasInitialized = false;

$(document).ready(function() {

$('ul.tabs li a:first').addClass('active');
	$('.secciones article').hide();
	$('.secciones article:first').show();

	$('ul.tabs li a').click(function(){
		$('ul.tabs li a').removeClass('active');
		$(this).addClass('active');
		$('.secciones article').hide();

		var activeTab = $(this).attr('href');
		$(activeTab).show();
		return false;
	});

	});




function arrancaClinico(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsClinico  ={
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
            scrollY: '325px',
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
                 url:"/load_dataClinico/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{"render": function ( data, type, row ) {
                        var btn = '';

				    btn = btn + " <input type='radio' name='miRadio'  class='miClinico form-check-input ' data-pk='" + row.pk + "'>" + "</input>";
                       return btn;
                    },


		},
	{"render": function ( data, type, row ) {
                        var btn = '';

		 btn = btn + " <button class='ImprimirHc btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-solid fa-print"></i>' + "</button>";
                       return btn;
                    },


		},
     
                { data: "fields.id"},
                { data: "fields.tipoDoc"},
                { data: "fields.documento"},
                { data: "fields.nombre"},
                { data: "fields.consec"},
                { data: "fields.fechaIngreso"},
                { data: "fields.fechaSalida"},
		{ data: "fields.servicioNombreIng"},
                { data: "fields.camaNombreIng"},
                { data: "fields.dxActual"},
		{ data: "fields.salidaClinica"},
           ]
            }
			
	        dataTable = $('#tablaClinico').DataTable(dataTableOptionsClinico);
			
  }


    if (valorTabla == 2)
    {
        let dataTableOptionsInterConsultas  ={
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
	    { width: '10%', targets: [9] },
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
                 url:"/load_dataInterConsultas/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{

 "render": function ( data, type, row ) {
                        var btn = '';
             btn = btn + " <input type='radio' name='miInterConsulta' class='miInterConsulta form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";


                       return btn;
                    },
                 },
        {
		"render": function ( data, type, row ) {
                        var btn = '';

	 	 btn = btn + " <button class='ImprimirInterConsulta btn-primary ' data-pk='" + row.pk + "'>" + '<i class=""fa-duotone fa-solid fa-print""></i>' + "</button>";

                       return btn;
		}
                   },

                { data: "fields.id"},
                { data: "fields.descripcionConsulta"},
                { data: "fields.respuestaConsulta"},
                { data: "fields.diagnostico"},
                { data: "fields.espConsulta"},
                { data: "fields.historia_id"},
                { data: "fields.especialidadMedico"},
                { data: "fields.medicoConsulta"},
                { data: "fields.medicoConsultado"},
                { data: "fields.tiposNombre"},

            ]
            }
	        dataTable = $('#tablaInterConsultas').DataTable(dataTableOptionsInterConsultas);


  }


}

const initDataTableClinico = async () => {
	if  (dataTableClinicoInitialized)  {
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


        arrancaClinico(1,data);
	    dataTableClinicoInitialized = true;



        arrancaClinico(2,data);
	    dataTableInterConsultasInitialized = true;


}

 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableClinico();
	 $('#tablaClinico tbody tr:eq(0) .miClinico').prop('checked', true);  // Checkprimera fila el checkbox creo solo javascript

});


 /* FIN ONLOAD */

	/*--------------------------------------------
        Click to Edit Button
        --------------------------------------------
        --------------------------------------------*/
        $('body').on('click', '.miClinico', function () {
	
          var post_id = $(this).data('pk');


	$.ajax({
	           url: '/creacionHc/postConsultaHcli/',
	            data : {post_id:post_id},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {

			 $('#pk').val(data.pk);
	       	        $('#tipoDocId').val(data.tipoDocId);
        	       	$('#nombreTipoDoc').val(data.nombreTipoDoc);
	                $('#documentoId').val(data.documentoId);
	                $('#documento2').val(data.documento);
	                $('#consec').val(data.consec);

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



$('#tablaClinico tbody').on('click', '.ImprimirHc', function() {

	alert ("Entre tablaClinico ");

	     var post_id = $(this).data('pk');
	alert ("post_id = " + post_id);
	var ingresoId = post_id;

$.ajax({
    url: '/imprimirHistoriaClinica/',
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


$('#tablaInterConsultas tbody').on('click', '.ImprimirInterConsulta', function() {

	alert ("Entre tablaInterConsultas ");

	     var post_id = $(this).data('pk');
	alert ("post_id = " + post_id);
	var interConsultaId = post_id;

$.ajax({
	           url: '/imprimirInterConsultas/',
	            data : {interConsultaId:interConsultaId},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {

			 $('#pk').val(data.pk);
	       	     

                  },
	   		    error: function (request, status, error) {
	   			   document.getElementById("mensajesError").innerHTML = 'Error Contacte a su Administrador' + ': ' + error
	   	    	}
	     });




    });

$('#tablaInterConsultas tbody').on('click', '.miInterConsulta', function() {

	alert ("Entre miInterconsulta ");

	     var post_id = $(this).data('pk');
	alert ("post_id = " + post_id);
	var interConsultaId = post_id;

$.ajax({
	           url: '/leerInterConsulta/',
	            data : {'interConsultaId':interConsultaId},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {
			dato = JSON.parse(data);

			$('#interConsultaId').val(dato[0].fields.id);

			 $('#descripcionConsulta').val(dato[0].fields.descripcionConsulta);
			 $('#respuestaConsulta').val(dato[0].fields.respuestaConsulta);
			 $('#diagnostico').val(dato[0].fields.diagnostico);
			 $('#espConsulta').val(dato[0].fields.espConsulta);
			 $('#especialidadMedico').val(dato[0].fields.especialidadMedico);
			 $('#medicoConsulta').val(dato[0].fields.medicoConsulta);
			 $('#medicoConsultado').val(dato[0].fields.medicoConsultado);
			 $('#tiposNombre').val(dato[0].fields.tiposNombre);

			$('#crearModelInterConsultas').modal('show');
			 $('#pk').val(data.pk);	       	     

                  },
	   		      error: function(data){
		           alert("data = " + JSON.stringify(data)); // data
		           alert(data.status); // the status code
		   
		           alert(data.JsonResponse['error']); // the message
		document.getElementById("mensajesError").innerHTML =  data.JsonResponse.error
			        },
	     });

    });


$('#saveBtnResponderInterConsulta').click(function (e) {
		e.preventDefault();

	alert ("Entre a actualizar Interconsulta");

     var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;


  		  $.ajax({
                data: $('#postFormInterConsultas').serialize(),
	        url: "/guardarInterConsulta/",
                type: "POST",
                dataType: 'json',
                success: function (data) {
		  $("#mensajes").html(data.message);

		  if (data.success== false)
				{
                alert("entre error");
				document.getElementById("mensajesErrorModalInterConsulta").innerHTML = data.Mensaje;
				return;
				}

                  $('#postFormInterConsultas').trigger("reset");
    		  
			 var data2 =  {}   ;
			data2['username'] = username;
		        data2['sedeSeleccionada'] = sedeSeleccionada;
		        data2['nombreSede'] = nombreSede;
		        data2['sede'] = sede;
		        data2['username_id'] = username_id;

		        data2 = JSON.stringify(data2);


		  arrancaClinico(2,data2);
		    dataTableInterConsultasInitialized = true;

		$('#crearModelInterConsultas').modal('hide');

                },
                   error: function(data){
		           alert("data = " + JSON.stringify(data)); // data
		           alert(data.status); // the status code
		   
		           alert(data.JsonResponse['error']); // the message
		document.getElementById("mensajesError").innerHTML =  data.JsonResponse.error
			        },
      });

     });


FormEvolucionarHistoria.addEventListener('submit', e=>{

	 var radios = $('input[type="radio"][name="miRadio"]');
	 var filaSeleccionada =	radios.filter(":checked")
	
  if (radios.is(':checked')) {

		 $("#FormEvolucionarHistoria").submit();
  } else {
    alert('Por favor, selecciona un Paciente.');
	event.preventDefault();
		return;
  }

})
