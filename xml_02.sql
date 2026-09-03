select * from facturacion_empresas
UPDATE facturacion_empresas SET nombre= 'CLINICA SET DE PRUEBA ALBERTO',
                          direccion= 'Calle 87 # 12-30', telefono='1111',
						   correo='alberto_bernalf@yahoo.com.co',
						   documento='889988999-7'
						   where id='3'

select * from usuarios_usuarios where id='8';
update usuarios_usuarios set nombre='MARIA CAMILA PRUEBAS CORTEZ',
                          "primerApellido"='PRUEBAS',"segundoApellido"='CORTEZ',
						    correo='alberto_bernalf@yahoo.com.co', telefono='1111',
							 direccion='Avenida calatraba'
							 where id='8';
select * from clinico_historia
select * from facturacion_facturaciondetalle order by id desc
select * from facturacion_liquidaciondetalle order by id desc

select documento_id,* from admisiones_ingresos where id='13'
select * from facturacion_liquidacion where documento_id='8'
select examen_id,cums_id,anulado,"estadoRegistro",* from facturacion_liquidaciondetalle where liquidacion_id=32

select documento_id,* from facturacion_facturacion order by id desc
SELECT FacturaJsonDian_2(536) dato

	SELECT '{"emisor":{"nit":'||'"'||emp.documento|| '", "dv":'||'"'|| substring(emp.documento,11,1) || '",' || '"nombreRazonSocial": ' ||'"' || emp.nombre || '",'||'"tipoPersona":"1",' || '"correo":'||	'"' || CASE WHEN trim(cast(emp.correo as text)) is null THEN null ELSE emp.correo  END   ||   '","telefono":'||	'"' || CASE WHEN trim(cast(emp.telefono as text)) is null THEN null ELSE emp.telefono  END  || '","ciudadCodigo":'||	'"'|| CASE WHEN trim(cast(ciu."ciudadCodigoDian" as text)) is null THEN null ELSE ciu."ciudadCodigoDian"  END  || '","ciudadNombre":'||	'"'|| CASE WHEN trim(cast(ciu.nombre as text)) is null THEN null ELSE ciu.nombre  END  || '","paisCodigo":'||	'"'|| CASE WHEN trim(cast(pais."paisCodigoDian" as text)) is null THEN null ELSE pais."paisCodigoDian"  END  || '","paisNombre":'||	'"'|| CASE WHEN trim(cast(pais.nombre as text)) is null THEN null ELSE pais.nombre  END  ||'","direccion":{"codigomunicipio":'|| '"' || mun."municipioCodigoDian" ||'","direccion":' ||'"' || emp.direccion || '",'||'"departamento":' || '"' ||dep."departamentoCodigoDian"  || '",'||'"pais":' || '"' ||pais."paisCodigoDian"  || '"}}},'
	
	FROm facturacion_empresas emp
	LEFT JOIN sitios_departamentos dep ON (dep.id=emp.departamento_id)
	LEFT JOIN sitios_municipios mun ON (mun.id=emp.municipio_id)
	LEFT JOIN sitios_ciudades ciu ON (ciu.id=emp.ciudad_id)
	LEFT JOIN sitios_paises  pais ON (pais.id=emp.departamento_id)
	WHERE emp.nombre ='CLINICA MEDICAL S.A.S';

	select * from facturacion_empresas
CLINICA SET DE PRUEBA ALBERTO
						