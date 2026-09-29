class Alerta:
    def __init__(self, mensaje, nivel):
        self.mensaje = mensaje
        self.nivel = nivel

    def mostrar_alerta(self):
        return f"[!] ALERTA {self.nivel.upper()}: {self.mensaje}"