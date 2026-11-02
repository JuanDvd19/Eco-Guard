import sqlite3

def iniciar_bd():
    #Conectar al archivo de base de datos (En caso de que no exista, se creará automáticamente)
    conexion = sqlite3.connect("ecoguard.db")
    cursor = conexion.cursor()

    #SQL: CREATE TABLE (crea la tabla con sus columnas y tipos de datos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avistamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            especie TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def insertar_avistamiento(fecha, especie):
    conexion = sqlite3.connect("ecoguard.db")
    cursor = conexion.cursor()

    #SQL: INSERT INTO (guarda una fila nueva de forma segura usando "?")
    cursor.execute(
        "INSERT INTO avistamientos (fecha, especie) VALUES (?, ?)", (fecha, especie)
    )
    conexion.commit()
    conexion.close()

def consultar_conteo_especies():
    conexion = sqlite3.connect("ecoguard.db")
    cursor = conexion.cursor()

    #SQL: SELECT y GROUP BY (Cuenta cuantos animales hay de cada especie)
    cursor.execute("""
        SELECT especie, COUNT(*)
        FROM avistamientos
        GROUP BY especie
    """)
    resultados = cursor.fetchall()
    conexion.close()
    return dict(resultados) # Devuelve un diccionario con la especie como clave y el conteo como valor

#Bloque de prueba
if __name__ == "__main__":
    iniciar_bd()
    insertar_avistamiento("2026-11-02-14:30", "Zorro rojo")
    insertar_avistamiento("2026-11-02-15:00", "Animal detectado")
    insertar_avistamiento("2026-11-02-15:30", "Zorro rojo")

    print("Conteo directo desde SQL:", consultar_conteo_especies())