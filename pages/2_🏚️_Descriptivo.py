# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:32:44 2023

@author: ECM7985D
"""

import streamlit as st
import plotly.express as px
import base64
import numpy as np
import pandas as pd
from streamlit_folium import folium_static
import folium

st.title("Análisis Descriptivo")
st.sidebar.title('')
df = st.session_state['ofertas']
df = df.loc[df['ID_Estrato']!='campestre']

st.sidebar.header('Ingrese las filtros')

### filtro de Ciudad
ciudades = st.sidebar.selectbox("Ciudad",sorted(list(df['ciudad'].unique())))


### filtro precio 

precio_min = st.sidebar.number_input("Precio mínimo", value=100_000)
precio_max = st.sidebar.number_input("Precio Máximo", value=1_000_000)

### filtro por estrato

# Sidebar - Estratos
unique_pos = sorted(list(df['ID_Estrato'].unique()))
estrato= st.sidebar.multiselect('Estrato', unique_pos, unique_pos)

boton = st.sidebar.button("Ejecutar")


def Filtrandodataframe(df_fil,ciuda,pre_min,pre_max,estra):
    return df_fil.loc[(df_fil['ciudad']==ciuda)&
                      (df_fil['Canon']>=pre_min)&
                      (df_fil['Canon']<=pre_max)&(df_fil['ID_Estrato'].isin(estra))].\
        reset_index(drop=True)

def DiagramaCaja(df):
    fig = px.box(df, x='Canon',notched=True)
    return fig

def Scatterplot(df):
    fig = px.scatter(df,
            y='Canon', x='Area_Construida',size='Area_Privada',color='ID_Estrato', 
       category_orders ={"ID_Estrato":['0','1','2','3','4','5','6','campestre']} )
    
    return fig
                 
def filedownload(df,city):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="Inmuebles{city}.csv">Download CSV File</a>'
    return href

def Map(df,city):
    center_lat = df.query(f"ciudad == '{city}'").Latitud.values[0]
    center_lon = df.query(f"ciudad == '{city}'").Longitud.values[0]
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap',
        width='80%',
        ##Stamen Toner
    )
    m.add_child(folium.LatLngPopup())
    
    conta = 0
    for i, row in df.iterrows():
        
        name = row.Indice
        lat = row.Latitud
        lon = row.Longitud
        # opened = row.codigo
        # HTML here in the pop up
        #### PABLOOOOOO SERIA CHEVERE EL CODIGO Y ADEMAS EL CANONO DE ARRENDAMIENTO
        popup = '<b>Codigo= {}</br>'.format(name)
    
        folium.Marker([lat, lon], tooltip=name,popup=popup, icon=folium.Icon(color='green', icon='cloud'),
                      ).add_to(m)
        conta+=1
        if conta==100:
            break
    return m


df_filterin = Filtrandodataframe(df, ciudades, precio_min, precio_max,estrato) 

df_filterin['Indice'] = df_filterin.index


if boton:
    col1,col2 = st.columns(2)
    
    with col1:
        st.header("Diagrama distribución Canon")
        box =DiagramaCaja(df_filterin )
        st.plotly_chart(box, theme="streamlit", use_container_width=True)
        
    with col2:
        st.header("Diagrama de Dispersión por estrato")
        scatter = Scatterplot(df_filterin )
        st.plotly_chart(scatter, theme="streamlit", use_container_width=True)
    
    st_data = folium_static(Map(df_filterin,ciudades), width=1100)
    
    st.header("Datos Filtratos")
    st.write(df_filterin )
    st.markdown(filedownload(df_filterin ,
                             ciudades), unsafe_allow_html=True)
    
else:
    st.write("")




