/*
Se envia Para datos abirtos de la web

*/

SELECT 
	m.bikeMemberAttributes_gender AS Genero_Usuario,
	TIMESTAMPDIFF(YEAR, CONVERT_TZ("1970-01-01" + INTERVAL (r.member_birthday/1000) SECOND, 'UTC', 'America/Costa_Rica'), CURDATE()) AS Edad_Usuario,
	b.displayedNumber AS Bici,
	stationOrig.logicalTerminal AS Ciclo_Estacion_Retiro,
	DATE_FORMAT(DATE(CONVERT_TZ(FROM_UNIXTIME(r.startTimeMs/1000), 'UTC', 'America/Costa_Rica')), '%%d/%%m/%%Y') AS Fecha_Retiro,
	DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME((r.startTimeMs)/1000), 'UTC', 'America/Costa_Rica'), '%%H:%%i:%%s') AS Hora_Retiro,
	stationDest.logicalTerminal AS Ciclo_EstacionArribo,
	DATE_FORMAT(DATE(CONVERT_TZ(FROM_UNIXTIME(r.endTimeMs/1000), 'UTC', 'America/Costa_Rica')), '%%d/%%m/%%Y') AS Fecha_Arribo,
	DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME((r.endTimeMs)/1000), 'UTC', 'America/Costa_Rica'), '%%H:%%i:%%s') AS Hora_Arribo

FROM mex_datawarehouse_bss4.BikeRentalFact AS r
LEFT JOIN BikeDim AS b ON r.bike_id=b.id
LEFT JOIN BikeStationDim AS stationOrig ON r.startStation_id=stationOrig.id
LEFT JOIN BikeStationDim AS stationDest ON r.endStation_id=stationDest.id
LEFT JOIN BikeMemberFact AS m ON r.member_accountNumber=m.bikeMemberAttributes_accountNumber
WHERE
	(r.startStation_id<>r.endStation_id OR billableDurationMs>=120000) AND
	r.endTimeMs>=UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}', 'America/Costa_Rica', 'UTC'))*1000 AND # fecha de inicio		
	r.endTimeMs<UNIX_TIMESTAMP(CONVERT_TZ('{fecha_fin}', 'America/Costa_Rica', 'UTC'))*1000  # fecha de cierre		
  
   
ORDER BY r.endTimeMs ASC	
;