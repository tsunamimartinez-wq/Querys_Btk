import mysql.connector
import pandas as pd
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from pathlib import Path

def obtener_inicio_mes_siguiente(fecha=None):
    """
    Devuelve el primeri dia del mes siguiente.

    fecha : string "yyyy-mm-dd"" o datetime.
        Si es None, usa la fecha actual como referencia.
    """

    if fecha is None:
        fecha = datetime.today()
    elif isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")

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
    return pd.read_sql(query, conn)

def guardar_csv(df,ruta_archivo):
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
    df = ejecutar_query(query, conn)
    guardar_csv(df,ruta_archivo)
    return df

def obtener_mes_anterior(fecha=None):
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