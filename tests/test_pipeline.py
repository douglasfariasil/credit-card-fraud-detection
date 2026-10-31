"""Testes de integração do pipeline de Machine Learning."""

import numpy as np
import pandas as pd

from fraud_detection.models.inference import prever_transacoes
from fraud_detection.models.persistence import (
    carregar_modelo,
    salvar_modelo,
)
from fraud_detection.models.training import (
    criar_random_forest,
    treinar_modelo,
)


def test_pipeline_completo_treinamento_persistencia_e_inferencia(
    tmp_path,
) -> None:
    X_treino = pd.DataFrame(
        {
            "Time": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
            "Amount": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
        }
    )
    y_treino = pd.Series([0, 0, 0, 1, 1, 1])

    X_novas = pd.DataFrame(
        {
            "Time": [6.0, 7.0],
            "Amount": [70.0, 80.0],
        }
    )

    modelo = criar_random_forest()
    modelo = treinar_modelo(modelo, X_treino, y_treino)

    probabilidades_originais = modelo.predict_proba(X_novas)[:, 1]

    caminho = tmp_path / "modelos" / "random_forest.joblib"

    salvar_modelo(
        modelo,
        caminho,
        limiar=0.15,
        colunas_entrada=X_treino.columns.tolist(),
    )

    artefato = carregar_modelo(caminho)

    resultado = prever_transacoes(X_novas, artefato)

    assert len(resultado) == len(X_novas)
    assert artefato.limiar == 0.15
    assert artefato.colunas_entrada == ("Time", "Amount")

    assert np.allclose(
        resultado["probabilidade_fraude"],
        probabilidades_originais,
    )

    assert np.array_equal(
        resultado["classe_prevista"],
        (probabilidades_originais >= 0.15).astype(int),
    )
