#Archivo donde se llama a la funcion garlekin y se hacen pruebas numericas

import numpy as np
import matplotlib.pyplot as plt
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
from GalerkinFuntion import *

l = 0.6 #Distancia en x
#l=symbols('l')
w = 0.6 #Distancia en y
#w=symbols('w')
p = 2  #Divisiones en x
m = 2  #Divisiones en y

elemLength=l/p
elemWidth=w/m
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

NL,EL = uniform_mesh(l,w,p,m,tipoDeElemento) #Generar malla

graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

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

print(EL)
print(NL)
eqSist=[]
for i in range (0, len(EL)):
    galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i)
    #eqSist.append(galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i))
    #print(eqSist)#

#eqSist = (galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, 0)) #Para prueba conveccion primer elemento

#print(eqSist)