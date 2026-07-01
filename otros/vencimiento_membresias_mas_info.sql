SELECT 
    -- bsf.member_accountNumber AS cuenta,
    CONCAT_WS(' ',
        baf.accountHolderFirstName,
        baf.accountHolderLastName
    ) AS nombre_completo,
    baf.accountHolderEmail AS correo,
    TIMESTAMPDIFF(
    YEAR,
    FROM_UNIXTIME(bmf.bikeMemberAttributes_birthday / 1000),
    CURDATE()) AS edad,
    bmf.phoneNumber AS Phone_Number,
    bmf.bikeMemberAttributes_country AS Pais,
    bstD.name_localizedValue1 AS tipo_membresia,
    bssD.localizedValue0 AS estado_membresia,
    bmf.province,

    -- agregar tipo de membresia
    -- activa/desactivada
CONVERT_TZ(FROM_UNIXTIME(end/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ) AS vencimiento
FROM BikeSubscriptionFact bsf
LEFT JOIN BikeAccountFact baf ON bsf.member_accountNumber = baf.publicAccountNumber 
LEFT JOIN BikeMemberFact bmf ON bsf.member_accountNumber = bmf.bikeMemberAttributes_accountNumber
LEFT JOIN BikeSubscriptionTypeDim bstD ON bsf.subscriptionType_id = bstD.id
LEFT JOIN BikeSubscriptionStatusDim bssD ON bsf.status_id = bssD.id

WHERE subscriptionType_id IN (1,2,3,4,5,9,10) -- Incluir Anual+ y HSBC 5, 9,10
  AND bssD.localizedValue0 = 'Active'
  AND end/1000 BETWEEN UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}', 'America/Costa_Rica', 'UTC'))
  AND UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}' + INTERVAL 1 MONTH, 'America/Costa_Rica', 'UTC'))
ORDER BY vencimiento ASC
;