from pathlib import Path

import numpy as np
import pandas as pd

COLUNAS_ESPERADAS = [
    "Time",
    "Amount",
    *[f"V{i}" for i in range(1, 29)],
    "Class",
]


def carregar_dataset(caminho: str | Path) -> pd.DataFrame:
    """Carrega e valida o CSV de transações com cartão de crédito."""
    arquivo = Path(caminho)

    if not arquivo.exists():
        raise FileNotFoundError(
            f"Dataset não encontrado: {arquivo}. "
            "Disponibilize o arquivo CSV antes de continuar."
        )

    if not arquivo.is_file():
        raise ValueError(f"O caminho não aponta para um arquivo: {arquivo}")

    if arquivo.suffix.lower() != ".csv":
        raise ValueError("O arquivo do dataset deve ter extensão .csv.")

    df = pd.read_csv(arquivo)

    if df.empty:
        raise ValueError("O dataset está vazio.")

    colunas_faltantes = sorted(set(COLUNAS_ESPERADAS) - set(df.columns))
    colunas_extras = sorted(set(df.columns) - set(COLUNAS_ESPERADAS))

    if colunas_faltantes or colunas_extras:
        detalhes = []
        if colunas_faltantes:
            detalhes.append(f"colunas ausentes: {colunas_faltantes}")
        if colunas_extras:
            detalhes.append(f"colunas inesperadas: {colunas_extras}")

        raise ValueError("Esquema inválido; " + "; ".join(detalhes))

    if df.isna().any().any():
        colunas_com_nulos = df.columns[df.isna().any()].tolist()
        raise ValueError(
            f"O dataset contém valores ausentes nas colunas: {colunas_com_nulos}"
        )

    try:
        df = df.astype({coluna: "float64" for coluna in COLUNAS_ESPERADAS})
    except (TypeError, ValueError) as erro:
        raise ValueError(
            "Todas as colunas do dataset devem conter valores numéricos válidos."
        ) from erro

    if not np.isfinite(df.to_numpy()).all():
        raise ValueError("O dataset contém valores infinitos.")

    if not df["Class"].isin([0, 1]).all():
        raise ValueError("A coluna Class deve conter somente os valores 0 e 1.")

    return df
