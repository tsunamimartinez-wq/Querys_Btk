SELECT 
  b.displayedNumber AS ID_bicicleta,
  CASE WHEN b.bikeModelName = 'CLASSIC' THEN 'Mecánica' ELSE NULL END AS t_bicicleta,
  t.id AS ID_empleado,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(i.actionDateInMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%d, %%m, %%Y') AS fech_inicio,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(f.actionDateInMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%d, %%m, %%Y') AS fech_fin,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(i.actionDateInMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%H:%%i:%%s') AS ini_viaj,
  DATE_FORMAT(CONVERT_TZ(FROM_UNIXTIME(f.actionDateInMs/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ), '%%H:%%i:%%s') AS fin_viaj,
  ce_ini.logicalTerminal AS ciclo_inici,
  ce_fin.logicalTerminal AS ciclo_fin,
  DATE_FORMAT(SEC_TO_TIME((f.actionDateInMs - i.actionDateInMs) / 1000), '%%H:%%i:%%s') AS tiemp_viaj

FROM (SELECT * FROM BikeTechnicianActionFact WHERE actionType_id = 1) AS i
  LEFT JOIN BikeTechnicianDim AS t ON i.tech_id = t.id
  LEFT JOIN BikeDim AS b ON i.bike_id = b.id
  LEFT JOIN (SELECT * FROM BikeTechnicianActionFact WHERE actionType_id = 0) AS f ON i.bikeTransferByTechnicianId = f.bikeTransferByTechnicianId
  LEFT JOIN BikeStationDim AS ce_ini ON  i.station_id = ce_ini.id
  LEFT JOIN BikeStationDim AS ce_fin ON  f.station_id = ce_fin.id

WHERE i.actionDateInMs >= UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}', 'America/Costa_Rica', 'UTC')) * 1000
  AND i.actionDateInMs < UNIX_TIMESTAMP(CONVERT_TZ('{fecha_fin}', 'America/Costa_Rica', 'UTC')) * 1000
  AND f.actionDateInMs > i.actionDateInMs