class Participante:
    def __init__(self, nombre, fecha_nacimiento, curso, tipo, posicion=None):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.curso = curso
        self.tipo = tipo
        self.posicion = posicion
