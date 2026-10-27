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


def main():
    st.title("Análise Descritiva de Dados do Varejo")
    st.header("1. Carregamento e visualização prévia da base de dados")

    with st.spinner("Carregando a base de dados"):
        base_varejo = carregar_dados()

    apresentacao_da_base(base_varejo)


if __name__ == "__main__":
    main()
