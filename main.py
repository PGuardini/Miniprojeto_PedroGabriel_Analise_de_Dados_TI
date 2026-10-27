import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def carregar_dados():
    st.subheader("Carregando dataframe com Pandas")
    st.code("df = pd.read_csv('Base Varejo.csv', sep=';')")
    return pd.read_csv("Base Varejo.csv", sep=";")


def apresentacao_da_base(base_varejo: pd.DataFrame):
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
    st.subheader("Verificação de colunas sem nome")
    colunas_sem_nome = base_varejo.columns[-4:]
    st.dataframe(base_varejo[colunas_sem_nome])

    st.write("Remoção das colunas sem nome")
    st.code("base_varejo.drop(columns=base_varejo.columns[-4:], inplace=True)")
    base_varejo.drop(columns=colunas_sem_nome, inplace=True)

    base_varejo["DATA"] = pd.to_datetime(
        base_varejo["DATA"], format="%d/%m/%Y"
    ).dt.date
    st.subheader("Conversão da coluna DATA")
    st.code(
        """base_varejo['DATA'] = pd.to_datetime(
    base_varejo['DATA'], format="%d/%m/%Y"
).dt.date""",
        language="python",
    )
    st.dataframe(base_varejo["DATA"].head())

    st.write("Verificando linhas duplicadas")
    duplicados = base_varejo.duplicated()
    st.dataframe(base_varejo[duplicados])
    base_varejo = base_varejo.drop_duplicates()

    st.write("Substituindo valores #N/D e removendo registros sem categoria ou produto")
    base_varejo[["PR_CAT", "PR_NOME"]] = base_varejo[
        ["PR_CAT", "PR_NOME"]
    ].replace("#N/D", np.nan)
    base_varejo = base_varejo.dropna(subset=["PR_CAT", "PR_NOME"])
    st.dataframe(base_varejo)

    return base_varejo


def main():
    st.title("Análise Descritiva de Dados do Varejo")
    st.header("1. Carregamento e visualização prévia da base de dados")

    with st.spinner("Carregando a base de dados"):
        base_varejo = carregar_dados()

    apresentacao_da_base(base_varejo)

    st.header("2. Tratamento dos dados")
    base_varejo = limpeza_de_dados(base_varejo)


if __name__ == "__main__":
    main()
