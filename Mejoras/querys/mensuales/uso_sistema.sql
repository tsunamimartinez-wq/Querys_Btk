SELECT 
  v.member_accountNumber AS ID_usuario,
  b.displayedNumber AS ID_bicicleta,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(startTimeMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%d, %%m, %%Y') AS fech_inicio,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(endTimeMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%d, %%m, %%Y') AS fech_fin,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(startTimeMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%H:%%i:%%s') AS ini_viaj,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(endTimeMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%H:%%i:%%s') AS fin_viaj,
  ss.logicalTerminal AS ciclo_inici,
  es.logicalTerminal AS ciclo_fin,
  CONCAT(ss.longitude, ' ,', ss.latitude) AS ubica_inici,
  CONCAT(es.longitude, ' ,', es.latitude) AS ubica_fin,
  SEC_TO_TIME((endTimeMs - startTimeMs)/1000) AS tiemp_viaj,
  distanceInMeters AS dist_viaj,
  CONCAT(ss.longitude, " ", ss.latitude, ' ,', es.longitude, " ", es.latitude) AS GPS,
  CASE WHEN b.bikeModelName = 'CLASSIC' THEN 'Mecánica' ELSE NULL END AS t_unidad,
  CASE WHEN member_gender = 'M' THEN 'Hombre' 
       WHEN member_gender = 'F' THEN 'Mujer'
       WHEN member_gender = 'O' THEN 'Otro' 
       ELSE NULL
       END AS Género,
  FLOOR((UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}' + INTERVAL 1 MONTH, 'America/Costa_Rica', 'UTC')) - member_birthday/1000) / (365243600)) AS Edad

FROM BikeRentalFact AS v
  LEFT JOIN BikeDim AS b
    ON v.bike_id = b.id
  LEFT JOIN BikeStationDim AS ss
    ON v.startStation_id = ss.id
  LEFT JOIN BikeStationDim AS es
    ON v.endStation_id = es.id

         
WHERE v.endTimeMs >= UNIX_TIMESTAMP( CONVERT_TZ('{fecha_inicio}', 'America/Costa_Rica', 'UTC') ) * 1000
  AND v.endTimeMs < UNIX_TIMESTAMP( CONVERT_TZ('{fecha_fin}', 'America/Costa_Rica', 'UTC') ) * 1000 
             
         
 AND (totalDurationMs >= 120*1000
      OR startStation_id != endStation_id)
