import sys
from tokens import ErrorDeLenguaje
from lexer import tokenizar_monda
from parser import Parser
from interprete import Interprete

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.txt>")
        return

    ruta_archivo = sys.argv[1]

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return

    try:
        lista_tokens = tokenizar_monda(texto)#tokens 
        parser = Parser(lista_tokens)#lista total de tokens 
        arbol_programa = parser.programa()# entregamos tokens al parser
        
        interprete = Interprete() # inicializamos el interprete
        interprete.ejecutar_programa(arbol_programa)# NODOS al interprete

    except ErrorDeLenguaje as e:
        print(f"\n{e}") 
        
        # --- OBLIGATORIO 4: PUNTERO DE ERROR ---
        lineas_texto = texto.split('\n')
        # Validamos que la línea del error exista en el archivo
        if 1 <= e.linea <= len(lineas_texto):
            linea_error = lineas_texto[e.linea - 1]
            print(linea_error)
            # Imprime espacios hasta llegar a la columna y coloca el ^
            print(" " * (e.columna - 1) + "^")
            
        print(f"línea = {e.linea}, columna = {e.columna}")

if __name__ == "__main__":
    main()