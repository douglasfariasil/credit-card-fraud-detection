# AGENTS.md — Regras de trabalho do projeto

Este arquivo orienta pessoas e agentes de programação que contribuam para o repositório.

## Missão

Construir um projeto educacional, reproduzível e bem documentado de detecção de fraude em transações com cartão, priorizando aprendizado, avaliação honesta e explicabilidade.

## Antes de alterar código

1. Leia `README.md`, `ARCHITECTURE.md`, `BUSINESS_RULES.md` e `ROADMAP.md`.
2. Confira o estado do Git e preserve mudanças existentes.
3. Identifique a etapa atual do roadmap; não implemente etapas futuras sem necessidade.
4. Não invente a origem, licença, significado das variáveis ou resultados do dataset. Marque informações pendentes como pendentes.

## Regras de implementação

- Use Python com type hints em funções reutilizáveis.
- Prefira funções pequenas, nomes claros e responsabilidade única.
- Mantenha a lógica reutilizável em `src/fraud_detection/`; use notebooks para exploração, narrativa e visualizações.
- Evite duplicar lógica entre notebook e pacote.
- Use `pathlib` para caminhos e parâmetros/configuração explícitos.
- Defina sementes aleatórias quando houver aleatoriedade e registre-as.
- Não codifique caminhos absolutos específicos da máquina.
- Não esconda erros com `except` genérico.
- Não faça downloads de dados automaticamente sem informar a origem e validar o arquivo.
- Não inclua credenciais, dados sensíveis ou dataset bruto no Git.

## Regras de machine learning

- Faça o split antes de ajustar transformações ou balanceamento.
- Ajuste scaler, imputadores, seleção de atributos e outras transformações apenas nos dados de treino, preferencialmente dentro de `Pipeline`.
- Aplique undersampling/oversampling somente ao treino; nunca balanceie validação ou teste.
- Se usar SMOTE, avalie se faz sentido para os atributos e para a distribuição dos dados.
- Evite vazamento de dados. Se `Time` representar ordem temporal relevante, documente por que um split aleatório estratificado é ou não adequado.
- Use validação para escolher modelo e limiar. Preserve o teste para a avaliação final.
- Reporte precisão, recall e F1 especificamente para a classe fraude, além da matriz de confusão e curvas relevantes.
- Não declare um modelo “melhor” com base apenas em acurácia ou em uma única métrica.
- Documente trade-offs: falsos positivos, falsos negativos, custo computacional e limitações.
- Explique o significado do limiar escolhido e não trate 0,5 como obrigatório.
- SHAP e importância de atributos devem ser interpretados como explicações do modelo, não como causalidade.

## Qualidade e testes

- Rode `uv run pytest` após mudanças de código.
- Rode o notebook de cima para baixo antes de publicar resultados.
- Não invente saídas, métricas, gráficos ou evidências de execução.
- Atualize a documentação quando uma decisão de arquitetura ou negócio mudar.
- Mantenha dependências declaradas no `pyproject.toml` e o `uv.lock` sincronizado.

## Estilo de colaboração

- Explique o propósito e o raciocínio antes de introduzir conceitos novos.
- Prefira passos pequenos que o usuário consiga executar e verificar.
- Ao sugerir comandos, indique a pasta em que devem ser executados.
- Não diga que algo foi executado localmente se não foi.
