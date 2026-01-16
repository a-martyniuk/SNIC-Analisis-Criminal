import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from model import prepare_time_series, train_and_predict

# Configuration
ST_PAGE_TITLE = "Panel de Análisis Criminal SNIC"
DATA_PATH = "data/final/snic_analytics.parquet"
DATA_PATH = "data/final/snic_analytics.parquet"
FALLBACK_DATA_PATH = "data/processed/snic_clean.csv"
CENTROIDS_PATH = "data/provincias_centroids.csv"

st.set_page_config(page_title=ST_PAGE_TITLE, layout="wide")

# Mapeo de nombres cortos para mejor visualización
SHORT_NAMES = {
    # Homicidios
    "Homicidios dolosos": "Homicidios Dolosos",
    "Homicidios dolosos en grado de tentativa": "Tent. Homicidio",
    "Homicidios culposos por otros hechos": "Hom. Culposos (Otros)",
    "Suicidios (consumados)": "Suicidios",
    
    # Viales
    "Muertes en accidentes viales": "Muertes Viales",
    "Lesiones culposas en Accidentes Viales": "Lesiones Viales",
    
    # Lesiones
    "Lesiones dolosas": "Lesiones Dolosas",
    "Lesiones culposas por otros hechos": "Lesiones Culp. (Otras)",
    "Otros delitos contra las personas": "Otros (Personas)",
    
    # Sexuales
    "Abusos sexuales con acceso carnal (violaciones)": "Abuso Sexual (Acceso)",
    "Tentativa de abuso sexual con acceso carnal": "Tent. Abuso (Acceso)",
    "Abuso sexual simple": "Abuso Sexual Simple",
    "Abuso sexual agravado": "Abuso Sexual Agrav.",
    "Otros delitos contra la integridad sexual": "Otros (Sexual)",
    "Ciberdelitos sexuales vinculados a menores": "Ciberdelitos Menores",
    
    # Propiedad (Robo/Hurto)
    "Robos (excluye los agravados por el resultado de lesiones y/o muertes)": "Robos",
    "Tentativas de robo (excluye las agravadas por el res. de lesiones y/o muerte)": "Tent. Robo",
    "Robos agravados por el resultado de lesiones y/o muertes": "Robo Agrav. (Muerte/Lesión)",
    "Robos agravados por el resultado de lesiones y/o muertes ": "Robo Agrav. (Muerte/Lesión)", # Duplicate with space
    "Tentativas de robo agravado por el resultado de lesiones y/o muertes": "Tent. Robo Agrav.",
    "Hurtos": "Hurtos",
    "Tentativas de hurto": "Tent. Hurto",
    "Otros delitos contra la propiedad": "Otros (Propiedad)",
    "Daños (no incluye informáticos)": "Daños",
    
    # Estafas y Tecnológicos
    "Estafas y defraudaciones (no incluye virtuales) y usura": "Estafas (Tradicional)",
    "Estafas y defraudaciones asistidas virtualmente": "Estafas Virtuales",
    "Acceso ilegal a sistemas informáticos y daños informáticos": "Delitos Informáticos",
    
    # Armas
    "Tenencia ilegal de armas de fuego": "Tenencia Ilegal Armas",
    "Portación ilegal de armas de fuego": "Portación Ilegal Armas",
    "Entrega y comercialización ilegal de armas de fuego": "Comercio Ilegal Armas",
    "Acopio y fabricación ilegal de armas piezas y municiones": "Acopio/Fabr. Armas",
    "Fabricación adquisición transferencia y tenencia de explosivos y otros materiales peligrosos": "Explosivos",
    "Omisión adulteración y supresión de marcaje": "Adulteración Armas",
    
    # Drogas (Ley 23.737)
    "Ley 23.737 (estupefacientes)": "Ley Drogas",
    "Tenencia simple de estupefacientes": "Tenencia Simple",
    "Tenencia simple atenuada para uso personal de estupefacientes": "Tenencia Uso Personal",
    "Comercialización y entrega de estupefacientes": "Comercialización Drogas",
    "Siembra y producción de estupefacientes": "Siembra/Prod. Drogas",
    "Organización y financiación de estupefacientes": "Org/Financ. Drogas",
    "Confabulación de estupefacientes": "Confabulación Drogas",
    "Contrabando de estupefacientes": "Contrabando Drogas",
    "Otros delitos previstos en la ley 23.737": "Otros (Ley Drogas)",
    
    # Libertad / Trata / Otros
    "Amenazas": "Amenazas",
    "Otros delitos contra la libertad": "Otros (Libertad)",
    "Trata de personas simple": "Trata Personas",
    "Trata de personas agravado": "Trata Personas Agrav.",
    "Extorsiones": "Extorsiones",
    "Secuestros extorsivos": "Secuestros",
    
    # Contrabando y Aduana
    "Contrabando Simple": "Contrabando",
    "Contrabando simple": "Contrabando",
    "Contrabando Agravado": "Contrabando Agrav.",
    "Contrabando agravado": "Contrabando Agrav.",
    "Obstrucción del código aduanero": "Obstrucción Aduana",
    "Delitos migratorios": "Delitos Migratorios",
    
    # Otros Títulos
    "Delitos contra la seguridad pública": "Seguridad Pública",
    "Otros delitos contra la seguridad pública": "Seguridad Pública (Otros)",
    "Delitos contra el orden público": "Orden Público",
    "Delitos contra la seguridad de la nación": "Seguridad Nación",
    "Delitos contra los poderes públicos y el orden constitucional": "Orden Constitucional",
    "Delitos contra la administración pública": "Adm. Pública",
    "Delitos contra la fe pública": "Fe Pública",
    "Delitos contra el honor": "Honor",
    "Delitos contra el orden económico y financiero": "Orden Económico",
    "Delitos contra el estado civil": "Estado Civil",
    "Otros delitos previstos en leyes especiales": "Leyes Especiales",
    "Otros delitos previstos en leyes especiales n.c.p": "Leyes Especiales (NCP)",
    "Contravenciones": "Contravenciones",
    "Ley de fauna": "Ley Fauna",
    "Ley de residuos peligrosos": "Residuos Peligrosos"
}

# Descripciones para Tooltips (Lenguaje llano)
CRIME_DESCRIPTIONS = {
    "Homicidios dolosos": "Muerte causada intencionalmente a otra persona.",
    "Homicidios dolosos en grado de tentativa": "Intento de matar a otra persona que no se concretó.",
    "Homicidios culposos por otros hechos": "Muerte causada sin intención, por negligencia o imprudencia (no vial).",
    "Suicidios (consumados)": "Muerte autoinfligida intencionalmente.",
    "Muertes en accidentes viales": "Fallecimientos derivados de siniestros de tránsito.",
    "Lesiones culposas en Accidentes Viales": "Heridas no intencionales producidas en siniestros de tránsito.",
    "Lesiones dolosas": "Heridas causadas intencionalmente a otra persona.",
    "Lesiones culposas por otros hechos": "Heridas causadas sin intención (no vial).",
    "Otros delitos contra las personas": "Otros daños físicos no categorizados anteriormente.",
    "Abusos sexuales con acceso carnal (violaciones)": "Agresión sexual que implica penetración.",
    "Tentativa de abuso sexual con acceso carnal": "Intento de agresión sexual con penetración.",
    "Abuso sexual simple": "Tocamientos indebidos sin penetración.",
    "Abuso sexual agravado": "Abuso sexual con circunstancias que aumentan su gravedad (ej. vínculo, armas).",
    "Otros delitos contra la integridad sexual": "Delitos sexuales no encuadrados en los anteriores (ej. exhibicionismo).",
    "Ciberdelitos sexuales vinculados a menores": "Grooming o producción/distribución de material de abuso infantil.",
    "Robos (excluye los agravados por el resultado de lesiones y/o muertes)": "Apoderamiento de cosa ajena con fuerza o violencia (sin matar/lesionar gravemente).",
    "Tentativas de robo (excluye las agravadas por el res. de lesiones y/o muerte)": "Intento de robo no consumado.",
    "Robos agravados por el resultado de lesiones y/o muertes": "Robo donde la víctima resultó herida gravemente o fallecida.",
    "Robos agravados por el resultado de lesiones y/o muertes ": "Robo donde la víctima resultó herida gravemente o fallecida.",
    "Tentativas de robo agravado por el resultado de lesiones y/o muertes": "Intento de robo con resultado de lesiones graves o muerte.",
    "Hurtos": "Apoderamiento de cosa ajena SIN fuerza sobre las cosas ni violencia física.",
    "Tentativas de hurto": "Intento de hurto no consumado.",
    "Otros delitos contra la propiedad": "Daños, usurpaciones, etc.",
    "Daños (no incluye informáticos)": "Destrucción o inutilización de propiedad ajena.",
    "Estafas y defraudaciones (no incluye virtuales) y usura": "Engaño económico tradicional (cuento del tío, cheques sin fondo).",
    "Estafas y defraudaciones asistidas virtualmente": "Engaños económicos por internet/teléfono (phishing, vishing).",
    "Acceso ilegal a sistemas informáticos y daños informáticos": "Hacking, robo de identidad digital o sabotaje informático.",
    "Tenencia ilegal de armas de fuego": "Poseer un arma sin la autorización legal correspondiente.",
    "Portación ilegal de armas de fuego": "Llevar un arma cargada y lista para usar en lugares públicos sin permiso.",
    "Entrega y comercialización ilegal de armas de fuego": "Venta o entrega de armas fuera del circuito legal.",
    "Acopio y fabricación ilegal de armas piezas y municiones": "Reunir grandes cantidades de armas/municiones o fabricarlas ilegalmente.",
    "Fabricación adquisición transferencia y tenencia de explosivos y otros materiales peligrosos": "Manejo ilegal de explosivos.",
    "Omisión adulteración y supresión de marcaje": "Borrar números de serie de armas.",
    "Ley 23.737 (estupefacientes)": "Delitos generales de drogas.",
    "Tenencia simple de estupefacientes": "Posesión de drogas sin fines de comercialización evidentes.",
    "Tenencia simple atenuada para uso personal de estupefacientes": "Posesión de pequeña cantidad de droga para consumo propio.",
    "Comercialización y entrega de estupefacientes": "Venta o distribución de drogas (Narcomenudeo/Narcotráfico).",
    "Siembra y producción de estupefacientes": "Cultivo o fabricación de drogas.",
    "Organización y financiación de estupefacientes": "Jefes o financistas de organizaciones narco.",
    "Confabulación de estupefacientes": "Acuerdo entre personas para cometer delitos de drogas.",
    "Contrabando de estupefacientes": "Ingreso/Egreso ilegal de drogas por frontera.",
    "Otros delitos previstos en la ley 23.737": "Otros delitos de la ley de drogas.",
    "Amenazas": "Intimidación a una persona con causarle un mal futuro.",
    "Otros delitos contra la libertad": "Privación ilegítima de la libertad, etc.",
    "Trata de personas simple": "Captación/transporte de personas con fines de explotación (sexual/laboral).",
    "Trata de personas agravado": "Trata de personas con agravantes (menores, violencia, etc.).",
    "Extorsiones": "Obligar a alguien a hacer/dar algo mediante intimidación.",
    "Secuestros extorsivos": "Retener a una persona para pedir rescate.",
    "Contrabando Simple": "Ingreso/Egreso ilegal de mercadería.",
    "Contrabando simple": "Ingreso/Egreso ilegal de mercadería.",
    "Contrabando Agravado": "Contrabando con violencia, de sustancias peligrosas, o por funcionarios.",
    "Contrabando agravado": "Contrabando con violencia, de sustancias peligrosas, o por funcionarios.",
    "Obstrucción del código aduanero": "Impedir el control aduanero.",
    "Delitos migratorios": "Tráfico ilegal de inmigrantes.",
    "Delitos contra la seguridad pública": "Peligros comunes (incendios, explosiones).",
    "Otros delitos contra la seguridad pública": "Otros peligros comunes.",
    "Delitos contra el orden público": "Instigación a cometer delitos, asociación ilícita.",
    "Delitos contra la seguridad de la nación": "Traición, espionaje.",
    "Delitos contra los poderes públicos y el orden constitucional": "Rebelión, sedición.",
    "Delitos contra la administración pública": "Corrupción, abuso de autoridad, cohecho.",
    "Delitos contra la fe pública": "Falsificación de documentos o moneda.",
    "Delitos contra el honor": "Injurias y calumnias.",
    "Delitos contra el orden económico y financiero": "Lavado de dinero, delitos tributarios.",
    "Delitos contra el estado civil": "Matrimonios ilegales, supresión de identidad.",
    "Otros delitos previstos en leyes especiales": "Leyes no codificadas.",
    "Otros delitos previstos en leyes especiales n.c.p": "Leyes no codificadas.",
    "Contravenciones": "Faltas menores (no llegan a delito).",
    "Ley de fauna": "Caza ilegal, tráfico de animales.",
    "Ley de residuos peligrosos": "Mal manejo de sustancias tóxicas."
}

# Categorías de Delitos (Para Filtros Jerárquicos)
CRIME_CATEGORIES = {
    "Homicidios": [
        "Homicidios Dolosos", "Tent. Homicidio", "Hom. Culposos (Otros)", "Suicidios", 
        "Muertes Viales"
    ],
    "Lesiones": [
        "Lesiones Viales", "Lesiones Dolosas", "Lesiones Culp. (Otras)", "Otros (Personas)"
    ],
    "Delitos Sexuales": [
        "Abuso Sexual (Acceso)", "Tent. Abuso (Acceso)", "Abuso Sexual Simple", 
        "Abuso Sexual Agrav.", "Otros (Sexual)", "Ciberdelitos Menores"
    ],
    "Robos y Hurtos": [
        "Robos", "Tent. Robo", "Robo Agrav. (Muerte/Lesión)", "Tent. Robo Agrav.",
        "Hurtos", "Tent. Hurto", "Otros (Propiedad)", "Daños"
    ],
    "Estafas y Tecnología": [
        "Estafas (Tradicional)", "Estafas Virtuales", "Delitos Informáticos"
    ],
    "Armas y Explosivos": [
        "Tenencia Ilegal Armas", "Portación Ilegal Armas", "Comercio Ilegal Armas", 
        "Acopio/Fabr. Armas", "Explosivos", "Adulteración Armas"
    ],
    "Narcotráfico (Ley 23.737)": [
        "Ley Drogas", "Tenencia Simple", "Tenencia Uso Personal", "Comercialización Drogas",
        "Siembra/Prod. Drogas", "Org/Financ. Drogas", "Confabulación Drogas", 
        "Contrabando Drogas", "Otros (Ley Drogas)"
    ],
    "Libertad y Trata": [
        "Amenazas", "Otros (Libertad)", "Trata Personas", "Trata Personas Agrav.",
        "Extorsiones", "Secuestros"
    ],
    "Contrabando y Aduana": [
        "Contrabando", "Contrabando Agrav.", "Obstrucción Aduana", "Delitos Migratorios"
    ],
    "Seguridad y Orden Público": [
        "Seguridad Pública", "Seguridad Pública (Otros)", "Orden Público", "Seguridad Nación",
        "Orden Constitucional", "Adm. Pública", "Fe Pública", "Honor", "Orden Económico",
        "Estado Civil", "Leyes Especiales", "Leyes Especiales (NCP)", "Contravenciones",
        "Ley Fauna", "Residuos Peligrosos"
    ]
}

# Población Censo 2022 (para cálculo de tasas provinciales)
PROVINCIA_POBLACION = {
    "Buenos Aires": 17569053,
    "Ciudad Autónoma de Buenos Aires": 3120612,
    "Catamarca": 429556,
    "Chaco": 1142963,
    "Chubut": 603120,
    "Córdoba": 3978984,
    "Corrientes": 1197553,
    "Entre Ríos": 1426426,
    "Formosa": 606041,
    "Jujuy": 797955,
    "La Pampa": 366022,
    "La Rioja": 384607,
    "Mendoza": 2014533,
    "Misiones": 1280960,
    "Neuquén": 710814,
    "Río Negro": 762067,
    "Salta": 1440672,
    "San Juan": 817218,
    "San Luis": 540905,
    "Santa Cruz": 333473,
    "Santa Fe": 3556522,
    "Santiago del Estero": 1054028,
    "Tierra del Fuego": 190641, # Normalizado en ETL? Chequear
    "Tucumán": 1703186
}
# Fallback map for discrepancies
NORM_PROVS = {
    "Tierra del Fuego, Antártida e Islas del Atlántico Sur": "Tierra del Fuego"
}

def calculate_rates(df_grouped, group_col='provincia_nombre'):
    """Calculates rates based on population dict."""
    # This expects a DF aggregated by [group_col] with 'cantidad_hechos'
    rates = []
    
    for idx, row in df_grouped.iterrows():
        prov = row[group_col]
        # Normalize name if needed
        prov_key = NORM_PROVS.get(prov, prov)
        
        pop = PROVINCIA_POBLACION.get(prov_key, 0)
        
        if pop > 0:
            rate = (row['cantidad_hechos'] / pop) * 100000
        else:
            rate = 0 # Or row['tasa_hechos'] if exists? Better 0 to avoid mixed logic
            
        rates.append(rate)
        
    return rates

@st.cache_data
def load_geojson():
    """Loads Argentina Provinces GeoJSON."""
    url = "https://apis.datos.gob.ar/georef/api/v2.0/provincias.geojson"
    try:
        import urllib.request
        import json
        with urllib.request.urlopen(url) as response:
            geojson = json.load(response)
        return geojson
    except Exception as e:
        st.error(f"Error cargando mapa: {e}")
        return None

@st.cache_data
def load_data():
    """Loads data from Parquet or CSV fallback."""
    df = None
    if os.path.exists(DATA_PATH):
        df = pd.read_parquet(DATA_PATH)
    elif os.path.exists(FALLBACK_DATA_PATH):
        df = pd.read_csv(FALLBACK_DATA_PATH)
    
    return df

@st.cache_data
def load_centroids():
    """Loads province centroids."""
    if os.path.exists(CENTROIDS_PATH):
        return pd.read_csv(CENTROIDS_PATH)
    return None

def apply_short_names(df):
    """Applies short names and descriptions to the dataset."""
    if df is not None and 'codigo_delito_snic_nombre' in df.columns:
        # 1. Create Description Column (Before renaming definition)
        df['descripcion_delito'] = df['codigo_delito_snic_nombre'].map(CRIME_DESCRIPTIONS).fillna("Descripción no disponible.")
        
        # 2. Apply Short Names
        df['codigo_delito_snic_nombre'] = df['codigo_delito_snic_nombre'].replace(SHORT_NAMES)
        
    return df

def fmt_num(val, decimals=0):
    """Formats a number with Argentine locale (1.000,00)."""
    if pd.isna(val):
        return "-"
    fmt_str = f"{{:,.{decimals}f}}"
    return fmt_str.format(val).replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    # Custom Title with isolated emoji to avoid gradient masking
    st.markdown(f"<h1>📊 <span class='gradient-text'>{ST_PAGE_TITLE}</span></h1>", unsafe_allow_html=True)
    
    st.markdown("Exploración profunda de estadísticas criminales de Argentina.")
    
    with st.expander("ℹ️ Fuente de Datos y Metodología"):
        st.markdown("""
        **Fuente Oficial:** [Sistema Nacional de Información Criminal (SNIC)](https://www.argentina.gob.ar/seguridad/estadisticas/snic).
        
        **Origen:** Ministerio de Seguridad de la Nación Argentina.
        
        **Tasas:** Calculadas con datos del **Censo Nacional 2022**.
        """)
    
    # --- Custom CSS ---
    st.markdown("""
    <style>
        /* Import Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Reset & Theme */
        .stApp {
            background-color: #020617;
        }
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            color: #E2E8F0; /* Slate 200 - Softer white */
        }
        
        /* HEADERS - Hierarchy */
        h1 {
            font-weight: 800 !important;
            font-size: 3rem !important;
            padding-bottom: 0.5rem;
        }
        
        /* New Gradient Text Class */
        .gradient-text {
            background: linear-gradient(90deg, #818cf8 0%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        h2 {
            color: #F1F5F9 !important;
            font-weight: 600 !important;
            font-size: 1.8rem !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }
        
        h3 {
            color: #CBD5E1 !important;
            font-weight: 500 !important;
            font-size: 1.25rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* METRIC CARDS - Fluid & Aligned */
        [data-testid="stMetric"] {
            background-color: #0F172A; /* Slate 900 */
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #1E293B;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            text-align: center;
            height: 180px; /* Fixed height for perfect alignment */
            display: flex;
            flex-direction: column;
            justify-content: center; /* Vertical center */
            align-items: center; /* Horizontal center */
        }
        
        /* Label (Top) */
        [data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-size: 0.95rem !important; /* Slightly larger */
            font-weight: 600; /* Bolder */
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: auto; /* Push to top */
        }
        
        /* Value (Middle) */
        [data-testid="stMetricValue"] {
            color: #F8FAFC !important;
            font-size: 2.8rem !important; /* Much larger */
            font-weight: 800; /* Extra Bold */
            padding: 8px 0;
            margin: auto 0; /* Center vertically */
        }
        
        /* Delta (Bottom) */
        [data-testid="stMetricDelta"] {
            font-size: 0.9rem !important;
            font-weight: 700;
            margin-top: auto; /* Push to bottom */
        }    
        
        /* COMPONENTS */
        .stAlert {
            background-color: #1E1E2E;
            border: none;
            border-left: 4px solid #6366F1;
        }
        
        /* TABS - High Visibility */
        .stTabs [data-baseweb="tab-list"] {
            gap: 16px;
            border-bottom: 2px solid #1E293B;
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            font-size: 1.5rem !important; /* Force Larger text */
            font-weight: 700 !important;  /* Force Extra Bold */
            color: #64748B;
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            padding: 0 24px;
            transition: all 0.3s ease;
        }
        
        /* Specific target for text inside tabs to better override Streamlit defaults */
        .stTabs [data-baseweb="tab"] div, .stTabs [data-baseweb="tab"] p {
             font-size: 1.5rem !important;
             font-weight: 700 !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #CBD5E1;
            background-color: #0F172A; /* Slight background on hover */
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #FFFFFF !important; /* Bright White */
            background-color: #1E293B; /* Active Background tab style */
            border-bottom: 4px solid #6366F1; /* Thick Accent Border */
        }

        /* Sidebar Cleanup */
        [data-testid="stSidebar"] {
            background-color: #020617;
            border-right: 1px solid #1E293B;
        }
        
    </style>
    """, unsafe_allow_html=True)

    # Plotly Locale & Theme Config (Global)
    import plotly.io as pio
    
    # Define custom dark template matching the site
    pio.templates["midnight_blue"] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor="#020617", # Main Background
            plot_bgcolor="#0F172A",  # Chart Area Background
            font={'family': "Inter", 'color': "#CBD5E1"}, # Muted Text
            colorway=['#6366F1', '#A855F7', '#EC4899', '#3B82F6', '#10B981'], # Indigo, Purple, Pink, Blue, Emerald
            title={'font': {'color': '#F8FAFC', 'size': 20}},
            xaxis={'gridcolor': '#1E293B', 'linecolor': '#1E293B', 'zerolinecolor': '#1E293B'},
            yaxis={'gridcolor': '#1E293B', 'linecolor': '#1E293B', 'zerolinecolor': '#1E293B'},
            hoverlabel={'bgcolor': '#1E293B', 'font': {'color': '#F8FAFC'}},
        )
    )
    pio.templates.default = "midnight_blue"
    
    # Separators for Argentine Locale
    try:
        pio.templates[pio.templates.default].layout.separators = ",."
    except KeyError:
        pass

    df = load_data()
    df_centroids = load_centroids()
    df = apply_short_names(df)

    if df is None:
        st.error("No se encontraron datos. Por favor, ejecute el pipeline ETL primero.")
        return

    # --- Sidebar Filters ---
    st.sidebar.header("Filtros Globales")
    
    # Year Filter
    years = sorted(df['anio'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Seleccionar Año Base", years, index=0)
    
    # Province Filter (+ Select All)
    provinces = sorted(df['provincia_nombre'].unique())
    container = st.sidebar.container()
    all_provinces = st.sidebar.checkbox("Seleccionar todas las provincias", value=True)
    
    if all_provinces:
        selected_province = provinces
    else:
        selected_province = st.sidebar.multiselect("Seleccionar Provincia", provinces, default=provinces[:3])
    
    # Department Filter (Conditional for BA/CABA)
    selected_dept = []
    target_provinces = ["Buenos Aires", "Ciudad Autónoma de Buenos Aires"]
    # Check if any of the target provinces are selected
    show_dept_filter = any(p in target_provinces for p in selected_province)
    
    if show_dept_filter:
        # Create a display column for unambiguous selection: "Department (Province)"
        # We need to do this on a copy to avoid SettingWithCopy warnings if df is a slice (though here it's full df usually)
        # Actually df has this col now? No, we adding on the fly.
        
        # Filter DF to relevant provinces first to optimize
        df_dept_selection = df[df['provincia_nombre'].isin(selected_province)].copy()
        df_dept_selection['dept_display'] = df_dept_selection['departamento_nombre'] + " (" + df_dept_selection['provincia_nombre'] + ")"
        
        dept_options = sorted(df_dept_selection['dept_display'].unique())
        selected_dept = st.sidebar.multiselect("Filtrar por Departamento/Comuna", dept_options)

    # Crime Filter (Hierarchical)
    # 1. Select Category
    categories = sorted(CRIME_CATEGORIES.keys())
    # User requested a "Global Category" for a better panorama. "Robos y Hurtos" implies volume/general safety.
    # UPDATE: User requested "TODOS" by default for a complete panorama.
    selected_categories = st.sidebar.multiselect("Filtrar por Categoría", categories, default=categories)
    
    # 2. Filter available crime types based on category
    available_crimes = []
    if selected_categories:
        for cat in selected_categories:
            # Add crimes that are in the mapping AND in the dataframe (intersection)
            cat_crimes = CRIME_CATEGORIES.get(cat, [])
            valid_crimes = [c for c in cat_crimes if c in df['codigo_delito_snic_nombre'].unique()]
            available_crimes.extend(valid_crimes)
    else:
        # If no category selected, show None. This gives a "Clean Slate" feeling.
        available_crimes = []
    
    # Make unique and sort
    available_crimes = sorted(list(set(available_crimes)))
    
    # 3. Select Crime Types (Filtered)
    # User Request: "Panorama certero" -> Select ALL available crimes in the category by default
    default_s = available_crimes 
    
    # Use dynamic key to force reset when category changes.
    # This ensures that if I Add/Remove a category, the specific filter updates to select/deselect accordingly.
    # We use a hash of the selected categories to define the state.
    filter_key = f"crime_filter_{hash(tuple(sorted(selected_categories)))}"
    
    # Allow user to refine selection within category
    selected_crime = st.sidebar.multiselect("Seleccionar Tipo de Delito (Específico)", available_crimes, default=default_s, key=filter_key)
    
    # Mostrar referencias de los delitos seleccionados
    if selected_crime:
        # Create a mapping from Short Name -> Description
        short_to_desc = {}
        for long_name, desc in CRIME_DESCRIPTIONS.items():
            short_name = SHORT_NAMES.get(long_name, long_name)
            short_to_desc[short_name] = desc
            
        with st.sidebar.expander("ℹ️ ¿Qué significa cada delito?"):
            for crime in selected_crime:
                desc = short_to_desc.get(crime, "Sin descripción disponible.")
                st.markdown(f"**{crime}**: {desc}")

    # --- Data Filtering ---
    # Base filter
    mask = (
        (df['anio'] == selected_year) &
        (df['provincia_nombre'].isin(selected_province)) &
        (df['codigo_delito_snic_nombre'].isin(selected_crime))
    )
    
    # Apply Department filter if used
    if selected_dept:
        # Re-create the display column on the fly for the mask to match selection
        # Or parse the selection? Creating column on df is safer
        df['dept_display'] = df['departamento_nombre'] + " (" + df['provincia_nombre'] + ")"
        mask = mask & (df['dept_display'].isin(selected_dept))
        
    df_filtered = df[mask]
    
    # Data for trends (ignore year filter)
    # Re-apply dept filter for trends too logic-wise? Yes, usually users want the trend of the selection.
    trend_mask = (
        (df['provincia_nombre'].isin(selected_province)) &
        (df['codigo_delito_snic_nombre'].isin(selected_crime))
    )
    if selected_dept:
        # df already has dept_display from previous block if selected_dept is true
        trend_mask = trend_mask & (df['dept_display'].isin(selected_dept))
        
    df_trend = df[trend_mask]

    # --- Tabs Layout ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌎 Resumen General", "📈 Tendencias", "🔎 Detalle Geográfico", "🔮 Predicciones", "⚔️ Comparador", "📂 Datos"])

    # --- TAB 1: Resumen General ---
    with tab1:
        st.subheader(f"Panorama del Año {selected_year}")
        
        # --- Automatic Insights ---
        # Calculate interesting stats based on current filter (except year, we compare current year vs prev)
        if not df_filtered.empty:
            # 1. Top Crime Type
            top_crime = df_filtered.groupby('codigo_delito_snic_nombre')['cantidad_hechos'].sum().idxmax()
            top_crime_count = df_filtered.groupby('codigo_delito_snic_nombre')['cantidad_hechos'].sum().max()
            
            # 2. Province with highest increase vs previous year
            # (Needs filtered provinces context)
            df_prev_yr = df[(df['anio'] == selected_year - 1) & (df['provincia_nombre'].isin(selected_province))]
            if not df_prev_yr.empty:
                # Group by prov
                curr_prov = df_filtered.groupby('provincia_nombre')['cantidad_hechos'].sum()
                prev_prov = df_prev_yr.groupby('provincia_nombre')['cantidad_hechos'].sum()
                
                # Calculate change
                change = (curr_prov - prev_prov).sort_values(ascending=False)
                # Filter out NaN (provinces with no data in one of the years)
                change = change.dropna()
                
                if not change.empty:
                    worst_prov = change.index[0]
                    worst_increase = change.iloc[0]
                    best_prov = change.index[-1]
                    best_decrease = change.iloc[-1]
                    
                    # Display Insights
                    st.info(f"""
                    **💡 Insights Automáticos:**
                    - El delito más frecuente es **{top_crime}** con **{fmt_num(top_crime_count)}** hechos.
                    - **{worst_prov}** tuvo el mayor aumento de hechos (+{fmt_num(worst_increase)}) respecto al año anterior.
                    - **{best_prov}** registró la mayor disminución ({fmt_num(best_decrease)}).
                    """)
        
        # Metrics with Comparisons
        previous_year = selected_year - 1
        df_prev = df[
            (df['anio'] == previous_year) &
            (df['provincia_nombre'].isin(selected_province)) &
            (df['codigo_delito_snic_nombre'].isin(selected_crime))
        ]
        
        total_hechos = df_filtered['cantidad_hechos'].sum()
        total_hechos_prev = df_prev['cantidad_hechos'].sum()
        delta_hechos = total_hechos - total_hechos_prev
        delta_percent = (delta_hechos / total_hechos_prev * 100) if total_hechos_prev > 0 else 0
        
        total_victimas = df_filtered['cantidad_victimas'].sum()
        total_victimas_prev = df_prev['cantidad_victimas'].sum()
        delta_victimas = total_victimas - total_victimas_prev
        delta_victimas_percent = (delta_victimas / total_victimas_prev * 100) if total_victimas_prev > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Hechos", fmt_num(total_hechos), f"{fmt_num(delta_percent, 1)}% vs {previous_year}", delta_color="inverse")
        col2.metric("Total Víctimas", fmt_num(total_victimas), f"{fmt_num(delta_victimas_percent, 1)}% vs {previous_year}", delta_color="inverse")
        col3.metric("Provincias Filtradas", len(selected_province))

        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Top Provincias")
            
            # Ranking Type Toggle
            rank_type = st.radio("Criterio de Ranking:", ["Tasa c/100k hab", "Cantidad Total"], horizontal=True, label_visibility="collapsed")
            
            if not df_filtered.empty:
                # Logic: If department filter is active, show breakdown by department (Stacked Bar)
                if selected_dept:
                    # Department breakdown only makes sense for Count (Total). Rate per department requires population data per dept, which we might not have reliable here.
                    # Fallback to Total usually for Breakdown.
                    metric_col = 'cantidad_hechos'
                    df_prov = df_filtered.groupby(['provincia_nombre', 'departamento_nombre'])[metric_col].sum().reset_index()
                    
                    fig_bar = px.bar(
                        df_prov, 
                        x=metric_col, 
                        y='provincia_nombre', 
                        color='departamento_nombre', # Stack by department
                        orientation='h', 
                        text_auto='.2s',
                        title="Desglose por Departamento/Comuna (Cantidad)"
                    )
                else:
                    # Standard behavior: Aggregate by Province
                    if rank_type == "Cantidad Total":
                        metric_col = 'cantidad_hechos'
                        title_chart = "Top por Cantidad de Hechos"
                        df_prov = df_filtered.groupby('provincia_nombre')[metric_col].sum().reset_index().sort_values(metric_col, ascending=False).head(10)
                        
                        color_seq = ['#ff7f0e']
                    else:
                        # Dynamic Rate Calculation
                        df_prov = df_filtered.groupby('provincia_nombre')['cantidad_hechos'].sum().reset_index()
                        df_prov['tasa_hechos'] = calculate_rates(df_prov)
                        
                        metric_col = 'tasa_hechos'
                        title_chart = "Ranking por Tasa de Criminalidad (c/100k - Censo 2022)"
                        df_prov = df_prov.sort_values(metric_col, ascending=False).head(10)
                        
                        color_seq = ['#d62728']
                    
                    fig_bar = px.bar(
                        df_prov, 
                        x=metric_col, 
                        y='provincia_nombre', 
                        orientation='h', 
                        text_auto='.1f' if rank_type != "Cantidad Total" else '.2s',
                        color_discrete_sequence=color_seq,
                        title=title_chart
                    )
                
                fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_bar, use_container_width=True)
        
    # Reverse mapping for categorizing in charts
    crime_to_category = {crime: cat for cat, crimes in CRIME_CATEGORIES.items() for crime in crimes}

    # Use the existing c1, c2 columns from above (lines ~505)
    # They are already defined inside 'with tab1:' scope
    
    with c2:
        st.markdown("#### Distribución por Delito/Categoría")
        
        # Spacer to align with the radio button on the left column
        st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
        
        if not df_filtered.empty:
            # Logic: If too many crime types selected (>10), group by Category to avoid clutter
            unique_crimes = df_filtered['codigo_delito_snic_nombre'].nunique()
            
            if unique_crimes > 10:
                # Reverse map to get categories (already defined above loop, but safe to use)
                df_filtered['categoria_temp'] = df_filtered['codigo_delito_snic_nombre'].map(crime_to_category).fillna("Otros")
                
                df_pie = df_filtered.groupby('categoria_temp')['cantidad_hechos'].sum().reset_index()
                pie_names = 'categoria_temp'
                custom_data = ['categoria_temp'] # No desc available for cat
                hover_temp = "<b>%{label}</b><br>Hechos: %{value}"
            else:
                df_pie = df_filtered.groupby(['codigo_delito_snic_nombre', 'descripcion_delito'])['cantidad_hechos'].sum().reset_index()
                pie_names = 'codigo_delito_snic_nombre'
                custom_data = ['descripcion_delito']
                hover_temp = "<b>%{label}</b><br>Hechos: %{value}<br><i>%{customdata[0]}</i>"
            
            fig_pie = px.pie(
                df_pie, 
                values='cantidad_hechos', 
                names=pie_names,
                custom_data=custom_data,
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate=hover_temp
            )
            fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
            if unique_crimes > 10:
                st.caption("ℹ️ Se agruparon los delitos por categoría debido al volumen de datos.")


    # --- TAB 2: Tendencias ---
    with tab2:
        st.subheader("Evolución Histórica")
        
        if not df_trend.empty:
            st.markdown("De todos los años disponibles para la selección actual.")
            
            # Line Chart
            trend_data = df_trend.groupby(['anio', 'codigo_delito_snic_nombre', 'descripcion_delito'])['cantidad_hechos'].sum().reset_index()
            fig_line = px.line(
                trend_data, 
                x='anio', 
                y='cantidad_hechos', 
                color='codigo_delito_snic_nombre',
                custom_data=['descripcion_delito'],
                markers=True,
                title="Evolución de Hechos por Tipo de Delito"
            )
            fig_line.update_traces(
                hovertemplate="<b>%{x}</b><br>%{y:.0f} Hechos<br><i>%{customdata[0]}</i>"
            )
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Area Chart for Composition
            st.subheader("Composición de Delitos en el Tiempo")
            fig_area = px.area(
                trend_data, 
                x='anio', 
                y='cantidad_hechos', 
                color='codigo_delito_snic_nombre',
                custom_data=['descripcion_delito']
            )
        st.plotly_chart(fig_area, use_container_width=True)

    # --- TAB 3: Detalle Geográfico (Mapa Coroplético) ---
    with tab3:
        st.subheader("Distribución Geográfica")
        
        geojson = load_geojson()
        
        if not df_filtered.empty and geojson:
            # Prepare map data
            # Aggregate by Province
            map_data = df_filtered.groupby(['provincia_nombre'])['cantidad_hechos'].sum().reset_index()
            
            # Repopulate rates
            map_data['tasa_hechos'] = calculate_rates(map_data)
            
            # Map Metric Toggle
            map_metric = st.radio("Métrica del Mapa:", ["Tasa c/100k", "Cantidad Total"], horizontal=True, label_visibility="collapsed")
            
            val_col = 'tasa_hechos' if map_metric == "Tasa c/100k" else 'cantidad_hechos'
            title_legend = "Tasa (c/100k)" if map_metric == "Tasa c/100k" else "Total Hechos"
            
            fig_map = px.choropleth_mapbox(
                map_data,
                geojson=geojson,
                locations='provincia_nombre',
                featureidkey="properties.nombre",
                color=val_col,
                color_continuous_scale="Reds",
                mapbox_style="carto-darkmatter",
                zoom=3,
                center = {"lat": -38.4161, "lon": -63.6167},
                opacity=0.7,
                hover_name='provincia_nombre',
                hover_data={'cantidad_hechos': True, 'tasa_hechos': ':.2f', 'provincia_nombre': False}
            )
            
            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor="#020617",
                coloraxis_colorbar=dict(
                    title=title_legend,
                    bgcolor="rgba(0,0,0,0)",
                    title_font_color="#CBD5E1",
                    tickfont_color="#CBD5E1"
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)
            
            st.caption("ℹ️ El mapa utiliza geometrías oficiales de IGN/GeoRef. Regiones en gris no tienen datos para el filtro actual.")
        else:
            st.warning("No se pudo cargar el mapa o no hay datos filtrados.")

    # --- TAB 5: Predicciones ---
    with tab4:
        st.subheader("🔮 Predicción de Tendencias")
        st.markdown("""
        **Modelo**: Regresión Polinómica (Grado 2).  
        *Este modelo captura curvaturas en la tendencia (aceleración o desaceleración) mejor que una línea recta.*
        """)
        
        # Prediction Input
        years_to_predict = st.slider("Años a proyectar", 1, 5, 2)
        
        # Prepare Data for Prediction (Using current filters except year)
        # We predict based on the selected crime type(s) and province(s) aggregate
        
        if not df_trend.empty:
            # 1. Agregate data for time series
            ts_data = prepare_time_series(df_trend) # Aggregates all selected provinces/crimes
            
            # 2. Train and Predict
            pred_df, error = train_and_predict(ts_data, years_to_predict)
            
            if error:
                st.warning(error)
            else:
                # 3. Visualize
                fig_pred = go.Figure()
                
                # Historical Line
                hist = pred_df[pred_df['tipo'] == 'Histórico']
                fig_pred.add_trace(go.Scatter(
                    x=hist['anio'], y=hist['cantidad_hechos'],
                    mode='lines+markers', name='Histórico',
                    line=dict(color='blue')
                ))
                
                # Future Line
                future = pred_df[pred_df['tipo'] == 'Predicción']
                # Connect last historical point to first prediction
                last_hist = hist.iloc[-1]
                future_connect = pd.concat([hist.iloc[[-1]], future])
                
                fig_pred.add_trace(go.Scatter(
                    x=future_connect['anio'], y=future_connect['cantidad_hechos'],
                    mode='lines+markers', name='Predicción',
                    line=dict(color='red', dash='dot')
                ))
                
                fig_pred.update_layout(title="Proyección de Criminalidad", xaxis_title="Año", yaxis_title="Cantidad de Hechos")
                st.plotly_chart(fig_pred, use_container_width=True)
                
                st.info("Nota: Este modelo asume una tendencia lineal y sirve solo como referencia. No considera factores externos.")

    # --- TAB 5: Comparador ---
    with tab5:
        st.subheader("⚔️ Modo Versus: Comparador de Entidades")
        
        c_comp_1, c_comp_2 = st.columns(2)
        
        # Selectors (Independent of global province filter)
        all_provs = sorted(df['provincia_nombre'].unique())
        
        # Defaults requested: BA vs CABA
        try:
            default_ix_a = all_provs.index("Buenos Aires")
        except ValueError:
            default_ix_a = 0
            
        try:
            default_ix_b = all_provs.index("Ciudad Autónoma de Buenos Aires")
        except ValueError:
            default_ix_b = 1 if len(all_provs) > 1 else 0
        
        with c_comp_1:
            entity_a = st.selectbox("Entidad A", all_provs, index=default_ix_a)
        with c_comp_2:
            entity_b = st.selectbox("Entidad B", all_provs, index=default_ix_b)
         
        # Metric Selector
        st.write("") # Spacer
        comp_metric = st.radio("Métrica de Comparación:", ["Tasa c/100k hab", "Cantidad Total"], horizontal=True)
            
        if entity_a and entity_b:
            # Filter Data for both
            # Use same Crime selection as global
            
            mask_a = (df['provincia_nombre'] == entity_a) & (df['codigo_delito_snic_nombre'].isin(selected_crime))
            mask_b = (df['provincia_nombre'] == entity_b) & (df['codigo_delito_snic_nombre'].isin(selected_crime))
            
            df_a = df[mask_a]
            df_b = df[mask_b]
            
            # Metrics (Total Period or Selected Year?)
            # Let's use Selected Year for the "Scorecard"
            df_a_curr = df_a[df_a['anio'] == selected_year]
            df_b_curr = df_b[df_b['anio'] == selected_year]
            
            # Aggregate totals first
            total_a = df_a_curr['cantidad_hechos'].sum()
            total_b = df_b_curr['cantidad_hechos'].sum()
            
            # Population (Constant 2022 for simplicity in rate calc as per request "Censo 2022 constante")
            pop_a = PROVINCIA_POBLACION.get(NORM_PROVS.get(entity_a, entity_a), 1)
            pop_b = PROVINCIA_POBLACION.get(NORM_PROVS.get(entity_b, entity_b), 1)
            
            # Calculate Values based on Selection
            if comp_metric == "Tasa c/100k hab":
                val_a = (total_a / pop_a * 100000) if pop_a > 0 else 0
                val_b = (total_b / pop_b * 100000) if pop_b > 0 else 0
                label_prefix = "Tasa"
            else:
                val_a = total_a
                val_b = total_b
                label_prefix = "Total"
            
            col_a, col_vs, col_b = st.columns([2,1,2])
            with col_a:
                st.metric(f"{label_prefix} {entity_a} ({selected_year})", fmt_num(val_a, 1) if comp_metric == "Tasa c/100k hab" else f"{int(val_a):,}".replace(",", "."))
            with col_b:
                 st.metric(f"{label_prefix} {entity_b} ({selected_year})", fmt_num(val_b, 1) if comp_metric == "Tasa c/100k hab" else f"{int(val_b):,}".replace(",", "."))
            
            # Comparison Chart (Trend)
            # Group by Year
            trend_a = df_a.groupby('anio')['cantidad_hechos'].sum().reset_index()
            trend_a['Entidad'] = entity_a
            
            trend_b = df_b.groupby('anio')['cantidad_hechos'].sum().reset_index()
            trend_b['Entidad'] = entity_b
            
            # Calculate metric for trend logic
            if comp_metric == "Tasa c/100k hab":
                trend_a['valor'] = trend_a['cantidad_hechos'].apply(lambda x: (x / pop_a * 100000))
                trend_b['valor'] = trend_b['cantidad_hechos'].apply(lambda x: (x / pop_b * 100000))
                y_axis_title = "Tasa c/100k hab"
                chart_title_suffix = "Tasa c/100k"
            else:
                trend_a['valor'] = trend_a['cantidad_hechos']
                trend_b['valor'] = trend_b['cantidad_hechos']
                y_axis_title = "Cantidad de Hechos"
                chart_title_suffix = "Cantidad Total"

            trend_vs = pd.concat([trend_a, trend_b])
            
            fig_vs = px.line(
                trend_vs, x='anio', y='valor', color='Entidad',
                title=f"Evolución Comparativa: {chart_title_suffix} ({entity_a} vs {entity_b})",
                markers=True
            )
            fig_vs.update_layout(yaxis_title=y_axis_title, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_vs, use_container_width=True)
            
            if comp_metric == "Tasa c/100k hab":
                st.caption("ℹ️ Comparación basada en la Tasa cada 100k habitantes (Censo 2022 constante).")
    with tab6:
        st.subheader("Datos Crudos Filtrados")
        st.dataframe(df_filtered)
        
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Descargar CSV",
            data=csv,
            file_name=f"snic_data_{selected_year}.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
