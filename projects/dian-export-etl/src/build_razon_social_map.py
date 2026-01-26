from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd
from normalizar_razon_social import normalizar_razon_social


def extract_unique_values(
    parquet_raw_dir: Path,
    col: str = "RAZON_SOCIAL_EXPORTADOR",
) -> pd.DataFrame:
    """
    Extracts unique and lightly cleaned values (trim + collapsed spaces)
    from bronze Parquet files.

    Returns a DataFrame with a single column: original
    """
    raw_glob = (parquet_raw_dir / "*.parquet").as_posix()
    con = duckdb.connect()

    df = con.execute(f"""
        SELECT DISTINCT
          REGEXP_REPLACE(TRIM(CAST({col} AS VARCHAR)), '\\s+', ' ', 'g') AS original
        FROM read_parquet('{raw_glob}')
        WHERE {col} IS NOT NULL
          AND TRIM(CAST({col} AS VARCHAR)) <> ''
    """).fetchdf()

    con.close()
    return df


def build_razon_social_map(
    parquet_raw_dir: Path,
    out_map: Path,
    col: str = "RAZON_SOCIAL_EXPORTADOR",
    incremental: bool = True,
) -> Path:
    """
    Builds (or updates) a Parquet mapping with:
      - original (string)
      - limpia   (normalized string)

    incremental=True:
      - if out_map already exists, only new 'original' values are processed.
    """
    out_map.parent.mkdir(parents=True, exist_ok=True)

    df_current = extract_unique_values(parquet_raw_dir, col)

    # --- Incremental mode: process only new values if mapping exists ---
    if incremental and out_map.exists():
        df_old = pd.read_parquet(out_map)

        # Anti-join: identify originals not yet present in the mapping
        pending = df_current.merge(
            df_old[["original"]],
            on="original",
            how="left",
            indicator=True
        )
        df_new = pending[pending["_merge"] == "left_only"][["original"]]

        if df_new.empty:
            print("razon_social_map is already up to date. Nothing new.")
            return out_map

        print(f"New values to normalize: {len(df_new):,}")
        df_new["limpia"] = df_new["original"].astype(str).map(normalizar_razon_social)

        df_out = (
            pd.concat([df_old, df_new], ignore_index=True)
            .drop_duplicates(subset=["original"])
        )

        df_out.to_parquet(out_map, index=False)
        print(f"Mapping updated: {len(df_out):,} rows → {out_map}")
        return out_map

    # --- Full rebuild ---
    print(f"Building full mapping: {len(df_current):,} unique values")
    df_current["limpia"] = df_current["original"].astype(str).map(normalizar_razon_social)
    df_current.to_parquet(out_map, index=False)
    print(f"Mapping created: {out_map}")
    return out_map

