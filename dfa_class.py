import json
import numpy as np
from os import system
import networkx as nx
import matplotlib.pyplot as plt

class DFA :
    alphabet=[]
    states =[]
    initial_state=""
    accepting_states =[]
    transitions=[[0,0,0]]
    str_test=''
    transition_exists = True
    cumple = True

 #--------------------------------------------------------------------------------------------------------------------------------------#        
    def ingreso_json(self):
        if(self.cumple!=True):
            print("Archivo no compatible con DFA")
        tmp = input("Nombre del archivo (.json): ")
        try:
            f= open(tmp ,"r")
            content = f.read()
            jsondecoded = json.loads(content)
            self.cumple = True
            print("")   
            print("Mostrando Alfabeto")
            for entity in jsondecoded["alphabet"]:
                if(entity=="E"):
                    print("No se permite ingresar E en Alfabeto")
                    break
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
                if(entity[1]=="E"):
                    print("Transicion con E no permitidas")
                    self.cumple=False
                    break
                self.transitions = np.append(self.transitions, [entity] , axis=0)
            self.transitions = np.delete(self.transitions , 0 , axis=0)
            for entity in jsondecoded["transitions"]:
                for x in self.transitions:
                    if(entity[0]==x[0]  and entity[1]==x[1] and entity[2]!= x[2]):
                        self.cumple=False
                        break
            print(self.transitions)    

            if(self.cumple!=True):
                system("cls")
                self.alphabet=[]
                self.states =[]
                self.initial_state=""
                self.accepting_states =[]
                self.transitions=[[0,0,0]]
                self.ingreso_json()
            else:
                print("Se Ingreso Correctamente")
        except:
            print("Archivo Invalido")
            system("cls")
            self.ingreso_json()
 #--------------------------------------------------------------------------------------------------------------------------------------#
    def evaluar(self):
        print("")
        tmp = input("Valor a evaluar: ")
        self.str_test=tmp
        current_state = self.initial_state
        transition_exists = True
        for char_index in range(len(self.str_test)):
            current_char = self.str_test[char_index]
            if current_char in self.alphabet:
                for x in self.transitions:
                    if(x[0] == current_state and x[1] == current_char):
                        transition_exists = True
                        break
                    else:
                        transition_exists = False 
                next_state=""
                for x in self.transitions:
                    if(x[0]== current_state and x[1]==current_char):
                        next_state=x[2]        
                print(current_state, current_char, next_state)
                current_state = next_state
            else:
                print("No existe en alfabeto")
                return

        if transition_exists and current_state in self.accepting_states:
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
        print(grafo.edges())
        nx.draw(grafo , with_labels=True)
        plt.tight_layout()
        plt.savefig("DFA.png", format="PNG")
        plt.show()
 #--------------------------------------------------------------------------------------------------------------------------------------#