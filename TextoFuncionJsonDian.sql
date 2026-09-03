-- FUNCTION: public.FacturaJsonDian()

-- DROP FUNCTION IF EXISTS public.FacturaJsonDian();

drop function public.FacturaJsonDian1(numeric)

	
CREATE OR REPLACE FUNCTION public.FacturaJsonDian_2(facturaId numeric)
    RETURNS character varying
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$

	DECLARE valorJson character(50000);
		valorEmisor  character(50000);
		valorReceptor character(50000);
		valorDetalle character(50000);
		valorTotales character(50000);
		valorFormaPago character(50000);

		valorFinalJson character(50000);
	    valorTransaccionYusuarios character(50000);
		contador integer := 1;
		tipo character(7) :='FACTURA';
	


BEGIN

	
if (tipo = 'FACTURA') then 

	raise notice 'entre %s', facturaId;

-- Factura

	SELECT '{"tipoDocumento": "01",' || '"numero":'|| '"' || fac.id || '", "fecha": ' ||  '"'|| now() || '"'|| ',"moneda": "COP"'||','
	INTO valorJson
	FROM facturacion_facturacion fac
	WHERE fac.id= facturaId;

raise notice 'entre2';

	valorFinalJson := valorFinalJson || ' ' || valorJson;

raise notice 'Va esto en el valorfinalJson: %s' , valorfinalJson;

-- Datos del Emisor

	SELECT '"emisor": {"nit":	' || '"' || emp.documento  || '", "dv":' || '"' || substring(emp.documento,11,1) || '",' || '"nombreRazonSocial": ' ||'"' || emp.nombre || '",'
	||'"tipoPersona":"1",' ||'"direccion":{"codigomunicipio":'|| '"' || mun."municipioCodigoDian" ||'","direccion":' ||'"' || emp.direccion || '",'||'"departamento":' || '"' ||
	dep.nombre|| '"}},'
	INTO valorEmisor
	FROm facturacion_empresas emp, sitios_departamentos dep, sitios_municipios mun
	WHERE emp.nombre ='CLINICA MEDICAL S.A.S' AND emp.departamento_id = dep.id and 
		mun.id=emp.municipio_id;

	valorFinalJson := valorFinalJson || ' ' || valorEmisor;

-- Datos del Receptor


	SELECT '"receptor": {"nit": ' || usu.documento || '", "dv" : "0", "nombreRazonSocial": ' || '"' ||usu.nombre || '","tipoPersona": "2","tipoDocumentoIdentificacion": "13","direccion" : {"codigomunicipio":' || '"' || mun."municipioCodigoDian" || '",'|| 
     '"direccion": ' || '"' || usu.direccion || '","departamento":'|| '"' || dep.nombre||  '"' ||'}},'
	INTO valorReceptor
	from facturacion_facturacion fac
	inner join usuarios_usuarios usu on (usu.id = fac.documento_id)
	left join  sitios_departamentos dep ON (dep.id = usu.departamentos_id)
	left join sitios_municipios mun ON (mun.id=usu.municipio_id)
	where fac.id=facturaId;

	valorFinalJson := valorFinalJson || ' ' || valorReceptor;

-- Detalle de ítems (Líneas)


SELECT '"items": [{"codigoProducto":' || exa."codigoCups" || '","nombreProducto": ' || '"'|| exa.nombre || '", "cantidad": '|| det.cantidad ||'","unidadMedida": "94", "valorUnitario":' || '"' || det."valorUnitario" || '",' || '"valorTotal":' || '"' || det."valorTotal" || '","impuestos": [{"tipo": "01", 
          "porcentaje": 19.0,
          "valor": 19000.00
        }]}],'
--INTO valorDetalle
from facturacion_facturacion fac
inner join facturacion_facturaciondetalle det ON (det.facturacion_id = fac.id And det.anulado = 'N' and det."estadoRegistro" = 'A')		
inner join clinico_examenes exa ON  (exa.id =det.examen_id)
where fac.id=facturaId and det.examen_id is not null		
UNION
		SELECT '"items": [{"codigoProducto":' || sum.cums || '","nombreProducto": ' || '"'|| sum.nombre || '", "cantidad": '|| det.cantidad ||'","unidadMedida": "94", "valorUnitario":' || '"' || det."valorUnitario" || '",' || '"valorTotal":' || '"' || det."valorTotal" || '","impuestos": [{"tipo": "01", 
          "porcentaje": 19.0,
          "valor": 19000.00
        }]}],'
INTO valorDetalle
from facturacion_facturacion fac
inner join facturacion_facturaciondetalle det ON (det.facturacion_id = fac.id And det.anulado = 'N' and det."estadoRegistro" = 'A')		
inner join facturacion_suministros sum ON  (sum.id =det.cums_id)
where fac.id=facturaId and det.cums_id is not null;



	valorFinalJson := valorFinalJson || ' ' || valorDetalle;

-- Totales de la factura

SELECT '"totales": {"valorBruto": ' || '"' || 	fac."totalFactura" || '","valorNeto": ' || '","valorTotalImpuestos": 0.00,"valorTotal":' || '"' || fac."valorApagar"|| '},'
INTO valorTotales
from facturacion_facturacion fac
where fac.id=facturaId ;

	valorFinalJson = valorFinalJson || ' ' || valorTotales;

-- FormaPgo

	
end if;


raise notice 'Va esto en el valorfinalJson: %s' , valorFinalJson;
	
--RETURN 'OK'; 
RETURN valorFinalJson;

END 
$BODY$;

ALTER FUNCTION public.FacturaJsonDian_2(numeric)
    OWNER TO postgres;




select FacturaJsonDian_2(8)






