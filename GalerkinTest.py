#Archivo donde se llama a la funcion garlekin y se hacen pruebas numericas

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
from GalerkinFuntion import *
from GalerkinFuntionNormalizado import *

l = 0.6 #Distancia en x
#l=symbols('l')
w = 0.6 #Distancia en y
#w=symbols('w')
p = 4  #Divisiones en x
m = 4  #Divisiones en y

elemLength=l/p
elemWidth=w/m
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

NL,EL = uniform_mesh(l, w, p, m, tipoDeElemento) #Generar malla

# NL= [[0,0],[0.3,0],[0.3,0.3],[0,0.3],[-0.3,0.3],[-0.3,0],[-0.3,-0.3],[0,-0.3],[0.3,-0.3]]
# EL=[[1,2,3,4],[6,1,4,5],[7,8,1,6],[8,9,2,1]]
# graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

#Definicion de condiciones iniciales

#q Vatios/m3
#k conductividad en X y en Y (Watts)
#h Coeficiente de conveccion
#Tf Temperatura del aire 

#kx=symbols('kx')
kx=1.2
#ky=symbols('kx')
ky=1.2
#h=symbols('h')
h=20
#Tf=symbols('Tf')
Tf=30
#q=symbols('q')
q=1000

# print(EL)
# print(NL)
eqSist=[]
dataFrame=pd.DataFrame()
dataF1=pd.DataFrame()
dataF2=pd.DataFrame()
dataF3=pd.DataFrame()
dataF4=pd.DataFrame()

listaLadosConv=[True,True,True,True] #Lados i-j, j-m, m-n, n-i

dataFrameList = [] 
for i in range (0, len(EL)):
    # (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i,l,w))
    dataFrameList.append(galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i,l,w, listaLadosConv ))
    #print(eqSist)#

print(dataFrameList)

# dataF1 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 0,l,w))
# dataF2 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 1,l,w))
# dataF3 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 2,l,w))
# dataF4 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 3,l,w))

DataFrame = pd.concat(dataFrameList, axis=0)

# result.groupby(['indep'])['indep'].sum()
#result.fillna(0)
CompressedDF = DataFrame.replace(np.nan,0)
CompressedDF = DataFrame.groupby("nodo").sum()
CompressedDF.to_excel("ef.xlsx")
DataFrame.to_excel ("ef2.xlsx" )
#print(CompressedDF)

matrixFinal = np.matrix(CompressedDF.drop('indep', inplace=False, axis=1))
vectorFinal = np.array(CompressedDF['indep'])
CompressedDF.drop('indep', inplace=True, axis=1)
TemperatureVector =np.array(CompressedDF.columns )


print((matrixFinal))
print((vectorFinal))

listaTemperaturas=[]

for i in TemperatureVector:
    listaTemperaturas.append(symbols(str(i)))
    #print(i)
vectorFinal = vectorFinal.astype('float32')
matrixFinal = matrixFinal.astype('float32')

print(TemperatureVector)
# print(linsolve((matrixFinal, vectorFinal), listaTemperaturas))
result=np.linalg.solve(matrixFinal, vectorFinal)
print(result)
# eqSist = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 0)) #Para prueba conveccion primer elemento

# print(eqSist)