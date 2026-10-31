# Regras de negócio e critérios de avaliação

## 1. Contexto

O objetivo do projeto é classificar transações financeiras como legítimas ou fraudulentas.

O principal desafio é o desbalanceamento entre as classes: a quantidade de transações fraudulentas é muito menor que a de transações normais. O conjunto de dados descrito no desafio apresenta aproximadamente 0,17% de fraudes. Essa proporção deve ser calculada no dataset efetivamente utilizado, não presumida como uma característica universal.

## 2. Definição do alvo

- `Class = 1`: transação fraudulenta.
- `Class = 0`: transação normal.
- Confirmar os valores e tipos da variável-alvo durante o carregamento dos dados.
- Não inverter a classe positiva sem documentar a decisão.

## 3. Por que acurácia não basta

Em um conjunto altamente desbalanceado, um modelo pode prever todas as transações como normais e ainda apresentar uma acurácia elevada, mesmo sem identificar nenhuma fraude.

Por isso, a acurácia será utilizada apenas como informação complementar, nunca como único critério de seleção do modelo.

## 4. Métricas de avaliação

As seguintes métricas devem orientar a avaliação:

- **Recall da fraude:** proporção de fraudes reais identificadas pelo modelo.
- **Precisão da fraude:** proporção de alertas de fraude que realmente correspondem a fraudes.
- **F1-score da fraude:** média harmônica entre precisão e recall.
- **Matriz de confusão:** permite identificar verdadeiros positivos, falsos positivos, verdadeiros negativos e falsos negativos.
- **Average Precision e curva Precisão-Recall:** importantes para avaliar modelos em problemas com classe positiva rara.
- **ROC-AUC:** métrica complementar para avaliar a capacidade de discriminação do modelo.

As métricas devem ser interpretadas em conjunto. Nenhuma delas, isoladamente, representa a qualidade operacional de um sistema antifraude.

## 5. Trade-offs operacionais

- **Falso negativo:** uma fraude real não é identificada.
- **Falso positivo:** uma transação legítima é sinalizada como suspeita.
- Um limiar de classificação menor tende a aumentar o recall, mas também pode aumentar a quantidade de falsos positivos.
- Um limiar maior tende a reduzir os alertas, mas pode deixar mais fraudes sem identificação.

O projeto não possui informações sobre os custos financeiros reais de cada tipo de erro. Portanto, não deve afirmar que o modelo minimiza custos financeiros ou representa uma política operacional validada.

## 6. Regras contra vazamento de dados

1. Separar treino, validação e teste antes de ajustar transformações ou treinar modelos.
2. Quando houver transformações que aprendam parâmetros dos dados, ajustá-las somente com o conjunto de treino.
3. Se houver reamostragem, aplicá-la somente ao treino, preferencialmente dentro de um pipeline apropriado.
4. Utilizar validação para comparar modelos e selecionar o limiar de classificação.
5. Manter o conjunto de teste reservado para a avaliação final.
6. Não selecionar atributos nem ajustar hiperparâmetros consultando repetidamente os resultados do teste.
7. Preservar a separação entre as etapas experimentais e a avaliação final.

## 7. Critérios para considerar um experimento completo

Um experimento deve apresentar:

- Dataset e fonte identificados.
- Distribuição das classes calculada.
- Baseline documentado.
- Comparação de modelos com divisões de dados consistentes.
- Precisão, recall e F1-score da classe fraude.
- Métricas complementares adequadas ao desbalanceamento.
- Limiar escolhido com justificativa.
- Limitações e possíveis vieses descritos.
- Resultados reproduzíveis, com sementes e versões das dependências registradas.

## 8. Decisão sobre duplicatas — análise exploratória

A base original contém 284.807 linhas, incluindo 492 fraudes.

A análise identificou:

- 1.081 ocorrências repetidas após a primeira ocorrência.
- 1.854 linhas pertencentes a grupos de duplicatas exatas.
- Nenhum grupo identificado com atributos idênticos e rótulos conflitantes.

Ao remover as ocorrências repetidas, o conjunto passa a conter 283.726 linhas e 473 fraudes. Isso representa a remoção de 19 fraudes, aproximadamente 3,86% dos casos fraudulentos originais.

**Decisão:** manter a base original como cenário principal. A remoção de duplicatas será tratada como análise de sensibilidade, pois não há evidência suficiente para afirmar que todas as ocorrências repetidas sejam erros.

**Cuidados:**
- Preservar os dados brutos.
- Evitar vazamento entre os conjuntos.
- Documentar a estratégia de divisão antes do treinamento.
- Não interpretar duplicatas automaticamente como registros inválidos.

**Status:** decisão experimental inicial, sujeita a revisão.

## 9. Histórico experimental — Regressão Logística

A Regressão Logística foi utilizada como modelo de referência na comparação experimental.

A regra adotada para a seleção do limiar foi manter recall de fraude de pelo menos 85% na validação e minimizar o número total de alertas entre os limiares elegíveis.

**Resultado observado na validação:**

- Modelo: Regressão Logística com `class_weight="balanced"`.
- Limiar candidato: 0,95.
- Recall: 85,33%.
- Precisão: 38,55%.
- Fraudes detectadas: 64 de 75.
- Fraudes não identificadas: 11.
- Falsos positivos: 102.
- Total de alertas: 166.

Esse resultado pertence a um experimento anterior e deve ser interpretado como referência histórica para a comparação com outros modelos.

A meta de recall de 85% é uma hipótese experimental para o portfólio, não um requisito validado com uma instituição financeira.

O conjunto de teste permaneceu reservado para a avaliação final.

## 10. Seleção do modelo e do limiar final — Random Forest

Após a comparação experimental com a Regressão Logística, o Random Forest foi selecionado como modelo candidato principal.

A decisão considerou a Average Precision e a quantidade de alertas gerados sob a regra experimental de recall mínimo de 85%.

O limiar de classificação escolhido foi **0,15**, utilizando exclusivamente o conjunto de validação.

A escolha buscou atender à meta experimental de recall e minimizar o volume de alertas entre os limiares avaliados.

### Avaliação final no conjunto de teste

O modelo foi avaliado no conjunto de teste separado, sem utilizar esse conjunto para escolher o limiar.

| Métrica | Resultado |
|---|---:|
| Precisão da fraude | 68,42% |
| Recall da fraude | 89,04% |
| F1-score da fraude | 0,7738 |
| Average Precision | 0,8708 |
| ROC-AUC | 0,9614 |
| Limiar utilizado | 0,15 |

### Resultado operacional observado no teste

Das 42.720 transações avaliadas:

- Fraudes reais: 73.
- Fraudes detectadas: 65.
- Fraudes não identificadas: 8.
- Falsos positivos: 30.
- Total de alertas: 95.
- Transações classificadas como normais: 42.625.

Matriz de confusão:

| | Previsto normal | Previsto fraude |
|---|---:|---:|
| Real normal | 42.617 | 30 |
| Real fraude | 8 | 65 |

Os resultados demonstram o comportamento do modelo nesse conjunto de teste específico. Não garantem desempenho equivalente em outros períodos, bases de dados ou instituições financeiras.

## 11. Limitações e próximos passos

O projeto tem finalidade educacional e demonstrativa. O modelo ainda não representa um sistema antifraude pronto para produção.

Pontos que podem evoluir:

- Avaliar a estabilidade das métricas com diferentes partições ou validação cruzada apropriada.
- Investigar o impacto financeiro e operacional dos falsos positivos e falsos negativos.
- Avaliar a calibração das probabilidades antes de interpretá-las como riscos reais.
- Verificar o desempenho com dados temporalmente posteriores e representativos de uma operação real.
- Desenvolver uma API de inferência.
- Implementar monitoramento de desempenho e mudanças na distribuição dos dados.
- Avaliar requisitos adicionais de segurança, disponibilidade e rastreabilidade antes de qualquer implantação operacional.

**Status de engenharia:** o projeto já possui módulos reutilizáveis para carregamento, treinamento, avaliação, persistência e inferência, além de testes automatizados para validar o fluxo de treinamento, persistência e inferência. A API e o monitoramento permanecem como etapas futuras.

**Conclusão:** o Random Forest, com limiar de 0,15, é o modelo candidato selecionado neste experimento. Sua avaliação final apresentou recall de 89,04% e precisão de 68,42% para a classe fraude no conjunto de teste. A decisão é experimental e não deve ser interpretada como uma política financeira validada.
