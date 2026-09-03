select * from farmacia_farmacia where id = 4
select * from farmacia_farmaciadetalle where farmacia_id = 4
select * from farmacia_farmaciadespachos where farmacia_id = 4
select * from farmacia_farmaciadespachosdispensa where  "farmaciaDetalle_id" = 10
select * from farmacia_farmaciaestados
select * from clinico_unidadesdemedidadosis
select documento_id, "tipoDoc_id",* from clinico_historia
	select documento_id, "tipoDoc_id",* from triage_triage
select * from farmacia_farmaciadespachosdispensa order by id desc

-- Quey de despachos

SELECT disp.despacho_id, desp."usuarioEntrega_id", desp."usuarioRecibe_id", pla1.nombre, pla2.nombre
FROM farmacia_farmaciadespachos desp
inner join farmacia_farmaciadespachosdispensa disp on (disp.despacho_id = desp.id)
inner join planta_planta pla1 on (pla1.id= desp."usuarioEntrega_id")
inner join planta_planta pla2 on (pla2.id= desp."usuarioRecibe_id")
where disp."farmaciaDetalle_id" = 10 and disp.id = (select max(disp1.id) from  farmacia_farmaciadespachosdispensa disp1 where disp1."farmaciaDetalle_id" = disp."farmaciaDetalle_id")



comando ='SELECT disp.despacho_id, desp."usuarioEntrega_id", desp."usuarioRecibe_id", pla1.nombre, pla2.nombre FROM farmacia_farmaciadespachos desp inner join farmacia_farmaciadespachosdispensa disp on (disp.despacho_id = desp.id) inner join planta_planta pla1 on (pla1.id= desp."usuarioEntrega_id") inner join planta_planta pla2 on (pla2.id= desp."usuarioRecibe_id") where disp."farmaciaDetalle_id" = ' + "'" + str(detalleFarmaciaId) + "'" + ' and disp.id = (select max(disp1.id) from  farmacia_farmaciadespachosdispensa disp1 where disp1."farmaciaDetalle_id" = disp."farmaciaDetalle_id")'