"""Testes para análise e seleção de limiares."""

import pytest

from fraud_detection.evaluation.thresholds import (
    analisar_limiares,
    resultados_para_dataframe,
    selecionar_limiar,
)


def test_analisar_limiares_calcula_contagens() -> None:
    resultados = analisar_limiares(
        y_real=[0, 0, 1, 1],
        probabilidades=[0.1, 0.7, 0.8, 0.4],
        limiares=[0.5],
    )

    resultado = resultados[0]

    assert resultado.limiar == 0.5
    assert resultado.falsos_positivos == 1
    assert resultado.fraudes_detectadas == 1
    assert resultado.fraudes_perdidas == 1
    assert resultado.alertas_totais == 2
    assert resultado.precisao == pytest.approx(0.5)
    assert resultado.recall == pytest.approx(0.5)
    assert resultado.f1 == pytest.approx(0.5)


def test_selecionar_limiar_respeita_recall_e_minimiza_alertas() -> None:
    resultados = analisar_limiares(
        y_real=[0, 0, 1, 1],
        probabilidades=[0.1, 0.2, 0.8, 0.9],
        limiares=[0.1, 0.5, 0.8],
    )

    escolhido = selecionar_limiar(
        resultados,
        recall_minimo=0.5,
    )

    assert escolhido is not None
    assert escolhido.limiar == 0.8
    assert escolhido.recall == pytest.approx(1.0)
    assert escolhido.alertas_totais == 2
    assert escolhido.fraudes_detectadas == 2
    assert escolhido.fraudes_perdidas == 0


def test_selecionar_limiar_retorna_none_sem_candidato() -> None:
    resultados = analisar_limiares(
        y_real=[0, 1],
        probabilidades=[0.1, 0.4],
        limiares=[0.5, 0.8],
    )

    assert selecionar_limiar(resultados, recall_minimo=0.85) is None


def test_resultados_para_dataframe_cria_colunas_esperadas() -> None:
    resultados = analisar_limiares(
        y_real=[0, 1],
        probabilidades=[0.1, 0.9],
        limiares=[0.5],
    )

    tabela = resultados_para_dataframe(resultados)

    assert len(tabela) == 1
    assert "Limiar" in tabela.columns
    assert "Alertas totais" in tabela.columns
    assert tabela.iloc[0]["Fraudes detectadas"] == 1


def test_analisar_limiares_rejeita_probabilidade_invalida() -> None:
    with pytest.raises(ValueError, match="entre 0 e 1"):
        analisar_limiares([0, 1], [0.1, 1.2], [0.5])


def test_analisar_limiares_rejeita_tamanhos_diferentes() -> None:
    with pytest.raises(ValueError, match="mesmo tamanho"):
        analisar_limiares([0, 1], [0.2], [0.5])



@pytest.mark.parametrize(
    "limiares",
    [[], [float("nan")], [float("inf")], [-0.1], [1.1]],
)
def test_analisar_limiares_rejeita_limiares_invalidos(
    limiares: list[float],
) -> None:
    with pytest.raises(ValueError):
        analisar_limiares([0, 1], [0.1, 0.9], limiares)


def test_analisar_limiares_aceita_amostras_de_uma_classe() -> None:
    resultados = analisar_limiares(
        y_real=[0, 0],
        probabilidades=[0.1, 0.8],
        limiares=[0.5],
    )

    assert resultados[0].falsos_positivos == 1
    assert resultados[0].fraudes_detectadas == 0
    assert resultados[0].fraudes_perdidas == 0
    assert resultados[0].recall == 0.0
