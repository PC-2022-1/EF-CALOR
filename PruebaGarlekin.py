#Archivo principal de generación de mallas. 
#Este archivo importa de Mesh 

import numpy as np
import matplotlib.pyplot as plt
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, symbols,simplify, Eq

#l = 0.6 #Distancia en x
l=symbols('l')
#w = 0.6 #Distancia en y
w=symbols('w')
p = 2  #Divisiones en x
m = 2  #Divisiones en y
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

#NL,EL = uniform_mesh(l,w,p,m,tipoDeElemento) #Generar malla

#graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

#Definicion de condiciones iniciales

#q =1000 #Vatios/m3
#k = 1.2 #conductividad en X y en Y (Watts)
#h = 20  #Coeficiente de conveccion
#Tf = 30 #Temperatura del aire 
k=symbols('k')
h=symbols('h')
Tf=symbols('Tf')

#Dos caras aisladas y dos en contacto con el aire. Superficie es un foco de calor

print("Nodes list")
#print(NL)
print("Element list")
#print(EL)

#Funciones de Galerkin para un elemento de 4 nodos
x=symbols('x')
y=symbols('y')

def Si(x, y, l, w, i):
    if i==0: 
        return (1-(x/l))*(1-(y/w))
    elif i==1:
        return  (x/l)*(1-y/w) 
    elif i==2:
        return (x/l)*(y/w)
    elif i==3:
        return (1-x/l)*(y/w)    

#Temperatura aproximada
Ti=symbols('Ti')
Tm=symbols('Tm')
Tj=symbols('Tj')
Tn=symbols('Tn')

def Taprox(x, y, l, w):
    return Ti + ((x/l)*(Tj-Ti)) + y/w *((Tn+(x/l)*(Tm-Tn)) - (Ti+(x/l)*(Tj-Ti)))

# integral(KxTerm+KyTerm+q)Sdxdy = 0  
# KxTerm = Kxterm1 + Kxterm2
# KyTerm = KyTerm1 + Kyterm2
Kxterm1 = [0, 0, 0, 0]
for i in range (0, 4):
    A = -h* integrate( (Si(0, y, l, w, i) * Taprox(0,y,l,w) - Tf) ,( y, 0, w ) )
    Kxterm1[i] = simplify(A)
    print(Kxterm1[i])
