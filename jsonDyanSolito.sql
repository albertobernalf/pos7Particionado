select * from facturacion_empresas

select * from sitios_municipios
select * from sitios_departamentos

-- factura
	
		SELECT '{"tipoDocumento":' || '"' || '01' ||'",' || '"numero":'|| '"' || fac.id || '", "fecha": ' ||  '"'|| now() || '"'|| ',"moneda": "COP"'||','
	--INTO valorJson
	FROM facturacion_facturacion fac
	WHERE fac.id = 8;
	

	-- emisor
	

	SELECT '"emisor": {"nit":	' || '"' || emp.documento  || '", "dv":' || '"' || substring(emp.documento,11,1) || '",' || '"nombreRazonSocial": ' ||'"' || emp.nombre || '",'
||'"tipoPersona":"1",' ||'"direccion":{"codigomunicipio":'|| '"' || mun."municipioCodigoDian" ||'","direccion":' ||'"' || emp.direccion || '",'||'"departamento":' || '"' ||
	dep.nombre|| '"}},'
--	INTO valorJson
	FROm facturacion_empresas emp, sitios_departamentos dep, sitios_municipios mun
	WHERE emp.nombre ='CLINICA MEDICAL S.A.S' AND emp.departamento_id = dep.id and 
		mun.id=emp.municipio_id

-- receptor

		select * from usuarios_usuarios

SELECT '"receptor": {"nit": ' || usu.documento || '", "dv" : "0", "nombreRazonSocial": ' || '"' ||usu.nombre || '","tipoPersona": "2","tipoDocumentoIdentificacion": "13","direccion" : {"codigomunicipio":' || '"' || mun."municipioCodigoDian" || '",'|| 
     '"direccion": ' || '"' || usu.direccion || '","departamento":'|| '"' || dep.nombre||  '"' ||'}},'
from facturacion_facturacion fac
inner join usuarios_usuarios usu on (usu.id = fac.documento_id)
left join  sitios_departamentos dep ON (dep.id = usu.departamentos_id)
left join sitios_municipios mun ON (mun.id=usu.municipio_id)
where fac.id=8

-- detalle de los items

SELECT '"items": [{"codigoProducto":' || exa."codigoCups" || '","nombreProducto": ' || '"'|| exa.nombre || '", "cantidad": '|| det.cantidad ||'","unidadMedida": "94", "valorUnitario":' || '"' || det."valorUnitario" || '",' || '"valorTotal":' || '"' || det."valorTotal" || '","impuestos": [{"tipo": "01", 
          "porcentaje": 19.0,
          "valor": 19000.00
        }]}],'
from facturacion_facturacion fac
inner join facturacion_facturaciondetalle det ON (det.facturacion_id = fac.id And det.anulado = 'N' and det."estadoRegistro" = 'A')		
inner join clinico_examenes exa ON  (exa.id =det.examen_id)
where fac.id=8 and det.examen_id is not null		
UNION
		SELECT '"items": [{"codigoProducto":' || sum.cums || '","nombreProducto": ' || '"'|| sum.nombre || '", "cantidad": '|| det.cantidad ||'","unidadMedida": "94", "valorUnitario":' || '"' || det."valorUnitario" || '",' || '"valorTotal":' || '"' || det."valorTotal" || '","impuestos": [{"tipo": "01", 
          "porcentaje": 19.0,
          "valor": 19000.00
        }]}],'
from facturacion_facturacion fac
inner join facturacion_facturaciondetalle det ON (det.facturacion_id = fac.id And det.anulado = 'N' and det."estadoRegistro" = 'A')		
inner join facturacion_suministros sum ON  (sum.id =det.cums_id)
where fac.id=8 and det.cums_id is not null

select * from facturacion_facturaciondetalle

-- totales
SELECT
  "totales": {
    "valorBruto": 100000.00,
    "valorNeto": 100000.00,
    "valorTotalImpuestos": 19000.00,
    "valorTotal": 119000.00
  },

		
from facturacion_facturacion fac
where fac.id=8 

		


