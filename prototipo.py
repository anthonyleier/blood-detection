import streamlit as st
import pandas as pd

def carregarModelo(model):
    return model


st.write("# Íris Data App")

st.sidebar.write("## Parâmetros")
comp_sepala = st.sidebar.slider("Comprimento da Sépala", 4.3, 7.9)
larg_sepala = st.sidebar.slider("Largura da Sépala", 2.0, 4.4)
comp_petala = st.sidebar.slider("Comprimento da Pétala", 1.0, 6.9)
larg_petala = st.sidebar.slider("Largura da Pétala", 0.1, 2.5)

st.write("Este é um aplicativo de dados desenvolvido na disciplina de Big Data")
st.write("14/06/2021")

dados = {
    "comp_sepala": comp_sepala,
    "larg_sepala": larg_sepala,
    "comp_petala": comp_petala,
    "larg_petala": larg_petala,
}

st.write("Dados de entrada:")
entrada = pd.DataFrame(dados, index=[0])
st.write(entrada)

# predicao = dtc.predict(entrada)
st.write("Predição:")
# st.write(predicao)

# predicao_proba = dtc.predict_proba(entrada)
st.write("Probabilidade:")
# st.write(predicao_proba)

# st.write(dtc.feature_importances_)

# decisao = export_graphviz(dtc, filled=True, feature_names=entrada.columns, out_file=None)
# st.graphviz_chart(decisao)