from pdb import find_function
from numpy import *
from Mesh import *
from heatFunction import *
from scipy.sparse import *
import sys

# Parametros para el mallado
l = float(sys.argv[1]) # Distancia en x
w = float(sys.argv[2]) # Distancia en y
p = int(sys.argv[3])  #Divisiones en x
m = int(sys.argv[4]) # Divisiones en y

# Tipo de elemento
tipoDeElemento = str(sys.argv[5])

# Parametros de comportamientos
f_fun = lambda x : 0 #Funcion laplacianoU=f
g_fun = lambda x : 2 #Derivada de la temperatura en lados con condiciones neumann. g=0 es lado aislado
u_d_fun = lambda x : 100 #Temperaturas fijas en lados dirichlet

# --- ----------------discretización --------------------- ##

#NL es una lista con las coordenadas de cada elemento
#EL es una lista con los nodos de cada elemento
NL, EL = uniform_mesh(l, w, p, m, tipoDeElemento)

#Se convierte la lista NL en un arreglo
coordinates = array(NL)

#Se escoge la lista con los nodos dependiendo del tipo de elemento
if tipoDeElemento == 'CUADRADO':
    elements4 = EL
else:
    elements3 = EL


#----------------------Neumann & Dirichlet-----------------------#
# Se generan listas que contienen condiciones 
# Tipo de condicion de frontera: Lado inferior, derecho, superior, izquierdo 
# Si es True es Neumann, si es False es dirichlet
condicionesDeFrontera = [eval(sys.argv[6]), eval(sys.argv[7]), eval(sys.argv[8]), eval(sys.argv[9])] 
neumann,dirichlet = neumannOrDirichlet(condicionesDeFrontera, EL, NL, w, l)



# Pasos iniciales para generación de Matriz A & b

ZeroMatrix = np.zeros((size(coordinates, 0) , size(coordinates, 0)))
A = lil_matrix(ZeroMatrix)
aux = lil_matrix(ZeroMatrix)
b = zeros((size(coordinates, 0), 1))

## ---------------- ENSAMBLE-------------------- --- ##


#------------Matriz de esfuerzos A-------------------##

#dependiendo del tipo de elemento se llama a la función stima3/stima4 y se va actualizando la matriz A (sparse) con los
#valores que devuelve cada función. Si hay alguna posición repetida en la matriz se suma el valor. Esto se hace para cada 
#elemento.

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


#---------------------vector b-----------------------##

# se construye el vector b involucrando la funcion f (laplacianoU = f). Se soluciona la integral de la función f multiplicado el vector de la función Hat
# por medio de una aproximación que involucra el determinante de una matriz que corresponde al area del elemento y la evaluacion de f en el centro de masa
if tipoDeElemento == 'CUADRADO':
    for j in range(size(elements4, 0)):
        H = np.vstack((ones((1, 3)), coordinates[elements4[j,:3]-1, :].T)) 
        b[elements4[j, :]-1] = b[elements4[j, :]-1] + linalg.det(H) * f(sum(coordinates[elements4[j,:]-1, :], axis=0) / 4, f_fun)  / 4

else: 
    for j in range(size(elements3, 0)):
        H = np.vstack((ones((1, 3)), coordinates[elements3[j,:]-1, :].T))
        b[elements3[j, :]-1] = b[elements3[j, :]-1] + linalg.det(H) * f(sum(coordinates[elements3[j,:]-1, :], axis=0) / 3, f_fun)  / 6


##---------------- condiciones Neumann------------------------------##

#Se involucran las condiciones de frontera tipo neumann. modifica el vector b agregando el termino que contiene a la función g. Se hace tambien
#Una aproximación del punto medio y un determinante con la longitud del elemento

if len(neumann) > 0:
    for j in range(size(neumann, 0)):
        b[neumann[j][:]-1] = b[neumann[j][:]-1] + linalg.norm(coordinates[neumann[j][0]-1, :] - coordinates[neumann[j][1]-1, :]) * g(sum(coordinates[neumann[j,:]-1, :], axis=0) / 2, g_fun) / 2




#Se genera el vector de incognitas u
u = zeros_like(b)
u = u[:, 0].reshape(b.shape)

##---------------- condiciones dirchlet----------------------------------##

#Se reemplazan los valores en u de las incognitas cuyos valores son conocidos
BoundNodes = array(unique(dirichlet)) -1
u[BoundNodes] = u_d(coordinates[BoundNodes, :], u_d_fun)

#Se reescribe el primer bloque de ecuaciones
b = b - A * u

##-----------------solucion del sistema----------------------------------##

#Se soluciona el sistema de ecuaciones con la inversa de la matriz A 
FreeNodes = setdiff1d(range(size(coordinates, 0)), BoundNodes)
u[FreeNodes] = linalg.inv(A[FreeNodes][:, FreeNodes].toarray()) @ b[FreeNodes]
u = u[:, 0].reshape(coordinates[:, -1].shape)
print(u)

##---------------------Grafica-----------------------------------------##
if tipoDeElemento=='CUADRADO':
    matrixCalor = show(coordinates, u, 'CUADRADO', p)
else:
    matrixCalor = show(coordinates, u, 'TRIANGULO', p)


#Para hacer pruebas con funciones teoricas
matrixTeorica = np.zeros(array(matrixCalor).shape)
for row, Row in enumerate(matrixTeorica):
    for column, Column in enumerate(Row):
        matrixTeorica[row, column] = l/p * row + w/m * column
#print( matrixTeorica - matrixCalor )
print( linalg.norm(matrixTeorica - matrixCalor) /  linalg.norm(matrixTeorica) )
