# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:27:26 2023

@author: Pablo Lombana
"""

import streamlit as st
import pandas as pd


st.set_page_config(page_title="Multipage App",
                   page_icon="馃憟", layout='wide')


st.title("Modelo para predicci贸n de arriendos en Colombia")
st.write("""
         
         ### Objetivo del Aplicativo
         
         El objetivo principal corresponde a crear una herramienta que permita,
         predecir el valor del inmueble en arriendo para que sea un insumo base
         que apoye la decisi贸n de asignaci贸n del precio del inmueble.
         
         #### Objetivos Especificos
         
         1. Mostrar el panorama de los inmuebles en arriendo actualmente.
         2. Crear herramientas de visualizaci贸n para estad铆stica descriptiva.
         3. Desarrollar un modelo para predecir el valor del arriendo.
         
         La informaci贸n utilizada para le modelo, fue producto de un webscrapping sobre
         paginas en Colombia que publican informaci贸n sobre inmuebles.
         
         La informaci贸n descargada de inmuebles proviene de las paginas, por ende,
         **esta sujeta a lo que las personas ingresan directamente a cada portal y esto
         puede generar alguna inconsistencia con la informaci贸n.**
         
         Este producto **NO REPRESENTA UN AN脕LISIS PROFUNDO Y TAMPOCO SE RECOMIENDA
         PARA ASIGNAR UN VALOR DEL ARRIENDO** pero puede ser utilizado como aproximaci贸n.
         
         Creado por 
         Pablo Andr茅s Lombana
         
         """)



def ReadingData():
    df = pd.read_csv("Ofertas_finales.csv",sep="|")
    df.rename(columns={'ID_Subtipo':'Tipo'},inplace=True)
    #df.drop(['Unnamed: 0.1','index_right','Unnamed: 0'],axis=1, inplace=True)
    return df
ofertas = ReadingData()
st.session_state['ofertas'] = ofertas

#st.sidebar.success("Select a page above")


