#!/usr/bin/env python
# coding: utf-8

# # Análisis Criminal SNIC - Análisis Exploratorio de Datos (EDA)
# 
# Este notebook presenta un análisis descriptivo de las estadísticas criminales de Argentina utilizando datos del SNIC para el período 2000-2024.
# 
# **Objetivos:**
# 1.  Analizar la evolución temporal de los hechos delictivos.
# 2.  Identificar la distribución geográfica del crimen.
# 3.  Determinar las tipologías delictivas más frecuentes.
# 4.  Detectar patrones mediante mapas de calor.

# In[ ]:


import os
import matplotlib
matplotlib.use('Agg') # Set backend to non-interactive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración Visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Definir directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '../data/final/snic_analytics.parquet')
FIGURES_DIR = os.path.join(BASE_DIR, '../reports/figures')

# Crear directorio de figuras si no existe
os.makedirs(FIGURES_DIR, exist_ok=True)
print(f"Directorio de figuras configurado: {FIGURES_DIR}")


# ## 1. Carga y Preparación de Datos

# In[ ]:


try:
    df = pd.read_parquet(DATA_PATH)
    print("Datos cargados exitosamente.")
    print(f"Dimensiones: {df.shape}")
    print(f"Rango de Años: {df['anio'].min()} - {df['anio'].max()}")
except FileNotFoundError:
    print(f"No se encontró el archivo en {DATA_PATH}. Ejecuta el pipeline ETL primero.")
    exit(1)


# In[ ]:


# Vista previa
print(df.head())


# ## 2. Análisis Temporal (2000-2024)

# In[ ]:


# Evolución Total de Hechos
hechos_por_anio = df.groupby('anio')['cantidad_hechos'].sum()

plt.figure(figsize=(14, 6))
sns.lineplot(x=hechos_por_anio.index, y=hechos_por_anio.values, marker='o', linewidth=2.5, color='b')
plt.title('Evolución Total de Hechos Delictivos (2000-2024)', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Hechos', fontsize=12)
plt.xticks(hechos_por_anio.index, rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'evolucion_anual_hechos.png'))
plt.close()


# ### Tendencia por Principales Tipos de Delito
# Analizamos la evolución de los 5 delitos más frecuentes.

# In[ ]:


# Identificar Top 5 delitos
top_5_delitos = df.groupby('codigo_delito_snic_nombre')['cantidad_hechos'].sum().nlargest(5).index

df_top_delitos = df[df['codigo_delito_snic_nombre'].isin(top_5_delitos)]
delitos_anio = df_top_delitos.groupby(['anio', 'codigo_delito_snic_nombre'])['cantidad_hechos'].sum().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=delitos_anio, x='anio', y='cantidad_hechos', hue='codigo_delito_snic_nombre', marker='o')
plt.title('Evolución Temporal: Top 5 Delitos', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Hechos', fontsize=12)
plt.legend(title='Tipo de Delito', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'evolucion_top5_delitos.png'))
plt.close()


# ## 3. Análisis Geográfico

# In[ ]:


# Total Acumulado por Provincia
hechos_por_provincia = df.groupby('provincia_nombre')['cantidad_hechos'].sum().sort_values(ascending=False)

plt.figure(figsize=(14, 10))
sns.barplot(
    y=hechos_por_provincia.index, 
    x=hechos_por_provincia.values, 
    hue=hechos_por_provincia.index, 
    legend=False, 
    palette='viridis'
)
plt.title('Total de Hechos Delictivos por Provincia (Acumulado)', fontsize=16)
plt.xlabel('Cantidad de Hechos', fontsize=12)
plt.ylabel('Provincia', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'hechos_por_provincia.png'))
plt.close()


# ### Evolución de las 5 Provincias con más delitos

# In[ ]:


top_5_prov = hechos_por_provincia.head(5).index
df_top_prov = df[df['provincia_nombre'].isin(top_5_prov)]
prov_anio = df_top_prov.groupby(['anio', 'provincia_nombre'])['cantidad_hechos'].sum().reset_index()

plt.figure(figsize=(14, 8))
sns.lineplot(data=prov_anio, x='anio', y='cantidad_hechos', hue='provincia_nombre', marker='^')
plt.title('Evolución Temporal: Top 5 Provincias', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Hechos', fontsize=12)
plt.legend(title='Provincia')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'evolucion_top5_provincias.png'))
plt.close()


# ## 4. Tipología del Delito

# In[ ]:


# Top 10 Delitos
top_delitos = df.groupby('codigo_delito_snic_nombre')['cantidad_hechos'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(14, 8))
sns.barplot(
    y=top_delitos.index, 
    x=top_delitos.values, 
    hue=top_delitos.index,
    legend=False,
    palette='magma'
)
plt.title('Top 10 Tipos de Delitos Más Frecuentes', fontsize=16)
plt.xlabel('Cantidad de Hechos', fontsize=12)
plt.ylabel('Tipo de Delito', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'top10_delitos.png'))
plt.close()


# ## 5. Mapas de Calor (Heatmaps)

# In[ ]:


# Mapa de Calor: Provincia vs Año
pivot_prov = df.pivot_table(index='provincia_nombre', columns='anio', values='cantidad_hechos', aggfunc='sum')

plt.figure(figsize=(18, 12))
sns.heatmap(pivot_prov, cmap='YlOrRd', linewidths=0.1, linecolor='white')
plt.title('Mapa de Calor: Intensidad Delictiva por Provincia y Año', fontsize=16)
plt.xlabel('Año')
plt.ylabel('Provincia')
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'heatmap_provincia_anio.png'))
plt.close()


# In[ ]:


# Mapa de Calor: Top 10 Delitos vs Año
df_top_delitos_heat = df[df['codigo_delito_snic_nombre'].isin(top_delitos.index)]
pivot_delito = df_top_delitos_heat.pivot_table(index='codigo_delito_snic_nombre', columns='anio', values='cantidad_hechos', aggfunc='sum')

plt.figure(figsize=(18, 10))
sns.heatmap(pivot_delito, cmap='Blues', linewidths=0.1, linecolor='white')
plt.title('Mapa de Calor: Top 10 Delitos por Año', fontsize=16)
plt.xlabel('Año')
plt.ylabel('Tipo de Delito')
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'heatmap_delito_anio.png'))
plt.close()

