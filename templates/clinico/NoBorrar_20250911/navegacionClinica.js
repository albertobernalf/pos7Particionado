	$(document).ready(function() {
	var $ = jQuery;
	console.log('Hola Alberto Hi!')
	var controlLab = 0;
	var controlRad = 0;
	var controlTer = 0;
	var controlPro = 0;
	var controlMed = 0;
	var controlRev = 0;
	var controlDia = 0;
	var controlAnt = 0;
	var controlInt = 0;




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


//	tableActionsLaboratorios();
//	tableActionsRadiologia();
//	tableActionsTerapias();
//	tableActionsNoQx();
//	tableActionsAntecedentes();
//	tableActionsDiagnosticos();
//	tableActionsInterconsultas();
//	tableActionsRevisionSistemas();
//	tableActionsFormulacion();

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
        Delete Post Code Lab
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostLaboratorio",function(){
		alert("Entre a borrar el id laboratorio ");
      	        var rowIndex = $(this).parent().index('#tablaLaboratorios tbody tr');         
	     	alert("Entre a borrar la fila #  laboratorio Nro" + rowIndex );
		var tableL = $('#tablaLaboratorios').DataTable(); 
		// tableL.row(':eq(rowIndex-1)').remove().draw(false);
		 tableL.row.remove(rowIndex).draw(false);

		// document.getElementById("tablaLaboratorios").deleteRow(rowIndex);
                // tableL.ajax.reload();
	});


	/*------------------------------------------
        --------------------------------------------
        Delete Post Code Rx
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostRadiologia",function(){

		alert("Entre a borrar el id Radiologia ");
      	        var rowIndex = $(this).parent().index('#tablaRadiologia tbody tr');         
	     	alert("Entre a borrar la fila #  Tadiologia Nro" + rowIndex );
		var tableL = $('#tablaRadiologia').DataTable(); 

		 tableL.row.remove(rowIndex).draw(false);
	});

/*------------------------------------------
        --------------------------------------------
        Delete Post Code Terapias
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostTerapias",function(){
            var current_object = $(this);
            alert("current_object =" +current_object );
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');
	     	alert("Entre a borrar el radiologia Nro" + id);
	     	var table2 = $('#tablaTerapias');
            table2.find( 'tbody tr:eq(0)' ).remove();

            alert("valores = " + valores);
		        	  $('.success-msg').css('display','block');
                        $('.success-msg').text(data.message);
			              table2.ajax.reload();
	});

    /*--------------------------------------------
        Delete Post Code NoQx
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostNoQx",function(){
            var current_object = $(this);
            alert("current_object =" +current_object );
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');
	     	alert("Entre a borrar el Noqx Nro" + id);
	     	var table4 = $('#tablaNoQx');
            table4.find( 'tbody tr:eq(0)' ).remove();

            alert("valores = " + valores);
		        	  $('.success-msg').css('display','block');
                        $('.success-msg').text(data.message);
			              table4.ajax.reload();
	});

        /*--------------------------------------------
        Delete Post Code Antecedentes
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostAntecedentes",function(){
            var current_object = $(this);
            alert("current_object =" +current_object );
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');
	     	alert("Entre a borrar el Noqx Nro" + id);
	     	var table5 = $('#tablaAntecedentes');
            table5.find( 'tbody tr:eq(0)' ).remove();

            alert("valores = " + valores);
		        	  $('.success-msg').css('display','block');
                        $('.success-msg').text(data.message);
			              table5.ajax.reload();
	});


        /*--------------------------------------------
        Delete Post Code Diagnosticos
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostDiagnosticos",function(){
            var current_object = $(this);
            alert("current_object =" +current_object );
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');
	     	alert("Entre a borrar el Noqx Nro" + id);
	     	var table6 = $('#tablaDiagnosticos');
            table6.find( 'tbody tr:eq(0)' ).remove();

            alert("valores = " + valores);
		        	  $('.success-msg').css('display','block');
                        $('.success-msg').text(data.message);
			              table6.ajax.reload();
	});




        /*--------------------------------------------
        Delete Post Code Interconsultas
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostInterconsultas",function(){
            var current_object = $(this);
            alert("current_object =" +current_object );
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');
	     	alert("Entre a borrar el Interconsultas Nro" + id);
	     	var table7 = $('#tablaInterconsultas');
            table7.find( 'tbody tr:eq(0)' ).remove();

            alert("valores = " + valores);
		        	  $('.success-msg').css('display','block');
                        $('.success-msg').text(data.message);
			              table7.ajax.reload();
	});

        /*--------------------------------------------
        Delete Post Code Revision Sistemas
        --------------------------------------------
        --------------------------------------------*/
        $("body").on("click",".deletePostRevisionSistemas",function(){
            var current_object = $(this);
            alert("current_object =" +current_object );
            var action = current_object.attr('data-action');
            var token = $("input[name=csrfmiddlewaretoken]").val();
            var id = current_object.attr('data-pk');
	     	alert("Entre a borrar el Interconsultas Nro" + id);
	     	var table8 = $('#tablaRevisionSistemas');
            table8.find( 'tbody tr:eq(0)' ).remove();

            alert("valores = " + valores);
		        	  $('.success-msg').css('display','block');
                        $('.success-msg').text(data.message);
			              table8.ajax.reload();
	});


$('#tablaLaboratorios tbody').on('click', 'tr', function () {
    confirm("Desea eliminar LA FILA: ");
       var tableL = $('#tablaLaboratorios').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaLaboratorios").deleteRow(fila-1);

});

$('#tablaRadiologia tbody').on('click', 'tr', function () {
    confirm("Desea eliminar LA FILA: ");
       var tableL = $('#tablaRadiologia').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaRadiologia").deleteRow(fila-1);

});

$('#tablaFormulacion tbody').on('click', 'tr', function () {
    confirm("Desea eliminar LA FILA: ");
       var tableL = $('#tablaFormulacion').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaFormulacion").deleteRow(fila-1);

});





$('#tablaTerapias tbody').on('click', 'tr', function () {
      var tableL = $('#tablaTerapias').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaTerapias").deleteRow(fila-1);
});

$('#tablaNoQx tbody').on('click', 'tr', function () {
 
 var tableL = $('#tablaNoQx').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaNoQx").deleteRow(fila-1);
});



$('#tablaAntecedentes tbody').on('click', 'tr', function () {
 
 var tableL = $('#tablaAntecedentes').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaAntecedentes").deleteRow(fila-1);
});

$('#tablaDiagnosticos tbody').on('click', 'tr', function () {

 var tableL = $('#tablaDiagnosticos').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaDiagnosticos").deleteRow(fila-1);
});


$('#tablaInterconsultas tbody').on('click', 'tr', function () {

 var tableL = $('#tablaInterconsultas').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaInterconsultas").deleteRow(fila-1);
});

$('#tablaRevisionSistemas tbody').on('click', 'tr', function () {

 var tableL = $('#tablaRevisionSistemas').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaRevisionSistemas").deleteRow(fila-1);
});


$('#tablaFacturacions tbody').on('click', 'tr', function () {

 var tableL = $('#tablaFacturacion').DataTable();
      var fila = $(this).parents("tr")['prevObject']['0']['_DT_RowIndex'];
          alert("Fila a borrar = " + fila);
		var rows = tableL
			    .rows(fila)
			    .remove()
			    .draw();
		 document.getElementById("tablaFacturacion").deleteRow(fila-1);
});


        /*------------------------------------------
        --------------------------------------------
        Create Post Code Radiologia
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarRadiologia').click(function (e) {
            e.preventDefault();

   	   if (controlRad == 0)
   	   {
   	   var table1 = $('#tablaRadiologia').DataTable({scrollY: '150px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlRad=1;
   	   }
   	   else
   	   {
   	   var table1 = $('#tablaRadiologia').DataTable();
   	   }

	   var cantidad = document.getElementById("cantidad3").value;
	   var observa = document.getElementById("observa3").value;
           var select = document.getElementById("rad"); /*Obtener el SELECT */
      	   var rad = select.options[select.selectedIndex].value; /* Obtener el valor */
      	   text = select.options[select.selectedIndex].innerText; //El texto de la opción seleccionada

	        table1.row.add([
                    rad, text,  cantidad, observa, '<i class="fa fa-trash"></i>'
                ]).draw(false);
        });

        /*------------------------------------------
        --------------------------------------------
        Create Post Code Terapias
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarTerapias').click(function (e) {
            e.preventDefault();
         //   $('.success-msg').css('display','block');
         //   $('.success-msg').text('Dato actualizado');


   	   if (controlTer == 0)
   	   {
   	   var table3 = $('#tablaTerapias').DataTable({scrollY: '150px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlTer=1;
   	   }
   	   else
   	   {
   	   var table3 = $('#tablaTerapias').DataTable();
   	   }


	   var cantidad = document.getElementById("cantidad4").value;
	   var observa = document.getElementById("observa4").value;
           var select = document.getElementById("ter"); /*Obtener el SELECT */
      	   var ter = select.options[select.selectedIndex].value; /* Obtener el valor */
      	   text = select.options[select.selectedIndex].innerText; //El texto de la opción seleccionada

	        table3.row.add([
                    ter, text,  cantidad, observa, '<i class="fa fa-trash"></i>'
                ]).draw(false);
        });

       /*------------------------------------------
        --------------------------------------------
        Create Post Code NoQx
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarNoQx').click(function (e) {
            e.preventDefault();
         //   $('.success-msg').text('Dato actualizado');

   	   if (controlPro == 0)
   	   {
   	   var table4 = $('#tablaNoQx').DataTable({scrollY: '150px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlPro=1;
   	   }
   	   else
   	   {
   	   var table4 = $('#tablaNoQx').DataTable();
   	   }

	   var cantidad = document.getElementById("cantidad5").value;
       var observa = document.getElementById("observa5").value;
           var select = document.getElementById("noQx"); /*Obtener el SELECT */
      	   var noQx = select.options[select.selectedIndex].value; /* Obtener el valor */
      	   text = select.options[select.selectedIndex].innerText; //El texto de la opción seleccionada

	        table4.row.add([
                    noQx, text,  cantidad, observa, '<i class="fa fa-trash"></i>'
                ]).draw(false);
        });


    /*------------------------------------------
        --------------------------------------------
        Create Post Code Antecedentes
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarAntecedentes').click(function (e) {
            e.preventDefault();


   	   if (controlAnt == 0)
   	   {
   	   var table5 = $('#tablaAntecedentes').DataTable({scrollY: '150px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlAnt=1;
   	   }
   	   else
   	   {
   	   var table5 = $('#tablaAntecedentes').DataTable()
   	   }


       var observa = document.getElementById("observa6").value;

           var select = document.getElementById("antecedentes"); /*Obtener el SELECT */
      	   var antecedentes = select.options[select.selectedIndex].value; /* Obtener el valor */
      	   text = select.options[select.selectedIndex].innerText; //El texto de la opción seleccionada

	        table5.row.add([
                    antecedentes, text,   observa, '<i class="fa fa-trash"></i>'
                ]).draw(false);
        });

    /*------------------------------------------
        --------------------------------------------
        Create Post Code Diagnosticos
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarDiagnosticos').click(function (e) {
            e.preventDefault();


   	   if (controlDia == 0)
   	   {
   	   var table6 = $('#tablaDiagnosticos').DataTable({scrollY: '150px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlDia=1;
   	   }
   	   else
   	   {
   	   var table6 = $('#tablaDiagnosticos').DataTable();
   	   }


       var observa = document.getElementById("observa7").value;

           var select = document.getElementById("diagnosticos"); /*Obtener el SELECT */
      	   var diagnosticos = select.options[select.selectedIndex].value; /* Obtener el valor */
      	   textDiagnosticos = select.options[select.selectedIndex].innerText; //El texto de la opción seleccionada

            var select1 = document.getElementById("tiposDiagnosticos"); /*Obtener el SELECT */
      	   var tiposDiagnosticos = select1.options[select1.selectedIndex].value; /* Obtener el valor */
      	   textTiposDiagnosticos = select1.options[select1.selectedIndex].innerText; //El texto de la opción seleccionada

	        table6.row.add([
                    tiposDiagnosticos ,  textTiposDiagnosticos  ,diagnosticos,  textDiagnosticos,  observa, '<i class="fa fa-trash"></i>'
                ]).draw(false);
        });

    /*------------------------------------------
        --------------------------------------------
        Create Post Code Interconsultas
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarInterconsultas').click(function (e) {
            e.preventDefault();

   	   if (controlInt == 0)
   	   {
   	   var table7 = $('#tablaInterconsultas').DataTable({scrollY: '150px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlInt=1;
   	   }
   	   else
   	   {
   	   var table7 = $('#tablaInterconsultas').DataTable();
   	   }

	   var descripcion = document.getElementById("descripcionI").value;

           var select = document.getElementById("diagnosticosI"); /*Obtener el SELECT */
      	   var diagnosticos = select.options[select.selectedIndex].value; /* Obtener el valor */
      	   textDiagnosticos = select.options[select.selectedIndex].innerText; //El texto de la opción seleccionada

            var select1 = document.getElementById("tiposInterconsulta"); /*Obtener el SELECT */
      	   var tiposInterconsulta = select1.options[select1.selectedIndex].value; /* Obtener el valor */
      	   texttiposInterconsulta = select1.options[select1.selectedIndex].innerText; //El texto de la opción seleccionada

            var select2 = document.getElementById("especialidadConsultada"); /*Obtener el SELECT */
      	   var especialidadConsultada = select2.options[select2.selectedIndex].value; /* Obtener el valor */
      	   textespecialidadConsultada = select2.options[select2.selectedIndex].innerText; //El texto de la opción seleccionada

            var select3 = document.getElementById("medicoConsultado"); /*Obtener el SELECT */
      	   var medicoConsultado = select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textmedicoConsultado = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada


	        table7.row.add([ tiposInterconsulta, texttiposInterconsulta,   especialidadConsultada ,  textespecialidadConsultada ,medicoConsultado, textmedicoConsultado , descripcion, diagnosticos,  textDiagnosticos,  '<i class="fa fa-trash"></i>']).draw(false);
        });


    /*------------------------------------------
        --------------------------------------------
        Create Post Code RevisionSistemas
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarRevisionSistemas').click(function (e) {
            e.preventDefault();

   	   var table9 = $('#tablaRevisionSistemas').DataTable();   // accede de nuevo a la DataTable.

           var observa= document.getElementById("observa9").value;

           var select3 = document.getElementById("rev"); /*Obtener el SELECT */
      	   var revisionSistemas = select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textRevisionSistemas = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada

           table9.row.add([ revisionSistemas, textRevisionSistemas,  observa,  '<i class="fa fa-trash"></i>']).draw(false);
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
   	   var table10 = $('#tablaFormulacion').DataTable({scrollY: '50px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
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


           var select3 = document.getElementById("formaFarma"); /*Obtener el SELECT */
      	   var formaFarma = select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textFormaFarma = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada

	   var select3 = document.getElementById("frecuencia"); /*Obtener el SELECT */
      	   var frecuencia = select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textFrecuencia = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada
	
	   var select3 = document.getElementById("vias"); /*Obtener el SELECT */
      	   var viasAdministracion = select3.options[select3.selectedIndex].value; /* Obtener el valor */
      	   textViasAdministracion = select3.options[select3.selectedIndex].innerText; //El texto de la opción seleccionada
	
	   var cantidadMedicamento =  document.getElementById("cantidadMedicamento").value;
	   var diasTratamiento =  document.getElementById("diasTratamiento").value;

	    table10.row.add([ medicamentos, textMedicamentos, dosis,uMedidaDosis, textUMedidaDosis, formaFarma,  textFormaFarma, frecuencia, textFrecuencia,viasAdministracion, textViasAdministracion, cantidadMedicamento,  diasTratamiento    ,  '<i class="fa fa-trash"></i>']).draw(false);

        });

  /*------------------------------------------
        --------------------------------------------
        Create Post Code Laboratorios
        --------------------------------------------
        --------------------------------------------*/
        $('#BtnAdicionarLaboratorio').click(function (e) {
            e.preventDefault();
         //   $('.success-msg').css('display','block');
         //   $('.success-msg').text('Dato actualizado');

   	   if (controlLab == 0)
   	   {
   	   var tableL = $('#tablaLaboratorios').DataTable({scrollY: '150px', paging:false,   scrollX: true,  scrollCollapse: true,  lengthMenu: [5]});   // accede de nuevo a la DataTable.
   	   controlLab=1;
   	   }
   	   else
   	   {
   	   var tableL = $('#tablaLaboratorios').DataTable();
   	   }
   	   var TipoDocPaciente = document.getElementById("tipoDocPaciente1").value;
	   var documentoPaciente = document.getElementById("documentoPaciente1").value;
	   var IngresoPaciente = document.getElementById("ingresoPaciente1").value;

	   var cantidad = document.getElementById("cantidad").value;
     	   var observa = document.getElementById("observa").value;
           var select = document.getElementById("lab"); /*Obtener el SELECT */
      	   var lab = select.options[select.selectedIndex].value; /* Obtener el valor */
      	   text = select.options[select.selectedIndex].innerText; //El texto de la opción seleccionada
	        tableL.row.add([lab, text,  cantidad, observa, '<i class="fa fa-trash"></i>']).draw(false);
        });
      


// I. LABORATORIOS

function tableActionsLaboratorios() {

   var table= $('#tablaLaboratorios').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '250px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostLaboratorio' >" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 4
               }
            ],
        lengthMenu: [5],
    columns:[
    
        { visible: true }, 
        { visible: true },
        { visible: true }, 
        { visible: true }, 
        { visible: true }, 
            ],
    });
}
});  // Aquip fin del document.ready



// II. RADIOLOGIA


function tableActionsRadiologia() {

      var table1= $('#tablaRadiologia').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			   btn = btn + " <button class='btn btn-danger deletePostRadiologia'>" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 5
               }
            ],
        lengthMenu: [4],
    columns:[
 
        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
        { visible: true }, //col 4

            ],
    });
}
// FIN RADIOLOGIA


// III. TERAPIAS

function tableActionsTerapias() {


   var table3 = $('#tablaTerapias').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostLaboratorio1' id='borraTer'>" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 4
               }
            ],
        lengthMenu: [5],
    columns:[

        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
        { visible: true }, //col 4
            ],
    });
}

// FIN TERAPIAS

// III. NOQX

function tableActionsNoQx() {


   var table4 = $('#tablaNoQx').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostLaboratorio1' id='borraNoQx'>" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 4
               }
            ],
        lengthMenu: [5],
    columns:[

        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
        { visible: true }, //col 4
            ],
    });
}

// FIN NOQX



// III. ANTECEDENTES

function tableActionsAntecedentes() {

   var table5 = $('#tablaAntecedentes').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostAntecedentes1' id='borraAnt'>" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 3
               }
            ],
        lengthMenu: [5],
    columns:[
    //"dummy" configuration
        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
            ],
    });
}

// FIN ANTECEDENTES


// III. DIAGNOSTICOS

function tableActionsDiagnosticos() {

   var table6 = $('#tablaDiagnosticos').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostDiagnosticos1' id='borraDiag'>" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 5
               }
            ],
        lengthMenu: [5],
    columns:[
    //"dummy" configuration
        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
        { visible: true }, //col 3
        { visible: true }, //col 3
            ],
    });
}

// FIN DIAGNOSTICOS




// III. INTERCONSULTAS

function tableActionsInterconsultas() {

   var table6 = $('#tablaInterconsultas').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
	            scrollX: true,
	            scrollCollapse: true,
                paging:false,
                 columnDefs: [
                {
                    "render": function ( data, type, row ) {
                        var btn = '';
			  btn = btn + " <button class='btn btn-danger deletePostDiagnosticos1' id='borraDiag'>" + '<i class="fa fa-trash"></i>' + "</button>";
                        return btn;
                    },
                    "targets": 9
               }
            ],
        lengthMenu: [5],
    columns:[
    //"dummy" configuration
        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
        { visible: true }, //col 3
        { visible: true }, //col 3
        { visible: true }, //col 3
        { visible: true }, //col 3
        { visible: true }, //col 3
        { visible: true }, //col 3

            ],
    });
}

// FIN INTERCONSULTAS




// IV. REVISION SISTEMAS

function tableActionsRevisionSistemas() {

   var table9 = $('#tablaRevisionSistemas').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
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
                    "targets": 3
               }
            ],
        lengthMenu: [5],
    columns:[
    //"dummy" configuration
        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
      

            ],
    });
}

// FIN REVISION SISTEMAS


// MEDICAMENTOS

function tableActionsFormulacion() {

   var table10 = $('#tablaFormulacion').DataTable({
                "language": {
                  "lengthMenu": "Display _MENU_ registros",
                   "search": "Filtrar registros:",
                    },
                processing: true,
                serverSide: false,
                scrollY: '130px',
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
                    "targets": 13
               }
            ],
        lengthMenu: [5],
    columns:[
    //"dummy" configuration
        { visible: true }, //col 1
        { visible: true }, //col 2
        { visible: true }, //col 3
	  { visible: true }, //col 3
	  { visible: true }, //col 3
	  { visible: true }, //col 3
	  { visible: true }, //col 3
	  { visible: true }, //col 3
	  { visible: true }, //col 3
    { visible: true }, //col 3
    { visible: true }, //col 3
	{ visible: true }, //col 3
    { visible: true }, //col 3

            ],
    });
}



// FIN MEDICAMENTOS

formHistoriaClinica.addEventListener('submit', e=>{
           const respuestaUsuario =  confirm("Confirma Guardar Folio !");
	
	if (respuestaUsuario) {
		
  console.log("El usuario confirmó la acción.");

	} else {
	event.preventDefault();
		return;
	  console.log("El usuario canceló la acción.");

	}


        e.preventDefault()
        // Ah peros si se puede solo hay que recorrer y yap

        // LABORATORIO

        const table = $('#tablaLaboratorios').DataTable();
        var datos_tabla = table.rows().data().toArray();


        laboratorios=[]
        cadenas = {}


	for(var i= 0; i < datos_tabla.length; i++) {

	    laboratorios.push({
        	"tiposExamen_Id"    : "1",
	        "cups"  : datos_tabla[i][0],
	        "cantidad"    : datos_tabla[i][2] ,
		"observa"    : datos_tabla[i][3] 
	      });
	   };

	laboratorios  = JSON.stringify(laboratorios);

        // FIN LABORATORIO

        // RADIOLOGIA

                const table1 = $('#tablaRadiologia').DataTable();
                var datos_tabla1 = table1.rows().data().toArray();

        radiologia=[]
        cadenas = {}


	for(var i= 0; i < datos_tabla1.length; i++) {

	    radiologia.push({
        	"tiposExamen_Id"    : "3",
	        "cups"  : datos_tabla1[i][0],
	        "cantidad"    : datos_tabla1[i][2] ,
		"observa"    : datos_tabla1[i][3]
	      });
	   };

	    radiologia  = JSON.stringify(radiologia);



        // FIN RADIOLOGIA


        // TERAPIAS

                const table3 = $('#tablaTerapias').DataTable();
                var datos_tabla3 = table3.rows().data().toArray();

        terapias=[]

	for(var i= 0; i < datos_tabla3.length; i++) {

	    terapias.push({
        	"tiposExamen_Id"    : "2",
	        "cups"  : datos_tabla3[i][0],
	        "cantidad"    : datos_tabla3[i][2] ,
		"observa"    : datos_tabla3[i][3]
	      });
	   };

	    terapias  = JSON.stringify(terapias);



        // FIN TERAPIAS


        // NoQx

                const table4 = $('#tablaNoQx').DataTable();
                var datos_tabla4 = table4.rows().data().toArray();

        noQx=[]

	for(var i= 0; i < datos_tabla4.length; i++) {

	    noQx.push({
        	"tiposExamen_Id"    : "4",
	        "cups"  : datos_tabla4[i][0],
	        "cantidad"    : datos_tabla4[i][2] ,
		"observa"    : datos_tabla4[i][3]
	      });
	   };

	    noQx  = JSON.stringify(noQx);


        // FIN noQx

	// Antecedentes

        const table5 = $('#tablaAntecedentes').DataTable();
                var datos_tabla5 = table5.rows().data().toArray();

        antecedentes=[]


	for(var i= 0; i < datos_tabla5.length; i++) {

	    antecedentes.push({

	        "id"  : datos_tabla5[i][0],
	        "tipo"    : datos_tabla5[i][1] ,
		"descripcion"    : datos_tabla5[i][2]
	      });
	   };

	    antecedentes  = JSON.stringify(antecedentes);

 	// Fin Antecedentes

	// Diagnosticos

    const table6 = $('#tablaDiagnosticos').DataTable();
     var datos_tabla6 = table6.rows().data().toArray();

        diagnosticos=[]


	for(var i= 0; i < datos_tabla6.length; i++) {

	    diagnosticos.push({
	        "diagnosticos"    : datos_tabla6[i][2] ,
	        "tiposDiagnosticos"    : datos_tabla6[i][0] ,
	    	"observa"    : datos_tabla6[i][4]
	      });
	   };

	    diagnosticos  = JSON.stringify(diagnosticos);



 	// Fin Diagnosticos

	// Cirugias

	// Fin Cirugias


	// Interconsultas


    const table7 = $('#tablaInterconsultas').DataTable();
     var datos_tabla7 = table7.rows().data().toArray();

        interconsultas=[]


	for(var i= 0; i < datos_tabla7.length; i++) {

	    interconsultas.push({
	        "tiposInterconsulta"    : datos_tabla7[i][0] ,
	        "tiposInterconsultaNombre"    : datos_tabla7[i][1] ,
	        "especialidadConsultada"    : datos_tabla7[i][2] ,
	        "especialidadConsultadaNombre"    : datos_tabla7[i][3] ,
	        "medicoConsultado"    : datos_tabla7[i][4] ,
	        "medicoConsultadoNombre"    : datos_tabla7[i][5] ,
	        "descripcion"    : datos_tabla7[i][6] ,
	        "diagnosticos"    : datos_tabla7[i][7],
	        "diagnosticosNombre"    : datos_tabla7[i][8]
	      });
	   };

	    interconsultas  = JSON.stringify(interconsultas);

 	// Fin Interconsulta

	// Incapacidades

	const forma = document.getElementById("formIncapacidades");
	const vale = new FormData(forma);

	inca = [];

	tiposIncapacidad=vale.get("tiposIncapacidad");
	diagnosticosIncapacidad=vale.get("diagnosticosIncapacidad");
	desdeFecha=vale.get("desdeFecha");
	hastaFecha=vale.get("hastaFecha");
	numDias=vale.get("numDias");
	descripcion=vale.get("descripcion");


   inca.push({"tiposIncapacidad":tiposIncapacidad,
            "diagnosticosIncapacidad":diagnosticosIncapacidad,
            "desdeFecha":desdeFecha,
            "hastaFecha" :hastaFecha,
            "numDias" :numDias,
            "descripcion" :descripcion   });


	inca  = JSON.stringify(inca);

 	// Fin Incapacidades

    // Signos vitales

	const formaSignos = document.getElementById("formSignos");
	const vale2 = new FormData(formaSignos);

	signos = [];

	fecha=vale2.get("fecha");
	frecCardiaca=vale2.get("frecCardiaca");
	frecRespiratoria=vale2.get("frecRespiratoria");
	tensionADiastolica=vale2.get("tensionADiastolica");
	tensionASistolica=vale2.get("tensionASistolica");
	tensionAMedia=vale2.get("tensionAMedia");
	temperatura=vale2.get("temperatura");
	saturacion=vale2.get("saturacion");
	glucometria=vale2.get("glucometria");
	glasgow=vale2.get("glasgow");
	apache=vale2.get("apache");
	pvc=vale2.get("pvc");
	cuna=vale2.get("cuna");
	ic=vale2.get("ic");
	glasgowOcular=vale2.get("glasgowOcular");
	glasgowVerbal=vale2.get("glasgowVerbal");
	glasgowMotora=vale2.get("glasgowMotora");


   signos.push({"fecha":fecha,
            "frecCardiaca":frecCardiaca,
            "frecRespiratoria":frecRespiratoria,
            "tensionADiastolica" :tensionADiastolica,
            "tensionASistolica" :tensionASistolica,
            "tensionAMedia" :tensionAMedia,
            "temperatura" :temperatura,
            "saturacion" :saturacion,
            "glucometria" :glucometria,
            "glasgow" :glasgow,
            "apache" :apache,
            "pvc" :pvc,
            "cuna" :cuna,
            "ic" :ic,
            "glasgowOcular" :glasgowOcular,
            "glasgowVerbal" :glasgowVerbal,
            "glasgowMotora" :glasgowMotora});


	// alert("signos = final  = " + JSON.stringify(signos));
	signos  = JSON.stringify(signos);

 	// Fin Signos vitales

	// Medicamentos

 	// Fin Medicamentos


	// Revision Sistemas


    const table9 = $('#tablaRevisionSistemas').DataTable();
     var datos_tabla9 = table9.rows().data().toArray();

        revisionSistemas=[]


	for(var i= 0; i < datos_tabla9.length; i++) {

	    revisionSistemas.push({
	        "revisionSistemas"    : datos_tabla9[i][0] ,
	        "observa"    : datos_tabla9[i][2] ,
	      });
	   };

	    revisionSistemas  = JSON.stringify(revisionSistemas);
     

 	// Fin Revision Sistemas


	// Formulacion

    const table10 = $('#tablaFormulacion').DataTable();
     var datos_tabla10 = table10.rows().data().toArray();

        formulacion=[]


	for(var i= 0; i < datos_tabla10.length; i++) {

	    formulacion.push({
	        "medicamentos"    : datos_tabla10[i][0] ,
	        "dosis"    : datos_tabla10[i][2],
	        "uMedidaDosis"    : datos_tabla10[i][3] ,
	        "formaFarma"    : datos_tabla10[i][6] ,
	        "frecuencia"    : datos_tabla10[i][7] ,
	        "vias"    : datos_tabla10[i][9] ,
	        "viasAdministracion"    : datos_tabla10[i][10] ,
	        "cantidadMedicamento"    : datos_tabla10[i][11] ,
	        "diasTratamiento"    : datos_tabla10[i][12] ,
	      });
	   };

	    formulacion  = JSON.stringify(formulacion);
    
 	// Fin Formulacion


	 var salidaClinica = $('input[name="salClinica"]:checked').val();

	 if (salidaClinica != 'on')
		{

		salidaClinica='off'
		}


	 var salidaClinicax    =  document.getElementById("salClinica").value
	 // alert ("salidaClinicax = " + salidaClinicax);
      

	 var sede    =  document.getElementById("sede").value
         var tipoDocPaciente    =  document.getElementById("tipoDocPaciente1").value
         var documentoPaciente  =  document.getElementById("documentoPaciente1").value;
         var folio      = "0";
         var fecha      =  document.getElementById("fecha").value;
         var motivo     =  document.getElementById("id_motivo").value;
         var subjetivo  =  document.getElementById("id_subjetivo").value;
         var objetivo   =  document.getElementById("id_objetivo").value;
         var analisis   =  document.getElementById("id_analisis").value;
         var plan 	=  document.getElementById("id_plann").value;
	 var ordenDeControl	=  document.getElementById("id_ordenDeControl").value;


          var apache2 =  document.getElementById("id_apache2").value;
          var antibioticos =  document.getElementById("id_antibioticos").value;
            var monitoreo =  document.getElementById("id_monitoreo").value;
            var movilidadLimitada = document.getElementById("id_movilidadLimitada").value;

            var nauseas = document.getElementById("id_nauseas").value;
            var llenadoCapilar = document.getElementById("id_llenadoCapilar").value;
            var neurologia =document.getElementById("id_neurologia").value;
            var irritacion =document.getElementById("id_irritacion").value;
            var pulsos = document.getElementById("id_pulsos").value;
            var retiroPuntos = document.getElementById("id_retiroPuntos").value;
            var inmovilizacion = document.getElementById("id_inmovilizacion").value;
            var notaAclaratoria = document.getElementById("id_notaAclaratoria").value;
            var fecNotaAclaratoria = document.getElementById("id_fecNotaAclaratoria").value;
            var fecNotaAclaratoria = document.getElementById("id_fecNotaAclaratoria").value;
            var examenFisico = document.getElementById("id_examenFisico").value;
            var noQx1 = document.getElementById("id_noQx").value;
            var observaciones = document.getElementById("id_observaciones").value;
            var riesgoHemodinamico = document.getElementById("id_riesgoHemodinamico").value;
            //var riesgoVentilatorio = document.getElementById("id_riesgoVentilatorio").value;
            var riesgos = document.getElementById("id_riesgos").value;
            var trombocitopenia = document.getElementById("id_trombocitopenia").value;
            var hipotension = document.getElementById("id_hipotension").value;
            var indiceMortalidad = document.getElementById("id_indiceMortalidad").value;
            var ingestaAlcohol = document.getElementById("id_ingestaAlcohol").value;

            var inmovilizacionObservaciones = document.getElementById("id_inmovilizacionObservaciones").value;
            var justificacion = document.getElementById("id_justificacion").value;
            var leucopenia = document.getElementById("id_leucopenia").value;
            var manejoQx = document.getElementById("id_manejoQx").value;


         var tratamiento =           document.getElementById("id_tratamiento").value;
         var causasExterna = document.getElementById("causasExterna").value;
         //var dependenciasRealizado = document.getElementById("dependenciasRealizado").value;
         var serviciosAdministrativos = document.getElementById("serviciosAdministrativos").value;


         var usuarioRegistro = document.getElementById("usuarioRegistro").value;
         var ingresoPaciente=document.getElementById("ingresoPaciente1").value;

         var tiposFolioEscogido  =  document.getElementById("tiposFolioEscogido").value;
        // alert("tiposFolioEscogido =" + tiposFolioEscogido);
         var profesional = document.getElementById("profesional").value;
         // alert("Profesional = ", profesional);

   	    var espMedico  =  document.getElementById("espMedico").value;

         var planta = document.getElementById("username").value;

         var fechaRegistro = document.getElementById("fechaRegistro").value;
         var estadoReg = "A"
         var tipoIng = document.getElementById("tipoIng").value;

	 var tiposSalidas  =  document.getElementById("tiposSalidas").value;
         // alert("tiposSalidas =" + tiposSalidas);

	var dxComplicacion =  document.getElementById("dxComplicacion").value;
	var mipres =  document.getElementById("id_mipres").value;

	var ordenMedicaLab =  document.getElementById("id_ordenMedicaLab").value;
	var ordenMedicaRad =  document.getElementById("id_ordenMedicaRad").value;
	var ordenMedicaTer =  document.getElementById("id_ordenMedicaTer").value;
	var ordenMedicaMed =  document.getElementById("id_ordenMedicaMed").value;
	var ordenMedicaOxi =  document.getElementById("id_ordenMedicaOxi").value;
	var ordenMedicaInt =  document.getElementById("id_ordenMedicaInt").value;
    // DESDE AQUI LOS DATOS DE CIRUGIA


     var cBoxCirugia = document.getElementById("cBoxCirugia").checked;
     // alert("cboxcirugia = " + cBoxCirugia);
     var solicitaSangre =  document.getElementById("solicitaSangre").value;
      //    alert("solicitaSangre = " + solicitaSangre);
     var describeSangre =  document.getElementById("describeSangre").value;
     var cantidadSangre =  document.getElementById("cantidadSangre").value;
     var solicitaCamaUci =  document.getElementById("solicitaCamaUci").value;
     var solicitaRx =  document.getElementById("solicitaRx").value;
     var solicitaMicroscopio =  document.getElementById("solicitaMicroscopio").value;
     var solicitaOsteosintesis =  document.getElementById("solicitaOsteosintesis").value;
     var solicitaBiopsia =  document.getElementById("solicitaBiopsia").value;
     var solicitaMalla =  document.getElementById("solicitaMalla").value;
     var solicitaOtros =  document.getElementById("solicitaOtros").value;
     var solicitaHospitalizacion =  document.getElementById("solicitaHospitalizacion").value;
     var solicitaAyudante =  document.getElementById("solicitaAyudante").value;
     var solicitaTiempoQx =  document.getElementById("solicitaTiempoQx").value;
     var solicitaTipoQx =  document.getElementById("solicitaTipoQx").value;
     var solicitaAnestesia =  document.getElementById("solicitaAnestesia").value;
     var tiempoMaxQx =  document.getElementById("tiempoMaxQx").value;
     var solicitaAutoSutura =  document.getElementById("solicitaAutoSutura").value;
     var solicitaSoporte =  document.getElementById("solicitaSoporte").value;
     var describeOtros =  document.getElementById("describeOtros").value;
     var tiposCirugia =  document.getElementById("tiposCirugia").value;
     var dxPreQx =  document.getElementById("dxPreQx").value;
     var dxPrinc =  document.getElementById("dxPrinc").value;
     var dxRel1 =  document.getElementById("dxRel1").value;
     var anestesia =  document.getElementById("anestesia").value;
     var tipoDocCirugia =  document.getElementById("tipoDocCirugia").value;
     var documentoCirugia =  document.getElementById("documentoCirugia").value;
     var consecutivoIngresoCirugia =  document.getElementById("consecutivoIngresoCirugia").value;

    // HASTA AQUIP DATOS DE CIRUGIA

            var form_valido;

     
      
               $.ajax({
            	   type: 'POST',
 	               url: '/crearHistoriaClinica/',
  	               data: { 'tipoDocPaciente':tipoDocPaciente,
  	                      'documentoPaciente':documentoPaciente,
  	                      'ingresoPaciente':ingresoPaciente,
  	               		  'folio':folio,
			               'motivo':motivo,
			                'subjetivo':subjetivo,
			                'objetivo':objetivo,
                            'analisis':analisis,
                            'plan':plan,
	                        'causasExterna':causasExterna,
	                        'serviciosAdministrativos':serviciosAdministrativos,
			                'usuarioRegistro':usuarioRegistro,
			                'ingresoPaciente':ingresoPaciente,
			                'profesional':profesional,
				            'espMedico':espMedico,
				            'planta':planta,
				            'estadoReg':estadoReg,
				           'laboratorios':laboratorios,
				           'radiologia':radiologia,
				           'terapias':terapias,
				           'noQx':noQx,
				           'tipoIng':tipoIng,
				           'antecedentes':antecedentes,
				           'diagnosticos':diagnosticos,
				           'interconsultas':interconsultas,
				           'incapacidades':inca,
				           'tiposFolioEscogido':tiposFolioEscogido,
				           'signos':signos ,
				           'tratamiento':tratamiento,
					      'revisionSistemas':revisionSistemas,
		                  'apache2':apache2,
		                  'antibioticos':antibioticos,
                         'monitoreo':monitoreo,
                        'movilidadLimitada':movilidadLimitada,
                        'nauseas':nauseas,
                        'llenadoCapilar':llenadoCapilar,
                        'neurologia':neurologia,
                        'irritacion':irritacion,
                        'pulsos':pulsos,
                        'retiroPuntos':retiroPuntos,
                        'inmovilizacion':inmovilizacion,
                        'notaAclaratoria':inmovilizacion,
                        'fecNotaAclaratoria':fecNotaAclaratoria,
                        'fecNotaAclaratoria':fecNotaAclaratoria,
                        'examenFisico':examenFisico,
                        'noQx1':noQx1,
                        'observaciones':observaciones,
                        'riesgoHemodinamico':riesgoHemodinamico,
                       // 'riesgoVentilatorio':_riesgoVentilatorio,
                        'riesgos':riesgos,
                        'trombocitopenia':trombocitopenia,
                        'hipotension':hipotension,
                        'indiceMortalidad':indiceMortalidad,
                        'ingestaAlcohol':ingestaAlcohol,
                        'tratamiento':tratamiento,
                        'inmovilizacionObservaciones':inmovilizacionObservaciones,
                        'justificacion':justificacion,
                        'leucopenia':leucopenia,
                        'manejoQx':manejoQx,
        			'formulacion':formulacion,
                                'salidaClinica':salidaClinica, 
    				'tiposSalidas':tiposSalidas,
	    			'dxComplicacion':dxComplicacion,
		    		'mipres':mipres	,
                                'sede':sede,
                                'ordenMedicaLab':ordenMedicaLab,
                                'ordenMedicaRad':ordenMedicaRad,
                                'ordenMedicaTer':ordenMedicaTer,
                                'ordenMedicaMed':ordenMedicaMed,
                                'ordenMedicaOxi':ordenMedicaOxi,
                                'ordenMedicaInt':ordenMedicaInt,
				                'serviciosAdministrativos':serviciosAdministrativos,
				                'cBoxCirugia':cBoxCirugia,
                                'solicitaSangre':solicitaSangre,
	                            'describeSangre':describeSangre,
            	                'cantidadSangre':cantidadSangre,
	                            'solicitaCamaUci':solicitaCamaUci,
                                'solicitaMicroscopio':solicitaMicroscopio,
                                'solicitaRx':solicitaRx,
                                'solicitaOsteosintesis':solicitaOsteosintesis,
	                        'solicitaBiopsia':solicitaBiopsia,
	                        'solicitaMalla':solicitaMalla,
	                        'solicitaOtros':solicitaOtros,
	                        'solicitaHospitalizacion':solicitaHospitalizacion,
	                        'solicitaAyudante':solicitaAyudante,
	                        'solicitaTiempoQx':solicitaTiempoQx,
	                        'solicitaTipoQx':solicitaTipoQx,
	                        'solicitaAnestesia':solicitaAnestesia,
	                        'solicitaOtros':solicitaOtros,
                            'tiempoMaxQx':tiempoMaxQx,
	                        'solicitaAutoSutura':solicitaAutoSutura,
	                        'solicitaSoporte':solicitaSoporte,
	                        'describeOtros':describeOtros,
	                        'tiposCirugia':tiposCirugia,
	                        'dxPreQx':dxPreQx,
	                        'dxPrinc':dxPrinc,
	                        'dxRel1':dxRel1,
	                        'anestesia':anestesia,
	                       'tipoDocCirugia':tipoDocCirugia,
	                        'documentoCirugia':documentoCirugia,
	                        'consecutivoIngresoCirugia':consecutivoIngresoCirugia,
				'ordenDeControl':ordenDeControl,

				   },
 	      		success: function (data) {

		// alert("data = " + JSON.stringify(data));

				
                    dato = data;
                    var dataRespuesta = JSON.parse(dato);

			alert("dataRespuesta = ", dataRespuesta);

                  var dato = dataRespuesta['Mensaje'];


		        if ( dato == 'OK')
		            {

		            $("#formHistoriaClinicaT").submit();

		            }
		        else
		            {
		           $("#mensajes").html(dato);

		            }


 	      		}, // cierra function sucess

			 error: function(data){
		           alert(data.status); // the status code
		           alert(data.responseJSON.error); // the message
		document.getElementById("mensajesError").innerHTML =  data.responseJSON.error
			        },


  	        });  // cierra ajax

});  // cierra commit