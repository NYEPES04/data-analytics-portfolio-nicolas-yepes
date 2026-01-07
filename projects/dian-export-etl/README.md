# ETL – Exportaciones DANE/DIAN (Colombia)

Pipeline ETL para **descargar** ZIPs de exportaciones, **extraer**, **convertir** (XLSX → CSV), **consolidar** y **limpiar** la base final para análisis.

## Objetivo

- Automatizar la descarga y consolidación mensual/anual.
- Estandarizar tipos (fechas, códigos) y remover ruido (columnas *Unnamed*, duplicados).
- Dejar un dataset listo para BI/analítica (Parquet/CSV).

## Estructura del repositorio

```
.
├── notebooks/
│   └── ETL_Master_file_github.ipynb
├── src/
│   ├── dian_export_sync.py
│   ├── dian_extract_zip.py
│   ├── convert_xlsx_to_csv.py
│   └── consolidar_csv.py
├── data/                # se ignora en git (ver .gitignore)
│   ├── raw_zip/
│   ├── extracted/
│   ├── csv/
│   ├── consolidated/
│   └── processed/
├── logs/
├── requirements.txt
└── .gitignore
```

## Requisitos

- Python 3.10+

Instalación:

```bash
pip install -r requirements.txt
```

## Cómo correr

1. Ubica los módulos ETL en `src/`.
2. Abre y ejecuta el notebook:

- `notebooks/ETL_Master_file_github.ipynb`

El notebook generará:
- Consolidado: `data/consolidated/exportaciones_consolidadas.csv`
- Dataset limpio: `data/processed/exportaciones_limpias.parquet`

## Notas

- Este repo **no versiona** datos en `data/` (por tamaño).  
- Si necesitas compartir muestras, considera `data/sample/` y sube un subset pequeño anonimizado.

## Licencia

MIT (opcional)
