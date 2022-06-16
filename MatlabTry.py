
from calendar import c

import numpy as np
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
from GalerkinFuntion import *
from GalerkinFunRect import *
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
from scipy.sparse import csr_matrix


def stima3(V):
    V


l = 0.6 #Distancia en x
#l=symbols('l')
w = 0.6 #Distancia en y
#w=symbols('w')
p = 2  #Divisiones en x
m = 2  #Divisiones en y

elemLength = l/p #Largo del elemento
elemWidth = w/m  #Ancho del elemento
tipoDeElemento = 'TRIANGULO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'
listaLadosConv=[True,True,False,False] #Lados i-j, j-m, m-n, n-i Lista con lados con conv


#Se genera la lista NL ("Node list") que contiene las coordenadas de cada nodo
#y EL("Element list") que contiene la lista de nodos de cada elemento
NL,EL = uniform_mesh(l, w, p, m, tipoDeElemento) # Generar malla
graph_mesh(tipoDeElemento,NL,EL) #Graficar malla
neumann=[]
dirichlet=[]
for i in range (0, len(NL)): #Lados i-j n-j con neumann
    if (NL[i][0]==0 or NL[i][1]==0):
        neumann.append(NL[i])

for i in range (0, len(NL)): #Lados j-m m-n con dirichlet
    if (NL[i][0]==w or NL[i][1]==l):
        dirichlet.append(NL[i])

neumann  = np.array(neumann)
dirichlet= np.array(dirichlet)

freeNode=[]
#Nodos lbres (Nodos interiores)
for i in range (0, len(EL)):
    if(NL[i][0]!=0 and NL[i][0]!=l and NL[i][1]!=0 and NL[i][1]!=w):
        freeNode.append(NL[i])

freeNode= np.array(freeNode)

A=csr_matrix(np.zeros((len(NL)))) #matriz vacia del tamaño de las listas 
B=csr_matrix(np.zeros(((len(NL)), 1))) #vector vacia del tamaño de las listas 

#Asembly
for i in range (0, len(EL)):
    stima3(EL[i])


print(freeNode)
print(neumann)
print(dirichlet)
print(NL)
print(EL)

