from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import duckdb


@dataclass
class ConvertResult:
    processed: int
    ok: int
    skipped: int
    errors: int
    error_details: list[tuple[str, str]]  # (filename, repr(error))


def xlsx_dir_to_parquet_dir(
    xlsx_dir: Path,
    out_dir: Path,
    pattern: str = "*.xlsx",
    overwrite: bool = False,
    sheet: Optional[str] = None,
    threads: int = 4,
    memory_limit: str = "8GB",
    use_parent_name: bool = True,
    verbose: bool = True,
    #  NEW: controls type inference and tolerance to "messy" Excel cells
    all_varchar: bool = True,      # <- recommended for raw/bronze layer
    ignore_errors: bool = False,   # <- if True, invalid casts become NULL instead of failing
    empty_as_varchar: bool = True  # <- prevents empty cells from breaking inference
) -> ConvertResult:
    """
    Converts XLSX files to Parquet using DuckDB with the Excel extension.

    To avoid type inference errors (e.g. 'C100' in a column inferred as DOUBLE),
    set all_varchar=True (recommended for the raw/bronze layer).
    """
    xlsx_dir = Path(xlsx_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Discover valid XLSX files (ignores temp and hidden files)
    files = sorted(
        p for p in xlsx_dir.rglob("*")
        if p.is_file()
        and p.suffix.lower() == ".xlsx"
        and not p.name.startswith("~$")
        and not p.name.startswith(".")
    )

    if verbose:
        print(f"[xlsx_to_parquet] Valid XLSX files found: {len(files)} in {xlsx_dir}")

    # Initialize DuckDB connection
    con = duckdb.connect()
    con.execute(f"PRAGMA threads={threads};")
    con.execute(f"PRAGMA memory_limit='{memory_limit}';")

    # Enable Excel support in DuckDB
    con.execute("INSTALL excel;")
    con.execute("LOAD excel;")

    error_details: list[tuple[str, str]] = []
    ok = skipped = 0

    # Build SQL options for read_xlsx(...)
    read_opts = []
    if sheet:
        # Note: sheet name must be a string
        read_opts.append(f"sheet='{sheet}'")
    read_opts.append(f"all_varchar={'true' if all_varchar else 'false'}")
    read_opts.append(f"ignore_errors={'true' if ignore_errors else 'false'}")
    read_opts.append(f"empty_as_varchar={'true' if empty_as_varchar else 'false'}")
    opts_sql = ", ".join(read_opts)

    for p in files:
        # Output file naming strategy
        if use_parent_name:
            out_path = out_dir / f"{p.parent.name}.parquet"
        else:
            rel = p.relative_to(xlsx_dir)
            safe_name = "_".join(rel.parts)
            safe_name = safe_name[:-5] if safe_name.lower().endswith(".xlsx") else safe_name
            out_path = out_dir / f"{safe_name}.parquet"

        if out_path.exists() and not overwrite:
            skipped += 1
            continue

        try:
            src = f"read_xlsx('{p.as_posix()}', {opts_sql})"

            # Single-step COPY for efficient XLSX → Parquet conversion
            con.execute(f"""
                COPY (
                  SELECT * FROM {src}
                ) TO '{out_path.as_posix()}'
                (FORMAT 'parquet', COMPRESSION 'snappy');
            """)
            ok += 1
            if verbose:
                print(f"OK -> {out_path.name}")

        except Exception as e:
            error_details.append((p.name, repr(e)))
            if verbose:
                print(f"ERROR -> {p.name}: {repr(e)}")

    con.close()

    return ConvertResult(
        processed=len(files),
        ok=ok,
        skipped=skipped,
        errors=len(error_details),
        error_details=error_details,
    )

