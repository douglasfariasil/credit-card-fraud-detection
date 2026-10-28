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
