# Arquitetura do Projeto

## 1. Objetivo

O projeto organiza o desenvolvimento de um sistema experimental de detecção de fraudes em transações com cartão de crédito.

A arquitetura separa duas responsabilidades:

- **Notebook:** exploração dos dados, experimentos, visualizações e apresentação dos resultados.
- **Pacote Python:** implementação de funções reutilizáveis, testáveis e independentes do notebook.

O objetivo é manter o código de Machine Learning organizado, facilitar sua manutenção e permitir a evolução futura para serviços de inferência.

## 2. Visão geral do fluxo

```text
Dataset
   |
   v
Carregamento e validação
   |
   v
Exploração dos dados
   |
   v
Separação treino / validação / teste
   |
   v
Treinamento do Random Forest
   |
   v
Avaliação na validação
   |
   v
Seleção do limiar de classificação
   |
   v
Persistência do modelo e configuração
   |
   v
Carregamento do artefato
   |
   v
Inferência de novas transações
   |
   v
Avaliação final no conjunto de teste
```

O conjunto de teste permanece reservado para a avaliação final. A seleção do limiar é realizada exclusivamente com os dados de validação.

## 3. Organização dos módulos

### `src/fraud_detection/data/`

Responsável pelo carregamento e pela validação estrutural dos dados.

- `loader.py`: verifica a existência do arquivo, extensão, esquema esperado, valores ausentes, valores finitos e domínio da variável-alvo.

### `src/fraud_detection/evaluation/`

Responsável pela avaliação dos modelos e pela análise de limiares.

- `metrics.py`: calcula métricas de classificação, relatório, matriz de confusão, Average Precision e ROC-AUC.
- `thresholds.py`: analisa diferentes limiares e seleciona candidatos conforme os critérios experimentais.

### `src/fraud_detection/models/`

Responsável pelo treinamento, armazenamento e inferência.

- `training.py`: configura e treina o Random Forest.
- `persistence.py`: salva e carrega o modelo junto com o limiar e os nomes das colunas de entrada.
- `inference.py`: valida novas entradas, calcula probabilidades e produz as decisões de classificação.

### `src/fraud_detection/features/`

Espaço reservado para futuras transformações e construção de atributos. Não representa, neste momento, um pipeline independente de engenharia de atributos.

### `notebooks/`

Contém os experimentos, análises, visualizações e resultados utilizados para desenvolver e documentar o modelo.

### `tests/`

Contém testes automatizados para validação dos módulos e do fluxo integrado de treinamento, persistência e inferência.

### `reports/figures/`

Diretório destinado às figuras selecionadas para documentação e apresentação dos resultados.

## 4. Responsabilidades e fluxo de dados

1. Carregar o dataset e validar sua estrutura.
2. Explorar a distribuição das classes e as características dos dados.
3. Separar treino, validação e teste.
4. Treinar o modelo usando somente os dados de treinamento.
5. Calcular probabilidades e avaliar candidatos na validação.
6. Selecionar o limiar de classificação usando o critério experimental definido.
7. Salvar o modelo treinado, o limiar e as colunas esperadas.
8. Carregar o artefato para realizar inferência.
9. Avaliar o desempenho final no conjunto de teste.

## 5. Persistência do modelo

A persistência utiliza `joblib`.

O artefato contém:

- Modelo treinado.
- Limiar de classificação.
- Nomes e ordem das colunas esperadas na entrada.

O arquivo é armazenado localmente em:

`artifacts/models/random_forest.joblib`

Os artefatos treinados não devem ser versionados no Git.

**Segurança:** arquivos serializados com joblib podem executar código durante o carregamento. Portanto, somente artefatos de origem confiável devem ser carregados.

## 6. Inferência

A função `prever_transacoes` recebe um DataFrame com as variáveis de entrada e um artefato carregado.

Antes de realizar as previsões, valida:

- Tipo do objeto recebido.
- Presença de registros.
- Colunas obrigatórias e ausência de colunas extras.
- Conversibilidade dos valores para formato numérico.
- Ausência de valores nulos e infinitos.

O resultado contém:

- `probabilidade_fraude`
- `classe_prevista`
- `decisao`

A decisão utiliza o limiar armazenado no artefato, evitando depender de um valor definido separadamente durante a inferência.

## 7. Testes e qualidade

O projeto utiliza:

- `pytest` para testes unitários e de integração.
- `ruff` para análise estática e qualidade do código.
- `git diff --check` para verificar problemas de whitespace nas alterações.

Na última execução validada, a suíte apresentou 59 testes aprovados e o Ruff não encontrou erros.

## 8. Ambiente e dependências

- Python 3.13 ou superior.
- Astral `uv` para gerenciamento de dependências.
- `pyproject.toml` para configuração do projeto.
- `uv.lock` para reprodutibilidade das dependências.
- Git para controle de versão.

## 9. Limitações e evoluções futuras

O projeto é um experimento educacional e não constitui um sistema de detecção de fraude pronto para produção.

Não fazem parte da implementação atual:

- API de inferência com FastAPI.
- Banco de dados transacional.
- Monitoramento de modelos em produção.
- Detecção de drift.
- Bloqueio automático de transações.
- Integração com instituições financeiras.

Essas funcionalidades poderão ser consideradas em etapas futuras, após a validação do fluxo offline e de seus resultados.
