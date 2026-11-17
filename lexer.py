from tokens import Token, ErrorLexico

# -------- Tipos, Booleanos y Asignación --------
TIPOS = {"entero", "real", "booleano", "texto"}
BOOLEANOS = {"velda", "embuste"}
ASIGNACION = {"igualito_con"}

# -------- Operadores Relacionales --------
OPERADORES_RELACIONALES = {
    "la_misma_vaina_que",  
    "no_cuadra_con", 
    "menor_que", 
    "mas_pesao_que",
    "menor_o_igualito_que", 
    "pesao_o_igualito_que"
}

# -------- Palabras Reservadas --------
PALABRAS_RESERVADAS = {
    "armaladef", "retornala", "tonces",
    "aja_si", "eso_entonce", "ya_que_hpta",
    "para", "en", "pinta", "mientras", 
    "Y", "O", "no",
    "nadita"
}

# -------- Comentario y bloque de comentario, Simbolos y Comillas --------
SIMBOLO_COMENTARIO = "#" 
APERTURA_BLOQUE = "/*" 
CIERRE_BLOQUE = "*/"
SIMBOLOS = "(){}[],."         
COMILLA = {"'", '"'}          

# -------- Operadores --------
OPERADORES = "+-*/"

# -------- Cule de codigo mi vale 🥵💀 --------
def tokenizar_monda(texto):
    tokens = []
    i = 0
    linea = 1
    columna = 1
    n = len(texto)
    tokens_en_linea = False

    while i < n:
        c = texto[i]

        if c == '\n':
            if tokens_en_linea:
                # CAMBIO: Ahora usa Token()
                tokens.append(Token("FIN_INSTRUCCION", "\\n", linea, columna))
                tokens_en_linea = False
            i += 1
            linea += 1
            columna = 1
            continue

        if c in ' \t\r':
            i += 1
            columna += 1
            continue

        if texto.startswith(APERTURA_BLOQUE, i):
            col_inicio = columna
            linea_inicio = linea
            i += 2
            columna += 2
            cerrado = False
            while i < n:
                if texto.startswith(CIERRE_BLOQUE, i):
                    i += 2
                    columna += 2
                    cerrado = True
                    break
                if texto[i] == '\n':
                    i += 1
                    linea += 1
                    columna = 1
                else:
                    i += 1
                    columna += 1
            if not cerrado:
                # CAMBIO: Ahora usa ErrorLexico()
                raise ErrorLexico("Comentario sin cerrar", linea_inicio, col_inicio)
            continue

        if c == SIMBOLO_COMENTARIO:
            while i < n and texto[i] != '\n':
                i += 1
            continue

        if c in COMILLA:
            col_inicio = columna
            linea_inicio = linea
            i += 1
            columna += 1
            inicio = i
            while i < n and texto[i] not in COMILLA:
                if texto[i] == '\n':
                    # CAMBIO: Ahora usa ErrorLexico()
                    raise ErrorLexico("Cadena sin cerrar", linea_inicio, col_inicio)
                i += 1
                columna += 1
            if i >= n:
                # CAMBIO: Ahora usa ErrorLexico()
                raise ErrorLexico("Cadena sin cerrar", linea_inicio, col_inicio)
            lexema = texto[inicio:i]
            i += 1
            columna += 1
            # CAMBIO: Ahora usa Token()
            tokens.append(Token("CADENA", lexema, linea_inicio, col_inicio))
            tokens_en_linea = True
            continue

        if c.isdigit():
            col_inicio = columna
            inicio = i
            while i < n and texto[i].isdigit():
                i += 1
                columna += 1
            if i < n and texto[i] == '.':
                if i + 1 < n and texto[i + 1].isdigit():
                    i += 1
                    columna += 1
                    while i < n and texto[i].isdigit():
                        i += 1
                        columna += 1
                else:
                    columna += 1
                    # CAMBIO: Ahora usa ErrorLexico()
                    raise ErrorLexico("Decimal mal formado", linea, columna)
            lexema = texto[inicio:i]
            # CAMBIO: Ahora usa Token()
            tokens.append(Token("NUMERO", lexema, linea, col_inicio))
            tokens_en_linea = True
            continue

        if c.isalpha():
            col_inicio = columna
            inicio = i
            while i < n and (texto[i].isalnum() or texto[i] == '_'):
                i += 1
                columna += 1
            lexema = texto[inicio:i]

            if lexema in TIPOS:
                tipo_token = "TIPO"
            elif lexema in BOOLEANOS:
                tipo_token = "BOOLEANO"
            elif lexema in ASIGNACION:
                tipo_token = "ASIGNACION"
            elif lexema in OPERADORES_RELACIONALES:    
                tipo_token = "OPERADOR_RELACIONAL"
            elif lexema in PALABRAS_RESERVADAS:
                tipo_token = "PALABRA_RESERVADA"
            else:
                tipo_token = "IDENTIFICADOR"

            # CAMBIO: Ahora usa Token()
            tokens.append(Token(tipo_token, lexema, linea, col_inicio))
            tokens_en_linea = True
            continue

        if c in OPERADORES:
            # CAMBIO: Ahora usa Token()
            tokens.append(Token("OPERADOR", c, linea, columna))
            tokens_en_linea = True
            i += 1
            columna += 1
            continue

        if c in SIMBOLOS:
            # CAMBIO: Ahora usa Token()
            tokens.append(Token("SIMBOLO", c, linea, columna))
            tokens_en_linea = True
            i += 1
            columna += 1
            continue

        # CAMBIO: Ahora usa ErrorLexico()
        raise ErrorLexico(f"carácter '{c}' no reconocido", linea, columna)

    if tokens_en_linea:
        # CAMBIO: Ahora usa Token()
        tokens.append(Token("FIN_INSTRUCCION", "\\n", linea, columna))
    
    # CAMBIO: Ahora usa Token()
    tokens.append(Token("EOF", "", linea, columna))

    return tokens


tokenizar = tokenizar_monda