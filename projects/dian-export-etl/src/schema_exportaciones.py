from __future__ import annotations

# Notes:
# This dictionary defines the base schema for the bronze layer.
# All columns are explicitly cast in DuckDB to ensure type consistency
# and avoid automatic type inference issues when reading raw data.

BRONZE_CASTS: dict[str, str] = {
    # ------------------------------------------------------------------
    # Identifiers, classifications, and categorical fields
    # Stored as VARCHAR to preserve original values at the bronze stage
    # ------------------------------------------------------------------
    "ADUANA_SALIDA": "VARCHAR",
    "CIUDAD_DESTINATARIO": "VARCHAR",
    "CLASE_EXPORTADOR": "VARCHAR",
    "COD_LUG_SALIDA_ALF": "VARCHAR",
    "COD_LUGAR_SALIDA_NUM": "VARCHAR",
    "COD_MODALIDAD_EXPORTACION": "VARCHAR",
    "COD_MONEDA_TRANSACCION": "VARCHAR",
    "COD_PAIS_DESTINO": "VARCHAR",
    "COD_PAIS_DESTINO_ALF": "VARCHAR",
    "COD_UNIDAD_FISICA_ALF": "VARCHAR",
    "EXPORTACION_EN_TRANSITO": "VARCHAR",
    "MODALIDAD_EXPORTACION": "VARCHAR",
    "MODO_TRANSPORTE": "VARCHAR",
    "NIT_DECLARANTE": "VARCHAR",
    "NIT_EXPORTADOR": "VARCHAR",
    "NUM_SOLICITUD_AUTO_EMBARQUE": "VARCHAR",
    "NUMERO_FORMULARIO": "VARCHAR",
    "PAIS_DESTINO_FINAL": "VARCHAR",
    "RAZON_SOCIAL_DECLARANTE": "VARCHAR",
    "RAZON_SOCIAL_DESTINATARIO": "VARCHAR",
    "RAZON_SOCIAL_EXPORTADOR": "VARCHAR",
    "REGION_DE_ORIGEN": "VARCHAR",
    "SISTEMAS_ESPECIALES": "VARCHAR",
    "TIPO_CERTIFICADO_ORIGEN": "VARCHAR",
    "TIPO_DE_EMBARQUE": "VARCHAR",
    "TIPO_DECLARACION": "VARCHAR",
    "TIPO_DESPACHO": "VARCHAR",
    "UNIDAD_FISICA": "VARCHAR",

    # ------------------------------------------------------------------
    # Quantitative fields
    # Stored as DOUBLE to enable numerical aggregation and analysis
    # ------------------------------------------------------------------
    "CANTIDAD_UNIDADES_FISICAS": "DOUBLE",
    "PESO_BRUTO_KGS": "DOUBLE",
    "PESO_NETO_KGS": "DOUBLE",
    "VALOR_FOB_PESOS": "DOUBLE",
    "VALOR_FOB_USD": "DOUBLE",
    "VALOR_SERIE_FLETES_USD": "DOUBLE",
    "VALOR_SERIE_SEGUROS_USD": "DOUBLE",
    "VLR_SERIE_AGREGADO_NAL_USD": "DOUBLE",
    "VLR_SERIE_OTROS_GASTOS_USD": "DOUBLE",
}

