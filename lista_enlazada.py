from nodo import Nodo
import numpy as np

class Lista:

    def __init__(self):
        self.cabeza = None

    def estaVacia(self):
        return self.cabeza == None

    def agregar(self,item):
        temp = Nodo(item)
        temp.asignarSiguiente(self.cabeza)
        self.cabeza = temp
    
    def tamano(self):
        actual = self.cabeza
        contador = 0
        while actual != None:
            contador = contador + 1
            actual = actual.obtenerSiguiente()
        return contador
    
    def pop(self):
        if (self.cabeza == None):
            return None
        tmp = self.cabeza
        self.cabeza = tmp.obtenerSiguiente()
        return tmp.obtenerDato()

    def imprimir(self):
        actual = self.cabeza
        while actual != None:
            print(actual.obtenerDato())
            actual= actual.obtenerSiguiente() 
    
    def buscar(self,item):
        actual = self.cabeza
        encontrado = False
        while actual != None and not encontrado:
            if (actual.obtenerDato() == item).all():
                encontrado = True
            else:
                actual = actual.obtenerSiguiente()
        return encontrado
     
    def buscarREGEX(self,item):
        actual = self.cabeza
        encontrado = False
        while actual != None and not encontrado:
            if (list(actual.obtenerDato()) == list(item)):
                encontrado = True
            else:
                actual = actual.obtenerSiguiente()
        return encontrado

    def buscar_alter(self,item):
        actual = self.cabeza
        lista = Lista()
        tmp = []
        while actual != None:
            tmp = actual.obtenerDato()
            for x in tmp:
                if(x == item):
                    lista.agregar(actual.obtenerDato())
            actual= actual.obtenerSiguiente()
        return lista

    def buscar_uno_en_elemento(self,item ,i):
        actual = self.cabeza
        encontrado = False
        while (actual != None and not encontrado):
            aux = actual.obtenerDato()
            if (aux[i] == item).all():
                encontrado = True
            else:
                actual = actual.obtenerSiguiente()
        return encontrado
    
    def buscar_uno_en_elementoREGEX(self,item ,i):
        actual = self.cabeza
        encontrado = False
        while (actual != None and not encontrado):
            aux = actual.obtenerDato()
            if (list(aux[i]) == list(item)):
                encontrado = True
            else:
                actual = actual.obtenerSiguiente()
        return encontrado
        
    def devolverLista(self):
        actual = self.cabeza
        lista = Lista()
        while( actual !=  None):
            lista.agregar(actual.obtenerDato())
            actual= actual.obtenerSiguiente()
        return lista