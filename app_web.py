import pandas as pd
import sqlite3
import streamlit as st
import subprocess
import sys
import os 
from base_datos import iniciar_bd, consultar_conteo_especies

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def pantalla_login():
    col1, col2, col3 = st.columns([1, 2, 1]) # Crea 3 columnas para centrar el formulario

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2913/2913990.png", width=80)
        st.markdown("### 🌿 Ecoguard - Acceso")
        st.caption("Panel de control y monitoreo inteligente")

        st.write("")

        with st.form("formulario_login"):
            usuario = st.text_input("Usuario", placeholder="Ej: admin")
            contrasena = st.text_input("Contraseña", type="password", placeholder="••••••••")

            boton_ingreso = st.form_submit_button("Iniciar sesión", use_container_width=True)

            if boton_ingreso:
                if usuario == "admin" and contrasena == "ecoguard2026":
                    st.session_state['autenticado'] = True
                    st.success("¡Bienvenido al sistema Ecoguard!")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")



def mostrar_dashboard():
    st.title("🌿 Panel de Monitoreo Inteligente de Fauna")
    
    # Aseguramos que la base de datos esté iniciada usando tu función importada
    iniciar_bd()
    
    tab1, tab2, tab3 = st.tabs(["Análisis General", "Control de Cámaras", "Base de Datos"])
    
    with tab1:
        st.markdown("### Resumen de Fauna Detectada")
       
        datos = consultar_conteo_especies() 
        
        if datos:
           
            df_conteo = pd.DataFrame(datos, columns=["Especie", "Cantidad"])
            
            
            if not df_conteo.empty and df_conteo["Cantidad"].sum() > 0:
               
                m1, m2 = st.columns(2)
                m1.metric(label="Total Detectados", value=int(df_conteo["Cantidad"].sum()))
                m2.metric(label="Especie más vista", value=df_conteo.iloc[0]["Especie"])
                
                st.markdown("---")
                
                st.bar_chart(df_conteo.set_index("Especie"))
            else:
                st.info("Aún no hay detecciones registradas en la base de datos.")
        else:
            st.info("Aún no hay detecciones registradas en la base de datos.")
      

    with tab2:
        st.subheader("Control de Visión Artificial (YOLOv8)")
        st.write("Usa este panel para iniciar la cámara sin bloquear la página web.")
        
       
        if st.button("Iniciar Detección en Tiempo Real", type="primary"):
            
            subprocess.Popen([sys.executable, "main.py"])
            st.success("Cámara iniciada en una ventana externa.")
            
        st.markdown("---")
        st.write("Últimas capturas:")
        
       
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        ruta_fotos = os.path.join(directorio_actual, "ecoguard", "laboratorio", "evidencias_ecoguard")
        
        if os.path.exists(ruta_fotos):
            fotos = os.listdir(ruta_fotos)
            if fotos:
                cols = st.columns(3)
                for i, foto in enumerate(fotos[-6:]): # Muestra solo las últimas 6
                    cols[i % 3].image(os.path.join(ruta_fotos, foto), use_container_width=True)
            else:
                st.warning("La carpeta de capturas está vacía.")
        else:
            st.warning(f"No se encontró la carpeta '{ruta_fotos}'.")

    with tab3:
        st.subheader("Registros Históricos")
        try:
            # CAMBIA "ecoguard.db" y "avistamientos" por los nombres reales de tu BD y tu tabla
            conexion = sqlite3.connect("ecoguard.db") 
            df_fauna = pd.read_sql_query("SELECT * FROM avistamientos ORDER BY id DESC", conexion)
            
            # Muestra la tabla profesional
            st.dataframe(df_fauna, use_container_width=True, hide_index=True)
            
            # Botón de descarga CSV
            st.markdown("---")
            csv = df_fauna.to_csv(index=False).encode('utf-8')
            st.download_button(" Descargar Reporte (CSV)", data=csv, file_name='reporte_ecoguard.csv', mime='text/csv')
            conexion.close()
            
        except Exception as e:
            st.error(f"Error conectando a la base de datos: Verifica el nombre del archivo .db. Detalle: {e}")

    # Botón para cerrar sesión (Barra lateral)
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['autenticado'] = False
        st.rerun()

    


if not st.session_state['autenticado']:
    pantalla_login()
else:
    mostrar_dashboard()


    
