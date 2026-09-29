# EcoGuard - Sistema Inteligente de Monitoreo y Gestion de Fauna

EcoGuard es una plataforma desarrollada en Python para el registro, monitoreo por vision artificial y notificacion en tiempo real de avistamientos de fauna en reservas naturales. El proyecto integra programacion orientada a objetos, modelos de deteccion neuronal (YOLOv8) y agentes automatizados conectados mediante APIs.

---

## Arquitectura del Sistema

El proyecto se divide en dos entornos principales:

### 1. Nucleo de Gestion (`ecoguard/` y `main.py`)
Modulo encargado de modelar las entidades biologicas mediante Programacion Orientada a Objetos (POO) y registrar la trazabilidad de avistamientos en almacenamiento local (`historial_ecoguard.txt`).

### 2. Laboratorio de Vision y Agentes (`laboratorio/`)
* **Sistema de Vision de Doble Modelo (`prueba_vision.py`):** Procesa secuencias de video utilizando OpenCV y combina un modelo general (`yolov8n.pt`) con un modelo especializado entrenado a medida (`zorro.pt`) para confirmar la especie detectada y almacenar evidencia fotografica dinamica.
* **Agente Mensajero (`agente_mensajero.py`):** Conecta el sistema de vision con Discord a traves de peticiones HTTP (`requests`) y Webhooks, enviando alertas en tiempo real con fecha, hora, especie confirmada y fotografia adjunta.
* **Agente Copiloto (`agente_copiloto.py`):** Herramienta de auditoria de codigo asistida por inteligencia artificial (Google Gemini API) bajo el patron *Human-in-the-Loop*. Analiza scripts linea por linea, propone opciones de mejora y ejecuta puntos de respaldo automaticos en Git (`subprocess`) antes de aplicar cambios.

---

## Tecnologias Utilizadas

* **Lenguaje:** Python 3
* **Vision Artificial:** Ultralytics YOLOv8, OpenCV (`cv2`), PyTorch
* **Integraciones y APIs:** Google Gemini API (`v1beta`), Discord Webhooks, `requests`
* **Control de Versiones:** Git y GitHub

---

## Estructura del Repositorio

```text
Eco-Guard/
├── ecoguard/                  # Clases y logica de negocio (POO)
├── laboratorio/
│   ├── fotos_zorro/           # Dataset de imagenes de entrenamiento
│   ├── agente_copiloto.py     # Auditor de codigo con Gemini API y auto-backup en Git
│   ├── agente_mensajero.py    # Despacho de alertas y evidencia a Discord
│   ├── prueba_vision.py       # Motor de inferencia dual con YOLOv8 y OpenCV
│   └── zorro.pt               # Modelo personalizado entrenado
├── .gitignore                 # Reglas de exclusion de entornos, videos y credenciales
├── historial_ecoguard.txt     # Registro persistente de eventos
├── main.py                    # Punto de entrada del sistema de gestion
└── yolov8n.pt                 # Modelo base YOLOv8 nano