"""Métricas e avaliação de classificadores de fraude."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)


@dataclass(frozen=True)
class ResultadoAvaliacao:
    """Resultados da avaliação de um classificador binário."""

    previsoes: NDArray[np.int64]
    relatorio_classificacao: str
    matriz_confusao: NDArray[np.int64]
    average_precision: float | None
    roc_auc: float | None


def avaliar_classificacao(
    y_real: ArrayLike,
    probabilidades: ArrayLike,
    limiar: float = 0.5,
) -> ResultadoAvaliacao:
    """Avalia previsões probabilísticas usando um limiar definido.

    O limiar deve ser escolhido previamente com dados de validação.
    Esta função não seleciona nem otimiza o limiar.
    """
    if not 0.0 <= limiar <= 1.0:
        raise ValueError("O limiar deve estar entre 0 e 1.")

    valores_reais = np.asarray(y_real)
    valores_probabilidade = np.asarray(probabilidades)

    if valores_reais.ndim != 1 or valores_probabilidade.ndim != 1:
        raise ValueError("Os rótulos e as probabilidades devem ser unidimensionais.")

    if len(valores_reais) != len(valores_probabilidade):
        raise ValueError("Os rótulos e as probabilidades devem ter o mesmo tamanho.")

    if len(valores_reais) == 0:
        raise ValueError("A avaliação exige pelo menos uma amostra.")

    if not np.isin(valores_reais, [0, 1]).all():
        raise ValueError("Os rótulos reais devem conter apenas 0 e 1.")

    if not np.isfinite(valores_probabilidade).all():
        raise ValueError("As probabilidades não podem conter valores não finitos.")

    if (
        (valores_probabilidade < 0).any()
        or (valores_probabilidade > 1).any()
    ):
        raise ValueError("As probabilidades devem estar entre 0 e 1.")

    previsoes = (valores_probabilidade >= limiar).astype(np.int64)

    relatorio = classification_report(
        valores_reais,
        previsoes,
        labels=[0, 1],
        target_names=["Normal", "Fraude"],
        digits=4,
        zero_division=0,
    )

    matriz = confusion_matrix(
        valores_reais,
        previsoes,
        labels=[0, 1],
    ).astype(np.int64)

    tem_duas_classes = np.unique(valores_reais).size == 2

    average_precision = (
        float(average_precision_score(valores_reais, valores_probabilidade))
        if tem_duas_classes
        else None
    )
    roc_auc = (
        float(roc_auc_score(valores_reais, valores_probabilidade))
        if tem_duas_classes
        else None
    )

    return ResultadoAvaliacao(
        previsoes=previsoes,
        relatorio_classificacao=relatorio,
        matriz_confusao=matriz,
        average_precision=average_precision,
        roc_auc=roc_auc,
    )
