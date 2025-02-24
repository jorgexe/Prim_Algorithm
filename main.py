import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Función para determinar el inicio del algoritmo de Prim, basado en la arista de menor peso en el grafo
def min_edge(graph):
    min_weight = float('inf') # almacenar el peso mínimo encontrado hasta ahora.
    min_vertex = None # almacenar el nodo asociado con la arista de menor peso.
    for vertex in graph:
        for neighbor, weight in graph[vertex]:
            if weight < min_weight:
                min_weight = weight
                min_vertex = vertex
    return min_vertex

def prim(graph, start):
    visited = set()  # Visited: Un conjunto para mantener un registro de los nodos visitados durante el proceso.
    mst = []  # Una lista que almacenará las aristas del Árbol de Expansión Mínima (MST, por sus siglas en inglés).
    pq = [(0, start, None)]  # Una cola de prioridad (implementada como una lista de tuplas) que se utilizará
    # para almacenar las aristas pendientes de explorar. Cada elemento de la cola tiene la forma
    """(weight, vertex, parent)"""

    # Definir las posiciones de los nodos manualmente, aproximando el mapa original
    pos = {
        'A': (5, 16), 'B': (12, 16), 'C': (23, 14), 'D': (4, 13), 'E': (8, 13),
        'F': (12, 13), 'G': (16, 13), 'H': (25, 10), 'I': (10, 11), 'J': (13, 8),
        'K': (17, 9), 'L': (19, 10), 'M': (18, 6), 'N': (21, 5), 'O': (27, 5),
        'P': (5, 7), 'Q': (9, 5), 'R': (11, 2), 'S': (17, 4), 'T': (19, 3)
    }

    # Variable G para dibujar el arbol
    G = nx.Graph() # crear objeto de grafo vacío
    for vertex in graph:
        G.add_node(vertex, pos=pos[vertex])
    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(vertex, neighbor, weight=weight, color='k')

    # Dibujar el grafo completo inicialmente
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
    plt.pause(2)

    while pq:
        weight, vertex, parent = heapq.heappop(pq)  # Utiliza heapq.heappop() para extraer el elemento con el
        # peso mínimo de la cola de prioridad pq.
        if vertex in visited:
            continue

        visited.add(vertex)

        if parent is not None:
            mst.append((parent, vertex, weight))  # se encarga de agregar la arista seleccionada al Árbol de Expansión Mínima (MST).

            # Resaltar la arista seleccionada en rojo
            G.edges[parent, vertex]['color'] = 'r'

            # Dibujar el grafo actualizado
            plt.clf()
            nx.draw(G, pos, with_labels=True, edge_color=[e[2]['color'] for e in G.edges(data=True)])
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})

            # Modificar el grosor de las lineas rojas para que resalten más
            mst_edges = [(edge[0], edge[1]) for edge in mst]
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3.0, alpha=0.8,
                                   edge_color='r')  # Aumentar el ancho de las líneas rojas
            plt.pause(0.7)

        """Esta parte del código se encarga de explorar las aristas conectadas al nodo actual (vertex) en el grafo y 
        agregar las aristas no visitadas a la cola de prioridad pq, manteniendo la propiedad de que la arista con el 
        peso mínimo se procesa primero."""

        for neighbor, weight in graph[vertex]: # itera sobre los vecinos del vértice actual (vertex) en el grafo original.
            if neighbor not in visited:  # Verifica si el nodo vecino no ha sido visitado previamente.
                # Esto asegura que no se agreguen aristas que ya están en el MST, evitando ciclos.
                heapq.heappush(pq, (weight, neighbor, vertex)) # Agrega la arista a la cola de prioridad pq

    return mst

graph = {
    'A': [('B', 100), ('D', 85)],
    'B': [('A', 100), ('C', 100), ('E', 40), ('F', 45), ('G', 70)],
    'C': [('B', 100), ('H', 60), ('G', 55)],
    'D': [('A', 85), ('P', 10), ('A', 30)],
    'E': [('B', 40), ('I', 10)],
    'F': [('B', 45), ('J', 55)],
    'G': [('B', 70), ('C', 55), ('L', 20), ('K', 15)],
    'H': [('C', 60), ('O', 70), ('N', 85), ('L', 40)],
    'I': [('E', 10), ('J', 60), ('P', 60)],
    'J': [('F', 55), ('I', 60), ('K', 80), ('Q', 45)],
    'K': [('G', 15), ('J', 80), ('M', 60)],
    'L': [('G', 20), ('H', 40), ('M', 50)],
    'M': [('K', 60), ('S', 2), ('L', 50)],
    'N': [('H', 85), ('O', 105), ('O', 120), ('T', 60), ('S', 55)],
    'O': [('T', 195), ('N', 105), ('N', 120), ('H', 70)],
    'P': [('D', 50), ('I', 90), ('R', 205)],
    'Q': [('J', 45), ('R', 5)],
    'R': [('T', 230), ('Q', 5), ('P', 205)],
    'S': [('M', 2), ('N', 55), ('T', 25)],
    'T': [('N', 60), ('S', 25), ('O', 195)]
}

start = min_edge(graph)  # Punto de inicio en el grafo
mst = prim(graph, start)  # resultado

print("Árbol de Expansión Mínima:")
for edge in mst:
    print(f"{edge[0]} -- {edge[1]} (peso: {edge[2]})")

plt.show()
