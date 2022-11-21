import streamlit as st

import pandas as pd
import geopandas as gpd

import plotly.express as px

import folium
from folium import Marker
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from streamlit_folium import folium_static

import math

st.set_page_config(layout="wide")

#
# Entradas
#

archivo_registros_presencia = st.sidebar.file_uploader('Seleccione un archivo CSV que siga el estándar DwC')

if archivo_registros_presencia is not None:
      # Carga de registros de presencia en un dataframe
    registros_presencia = pd.read_csv(archivo_registros_presencia, delimiter='\t')
    # Conversión del dataframe de registros de presencia a geodataframe
    registros_presencia = gpd.GeoDataFrame(registros_presencia, 
                                           geometry=gpd.points_from_xy(registros_presencia.decimalLongitude, 
                                                                       registros_presencia.decimalLatitude),
                                           crs='EPSG:4326')

# Limpieza de datos
    # Eliminación de registros con valores nulos en la columna 'species'
    registros_presencia = registros_presencia[registros_presencia['species'].notna()]
    # Cambio del tipo de datos del campo de fecha
    registros_presencia["eventDate"] = pd.to_datetime(registros_presencia["eventDate"])

     # Especificación de filtros
    # Especie
    lista_especies = registros_presencia.species.unique().tolist()
    lista_especies.sort()
    filtro_especie = st.sidebar.selectbox('Seleccione la especie', lista_especies)

     #
    # PROCESAMIENTO
    #

    # Filtrado
    registros_presencia = registros_presencia[registros_presencia['species'] == filtro_especie]

     # Tabla de registros de presencia
    st.header('Registros de presencia')
    st.dataframe(registros_presencia[['family', 'species', 'eventDate', 'locality', 'occurrenceID']].rename(columns = {'family':'Familia', 'species':'Especie', 'eventDate':'Fecha', 'locality':'Localidad', 'occurrenceID':'Origen del dato'}))
    