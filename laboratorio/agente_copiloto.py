import os 
import subprocess
import requests
from claves import GEMINI_API_KEY

def consultar_gemini(prompt):
    url_lista = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    resp_lista = requests.get(url_lista)
    
    if resp_lista.status_code != 200:
        print(f"[ERROR] Fallo al verificar la API Key: {resp_lista.text}")
        return None

    modelos_disponibles = []
    for m in resp_lista.json().get("models", []):
        nombre = m.get("name", "")
        metodos = m.get("supportedGenerationMethods", [])
        if "generateContent" in metodos and "gemini" in nombre and "2.5" not in nombre:
            modelos_disponibles.append(nombre)

    modelos_flash = [m for m in modelos_disponibles if "flash" in m]
    candidatos = modelos_flash + [m for m in modelos_disponibles if m not in modelos_flash]

    print(f"\n[DEBUG] Encontrados {len(candidatos)} modelos compatibles. Intentando conectar...")

    datos = {"contents": [{"parts": [{"text": prompt}]}]}
    for modelo in candidatos:
        url_ia = f"https://generativelanguage.googleapis.com/v1beta/{modelo}:generateContent?key={GEMINI_API_KEY}"
        respuesta = requests.post(url_ia, json=datos)
        
        if respuesta.status_code == 200:
            print(f"[INFO] Conexion exitosa con el modelo: {modelo}")
            return respuesta.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # AQUI ESTA LA MAGIA: Nos imprimira el motivo exacto del rechazo
            print(f"[DEBUG] {modelo} fallo -> Codigo {respuesta.status_code}: {respuesta.text}")

    print("[ERROR] Ningun modelo disponible respondio.")
    return None


def auditar_codigo(ruta_archivo):
    #1. Comprueba que el archivo que le pido revisar realmente exista
    if not os.path.exists(ruta_archivo):
        print(f"[ERROR] No se encontro el archivo: {ruta_archivo}")
        return

    # 2. Lee el codigo original
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # 3. Le pone el numero de linea a cada renglon para que la IA no se pierda
    codigo_numerado = ""
    for num, texto in enumerate(lineas, start=1):
        codigo_numerado += f"Linea {num}: {texto}"

    # 4. Interfaz en la consola para pedirte la orden
    print(f"\n[COPILOTO] Archivo cargado: '{ruta_archivo}'")
    print("====================================================")
    print("MISION DEL COPILOTO:")
    print("- Presiona ENTER en blanco para auditar y buscar errores.")
    print("- O escribe una tarea (ej. 'Crea un bloque para guardar datos en un Excel').")
    instruccion_usuario = input("Tu orden: ").strip()

    print("\n[INFO] Analizando el codigo, calculando opciones y preparando explicacion...\n")

    # Ajusta el contexto dependiendo de si le di una orden o si solo le di Enter
    if instruccion_usuario:
        contexto = f"TAREA ESPECIFICA DEL USUARIO: {instruccion_usuario}\nTu objetivo es proponer como modificar o agregar el codigo necesario para cumplir esta peticion."
    else:
        contexto = "OBJETIVO: Realizar una auditoria buscando errores o mejoras de eficiencia."

    # 5. El prompt maestro con nuevas reglas de explicacion exhaustiva
    prompt_revision = f"""
    Actua como mi Arquitecto de Software experto en Python.
    Revisa este codigo numerado.

    {contexto}

    Responde en espanol claro, sin usar emojis, con esta estructura exacta:
    
    1. ANALISIS DE LA TAREA: Explica brevemente que vamos a hacer y su impacto en el archivo.
    2. OPCIONES VIABLES: Propón 'Opcion 1' y 'Opcion 2'. Para cada una, analiza su RENTABILIDAD Y EFICIENCIA (Cual consume menos memoria, cual es mas facil de mantener).
    3. EXPLICACION PASO A PASO: Toma la opcion mas optima y explicame de forma muy sencilla, linea por linea, que codigo vas a escribir, que hace exactamente cada linea nueva y por que la elegiste. No te saltes ningun detalle, quiero entender la logica de todo lo que vas a hacer.
    
    Aun no me des el codigo final puro para reescribir el archivo, solo dame este diagnostico y explicacion.

    Codigo a revisar:
    {codigo_numerado}
    """

    # 6. Manda la consulta y muestra el diagnostico en consola
    diagnostico = consultar_gemini(prompt_revision)
    if diagnostico is None: 
        return

    print("====================================================")
    print(diagnostico)
    print("====================================================")

# 7. El candado de seguridad: Espera la aprobacion
    decision = input("\n[CONFIRMACION] Cual opcion aplicamos? (Escribe '1', '2' o 'n' para cancelar): ").strip().lower()

    if decision in ["1", "2"]:
        # 8. Crea la copia de seguridad en Git antes de tocar nada
        subprocess.run(["git", "add", ruta_archivo])
        mensaje_commit = f"Respaldo previo: Tarea '{instruccion_usuario}'" if instruccion_usuario else "Respaldo previo a auditoria"
        subprocess.run(["git", "commit", "-m", f"{mensaje_commit} (Opcion {decision}) en {ruta_archivo}"])
        
        print("[GIT] Punto de control guardado automaticamente.")
        print(f"[INFO] Escribiendo el nuevo codigo para la Opcion {decision} en '{ruta_archivo}'...")

        # 9. Le ordena a la IA que genere el codigo puro sin explicaciones extra
        prompt_edicion = f"""
        Toma este codigo original:
        {''.join(lineas)}

        Segun este diagnostico y la opcion elegida:
        {diagnostico}

        Aplica unicamente la Opcion {decision}.
        Devuelve SOLAMENTE el codigo Python puro, completo y funcional. No uses bloques markdown, no uses la palabra python al inicio, ni emojis, ni explicaciones adicionales, solo el codigo listo para guardar.
        """

        nuevo_codigo = consultar_gemini(prompt_edicion)
        if nuevo_codigo is not None:
            # 10. Limpia posibles basuras de texto y sobreescribe el archivo
            nuevo_codigo = nuevo_codigo.replace("```python", "").replace("```", "").strip()
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(nuevo_codigo + "\n")

            print(f"[OK] '{ruta_archivo}' fue actualizado exitosamente.")
            print(f"[TIP] Si no te gusta el resultado, escribe en la terminal: git checkout -- {ruta_archivo}")
    else:
        print("[INFO] Operacion cancelada. El archivo original sigue intacto.")

# 11. El punto de arranque del programa
if __name__ == "__main__":
    print("\n--- INICIANDO ECOGUARD COPILOTO ---")
    archivo_objetivo = input("Archivo a intervenir (ej. main.py o agente_mensajero.py): ").strip()
    
    # Busca si el archivo esta en la carpeta principal o dentro de laboratorio/
    if not os.path.exists(archivo_objetivo) and os.path.exists(f"laboratorio/{archivo_objetivo}"):
        archivo_objetivo = f"laboratorio/{archivo_objetivo}"
        
    auditar_codigo(archivo_objetivo)    