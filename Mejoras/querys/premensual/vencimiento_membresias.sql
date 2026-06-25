SELECT 
    bsf.member_accountNumber AS cuenta,
    baf.accountHolderFirstName AS nombre,
    baf.accountHolderLastName AS apellido,
    baf.accountHolderEmail AS correo,
    bstD.name_localizedValue1 AS tipo_membresia,
    bssD.localizedValue0 AS estado_membresia,
    -- agregar tipo de membresia
    -- activa/desactivada
CONVERT_TZ(FROM_UNIXTIME(end/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ) AS vencimiento
FROM BikeSubscriptionFact bsf
LEFT JOIN BikeAccountFact baf ON bsf.member_accountNumber = baf.publicAccountNumber
LEFT JOIN BikeSubscriptionTypeDim bstD ON bsf.subscriptionType_id = bstD.id
LEFT JOIN BikeSubscriptionStatusDim bssD ON bsf.status_id = bssD.id
WHERE subscriptionType_id IN (4,5, 9,10) -- Incluir Anual+ y HSBC
  AND end/1000 BETWEEN UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}', 'America/Costa_Rica', 'UTC'))
  AND UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}' + INTERVAL 1 MONTH, 'America/Costa_Rica', 'UTC'))
ORDER BY vencimiento ASC
;