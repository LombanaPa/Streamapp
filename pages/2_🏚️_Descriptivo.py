# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:32:44 2023

@author: ECM7985D
"""

import streamlit as st

st.title("Análisis Descriptivo")
st.sidebar.title('')
df = st.session_state['ofertas']

st.header('Statistics of Dataframe')
st.write(df.head(10))



