import mysql.connector
import pandas as pd
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from pathlib import Path

def obtener_inicio_mes_siguiente(fecha=None):
    """
    Obtiene el primer día del mes siguiente a la fecha proporcionada.

    Parámetros
    ----------
    fecha : str o datetime, opcional
        Fecha de referencia en formato 'YYYY-MM-DD' o un objeto datetime.
        Si no se proporciona, se utiliza la fecha actual.

    Retorna
    -------
    str
        Fecha correspondiente al primer día del mes siguiente
        en formato 'YYYY-MM-DD HH:MM:SS'.
    """

    if fecha is None:
        fecha = datetime.today()
    elif isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")


    # Se posiciona en el primer día del mes actual y suma un mes
    mes_siguiente = (
        fecha.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0                          
        ) + relativedelta(months=1)
    )
    return (mes_siguiente.strftime("%Y-%m-%d %H:%M:%S"),
    None)

def ejecutar_query(query,conn):
    """
    Ejecuta una consulta SQL y devuelve el resultado
    como un DataFrame de pandas.

    Parámetros
    ----------
    query : str
        Consulta SQL a ejecutar.
    conn : conexión
        Conexión activa a la base de datos.

    Retorna
    -------
    pandas.DataFrame
        Resultado de la consulta.
    """
    return pd.read_sql(query, conn)

def guardar_csv(df,ruta_archivo):
    """
    Guarda un DataFrame en formato CSV.

    Si la carpeta destino no existe, la crea automáticamente.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame a guardar.
    ruta_archivo : str
        Ruta completa donde se almacenará el archivo.

    Retorna
    -------
    pandas.DataFrame
        El mismo DataFrame recibido.
    """

    Path(ruta_archivo).parent.mkdir(
        parents=True,
        exist_ok=True
    )
    df.to_csv(
        ruta_archivo,
        index=False,
        encoding="utf-8-sig"
    )
    print(f"Archivo guadado: {ruta_archivo}")

    return df

def ejecutar_y_guardar(query, conn, ruta_archivo):
    """
    Ejecuta una consulta SQL y guarda el resultado en un archivo CSV.

    Parámetros
    ----------
    query : str
        Consulta SQL a ejecutar.
    conn : conexión
        Conexión activa a la base de datos.
    ruta_archivo : str
        Ruta donde se guardará el archivo CSV.

    Retorna
    -------
    pandas.DataFrame
        Resultado de la consulta.
    """
    df = ejecutar_query(query, conn)
    guardar_csv(df,ruta_archivo)
    return df

def obtener_mes_anterior(fecha=None):
    """
    Obtiene el rango completo del mes anterior.

    Parámetros
    ----------
    fecha : str o datetime, opcional
        Fecha de referencia. Si no se proporciona,
        se utiliza la fecha actual.

    Retorna
    -------
    tuple(str, str)
        (
            inicio del mes anterior,
            inicio del mes actual
        )
        Ambas fechas en formato 'YYYY-MM-DD HH:MM:SS'.
    """

    if fecha is None:
        fecha = datetime.today()
    elif isinstance(fecha, str):
        fecha = datetime.strptimw(fecha, "%Y-%m-%d")

    inicio_mes_actual = fecha.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    inicio_mes_anterior = (
        inicio_mes_actual
        - relativedelta(months=1)
    )

    return(
         inicio_mes_anterior.strftime("%Y-%m-%d %H:%M:%S"),
        inicio_mes_actual.strftime("%Y-%m-%d %H:%M:%S")
    )

def obtener_quincena_anterior(fecha =None):
    """
    Obtiene el rango de la quincena inmediatamente anterior
    a la fecha de referencia.

    Reglas:
    - Si la fecha está entre el día 1 y 15, devuelve
      la segunda quincena del mes anterior.
    - Si la fecha está entre el día 16 y fin de mes,
      devuelve la primera quincena del mes actual.

    Parámetros
    ----------
    fecha : str o datetime, opcional
        Fecha de referencia.

    Retorna
    -------
    tuple(str, str)
        (
            fecha_inicio,
            fecha_fin
        )
        En formato 'YYYY-MM-DD HH:MM:SS'.
    """

    if fecha is None:
        fecha = datetime.today()
    elif isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
    
    if fecha.day < 16:
        # estamos en la primera quincena
        fecha_inicio = (
            fecha.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            - relativedelta(months=1)
        ).replace(day=16)

        fecha_fin = fecha.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    else:
        # Estamos en la segunda quincena
        fecha_inicio = fecha.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        fecha_fin = fecha.replace(
            day=16,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    return (
        fecha_inicio.strftime("%Y-%m-%d %H:%M:%S"),
        fecha_fin.strftime("%Y-%m-%d %H:%M:%S")
    )


def obtener_trimestre_anterior(fecha =None):
    """
    Obtiene el rango correspondiente al trimestre anterior
    respecto a una fecha de referencia.

    Trimestres:
    - T1: Ene-Mar
    - T2: Abr-Jun
    - T3: Jul-Sep
    - T4: Oct-Dic

    Parámetros
    ----------
    fecha : str o datetime, opcional
        Fecha de referencia.

    Retorna
    -------
    tuple(str, str)
        (
            fecha_inicio_trimestre_anterior,
            fecha_fin_trimestre_anterior
        )
        En formato 'YYYY-MM-DD HH:MM:SS'.
    """

    if fecha is None:
        fecha = datetime.today()
    elif isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
    
    anio = fecha.year
    mes = fecha.month
    
    trimestre_actual = ((mes-1) // 3) + 1

    if trimestre_actual == 1:
        fecha_inicio = datetime(anio - 1,10,1)
        fecha_fin = datetime(anio,1,1)

    elif trimestre_actual == 2:
        fecha_inicio = datetime(anio, 1, 1)
        fecha_fin = datetime(anio, 4, 1)

    elif trimestre_actual == 3:
        fecha_inicio = datetime(anio, 4, 1)
        fecha_fin = datetime(anio, 7, 1)

    else:
        fecha_inicio = datetime(anio, 7, 1)
        fecha_fin = datetime(anio, 10, 1)

    return (
        fecha_inicio.strftime("%Y-%m-%d %H:%M:%S"),
        fecha_fin.strftime("%Y-%m-%d %H:%M:%S")
    )

def ejecutar_queries(periodo, extractor, paths, fecha_funcs):

    print(f"\n=== Iniciando proceso {periodo} ===")

    fecha_inicio, fecha_fin = fecha_funcs[periodo]()

    carpeta_queries = Path(paths[periodo])
    # print("Directorio actual:", Path.cwd())
    # print("Ruta buscada:", carpeta_queries.resolve())

    print(f"Buscando consultas en: {carpeta_queries}")

    archivos_sql = list(carpeta_queries.glob("*.sql"))
    
    print(f"Consultas encontradas: {len(archivos_sql)}")

    mes_anterior = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")

    if periodo == "premensual":
        nombre_fecha = datetime.strptime(
        fecha_inicio, "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m")
    else:
        nombre_fecha = mes_anterior

    output_dir = Path("resultados") / periodo

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Carpeta creada: {output_dir}")
    else:
        print(f"Carpeta existente: {output_dir}")

    # print(f"Carpeta de salida: {output_dir}")

    for archivo in archivos_sql:
        print("\n--------------------------------")
        print(f"Procesando: {archivo.name}")

    
        with open(archivo, "r", encoding="utf-8") as f:
            query = f.read()
      
        query = query.replace("{fecha_inicio}", fecha_inicio)
        print(f"Fecha inicio: {fecha_inicio}")

        if "{fecha_fin}" in query:
            query = query.replace("{fecha_fin}", fecha_fin)
            print(f"Fecha fin: {fecha_fin}")

        print(f"Ejecutando consulta...")
        data = extractor.run_sql(query)

        if data is None:
            print(f"Error al ejecutar {archivo.name}")
            continue

        if archivo.stem == "tarjetas_mi_reporte_uso":
            print("Aplicando transformación para tarjetas mi reporte uso...")
            data = transformar_public_data_web(data)

        print(f"Registros obtenidos: {len(data):,}")

        output_path = output_dir / f"{archivo.stem}_{nombre_fecha}.csv"
        data.to_csv(output_path, index=False)

        print(f"CSV generado: {output_path}")

    return True


def transformar_public_data_web(df):
    """
    Transforma el resultado de la consulta public_data_web
    generando un registro para el retiro y otro para el arribo
    de cada viaje.

    Parámetros
    ----------
    df : pandas.DataFrame
        Resultado de la consulta SQL.

    Retorna
    -------
    pandas.DataFrame
        DataFrame transformado.
    """

    salida = df[[
        "VIAJE_ID",
        "ACCESO",
        "customer",
        "membresia_tipo",
        "NUMERO_SERIE_HEX",
        "FECHA_HORA_TRANSACCION_SALIDA",
        "Ciclo_EstacionOrigen"
    ]].copy()

    salida = salida.rename(columns={
        "VIAJE_ID": "ID_TRANSACCION_ORGANISMO",
        "membresia_tipo": "TIPO_MEMBRESIA",
        "FECHA_HORA_TRANSACCION_SALIDA": "FECHA_HORA_TRANSACCION",
        "Ciclo_EstacionOrigen": "LOCATION_ID"
    })

    salida["PROVIDER"] = 96
    salida["TIPO_TRANSACCION"] = 70

    arribo = df[[
        "VIAJE_ID",
        "ACCESO",
        "customer",
        "membresia_tipo",
        "NUMERO_SERIE_HEX",
        "Fecha_Arribo",
        "Ciclo_EstacionArribo"
    ]].copy()

    arribo = arribo.rename(columns={
        "VIAJE_ID": "ID_TRANSACCION_ORGANISMO",
        "membresia_tipo": "TIPO_MEMBRESIA",
        "Fecha_Arribo": "FECHA_HORA_TRANSACCION",
        "Ciclo_EstacionArribo": "LOCATION_ID"
    })

    arribo["PROVIDER"] = 96
    arribo["TIPO_TRANSACCION"] = 71

    df_final = pd.concat([salida, arribo], ignore_index=True)

    df_final = df_final.sort_values(
        ["ID_TRANSACCION_ORGANISMO", "TIPO_TRANSACCION"],
        ignore_index=True
    )

    return df_final