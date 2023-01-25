# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:37:58 2023

@author: ECM7985D
"""

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.express as px


st.title("Modelo por Tipo de Inmueble")
st.sidebar.title('Parámetros Predicción')
df = st.session_state['ofertas']
df = df.loc[df['ID_Estrato']!='campestre']


### filtro estrato 
# Sidebar - Estratos
unique_pos = sorted(list(df['ID_Estrato'].unique()))


### filtro area construida
estrato= st.sidebar.selectbox('Estrato', unique_pos)
area_construida = st.sidebar.number_input("Area Construida",min_value = 30.5)
area_privada = st.sidebar.number_input("Area Privada",min_value = 29.5)
antiguedad= st.sidebar.number_input("Antiguedad",min_value = 1)
piso= st.sidebar.slider("Piso",min_value = 1, max_value=30, step=1, value=5)
habitaciones= st.sidebar.slider("Habitaciones",min_value = 0, max_value=10, step=1, value=1)
banio= st.sidebar.slider("Baño",min_value = 1, max_value=10, step=1, value=4)
parqueadero =  st.sidebar.slider("Parqueadero",min_value = 0, max_value=10, step=1, value=2)
admin = st.selectbox("Administración", ('SI','NO'))


### tipo

tipo = st.selectbox("Tipo de Inmueble", df['Tipo'].unique())
boton = st.sidebar.button("Ejecutar")

def Histograma(df_ingreso,est,typee):
    df_ingreso = df_ingreso.query(f"ID_Estrato=='{est}' and Tipo=='{typee}'")
    mean = np.mean(df_ingreso['Canon'])
    std = np.std(df_ingreso['Canon'])

    fig= px.histogram(df_ingreso.loc[(df_ingreso ['Canon']>mean-1*std)\
                                     &(df_ingreso ['Canon']<mean+1*std)],
                        x='Canon',
                        nbins=100, template='plotly_white', title='Histograma Precio Canon')
    fig.update_xaxes(title='Canon')#title_font_family="Arial")
    return fig

def Modelo(tipo,estrato,area_cons,area_pri,antigue,piso,habitaciones,banio,parquedero,admin):
    mod = joblib.load(f"Modelo_{tipo}.pkl")
    X_predict = pd.DataFrame(columns = ['ID_Estrato', 'Area_Construida', 'Area_Privada',
       'Antiguedad', 'Piso', 'Habitaciones', 'Banios', 'Parqueadero',
       'Incluye_admin'])
    X_predict.loc[0] = [estrato,area_cons,area_pri
                        ,antigue,piso,habitaciones
                        ,banio,parquedero,admin]
    
    prediccion = mod.predict(X_predict)
    X_predict.rename(columns={'ID_Estrato':'Estrato','Incluye_admin':'Administración'},inplace=True)
    return X_predict,prediccion


if boton:
    if area_construida<=area_privada:
        st.write("El área construida es menor que el área privada, por \
                 favor ajustar")
    
    else:
        histo = Histograma(df, estrato, tipo)
        st.plotly_chart(histo)
        data_predict,predi = Modelo(tipo,estrato,area_construida,area_privada,antiguedad,piso,habitaciones,banio,
               parqueadero,admin)
        data_predict['Predicción'] = predi
        
        st.write(data_predict)
else:
    st.write("")

