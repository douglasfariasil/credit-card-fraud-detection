"""Análise e seleção de limiares usando dados de validação."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score


@dataclass(frozen=True)
class ResultadoLimiar:
    """Métricas e contagens para um limiar de classificação."""

    limiar: float
    precisao: float
    recall: float
    f1: float
    falsos_positivos: int
    fraudes_detectadas: int
    fraudes_perdidas: int
    alertas_totais: int


def analisar_limiares(
    y_real: ArrayLike,
    probabilidades: ArrayLike,
    limiares: ArrayLike,
) -> list[ResultadoLimiar]:
    """Calcula métricas para cada limiar, sem escolher o limiar final."""
    valores_reais = np.asarray(y_real)
    valores_probabilidade = np.asarray(probabilidades)
    valores_limiares = np.asarray(limiares, dtype=float)

    if valores_reais.ndim != 1 or valores_probabilidade.ndim != 1:
        raise ValueError("Os rótulos e as probabilidades devem ser unidimensionais.")

    if len(valores_reais) == 0:
        raise ValueError("A análise exige pelo menos uma amostra.")

    if len(valores_reais) != len(valores_probabilidade):
        raise ValueError("Os rótulos e as probabilidades devem ter o mesmo tamanho.")

    if not np.isin(valores_reais, [0, 1]).all():
        raise ValueError("Os rótulos reais devem conter apenas 0 e 1.")

    if not np.isfinite(valores_probabilidade).all():
        raise ValueError("As probabilidades devem ser finitas.")

    if ((valores_probabilidade < 0) | (valores_probabilidade > 1)).any():
        raise ValueError("As probabilidades devem estar entre 0 e 1.")

    if valores_limiares.ndim != 1 or len(valores_limiares) == 0:
        raise ValueError("Informe pelo menos um limiar em uma lista unidimensional.")

    if not np.isfinite(valores_limiares).all():
        raise ValueError("Os limiares devem ser finitos.")

    if ((valores_limiares < 0) | (valores_limiares > 1)).any():
        raise ValueError("Os limiares devem estar entre 0 e 1.")

    resultados = []

    for limiar in valores_limiares:
        previsoes = (valores_probabilidade >= limiar).astype(int)

        _tn, fp, fn, tp = confusion_matrix(
            valores_reais,
            previsoes,
            labels=[0, 1],
        ).ravel()

        resultados.append(
            ResultadoLimiar(
                limiar=float(limiar),
                precisao=float(
                    precision_score(valores_reais, previsoes, zero_division=0)
                ),
                recall=float(
                    recall_score(valores_reais, previsoes, zero_division=0)
                ),
                f1=float(f1_score(valores_reais, previsoes, zero_division=0)),
                falsos_positivos=int(fp),
                fraudes_detectadas=int(tp),
                fraudes_perdidas=int(fn),
                alertas_totais=int(tp + fp),
            )
        )

    return resultados


def selecionar_limiar(
    resultados: list[ResultadoLimiar],
    recall_minimo: float = 0.85,
) -> ResultadoLimiar | None:
    """Seleciona o menor volume de alertas entre os candidatos elegíveis.

    Em caso de empate no número de alertas, prefere o maior limiar.
    """
    if not 0 <= recall_minimo <= 1:
        raise ValueError("O recall mínimo deve estar entre 0 e 1.")

    candidatos = [
        resultado
        for resultado in resultados
        if resultado.recall >= recall_minimo
    ]

    if not candidatos:
        return None

    return min(
        candidatos,
        key=lambda resultado: (
            resultado.alertas_totais,
            -resultado.limiar,
        ),
    )


def resultados_para_dataframe(
    resultados: list[ResultadoLimiar],
) -> pd.DataFrame:
    """Converte os resultados para uma tabela adequada ao notebook."""
    return pd.DataFrame(
        [
            {
                "Limiar": resultado.limiar,
                "Precisao": resultado.precisao,
                "Recall": resultado.recall,
                "F1": resultado.f1,
                "Falsos positivos": resultado.falsos_positivos,
                "Fraudes detectadas": resultado.fraudes_detectadas,
                "Fraudes perdidas": resultado.fraudes_perdidas,
                "Alertas totais": resultado.alertas_totais,
            }
            for resultado in resultados
        ]
    )
