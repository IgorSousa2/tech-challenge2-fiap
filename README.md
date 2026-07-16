# Assistente Inteligente para Apoio ao Diagnóstico de Câncer de Mama

## Descrição

Este projeto implementa um sistema de apoio ao diagnóstico de câncer de mama utilizando técnicas de Aprendizado de Máquina, Otimização por Algoritmo Genético e um Assistente baseado em LLM.

O sistema possui dois módulos principais:

- **Treinamento e otimização dos modelos de classificação**, utilizando um algoritmo genético para encontrar os melhores hiperparâmetros.
- **Assistente inteligente em Streamlit**, que utiliza um modelo de linguagem para interpretar os resultados do modelo treinado e responder perguntas do usuário.

O objetivo do projeto é demonstrar a integração entre modelos tradicionais de Machine Learning e Large Language Models (LLMs), fornecendo explicações em linguagem natural sobre os resultados obtidos.

## Dataset

O projeto utiliza o conjunto de dados **Breast Cancer Wisconsin Dataset**, contendo características extraídas de exames citológicos para classificação de tumores em:

- **B** — Benigno
- **M** — Maligno

Foram utilizadas as seguintes variáveis durante o treinamento:

- `concave points_mean`
- `radius_worst`
- `perimeter_worst`
- `concave points_worst`

## Estrutura do Projeto

```
.
├── agent-llm.py
├── genetic_algorithm.py
├── hyperparameter_otim.py
├── requirements.txt
├── content/
│   └── data.csv
├── model.pkl
├── scaler.pkl
└── results_model.json
```

## Funcionamento

### 1. Otimização dos hiperparâmetros

O arquivo `hyperparameter_otim.py` é responsável por:

- carregar o dataset;
- realizar o pré-processamento dos dados;
- dividir treino e teste;
- treinar os modelos base;
- executar um Algoritmo Genético para otimização dos hiperparâmetros;
- selecionar a melhor solução encontrada;
- exportar:
  - modelo treinado (`model.pkl`);
  - scaler (`scaler.pkl`);
  - métricas do modelo (`results_model.json`).

Os modelos disponíveis para otimização são:

- Random Forest
- Linear SVM
- KNN

O algoritmo genético implementa:

- geração aleatória da população;
- seleção por torneio;
- crossover;
- mutação;
- elitismo.

A função de avaliação (fitness) utiliza a métrica **Recall Macro** através de validação cruzada estratificada.

## Assistente Inteligente

O arquivo `agent-llm.py` implementa uma interface em Streamlit integrada à API da OpenAI.

O assistente é capaz de:

- explicar o funcionamento do modelo treinado;
- informar as métricas obtidas;
- interpretar o diagnóstico em linguagem natural;
- realizar previsões utilizando o modelo exportado;
- responder perguntas do usuário relacionadas ao sistema.

O assistente utiliza Function Calling para acessar funções Python responsáveis por:

- retornar as métricas do modelo;
- explicar o processo de classificação;
- realizar previsões utilizando o modelo treinado.

## Requisitos

Instale as dependências utilizando:

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto contendo sua chave da OpenAI:

```env
OPENAI_API_KEY=sua_chave_aqui
```

## Execução

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

Caso o projeto já esteja baixado, basta abrir um terminal na pasta do projeto.

### 2. Criar um ambiente virtual (opcional, mas recomendado)

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Windows (Prompt de Comando)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

#### Windows

```powershell
pip install -r requirements.txt
```

#### Linux/macOS

```bash
pip3 install -r requirements.txt
```

### 4. Configurar a chave da OpenAI

Crie um arquivo chamado `.env` na raiz do projeto contendo:

```env
OPENAI_API_KEY=sua_chave_aqui
```

### 5. Adicionar o dataset

Crie a pasta `content` na raiz do projeto e coloque o arquivo `data.csv` dentro dela:

```
content/
└── data.csv
```

### 6. Executar o treinamento

O script abaixo realiza:

- pré-processamento dos dados;
- treinamento dos modelos;
- otimização dos hiperparâmetros utilizando Algoritmo Genético;
- exportação do modelo treinado.

#### Windows

```powershell
python hyperparameter_otim.py
```

#### Linux/macOS

```bash
python3 hyperparameter_otim.py
```

Ao final da execução serão gerados:

- `model.pkl`
- `scaler.pkl`
- `results_model.json`

### 7. Executar o assistente

Após o treinamento, execute o Streamlit.

#### Windows

```powershell
streamlit run agent-llm.py
```

#### Linux/macOS

```bash
streamlit run agent-llm.py
```

O navegador abrirá automaticamente a interface do sistema.

Caso isso não ocorra, acesse o endereço exibido no terminal, normalmente:

```
http://localhost:8501
```

## Fluxo do Projeto

```
Dataset
      │
      ▼
Pré-processamento
      │
      ▼
Treinamento Inicial
      │
      ▼
Algoritmo Genético
      │
      ▼
Melhores Hiperparâmetros
      │
      ▼
Treinamento Final
      │
      ▼
Exportação do Modelo
      │
      ▼
Assistente LLM
      │
      ▼
Interpretação dos Resultados
```

## Vídeo de Demonstração

A demonstração completa do funcionamento do projeto está disponível em:

https://youtu.be/RXf7-zNzPHA

## Observações

- O sistema possui finalidade acadêmica e de demonstração.
- As previsões realizadas pelo modelo não substituem avaliação médica profissional.
- O modelo deve ser utilizado apenas como ferramenta de apoio à decisão.

## Autor
- Igor de Sousa
- RM 371788
- FIAP - Pós-Tech IA para Devs - 9IADT
- Grupo 117