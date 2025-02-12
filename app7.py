# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 17:47:27 2025

@author: jperezr
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Análisis de Riesgo y Rentabilidad - PENSIONISSSTE", layout="wide")

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Título principal
st.title("Análisis de Riesgo y Rentabilidad de la Cartera de PENSIONISSSTE")
st.markdown("""
Esta aplicación permite evaluar el riesgo y la rentabilidad de una cartera de inversiones utilizando simulaciones de Monte Carlo.
""")

# Sidebar: Botón de descarga y sección de ayuda
with st.sidebar:
    # Botón para descargar el archivo PDF
    with open("riesgo_inversion.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        st.download_button(
            label="Descargar Manual de la Aplicación",
            data=pdf_bytes,
            file_name="riesgo_inversion.pdf",
            mime="application/pdf"
        )
    
    st.header("Ayuda")
    st.write("""
    ### ¿Qué hace esta aplicación?
    Esta aplicación simula el comportamiento futuro de una cartera de inversiones utilizando la técnica de **Simulación de Monte Carlo**. 
    El objetivo es evaluar el **riesgo** y la **rentabilidad** de la cartera, considerando la volatilidad y correlación entre los instrumentos de inversión.
    
    ### Instrumentos de Inversión
    La cartera está compuesta por 5 instrumentos:
    1. **Acciones**: Activos de alto riesgo y alta rentabilidad.
    2. **Bonos**: Activos de bajo riesgo y rentabilidad moderada.
    3. **Fondos Inmobiliarios**: Inversiones en bienes raíces con riesgo y rentabilidad intermedia.
    4. **ETF**: Fondos cotizados que replican índices o sectores.
    5. **Divisas**: Monedas extranjeras con riesgo asociado a fluctuaciones cambiarias.
    
    ### Parámetros de la Simulación
    - **Días de Proyección**: Número de días para proyectar los rendimientos.
    - **Número de Simulaciones**: Cantidad de escenarios simulados.
    - Los resultados se actualizan automáticamente al cambiar los parámetros.
    """)
    
    st.markdown("---")
    st.write("Desarrollado por: **Javier Horacio Pérez Ricárdez**")
    st.write("© 2025 Derechos Reservados")
