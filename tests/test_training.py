"""Testes para configuração e treinamento dos modelos."""

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from fraud_detection.models.training import (
    criar_random_forest,
    treinar_modelo,
)


def test_criar_random_forest_com_parametros_esperados() -> None:
    modelo = criar_random_forest()

    assert isinstance(modelo, RandomForestClassifier)
    assert modelo.n_estimators == 200
    assert modelo.class_weight == "balanced"
    assert modelo.min_samples_leaf == 2
    assert modelo.random_state == 42
    assert modelo.n_jobs == -1


def test_treinar_modelo_com_dados_sinteticos() -> None:
    X_treino = np.array([
        [0.0, 0.0],
        [0.1, 0.2],
        [0.2, 0.1],
        [0.8, 0.9],
        [0.9, 0.8],
        [1.0, 1.0],
    ])
    y_treino = np.array([0, 0, 0, 1, 1, 1])

    modelo = criar_random_forest()
    modelo_treinado = treinar_modelo(
        modelo,
        X_treino,
        y_treino,
    )

    assert modelo_treinado is modelo
    assert modelo_treinado.classes_.tolist() == [0, 1]

    previsoes = modelo_treinado.predict(X_treino)
    assert previsoes.shape == y_treino.shape
    assert set(previsoes).issubset({0, 1})
