import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():
    # Mantém o arquivo de origem em cache para evitar releituras no Streamlit.
    st.subheader("Carregando dataframe com Pandas")
    st.code("df = pd.read_csv('Base Varejo.csv', sep=';')")
    return pd.read_csv("Base Varejo.csv", sep=";")


def apresentacao_da_base(base_varejo: pd.DataFrame):
    # Apresenta a dimensão, os tipos inferidos e uma amostra dos dados originais.
    st.subheader("Estrutura da base de dados")
    st.table(
        {
            "Linhas": base_varejo.shape[0],
            "Colunas": base_varejo.shape[1],
        }
    )

    st.subheader("Colunas e seus tipos")
    st.table(base_varejo.dtypes.astype(str).to_dict())

    st.subheader("Visualização prévia da base")
    st.dataframe(base_varejo.head())


def limpeza_de_dados(base_varejo: pd.DataFrame):
    # As últimas quatro colunas sem nome são vazias e não contribuem para a análise.
    st.subheader("Verificação de colunas sem nome")
    colunas_sem_nome = base_varejo.columns[-4:]
    st.dataframe(base_varejo[colunas_sem_nome])

    st.write("Remoção das colunas sem nome")
    st.code("base_varejo.drop(columns=base_varejo.columns[-4:], inplace=True)")
    base_varejo.drop(columns=colunas_sem_nome, inplace=True)

    # Converte as datas para o tipo datetime do pandas para permitir agrupamentos temporais.
    base_varejo["DATA"] = pd.to_datetime(
        base_varejo["DATA"], format="%d/%m/%Y"
    )
    st.subheader("Conversão da coluna DATA")
    st.code(
        """base_varejo['DATA'] = pd.to_datetime(
    base_varejo['DATA'], format="%d/%m/%Y"
)""",
        language="python",
    )
    st.dataframe(base_varejo["DATA"].head())

    # Remove somente linhas integralmente repetidas, preservando compras com vários itens.
    st.write("Verificando linhas duplicadas")
    duplicados = base_varejo.duplicated()
    st.dataframe(base_varejo[duplicados])
    base_varejo = base_varejo.drop_duplicates()

    # Não há informação suficiente para recuperar categoria/nome marcados como #N/D.
    st.write("Substituindo valores #N/D e removendo registros sem categoria ou produto")
    base_varejo[["PR_CAT", "PR_NOME"]] = base_varejo[
        ["PR_CAT", "PR_NOME"]
    ].replace("#N/D", np.nan)
    base_varejo = base_varejo.dropna(subset=["PR_CAT", "PR_NOME"])
    st.dataframe(base_varejo)

    return base_varejo


def estatistica_descritiva(base_varejo: pd.DataFrame):
    # Usa um registro por cliente para não contar clientes repetidos em cada compra.
    clientes_unicos = base_varejo.drop_duplicates(subset=["CL_ID"])
    filhos = clientes_unicos["CL_FHL"]
    quartis = filhos.quantile([0.25, 0.5, 0.75])
    moda = filhos.mode()

    medidas_estatisticas = pd.DataFrame(
        {
            "Medida": [
                "Média de filhos por cliente",
                "Mediana de filhos por cliente",
                "Desvio padrão de filhos por cliente",
                "Moda de filhos por cliente",
                "Máximo de filhos",
                "Mínimo de filhos",
                "Quantidade de clientes",
                "1º quartil (25%)",
                "2º quartil (50%)",
                "3º quartil (75%)",
            ],
            "Valor": [
                filhos.mean(),
                filhos.median(),
                filhos.std(),
                ", ".join(moda.astype(str)),
                filhos.max(),
                filhos.min(),
                filhos.count(),
                quartis.loc[0.25],
                quartis.loc[0.5],
                quartis.loc[0.75],
            ],
        }
    )

    st.subheader("Estatística descritiva do número de filhos por cliente")
    st.dataframe(medidas_estatisticas)


def agrupamento_de_dados(base_varejo: pd.DataFrame):
    # A primeira tabela conta linhas de itens por categoria e gênero do cliente.
    vendas_por_genero = pd.pivot_table(
        base_varejo,
        values="CO_ID",
        index="PR_CAT",
        columns="CL_GENERO",
        aggfunc="count",
        margins=True,
    )
    st.subheader("Itens por categoria e gênero do cliente")
    st.dataframe(
        vendas_por_genero.rename(
            columns={"F": "Feminino", "M": "Masculino", "All": "Total"}
        )
    )

    # Agrupa as linhas por dia e categoria para mostrar o volume de itens no tempo.
    st.subheader("Itens por categoria ao longo do tempo")
    categoria_por_data = (
        base_varejo.groupby(["DATA", "PR_CAT"])["CO_ID"]
        .count()
        .reset_index(name="ITENS")
    )
    itens_temporais = categoria_por_data.pivot(
        index="DATA", columns="PR_CAT", values="ITENS"
    )
    st.line_chart(itens_temporais)
    st.dataframe(itens_temporais)


def exibir_conclusoes(base_varejo: pd.DataFrame):
    # Calcula os indicadores usados nas conclusões sobre clientes, compras e período.
    clientes = base_varejo.drop_duplicates(subset=["CL_ID"])
    total_clientes = clientes["CL_ID"].nunique()
    clientes_sem_filhos = int(clientes["CL_FHL"].eq(0).sum())
    media_filhos = clientes["CL_FHL"].mean()

    compras_por_genero = base_varejo.groupby("CL_GENERO")["CO_ID"].nunique()
    maior_genero = compras_por_genero.idxmax()
    compras_maior_genero = int(compras_por_genero.max())
    demais_compras = compras_por_genero.drop(index=maior_genero)
    outro_genero = demais_compras.idxmax()
    compras_outro_genero = int(demais_compras.max())
    total_compras = int(base_varejo["CO_ID"].nunique())
    percentual_compras = compras_maior_genero / total_compras * 100
    nome_genero = {"F": "feminino", "M": "masculino"}.get(
        maior_genero, str(maior_genero)
    )
    nome_outro_genero = {"F": "feminino", "M": "masculino"}.get(
        outro_genero, str(outro_genero)
    )

    itens_por_categoria = base_varejo["PR_CAT"].value_counts()
    categoria_lider = str(itens_por_categoria.index[0])
    itens_categoria_lider = int(itens_por_categoria.iloc[0])
    percentual_categoria = itens_categoria_lider / len(base_varejo) * 100

    itens_por_mes = (
        base_varejo.groupby(base_varejo["DATA"].dt.to_period("M"))
        .size()
        .sort_values(ascending=False)
    )
    mes_pico = str(itens_por_mes.index[0])
    itens_mes_pico = int(itens_por_mes.iloc[0])

    # Mostra conclusões calculadas sobre a base já limpa, sem inferir faturamento.
    st.subheader("Conclusões")
    st.markdown(
        f"""
- A base tratada contém **{total_clientes:,} clientes únicos**; **{clientes_sem_filhos:,}**
  ({clientes_sem_filhos / total_clientes:.1%}) não têm filhos registrados. A média é
  **{media_filhos:.2f} filhos por cliente**.
- Clientes do gênero **{nome_genero}** aparecem em mais compras distintas
  (**{compras_maior_genero:,}**) do que os do gênero **{nome_outro_genero}**
  (**{compras_outro_genero:,}**); isso corresponde a **{percentual_compras:.1f}%**
  das compras identificadas por `CO_ID`.
- **{categoria_lider}** é a categoria com mais linhas de itens (**{itens_categoria_lider:,}**,
  **{percentual_categoria:.1f}%** das linhas da base tratada); isso mede volume de registros,
  não faturamento.
- O mês com maior volume de linhas de itens é **{mes_pico}**, com **{itens_mes_pico:,}**
  registros. O resultado descreve volume observado, não sazonalidade nem receita.
- A base não contém coluna de preço/valor; portanto, não permite concluir qual grupo
  gera maior faturamento ou calcular ticket médio. A remoção de duplicatas exatas
  também merece validação com a origem para confirmar que não eram itens repetidos legítimos.
"""
    )


def main():
    st.title("Análise Descritiva de Dados do Varejo")
    st.header("1. Carregamento e visualização prévia da base de dados")

    # Executa as etapas em ordem: leitura, inspeção, tratamento e análise.
    with st.spinner("Carregando a base de dados"):
        base_varejo = carregar_dados()

    apresentacao_da_base(base_varejo)

    st.header("2. Tratamento dos dados")
    base_varejo = limpeza_de_dados(base_varejo)

    st.header("3. Estatística descritiva da base")
    estatistica_descritiva(base_varejo)

    st.header("4. Exploração de padrões de agrupamento")
    agrupamento_de_dados(base_varejo)

    st.header("5. Conclusões")
    exibir_conclusoes(base_varejo)


if __name__ == "__main__":
    main()
