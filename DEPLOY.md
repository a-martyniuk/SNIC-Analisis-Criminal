# Guía de Despliegue (Deployment) 🚀

Esta guía detalla cómo poner en funcionamiento el **Panel de Análisis Criminal SNIC** en internet o en un servidor local, utilizando opciones **100% gratuitas**.

## Opción 1: Streamlit Community Cloud (Recomendada) ⭐

La forma más rápida y sencilla de compartir tu aplicación sin coste alguno.

### Prerrequisitos
1.  Una cuenta en [GitHub](https://github.com/).
2.  Una cuenta en [Streamlit Cloud](https://streamlit.io/cloud) (puedes iniciar sesión con tu cuenta de GitHub).

### Pasos
1.  **Subir el código a GitHub**:
    *   Crea un nuevo repositorio público en GitHub.
    *   Sube todos los archivos de este proyecto al repositorio.
    *   Asegúrate de que el archivo `requirements.txt` y la carpeta `src/` estén en la raíz.

2.  **Conectar con Streamlit**:
    *   Ve a [share.streamlit.io](https://share.streamlit.io/).
    *   Haz clic en **"New app"**.
    *   Selecciona tu repositorio de GitHub, la rama (usualmente `main` o `master`) y el archivo principal: `src/app.py`.
    *   Haz clic en **"Deploy!"**.

3.  **¡Listo!**:
    *   En unos minutos, tu aplicación estará viva en una URL pública (ej: `https://snic-analisis.streamlit.app`).
    *   Streamlit instalará automáticamente las dependencias listadas en `requirements.txt`.

---

## Opción 2: Ejecución Local con Docker 🐳

Ideal si prefieres ejecutar la aplicación en tu propia máquina o en un servidor privado (VPS) de manera aislada.

### Prerrequisitos
*   Tener **Docker Desktop** instalado y corriendo.

### Pasos
1.  **Construir la imagen**:
    Abre una terminal en la carpeta del proyecto y ejecuta:
    ```bash
    docker-compose up --build
    ```

2.  **Acceder a la aplicación**:
    *   Una vez que termine el proceso, abre tu navegador.
    *   Ve a: `http://localhost:8501`.

### Comandos Útiles
*   **Detener la aplicación**: `Ctrl + C` en la terminal.
*   **Ejecutar en segundo plano**: `docker-compose up -d`.
*   **Ver logs**: `docker-compose logs -f`.

---

## Solución de Problemas Comunes

*   **Error "ModuleNotFoundError"**: Verifica que todas las librerías estén en `requirements.txt` (especialmente `plotly` y `pandas`).
*   **La app no carga datos**: Asegúrate de que el archivo `data/final/snic_analytics.parquet` se haya subido a GitHub. Si el archivo es muy pesado (>100MB), necesitarás usar *Git LFS* o generar los datos en el deploy (lo cual requeriría ejecutar el pipeline ETL antes de levantar la app).
