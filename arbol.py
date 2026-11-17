from dataclasses import dataclass
from tokens import Token

@dataclass
class Numero:
    token: Token

@dataclass
class Variable:
    token: Token

@dataclass
class Cadena:
    token: Token

@dataclass
class OperacionBinaria:
    izq: object
    operador: Token
    der: object

@dataclass
class Negativo:
    operador: Token
    valor: object

@dataclass
class Comparacion:
    izq: object
    operador: Token
    der: object

@dataclass
class OperacionLogica:
    izq: object
    operador: Token
    der: object

@dataclass
class NegacionLogica:
    operador: Token
    valor: object

@dataclass
class Declaracion:
    tipo: Token
    nombre: Token
    valor: object

@dataclass
class Asignacion:
    nombre: Token
    valor: object

@dataclass
class Pinta:
    palabra: Token
    valor: object

@dataclass
class Si:
    palabra: Token
    condicion: object
    bloque_si: list
    bloque_else: list

@dataclass
class Mientras:
    condicion: object
    bloque: list
    palabra: Token

@dataclass
class Programa:
    instrucciones: list

@dataclass
class Booleano:
    token: Token

@dataclass
class Para:
    variable: Token
    iterable: object
    bloque: list