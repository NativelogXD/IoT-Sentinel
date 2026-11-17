# IoT-Sentinel

## 1. Nombre del Lenguaje e Integrantes

* **Lenguaje:** `IoT-Sentinel`
* **Grupo:** Herederos de Epstein
* **Integrantes:** D. Gonzalez, J. Castañeda, J. Orozco
* **Materia:** Teoría de Autómatas y Lenguajes Formales — Institución Universitaria EAM

---

## 2. Cómo Ejecutar

Desde la carpeta del proyecto (donde están `main.py`, `tokens.py`, `lexer.py`, `arbol.py`, `parser.py`, `interprete.py` y `README.md`):

```bash
python main.py programa.txt
```

Ejemplos con los tres programas de muestra y las pruebas incluidas:

```bash
python main.py programa_tabla_3.txt
python main.py programa_factorial_5.txt
python main.py programa_promedio_notas.txt
```

---

## 3. Ficha del Lenguaje (IoT-Sentinel)

### Nombre y por qué se llama así
**IoT-Sentinel** nace como un lenguaje formal especializado para redactar **reglas de detección y políticas de respuesta en dispositivos IoT**, combinando la legibilidad de una sintaxis tipo Python con expresiones propias del **Diccionario Costeñol** (`igualito_con`, `aja_si`, `ya_que_hpta`, `tonces`, `la_misma_vaina_que`, `mas_pesao_que`, `pinta`, `velda`, `embuste`), de modo que cada regla de monitoreo pueda leerse como una decisión natural.

### Tabla de Traducción desde Java

| Elemento | Java | IoT-Sentinel | Ejemplo en IoT-Sentinel |
| :--- | :--- | :--- | :--- |
| **Tipos de datos** | `int`, `double`, `String`, `boolean` | `entero`, `real`, `texto`, `booleano` | `entero puerto igualito_con 8080` |
| **Asignación** | `=` | `igualito_con` | `suma igualito_con suma + n` |
| **Fin de instrucción** | `;` | Salto de línea `\n` (`FIN_INSTRUCCION`) | *(sin `;` al final de la línea)* |
| **Salida por consola** | `System.out.println(x);` | `pinta(x)` | `pinta("aprueba")` |
| **Condicional** | `if (...) { ... } else { ... }` | `aja_si ... tonces { ... } ya_que_hpta { ... }` | `aja_si n mas_pesao_que 10 tonces { pinta("ok") }` |
| **Ciclo `while`** | `while (...) { ... }` | `mientras ... tonces { ... }` | `mientras n menor_o_igualito_que 5 tonces { n igualito_con n + 1 }` |
| **Ciclo `for`** | `for (int i = 0; i < n; i = i + 1) { ... }` | `para i en n tonces { ... }` | `para i en 5 tonces { pinta(i) }` |
| **Comparadores** | `==`, `!=`, `<`, `>`, `<=`, `>=` | `la_misma_vaina_que`, `no_cuadra_con`, `menor_que`, `mas_pesao_que`, `menor_o_igualito_que`, `pesao_o_igualito_que` | `a mas_pesao_que 0` |
| **Operadores lógicos** | `&&`, `\|\|`, `!` | `Y`, `O`, `no` | `n pesao_o_igualito_que 1 Y n menor_o_igualito_que 10` |
| **Booleanos** | `true`, `false` | `velda`, `embuste` | `booleano listo igualito_con velda` |
| **Comentarios** | `// ...`, `/* ... */` | `# ...`, `/* ... */` | `# calcula total` |

### Una Decisión de Diseño
**Sin punto y coma (`;`) y con palabras en español costeño (`igualito_con`):** En lugar de exigir `;` al final de cada instrucción como en Java, el lexer emite un token `FIN_INSTRUCCION` al detectar el salto de línea `\n` cuando hubo tokens en esa línea. Además, la asignación se escribe `igualito_con` y la igualdad `la_misma_vaina_que`, eliminando la confusión clásica entre `=` y `==`.

---

## 4. Gramática Final en EBNF

```ebnf
programa      ::= ( instruccion | FIN_INSTRUCCION )* EOF
instruccion   ::= declaracion | asignacion | pinta | condicional | ciclo | ciclo_para

declaracion   ::= TIPO IDENTIFICADOR 'igualito_con' condicion FIN_INSTRUCCION
asignacion    ::= IDENTIFICADOR 'igualito_con' condicion FIN_INSTRUCCION
pinta         ::= 'pinta' '(' condicion ')' FIN_INSTRUCCION

condicional   ::= 'aja_si' condicion 'tonces' bloque ( 'ya_que_hpta' bloque )?
ciclo         ::= 'mientras' condicion 'tonces' bloque
ciclo_para    ::= 'para' IDENTIFICADOR 'en' expresion 'tonces' bloque
bloque        ::= '{' ( instruccion | FIN_INSTRUCCION )* '}'

condicion     ::= condicion_o
condicion_o   ::= condicion_y ( 'O' condicion_y )*
condicion_y   ::= condicion_no ( 'Y' condicion_no )*
condicion_no  ::= 'no' condicion_no | comparacion
comparacion   ::= expresion ( OPERADOR_RELACIONAL expresion )?

expresion     ::= termino ( ( '+' | '-' ) termino )*
termino       ::= factor ( ( '*' | '/' ) factor )*
factor        ::= '-' factor | NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | '(' condicion ')'
```

---

## 5. Reglas de Operaciones entre Tipos

### Tabla `ACEPTA` (Declaración y Asignación)
* `entero`: acepta `int`.
* `real`: acepta `int` y `float` (convierte `int` a `float`).
* `texto`: acepta `str`.
* `booleano`: acepta `bool` (`velda`, `embuste` o el resultado de una comparación/operación lógica).

### Operaciones Aritméticas (`+`, `-`, `*`, `/`)

| Operador | `entero` con `entero` | Al menos un `real` | `texto` con `texto` | `texto` con número |
| :---: | :--- | :--- | :--- | :--- |
| **`+`** | `entero` | `real` | Une los textos (`str + str`) | `Error semántico` |
| **`-` y `*`** | `entero` | `real` | `Error semántico` | `Error semántico` |
| **`/`** | División entera (`//`) | `real` (`/`) | `Error semántico` | `Error semántico` |

* Dividir entre `0` o `0.0` lanza `Error semántico: división por cero`.

---

## 6. Los Dos Requerimientos Electivos Escogidos

1. **Tipo booleano (`booleano`, `velda`, `embuste`):** Permite declarar y reasignar variables de tipo `booleano` tanto con literales (`velda`, `embuste`) como con el resultado de comparaciones y operadores lógicos (`booleano listo igualito_con n mas_pesao_que 3`), y usarlas directamente en condiciones de `aja_si` y `mientras`.
2. **Ciclo `for` (`para`):** Permite repetir un bloque con contador automático desde `0` hasta `limite - 1` mediante `para i en 5 tonces { pinta(i) }`, validando que el límite sea un número entero y creando un entorno propio para la variable del ciclo.
