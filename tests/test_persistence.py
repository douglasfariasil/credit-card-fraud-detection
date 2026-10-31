"""Testes de persistência dos modelos."""

import numpy as np
import pytest
from sklearn.dummy import DummyClassifier
from sklearn.exceptions import NotFittedError

from fraud_detection.models.persistence import (
    ArtefatoModelo,
    carregar_modelo,
    salvar_modelo,
)


@pytest.fixture
def modelo_treinado() -> DummyClassifier:
    """Cria um classificador simples e treinado para os testes."""
    modelo = DummyClassifier(strategy="prior")
    modelo.fit([[0.0, 1.0], [1.0, 0.0]], [0, 1])
    return modelo


def test_salvar_e_carregar_modelo_preserva_configuracoes(
    tmp_path,
    modelo_treinado,
) -> None:
    caminho = tmp_path / "modelos" / "fraude.joblib"

    salvar_modelo(
        modelo_treinado,
        caminho,
        limiar=0.15,
        colunas_entrada=("Time", "Amount"),
    )

    artefato = carregar_modelo(caminho)

    assert isinstance(artefato, ArtefatoModelo)
    assert artefato.limiar == pytest.approx(0.15)
    assert artefato.colunas_entrada == ("Time", "Amount")
    assert np.array_equal(
        artefato.modelo.predict([[0.0, 1.0]]),
        modelo_treinado.predict([[0.0, 1.0]]),
    )


def test_salvar_modelo_rejeita_modelo_nao_treinado(tmp_path) -> None:
    modelo = DummyClassifier(strategy="prior")

    with pytest.raises(NotFittedError):
        salvar_modelo(
            modelo,
            tmp_path / "modelo.joblib",
            limiar=0.5,
            colunas_entrada=("Time", "Amount"),
        )


@pytest.mark.parametrize("limiar", [-0.1, 1.1, np.nan, np.inf, -np.inf])
def test_salvar_modelo_rejeita_limiar_invalido(
    tmp_path,
    modelo_treinado,
    limiar,
) -> None:
    with pytest.raises(ValueError, match="limiar"):
        salvar_modelo(
            modelo_treinado,
            tmp_path / "modelo.joblib",
            limiar=limiar,
            colunas_entrada=("Time", "Amount"),
        )


@pytest.mark.parametrize(
    "colunas",
    [
        (),
        ("Time", "Time"),
        ("Time", ""),
        ("Time", "   "),
        ("Time", 123),
    ],
)
def test_salvar_modelo_rejeita_colunas_invalidas(
    tmp_path,
    modelo_treinado,
    colunas,
) -> None:
    with pytest.raises(ValueError):
        salvar_modelo(
            modelo_treinado,
            tmp_path / "modelo.joblib",
            limiar=0.5,
            colunas_entrada=colunas,
        )


def test_carregar_modelo_rejeita_arquivo_inexistente(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        carregar_modelo(tmp_path / "inexistente.joblib")
