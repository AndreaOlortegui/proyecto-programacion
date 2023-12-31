import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="Dashboard", layout='wide', initial_sidebar_state='auto')
st.title('POSITIVOS COVID-19 - 2023')
data = pd.read_csv("positivos_covid_2023.csv")
data["FECHA_RESULTADO"] = data["FECHA_RESULTADO"].astype(str).str.replace(",", "").str.split(".", expand=True)[0]
data["FECHA_RESULTADO"] = pd.to_datetime(data["FECHA_RESULTADO"], format="%Y%m%d", errors='coerce').dt.strftime("%Y%m%d")
num_filas = len(data)-1
year_filter_options = [2023]
year_filter = st.sidebar.radio("Filtrar por año", year_filter_options)
df_filtered = data[data["FECHA_RESULTADO"].str.startswith(str(year_filter))]
num_filas_filtrado = len(df_filtered) - 1
porcentaje_total = (num_filas / num_filas) * 100
porcentaje_filtrado = (num_filas_filtrado / num_filas) * 100
fig = go.Figure()
fig.add_trace(go.Bar(
    y=["Durante el año: "+str(num_filas_filtrado), "Total: "+str(num_filas)],
    x=[porcentaje_filtrado, porcentaje_total],
    orientation='h',
    marker=dict(
        color=['#ff7f0e','#1f77b4']
    ),
    text=[f"{porcentaje_filtrado:.2f}%", f"{porcentaje_total:.2f}%"],
    textposition="inside"
))
fig.update_layout(
    title="Total de positivos covid",
    xaxis_title="Porcentaje",
    yaxis_title="",
    showlegend=False
)
st.plotly_chart(fig)
count_by_department = df_filtered["DEPARTAMENTO"].value_counts().reset_index()
count_by_department.columns = ["Departamento", "Total"]
colors = px.colors.qualitative.Plotly
fig = px.bar(count_by_department, x="Departamento", y="Total", title="Positivos COVID-19 por Departamento", color="Departamento", color_discrete_sequence=colors)
st.plotly_chart(fig)
count_by_method = df_filtered["METODODX"].value_counts().reset_index()

count_by_method.columns = ["Metodo", "Total"]
count_by_method = count_by_method[count_by_method["Metodo"].isin(["AG", "PCR", "PR"])]

fig = px.bar(count_by_method, x="Metodo", y="Total", title="Tipo de prueba", color="Metodo", color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig)
count_by_sex = df_filtered["SEXO"].value_counts().reset_index()
count_by_sex.columns = ["Sexo", "Conteo"]
fig = px.pie(count_by_sex, values="Conteo", names="Sexo", title="Conteo por sexo")
st.plotly_chart(fig)
st.balloons()