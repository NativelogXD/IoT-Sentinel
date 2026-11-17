# Gramática en EBNF de IoT-Sentinel:
# programa      ::= ( instruccion | FIN_INSTRUCCION )* EOF
# instruccion   ::= declaracion | asignacion | pinta | condicional | ciclo | ciclo_para
# declaracion   ::= TIPO IDENTIFICADOR 'igualito_con' condicion fin_instruccion
# asignacion    ::= IDENTIFICADOR 'igualito_con' condicion fin_instruccion
# pinta         ::= 'pinta' '(' condicion ')' fin_instruccion
# condicional   ::= 'aja_si' condicion 'tonces' bloque ( 'ya_que_hpta' bloque )?
# ciclo         ::= 'mientras' condicion 'tonces' bloque
# ciclo_para    ::= 'para' IDENTIFICADOR 'en' expresion 'tonces' bloque
# bloque        ::= '{' ( instruccion | FIN_INSTRUCCION )* '}'
# condicion     ::= condicion_o
# condicion_o   ::= condicion_y ( 'O' condicion_y )*
# condicion_y   ::= condicion_no ( 'Y' condicion_no )*
# condicion_no  ::= 'no' condicion_no | comparacion
# comparacion   ::= expresion ( OPERADOR_RELACIONAL expresion )?
# expresion     ::= termino ( ( '+' | '-' ) termino )*
# termino       ::= factor ( ( '*' | '/' ) factor )*
# factor        ::= '-' factor | NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | '(' condicion ')'

from tokens import Token, ErrorSintactico
from arbol import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos]

    def avanzar(self):
        t = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return t

    def esperar(self, tipo, texto=None):
        t = self.actual()
        if t.tipo != tipo or (texto is not None and t.texto != texto):
            esperado = f"'{texto}'" if texto else f"un {tipo}"
            llegó = "el fin del archivo" if t.tipo == "EOF" else f"'{t.texto}'"
            raise ErrorSintactico(f"se esperaba {esperado} y llegó {llegó}", t.linea, t.columna)
        return self.avanzar()

    def programa(self):
        instrucciones = []
        while self.actual().tipo != "EOF":
            if self.actual().tipo == "FIN_INSTRUCCION":
                self.avanzar()
                continue
            instrucciones.append(self.instruccion())
        return Programa(instrucciones)

    def instruccion(self):
        t = self.actual()
        if t.tipo == "TIPO":
            return self.declaracion()
        if t.tipo == "IDENTIFICADOR":
            return self.asignacion()
        if t.tipo == "PALABRA_RESERVADA" and t.texto == "pinta":
            return self.pinta()
        if t.tipo == "PALABRA_RESERVADA" and t.texto == "aja_si":
            return self.condicional()
        if t.tipo == "PALABRA_RESERVADA" and t.texto == "mientras":
            return self.ciclo()
        # NUEVO ELECTIVO: Ciclo para
        if t.tipo == "PALABRA_RESERVADA" and t.texto == "para":
            return self.ciclo_para()
            
        raise ErrorSintactico(f"se esperaba el inicio de una instrucción y llegó '{t.texto}'", t.linea, t.columna)

    def fin_instruccion(self):
        t = self.actual()
        if t.tipo == "FIN_INSTRUCCION":
            self.avanzar()
            return
        if t.tipo == "EOF" or (t.tipo == "SIMBOLO" and t.texto == "}"):
            return
        raise ErrorSintactico(f"se esperaba fin de instrucción y llegó '{t.texto}'", t.linea, t.columna)

    def declaracion(self):
        tipo = self.esperar("TIPO")
        nombre = self.esperar("IDENTIFICADOR")
        self.esperar("ASIGNACION", "igualito_con")
        valor = self.condicion()
        self.fin_instruccion()
        return Declaracion(tipo, nombre, valor)

    def asignacion(self):
        nombre = self.esperar("IDENTIFICADOR")
        self.esperar("ASIGNACION", "igualito_con")
        valor = self.condicion()
        self.fin_instruccion()
        return Asignacion(nombre, valor)

    def pinta(self):
        palabra = self.esperar("PALABRA_RESERVADA", "pinta")
        self.esperar("SIMBOLO", "(")
        valor = self.condicion()
        self.esperar("SIMBOLO", ")")
        self.fin_instruccion()
        return Pinta(palabra, valor)

    def condicional(self):
        palabra = self.esperar("PALABRA_RESERVADA", "aja_si")
        cond = self.condicion()
        self.esperar("PALABRA_RESERVADA", "tonces")
        bloque_si = self.bloque() 
        
        while self.actual().tipo == "FIN_INSTRUCCION":
            self.avanzar()

        bloque_else = None
        if self.actual().tipo == "PALABRA_RESERVADA" and self.actual().texto == "ya_que_hpta":
            self.avanzar()
            bloque_else = self.bloque()
            
        return Si(palabra, cond, bloque_si, bloque_else)

    def ciclo(self):
        palabra = self.esperar("PALABRA_RESERVADA", "mientras")
        cond = self.condicion() # (base ,  mas pesao que , 0)
        self.esperar("PALABRA_RESERVADA", "tonces")
        bloque = self.bloque()
        return Mientras(cond, bloque, palabra)

    
    def ciclo_para(self):
        self.esperar("PALABRA_RESERVADA", "para")
        variable = self.esperar("IDENTIFICADOR")
        self.esperar("PALABRA_RESERVADA", "en")
        iterable = self.expresion()
        self.esperar("PALABRA_RESERVADA", "tonces")
        bloque = self.bloque()
        return Para(variable, iterable, bloque)

    def bloque(self):
        llave = self.esperar("SIMBOLO", "{")
        instrucciones = []
        while not (self.actual().tipo == "SIMBOLO" and self.actual().texto == "}"):
            if self.actual().tipo == "EOF":
                t = self.actual()
                raise ErrorSintactico(f"falta '}}' para cerrar el bloque abierto en la línea {llave.linea}", t.linea, t.columna)
            if self.actual().tipo == "FIN_INSTRUCCION":
                self.avanzar()
                continue
            instrucciones.append(self.instruccion())
        self.avanzar()
        return instrucciones

    # --- CONDICIONES LÓGICAS ---
    def condicion(self):
        return self.condicion_o()

    def condicion_o(self):
        izq = self.condicion_y()
        while self.actual().tipo == "PALABRA_RESERVADA" and self.actual().texto == "O":
            operador = self.avanzar()
            der = self.condicion_y()
            izq = OperacionLogica(izq, operador, der)
        return izq

    def condicion_y(self):
        izq = self.condicion_no()
        while self.actual().tipo == "PALABRA_RESERVADA" and self.actual().texto == "Y":
            operador = self.avanzar()
            der = self.condicion_no()
            izq = OperacionLogica(izq, operador, der)
        return izq

    def condicion_no(self):
        if self.actual().tipo == "PALABRA_RESERVADA" and self.actual().texto == "no":
            operador = self.avanzar()
            valor = self.condicion_no()
            return NegacionLogica(operador, valor)
            
        return self.comparacion()

    def comparacion(self):
        izq = self.expresion()#   base
        
        # Si el siguiente token es un operador relacional, hacemos la comparación
        if self.actual().tipo == "OPERADOR_RELACIONAL":#  mas pesao que
            operador = self.avanzar()# mas pesao que
            der = self.expresion()#0
            return Comparacion(izq, operador, der)# (base ,  mas pesao que , 0)
            
        # Si no hay operador relacional, es una condición booleana directa (ej: 'activo')
        return izq
    
    # --- MATEMÁTICAS ---
    def expresion(self):
        izq = self.termino() #none
        while self.actual().tipo == "OPERADOR" and self.actual().texto in ("+", "-"):
            operador = self.avanzar()
            der = self.termino()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    def termino(self):
        izq = self.factor()
        while self.actual().tipo == "OPERADOR" and self.actual().texto in ("*", "/"):
            operador = self.avanzar()
            der = self.factor()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    def factor(self):
        t = self.actual()
        
        if t.tipo == "OPERADOR" and t.texto == "-":
            operador = self.avanzar()
            valor = self.factor()
            return Negativo(operador, valor)
            
        if t.tipo == "NUMERO":
            return Numero(self.avanzar())
            
        if t.tipo == "CADENA":
            return Cadena(self.avanzar())
            
        # NUEVO ELECTIVO: Reconocer booleanos (velda / embuste)
        if t.tipo == "BOOLEANO":
            return Booleano(self.avanzar())
            
        if t.tipo == "IDENTIFICADOR":
            return Variable(self.avanzar())
            
        if t.tipo == "SIMBOLO" and t.texto == "(":
            self.avanzar()
            dentro = self.condicion()
            self.esperar("SIMBOLO", ")")
            return dentro
            
        raise ErrorSintactico(f"se esperaba un número, variable, booleano o '(' y llegó '{t.texto}'", t.linea, t.columna)