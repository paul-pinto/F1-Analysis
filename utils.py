from pathlib import Path
import pandas as pd

# Encontrar la carpeta raíz del proyecto de forma dinámica
ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data/raw"
CACHE_DIR = ROOT / "data/cache"


def slug(text: str) -> str:
    """Convierte un nombre de evento en algo apto para un nombre de archivo.
    Ejemplo: 'Australian Grand Prix' -> 'Australian_Grand_Prix'
    """
    return "_".join(str(text).split())


def to_parquet(df: pd.DataFrame, path: Path) -> None:
    """Guarda un DataFrame en formato Parquet, forzando la conversión
    de tipos nativos de FastF1 a Pandas estándar, y creando directorios si no existen.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(df).to_parquet(path, index=False)
    print(f"  guardado: {path}  ({len(df)} filas)")