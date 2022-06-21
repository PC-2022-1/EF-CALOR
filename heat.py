from pdb import find_function
from numpy import *
from Mesh import *
from heatFunction import *
from scipy.sparse import *

## --- Testing phase --- ##

# Dimentional Parameters
l = 4 # Distancia en x
w = 4 # Distancia en y
p = 30 # Divisiones en x
m = 30 # Divisiones en y

# Type Parameters
tipoDeElemento = 'CUADRADO'

# Behaviour Parameters
f_fun = lambda x : 0
g_fun = lambda x : 2*x
u_d_fun = lambda x : x

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

condicionesDeFrontera = [False, False, False, False]  #i-j n-i neumann, #j-m, m-n dirichlet

neumann,dirichlet = neumannOrDirichlet(condicionesDeFrontera, EL, NL, w, l)

# Generación de Matriz A & b

ZeroMatrix = np.zeros((size(coordinates, 0) , size(coordinates, 0)))
A = lil_matrix(ZeroMatrix)
aux = lil_matrix(ZeroMatrix)
b = zeros((size(coordinates, 0), 1))

## --- Assembly --- ##

#-----------A-------------#
#for j in range(size(elements3, 0)):
#    A[elements4[j, :], elements4[j, :]] = A[elements3[j, :], elements3[j, :]] + stima3(coordinates[elements3[j, :], :])

for j in range(size(elements4, 0)):
    k=0
    for i in elements4[j]-1:
        aux[elements4[j]-1, i] = stima4(coordinates[elements4[j]-1, :])[k]
        k=k+1
    A = A + aux
    aux =lil_matrix(ZeroMatrix)

#-----------b-------------#
# Volume Forces
#for j in range(size(elements3, 0)):
#    b[elements3[j, :]] = b[elements3[j, :]] + linalg.det(vstack(ones(1, 3), coordinates[elements3[j,:], :].T)) * f(sum(coordinates[elements3[j,:], :]) / 3) / 6

for j in range(size(elements4, 0)):
    H = np.vstack((ones((1, 3)), coordinates[elements4[j,:3]-1, :].T))

    b[elements4[j, :]-1] = b[elements4[j, :]-1] + linalg.det(H) * f(sum(coordinates[elements4[j,:]-1, :], axis=0) / 4, f_fun)  / 4
    #b[elements4[j, :]-1] = b[elements4[j, :]-1] + linalg.det(H) * 1 / 4


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

show(elements4, coordinates, u)
matrixCalor = show2d(u, p)

matrixTeorica = np.zeros(array(matrixCalor).shape)

for row, Row in enumerate(matrixTeorica):
    for column, Column in enumerate(Row):
        matrixTeorica[row, column] = l/p * row + w/m * column

#print( matrixTeorica - matrixCalor )
print( linalg.norm(matrixTeorica - matrixCalor) /  linalg.norm(matrixTeorica) )
