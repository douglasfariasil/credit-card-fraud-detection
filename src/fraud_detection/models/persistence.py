"""Persistência de modelos treinados e suas configurações de inferência."""

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.utils.validation import check_is_fitted


@dataclass(frozen=True)
class ArtefatoModelo:
    """Modelo treinado acompanhado de suas configurações de inferência."""

    modelo: Any
    limiar: float
    colunas_entrada: tuple[str, ...]


def _validar_limiar(limiar: float) -> None:
    """Verifica se o limiar está dentro do intervalo permitido."""
    if not np.isfinite(limiar) or not 0 <= limiar <= 1:
        raise ValueError("O limiar deve ser um número finito entre 0 e 1.")


def _validar_colunas(colunas: Sequence[str]) -> tuple[str, ...]:
    """Valida e normaliza os nomes das colunas de entrada."""
    resultado = tuple(colunas)

    if not resultado:
        raise ValueError("É necessário informar pelo menos uma coluna de entrada.")

    if any(not isinstance(coluna, str) or not coluna.strip() for coluna in resultado):
        raise ValueError("Os nomes das colunas devem ser strings não vazias.")

    if len(resultado) != len(set(resultado)):
        raise ValueError("A lista de colunas não pode conter nomes duplicados.")

    return resultado


def salvar_modelo(
    modelo: Any,
    caminho: str | Path,
    limiar: float,
    colunas_entrada: Sequence[str],
) -> Path:
    """Salva o modelo treinado e suas configurações em um único artefato."""
    check_is_fitted(modelo)
    _validar_limiar(limiar)

    artefato = ArtefatoModelo(
        modelo=modelo,
        limiar=float(limiar),
        colunas_entrada=_validar_colunas(colunas_entrada),
    )

    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(artefato, destino)

    return destino


def carregar_modelo(caminho: str | Path) -> ArtefatoModelo:
    """Carrega e valida um artefato de modelo previamente salvo."""
    origem = Path(caminho)

    if not origem.is_file():
        raise FileNotFoundError(f"Artefato de modelo não encontrado: {origem}")

    artefato = joblib.load(origem)

    if not isinstance(artefato, ArtefatoModelo):
        raise TypeError("O arquivo não contém um artefato de modelo válido.")

    _validar_limiar(artefato.limiar)
    _validar_colunas(artefato.colunas_entrada)
    check_is_fitted(artefato.modelo)

    return artefato
