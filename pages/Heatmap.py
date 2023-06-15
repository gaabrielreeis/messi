import streamlit as st
import pandas as pd
import matplotsoccer
from mplsoccer import Pitch
import scipy
import scipy.ndimage
import matplotlib.pyplot as plt

dfhm = st.session_state['messi_heatmap']

st.title('Heatmap')

temporada = st.sidebar.selectbox('Temporada:', ['Todas'] + list(dfhm['temporada'].unique()))

if temporada == 'Todas':
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
        pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
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
        
    mando = col1.selectbox('Mando de Campo', options=['Todos', 'Casa', 'Fora'])
    oponente = col2.selectbox('Adversário', options=['Todos']+list(dfhm_filtered.oponente.unique()))

    if mando != 'Todos' and oponente != 'Todos':
        dfhm_filtered = dfhm_filtered[(dfhm_filtered['oponente'] == oponente) & (dfhm_filtered['mando'] == mando)]
    elif mando != 'Todos' and oponente == 'Todos':
        dfhm_filtered = dfhm_filtered[(dfhm_filtered['mando'] == mando)]
    elif mando == 'Todos' and oponente != 'Todos':
        dfhm_filtered = dfhm_filtered[(dfhm_filtered['oponente'] == oponente)]
    else:
        pass

    hm = matplotsoccer.count(dfhm_filtered['x_messi'],dfhm_filtered['y_messi'],n=50,m=50)


    pitch = Pitch(pitch_type='statsbomb', line_zorder=2,
                pitch_color='#22312b', line_color='#efefef')
    # draw
    fig, ax = pitch.draw(figsize=(6.6, 4.125))
    fig.set_facecolor('#22312b')
    bin_statistic = pitch.bin_statistic(dfhm_filtered['x_messi'],dfhm_filtered['y_messi'], statistic='count', bins=(35, 35))
    bin_statistic['statistic'] = scipy.ndimage.gaussian_filter(bin_statistic['statistic'], 1)
    pcm = pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')
    # Add the colorbar and format off-white
    cbar = fig.colorbar(pcm, ax=ax, shrink=0.6)
    cbar.outline.set_edgecolor('#efefef')
    cbar.ax.yaxis.set_tick_params(color='#efefef')
    ticks = plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#22312b')

    st.pyplot(fig)
