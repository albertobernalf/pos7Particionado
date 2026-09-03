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

const form = document.getElementById('formHistoria')

const form2 = document.getElementById('formClinicos')
console.log(form)
console.log(form2)


function valida(forma)
{



	};

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
	alert("Entre a Grabar Usuario Triage");

	var envios = new FormData();


	var tipoDoc = document.getElementById("tipoDocTriageModal").value;
	alert("tipoDoc = " +  tipoDoc);

	var documento = document.getElementById("documentoTriageModal").value;
        var nombre = document.getElementById("nombre").value;

	alert("Documento = " +  documento);

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


	var centrosC = document.getElementById("centrosC").value;
	var tiposUsuario = document.getElementById("tiposUsuario").value;

	$.ajax({
		type: 'POST',
	    	url: '/grabaUsuariosTriage/',
		data: {'tipoDoc':tipoDoc,
		       'documento':documento,
               'nombre':nombre,
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
		       'correo':correo},
		success: function (respuesta) {

                $('#mensaje1').html('<span> respuesta</span>');
                $('#usuariosModalTriage').modal('hide');		     

                    },
	   		    error: function (request, status, error) {
	   	    	}
	});
};

///// Aqui la para buscar Usuario Triage ////

$(document).on('change', '#busDocumentoSelTriage', function(event) {

        alert("Entre cambio Modal usuarios Triage");

	
	 var select = document.getElementById("tipoDocTriage"); /*Obtener el SELECT */
    var tipoDoc = select.options[select.selectedIndex].value; /* Obtener el valor */

   documento = document.getElementById("busDocumentoSelTriage").value;
   alert( "Este es el documento : " + tipoDoc +  " " + documento);

	$.ajax({
		type: 'POST',
	    	url: '/findOneUsuarioTriage/',
		data: {'tipoDoc':tipoDoc,'documento':documento},
		success: function (Usuarios) {

			 alert("REGRESE DATOS MODAL2 = " + Usuarios.tipoDoc + " " +  Usuarios.documento);

				if (Usuarios.tipoDoc == null ) 
					{
                                       
					$('#tipoDocTriageModal').val(tipoDoc);
					$('#documentoTriageModal').val(documento);
					}
				else
					{
					$('#tipoDocTriageModal').val(Usuarios.tipoDoc);
					$('#documentoTriageModal').val(Usuarios.documento);
					}

				// $('#tipoDocTriageModal').val(Usuarios.tipoDoc);
				// $('#documentoTriageModal').val(Usuarios.documento);
				$('#nombre').val(Usuarios.nombre);
				$('#genero').val(Usuarios.genero);
				$('#departamentos').val(Usuarios.departamentos);
				$('#fechaNacio').val(Usuarios.fechaNacio);
				$('#municipios').val(Usuarios.municipios);
				$('#localidades').val(Usuarios.localidades);
				$('#ciudades').val(Usuarios.ciudad);
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
				 alert("Ya abri la ventana Modial");



                    },
	   		    error: function (request, status, error) {
	   	    	}
	});

});




$('#tablaDatosTriage tbody td').click(function(){
      var rowIndex = $(this).parent().index('#tablaDatosTriage tbody tr');
      var tdIndex = $(this).index('#tablaDatosTriage tbody tr:eq('+rowIndex+') td');
   //   alert('Row Number: '+(rowIndex+1)+'\nColumn Number: '+(tdIndex+1));
  //    var celda = $(this);
      //alert("valor celda = " + celda.html());
 //     let obtenerDato = document.getElementsByTagName("td");

      tiposDoc=$(this).parents("tr").find("td").eq(0).html();
      documento=$(this).parents("tr").find("td").eq(1).html();
      var sede = document.getElementById("sede").value;

      if ((tdIndex+1) == '9')
      {


      $.ajax({
		type: 'POST',
    	url: '/encuentraTriageModal/',
		data: {'tiposDoc':tiposDoc,'documento':documento,'sede':sede},
		success: function (response_data) {

              //  var options = '<option value="=================="></option>';
              //  const $id9 = document.querySelector("#busServicioT");

		var dato =   JSON.parse(response_data['Triage'].servicioSedes);
		alert("dato = " + dato);

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

		

				 $('#modalActualizaTriage').modal({show:true});
			$('#clasificacionTriage').val(response_data['Triage'].clasificacionTriage);
                    },
   		    error: function (request, status, error) {
	   	    	}
	});
      }

	// Aqui es la creacion de la Admision para el triage

 if ((tdIndex+1) == '10')
      {
	alert ("Entre a crear la admision Triage");
	//$('#tiposDoc').val(tiposDoc);
	//$('#documento').val(documento);
	//$('#sede').val(sede);
	//$('#tiposDoc').val(tiposDoc);
	//$('#busDocumentoSel').val(documento);
  	var username = document.getElementById("username").value;
  	alert ("username = " + username);

      $.ajax({
		type: 'POST',
    	url: '/admisionTriageModal/',
		data: {'tiposDoc':tiposDoc,
		        'documento':documento,
		        'sede':sede,
		        'username':username},
		success: function (response_data) {

   			    alert("entre DATOS MODAL ADMISION DESDE TRIAGE  de tipoDoc y documento  = " + response_data['TiposDoc2'] + " " +  response_data['Documento']);
   			    alert("Servicios  = " + response_data['Servicios']);

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


			alert("voy para SubServicios  = " + response_data['SubServicios']);



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
				
				alert("response_data COMPLETA que viene  = "  + JSON.stringify(response_data));

				$('#medicoIngreso').val(response_data['Medicos']);
				$('#viasIngreso').val(response_data['ViasIngreso']);
				$('#causasExterna').val(response_data['CausasExterna']);
				$('#regimenes').val(response_data['Regimenes']);
				$('#tiposCotizante').val(response_data['TiposCotizante']);
				$('#remitido').val('N');
				$('#ips').val(response_data['Ips']);
				$('#numManilla').val('0');
		            $('#crearAdmTriage').modal({show:true});
                    },
   		    error: function (request, status, error) {
	   	    	}
	});
      }

});


 $('.eBtn').on('click',function(event)
	        {
			event.preventDefault();
			var href = $(this).attr('href');
			console.log("Entre AlBERTO BERNAL F Cargue la Forma Modal Usuarios");
			alert("Entre carga MODAL");

			$.get(href, function(Usuarios,status)
			 {
			 alert("entre DATOS MODAL y el nombre es = ");


                $('#tipoDoc').val(Usuarios.tipoDoc_id);
				$('#documento').val(Usuarios.documento);

				alert(Usuarios.nombre);

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


$(document).on('change', '#departamentos', function(event) {

        alert("Entre cambio Departamento");


       var Departamento =   $(this).val()

       alert("Departamento = " + Departamento);



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
	   		    error: function (request, status, error) {

	   			    $("#mensajeria").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});


$(document).on('change', '#busServicio', function(event) {

       var serv =   $(this).val()
      alert("Este es mi servicio codigo = " + serv);

    //   alert("Entre para llamar a buscarServiciosTriage : " + Serv)

        var sede =  document.getElementById("sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];



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
	   		    error: function (request, status, error) {

	   			    $("#mensajeria").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});


$(document).on('change', '#busServicio2', function(event) {

       var serv =   $(this).val()

       alert("Servicio = " + serv)

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
	   		    error: function (request, status, error) {

	   			    $("#mensajeria").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});






$(document).on('change', '#busServicioX', function(event) {

       var serv =   $(this).val()

       alert("Servicio = " + serv)

        var sede =  document.getElementById("sede").value;
       // var Sede1 = document.getElementById("FormBuscar").elements["Sede"];



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
	   		    error: function (request, status, error) {

	   			    $("#mensajes").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});

$(document).on('change', '#busSubServicio', function(event) {

        alert("Entre a busSubServicio");

        var select = document.getElementById('busServicio'); /*Obtener el SELECT */

        var Serv = select.options[select.selectedIndex].value; /* Obtener el valor */

        alert("servicio = " + Serv);

        var SubServ =   $(this).val();

        alert("SubServ = " + SubServ);

        var Sede =  document.getElementById("Sede").value;

         alert("Sede = " + Sede);
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
	   		    error: function (request, status, error) {

	   			    $("#mensajes").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});



$(document).on('change', '#busSubServicioT', function(event) {

        alert("Entre a busSubServicioT");

        var select = document.getElementById('busServicioX'); /*Obtener el SELECT */

        var serv = select.options[select.selectedIndex].value; /* Obtener el valor */

        alert("servicio = " + serv);

        var subServ =   $(this).val();

        alert("SubServ = " + subServ);

        var sede =  document.getElementById("sede").value;

         alert("Sede = " + sede);
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
	   		    error: function (request, status, error) {

	   			    $("#mensajes").html(" !  Reproduccion  con error !");
	   	    	}

	     });
});


$(document).on('change', '#busSubServicio2', function(event) {

        alert("Entre a busSubServicio2");

        var select = document.getElementById('busServicio2'); /*Obtener el SELECT */

        var serv = select.options[select.selectedIndex].value; /* Obtener el valor */

        alert("servicio = " + serv);

        var subServ =   $(this).val();

        alert("subServ = " + subServ);

        var sede =  document.getElementById("sede").value;

         alert("Sede = " + sede);
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
	   		    error: function (request, status, error) {

	   			    $("#mensajes").html(" !  Reproduccion  con error !");
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
			 alert("entre");


                $('#username').val(UsuariosHc.username);
				$('#password').val(UsuariosHc.password);

				}
			);

			 $('#exampleModal').modal({show:true});

			  });




// FUnciones para Modales

function abrir_modal(url)
        {
            alert ("Entre NModal_0000000000000000000000000001");
            $('#modalActualizaTriage').load(url, function()
            {
            alert ("Entre NModal_001");
            $(this).modal({

                backdrop: 'static',
                keyboard: false
            })
            alert ("Entre NModal_003");

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
	    dataType: 'JSON',
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

                $('#mensaje1').html('<span> respuesta</span>');
                // $('#modalActualizaTriage').modal('hide');
                alert("esta es la clasificacion triage = " + respuesta['clasificacionTriage'] );
                $('#clasificacionTriage').val(respuesta['clasificacionTriage']);

                $('#modalActualizaTriage').modal({show:false});




		$('#clasificacionTriage').val(respuesta['clasificacionTriage']);		

		        window.location.reload();
		        $('#mensajeria').val("Triage Actualizado ...");

                },
	   		    error: function (request, status, error)
	   		    {
	   	    	}
	});

};


function guardarAdmisionTriage()
{

	var tiposDoc = document.getElementById("tiposDoc2").value;
	alert("tiposDoc = " +  tiposDoc);
	var documento = document.getElementById("busDocumentoSel2").value;
	alert("documento = " +  documento);
  	var busServicio2 = document.getElementById("busServicio2").value;
  	var busSubServicio2 = document.getElementById("busSubServicio2").value;
  	var dependenciasIngreso = document.getElementById("dependenciasIngreso").value;
  	var dxIngreso = document.getElementById("dxIngreso").value;
  	var dependenciasIngreso = document.getElementById("dependenciasIngreso").value;
  	var busEspecialidad = document.getElementById("busEspecialidad").value;
  	var medicoIngreso = document.getElementById("medicoIngreso").value;
  	alert(" medicoIngreso" + medicoIngreso);
  	var viasIngreso = document.getElementById("viasIngreso").value;
  	var causasExterna = document.getElementById("causasExterna").value;
  	var regimenes = document.getElementById("regimenes").value;
  	var tiposCotizante = document.getElementById("tiposCotizante").value;
  	var remitido = document.getElementById("remitido").value;
  	var ips = document.getElementById("ips").value;
  	var numManilla = document.getElementById("numManilla").value;
  	var sede = document.getElementById("sede").value;
  	alert("sede =" + sede);
    var username = document.getElementById("username").value;
    var Profesional = document.getElementById("profesional").value;
   alert("Profesional =" + Profesional);
    var nombreSede = document.getElementById("nombreSede").value;
    alert("nombreSede =" + nombreSede);
    var Username_id = document.getElementById("username_id").value;
    var escogeModulo = document.getElementById("escogeModulo").value;

     var ripsServiciosIng = document.getElementById("ripsServiciosIng").value;
     alert(" Envio ripsServiciosIng = " + ripsServiciosIng);
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


	$.ajax({
		type: 'POST',
	    url: '/guardarAdmisionTriage/',
	    dataType: 'JSON',
	    data: {'tiposDoc': tiposDoc,
	            'documento': documento,
	            'busServicio2' : busServicio2,
	            'busSubServicio2':busSubServicio2,
   	            'dependenciasIngreso':dependenciasIngreso,
		        'dxIngreso':dxIngreso,
		        'busEspecialidad':busEspecialidad,
		        'medicoIngreso':medicoIngreso,
		        'viasIngreso':viasIngreso,
		        'causasExterna':causasExterna,
		        'regimenes':regimenes,
		        'tiposCotizante':tiposCotizante,
		        'remitido':remitido,
		        'ips':ips,
		        'numManilla':numManilla,
		        'ripsServiciosIng' : ripsServiciosIng ,
		        'ripsmodalidadGrupoServicioTecSal' : ripsmodalidadGrupoServicioTecSal ,
		        'ripsViaIngresoServicioSalud' : ripsViaIngresoServicioSalud ,
		        'ripsGrupoServicios' : ripsGrupoServicios ,
		        'ripsCondicionDestinoUsuarioEgreso' : ripsCondicionDestinoUsuarioEgreso,
		        'ripsCausaMotivoAtencion' : ripsCausaMotivoAtencion,
		        'ripsRecienNacido' : ripsRecienNacido ,
		        'ripsNumConsultasCPrenatal' : ripsNumConsultasCPrenatal,
		        'ripsEdadGestacional' :  ripsEdadGestacional,
		         'ripsDestinoUsuarioEgresoRecienNacido' : ripsDestinoUsuarioEgresoRecienNacido,
		          'ripsPesoRecienNacido' : ripsPesoRecienNacido ,
		        'Sede':sede,
	             'username':username,
	             'Profesional':Profesional,
	             'nombreSede':nombreSede,
	             'escogeModulo':escogeModulo,
	             'Username_id':Username_id},
		success: function (respuesta)
		        {
		        alert ("respuesta =" + respuesta);
         		alert ("REGRESE DE GUARDAR Admision triage ");

                        $('#mensajes').html('<span> respuesta</span>');
			//   $('#crearAdmTriage').modal().hide();
		     $('#crearAdmTriage').modal({show:false});
		         window.location.reload();

		        $('#mensajeria').val("Admision creada ...");

                },
	   		    error: function (request, status, error)
	   		    {
	   	    	}
	});

};


