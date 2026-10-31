"""Inferência de novas transações com modelos treinados."""

from collections.abc import Sequence

import numpy as np
import pandas as pd

from fraud_detection.models.persistence import ArtefatoModelo


def _validar_entradas(
    transacoes: pd.DataFrame,
    colunas_esperadas: Sequence[str],
) -> pd.DataFrame:
    """Valida e organiza as colunas recebidas para inferência."""
    if not isinstance(transacoes, pd.DataFrame):
        raise TypeError("As transações devem ser fornecidas em um DataFrame.")

    if transacoes.empty:
        raise ValueError("Não há transações para realizar a inferência.")

    faltantes = sorted(set(colunas_esperadas) - set(transacoes.columns))
    extras = sorted(set(transacoes.columns) - set(colunas_esperadas))

    if faltantes or extras:
        detalhes = []

        if faltantes:
            detalhes.append(f"colunas ausentes: {faltantes}")

        if extras:
            detalhes.append(f"colunas inesperadas: {extras}")

        raise ValueError("Esquema inválido; " + "; ".join(detalhes))

    dados = transacoes.loc[:, colunas_esperadas].copy()

    try:
        dados = dados.astype("float64")
    except (TypeError, ValueError) as erro:
        raise ValueError(
            "Todas as colunas de entrada devem conter valores numéricos."
        ) from erro

    if dados.isna().any().any():
        raise ValueError("As transações contêm valores ausentes.")

    if not np.isfinite(dados.to_numpy()).all():
        raise ValueError("As transações contêm valores infinitos.")

    return dados


def prever_transacoes(
    transacoes: pd.DataFrame,
    artefato: ArtefatoModelo,
) -> pd.DataFrame:
    """Calcula probabilidades e decisões para novas transações."""
    dados = _validar_entradas(transacoes, artefato.colunas_entrada)

    modelo = artefato.modelo

    if not hasattr(modelo, "predict_proba"):
        raise TypeError("O modelo precisa disponibilizar o método predict_proba.")

    classes = np.asarray(modelo.classes_)
    indices_fraude = np.flatnonzero(classes == 1)

    if len(indices_fraude) != 1:
        raise ValueError("O modelo precisa ter uma classe de fraude identificada por 1.")

    probabilidades = modelo.predict_proba(dados)[:, indices_fraude[0]]

    if not np.isfinite(probabilidades).all():
        raise ValueError("O modelo retornou probabilidades inválidas.")

    previsoes = (probabilidades >= artefato.limiar).astype(int)

    return pd.DataFrame(
        {
            "probabilidade_fraude": probabilidades,
            "classe_prevista": previsoes,
            "decisao": np.where(previsoes == 1, "ALERTA", "NORMAL"),
        },
        index=transacoes.index,
    )
