# Credit Card Fraud Detection

Projeto de engenharia de Machine Learning para detecção de fraudes em transações com cartão de crédito. O objetivo é desenvolver um fluxo reproduzível, testável e organizado, desde a validação dos dados até a inferência com um modelo persistido.

O projeto dá atenção especial ao desbalanceamento entre transações legítimas e fraudulentas, à prevenção de vazamento de dados e à escolha de um limiar de classificação orientado por métricas.

## Status

Repositório público publicado no GitHub. O projeto possui um pipeline de Machine Learning modular, testável e documentado.

Implementado:

- Carregamento e validação do dataset.
- Treinamento do modelo Random Forest.
- Cálculo de métricas de classificação.
- Seleção de limiar usando dados de validação.
- Persistência e carregamento do modelo.
- Inferência de novas transações.
- Testes unitários e de integração.
- Integração contínua com GitHub Actions, executando Pytest e Ruff.

A suíte possui 59 testes automatizados aprovados. O workflow publicado no GitHub também foi executado com sucesso.

Próximas evoluções: avaliação temporal, calibração de probabilidades, explicabilidade, API de inferência e monitoramento.

## Problema de negócio

Identificar transações potencialmente fraudulentas em uma base altamente desbalanceada.

Nesse cenário, a acurácia isolada pode ser enganosa: um modelo pode classificar quase todas as transações como legítimas e ainda apresentar acurácia elevada, deixando de detectar fraudes.

Por isso, a avaliação considera principalmente:

- **Precisão:** proporção dos alertas que realmente são fraudes.
- **Recall:** proporção das fraudes reais que foram identificadas.
- **F1-score:** equilíbrio entre precisão e recall.
- **Matriz de confusão:** distribuição de acertos e erros.
- **Average Precision:** desempenho resumido da curva Precisão-Recall.
- **ROC-AUC:** métrica complementar de discriminação.

## Resultado experimental

<text>Modelo selecionado: Random Forest</text>

<text>Limiar de classificação: 0,15, selecionado com dados de validação.</text>

| Métrica no teste | Resultado |
|---|---:|
| Precisão da fraude | 68,42% |
| Recall da fraude | 89,04% |
| F1-score da fraude | 0,7738 |
| Average Precision | 0,8708 |
| ROC-AUC | 0,9614 |

### Matriz de confusão

| | Previsto normal | Previsto fraude |
|---|---:|---:|
| Real normal | 42.617 | 30 |
| Real fraude | 8 | 65 |

No conjunto de teste, o modelo identificou 65 das 73 fraudes, deixou 8 passar e gerou 95 alertas, dos quais 30 eram falsos positivos.

Esses resultados representam o experimento atual e não garantem desempenho equivalente em dados de produção.

## Arquitetura

O projeto separa a exploração experimental da lógica reutilizável:

- `notebooks/`: exploração, experimentos, visualizações e comunicação dos resultados.
- `src/fraud_detection/data/`: carregamento e validação dos dados.
- `src/fraud_detection/evaluation/`: métricas e análise de limiares.
- `src/fraud_detection/models/`: treinamento, persistência e inferência.
- `src/fraud_detection/features/`: espaço reservado para futuras transformações de atributos.
- `tests/`: testes automatizados dos módulos e do pipeline.

A organização segue o princípio de manter no pacote Python a lógica que precisa ser reutilizada e testada, deixando o notebook responsável pela narrativa experimental.

Consulte também:
- `ARCHITECTURE.md`: decisões e fluxo da arquitetura.
- `BUSINESS_RULES.md`: regras de negócio e critérios experimentais.
- `ROADMAP.md`: etapas e evoluções planejadas.
- `data/README.md`: fonte e informações do dataset.

## Regras contra vazamento de dados

A avaliação segue estas regras:

1. Separar treino, validação e teste antes de ajustar transformações.
2. Treinar o modelo somente com os dados de treinamento.
3. Usar validação para comparar modelos e selecionar o limiar.
4. Manter o conjunto de teste reservado para a avaliação final.
5. Não ajustar o limiar com base nos resultados do teste.

A meta experimental de recall mínimo é de 85%. Entre os limiares que atendem a essa meta na validação, busca-se minimizar a quantidade de alertas.

Essa meta é uma hipótese de avaliação para o projeto, não uma exigência operacional validada por uma instituição financeira.

## Tecnologias

### Utilizadas no projeto

- Python 3.13+
- pandas e NumPy
- scikit-learn
- imbalanced-learn
- matplotlib e seaborn
- joblib
- JupyterLab
- pytest
- Ruff
- Astral uv
- Git e GitHub Actions

### Dependências adicionais

XGBoost e SHAP estão declarados no ambiente de dependências, mas não fazem parte dos resultados do modelo final apresentados neste experimento.
## Como executar

### 1. Pré-requisitos

Instale Python compatível com o `pyproject.toml` e o gerenciador de dependências `uv`.

### 2. Obter o projeto

```bash
git clone https://github.com/douglasfariasil/credit-card-fraud-detection.git
cd credit-card-fraud-detection
```


### 3. Instalar dependências

```bash
uv sync
```

### 4. Preparar os dados

Consulte `data/README.md` para obter a referência do dataset e as instruções relacionadas à sua origem.

Os arquivos brutos não devem ser adicionados ao Git.

### 5. Executar o notebook

```bash
uv run jupyter lab
```

Abra `notebooks/01_exploracao_e_modelagem.ipynb` e execute as células em ordem.

### 6. Executar os testes

```bash
uv run pytest -q
```

### 7. Verificar qualidade do código

```bash
uv run ruff check .
git diff --check
```

No estado atual da suíte, foram aprovados 59 testes automatizados.

## Persistência e inferência

O projeto permite salvar e carregar um artefato contendo:

- Modelo treinado.
- Limiar de classificação selecionado.
- Nomes e ordem das colunas de entrada.

A função de inferência valida o esquema, os valores numéricos e a presença de valores finitos antes de produzir os resultados.

As saídas incluem:

- `probabilidade_fraude`
- `classe_prevista`
- `decisao`

A decisão pode ser `ALERTA` ou `NORMAL`, conforme a probabilidade estimada e o limiar armazenado.

Os artefatos `.joblib` são arquivos locais e não devem ser carregados quando sua origem não for confiável.

## Dataset

O arquivo utilizado no laboratório é `creditcard.csv`.

A referência indicada na Aula 1 da DIO é:

https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv

A base contém as colunas `Time`, `Amount`, `V1` a `V28` e `Class`.

- `Class = 1`: fraude.
- `Class = 0`: transação normal.
- `V1` a `V28`: atributos transformados por PCA, conforme a descrição tradicional da base.

A licença e os termos de uso e redistribuição ainda precisam ser confirmados. Consulte `data/README.md` antes de redistribuir o dataset.

## Limitações

- O projeto tem finalidade educacional e demonstrativa.
- O limiar escolhido não representa uma política operacional validada.
- Os custos financeiros de falsos positivos e falsos negativos não foram definidos.
- A calibração das probabilidades ainda precisa ser investigada.
- A avaliação temporal e a estabilidade em diferentes partições são evoluções futuras.
- As variáveis transformadas por PCA não permitem atribuir diretamente significado de negócio aos componentes.
- Não existe integração com sistemas financeiros reais.

## Próximos passos

- Avaliar estabilidade e generalização do modelo.
- Investigar calibração de probabilidades.
- Avaliar uma estratégia de divisão temporal.
- Implementar análise de explicabilidade com SHAP.
- Desenvolver uma API de inferência com FastAPI.
- Investigar monitoramento de qualidade dos dados e drift.
- Confirmar a licença e os termos de uso do dataset.
## Finalidade

Este projeto demonstra conhecimentos de Python, análise de dados, Machine Learning, organização de código, persistência de modelos, inferência e testes automatizados.

Não deve ser utilizado para bloquear transações reais sem validação adicional, avaliação operacional, controles de segurança e monitoramento adequado.
