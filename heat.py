from numpy import *
from Mesh import *
from heatFunction import *

## ------ Testing phase ------- ##

l = 4 #Distancia en x
#l=symbols('l')
w = 4 #Distancia en y
#w=symbols('w')
p = 2  #Divisiones en x
m = 2  #Divisiones en y
tipoDeElemento = 'CUADRADO'

# --- Se generan los archivos a cargar --- ##

NL, EL = uniform_mesh(l, w, p, m, tipoDeElemento)

coordinates = NL

if tipoDeElemento == 'CUADRADO':
    elements4 = EL
else:
    elements3 = EL

## --- Se generan Newman & Dirichlet --- ##

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

A = zeros((size(coordinates, 0), size(coordinates, 0)))
b = zeros((size(coordinates, 0), 1))

## Assembly

#for j in range(size(elements3, 0)):
#    A[elements4[j, :], elements4[j, :]] = A[elements3[j, :], elements3[j, :]] + stima3(coordinates[elements3[j, :], :])

for j in range(size(elements4, 0)):

    A[elements4[j, :]-1][:, elements4[j, :]-1] = A[elements4[j, :]-1][:, elements4[j, :]-1] + stima4(coordinates[elements4[j, :]-1, :])


# Volume Forces

#for j in range(size(elements3, 0)):
#    b[elements3[j, :]] = b[elements3[j, :]] + linalg.det(vstack(ones(1, 3), coordinates[elements3[j,:], :].T)) * f(sum(coordinates[elements3[j,:], :]) / 3) / 6

for j in range(size(elements4, 0)):

    H = vstack((ones((1, 3)), coordinates[elements4[j,:4], :].T))
    b[elements4[j, :]] = b[elements4[j, :]] + linalg.det(H) * f(sum(coordinates[elements4[j,:], :]) / 4) / 4

# Neumann conditions

if len(neumann) > 0:
    for j in range(size(neumann, 0)):

        b[neumann[j,:]] = b[neumann[j,:]] + linalg.norm(coordinates[neumann[j, 0],:]) - coordinates[neumann[j, 1], :] * g(sum(coordinates[neumann[j,:], :]) / 2) / 2


u = zeros_like(b)

BoundNodes = unique(dirichlet)
u[BoundNodes] = u_d(coordinates[BoundNodes, :])
b = b - A * u

FreeNodes = setdiff1d(range(size(coordinates, 0)), BoundNodes)

u[FreeNodes] = linalg.inv(A[FreeNodes, FreeNodes]) * b

show(elements3, elements4, coordinates, full(u))
