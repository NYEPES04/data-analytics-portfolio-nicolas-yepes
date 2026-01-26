from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import List
import requests

# Months as they appear in the file names
MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Base URL used for manual download of export reports
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
    Synchronizes DIAN export ZIP files.

    - Generates file names following the pattern NN_Exportaciones_YYYY_Month.zip.
    - By default, downloads files from `desde_anio/desde_mes` up to the current year/month.
    - Downloads only files that do NOT already exist in `dest_dir`.
    - Returns a list of newly downloaded files.
    """

    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now()

    if hasta_anio is None:
        hasta_anio = today.year
    if hasta_mes is None:
        hasta_mes = today.month  # up to the current month

    new_files: List[Path] = []

    if verbose:
        print(
            f"Synchronizing exports {desde_anio}-{desde_mes:02d} "
            f"→ {hasta_anio}-{hasta_mes:02d}"
        )

    for year in range(desde_anio, hasta_anio + 1):
        start_month = desde_mes if year == desde_anio else 1
        end_month = hasta_mes if year == hasta_anio else 12

        for m in range(start_month, end_month + 1):
            num = f"{m:02d}"
            month_name = MESES[m - 1]

            filename = f"{num}_Exportaciones_{year}_{month_name}.zip"
            url = BASE_URL + filename
            local_path = dest_dir / filename

            if local_path.exists():
                if verbose:
                    print(f"Already exists: {filename}")
                continue

            if verbose:
                print(f"\n Downloading {filename}...")

            resp = requests.get(url, stream=True)

            if resp.status_code == 200:
                with open(local_path, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        if chunk:
                            f.write(chunk)
                if verbose:
                    print(f"Saved to: {local_path}")
                new_files.append(local_path)
            else:
                if verbose:
                    print(f"HTTP {resp.status_code} (Not yet available on DIAN)")

    if verbose:
        print(f"\n New files downloaded: {len(new_files)}")

    return new_files
