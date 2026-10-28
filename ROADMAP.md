# Roadmap do projeto

## Etapa 0 — Preparação

- [ ] Criar repositório Git.
- [ ] Instalar/validar `uv` e Python.
- [ ] Criar ambiente com `uv sync`.
- [ ] Confirmar a URL do dataset na Aula 1 da DIO.
- [ ] Verificar licença, condições de uso, formato e tamanho do dataset.

**Pronto quando:** o ambiente é reproduzível e a origem dos dados está documentada.

## Etapa 1 — Exploração

- [ ] Criar `notebooks/01_exploracao_e_modelagem.ipynb`.
- [ ] Carregar dados a partir da fonte confirmada.
- [ ] Verificar dimensões, tipos, nulos, duplicatas e estatísticas.
- [ ] Calcular prevalência de fraude e documentar a desproporção.
- [ ] Criar visualizações iniciais.

**Pronto quando:** o notebook executa até o fim e as saídas são verificáveis.

## Etapa 2 — Preparação e baseline

- [ ] Definir split e justificar a estratégia considerando `Time`.
- [ ] Criar baseline de Regressão Logística com pipeline.
- [ ] Calcular métricas da classe fraude.
- [ ] Inspecionar matriz de confusão e curva Precisão-Recall.

## Etapa 3 — Comparação

- [ ] Comparar Regressão Logística, Random Forest e XGBoost.
- [ ] Comparar pesos de classe e, quando apropriado, estratégias de reamostragem.
- [ ] Evitar vazamento: reamostragem apenas no treino.
- [ ] Fazer ajuste de hiperparâmetros com validação.
- [ ] Registrar tempo de treino e trade-offs relevantes.

## Etapa 4 — Limiar e explicabilidade

- [ ] Escolher limiar usando validação e um critério documentado.
- [ ] Comparar precisão/recall em diferentes limiares.
- [ ] Usar SHAP quando compatível com o modelo escolhido.
- [ ] Explicar limites de interpretação das variáveis PCA.

## Etapa 5 — Engenharia e testes

- [ ] Extrair funções estáveis para `src/fraud_detection/`.
- [ ] Adicionar testes unitários.
- [ ] Configurar CI com GitHub Actions.
- [ ] Confirmar que não há dados brutos ou caminhos locais no Git.

## Etapa 6 — Publicação

- [ ] Executar o notebook de cima para baixo.
- [ ] Executar `uv run pytest`.
- [ ] Atualizar README com resultados reais.
- [ ] Incluir gráficos essenciais e conclusões honestas.
- [ ] Conferir arquivos e links citados.
- [ ] Publicar repositório público no GitHub.

## Ideias futuras, após a entrega principal

- [ ] Avaliação temporal mais realista.
- [ ] API de inferência com FastAPI.
- [ ] Monitoramento de drift e qualidade dos dados.
- [ ] Relatório de desempenho e custos de falsos positivos/falsos negativos.
