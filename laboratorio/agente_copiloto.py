import os
import subprocess
import requests
from claves import GEMINI_API_KEY

def consultar_gemini(prompt):
    # 1. Consulta la lista oficial de modelos activos en tu cuenta
    url_lista = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    resp_lista = requests.get(url_lista)
    
    if resp_lista.status_code != 200:
        print(f"[ERROR] Fallo al verificar la API Key ({resp_lista.status_code}): {resp_lista.text}")
        return None

    # 2. Filtra los modelos compatibles con 'generateContent' (excluyendo el 2.5)
    modelos_disponibles = []
    for m in resp_lista.json().get("models", []):
        nombre = m.get("name", "")
        metodos = m.get("supportedGenerationMethods", [])
        if "generateContent" in metodos and "gemini" in nombre and "2.5" not in nombre:
            modelos_disponibles.append(nombre)

    # Prioriza los modelos 'flash'
    modelos_flash = [m for m in modelos_disponibles if "flash" in m]
    candidatos = modelos_flash + [m for m in modelos_disponibles if m not in modelos_flash]

    # 3. Prueba los candidatos hasta recibir respuesta exitosa (Codigo 200)
    datos = {"contents": [{"parts": [{"text": prompt}]}]}
    for modelo in candidatos:
        url_ia = f"https://generativelanguage.googleapis.com/v1beta/{modelo}:generateContent?key={GEMINI_API_KEY}"
        respuesta = requests.post(url_ia, json=datos)
        if respuesta.status_code == 200:
            print(f"[INFO] Conectado con el modelo: {modelo}")
            return respuesta.json()["candidates"][0]["content"]["parts"][0]["text"]

    print("[ERROR] Ningun modelo disponible respondio. Verifica tu conexion o cuenta en AI Studio.")
    return None

def auditar_codigo(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"[ERROR] No se encontro el archivo: {ruta_archivo}")
        return

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    codigo_numerado = ""
    for num, texto in enumerate(lineas, start=1):
        codigo_numerado += f"Linea {num}: {texto}"

    print(f"\n[COPILOTO] Analizando '{ruta_archivo}' linea por linea...\n")

    prompt_revision = f"""
    Actua como mi Agente Copiloto experto en Python para mi proyecto EcoGuard.
    Revisa este codigo numerado y responde en espanol claro, sin usar emojis, con esta estructura:
    
    1. DIAGNOSTICO POR LINEAS: Indica que lineas exactas tienen fallos, riesgos o cosas por mejorar y explica el porque de forma sencilla.
    2. OPCIONES VIABLES: Dame la 'Opcion 1' y la 'Opcion 2' explicando que cambio harias en cada una.
    No reescribas el codigo completo todavia.

    Codigo a revisar:
    {codigo_numerado}
    """

    diagnostico = consultar_gemini(prompt_revision)
    
    if diagnostico is None:
        return

    print("====================================================")
    print(diagnostico)
    print("====================================================")

    decision = input("\n[CONFIRMACION] Quieres que lo arregle? (Escribe '1', '2' o 'n' para no tocar el archivo): ").strip().lower()

    if decision in ["1", "2"]:
        subprocess.run(["git", "add", ruta_archivo])
        subprocess.run(["git", "commit", "-m", f"Respaldo antes de aplicar Opcion {decision} del Copiloto en {ruta_archivo}"])
        print("[GIT] Punto de control guardado automaticamente.")
        print(f"[INFO] Aplicando la Opcion {decision} en '{ruta_archivo}'...")

        prompt_edicion = f"""
        Toma este codigo original:
        {''.join(lineas)}

        Segun este diagnostico:
        {diagnostico}

        Aplica unicamente la Opcion {decision}.
        Devuelve SOLAMENTE el codigo Python puro y funcional, sin bloques markdown, sin emojis ni explicaciones adicionales.
        """

        nuevo_codigo = consultar_gemini(prompt_edicion)
        if nuevo_codigo is not None:
            nuevo_codigo = nuevo_codigo.replace("```python", "").replace("```", "").strip()
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write(nuevo_codigo + "\n")

            print(f"[OK] '{ruta_archivo}' fue actualizado con la Opcion {decision}.")
            print(f"[TIP] Para deshacer el cambio, ejecuta en la terminal: git checkout -- {ruta_archivo}")
    else:
        print("[INFO] Operacion cancelada. El archivo original no fue modificado.")

if __name__ == "__main__":
    nombre = input("Archivo a revisar (ej. main.py o agente_mensajero.py): ").strip()
    if not os.path.exists(nombre) and os.path.exists(f"laboratorio/{nombre}"):
        nombre = f"laboratorio/{nombre}"
    auditar_codigo(nombre)