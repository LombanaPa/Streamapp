# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:37:58 2023

@author: ECM7985D
"""

import streamlit as st
import joblib
import pandas as pd
import numpy as np


st.title("Modelo por Tipo de Inmueble")
st.sidebar.title('Parámetros Predicción')
df = st.session_state['ofertas']
df = df.loc[df['ID_Estrato']!='campestre']


### filtro estrato 
# Sidebar - Estratos
unique_pos = sorted(list(df['ID_Estrato'].unique()))
estrato= st.sidebar.multiselect('Estrato', unique_pos, unique_pos)

### filtro area construida

area_construida = st.sidebar.number_input("Area Construida",min_value = 10.5)
area_privada = st.sidebar.number_input("Area Privada",min_value = 9.5)
antiguedad= st.sidebar.number_input("Antiguedad",min_value = 9.5)
piso= st.sidebar.slider("Piso",min_value = 1, max_value=30, step=1, value=5)
habitaciones= st.sidebar.slider("Habitaciones",min_value = 1, max_value=10, step=1, value=8)
banio= st.sidebar.slider("Baño",min_value = 1, max_value=10, step=1, value=4)
parqueadero =  st.sidebar.slider("Parqueadero",min_value = 1, max_value=10, step=1, value=2)
admin = st.sidebar.selectbox("Administración", ('SI','NO'))

### tipo

tipo = st.sidebar.selectbox("Tipo de Inmueble", df['Tipo'].unique())



def Modelo(tipo,estrato,area_cons,area_pri,antigue,piso,habitaciones,banio,parquedero,admin):
    mod = joblib.load(f"Modelo_{tipo}.pkl")
    X_predict = pd.DataFrame(columns = ['ID_Estrato', 'Area_Construida', 'Area_Privada',
       'Antiguedad', 'Piso', 'Habitaciones', 'Banios', 'Parqueadero',
       'Incluye_admin'])
    X_predict.loc[0] = [estrato,area_cons,area_pri
                        ,antigue,piso,habitaciones
                        ,banio,parquedero,admin]
    prediccion = mod.predict(X_predict)
    
    return X_predict

st.write(Modelo(tipo,estrato,area_construida,area_privada,antiguedad,piso,habitaciones,banio,
       parqueadero,admin))

