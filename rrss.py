import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import zipfile
import io
import openpyxl

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Dashboard Redes Sociales 2026",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONFIGURACIÓN DE USUARIOS
# ============================================
USERS = {
    "admin": {
        "password": "admin123",
        "name": "Administrador",
        "role": "admin",
        "avatar": "👨‍💼"
    },
    "social": {
        "password": "social123",
        "name": "Community Manager",
        "role": "social",
        "avatar": "📱"
    },
    "analyst": {
        "password": "analyst123",
        "name": "Analista",
        "role": "analyst",
        "avatar": "📊"
    }
}

# ============================================
# FUNCIONES DE AUTENTICACIÓN
# ============================================

def check_password(username, password):
    """Verifica las credenciales"""
    if username in USERS:
        return USERS[username]["password"] == password
    return False

def login_form():
    """Muestra el formulario de login"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 50px;'>📱 Dashboard Redes Sociales 2026</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray; margin-bottom: 30px;'>Análisis de métricas de redes sociales</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuario", placeholder="Ej: admin, social, analyst")
            password = st.text_input("🔑 Contraseña", type="password", placeholder="••••••••")
            
            submitted = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
            
            if submitted:
                if check_password(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["user_info"] = USERS[username]
                    st.session_state["login_time"] = datetime.now()
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; font-size: 0.9em; color: gray; background: #f0f2f6; padding: 15px; border-radius: 10px;'>
        <p><strong>🔐 Usuarios de prueba:</strong></p>
        <p>👨‍💼 <strong>admin</strong> / admin123 (Acceso total)</p>
        <p>📱 <strong>social</strong> / social123 (Community Manager)</p>
        <p>📊 <strong>analyst</strong> / analyst123 (Analista)</p>
        </div>
        """, unsafe_allow_html=True)

def logout():
    """Cierra la sesión del usuario"""
    keys_to_clear = ["authenticated", "username", "user_info", "login_time", "data_source"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ============================================
# FUNCIÓN CORREGIDA PARA CARGAR EL ARCHIVO
# ============================================

def cargar_archivo_excel(archivo):
    """Carga archivo Excel directamente desde ZIP o archivo normal"""
    try:
        # Leer los bytes del archivo
        contenido_bytes = archivo.read()
        
        # Verificar si es un archivo ZIP (PK es la firma de ZIP)
        if contenido_bytes[:2] == b'PK':
            st.info("📦 Detectado archivo ZIP, leyendo Excel directamente...")
            
            # El archivo es un Excel comprimido, podemos leerlo directamente
            try:
                # Intentar leer como Excel directamente desde los bytes
                df = pd.read_excel(io.BytesIO(contenido_bytes), engine='openpyxl')
                st.success("✅ Archivo Excel cargado correctamente desde ZIP")
                return procesar_dataframe(df)
            except Exception as e:
                st.error(f"Error al leer Excel desde ZIP: {str(e)}")
                
                # Si falla, intentar abrir como ZIP y buscar el archivo
                try:
                    with zipfile.ZipFile(io.BytesIO(contenido_bytes)) as zip_file:
                        # Buscar cualquier archivo con extensión .xlsx o .xls
                        archivos_excel = [f for f in zip_file.namelist() 
                                        if f.endswith('.xlsx') or f.endswith('.xls')]
                        
                        if archivos_excel:
                            st.info(f"📄 Archivo Excel encontrado: {archivos_excel[0]}")
                            with zip_file.open(archivos_excel[0]) as excel_file:
                                df = pd.read_excel(io.BytesIO(excel_file.read()), engine='openpyxl')
                                return procesar_dataframe(df)
                        else:
                            st.error("No se encontró archivo Excel en el ZIP")
                            return None
                except:
                    st.error("No se pudo procesar el archivo ZIP")
                    return None
        
        # Si no es ZIP, intentar leer directamente como Excel
        else:
            try:
                df = pd.read_excel(io.BytesIO(contenido_bytes), engine='openpyxl')
                st.success("✅ Archivo Excel cargado correctamente")
                return procesar_dataframe(df)
            except Exception as e:
                st.error(f"Error al leer archivo Excel: {str(e)}")
                return None
                
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
        return None

def procesar_dataframe(df):
    """Procesa el DataFrame y formatea las columnas correctamente"""
    
    # Limpiar nombres de columnas
    df.columns = [col.strip() for col in df.columns]
    
    # Mostrar columnas encontradas
    st.info(f"Columnas encontradas: {list(df.columns)}")
    
    # Convertir fecha
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%B')
        df['Day_Name'] = df['Date'].dt.day_name()
    
    # Lista de columnas numéricas
    columnas_numericas = [
        'Impressions', 'Views', 'Reach', 'Likes', 'Comments/Replies', 
        'Shares', 'Saves', 'Profile Clicks', 'URL Clicks', 'Link Clicks',
        'Tag Clicks', 'Open Detail', 'Permanent Links', 
        'Multimedia Content Interactions', 'Interacciones', 'E.R.'
    ]
    
    # Convertir columnas numéricas
    for col in columnas_numericas:
        if col in df.columns:
            # Convertir a string, reemplazar comas y espacios
            df[col] = df[col].astype(str).str.replace(',', '').str.replace(' ', '').str.strip()
            # Reemplazar valores vacíos con 0
            df[col] = df[col].replace(['', 'nan', 'NaN', 'None', '-'], '0')
            # Convertir a numérico
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Calcular Interacciones si no existe
    if 'Interacciones' not in df.columns:
        cols_interaccion = ['Likes', 'Comments/Replies', 'Shares', 'Saves', 
                           'Profile Clicks', 'URL Clicks', 'Link Clicks',
                           'Tag Clicks', 'Open Detail', 'Permanent Links',
                           'Multimedia Content Interactions']
        df['Interacciones'] = 0
        for col in cols_interaccion:
            if col in df.columns:
                df['Interacciones'] += df[col]
    
    return df

def generar_datos_ejemplo():
    """Genera datos de ejemplo para redes sociales"""
    np.random.seed(42)
    
    fechas = pd.date_range(start='2026-01-01', end='2026-03-31', freq='D')
    plataformas = ['Instagram', 'TikTok', 'Twitter', 'YouTube', 'Facebook']
    formatos = ['Carrusel', 'Reel', 'Video', 'Foto', 'Shorts']
    generos = ['Drama', 'Comedia', 'Acción', 'Romance', 'Animación']
    
    datos = []
    for fecha in fechas:
        for _ in range(np.random.randint(5, 15)):
            platform = np.random.choice(plataformas)
            impressions = np.random.randint(1000, 100000)
            views = int(impressions * np.random.uniform(0.3, 0.9))
            reach = int(impressions * np.random.uniform(0.6, 0.95))
            likes = int(views * np.random.uniform(0.01, 0.08))
            comments = int(likes * np.random.uniform(0.05, 0.3))
            shares = int(views * np.random.uniform(0.002, 0.02))
            
            interacciones = likes + comments + shares
            
            if platform == 'Instagram':
                er = (interacciones / reach) * 100 if reach > 0 else 0
            elif platform in ['TikTok', 'YouTube']:
                er = (interacciones / views) * 100 if views > 0 else 0
            elif platform == 'Twitter':
                er = (interacciones / impressions) * 100 if impressions > 0 else 0
            else:
                er = (interacciones / reach) * 100 if reach > 0 else 0
            
            datos.append({
                'Platform': platform,
                'Date': fecha,
                'Impressions': impressions,
                'Views': views,
                'Reach': reach,
                'Likes': likes,
                'Comments/Replies': comments,
                'Shares': shares,
                'Interacciones': interacciones,
                'E.R.': round(er, 2),
                'Formato': np.random.choice(formatos),
                'Género': np.random.choice(generos),
                'Título': f"Post de ejemplo {np.random.randint(1, 100)}",
                'PV_Content Format': np.random.choice(['Trailer', 'Clip', 'Behind Scenes']),
                'PV_Content Format Group': np.random.choice(['Video', 'Image'])
            })
    
    return pd.DataFrame(datos)

# ============================================
# FUNCIONES DE ANÁLISIS
# ============================================

def calcular_kpis_social(df):
    """Calcula KPIs específicos para redes sociales"""
    kpis = {}
    
    kpis['total_posts'] = len(df)
    kpis['total_impressions'] = df['Impressions'].sum() if 'Impressions' in df.columns else 0
    kpis['total_views'] = df['Views'].sum() if 'Views' in df.columns else 0
    kpis['total_reach'] = df['Reach'].sum() if 'Reach' in df.columns else 0
    kpis['total_interacciones'] = df['Interacciones'].sum() if 'Interacciones' in df.columns else 0
    
    kpis['avg_impressions'] = df['Impressions'].mean() if 'Impressions' in df.columns else 0
    kpis['avg_views'] = df['Views'].mean() if 'Views' in df.columns else 0
    kpis['avg_reach'] = df['Reach'].mean() if 'Reach' in df.columns else 0
    kpis['avg_interacciones'] = df['Interacciones'].mean() if 'Interacciones' in df.columns else 0
    kpis['avg_er'] = df['E.R.'].mean() if 'E.R.' in df.columns else 0
    
    return kpis

def analisis_por_plataforma(df):
    """Análisis detallado por plataforma"""
    if 'Platform' not in df.columns:
        return pd.DataFrame()
    
    columnas_analisis = ['Impressions', 'Views', 'Reach', 'Interacciones', 'Likes', 'E.R.']
    columnas_existentes = [col for col in columnas_analisis if col in df.columns]
    
    if not columnas_existentes:
        return df.groupby('Platform').size().reset_index(name='Posts')
    
    agg_dict = {}
    for col in columnas_existentes:
        if col == 'E.R.':
            agg_dict[col] = 'mean'
        else:
            agg_dict[col] = 'sum'
    
    analisis = df.groupby('Platform').agg(agg_dict).round(2).reset_index()
    conteo = df.groupby('Platform').size().reset_index(name='Posts')
    analisis = analisis.merge(conteo, on='Platform')
    
    # Ordenar por interacciones de mayor a menor
    if 'Interacciones' in analisis.columns:
        analisis = analisis.sort_values('Interacciones', ascending=False)
    
    # Orden consistente de columnas
    columnas_orden = ['Platform', 'Posts', 'Impressions', 'Views', 'Reach', 'Interacciones', 'Likes', 'E.R.']
    columnas_orden = [col for col in columnas_orden if col in analisis.columns]
    
    return analisis[columnas_orden]

def analisis_por_titulo(df, top_n=15):
    """Análisis por título de contenido"""
    if 'Título' not in df.columns:
        return pd.DataFrame()
    
    analisis = df.groupby('Título').agg({
        'Impressions': 'sum' if 'Impressions' in df.columns else 'count',
        'Views': 'sum' if 'Views' in df.columns else 'count',
        'Interacciones': 'sum' if 'Interacciones' in df.columns else 'count',
        'E.R.': 'mean' if 'E.R.' in df.columns else 'mean',
    }).round(2).reset_index()
    
    # Agregar conteo de posts
    conteo = df.groupby('Título').size().reset_index(name='Posts')
    analisis = analisis.merge(conteo, on='Título')
    
    # Ordenar por interacciones de mayor a menor
    if 'Interacciones' in analisis.columns:
        analisis = analisis.sort_values('Interacciones', ascending=False).head(top_n)
    
    # Orden consistente
    columnas_orden = ['Título', 'Posts', 'Impressions', 'Views', 'Interacciones', 'E.R.']
    columnas_orden = [col for col in columnas_orden if col in analisis.columns]
    
    return analisis[columnas_orden]

def analisis_por_genero(df):
    """Análisis por género de contenido"""
    if 'Género' not in df.columns:
        return pd.DataFrame()
    
    analisis = df.groupby('Género').agg({
        'Impressions': 'sum' if 'Impressions' in df.columns else 'count',
        'Views': 'sum' if 'Views' in df.columns else 'count',
        'Interacciones': 'sum' if 'Interacciones' in df.columns else 'count',
        'E.R.': 'mean' if 'E.R.' in df.columns else 'mean',
    }).round(2).reset_index()
    
    # Agregar conteo de posts
    conteo = df.groupby('Género').size().reset_index(name='Posts')
    analisis = analisis.merge(conteo, on='Género')
    
    # Ordenar por interacciones de mayor a menor
    if 'Interacciones' in analisis.columns:
        analisis = analisis.sort_values('Interacciones', ascending=False)
    
    # Orden consistente
    columnas_orden = ['Género', 'Posts', 'Impressions', 'Views', 'Interacciones', 'E.R.']
    columnas_orden = [col for col in columnas_orden if col in analisis.columns]
    
    return analisis[columnas_orden]

def analisis_por_formato(df):
    """Análisis por formato de contenido"""
    if 'Formato' not in df.columns:
        return pd.DataFrame()
    
    analisis = df.groupby('Formato').agg({
        'Impressions': 'sum' if 'Impressions' in df.columns else 'count',
        'Views': 'sum' if 'Views' in df.columns else 'count',
        'Interacciones': 'sum' if 'Interacciones' in df.columns else 'count',
        'E.R.': 'mean' if 'E.R.' in df.columns else 'mean',
    }).round(2).reset_index()
    
    # Calcular posts y promedio
    conteo = df.groupby('Formato').size().reset_index(name='Posts')
    analisis = analisis.merge(conteo, on='Formato')
    analisis['Interacciones Promedio'] = (analisis['Interacciones'] / analisis['Posts']).round(0)
    
    # Ordenar por interacciones de mayor a menor
    if 'Interacciones' in analisis.columns:
        analisis = analisis.sort_values('Interacciones', ascending=False)
    
    # Orden consistente
    columnas_orden = ['Formato', 'Posts', 'Impressions', 'Views', 'Interacciones', 'Interacciones Promedio', 'E.R.']
    columnas_orden = [col for col in columnas_orden if col in analisis.columns]
    
    return analisis[columnas_orden]

def analisis_por_content_format(df):
    """Análisis por PV Content Format"""
    if 'PV_Content Format' not in df.columns:
        return pd.DataFrame()
    
    analisis = df.groupby('PV_Content Format').agg({
        'Impressions': 'sum' if 'Impressions' in df.columns else 'count',
        'Views': 'sum' if 'Views' in df.columns else 'count',
        'Interacciones': 'sum' if 'Interacciones' in df.columns else 'count',
        'E.R.': 'mean' if 'E.R.' in df.columns else 'mean',
    }).round(2).reset_index()
    
    # Calcular posts y promedio
    conteo = df.groupby('PV_Content Format').size().reset_index(name='Posts')
    analisis = analisis.merge(conteo, on='PV_Content Format')
    analisis['Interacciones Promedio'] = (analisis['Interacciones'] / analisis['Posts']).round(0)
    
    # Ordenar por interacciones de mayor a menor
    if 'Interacciones' in analisis.columns:
        analisis = analisis.sort_values('Interacciones', ascending=False)
    
    # Orden consistente
    columnas_orden = ['PV_Content Format', 'Posts', 'Impressions', 'Views', 'Interacciones', 'Interacciones Promedio', 'E.R.']
    columnas_orden = [col for col in columnas_orden if col in analisis.columns]
    
    return analisis[columnas_orden]

def analisis_content_format_group(df):
    """Análisis por PV Content Format Group"""
    if 'PV_Content Format Group' not in df.columns:
        return pd.DataFrame()
    
    analisis = df.groupby('PV_Content Format Group').agg({
        'Impressions': 'sum' if 'Impressions' in df.columns else 'count',
        'Views': 'sum' if 'Views' in df.columns else 'count',
        'Interacciones': 'sum' if 'Interacciones' in df.columns else 'count',
        'E.R.': 'mean' if 'E.R.' in df.columns else 'mean',
    }).round(2).reset_index()
    
    # Agregar conteo de posts
    conteo = df.groupby('PV_Content Format Group').size().reset_index(name='Posts')
    analisis = analisis.merge(conteo, on='PV_Content Format Group')
    
    # Ordenar por interacciones de mayor a menor
    if 'Interacciones' in analisis.columns:
        analisis = analisis.sort_values('Interacciones', ascending=False)
    
    # Orden consistente
    columnas_orden = ['PV_Content Format Group', 'Posts', 'Impressions', 'Views', 'Interacciones', 'E.R.']
    columnas_orden = [col for col in columnas_orden if col in analisis.columns]
    
    return analisis[columnas_orden]

# ============================================
# FUNCIONES DE VISUALIZACIÓN CON FORMATO MEJORADO
# ============================================

def formatear_numero(valor):
    """Formatea números con separadores de miles"""
    if pd.isna(valor) or valor == 0:
        return "0"
    try:
        return f"{int(valor):,}".replace(",", ".")
    except:
        return str(valor)

def formatear_porcentaje(valor):
    """Formatea porcentajes"""
    try:
        return f"{float(valor):.2f}%"
    except:
        return "0%"

def crear_tabla_formateada(df, columnas_centradas=['Posts', 'E.R.']):
    """
    Crea una tabla con formato correcto manteniendo los valores originales para ordenamiento
    """
    # Crear una copia para formatear la visualización
    df_display = df.copy()
    
    # Formatear columnas numéricas para visualización
    for col in df_display.columns:
        if col not in ['Platform', 'Título', 'Género', 'Formato', 'PV_Content Format', 'PV_Content Format Group']:
            if col == 'E.R.':
                df_display[col] = df_display[col].apply(formatear_porcentaje)
            elif col not in columnas_centradas:  # No formatear Posts como número
                df_display[col] = df_display[col].apply(formatear_numero)
    
    # Devolver el DataFrame original para ordenamiento y el formateado para visualización
    return df_display

# ============================================
# DASHBOARD PRINCIPAL
# ============================================

def main():
    """Función principal"""
    
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        login_form()
        return
    
    user = st.session_state["user_info"]
    
    with st.sidebar:
        st.markdown(f"""
        ### {user['avatar']} {user['name']}
        **Rol:** {user['role'].capitalize()}
        **Usuario:** {st.session_state['username']}
        **Inicio:** {st.session_state['login_time'].strftime('%H:%M:%S')}
        """)
        
        st.divider()
        
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="primary"):
            logout()
        
        st.divider()
        
        st.header("📂 Carga de Datos")
        
        opcion_datos = st.radio(
            "Selecciona fuente de datos:",
            ["📊 Datos de ejemplo", "📁 Cargar archivo"],
            key="data_source_option"
        )
        
        if opcion_datos == "📁 Cargar archivo":
            archivo = st.file_uploader(
                "Selecciona el archivo",
                type=['xlsx', 'xls', 'zip'],
                help="Sube el archivo datos_rrss.xlsx o .zip"
            )
            
            if archivo is not None:
                with st.spinner("Cargando datos..."):
                    df = cargar_archivo_excel(archivo)
                    if df is not None and not df.empty:
                        st.session_state['df'] = df
                        st.session_state['data_source'] = archivo.name
                        st.success(f"✅ Datos cargados: {len(df)} registros")
        
        if opcion_datos == "📊 Datos de ejemplo" or 'df' not in st.session_state:
            if 'df' not in st.session_state or opcion_datos == "📊 Datos de ejemplo":
                with st.spinner("Generando datos de ejemplo..."):
                    st.session_state['df'] = generar_datos_ejemplo()
                    st.session_state['data_source'] = "Datos de ejemplo"
                st.success("✅ Datos de ejemplo cargados")
        
        if 'df' in st.session_state:
            st.divider()
            st.header("🔍 Filtros")
            df = st.session_state['df']
            
            if 'Platform' in df.columns:
                plataformas = st.multiselect(
                    "Plataformas",
                    options=df['Platform'].unique(),
                    default=df['Platform'].unique()
                )
            else:
                plataformas = []
            
            if 'Formato' in df.columns:
                formatos = st.multiselect(
                    "Formatos",
                    options=df['Formato'].unique(),
                    default=df['Formato'].unique()
                )
            else:
                formatos = []
    
    if 'df' not in st.session_state:
        st.info("👈 Por favor, selecciona una fuente de datos en el panel lateral")
        return
    
    df = st.session_state['df']
    df_filtrado = df.copy()
    
    if 'plataformas' in locals() and len(plataformas) > 0 and 'Platform' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['Platform'].isin(plataformas)]
    
    if 'formatos' in locals() and len(formatos) > 0 and 'Formato' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['Formato'].isin(formatos)]
    
    st.title(f"📱 Dashboard Redes Sociales 2026 - {user['name']}")
    
    kpis = calcular_kpis_social(df_filtrado)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Total Posts", f"{kpis['total_posts']:,}")
    with col2:
        st.metric("👁️ Impressions", formatear_numero(kpis['total_impressions']))
    with col3:
        st.metric("🎬 Views", formatear_numero(kpis['total_views']))
    with col4:
        st.metric("🎯 Reach", formatear_numero(kpis['total_reach']))
    with col5:
        st.metric("💬 Interacciones", formatear_numero(kpis['total_interacciones']))
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Avg Impressions", formatear_numero(kpis['avg_impressions']))
    with col2:
        st.metric("📊 Avg Views", formatear_numero(kpis['avg_views']))
    with col3:
        st.metric("💫 Avg Interacciones", formatear_numero(kpis['avg_interacciones']))
    with col4:
        st.metric("❤️ Avg E.R.", formatear_porcentaje(kpis['avg_er']))
    
    st.divider()
    
    # Pestañas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Visión General",
        "📈 Por Plataforma",
        "🎬 Por Título",
        "🎭 Por Género",
        "📽️ Por Formato",
        "📦 Content Format",
        "📋 Datos Detallados"
    ])
    
    # ============================================
    # TAB 1: VISIÓN GENERAL
    # ============================================
    with tab1:
        st.subheader("Visión General")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Platform' in df_filtrado.columns:
                platform_count = df_filtrado['Platform'].value_counts().reset_index()
                platform_count.columns = ['Plataforma', 'Cantidad']
                fig = px.pie(platform_count, values='Cantidad', names='Plataforma',
                           title='Distribución de Posts por Plataforma', hole=0.3)
                st.plotly_chart(fig, width='stretch')
        
        with col2:
            if 'Interacciones' in df_filtrado.columns:
                top_posts = df_filtrado.nlargest(10, 'Interacciones')[['Platform', 'Interacciones']]
                fig = px.bar(top_posts, x='Platform', y='Interacciones',
                           title='Top 10 Posts por Interacciones',
                           color='Platform', text_auto='.2s')
                st.plotly_chart(fig, width='stretch')
    
    # ============================================
    # TAB 2: ANÁLISIS POR PLATAFORMA
    # ============================================
    with tab2:
        st.subheader("Análisis por Plataforma")
        
        analisis_plat = analisis_por_plataforma(df_filtrado)
        
        if not analisis_plat.empty:
            df_display = crear_tabla_formateada(analisis_plat)
            
            # Configurar columnas para mantener el ordenamiento
            column_config = {
                "Platform": st.column_config.TextColumn("Platform"),
                "Posts": st.column_config.NumberColumn("Posts", format="%d"),
                "Impressions": st.column_config.TextColumn("Impressions"),
                "Views": st.column_config.TextColumn("Views"),
                "Reach": st.column_config.TextColumn("Reach"),
                "Interacciones": st.column_config.TextColumn("Interacciones"),
                "Likes": st.column_config.TextColumn("Likes"),
                "E.R.": st.column_config.TextColumn("E.R.")
            }
            
            st.dataframe(
                df_display,
                column_config=column_config,
                width='stretch',
                hide_index=True,
                use_container_width=True
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'Interacciones' in analisis_plat.columns:
                    fig = px.bar(analisis_plat, x='Platform', y='Interacciones',
                               title='Interacciones por Plataforma',
                               color='Platform', text_auto='.2s')
                    st.plotly_chart(fig, width='stretch')
            
            with col2:
                if 'E.R.' in analisis_plat.columns:
                    fig = px.bar(analisis_plat, x='Platform', y='E.R.',
                               title='Engagement Rate por Plataforma',
                               color='Platform', text_auto='.2f')
                    fig.update_traces(texttemplate='%{text}%', textposition='outside')
                    st.plotly_chart(fig, width='stretch')
    
    # ============================================
    # TAB 3: ANÁLISIS POR TÍTULO
    # ============================================
    with tab3:
        st.subheader("Análisis por Título")
        
        analisis_titulo = analisis_por_titulo(df_filtrado)
        
        if not analisis_titulo.empty:
            df_display = crear_tabla_formateada(analisis_titulo)
            
            column_config = {
                "Título": st.column_config.TextColumn("Título"),
                "Posts": st.column_config.NumberColumn("Posts", format="%d"),
                "Impressions": st.column_config.TextColumn("Impressions"),
                "Views": st.column_config.TextColumn("Views"),
                "Interacciones": st.column_config.TextColumn("Interacciones"),
                "E.R.": st.column_config.TextColumn("E.R.")
            }
            
            st.dataframe(
                df_display,
                column_config=column_config,
                width='stretch',
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No hay datos de Título disponibles")
    
    # ============================================
    # TAB 4: ANÁLISIS POR GÉNERO
    # ============================================
    with tab4:
        st.subheader("Análisis por Género")
        
        analisis_genero = analisis_por_genero(df_filtrado)
        
        if not analisis_genero.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(analisis_genero, x='Género', y='Interacciones',
                           title='Interacciones por Género', color='Género',
                           text_auto='.2s')
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                fig = px.bar(analisis_genero, x='Género', y='E.R.',
                           title='Engagement Rate por Género', color='Género',
                           text_auto='.2f')
                fig.update_traces(texttemplate='%{text}%', textposition='outside')
                st.plotly_chart(fig, width='stretch')
            
            df_display = crear_tabla_formateada(analisis_genero)
            
            column_config = {
                "Género": st.column_config.TextColumn("Género"),
                "Posts": st.column_config.NumberColumn("Posts", format="%d"),
                "Impressions": st.column_config.TextColumn("Impressions"),
                "Views": st.column_config.TextColumn("Views"),
                "Interacciones": st.column_config.TextColumn("Interacciones"),
                "E.R.": st.column_config.TextColumn("E.R.")
            }
            
            st.dataframe(
                df_display,
                column_config=column_config,
                width='stretch',
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No hay datos de Género disponibles")
    
    # ============================================
    # TAB 5: ANÁLISIS POR FORMATO
    # ============================================
    with tab5:
        st.subheader("Análisis por Formato")
        
        analisis_formato = analisis_por_formato(df_filtrado)
        
        if not analisis_formato.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(analisis_formato, x='Formato', y='Interacciones',
                           title='Interacciones por Formato', color='Formato',
                           text_auto='.2s')
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                fig = px.bar(analisis_formato, x='Formato', y='Interacciones Promedio',
                           title='Promedio de Interacciones por Formato',
                           color='Formato', text_auto='.2s')
                st.plotly_chart(fig, width='stretch')
            
            df_display = crear_tabla_formateada(analisis_formato)
            
            column_config = {
                "Formato": st.column_config.TextColumn("Formato"),
                "Posts": st.column_config.NumberColumn("Posts", format="%d"),
                "Impressions": st.column_config.TextColumn("Impressions"),
                "Views": st.column_config.TextColumn("Views"),
                "Interacciones": st.column_config.TextColumn("Interacciones"),
                "Interacciones Promedio": st.column_config.TextColumn("Interacciones Promedio"),
                "E.R.": st.column_config.TextColumn("E.R.")
            }
            
            st.dataframe(
                df_display,
                column_config=column_config,
                width='stretch',
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No hay datos de Formato disponibles")
    
    # ============================================
    # TAB 6: ANÁLISIS POR CONTENT FORMAT
    # ============================================
    with tab6:
        st.subheader("Análisis por Content Format")
        
        analisis_content = analisis_por_content_format(df_filtrado)
        analisis_group = analisis_content_format_group(df_filtrado)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not analisis_content.empty:
                st.write("**Por Content Format**")
                fig = px.bar(analisis_content, x='PV_Content Format', y='Interacciones',
                           title='Interacciones por Content Format',
                           color='PV_Content Format', text_auto='.2s')
                st.plotly_chart(fig, width='stretch')
                
                df_display = crear_tabla_formateada(analisis_content)
                
                column_config = {
                    "PV_Content Format": st.column_config.TextColumn("Content Format"),
                    "Posts": st.column_config.NumberColumn("Posts", format="%d"),
                    "Impressions": st.column_config.TextColumn("Impressions"),
                    "Views": st.column_config.TextColumn("Views"),
                    "Interacciones": st.column_config.TextColumn("Interacciones"),
                    "Interacciones Promedio": st.column_config.TextColumn("Promedio"),
                    "E.R.": st.column_config.TextColumn("E.R.")
                }
                
                st.dataframe(
                    df_display,
                    column_config=column_config,
                    width='stretch',
                    hide_index=True,
                    use_container_width=True
                )
        
        with col2:
            if not analisis_group.empty:
                st.write("**Por Content Format Group**")
                fig = px.pie(analisis_group, values='Interacciones', names='PV_Content Format Group',
                           title='Distribución por Grupo', hole=0.3)
                st.plotly_chart(fig, width='stretch')
                
                df_display = crear_tabla_formateada(analisis_group)
                
                column_config = {
                    "PV_Content Format Group": st.column_config.TextColumn("Grupo"),
                    "Posts": st.column_config.NumberColumn("Posts", format="%d"),
                    "Impressions": st.column_config.TextColumn("Impressions"),
                    "Views": st.column_config.TextColumn("Views"),
                    "Interacciones": st.column_config.TextColumn("Interacciones"),
                    "E.R.": st.column_config.TextColumn("E.R.")
                }
                
                st.dataframe(
                    df_display,
                    column_config=column_config,
                    width='stretch',
                    hide_index=True,
                    use_container_width=True
                )
    
    # ============================================
    # TAB 7: DATOS DETALLADOS
    # ============================================
    with tab7:
        st.subheader("Datos Detallados")
        
        columnas_mostrar = ['Platform', 'Date', 'Formato', 'Impressions', 'Views', 
                           'Reach', 'Likes', 'Comments/Replies', 'Shares', 
                           'Interacciones', 'E.R.', 'Género', 'Título',
                           'PV_Content Format', 'PV_Content Format Group']
        
        columnas_existentes = [col for col in columnas_mostrar if col in df_filtrado.columns]
        
        if columnas_existentes:
            df_display = df_filtrado[columnas_existentes].head(200).copy()
            
            # Formatear columnas para visualización
            for col in ['Impressions', 'Views', 'Reach', 'Likes', 'Comments/Replies', 
                       'Shares', 'Interacciones']:
                if col in df_display.columns:
                    df_display[col] = df_display[col].apply(formatear_numero)
            if 'E.R.' in df_display.columns:
                df_display['E.R.'] = df_display['E.R.'].apply(formatear_porcentaje)
            if 'Date' in df_display.columns:
                df_display['Date'] = pd.to_datetime(df_display['Date']).dt.strftime('%d/%m/%Y')
            
            # Configurar columnas para mantener ordenamiento
            column_config = {}
            for col in df_display.columns:
                if col in ['Impressions', 'Views', 'Reach', 'Likes', 'Comments/Replies', 
                          'Shares', 'Interacciones']:
                    column_config[col] = st.column_config.TextColumn(col)
                elif col == 'E.R.':
                    column_config[col] = st.column_config.TextColumn(col)
                elif col == 'Date':
                    column_config[col] = st.column_config.DateColumn(col, format="DD/MM/YYYY")
                else:
                    column_config[col] = st.column_config.TextColumn(col)
            
            st.dataframe(
                df_display,
                column_config=column_config,
                width='stretch',
                height=500,
                hide_index=True,
                use_container_width=True
            )
    
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: gray; font-size: 0.8em;'>
        Dashboard Redes Sociales 2026 | Usuario: {user['name']} ({user['role']}) | 
        Fuente: {st.session_state.get('data_source', 'Desconocida')} |
        {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | 
        Registros: {len(df_filtrado):,}
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()