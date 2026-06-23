SELECT  CONCAT(m.firstName, " ", m.lastName) AS nombre_completo,
        m.bikeMemberAttributes_gender AS genero,
        DATE(CONVERT_TZ(FROM_UNIXTIME(m.bikeMemberAttributes_birthday/1000), 'UTC', 'America/Costa_Rica')) AS fecha_nacimiento,
        m.address AS domicilio,
        m.bikeMemberAttributes_postalCode AS cp,
        m.email AS correo_electronico, 
        m.phoneNumber AS tel_contacto,
        IF(ss.id = 1, 'sitio_web', IF(ss.id = 3, 'renov_auto', IF(ss.id = 6, 'app_movil', 'otra'))) AS forma_inscripcion,
        m.bikeMemberAttributes_memberNumber AS num_pers_usuaria,
        m.currentTransitCardNumber AS num_tarjeta,
        st.name_localizedValue1 AS tipo_membresia

FROM BikeSubscriptionFact AS s
LEFT JOIN BikeMemberFact AS m ON s.member_accountNumber = m.bikeMemberAttributes_accountNumber
LEFT JOIN BikeSubscriptionTypeDim AS st ON s.subscriptionType_id = st.id
LEFT JOIN BikeSubscriptionRequestSourceDim AS ss ON s.subscriptionSourceDim_id = ss.id

WHERE s.start BETWEEN UNIX_TIMESTAMP(CONVERT_TZ('{fecha_inicio}', 'America/Costa_Rica', 'UTC'))*1000
  AND UNIX_TIMESTAMP(CONVERT_TZ('{fecha_fin}' , 'America/Costa_Rica', 'UTC'))*1000
  AND (s.subscriptionType_id < 6 OR s.subscriptionType_id = 9 ) -- sólo anuales, migradas, temporales y plus
;