import requests
from datetime import datetime
from claves import DISCORD_WEBHOOK_URL as WEBHOOK_URL



def enviar_alerta_discord(especie, ruta_foto):
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Mensaje de texto que acompañara a la foto


    datos_mensaje = {"username": "Ecoguard Centinela", 
                    "content":(
                    f"AlERTA DE FAUNA EN RESERVA\n"
                    f"Especie confirmada: {especie}\n"
                    f"Fecha y hora: {hora_actual}\n"
                    f"Estado: Evidencia fotografica capturada con exito"
                    )
    }

    # Empacar la foto para mandarla por internet 

    try:
        with open(ruta_foto, "rb") as foto:
            archivos = {"file": (ruta_foto, foto, "imagen/jpeg")}
            respuesta = requests.post(WEBHOOK_URL, data=datos_mensaje, files=archivos)

        if respuesta.status_code in [200, 204]:
            print("[AGENTE MENSAJERO] Alerta foto enviada a discord con exito")
        else:
            print("[AGENTE MENSAJERO] Discord rechazo el mensaje (Codigo: {respuesta.status_code})")

    except Exception as error:
        print(f"[AGENTE MENSAJERO] fallo de conexion: {error}")