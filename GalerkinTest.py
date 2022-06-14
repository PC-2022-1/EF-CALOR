#Archivo donde se llama a la funcion galerkin y se hacen pruebas numericas

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
from GalerkinFuntion import *
#from GalerkinFuntionNormalizado import *

l = 0.6 #Distancia en x
#l=symbols('l')
w = 0.6 #Distancia en y
#w=symbols('w')
p = 2  #Divisiones en x
m = 2  #Divisiones en y

elemLength = l/p #Largo del elemento
elemWidth = w/m  #Ancho del elemento
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

#Se genera la lista NL ("Node list") que contiene las coordenadas de cada nodo
#y EL("Element list") que contiene la lista de nodos de cada elemento

NL,EL = uniform_mesh(l, w, p, m, tipoDeElemento) # Generar malla

# graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

#Definicion de condiciones iniciales

#kx=symbols('kx')
kx=1.2 #k conductividad en y
#ky=symbols('kx')
ky=1.2 #k conductividad en X

#Para caso donde la superficie es fuente de calor
#h=symbols('h')
h=20 #h Coeficiente de conveccion
#Tf=symbols('Tf')
Tf=30 #Tf Temperatura del aire 
#q=symbols('q')
q=1000 #q Flujo especifico de calor Vatios/m3  

#Para caso donde el calor viene del ambiente:
# h=-20 #h Coeficiente de conveccion
# Tf=100 #Tf Temperatura del aire 
# q=-100 #q Flujo especifico de calor Vatios/m3 




eqSist=[]
dataFrame=pd.DataFrame()

listaLadosConv=[True,True,True,False] #Lados i-j, j-m, m-n, n-i Lista con lados con conv

dataFrameList = []  #Se juntan las dataframe de cada elemento en una lista dataFrameList
for i in range (0, len(EL)):
    dataFrameList.append(galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i,l,w, listaLadosConv ))

#print(dataFrameList)

#Nuevo dataframe juntando todas las dataFrame con elementos. Teniendo 4x#El ecuaciones
DataFrame = pd.concat(dataFrameList, axis=0)

#Las ecuaciones se suma deacuerdo a los nodos, para tener #Nodos ecuaciones
CompressedDF = DataFrame.replace(np.nan,0) #0 donde no hay termino
CompressedDF = DataFrame.groupby("nodo").sum() #suma por columna nodo
#CompressedDF.to_excel("ef.xlsx") #Para visualizar dataFrame comprimido
#DataFrame.to_excel ("ef2.xlsx" ) #Para visualizar dataFrame original

#Generación de matrices
matrixFinal = np.matrix(CompressedDF.drop('indep', inplace=False, axis=1)) #Matriz de coeff final
vectorFinal = np.array(CompressedDF['indep']) #Vector independiente para la solucion 
CompressedDF.drop('indep', inplace=True, axis=1) #Eliminamos de CompressedDF la columna indep
TemperatureVector =np.array(CompressedDF.columns ) #Se genera un vector con las incognitas


#print(matrixFinal)
#print(vectorFinal)

#Se genera una lista para guardar como incognitas las temperaturas
listaTemperaturas=[]
for i in TemperatureVector:
    listaTemperaturas.append(symbols(str(i)))

#Para usar la funcion linsolve de numpy 
vectorFinal = vectorFinal.astype('float32')
matrixFinal = matrixFinal.astype('float32')

print(TemperatureVector)
#Se resuelve el sistema de ecuaciones
result=np.linalg.solve(matrixFinal, vectorFinal)
print(result)