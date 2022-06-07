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
p = 2  #Divisiones en x
m = 2  #Divisiones en y

elemLength=l/p
elemWidth=w/m
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

# NL,EL = uniform_mesh(l,w,p,m,tipoDeElemento) #Generar malla

NL= [[0,0],[0.3,0],[0.3,0.3],[0,0.3],[-0.3,0.3],[-0.3,0],[-0.3,-0.3],[0,-0.3],[0.3,-0.3]]
EL=[[1,2,3,4],[6,1,4,5],[7,8,1,6],[8,9,2,1]]
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

# for i in range (0, len(EL)):
#      (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i,l,w))
#     #eqSist.append(galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i))
#     #print(eqSist)#

# dataF1 = (galerkinMethodNorm(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 0,l,w))
# dataF2 = (galerkinMethodNorm(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 1,l,w))
# dataF3 = (galerkinMethodNorm(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 2,l,w))
# dataF4 = (galerkinMethodNorm(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 3,l,w))

dataF1 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 0,l,w))
dataF2 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 1,l,w))
dataF3 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 2,l,w))
dataF4 = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 3,l,w))

result = pd.concat([dataF1, dataF2, dataF3, dataF4], axis=0)

# result.groupby(['indep'])['indep'].sum()
#result.fillna(0)
algo = result.replace(np.nan,0)
algo = result.groupby("nodo").sum()

algo.to_excel("ef.xlsx")
result.to_excel ("ef2.xlsx" )
print(algo)

# eqSist = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 0)) #Para prueba conveccion primer elemento

# print(eqSist)