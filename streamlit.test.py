import streamlit as st
import pandas as pd
from riot_api import get_stats

header = st.container()


with st.sidebar:
    st.header('You:')
    st.text_input('Summoner name:', '', key='')
    
    



with header:
    st.image('https://www.leagueoflegends.com/static/logo-1200-589b3ef693ce8a750fa4b4704f1e61f2.png', width=500)
    st.title('DataScience Project')
    st.text('In this project i will use the League of legends API to show you how you can improve your gameplay!')


table = get_stats('Armstr0ng', 'RGAPI-df8ad0cb-53c8-4658-ac50-605131769dd6')

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

