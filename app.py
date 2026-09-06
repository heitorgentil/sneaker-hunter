from ast import With

import streamlit as st

st.set_page_config(
    page_title="Sneaker Hunter",
    page_icon="👟",
    layout="wide" 
)

from src.collectors.yourid import coletar_tenis_yourid


st.image("assets/logo.png", width=400)

df = coletar_tenis_yourid()

coluna = st.columns(3)
for indice, produto in df.iterrows():
        with coluna[indice%3]:
            with st.container(border=True):
                st.image(produto["imagem"], width=250)
                st.write(produto["marca"])
                st.write(produto["nome"])
                st.write(f"De R$ {produto['preco_original']:.2f}")
                st.write(f"Por R$ {produto['preco_promocional']:.2f}")
                st.write(f"{produto['desconto_pct']:.0f}% OFF")