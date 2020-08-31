import os 
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from os import system
from lista_enlazada import Lista
from nodo import Nodo

class NFAe :
    alphabet=[]
    states =[]
    initial_state=""
    accepting_states =[]
    transitions=[[0,0,0]]
    str_test=''
    transition_exists = True
    new_states = Lista()
    new_fstates = Lista()
    new_transitions = Lista()
    tabla_trs = Lista()

 #--------------------------------------------------------------------------------------------------------------------------------------#
    def ingreso_json(self):
        tmp = input("Valor a Test (.json): ")
        try:
            f= open(tmp ,"r")
            content = f.read()
            jsondecoded = json.loads(content)

            print("")   
            print("Mostrando Alfabeto")
            for entity in jsondecoded["alphabet"]:
                self.alphabet= np.append(self.alphabet, entity)
            print(self.alphabet)

            print("")
            print("Mostrando Estados")
            for entity in jsondecoded["states"]:
                self.states= np.append(self.states, entity)
            print(self.states)

            print("")
            print("Mostrando Estado Inicial")
            for entity in jsondecoded["initial_state"]:
                self.initial_state += entity
            print(self.initial_state)

            print("")
            print("Mostrando Estados Finales")
            for entity in jsondecoded["accepting_states"]:
                self.accepting_states= np.append(self.accepting_states, entity)
            print(self.accepting_states)

            print("")
            print("Mostrando Transiciones")
            for entity in jsondecoded["transitions"]:
                self.transitions = np.append(self.transitions, [entity] , axis=0)
            self.transitions = np.delete(self.transitions , 0 , axis=0)
            print(self.transitions)    
        except:
            print("Archivo Invalido")
            system("cls")
            self.ingreso_json()
 #--------------------------------------------------------------------------------------------------------------------------------------#
    def convertir_NFAe_DFA(self):
        print("#-------------------------- Convirtiendo --------------------------------#")
        self.alphabet = np.delete(self.alphabet, 0)
        cerraduraE = []
        cerraduraD = []
        cerraduraEF=[]
        for al in self.alphabet:
            if(al!="E"):
                for es in self.states: 
                    cerraduraE = np.append(cerraduraE , [es])     
                    for tra in self.transitions:   
                        if(es == tra[0] and tra[1] == "E"):
                            cerraduraE = np.append(cerraduraE , [tra[2]])  
                                
                    for est in cerraduraE:
                        for trs in self.transitions:
                            if(est == trs[0] and trs[1]==al):
                                cerraduraD = np.append(cerraduraD , [trs[2]] , axis=0) 

                        for estad in cerraduraD:
                            if not estad in cerraduraEF:
                                cerraduraEF = np.append(cerraduraEF , [estad])     
                            for tran in self.transitions:   
                                if(estad == tran[0] and tran[1] == "E"):
                                    if not tran[2] in cerraduraEF:
                                        cerraduraEF = np.append(cerraduraEF , [tran[2]])

                        if (len(cerraduraEF)!=0):
                            if not self.new_states.buscar(cerraduraEF):
                                self.new_states.agregar(cerraduraEF)    
                            aux = list(cerraduraEF)
                            self.tabla_trs.agregar([[es] , [al] , aux])
                        cerraduraEF=[]
                
                    cerraduraD=[]
                    cerraduraE=[]
            else:
                print("")
        self.new_states.agregar([self.initial_state])
        listatmp=Lista()
        # ESTADOS FINALES NUEVOS 
        for x in self.accepting_states:
            listatmp = self.new_states.buscar_alter(x)
            i = listatmp.tamano()
            while (i >0):
                tmp = listatmp.pop()
                self.new_fstates.agregar(tmp)
                i=i-1
        #TRANSICIONES NUEVAS
        iterador=0
        tamano=self.tabla_trs.tamano()
        lista_aux=self.tabla_trs.devolverLista()
        self.tabla_trs.imprimir()
        while(iterador< tamano):
            tmp = lista_aux.pop()
            aux = np.array(tmp , dtype=object)
            if(len(tmp[2])!=0) and  not(self.new_transitions.buscar(aux)):
                aux = np.array(tmp[0])
                if(self.new_states.buscar(aux)):
                    self.new_transitions.agregar(tmp)
            iterador= iterador+1
        self.new_transitions.imprimir() 
        lista_aux = self.new_transitions.devolverLista()
        iterador=0
        tamano=self.new_transitions.tamano()
        while(iterador< tamano):
            tmp = lista_aux.pop()
            aux = np.array(tmp , dtype=object)
            aux = np.array(aux[2])
            if not(self.new_transitions.buscar_uno_en_elemento(aux ,0)):
                if(len(aux)>1):
                    arr = [] 
                    for al in self.alphabet:
                        if not(al == "E"):
                            for y in aux:
                                for x in self.transitions:
                                    if(x[0]== y) and (x[1] == al):
                                        arr = np.append(arr , x[2])
                            aux_tmp = [ list(aux) , al , list(arr)]
                            if not(len(aux_tmp[2])==0) and self.new_states.buscarREGEX(aux_tmp[2]):
                                self.new_transitions.agregar(aux_tmp)        
                            arr=[]
                else:
                    for al in self.alphabet:
                        if not(al=="E"):
                            for x in self.transitions:
                                if(x[0]== aux) and (x[1] == al):
                                    aux_tmp = [ aux , al , x[2]]
                                    if not(len(aux_tmp[2])==0) and self.new_states.buscarREGEX(x[2]):
                                        self.new_transitions.agregar(aux_tmp)        
            iterador= iterador+1
        print("#-------------------------- Graficando --------------------------------#")
        print("")
        print("Alphabet: ",self.alphabet)
        print("States: ")
        self.new_states.imprimir()
        print("Initial State: ", self.initial_state)
        print("Final States: ")
        self.new_fstates.imprimir()
        print("\nTransitions:")
        self.new_transitions.imprimir()
        grafo = nx.MultiDiGraph()
        grafo.add_node(self.initial_state)
        tam = self.new_states.tamano()
        lista_aux = self.new_states.devolverLista()
        while(tam>0):
            x= lista_aux.pop()
            aux = np.append(aux ,x)
            if not((aux == [self.initial_state]).all()):
                listToStr = ' '.join(x)
                grafo.add_node(listToStr)
            tam = tam - 1
        tam = self.new_transitions.tamano()
        lista_aux = self.new_transitions.devolverLista()
        while(tam>0):
            x= lista_aux.pop()
            s = ' '.join(x[0])
            d = ' '.join(x[2])
            a = ' '.join(x[1])
            grafo.add_edge(s, d, element=a)
            tam = tam - 1
        nx.draw(grafo , with_labels=True)
        plt.tight_layout()
        plt.savefig("ConversionNFAe_DFA.png", format="PNG")
        plt.show()
        print("#-------------------------- Evaluando --------------------------------#")
        print("")
        tmp = input("Valor a evaluar: ")
        self.str_test = tmp
        current_state= np.array(self.initial_state)
        for char_index in range(len(self.str_test)):    
            lista_aux = self.new_transitions.devolverLista()
            current_char = self.str_test[char_index]
            if current_char in self.alphabet:
                tam = self.new_transitions.tamano()
                while (tam>0):
                    x = list(lista_aux.pop())
                    aux= np.array(x[0])
                    aux3 = np.array(current_char)
                    current_state=np.array(current_state)
                    if ((aux==current_state).all()) and (x[1] == aux3):
                        self.transition_exists = True
                        break
                    else:
                        self.transition_exists = False
                    tam = tam -1 
                lista_aux = self.new_transitions.devolverLista()        
                tam = self.new_transitions.tamano()
                while (tam>0):
                    x = list(lista_aux.pop())
                    aux= np.array(x[0])
                    aux2 = np.array(x[2])
                    aux3 = np.array(current_char)
                    if((aux == current_state ).all() and x[1] == aux3):
                        next_state = np.array(aux2) 
                        break
                    tam = tam-1
                print(current_state, current_char, next_state)
                current_state = next_state
            else:
                print("No existe en el alphabeto")
                return
        current_state= np.array(current_state)
        if (self.transition_exists == True) and (self.new_fstates.buscar(current_state)):
            print("Pertenece a L(M)")
        else:
            print("No pertenece a L(M)")
 #--------------------------------------------------------------------------------------------------------------------------------------#   
    def graficar(self):
        print("")
        print("Alphabet: ",self.alphabet)
        print("States: " , self.states)
        print("Initial State: ", self.initial_state)
        print("Final States: ", self.accepting_states)
        print("Transitions: \n", self.transitions)
        grafo = nx.MultiDiGraph()
        
        grafo.add_node(self.initial_state)

        for x in self.states:
            if(x != self.initial_state):
                grafo.add_node(x)

        for x in self.transitions:
            grafo.add_edge(x[0], x[2], element=x[1])
        
        nx.draw(grafo , with_labels=True)
        plt.tight_layout()
        plt.savefig("NFAe.png", format="PNG")
        plt.show()
 #--------------------------------------------------------------------------------------------------------------------------------------#