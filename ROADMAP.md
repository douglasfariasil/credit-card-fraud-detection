# Roadmap do projeto

Legenda:
- [x] Concluído e validado.
- [ ] Pendente ou aguardando verificação.

## Etapa 0 — Preparação

- [x] Criar repositório Git.
- [x] Instalar e validar `uv` e Python.
- [x] Criar ambiente com `uv sync`.
- [x] Documentar a origem e a URL de referência do dataset.
- [ ] Verificar licença e condições de uso e redistribuição do dataset.

**Status:** ambiente configurado e origem documentada. A verificação da licença ainda está pendente.

## Etapa 1 — Exploração

- [x] Criar `notebooks/01_exploracao_e_modelagem.ipynb`.
- [x] Carregar dados a partir da fonte documentada.
- [x] Verificar dimensões, tipos, valores ausentes, duplicatas e estatísticas.
- [x] Calcular prevalência de fraude e analisar o desbalanceamento.
- [x] Criar visualizações exploratórias.
- [ ] Executar novamente o notebook completo, de cima para baixo, para validar a reprodução final.

**Status:** exploração e análise implementadas. A execução completa precisa ser confirmada na revisão final.

## Etapa 2 — Preparação e baseline

- [x] Definir os conjuntos de treino, validação e teste.
- [x] Implementar baseline de Regressão Logística.
- [x] Calcular métricas da classe fraude.
- [x] Inspecionar matriz de confusão e curva Precisão-Recall.
- [ ] Documentar de forma explícita as limitações da estratégia de divisão em relação à variável `Time`.

**Status:** baseline e avaliação implementados. A estratégia temporal merece documentação adicional.

## Etapa 3 — Comparação de modelos

- [x] Comparar Regressão Logística e Random Forest.
- [x] Avaliar o tratamento do desbalanceamento com pesos de classe.
- [x] Preservar a separação entre treino, validação e teste.
- [x] Comparar métricas e volume de alertas.
- [ ] Registrar e comparar sistematicamente o tempo de treinamento.
- [ ] Avaliar XGBoost como experimento adicional, caso agregue valor à comparação.

**Status:** comparação principal concluída com dois modelos. XGBoost não faz parte do escopo mínimo da primeira entrega.

## Etapa 4 — Limiar e explicabilidade

- [x] Escolher o limiar usando exclusivamente a validação.
- [x] Documentar o critério experimental de recall mínimo de 85%.
- [x] Comparar o comportamento de diferentes limiares.
- [x] Registrar os resultados finais do Random Forest no conjunto de teste.
- [x] Documentar limitações das variáveis e da interpretação dos resultados.
- [ ] Avaliar SHAP como recurso adicional de explicabilidade.

**Status:** seleção do limiar e avaliação final concluídas. SHAP permanece como melhoria opcional.

## Etapa 5 — Engenharia e testes

- [x] Extrair funções reutilizáveis para `src/fraud_detection/`.
- [x] Implementar módulos de carregamento, treinamento, avaliação, persistência e inferência.
- [x] Adicionar testes automatizados.
- [x] Criar teste de integração do fluxo de treinamento, persistência e inferência.
- [x] Validar a suíte de testes: 59 testes aprovados.
- [x] Validar qualidade do código com Ruff.
- [x] Configurar workflow de CI com GitHub Actions.
- [ ] Revisar a execução do workflow de CI no GitHub.
- [ ] Confirmar que dados brutos, modelos gerados e caminhos locais não serão publicados indevidamente.

**Status:** implementação e testes locais concluídos. CI remoto e revisão final dos arquivos pendentes.

## Etapa 6 — Publicação e entrega

- [ ] Executar o notebook completo de cima para baixo.
- [x] Executar testes automatizados localmente.
- [x] Executar Ruff localmente.
- [x] Atualizar README com arquitetura e resultados experimentais.
- [x] Atualizar ARCHITECTURE.md.
- [x] Atualizar BUSINESS_RULES.md.
- [ ] Atualizar notebooks/README.md para refletir o notebook existente.
- [ ] Incluir ou revisar os gráficos essenciais no README.
- [ ] Conferir arquivos, links e referências.
- [ ] Revisar `git status` e o diff completo.
- [ ] Confirmar a configuração do repositório remoto.
- [ ] Publicar a versão final no GitHub.
- [ ] Preparar a descrição e os materiais para entrega à DIO.

**Status:** documentação principal revisada. Revisão final, publicação e entrega ainda pendentes.

## Melhorias futuras — Após a primeira entrega

- [ ] Avaliação temporal mais realista.
- [ ] API de inferência com FastAPI.
- [ ] Monitoramento de drift e qualidade dos dados.
- [ ] Avaliação de calibração das probabilidades.
- [ ] Análise de custos de falsos positivos e falsos negativos.
- [ ] Avaliação adicional com XGBoost e SHAP, se justificável.
- [ ] Melhorias de segurança, disponibilidade e rastreabilidade.

## Critério de conclusão do projeto

A primeira versão será considerada pronta para apresentação quando:

1. O notebook executar integralmente.
2. Os testes automatizados passarem.
3. O Ruff não apresentar problemas.
4. A documentação corresponder ao código implementado.
5. A origem e as condições de uso dos dados estiverem documentadas.
6. Não houver dados sensíveis, arquivos locais ou artefatos indevidos no repositório.
7. O projeto estiver publicado e acessível no GitHub.

A conclusão desta primeira versão não significa que o projeto esteja pronto para produção. Significa que existe uma implementação educacional reproduzível, testada, documentada e adequada para demonstrar competências de engenharia de dados e Machine Learning.
