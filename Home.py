#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px

st.set_page_config(layout="wide")

# Functions for each of the pages
def home():
    st.header('Carreira no Barcelona Através dos Dados')
    image = Image.open('messi.jpg')
    st.image(image, caption='',width=800)

def data_summary():
    st.header('Statistics of Dataframe')
    st.write("""A principal fonte será a plataforma de coleta de dados esportivos StatsBomb, 
             que fornece gratuitamente dados de evento para todos os jogos do Barcelona na liga
               espanhola entre as temporadas 2004/05 e 2020/21. Dados de evento contemplam 
               praticamente todas as ações de jogadores individuais durante uma partida, além
                 de colunas descritivas que caracterizam a ação.""")
    
    image1 = Image.open('Statsbomb_Logo.jpg')
    st.image(image1, caption='',width=500)
    
    st.write("""A plataforma SofaScore é uma fonte de dados de futebol que fornece estatísticas
      de jogadores, notas de desempenho, dados de jogos, informações sobre ligas e competições,
        e dados de equipe. Sua grande vantagem é a avaliação de desempenho atribuída aos jogadores,
          que varia de 3 a 10, baseada em diversas métricas. Com isso, podemos, por exemplo, criar
            um gráfico iterativo para avaliar o jogador argentino em cada fase de sua carreira.""")
    
    image2 = Image.open('sofascore.png')
    st.image(image2, caption='',width=500)
    
def data_header():
    st.header('Motivação')

    st.write("""A principal motivação para escolhermos o tema de visualização de dados é a nossa paixão pelo futebol
      e o reconhecimento de Lionel Messi como um dos maiores jogadores da história desse esporte. Sua magnitude como
        jogador é inegável, com uma carreira repleta de conquistas e recordes impressionantes. Além disso, observamos
          que a área de "Football Analytics" vem crescendo tanto no Brasil quanto no mundo, com exemplos de sucesso
            como o Brentford, da Inglaterra, que utiliza um modelo de prospecção de jogadores baseado em análise de
              dados, e o Atlético Mineiro, pioneiro em analytics no Brasil.""")

    st.write(""" Nossa expectativa é que esta plataforma forneça insights valiosos sobre o desempenho de Messi e sua contribuição
          para o sucesso de sua equipe. Acreditamos que como estas são fundamentais para compreendermos melhor o desempenho
            de jogadores de futebol, suas tendências e estratégias, bem como as técnicas consolidadas na área de Football
              Analytics. """)



# Add a title and intro text
st.title('Lionel Messi')

# Sidebar setup
# upload_file = st.sidebar.file_uploader('Upload a file containing earthquake data')
# Sidebar navigation
st.sidebar.title('Sumário de Dados')
options = st.sidebar.radio('Selecione o que deseja ver:', ['Home', 'Fontes de Dados', 'Motivação'])

st.session_state['temporada'] = None
st.session_state['jogo'] = None

# Navigation options
if options == 'Home':
    home()
elif options == 'Fontes de Dados':
    data_summary()
elif options == 'Motivação':
    data_header()