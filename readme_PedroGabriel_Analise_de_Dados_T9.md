# Análise de Dados com Python [T9]
## Mini-Projeto Avaliativo — Módulo 1, Semana 07

Projeto de análise exploratória da base de varejo, realizado por Pedro Gabriel
Guardini como atividade do curso de Análise de Dados do programa SCTec/Sebrae.
O código executa a leitura, inspeção, tratamento e análise exploratória dos dados
em uma aplicação Streamlit.

## Arquivos

- `main.py`: código Python da análise e da interface.
- `Base Varejo.csv`: base de dados de origem, lida com separador `;`.
- `README.md`: documentação geral do repositório.

## Como executar

Com Python e as dependências do projeto instaladas, abra um terminal na pasta do
projeto e execute:

```bash
uv sync
uv run streamlit run main.py
```

Também é possível instalar as dependências com `pip`:

```bash
python -m pip install pandas numpy streamlit
streamlit run main.py
```

A base `Base Varejo.csv` deve permanecer na mesma pasta que `main.py`.

## Etapas realizadas

1. Leitura do arquivo CSV com pandas e apresentação de dimensões, tipos e amostra.
2. Identificação das quatro colunas sem nome, que estão totalmente vazias.
3. Conversão da coluna `DATA` para o tipo datetime do pandas.
4. Exibição e remoção de linhas integralmente duplicadas.
5. Substituição de `#N/D` por valor ausente em `PR_CAT` e `PR_NOME`, seguida da
   remoção desses registros, pois não há informação para recuperar categoria ou
   produto com segurança.
6. Cálculo de estatísticas de `CL_FHL` usando um registro por cliente.
7. Agrupamentos de volume de itens por categoria/gênero e por data/categoria.
8. Apresentação de conclusões calculadas sobre a base tratada.

## Conclusões e insights

Os números abaixo foram verificados após aplicar as etapas de limpeza descritas:

- A base tratada contém **730.219 linhas**, **18.469 compras distintas** e
  **1.000 clientes únicos**.
- **527 clientes (52,7%)** não têm filhos registrados. O número médio é
  **1,14 filho por cliente**; mediana e moda são **0**.
- Foram identificadas **9.614 compras distintas** para clientes do gênero feminino
  e **8.855** para clientes do gênero masculino. A comparação usa IDs de compra
  distintos, não a quantidade de linhas.
- **ALIMENTOS** é a categoria com mais linhas de itens (**384.197**, cerca de
  **52,6%** das linhas mantidas). Essa métrica representa registros de itens, não
  receita.
- **Outubro de 2021** foi o mês com maior volume observado, com **28.451 linhas de
  itens**. Como a base não possui valores monetários, não é possível determinar
  faturamento, ticket médio ou qual grupo de clientes gasta mais.

Na base original havia **830.000 linhas** e quatro colunas inteiramente vazias.
Foram encontradas **96.553 linhas integralmente duplicadas**; depois de removê-las,
**3.228 registros** ainda apresentavam `#N/D` em categoria ou nome de produto e
foram descartados. Os registros de origem devem ser conferidos para confirmar se as
linhas idênticas são duplicidades acidentais e se é possível recuperar os campos
ausentes.

## Reflexão teórica: ETL e qualidade de dados

ETL é o processo de **Extração, Transformação e Carga** de dados. A extração obtém
os dados de uma fonte e os disponibiliza para processamento. A transformação
corrige formatos, trata valores ausentes e duplicidades e aplica regras para
preparar uma base adequada à análise. A carga disponibiliza o resultado tratado
para consumo, como um relatório, um banco de dados ou um arquivo.

Neste projeto, a extração ocorre na leitura de `Base Varejo.csv`; a transformação
inclui a remoção das colunas vazias, a conversão de `DATA`, a deduplicação exata e
o tratamento dos registros marcados com `#N/D`. A aplicação carrega os resultados
na interface Streamlit para análise, mas não salva uma cópia persistente dos dados
limpos. Exportar essa cópia seria uma extensão natural do fluxo ETL.

Qualidade de dados deve ser avaliada de acordo com o uso pretendido. Completude
indica se os campos necessários estão preenchidos; validade verifica se os valores
respeitam formatos e domínios; consistência procura conflitos entre campos;
unicidade avalia duplicidades; e adequação verifica se os dados permitem responder
à pergunta de negócio. Assim, remover uma linha idêntica pode evitar contagens
infladas, mas é preciso confirmar que não representa itens legitimamente repetidos.
Da mesma forma, descartar `#N/D` reduz registros e pode introduzir viés; imputar
valores sem fonte confiável também seria inadequado. As decisões devem ser
documentadas e revistas conforme a finalidade da análise.

## Limitações

- A base não contém preço ou valor de compra; as conclusões tratam de linhas de
  itens e contagens de compras, não de faturamento.
- A deduplicação considera linhas integralmente idênticas e depende da hipótese de
  que tais repetições são erros na origem.
- Registros sem categoria ou nome de produto foram removidos porque não havia
  informação suficiente para imputá-los com segurança.
- A aplicação exibe a base limpa em memória, sem exportar um arquivo `df_limpo`.

---

**Autor:** Pedro Gabriel Guardini  
**Turma:** Análise de Dados T9
