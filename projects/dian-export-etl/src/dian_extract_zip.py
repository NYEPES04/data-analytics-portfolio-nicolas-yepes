from pathlib import Path
import zipfile

def extract_all_zips(
    zip_dir: str | Path,
    extract_dir: str | Path,
    overwrite: bool = False,
    verbose: bool = True
):
    """
    Extracts all ZIP files contained in zip_dir into subfolders inside extract_dir.

    Each ZIP file is extracted into a folder with the SAME name as the ZIP:
        e.g.: 01_Exportaciones_2021_Enero.zip
        →     extract_dir/01_Exportaciones_2021_Enero/

    Parameters
    ----------
    zip_dir : directory containing the downloaded ZIP files
    extract_dir : destination directory for extracted files
    overwrite : if False, extraction is skipped when the target folder already exists
    verbose : if True, prints progress messages

    Returns
    -------
    List[Path] : list of newly created folders
    """
    zip_dir = Path(zip_dir)
    extract_dir = Path(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    new_folders = []

    for zip_path in zip_dir.glob("*.zip"):
        folder_name = zip_path.stem  # ZIP file name without .zip
        target_folder = extract_dir / folder_name

        if target_folder.exists() and not overwrite:
            if verbose:
                print(f"Already exists: {target_folder.name}")
            continue

        if verbose:
            print(f"\n Extracting: {zip_path.name}")
            print(f"   → Target folder: {target_folder}")

        # Create destination folder
        target_folder.mkdir(exist_ok=True)

        # Extract contents
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(target_folder)

        if verbose:
            print(f"   Extracted successfully")

        new_folders.append(target_folder)

    print(f"\n New folders created: {len(new_folders)}")
    return new_folders
