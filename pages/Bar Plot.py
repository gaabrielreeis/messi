import streamlit as st
import pandas as pd
import plotly.express as px

df = st.session_state['df']

df=df[['Rating','Gols','Gols_Falta', 'Dribles_Certos','Gols_Penalti','Temporada']]
st.title('Bar Plot')

selected_columns = st.selectbox('Select Columns to Display', df.columns)

if selected_columns== 'Rating':
    teste = df.groupby(['Temporada']).mean()['Rating']
    plot = px.bar(teste, y='Rating')
    plot.add_vrect(x0=4.5, x1=4.5000001, line_width=1, line_dash="dash", line_color="gray", fillcolor="red", opacity=0.7)
    plot.add_annotation(
        x=4.5,
        y=max(teste)*1.3,
        text="Saida\n do Messi\n do Barcelona",
        showarrow=False,
        font=dict(color="black")
    )
    st.plotly_chart(plot, use_container_width=True)
else:
    teste = df.groupby(['Temporada']).sum()[selected_columns]
    plot = px.bar(teste, y=selected_columns)
    plot.add_vrect(x0=4.5, x1=4.5000001, line_width=1, line_dash="dash", line_color="gray", fillcolor="red",
                   opacity=0.7)
    plot.add_annotation(
        x=4.5,
        y=max(teste),
        text="Saida\n do Messi\n do Barcelona",
        showarrow=False,
        font=dict(color="black")
    )
    st.plotly_chart(plot, use_container_width=True)
