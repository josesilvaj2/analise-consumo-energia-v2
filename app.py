import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(
    page_title="Análise de Consumo de Energia",
    page_icon="⚡",
    layout="wide"
)

# ==============================
# ESTILO PERSONALIZADO
# ==============================

st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: 700;
            color: #1f2937;
        }
        .section-title {
            font-size: 22px;
            font-weight: 600;
            margin-top: 20px;
        }
        .footer {
            margin-top: 40px;
            font-size: 14px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# TÍTULO
# ==============================

st.markdown('<p class="main-title">⚡ Análise Profissional de Consumo de Energia</p>', unsafe_allow_html=True)
st.write("Insira os dados mensais para gerar análise estatística detalhada e previsão de consumo.")

# ==============================
# ENTRADA DE DADOS
# ==============================

st.markdown('<p class="section-title">📅 Dados de Consumo</p>', unsafe_allow_html=True)

qtd_meses = st.number_input(
    "Quantos meses deseja informar? (mínimo 3 e máximo 12)",
    min_value=1,
    max_value=12,
    step=1
)

if qtd_meses < 3:
    st.warning("É necessário informar no mínimo 3 meses.")
    st.stop()

dados = []

for i in range(int(qtd_meses)):
    col1, col2, col3 = st.columns(3)

    with col1:
        mes = st.text_input("Mês", key=f"mes_{i}")
    with col2:
        ano = st.number_input("Ano", min_value=2000, max_value=2100, step=1, key=f"ano_{i}")
    with col3:
        consumo = st.number_input("Consumo (kWh)", min_value=0.0, step=0.1, key=f"consumo_{i}")

    if mes:
        dados.append({
            "Mes/Ano": f"{mes}/{ano}",
            "Consumo (kWh)": consumo
        })

# ==============================
# PROCESSAMENTO
# ==============================

if len(dados) >= 3:

    df = pd.DataFrame(dados)

    st.markdown('<p class="section-title">💰 Tarifa de Energia</p>', unsafe_allow_html=True)

    valor_kwh = st.number_input(
        "Valor do kWh (R$/kWh)",
        min_value=0.0,
        step=0.01
    )

    confirmar = st.checkbox(f"Confirmo o valor de R$ {valor_kwh:.2f} por kWh")

    if confirmar:

        media = df["Consumo (kWh)"].mean()
        mediana = df["Consumo (kWh)"].median()
        maximo = df["Consumo (kWh)"].max()
        minimo = df["Consumo (kWh)"].min()
        desvio_padrao = df["Consumo (kWh)"].std()
        amplitude = maximo - minimo

        consumo_diario = media / 30
        previsao = df["Consumo (kWh)"].tail(3).mean()
        valor_estimado = previsao * valor_kwh

        # ==============================
        # MÉTRICAS DESTACADAS
        # ==============================

        st.markdown('<p class="section-title">📊 Indicadores Principais</p>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Média (kWh)", f"{media:.2f}")
        col2.metric("Máximo (kWh)", f"{maximo:.2f}")
        col3.metric("Mínimo (kWh)", f"{minimo:.2f}")
        col4.metric("Desvio Padrão", f"{desvio_padrao:.2f}")

        # ==============================
        # GRÁFICO
        # ==============================

        st.markdown('<p class="section-title">📈 Evolução do Consumo</p>', unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x="Mes/Ano", y="Consumo (kWh)", data=df, ax=ax)
        ax.axhline(media, linestyle="--", color="red", label=f"Média = {media:.1f} kWh")
        ax.set_xlabel("Mês/Ano")
        ax.set_ylabel("Consumo (kWh)")
        ax.set_title("Histórico de Consumo Mensal")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)

        # ==============================
        # RESULTADOS FINAIS
        # ==============================

        st.markdown('<p class="section-title">🔮 Previsão e Estimativa</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        col1.metric("Previsão Próximo Mês (kWh)", f"{previsao:.2f}")
        col2.metric("Valor Estimado (R$)", f"{valor_estimado:.2f}")

        st.markdown("""
        ---
        ### 📝 Observação Técnica
        A previsão foi realizada utilizando **média móvel simples com janela de 3 meses**,
        considerando os três períodos mais recentes informados.
        """)

# ==============================
# RODAPÉ
# ==============================

st.markdown('<p class="footer">Desenvolvido por José Silva • Projeto de Extensão CEP</p>', unsafe_allow_html=True)
