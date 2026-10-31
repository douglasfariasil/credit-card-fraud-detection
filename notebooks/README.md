# Notebooks

Este diretório contém os notebooks utilizados na exploração dos dados, experimentação e análise dos modelos do projeto de detecção de fraudes em cartões de crédito.

## Notebook disponível

### `01_exploracao_e_modelagem.ipynb`

Notebook principal do projeto. Documenta o processo experimental de detecção de transações fraudulentas, incluindo:

1. Contextualização do problema e objetivo.
2. Importação das bibliotecas e configuração do experimento.
3. Carregamento e validação dos dados.
4. Análise exploratória e distribuição das classes.
5. Separação dos dados para treinamento, validação e teste.
6. Treinamento e avaliação dos modelos.
7. Análise das métricas e seleção do limiar de decisão usando validação.
8. Avaliação final no conjunto de teste.
9. Persistência do modelo e configuração de inferência.
10. Conclusões, limitações e próximos passos.

## Relação entre notebook e pacote Python

O notebook é responsável pela exploração, experimentação e apresentação dos resultados.

As funcionalidades reutilizáveis e testáveis ficam no pacote `src/fraud_detection/`, organizado em módulos de:

- `data`: carregamento e validação dos dados.
- `models`: treinamento, persistência e inferência.
- `evaluation`: métricas e seleção do limiar.
- `features`: espaço reservado para funcionalidades futuras de engenharia de atributos.

Essa separação evita concentrar toda a lógica do projeto no notebook e facilita a manutenção, os testes automatizados e uma futura integração com uma API.

## Resultados experimentais

O experimento final com Random Forest selecionou o limiar de decisão `0.15`, utilizando o conjunto de validação.

No conjunto de teste, foram obtidos:

- Precision para fraudes: 68,42%.
- Recall para fraudes: 89,04%.
- F1-score para fraudes: 0,7738.
- Average Precision: 0,8708.
- ROC-AUC: 0,9614.

O conjunto de teste foi reservado para a avaliação final, sem ser utilizado na seleção do limiar.

Os resultados completos e as regras de negócio estão documentados em `BUSINESS_RULES.md` e `README.md`.

## Execução

Na raiz do projeto, ative o ambiente e inicie o JupyterLab:

```bash
uv sync
uv run jupyter lab
```

Abra `01_exploracao_e_modelagem.ipynb` e execute as células na ordem apresentada.

O arquivo de dados original não é versionado. Consulte `data/README.md` para as instruções de obtenção e posicionamento do dataset.

## Boas práticas

- Execute as células em ordem.
- Não utilize o conjunto de teste para escolher modelos ou limiares.
- Não registre métricas que não tenham sido efetivamente calculadas.
- Mantenha a lógica reutilizável no pacote Python, sempre que apropriado.
- Atualize a documentação quando os experimentos ou resultados forem alterados.
