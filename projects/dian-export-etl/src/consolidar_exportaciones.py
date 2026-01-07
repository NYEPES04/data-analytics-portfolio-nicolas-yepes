from __future__ import annotations

from pathlib import Path
from typing import List
import pandas as pd


def _cargar_log(log_path: Path) -> set[str]:
    """Lee el archivo de log con rutas de CSV ya procesados."""
    if not log_path.exists():
        return set()
    with log_path.open("r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]
    return set(lineas)


def _guardar_log(log_path: Path, rutas: List[str]) -> None:
    """Sobrescribe el log con la lista completa de rutas procesadas."""
    with log_path.open("w", encoding="utf-8") as f:
        for r in sorted(rutas):
            f.write(r + "\n")


def consolidar_csv_nuevos(
    csv_dir: str | Path,
    output_csv: str | Path,
    log_file: str | Path | None = None,
    verbose: bool = True,
) -> None:
    """
    Consolidación incremental de CSV:

    - Busca CSV dentro de csv_dir.
    - Procesa únicamente los que no estén registrados en log_file.
    - Agrega una columna 'origen_archivo' con el nombre del archivo.
    - Combina los nuevos registros con el CSV maestro (output_csv).
    """

    csv_dir = Path(csv_dir)
    output_csv = Path(output_csv)

    if log_file is None:
        log_file = output_csv.with_suffix("")
        log_file = log_file.with_name(log_file.name + "_log.txt")

    log_path = Path(log_file)

    if verbose:
        print("Carpeta CSV:", csv_dir)
        print("CSV maestro:", output_csv)
        print("Log de procesados:", log_path)

    # 1) Cargar log de procesados
    procesados = _cargar_log(log_path)
    if verbose:
        print("CSV ya registrados en log:", len(procesados))

    # 2) Buscar CSV físicos
    todos_csv = sorted(csv_dir.glob("*.csv"))
    if verbose:
        print("CSV encontrados en disco:", len(todos_csv))

    # 3) Filtrar nuevos
    nuevos_paths = []
    for p in todos_csv:
        key = str(p.resolve())
        if key not in procesados:
            nuevos_paths.append(p)

    if verbose:
        print("CSV nuevos a procesar:", len(nuevos_paths))

    if not nuevos_paths:
        if verbose:
            print("No hay archivos nuevos. Consolidación no requerida.")
        return

    # 4) Cargar maestro si existe
    if output_csv.exists():
        if verbose:
            print("Leyendo CSV maestro existente...")
        df_maestro = pd.read_csv(output_csv, low_memory=False)
    else:
        df_maestro = pd.DataFrame()

    # 5) Cargar nuevos CSV
    nuevos_registros = []
    for p in nuevos_paths:
        if verbose:
            print("Leyendo:", p.name)
        try:
            df = pd.read_csv(p, low_memory=False)
            df["origen_archivo"] = p.name
            nuevos_registros.append(df)
        except Exception as e:
            print("Error leyendo", p, ":", e)

    if not nuevos_registros:
        print("Ningún CSV pudo ser leído. No se modifica el maestro.")
        return

    df_nuevos = pd.concat(nuevos_registros, ignore_index=True)

    # 6) Unir con maestro
    if not df_maestro.empty:
        df_final = pd.concat([df_maestro, df_nuevos], ignore_index=True)
    else:
        df_final = df_nuevos

    if verbose:
        print("Guardando CSV maestro consolidado con", len(df_final), "filas..." )

    # Crear carpeta destino si no existe
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    # Guardar CSV
    df_final.to_csv(output_csv, index=False, encoding="utf-8-sig")

    # 7) Actualizar log
    rutas_actualizadas = procesados.union(str(p.resolve()) for p in nuevos_paths)
    _guardar_log(log_path, list(rutas_actualizadas))

    if verbose:
        print("Consolidación completada.")
