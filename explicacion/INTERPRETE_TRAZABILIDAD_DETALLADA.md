# Trazabilidad Detallada e Intuición del Intérprete (`interprete.py`)

Esta guía reúne todas las analogías, aclaraciones conceptuales, estructuras textuales del AST y tablas de trazabilidad de [`programa_completo_trazabilidad.txt`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/explicacion/programa_completo_trazabilidad.txt) usando las **líneas exactas actuales** de [`compilador/interprete.py`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py) y [`compilador/main.py`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/main.py).

---

## 1. ¿Cómo se conecta el Parser con el Intérprete?

El [`parser.py`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/parser.py) y el [`interprete.py`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py) **no se hablan directamente**; el puente es [`main.py`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/main.py#L23-L27) en estas **4 líneas exactas**:

1. **Sale del Parser ([`parser.py#L52`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/parser.py#L52)):** al encontrar `EOF`, termina y retorna `Programa(instrucciones)`.
2. **Lo recibe y lo pasa `main.py` ([`main.py#L23-L27`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/main.py#L23-L27)):**
   ```python
   23: parser = Parser(lista_tokens)
   24: arbol_programa = parser.programa()             # Recibe Programa(instrucciones=[...])
   25: 
   26: interprete = Interprete()                        # Crea entorno_global y entorno_actual
   27: interprete.ejecutar_programa(arbol_programa)   # Entrega el árbol al Intérprete
   ```
3. **Entra al Intérprete ([`interprete.py#L34-L36`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L34-L36)):**
   ```python
   34: def ejecutar_programa(self, programa):
   35:     for instruccion in programa.instrucciones:
   36:         self.ejecutar(instruccion)
   ```

### ¿Se recorre de izquierda a derecha?
**Sí, en ambos niveles:**
* **En la lista raíz (`programa.instrucciones`):** el `for` de [`L35`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L35) recorre la lista de izquierda a derecha (índices `[0]` hasta `[6]`, es decir, línea por línea).
* **Dentro de cada árbol de expresión (`OperacionBinaria`, `Comparacion`, `OperacionLogica`):** siempre se ejecuta primero `izq = self.evaluar(nodo.izq)` ([`L145`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L145)) y luego `der = self.evaluar(nodo.der)` ([`L146`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L146)), bajando primero hasta la hoja más a la izquierda.

> **Árbol completo:** El AST completo (en modo jerárquico y textual de Python) está guardado en [`programas_docente/arbol_programa_completo_trazabilidad.txt`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/programas_docente/arbol_programa_completo_trazabilidad.txt).

---

## 2. Ideas y Analogías Clave para Comprender la Teoría

### A. La analogía de la libreta (`entorno_actual` y `self.padre`)
* **`self.entorno_actual`** ([`interprete.py#L31-L32`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L31-L32)) es un puntero hacia la **libreta de apuntes** que el Intérprete tiene en la mano en este preciso instante.
* Cada libreta es una instancia de `Entorno` ([`interprete.py#L11-L27`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L11-L27)) con:
  1. `self.variables`: diccionario `{ "nombre": {"tipo": ..., "valor": ..., "linea": ...} }` con las variables que nacieron en ese bloque.
  2. `self.padre`: flecha hacia el `Entorno` exterior (o `None` si es `entorno_global`).

### B. Aclaración fundamental: ¿Qué es `self.padre`?
**`self.padre` NO es un número, ni un carácter, ni el operador `+` del dibujo del árbol.**
* En el árbol de expresiones, al `+` se le llama informalmente "nodo padre" de `3` y `6`, pero en código es un objeto `OperacionBinaria`.
* En `Entorno` ([`L14`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L14), [`L25-L26`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L25-L26)), `self.padre` es **otra libreta (otro objeto `Entorno` externo)** con su propio diccionario de variables donde se puede consultar externamente cuánto vale una variable declarada afuera (ej. `base` o `x` en `x + 1`).
* **Detalle clave de la "investigación externa":** cuando una operación dentro de un bloque consulta una variable de afuera (ej. `base`), `obtener("base")` sube por `self.padre` ([`L26`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L26)), lee cuánto vale y **se trae el valor en la mano (`return var["valor"]` en [`L136`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L136)) sin copiar esa variable dentro de la libreta interna**. Así, cada variable sigue viviendo únicamente en la libreta donde nació.

### C. Qué es `ejecutar_bloque(instrucciones)` y qué son `bloque` e `inst` ([`L38-L43`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L38-L43))
* **`bloque=[ ... ]`** (como argumento `instrucciones` en [`L38`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L38)) **es una lista (`list`)**, no un diccionario: contiene en orden todas las instrucciones que estaban entre `{` y `}`.
* **`inst`** en `for inst in instrucciones:` ([`L41`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L41)) **equivale al objeto/sub-grafo completo de esa instrucción hija** (por ejemplo todo el nodo `Asignacion(...)` o todo el nodo `Pinta(...)`), **no** a una palabra suelta. En [`L42`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L42), `self.ejecutar(inst)` lo clasifica con `isinstance(...)`.
* **Doble papel de `ejecutar_bloque`:**
  1. Conecta hacia afuera mediante `Entorno(padre)` ([`L39-L40`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L39-L40)) para poder leer y actualizar variables externas como `base`.
  2. **Reinicia una libreta temporal limpia en cada vuelta** de un ciclo y la suelta en [`L43`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L43) (`self.entorno_actual = padre`), evitando colisiones si se declaran variables locales dentro del bucle.

### D. Recursividad en `OperacionBinaria` y el doble tiempo de la línea 65
* **¿Por qué no se guardan variables para los resultados intermedios (`4` y `8`) en `(base + 6) * 2 / 2.0`?**
  Porque `evaluar()` es **recursivo**. Al llamar `izq = self.evaluar(nodo.izq)` ([`L145`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L145)), la operación padre se queda pausada en la pila de llamadas de Python; cuando el hijo hace `return` (`4`, luego `8`), ese resultado cae directamente en el `izq` temporal del padre y la llamada del hijo desaparece. La libreta `entorno_actual` solo se toca al final, cuando llega a `Declaracion` o `Asignacion`.
* **¿Por qué `Declaracion` se pausa en la línea 65 y regresa a la misma línea 65 antes de bajar a la 66?**
  ```python
  65: valor = self.validar_tipo(tipo, self.evaluar(nodo.valor), nodo.nombre)
  66: self.entorno_actual.declarar(nombre, {"tipo": tipo, "valor": valor, "linea": nodo.nombre.linea})
  ```
  Python evalúa **de adentro hacia afuera** en la misma línea [`65`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L65):
  1. Primero queda pausado en la **línea 65** mientras `self.evaluar(nodo.valor)` resuelve todo el árbol.
  2. Cuando `evaluar()` retorna `4.0`, regresa a la **misma línea 65** para ejecutar `self.validar_tipo("real", 4.0, nodo.nombre)` ([`L45-L54`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L45-L54)).
  3. Recién cuando `validar_tipo()` retorna `4.0`, baja a la **línea 66** para anotarlo en la libreta (`declarar`).

---

## 3. Casos Específicos Desglosados en Profundidad

### Caso 1: Declaración con Operaciones Anidadas (`real nota igualito_con (base + 6) * 2 / 2.0`)

Estado inicial antes de esta línea: `entorno_actual = E_global` con `{"base": {"tipo": "entero", "valor": -2, "linea": 2}}`.

| Paso | Nodo procesando | Método activo y línea | Qué hace exactamente |
| :-: | :--- | :--- | :--- |
| **1** | `Programa.instrucciones[1]` | `main()` $\to$ `ejecutar_programa()`<br>[`main.py#L27`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/main.py#L27), [`L34-L36`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L34-L36) | En la 2ª vuelta del `for`, entrega el nodo `Declaracion(real, nota, ...)` a `self.ejecutar(instruccion)`. |
| **2** | `Declaracion(real, nota, ...)` | `ejecutar()`<br>[`L59-L65`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L59-L65) | Lee `nombre="nota"` (`L60`), `tipo="real"` (`L61`), confirma en `L62` que `"nota"` no esté ya anotada y **se pausa en `L65`** esperando `self.evaluar(nodo.valor)`. |
| **3** | `OperacionBinaria` **`/`** | `evaluar()` #1<br>[`L144-L145`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L144-L145) | Pide `izq = self.evaluar((base + 6) * 2)` y **se pausa en `L145`**. |
| **4** | `OperacionBinaria` **`*`** | `evaluar()` #2<br>[`L144-L145`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L144-L145) | Pide `izq = self.evaluar(base + 6)` y **se pausa en `L145`**. |
| **5** | `OperacionBinaria` **`+`** | `evaluar()` #3<br>[`L144-L145`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L144-L145) | Pide `izq = self.evaluar(Variable('base'))` y **se pausa en `L145`**. |
| **6** | `Variable('base')` *(hoja)* | `evaluar()` #4 $\to$ `obtener("base")`<br>[`L131-L136`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L131-L136), [`L22-L24`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L22-L24) | Encuentra `"base"` directo en la libreta actual (`E_global`), toma `-2` y lo retorna al `izq` de `+`. |
| **7** | `Numero('6')` *(hoja)* | `evaluar()` #3 $\to$ `evaluar()` #5<br>[`L146`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L146), [`L120-L122`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L120-L122) | Despierta `+` en `L146`, evalúa `Numero('6')` $\to$ retorna `int(6)`. |
| **8** | `OperacionBinaria` **`+`** *(resuelve)* | `evaluar()` #3<br>[`L147-L157`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L147-L157) | Valida tipos numéricos (`L149-L155`), suma `-2 + 6` en `L157` y **retorna `4`** directo al `izq` de `*` (sin guardarlo en libreta). |
| **9** | `Numero('2')` *(hoja)* | `evaluar()` #2 $\to$ `evaluar()` #6<br>[`L146`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L146), [`L120-L122`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L120-L122) | Despierta `*` en `L146`, evalúa `Numero('2')` $\to$ retorna `int(2)`. |
| **10** | `OperacionBinaria` **`*`** *(resuelve)* | `evaluar()` #2<br>[`L147-L159`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L147-L159) | Valida tipos, multiplica `4 * 2` en `L159` y **retorna `8`** directo al `izq` de `/`. |
| **11** | `Numero('2.0')` *(hoja)* | `evaluar()` #1 $\to$ `evaluar()` #7<br>[`L146`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L146), [`L120-L122`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L120-L122) | Despierta `/` en `L146`, evalúa `Numero('2.0')` $\to$ como tiene `"."`, retorna `float(2.0)`. |
| **12** | `OperacionBinaria` **`/`** *(resuelve)* | `evaluar()` #1<br>[`L147-L163`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L147-L163) | Verifica `der != 0` (`L161`), divide `8 / 2.0` (`float`) en `L163` y **retorna `4.0`** hacia `ejecutar()` (`L65`). |
| **13** | Validación de tipo (`real`) | `ejecutar()` $\to$ `validar_tipo()`<br>[`L65`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L65), [`L45-L54`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L45-L54) | **Regresa a la misma línea 65** con `4.0` y llama a `validar_tipo("real", 4.0, Token('nota'))` (`type(4.0) in (int, float)` $\to$ `4.0`). |
| **14** | Anotar en la libreta | `ejecutar()` $\to$ `declarar()`<br>[`L66`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L66), [`L16-L20`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L16-L20) | Baja a `L66`, anota `"nota": {"tipo": "real", "valor": 4.0, "linea": 3}` en `E_global` y termina `Declaracion`. |

---

### Caso 2: Flujo real dentro de `Mientras` ([`L87-L98`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L87-L98))

* **Aclaración clave:** `Asignacion` **NO** ocurre después de que se acaba el `Mientras`, sino **adentro en cada vuelta mientras la condición sea `True` (`L98`)**. Cuando la condición da `False` (`0 < 0`), `if not cond: break` ([`L93-L94`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L93-L94)) rompe el ciclo sin volver a ejecutar `L98` ni `Asignacion`.
* **Cadena de cada vuelta:** `while True` (`L89`) $\to$ evalúa `cond = Comparacion(base < 0)` (`L90`) $\to$ valida `bool` (`L91`) $\to$ suma `vueltas` (`L95`) $\to$ `ejecutar_bloque(nodo.bloque)` (`L98` $\to$ `L41-L42`) toma el elemento `[0]` (`Asignacion(...)`) y entra a `L68-L73`, sube por `self.padre` (`L26`) para encontrar y modificar `base` en `E_global`, suelta la libreta temporal en `L43` y regresa a `L89`.

---

### Caso 3: Convivencia de los 3 Entornos en el Ciclo `Para` ([`L101-L114`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L101-L114))

Cuando se ejecuta `para i en 2 tonces { pinta(base + i) }`, coexisten **3 libretas apiladas** conectadas hacia afuera por `.padre` (mientras `self.entorno_actual` señala en qué libreta estamos):

```text
[ E_global: {base: 0, nota: 4.0, activo: True} ]   <── Caja grande (afuera, padre = None)
    ▲ (.padre)
    └── [ E_para: {i: 0 o 1} ]                     <── Caja del medio (convive durante todo el ciclo)
            ▲ (.padre)
            └── [ E_bloque: {} ]                   <── Caja chiquita (nace y muere en cada vuelta)
```

| Momento | Línea exacta | A quién apunta `self.entorno_actual` | Qué cambia en los datos |
| :--- | :---: | :--- | :--- |
| **1. Antes del `para`** | [`L101-L102`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L101-L102) | **`E_global`** | Evalúa `limite = 2` (`int`). `E_global = {base: 0, nota: 4.0, activo: True}`. |
| **2. Entra al `para`** | [`L106-L108`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L106-L108) | **`E_para`** *(padre: `E_global`)* | Guarda `padre = E_global` (`L106`), crea `E_para` (`L107`) y anota `i = 0` en `E_para` (`L108`). |
| **3. Vuelta 1 (`i=0`) — abre `{`** | [`L112-L113`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L112-L113) $\to$ [`L40`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L40) | **`E_bloque_1`** *(padre: `E_para` $\to$ `E_global`)* | `L112` deja `i = 0` en `E_para`. `L113` llama a `ejecutar_bloque` y `L40` abre `E_bloque_1 = {}`. |
| **4. Vuelta 1 — `pinta(base + i)`** | [`L41-L42`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L41-L42) $\to$ [`L26`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L26) | **`E_bloque_1`** | `base` sube 2 veces (`E_bloque_1` $\to$ `E_para` $\to$ `E_global` = `0`); `i` sube 1 vez (`E_bloque_1` $\to$ `E_para` = `0`). Imprime **`0`**. En `L43` vuelve a `E_para`. |
| **5. Vuelta 2 (`i=1`)** | [`L112-L113`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L112-L113) $\to$ [`L40`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L40) | **`E_bloque_2`** | `L112` cambia `i` en `E_para` a **`1`**. Abre `E_bloque_2`, lee `base = 0` + `i = 1`, imprime **`1`**, y en `L43` vuelve a `E_para`. |
| **6. Termina el `para`** | [`L114`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L114) | **`E_global`** | `self.entorno_actual = padre` (`E_global`). **`E_para` e `i` desaparecen de la memoria.** |

---

## 4. Desmontaje Completo Paso a Paso (`programa_completo_trazabilidad.txt`, Pasos 1–27)

### Arranque e Instrucciones 1, 2 y 3 (`base`, `nota`, `activo`)

| Paso | Nodo / Instrucción | Método activo y línea | Estado de `entorno_actual` (libreta) | Qué hace exactamente |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Arranque del Intérprete | `main()` $\to$ `Interprete.__init__()`<br>[`main.py#L26-L27`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/main.py#L26-L27), [`L30-L36`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L30-L36) | `E_global = {}`<br>`padre = None` | Crea `entorno_global` vacío y pone `entorno_actual = entorno_global` (`L31-L32`). Entra a `ejecutar_programa()` (`L34`) para recorrer los 7 nodos de `programa.instrucciones`. |
| **2** | **Inst 1:** `entero base igualito_con -2`<br>*(Línea 2 del `.txt`)* | `ejecutar(Declaracion)`<br>[`L58-L65`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L58-L65) | `E_global = {}` | Toma `nombre="base"`, `tipo="entero"`. Revisa en `L62` que no exista. En `L65` se pausa esperando `self.evaluar(Negativo('-', Numero('2')))`. |
| **3** | `Negativo('-', Numero('2'))` | `evaluar(Negativo)` $\to$ `evaluar(Numero)`<br>[`L138-L142`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L138-L142), [`L120-L122`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L120-L122) | `E_global = {}` | En `L139` evalúa `Numero('2')` $\to$ `2` (`int`). En `L140` valida que sea número. En `L142` retorna `-2` hacia `L65`. |
| **4** | Guardar `base` | `ejecutar()` $\to$ `validar_tipo()` $\to$ `declarar()`<br>[`L65-L66`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L65-L66), [`L45-L54`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L45-L54) | `E_global = {base: -2}` | Vuelve a `L65`, `validar_tipo("entero", -2)` aprueba `int`. En `L66` anota `"base": -2` en `E_global`. Termina Inst 1. |
| **5** | **Inst 2:** `real nota igualito_con (base + 6) * 2 / 2.0`<br>*(Línea 3 del `.txt`)* | `ejecutar(Declaracion)` $\to$ `evaluar(/ -> * -> +)`<br>[`L59-L65`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L59-L65), [`L144-L145`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L144-L145) | `E_global = {base: -2}` | Se pausa en `L65`. Baja por `izq` (`L145`): `/` $\to$ `*` $\to$ `+` $\to$ `Variable('base')`. |
| **6** | `Variable('base')` y `Numero('6')` en `+` | `evaluar(Variable)` $\to$ `obtener("base")`<br>[`L131-L136`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L131-L136), [`L22-L24`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L22-L24), [`L157`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L157) | `E_global = {base: -2}` | `obtener("base")` la halla directo en `E_global` $\to$ `-2`. Luego evalúa `der = 6` (`L146`). En `L157` suma `-2 + 6` y retorna `4` al `izq` del `*`. |
| **7** | Subida por `*` y `/` | `evaluar(*)` $\to$ `evaluar(/)`<br>[`L146`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L146), [`L159-L163`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L159-L163) | `E_global = {base: -2}` | `*` evalúa `der = 2`, multiplica `4 * 2` (`L159`) y retorna `8` al `izq` del `/`. `/` evalúa `der = 2.0` (`float`), valida `der != 0` (`L161`) y en `L163` divide `8 / 2.0` $\to$ retorna `4.0` a `L65`. |
| **8** | Guardar `nota` | `ejecutar()` $\to$ `validar_tipo()` $\to$ `declarar()`<br>[`L65-L66`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L65-L66) | `E_global = {base: -2, nota: 4.0}` | Vuelve a `L65`, `validar_tipo("real", 4.0)` aprueba `float`. En `L66` anota `"nota": 4.0` en `E_global`. Termina Inst 2. |
| **9** | **Inst 3:** `booleano activo igualito_con nota pesao_o_igualito_que 3.0 Y no embuste`<br>*(Línea 4 del `.txt`)* | `ejecutar(Declaracion)` $\to$ `evaluar(OperacionLogica 'Y')`<br>[`L65`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L65), [`L183-L184`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L183-L184) | `E_global = {base: -2, nota: 4.0}` | Se pausa en `L65`. Entra a `OperacionLogica('Y')` (`L183`). En `L184` pide `izq`: `Comparacion(nota >= 3.0)`. |
| **10** | `Comparacion(nota >= 3.0)` | `evaluar(Comparacion)`<br>[`L165-L181`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L165-L181) | `E_global = {base: -2, nota: 4.0}` | Lee `nota` de `E_global` (`4.0`), evalúa `der = 3.0`. Verifica que ambos sean números (`L174-L177`) y en `L181` calcula `4.0 >= 3.0` $\to$ retorna `True` al `izq` de `'Y'`. |
| **11** | `NegacionLogica('no', embuste)` y `'Y'` | `evaluar(NegacionLogica)` $\to$ `evaluar(OperacionLogica)`<br>[`L192-L196`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L192-L196), [`L128-L129`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L128-L129), [`L187-L189`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L187-L189) | `E_global = {base: -2, nota: 4.0}` | En `L185` `'Y'` evalúa `der`: `NegacionLogica` lee `embuste` $\to$ `False` (`L129`), valida `bool` (`L194`) y retorna `not False` = `True` (`L196`). En `L187` `'Y'` valida `bool` y en `L189` retorna `True and True` = `True` a `L65`. |
| **12** | Guardar `activo` | `ejecutar()` $\to$ `validar_tipo()` $\to$ `declarar()`<br>[`L65-L66`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L65-L66) | `E_global = {base: -2, nota: 4.0, activo: True}` | Vuelve a `L65`, `validar_tipo("booleano", True)` aprueba `bool`. En `L66` anota `"activo": True` en `E_global`. Termina Inst 3. |

### Instrucción 4: Condicional `aja_si` y Alcance de Bloques (`E_si`)

| Paso | Nodo / Instrucción | Método activo y línea | Estado de `entorno_actual` (libreta) | Qué hace exactamente |
| :-: | :--- | :--- | :--- | :--- |
| **13** | **Inst 4:** `aja_si activo O base mas_pesao_que 0 tonces { ... }`<br>*(Línea 6 del `.txt`)* | `ejecutar(Si)` $\to$ `evaluar(OperacionLogica 'O')`<br>[`L78-L80`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L78-L80), [`L183-L190`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L183-L190) | `E_global = {base: -2, nota: 4.0, activo: True}` | En `L79` evalúa `activo O (base > 0)`: lee `activo` (`True`), evalúa `base > 0` (`-2 > 0` = `False` en `L179`), y en `L190` `'O'` retorna `True or False` = `True`. En `L80` verifica `type(True) is bool`. |
| **14** | Abrir bloque del `aja_si` | `ejecutar(Si)` $\to$ `ejecutar_bloque()`<br>[`L82-L83`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L82-L83), [`L38-L40`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L38-L40) | `E_si = {}`<br>`padre = E_global` | Como `cond` es `True`, llama a `ejecutar_bloque(bloque_si)` (`L83`). En `L39` guarda `padre = E_global` y en `L40` cambia la libreta actual a `E_si(padre=E_global)`. *(El `ya_que_hpta` de `L84` no se ejecuta).* |
| **15** | `texto estado igualito_con "aprobado"`<br>*(Línea 7 del `.txt`)* | `ejecutar(Declaracion)` $\to$ `evaluar(Cadena)`<br>[`L59-L66`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L59-L66), [`L124-L125`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L124-L125) | `E_si = {estado: "aprobado"}`<br>`padre = E_global` | Evalúa `Cadena("aprobado")` (`L125`). En `L65` valida `str` y en `L66` anota `"estado": "aprobado"` **dentro de `E_si` (no en `E_global`)**. |
| **16** | `pinta(estado)`<br>*(Línea 8 del `.txt`)* | `ejecutar(Pinta)` $\to$ `evaluar(Variable)`<br>[`L75-L76`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L75-L76), [`L131-L136`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L131-L136) | `E_si = {estado: "aprobado"}`<br>`padre = E_global` | `obtener("estado")` (`L23-L24`) la encuentra en `E_si` y retorna `"aprobado"`. En `L76` imprime **`aprobado`** en consola. |
| **17** | Cerrar bloque del `aja_si` | `ejecutar_bloque()`<br>[`L43`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L43) | `E_global = {base: -2, nota: 4.0, activo: True}` | Ejecuta `self.entorno_actual = padre`. **Suelta `E_si` y la variable `estado` desaparece para siempre.** Termina Inst 4. |

### Instrucción 5: Ciclo `mientras` (2 vueltas modificando `base` afuera)

| Paso | Nodo / Instrucción | Método activo y línea | Estado de `entorno_actual` (libreta) | Qué hace exactamente |
| :-: | :--- | :--- | :--- | :--- |
| **18** | **Inst 5 (Vuelta 1):** `mientras base menor_que 0`<br>*(Líneas 13–15 del `.txt`)* | `ejecutar(Mientras)` $\to$ `evaluar(Comparacion)`<br>[`L87-L98`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L87-L98), [`L178`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L178) | `E_global = {base: -2, ...}` | En `L90` evalúa `base < 0` (`-2 < 0` = `True`). Valida `bool` (`L91`), suma `vueltas = 1` (`L95`) y en `L98` abre `E_mientras1(padre=E_global)`. |
| **19** | `base igualito_con base + 1` *(Vuelta 1)* | `ejecutar(Asignacion)` $\to$ `obtener("base")`<br>[`L68-L73`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L68-L73), [`L25-L26`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L25-L26) | `E_mientras1 = {}` $\to$ `padre = E_global` | En `L70` `obtener("base")` sube por `self.padre` (`L26`) hasta `E_global`. En `L73` evalúa `-2 + 1 = -1`, valida `int` y **actualiza `base = -1` en `E_global`**. En `L43` cierra `E_mientras1`. |
| **20** | **Inst 5 (Vuelta 2):** `mientras base menor_que 0` | `ejecutar(Mientras)` $\to$ `ejecutar(Asignacion)`<br>[`L89-L98`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L89-L98), [`L68-L73`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L68-L73) | `E_global = {base: 0, nota: 4.0, activo: True}` | En `L90` evalúa `-1 < 0` = `True`. `vueltas = 2`. Abre `E_mientras2(padre=E_global)`, evalúa `-1 + 1 = 0`, actualiza **`base = 0` en `E_global`** y cierra `E_mientras2`. |
| **21** | **Inst 5 (Salida):** `base < 0` | `ejecutar(Mientras)`<br>[`L90-L94`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L90-L94) | `E_global = {base: 0, nota: 4.0, activo: True}` | En `L90` evalúa `0 < 0` = `False`. En `L93-L94` ejecuta `break` y **termina el ciclo `mientras` sin volver a `Asignacion`**. Termina Inst 5. |

### Instrucción 6: Ciclo `para` (`E_bloque` $\to$ `E_para` $\to$ `E_global`)

| Paso | Nodo / Instrucción | Método activo y línea | Estado de `entorno_actual` (libreta) | Qué hace exactamente |
| :-: | :--- | :--- | :--- | :--- |
| **22** | **Inst 6:** `para i en 2 tonces { ... }`<br>*(Líneas 17–19 del `.txt`)* | `ejecutar(Para)`<br>[`L101-L108`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L101-L108) | `E_para = {i: 0}`<br>`padre = E_global` | En `L102` evalúa `limite = 2` (`L122`). En `L103` verifica `type(2) is int`. En `L106-L108` abre `E_para(padre=E_global)` y declara ahí `i = 0`. |
| **23** | **Iteración `i = 0`:** `pinta(base + i)` | `ejecutar(Para)` $\to$ `ejecutar_bloque()` $\to$ `ejecutar(Pinta)`<br>[`L111-L113`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L111-L113), [`L75-L76`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L75-L76), [`L144-L157`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L144-L157) | `E_bloque_1 = {}` $\to$ `E_para(i:0)` $\to$ `E_global(base:0)` | Actualiza `i = 0` (`L112`) y entra a `ejecutar_bloque` (`L113`). `base` sube 2 veces (`E_global` = `0`); `i` sube 1 vez (`E_para` = `0`). Suma `0 + 0 = 0`, imprime **`0`** (`L76`) y cierra `E_bloque_1`. |
| **24** | **Iteración `i = 1`:** `pinta(base + i)` | `ejecutar(Para)` $\to$ `ejecutar_bloque()` $\to$ `ejecutar(Pinta)`<br>[`L111-L113`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L111-L113), [`L75-L76`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L75-L76) | `E_bloque_2 = {}` $\to$ `E_para(i:1)` $\to$ `E_global(base:0)` | Actualiza `i = 1` (`L112`) y abre `E_bloque_2`. Lee `base = 0` de `E_global` e `i = 1` de `E_para`. Suma `0 + 1 = 1`, imprime **`1`** (`L76`) y cierra `E_bloque_2`. |
| **25** | Cerrar ciclo `para` | `ejecutar(Para)`<br>[`L114`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L114) | `E_global = {base: 0, nota: 4.0, activo: True}` | Termina `range(2)` y en `L114` restaura `self.entorno_actual = padre`. **`E_para` e `i` desaparecen de memoria.** Termina Inst 6. |

### Instrucción 7: El Error Semántico con Puntero `^` (`pinta(estado)`)

| Paso | Nodo / Instrucción | Método activo y línea | Estado de `entorno_actual` (libreta) | Qué hace exactamente |
| :-: | :--- | :--- | :--- | :--- |
| **26** | **Inst 7:** `pinta(estado)`<br>*(Línea 21 del `.txt`)* | `ejecutar(Pinta)` $\to$ `evaluar(Variable)` $\to$ `obtener("estado")`<br>[`L75-L76`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L75-L76), [`L131-L135`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L131-L135), [`L22-L27`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/interprete.py#L22-L27) | `E_global = {base: 0, nota: 4.0, activo: True}` | En `L76` llama a `evaluar(Variable('estado'))`. En `L133` busca `"estado"` en `E_global`. Como `estado` murió en el Paso 17 y `self.padre` es `None`, `obtener()` retorna `None` (`L27`). En `L135` lanza `ErrorSemantico("la variable 'estado' no ha sido declarada", 21, 7)`. |
| **27** | Captura y puntero visual `^` | `main()` (`except ErrorDeLenguaje`)<br>[`main.py#L29-L41`](file:///c:/Users/xiao/Documents/universidad/lenguajes%20formales/mi_compilador_v2/mi_compilador_v3/mi_compilador_v3/compilador/main.py#L29-L41) | Fin del programa | `main.py` atrapa el error en `L29`, imprime el mensaje (`L30`), imprime la línea 21 `pinta(estado)` (`L37`), alinea 6 espacios y coloca `^` debajo de la columna 7 (`L39`), e imprime `línea = 21, columna = 7` (`L41`). |

---

## 5. Salida Final en Consola

```text
aprobado
0
1

Error semántico en línea 21, columna 7: la variable 'estado' no ha sido declarada
pinta(estado)
      ^
línea = 21, columna = 7
```
