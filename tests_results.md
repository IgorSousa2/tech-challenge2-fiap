# Testes Realizados e Observações

## Objetivo

Este documento tem como finalidade registrar os testes realizados durante o desenvolvimento do projeto, os resultados obtidos e observações relevantes sobre o comportamento dos modelos e do algoritmo genético.

---

# Testes Realizados - Otimização por Algoritmo Genético

## Teste 1

### Configuração

| Parâmetro | Valor |
|-----------|-------|
| Modelo otimizado | Random Forest |
| Tamanho da população | 100 |
| Número de gerações | 10 |
| Probabilidade de mutação | 0.5 (50%) |
| Método de seleção | Torneio |

### Resultado

**Melhores hiperparâmetros encontrados**

```text
{'rf_n_estimators': 50, 'rf_max_depth': 5, 'rf_min_samples_split': 10, 'rf_min_samples_leaf': 2, 'rf_max_features': None}
```

**Resultado do terminal**

```text
Generation 0: Best fitness = 0.9471620227038183
Generation 1: Best fitness = 0.9471620227038183
Generation 2: Best fitness = 0.9483488132094944
Generation 3: Best fitness = 0.9483488132094944
Generation 4: Best fitness = 0.9483488132094944
Generation 5: Best fitness = 0.9489164086687305
Generation 6: Best fitness = 0.9489164086687305
Generation 7: Best fitness = 0.9489164086687305
Generation 8: Best fitness = 0.9489164086687305
Generation 9: Best fitness = 0.9489164086687305
```

**Comparação**

| Situação | Recall Macro |
|----------|--------------|
| Antes da otimização | 0.9353973168214654 |
| Após a otimização | 0.9489164086687305 |

**Observações**

```text
O modelo Random Forest foi o primeiro que utilizei para realizar os testes. Por mais que eu tenha setado o hiperparâmetro n_jobs=-1 para destinar todos os núcleos da minha máquina para o treinamento, ele ainda é bem demorado. Alterei o modo de seleção que utilizei antes (de truncamento para torneio) para que tivéssemos uma variabilidade maior na seleção dos pais. 
```

## Teste 2

### Configuração

| Parâmetro | Valor |
|-----------|-------|
| Modelo otimizado | SVM |
| Tamanho da população | 100 |
| Número de gerações | 10 |
| Probabilidade de mutação | 0.5 (50%) |
| Método de seleção | Torneio |

### Resultado

**Melhores hiperparâmetros encontrados**

```text
{'svm_C': 100, 'svm_max_iter': 2000, 'svm_tol': 0.0001}
```

**Resultado do terminal**

```text
Generation 0: Best fitness = 0.9395252837977296
Generation 1: Best fitness = 0.9395252837977296
Generation 2: Best fitness = 0.9395252837977296
Generation 3: Best fitness = 0.9395252837977296
Generation 4: Best fitness = 0.9395252837977296
Generation 5: Best fitness = 0.9395252837977296
Generation 6: Best fitness = 0.9395252837977296
Generation 7: Best fitness = 0.9395252837977296
Generation 8: Best fitness = 0.9395252837977296
Generation 9: Best fitness = 0.9395252837977296
```

**Comparação**

| Situação | Recall Macro |
|----------|--------------|
| Antes da otimização | 0.9318885448916407 |
| Após a otimização | 0.9395252837977296 |

**Observações**

```text
Em seguida, apliquei as mesmas configurações de população e gerações para o modelo SVM, e a diferença de velocidade de cálculo de fitness foi gritante (terminou as 10 gerações em menos de 30 segundos, quanto o RF foi mais de 10 minutos), porém convergiu no resultado máximo de recall na primeira geração. Acredito que, por utilizar o modelo LinearSVC, que tem um treinamento propositalmente mais rápido, pode significar que os hiperparâmetros não impactem tanto no resultado final e isso explica a rápida convergência.
```

## Teste 3

### Configuração

| Parâmetro | Valor |
|-----------|-------|
| Modelo otimizado | KNN |
| Tamanho da população | 100 |
| Número de gerações | 10 |
| Probabilidade de mutação | 0.5 (50%) |
| Método de seleção | Torneio |

### Resultado

**Melhores hiperparâmetros encontrados**

```text
{'knn_neighbors': 15, 'knn_weights': 'uniform', 'knn_metric': 'cosine', 'knn_p': 3}
```

**Resultado do terminal**

```text
Generation 0: Best fitness = 0.9460268317853456
Generation 1: Best fitness = 0.9460268317853456
Generation 2: Best fitness = 0.9460268317853456
Generation 3: Best fitness = 0.9460268317853456
Generation 4: Best fitness = 0.9460268317853456
Generation 5: Best fitness = 0.9460268317853456
Generation 6: Best fitness = 0.9460268317853456
Generation 7: Best fitness = 0.9460268317853456
Generation 8: Best fitness = 0.9460268317853456
Generation 9: Best fitness = 0.9460268317853456
```

**Comparação**

| Situação | Recall Macro |
|----------|--------------|
| Antes da otimização | 0.9406604747162023 |
| Após a otimização | 0.9460268317853456 |

**Observações**

```text
No modelo KNN, segui com as mesmas configurações. Ele atingiu um resultado melhor com os hiperparâmetros otimizados - igual nos outros testes - porém é interessante notar que no tech-challenge anterior utilizei o GridSearch para validar as melhores opções por força bruta, e a diferença de lá para o algoritmo genético foi apenas a quantidade de vizinhos. Acredito que um dataset mais robusto faria uma diferença maior no treinamento, tendo uma versão mais definitiva de quais seriam os verdadeiros hiperparâmetros otimizados.
```

## Teste 4

### Configuração

| Parâmetro | Valor |
|-----------|-------|
| Modelo otimizado | Random Forest |
| Tamanho da população | 50 |
| Número de gerações | 15 |
| Probabilidade de mutação | 0.5 (50%) |
| Método de seleção | Torneio |

### Resultado

**Melhores hiperparâmetros encontrados**

```text
{'rf_n_estimators': 50, 'rf_max_depth': 20, 'rf_min_samples_split': 10, 'rf_min_samples_leaf': 2, 'rf_max_features': None}
```

**Resultado do terminal**

```text
Generation 0: Best fitness = 0.9459752321981423
Generation 1: Best fitness = 0.9489164086687305
Generation 2: Best fitness = 0.9489164086687305
Generation 3: Best fitness = 0.9489164086687305
Generation 4: Best fitness = 0.9489164086687305
Generation 5: Best fitness = 0.9489164086687305
Generation 6: Best fitness = 0.9489164086687305
Generation 7: Best fitness = 0.9489164086687305
Generation 8: Best fitness = 0.9489164086687305
Generation 9: Best fitness = 0.9489164086687305
Generation 10: Best fitness = 0.9489164086687305
Generation 11: Best fitness = 0.9489164086687305
Generation 12: Best fitness = 0.9489164086687305
Generation 13: Best fitness = 0.9489164086687305
Generation 14: Best fitness = 0.9489164086687305
```

**Comparação**

| Situação | Recall Macro |
|----------|--------------|
| Antes da otimização | 0.9353973168214654 |
| Após a otimização | 0.9489164086687305 |

**Observações**

```text
Decidi testar o Random Forest novamente, com uma mudança na população e no número de gerações, para verificar se teríamos uma redução de tempo de treinamento e se os testes resultariam em hiperparâmetros parecidos com os da primeira vez. O resultado foi surpreendente: ele retornou uma taxa de recall idêntica, só que com uma convergência muito mais rápida (já na segunda geração) e com uma única diferença de valor no hiperparâmetro rf_max_depth.
```

## Teste 5

### Configuração

| Parâmetro | Valor |
|-----------|-------|
| Modelo otimizado | Random Forest |
| Tamanho da população | 100 |
| Número de gerações | 10 |
| Probabilidade de mutação | 0.7 (70%) |
| Método de seleção | Truncamento |

### Resultado

**Melhores hiperparâmetros encontrados**

```text
{'rf_n_estimators': 300, 'rf_max_depth': None, 'rf_min_samples_split': 10, 'rf_min_samples_leaf': 1, 'rf_max_features': 'sqrt'}
```

**Resultado do terminal**

```text
Generation 0: Best fitness = 0.9471620227038183
Generation 1: Best fitness = 0.9483488132094944
Generation 2: Best fitness = 0.9483488132094944
Generation 3: Best fitness = 0.9483488132094944
Generation 4: Best fitness = 0.9483488132094944
Generation 5: Best fitness = 0.9483488132094944
Generation 6: Best fitness = 0.9483488132094944
Generation 7: Best fitness = 0.9483488132094944
Generation 8: Best fitness = 0.9483488132094944
Generation 9: Best fitness = 0.9483488132094944
```

**Comparação**

| Situação | Recall Macro |
|----------|--------------|
| Antes da otimização | 0.9353973168214654 |
| Após a otimização | 0.9483488132094944 |

**Observações**

```text
Realizei um último teste com o modelo RF mas alterando principalmente a taxa de mutação e o método de seleção (aumentando também a população para 100 novamente) e chegamos num resultado diferente das outras duas vezes. O recall atingiu uma convergência já na segunda geração, porém com um valor inferior ao das outras duas vezes, e também tendo um resultado diferente de hiperparâmetros. Pode ser que a métrica atingisse um valor maior com mais gerações, mas creio que o principal agravante nesse resultado tenha sido a taxa de mutação.
```

---

# Testes Realizados — Assistente Inteligente (LLM)

## Teste 1 - Predição utilizando o modelo exportado

### Dados de entrada

| Variável | Valor |
|----------|-------|
| concave_points_mean | 0.04781 |
| radius_worst | 15.11 |
| perimeter_worst | 99.7 |
| concave_points_worst | 0.1288 |

### Resultado esperado

```text
Diagnóstico benigno.
```

### Resultado obtido

```text
Com base nos dados fornecidos e no modelo de aprendizado de máquina, o diagnóstico previsto é benigno (B). No entanto, é importante ressaltar que a decisão final deve ser sempre tomada por um médico, que irá considerar não apenas o resultado do modelo, mas também outros fatores clínicos e de exames. É essencial que um profissional de saúde avalie o paciente de forma global para estabelecer o diagnóstico correto e definir o melhor plano de tratamento, se necessário.
```

### Prompt utilizado

```text
Tendo os seguintes dados: {concave_points_mean: 0.04781, radius_worst: 15.11,perimeter_worst: 99.7,concave_points_worst: 0.1288}, preveja se é um diagnóstico maligno ou benigno.
```

## Teste 2 - Predição utilizando o modelo exportado

### Dados de entrada

| Variável | Valor |
|----------|-------|
| concave_points_mean | 0.1471 |
| radius_worst | 25.38 |
| perimeter_worst | 184.6 |
| concave_points_worst | 0.2654 |

### Resultado esperado

```text
Diagnóstico maligno.
```

### Resultado obtido

```text
Com base nos dados fornecidos e no modelo de aprendizado de máquina, a previsão é de que o diagnóstico seja maligno (M). É importante ressaltar que essa é uma previsão baseada em dados e deve ser interpretada por um profissional de saúde qualificado. Recomenda-se procurar um médico para uma avaliação clínica e exames adicionais para um diagnóstico preciso e um plano de tratamento adequado.
```

### Prompt utilizado

```text
Tendo os seguintes dados: {concave_points_mean: 0.1471, radius_worst: 25.38,perimeter_worst: 184.6,concave_points_worst: 0.2654}, preveja se é um diagnóstico maligno ou benigno.
```

## Teste 3 — Explicação da métrica utilizada em linguagem natural


### Prompt utilizado

```text
Qual a métrica e seu valor no treinamento do modelo?
```

### Resposta obtida

```text
A métrica utilizada para avaliar o desempenho do modelo de aprendizado de máquina foi o recall, e o valor obtido durante o treinamento foi de aproximadamente 0.949. O recall mede a capacidade do modelo em identificar corretamente os casos positivos, ou seja, a proporção de verdadeiros positivos em relação a todos os exemplos que realmente são positivos. Um valor alto de recall indica que o modelo é capaz de identificar a maioria dos casos positivos de forma correta.
```

## Teste 4 — Explicação de como foi feito o treinamento do modelo para médicos


### Prompt utilizado

```text
Explique quais métricas o modelo usa para diagnosticar os pacientes.
```

### Resposta obtida

```text
O modelo utiliza a métrica de Recall Macro para diagnosticar os pacientes. O recall é a capacidade do modelo em identificar corretamente os casos positivos. No caso do Recall Macro, ele calcula a média do recall para cada classe, sendo uma medida útil para avaliar modelos em conjuntos de dados desbalanceados. 

O objetivo do modelo é auxiliar na classificação de tumores benignos (B) e malignos (M) da base de dados Breast Cancer Wisconsin. Ele faz previsões com base nos parâmetros fornecidos, como concave_points_mean, radius_worst, perimeter_worst e concave_points_worst.

É importante ressaltar que o modelo é uma ferramenta de apoio à decisão e não deve substituir a avaliação médica. A interpretação dos resultados e a decisão final devem sempre ser feitas por um médico, considerando não apenas as previsões do modelo, mas também outras informações clínicas relevantes.
```

### Observações

Um disclaimer que foi definido nas funções dentro o arquivo agent-llm.py: sempre importante mencionar que o resultado final tem que ser feito por um médico. A ferramenta serve de APOIO À DECISÃO, não de diagnóstico definitivo.

---

# Observações Extras

## Sobre o Algoritmo Genético

Notei que o algoritmo genético desenvolvido acaba atingindo uma convergência muito cedo na maioria dos testes, seja alterando a população, alterando a quantidade de gerações, o método de seleção, aplicando ou não o elitismo. Isso pode ser devido a pouca variedade de valores dos hiperparâmetros e/ou o dataset ter poucos dados, o que acaba influenciando na facilidade de achar o melhor indivíduo de cada geração. Inicialmente, validei com prints durante o fluxo todos os indivíduos para verificar se o método de geração aleatória de população estava funcionando, e realmente estava. Alguns hiperparâmetros que selecionei não impactavam tanto na melhora do recall, mas podem melhorar em outras métricas e podem ser úteis se formos aplicar em outros datasets, então é um ponto válido. Mas fiquei satisfeito que todos os resultados tiveram um valor de recall aumentado se comparado ao valor sem otimização. No código, deixei o método de seleção por truncamento comentado e segui pelo de torneio, visto que é possível selecionar (numa população de 100) qualquer indivíduo, permitindo uma variação maior de pais e, consequentemente, genes. Testei também os modelos sem a técnica de elitismo, mas não teve mudança significativa nos resultados.

---

## Sobre o Assistente LLM

Notei que o assistente possui bastante variedade de interpretações que podem apontar para as funções designadas. Coloquei duas que possuem uma dinâmica parecida propositalmente, para ver se o modelo conseguiria identificar diferenças mínimas e direcionar as explicações corretamente. O resultado foi positivo, por mais que algumas vezes ele tenha se perdido no prompt e caído na exceção. 

---