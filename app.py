# SISTEMA DE NAVEGACIÓN ENES JURIQUILLA
# INTEGRANTES: Ávila Gónzález Jimena, Macías García Mayra, Pérez Rodríguez José Luis y Ramírez Conejo Christian Alexis
# 19 - May - 2026

import streamlit as st
import networkx as nx
from PIL import Image, ImageDraw, ImageFont
import base64

# Guardar en caché para los logos en Base64
@st.cache_data
def cargar_imagen_b64(ruta):
    try:
        with open(ruta, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

# CONFIGURACIÓN DE PÁGINA
try:
    icono_unam = Image.open("logo_unam_dorado.png")
except:
    icono_unam = "📍"

st.set_page_config(
    page_title="Navegador ENES Juriquilla", 
    layout="wide", 
    page_icon=icono_unam
)

# ESTILOS CSS (Inspirado en SIIAJ)
st.markdown("""
    <style>
    /* Importar fuente Roboto de Google */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Variables de colores UNAM */
    :root {
        --unam-blue: #002B5C;
        --unam-gold: #D4A106;
    }
    
    html, body, [class*="css"]  {
        font-family: 'Roboto', Helvetica, Arial, sans-serif !important;
    }
    
    /* Eliminar margenes blancos de streamlit */
    .block-container, div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
        margin-top: -1rem !important;
    }
    
    /* Eliminar por completo el header por defecto de Streamlit */
    header[data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
        opacity: 0 !important;
    }

    /* Estilo del encabezado institucional */
    .header-institucional {
        background-color: var(--unam-blue);
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px 20px;
        border-bottom: 4px solid var(--unam-gold);
        margin-bottom: 20px;
        color: white;
    }
    
    /* Diseño del título */
    .header-titulo {
        text-align: center;
        font-weight: bold;
        font-size: 45px;
        line-height: 1.2;
    }

    .logo-header {
        max-height: 100px;
        max-width: 100%;
        object-fit: contain;
        cursor: pointer;
    }
    
    /* Responsiva para celulares */
    @media (max-width: 768px) {
        .header-titulo {
            font-size: 20px !important;
        }
        .logo-header {
            max-height: 60px !important;
        }
        .header-institucional {
            padding: 10px 5px !important;
        }
    }

    /* Estilo del botón principal */
    div.stButton > button:first-child {
        background-color: var(--unam-blue) !important;
        color: white !important;
        border: 2px solid var(--unam-gold) !important;
        border-radius: 8px !important;
        width: 100% !important;
        height: 3em !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: var(--unam-gold) !important;
        color: var(--unam-blue) !important;
        border: 2px solid var(--unam-blue) !important;
    }

    /* Footer estático */
    .footer {
        width: 100%;
        background-color: var(--unam-blue);
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 14px;
        border-top: 4px solid var(--unam-gold);
        margin-top: 50px;
    }
    
    /* Dar un poco de margen interno al contenido principal */
    .contenido-principal {
        padding: 0 15px;
    }
            
    /* Redondear las esquinas del mapa */
    [data-testid="stImage"] img {
        border-radius: 20px !important;
        border: 2px solid var(--unam-gold) !important;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3) !important;
    }
            
    /* Redondear los mensajes de alerta */
    [data-testid="stAlert"] {
        border-radius: 15px !important;
        width: 90% !important;
        margin: 0 auto 15px auto !important;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.05) !important;
    }
            
    /* Agregar margen al mapa */
    [data-testid="stImage"] {
        width: 95% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        margin-bottom: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ENCABEZADO CON LOGOS (Cinta Azul)
img_unam = cargar_imagen_b64("logo_unam_dorado_1.png")
img_enes = cargar_imagen_b64("logo_enes_dorado.png")

html_header = f"""
<div class="header-institucional">
    <div style="width: 25%; text-align: left;">
        <a href="https://www.unam.mx/" target="_blank">
            <img class="logo-header" src="data:image/png;base64,{img_unam}">
        </a>
    </div>
    <div class="header-titulo" style="width: 50%;">
        Sistema de Navegación<br>ENES Juriquilla
    </div>
    <div style="width: 25%; text-align: right;">
        <a href="https://www.enesjuriquilla.unam.mx/" target="_blank">
            <img class="logo-header" src="data:image/png;base64,{img_enes}">
        </a>
    </div>
</div>
"""
st.markdown(html_header, unsafe_allow_html=True)

st.markdown('<div class="contenido-principal">', unsafe_allow_html=True)

# GENERACIÓN DEL GRAFO Y COORDENADAS DE LOS NODOS
@st.cache_resource
def generar_grafo():
    G = nx.Graph()
    rutas_ps = [('Salones de usos múltiples', 'Escaleras 1 sótano', 11), ('Escaleras 1 sótano', 'Baños 1 sótano', 5), ('Escaleras 1 sótano', 'Cafetería', 17), ('Cafetería', 'Juegos', 43), ('Juegos', 'Explanada', 3), ('Explanada', 'Escaleras 2 sótano', 12), ('Juegos', 'TIC', 5), ('Juegos', 'Deportes', 8), ('TIC', 'Intendencia de obras', 15), ('Intendencia de obras', 'Túnel de viento', 35), ('Túnel de viento', 'UIOYP', 5), ('UIOYP', 'Escaleras 3 sótano', 5), ('Escaleras 3 sótano', 'Baños 2 sótano', 5)]
    rutas_pb = [('Auditorio', 'Escaleras 1 planta baja', 29), ('Escaleras 1 planta baja', 'Baños 1 planta baja', 5), ('Escaleras 1 planta baja', 'Entrada', 16), ('Entrada', 'Recepción', 23), ('Recepción','Baños 2 planta baja', 17), ('Baños 2 planta baja','Escaleras 2 planta baja', 5), ('Escaleras 2 planta baja','Vitrinas', 5), ('Vitrinas','VI-PB01', 43), ('Escaleras 2 sótano', 'Microondas', 30.5), ('VI-PB01','Nutrición', 13), ('VI-PB01','VI-PB02', 8), ('VI-PB02','Médico', 13), ('VI-PB02', 'Lactancia', 13), ('VI-PB02', 'VI-PB03', 8), ('VI-PB03', 'Psicopedagogía', 13), ('VI-PB03', 'VI-PB04', 8), ('VI-PB04', 'CID planta baja', 13), ('VI-PB04', 'Escaleras 3 planta baja', 11), ('Escaleras 3 planta baja', 'Baños 3 planta baja', 5)]
    rutas_p1 = [('Escaleras 1 piso 1', 'Baños 1 piso 1', 5), ('Escaleras 1 piso 1', 'IV-101', 9), ('IV-101', 'IV-102', 16), ('IV-102', 'IV-103', 17), ('IV-103', 'Escaleras 2 piso 1', 15), ('Escaleras 2 piso 1', 'Baños 2 piso 1', 5), ('Escaleras 2 piso 1', 'V-101', 10), ('V-101', 'V-102', 18), ('V-102', 'Ajedrez', 31.5), ('CID piso 1', 'Ajedrez', 14), ('Ajedrez', 'Escaleras 3 piso 1', 13), ('Escaleras 3 piso 1', 'Baños 3 piso 1', 5)]
    rutas_p2 = [('III-201', 'III-202', 8), ('III-202', 'Secretaría administrativa', 8), ('Secretaría administrativa', 'Escaleras 1 piso 2', 11), ('Escaleras 1 piso 2', 'Baños 1 piso 2', 5), ('Escaleras 1 piso 2', 'Secretaría académica', 15.5), ('Secretaría académica', 'Secretaría general', 6.5), ('Secretaría general', 'Sala de juntas', 20), ('Sala de juntas', 'Dirección', 7.5), ('Dirección', 'Escaleras 2 piso 2', 8.5), ('Escaleras 2 piso 2', 'Baños 2 piso 2', 5), ('Escaleras 2 piso 2', 'Secretaría de educación y vinculación', 16), ('Secretaría de educación y vinculación', 'Servicios escolares', 17.5), ('Servicios escolares', 'VI-201', 16), ('VI-201', 'VI-202', 8), ('VI-202', 'VI-203', 8), ('VI-203', 'VI-204', 8), ('VI-204', 'Escaleras 3 piso 2', 5), ('Escaleras 3 piso 2', 'Baños 3 piso 2', 5)]
    rutas_p3 = [('III-301', 'III-302'   , 8), ('III-302', 'III-303', 8), ('III-303', 'III-304', 8), ('III-304', 'Escaleras 1 piso 3', 5), ('Escaleras 1 piso 3', 'Baños 1 piso 3', 5), ('Escaleras 1 piso 3', 'IV-301', 5), ('IV-301', 'IV-302', 8), ('IV-302', 'IV-303', 8), ('IV-303', 'IV-304', 8), ('IV-304', 'IV-305', 8), ('IV-305', 'Escaleras 2 piso 3', 5), ('Escaleras 2 piso 3', 'Baños 2 piso 3', 5), ('Escaleras 2 piso 3', 'V-301', 5), ('V-301', 'V-302', 8), ('V-302', 'V-303', 8), ('V-303', 'V-304', 8), ('V-304', 'VI-301', 8), ('VI-301', 'VI-302', 8), ('VI-302', 'VI-303', 8), ('VI-303', 'CID piso 3', 14), ('VI-303', 'VI-304', 8), ('VI-304', 'Escaleras 3 piso 3', 5), ('Escaleras 3 piso 3', 'Baños 3 piso 3', 5)]
    rutas_p4 = [('Zona de docentes 1', 'Escaleras 1 piso 4', 16), ('Escaleras 1 piso 4', 'Baños 1 piso 4', 5), ('Escaleras 1 piso 4', 'Zona de docentes 2', 17), ('Zona de docentes 2', 'Zona de docentes 3', 8), ('Zona de docentes 3', 'Zona de docentes 4', 8), ('Zona de docentes 4', 'Zona de docentes 5', 8), ('Zona de docentes 5', 'Escaleras 2 piso 4', 12), ('Escaleras 2 piso 4', 'Baños 2 piso 4', 5), ('Escaleras 2 piso 4', 'V-401', 10), ('V-401', 'V-402', 8), ('V-402', 'V-403', 8), ('V-403', 'V-404', 8), ('V-404', 'VI-401', 8), ('VI-401', 'VI-402', 8), ('VI-402', 'CID piso 4', 14), ('VI-402', 'VI-403', 8), ('VI-403', 'VI-404', 8), ('VI-404', 'Escaleras 3 piso 4', 5), ('Escaleras 3 piso 4', 'Baños 3 piso 4', 5)]
    rutas_p5 = [('Paneles solares', 'Escaleras 1 piso 5', 5), ('Escaleras 1 piso 5', 'Baños 1 piso 5', 5), ('Escaleras 1 piso 5', 'Escaleras 2 piso 5', 55), ('Jardineras', 'Escaleras 2 piso 5', 12), ('Gym al aire libre', 'Escaleras 2 piso 5', 30.5 ), ('Escaleras 2 piso 5', 'Baños 2 piso 5', 5), ('Gym al aire libre', 'Escaleras 3 piso 5', 35)]
    escaleras = [('Escaleras 1 sótano', 'Escaleras 1 planta baja', 5), ('Escaleras 2 sótano', 'Vitrinas', 5), ('Escaleras 3 sótano', 'Escaleras 3 planta baja', 5), ('Escaleras 1 planta baja', 'Escaleras 1 piso 1', 5), ('Escaleras 2 planta baja', 'Escaleras 2 piso 1', 5), ('Escaleras 3 planta baja', 'Escaleras 3 piso 1', 5), ('Escaleras 1 piso 1', 'Escaleras 1 piso 2', 5), ('Escaleras 2 piso 1', 'Escaleras 2 piso 2', 5), ('Escaleras 3 piso 1', 'Escaleras 3 piso 2', 5), ('Escaleras 1 piso 2', 'Escaleras 1 piso 3', 5), ('Escaleras 2 piso 2', 'Escaleras 2 piso 3', 5), ('Escaleras 3 piso 2', 'Escaleras 3 piso 3', 5), ('Escaleras 1 piso 3', 'Escaleras 1 piso 4', 5), ('Escaleras 2 piso 3', 'Escaleras 2 piso 4', 5), ('Escaleras 3 piso 3', 'Escaleras 3 piso 4', 5), ('Escaleras 1 piso 4', 'Escaleras 1 piso 5', 5), ('Escaleras 2 piso 4', 'Escaleras 2 piso 5', 5), ('Escaleras 3 piso 4', 'Escaleras 3 piso 5', 5)]

    G.add_weighted_edges_from(rutas_ps + rutas_pb + rutas_p1 + rutas_p2 + rutas_p3 + rutas_p4 + rutas_p5 + escaleras)
    return G

pos = {
    # Mapeo de Sótano
    'Escaleras 1 sótano': (7, -0.25), 'Escaleras 1 planta baja': (7, 0.5),
    'Escaleras 2 sótano': (35, 0.5), 'Escaleras 2 planta baja': (26, 1),
    'Escaleras 3 sótano': (50, 0.75), 'Escaleras 3 planta baja': (50, 1.25),
    'Salones de usos múltiples': (2, -0.25),
    'Cafetería': (21, 0.25), 'Juegos': (25.5, 0.375), 'Deportes': (30, 0.375), 'Explanada': (27, 0),
    'TIC': (24.25, 0.75), 'Intendencia de obras': (31, 0.75), 
    'Túnel de viento': (43, 0.75), 'UIOYP': (48, 0.5),
    'Baños 1 sótano': (9, 0),
    'Baños 2 sótano': (51, 0.875),

    # Mapeo Planta Baja 
    'Auditorio': (1, 0.5),
    'Entrada': (16, 0.75),
    'Recepción': (20, 1),
    'Baños 1 planta baja': (9, 0.625),
    'Baños 2 planta baja': (25, 1.125),
    'Baños 3 planta baja': (51, 1.375),
    'Vitrinas': (31, 1),
    'VI-PB01': (38, 1.25),
    'Microondas': (36, -0.5),
    'VI-PB02': (41, 1.25),
    'VI-PB03': (44, 1.25),
    'VI-PB04': (47, 1.25),
    'Nutrición': (38, 1),
    'Médico': (40, 1),
    'Lactancia': (42, 1),
    'Psicopedagogía': (44, 1),
    'CID planta baja': (46, 1),

    # Mapeo Piso 1 
    'Escaleras 1 piso 1': (7, 1.125),
    'Escaleras 2 piso 1': (26, 1.8),
    'Escaleras 3 piso 1': (50, 1.8),
    'Baños 1 piso 1': (9, 1.375),
    'Baños 2 piso 1': (27, 1.9),
    'Baños 3 piso 1': (51, 1.9),
    'IV-101': (13, 1.275), 'IV-102': (18.2, 1.5), 'IV-103': (22, 1.7),
    'V-101': (31, 1.8), 'V-102': (34, 1.8),
    'Ajedrez': (44, 1.8),
    'CID piso 1': (45, 1.5),
    
    # Mapeo Piso 2 
    'Escaleras 1 piso 2': (7, 1.8),
    'Escaleras 2 piso 2': (26, 2.30),
    'Escaleras 3 piso 2': (50, 2.45),
    'III-201': (-4, 1.75), 'III-202': (-1.5, 1.75), 'Secretaría administrativa': (4, 1.8),
    'Secretaría académica': (12, 1.95), 'Secretaría general': (15, 2.05), 'Sala de juntas': (19, 2.15), 'Dirección': (22, 2.25),
    'Secretaría de educación y vinculación': (30, 2.45), 'Servicios escolares': (34, 2.45),
    'VI-201': (38, 2.45), 'VI-202': (41, 2.45), 'VI-203': (44, 2.45), 'VI-204': (47, 2.45),
    'Baños 1 piso 2': (9, 1.95), 
    'Baños 2 piso 2': (27, 2.45), 
    'Baños 3 piso 2': (51, 2.55),

    # Mapeo Piso 3
    'Escaleras 1 piso 3': (7, 2.3),
    'Escaleras 2 piso 3': (26, 2.9),
    'Escaleras 3 piso 3': (50, 3),
    'III-301': (-4, 2.3), 'III-302': (-1.5, 2.3), 'III-303': (1, 2.3), 'III-304': (4.5, 2.3),
    'IV-301': (12, 2.5), 'IV-302': (15, 2.60), 'IV-303': (17, 2.65), 'IV-304': (20, 2.72), 'IV-305': (22, 2.8),
    'V-301': (29, 3), 'V-302': (31, 3), 'V-303': (33, 3), 'V-304': (35.5, 3),
    'VI-301': (38, 3), 'VI-302': (41, 3), 'VI-303': (44, 3), 'VI-304': (47, 3),
    'CID piso 3': (45, 2.75),
    'Baños 1 piso 3': (9, 2.45), 
    'Baños 2 piso 3': (27, 3.1), 
    'Baños 3 piso 3': (51, 3.15),

    # Mapeo Piso 4
    'Escaleras 1 piso 4': (7, 3),
    'Escaleras 2 piso 4': (26, 3.5),
    'Escaleras 3 piso 4': (50, 3.5),
    'Zona de docentes 1': (3, 3),
    'Zona de docentes 2': (14, 3.2), 'Zona de docentes 3': (17, 3.3), 'Zona de docentes 4': (20, 3.4), 'Zona de docentes 5': (22, 3.45),
    'V-401': (29, 3.5), 'V-402': (31, 3.5), 'V-403': (33, 3.5), 'V-404': (35.5, 3.5),
    'VI-401': (38, 3.5), 'VI-402': (41, 3.5), 'VI-403': (44, 3.5), 'VI-404': (47, 3.5),
    'CID piso 4': (42.7, 3.25),
    'Baños 1 piso 4': (9, 3.2), 
    'Baños 2 piso 4': (27, 3.65), 
    'Baños 3 piso 4': (51, 3.65),

    # Mapeo Piso 5
    'Escaleras 1 piso 5': (7, 3.6),
    'Escaleras 2 piso 5': (26, 4),
    'Escaleras 3 piso 5': (50, 4),
    'Paneles solares': (0, 3.7),
    'Jardineras': (20, 3.9), 'Gym al aire libre': (39, 3.9),
    'Baños 1 piso 5': (9, 3.85), 'Baños 2 piso 5': (31, 4.2)
    }

directorio_profes = {
    "Dr. Heriberto Ruiz Tafoya": "Zona de docentes 1", "Dra. Ana Paola Galicia Gallardo": "Zona de docentes 1", 
    "Dr. Javier Sanchez Lopez": "Zona de docentes 1", "Dr. Jesus Arturo Muñiz Jauregui": "Zona de docentes 1", 
    "Dra. Diana Cristina Martinez Casillas": "Zona de docentes 1", "Dr. Jesus Emmanuel Solis Perez": "Zona de docentes 1", 
    "Dr. Jose Carlos Ramirez Sanchez": "Zona de docentes 1", "Dra. Maria Guadalupe Garcia Gomar": "Zona de docentes 1", 
    "Dr. Dante Ruiz Robles": "Zona de docentes 1", "Dra. Martha Cecilia Herrera Garcia": "Zona de docentes 1", 
    "Dr. Mario Santana Cibrian": "Zona de docentes 1", "Dr. Hugo Harlan Mejia Madrid": "Zona de docentes 1", 
    "Dr. Alberto Padro": "Zona de docentes 2", "Dra. Iliana del Rocio": "Zona de docentes 2", 
    "Dr. Octavio Diaz": "Zona de docentes 2", "Dr. Raide A. Gonzalez": "Zona de docentes 3", 
    "Dra. Marie C. Bedos": "Zona de docentes 3", "Dr. Raul Iturralde": "Zona de docentes 3", 
    "Dr. Adolfo V. Magaldi": "Zona de docentes 3", "Dr. Jesus A. Franco": "Zona de docentes 3", 
    "Dra. Marisol de la Mora": "Zona de docentes 3", "Dra. Elisa Ventura": "Zona de docentes 4", 
    "Dr. Quetzalcoatl Cruz": "Zona de docentes 4", "Dr. David O. Perez": "Zona de docentes 4", 
    "Dra. Rosario Vazquez": "Zona de docentes 4", "Dr. Ulises Olivares": "Zona de docentes 4", 
    "Dra. Criseida Ruiz": "Zona de docentes 5", "Dr. Abdiel Hernandez": "Zona de docentes 5", 
    "Dra. Monica A. Lopez": "Zona de docentes 5"}

G = generar_grafo()

# INTERFAZ DE USUARIO

# Contenedor de instrucciones
st.markdown("<h3 style='text-align: center;'>🗺️ ¿Cómo usar el navegador?</h3>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-bottom: 15px;'>
1. 📍 <b>Estás en:</b> Selecciona tu ubicación actual.<br>
2. 🎯 <b>Vas a:</b> Elige tu destino (área o docente).<br>
3. Haz clic en <b>Trazar Ruta</b>.<br><br>
</div>
""", unsafe_allow_html=True)

with st.expander("¿Cómo funciona esta tecnología?"):
    st.markdown(" Este sistema modela la infraestructura de la escuela usando la **Teoría de Grafos**. Para encontrar el camino exacto," \
    " utiliza el **Algoritmo de Dijkstra**, calculando la ruta más corta y eficiente entre los diferentes pisos del edificio.")

st.markdown("<br>", unsafe_allow_html=True)

# Separadores 
sep_aulas = "🏢 --- ÁREAS Y AULAS ---"
sep_docentes = "👨‍🏫 --- DOCENTES ---"

# Listas pre-calculadas 
nodos_ordenados = sorted(list(G.nodes()))
profes_ordenados = sorted(list(directorio_profes.keys()))
opciones_destino = [sep_aulas] + nodos_ordenados + [sep_docentes] + profes_ordenados

# Cajas a ancho completo
origen = st.selectbox("📍 Estás en:", nodos_ordenados)
seleccion = st.selectbox("🎯 Vas a:", opciones_destino)

st.markdown("<br>", unsafe_allow_html=True)

# Botón a ancho completo
boton_trazar = st.button("Trazar Ruta", use_container_width=True)

# LÓGICA DE DIBUJO
if boton_trazar:
    # Validamos que no elijan los separadores
    if seleccion == sep_aulas or seleccion == sep_docentes:
        st.warning("⚠️ Por favor, selecciona un destino válido debajo de los separadores.")
    else:
        destino_real = directorio_profes.get(seleccion, seleccion)
        
        try:
            # Implementación rápida de Dijkstra
            distancia, ruta = nx.bidirectional_dijkstra(G, source=origen, target=destino_real, weight='weight')
    
            st.success(f"✅ ¡Ruta Encontrada! Distancia aproximada: {distancia} metros")
            st.info(f"🧭 **Camino a seguir:** {' ➔ '.join(ruta)}")

            # --- DIBUJO INSTANTÁNEO CON PILLOW ---
            # 1. Cargar la imagen base
            img = Image.open('foto_enes(2).webp').convert('RGBA')
            
            # Crear una capa transparente del mismo tamaño para dibujar la ruta
            capa_ruta = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(capa_ruta)

            W, H = img.size

            # 2. Función traductora: Convierte las coordenadas del grafo a píxeles de tu foto
            def a_pixeles(x, y):
                # Según tus límites originales de Matplotlib
                px_x = int(((x - (-8)) / 62) * W)
                px_y = int(H - (((y - (-1.5)) / 7.5) * H))
                return px_x, px_y

            # 3. Dibujar las líneas de la ruta
            for u, v in zip(ruta, ruta[1:]):
                x1, y1 = a_pixeles(pos[u][0], pos[u][1])
                x2, y2 = a_pixeles(pos[v][0], pos[v][1])
                # Ajusta el grosor según te parezca mejor (15 es buen punto de partida para fotos grandes)
                draw.line([(x1, y1), (x2, y2)], fill="#D4A106", width=15)

            # 4. Dibujar los puntos blancos intermedios
            nodos_intermedios = ruta[1:-1]
            radio_int = 8
            for nodo in nodos_intermedios:
                px, py = a_pixeles(pos[nodo][0], pos[nodo][1])
                draw.ellipse([(px - radio_int, py - radio_int), (px + radio_int, py + radio_int)], 
                             fill="white", outline="#002B5C", width=4)

            # 5. Configurar la fuente para los letreros
            # Pillow intenta buscar una fuente instalada en el sistema. 
            # Si estás en Windows usa Arial, en servidores web usa una libre, si falla usa la básica.
            try:
                fuente = ImageFont.truetype("arial.ttf", 36)
            except IOError:
                try:
                    fuente = ImageFont.truetype("DejaVuSans.ttf", 36)
                except IOError:
                    try:
                        # Fallback moderno para versiones nuevas de Pillow
                        fuente = ImageFont.load_default(size=36)
                    except:
                        # Fallback clásico
                        fuente = ImageFont.load_default()

            # 6. Dibujar nodo de Origen (Azul) y Letrero
            px_orig, py_orig = a_pixeles(pos[origen][0], pos[origen][1])
            radio_ext = 22
            draw.ellipse([(px_orig - radio_ext, py_orig - radio_ext), (px_orig + radio_ext, py_orig + radio_ext)], 
                         fill="#002B5C", outline="white", width=6)
            
            # Letrero de Origen
            texto_inicio = f"📍 Inicio: {origen}"
            draw.text((px_orig, py_orig - 40), texto_inicio, fill="white", font=fuente, anchor="ms", 
                      stroke_width=4, stroke_fill="#002B5C")

            # 7. Dibujar nodo de Destino (Dorado) y Letrero
            px_dest, py_dest = a_pixeles(pos[destino_real][0], pos[destino_real][1])
            draw.ellipse([(px_dest - radio_ext, py_dest - radio_ext), (px_dest + radio_ext, py_dest + radio_ext)], 
                         fill="#D4A106", outline="white", width=6)
            
            # Letrero de Destino
            texto_destino = f"🎯 Destino: {seleccion}"
            draw.text((px_dest, py_dest - 40), texto_destino, fill="white", font=fuente, anchor="ms", 
                      stroke_width=4, stroke_fill="#D4A106")

            # 8. Combinar la foto original con la ruta dibujada
            img_final = Image.alpha_composite(img, capa_ruta)

            # 9. Mostrar en pantalla
            st.image(img_final, use_container_width=True)

        except nx.NetworkXNoPath:
            st.error("❌ No se encontró una ruta válida entre estos dos puntos.")
        except Exception as e:
            st.error(f"❌ Error al procesar: {e}")

else:
    # MAPA INICIAL ESTÁTICO
    st.info("👆 Selecciona tu ubicación y destino arriba para trazar la ruta.")
    
    try:
        st.image("mapa_guia.png", use_container_width=True)
    except Exception as e:
        st.warning(f"❌ Error al cargar el mapa guía: {e}")

# FOOTER INSTITUCIONAL 
st.markdown("""
    <div class="footer">
        Hecho en México, Universidad Nacional Autónoma de México (UNAM).<br>
        Desarrollado por estudiantes de la Licenciatura en Tecnología, ENES Juriquilla.<br>
        © 2026 Todos los derechos reservados.
    </div>
    """, unsafe_allow_html=True)
