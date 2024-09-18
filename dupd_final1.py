# -*- coding: utf-8 -*-
"""DUPD_FINAL1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/EHN8829/DUPD_FINAL1/blob/main/DUPD_FINAL1.ipynb

---
$$\small\textbf{Análisis de sensaciones a videos de Ecuaciones Diferenciales en YouTube como material de estudio complementario}$$

---
<br>

$\small\text{Autor: Eginhardo Navarro Honda}$

---

$$\large\textbf{Método 1}$$

---

$\small\text{1. Instalación de las librerías necesarias}$
"""

#!pip install streamlit

"""No se ha ejecutado, debido que al cargar 'DUPD_FINAL1.py' en el entorno de 'Streamlit Cloud', éste está DISPONIBLE. Además, se ha incluido en 'requirements.txt'."""

#!pip install google-api-python-client
#!pip install textblob

"""No se han ejecutado, debido que al cargar 'DUPD_FINAL1.py' en el entorno de 'Streamlit Cloud', éstos también están DISPONIBLES. Por lo que, no es necesario incluirlo en 'requirements.txt'."""

#!pip install nltk

import streamlit as st
from googleapiclient.discovery import build

"""$\small\text{2. Configurando la API Key de YouTube}$"""

API_KEY = 'AIzaSyBdU3XsjhpgZtLLFKoqp9EUHeNI-7U7J30'

"""$\small\text{3. Funciones para la obtención de datos en los videos}$"""

from googleapiclient.discovery import build

# Configurando la API Key
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_ids(playlist_id):
    video_ids = []
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50  # Se puedes ajustar este número (si hay más de 50 videos o menos)
    )
    response = request.execute()
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
    return video_ids

def get_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # Se puedes ajustar este número (si hay más de 50 comentarios o menos)
    )
    response = request.execute()
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    return comments

# ID de la lista de reproducción
playlist_id = 'PLeySRPnY35dFSDPi_4Q5R1VCGL_pab26A'
video_ids = get_video_ids(playlist_id)

# Obteniendo los comentarios para cada video
video_comments = {}
for video_id in video_ids:
    video_comments[video_id] = get_comments(video_id)

# Mostrando los resultados
print(video_comments)

"""$\small\text{3. Análiisis de Sensaciones }$

$\small\text{3.1. Instalación de las librerías necesarias}$
"""

from textblob import TextBlob
import nltk
nltk.download('punkt')

def analyze_sentiment(comments):
    sentiments = []
    for comment in comments:
        blob = TextBlob(comment)
        sentiments.append(blob.sentiment.polarity)  # Polaridad: De -1 (negativo) a 1 (positivo)
    return sentiments

# Analizando las sensaciones de los comentarios para cada video
video_sentiments = {}
for video_id, comments in video_comments.items():
    video_sentiments[video_id] = analyze_sentiment(comments)

# Mostrando las sensaciones
print(video_sentiments)

"""$\small\text{4. Exportación y visualización los resultados}$"""

import pandas as pd

"""$\small\text{4.1. Verificación del contenido de video_sentiments}$"""

for video_id, sentiments in video_sentiments.items():
    print(f"Video ID: {video_id}")
    print(f"Sentiments: {sentiments[:9]}")  # Muestra solo las primeras 9 sensaciones para simplificar
    print("------")

"""$\small\text{4.2. Preparación de los Datos para el DataFrame}$"""

# Calculando la sensación promedio para cada video
def calculate_average_sentiment(sentiments):
    if sentiments:
        return sum(sentiments) / len(sentiments)
    return 0

# Creando un diccionario con los promedios de la sensación
average_sentiments = {video_id: calculate_average_sentiment(sentiments) for video_id, sentiments in video_sentiments.items()}

# Convirtiendo a DataFrame
df = pd.DataFrame(list(average_sentiments.items()), columns=['VideoID', 'AverageSentiment'])

# Configurando el índice (si es necesario)
df.set_index('VideoID', inplace=True)

# Guardando la 'data' en un archivo CSV
df.to_csv('/content/video_sentiments.csv')

"""$\small\text{4.3. Descarga del archivo [video_sentiments.csv] en el procesador}$"""

from google.colab import files

# Activando una descarga en nuestro procesador
files.download('video_sentiments.csv')

# Mostrando el DataFrame
print(df)

df

"""$\small\text{5. Instalación y configuración de las Bibliotecas de Visualización}$"""

#!pip install matplotlib seaborn

"""No se han ejecutado, debido que al cargar nuevamente 'DUPD_FINAL1.py' en el entorno de 'Streamlit Cloud', éstos también están DISPONIBLES. Por lo que, tampoco se ha incluido en 'requirements.txt'.

$\small\text{6. Creación de gráficos usando Matplotlib y Seaborn}$

$\small\text{6.1. Histograma de Sensaciones}$
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Configurando el estilo de los gráficos
sns.set(style="whitegrid")

# Creando histograma
plt.figure(figsize=(10, 6))
sns.histplot(df['AverageSentiment'], bins=20, kde=True, color='coral')
plt.title('Distribución de Sensaciones Promedio de Videos')
plt.xlabel('Sensación Promedio')
plt.ylabel('Frecuencia')
plt.show()

"""$\small\text{6.2. Creación de Gráfico de Barras de Sensaciones por Video}$"""

# Ordenando los valores para mejorar la visualización
df_sorted = df.sort_values(by='AverageSentiment', ascending=False)

# Creando el gráfico de barras
plt.figure(figsize=(14, 8))
sns.barplot(x=df_sorted.index, y=df_sorted['AverageSentiment'], palette='viridis')
plt.title('Sensaciones Promedio por Video')
plt.xlabel('ID del Video')
plt.ylabel('Sensación Promedio')
plt.xticks(rotation=90)  # Rotando 90° las etiquetas del eje 'x' para mayor legibilidad
plt.show()

"""$\small\text{6.3. Creación de Gráfico de Caja (Boxplot) de Sensaciones}$"""

# Creando el gráfico de caja
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['AverageSentiment'], color='cyan')
plt.title('Distribución de Sensaciones Promedio')
plt.xlabel('Sensación Promedio')
plt.show()

"""$\small\text{7. Extracción de Comentarios positivos para realizar un Análisis de Sensaciones}$"""

#!pip install textblob

"""Explicado líneas arriba."""

#!pip install pandas nltk

"""Lo mismo que el caso anterior."""

import pandas as pd
from textblob import TextBlob
import nltk
nltk.download('punkt')  # Descargando el tokenizador de nltk nuevamente

def analyze_sentiment(comment):
    blob = TextBlob(comment)
    return blob.sentiment.polarity  # Polaridad: -1 De (negativo) a 1 (positivo)

# Creando una lista para almacenar los comentarios positivos
positive_comments = []

# Analizando cada video y sus comentarios
for video_id, comments in video_comments.items():
    for comment in comments:
        sentiment = analyze_sentiment(comment)
        if sentiment > 0:  # Considerando como positivo si la polaridad es mayor que 0
            positive_comments.append({
                'VideoID': video_id,
                'Comment': comment,
                'Sentiment': sentiment
            })

# Convirtiendo la lista a un DataFrame
df_positive_comments = pd.DataFrame(positive_comments)

# Mostrando el DataFrame
print(df_positive_comments)

df_positive_comments

# Mostrando la tabla de comentarios positivos
plt.figure(figsize=(12, 8))
ax = sns.heatmap(df_positive_comments[['Comment', 'Sentiment']].head(20).set_index('Comment'), annot=True, cmap='YlGnBu')
ax.set_title('Comentarios Positivos')
plt.show()