    $(document).ready(function() {

	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;
	var tipoDoc_id = document.getElementById("tipoDoc_id").value;
	var documentoPaciente = document.getElementById("documentoPaciente").value;
	var IngresoPaciente = document.getElementById("IngresoPaciente").value;

        var data =  {}   ;

        data['sede'] = sede;
        data['username_id'] = username_id;
        data['tipoDoc_id'] = tipoDoc_id;
        data['documentoPaciente'] = documentoPaciente;
        data['IngresoPaciente'] = IngresoPaciente;

        data = JSON.stringify(data);

	initTableLaboratorios(data);
	tableActionsLaboratorios();

	    /*------------------------------------------
        --------------------------------------------
        Click to Button
        --------------------------------------------
        --------------------------------------------*/
        $('#createNewPostLaboratorios').click(function () {

	    //var ingresoId= document.getElementById("ingresoId1").value;
	    //document.getElementById("ingresoId2").value = ingresoId;
	    alert("A cargar Modal");

            $('#saveBtnCrearLaboratorios').val("Create Post");
            $('#post_id').val('');
            $('#postFormCrearLaboratorios').trigger("reset");
            $('#modelHeadingLaboratorios').html("Creacion Laboratorios");
            $('#crearLaboratoriosModel').modal('show');
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
        $('#saveBtnCrearLaboratorio').click(function (e) {
            e.preventDefault();
            $(this).html('Sending..');
	        $('#crearLaboratoriosModel').modal('hide');
            $('.success-msg').css('display','block');
            $('.success-msg').text('Dato actualizado');
 		   var table = $('#tablaLaboratorios').DataTable(); // accede de nuevo a la DataTable.
	       table.ajax.reload();



        });
/*------------------------------------------
        --------------------------------------------
        Delete Post Code
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostLaboratorio",function(){
            var current_object = $(this);
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');


		   $.ajax({
	           url: '/postDeleteLaboratorios/' ,
	            data : {'id':id},
	           type: 'POST',
	           dataType : 'json',
	  		success: function (data) {

		        	  $('.success-msg').css('display','block');
                        $('.success-msg').text(data.message);
			            var table = $('#tablaLaboratorios').DataTable(); // accede de nuevo a la DataTable.
		                table.ajax.reload();
                    },
	   		    error: function (request, status, error) {
	   			    $("#mensajes").html(" !  Reproduccion  con error !");
	   	    	}
	           });
	});
});  // Aquip fin del document.ready


function initTableLaboratorios(data) {

	return new DataTable('.tablaLaboratorios', {
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
                      //    btn = btn + " <button   class='btn btn-primary editPost' data-pk='" + row.pk + "'>" + "</button>";
                      // Falta el borrar
                          btn = btn + " <input type='radio'  class='form-check-input editPostLaboratorios' data-pk='" + row.pk + "'>" + "</input>";
                        return btn;
                    },
                    "targets": 2
               }
            ],
              ajax: {
                 url:"" ,
                 type: "POST",
                dataSrc: ""
            },
            lengthMenu: [2,3, 5, 10, 20, 30, 40, 50],
            columns: [
                { data: "fields.id"},
                { data: "fields.nombre"},
                 ]
 });

}

function tableActionsLaboratorios() {
   var table = initTableLaboratorios();

    // perform API operations with `table`
    // ...
}

formHistoriaClinica.addEventListener('submit', e=>{


         alert("Entre Form formHistoriaClinica");
         alert("serlialiLab = " +  serialiLab);

        e.preventDefault()

             var tipoDoc    =  document.getElementById("tipoDoc_id").value

             var documento      =  document.getElementById("documentoPaciente").value;

             var folio  = "0";
             var fecha          =  document.getElementById("fecha").value;

             var motivo =          document.getElementById("id_motivo").value;
             var subjetivo =      document.getElementById("id_subjetivo").value;
             var objetivo =       document.getElementById("id_objetivo").value;
             var analisis =        document.getElementById("id_analisis").value;
             var plan =           document.getElementById("id_plan").value;
             var causasExterna = document.getElementById("causasExterna").value;
             var dependenciasRealizado = document.getElementById("dependenciasRealizado").value;
             var usuarioRegistro = document.getElementById("usuarioRegistro").value;
             var consecAdmision=document.getElementById("IngresoPaciente").value;
             var perfil = document.getElementById("perfil").value;
             var tiposfolio = 0;
             // Medico Verificar
             if (perfil == 1)
                {
                document.getElementById("tiposFolio").value=1;
                }
                // Enfermeria Verificar
             if (perfil == 2)
                {
                document.getElementById("tiposFolio").value=2;
                }


             var tiposFolio = document.getElementById("tiposFolio").value;
             alert("tiposFolio =" + tiposFolio);
             var profesional = document.getElementById("profesional").value;
             alert("Profesional = ", profesional);
             var espMedico = document.getElementById("espMedico").value;
             var planta = document.getElementById("Username_id").value;
             var fechaRegistro = document.getElementById("fechaRegistro").value;
             var estadoReg = "A"
             var diagnosticos = document.getElementById("diagnosticos").value;


             envio1.append('tipoDoc', tipoDoc );
             envio1.append( 'documento', documento);
             envio1.append( 'consecAdmision', consecAdmision);
             envio1.append('folio', folio);
             envio1.append('fecha', fecha);
             envio1.append('tiposFolio', tiposFolio);
             envio1.append('profesional', profesional);
             envio1.append('causasExterna', causasExterna);
             envio1.append('dependenciasRealizado', dependenciasRealizado);
             envio1.append('espMedico', espMedico);
             envio1.append('planta', planta);
             envio1.append('motivo' , motivo);
             envio1.append('subjetivo' , subjetivo);
             envio1.append('objetivo' , objetivo);
             envio1.append('analisis' , analisis);
             envio1.append('plan' , plan);
             envio1.append('fechaRegistro' , fechaRegistro);
             envio1.append('usuarioRegistro' , usuarioRegistro);
             envio1.append('estadoReg' , estadoReg);
             envio1.append('diagnosticos' , diagnosticos);

             // InicioLaboratorio
             // Aqui serializar la forma  HistoriaExamenesCabezoteForm

             document.formCabezoteLab['historia'].value =0;
             document.formCabezoteLab['estadoReg'].value ='A';

             // convertir formdata a JSON

             const formDataCabezoteLab = new FormData(formCabezoteLab);
             var object = {};
             formDataCabezoteLab.forEach((value, key) => object[key] = value);

             //Convierto a JSON

             var jsonCabezoteLab = JSON.stringify(object);

             envio1.append('jsonCabezoteLab' , jsonCabezoteLab);


            // Rutina manejo serialiLab

// Display the key/value pairs


                    for (var clave in serialiLab){
                 		   // Controlando que json realmente tenga esa propiedad
            		    if (serialiLab.hasOwnProperty(clave)) {
             		    // Mostrando en pantalla la clave junto a su valor
               		    //   alert("La clave es " + clave + " y el valor es " + serialiLab[clave]);
               		    console.log ("clave PRIMER FOR");

			           	console.log (clave + ', ' + serialiLab[clave]);
                 	       envio_final = serialiLab[clave];


	                     }
        	           }
        	         //   var dato = JSON.parse(envio_final);
                        console.log("Envio final = ");
                        console.log(JSON.stringify (envio_final));



                      var jsonLab = {};
                    var jsonDefLab = [];
                    var inicio = 0;

           //     alert("Entries = " + JSON.stringify (envio_final.entries()));


     		    for(var pair of envio_final.entries()) {

                 	       if (inicio == 3)
                        {
                         // insjsonDeferto desde aqui
                      //   alert("Los datos jsonLab son : ");

                       //  alert( JSON.stringify (jsonLab ));

                         jsonDefLab.push(JSON.stringify (jsonLab ));
                          delete jsonLab['tipoExamen'];
                          delete jsonLab['examen'];
                          delete jsonLab['cantidad'];

                         //   alert( "Con El jSONlAB bORRADO QUEDA = " + JSON.stringify (jsonLab ));
                             alert( "y El jSONdeflAB queda = " + JSON.stringify (jsonDefLab ));
                         inicio = 0;

		            	}

		           inicio = inicio +1;

                   if (pair[0] == "tipoExamen" )
                    {

                   jsonLab[pair[0]] = pair[1];
                    }

                    if (pair[0] == "examen"  )
                    {

                       jsonLab[pair[0]] = pair[1];

                    }

                   if (pair[0] == "cantidad" )
                            {

                       jsonLab[pair[0]] = pair[1];

                            }

        	        }


        	        alert("jsondef = " + JSON.stringify (jsonDefLab));


        console.log(JSON.stringify (jsonDefLab));

                  var jsonDefLab1 = JSON.stringify(jsonDefLab);

                  envio1.append('serialiLab',jsonDefLab1);

                 // Fin Rutina manejo serialiLab

                 // Fin Laboratorio



                 // Inicio Radiologia

                 // Aqui serializar la forma  HistoriaExamenesCabezoteForm

                   document.formCabezoteRad['historia'].value =0;
                   document.formCabezoteRad['estadoReg'].value ='A';

             // convertir formdata a JSON

             const formDataCabezoteRad = new FormData(formCabezoteRad);
             var object = {};
             formDataCabezoteRad.forEach((value, key) => object[key] = value);

             //Convierto a JSON

             var jsonCabezoteRad = JSON.stringify(object);

             envio1.append('jsonCabezoteRad' , jsonCabezoteRad);

             // Rutina manejo serialiRad


     		    for (var clave in serialiRad){
                 		   // Controlando que json realmente tenga esa propiedad
            		    if (serialiRad.hasOwnProperty(clave)) {
             		    // Mostrando en pantalla la clave junto a su valor
               		    //   alert("La clave es " + clave + " y el valor es " + serialiLab[clave]);
			           	console.log (clave + ', ' + serialiRad[clave]);
                 	       envio_finalRad = serialiRad[clave];
	                     }
        	           }
                        console.log("Envio final = ");
                        console.log(envio_finalRad);


                   // Display the key/value pairs

                    var jsonRad = {};
                    var jsonDefRad = [];
                    var inicio = 0;

                    for(var pair of envio_finalRad.entries()) {
                        console.log(pair[0]+ ', '+ pair[1]);

                          if (inicio == 3)
                        {
                         // insjsonDeferto desde aqui
                         alert(" VOYA PUSH jsonLab = " + jsonRad);
                         jsonDefRad.push(jsonRad);
                         delete jsonRad.tipoExamen ;
                         delete jsonRad.examen ;
                         delete jsonRad.Cantidad ;
                         inicio = 0;
                         alert("entre esta vez");
                         alert("jsonDefRad = " + jsonDefRad);
		            	}
		           inicio = inicio +1;

                   if (pair[0] == "tipoExamen" )
                    {
                   jsonRad.tipoExamen = pair[1];
                    }
                    if (pair[0] == "examen"  )
                    {
                       jsonRad.examen = pair[1];

                    }
                   if (pair[0] == "cantidad" )
                    {
                        jsonRad.cantidad = pair[1];

                    }
                    }

                  console.log(jsonDefRad);
                  var jsonDefRad1 = JSON.stringify(jsonDefRad);

                  envio1.append('serialiRad',jsonDefRad1);

                 // Fin Rutina manejo serialiRad





                 // Fin Radiologia


               $.ajax({
            	   type: 'POST',
 	               url: '/crearHistoriaClinica/',
  	               data: envio1,
 	      		success: function (respuesta2) {
 	      		       // var data = JSON.parse(respuesta2);
 	      		        alert("con stringy = " + JSON.stringify(respuesta2))
 	      		        // alert(data['Tipo']);
 	      		        //alert(data['Mensaje']);

 	      		        alert(respuesta2.Tipo);
 	      		        alert(respuesta2.Mensaje);


 	      		        if (respuesta2.Tipo != '"Error')
 	      		         {
 	      		        document.getElementById("id_motivo").value = "";
                        document.getElementById("id_subjetivo").value = "";
                        document.getElementById("id_objetivo").value = "";
                        document.getElementById("id_analisis").value = "";
                        document.getElementById("id_plan").value = "";
                        document.getElementById("causasExterna").value = "";
                        document.getElementById("dependenciasRealizado").value = "";
                        document.getElementById("diagnosticos").value = "";

                         const $id2 = document.querySelector("#id_id_medico");

 	      		         //  $("#laboratorios1").empty();
 	      		         //  $("#radiologias1").empty();
 	      		        //   $("#terapias").empty();
 	      		          // $("#tiposAntecedente").empty();
                            //$("#antecedente").empty();
                        //$("#tiposDiagnostico").empty();
                            //$("#diagnostico").empty();
 	      		        }

 	      	 			$("#mensajes").html(respuesta2.Mensaje);


 	      		},
 	      		error: function (request, status, error) {
 	      			alert(request.responseText);
 	      			alert (error);
 	      			$("#mensajes").html("Error Venta AJAX O RESPUESTA");
 	      		},
 	      		cache : false,
 	      		contentType : false,
 	      		processData: false,

 	        });

})
