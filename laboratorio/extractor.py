import cv2 
import os 

ruta_video = "laboratorio/video_reserva.mp4"
carpeta_salida = "laboratorio/fotos_zorro"

os.makedirs(carpeta_salida, exist_ok=True)

cap = cv2.VideoCapture(ruta_video)

contador_fotogramas = 0

fotos_guardadas = 0

print("INICIANDO EXTRACCIÓN DE FOTOS")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if contador_fotogramas % 15 == 0:
        nombre_archivo = f"{carpeta_salida}/zorro_{fotos_guardadas}.jpg"

    cv2.imwrite(nombre_archivo, frame)
    fotos_guardadas += 1
    print(f"Guardada: {nombre_archivo}")
contador_fotogramas += 1

cap.release()
print(f"\nProceso terminado se extrajeron {fotos_guardadas} fotos listas")