# ==========================================
# Proyecto: Simulador de Automatas Finitos
# Autor: Angel Pereira
# Carrera: Ingeniería de Sistemas
# Lenguaje: Python
# ==========================================

import os

def dibujar_automata(estados, alfabeto, transiciones, estado_inicial, estados_finales):

    import networkx as nx
    import matplotlib.pyplot as plt

    grafo = nx.DiGraph()

    grafo.add_nodes_from(estados)

    etiquetas = {}

    for estado in estados:
        for simbolo in alfabeto:
            destino = transiciones[estado][simbolo]

            if (estado, destino) not in etiquetas:
                etiquetas[(estado, destino)] = []

            etiquetas[(estado, destino)].append(simbolo)

    for origen, destino in etiquetas:
        grafo.add_edge(origen, destino)

    # Organizar estados horizontalmente
    posiciones = {
        estado: (i * 2, 0)
        for i, estado in enumerate(estados)
    }

    plt.figure(figsize=(10, 5))

    # Dibujar estados normales
    nx.draw_networkx_nodes(
        grafo, posiciones,
        nodelist=[e for e in estados if e not in estados_finales],
        node_size=1800,
        node_color="white",
        edgecolors="black"
    )

    # Dibujar estados finales
    nx.draw_networkx_nodes(
        grafo, posiciones,
        nodelist=estados_finales,
        node_size=1800,
        node_color="white",
        edgecolors="black",
        linewidths=2
    )

    # Dibujar nombres de estados
    nx.draw_networkx_labels(
        grafo, posiciones,
        font_size=12
    )

    # Dibujar transiciones
    for (origen, destino), simbolos in etiquetas.items():

        if origen == destino:
            curva = 0.4
        else:
            curva = 0.15

        nx.draw_networkx_edges(
            grafo,
            posiciones,
            edgelist=[(origen, destino)],
            arrows=True,
            arrowsize=25,
            connectionstyle=f"arc3,rad={curva}"
        )

    # Etiquetas de transiciones
    nx.draw_networkx_edge_labels(
        grafo,
        posiciones,
        edge_labels={
            (origen, destino): ", ".join(simbolos)
            for (origen, destino), simbolos in etiquetas.items()
        },
        font_size=11
    )

    # Flecha del estado inicial
    x, y = posiciones[estado_inicial]

    plt.annotate(
        "",
        xy=(x - 0.35, y),
        xytext=(x - 0.9, y),
        arrowprops=dict(arrowstyle="->", lw=2)
    )

    plt.title("Grafo del Automata Finito")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def buscar_palabras(estados, alfabeto, transiciones, estado_inicial, estados_finales):
    palabras_reconocidas = []
    cola = [(estado_inicial, "")]

    while cola and len(palabras_reconocidas) < 5:  # Limitar la cantidad de palabras reconocidas
        estado_actual, palabra_actual = cola.pop(0)

        if estado_actual in estados_finales:
            palabras_reconocidas.append(palabra_actual)

        if len(palabra_actual) < 10:  # Limitar la longitud de las palabras generadas    
            for simbolo in alfabeto:
                estado_siguiente = transiciones[estado_actual][simbolo]
                cola.append((estado_siguiente, palabra_actual + simbolo))

    return palabras_reconocidas

def mostrar_recorrido(estados, alfabeto, transiciones, estado_inicial, estados_finales, palabra):
    estado_actual = estado_inicial
    recorrido = [estado_actual]

    for simbolo in palabra:
        if simbolo in alfabeto:
            estado_siguiente = transiciones[estado_actual][simbolo]
            recorrido.append(estado_siguiente)
            estado_actual = estado_siguiente
        else:
            print(f"El símbolo '{simbolo}' no pertenece al alfabeto.")
            return

    print("Recorrido del automata:", " -> ".join(recorrido))

automata_construido = False
while True:
    print("================================")
    print("   SIMULADOR DE AUTOMATAS FINITOS")
    print("================================")
    print("   Autor: Angel Pereira")
    print("================================")
    print("1. Construir automata")
    print("2. Mostrar palabras reconocidas")
    print("3. Probar una palabra")
    print("4. Salir") 

    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        print("Construyendo el automata...")

        estados = [estado.strip() for estado in input("Ingrese los estados separados por coma: ").split(",")]
        print("Estados ingresados:", estados)

        alfabeto = [simbolo.strip() for simbolo in input("Ingrese el alfabeto separado por coma: ").split(",")]
        print("Alfabeto ingresado:", alfabeto)
        transiciones = {}
        for estado in estados:
            transiciones[estado] = {}
            for simbolo in alfabeto:
                transicion = input(f"Ingrese el estado de transición desde {estado} con el símbolo '{simbolo}': ")
                transiciones[estado][simbolo] = transicion.strip()
        print("Transiciones ingresadas:", transiciones) 

        estado_inicial = input("Ingrese el estado inicial: ").strip()
        print("Estado inicial ingresado:", estado_inicial)  

        estados_finales = [estado.strip() for estado in input("Ingrese los estados finales separados por coma: ").split(",")]
        print("Estados finales ingresados:", estados_finales)

        print("\n ---DEFINICION FORMAL DEL AUTOMATA---")
        print("M = (Q, Σ, δ, q0, F)")
        print("Q =", estados)
        print("Σ =", alfabeto)
        print("δ =")
        for estado, transiciones_estado in transiciones.items():
            for simbolo, estado_siguiente in transiciones_estado.items():
                print(f"  δ({estado}, {simbolo}) = {estado_siguiente}")
        print("q0 =", estado_inicial)
        print("F =", estados_finales)

        print("\n --- TABLA DE TRANSICIONES ---")
        print("Estado\t", end="")
        for simbolo in alfabeto:
            print(f"{simbolo}\t", end="")
        print()

        for estado in estados:
            marca = ""
            if estado == estado_inicial:
                marca += "→"
            if estado in estados_finales:
                marca += "*"    

            print(f"{marca}{estado}\t", end="")
            for simbolo in alfabeto:
                estado_siguiente = transiciones[estado][simbolo]
                print(f"{estado_siguiente}\t", end="")
            print()



        automata_construido = True 
        print("Automata construido exitosamente.")
        dibujar_automata(estados, alfabeto, transiciones, estado_inicial, estados_finales)

        


    elif opcion == "2": 
        if automata_construido == False:
            print("Primero debe construir el automata.")
        else:
            print("Estados:", estados)
            print("Alfabeto:", alfabeto)
            print("Transiciones:", transiciones)
            print("Estado inicial:", estado_inicial)
            print("Estados finales:", estados_finales)

            palabras_reconocidas = buscar_palabras(estados, alfabeto, transiciones, estado_inicial, estados_finales)

            if palabras_reconocidas:
                print(f"se encontraron {len(palabras_reconocidas)} palabras reconocidas por el automata:")
                print("palabras reconocidas:", palabras_reconocidas)

                for palabra in palabras_reconocidas:
                    print("Palabra:", palabra if palabra else "ε (cadena vacía)")
                    mostrar_recorrido(estados, alfabeto, transiciones, estado_inicial, estados_finales, palabra)
                    print("--------------")
            else:
                print("se encontraron 0 palabras reconocidas por el automata.") 

    elif opcion == "3":
        if automata_construido == False:
            print("Primero debe construir el automata.")
        else:
            while True:
                palabra = input("Ingrese la palabra a probar (o 'salir' para regresar al menú): ")
                if palabra.lower() == "salir":
                    break
                estado_actual = estado_inicial
                print(f"Estado inicial: {estado_actual}")

                valido = True
                for posicion, simbolo in enumerate(palabra, start=1):
                    if simbolo in alfabeto:
                        estado_siguiente = transiciones[estado_actual][simbolo]
                        print(f"δ({estado_actual}, {simbolo}) = {estado_siguiente}")
                        estado_actual = estado_siguiente
                    else:
                        print(f"El símbolo '{simbolo}' en la posición {posicion} no pertenece al alfabeto.")
                        valido = False
                        break

                if valido:
                    if estado_actual in estados_finales:
                        print(f"La palabra '{palabra}' es reconocida por el automata.")
                    else:
                        print(f"La palabra '{palabra}' NO es reconocida por el automata.")

                else:
                    print(f"La palabra '{palabra}' NO es reconocida por el automata debido a símbolos inválidos.")        

    elif opcion == "4":
        print("Saliendo del programa...") 
        break

    
