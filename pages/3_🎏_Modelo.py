# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:37:58 2023

@author: ECM7985D
"""

import streamlit as st
import joblib
st.title("Modelo")

modelo = joblib.load("../Modelo.pkl")


