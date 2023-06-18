import plotly.express as px
from  datatable import fread
import streamlit as st
import pandas as pd
import numpy as np

barca_red = '#A50044'
barca_blue = '#004D98'


st.title('Correlation Charts')

rename_dict = {
    'Ball Receipt*':'Recebimento de Bola',
    'Ball Recovery':'Recuperação de Posse',
    'Carry':'Condução',
    'Dribble':'Drible',
    'Dribbled Past':'Drible Sofrido',
    'Foul Won':'Falta Sofrida',
    'Shot':'Chutes',
    'pass_outcomeSuccessful':'Passe Certo',
    'Interception':'Interceptação',
    'shot_outcome_Goal':'Gol',
    'shot_outcome_Off T':'Chute Para Fora'
}

df = fread('data_corr.csv').to_pandas().rename(columns=rename_dict)

df['Partida'] = df.apply(lambda row: row.jogo + '\n' + row.temporada, axis=1) 
variaveis = rename_dict.values()

temporadas = ['Todas'] + list(df['temporada'].unique())
chosen_season = st.sidebar.selectbox('Temporada', options=temporadas, index=0)

if chosen_season != 'Todas':
    df = df[df['temporada'] == chosen_season]

col1, col2 = st.sidebar.columns(2)

var1 = col1.selectbox('Variável 1', options=variaveis, index=0)
var2 = col2.selectbox('Variável 2', options=variaveis, index=1)


fig = px.scatter(df, x=var1, y=var2, hover_data=['Partida'], marginal_x="box", marginal_y="box", color_discrete_map={'': barca_blue})

coef = np.polyfit(df[var1], df[var2], 1)
poly1d_fn = np.poly1d(coef)

fig.add_scatter(x=df[var1], y=poly1d_fn(df[var1]), mode='lines', name='Linha de Correlação', line=dict(color=barca_red))
poly1d_fn = np.poly1d(coef)


st.plotly_chart(fig)


