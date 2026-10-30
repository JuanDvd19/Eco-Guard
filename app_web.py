import streamlit as st
import subprocess
import sys
import os 

st.set_page_config(page_title="Ecoguard Dashboard", layout="wide") #Configura la pestaña de navegador y activa el modo ancho para aprovechar toda la pantalla.
st.title("Panel de control Ecoguard v2.0") #Tanto title como write reemplazan el print de la consola dibujando texto directamente en la pagina web
st.write("Monitoreo inteligente de fauna y análisis de datos en tiempo real.")

st.sidebar.header("Centro de Mando") #Sidebar crea una columna desplegable que separa los botones de las graficas en la pagina

if st.sidebar.button("Iniciar cámara de Monitoreo de IA"): #Detecta el click del raton y ejecuta el subproceso programado en main.py
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_camara = os.path.join(directorio_actual, "laboratorio", "prueba_vision.py")

    if os.path.exists(ruta_camara):
        st.sidebar.info("Radar activo. Presiona la tecla q en la ventana de video para cerrar")
        subprocess.run([sys.executable, ruta_camara])
        st.sidebar.success("Monitoreo Finalizado")
    else:
        st.sidebar.error("No se encontró el archivo de visión")

st.subheader("Estadisticas de avistamientos")
conteo_especies = {}

if os.path.exists("historial_ecoguard.txt"):
    with open("historial_ecoguard.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea_limpia = linea.strip()
            if linea_limpia:
                partes = linea_limpia.split(",")
                if len(partes) >= 2:
                    especie = partes[1].strip()
                    conteo_especies[especie] = conteo_especies.get(especie, 0) + 1

if conteo_especies: 
    col1, col2 = st.columns(2) #Divide la pantalla en dos tarjetas superiores donde metric muestra contadores con el total de animales y especies
    col1.metric("Total de avistamientos", sum(conteo_especies.values()))
    col2.metric("Especies distintas", len(conteo_especies))

    st.bar_chart(conteo_especies, color="#2E7D32") #Toma el diccionario y genera en una sola linea un grafico de barras interactivo de color verde
else:
    st.warning("Aun no hay registros validos en el historial")


st.subheader("Galeria de Evidencias recientes")
carpeta_fotos = os.path.join("laboratorio", "evidencias_ecoguard")

if os.path.exists(carpeta_fotos):
    fotos = [f for f in os.listdir(carpeta_fotos) if f.endswith(".jpg")]
    if fotos:
        columnas_galeria = st.columns(3)
        for i, foto in enumerate(fotos[-6:]): #Selecciona automaticamente las ultimas seis capturas para mantener la apgina rapida y ordenada
            ruta_foto = os.path.join(carpeta_fotos, foto)
            columnas_galeria [i % 3].image(ruta_foto, caption=foto)
    else:
        st.info("Todavia no hay fotos guardadas en la carpeta de evidencias.")

    
