import cv2
import os
import time
from datetime import datetime
import mss
import numpy as np
from ultralytics import YOLO
from agente_mensajero import enviar_alerta_discord

cerebro_rastreo = YOLO("yolov8n.pt")           
cerebro_experto = YOLO("laboratorio/zorro.pt") 

carpeta_evidencias = "laboratorio/evidencias_ecoguard"
os.makedirs(carpeta_evidencias, exist_ok=True)

especie_confirmada = None
foto_evidencia_tomada = False
inicio_avistamiento = None
tiempo_total_zona = 0

ultima_caja = None
frames_camuflado = 0
MAX_FRAMES_MEMORIA = 45  
CONF_RASTREO = 0.65

modo_entrada = input("Seleccione modo de entrada ('1' para video, '2' para pantalla en vivo): ").strip()
cap = None
sct = None
region_pantalla = None

if modo_entrada == '1':
    ruta_video = "laboratorio/video_reserva.mp4"
    cap = cv2.VideoCapture(ruta_video)
elif modo_entrada == '2':
    sct = mss.mss()
    region_pantalla = {"top": 150, "left": 100, "width": 850, "height": 500}
else:
    print("Modo no valido. Saliendo...")
    exit()

clases_fauna = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

while True:
    if modo_entrada == '1':
        ret, frame = cap.read()
        if not ret:
            break
    else:
        captura_cruda = sct.grab(region_pantalla)
        frame = np.array(captura_cruda)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    frame_limpio = frame.copy()
    frame_anotado = frame.copy()
    caja_detectada_hoy = None

    resultados_experto = cerebro_experto(frame, conf=0.85, verbose=False)
    if len(resultados_experto[0].boxes) > 0:
        caja_detectada_hoy = [int(coord) for coord in resultados_experto[0].boxes[0].xyxy[0]]
        
        if especie_confirmada is None:
            id_esp = int(resultados_experto[0].boxes[0].cls[0])
            nombre_bruto = cerebro_experto.names[id_esp].lower()
            if "redfox" in nombre_bruto or "zorro" in nombre_bruto:
                especie_confirmada = "Zorro Rojo"
            else:
                especie_confirmada = nombre_bruto.capitalize()
            print(f"Confirmado por el Biologo: {especie_confirmada.upper()}")

    resultados_rastreo = cerebro_rastreo(
        frame, conf=CONF_RASTREO, classes=clases_fauna, verbose=False
    )
    if caja_detectada_hoy is None and len(resultados_rastreo[0].boxes) > 0:
        caja_detectada_hoy = [int(coord) for coord in resultados_rastreo[0].boxes[0].xyxy[0]]

    if caja_detectada_hoy is not None:
        ultima_caja = tuple(caja_detectada_hoy)
        frames_camuflado = 0  
    else:
        frames_camuflado += 1 

    if frames_camuflado > MAX_FRAMES_MEMORIA:
        ultima_caja = None
        inicio_avistamiento = None
        tiempo_total_zona = 0
        especie_confirmada = None
        foto_evidencia_tomada = False

    if ultima_caja is not None and frames_camuflado <= MAX_FRAMES_MEMORIA:
        if inicio_avistamiento is None:
            inicio_avistamiento = time.time()
            print("Movimiento de fauna detectado. Analizando especie...")

        tiempo_total_zona = time.time() - inicio_avistamiento

        if especie_confirmada is None and tiempo_total_zona >= 3.0:
            especie_confirmada = "Animal detectado"
            print(f"Tiempo limite alcanzado. Clasificacion generica asignada: {especie_confirmada}")

        x1, y1, x2, y2 = ultima_caja

        if especie_confirmada is None:
            color = (0, 255, 255) 
            texto_caja = f"Analizando fauna... ({tiempo_total_zona:.1f}s)"
        else:
            color = (0, 255, 0)   
            texto_caja = f"Confirmado: {especie_confirmada} ({tiempo_total_zona:.1f}s)"

            if not foto_evidencia_tomada:
                marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_especie_archivo = especie_confirmada.lower().replace(" ", "_")
                ruta_foto = f"{carpeta_evidencias}/evidencia_{nombre_especie_archivo}_{marca_tiempo}.jpg"
                cv2.imwrite(ruta_foto, frame_limpio)
                print(f"Evidencia guardada en: {ruta_foto}")
                
                enviar_alerta_discord(especie_confirmada, ruta_foto)

                ruta_script = os.path.abspath(__file__)
                directorio_laboratorio = os.path.dirname(ruta_script)
                directorio_raiz = os.path.dirname(directorio_laboratorio)
                ruta_historial = os.path.join(directorio_raiz, "historial_ecoguard.txt")
                
                nombre_dispositivo = "EcoGuard-Cam01"
                zona_monitoreo = "Sector Norte"
                nivel_alerta = "Prioridad Alta" if especie_confirmada == "Zorro Rojo" else "Estandar"
                
                registro_linea = f"{nombre_dispositivo}, {especie_confirmada}, {zona_monitoreo}, {nivel_alerta}\n"
                
                with open(ruta_historial, mode="a", encoding="utf-8") as archivo_historial:
                    archivo_historial.write(registro_linea)
                
                print(f"Registro guardado exitosamente en: {ruta_historial}")
                
                foto_evidencia_tomada = True

        cv2.rectangle(frame_anotado, (x1, y1), (x2, y2), color, 3)
        cv2.putText(frame_anotado, texto_caja, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("EcoGuard AI - Doble Cerebro", frame_anotado)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

if cap is not None:
    cap.release()
if sct is not None:
    sct.close()
cv2.destroyAllWindows()

print("\n--- REPORTE FINAL ECOGUARD ---")
print(f"Especie identificada : {especie_confirmada}")
print(f"Tiempo en zona       : {tiempo_total_zona:.1f} segundos")
print(f"Evidencia guardada   : {'Si' if foto_evidencia_tomada else 'No'}")
