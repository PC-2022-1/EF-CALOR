
from re import X
from tkinter import Y
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import seaborn as sns
from matplotlib import cm


#Definicion de funciones usadas en heat.py
#Funciones stima3 y stima4 para generar la matriz de esfuerzo (triangulos y cuadrados)
#Funciones f, g y u_d
#Y funciones para graficas en 2d y 3d (3er eje temperatura)

def stima3(vertices): #Genera la matriz de esfuerzos para un elemento tipo triangular
    d  = np.size(vertices, 1) 

    G1 = np.vstack((np.ones((1,d+1)),vertices.transpose()))  
    G2 = np.vstack((np.zeros((1,d)),np.eye(d)))
    G = np.linalg.solve(G1, G2)

    MM=np.linalg.det(np.vstack((np.ones((1,d+1)),vertices.transpose())))*G
    MM=np.dot(MM,G.transpose())
    M=MM / 2   

    return M

def stima4(vertices): #Genera la matriz de esfuerzos para un elemento tipo cuadrado

    D_phi = np.vstack((vertices[1,:] - vertices[0,:], vertices[3,:] - vertices[0,:]))
    D_phiTrans = D_phi.transpose()
   
    B = np.linalg.inv (D_phiTrans @ D_phi )

    C1matrix= [[[2, -2],[-2,2]], [[3, 0],[0,-3]],  [[2, 1],[1,2]] ]

    C1 = np.array(C1matrix[0]) * B[0,0] + np.array(C1matrix[1]) * B[0,1] + np.array(C1matrix[2]) * B[1,1] 

    C2matrix= [[[-1, 1],[1,-1]], [[-3, 0],[0,3]],  [[-1, -2],[-2,-1]] ]
    C2 = np.matrix(C2matrix[0]) * B[0,0] + np.matrix(C2matrix[1]) * B[0,1] + np.matrix(C2matrix[2]) * B[1,1] 

    M = (np.linalg.det(D_phiTrans) * np.vstack((np.hstack((C1, C2)), np.hstack((C2, C1))))) / 6
    return M


def f(u, fun): 
    w = u.copy()
    w = w[0]+w[-1]  #Argumento que entra a la funcion.
    value = fun(w)
    return value

def g(u, fun): #Valor derivada u en fronteras neumann
    w = u.copy()
    w = w[0]+w[-1]  #Argumento que entra a la funcion.
    value = fun(w)
    return value

def u_d(u, fun):  #Valor en las fronteras dirichlet
    w = u.copy()
    # v=w[:,-1]
    # ww=w[:,0]
    # w=(v**2)+(ww**2)
    w = np.sum(w, axis=1)
    w = w.reshape((len(u), 1))
    value = fun(w)
    return value

def show(coordinates, u, tipodeElemento, p): #Para un elemento tipo triangular genera una grafica 3d, para un elemento tipo cuadrado genera una grafica 2d
    
    matrixCalor = []
    v =u.copy()
    while v.size > 0:
        matrixCalor.append(v[:p+1])  #Matriz en orden para graficar en 2d con sns
        v = v[p+1:]
    if tipodeElemento == "CUADRADO":
        ax = sns.heatmap(matrixCalor, linewidth=0.01,cmap="Spectral_r",  cbar_kws={'label': 'Temperatura °C'})
        ax.invert_yaxis()
        plt.show()    
    else:
        fig = plt.figure()
        ax = fig.add_subplot(projection= '3d')
        X, Y = coordinates[:, 0], coordinates[:, -1]
        result = ax.plot_trisurf(X, Y, u, linewidth=0.2,  cmap=plt.cm.Spectral_r)
        fig.colorbar(result)
        plt.show()
    return matrixCalor


def neumannOrDirichlet(condicionesDeFrontera, EL, NL, w, l):
    # Se generan listas que contienen condiciones 
    # lista condicionesDeFrontera: Lado inferior, derecho, superior, izquierdo 
    # Si es True es Neumann, si es False es dirichlet
    neumann=[]
    dirichlet=[]
    listaAuxX=[]
    listaAuxY=[]
    listaAuxX_D=[]
    listaAuxY_D=[]

    #Recorre cada elemento y cada nodo del elemento, verifica si se encuentra en una frontera
    #Y luego el tipo de condicion de la misma. 
    #Deacuerdo a eso se guarda en una lista diferente que se retorna al final

    #Se usan listas auxiliares para guardar dos nodos por elemento en la lista

    for element in EL:
        for nodo in element:
            if (NL[nodo-1][0]==0): 
                if (condicionesDeFrontera[0] == True):
                    listaAuxX.append(nodo)
                else: listaAuxX_D.append(nodo)
            if (NL[nodo-1][1]==0): 
                if (condicionesDeFrontera[3] == True):
                    listaAuxY.append(nodo)
                else: listaAuxY_D.append(nodo)
            if (NL[nodo-1][0]==l):
                if (condicionesDeFrontera[1] == True):
                    listaAuxX.append(nodo)
                else: listaAuxX_D.append(nodo)
            if (NL[nodo-1][1]==w): 
                if(condicionesDeFrontera[2] == True):
                    listaAuxY.append(nodo) 
                else: listaAuxY_D.append(nodo)

        if listaAuxX and len(listaAuxX)==2:
            neumann += [listaAuxX.copy()]
        if listaAuxX_D and len(listaAuxX_D)==2:
            dirichlet += [listaAuxX_D.copy()]
        listaAuxX.clear()
        listaAuxX_D.clear()
        if listaAuxY and len(listaAuxY)==2:
            neumann += [listaAuxY.copy()]
        if listaAuxY_D and len(listaAuxY_D)==2:
            dirichlet += [listaAuxY_D.copy()]
        listaAuxY.clear()
        listaAuxY_D.clear()

    return np.array(neumann), np.array(dirichlet) 