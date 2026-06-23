SELECT 
	member_accountNumber AS cuenta,
    accountHolderFirstName AS nombre,
	accountHolderLastName AS apellido,
	accountHolderEmail AS correo,
CONVERT_TZ(FROM_UNIXTIME(end/1000, '%%Y-%%m-%%d %%H:%%i:%%s'), 'UTC', 'America/Costa_Rica' ) AS vencimiento
FROM BikeSubscriptionFact AS s
LEFT JOIN BikeAccountFact AS a ON s.member_accountnumber = a.publicAccountNumber
WHERE ( subscriptionType_id = 4 OR subscriptionType_id = 5 )
  AND end/1000 BETWEEN UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}', 'America/Costa_Rica', 'UTC'))
  AND UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}' + INTERVAL 1 MONTH, 'America/Costa_Rica', 'UTC'))
ORDER BY vencimiento ASC
;
