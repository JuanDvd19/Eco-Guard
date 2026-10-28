from ecoguard.domain.animal import Animal
from ecoguard.domain.zona import Zona
from ecoguard.domain.alerta import Alerta
from ecoguard.domain.agente import AgenteVigilancia
import os
import csv
import matplotlib.pyplot as plt
import subprocess
import sys

def main():
    zona_norte = Zona("Norte", "Riesgo Bajo")
    zona_sur = Zona("Sur", "Riesgo Alto")
    zona_este = Zona("Este", "Riesgo Medio")
    
    inventario_animales = []

    print("--- INICIANDO SISTEMA ECOGUARD ---")

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar nuevo animal")
        print("2. Ver inventario de fauna")
        print("3. Salir del sistema")
        print("4. Activar cámara de vigilancia (Agente Autonomo)")
        print("5. Exportar historial a CSV")
        print("6. Ver grafico de avistamientos por especie")
        print("7. Iniciar camara de monitoreo de IA")

        opcion = input("Selecciona una opción (1/2/3/4/5/6/7): ")

        if opcion == "1":

            print("\n-- REGISTRO DE ANIMAL --")

            while True:
                nuevo_nombre = input("Ingresa el nombre del animal: ").strip()

                if nuevo_nombre == "":
                    print("Error: El nombre no puede estar en blanco")
                elif nuevo_nombre.isnumeric():
                    print("Error: El nombre no puede tener solo numeros")
                else:
                    break

            while True:
                nueva_especie = input("Ingresa la especie del animal: ").strip()

                if nueva_especie == "":
                    print("Error: La especie no puede estar en blanco")
                elif nueva_especie.isnumeric():
                    print("Error: La especie no puede tener solo numeros")
                else:
                    break
            
            print("\n A que zona desea asignarlo?")
            print("1. Norte (Riesgo Bajo)")
            print("2. Sur (Riesgo Alto)")
            print("3. Este (Riesgo Medio)")

            opcion_zona = input("Elige la zona (1/2/3): ")

            if opcion_zona == "1":
                zona_asignada = zona_norte
            elif opcion_zona == "2":
                zona_asignada = zona_sur
            elif opcion_zona == "3":
                zona_asignada = zona_este
            else:
                print("Opcion invalida Se asginara a zona norte por defecto")
                zona_asignada = zona_norte
            
            nuevo_animal = Animal(nuevo_nombre, nueva_especie, zona_asignada)
            inventario_animales.append(nuevo_animal)

            with open("historial_ecoguard.txt", "a", encoding="utf-8") as archivo:
                archivo.write(nuevo_animal.summary() + "\n")
            
            print(f"\n¡{nuevo_nombre} registrado con éxito!")
            
            if zona_asignada.risk_level == "Riesgo Alto":
                nueva_alerta = Alerta(f"Se ha detectado un {nuevo_animal.species} en una zona de peligro.", "Crítica")
                print(nueva_alerta.mostrar_alerta())

        elif opcion == "2":
            print("\n--- INVENTARIO HISTORICO ECOGUARD ---")

            try:
                with open("historial_ecoguard.txt", "r", encoding="utf-8") as archivo:
                    lineas = archivo.readlines()
                if len(lineas) == 0:
                    print("El documento esta vacio. No hay animales registrados")
                else:
                    for linea in lineas:
                        print(linea.strip())
            except FileNotFoundError:
                print("La base de datos no existe. Registra un animal primero")

        elif opcion == "4":
            print("\n-- MODO VIGILANCIA AUTÓNOMA --")
            zona_reserva = [zona_norte, zona_sur, zona_este]

            camara_ia = AgenteVigilancia(zona_reserva)

            animal_detectado = camara_ia.detectar_anomalia()

            inventario_animales.append(animal_detectado)

            with open("historial_ecoguard.txt", "a", encoding="utf-8") as archivo:
                archivo.write(animal_detectado.summary() + "\n")
            
            print(f"\nEl Agente registro a {animal_detectado.name} con exito.")

            if animal_detectado.zone.risk_level == "Riesgo Alto":

                nueva_alerta = Alerta(f"El Agente detecto un {animal_detectado.species} en una zona de peligro.", "Critica")
                print(nueva_alerta.mostrar_alerta())

        elif opcion == "5":
            print("\n-- EXPORTAR HISTORIAL A CSV --")
            try:
                with open("historial_ecoguard.txt", "r", encoding="utf-8") as archivo_txt:
                    lineas = archivo_txt.readlines()

                if len(lineas) == 0:
                    print("El archivo de texto está vacío. No hay datos para exportar.")
                else:
                    with open("historial_ecoguard.csv", "w", newline="", encoding="utf-8") as archivo_csv:
                        escritor = csv.writer(archivo_csv)
                        escritor.writerow(["Información del Registro"])
                        
                        for linea in lineas:
                            escritor.writerow([linea.strip()])

                    print("¡Historial exportado con éxito a 'historial_ecoguard.csv'!")
            except FileNotFoundError:
                print("No se encontró el archivo de historial. Registra un animal primero.")

        elif opcion == "6":
            print("\n-- GENERANDO GRAFICO DE AVISTAMIENTOS --")
            conteo_especies = {}

            try:
                with open("historial_ecoguard.txt", "r", encoding="utf-8") as archivo:
                    for linea in archivo:
                        linea_limpia = linea.strip()
                        if linea_limpia:
                            partes = linea_limpia.split(",")
                            if len(partes) >= 2:
                                especie = partes[1].strip()
                                conteo_especies[especie] = conteo_especies.get(especie, 0) + 1

                if not conteo_especies:
                    print("No se encontraron registros de especies para graficar.")
                else:
                    especies = list(conteo_especies.keys())
                    cantidades = list(conteo_especies.values())

                    plt.figure(figsize=(9, 5))
                    plt.bar(especies, cantidades, color="#2E7D32", edgecolor="black")
                    plt.title("Avistamientos por Especie - Sistema EcoGuard", fontsize=14, fontweight="bold")
                    plt.xlabel("Especie", fontsize=12)
                    plt.ylabel("Numero de Avistamientos", fontsize=12)
                    plt.grid(axis="y", linestyle="--", alpha=0.7)
                    plt.tight_layout()
                    plt.show()

            except FileNotFoundError:
                print("No se encontro el archivo 'historial_ecoguard.txt'. Registra animales primero.")

        elif opcion == "7":
            print("\n--- INICIANDO RADAR DE VISION ARTIFICIAL ---")
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_camara = os.path.join(directorio_actual, "prueba_vision.py")
            
            # Si no esta en la raiz, busca dentro de la carpeta laboratorio
            if not os.path.exists(ruta_camara):
                ruta_camara = os.path.join(directorio_actual, "laboratorio", "prueba_vision.py")
                
            if os.path.exists(ruta_camara):
                subprocess.run([sys.executable, ruta_camara])
                print("\n--- Monitoreo finalizado. Regresando al menu principal ---")
            else:
                print("Error: No se encontro el archivo 'prueba_vision.py'.")

        elif opcion == "3":
            print("\nCerrando el sistema EcoGuard. ¡Hasta pronto!")
            break 

        else:
            print("\nOpción no válida. Por favor, elige 1, 2, 3, 4, 5, 6 o 7.")

        input("\nPresiona Enter para continuar...")

        os.system("cls") 

if __name__ == "__main__":
    main()

