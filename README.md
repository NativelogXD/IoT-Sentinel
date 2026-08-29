# IoT-Sentinel
integrantes: D.GONZALEZ ,J.CASTANEDA,J.OROZCO
Este repositorio contiene la definición y el motor de procesamiento de **IoT-Sentinel**, un sistema de evaluación de amenazas y microsegmentación adaptado para redes IoT, implementando un lenguaje de dominio específico.

---

##  Sobre Kitsune (El Motor Base)

Este proyecto toma como núcleo y referencia arquitectónica el repositorio [Kitsune-py](https://github.com/ymirsky/Kitsune-py). 

**Kitsune** es un Sistema de Detección de Intrusos en la Red (NIDS) de tipo *plug-and-play* basado en aprendizaje profundo (*Deep Learning*). Fue diseñado para ser lo suficientemente ligero como para ejecutarse en tiempo real en dispositivos de borde (*edge devices*) como una Raspberry Pi, sin necesidad de enviar el tráfico a un servidor externo.

El funcionamiento de Kitsune se divide en dos componentes principales que nuestro aplicativo respeta:

1. **AfterImage:** Un extractor de características estadísticas que analiza el tráfico de la red (archivos PCAP) paquete por paquete de forma incremental.
2. **KitNET:** Un ensamble de redes neuronales (*Autoencoders*) que procesa estas estadísticas. KitNET aprende cómo se ve el tráfico "normal" durante sus fases de mapeo y entrenamiento. Una vez entrenado, calcula un **Error Cuadrático Medio (RMSE)**; si el error de reconstrucción es alto, significa que el paquete es anómalo y representa un posible ataque.

---

##  Sintaxis del Lenguaje (Lenguajes Formales)

Para interactuar con el motor estadístico de Kitsune y definir las reglas de firewall, desarrollamos un lenguaje formal propio con un analizador léxico y sintáctico a medida. El lenguaje utiliza una sintaxis coloquial, estructurada mediante indentación (espacios en blanco) similar a Python.

### Diccionario de Tokens

| Categoría | Sintaxis Personalizada | Equivalente | Descripción |
| :--- | :--- | :--- | :--- |
| **Control** | `armala` | `def` | Declara el inicio de una rutina o función. |
| **Control** | `tonces` | `:` | Delimitador de inicio de bloque. |
| **Control** | `retornala` | `return` | Retorna un valor al flujo principal. |
| **Decisión** | `aja_si` | `if` | Condicional principal. |
| **Decisión** | `o_entonce` | `elif` | Condicional alternativo. |
| **Decisión** | `ya_que_hpta` | `else` | Acción por defecto. |
| **Ciclos** | `para` | `for` | Estructura iterativa. |
| **Ciclos** | `en` | `in` | Recorre elementos capturados. |
| **Operador** | `igualito_con` | `=` | Asignación de variables. |
| **Operador** | `la_misma_vaina_que` | `==` | Comparación de igualdad. |
| **Operador** | `mas_pesao_que` | `>` | Comparación de superioridad. |
| **Lógica** | `Y` / `O` | `and` / `or` | Encadena múltiples condiciones lógicas. |
| **Lógica** | `no` | `not` | Niega estados booleanos (ej. `velda`, `embuste`). |

*(Para ver el diccionario completo de tokens y operadores, revisa el archivo `sintaxis.txt` en este repositorio).*

---

##  Reglas de Evaluación (Normativa del Proyecto)

El sistema evalúa las anomalías de red basándose en 15 reglas construidas con nuestro lenguaje formal, diseñadas para cumplir estrictamente con los lineamientos de la rúbrica de la asignatura:

**Reglas con una sola condición (Al menos 3):**

1. `aja_si` rmse_actual `mas_pesao_que` 0.8 `tonces` notificar_anomalia()
2. `aja_si` fase_entrenamiento `la_misma_vaina_que` `velda` `tonces` actualizar_pesos_red()
3. `aja_si` tasa_paquetes `mas_pesao_que` 5000 `tonces` activar_alerta_inundacion()
4. `aja_si` dispositivo_aislado `la_misma_vaina_que` `velda` `tonces` descartar_paquete()
5. `aja_si` rmse_actual `menor_que` 0.1 `tonces` marcar_trafico_benigno()
6. `aja_si` tasa_paquetes `la_misma_vaina_que` 0 `tonces` ignorar_procesamiento()

**Reglas con condiciones compuestas usando Y / O (Al menos 3):**

7. `aja_si` tamaño_paquete `mas_pesao_que 1500` Y puerto_destino `la_misma_vaina_que` 53 `tonces` registrar_posible_exfiltracion()
8. `aja_si` tasa_paquetes `mas_pesao_que 1000` O rmse_actual `mas_pesao_que` 0.9 `tonces` aislar_dispositivo_iot()
9. `aja_si` puerto_destino `la_misma_vaina_que` 22 Y rmse_actual `mas_pesao_que` 0.5 `tonces` bloquear_puerto_ssh()
10. `aja_si` puerto_destino `la_misma_vaina_que` 80 O puerto_destino `la_misma_vaina_que` 443 `tonces` permitir_trafico_web()

**Reglas que combinan tipos de datos distintos - Numérico + Booleano (Al menos 2):**

11. `aja_si` fase_entrenamiento `la_misma_vaina_que` embuste Y rmse_actual `mas_pesao_que` 0.85 `tonces` aplicar_microsegmentacion()
12. `aja_si` modo_estricto `la_misma_vaina_que velda` O tasa_paquetes `mas_pesao_que` 10000 `tonces` bloquear_ip_origen()
13. `aja_si` trafico_cifrado `la_misma_vaina_que` `embuste` Y puerto_destino `la_misma_vaina_que` 23 `tonces` alertar_conexion_telnet()
14. `aja_si` tamaño_paquete `menor_que` 64 Y fase_entrenamiento `la_misma_vaina_que` embuste `tonces` registrar_paquete_malformado()
15. `aja_si` ancho_banda_mbps `mas_pesao_que` 100 Y trafico_cifrado `la_misma_vaina_que` velda `tonces` limitar_ancho_banda()

---

##  Ejemplo de Uso y Aplicación

El siguiente script, escrito completamente en nuestra sintaxis personalizada, es el corazón de **IoT-Sentinel**. 

**¿Qué hace este código?** 
El script carga una captura de red e itera sobre cada paquete. Durante los primeros paquetes, entrena las capas de mapeo y anomalías de la red neuronal KitNET. Una vez que el sistema termina de aprender, entra en modo de evaluación: calcula el puntaje RMSE de cada paquete nuevo y lo envía a la rutina `evaluar_amenaza`. Allí, nuestro motor de reglas decide si clasifica el tráfico como benigno, si alerta sobre una inundación de red o si ejecuta una microsegmentación bloqueando la IP de origen.

```text
// ==========================================
// ARCHIVO: motor_kitsune_iot.ks
// ==========================================

limite_mapeo igualito_con 50000
limite_entrenamiento igualito_con 100000
contador_paquetes igualito_con 0
modo_entrenamiento igualito_con velda

armala evaluar_amenaza(rmse, tasa_paquetes, puerto, protocolo) tonces
    
    // Evaluando si el sistema ya terminó de aprender
    aja_si no (modo_entrenamiento la_misma_vaina_que velda) tonces
        
        // Bloqueo crítico combinando RMSE alto y puertos de administración
        aja_si rmse mas_pesao_que 0.85 Y (puerto la_misma_vaina_que 22 O puerto la_misma_vaina_que 23) tonces
            retornala "ALERTA_CRITICA_SSH_TELNET"
            
        // Detección de inundación de paquetes
        o_entonce rmse pesao_o_igualito_que 0.75 Y tasa_paquetes mas_pesao_que 5000 tonces
            retornala "ALERTA_INUNDACION"
            
        // Anomalía general en protocolos no esperados
        o_entonce protocolo no_cuadra_con "TCP" Y rmse mas_pesao_que 0.9 tonces
            retornala "ALERTA_ANOMALIA_DESCONOCIDA"
            
        ya_que_hpta tonces
            retornala "TRAFICO_BENIGNO"
            
    ya_que_hpta tonces
        retornala "SISTEMA_APRENDIENDO"


armala iniciar_deteccion(archivo_pcap) tonces
    
    extractor igualito_con instanciar_afterimage(archivo_pcap)
    red_kitnet igualito_con instanciar_kitnet()
    paquetes igualito_con leer_archivo(archivo_pcap)
    
    // Bucle principal procesando el tráfico de red
    para paquete en paquetes tonces
        
        contador_paquetes igualito_con contador_paquetes + 1
        vector_estadistico igualito_con extractor.obtener_caracteristicas(paquete)
        
        // Fase 1: Feature Mapper (FM)
        aja_si contador_paquetes menor_o_igualito_que limite_mapeo tonces
            red_kitnet.entrenar_capa_mapeo(vector_estadistico)
            
        // Fase 2: Anomaly Detector (AD)
        o_entonce contador_paquetes menor_o_igualito_que limite_entrenamiento tonces
            red_kitnet.entrenar_capa_anomalias(vector_estadistico)
            
        // Fase 3: Ejecución y Microsegmentación
        ya_que_hpta tonces
            modo_entrenamiento igualito_con embuste
            rmse_calculado igualito_con red_kitnet.ejecutar_evaluacion(vector_estadistico)
            estado igualito_con evaluar_amenaza(rmse_calculado, paquete.tasa, paquete.puerto, paquete.protocolo)
            
            aja_si estado no_cuadra_con "TRAFICO_BENIGNO" Y estado no_cuadra_con "SISTEMA_APRENDIENDO" tonces
                REGISTRAR_ALERTA("Intrusión detectada en paquete: " + contador_paquetes)
                bloquear_origen(paquete.ip_origen)
                
    retornala contador_paquetes
