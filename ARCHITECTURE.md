# Arquitetura

## 1. Objetivo

Organizar o projeto em duas camadas complementares: notebook para exploração e comunicação dos experimentos; pacote Python para lógica reutilizável, testável e independente da interface.

## 2. Visão inicial

```text
Fonte de dados confirmada
        |
        v
Carregamento e validação
        |
        v
Exploração / qualidade dos dados
        |
        v
Separação treino / validação / teste
        |
        v
Pré-processamento dentro de Pipeline
        |
        v
Treino e comparação de modelos
        |
        v
Escolha do limiar na validação
        |
        v
Avaliação final no teste
        |
        v
Explicabilidade + relatório
```

## 3. Estrutura de módulos

- `src/fraud_detection/data/`: leitura, validação de esquema e verificações básicas de qualidade.
- `src/fraud_detection/features/`: transformações e construção de atributos.
- `src/fraud_detection/models/`: criação de pipelines e configuração de estimadores.
- `src/fraud_detection/evaluation/`: métricas, matrizes de confusão e escolha/avaliação de limiar.
- `notebooks/`: narrativa experimental, tabelas e gráficos com saídas verificáveis.
- `tests/`: testes unitários das funções reutilizáveis.
- `reports/figures/`: figuras selecionadas para documentação; não armazenar grandes artefatos desnecessários.
- `.github/workflows/`: verificações automatizadas básicas.

## 4. Fluxo de dados

1. Obter a base a partir da fonte indicada na Aula 1 da DIO.
2. Guardar o arquivo localmente fora do controle de versão, salvo se houver uma razão e permissão explícitas para outra abordagem.
3. Validar colunas esperadas, tipos, valores ausentes, duplicatas e distribuição do alvo.
4. Separar os dados antes de aprender parâmetros de pré-processamento.
5. Treinar candidatos usando pipelines; qualquer reamostragem deve ocorrer apenas dentro do treino.
6. Selecionar modelo e limiar com validação.
7. Avaliar uma única vez no teste reservado e registrar limitações.

## 5. Decisões importantes

### Notebook primeiro

A primeira entrega será `notebooks/01_exploracao_e_modelagem.ipynb`, pois o desafio pede um notebook completo. A lógica que amadurecer e precisar de testes será movida para `src/`.

### Desbalanceamento

Não se deve balancear o conjunto inteiro antes do split. Oversampling e undersampling serão comparados apenas no conjunto de treino ou dentro de validação cruzada, evitando vazamento.

### Métricas e limiar

A seleção do limiar depende do objetivo operacional. Recall alto pode aumentar falsos positivos; precisão alta pode deixar passar fraudes. O projeto deve mostrar esse trade-off e não afirmar que existe um limiar universalmente correto.

### Split aleatório versus temporal

O desafio sugere `train_test_split(..., stratify=y)`. Como existe uma coluna `Time`, vamos verificar sua semântica e a ordenação dos dados antes de decidir. O split estratificado pode ser usado para reproduzir o exercício, mas a limitação de não representar uma implantação futura deve ser documentada. Se adequado, uma análise temporal será uma evolução separada.

### Explicabilidade

Importância de atributos e SHAP serão usados para entender o comportamento do modelo. As colunas `V1`–`V28` foram transformadas por PCA segundo a descrição do desafio; portanto, não se deve atribuir a elas um significado de negócio que não foi fornecido.

## 6. Ambiente e reprodução

- Gerenciamento de dependências: Astral `uv`.
- Ambiente virtual: `.venv/`, ignorado pelo Git.
- Dependências e metadados: `pyproject.toml`.
- Lockfile: `uv.lock`, gerado e versionado após resolver dependências.
- Testes: `pytest`.
- Controle de versão: Git/GitHub.

## 7. Fora do escopo inicial

API de produção, serviço online, banco transacional, monitoramento operacional e bloqueio real de cartões. Essas extensões só serão consideradas após o experimento offline estar validado.
