from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import requests

# Meses tal como aparecen en los nombres de archivo
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Enlace que permite la descarga manual de cada reporte de exportaciones
BASE_URL = "https://www.dian.gov.co/dian/cifras/Basesestadisticasexportaciones/"


def sync_dian_exportaciones(
    dest_dir: str | Path,
    desde_anio: int = 2021,
    desde_mes: int = 1,
    hasta_anio: int | None = None,
    hasta_mes: int | None = None,
    verbose: bool = True,
) -> List[Path]:
    """
    Sincroniza ZIP de EXPORTACIONES de la DIAN.

    - Genera nombres NN_Exportaciones_AAAA_Mes.zip usando el patrón conocido.
    - Por defecto va desde `desde_anio/desde_mes` hasta el año/mes actual.
    - Solo descarga los que NO existan aún en `dest_dir`.
    - Devuelve una lista con los archivos NUEVOS descargados.
    """

    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    hoy = datetime.now()

    if hasta_anio is None:
        hasta_anio = hoy.year
    if hasta_mes is None:
        hasta_mes = hoy.month  # hasta el mes actual

    nuevos: List[Path] = []

    if verbose:
        print(
            f" Sincronizando exportaciones {desde_anio}-{desde_mes:02d} "
            f"→ {hasta_anio}-{hasta_mes:02d}"
        )

    for year in range(desde_anio, hasta_anio + 1):
        mes_inicio = desde_mes if year == desde_anio else 1
        mes_fin = hasta_mes if year == hasta_anio else 12

        for m in range(mes_inicio, mes_fin + 1):
            num = f"{m:02d}"
            nombre_mes = MESES[m - 1]

            filename = f"{num}_Exportaciones_{year}_{nombre_mes}.zip"
            url = BASE_URL + filename
            local_path = dest_dir / filename

            if local_path.exists():
                if verbose:
                    print(f" Ya existe, omito: {filename}")
                continue

            if verbose:
                print(f"\n Descargando {filename}...")
                

            resp = requests.get(url, stream=True)

            if resp.status_code == 200:
                with open(local_path, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                if verbose:
                    print(f"    Guardado en: {local_path}")
                nuevos.append(local_path)
            else:
                if verbose:
                    print(f"    HTTP {resp.status_code} (probablemente aún no existe en DIAN)")

    if verbose:
        print(f"\n Nuevos archivos descargados: {len(nuevos)}")

    return nuevos
