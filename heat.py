from pdb import find_function
from numpy import *
from Mesh import *
from heatFunction import *
from scipy.sparse import *
import sys

## --- Testing phase --- ##

# Dimentional Parameters
l = float(sys.argv[1]) # Distancia en x=6
w = float(sys.argv[2]) # Distancia en y=6
p = int(sys.argv[3]) # Divisiones en x=20
m = int(sys.argv[4]) # Divisiones en y=20

# Type Parameters
tipoDeElemento = 'TRIANGULO'

# Behaviour Parameters
f_fun = lambda x : 0
g_fun = lambda x : 10
u_d_fun = lambda x : 100

# --- Se generan los archivos a cargar --- ##

NL, EL = uniform_mesh(l, w, p, m, tipoDeElemento)

coordinates = array(NL)

if tipoDeElemento == 'CUADRADO':
    elements4 = EL
else:
    elements3 = EL

## --- Se generan Newman & Dirichlet --- ##
# Lados i-j, j-m, m-n, n-i Que tipo de condicion de frontera
# Si es True es Neumann, si es False es dirichlet

condicionesDeFrontera = [False, True, True, True]  #i-j n-i neumann, #j-m, m-n dirichlet

neumann,dirichlet = neumannOrDirichlet(condicionesDeFrontera, EL, NL, w, l)

# if tipoDeElemento == 'TRIANGULO':
#     neumann   =np.array([[1,4],[1,2],[2,3],[4,7]])
#     dirichlet =np.array([[3,6],[6,9],[9,8],[8,7]])
# else: neumann,dirichlet = neumannOrDirichlet(condicionesDeFrontera, EL, NL, w, l)

# Generación de Matriz A & b

ZeroMatrix = np.zeros((size(coordinates, 0) , size(coordinates, 0)))
A = lil_matrix(ZeroMatrix)
aux = lil_matrix(ZeroMatrix)
b = zeros((size(coordinates, 0), 1))

## --- Assembly --- ##

#-----------A-------------#
#for j in range(size(elements3, 0)):
#    A[elements4[j, :], elements4[j, :]] = A[elements3[j, :], elements3[j, :]] + stima3(coordinates[elements3[j, :], :])

if tipoDeElemento == 'CUADRADO':
    for j in range(size(elements4, 0)):
        k=0
        for i in elements4[j]-1:
            aux[elements4[j]-1, i] = stima4(coordinates[elements4[j]-1, :])[k]
            k=k+1
        A = A + aux
        aux =lil_matrix(ZeroMatrix)
else: 
    for j in range(size(elements3, 0)):
        k=0
        for i in elements3[j]-1:
            aux[elements3[j]-1, i] = stima3(coordinates[elements3[j]-1, :])[k]
            k=k+1
        A = A + aux
        aux =lil_matrix(ZeroMatrix)


#-----------b-------------#
# Volume Forces
#for j in range(size(elements3, 0)):
#    b[elements3[j, :]] = b[elements3[j, :]] + linalg.det(vstack(ones(1, 3), coordinates[elements3[j,:], :].T)) * f(sum(coordinates[elements3[j,:], :]) / 3) / 6

if tipoDeElemento == 'CUADRADO':
    for j in range(size(elements4, 0)):
        H = np.vstack((ones((1, 3)), coordinates[elements4[j,:3]-1, :].T))
        
        b[elements4[j, :]-1] = b[elements4[j, :]-1] + linalg.det(H) * f(sum(coordinates[elements4[j,:]-1, :], axis=0) / 4, f_fun)  / 4
        #b[elements4[j, :]-1] = b[elements4[j, :]-1] + linalg.det(H) * 1 / 4
else: 
    for j in range(size(elements3, 0)):
        H = np.vstack((ones((1, 3)), coordinates[elements3[j,:]-1, :].T))
        b[elements3[j, :]-1] = b[elements3[j, :]-1] + linalg.det(H) * f(sum(coordinates[elements3[j,:]-1, :], axis=0) / 3, f_fun)  / 6


# Neumann conditions
if len(neumann) > 0:
    for j in range(size(neumann, 0)):
        b[neumann[j][:]-1] = b[neumann[j][:]-1] + linalg.norm(coordinates[neumann[j][0]-1, :] - coordinates[neumann[j][1]-1, :]) * g(sum(coordinates[neumann[j,:]-1, :], axis=0) / 2, g_fun) / 2
        #b[neumann[j][:]-1] = b[neumann[j][:]-1] + linalg.norm(coordinates[neumann[j][0]-1,:] - coordinates[neumann[j][1]-1, :] ) * 0 / 2


u = zeros_like(b)
u = u[:, 0].reshape(b.shape)

BoundNodes = array(unique(dirichlet)) -1
u[BoundNodes] = u_d(coordinates[BoundNodes, :], u_d_fun)
b = b - A * u

FreeNodes = setdiff1d(range(size(coordinates, 0)), BoundNodes)

u[FreeNodes] = linalg.inv(A[FreeNodes][:, FreeNodes].toarray()) @ b[FreeNodes]
u = u[:, 0].reshape(coordinates[:, -1].shape)


# show(elements4, coordinates, u)
if tipoDeElemento=='CUADRADO':
    matrixCalor = show(elements4, coordinates, u, 'CUADRADO', p)
else:
    matrixCalor = show(elements3, coordinates, u, 'TRIANGULO', p)

matrixTeorica = np.zeros(array(matrixCalor).shape)

for row, Row in enumerate(matrixTeorica):
    for column, Column in enumerate(Row):
        matrixTeorica[row, column] = l/p * row + w/m * column

#print( matrixTeorica - matrixCalor )
print( linalg.norm(matrixTeorica - matrixCalor) /  linalg.norm(matrixTeorica) )
print(u)
