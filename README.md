# Miniprojeto de Análise de Dados do Varejo

Projeto de análise exploratória de dados desenvolvido no contexto do curso de Análise de Dados do programa SCTec - Sebrae, em 2026. O objetivo principal é aplicar técnicas de coleta, limpeza, validação, estatística descritiva e exploração de padrões em uma base realista de varejo, transformando os dados em informações úteis para tomada de decisão.

## Visão geral

Este projeto utiliza a base `Base Varejo.csv` para:

- carregar e validar a estrutura dos dados;
- identificar problemas de qualidade de dados;
- realizar limpeza e padronização;
- gerar métricas estatísticas sobre o número de filhos por cliente;
- analisar padrões de agrupamento por gênero, categoria e período;
- apresentar os resultados em uma interface interativa construida com Streamlit.

A aplicação foi implementada em Python e centraliza o fluxo analítico em `main.py`, sendo executada localmente em ambiente de desenvolvimento ou em notebooks/ambientes compatíveis com Python.

## Objetivo do projeto

O mini projeto aborda uma análise exploratória de dados de varejo, com foco em:

- compreender a estrutura da base;
- verificar inconsistências e ruídos nos dados;
- preparar a base para análise;
- responder perguntas de negócio simples, como:
  - qual é a distribuição do número de filhos por cliente?
  - há diferenças de comportamento por gênero?
  - quais categorias de produto concentram mais vendas?
  - como as vendas se comportam ao longo do tempo?

## Base de dados

A base utilizada está no arquivo raiz do projeto:

- `Base Varejo.csv`

### Estrutura dos dados

A base contém 830.000 registros e 14 colunas, com separador `;`. Os campos principais são:

- `DATA`: data da venda
- `CO_ID`: identificador da compra/compra do cliente
- `CL_ID`: identificador do cliente
- `CL_GENERO`: gênero do cliente
- `CL_EC`: estado civil do cliente
- `CL_FHL`: número de filhos do cliente
- `CL_SEG`: segmento do cliente
- `PR_ID`: identificador do produto
- `PR_CAT`: categoria do produto
- `PR_NOME`: nome do produto

Além dessas colunas, a base original possui quatro colunas sem nome (`Unnamed: 10` a `Unnamed: 13`), que foram removidas no processo de limpeza, pois não possuem valor analítico.

## Requisitos

### Tecnologias utilizadas

- Python 3.13+
- pandas
- numpy
- streamlit

### Dependências do projeto

O arquivo `pyproject.toml` define as dependências principais do projeto:

- `numpy`
- `pandas`
- `plotly`
- `streamlit`

## Estrutura do projeto

```text
Miniprojeto_PedroGabriel_Analise_de_Dados_TI/
├── Base Varejo.csv              # base principal de dados
├── README.md                    # documentação do projeto
├── main.py                      # script principal da aplicação Streamlit
├── pyproject.toml               # configuração do projeto e dependências
├── uv.lock                      # lockfile do ambiente
├── .venv/                       # ambiente virtual local
├── src/                        # estrutura de pacote do projeto
└── .gitignore
```

## Fluxo da análise

O fluxo implementado na aplicação segue esta sequência:

1. Carregamento da base com `pandas`
2. Visualização inicial da estrutura da base
3. Checagem de qualidade dos dados
   - colunas sem nome e sem conteúdo analítico
   - linhas duplicadas
   - valores `#N/D` em categoria e nome do produto
   - datas que precisam ser convertidas para o formato temporal
4. Limpeza mínima necessária
   - remoção das colunas sem nome
   - conversão da coluna `DATA` para tipo temporal
   - remoção de registros duplicados
   - padronização de valores como `#N/D` em categorias e nomes de produtos
5. Estatísticas descritivas da variável `CL_FHL`
   - média
   - mediana
   - desvio padrão
   - moda
   - máximo
   - mínimo
   - quartis
6. Agrupamento e exploração de padrões
   - comparação por gênero
   - análise por categoria de produto
   - visualização temporal por data/categoria
7. Interpretação dos resultados e observações finais

## Principais rotinas implementadas

No arquivo `main.py`, o projeto organiza a lógica em funções específicas:

- `carregar_dados()`: lê a base de dados com `pd.read_csv()`
- `apresentacao_da_base()`: mostra quantidade de linhas, colunas e tipos
- `limpeza_de_dados()`: aplica validação e limpeza dos dados
- `estatistica_descritiva()`: calcula medidas estatísticas da variável de filhos
- `agrupamento_de_dados()`: gera tabelas e gráficos agrupados
- `main()`: ponto de entrada da aplicação Streamlit

## Como executar o projeto

### Opção 1: via ambiente virtual e pip

```bash
cd "Miniprojeto_PedroGabriel_Analise_de_Dados_TI"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install numpy pandas streamlit plotly
streamlit run main.py
```

### Opção 2: via `uv` (recomendado para manter consistência do ambiente)

```bash
cd "Miniprojeto_PedroGabriel_Analise_de_Dados_TI"
uv sync
uv run streamlit run main.py
```

> O projeto também pode ser executado em ambiente do VS Code, desde que a base `Base Varejo.csv` esteja no diretório raiz e as dependências estejam instaladas corretamente.

## Como a aplicação se comporta

Ao iniciar a aplicação, a interface exibe uma sequência de blocos para:

- carregar a base;
- mostrar a estrutura inicial;
- apresentar dados da base;
- validar e limpar os registros;
- exibir estatísticas descritivas;
- apresentar agrupamentos e gráficos;
- facilitar a interpretação dos resultados.

## Problemas de qualidade identificados

A aplicação verifica e trata alguns itens de qualidade da base, como:

- linhas duplicadas;
- colunas não identificadas (`Unnamed: 10` a `Unnamed: 13`);
- valores como `#N/D` em campos categóricos;
- necessidade de conversão da coluna de data para formato temporal;
- registros sem categoria ou nome de produto, que são removidos.

As quatro colunas sem nome são removidas e a aplicação exibe as linhas duplicadas antes de eliminá-las. A limpeza reduz ruído nas métricas, mas não substitui uma auditoria completa de qualidade dos dados.

## Resultados esperados

A execução da análise deve produzir:

- tabela com estrutura da base;
- verificações e tratamentos de qualidade dos dados;
- remoção de dados irrelevantes ou inconsistentes;
- estatísticas do número de filhos por cliente;
- agrupamentos por gênero e categoria;
- gráficos de evolução de vendas por categoria ao longo do tempo;
- visualizações e tabelas para apoiar a interpretação dos padrões observados.

## Observações finais

Este projeto é uma aplicação didática de análise exploratória, com foco na prática de limpeza e visualização. Ele demonstra como aplicar ferramentas e técnicas de ciência de dados em um conjunto de dados de varejo de forma acessível, com destaque para:

- tratamento de dados incompletos;
- padronização de colunas;
- geração de indicadores estatísticos;
- exploração por agrupamento;
- comunicação visual dos resultados.

## Autor

- Pedro Gabriel Guardini

## Licença

O projeto foi desenvolvido como atividade acadêmica e pode ser reutilizado ou adaptado para fins de estudo e aprendizado.
