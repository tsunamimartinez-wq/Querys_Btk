SELECT  CONCAT(m.firstName, " ", m.lastName) AS nombre_completo,
        m.bikeMemberAttributes_gender AS genero,
        CONVERT_TZ(FROM_UNIXTIME(m.bikeMemberAttributes_birthday/1000), 'UTC', 'America/Mexico_City') AS fecha_nacimiento,
        m.address AS domicilio,
        m.email AS correo_electronico, 
        m.phoneNumber AS tel_contacto,
        IF(ss.id = 1, 'sitio_web', IF(ss.id = 3, 'renov_auto', IF(ss.id = 6, 'app_movil', 'otra')))
          AS forma_inscripcion,
        m.bikeMemberAttributes_memberNumber AS num_pers_usuaria,
        m.currentTransitCardNumber AS num_tarjeta,
        st.name_localizedValue1 AS tipo_membresia

FROM (SELECT id, subscriptionType_id, subscriptionSourceDim_id
      FROM BikeSubscriptionFact
      WHERE start/1000 <= UNIX_TIMESTAMP('{fecha_fin}') -- actualizar fecha a fin del trimestre
      AND end/1000 > UNIX_TIMESTAMP('{fecha_fin}') -- actualizar fecha a fin del trimestre
      AND subscriptionType_id < 5) AS s -- excluye migradas y test product

LEFT JOIN BikeMemberFact AS m ON s.id = m.currentSubscription_id
LEFT JOIN BikeSubscriptionTypeDim AS st ON s.subscriptionType_id = st.id
LEFT JOIN BikeSubscriptionRequestSourceDim AS ss ON s.subscriptionSourceDim_id = ss.id

WHERE m.bikeMemberAttributes_memberNumber IS NOT NULL
;
