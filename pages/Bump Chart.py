import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from  datatable import fread
from PIL import Image

st.title('Bump Chart')

st.write("Ranking de jogadores que mais trocaram \npasses com Messi ao longo das temporadas.")

df_duplas_loc = fread('df_duplas_loc.csv').to_pandas()

df_duplas_loc['player1'] = df_duplas_loc['dupla'].apply(lambda x: x.split('_')[0])
df_duplas_loc['player2'] = df_duplas_loc['dupla'].apply(lambda x: x.split('_')[1])

df_duplas_messi = df_duplas_loc[(df_duplas_loc['player1'] == 'Lionel Andrés Messi Cuccittini') |
              (df_duplas_loc['player2'] == 'Lionel Andrés Messi Cuccittini')]
df_duplas_messi['dupla'] = df_duplas_messi['dupla'].apply(lambda x: x.replace('Lionel Andrés Messi Cuccittini','').replace('_',''))
df_duplas_messi = df_duplas_messi.groupby(['temporada', 'dupla']).sum().reset_index()
df_duplas_messi.groupby('temporada').apply(lambda x: x.nlargest(10, 'interaction')).reset_index(drop=True)#.query("temporada == '2006/2007'")
df_duplas_messi['rank'] = df_duplas_messi.groupby('temporada')['interaction'].rank(ascending=False, method='dense')

df_duplas_messi_ranked = df_duplas_messi[df_duplas_messi['rank'] <= 10]

de_para = pd.DataFrame({
    'temporada' : df_duplas_messi_ranked['temporada'].unique(),
    'index_temporada': range(0,16)
})

# List of players categorized by position
player_position = {
'atacantes' : [
    'Samuel Eto''o Fils',
    'David Villa Sánchez',
    'Zlatan Ibrahimović',
    'Neymar da Silva Santos Junior',
    'Antoine Griezmann',
    'Pedro González López',
    'Thierry Henry',
    'Ousmane Dembélé',
     'Luis Alberto Suárez Díaz',
    'Pedro Eliezer Rodríguez Ledesma',
    "Samuel Eto''o Fils",
    'Ronaldo de Assis Moreira',
],

'zagueiros' : [
    'Carles Puyol i Saforcada',
    'Gerard Piqué Bernabéu',
    'Lilian Thuram',
    'Eric-Sylvain Bilal Abidal',
    'Javier Alejandro Mascherano',
    'Clément Lenglet',
    'Óscar Mingueza García'
],

'meio-campistas' : [
    'Andrés Iniesta Luján',
    'José Edmílson Gomes de Moraes',
    'Juliano Haus Belletti',
    'Mark van Bommel',
    'Rafael Márquez Álvarez',
    'Xavier Hernández Creus',
    'Giovanni van Bronckhorst',
    'Gnégnéri Yaya Touré',
    'Sergio Busquets i Burgos',
    'Maxwell Scherrer Cabelino Andrade',
    'Seydou Kéita',
    'Alexis Alejandro Sánchez Sánchez',
    'Francesc Fàbregas i Soler',
    'Thiago Alcântara do Nascimento',
    'Alexandre Dimitri Song-Billong',
    'Ivan Rakitić',
    'Arturo Erasmo Vidal Pardo',
    'Frenkie de Jong',
    'Arthur Henrique Ramos de Oliveira Melo',
    'Philippe Coutinho Correia',
    'José Paulo Bezzera Maciel Júnior',
    'André Filipe Tavares Gomes',
    'Anderson Luís de Souza'
],

'laterais' : [
    'Daniel Alves da Silva',
    'Jordi Alba Ramos',
    'Adriano Correia Claro',
    'Nélson Cabral Semedo',
    'Sergiño Dest',
    'Sergino Dest',
    'Sylvio Mendes Campos Junior',
    'Gianluca Zambrotta',
    'Oleguer Presas Renom',
    'Sergi Roberto Carnicer',
]
}

barca_red = '#A50044'
barca_blue = '#004D98'
barca_yellow = '#EDBB00'
barca_lavender = '#827DC2'

cores = {
  'atacantes':barca_red,
  'meio-campistas':barca_lavender,
  'zagueiros':barca_blue,
  'laterais':barca_yellow
}

options = st.sidebar.multiselect(
    'Posições',
    player_position.keys(),
    player_position.keys())

por_posicao = st.sidebar.checkbox('Cores por posição', True)

image_campo = Image.open('campo_posicoes.jpeg')
st.sidebar.image(image_campo, caption='',width=300)

jogadores = []
for option in options:
  jogadores += player_position[option]


fig = go.Figure()
for dupla in jogadores:
  dfr = df_duplas_messi_ranked[df_duplas_messi_ranked['dupla'] == dupla].sort_values('temporada').reset_index()
  dfr = dfr.merge(de_para)
  for option in options:
    if dupla in player_position[option]:
      cor = cores[option]
  if por_posicao:
    fig.add_trace(go.Scatter(x=dfr.index_temporada, y=dfr['rank'], mode='lines+markers', name=dupla, marker=dict(size=9),
                           hovertemplate=f'{dupla}<extra></extra>'.format(dupla), line_shape='spline', line=dict(color=cor)))
  else:
    fig.add_trace(go.Scatter(x=dfr.index_temporada, y=dfr['rank'], mode='lines+markers', name=dupla, marker=dict(size=9),
                           hovertemplate=f'{dupla}<extra></extra>'.format(dupla), line_shape='spline'))
fig.update_layout(
    barmode='group',
    xaxis_title='Temporada',
    yaxis_title='Rank',
    yaxis=dict(autorange='reversed',
               tickvals = list(range(1,17))),
    xaxis=dict(
        tickmode = 'array',
        tickvals = de_para.index_temporada.to_list(),
        ticktext = de_para.temporada.to_list(),
        tickangle=40
    )
)

st.plotly_chart(fig)



