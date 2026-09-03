select * from facturacion_empresas


	select * from tarifarios_tablahonorariossoat
	select cups_id,* from sitios_dependencias
	select * from clinico_examenes
	select * from tarifarios_tipostarifa --5 soat 2024
	select * from tarifarios_tipostarifaproducto -- 1 proc
	select * from clinico_servicios
		select * from sitios_serviciossedes
		select * from sitios_subserviciossedes
select * from sitios_dependencias	
	3	"S11101"	"HABITACION UNIPERSONAL"
41	"S11102"	"HABITACION BIPERSONAL"
83	"S11201"	"SERVICIO DE COMPLEJIDAD MEDIANA HABITACION UNIPERSONAL"
111	"S11301"	"SERVICIO DE COMPLEJIDAD ALTA HABITACION UNIPERSONAL"
		select * from clinico_examenes where NOMBRE LIKE ('%SALA%')
	select * from clinico_examenes where "codigoCups" IN ('S113030','S11304','S12103','S20200','S11101','S11102','S11201','S11204''S11301','S11302','S12301','S12302')
select * from rips_ripscups
select * from admisiones_ingresos
select * from tarifarios_estancias
	select * from tarifarios_tiposestancias
	update tarifarios_estancias set "tiposTarifa_id" =5
select * from tarifarios_tipostarifa
	



select * from clinico_nivelesclinica
	UPDATE clinico_nivelesclinica SET nombre = 'NIVEL III' where id=3
select * from tarifarios_nivelesestancias
select * from sitios_salas
select * from sitios_disponibilidadsalas

	select * from clinico_examenes where "codigoCups" in ('38114','38124','38134')
		select * from clinico_examenes where nombre like ('%PERSONAL%')
			select * from clinico_examenes where nombre like ('%CAMA%')
	select * from clinico_examenes where nombre like ('%CUATRO%')
		select * from clinico_examenes where nombre like ('%SOMATI%')
		select * from clinico_examenes where nombre like ('%SALA%')
		select * from clinico_examenes where nombre like ('%INTENS%')

update cirugia_ProgramacionCirugias set "fechaProgramacionInicia" ='2026-03-09',"fechaProgramacionFin" ='2026-03-09' where id= 5
update cirugia_ProgramacionCirugias set "fechaProgramacionInicia" ='2026-03-10',"fechaProgramacionFin" ='2026-03-10' where id= 4

	select * from clinico_examenes where nombre liKe ('%SALA%') -- S20200 , 3891
	select cups_id,documento_id,* 
from sitios_dependencias 

	ORDER BY documento_id
select * from tarifarios_especialidadesEnestancias	
--update sitios_dependencias set cups_id = 3891  where id =4

update clinico_especialidades set "especialidadesEnEstancias_id" = '1'  where id='1';
select * from clinico_especialidadesmedicos; --  especialiddes_id = '1'

select * from sitios_serviciossedes
	SELECT * FROM clinico_servicios
select * from tarifarios_estancias	 where id in (9,17)
	select * from sitios_subserviciossedes
		select * from sitios_dependencias
select * from contratacion_convenios
select * from tarifarios_tarifariosdescripcion
	select * from facturacion_conveniospacienteingresos
	select * from tarifarios_tarifariosdescripcion
	select * from contratacion_convenios
select * from tarifarios_estancias
	select * from tarifarios_tiposestancias
select * from cirugia_ProgramacionCirugias	
	select * from tarifarios_tiposestancias
	select documento_id,* from  admisiones_ingresos
	
-- query automatico dia a dia de estancias
begin transaction;
INSERT INTO facturacion_liquidaciondetalle(consecutivo, fecha, cantidad, "valorUnitario", "valorTotal",  "fechaCrea", 
		observaciones, "fechaRegistro", "estadoRegistro", examen_id, liquidacion_id 
		,"tipoRegistro",anulado, "codigoHomologado") 	
   
SELECT 
	(SELECT  (coalesce(max(liqDet.consecutivo), 1) +1) AS MaxX
		FROM facturacion_liquidaciondetalle liqdet
		WHERE liqDet.liquidacion_id = l1.id) consecutivo,
		now(),1,tarEstancias.valor,tarEstancias.valor,now(),'',now(),'A',tarEstancias.cups_id,l1.id,'SISTEMA','N',tarEstancias.homologado	
FROM facturacion_liquidacion l1
INNER JOIN admisiones_ingresos ing ON  (ing."tipoDoc_id" = l1."tipoDoc_id" AND ing.documento_id = l1.documento_id and ing.consec = l1."consecAdmision")
LEFT JOIN clinico_especialidadesmedicos espMed on (espMed.id = ing."especialidadesMedicosActual_id")
INNER JOIN sitios_dependencias dep on (dep.id = ing."dependenciasActual_id")
INNER JOIN sitios_serviciossedes servSedes ON (servSedes.id =dep."serviciosSedes_id" )
INNER JOIN sitios_subserviciossedes subServiciosSedes ON (subServiciosSedes.id = dep."subServiciosSedes_id")
inner JOIN clinico_servicios serv ON (serv.id = servSedes.servicios_id ANd serv.nombre in ( 'HOSPITALIZACION','URGENCIAS'))
left JOIN facturacion_conveniospacienteingresos convIng on (convIng."tipoDoc_id" = ing."tipoDoc_id" AND convIng.documento_id = ing.documento_id and convIng."consecAdmision"=ing.consec)
left JoIN contratacion_convenios conv ON (conv.id = convIng.convenio_id)
left JOIN tarifarios_tarifariosdescripcion descripcion ON (descripcion.id =conv."tarifariosDescripcionProc_id" )
left JOIN tarifarios_estancias tarEstancias ON (tarEstancias."tiposTarifa_id" = descripcion."tiposTarifa_id" AND tarEstancias.cups_id = dep.cups_id  and tarEstancias."especialidadesEnEstancias_id" = espMed.especialidades_id)
left JOIN clinico_nivelesclinica nivel ON (nivel.id = tarEstancias."nivelesClinica_id" )
left join tarifarios_tipostarifa  tiptarifa 	on (tiptarifa.id=tarEstancias."tiposTarifa_id")
INNER JOIN facturacion_empresas emp on (emp.nombre ='CLINICA MEDICAL S.A.S' AND emp."nivelesClinica_id" = nivel.id)	
	WHERE l1."sedesClinica_id" = '1' 
	
	--commit
                                                                        
select * from facturacion_liquidacion where documento_id ='4'	
	select * from facturacion_liquidaciondetalle where liquidacion_id=2 order by fecha desc
	-- rollback
select * from facturacion_empresas
select * from clinico_nivelesclinica
select documento_id,* from facturacion_conveniospacienteingresos
--  convenio 1 = alb / convenio 7 mp
select * from contratacion_convenios where id in (1,7)
select * from tarifarios_tarifariosdescripcion
select * from tarifarios_tipostarifa
select * from tarifarios_estancias
	select cups_id,"especialidadesEnEstancias_id",* from tarifarios_estancias
	select * from usuarios_usuarios  -- 1 alb /  4 mpaula
select documento_id, "especialidadesMedicosActual_id",* from admisiones_ingresos order by documento_id
select * from clinico_especialidades where id='1';
select * from clinico_especialidadesmedicos
select * from contratacion_convenios
update contratacion_convenios set "tarifariosDescripcionProc_id" = 20 where id = 1-- estaba en 20
update contratacion_convenios set "tarifariosDescripcionProc_id" = 20 where id = 1-- estaba en 1

select * from tarifarios_tarifariossuministros 

select cums_id,* from facturacion_liquidaciondetalle where liquidacion_id=2
	select * from facturacion_suministros where id = 11871 --"19914355-11"

select sum.cums cups,tarSum."codigoHomologado" homologado, sum.nombre  descripcion, detFac.cantidad cantidad,
	detFac."valorUnitario" valorUnitario, detFac."valorTotal" valorTotal
FROM facturacion_liquidaciondetalle detFac
INNER JOIN facturacion_liquidacion fac ON (fac.id=detFac.liquidacion_id) 
INNER JOIN facturacion_suministros sum on (sum.id=detFac.cums_id) 
INNER JOIN contratacion_convenios conv ON (conv.id=fac.convenio_id) 
LEFT JOIN tarifarios_tarifariosdescripcion tarDesc ON (tarDesc.id=conv."tarifariosDescripcionSum_id") 
LEFT JOIN tarifarios_tarifariossuministros tarSum ON (tarSum."tiposTarifa_id"=tarDesc."tiposTarifa_id" AND tarSum."codigoCum_id" = detFac.cums_id )
where detfac.liquidacion_id= '2' AND (detfac.anulado ='N' or detfac.anulado='R') 
	AND sum.concepto_id = '6'
ORDER BY sum.cums
	
select * from facturacion_conceptos
select * from tarifarios_tarifariossuministros -- "19914355-11" ,"1982869-1"
select * from tarifarios_tarifariossuministros -- "19914355-11" ,"1982869-1"
where "codigoCum_id" =11871
903820
select * from tarifarios_tarifariosprocedimientos where "codigoCups_id" = '903820'
select * from facturacion_facturacion order by id desc       
select examen_id,* from facturacion_facturaciondetalle where facturacion_id=9 order by fecha desc
select examen_id,"valorTotal",* from facturacion_facturaciondetalle where facturacion_id=9 and examen_id is not null order by fecha desc
select anulado,cums_id,"valorTotal",* from facturacion_facturaciondetalle where facturacion_id=9 and cums_id is not null order by fecha desc


-- Estancias del sistma RIPS

INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id)

SELECT sed."codigoHabilitacion", ' ' -- autdet."numeroAutorizacion"
	, ' '  -- his.mipres
	, facdet."fecha",	ripsOtros.id,  exa.id, 
substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal",  
(select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),
(select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), 
fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo, 
now(), 'USERNAME',detrips.id,facdet."consecutivoFactura",'9' ,'transaccionId' ,'A','INGRESOiD'	
FROM sitios_sedesclinica sed 
inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)	
inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = 'N' or facdet.anulado = 'R') And "tipoRegistro" = 'SISTEMA'  ) 
inner join clinico_examenes exa ON (exa.id = facdet."examen_id")
inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") 
inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) 
inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) 
inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) 
left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) 
inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) 
left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) 
--INNER join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id )
inner join autorizaciones_autorizaciones  aut on (aut.historia_id = his.id)	
--left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) 
--inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" ) 
inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.nombre='ESTANCIAS') 
inner join sitios_dependencias dep on (dep.id = i."dependenciasSalida_id")
inner join 	sitios_serviciossedes servSedes ON (servSedes."sedesClinica_id" = sed.id and servSedes.id =dep."serviciosSedes_id" )
inner join 	clinico_servicios serv ON (serv.id =servSedes.servicios_id )
inner join tarifarios_estancias estancias ON (estancias.cups_id= facDet.examen_id)
	where sed.id = '1' and e.id = 2 and fac.id = 9 
	and his.id in (
	select aut1.id 
	from autorizaciones_autorizaciones aut1
	inner join autorizaciones_autorizacionesdetalle autdet1 ON  (autdet1.autorizaciones_id = aut1.id and autdet1.examenes_id = facdet.examen_id) 
	where aut1.id = aut.id
	)


-- QUEDARIA ASI EL QUERY CON AUTORIZACIONES EL CAMPO INGRESO
begin transaction;
INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id)

SELECT sed."codigoHabilitacion",  autdet."numeroAutorizacion"
	, ' '  
	, facdet."fecha",	ripsOtros.id,  exa.id, 
substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal",  
(select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),
(select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), 
fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo, 
now(), 'USERNAME',detrips.id,facdet."consecutivoFactura",'9' ,'transaccionId' ,'A','INGRESOiD'	
FROM sitios_sedesclinica sed 
inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)	
inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = 'N' or facdet.anulado = 'R') And "tipoRegistro" = 'SISTEMA'  ) 
inner join clinico_examenes exa ON (exa.id = facdet."examen_id")
inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") 
inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) 
inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) 
inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) 
left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) 
inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) 
left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id)	
left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) 
inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.nombre='ESTANCIAS') 
inner join sitios_dependencias dep on (dep.id = i."dependenciasSalida_id")
inner join 	sitios_serviciossedes servSedes ON (servSedes."sedesClinica_id" = sed.id and servSedes.id =dep."serviciosSedes_id" )
inner join 	clinico_servicios serv ON (serv.id =servSedes.servicios_id )
inner join tarifarios_estancias estancias ON (estancias.cups_id= facDet.examen_id)
	where sed.id = '1' and e.id = 2 and fac.id = 9 
 -- rollback;
	
 
	select * from autorizaciones_autorizaciones
SELECT * FROM rips_ripstipootrosservicios
SELECT * FROM  sitios_dependencias
SELECT * FROM  sitios_serviciossedes
select * from clinico_servicios
select documento_id,* from admisiones_ingresos
select * from tarifarios_estancias
select * from clinico_historia where documento_id='4'

detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS", 	"tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",	"tipoPagoModerador_id",	"valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",	"ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion",  autdet."numeroAutorizacion", null, facdet."fecha",	ripsOtros.id,  exa.id, substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",	facdet."valorTotal",  (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo,  now(), ' + "'" + str(username_id) + "'" + ' ',detrips.id,facdet."consecutivoFactura",' + "'" + str('9') + "','" + str(transaccionId) + "','A','" + str(ingresoId) + "'" + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)	inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = 'N' or facdet.anulado = 'R') And "tipoRegistro" = 'SISTEMA'  ) inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.nombre=' + "'" + str('ESTANCIAS') + "'" +' inner join sitios_dependencias dep on (dep.id = i."dependenciasSalida_id") inner join 	sitios_serviciossedes servSedes ON (servSedes."sedesClinica_id" = sed.id and servSedes.id =dep."serviciosSedes_id" ) inner join 	clinico_servicios serv ON (serv.id =servSedes.servicios_id ) inner join tarifarios_estancias estancias ON (estancias.cups_id= facDet.examen_id) 	where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + 'and fac.id = ' + "'" +  str(elemento) + "'" 


begin transaction;
INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id",
	"nomTecnologiaSaludCups", "cantidadOS",   "tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS",
	"vrServicio",       "tipoPagoModerador_id", "valorPagoModerador","numFEVPagoModerador", consecutivo, 
	"fechaRegistro",   "usuarioRegistro_id",       "ripsDetalle_id", "itemFactura", "ripsTipos_id",
	"ripsTransaccion_id", "estadoReg", ingreso_id)
SELECT sed."codigoHabilitacion", autdet."numeroAutorizacion", null, facdet."fecha",     ripsOtros.id,  exa.id,
	substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",      
	facdet."valorTotal",
	(select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), 
	(select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), 
	fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo, 
	now(), '1',null, detrips.id,facdet."consecutivoFactura",'9','323','A','Ingresos object (3)' 
FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = 'N' or facdet.anulado = 'R')  And "tipoRegistro" = 'SISTEMA') inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join autorizaciones_autorizaciones  aut on (aut.ingreso_id = i.id) left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.nombre='ESTANCIAS') inner join sitios_dependencias dep on (dep.id = i."dependenciasSalida_id") inner join        sitios_serviciossedes servSedes ON (servSedes."sedesClinica_id" = sed.id and servSedes.id =dep."serviciosSedes_id" ) inner join         clinico_servicios serv ON (serv.id =servSedes.servicios_id ) inner join tarifarios_estancias estancias ON (estancias.cups_id= facDet.examen_id) 
	where sed.id = '1' and e.id = '2' and fac.id = '6'
-- rollback;	


SELECT 	(SELECT  (coalesce(max(liqDet.consecutivo), 1) +1) AS MaxX	FROM facturacion_liquidaciondetalle liqdet WHERE liqDet.liquidacion_id = l1.id) consecutivo, 
	now() fecha,1 noSe,tarEstancias.valor valorUnitario,tarEstancias.valor valor,now() fechaRegistro,'' nada,
	now() otraFecha,'A' estado,tarEstancias.cups_id cupsId,l1.id liqId,'SISTEMA' tipoTx,
	'N' anulado,tarEstancias.homologado	hmologacion
	FROM facturacion_liquidacion l1 
	INNER JOIN admisiones_ingresos ing ON  (ing."tipoDoc_id" = l1."tipoDoc_id" AND ing.documento_id = l1.documento_id and ing.consec = l1."consecAdmision") 
LEFT JOIN clinico_especialidadesmedicos espMed on (espMed.id = ing."especialidadesMedicosActual_id") 
INNER JOIN sitios_dependencias dep on (dep.id = ing."dependenciasActual_id")
INNER JOIN sitios_serviciossedes servSedes ON (servSedes.id =dep."serviciosSedes_id" )
left JOIN facturacion_conveniospacienteingresos convIng on (convIng."tipoDoc_id" = ing."tipoDoc_id" AND convIng.documento_id = ing.documento_id and convIng."consecAdmision"=ing.consec) 
left JoIN contratacion_convenios conv ON (conv.id = convIng.convenio_id) 
left JOIN tarifarios_tarifariosdescripcion descripcion ON (descripcion.id =conv."tarifariosDescripcionProc_id" ) 
left JOIN tarifarios_estancias tarEstancias ON (tarEstancias."tiposTarifa_id" = descripcion."tiposTarifa_id" AND tarEstancias.cups_id = dep.cups_id  and tarEstancias."especialidadesEnEstancias_id" = espMed.especialidades_id) 
INNER JOIN clinico_nivelesclinica nivel ON (nivel.id = tarEstancias."nivelesClinica_id" )
left join tarifarios_tipostarifa  tiptarifa 	on (tiptarifa.id=tarEstancias."tiposTarifa_id") 
INNER JOIN facturacion_empresas emp on (emp.nombre ='CLINICA MEDICAL S.A.S' AND emp."nivelesClinica_id" = nivel.id) 
--WHERE servSedes.id = tablaGeneral.servSedesId AND dep.id = tablaGeneral.depId
WHERE servSedes.id =1

	select * from sitios_serviciossedes
	select * from sitios_dependencias where documento_id='1'  -- 3
	select "dependenciasActual_id" ,* from admisiones_ingresos where documento_id ='1'
select * from contratacion_convenios	
	update contratacion_convenios set "tarifariosDescripcionProc_id" = 1 where id = 1 -- estaba en 20
	update contratacion_convenios set "tarifariosDescripcionProc_id" = 20 where id = 1 -- estaba en 20

	select * from facturacion_liquidaciondetalle

	select sum("valorTotal") 	FROM facturacion_liquidaciondetalle where liquidacion_id= 4 AND  anulado='N' AND examen_id is not null

-- 22832175
	select creaestanciaautomatica(1)
	-- 23310175

	select * from sitios_dependencias
select * from facturacion_liquidacion where id=4
	select examen_id, * from facturacion_liquidaciondetalle where liquidacion_id=4 order by fecha desc
		select examen_id, * from facturacion_liquidaciondetalle order by fecha desc

select * from autorizaciones_autorizaciones	

select * from clinico_examenes where id=41	
	update clinico_examenes set concepto_id = 1 where id=41	
	select * from rips_ripsconsultas

	select * from contratacion_convenios

update	 contratacion_convenios set "tarifariosDescripcionProc_id" = 20 where id=1

	select * from facturacion_conceptos
			select "requiereAutorizacion",* from clinico_examenes order by "requiereAutorizacion" desc


	begin transaction;
	 INSERT INTO autorizaciones_autorizaciones ("estadoAutorizacion_id","fechaModifica", "fechaRegistro", "estadoReg",empresa_id, "plantaOrdena_id", "sedesClinica_id", "usuarioRegistro_id", historia_id, convenio_id, ingreso_id )  SELECT '1', now(), now(), 'A', conv.empresa_id,  '1','1','1','252', conv.id, '1' FROM facturacion_conveniospacienteingresos convIngreso,  contratacion_convenios conv WHERE conv.id = '1' AND conv.id = convIngreso.convenio_id AND convIngreso."tipoDoc_id" = '4' AND convIngreso.documento_id = '1' AND convIngreso."consecAdmision" = '1' AND conv.id = '1' RETURNING id
	-- rollback;

	select * from autorizaciones_autorizaciones