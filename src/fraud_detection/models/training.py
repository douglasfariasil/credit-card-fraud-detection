"""Configuração e treinamento de modelos de detecção de fraude."""

from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.validation import check_is_fitted


def criar_random_forest() -> RandomForestClassifier:
    """Cria o Random Forest com os parâmetros do experimento inicial."""
    return RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        max_depth=None,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )


def treinar_modelo(
    modelo: Any,
    X_treino: Any,
    y_treino: Any,
) -> Any:
    """Treina um estimador usando exclusivamente os dados de treino."""
    modelo.fit(X_treino, y_treino)
    check_is_fitted(modelo)
    return modelo
