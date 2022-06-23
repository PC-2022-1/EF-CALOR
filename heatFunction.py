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

def stima3(vertices):
    d  = np.size(vertices, 1)

    G1 = np.vstack((np.ones((1,d+1)),vertices.transpose()))  
    G2 = np.vstack((np.zeros((1,d)),np.eye(d)))
    G = np.linalg.solve(G1, G2)

    MM=np.linalg.det(np.vstack((np.ones((1,d+1)),vertices.transpose())))*G
    MM=np.dot(MM,G.transpose())
    M=MM / 2   

    return M

def stima4(vertices):

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
    # w = w[0]+w[-1] # Tipo de argumento
    value = fun(w)
    return value

def g(u, fun):
    w = u.copy()
    # w = w[0]+w[-1] # Tipo de argumento
    value = fun(w)
    return value

def u_d(u, fun):
    w = u.copy()
    # v=w[:,-1]
    # ww=w[:,0]
    # w=(v**2)+(ww**2)
    w = np.sum(w, axis=1)
    w = w.reshape((len(u), 1))
    value = fun(w)
    return value

def show(elementsx, coordinates, u, tipodeElemento, p):
    
    matrixCalor = []
    v=u.copy()
    while v.size > 0:
        matrixCalor.append(v[:p+1])
        v = v[p+1:]
    if tipodeElemento == "CUADRADO":
        return matrixCalor  
    else:
        
        return matrixCalor



def neumannOrDirichlet(condicionesDeFrontera, EL, NL, w, l):
    #Lados i-j, j-m, m-n, n-i Que tipo de condicion de frontera
    #Si es True es Neumann, si es False es dirichlet
    neumann=[]
    dirichlet=[]
    listaAuxX=[]
    listaAuxY=[]
    listaAuxX_D=[]
    listaAuxY_D=[]

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