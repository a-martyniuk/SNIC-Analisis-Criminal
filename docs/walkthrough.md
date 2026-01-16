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

## 5. Visualización (Dashboard Interactivo)
Se implementó un dashboard con Streamlit para la exploración dinámica de datos.

### Características
- **Pestana 1: Resumen General**: KPIs con comparativa interanual (Var %) y gráficos de top provincias.
- **Limpieza Visual**: Mayor espacio para gráficos y menús.
- **Referencias Dinámicas**: En el menú lateral, debajo del selector de delitos, se agregó un desplegable **"ℹ️ ¿Qué significa cada delito?"** que explica en lenguaje llano los delitos seleccionados.
- **Pestana 2: Tendencias**: Gráficos de línea y área para ver la evolución histórica.
- **Mapa Geográfico**: La pestaña "Detalle Geográfico" ahora muestra un mapa de Argentina con burbujas rojas sobre **OpenStreetMap**, permitiendo ver claramente las divisiones provinciales, rutas y ciudades.
- **Pestana 4: Datos**: Tabla de datos filtrados con opción de **descarga a CSV**.

### Ejecución
```bash
streamlit run src/app.py
```

## 6. Despliegue con Docker
Se han creado los archivos de configuración para ejecutar la aplicación en contenedores.

### Requisitos
- Docker y Docker Compose instalados.

### Ejecución
1. **Construir y levantar**:
   ```bash
   docker-compose up --build
   ```
2. **Acceder**:
   Navegar a `http://localhost:8501`.

## 7. Automatización CI/CD
Se configuró un flujo de trabajo en GitHub Actions (`.github/workflows/ci.yml`) que:
1. Ejecuta pruebas unitarias (`pytest`).
2. Verifica que la imagen Docker se construya correctamente.

Esto asegura la calidad del código y la desplegabilidad en cada push a `main`.


## 8. Modelo Predictivo (Machine Learning)
Se incorporó un modelo de **Regresión Lineal** (`src/model.py`) para proyectar tendencias futuras.

### Características
- **Entrenamiento On-the-fly**: El modelo se entrena en tiempo real con los datos filtrados por el usuario.
- **Visualización**: Muestra la línea histórica y la proyección futura (punteada) en una nueva pestaña **"🔮 Predicciones"**.
- **Interactividad**: Slider para elegir cuántos años proyectar hacia el futuro.

## Próximos Pasos
- Refinar el modelo (considerar estacionalidad si hubiera datos mensuales).
- Agregar más variables predictoras.
