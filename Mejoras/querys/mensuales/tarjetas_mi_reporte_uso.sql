
SELECT 
	r.id AS VIAJE_ID, 
    acc.localizedValue0 AS ACCESO,
    CASE
		WHEN ISNULL(m.currentTransitCardNumber) THEN ""
        ELSE m.currentTransitCardNumber
	END  AS NUMERO_SERIE_HEX,
    stationOrig.name AS Ciclo_EstacionOrigen,
    DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(r.startTimeMs/1000), 'UTC', 'America/Mexico_City'), '%%Y-%%m-%%d %%H:%%i:%%s') AS FECHA_HORA_TRANSACCION_SALIDA,
	stationDest.name AS Ciclo_EstacionArribo,
	DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(r.endTimeMs/1000), 'UTC', 'America/Mexico_City'), '%%Y-%%m-%%d %%H:%%i:%%s') AS Fecha_Arribo,
    r.member_accountNumber AS customer,
    st.description_localizedValue1 AS membresia_tipo
FROM mex_datawarehouse_bss4.BikeRentalFact AS r
LEFT JOIN mex_datawarehouse_bss4.BikeDim AS b ON r.bike_id=b.id
LEFT JOIN mex_datawarehouse_bss4.BikeStationDim AS stationOrig ON r.startStation_id=stationOrig.id
LEFT JOIN mex_datawarehouse_bss4.BikeStationDim AS stationDest ON r.endStation_id=stationDest.id
LEFT JOIN mex_datawarehouse_bss4.BikeMemberFact AS m ON r.member_accountNumber=m.bikeMemberAttributes_accountNumber
LEFT JOIN mex_datawarehouse_bss4.RentalAccessMethodDim AS acc ON r.accessMethod_id=acc.id
LEFT JOIN mex_datawarehouse_bss4.BikeSubscriptionFact AS s ON r.subscriptionId=s.id
LEFT JOIN mex_datawarehouse_bss4.BikeSubscriptionTypeDim AS st ON s.subscriptionType_id=st.id

WHERE
	(r.startStation_id<>r.endStation_id OR billableDurationMs>=120000) AND
	r.endTimeMs>=UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}', 'America/Mexico_City', 'UTC'))*1000 AND # fecha de inicio 
	r.endTimeMs<=UNIX_TIMESTAMP(CONVERT_TZ('{fecha_fin}', 'America/Mexico_City', 'UTC'))*1000 # fecha de cierre
ORDER BY r.id ASC
;
