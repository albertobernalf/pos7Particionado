select factura,* from facturacion_facturacion order by id desc
select factura,* from facturacion_liquidacion order by id desc

SELECT distinct con.id, con.nombre nombreConcepto 
from facturacion_conceptos con  
INNER JOIN facturacion_liquidaciondetalle facDet  ON (facDet.concepto_id = con.id and con.nombre != 'MATERIAL QX Y/O MATERIAL ESPEC')
INNER JOIN clinico_examenes exa ON (exa.id= facDet.examen_id)
where facdet.liquidacion_id = '4' 
union 
SELECT distinct con.id, con.nombre nombreConcepto 
from facturacion_conceptos con 
INNER JOIN facturacion_liquidaciondetalle facDet  ON (facDet.concepto_id = con.id and con.nombre != 'MATERIAL QX Y/O MATERIAL ESPEC') 
INNER JOIN facturacion_suministros sum ON (sum.id = facDet.cums_id) 
where facdet.liquidacion_id = '4' 
order by 1 asc

select cums_id, examen_id,concepto_id, * from facturacion_liquidaciondetalle where liquidacion_id = 4

select * from facturacion_empresas;
select * from facturacion_conceptos;
select concepto_id,* from clinico_examenes
-- 197
select count(*) from  facturacion_liquidaciondetalle where liquidacion_id = 4
begin transaction;
update facturacion_liquidaciondetalle det
set concepto_id = (select exa.concepto_id from clinico_examenes exa
					where exa.id = det.examen_id)
 where liquidacion_id = 4 and examen_id is not null
 select cums_id, examen_id,concepto_id, * from facturacion_liquidaciondetalle where liquidacion_id = 4
 --rollback;
 -- commit

  SELECT "consecutivoFactura" 

		  FROM facturacion_facturaciondetalle det
		  WHERE det.facturacion_id = 25 And det.anulado in ('N','R') 
		  and det."estadoRegistro" = 'A' and det.examen_id is not null;


 SELECT FacturaJsonDian_2(9) dato

 select * from facturacion_liquidacion order by id desc
 select documento_id,* from facturacion_facturacion order by id desc

select facturacion_id, count(*) from facturacion_facturaciondetalle group by facturacion_id

select "consecutivoFactura", cums_id,examen_id,* from  facturacion_facturaciondetalle
where facturacion_id=13 and examen_id is not null
order by "consecutivoFactura"

begin transaction;
update facturacion_liquidaciondetalle det
set concepto_id = (select exa.concepto_id from facturacion_suministros exa
					where exa.id = det.cums_id)
 where liquidacion_id = 4 and cums_id is not null
 select cums_id, examen_id,concepto_id, * from facturacion_liquidaciondetalle where liquidacion_id = 4
 --rollback;
sELECT FacturaJsonDian_2(535)

select prefijo,* from facturacion_facturacion order by id desc

select * from facturacion_empresas

update facturacion_empresas set direccion = 'Calle 68 Avenida 26'
where id=1

    	    SELECT '{"codigoProducto":' || '"' || exa."codigoCups" || '","nombreProducto": ' || '"'|| exa.nombre || '", "cantidad": '|| det.cantidad ||',"unidadMedida": "94", "valorUnitario":' || '"' || det."valorUnitario" || '",' || '"valorTotal":' || '"' || det."valorTotal" || '","impuestos": {"tipo": "01","porcentaje": 0.0,"valor": 0.00}},'
		    from facturacion_facturacion fac
		    inner join facturacion_facturaciondetalle det ON (det.facturacion_id = fac.id And det.anulado in ('N','R') and det."estadoRegistro" = 'A')		
		    inner join clinico_examenes exa ON  (exa.id =det.examen_id)
	        where fac.id=535 and det.examen_id is not null	;
			---and det."consecutivoFactura" = consecExamen;
select examen_id,cums_id,* from facturacion_facturaciondetalle 
where facturacion_id=535
select * from usuarios_usuarios where id=8
select documento_id,"codigoQr",* from facturacion_facturacion where id=535
update 
select * from clinico_examenes where id=2807

select * from facturacion_liquidacion where documento_id='8'
select anulado, "estadoReg",* from facturacion_facturacion
where documento_id='8'
select * from facturacion_facturaciondetalle where facturacion_id=535

 select documento_id,* from admisiones_ingresos where id = 13
 select * from facturacion_conveniospacienteingresos where documento_id='13'

select fac.id id, fac.id factura, fac."fechaFactura" fechaFactura,
tip.nombre tipoDoc, usu.documento documento, usu.nombre paciente, 
fac."consecAdmision" consecAdmision, conv.nombre nombreConvenio, 
"totalSuministros","totalProcedimientos","totalCopagos","totalCuotaModeradora",
"totalAbonos","totalRecibido", anticipos totalAnticipos,"valorApagar",
"totalFactura" , "valorAPagarLetras" , fac."estadoReg" estadoReg,
fac.anulado anulado, "rutaXml" rutaXml, "rutaJson" rutaJson, "rutaPdf" rutaPdf
FROM facturacion_facturacion fac, contratacion_convenios conv,
usuarios_usuarios usu, usuarios_tiposdocumento tip
where fac.id =535  AND
fac.convenio_id = conv.id and usu.id = fac.documento_id  and
fac."tipoDoc_id" = usu."tipoDoc_id"   AND tip.id = fac."tipoDoc_id" 
AND fac.documento_id = usu.id  
AND conv.id = fac.convenio_id 

-- Este query tiene problemas

select liq.id id,"consecutivoFactura" consecutivo ,  cast(date(fecha)||' '||to_char(fecha, 'HH:MI:SS') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||' '||to_char("fechaCrea", 'HH:MI:SS') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , exa.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg 
FROM facturacion_facturaciondetalle liq
inner join clinico_examenes exa on (exa.id = liq."examen_id")  
where facturacion_id= '535' -- AND "estadoRegistro" = 'A' 
and (anulado='N' or anulado = 'R' )
UNION 
select liq.id id,"consecutivoFactura"  consecutivo,
cast(date(fecha)||' '||to_char(fecha, 'HH:MI:SS') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||' '||to_char("fechaCrea", 'HH:MI:SS') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg 
FROM facturacion_facturaciondetalle liq 
inner join facturacion_suministros sum on (sum.id = liq.cums_id) 
where facturacion_id= '535' -- AND "estadoRegistro" = 'A' 
and (anulado='N' or anulado = 'R' )
order by consecutivo

select * from facturacion_facturaciondetalle where facturacion_id=535
select * from facturacion_facturacion where id=535

select liq.id id,"consecutivoFactura" consecutivo ,  cast(date(fecha)||' '||to_char(fecha, 'HH:MI:SS') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||' '||to_char("fechaCrea", 'HH:MI:SS') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , exa.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg 
FROM facturacion_facturaciondetalle liq
inner join clinico_examenes exa on (exa.id = liq."examen_id") 
where facturacion_id= '322' AND (anulado='N' OR anulado = 'R')
UNION 
select liq.id id,"consecutivoFactura"  consecutivo, cast(date(fecha)||' '||to_char(fecha, 'HH:MI:SS') as text) fecha  ,  liq.cantidad ,  "valorUnitario" ,  "valorTotal" ,  cirugia_id ,  cast(date("fechaCrea")||' '||to_char("fechaCrea", 'HH:MI:SS') as text)  fechaCrea , liq.observaciones ,  "estadoRegistro" ,  "examen_id" ,  cums_id , sum.nombre  nombreExamen  ,  facturacion_id ,  liq."tipoHonorario_id" ,  "tipoRegistro" , liq."estadoRegistro" estadoReg 
FROM facturacion_facturaciondetalle liq 
inner join facturacion_suministros sum on (sum.id = liq.cums_id) 
where facturacion_id= '322' AND (anulado='N' or anulado = 'R') 
order by consecutivo
