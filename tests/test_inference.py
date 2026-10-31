"""Testes de inferência de novas transações."""

import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyClassifier

from fraud_detection.models.inference import prever_transacoes
from fraud_detection.models.persistence import ArtefatoModelo


@pytest.fixture
def artefato_treinado() -> ArtefatoModelo:
    """Cria um artefato com modelo treinado para os testes."""
    modelo = DummyClassifier(
        strategy="constant",
        constant=1,
    )

    X = pd.DataFrame(
        {
            "Time": [0.0, 1.0, 2.0, 3.0],
            "Amount": [10.0, 20.0, 30.0, 40.0],
        }
    )

    y = [0, 1, 0, 1]
    modelo.fit(X, y)

    return ArtefatoModelo(
        modelo=modelo,
        limiar=0.5,
        colunas_entrada=("Time", "Amount"),
    )


def test_prever_transacoes_retorna_probabilidade_e_decisao(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame(
        {
            "Time": [10.0, 20.0],
            "Amount": [100.0, 200.0],
        }
    )

    resultado = prever_transacoes(transacoes, artefato_treinado)

    assert list(resultado.columns) == [
        "probabilidade_fraude",
        "classe_prevista",
        "decisao",
    ]
    assert resultado["probabilidade_fraude"].tolist() == [1.0, 1.0]
    assert resultado["classe_prevista"].tolist() == [1, 1]
    assert resultado["decisao"].tolist() == ["ALERTA", "ALERTA"]


def test_prever_transacoes_preserva_indice_original(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame(
        {
            "Time": [10.0, 20.0],
            "Amount": [100.0, 200.0],
        },
        index=[15, 25],
    )

    resultado = prever_transacoes(transacoes, artefato_treinado)

    assert resultado.index.tolist() == [15, 25]


def test_prever_transacoes_aceita_colunas_em_ordem_diferente(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame(
        {
            "Amount": [100.0],
            "Time": [10.0],
        }
    )

    resultado = prever_transacoes(transacoes, artefato_treinado)

    assert resultado["decisao"].tolist() == ["ALERTA"]


def test_prever_transacoes_rejeita_colunas_ausentes(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame({"Time": [10.0]})

    with pytest.raises(ValueError, match="colunas ausentes"):
        prever_transacoes(transacoes, artefato_treinado)


def test_prever_transacoes_rejeita_colunas_extras(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame(
        {
            "Time": [10.0],
            "Amount": [100.0],
            "Class": [1],
        }
    )

    with pytest.raises(ValueError, match="colunas inesperadas"):
        prever_transacoes(transacoes, artefato_treinado)


def test_prever_transacoes_rejeita_dataframe_vazio(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame(columns=["Time", "Amount"])

    with pytest.raises(ValueError, match="Não há transações"):
        prever_transacoes(transacoes, artefato_treinado)


def test_prever_transacoes_rejeita_valores_nulos(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame(
        {
            "Time": [10.0],
            "Amount": [np.nan],
        }
    )

    with pytest.raises(ValueError, match="ausentes"):
        prever_transacoes(transacoes, artefato_treinado)


@pytest.mark.parametrize("valor", [np.inf, -np.inf])
def test_prever_transacoes_rejeita_valores_infinitos(
    artefato_treinado,
    valor,
) -> None:
    transacoes = pd.DataFrame(
        {
            "Time": [10.0],
            "Amount": [valor],
        }
    )

    with pytest.raises(ValueError, match="infinitos"):
        prever_transacoes(transacoes, artefato_treinado)


def test_prever_transacoes_rejeita_valores_nao_numericos(
    artefato_treinado,
) -> None:
    transacoes = pd.DataFrame(
        {
            "Time": ["texto"],
            "Amount": [100.0],
        }
    )

    with pytest.raises(ValueError, match="numéricos"):
        prever_transacoes(transacoes, artefato_treinado)


def test_prever_transacoes_rejeita_modelo_sem_predict_proba() -> None:
    from sklearn.dummy import DummyRegressor

    modelo = DummyRegressor()
    modelo.fit([[0.0], [1.0]], [0.0, 1.0])

    artefato = ArtefatoModelo(
        modelo=modelo,
        limiar=0.5,
        colunas_entrada=("Time",),
    )

    transacoes = pd.DataFrame({"Time": [10.0]})

    with pytest.raises(TypeError, match="predict_proba"):
        prever_transacoes(transacoes, artefato)
