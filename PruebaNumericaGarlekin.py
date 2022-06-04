'''
Prueba numerica con datos del libro para un ejemplo de 4 nodos (1 solo elemento)
'''

import numpy as np
import matplotlib.pyplot as plt
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *

l = 0.6 #Distancia en x
#l=symbols('l')
w = 0.6 #Distancia en y
#w=symbols('w')
p = 2  #Divisiones en x
m = 2  #Divisiones en y
tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

#NL,EL = uniform_mesh(l,w,p,m,tipoDeElemento) #Generar malla

#graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

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

#Dos caras aisladas y dos en contacto con el aire. Superficie es un foco de calor

#print("Nodes list")
#print(NL)
#print("Element list")
#print(EL)

#Funciones de Galerkin para un elemento de 4 nodos
x=symbols('x')
y=symbols('y')

def Si(x, y, l, w, i):
    if  i==0: 
        return (1-(x/l))*(1-(y/w))
    elif i==1:
        return  (x/l)*(1-(y/w)) 
    elif i==2:
        return (x/l)*(y/w)
    elif i==3:
        return (1-(x/l))*(y/w)    

#Temperatura aproximada
Ti=symbols('Ti')
Tm=symbols('Tm')
Tj=symbols('Tj')
Tn=symbols('Tn')

def Taprox(x, y, l, w):
    return Ti + (x/l)*(Tj-Ti) + y/w *((Tn+(x/l)*(Tm-Tn)) - (Ti+(x/l)*(Tj-Ti)))

''' CONSTRUCCION DE LA INTEGRAL: 
    integral(KxTerm + KyTerm + q)Sidxdy = 0  donde: 
    KxTerm = Kxterm1 + Kxterm2
    KyTerm = KyTerm1 + Kyterm2 '''

#print("Kxterm1")
Kxterm1 = [0, 0, 0, 0]

#For index, row
Kxterm1[0] = -h* integrate( Si(0, y, l, w, 0) * (Taprox(0,y,l,w) - Tf) ,( y, 0, w ) ) 
Kxterm1[0]= simplify(Kxterm1[0])
Kxterm1[1] = -h* integrate( Si(l, y, l, w, 1) * (Taprox(l,y,l,w) - Tf) ,( y, 0, w ) )
Kxterm1[1]= simplify(Kxterm1[1])
Kxterm1[2] = -h* integrate( Si(l, y, l, w, 2) * (Taprox(l,y,l,w) - Tf) ,( y, 0, w ) )
Kxterm1[2]= simplify(Kxterm1[2])
Kxterm1[3] = -h* integrate( Si(0, y, l, w, 3) * (Taprox(0,y,l,w) - Tf) ,( y, 0, w ) )
Kxterm1[3]= simplify(Kxterm1[3])

#print("Kyterm1")
Kyterm1 = [0, 0, 0, 0]
Kyterm1[0] = -h* integrate( Si(x, 0, l, w, 0) * (Taprox(x,0,l,w) - Tf) ,( x, 0, l ) )
Kyterm1[0]= simplify(Kyterm1[0])
Kyterm1[1] = -h* integrate( Si(x, 0, l, w, 1) * (Taprox(x,0,l,w) - Tf) ,( x, 0, l ) )
Kyterm1[1]= simplify(Kyterm1[1])
Kyterm1[2] = -h* integrate( Si(x, w, l, w, 2) * (Taprox(x,w,l,w) - Tf) ,( x, 0, l ) )
Kyterm1[2]= simplify(Kyterm1[2])
Kyterm1[3] = -h* integrate( Si(x, w, l, w, 3) * (Taprox(x,w,l,w) - Tf) , ( x, 0, l ))
Kyterm1[3]= simplify(Kyterm1[3])

#print("Kxterm2")
Kxterm2=[0,0,0,0]
for i in range (0, 4):
    
    A=integrate(integrate(-kx*Ti*diff(Si(x,y,l,w,0),x)*diff(Si(x,y,l,w,i),x),(x,0,l)),(y,0,w))
    B=integrate(integrate(-kx*Tj*diff(Si(x,y,l,w,1),x)*diff(Si(x,y,l,w,i),x),(x,0,l)),(y,0,w))
    C=integrate(integrate(-kx*Tm*diff(Si(x,y,l,w,2),x)*diff(Si(x,y,l,w,i),x),(x,0,l)),(y,0,w))
    D=integrate(integrate(-kx*Tn*diff(Si(x,y,l,w,3),x)*diff(Si(x,y,l,w,i),x),(x,0,l)),(y,0,w))

    sum = A+B+C+D

    Kxterm2[i] = sum
    Kxterm2[i] = simplify(sum)
    #print(Kxterm2[i])

#print("Kyterm2")
Kyterm2=[0,0,0,0]
for i in range (0, 4):
    A=integrate(integrate(-ky*Ti*diff(Si(x,y,l,w,0),y)*diff(Si(x,y,l,w,i),y),(x,0,l)),(y,0,w))
    B=integrate(integrate(-ky*Tj*diff(Si(x,y,l,w,1),y)*diff(Si(x,y,l,w,i),y),(x,0,l)),(y,0,w))
    C=integrate(integrate(-ky*Tm*diff(Si(x,y,l,w,2),y)*diff(Si(x,y,l,w,i),y),(x,0,l)),(y,0,w))
    D=integrate(integrate(-ky*Tn*diff(Si(x,y,l,w,3),y)*diff(Si(x,y,l,w,i),y),(x,0,l)),(y,0,w))

    sum = A+B+C+D
    
    Kyterm2[i] = sum
    Kyterm2[i] = simplify(sum)


#print("q")
qterm = [0,0,0,0]
for i in range (0, 4):
    A = integrate(integrate(q*Si(x,y,l,w,i),(x,0,l)),(y,0,w))
    qterm[i] = simplify(A)
    #print(qterm[i])

#Reuniendo el Sistema de ecuaciones para cada nodo juntando los terminos 
eqSist=[0,0,0,0]
for i in range (0,4):
    eqSist[i]= Kxterm1[i] + Kxterm2[i] + Kyterm1[i] + Kyterm2[i] + qterm[i] 
    print(eqSist[i])

    #print("--------")

#Obteniendo el sistema de ecuaciones en forma matricial : (coeffMatrix)(Ti, Tn, Tj, Tm)trans + independentVector = 0
coeffMatrix, independentVector = linear_eq_to_matrix(eqSist, [Ti, Tj, Tm, Tn])
#print(coeffMatrix)
print("------")
#print(independentVector)

#Resolviendo el sistema de ecuaciones
print(linsolve((coeffMatrix, independentVector), [Ti, Tj, Tm, Tn]))