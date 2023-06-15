import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = st.session_state['df']

st.header('Plot of Data')
    
fig, ax = plt.subplots(1,1)
ax.scatter(x=df['Idade'], y=df['Renda'])
ax.set_xlabel('Depth')
ax.set_ylabel('Magnitude')
    
st.pyplot(fig)
