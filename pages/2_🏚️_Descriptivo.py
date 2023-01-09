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

import locale
locale.setlocale(locale.LC_ALL, '')
from folium.plugins import TagFilterButton


# %%
men_momney = lambda x: locale.currency(x, grouping=True)


st.title("Análisis Descriptivo")
st.sidebar.title('')
df = st.session_state['ofertas']
df = df.loc[df['ID_Estrato']!='campestre']

st.sidebar.header('Ingrese las filtros')

### filtro de Ciudad
ciudades = st.sidebar.selectbox("Ciudad",sorted(list(df['ciudad'].unique())))


### filtro precio 

precio_min = st.sidebar.number_input("Precio mínimo", value=100_000, step=50_000)
precio_max = st.sidebar.number_input("Precio Máximo", value=10_000_000, step=50_000)

### filtro por estrato

# Sidebar - Estratos
unique_pos = sorted(list(df['ID_Estrato'].unique()))
estrato= st.sidebar.multiselect('Estrato', unique_pos, unique_pos)

### filtro mapa cantidad de puntos

slider_puntos = st.sidebar.slider("Cantidad de Ofertas", min_value=1,
                                  max_value=300,step=10, value=50)


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
    csv = df.to_csv(index=False, sep=";",decimal=",")
    b64 = base64.b64encode(csv.encode('latin1')).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="Inmuebles{city}.csv">Download CSV File</a>'
    return href

def Map(df,city,cantidad_puntos):
    center_lat = df.query(f"ciudad == '{city}'").Latitud.values[0]
    center_lon = df.query(f"ciudad == '{city}'").Longitud.values[0]
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap',
        #tiles = "Stamen Toner",
        width='80%',
        ##Stamen Toner
    )
    #m.add_child(folium.LatLngPopup())
    
    conta = 0
    for i, row in df.iterrows():
        
        name = row.Indice
        lat = row.Latitud
        lon = row.Longitud
        estrato = row.ID_Estrato
        canon = men_momney(int(row.Canon))
        
        
        html = '<b>Codigo = {0}</br> <b>Canon = {1}</br>'.format(name,canon)
        iframe = folium.IFrame(html,
                               width=200, height=50)
        
        popup = folium.Popup(iframe,
                             max_width=210)
        
        # opened = row.codigo
        # HTML here in the pop up
        #### PABLOOOOOO SERIA CHEVERE EL CODIGO Y ADEMAS EL CANONO DE ARRENDAMIENTO
        
    
        folium.Marker([lat, lon], tooltip=canon,popup=popup, icon=folium.Icon(color='blue', icon='home'),
                      tags=[estrato]).add_to(m)
        conta+=1
        if conta==cantidad_puntos:
            break
    estra = df['ID_Estrato'].unique()
    categories = ['{0}'.format(i) for i in estra]
    categories = sorted(categories)
    TagFilterButton(categories).add_to(m)
    
    return m


df_filterin = Filtrandodataframe(df, ciudades, precio_min, precio_max,estrato) 
df_filterin['Indice'] = df_filterin.index


if boton:
    col1,col2 = st.columns(2)
    
    with col1:
        if not df_filterin.shape[0]==1:
            st.header("Diagrama distribución Canon")
            box =DiagramaCaja(df_filterin )
            st.plotly_chart(box, theme="streamlit", use_container_width=True)
        else:
            st.header("Diagrama distribución Canon")
            st.write("No es posible graficar debido que solo hay 1 oferta")
        
    with col2:
        if not df_filterin.shape[0]==1:
            st.header("Diagrama de Dispersión por estrato")
            scatter = Scatterplot(df_filterin )
            st.plotly_chart(scatter, theme="streamlit", use_container_width=True)
        else:
            st.header("Diagrama de Dispersión por estrato")
            st.write("No es posible graficar debido que solo hay 1 oferta")
            
    st.header("Mapa Distribución Ofertas")
    st.write("No se despliegan todos los puntos porque satura el mapa")
    st_data = folium_static(Map(df_filterin,ciudades,slider_puntos), width=1100)
    
    st.header("Datos Filtratos")
    st.write(df_filterin )
    st.markdown(filedownload(df_filterin ,
                             ciudades), unsafe_allow_html=True)
    
else:
    st.write("")




