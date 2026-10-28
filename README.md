# Credit Card Fraud Detection

Projeto de portfólio para estudar detecção de fraude em transações com cartão de crédito, com foco em avaliação correta de dados altamente desbalanceados, explicabilidade e reprodutibilidade.

> **Status:** estrutura inicial. O dataset ainda precisa ser confirmado a partir da Aula 1 do laboratório da DIO. Não coloque dados privados ou o arquivo bruto no Git.

## Objetivos

- Explorar os dados e entender a prevalência de fraude.
- Criar um baseline com Regressão Logística e compará-lo com Random Forest e XGBoost.
- Avaliar a classe fraude com precisão, recall, F1 e curvas ROC/Precisão-Recall.
- Escolher o limiar de decisão com base em custos e objetivos explícitos, não apenas no padrão 0,5.
- Investigar explicações globais e locais com SHAP, quando apropriado.
- Tornar os experimentos reproduzíveis e documentar limitações.

## Tecnologias

Python, pandas, NumPy, scikit-learn, imbalanced-learn, XGBoost, SHAP, Jupyter, matplotlib, seaborn, pytest e Astral uv.

## Começar

Pré-requisitos: Python compatível com o `pyproject.toml` e `uv` instalado.

```bash
uv sync
uv run python -c "import pandas, sklearn; print('Ambiente pronto')"
uv run jupyter lab
```

Se ainda não existir `uv.lock`, gere-o localmente com `uv lock` e versione o arquivo.

## Estrutura

```text
.
├── AGENTS.md
├── ARCHITECTURE.md
├── BUSINESS_RULES.md
├── ROADMAP.md
├── README.md
├── pyproject.toml
├── data/
│   └── README.md
├── notebooks/
│   └── README.md
├── reports/
│   └── figures/
├── src/
│   └── fraud_detection/
│       ├── __init__.py
│       ├── data/
│       ├── evaluation/
│       ├── features/
│       └── models/
├── tests/
└── .github/workflows/
    └── tests.yml
```

## Princípios de avaliação

A acurácia não será a métrica principal porque a classe fraude é rara. Recall, precisão, F1, matriz de confusão e curva Precisão-Recall serão analisados em conjunto. Métricas de teste só serão usadas para avaliação final; decisões de modelo e limiar devem ser feitas com validação, sem ajustar decisões ao conjunto de teste.

## Dataset

Consulte `data/README.md`. O link e a licença/termos de uso precisam ser confirmados no material da Aula 1. O dataset não deve ser commitado.

## Como reproduzir

Depois de confirmar a fonte e implementar o notebook:

1. Clone o repositório.
2. Execute `uv sync`.
3. Abra a pasta no VS Code e selecione o interpretador `.venv`.
4. Execute o notebook `notebooks/01_exploracao_e_modelagem.ipynb` de cima para baixo.
5. Execute `uv run pytest`.

## Limitações

Este é um projeto educacional, não um sistema pronto para bloquear transações reais. Os dados descritos no desafio incluem `Time`, `Amount`, `Class` e `V1`–`V28`; a semântica das variáveis PCA é limitada. Resultados dependem da versão e origem exatas do dataset.
