#Archivo principal de generación de mallas

import numpy as np
import matplotlib.pyplot as plt
from Mesh import * #Archivo donde esta la función para generar malla y para graficar


d1 = 1 #Distancia en x
d2 = 1 #Distancia en y
p = 5  #Divisiones en x
m = 5  #Divisiones en y
tipoDeElemento = 'TRIANGULO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

NL,EL = uniform_mesh(d1,d2,p,m,tipoDeElemento) #Generar malla

graph_mesh(tipoDeElemento,NL,EL) #Graficar malla