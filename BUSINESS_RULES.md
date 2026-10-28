# Regras de negócio e critérios de avaliação

## Contexto

O problema é classificar transações como legítimas ou fraudulentas. O desafio informa que a classe positiva é rara (aproximadamente 0,17% no conjunto descrito); essa proporção deve ser recalculada no dataset real, não presumida como verdade universal.

## Definição do alvo

- `Class = 1`: fraude, conforme a descrição do desafio.
- `Class = 0`: transação normal.
- Confirmar valores e tipos ao carregar a base. Não inverter a classe positiva sem documentar.

## Por que acurácia não basta

Quando quase todas as transações são normais, prever sempre “normal” pode gerar acurácia alta e recall de fraude igual a zero. Portanto, a acurácia será contextual, nunca a única métrica de seleção.

## Métricas obrigatórias

- **Recall da fraude:** fraudes identificadas / todas as fraudes reais.
- **Precisão da fraude:** fraudes verdadeiras identificadas / todas as transações marcadas como fraude.
- **F1 da fraude:** média harmônica entre precisão e recall.
- **Matriz de confusão:** para explicitar verdadeiros positivos, falsos positivos, verdadeiros negativos e falsos negativos.
- **Curva Precisão-Recall:** especialmente informativa quando a classe positiva é rara.
- **ROC-AUC:** útil como visão complementar, mas não substitui métricas no limiar operacional.

## Trade-offs operacionais

- Falso negativo: fraude não detectada.
- Falso positivo: transação legítima sinalizada como fraude.
- Um limiar menor geralmente aumenta recall e também pode aumentar falsos positivos.
- O projeto não conhece o custo financeiro real de cada erro; não alegar otimização de custo sem definir esses valores.

## Regras contra vazamento

1. Separar os conjuntos antes de ajustar transformações.
2. Ajustar o `StandardScaler` somente no treino, via pipeline.
3. Aplicar reamostragem apenas ao treino, idealmente dentro de `imblearn.pipeline.Pipeline`.
4. Usar validação para comparar modelos e escolher limiar.
5. Usar o teste reservado apenas para a avaliação final.
6. Não selecionar atributos nem ajustar hiperparâmetros olhando repetidamente para o teste.

## Critérios para considerar um experimento completo

- Dataset e fonte identificados.
- Distribuição da classe calculada e registrada.
- Baseline simples incluído.
- Comparação de modelos com as mesmas divisões de dados.
- Precisão, recall e F1 da classe fraude reportados.
- Limiar escolhido com justificativa.
- Limitações e possíveis vieses descritos.
- Resultados reproduzíveis, com sementes e versões registradas.

## Decisão sobre duplicatas — análise exploratória

A base original contém 284.807 linhas, incluindo 492 fraudes. A verificação identificou 1.081 ocorrências repetidas após a primeira ocorrência e 1.854 linhas pertencentes a grupos de duplicatas exatas.

Ao remover as ocorrências repetidas, o conjunto passa a conter 283.726 linhas e 473 fraudes. Portanto, 19 fraudes seriam removidas, equivalentes a aproximadamente 3,86% dos casos fraudulentos originais.

A inspeção não encontrou grupos com atributos idênticos e rótulos conflitantes.

**Decisão inicial:** manter a base original como cenário principal. A remoção de duplicatas será tratada como análise de sensibilidade, pois não há evidência suficiente para afirmar que todas as ocorrências repetidas sejam erros.

**Cuidados:** preservar os dados brutos, evitar vazamento entre conjuntos e documentar a estratégia de divisão antes de treinar modelos.

**Status:** decisão inicial, sujeita a revisão após a avaliação experimental.


### Regra experimental para seleção do limiar

**Objetivo:** reduzir o volume de alertas sem deixar o recall de fraude abaixo da meta definida para o experimento.

- Meta inicial de recall: pelo menos 85% na validação.
- Critério de desempate: minimizar o total de alertas.
- Modelo avaliado: regressão logística com `class_weight="balanced"`.
- Resultado observado: o limiar 0,95 atende à meta e gera 166 alertas, detectando 64 das 75 fraudes na validação.
- Limitação: essa meta é uma hipótese experimental, não um requisito validado com uma instituição financeira.
- Controle de avaliação: o conjunto de teste permanece reservado até que o modelo e o limiar sejam definidos.

A escolha será reavaliada após a comparação com outros modelos e a análise dos custos de falsos positivos e falsos negativos.


### Seleção do limiar — Regressão Logística

**Regra experimental:** manter recall de fraude de pelo menos 85% na validação e minimizar o número total de alertas entre os limiares elegíveis.

**Resultado:** limiar candidato de 0,95.

- Recall: 85,33%.
- Precisão: 38,55%.
- Fraudes detectadas: 64 de 75.
- Fraudes perdidas: 11.
- Falsos positivos: 102.
- Total de alertas: 166.

**Limitação:** a meta de recall é uma hipótese experimental para o portfólio. O limiar deverá ser avaliado em conjunto com outros modelos e, posteriormente, no conjunto de teste reservado.

A seleção não deve ser interpretada como uma política operacional validada para uma instituição financeira.


## Conclusão e limitações

O Random Forest foi selecionado como modelo candidato principal após comparação com a Regressão Logística. A escolha considerou a Average Precision e a quantidade de alertas gerados sob uma regra experimental de recall mínimo de 85%.

O limiar de classificação de 0,15 foi escolhido usando exclusivamente o conjunto de validação. No conjunto de teste separado, o modelo obteve:

- **Precisão para fraudes:** 68,42%
- **Recall para fraudes:** 89,04%
- **F1-score para fraudes:** 0,7738
- **Average Precision:** 0,8708
- **ROC-AUC:** 0,9614

Das 73 fraudes presentes no conjunto de teste, 65 foram detectadas e 8 não foram identificadas. O modelo gerou 95 alertas, incluindo 30 falsos positivos.

Os resultados são promissores para um experimento de classificação com classes altamente desbalanceadas. Entretanto, o limiar adotado é uma decisão experimental, não uma regra validada para uma operação financeira real.

### Limitações e próximos passos

- Avaliar a estabilidade das métricas com diferentes partições ou validação cruzada apropriada.
- Investigar o impacto de falsos positivos e fraudes perdidas considerando custos operacionais.
- Avaliar a calibração das probabilidades antes de interpretá-las como riscos reais.
- Verificar o desempenho com dados temporalmente posteriores e representativos de uma operação real.
- Desenvolver testes automatizados, uma API de inferência e monitoramento antes de considerar qualquer implantação operacional.

Este projeto tem finalidade educacional e demonstrativa. Os resultados não garantem desempenho equivalente em dados reais de instituições financeiras.
