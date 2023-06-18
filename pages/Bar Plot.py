import streamlit as st
import pandas as pd
import plotly.express as px
from datatable import fread

barca_red = '#A50044'
barca_blue = '#004D98'

df = fread('barca.csv').to_pandas()

df=df[['Rating','Gols','Gols_Falta', 'Dribles_Certos','Gols_Penalti','Temporada']]
st.title('Bar Plot')

temp=df[['Rating','Gols','Gols_Falta', 'Dribles_Certos','Gols_Penalti','Temporada']]
column_options = temp.columns.tolist()
column_options.remove('Temporada')

selected_columns = st.selectbox('Select Columns to Display', column_options)


if selected_columns== 'Rating':
    teste = df.groupby(['Temporada']).mean()['Rating']
    plot = px.bar(teste, y='Rating',color_discrete_sequence=[barca_blue])
    plot.add_vrect(x0=4.5, x1=4.5000001, line_width=1, line_dash="dash", line_color=barca_red, fillcolor="red", opacity=1)
    plot.add_annotation(
        x=4.5,
        y=max(teste)*1.3,
        text="Saída\n do Messi\n do Barcelona",
        showarrow=False,
        font=dict(color=barca_red)
    )
    st.plotly_chart(plot, use_container_width=True)
else:
    teste = df.groupby(['Temporada']).sum()[selected_columns]
    plot = px.bar(teste, y=selected_columns,color_discrete_sequence=[barca_blue])
    plot.add_vrect(x0=4.5, x1=4.5000001, line_width=1, line_dash="dash", line_color=barca_red, fillcolor="red",
                   opacity=1)
    plot.add_annotation(
        x=4.5,
        y=max(teste),
        text="Saida\n do Messi\n do Barcelona",
        showarrow=False,
        font=dict(color=barca_red)
    )
    st.plotly_chart(plot, use_container_width=True)
