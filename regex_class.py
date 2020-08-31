import os
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from os import system
from nfae_class import NFAe
from lista_enlazada import Lista
from nodo import Nodo

class Regex :
    expre= ""
    it=1
    alphabet=[]
    states=[]
    initial_state="q0"
    accepting_states=[]
    operations=[]
    transitions=[[0,0,0,0]]#[estadosaliente , elemento alfabeto , estado destino , flag inicial]
    transition_exist=True
    new_states = Lista()
    new_fstates = Lista()
    new_transitions = Lista()
    tabla_trs = Lista()
    
    def ingreso_json(self):
        tmp = input("Valor a Test (.json): ")
        try:
            f= open(tmp ,"r")
            content = f.read()
            jsondecoded = json.loads(content)
            print("")   
            print("Mostrando Expresion")
            for entity in jsondecoded["expresion"]:
                self.expre += entity
            print(self.expre)
            
        except:
            system("cls")
            self.ingreso_json()

    def conversion_regex_NFAe(self):
        ini= 0
        tmpFinales=[]
        est_i=""
        est_f=""
        lastC=""
        for char in self.expre:
            if char!=' ': 
                if char =='|':
                    self.operations = np.append(self.operations , [char])
                    est_f= "q"+ str(self.it)
                    tmpFinales = np.append(tmpFinales , est_f)
                    self.it+=1
                    ini=0
                elif char=='+':
                    self.operations = np.append(self.operations , [char])
                    trns = [est_f , 'E' , est_i,ini]
                    self.transitions = np.append(self.transitions , [trns] , axis=0)
                elif char=='*':
                    est_f= "q"+ str(self.it)
                    self.it-=1
                    self.operations = np.append(self.operations , [char])
                    auxInt= len(self.transitions)
                    if(self.transitions[auxInt-1][3]=='0'):
                        ini=0                    
                    self.transitions = np.delete(self.transitions, (auxInt-1), axis=0)
                    trns = [est_i , lastC , est_i,ini]
                    self.transitions = np.append(self.transitions , [trns] , axis=0)
                    self.states = np.delete(self.states , (len(self.states)-1), axis=0)
                    ini=1
                    
                else:
                    if char not in self.alphabet:
                        self.alphabet = np.append(self.alphabet , [char])
                    est_i= "q"+ str(self.it)                      
                    self.it+=1
                    est_f= "q"+ str(self.it) 
                    trns = [est_i , char , est_f,ini]
                    lastC=char
                    self.transitions = np.append(self.transitions , [trns] , axis=0)
                    ini=1

                    if est_i not in self.states:
                        self.states = np.append(self.states , [est_i] , axis=0)
                    if est_f not in self.states:
                        self.states = np.append(self.states , [est_f] , axis=0)
        est_i= "q0" 
        est_f= "q"+ str(self.it)           
        tmpFinales = np.append(tmpFinales , est_f)           
        self.transitions = np.delete(self.transitions , 0 , axis=0)
        for trs in self.transitions:
            aux = list(trs)
            if aux[3]=='0':
                trns = [est_i , 'E' , aux[0] , 1 ]
                self.transitions = np.append(self.transitions , [trns] , axis=0)

        if '|' in self.operations:
            self.it+=1
            est_f= "q"+ str(self.it)
            for st in tmpFinales:
                trns = [st , 'E' , est_f, 1]
                self.transitions = np.append(self.transitions , [trns] , axis=0)
        else:
            est_i= "q"+ str(self.it)
            self.it+=1
            est_f= "q"+ str(self.it)
            trns = [tmpFinales[0] , 'E' , est_f, 1]
            self.transitions = np.append(self.transitions , [trns] , axis=0)
      
        self.states = np.append(self.states , [est_f] , axis=0)
        self.states = np.insert(self.states , 0, ["q0"])
        self.alphabet = np.insert(self.alphabet, 0 , ['E'])
        self.transitions = np.delete(self.transitions , 3 , axis=1)
        self.accepting_states = np.array([est_f])

        print("")   
        print("Mostrando Alfabeto")
        print(self.alphabet)
        print("Mostrando Estados")
        print(self.states)
        print("Mostrando Estado Inicial")
        print(self.initial_state)
        print("Mostrando Estados Finales")
        print(self.accepting_states)
        print("Mostrando Operaciones")
        print(self.operations) 
        print("Transiciones :")
        print(self.transitions)
        
        grafo = nx.MultiDiGraph()
        grafo.add_node(self.initial_state)
        for x in self.states:
            if(x != self.initial_state):
                grafo.add_node(x)

        for x in self.transitions:
            grafo.add_edge(x[0], x[2], element=x[1])
        
        nx.draw(grafo , with_labels=True)
        plt.tight_layout()
        plt.savefig("REGEX_NFAE.png", format="PNG")
        plt.show()

    def conversion_nfae_dfa(self):
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
                        if not(len(cerraduraEF) == 0):
                            if(self.new_states.buscarREGEX(cerraduraEF)==False):
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
        while(iterador< tamano):
            tmp = lista_aux.pop()
            aux = np.array(tmp,dtype=object)
            if not(len(tmp[2])==0) and  not(self.new_transitions.buscar(aux)):
                aux = np.array(tmp[0])
                if(self.new_states.buscar(aux)):
                    self.new_transitions.agregar(tmp)
            iterador= iterador+1
        lista_aux = self.new_transitions.devolverLista()
        iterador=0
        tamano=self.new_transitions.tamano()
        while(iterador< tamano):
            tmp = lista_aux.pop()
            aux = np.array(tmp , dtype=object)
            aux = np.array(aux[2])
            if not(self.new_transitions.buscar_uno_en_elementoREGEX(aux ,0)):
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
    
        print("----------------------------")
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
        if (self.transition_exists == True) and (self.new_fstates.buscarREGEX(current_state)):
            print("Pertenece a L(M)")
        else:
            print("No pertenece a L(M)")