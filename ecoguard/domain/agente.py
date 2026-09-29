import random
import time
from ecoguard.domain.animal import Animal

class AgenteVigilancia:
    def __init__(self, zonas_disponibles):
        self.zonas = zonas_disponibles
        # Listas de datos simulados que la "cámara" podría detectar
        self.nombres_posibles = ["Sombra", "Rayo", "Fantasma", "Pecas", "Bribón"]
        self.especies_posibles = ["Puma", "Tigrillo", "Oso de Anteojos", "Venado", "Zorro"]

    def detectar_anomalia(self):
        print("\n[Agente] Analizando feed de cámaras de la reserva...")
        time.sleep(2) # Pausa el programa por 2 segundos para simular procesamiento
        
        # random.choice() elige un elemento al azar de la lista
        nombre_detectado = random.choice(self.nombres_posibles)
        especie_detectada = random.choice(self.especies_posibles)
        zona_detectada = random.choice(self.zonas)
        
        print(f"[Agente] ¡Movimiento detectado! Identificando silueta de {especie_detectada}...")
        time.sleep(1.5)
        
        # El agente crea el objeto Animal por sí mismo y lo devuelve
        return Animal(nombre_detectado, especie_detectada, zona_detectada)