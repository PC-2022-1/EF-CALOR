#Archivo donde se llama a la funcion galerkin y se hacen pruebas numericas

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
#from GalerkinFuntion import *
from GalerkinFunRect import *
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import sys


def GalerkinResult(dataFrameList):
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
  listaprueba=[]
  listaprueba2=[]
  for i in TemperatureVector:
      listaTemperaturas.append(symbols(str(i)))
      listaprueba.append(str(i))

  for ele in listaprueba:
    listaprueba2.append(int(ele[1:]))

  #Para usar la funcion linsolve de numpy 
  vectorFinal = vectorFinal.astype('float32')
  matrixFinal = matrixFinal.astype('float32')

  # print(TemperatureVector)
  #Se resuelve el sistema de ecuaciones
  result=np.linalg.solve(matrixFinal, vectorFinal)
  #print(result)

  matrixCalor = np.zeros((p+1, m+1))
  listaSinOrden=[]
  for i in range (0,len(listaprueba2)):
    listaSinOrden.append([listaprueba2[i],result[i]])

  def getKey(item):
    return item[0]

  listaOrdenada=sorted(listaSinOrden, key=getKey)

  # print(listaOrdenada)

  contador=0
  for j in range(0,m+1):
      for i in range (0,p+1):
          matrixCalor[j,i]=listaOrdenada[contador][1]
          contador=contador+1

  return  matrixCalor
  #print(matrixCalor)

  # plt.imshow(matrixCalor, cmap='hot', interpolation='nearest')
  # plt.show()
#from GalerkinFuntionNormalizado import *

l = float(sys.argv[1]) #Distancia en x
#l=symbols('l')
w = float(sys.argv[2]) #Distancia en y
#w=symbols('w')
p = int(sys.argv[3])  #Divisiones en x
m = int(sys.argv[4])  #Divisiones en y

#Definicion de condiciones iniciales

#kx=symbols('kx')
kx=float(sys.argv[5]) #k conductividad en y
#ky=symbols('kx')
ky=float(sys.argv[6]) #k conductividad en X

#Para caso donde la superficie es fuente de calor
#h=symbols('h')
h=float(sys.argv[7]) #h Coeficiente de conveccion h=-20
#Tf=symbols('Tf')
Tf=float(sys.argv[8]) #Tf Temperatura del aire  Tf=100
#q=symbols('q')
q=float(sys.argv[9]) #q Flujo especifico de calor Vatios/m3   q=-100 


elemLength = l/p #Largo del elemento
elemWidth = w/m  #Ancho del elemento
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'
listaLadosConv=[eval(sys.argv[10]),eval(sys.argv[11]),eval(sys.argv[12]),eval(sys.argv[13])] #Lados i-j, j-m, m-n, n-i Lista con lados con conv


#Se genera la lista NL ("Node list") que contiene las coordenadas de cada nodo
#y EL("Element list") que contiene la lista de nodos de cada elemento
NL,EL = uniform_mesh(l, w, p, m, tipoDeElemento) # Generar malla
#graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

print(NL)
print(EL)
#galerkinMethodRect retorna un dataframe por elemento
dataFrameList = []  #Se juntan las dataframe de cada elemento en una lista dataFrameList
for i in range (0, len(EL)):
    dataFrameList.append(galerkinMethodRect(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i,l,w, listaLadosConv ))
#print(dataFrameList)

matrixCalor = GalerkinResult(dataFrameList) #GalerkinResult organiza, combina y reduce los dataframes, los convierte en matrices 
#y se encuentra la solución al sistema de ecuaciones que se guarda en una matriz solución (matrixCalor)
ax = sns.heatmap(matrixCalor, linewidth=0.5,cmap="Spectral_r")
ax.invert_yaxis()
plt.show()