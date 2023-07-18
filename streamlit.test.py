import streamlit as st
import pandas as pd
from riot_api import get_stats
from PIL import Image
import requests



st.set_page_config(page_title='League of Legends API', 
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/2/2a/LoL_icon.svg")



header = st.container()

with st.sidebar:
    st.header('You:')
    summoner = st.text_input('Summoner name:', '', key='')
    number = st.slider('Escolha o número de partidas', 0, 100)
    agree = st.checkbox('Run!')
    



with header:
    
    st.image('https://www.leagueoflegends.com/static/logo-1200-589b3ef693ce8a750fa4b4704f1e61f2.png', width=500)
    st.title('DataScience Project')
    st.text('In this project i will use the League of legends API to show you how you can improve your gameplay!')

if agree:
    table = get_stats(summoner, number, 'RGAPI-a3f27e13-34b2-411e-a63d-f54ecf504cac')

    df = pd.DataFrame(data=table)

    df2 = df.groupby('Champion')['KDA'].mean().round(2).to_frame().sort_values(by='KDA', ascending=False)

    df3 = df.groupby('Champion').size().sort_values(ascending=False).to_frame()


    col1, col2 = st.columns(2)

    with col1:
        st.subheader("You are good with:")
        st.dataframe(df2)


    with col2: 
        st.subheader("Most played champions:")
        st.dataframe(df3)

