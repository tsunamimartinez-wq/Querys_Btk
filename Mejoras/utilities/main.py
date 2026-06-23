
from get_data import GetData
from utils import (
    obtener_quincena_anterior,
    obtener_inicio_mes_siguiente,
    obtener_mes_anterior,
    obtener_trimestre_anterior,
    ejecutar_queries
    )

FECHA_FUNCS = {
    "mensual": obtener_mes_anterior,
    "trimestral": obtener_trimestre_anterior,
    "quincenal": obtener_quincena_anterior,
    "premensual": obtener_inicio_mes_siguiente
}

PATHS = {
    "mensual": "Mejoras/querys/mensuales",
    "trimestral": "Mejoras/querys/trimestral",
    "quincenal": "Mejoras/querys/quincenal",
    "premensual": "Mejoras/querys/premensual"
}

def main():

    periodo = input("Selecciona periodo (mensual, trimestral, quincenal, premensual): ").strip().lower()

    if periodo not in PATHS:
        raise ValueError(f"Periodo no válido: {periodo}")
   
    extractor = GetData("Mejoras/config/db_config.json")

    ejecutar_queries(periodo,extractor, PATHS, FECHA_FUNCS)

    return None


if __name__ == "__main__":
    main()
    