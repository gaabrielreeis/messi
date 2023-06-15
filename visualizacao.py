#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px

st.set_page_config(layout="wide")

# Functions for each of the pages
def home(uploaded_file):
    if uploaded_file:
        st.text('Explore com o menu à esquerda')
    else:
        st.text('Para começar, carregue os datasets')
    image = Image.open('messi.jpg')
    st.image(image, caption='Lionel Messi comemora gol da vitória em Madri.')

def data_summary():
    st.header('Statistics of Dataframe')
    st.write(df.describe())

def data_header():
    st.header('Header of Dataframe')
    st.write(df.head())
    

def interactive_plot():
    col1, col2 = st.columns(2)
    
    x_axis_val = col1.selectbox('Select the X-axis', options=df.columns)
    y_axis_val = col2.selectbox('Select the Y-axis', options=df.columns)

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val)
    st.plotly_chart(plot, use_container_width=True)

# Add a title and intro text
st.title('Lionel Messi')

# Sidebar setup
upload_file = st.button('Load Datasets')
# upload_file = st.sidebar.file_uploader('Upload a file containing earthquake data')
#Sidebar navigation
st.sidebar.title('Sumário de Dados')
options = st.sidebar.radio('Selecione o que deseja ver:', ['Home', 'Data Summary', 'Data Header', 'Interactive Plots'])

# Check if file has been uploaded
if upload_file is not None:
    df = pd.read_csv('barca.csv',encoding= 'unicode_escape')
    st.session_state['df'] = df
    df_hm = pd.read_csv('messi_heatmap.csv')
    st.session_state['messi_heatmap'] = df_hm


# Navigation options
if options == 'Home':
    home(upload_file)
elif options == 'Data Summary':
    data_summary()
elif options == 'Data Header':
    data_header()
elif options == 'Interactive Plots':
    interactive_plot()