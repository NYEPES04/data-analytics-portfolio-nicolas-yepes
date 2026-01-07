from pathlib import Path
import zipfile

def extract_all_zips(
    zip_dir: str | Path,
    extract_dir: str | Path,
    overwrite: bool = False,
    verbose: bool = True
):
    """
    Extrae todos los ZIP contenidos en zip_dir hacia carpetas dentro de extract_dir.

    Cada ZIP se descomprime en una carpeta con el MISMO nombre que el ZIP:
        EJ: 01_Exportaciones_2021_Enero.zip
        →  extract_dir/01_Exportaciones_2021_Enero/

    Parámetros
    ----------
    zip_dir : carpeta donde están los ZIP descargados
    extract_dir : carpeta destino para los archivos descomprimidos
    overwrite : si False, no vuelve a descomprimir si la carpeta ya existe
    verbose : si True, imprime progreso

    Retorna
    -------
    List[Path] : lista con las carpetas nuevas creadas
    """
    zip_dir = Path(zip_dir)
    extract_dir = Path(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    nuevos = []

    for zip_path in zip_dir.glob("*.zip"):
        folder_name = zip_path.stem  # nombre del ZIP sin .zip
        target_folder = extract_dir / folder_name

        if target_folder.exists() and not overwrite:
            if verbose:
                print(f"⏭️ Ya existe, omito: {target_folder.name}")
            continue

        if verbose:
            print(f"\n Extrayendo: {zip_path.name}")
            print(f"   → Carpeta destino: {target_folder}")

        # Crear carpeta destino
        target_folder.mkdir(exist_ok=True)

        # Extraer
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(target_folder)

        if verbose:
            print(f"   ✅ Extraído correctamente")

        nuevos.append(target_folder)

    print(f"\n Carpetas nuevas creadas: {len(nuevos)}")
    return nuevos
