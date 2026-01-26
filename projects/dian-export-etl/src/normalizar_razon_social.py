import pandas as pd
import re
import unicodedata


def _quitar_acentos(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def _normalizar_sufijos(texto: str) -> str:
    """
    Unifica sufijos legales comunes en Colombia.
    """
    reemplazos = {
        r"\bSOCIEDAD ANONIMA\b": "SA",
        r"\bSOCIEDAD POR ACCIONES SIMPLIFICADA\b": "SAS",
        r"\bLIMITADA\b": "LTDA",
        r"\bCOMPANIA\b": "CIA",
        r"\bCIA\b": "CIA",
        r"\bS A S\b": "SAS",
        r"\bS A\b": "SA",
    }

    for patron, reemplazo in reemplazos.items():
        texto = re.sub(patron, reemplazo, texto)

    return texto


def normalizar_razon_social(texto: str) -> str:
    """
    Normaliza una razón social para evitar duplicados por:
    - puntos / comas
    - espacios múltiples
    - acentos
    - variaciones de sufijos legales (S.A. / S A / SOCIEDAD ANONIMA)
    """
    if pd.isna(texto):
        return texto

    texto = texto.upper()
    texto = _quitar_acentos(texto)

    # Reemplazar puntuación por espacios
    texto = re.sub(r"[.,]", " ", texto)

    # Colapsar espacios
    texto = re.sub(r"\s+", " ", texto).strip()

    texto = _normalizar_sufijos(texto)

    # Limpieza final de espacios
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def add_razon_social_normalizada(
    df: pd.DataFrame,
    col_original: str = "RAZON_SOCIAL_EXPORTADOR",
    col_limpia: str = "RAZON_SOCIAL_EXPORTADOR_LIMPIA",
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Agrega una columna normalizada de razón social al DataFrame.
    """
    out = df if inplace else df.copy()

    out[col_limpia] = (
        out[col_original]
        .astype(str)
        .apply(normalizar_razon_social)
    )

    return out