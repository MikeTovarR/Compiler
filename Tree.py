class Node:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []
    
    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

class Tree:
    def __init__(self, raiz=None):
        self.raiz = raiz

    def agregar_hijo_a_raiz(self, valor):
        if self.raiz is not None:
            nuevo_hijo = Node(valor)
            self.raiz.agregar_hijo(nuevo_hijo)
        else:
            raise ValueError("El árbol no tiene una raíz definida.")

    def pre_orden(self, nodo=None):
        if nodo is None:
            nodo = self.raiz

        if nodo:
            print(nodo.valor, end=' ')
            for hijo in nodo.hijos:
                self.pre_orden(hijo)

