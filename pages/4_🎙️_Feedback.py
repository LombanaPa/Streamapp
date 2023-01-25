# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 16:37:58 2023

@author: ECM7985D
"""

import streamlit as st
import pandas as pd
import numpy as np
import os

from streamlit_extras.let_it_rain import rain




st.title("Comentarios")
x = st.slider('Por favor escoge el ranking que le das a la app',1,5,value=3,step=1)
st.sidebar.markdown('''Esta pagina es para que por favor califiques tu experiencia con la app,
                 sabemos que no es la mejor y por ende, trataré de desarrollar algo mejor para que cumpla tus expectivas,
                 pero te pido que por favor nos califiques y dejes tu comentario!! Así sabré que es necesario
                 para mejorar y ayudarte en tu labor.''')

if x==1:
	#st.markdown(":star: Lamento no llenar tus expectativas, prometo mejorar, ¿Podrías indicarnos que no te gustó?")
    repuesta=1
    st.markdown(":star: Lamento no llenar tus expectativas, prometo mejorar, ¿Podrías indicarnos que no te gustó?")
elif x==2:
    repuesta=2
    st.markdown(":star::star: Vaya!, fue mala tu calificación, lamento no poder cumplir completamente tu expectativa, voy a mejorar! deja tu comentario por favor.")
elif x==3:
    repuesta=3
    st.markdown(":star::star::star: Pasar raspando, supongo que hay mucho por hacer,por favor deja tu comentario y te aseguro que voy a mejorar.")	
elif x==4:
    repuesta=4
    st.markdown(":star::star::star::star: Super, me alegra ser de tu ayud ¿Qué nos faltaría para ser mejores? deja tu comentario.")
elif x==5:
    repuesta=5
    st.markdown(":star::star::star::star::star: Genial, que alegría ver que te gustó ¿Piensas que podemos adicionar algo más? Cuentanos!!!")

texto = st.text_area("Ingresa tu comentario por favor! y muchas gracias por usar la aplicación 👇")

boton = st.button("Enviar Califiación")
if boton:
    guardar_comentarios = pd.DataFrame(columns=['Calificacion','Comentario'])
    aleatorio = np.random.randint(0,10000000)
    guardar_comentarios.loc[0,'Calificacion'] = repuesta
    guardar_comentarios.loc[0,'Comentario'] = texto
    guardar_comentarios.to_csv(f"D:\PABLO\Streamapp/comentarios/respuesta{aleatorio}_{aleatorio}.csv",sep=";", index=False)
    rain(
        emoji="👍",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )

    
    
    
    

 


