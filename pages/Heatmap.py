import streamlit as st
import pandas as pd
import matplotsoccer
from mplsoccer import Pitch
import scipy
import scipy.ndimage
import matplotlib.pyplot as plt
from datatable import fread

dfhm = fread('messi_heatmap.csv').to_pandas()

st.title('Heatmap')

if st.session_state['temporada'] == None:
    st.session_state['temporada'] = 'Todas'

temporadas = ['Todas'] + list(dfhm['temporada'].unique())
temporada = st.sidebar.selectbox('Temporada:', temporadas, index=temporadas.index(st.session_state['temporada']))

if temporada != st.session_state['temporada'] and temporada != "Todas":
    st.session_state['temporada'] = temporada
    st.session_state['jogo'] = None

if st.session_state['jogo'] == None:
    mando = 'Todos'
    adversario = 'Todos'
else:
    time1, time2 = st.session_state['jogo'].split(' x ')
    if time1 == 'Barcelona':
        mando = 'Casa'
        adversario = time2
    else:
        mando = 'Fora'
        adversario = time1



if temporada == 'Todas':
    norm_scale = st.sidebar.checkbox('Fixar Escalas', value=False)
    col1, col2 = st.columns(2)
    k = 0
    for season in dfhm['temporada'].unique():
        dfhm_filtered = dfhm[dfhm['temporada'] == season]

        hm = matplotsoccer.count(dfhm_filtered['x_messi'],dfhm_filtered['y_messi'],n=50,m=50)


        pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
                    pitch_color='#22312b', line_color='#efefef')
        # draw
        fig, ax = pitch.draw(figsize=(6.6, 4.125))
        fig.set_facecolor('#22312b')
        ax.set_title(str(season))
        bin_statistic = pitch.bin_statistic(dfhm_filtered['x_messi'],dfhm_filtered['y_messi'], statistic='count', bins=(35, 35))
        bin_statistic['statistic'] = scipy.ndimage.gaussian_filter(bin_statistic['statistic'], 1)
        if norm_scale:
            pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
        else:
            pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b', vmin=0, vmax=40)
        # Add the colorbar and format off-white
        cbar = fig.colorbar(pcm, ax=ax, shrink=0.6)
        cbar.outline.set_edgecolor('#efefef')
        cbar.ax.yaxis.set_tick_params(color='#efefef')
        ticks = plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#22312b')
        if k == 0:
            col1.pyplot(fig)
            k = 1
        else:
            col2.pyplot(fig)
            k = 0



else:
    dfhm_filtered = dfhm[dfhm['temporada'] == temporada]

    col1, col2 = st.sidebar.columns(2)
    
    opcoes_mando = ['Todos', 'Casa', 'Fora']
    mando = col1.selectbox('Mando de Campo', options=['Todos', 'Casa', 'Fora'], index=opcoes_mando.index(mando))
    opcoes_adversario = ['Todos']+list(dfhm_filtered.oponente.unique())
    try:
        opcoes_adversario.index(adversario)
    except:
        adversario = 'Todos'
    oponente = col2.selectbox('Adversário', options=opcoes_adversario, index=opcoes_adversario.index(adversario))
    norm_scale = st.sidebar.checkbox('Fixar Escalas', value=False)

    if mando == 'Fora':
        st.session_state['jogo'] = oponente + ' x ' + 'Barcelona' if oponente != 'Todos' else st.session_state['jogo']
    else:
        st.session_state['jogo'] = 'Barcelona' + ' x ' + oponente if oponente != 'Todos' else st.session_state['jogo']

    if mando != 'Todos' and oponente != 'Todos':
        dfhm_filtered = dfhm_filtered[(dfhm_filtered['oponente'] == oponente) & (dfhm_filtered['mando'] == mando)]
        vmax = 2
    elif mando != 'Todos' and oponente == 'Todos':
        dfhm_filtered = dfhm_filtered[(dfhm_filtered['mando'] == mando)]
        vmax = 15
    elif mando == 'Todos' and oponente != 'Todos':
        dfhm_filtered = dfhm_filtered[(dfhm_filtered['oponente'] == oponente)]
        vmax = 4
    else:
        vmax = 30
        pass

    

    hm = matplotsoccer.count(dfhm_filtered['x_messi'],dfhm_filtered['y_messi'],n=50,m=50)


    pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
                pitch_color='#22312b', line_color='#efefef')
    # draw
    fig, ax = pitch.draw(figsize=(6.6, 4.125))
    fig.set_facecolor('#22312b')
    bin_statistic = pitch.bin_statistic(dfhm_filtered['x_messi'],dfhm_filtered['y_messi'], statistic='count', bins=(35, 35))
    bin_statistic['statistic'] = scipy.ndimage.gaussian_filter(bin_statistic['statistic'], 1)

    if norm_scale:
        pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
    else:
        pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b', vmin=0, vmax=vmax)
    # Add the colorbar and format off-white
    cbar = fig.colorbar(pcm, ax=ax, shrink=0.6)
    cbar.outline.set_edgecolor('#efefef')
    cbar.ax.yaxis.set_tick_params(color='#efefef')
    ticks = plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#22312b')

    if len(dfhm_filtered) == 0:
        st.write("Messi não participou desta partida!")
    else:
        st.pyplot(fig)

st.session_state['jogo'] = st.session_state['jogo']
st.session_state['temporada'] = temporada