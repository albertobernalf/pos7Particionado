select * from rips_ripsconsultas
select * from rips_ripsenvios
	select * from rips_ripsdetalle
select "estadoCirugia_id", "estadoProgramacion_id",* from cirugia_cirugias	 where documento_id='2'
select * from cirugia_estadoscirugias	 -- 3 esta realizada
select * from cirugia_estadosprogramacion -- 2 esta programada
select * from triage_triage

	select * from rips_ripsconsultas
	delete from rips_ripsconsultas;
	delete from rips_ripsconsultas
	select * from rips_ripsservicios
	select * from rips_ripstiposdocumento
	
INSERT INTO rips_ripsconsultas ( "codPrestador","fechaInicioAtencion","numAutorizacion","tipoDiagnosticoPrincipal", "numDocumentoIdentificacion",
	"vrServicio","valorPagoModerador","numFEVPagoModerador",consecutivo, "itemFactura",  "fechaRegistro", "estadoReg","causaMotivoAtencion_id",
	"codConsulta_id", "codDiagnosticoPrincipal_id",  "codDiagnosticoRelacionado1_id", "codDiagnosticoRelacionado2_id", "codDiagnosticoRelacionado3_id", 
	"codServicio_id", "finalidadTecnologiaSalud_id", "grupoServicios_id",ingreso_id, "modalidadGrupoServicioTecSal_id",
	"ripsDetalle_id","ripsTipos_id", "ripsTransaccion_id","tipoDocumentoIdentificacion_id", "usuarioRegistro_id")
SELECT sed."codigoHabilitacion",i."fechaIngreso",autdet."numeroAutorizacion",dxTipo.codigo,usu.documento,
	(select sum(facDet1."valorTotal")
	 FROM facturacion_facturaciondetalle facDet1 
	WHERE facDet1.anulado='N' and facDet1."estadoRegistro"='A' and facDet1.facturacion_id=fac.id ) vrServicio,
	0 valorPagoModerador,
	fac.id ,row_number()  OVER(ORDER BY facdet.id), facdet."consecutivoFactura", now(),'A', causaExternaRips.id, facdet.examen_id,
	--  aqui diagnosticos
	(select histdiag1.diagnosticos_id 
	 from clinico_historia his2
	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre='PRINCIPAL') 
	 left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)
	 where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision"
	) principal,
	(select histdiag1.diagnosticos_id 
	 from clinico_historia his2
	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre='RELACIONADO 1') 
	 left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)
	 where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision"
	) relacionado1,
	(select histdiag1.diagnosticos_id 
	 from clinico_historia his2
	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre='RELACIONADO 3') 
	 left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)
	 where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision"
	) relacionado2,
	(select histdiag1.diagnosticos_id 
	 from clinico_historia his2
	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre='RELACIONADO 3') 
	 left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)
	 where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision"
	) relacionado3,
	ripsServicios.id, finConsulta.id, grupoServicios.id,i.id ingreso, modalAtencion.id, 
	detrips.id,3,null,  tipdocrips.id   ,'1'
	--select *	
FROM sitios_sedesclinica sed
inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)
inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet.examen_id is not null and 
	(facdet.anulado = 'N' or facdet.anulado = 'R')  and "tipoRegistro" = 'SISTEMA' AND facDet.cirugia_id is not null ) 
inner join clinico_examenes exa ON (exa.id = facdet."examen_id") 
inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision")	
inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) 
inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) 
inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) 
left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) 
inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) 
inner join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec )
inner  join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) 
left join autorizaciones_autorizaciones  aut on (aut.historia_id = his.id)
left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) 
INNER JOIN 	tarifarios_tiposhonorarios hono ON (hono.id= facDet."tipoHonorario_id" and hono.nombre='CIRUJANO')
INNER JOIN sitios_dependencias dep ON (dep.id= i."dependenciasSalida_id")	
INNER JOIN sitios_serviciosSedes servSedes on (servSedes.id=dep."serviciosSedes_id")
INNER JOIN sitios_subServiciosSedes subServSedes on (subServSedes.id=dep."subServiciosSedes_id")
INNER JOIN clinico_servicios serv on (serv.id = servSedes.servicios_id AND serv.nombre='AMBULATORIO')
INNER JOIN rips_ripstipodiagnosticoPrincipal dxTipo on (dxTipo.nombre='Impresión diagnóstica')
LEFT JOIN rips_ripscausaexterna causaExternaRips ON (causaExternaRips.id = i."ripsCausaMotivoAtencion_id")
left join rips_ripsservicios ripsServicios ON (ripsServicios.id = i."ripsServiciosIng_id" )
left join rips_ripsfinalidadconsulta finConsulta ON (finConsulta.id = i."ripsFinalidadConsulta_id" )
left join rips_ripsgruposervicios grupoServicios ON (grupoServicios.id = i."ripsGrupoServicios_id" )
left join rips_ripsmodalidadatencion modalAtencion ON (modalAtencion.id = i."ripsmodalidadGrupoServicioTecSal_id" )
where sed.id = '1' and e.id = '2' and fac.id = '8'


		select * from rips_ripsconsultas
			select * from rips_ripstransaccion -- 135/138

select * from rips_ripsenvios		
		select * from rips_ripsdetalle where "ripsEnvios_id" =2
		
	left join clinico_historialdiagnosticos histdiag2	
left join  clinico_tiposdiagnostico tipoDiag2 ON (tipoDiag2.nombre='RELACIONADO 1')
left join clinico_historialdiagnosticos histdiag3
left join  clinico_tiposdiagnostico tipoDiag3 ON (tipoDiag3.nombre='RELACIONADO 2')
left join clinico_historialdiagnosticos histdiag4
left join  clinico_tiposdiagnostico tipoDiag4 ON (tipoDiag4.nombre='RELACIONADO 3')
	
	select * from clinico_tiposdiagnostico
select * from clinico_historialdiagnosticos WHERE HISTORIA_ID IN (select ID from clinico_historia where documento_id='2')
select * from rips_ripstipos
	
	select * from rips_ripsservicios
select * from admisiones_ingresos	
	select * from rips_ripscausaexterna
	select * from clinico_causasexterna
	
select * from clinico_historia where documento_id='2'

	
select * from clinico_servicios
	select * from admisiones_ingresos where documento_id='2' -- 10 dependenciasalida_id
	select * from sitios_dependencias where id=10 -- subsrviciosSedes_id
	select * from sitios_subserviciossedes where id=5
	select * from sitios_serviciossedes where id=5
	select cirugia_id,* from facturacion_facturaciondetalle where facturacion_id=8


comando = 'INSERT INTO rips_ripsconsultas ( "codPrestador","fechaInicioAtencion","numAutorizacion","tipoDiagnosticoPrincipal", "numDocumentoIdentificacion","vrServicio","valorPagoModerador","numFEVPagoModerador",consecutivo, "itemFactura",  "fechaRegistro", "estadoReg","causaMotivoAtencion_id","codConsulta_id", "codDiagnosticoPrincipal_id",  "codDiagnosticoRelacionado1_id", "codDiagnosticoRelacionado2_id", "codDiagnosticoRelacionado3_id", "codServicio_id", "finalidadTecnologiaSalud_id", "grupoServicios_id",ingreso_id, "modalidadGrupoServicioTecSal_id","ripsDetalle_id","ripsTipos_id", "ripsTransaccion_id","tipoDocumentoIdentificacion_id", "usuarioRegistro_id") SELECT sed."codigoHabilitacion",i."fechaIngreso",autdet."numeroAutorizacion",dxTipo.codigo,usu.documento,	(select sum(facDet1."valorTotal") 	 FROM facturacion_facturaciondetalle facDet1 WHERE facDet1.anulado='N' and facDet1."estadoRegistro"='A' and facDet1.facturacion_id=fac.id ) vrServicio, 	0 valorPagoModerador, 	fac.id ,row_number()  OVER(ORDER BY facdet.id), facdet."consecutivoFactura", now(),' + "'" + str('A') + "'" + ', causaExternaRips.id, facdet.examen_id, 	(select histdiag1.diagnosticos_id from clinico_historia his2 left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('PRINCIPAL') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)  where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision" 	) principal,(select histdiag1.diagnosticos_id  from clinico_historia his2	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('RELACIONADO 1') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)  where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision" 	) relacionado1,	(select histdiag1.diagnosticos_id  from clinico_historia his2 	left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('RELACIONADO 3') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id)  where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision" 	) relacionado2,	(select histdiag1.diagnosticos_id  from clinico_historia his2 left join clinico_tiposdiagnostico tipoDiag1 ON (tipoDiag1.nombre=' + "'" + str('RELACIONADO 3') + "')" + ' left join clinico_historialdiagnosticos histdiag1 on (histdiag1.historia_id =his2.id) where his2."tipoDoc_id" = his."tipoDoc_id" AND his2.documento_id = his.documento_id and his2."consecAdmision" = his."consecAdmision") relacionado3, ripsServicios.id, finConsulta.id, grupoServicios.id,i.id ingreso, modalAtencion.id, detrips.id,3,null,  tipdocrips.id   ,' + "'" + str(usrname_id) + "'" + ' FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet.examen_id is not null and 	(facdet.anulado = ' + "'" + str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') +"'" + ' and "tipoRegistro" = ' + "'" + str('SISTEMA') + "'" + ' AND facDet.cirugia_id is not null ) inner join clinico_examenes exa ON (exa.id = facdet."examen_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision")	 inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) inner join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) inner  join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) left join autorizaciones_autorizaciones  aut on (aut.historia_id = his.id) left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) INNER JOIN 	tarifarios_tiposhonorarios hono ON (hono.id= facDet."tipoHonorario_id" and hono.nombre=' + "'" + str('CIRUJANO') + "')" + ' INNER JOIN sitios_dependencias dep ON (dep.id= i."dependenciasSalida_id") INNER JOIN sitios_serviciosSedes servSedes on (servSedes.id=dep."serviciosSedes_id") INNER JOIN sitios_subServiciosSedes subServSedes on (subServSedes.id=dep."subServiciosSedes_id") INNER JOIN clinico_servicios serv on (serv.id = servSedes.servicios_id AND serv.nombre=' + "'" + str('AMBULATORIO') + "')" + ' INNER JOIN rips_ripstipodiagnosticoPrincipal dxTipo on (dxTipo.nombre=' + "'"  +  str('Impresión diagnóstica') + "')" + ' LEFT JOIN rips_ripscausaexterna causaExternaRips ON (causaExternaRips.id = i."ripsCausaMotivoAtencion_id") left join rips_ripsservicios ripsServicios ON (ripsServicios.id = i."ripsServiciosIng_id" ) left join rips_ripsfinalidadconsulta finConsulta ON (finConsulta.id = i."ripsFinalidadConsulta_id" ) left join rips_ripsgruposervicios grupoServicios ON (grupoServicios.id = i."ripsGrupoServicios_id" ) left join rips_ripsmodalidadatencion modalAtencion ON (modalAtencion.id = i."ripsmodalidadGrupoServicioTecSal_id" ) where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"

		select * from rips_ripscups
		select * from rips_ripscums where cum='1980578-1'

		select * from facturacion_suministros  where nombre like ('%COPIN%')
		where id=2
		select * from clinico_examenes where id = 91
		select * from rips_RipsCums

-- esto fallo
INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSaludCups_id", "nomTecnologiaSaludCups", "cantidadOS",   "tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",       "tipoPagoModerador_id", "valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",       "ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id)
SELECT sed."codigoHabilitacion", autdet."numeroAutorizacion", his.mipres, facdet."fecha",       ripsOtros.id,  exa.id,  
		substring(exa.nombre,1,60) , facdet.cantidad, tipdocrips.id, usu.documento,facdet."valorUnitario",      facdet."valorTotal", 
		(select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora ,
		cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec
		and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and
		ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), 
		(select carFac."valorAplicado" 
		from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac
		where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and 
		carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), fac.id, 
		row_number()  OVER(ORDER BY facdet.id) +   3   AS consecutivo, now(), '1',detrips.id,facdet."consecutivoFactura",'9','144','A','8' 
		FROM sitios_sedesclinica sed 
		inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)
        inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."examen_id" is not null and (facdet.anulado = 'N' or facdet.anulado = 'R') and "tipoRegistro" = 'SISTEMA' AND facDet.cirugia_id is not null)
		inner join clinico_examenes exa ON (exa.id = facdet."examen_id")
		inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") 
		inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) 
		inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) 
		inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) 
		left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec )
		INNER join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id )
		left join autorizaciones_autorizaciones  aut on (aut.historia_id = his.id)
		left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id)
		inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" )
		inner join rips_ripstipootrosservicios ripsOtros on ( ripsOtros.id=tipHonor."ripsTipoOtrosServicios_id" and ripsOtros.nombre='HONORARIOS')
		where sed.id = '1' and e.id = '2' and fac.id = '8'

		-- OPS ES POR QUE ES MANUAL OJO LO MISMO VER SISTEMA Y MANUAL AMBOS
		-- QUERYS Y CORREGIRLOS MAÑANA
		
-- Parece este es el query que falla
select * from	rips_ripsotrosservicios -- el id : 85 y 86 mal subidos
begin transaction;
		INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSalud_id",       "nomTecnologiaSalud", "cantidadOS",     "tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",       "tipoPagoModerador_id", "valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",       "ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) 	
SELECT sed."codigoHabilitacion", autdet."numeroAutorizacion", his.mipres, facdet."fecha",   ripsOtros.id,  exa.id,  substring(exa.nombre,1,60), facdet.cantidad,        tipdocrips.id, usu.documento,facdet."valorUnitario",    facdet."valorTotal",
		(select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), 
		(select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),  
		fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo, now(), '1',detrips.id,facdet."consecutivoFactura",'9','177','A','8'     
		FROM sitios_sedesclinica sed 
		inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id)
		inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."cums_id" is not null and (facdet.anulado = 'N' or facdet.anulado = 'R') and "tipoRegistro" = 'MANUAL' AND facDet.cirugia_id is not null)
		inner join facturacion_suministros exa ON (exa.id = facdet."cums_id")
		inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") 
		inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id) 
		inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id)
		inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" )
		left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" )
		inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) 
		left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) 
		inner join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) 
		left join autorizaciones_autorizaciones  aut on (aut.historia_id = his.id) 
		left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id)
		inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" and tipHonor.nombre ='MATERIALES DE SUTURA Y CURACIO')
		inner join rips_ripstipootrosservicios ripsOtros on (ripsOtros.id=tipHonor."ripsTipoOtrosServicios_id"  )
		--and ripsOtros.nombre='DISPOSITIVOS MEDICOS E INSUMOS') 	
		where sed.id = '1' and e.id = '2' and fac.id = '8'
-- rollback  
select * from tarifarios_tiposhonorarios -- tipohonorario 5 "MATERIALES DE SUTURA Y CURACIO"

select anulado, "tipoRegistro",cirugia_id,cums_id,"tipoHonorario_id",* from facturacion_facturaciondetalle where facturacion_id=8 -- 2908		 -- 2908 ojo hay que colocar el tipoHonorario_id= 5 de la cirugia en el cums_id
-- ES COMPELJO MALIDAR
		update facturacion_facturaciondetalle set "tipoHonorario_id" = '5' where id=32
		
		select * from facturacion_suministros where id =2908 -- "1980578-1"


detalle = 'INSERT INTO rips_ripsotrosservicios ( "codPrestador", "numAutorizacion", "idMIPRES", "fechaSuministroTecnologia","tipoOS_id", "codTecnologiaSalud_id","nomTecnologiaSalud", "cantidadOS",     "tipoDocumentoIdentificacion_id", "numDocumentoIdentificacion", "vrUnitOS", "vrServicio",       "tipoPagoModerador_id", "valorPagoModerador","numFEVPagoModerador", consecutivo, "fechaRegistro",   "usuarioRegistro_id",       "ripsDetalle_id", "itemFactura", "ripsTipos_id", "ripsTransaccion_id", "estadoReg", ingreso_id) SELECT sed."codigoHabilitacion", autdet."numeroAutorizacion", his.mipres, facdet."fecha",   ripsOtros.id,  exa.id,  substring(exa.nombre,1,60), facdet.cantidad,        tipdocrips.id, usu.documento,facdet."valorUnitario",    facdet."valorTotal", (select max(ripsmoderadora.id) from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)), (select carFac."valorAplicado" from cartera_pagos pagos, cartera_formaspagos formapago, rips_ripstipospagomoderador ripsmoderadora , cartera_pagosfacturas carFac where i."tipoDoc_id" = pagos."tipoDoc_id" and i.documento_id = pagos.documento_id and i.consec = pagos.consec and carFac.pago_id = pagos.id and pagos."formaPago_id" = formapago.id and ripsmoderadora."codigoAplicativo" = cast(formapago.id as text)),  fac.id, row_number()  OVER(ORDER BY facdet.id)  AS consecutivo, now(), ' + "'" + str(username_id) + "'" + ',detrips.id,facdet."consecutivoFactura",'  + "'" + str('9') + "'" + ','  + str(transaccionId) + ",'" + str('A') + "'" + ',i.id  FROM sitios_sedesclinica sed inner join facturacion_facturacion fac ON (fac."sedesClinica_id" = sed.id) inner join facturacion_facturaciondetalle facdet ON (facdet.facturacion_id = fac.id and facdet."cums_id" is not null and (facdet.anulado = ' + "'" +str('N') + "'" + ' or facdet.anulado = ' + "'" + str('R') + "'" + ') and "tipoRegistro" = ' + "'" + str('SISTEMA') + "'" + ' AND facDet.cirugia_id is not null) inner join facturacion_suministros exa ON (exa.id = facdet."cums_id") inner join admisiones_ingresos i on (i."tipoDoc_id" = fac."tipoDoc_id" and i.documento_id = fac.documento_id and i.consec = fac."consecAdmision") inner join rips_ripsenvios e ON (e."sedesClinica_id" = sed.id)  inner join rips_ripsdetalle detrips ON (detrips."ripsEnvios_id" = e.id and detrips."numeroFactura_id" = fac.id) inner join usuarios_tiposdocumento tipdoc ON (tipdoc.id = fac."tipoDoc_id" ) left join  rips_ripstiposdocumento tipdocrips on (tipdocrips.id = tipdoc."tipoDocRips_id" ) 	inner join usuarios_usuarios usu ON (usu."tipoDoc_id" = fac."tipoDoc_id" and usu.id = fac.documento_id ) left join clinico_historia his ON (his."tipoDoc_id" = i."tipoDoc_id" and his.documento_id = i.documento_id and his."consecAdmision" = i.consec ) inner join clinico_historialcirugias hisCiru ON (hisCiru.historia_id = his.id and hisCiru.cirugia_id = facDet.cirugia_id) left join autorizaciones_autorizaciones  aut on (aut.historia_id = his.id) left join autorizaciones_autorizacionesdetalle autdet on (autdet.autorizaciones_id = aut.id and autdet.examenes_id = facdet.examen_id) inner join tarifarios_tiposhonorarios tipHonor on ( tipHonor.id = facDet."tipoHonorario_id" and tipHonor.nombre =' + "'" + str('MATERIALES DE SUTURA Y CURACIO') + "')" + ' inner join rips_ripstipootrosservicios ripsOtros on (ripsOtros.id=tipHonor."ripsTipoOtrosServicios_id") where sed.id = ' + "'" + str(sede) + "'" + ' and e.id = ' + "'" + str(envioRipsId) + "'" + ' and fac.id = ' + "'" + str(elemento) + "'"


select * from cirugia_programacioncirugias
update cirugia_programacioncirugias set "fechaProgramacionInicia" = '2026-03-05', "fechaProgramacionFin" = '2026-03-05' where id=4
update cirugia_programacioncirugias set "fechaProgramacionInicia" = '2026-03-06', "fechaProgramacionFin" = '2026-03-06' where id=5

select * from sitios_disponibilidadsalas
update sitios_disponibilidadsalas set fecha='2026-03-05' where id=1
update sitios_disponibilidadsalas set fecha='2026-03-06' where id=9
update sitios_disponibilidadsalas set fecha='2026-03-06' where id=10
			select * from rips_ripsconsultas
			DELETE FROM rips_ripsconsultas WHERE "ripsTransaccion_id" IS NULL
			select * from clinico_examenes where id=91

			select * from clinico_diagnosticos
			select * from rips_ripstransaccion

select * from rips_ripsotrosservicios			
			update rips_ripsconsultas set "ripsTransaccion_id" = 237


		SELECT '{"codPrestador": '|| '"' || consulta."codPrestador" || '"' 
			||',"fechaInicioatencion": '|| '"' || substring(cast(consulta."fechaInicioAtencion" as text), 1,16) || '"'  		
	   ||',"numAutorizacion": '|| '"' || CASE WHEN consulta."numAutorizacion" is null THEN 'null' ELSE consulta."numAutorizacion"  END || '"'		
	||',"codConsulta": '|| '"' || CASE WHEN consulta."codConsulta_id" is null THEN 'null' ELSE exa."codigoCups"  END || '"'		
	||',"modalidadGrupoServicioTecSal": '|| '"' || case when modalidadAtencion.codigo is null then 'null' else modalidadAtencion.codigo end   || '"'		
	||',"grupoServicios": '|| '"' || case when grupoServicios.codigo is null then 'null' else grupoServicios.codigo end   || '"'	
	||',"codServicio": '|| '"' || case when servicios.codigo is null then 'null' else servicios.codigo end   || '"'	
	||',"finalidadTecnologiaSalud": '|| '"' || case when finalidadConsulta.codigo is null then 'null' else finalidadConsulta.codigo end   || '"'	
			||',"causaMotivoAtencion": '|| '"' || case when causaExterna.codigo is null then 'null' else causaExterna.codigo end   || '"'				
	||',"codDiagnosticoPrincipal": '|| '"' || case when diag1.cie10 is null then 'null' else diag1.cie10 end   || '"'				
	||',"codDiagnosticoRelacionado1": '|| '"' || case when diag2.cie10 is null then 'null' else diag2.cie10 end   || '"'				
	||',"codDiagnosticoRelacionado2": '|| '"' || case when diag3.cie10 is null then 'null' else diag3.cie10 end   || '"'				
	||',"codDiagnosticoRelacionado3": '|| '"' || case when diag4.cie10 is null then 'null' else diag4.cie10 end   || '"'							
	||',"tipoDiagnosticoPrincipal": '|| '"' || case when "tipoDiagnosticoPrincipal" is null then 'null' else "tipoDiagnosticoPrincipal" end   || '"'		
	||',"tipoDocumentoIdentificacion": '|| '"' || ripsTiposDoc.codigo  || '"'					
	||',"numDocumentoIdentificacion":  '|| '"' || CASE WHEN consulta."numDocumentoIdentificacion" is null THEN 'null' ELSE consulta."numDocumentoIdentificacion"  END  || '"'					
	||',"vrServicio": '|| consulta."vrServicio"   || ''		
	||',"tipoPagoModerador": '|| '"' || case when modera.codigo is null then 'null' else modera.codigo end   || '"'		
	||',"valorPagoModerador": '||  CASE WHEN cast(consulta."valorPagoModerador" as text) is null THEN 0 ELSE consulta."valorPagoModerador"  END  || ''
	||',"numFEVPagoModerador": '|| '"' || consulta."numFEVPagoModerador" || '"'				
||',"consecutivo": '||  consulta."consecutivo" ||'	},'
    INTO valorConsultas
	from rips_ripstransaccion ripstra
	inner join rips_ripsconsultas consulta on (consulta."ripsTransaccion_id" = ripstra.id)
	left join clinico_examenes exa on (exa.id = consulta."codConsulta_id" )
	left join rips_ripsmodalidadatencion modalidadAtencion ON (modalidadAtencion.id=consulta."modalidadGrupoServicioTecSal_id")
	left join rips_ripsgruposervicios grupoServicios ON (grupoServicios.id=consulta."grupoServicios_id")
	left join rips_ripsservicios servicios ON (servicios.id=consulta."codServicio_id")
	left join rips_ripsfinalidadconsulta finalidadConsulta ON (finalidadConsulta.id=consulta."finalidadTecnologiaSalud_id")
	left join rips_ripscausaexterna causaExterna ON (causaExterna.id=consulta."causaMotivoAtencion_id")
	left join clinico_diagnosticos diag1 ON (diag1.id=consulta."codDiagnosticoPrincipal_id")
	left join clinico_diagnosticos diag2 ON (diag2.id=consulta."codDiagnosticoRelacionado1_id")
	left join clinico_diagnosticos diag3 ON (diag3.id=consulta."codDiagnosticoRelacionado2_id")
	left join clinico_diagnosticos diag4 ON (diag4.id=consulta."codDiagnosticoRelacionado3_id")			
	inner join rips_ripstiposdocumento ripsTiposDoc on (ripsTiposDoc.id = consulta."tipoDocumentoIdentificacion_id" )		
	left join rips_ripstipospagomoderador modera on (modera.id=consulta."tipoPagoModerador_id")
	where  ripstra."ripsEnvio_id" = envioRipsId AND  ripstra."numFactura" = cast(facturaId as text) AND consulta.consecutivo = i; 
   where  ripstra."ripsEnvio_id" = '2' AND  ripstra."numFactura" = cast('8' as text) AND consulta.consecutivo >=1; 


select * from rips_ripsconsultas
	select * from clinico_examenes where id=91-- codigoCups
	select * from facturacion_suministros  where id=91--cums

	select * from rips_ripsotrosservicios
	select * from sitios_disponibilidadsalas
	SELECT prog.id,  prog."fechaProgramacionInicia" fechaProgramacionInicia, prog."fechaProgramacionFin" fechaProgramacionFin,        prog."horaProgramacionInicia" horaProgramacionInicia, prog."horaProgramacionFin" horaProgramacionFin , usu.nombre nombrePaciente FROM cirugia_programacioncirugias prog INNER JOIN usuarios_usuarios usu ON (usu.id = prog.documento_id ) WHERE prog.sala_id = '3' AND prog."fechaProgramacionInicia" = '2026-03-06' ORDER BY  prog."horaProgramacionInicia"


  SELECT dispoSalas.id id , dispoSalas.id dispoId , dispoSalas.fecha, dispoSalas."desdeHora", dispoSalas."hastaHora", dispoSalas."estadoDisponibilidad" FROM sitios_disponibilidadsalas dispoSalas, sitios_salas salas WHERE salas.id = '3' AND  salas.id = dispoSalas.salas_id  AND disposalas.fecha = '2026-03-05' ORDER BY "desdeHora", "hastaHora"
