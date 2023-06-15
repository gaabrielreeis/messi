import streamlit as st
import pandas as pd
import matplotsoccer
from mplsoccer import Pitch
from statsbombpy import sb
import matplotlib.pyplot as plt
from plotly_football_pitch import make_pitch_figure, PitchDimensions
import plotly.graph_objects as go
import numpy as np

st.title('Passmap')



laliga = sb.competitions().query("competition_name == 'La Liga'")


temporada = st.sidebar.selectbox('Temporada', laliga.season_name)
temporada_escolhida = laliga[laliga['season_name'] == temporada].iloc[0]

jogos_temporada = sb.matches(competition_id=temporada_escolhida.competition_id, season_id=temporada_escolhida.season_id)
jogos_temporada['Jogo'] = jogos_temporada['home_team'] + ' x ' + jogos_temporada['away_team'] 
jogo = st.sidebar.selectbox('Jogo', jogos_temporada.Jogo)

ht, at = jogo.split(' x ')
jogo_escolhido = jogos_temporada[(jogos_temporada['home_team'] == ht) & (jogos_temporada['away_team'] == at)].iloc[0].match_id

events = sb.events(match_id=jogo_escolhido)

StartingXI = [x['player']['name'] for x in events[(events['type'] == 'Starting XI') & (events['team'] == 'Barcelona')].iloc[0].tactics['lineup']]

events = events[(events['type'] == 'Pass')]
events = events[(events['player'].isin(StartingXI)) & (events['pass_recipient'].isin(StartingXI))]
events = events.query("""
 team == 'Barcelona' 
""")
events.dropna(subset=['pass_recipient', 'player'], inplace=True)

events['x'] = events['location'].apply(lambda row: row[0])
events['y'] = events['location'].apply(lambda row: row[1])
events['y'] = 75 - events['y']
avg_position_by_player = events.groupby('player').mean()[['x', 'y']].reset_index()

df = events[['pass_recipient', 'player']].rename(columns={'pass_recipient':'player1', 'player':'player2'})
df = df.dropna()

import pandas as pd

# Assuming your dataframe is called 'df'
# df = pd.DataFrame({'player1': ['John', 'Alice', 'Bob', 'Alice'],
#                    'player2': ['Alice', 'Bob', 'John', 'John']})

# Concatenate the two columns with a separator to create a combined column
df['combination'] = df[['player1', 'player2']].apply(lambda x: '_'.join(sorted(x)), axis=1)

# Count the occurrences of each combination
combination_counts = df['combination'].value_counts()

duplas = pd.DataFrame(combination_counts).reset_index().rename(columns={'index':'dupla'})
duplas['player1'] = duplas['dupla'].apply(lambda x: x.split('_')[0])
duplas['player2'] = duplas['dupla'].apply(lambda x: x.split('_')[1])
duplas['interaction'] = duplas['combination']

avg_position_by_player['loc'] = avg_position_by_player.apply(lambda row: np.array([row.x, row.y]), axis=1)
pos = {}
for i, row in avg_position_by_player[['player', 'loc']].iterrows():
  pos[row['player']] = np.array(row['loc'])

duplas_loc = duplas.merge(avg_position_by_player[['player','x','y']], left_on='player1', right_on='player').rename(columns={'x':'x1','y':'y1'})
duplas_loc = duplas_loc.merge(avg_position_by_player[['player','x','y']], left_on='player2', right_on='player').rename(columns={'x':'x2','y':'y2'})

player_interactions = pd.concat([duplas_loc[['player1', 'interaction']].rename(columns={'player1':'player'}),
                                 duplas_loc[['player2', 'interaction']].rename(columns={'player2':'player'})])
player_interactions = player_interactions.groupby('player').sum().reset_index()

avg_position_by_player = avg_position_by_player.merge(player_interactions, how='left').fillna(0)


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

colors = ['rgba(255,0,0,1)' if p != highlight_player else 'rgba(100,100,255,1)' for p in avg_position_by_player.player] 

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