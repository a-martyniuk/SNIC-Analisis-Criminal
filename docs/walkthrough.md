# Guía del Proyecto de Análisis SNIC

Este documento registra los pasos realizados para configurar el proyecto de Análisis Criminal SNIC e implementar el pipeline ETL inicial.

## 1. Inicialización del Proyecto
- Directorio de proyecto creado: `d:\Projects\SNIC-Analisis-Criminal`
- Entorno Python y repositorio Git inicializados.
- Estructura de directorios creada:
    - `src/`: Código fuente para ETL
    - `data/`: Almacenamiento de datos (raw, processed, final)
    - `notebooks/`: Notebooks de análisis

## 2. Implementación del Pipeline ETL
Implementamos un pipeline ETL (Extracción, Transformación, Carga) robusto en `src/`.

### Extracción (`src/extract.py`)
- **Función**: Descarga datos reales del SNIC desde `cloud-snic.minseg.gob.ar`.
- **Estado**: listo para producción. Utiliza el enlace directo CSV para datos departamentales.

### Transformación (`src/transform.py`)
- **Función**: Limpia y normaliza los datos CSV crudos.
- **Lógica Clave**: Maneja codificación `latin-1` y delimitador de punto y coma (`;`).
- **Pasos**:
    - Elimina filas con valores clave faltantes.
    - Convierte tipos (ej. `anio` a int).
    - Estandariza nombres de columnas.

### Carga (`src/load.py`)
- **Función**: Guarda los datos procesados en un formato altamente eficiente.
- **Salida**: `data/final/snic_analytics.parquet`.

### Orquestación del Pipeline (`src/pipeline.py`)
- Conecta todos los pasos.
- Comando de ejecución: `python src/pipeline.py`.

## 3. Configuración de Análisis de Datos
- **Dependencias**: Se agregaron `matplotlib`, `seaborn`, `jupyter` a `requirements.txt`.
- **Notebook**: Se creó `notebooks/01_eda.ipynb` para Análisis Exploratorio de Datos.

## 4. Cómo Ejecutar
1. **Instalar Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Ejecutar Pipeline ETL**:
   ```bash
   python src/pipeline.py
   ```
3. **Ejecutar Análisis**:
   ```bash
   jupyter notebook notebooks/01_eda.ipynb
   ```
