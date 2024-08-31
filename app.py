# Core PKG's
import streamlit as st

# Exploratory Data Analysis PKG's
import pandas as pd

# Data visualizaation PKG's
import plotly.express as px



st.set_page_config(page_title="NLP App", page_icon="🧊", layout="wide")

def main():
    st.title("Aplicativo NLP")
    menu = ["Home", "NLP(arquivos)", "Sobre"]
    
    escolha = st.sidebar.selectbox("Menu", menu)
    if escolha == "Home":
        st.subheader("Home: Analyse Text")
        texto_puro = st.text_area("Digite o texto aqui")
        nmr_mais_comum = st.sidebar.number_input("Número mais comuns de Tokens", 5, 15)
        if st.button("Análise"):
            
            with st.expander("Texto Original"):
                st.write(texto_puro)
        
            with st.expander("Análise de Texto"):
                st.write(texto_puro)
                
            with st.expander("Entities/ Entidades"):
                st.write(texto_puro)    
                
            # Layouts
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Estatísticas de Palavras"):
                    pass
                
                with st.expander("Top Palavras-Chave"):
                    pass
                
                with st.expander("Sentiment"):
                    pass
            
            with col2:
                with st.expander("Plot Frequência de Palavras"):
                    pass
                
                with st.expander("Plot Partes do Discurso"):
                    pass
                
                with st.expander("Plot WordCloud"):
                    pass
            
        
            with st.expander("Download Resultado da Análise"):
                pass
        
    elif escolha == "NLP(arquivos)":
        st.subheader("NLP Task")
        
    else:
        st.subheader("Sobre")
    
    
if __name__ == '__main__':
    main()