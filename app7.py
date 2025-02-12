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

# Sidebar: Sección de ayuda y créditos
with st.sidebar:
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
    st.write("© 2023 Derechos Reservados")

# Generar datos simulados para 5 instrumentos
@st.cache_data
def generar_datos_simulados():
    np.random.seed(42)  # Para reproducibilidad
    dias = 252 * 5  # 5 años de datos (252 días hábiles por año)
    instrumentos = ["Acciones", "Bonos", "Fondos Inmobiliarios", "ETF", "Divisas"]
    
    # Parámetros de cada instrumento (rendimiento promedio y volatilidad)
    parametros = {
        "Acciones": {"rendimiento": 0.0008, "volatilidad": 0.02},
        "Bonos": {"rendimiento": 0.0003, "volatilidad": 0.005},
        "Fondos Inmobiliarios": {"rendimiento": 0.0005, "volatilidad": 0.01},
        "ETF": {"rendimiento": 0.0006, "volatilidad": 0.015},
        "Divisas": {"rendimiento": 0.0002, "volatilidad": 0.008},
    }
    
    # Generar rendimientos diarios para cada instrumento
    datos = {}
    for instrumento in instrumentos:
        rendimientos = np.random.normal(
            parametros[instrumento]["rendimiento"],
            parametros[instrumento]["volatilidad"],
            dias
        )
        datos[instrumento] = rendimientos
    
    # Crear un DataFrame con fechas y rendimientos
    fechas = pd.date_range(start="2018-01-01", periods=dias, freq="B")  # Fechas hábiles
    df = pd.DataFrame(datos, index=fechas)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Fecha"}, inplace=True)
    return df

data = generar_datos_simulados()

# Mostrar datos
st.subheader("Datos Históricos de Rendimientos por Instrumento")
st.write(data)

# Análisis de Volatilidad por Instrumento
st.subheader("Volatilidad Anualizada por Instrumento")
volatilidad_anualizada = data.iloc[:, 1:].std() * np.sqrt(252)  # Volatilidad anualizada
st.write(volatilidad_anualizada)

# Simulación de Monte Carlo para la Cartera Completa
st.subheader("Simulación de Monte Carlo para la Cartera Completa")

# Parámetros de la simulación
st.sidebar.header("Parámetros de la Simulación")
dias_proyeccion = st.sidebar.slider("Días de Proyección", 30, 365, 252)
num_simulaciones = st.sidebar.slider("Número de Simulaciones", 100, 10000, 1000)

# Pesos de la cartera (distribución de inversión)
pesos = np.array([0.4, 0.3, 0.15, 0.1, 0.05])  # Ejemplo: 40% Acciones, 30% Bonos, etc.

# Matriz de correlación (simulada)
correlaciones = np.array([
    [1.0, 0.2, 0.4, 0.6, 0.1],  # Acciones
    [0.2, 1.0, 0.3, 0.1, 0.0],  # Bonos
    [0.4, 0.3, 1.0, 0.5, 0.2],  # Fondos Inmobiliarios
    [0.6, 0.1, 0.5, 1.0, 0.3],  # ETF
    [0.1, 0.0, 0.2, 0.3, 1.0],  # Divisas
])

# Función para simular Monte Carlo de la cartera
def monte_carlo_cartera(dias, rendimientos_medios, volatilidades, pesos, correlaciones, simulaciones):
    num_instrumentos = len(pesos)
    # Generar choques correlacionados
    choques = np.random.multivariate_normal(
        np.zeros(num_instrumentos),
        correlaciones,
        size=(dias, simulaciones)
    )
    # Aplicar rendimientos y volatilidades
    choques = choques * volatilidades[np.newaxis, np.newaxis, :]
    choques += rendimientos_medios[np.newaxis, np.newaxis, :]
    # Calcular rendimientos acumulados de la cartera
    rendimientos_cartera = np.dot(choques, pesos)
    rendimientos_acumulados = np.cumprod(1 + rendimientos_cartera, axis=0)
    return rendimientos_acumulados

# Rendimientos medios y volatilidades diarias
rendimientos_medios = data.iloc[:, 1:].mean().values
volatilidades_diarias = data.iloc[:, 1:].std().values

# Ejecutar simulación
simulaciones_cartera = monte_carlo_cartera(
    dias_proyeccion, rendimientos_medios, volatilidades_diarias, pesos, correlaciones, num_simulaciones
)

# Gráfico de las simulaciones de la cartera
st.write(f"Simulación de Monte Carlo para {dias_proyeccion} días y {num_simulaciones} simulaciones")
plt.figure(figsize=(10, 6))
for i in range(num_simulaciones):
    plt.plot(simulaciones_cartera[:, i], lw=1, alpha=0.1, color="blue")
plt.title("Simulación de Monte Carlo de la Cartera Completa")
plt.xlabel("Días")
plt.ylabel("Valor de la Cartera")
st.pyplot(plt)

# Distribución de rendimientos finales de la cartera
st.subheader("Distribución de Rendimientos Finales de la Cartera")
rendimientos_finales_cartera = simulaciones_cartera[-1, :]
plt.figure(figsize=(10, 6))
sns.histplot(rendimientos_finales_cartera, kde=True, color="blue")
plt.title("Distribución de Rendimientos de la Cartera al Final del Período")
plt.xlabel("Rendimiento")
plt.ylabel("Frecuencia")
st.pyplot(plt)

# Cálculo de métricas de riesgo de la cartera
percentil_5_cartera = np.percentile(rendimientos_finales_cartera, 5)
percentil_95_cartera = np.percentile(rendimientos_finales_cartera, 95)
st.write(f"El percentil 5% de los rendimientos de la cartera es: **{percentil_5_cartera:.4f}**")
st.write(f"El percentil 95% de los rendimientos de la cartera es: **{percentil_95_cartera:.4f}**")

# Interpretación de Resultados
st.subheader("Interpretación de Resultados")
st.write("""
- **Volatilidad Anualizada por Instrumento**: Mide el riesgo individual de cada instrumento.
- **Simulación de Monte Carlo de la Cartera**: Proyecta posibles escenarios futuros para la cartera completa.
- **Distribución de Rendimientos Finales**: Muestra la probabilidad de obtener ciertos rendimientos al final del período.
- **Percentiles 5% y 95%**: Indican los rangos dentro de los cuales se espera que caigan la mayoría de los rendimientos de la cartera.
""")

# 1. Interpretación de los Percentiles
st.subheader("1. Interpretación de los Percentiles")
st.write(f"""
- **Percentil 5% ({percentil_5_cartera:.4f})**:
  - Representa el rendimiento mínimo esperado en el **5% de los peores escenarios**.
  - Indica que hay un **5% de probabilidad** de que el valor de la cartera al final del período sea **menor o igual a {percentil_5_cartera:.4f}** (una pérdida de aproximadamente **{(1 - percentil_5_cartera) * 100:.2f}%** respecto al valor inicial).

- **Percentil 95% ({percentil_95_cartera:.4f})**:
  - Representa el rendimiento máximo esperado en el **95% de los mejores escenarios**.
  - Indica que hay un **95% de probabilidad** de que el valor de la cartera al final del período sea **menor o igual a {percentil_95_cartera:.4f}** (una ganancia de aproximadamente **{(percentil_95_cartera - 1) * 100:.2f}%** respecto al valor inicial).
""")

# 2. Análisis de Riesgo y Rentabilidad
st.subheader("2. Análisis de Riesgo y Rentabilidad")
st.write(f"""
- **Rango de Rendimientos**:
  - Los rendimientos de la cartera oscilan entre **-{(1 - percentil_5_cartera) * 100:.2f}%** (percentil 5%) y **+{(percentil_95_cartera - 1) * 100:.2f}%** (percentil 95%).
  - Esto sugiere que la cartera tiene un **riesgo moderado**, con posibilidad de pérdidas limitadas pero también con un **potencial significativo de ganancias**.

- **Volatilidad**:
  - La diferencia entre el percentil 95% y el percentil 5% (rango interpercentil 90%) es **{percentil_95_cartera - percentil_5_cartera:.4f}**, lo que indica una **volatilidad significativa** en los rendimientos.

- **Riesgo de Pérdida**:
  - El percentil 5% de **{percentil_5_cartera:.4f}** sugiere que existe un **riesgo de pérdida**, pero no es extremadamente alto.
  - Esto podría ser aceptable para un inversionista con una **tolerancia moderada al riesgo**.

- **Potencial de Ganancia**:
  - El percentil 95% de **{percentil_95_cartera:.4f}** indica que la cartera tiene un **alto potencial de crecimiento** en escenarios favorables.
""")

# 3. Recomendaciones
st.subheader("3. Recomendaciones")
st.write("""
1. **Para Inversionistas Conservadores**:
   - Reducir la exposición a activos más volátiles (como acciones) y aumentar la asignación a activos más estables (como bonos).

2. **Para Inversionistas Moderados**:
   - La cartera actual parece equilibrada, con un **riesgo y rendimiento adecuados** para una **tolerancia moderada al riesgo**.

3. **Para Inversionistas Agresivos**:
   - Aumentar la exposición a activos de mayor rendimiento (como acciones o ETFs) para aprovechar el potencial de ganancias.

4. **Diversificación**:
   - Revisar la **diversificación de la cartera** para asegurarse de que no esté demasiado concentrada en un solo tipo de activo o sector.

5. **Monitoreo Continuo**:
   - Realizar un **seguimiento periódico** de la cartera para ajustar las asignaciones según las condiciones del mercado y los objetivos del inversionista.
""")

# 4. Conclusión
st.subheader("4. Conclusión")
st.write(f"""
Los resultados indican que la cartera tiene un **riesgo moderado** con un **potencial de crecimiento significativo**. Sin embargo, también existe la posibilidad de pérdidas, especialmente en escenarios adversos. La decisión de mantener o ajustar la cartera dependerá de la **tolerancia al riesgo** y los **objetivos de inversión** del inversionista. En general, la cartera es adecuada para inversionistas con un **perfil de riesgo moderado** que buscan un equilibrio entre rentabilidad y seguridad.
""")

# Nota Final
st.write("""
**Nota Final**: Este análisis proporciona una visión general del comportamiento esperado de la cartera. Sin embargo, es importante recordar que las simulaciones se basan en datos históricos y supuestos, por lo que los resultados futuros pueden variar. Se recomienda consultar con un **asesor financiero** para tomar decisiones informadas y personalizadas.
""")

# Footer con copyright
st.markdown("---")
st.write("© 2025 Derechos Reservados | Desarrollado por Javier Horacio Pérez Ricárdez")
