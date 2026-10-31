import numpy as np
import pandas as pd
import pytest

from fraud_detection.data.loader import COLUNAS_ESPERADAS, carregar_dataset


def criar_dataset_valido():
    """Cria uma transação válida para os testes."""
    return pd.DataFrame(
        [[0.0] * (len(COLUNAS_ESPERADAS) - 1) + [0.0]],
        columns=COLUNAS_ESPERADAS,
    )


def test_rejeita_arquivo_com_extensao_invalida(tmp_path):
    arquivo = tmp_path / "dataset.txt"
    criar_dataset_valido().to_csv(arquivo, index=False)

    with pytest.raises(ValueError, match="extensão .csv"):
        carregar_dataset(arquivo)


def test_rejeita_caminho_que_e_diretorio(tmp_path):
    diretorio = tmp_path / "dataset.csv"
    diretorio.mkdir()

    with pytest.raises(ValueError, match="não aponta para um arquivo"):
        carregar_dataset(diretorio)


def test_rejeita_dataset_vazio(tmp_path):
    arquivo = tmp_path / "vazio.csv"
    pd.DataFrame(columns=COLUNAS_ESPERADAS).to_csv(
        arquivo, index=False
    )

    with pytest.raises(ValueError, match="dataset está vazio"):
        carregar_dataset(arquivo)


def test_rejeita_texto_em_coluna_numerica(tmp_path):
    arquivo = tmp_path / "texto.csv"
    df = criar_dataset_valido()
    df["Amount"] = df["Amount"].astype(object)
    df.loc[0, "Amount"] = "valor_invalido"
    df.to_csv(arquivo, index=False)

    with pytest.raises(ValueError, match="valores numéricos válido"):
        carregar_dataset(arquivo)


def test_rejeita_classe_diferente_de_zero_ou_um(tmp_path):
    arquivo = tmp_path / "classe_invalida.csv"
    df = criar_dataset_valido()
    df.loc[0, "Class"] = 2
    df.to_csv(arquivo, index=False)

    with pytest.raises(ValueError, match="somente os valores 0 e 1"):
        carregar_dataset(arquivo)


def test_rejeita_valor_infinito(tmp_path):
    arquivo = tmp_path / "infinito.csv"
    df = criar_dataset_valido()

    df["Amount"] = df["Amount"].astype(float)
    df.loc[0, "Amount"] = np.inf
    df.to_csv(arquivo, index=False)

    with pytest.raises(ValueError, match="valores infinitos"):
        carregar_dataset(arquivo)
