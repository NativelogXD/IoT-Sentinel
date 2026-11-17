from tokens import ErrorSemantico
from arbol import *

ACEPTA = {
    "entero": (int,),
    "real": (int, float),
    "texto": (str,),
    "booleano": (bool,),
}

class Entorno:
    def __init__(self, padre=None):
        self.variables = {}
        self.padre = padre

    def declarar(self, nombre, info):
        if nombre in self.variables:
            return False
        self.variables[nombre] = info
        return True

    def obtener(self, nombre):
        if nombre in self.variables:
            return self.variables[nombre]
        if self.padre is not None:
            return self.padre.obtener(nombre)
        return None

class Interprete:
    def __init__(self):
        self.entorno_global = Entorno()
        self.entorno_actual = self.entorno_global

    def ejecutar_programa(self, programa):
        for instruccion in programa.instrucciones:
            self.ejecutar(instruccion)

    def ejecutar_bloque(self, instrucciones):
        padre = self.entorno_actual
        self.entorno_actual = Entorno(padre)
        for inst in instrucciones:
            self.ejecutar(inst)
        self.entorno_actual = padre

    def validar_tipo(self, tipo, valor, token):
        if type(valor) not in ACEPTA[tipo]:
            raise ErrorSemantico(
                f"no se puede guardar ese valor en la variable '{token.texto}' de tipo {tipo}",
                token.linea,
                token.columna,
            )
        if tipo == "real" and type(valor) is int:
            return float(valor)
        return valor


#---------------------------------------------------------------------------------------------------
    def ejecutar(self, nodo):
        if isinstance(nodo, Declaracion):
            nombre = nodo.nombre.texto
            tipo = nodo.tipo.texto
            if nombre in self.entorno_actual.variables:
                linea_previa = self.entorno_actual.variables[nombre]["linea"]
                raise ErrorSemantico(f"la variable '{nombre}' ya fue declarada en la línea {linea_previa}", nodo.nombre.linea, nodo.nombre.columna)
            valor = self.validar_tipo(tipo, self.evaluar(nodo.valor), nodo.nombre)
            self.entorno_actual.declarar(nombre, {"tipo": tipo, "valor": valor, "linea": nodo.nombre.linea})
            
        elif isinstance(nodo, Asignacion):
            nombre = nodo.nombre.texto # base
            var = self.entorno_actual.obtener(nombre)
            if var is None:
                raise ErrorSemantico(f"la variable '{nombre}' no ha sido declarada", nodo.nombre.linea, nodo.nombre.columna)
            var["valor"] = self.validar_tipo(var["tipo"], self.evaluar(nodo.valor), nodo.nombre)
            
        elif isinstance(nodo, Pinta):
            print(self.evaluar(nodo.valor))
            
        elif isinstance(nodo, Si):
            cond = self.evaluar(nodo.condicion)
            if type(cond) is not bool:
                raise ErrorSemantico("la condición de 'aja_si' debe ser de tipo booleano", nodo.palabra.linea, nodo.palabra.columna)
            if cond:
                self.ejecutar_bloque(nodo.bloque_si)
            elif nodo.bloque_else is not None:
                self.ejecutar_bloque(nodo.bloque_else)
                
        elif isinstance(nodo, Mientras):
            vueltas = 0
            while True:
                cond = self.evaluar(nodo.condicion)#TRUE
                if type(cond) is not bool:
                    raise ErrorSemantico("la condición de 'mientras' debe ser de tipo booleano", nodo.palabra.linea, nodo.palabra.columna)
                if not cond:# valida que si validcion del mientras es verdadera 
                    break
                vueltas += 1
                if vueltas > 100000:
                    raise ErrorSemantico("el ciclo superó 100000 vueltas; ¿falta actualizar la variable de la condición?", nodo.palabra.linea, nodo.palabra.columna)
                self.ejecutar_bloque(nodo.bloque)

        # NUEVO ELECTIVO: Ejecución del ciclo Para
        elif isinstance(nodo, Para):
            limite = self.evaluar(nodo.iterable)
            if type(limite) is not int:
                raise ErrorSemantico("El límite del ciclo 'para' debe ser un número entero", nodo.variable.linea, nodo.variable.columna)

            padre = self.entorno_actual
            self.entorno_actual = Entorno(padre)     #2         #numero
            self.entorno_actual.declarar(nodo.variable.texto , {"tipo": "entero", "valor": 0, "linea": nodo.variable.linea})

            # Itera desde 0 hasta limite - 1
            for i in range(limite):
                self.entorno_actual.obtener(nodo.variable.texto)["valor"] = i #incrementa i
                self.ejecutar_bloque(nodo.bloque) # realizar lo del bloque del para
            self.entorno_actual = padre


#------------------------------------------------------------------

    def evaluar(self, nodo):# evaluar valor
        if isinstance(nodo, Numero):
            texto = nodo.token.texto
            return float(texto) if "." in texto else int(texto)
            
        elif isinstance(nodo, Cadena):
            return nodo.token.texto

        # NUEVO ELECTIVO: Evaluación de booleanos
        elif isinstance(nodo, Booleano):
            return True if nodo.token.texto == "velda" else False
            
        elif isinstance(nodo, Variable):
            nombre = nodo.token.texto
            var = self.entorno_actual.obtener(nombre)
            if var is None:
                raise ErrorSemantico(f"la variable '{nombre}' no ha sido declarada", nodo.token.linea, nodo.token.columna)
            return var["valor"]

        elif isinstance(nodo, Negativo):
            valor = self.evaluar(nodo.valor)
            if type(valor) not in (int, float):
                raise ErrorSemantico("no se puede aplicar '-' a ese tipo de valor", nodo.operador.linea, nodo.operador.columna)
            return -valor
            
        elif isinstance(nodo, OperacionBinaria):
            izq = self.evaluar(nodo.izq)#6 
            der = self.evaluar(nodo.der)#2
            op = nodo.operador.texto# suma 

            if isinstance(izq, str) or isinstance(der, str):
                if op == "+" and isinstance(izq, str) and isinstance(der, str):
                    return izq + der
                raise ErrorSemantico(f"no se puede usar '{op}' con textos", nodo.operador.linea, nodo.operador.columna)

            if type(izq) not in (int, float) or type(der) not in (int, float):
                raise ErrorSemantico(f"no se puede usar '{op}' con esos tipos", nodo.operador.linea, nodo.operador.columna)

            if op == "+": return izq + der
            if op == "-": return izq - der
            if op == "*": return izq * der
            if op == "/":
                if der == 0:
                    raise ErrorSemantico("división por cero", nodo.operador.linea, nodo.operador.columna)
                return izq // der if type(izq) is int and type(der) is int else izq / der
                
        elif isinstance(nodo, Comparacion):
            izq = self.evaluar(nodo.izq)#-1
            der = self.evaluar(nodo.der)#0
            op = nodo.operador.texto##menor_que
            if op in ("la_misma_vaina_que", "no_cuadra_con"):
                if (type(izq) is bool) != (type(der) is bool):
                    raise ErrorSemantico(f"no se puede comparar booleano con otro tipo usando '{op}'", nodo.operador.linea, nodo.operador.columna)
                return (izq == der) if op == "la_misma_vaina_que" else (izq != der)

            son_numeros = type(izq) in (int, float) and type(der) in (int, float)
            son_textos = type(izq) is str and type(der) is str
            if not (son_numeros or son_textos):
                raise ErrorSemantico(f"no se puede usar '{op}' entre esos tipos", nodo.operador.linea, nodo.operador.columna)
            if op == "menor_que": return izq < der # TRUE
            if op == "mas_pesao_que": return izq > der
            if op == "menor_o_igualito_que": return izq <= der
            if op == "pesao_o_igualito_que": return izq >= der

        elif isinstance(nodo, OperacionLogica):
            izq = self.evaluar(nodo.izq)  
            der = self.evaluar(nodo.der) 
            op = nodo.operador.texto
            if type(izq) is not bool or type(der) is not bool:
                raise ErrorSemantico(f"el operador lógico '{op}' solo acepta booleanos", nodo.operador.linea, nodo.operador.columna)
            if op == "Y": return izq and der
            if op == "O": return izq or der

        elif isinstance(nodo, NegacionLogica):
            valor = self.evaluar(nodo.valor)
            if type(valor) is not bool:
                raise ErrorSemantico("el operador 'no' solo acepta booleanos", nodo.operador.linea, nodo.operador.columna)
            return not valor # return not false = true