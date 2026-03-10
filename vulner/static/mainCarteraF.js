console.log('Hola Alberto Hi!')

let dataTable;
let dataTableA;
let dataTableB;
let dataTableC;
let dataTableD;
let dataTableF;
let dataTableG;
let dataTableH;

let dataTableCajaInitialized = false;
let dataTableCarteraInitialized = false;
let dataTableCarteraDetalleInitialized = false;
let dataTablePagosEmpresasInitialized = false;
let dataTablePagosEmpresasDetalleInitialized = false;
let dataTableEmpresasInitialized = false;



$(document).ready(function() {
    var table = $('#tablaCaja').DataTable();
    
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


function arrancaCartera(valorTabla,valorData)
{
    data = {}
    data = valorData;

    if (valorTabla == 1)
    {
        let dataTableOptionsCaja  ={
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

		{   
                    "targets": 18
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
                 url:"/load_dataCaja/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='cajaSeleccion' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miSeleccionCaja form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},

	{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='caja' class='miCaja form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },

		},


                { data: "fields.id"},
                { data: "fields.fecha"},
                { data: "fields.usuarioEntrega_id"},
                { data: "fields.totalEfectivo"},
                { data: "fields.totalTarjetasDebito"},
                { data: "fields.totalTarjetasCredito"},
                { data: "fields.totalCheques"},
                { data: "fields.total"},
                { data: "fields.usuarioRecibe_id"},
		{ data: "fields.usuarioSuperviza_id"},
		{ data: "fields.estadoCaja"},
                { data: "fields.totalEfectivoEsperado"},
                { data: "fields.totalTarjetasDebitoEsperado"},
                { data: "fields.totalTarjetasCreditoEsperado"},
                { data: "fields.totalChequesEsperado"},
                { data: "fields.totalEsperado"},
                { data: "fields.serviciosAdministrativos_id"},    
       ]
            }
	        dataTable = $('#tablaCaja').DataTable(dataTableOptionsCaja);
  }

    if (valorTabla == 2)
    {
        let dataTableOptionsCartera  ={
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
                 url:"/load_dataCartera/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='cartera' class='miCartera form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
		},

              /*  { data: "fields.id"}, */
	{
			target: 0,
			visible: false
		},

                { data: "fields.factura"},
                { data: "fields.nombre"},
                { data: "fields.fecha"},
                { data: "fields.empresa"},

                { data: "fields.valor"},
                { data: "fields.pagos"},
                { data: "fields.saldo"},
       ]
            }
	        dataTable = $('#tablaCartera').DataTable(dataTableOptionsCartera);
  }

    if (valorTabla == 3)
    {
        let dataTableOptionsPagosEmpresas  ={
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
                 url:"/load_dataPagosEmpresas/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='editarPagosEmpresas1' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='editarPagosEmpresas form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
		},
                { data: "fields.id"},
                { data: "fields.empresa"},
                { data: "fields.fecha"},
                { data: "fields.formaPago"},
                { data: "fields.tipoPago"},
                { data: "fields.valor"},
                { data: "fields.descripcion"},
                { data: "fields.fechaRegistro"},
                { data: "fields.radicado"},
                { data: "fields.servicio"},
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='cargarPagosEmpresas1' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='cargarPagosEmpresas form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
		},
       ]
            }
	        dataTable = $('#tablaPagosEmpresas').DataTable(dataTableOptionsPagosEmpresas);
  }


    if (valorTabla == 4)
    {
        let dataTableOptionsPagosEmpresasDetalle  ={
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

		{   
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
                 url:"/load_dataPagosEmpresasDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='editarPagosEmpresasDetalle1' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='editarPagosEmpresasDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
		},
                { data: "fields.id"},
                { data: "fields.facturaId"},
                { data: "fields.valor"},
                { data: "fields.radicadoFactura"},
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='borrarPagosEmpresasDetalle1' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='borrarPagosEmpresasDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
		},
       ]
            }
	        dataTable = $('#tablaPagosEmpresasDetalle').DataTable(dataTableOptionsPagosEmpresasDetalle);
  }



    if (valorTabla == 5)
    {
        alert("entre options");


        let dataTableOptionsCarteraDetalle  ={
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
                 url:"/load_dataCarteraDetalle/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='editarCarteraDetalle1' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='editarCarteraDetalle form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
		},
                { data: "fields.id"},
                { data: "fields.nombreEmpresa"},
                { data: "fields.pagoId"},
                { data: "fields.fecha"},
                { data: "fields.factura"},
                { data: "fields.valor"},
                { data: "fields.pagos"},
                { data: "fields.saldo"},
       ]
            }
                    alert("entre options2");
	        dataTable = $('#tablaCarteraDetalle').DataTable(dataTableOptionsCarteraDetalle);
  }



    if (valorTabla == 6)
    {
        let dataTableOptionsEmpresas  ={
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
                 url:"/load_dataEmpresas/" +  data,
                 type: "POST",
                 dataSrc: ""
            },
            columns: [
		{
		  "render": function ( data, type, row ) {
                        var btn = '';
        		     btn = btn + " <input type='radio' name='empresas' style='width:15px;height:15px;accent-color: purple;border-color: purple;background-color: purple;' class='miEmpresa form-check-input ' data-pk='"  + row.pk + "'>" + "</input>";
                       return btn;
                    },
		},
                { data: "fields.id"},
                { data: "fields.tipoempresa"},
                { data: "fields.tipoDoc"},
                { data: "fields.documento"},
                { data: "fields.empresa"},
                { data: "fields.codigoEapb"},
                { data: "fields.departamento"},
                { data: "fields.municipio"},
                { data: "fields.telefono"},
                { data: "fields.representante"},
       ]
            }
	        dataTable = $('#tablaEmpresas').DataTable(dataTableOptionsEmpresas);
  }


}

const initDataTableCaja = async () => {
	if  (dataTableCajaInitialized)  {
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
	sedesClinica_id = sede;
	data['sedesClinica_id'] = sedesClinica_id
	data['facturaId'] = 1

        data = JSON.stringify(data);

         arrancaCartera(1,data);
	 dataTableCajaInitialized = true;

	alert("voy para cartera");

         arrancaCartera(2,data);
	  dataTableCarteraInitialized = true;

	alert("acabe de mostrar cartera");

       //  arrancaCartera(3,data);
//	   dataTablePagosEmpresasInitialized = true;
   //	alert("acabe de mostrar pagos");

     arrancaCartera(4,data);
	   dataTablePagosEmpresasDetalleInitialized = true;
	alert("ya cargue la tabla");

         arrancaCartera(6,data);
	 dataTableEmpresasInitialized = true;




}

 // COMIENZA ONLOAD

window.addEventListener('load', async () => {
    await  initDataTableCaja();
	 

});


 /* FIN ONLOAD */


 $('#tablaCaja tbody').on('click', '.miCaja', function() {

        var post_id = $(this).data('pk');
        var cajaId = post_id;
	var row = $(this).closest('tr'); // Encuentra la fila

        var data =  {}   ;

 	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;


        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	sedesClinica_id = sede;
	data['sedesClinica_id'] = sedesClinica_id

     $.ajax({
		data: {'cajaId':cajaId},
	        url: "/editarCaja/",
                type: "POST",
                dataType: 'json',
                success: function (info) {

		alert("Iregrese de editarCaja" + JSON.stringify(info));

	//	if (info.success == true)
	//		 {
	//		  document.getElementById("mensajes").value = data.Mensajes;
	//		 }
	//		else
	//		{
	//		document.getElementById("mensajesError").value = data.Mensajes;
	//		return;
	//		}

		alert("sigo marcha");

		$('#postFormCaja').trigger("reset");

			// $('#fecha').val(info[0].fields.fecha);
			document.getElementById("fecha").value = info[0].fields.fecha;
			 $('#usuarioEngrega_id').val(info[0].fields.usuarioEntrega_id);
			 $('#serviciosAdministrativos_id').val(info[0].fields.serviciosAdministrativos_id);



			$('#usuarioRecibe_id').val(info[0].fields.usuarioRecibe_id);
			$('#usuarioSuperviza_id').val(info[0].fields.usuarioSuperviza_id);
			$('#totalEfectivo').val(info[0].fields.totalEfectivo);
			$('#totalEfectivoEsperado').val(info[0].fields.totalEfectivoEsperado);
			$('#totalTarjetasDebito').val(info[0].fields.totalTarjetasDebito);
			$('#totalTarjetasDebitoEsperado').val(info[0].fields.totalTarjetasDebitoEsperado);
			$('#totalTarjetasCredito').val(info[0].fields.totalTarjetasCredito);
			$('#totalTarjetasCreditoEsperado').val(info[0].fields.totalTarjetasCreditoEsperado);
			$('#totalCheques').val(info[0].fields.totalCheques);
			$('#totalChequesEsperado').val(info[0].fields.totalChequesEsperado);
			$('#total').val(info[0].fields.total);
			$('#totalEsperado').val(info[0].fields.totalEsperado);
			$('#estadoCaja').val(info[0].fields.estadoCaja);
			$('#cajaId').val(cajaId);

	
		 $('#crearModelCaja').modal('show');
                },
          error: function (data) {
		
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
            });
  });


function GuardarCaja()
{
	
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;


            $.ajax({
                data: $('#postFormCaja').serialize(),
	        url: "/guardarCaja/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

		if (data2.success == true)
			 {
			  document.getElementById("mensajes").value = data.Mensajes;
			 }
			else
			{
			document.getElementById("mensajesError").value = data.Mensajes;
			return;
			}



		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;

		 $('#crearModelCaja').modal('hide');

	        data = JSON.stringify(data);

		 arrancaCartera(1,data);
	         dataTableCajaInitialized = true;
	
                },
            error: function (data) {
		
	document.getElementById("mensajesError").value =  data.responseText;

	   	    	}
            });


}

function AdicionarPagosEmpresas()
{
		alert("Entre Adicionar pago");
            $('#post_id').val('');
            $('#postFormPagosEmpresas').trigger("reset");
            $('#modelHeadingPagosEmpresas').html("Creacion Pago empresa");
            $('#crearModelPagosEmpresas').modal('show');        
}



function GuardarPagosEmpresas()
{
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	    	var empresaId = document.getElementById("empresaPago").value;


            $.ajax({
                data: $('#postFormPagosEmpresas').serialize(),
	        url: "/guardarPagosEmpresas/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

		if (data2.success == true)
			 {
			  document.getElementById("mensajes").value = data2.Mensajes;
			 }
			else
			{
			document.getElementById("mensajesErrorModalPagosEmpresas").value = data2.Mensajes;
			return;
			}

		var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;
	        data['empresaId'] = empresaId;


		 $('#crearModelPagosEmpresas').modal('hide');

	        data = JSON.stringify(data);

		 arrancaCartera(3,data);
	         dataTablePagosEmpresasInitialized = true;
                },
            error: function (data) {
            	document.getElementById("mensajesErrorModalPagosEmpresas").value =  data.responseText;

	   	    	}
            });
}




$('#tablaPagosEmpresas tbody').on('click', '.cargarPagosEmpresas', function() {

	 alert("Entre cargarPagosEmpresasa");
	var row = $(this).closest('tr'); // Encuentra la fila
	var sede = document.getElementById("sede").value;
	document.getElementById("sedesClinica_id").value =  sede;

		var table = $('#tablaPagosEmpresas').DataTable();  // Inicializa el DataTable jquery 	      

  	        var rowindex = table.row(row).data(); // Obtiene los datos de la fila


	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato pago = " , dato3.id); 
	        console.log ( "dato valor = " , dato3.valor); 
	        console.log ( "dato descripcion = " , dato3.descripcion); 
	        console.log ( "dato radicado = " , dato3.radicado); 


	document.getElementById("empresaPagoMuestra").value = dato3.id;
	document.getElementById("valorPagoMuestra").value =dato3.valor;
	document.getElementById("descripcionPagoMuestra").value = dato3.descripcion;
	document.getElementById("radicadoPagoMuestra").value = dato3.radicado;

	var data =  {}   ;
	        data['username'] = username;
		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;
	        data['pagoId'] = dato3.id;

	        data = JSON.stringify(data);

		 arrancaCartera(4,data);
	         dataTablePagosEmpresasDetalleInitialized = true;
	
		 $('#ModelPagosEmpresasDetalle').modal('show');

})


function GuardarPagosEmpresasDetalle()
{
		alert("Entre GuardarPagosEmpresasDetalle")
		var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
	        var username = document.getElementById("username").value;
	        var nombreSede = document.getElementById("nombreSede").value;
	    	var sede = document.getElementById("sede").value;
	    	var pagoId = document.getElementById("idPago").value;


            $.ajax({
                data: $('#postFormPagosEmpresasDetalle').serialize(),
	        url: "/guardarPagosEmpresasDetalle/",
                type: "POST",
                dataType: 'json',
                success: function (data2) {

		if (data2.success == true)
			 {
			  document.getElementById("mensajes").value = data2.Mensajes;
			 }
			else
			{
			document.getElementById("mensajesErrorModalPagosEmpresasDetalle").value = data2.Mensajes;
			return;
			}

		var data =  {}   ;
	        data['username'] = username;
    		data['username_id'] = username_id;
	        data['sedeSeleccionada'] = sedeSeleccionada;
	        data['nombreSede'] = nombreSede;
	        data['sede'] = sede;
	        data['sedesClinica_id'] = sede;
	        data['pagoId'] = pagoId;

		 // $('#crearModelPagosEmpresasDetalle').modal('hide');

	        data = JSON.stringify(data);

		     arrancaCartera(5,data);
	         dataTablePagosEmpresasDetalleInitialized = true;

                },

            error: function (data) {
            	document.getElementById("mensajesErrorModalPagosEmpresasDetalle").value =  data.responseText;

	   	    	}
            });
}

 $('#tablaCartera tbody').on('click', '.miCartera', function() {

        var post_id = $(this).data('pk');



	    		var table = $('#tablaCartera').DataTable();  // Inicializa el DataTable jquery
	var row = $(this).closest('tr'); // Encuentra la fila
  	        var rowindex = table.row(row).data(); // Obtiene los datos de la fila

	        console.log(" fila selecciona de vuelta AQUI PUEDE ESTAR EL PROBLEMA = " ,  table.row(row).data());
	        dato1 = Object.values(rowindex);
		console.log(" fila seleccionad d evuelta dato1 = ",  dato1);
	        dato3 = dato1[2];
		console.log(" fila selecciona de vuelta dato3 = ",  dato3);
	        console.log ( "dato pago = " , dato3.factura);
        var facturaId = dato3.factura;
        alert("entre cartera con FACTURA " + facturaId);


        var data =  {}   ;
     	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

        alert("pase01");
        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	    data['sedesClinica_id'] = sede;
	    data['facturaId'] = facturaId;
            data = JSON.stringify(data);

        		 arrancaCartera(5,data);
	         dataTableCarteraDetalleInitialized = true;
	         alert("despúes del cargue");
  });


 $('#tablaEmpresas tbody').on('click', '.miEmpresa', function() {

        var post_id = $(this).data('pk');
	var empresaId = post_id;

	alert("Entre Mi empresa");


        var data =  {}   ;
     	var sedeSeleccionada = document.getElementById("sedeSeleccionada").value;
        var username = document.getElementById("username").value;
        var nombreSede = document.getElementById("nombreSede").value;
    	var sede = document.getElementById("sede").value;
        var username_id = document.getElementById("username_id").value;

        data['username'] = username;
        data['sedeSeleccionada'] = sedeSeleccionada;
        data['nombreSede'] = nombreSede;
        data['sede'] = sede;
        data['username_id'] = username_id;
	    data['sedesClinica_id'] = sede;
	    data['empresaId'] = empresaId;
            data = JSON.stringify(data);

		document.getElementById("empresaPago").value= empresaId;
		// document.getElementById("empresaPago").disabled = true;

        		 arrancaCartera(3,data);
	         dataTablePagosEmpresasInitialized = true;


  });
