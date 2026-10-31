"""Testes para as métricas de avaliação."""

import numpy as np
import pytest

from fraud_detection.evaluation.metrics import avaliar_classificacao


def test_avaliar_classificacao_com_dados_sinteticos() -> None:
    y_real = np.array([0, 0, 1, 1])
    probabilidades = np.array([0.1, 0.7, 0.8, 0.4])

    resultado = avaliar_classificacao(
        y_real,
        probabilidades,
        limiar=0.5,
    )

    assert resultado.previsoes.tolist() == [0, 1, 1, 0]
    assert resultado.matriz_confusao.tolist() == [
        [1, 1],
        [1, 1],
    ]
    assert "Normal" in resultado.relatorio_classificacao
    assert "Fraude" in resultado.relatorio_classificacao
    assert resultado.average_precision == pytest.approx(5 / 6)
    assert resultado.roc_auc == pytest.approx(0.75)


def test_avaliar_classificacao_aceita_limiar_diferente() -> None:
    resultado = avaliar_classificacao(
        [0, 1],
        [0.4, 0.6],
        limiar=0.6,
    )

    assert resultado.previsoes.tolist() == [0, 1]


@pytest.mark.parametrize("limiar", [-0.1, 1.1])
def test_avaliar_classificacao_rejeita_limiar_invalido(
    limiar: float,
) -> None:
    with pytest.raises(ValueError, match="limiar"):
        avaliar_classificacao([0, 1], [0.2, 0.8], limiar=limiar)


def test_avaliar_classificacao_rejeita_tamanhos_diferentes() -> None:
    with pytest.raises(ValueError, match="mesmo tamanho"):
        avaliar_classificacao([0, 1], [0.2])


def test_avaliar_classificacao_rejeita_probabilidade_invalida() -> None:
    with pytest.raises(ValueError, match="entre 0 e 1"):
        avaliar_classificacao([0, 1], [0.2, 1.5])



def test_avaliar_classificacao_rejeita_dados_vazios() -> None:
    with pytest.raises(ValueError, match="pelo menos uma amostra"):
        avaliar_classificacao([], [])


@pytest.mark.parametrize(
    "probabilidades",
    [[0.2, float("nan")], [0.2, float("inf")], [0.2, float("-inf")]],
)
def test_avaliar_classificacao_rejeita_probabilidades_nao_finitas(
    probabilidades: list[float],
) -> None:
    with pytest.raises(ValueError, match="não podem conter valores não finitos"):
        avaliar_classificacao([0, 1], probabilidades)


def test_avaliar_classificacao_rejeita_rotulos_invalidos() -> None:
    with pytest.raises(ValueError, match="apenas 0 e 1"):
        avaliar_classificacao([0, 2], [0.1, 0.9])


def test_avaliar_classificacao_preserva_matriz_com_uma_classe() -> None:
    resultado = avaliar_classificacao([0, 0], [0.1, 0.8])

    assert resultado.previsoes.tolist() == [0, 1]
    assert resultado.matriz_confusao.tolist() == [[1, 1], [0, 0]]
    assert resultado.average_precision is None
    assert resultado.roc_auc is None
