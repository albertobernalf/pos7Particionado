select * from enfermeria_enfermeria
select * from enfermeria_enfermeriadetalle where enfermeria_id=4 order by id

	select * from enfermeria_enfermeriarecibe;
select documento_id,* from clinico_historia where documento_id=2
	select * from usuarios_usuarios where id=4
	select historia_id,* from clinico_historiamedicamentos where historia_id=9 order by id

	select * from farmacia_farmacia
	select * from planta_planta
		select * from farmacia_farmaciadespachos order by id
	select * from farmacia_farmaciadespachosdispensa where despacho_id=1 order by id
	select * from farmacia_farmaciadespachosdispensa

select rec.id,enf.id, enf.historia_id folio,rec."dosisCantidad",  rec."cantidadDispensada", rec."dosisUnidad_id", rec.suministro_id, rec."viaAdministracion_id" ,* 
	from  enfermeria_enfermeria enf
inner join enfermeria_enfermeriadetalle det on (enfermeria_id=enf.id)
inner join 	enfermeria_enfermeriarecibe rec on (rec."enfermeriaDetalle_id" = det.id)
 where enf.id=1
order by rec.id

select documento_id,folio,* from clinico_historia  order by  documento_id,folio
select historia
	_id,* from clinico_historiaexamenes order by id
select * from clinico_historiaexamenes where  historia_id in (1,6,7)
select * from enfermeria_enfermeriaplaneacion
select * from clinico_historia order by id

select * from clinico_historialnotasenfermeria
select * from clinico_historia;
select * from clinico_historialdietas;
select * from enfermeria_enfermeriadevolucion
select * from enfermeria_enfermeriadevoluciondetalle