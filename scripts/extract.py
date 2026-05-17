"""Módulo de extracción de datos de FastF1.

Descarga y guarda en formato parquet:
- El calendario (schedule) de la temporada.
- Para los primeros rounds del calendario: resultados y vueltas (laps) de la
  sesión indicada, agregando las columnas year y EventName a cada df.
"""

import sys
from pathlib import Path

# Inyección del directorio raíz en el PATH para poder importar utils de forma segura
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import fastf1
import pandas as pd

from utils import CACHE_DIR, RAW_DIR, slug, to_parquet

# --- Configuración del Pipeline ---
YEAR = 2026
ROUNDS = [1, 2, 3]
SESSION = "R"  # "R" corresponde a la Carrera del domingo (Race)


def extract_schedule(year: int) -> pd.DataFrame:
    print(f"[schedule] Descargando schedule {year}...")
    schedule = fastf1.get_event_schedule(year)
    to_parquet(schedule, RAW_DIR / f"schedule_{year}.parquet")
    print(f"[schedule] OK — {len(schedule)} eventos")
    return schedule


def extract_session(year: int, round_number: int, session_id: str = SESSION) -> None:
    print(f"[round {round_number}] Cargando sesión {session_id}...")
    session = fastf1.get_session(year, round_number, session_id)
    
    # Descargamos los datos principales omitiendo telemetría pesada para optimizar velocidad
    session.load(telemetry=False, weather=False, messages=False)

    event_name = session.event["EventName"]

    # 1. Procesar y guardar resultados de la carrera
    results = pd.DataFrame(session.results)
    results["year"] = year
    results["EventName"] = event_name
    to_parquet(results, RAW_DIR / f"results_{year}_{slug(event_name)}.parquet")

    # 2. Procesar y guardar vueltas de la carrera (con control de excepciones si no están disponibles)
    try:
        laps = pd.DataFrame(session.laps)
        laps["year"] = year
        laps["EventName"] = event_name
        to_parquet(laps, RAW_DIR / f"laps_{year}_{slug(event_name)}.parquet")
        laps_count = len(laps)
    except Exception as e:
        print(f"[round {round_number}] WARNING — laps no disponibles: {e}")
        laps_count = 0

    print(f"[round {round_number}] OK — {event_name}: {len(results)} resultados, {laps_count} vueltas")


def main() -> None:
    # Asegurar que el directorio de caché exista y activarlo en FastF1
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(CACHE_DIR)

    # Ejecutar extracción del calendario de carreras
    extract_schedule(YEAR)
    
    # Bucle para extraer cada uno de los rounds configurados
    for round_number in ROUNDS:
        extract_session(YEAR, round_number, SESSION)

    print("\nExtracción completada con éxito.")


if __name__ == "__main__":
    main()