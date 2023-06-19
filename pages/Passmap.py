import streamlit as st
import pandas as pd
import matplotsoccer
from mplsoccer import Pitch
from statsbombpy import sb
import matplotlib.pyplot as plt
from plotly_football_pitch import make_pitch_figure, PitchDimensions
import plotly.graph_objects as go
import numpy as np
from  datatable import fread

if 'temporada' not in st.session_state:
    st.session_state['temporada'] = None

if 'jogo' not in st.session_state:
    st.session_state['jogo'] = None

st.title('Passmap')

df_avg_position_by_player = fread('df_avg_position_by_player.csv').to_pandas()
df_duplas_loc = fread('df_duplas_loc.csv').to_pandas()

if st.session_state['temporada'] == 'Todas':
  st.session_state['temporada'] = '2020/2021'

temporadas = list(df_avg_position_by_player.temporada.unique())
temporada = st.sidebar.selectbox('Temporada', temporadas, index=temporadas.index(st.session_state['temporada']))
df_avg_position_by_player = df_avg_position_by_player[df_avg_position_by_player['temporada'] == temporada]


if temporada != st.session_state['temporada'] and temporada != "Todas":
    st.session_state['temporada'] = temporada
    st.session_state['jogo'] = None

jogos = list(df_avg_position_by_player[df_avg_position_by_player['temporada'] == temporada].Jogo.unique())
jogo_escolhido = st.session_state['jogo'] if st.session_state['jogo'] != None else jogos[0]
jogo = st.sidebar.selectbox('Jogo', jogos, jogos.index(jogo_escolhido))
st.session_state['jogo'] = jogo

avg_position_by_player = df_avg_position_by_player[(df_avg_position_by_player['temporada'] == temporada) & 
                                                   (df_avg_position_by_player['Jogo'] == jogo)]
duplas_loc = df_duplas_loc[(df_duplas_loc['temporada'] == temporada) & 
                              (df_duplas_loc['Jogo'] == jogo)]

min_passes = st.sidebar.slider('Mínimo de passes para haver conexão', 0, 30, 10)
duplas_loc = duplas_loc[duplas_loc['interaction'] > min_passes]

com_label = st.sidebar.checkbox('Labels visíveis', value=False)

mode = 'markers'
text = None
textposition = None
if com_label:
 mode = 'markers+text'
 text = avg_position_by_player.player
 textposition = 'middle center'
  
highlight_player = st.sidebar.selectbox('Destacar jogador', ['-'] + list(avg_position_by_player.player))
line_color = 'rgba(0,0,0,0.3)'
if highlight_player != '-':
  line_color = 'rgba(0,0,200,0.3)'



dimensions = PitchDimensions()
fig = make_pitch_figure(dimensions)

my_color = ('rgba('+str(np.random.randint(0, high = 256))+','+
                str(np.random.randint(0, high = 256))+','+
                str(np.random.randint(0, high = 256)))

for i,row in duplas_loc.iterrows():
  if (highlight_player in row.dupla) or (highlight_player == '-'):
    line_trace = go.Scatter(
        x=[row.x1,row.x2],
        y=[row.y1,row.y2],
        mode='lines',
        hoverinfo='none',  # Disable hover labels for the lines
        line=dict(color=line_color, width=row.interaction)
    )
    
    fig.add_trace(line_trace)

barca_red = '#A50044'
barca_blue = '#004D98'
colors = [barca_red if p != highlight_player else barca_blue for p in avg_position_by_player.player] 

fig.add_trace(go.Scatter(x=avg_position_by_player.x,
                         y=avg_position_by_player.y,
                         mode=mode, 
                         hovertext=avg_position_by_player.player,
                         text=text, #avg_position_by_player.player,  # Set the labels for each point
                         textposition=textposition, #'middle center',
                         hoverinfo='text',
                         marker=dict(size=(avg_position_by_player.interaction)/3 + 10, color=colors)))

fig.update_layout(
    showlegend=False  # Hide the legend
)

st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')

st.plotly_chart(fig)


