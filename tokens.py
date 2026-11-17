from dataclasses import dataclass

@dataclass
class Token:
    tipo: str
    texto: str
    linea: int
    columna: int

    def __str__(self):
        return f"{self.tipo}('{self.texto}') en {self.linea}:{self.columna}"

# --- NUEVA JERARQUÍA DE ERRORES ---
class ErrorDeLenguaje(Exception):
    fase = "Error"
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        super().__init__(f"{self.fase} en línea {linea}, columna {columna}: {mensaje}")

class ErrorLexico(ErrorDeLenguaje):
    fase = "Error léxico"

class ErrorSintactico(ErrorDeLenguaje):
    fase = "Error sintáctico"

class ErrorSemantico(ErrorDeLenguaje):
    fase = "Error semántico"