# Core PKG's
import streamlit as st
import streamlit.components.v1 as stc
# import warnings
# warnings.filterwarnings("ignore", message="numpy.dtype size changed")
# warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

# Exploratory Data Analysis PKG's
import pandas as pd

# Data visualizaation PKG's
import plotly.express as px
from wordcloud import WordCloud

# NLP PKG's
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
from textblob import TextBlob

# Text Cleaning
import neattext as nt
import neattext.functions as nfx

# utils
from collections import Counter
import base64
import time
timestr = time.strftime("%d%m%Y")

# File processing
import docx2txt
import pdfplumber

# Funções
def text_analyzer(my_text):
    docx = nlp(my_text)
    
    all_data = [(token.text, token.shape_, token.pos_, token.tag_, token.lemma, token.is_alpha, token.is_stop) for token in docx]
    # all_data = [('"Token":{}, "Dependência":{}'.format(token.text, token.dep_)) for token in docx]
   
    df = pd.DataFrame(all_data, columns=['Token', 'Shape', 'POS', 'Tag', 'Lemma', 'Is_Alpha', 'Is_Stop'])
    return df

def get_entites(my_text):
    docx = nlp(my_text)
    entities = [(entity.text, entity.label_) for entity in docx.ents]    
    return entities


HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
# @st.cache
def render_entities(texto_puro):
    docx = nlp(texto_puro)
    html = displacy.render(docx, style="ent")
    html = html.replace("\n\n", "\n")
    result = HTML_WRAPPER.format(html)
    return result


# Função para pegar os tokens mais comuns
def most_common_tokens(my_text, num=5):
    word_tokens = Counter(my_text.split())
    most_common_tokens = dict(word_tokens.most_common(num))
    return most_common_tokens
    
# Função para pegar Sentiment
def get_sentiment(my_text):
    blob = TextBlob(my_text)
    sentiment = blob.sentiment
    return sentiment

def plot_wordcloud(my_text):
    wordcloud = WordCloud().generate(my_text)
    fig = px.imshow(wordcloud) # 
    fig.update_layout(yaxis=dict(visible=False), xaxis=dict(visible=False))
    st.plotly_chart(fig)


# Download resultados
def mk_download(data):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    new_filename = f"nlp_result_{time.time()}.csv"
    st.markdown("### Download File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="nlp_result.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
    
# Ler PDF
def read_pdf(file):
    pdfReader = PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extract_text()
        
        return all_page_text
# Ambos da na mesma
def read_pdf2(file):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        return page.extract_text()

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
                token_resultado = text_analyzer(texto_puro)
                st.dataframe(token_resultado)
                
            with st.expander("Entities/ Entidades"):
                # entity_result = get_entites(texto_puro)
                # st.write(entity_result)
                
                entity_result = render_entities(texto_puro)
                st.write(entity_result, unsafe_allow_html=True)
                #stc.html(entity_result, height=500, scrolling=True)
                
            # Layouts
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Estatísticas de Palavras"):
                    st.info("Estatísticas de Palavras")
                    docx = nt.TextFrame(texto_puro)
                    st.write(docx.word_stats())
                    
                
                with st.expander("Top Palavras-Chave"):
                    st.info("Top Palavras-Chave")
                    processed_text = nfx.remove_stopwords(texto_puro)
                    palavras_chave = most_common_tokens(processed_text)
                    st.write(palavras_chave)
                    
                
                with st.expander("Sentiment"):
                    st.write(get_sentiment(texto_puro))
            
            with col2:
                with st.expander("Plot Frequência de Palavras"):
                    
                    chaves = list(palavras_chave.keys())
                    valores = list(palavras_chave.values())
                    df = pd.DataFrame({'Palavra': chaves, 'Frequência': valores})

                    fig = px.bar(df, x='Palavra', y='Frequência', color='Palavra')
                    st.plotly_chart(fig)
                    
                    # fig = px.bar(palavras_chave.keys(), palavras_chave.values())
                    # st.plotly_chart(fig)
                
                with st.expander("Plot Partes do Discurso"):
                    try:
                        df = token_resultado['POS'].value_counts().reset_index()
                        df.columns = ['POS', 'count']

                        fig = px.bar(df, x='POS', y='count', color='POS')
                        st.plotly_chart(fig)
                    except:
                        st.warning("Dados Insuficientes para Plot: Precisa ser mais que 2")
               
                with st.expander("Plot WordCloud"):
                    try:
                        plot_wordcloud(texto_puro)
                    except:
                        st.warning("Dados Insuficientes para Plot")
            
        
            with st.expander("Download Resultado da Análise"):
                mk_download(token_resultado)
        
    elif escolha == "NLP(arquivos)":
        st.subheader("NLP Task")
        
        texto_puro = st.file_uploader("Upload Arquivos", type=['txt', 'pdf', 'docx'])
        nmr_mais_comum = st.sidebar.number_input("Número mais comuns de Tokens", 5, 15)
        
        if texto_puro is not None:
            if texto_puro.type == 'application/pdf':
                texto_puro = read_pdf(texto_puro)
                # st.write(texto_puro)
            elif texto_puro.type == 'text/plain':
                # st.write(texto_puro.read()) # read as bytes
                texto_puro = str(texto_puro.read(), "utf-8" )
                # st.write(texto_puro)
            else:
                texto_puro = docx2txt.process(texto_puro)
                # st.write(texto_puro)
            
            with st.expander("Texto Original"):
                pass
                # st.write(texto_puro)
        
            with st.expander("Análise de Texto"):
                token_resultado = text_analyzer(texto_puro)
                st.dataframe(token_resultado)
                    
            with st.expander("Entities/ Entidades"):
                # entity_result = get_entites(texto_puro)
                # st.write(entity_result)
                
                entity_result = render_entities(texto_puro)
                st.write(entity_result, unsafe_allow_html=True)
                #stc.html(entity_result, height=500, scrolling=True)
                
            # Layouts
            col1, col2 = st.columns(2)
            with col1:
                with st.expander("Estatísticas de Palavras"):
                    st.info("Estatísticas de Palavras")
                    docx = nt.TextFrame(texto_puro)
                    st.write(docx.word_stats())
                    
                
                with st.expander("Top Palavras-Chave"):
                    st.info("Top Palavras-Chave")
                    processed_text = nfx.remove_stopwords(texto_puro)
                    palavras_chave = most_common_tokens(processed_text)
                    st.write(palavras_chave)
                    
                
                with st.expander("Sentiment"):
                    st.write(get_sentiment(texto_puro))
            
            with col2:
                with st.expander("Plot Frequência de Palavras"):
                    try:
                        chaves = list(palavras_chave.keys())
                        valores = list(palavras_chave.values())
                        df = pd.DataFrame({'Palavra': chaves, 'Frequência': valores})

                        fig = px.bar(df, x='Palavra', y='Frequência', color='Palavra')
                        st.plotly_chart(fig)
                        
                    except:
                        st.warning("Dados Insuficientes para Plot")
                    # fig = px.bar(palavras_chave.keys(), palavras_chave.values())
                    # st.plotly_chart(fig)
                
                with st.expander("Plot Partes do Discurso"):
                    df = token_resultado['POS'].value_counts().reset_index()
                    df.columns = ['POS', 'count']

                    fig = px.bar(df, x='POS', y='count', color='POS')
                    st.plotly_chart(fig)
               
                with st.expander("Plot WordCloud"):
                    try:
                        plot_wordcloud(texto_puro)
                    except:
                        st.warning("Dados Insuficientes para Plot")
            
        
            with st.expander("Download Resultado da Análise"):
                mk_download(token_resultado)
            
            # st.success("Arquivo Carregado com Sucesso")
        
    else:
        st.subheader("Sobre")
    
    
if __name__ == '__main__':
    main()