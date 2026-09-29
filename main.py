from ecoguard.domain.animal import Animal

from ecoguard.domain.zona import Zona

from ecoguard.domain.alerta import Alerta

import os

from ecoguard.domain.agente import AgenteVigilancia

def main():
    # 1. Zonas e Inventario inicial (esto va antes del ciclo para que no se reinicie)
    zona_norte = Zona("Norte", "Riesgo Bajo")
    zona_sur = Zona("Sur", "Riesgo Alto")
    zona_este = Zona("Este", "Riesgo Medio")
    
    inventario_animales = []

    print("--- INICIANDO SISTEMA ECOGUARD ---")

    # 2. El ciclo infinito que mantiene el programa encendido
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar nuevo animal")
        print("2. Ver inventario de fauna")
        print("3. Salir del sistema")
        print("4. Activar cámara de vigilancia (Agente Autonomo)")

        
        # Le pedimos al usuario que elija qué quiere hacer
        opcion = input("Selecciona una opción (1/2/3/4): ")

        # 3. Lógica Condicional: ¿Qué pasa con cada opción?
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
            
            # Disparamos la alerta si es necesario
            if zona_asignada.risk_level == "Riesgo Alto":
                nueva_alerta = Alerta(f"Se ha detectado un {nuevo_animal.species} en una zona de peligro.", "Crítica")
                print(nueva_alerta.mostrar_alerta())

        elif opcion == "2":
            print("\n--- INVENTARIO HISTORICO ECOGUARD ---")

            #El escudo hara
            try:
                # Usamos "r" (leer/read) en vez de "a" (agregar/append)
                with open("historial_ecoguard.txt", "r", encoding="utf-8") as archivo:
                    lineas = archivo.readlines() #Lee todas las lineas del archivo
                if len(lineas) == 0:
                    print("El documento esta vacio. No hay animales registrados")
                else:
                    for linea in lineas:
                        # .strip() sirve para limpiar el salto de linea extra al final de cada texto
                        print(linea.strip())
            #Si el archivo no se encuentra haz esto en lugar de cerrarte sin mas con error
            except FileNotFoundError:
                print("La base de datos no existe. Registra un animal primero")

        elif opcion == "4":
            print("\n-- MODO VIGILANCIA AUTÓNOMA --")
            #Agrupamos las zonas en una lista para pasarselas al agente
            zona_reserva = [zona_norte, zona_sur, zona_este]

            #Instanciamos al agente
            camara_ia = AgenteVigilancia(zona_reserva)

            #El agente hace su trabajo
            animal_detectado = camara_ia.detectar_anomalia()

            #Lo guarda en la memoria ram
            inventario_animales.append(animal_detectado)

            #Ahora se guarda en el disco duro o archivo 
            with open("historial_ecoguard.txt", "a", encoding="utf-8") as archivo:
                archivo.write(animal_detectado.summary() + "\n")
            
            print(f"\nEl Agente registro a {animal_detectado.name} con exito.")

            if animal_detectado.zone.risk_level == "Riesgo Alto":

                nueva_alerta = Alerta(f"El Agente detecto un {animal_detectado.species} en una zona de peligro.", "Critica")
                print(nueva_alerta.mostrar_alerta())

        elif opcion == "3":
            print("\nCerrando el sistema EcoGuard. ¡Hasta pronto!")
            break # Aquí rompemos el ciclo infinito y el programa termina

        else:
            # Si el usuario teclea "4" o una letra por accidente, el programa no explota.
            print("\nOpción no válida. Por favor, elige 1, 2 o 3.")
        # --- Nuevo: Pausa y limpia
        input("\nPresiona Enter para continuar...")

        os.system("cls") #cls es el comando nativo de windows para limpiar la terminal 

if __name__ == "__main__":
    main()
