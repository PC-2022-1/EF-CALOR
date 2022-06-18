
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

# def stima3(nodosElemento,newNL ):
#     vertices=[]
#     for element in nodosElemento:
#         vertices.append(newNL[element-1]) 
    
#     vertices=np.matrix(vertices)
#     print(vertices)
#     d=3
#     # vertices = np.insert(vertices, 0, col, axis=1)
#     # vertices = np.insert(vertices, 0, row, axis=0)
#     M1=np.vstack((np.ones((1,d+1)),vertices.transpose()))   
#     print(M1)
#     A=np.zeros((1,d))
#     B=np.eye(d)
#     M2=np.vstack((A,B))
#     #print(M2)
#     print(M2)
#     G=np.linalg.solve((M1),(M2))
#     print(G)
#     #print(G)
#     a=[1,2,3]
#     # MM=np.linalg.det(np.vstack((np.ones((1,d+1)),vertices.transpose())))
#     MM=np.linalg.det(np.vstack((np.ones((1,d+1)),vertices.transpose())))*G
#     MM=np.dot(MM,G.transpose())
#     M=MM/6    
#     return M



def stima3(vertices):
    d  = np.size(vertices, 1)

    G1 = np.vstack((np.ones((1,d+1)),vertices.transpose()))  
    G2 = np.vstack((np.zeros((1,d)),np.eye(d)))
    G = np.linalg.solve(G1, G2)

    MM=np.linalg.det(np.vstack((np.ones((1,d+1)),vertices.transpose())))*G
    MM=np.dot(MM,G.transpose())
    M=MM / np.prod([i for i in range (0,d)])    

    return M

def stima4(vertices):

    D_phi = np.array([[vertices[1,:] - vertices[0,:]], [vertices[3,:] - vertices[0,:]]])
    D_phiTrans =D_phi.transpose()
   
    B = np.linalg.inv (np.dot (D_phi, D_phiTrans) )

    C1matrix= [[[2, -2],[-2,2]], [[3, 0],[0,-3]],  [[2, 1],[1,2]] ]
    C1 = np.matrix(C1matrix[0]) * B[0,0] + np.matrix(C1matrix[1]) * B[0,1] + np.matrix(C1matrix[3]) * B[1,1] 

    C2matrix= [[[-1, 1],[1,-1]], [[-3, 0],[0,3]],  [[-1, -2],[-2,-1]] ]
    C2 = np.matrix(C2matrix[0]) * B[0,0] + np.matrix(C2matrix[1]) * B[0,1] + np.matrix(C2matrix[3]) * B[1,1] 

    M = (np.linalg.det(D_phiTrans) * np.matrix ([C1, C2], [C2, C1])) / 6
    return M


def f(u): 
    value = np.ones(np.size(u, 0), 0)
    return value

def g(u): 
    value = np.zeros(np.size(u, 0), 0)
    return value

def u_d(u): 
    value = np.zeros(np.size(u, 0), 0)
    return value


l = 0.6 #Distancia en x
#l=symbols('l')
w = 0.6 #Distancia en y
#w=symbols('w')
p = 2  #Divisiones en x
m = 2  #Divisiones en y

elemLength = l/p #Largo del elemento
elemWidth = w/m  #Ancho del elemento
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'
listaLadosConv=[True,True,False,False] #Lados i-j, j-m, m-n, n-i Lista con lados con conv

#Se genera la lista NL ("Node list") que contiene las coordenadas de cada nodo
#y EL("Element list") que contiene la lista de nodos de cada elemento
NL,EL = uniform_mesh(l, w, p, m, tipoDeElemento) # Generar malla
graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

#Lados i-j i-n condiciones neumann 
#Lados j-m m-n condiciones dirichlet 
neumann=[]
dirichlet=[]
listaAuxX=[]
listaAuxY=[]
for element in EL:
    for nodo in element:
        if (NL[nodo-1][0]==0): 
            listaAuxX.append(nodo)
        if (NL[nodo-1][1]==0): 
            listaAuxY.append(nodo)
    if listaAuxX:
        neumann += [listaAuxX.copy()]
    listaAuxX.clear()
    if listaAuxY:
        neumann += [listaAuxY.copy()]
    listaAuxY.clear()

for element in EL:
    for nodo in element:
        if (NL[nodo-1][0]==l): 
            listaAuxX.append(nodo)
        if (NL[nodo-1][1]==w): 
            listaAuxY.append(nodo)
    if listaAuxX:
        dirichlet += [listaAuxX.copy()]
    listaAuxX.clear()
    if listaAuxY:
        dirichlet += [listaAuxY.copy()]
    listaAuxY.clear()


# for i in range (0, len(NL)): #Lados i-j n-j con neumann
#     if (NL[i][0]==0 or NL[i][1]==0):
#         neumann.append(EL[i])

# for i in range (0, len(NL)): #Lados j-m m-n con dirichlet
#     if (NL[i][0]==w or NL[i][1]==l):
#         dirichlet.append(EL[i])

neumann   = np.array(neumann)
dirichlet = np.array(dirichlet)

freeNode=[]
#Nodos lbres (Nodos interiores)
for i in range (0, len(EL)):
    if(NL[i][0]!=0 and NL[i][0]!=l and NL[i][1]!=0 and NL[i][1]!=w):
        freeNode.append(NL[i])

freeNode= np.array(freeNode)

A=csr_matrix(np.zeros((len(NL)))) #matriz vacia del tamaño de las listas 
B=csr_matrix(np.zeros(((len(NL)), 1))) #vector vacia del tamaño de las listas 

#Asembly

#Nueva element list
col1=[]
for i in range (1, len(EL)+1):
    col1.append(i)
newEl=np.insert(EL, 0, col1, axis=1) #"element3"

col2=[]
for i in range (1, len(NL)+1):
    col2.append(i)

newNL=np.insert(NL, 0, col2, axis=1) #"coordinates"

for i in range (1, len(EL)):
    #col=EL[i]
    #row=[i+1,NL[i][0],NL[i][1]] #En vez de 1 se pone el número del elemento y la coordenada del nodo que coincide con el valor del elemento
    #A=(stima3(NL[EL[i]-1], col, row), (newEl[i], newEl[i]))
    #A[newEl[i]][newEl[i]]= A[newEl[i]][newEl[i]] + stima3(NL[EL[i]-1], col, row)
    #stima3(NL[EL[i]-1], col, row)
    #(stima3(newEl[i],newNL))
    
    EL


#print(newEl[0])
print("-----------")
print(neumann)
print(dirichlet)
print("-----------")
# print(freeNode)
# print(neumann)
# print(dirichlet)
# print(NL)
# print(EL)

