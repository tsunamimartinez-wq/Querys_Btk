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
    return mes_siguiente.strftime("%Y-%m-%d %H:%M:%S")

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
        fecha = datetime.strptimw(fecha, "%Y.%m.%d")

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
            fecha.replace(day=1, hour=0, second=0, microsecond=0)
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