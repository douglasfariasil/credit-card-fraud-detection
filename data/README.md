# Dados

# Fonte dos dados

## Dataset de transações com cartão de crédito

- **Arquivo:** `creditcard.csv`
- **URL oficial utilizada no laboratório:** https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv
- **Origem da referência:** Aula 1 do laboratório de detecção de anomalias em transações da DIO.
- **Método de carregamento:** leitura direta da URL com `pandas.read_csv()`.
- **Armazenamento no Git:** o arquivo bruto não será versionado.

## Colunas esperadas

- `Time`: tempo decorrido entre a primeira transação e a transação registrada, conforme a descrição tradicional dessa base.
- `Amount`: valor da transação.
- `Class`: variável-alvo; `1` representa fraude e `0` representa transação normal.
- `V1` a `V28`: variáveis numéricas transformadas por PCA, conforme a documentação tradicional da base.

## Validações pendentes

Ao carregar os dados, confirmar as colunas, os tipos, a quantidade de registros, os valores ausentes, as duplicatas e a proporção real de cada classe.

**Licença e termos de uso:** verificar as condições aplicáveis à fonte original antes de redistribuir os dados.

**Nota:** a URL é a mesma exibida na aula. A origem histórica e a licença do conjunto original devem ser documentadas separadamente, se identificadas.

