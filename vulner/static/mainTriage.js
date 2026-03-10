console.log('Hola Alberto Hi!')

var datavta;
var seriali = new Array();
var serialiLab = new Array();
var serialiRad = new Array();
var serialiTer = new Array();
var serialiDiag = new Array();
var serialiAnt = new Array();
var serialiInt = new Array();


var seriali2 = new Array();
var envio = new FormData()
var envio1 = new FormData()
var envio2 = new FormData()
var envioLab = new FormData()
var envioRad = new FormData()
var envioTer = new FormData()

var envioDiag = new FormData()
var formData = new FormData()
var envio_final = new FormData()
var envio_finalRad = new FormData()
var envio_final1 = new FormData()

var x=0
var  folio_final =0

let dataTableTriageInitialized = false;

const form = document.getElementById('formHistoria')

const form2 = document.getElementById('formClinicos')
console.log(form)
console.log(form2)



$(document).ready(function() {
    var table = $('#tablaDatosTriage').DataTable();
    
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

function arrancaTriage(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsTriage  ={
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
		{     "render": function ( data, type, row ) {
                        var btn = '';
        btn = btn + " <button class='miEditaTriage btn-primary ' data-pk='" + row.pk + "'>" + '<i class="fa-duotone fa-regular fa-thumbs-up"></i>' + "</button>";
 
                       return btn;
                    },

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
                 url:"/load_dataTriage/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [

		{
		"render": function ( data, type, row ) {
                        var btn = '';

	  btn = btn + " <button class='ImprimirTriage btn-primary ' data-pk='" + row.pk + "'>" + '<i class=""fa-duotone fa-solid fa-print""></i>' + "</button>";

                       return btn;
		}
                   },
                { data: "fields.id"},
                { data: "fields.tipoDoc"},
                { data: "fields.Documento"},
                { data: "fields.Nombre"},
                { data: "fields.Consec"},
                { data: "fields.camaNombre"},
                { data: "fields.solicita"},
                { data: "fields.motivo"},
		        { data: "fields.triage"},
{
		"render": function ( data, type, row ) {
                        var btn = '';

             btn = btn + " <input type='radio'  name='triageId' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miTriage form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";

                       return btn;
		}
                    },

		        ]
            }
	        dataTable = $('#tablaDatosTriage').DataTable(dataTableOptionsTriage);

      

  }
}

const initDataTableTriage = async () => {
	if  (dataTableTriageInitialized)  {
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


        arrancaTriage(1,data);
	    dataTableTriageInitialized = true;
}

 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableTriage();
	

});


 /* FIN ONLOAD */





function CierraModalUsuarioTriage()
{

       	 $('#usuariosModalTriage').modal('hide');

}



function CierraModalTriage()
{

       	 $('#modalActualizaTriage').modal('hide');

}

function CierraModalAdmisionTriage()
{

       	 $('#crearAdmTriage').modal('hide');

}


function AUsuarioTriage()
{
		var envios = new FormData();


	var tipoDoc = document.getElementById("tipoDocTriageModal").value;


	var documento = document.getElementById("documentoTriageModal").value;
        var nombre = document.getElementById("nombre").value;

	var genero = document.getElementById("genero").value;
	var departamentos = document.getElementById("departamentos").value;
	var ciudades = document.getElementById("ciudades").value;
	var direccion = document.getElementById("direccion").value;

	var telefono = document.getElementById("telefono").value;
	var contacto = document.getElementById("contacto").value;
	var municipios = document.getElementById("municipios").value;
	var localidades = document.getElementById("localidades").value;
	var estadoCivil = document.getElementById("estadoCivil").value;
	var ocupaciones = document.getElementById("ocupaciones").value;
	var correo = document.getElementById("correo").value;
	var fechaNacio = document.getElementById("fechaNacio").value;
	   var primerNombre = document.getElementById("primerNombre").value;
	   var segundoNombre = document.getElementById("segundoNombre").value;
	   var primerApellido = document.getElementById("primerApellido").value;
	   var segundoApellido = document.getElementById("segundoApellido").value;
	   var ripsZonaTerritorial = document.getElementById("ripsZonaTerritorial").value;



	if (departamentos =='')
		{

		document.getElementById("mensajesErrorModalUsuario").innerHTML = 'Suministre Departamento';
		return;
		}

	if (ciudades =='')
		{
		document.getElementById("mensajesErrorModalUsuario").innerHTML = 'Suministre Ciudad';
		return;
		}



if (direccion =='')
		{
		document.getElementById("mensajesErrorModalUsuario").innerHTML = 'Suministre Direccion';
		return;
		}
if (municipios =='')
		{
		document.getElementById("mensajesErrorModalUsuario").innerHTML = 'Suministre Municipio';
		return;
		}
if (localidades =='')
		{
		document.getElementById("mensajesErrorModalUsuario").innerHTML = 'Suministre Localidad';
		return;
		}




	var centrosC = document.getElementById("centrosC").value;
	var tiposUsuario = document.getElementById("tiposUsuario").value;

if (tiposUsuario =='')
		{
	document.getElementById("mensajesErrorModalUsuario").innerHTML = 'Suministre Tipo Usuario';
		return;
		}



	$.ajax({
	    	url: '/grabaUsuariosTriage/',
		type: 'POST',
		data: {'tipoDoc':tipoDoc,
		       'documento':documento,
               'nombre':nombre,
		 'primerNombre':primerNombre,
		'segundoNombre':segundoNombre,
		'primerApellido':primerApellido,
		'segundoApellido':segundoApellido,
               'genero':genero,
               'fechaNacio':fechaNacio,
		       'estadoCivil' : estadoCivil,
		       'departamentos':departamentos,
               'ciudades':ciudades,
               'direccion':direccion,
         	   'telefono':telefono,
     		   'contacto':contacto,
		       "centrosC":centrosC,
		       'tiposUsuario':tiposUsuario,
		       'municipios':municipios,
		       'localidades':localidades,
		       'estadoCivil':estadoCivil, 
		       'ocupaciones':ocupaciones, 
		       'correo':correo,
			'ripsZonaTerritorial':ripsZonaTerritorial},
		success: function (respuesta) {

              
	document.getElementById("mensajes").innerHTML = respuesta;
                $('#usuariosModalTriage').modal('hide');		     

                    },
			 error: function(data){
		       		document.getElementById("mensajesErrorModalUsuario").innerHTML =  data.responseText
			        },
	});
};

///// Aqui la para buscar Usuario Triage ////

$(document).on('change', '#busDocumentoSelTriage', function(event) {

      
	
	 var select = document.getElementById("tipoDocTriage"); /*Obtener el SELECT */
    var tipoDoc = select.options[select.selectedIndex].value; /* Obtener el valor */

   documento = document.getElementById("busDocumentoSelTriage").value;
  //  alert( "Este es el documento : " + tipoDoc +  " " + documento);

	$.ajax({
		type: 'POST',
	    	url: '/findOneUsuarioTriage/',
		data: {'tipoDoc':tipoDoc,'documento':documento},
		success: function (Usuarios) {

			 // alert("REGRESE DATOS MODAL222 = " + Usuarios.tipoDoc + " " +  Usuarios.documento);

		if (Usuarios.documento==undefined)
					{
					
				$('#tipoDocTriageModal').val(tipoDoc);
				$('#documentoTriageModal').val(documento);

					}
				else
					{

				$('#tipoDocTriageModal').val(Usuarios.tipoDoc);
				$('#documentoTriageModal').val(Usuarios.documento);

			}

				
				$('#nombre').val(Usuarios.nombre);
				$('#primerNombre').val(Usuarios.primerNombre);
				$('#segundoNombre').val(Usuarios.segundoNombre);
				$('#primerApellido').val(Usuarios.primerApellido);
				$('#segundoApellido').val(Usuarios.segundoApellido);
				$('#genero').val(Usuarios.genero);
				$('#departamentos').val(Usuarios.departamentos);
				$('#fechaNacio').val(Usuarios.fechaNacio);
				$('#municipios').val(Usuarios.municipios);
				$('#localidades').val(Usuarios.localidades);
				$('#ciudades').val(Usuarios.ciudades);
				$('#direccion').val(Usuarios.direccion);
				$('#telefono').val(Usuarios.telefono);
				$('#contacto').val(Usuarios.contacto);
				$('#estadoCivil').val(Usuarios.estadoCivil);
				$('#ocupaciones').val(Usuarios.ocupaciones);
				$('#correo').val(Usuarios.correo);
				$('#centrosC').val(Usuarios.centrosC);
				$('#tiposUsuario').val(Usuarios.tiposUsuario);

				$('#usuariosModalTriage').modal('show');
				 $('#usuariosModalTriage').modal({show:true});




                    },
	   		   			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText
	   	    	}
	});

});

$('#tablaDatosTriage tbody').on('click', '.miEditaTriage', function() {

	 var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	// alert("post_id=" + post_id);
	// alert("row=" + row);
	var triageId= post_id;
	 var sede =  document.getElementById("sede").value;
	 var username =  document.getElementById("username").value;


	var table = $('#tablaDatosTriage').DataTable();  // Inicializa el DataTable jquery 	      
        var rowindex = table.row(row).data(); // Obtiene los datos de la fila
        dato1 = Object.values(rowindex);
	console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
        dato3 = dato1[2];
	console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	// alert(" fila selecciona de vuelta dato3  glosaId= " +   dato3.Documento);
	// alert(" fila selecciona de vuelta dato3 factura = " + dato3.tipoDoc);
	// alert("Voy ajax editar Triage");
	

      $.ajax({
		type: 'POST',
    	url: '/encuentraTriageModal/',
		data: {'triageId':triageId,'sede':sede,'tiposDoc':dato3.tipoDoc,'documento':dato3.Documento},
		success: function (response_data) {

       
		var dato =   JSON.parse(response_data['Triage'].servicioSedes);
		// alert("REGRESE dato = " + dato);

                $('#busServicioT').val(response_data['Triage'].servicioSedes);
 
          	    $('#busSubServicioP').val(response_data['Triage'].subServiciosSedes);
				$('#dependenciasP').val(response_data['Triage'].dependencias);
          		$('#tiposDoc').val(response_data['Triage'].tiposDoc);
				$('#busDocumentoSel').val(response_data['Triage'].documento);
				$('#motivo').val(response_data['Triage'].motivo);
				$('#examenFisico').val(response_data['Triage'].examenFisico);
				$('#frecCardiaca').val(response_data['Triage'].frecCardiaca);
				$('#frecRespiratoria').val(response_data['Triage'].frecRespiratoria);
				$('#taSist').val(response_data['Triage'].taSist);
				$('#taDiast').val(response_data['Triage'].taDiast);
				$('#taMedia').val(response_data['Triage'].taMedia);
				$('#glasgow').val(response_data['Triage'].glasgow);
				$('#peso').val(response_data['Triage'].peso);
				$('#temperatura').val(response_data['Triage'].temperatura);
				$('#estatura').val(response_data['Triage'].estatura);
				$('#glucometria').val(response_data['Triage'].glucometria);
				$('#saturacion').val(response_data['Triage'].saturacion);
				$('#escalaDolor').val(response_data['Triage'].escalaDolor);
				$('#tipoIngreso').val(response_data['Triage'].tipoIngreso);
				$('#observaciones').val(response_data['Triage'].observaciones);
				$('#clasificacionTriage').val(response_data['Triage'].clasificacionTriage);
				// alert("Voy a abrit la modal = ");
		
				 $('#modalActualizaTriage').modal('show');

		//	$('#modalActualizaTriage').modal({show:true});
			$('#clasificacionTriage').val(response_data['Triage'].clasificacionTriage);
                    },
   		   			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

	   	    	}
	});
	});



$('#tablaDatosTriage tbody').on('click', '.miTriage', function() {

 	var PermisoCrearTriage= document.getElementById("PermisoCrearTriage").value;
	// alert("PermisoCrearTriage = " + PermisoCrearTriage);

	if (PermisoCrearTriage == "False")
		{
		// alert("No tiene permiso para ejecutar opcion");
		return;
		}
		

	 var post_id = $(this).data('pk');
	var row = $(this).closest('tr'); // Encuentra la fila
	// alert("post_id=" + post_id);
	// alert("row=" + row);
	var triageId= post_id;
	 var sede =  document.getElementById("sede").value;
	 var username =  document.getElementById("username").value;


	var table = $('#tablaDatosTriage').DataTable();  // Inicializa el DataTable jquery 	      
        var rowindex = table.row(row).data(); // Obtiene los datos de la fila
        dato1 = Object.values(rowindex);
	console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
        dato3 = dato1[2];
	console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	//alert(" fila selecciona de vuelta dato3  glosaId= " +   dato3.Documento);
	//alert(" fila selecciona de vuelta dato3 factura = " + dato3.tipoDoc);


	// Aqui es la creacion de la Admision para el triage

//	alert ("Entre a crear la admision Triage");

  	var username = document.getElementById("username").value;
  	// alert ("username = " + username);

      $.ajax({
		type: 'POST',
    	url: '/admisionTriageModal/',
		data: {'tiposDoc':dato3.tipoDoc,'documento':dato3.Documento,'sede':sede, 'username':username},
		success: function (response_data) {
   			   //  alert("entre DATOS MODAL ADMISION DESDE TRIAGE  de tipoDoc y documento  = " + response_data['TiposDoc2'] + " " +  response_data['Documento']);
   			  //   alert("Servicios  = " + response_data['Servicios']);
                var options = '<option value="=================="></option>';
                const $id2 = document.querySelector("#busServicio2");

 	      	    $("#busServicio2").empty();

	                 $.each(response_data['Servicios'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });


			// alert("voy para SubServicios  = " + response_data['SubServicios']);

          	    //$('#busSubServicio2').val(response_data['SubServicios']);

          	    const $id3 = document.querySelector("#busSubServicio2");

 	      	    $("#busSubServicio2").empty();

	                 $.each(response_data['SubServicios'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });


				$('#dependenciasIngreso').val(response_data['Habitaciones']);
          		$('#tiposDoc2').val(response_data['TiposDoc2']);
          		$('#busDocumentoSel2').val(response_data['Documento']);
				$('#dxIngreso').val(response_data['Diagnosticos']);
				$('#busEspecialidad').val(response_data['Especialidades']);
				//$('#medicoIngreso').val(response_data['Medicos']);


	          	    const $id4 = document.querySelector("#medicoIngreso");

	 	      	    $("#medicoIngreso").empty();

		                 $.each(response_data['Medicos'], function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id4.appendChild(option);
 	      		      });
				
				// alert("response_data COMPLETA que viene  = "  + JSON.stringify(response_data));

				$('#medicoIngreso').val(response_data['Medicos']);
				$('#viasIngreso').val(response_data['ViasIngreso']);
				$('#causasExterna').val(response_data['CausasExterna']);
				$('#regimenes').val(response_data['Regimenes']);
				$('#tiposCotizante').val(response_data['TiposCotizante']);
				$('#remitido').val('N');
				$('#ips').val(response_data['Ips']);
				$('#numManilla').val('0');

				// alert("listo todo voy a abrir la modal");

			 $('#crearAdmTriage').modal('show');

                    },
   		   			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


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
			// alert("entre DATOS MODAL y el nombre es = ");


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

				}
			);

			 $('#usuariosModal').modal({show:true});

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
			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

	   	    	}

	     });
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
			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

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
	   		  			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

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
	   		error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

	   	    	}

	     });

// aclara las localidades

 //    $("#localidades").empty();


});


$(document).on('change', '#busServicio', function(event) {

       var serv =   $(this).val()
     //  alert("Este es mi servicio codigo = " + serv);
        var sede =  document.getElementById("sede").value;		
	// alert("sede = " + sede);



        $.ajax({
	           url: '/buscarSubServiciosTriage',
	            data : {serv:serv, sede:sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id2 = document.querySelector("#busSubServicio");


 	      		     $("#busSubServicio").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

		//	$('#busSubServicio').val(respuesta);



                    },
	   		  	  error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

	   	    	}

	     });
});


$(document).on('change', '#busServicio2', function(event) {

       var serv =   $(this).val()

      // alert("Servicio = " + serv)

        var sede =  document.getElementById("sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];



        $.ajax({
	           url: '/buscarSubServicios',
	            data : {serv:serv, sede:sede},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id7 = document.querySelector("#busSubServicio2");


 	      		     $("#busSubServicio2").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id7.appendChild(option);
 	      		      });





                    },
	   		  error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

	   	    	}

	     });
});






$(document).on('change', '#busServicioX', function(event) {

       var serv =   $(this).val()

       // alert("Servicio = " + serv);
        var sede =  document.getElementById("sede").value;
  // alert("Sede = " + sede);



        $.ajax({
	           url: '/buscarSubServiciosTriage',
	            data : {serv:serv, sede:sede},
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
	   		  error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

	   	    	}

	     });
});

$(document).on('change', '#busSubServicio', function(event) {

      //  alert("Entre a busSubServicio");

        var select = document.getElementById('busServicio'); /*Obtener el SELECT */

        var Serv = select.options[select.selectedIndex].value; /* Obtener el valor */

     //   alert("servicio = " + Serv);

        var SubServ =   $(this).val();

        // alert("SubServ = " + SubServ);

        var Sede =  document.getElementById("Sede").value;

     //    alert("Sede = " + Sede);
//        alert("Entre para llamar a buscar SubServiciosTriage : " + SubServ);
  //      alert("Entre para llamar a buscar Sede : " + Sede);

        $.ajax({
	           url: '/buscarHabitacionesTriage',
	            data : {Serv:Serv, Sede:Sede, SubServ:SubServ, Exc:'S'},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

//	  		alert("Me devuelvo pos satisfactorio habitaciones");


	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);

                     const $id2 = document.querySelector("#busHabitacion");

 	      		     $("#busHabitacion").empty();

//                    alert("ya borre ahora a escribir depedencias" + dato);

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
	   		error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText

	   	    	}

	     });
});



$(document).on('change', '#busSubServicioT', function(event) {

     //   alert("Entre a busSubServicioT");

        var select = document.getElementById('busServicioT'); /*Obtener el SELECT */

        var serv = select.options[select.selectedIndex].value; /* Obtener el valor */

     //   alert("servicio = " + serv);

        var subServ =   $(this).val();

      //  alert("SubServ = " + subServ);

        var sede =  document.getElementById("sede").value;

        // alert("Sede = " + sede);
//        alert("Entre para llamar a buscar SubServiciosTriage : " + SubServ);
  //      alert("Entre para llamar a buscar Sede : " + Sede);

        $.ajax({
	           url: '/buscarHabitacionesTriage',
	            data : {serv:serv, sede:sede, subServ:subServ, Exc:'S'},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

//	  		alert("Me devuelvo pos satisfactorio habitaciones");


	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);

                     const $id2 = document.querySelector("#dependenciasT");

 	      		     $("#dependenciasT").empty();

//                    alert("ya borre ahora a escribir depedencias" + dato);

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
	   		  			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


	   	    	}

	     });
});


$(document).on('change', '#busSubServicio2', function(event) {

       // alert("Entre a busSubServicio2");

        var select = document.getElementById('busServicio2'); /*Obtener el SELECT */

        var serv = select.options[select.selectedIndex].value; /* Obtener el valor */

//        alert("servicio = " + serv);

        var subServ =   $(this).val();

//        alert("subServ = " + subServ);

        var sede =  document.getElementById("sede").value;

//         alert("Sede = " + sede);
//        alert("Entre para llamar a buscar SubServiciosTriage : " + subServ);
  //      alert("Entre para llamar a buscar Sede : " + sede);

        $.ajax({
	           url: '/buscarHabitaciones',
	            data : {serv:serv, sede:sede, subServ:subServ, Exc:'S'},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

//	  		alert("Me devuelvo pos satisfactorio habitaciones");


	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);

                     const $id5 = document.querySelector("#dependenciasIngreso");

 	      		     $("#dependenciasIngreso").empty();

//                    alert("ya borre ahora a escribir depedencias" + dato);

	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id5.appendChild(option);
 	      		      });

                    },
		   		 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


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
            $('#modalActualizaTriage').load(url, function()
            {
           //  alert ("Entre NModal_001");
            $(this).modal({

                backdrop: 'static',
                keyboard: false
            })
           // alert ("Entre NModal_003");

            $('#tipoDoc').val("1");
	    	$('#documento').val("33333333333333333333");



            $(this).modal('show');
            });
            return false;
        }

function cerrar_modalTriage()
        {
        $('#modalActualizaTriage').modal('hide');
return false;
        }


function guardaTriageModal()
{
	const forma = document.getElementById("guardaTriageModal");
	var tiposDoc = document.getElementById("tiposDoc").value;
	var documento = document.getElementById("busDocumentoSel").value;
  	var busServicioT = document.getElementById("busServicioT").value;
  	var busSubServicioP = document.getElementById("busSubServicioP").value;
  	var dependenciasP = document.getElementById("dependenciasP").value;
  	var motivo = document.getElementById("motivo").value;
  	var examenFisico = document.getElementById("examenFisico").value;
  	var frecCardiaca = document.getElementById("frecCardiaca").value;
  	var frecRespiratoria = document.getElementById("frecRespiratoria").value;
  	var taSist = document.getElementById("taSist").value;
  	var taDiast = document.getElementById("taDiast").value;
  	var taMedia = document.getElementById("taMedia").value;
  	var glasgow = document.getElementById("glasgow").value;
  	var peso = document.getElementById("peso").value;
  	var estatura = document.getElementById("estatura").value;
  	var temperatura = document.getElementById("temperatura").value;
  	var glucometria = document.getElementById("glucometria").value;
  	var saturacion = document.getElementById("saturacion").value;
  	var escalaDolor = document.getElementById("escalaDolor").value;
  	var tipoIngreso = document.getElementById("tipoIngreso").value;
  	var observaciones = document.getElementById("observaciones").value;
  	var clasificacionTriage = document.getElementById("clasificacionTriage").value;

  	var sede = document.getElementById("sede").value;

    var username = document.getElementById("username").value;
    var Profesional = document.getElementById("Profesional").value;

    var nombreSede = document.getElementById("nombreSede").value;

    var Username_id = document.getElementById("username_id").value;
    var escogeModulo = document.getElementById("escogeModulo").value;




	$.ajax({
		type: 'POST',
		 url: '/grabaTriageModal/',
		 dataType: 'json',
	        data: {'tiposDoc': tiposDoc,
	            'documento': documento,
	            'busServicioT' : busServicioT,
	            'busSubServicioP':busSubServicioP,
	            'dependenciasP':dependenciasP,
	            'motivo':motivo ,
	             'examenFisico':examenFisico,
	             'frecCardiaca':frecCardiaca,
	             'frecRespiratoria':frecRespiratoria,
	             'taSist':taSist,
	             'taDiast':taDiast,
	             'taMedia':taMedia,
	             'glasgow':glasgow,
	             'peso':peso,
	             'temperatura':temperatura ,
	             'estatura':estatura,
	             'glucometria':glucometria,
	             'saturacion':saturacion,
	             'escalaDolor':escalaDolor,
	             'tipoIngreso':tipoIngreso,
	             'observaciones':observaciones,
	             'clasificacionTriage':clasificacionTriage,
	             'sede':sede,
	             'username':username,
	             'Profesional':Profesional,
	             'nombreSede':nombreSede,
	             'escogeModulo':escogeModulo,
	             'Username_id':Username_id  },

		success: function (respuesta)
		        {
		       //  alert("De regreso con : " + JSON.stringify(respuesta));

		 $('#mensajes').html(respuesta.Mensaje);
               // $('#mensaje1').html('<span> respuesta</span>');

                $('#clasificacionTriage').val(respuesta['clasificacionTriage']);
                $('#modalActualizaTriage').modal({show:false});
		$('#clasificacionTriage').val(respuesta['clasificacionTriage']);		

		        window.location.reload();

			// document.getElementById("mensajes").innerHTML = 'Triage Actualizado';
		 $('#mensajes').html(respuesta.Mensaje);
                },
		   		  			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


	   	    	}
	});

};


function guardarAdmisionTriage()
{
	
	var tiposDoc = document.getElementById("tiposDoc2").value;
	// alert("tiposDoc = " +  tiposDoc);
	var documento = document.getElementById("busDocumentoSel2").value;
	// alert("documento = " +  documento);
  	var busServicio2 = document.getElementById("busServicio2").value;
  	var busSubServicio2 = document.getElementById("busSubServicio2").value;
  	var dependenciasIngreso = document.getElementById("dependenciasIngreso").value;
  	var dxIngreso = document.getElementById("dxIngreso").value;
  	var dependenciasIngreso = document.getElementById("dependenciasIngreso").value;
  	var busEspecialidad = document.getElementById("busEspecialidad").value;
  	var medicoIngreso = document.getElementById("medicoIngreso").value;
  	// alert(" medicoIngreso" + medicoIngreso);
  	var viasIngreso = document.getElementById("viasIngreso").value;
  	var causasExterna = document.getElementById("causasExterna").value;
  	var regimenes = document.getElementById("regimenes").value;
  	var tiposCotizante = document.getElementById("tiposCotizante").value;
  	var remitido = document.getElementById("remitido").value;
  	var ips = document.getElementById("ips").value;
  	var numManilla = document.getElementById("numManilla").value;
  	var sede = document.getElementById("sede").value;
  	// alert("sede =" + sede);
    var username = document.getElementById("username").value;
    var Profesional = document.getElementById("profesional").value;

    var nombreSede = document.getElementById("nombreSede").value;

    var Username_id = document.getElementById("username_id").value;
    var escogeModulo = document.getElementById("escogeModulo").value;

     var ripsServiciosIng = document.getElementById("ripsServiciosIng").value;
//     alert(" Envio ripsServiciosIng = " + ripsServiciosIng);
    var ripsPesoRecienNacido = document.getElementById("ripsPesoRecienNacido").value;
     var ripsmodalidadGrupoServicioTecSal = document.getElementById("ripsmodalidadGrupoServicioTecSal").value;
    var ripsViaIngresoServicioSalud = document.getElementById("ripsViaIngresoServicioSalud").value;
    var ripsGrupoServicios = document.getElementById("ripsGrupoServicios").value;
    var ripsCondicionDestinoUsuarioEgreso = document.getElementById("ripsCondicionDestinoUsuarioEgreso").value;
    var ripsCausaMotivoAtencion = document.getElementById("ripsCausaMotivoAtencion").value;
    var ripsRecienNacido = document.getElementById("ripsRecienNacido").value;
    var ripsNumConsultasCPrenatal = document.getElementById("ripsNumConsultasCPrenatal").value;
    var ripsEdadGestacional = document.getElementById("ripsEdadGestacional").value;
    var ripsDestinoUsuarioEgresoRecienNacido = document.getElementById("ripsDestinoUsuarioEgresoRecienNacido").value;


	// alert("Voy a guardar crear adnmision TRIAGE con empresa = " + empresasT);
       //  alert("ripsServiciosIng = " + ripsServiciosIng);


      if (ripsmodalidadGrupoServicioTecSal='')
	{
	document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = 'Campo RIPS Modalidad Grupo Servicio Obligatorio'
       return;
	}

      if (ripsViaIngresoServicioSalud='')
	{
	document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = 'Campo RIPS ViaIngreso Servicio Salud Obligatorio'
       return;
	}

     if (ripsGrupoServicios='')
	{
	document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = 'Campo RIPS Grupo Servicios Obligatorio'
       return;
	}

    if (ripsCondicionDestinoUsuarioEgreso='')
	{
	document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = 'Campo RIPS Condicion Destino Usuario Egreso Obligatorio'
       return;
	}
    if (ripsCausaMotivoAtencion='')
	{
	document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = 'Campo rips Causa Motivo Atencion Obligatorio'
       return;
	}
    if (ripsDestinoUsuarioEgresoRecienNacido='')
	{
	document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = 'Campo rips Destino Usuario Egreso Recien Nacido Obligatorio'
       return;
	}
    if (ripsServiciosIng='')
	{
	document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = 'Campo rips Servicios Ing Obligatorio'
       return;
	}


	

	// alert("Voy AJAX ");

	$.ajax({
     	 data: $('#AdmisionTriage').serialize(),
	    url: '/guardarAdmisionTriage/',
		type: 'POST',
	    dataType: 'json',
		success: function (respuesta)
		        {
		      
			if (respuesta.success==false)
			{
			// alert("Entre error");
			document.getElementById("mensajesErrorModalCreaAdmisionTriage").value = respuesta['Mensajes'];
			}
			else
			{
			document.getElementById("mensajes").innerHTML = respuesta['Mensajes'];
			}


		 $('#crearAdmTriage').modal('hide');
	      
		window.location.reload();
	document.getElementById("mensajes").innerHTML = respuesta['Mensajes'];

		document.getElementById("mensajes").innerHTML = respuesta['Mensajes'];

              },
		   		  			 error: function(data){

		       		document.getElementById("mensajesErrorModalCreaAdmisionTriage").value =  data.responseText


	   	    	}
	});

};


$(document).on('change', '#busEspecialidad', function(event) {

       // alert("Entre cambio busEspecialidad");


       var Esp =   $(this).val()

	// alert("especialidad Nro = " + Esp);


        var Sede =  document.getElementById("sede").value;
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


                     const $id2 = document.querySelector("#medicoIngreso");


 	      		     $("#medicoIngreso").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });


                    },
	   			   		  			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


	   	    	}

	     });
});

$('#tablaDatosTriage tbody').on('click', '.ImprimirTriage', function() {

	// alert ("Entre ImprimirTriage ");

	     var post_id = $(this).data('pk');
	// alert ("post_id = " + post_id);
	var triageId = post_id;

	   var data =  {}   ;
        data['triageId'] = triageId;
 	    data = JSON.stringify(data);

$.ajax({
    url: '/imprimirTriage/',
 data : {triageId:triageId},
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

$(document).on('change', '#busServicioT', function(event) {

	var serv =   $(this).val()

	// alert("Entre para llamar a buscarServiciosTriage : " + serv)

        var sede =  document.getElementById("sede").value;
	// alert("sede : " + sede)

        $.ajax({
	           url: '/buscarSubServiciosTriage',
	            data : {serv:serv, sede:sede},
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
		   		  			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


	   	    	}

	     });
});




$(document).on('change', '#empresasT', function(event) {


       var select = document.getElementById("empresasT"); /*Obtener el SELECT */
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


                     const $id2 = document.querySelector("#conveniosT");


 	      		     $("#conveniosT").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id2.appendChild(option);
 	      		      });

                    },
		   		  			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


	   	    	}

	     });
});



$(document).on('change', '#empresasTE', function(event) {


       var select = document.getElementById("empresasTE"); /*Obtener el SELECT */
       var empresaId  = select.options[select.selectedIndex].value; /* Obtener el valor */

	// alert("Entre para llamar a buscarConvenios de Empresa : " + empresaId);

        $.ajax({
	           url: '/buscarConvenioEmpresa',
	            data : {empresaId:empresaId},
	           type: 'GET',
	           dataType : 'json',

	  		success: function (respuesta) {

	  		   var options = '<option value="=================="></option>';

	  		  var dato = JSON.parse(respuesta);


                     const $id3 = document.querySelector("#conveniosTE");


 	      		     $("#conveniosTE").empty();


	                 $.each(dato, function(key,value) {
                                    options +='<option value="' + value.id + '">' + value.nombre + '</option>';
                                    option = document.createElement("option");
                                    option.value = value.id;
                                    option.text = value.nombre;
                                    $id3.appendChild(option);
 	      		      });

                    },
		   		  			 error: function(data){
		       		document.getElementById("mensajesError").innerHTML =  data.responseText


	   	    	}

	     });
});

