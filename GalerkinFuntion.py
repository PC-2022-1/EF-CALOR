
#Se desarrolla la funcion que arroja las 4 ecuaciones (por elemento)
#en terminos de las temperaturas de cada nodo perteneciente al elemento
 

import numpy as np
import matplotlib.pyplot as plt
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
import pandas as pd


def galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i, totallenght, totalwidth, listaLadosConv):

    #Funciones de Galerkin para un elemento de 4 nodos
    x=symbols('x')
    y=symbols('y')

    def Si(x, y, l , w, i): #l y w son el ancho y el alto de cada elemento, no de la malla
        if  i==0: 
            return (1-(x/l))*(1-(y/w))
        elif i==1:
            return  (x/l)*(1-(y/w)) 
        elif i==2:
            return (x/l)*(y/w)
        elif i==3:
            return (1-(x/l))*(y/w)    

    #T=[] #Lista de incognitas
    #for elemento in EL:
    #    for nodo in elemento:
    #  #      T.append(symbols("T"+str(nodo)))

    #print(T)
    def Taprox(x, y, l, w, E):
        return E[0] + (x/l)*(E[1]-E[0]) + y/w *((E[3]+(x/l)*(E[2]-E[3])) - 
        (E[0]+(x/l)*(E[1]-E[0])))

    ''' CONSTRUCCION DE LA INTEGRAL: 
        integral(KxTerm + KyTerm + q)Sidxdy = 0  donde: 
        KxTerm = Kxterm1 + Kxterm2
        KyTerm = KyTerm1 + Kyterm2 '''

    #print("Kxterm1")
    Kxterm1 = [0, 0, 0, 0]

    #For index, row

    # NL[EL[0]-1][1],NL[EL[3]-1][1])

    EL=EL[i]
    T=[]
    nodo=[]
    for j in EL:
        T.append(symbols("T"+str(j)))
        nodo.append(j)
    print(T)
    print("-----------------------")


    Kxterm1[0] = -h* integrate( Si(0, y, elemLength, elemWidth, 0) * (Taprox(0,y,elemLength,elemWidth,T) - Tf) ,( y, 0 ,elemWidth) ) 
    Kxterm1[0]= simplify(Kxterm1[0])
    Kxterm1[1] = -h* integrate( Si(elemLength, y, elemLength, elemWidth, 1) * (Taprox(elemLength,y,elemLength,elemWidth,T) - Tf) ,( y, 0,elemWidth ) )
    Kxterm1[1]= simplify(Kxterm1[1])
    Kxterm1[2] = -h* integrate( Si(elemLength, y, elemLength, elemWidth, 2) * (Taprox(elemLength,y,elemLength,elemWidth,T) - Tf) ,( y, 0,elemWidth) )
    Kxterm1[2]= simplify(Kxterm1[2])
    Kxterm1[3] = -h* integrate( Si(0, y, elemLength, elemWidth, 3) * (Taprox(0,y,elemLength,elemWidth,T) - Tf) ,( y, 0,elemWidth) )
    Kxterm1[3]= simplify(Kxterm1[3])

    Kyterm1 = [0, 0, 0, 0]
    Kyterm1[0] = -h* integrate( Si(x, 0, elemLength, elemWidth, 0) * (Taprox(x,0,elemLength,elemWidth,T) - Tf) ,( x, 0,elemLength) )
    Kyterm1[0]= simplify(Kyterm1[0])
    Kyterm1[1] = -h* integrate( Si(x, 0, elemLength, elemWidth, 1) * (Taprox(x,0,elemLength,elemWidth,T) - Tf) ,( x, 0,elemLength) )
    Kyterm1[1]= simplify(Kyterm1[1])
    Kyterm1[2] = -h* integrate( Si(x, elemWidth, elemLength, elemWidth, 2) * (Taprox(x,elemWidth,elemLength,elemWidth,T) - Tf) ,( x, 0,elemLength) )
    Kyterm1[2]= simplify(Kyterm1[2])
    Kyterm1[3] = -h* integrate( Si(x, elemWidth, elemLength, elemWidth, 3) * (Taprox(x,elemWidth,elemLength,elemWidth,T) - Tf) , ( x, 0,elemLength))
    Kyterm1[3]= simplify(Kyterm1[3])


    #print("Kxterm2")
    Kxterm2=[0,0,0,0]
    for i in range (0, 4):
        A=integrate(integrate(-kx*T[0]*diff(Si(x,y,elemLength,elemWidth,0),x)*diff(Si(x,y,elemLength,elemWidth,i),x),(x,0,elemLength)),(y,0,elemWidth))
        B=integrate(integrate(-kx*T[1]*diff(Si(x,y,elemLength,elemWidth,1),x)*diff(Si(x,y,elemLength,elemWidth,i),x),(x,0,elemLength)),(y,0,elemWidth))
        C=integrate(integrate(-kx*T[2]*diff(Si(x,y,elemLength,elemWidth,2),x)*diff(Si(x,y,elemLength,elemWidth,i),x),(x,0,elemLength)),(y,0,elemWidth))
        D=integrate(integrate(-kx*T[3]*diff(Si(x,y,elemLength,elemWidth,3),x)*diff(Si(x,y,elemLength,elemWidth,i),x),(x,0,elemLength)),(y,0,elemWidth))

        sum = A+B+C+D

        Kxterm2[i] = sum
        Kxterm2[i] = simplify(sum)
        #print(Kxterm2[i])

    #print("Kyterm2")
    Kyterm2=[0,0,0,0]
    for i in range (0, 4):
   
        A=integrate(integrate(-ky*T[0]*diff(Si(x,y,elemLength,elemWidth,0),y)*diff(Si(x,y,elemLength,elemWidth,i),y),(x,0,elemLength)),(y,0,elemWidth))
        B=integrate(integrate(-ky*T[1]*diff(Si(x,y,elemLength,elemWidth,1),y)*diff(Si(x,y,elemLength,elemWidth,i),y),(x,0,elemLength)),(y,0,elemWidth))    
        C=integrate(integrate(-ky*T[2]*diff(Si(x,y,elemLength,elemWidth,2),y)*diff(Si(x,y,elemLength,elemWidth,i),y),(x,0,elemLength)),(y,0,elemWidth))
        D=integrate(integrate(-ky*T[3]*diff(Si(x,y,elemLength,elemWidth,3),y)*diff(Si(x,y,elemLength,elemWidth,i),y),(x,0,elemLength)),(y,0,elemWidth))


        sum = A+B+C+D
        
        Kyterm2[i] = sum
        Kyterm2[i] = simplify(sum)
        #print(Kyterm2[i] )


    #print("q")
    qterm = [0,0,0,0]
    for i in range (0, 4):
        #A = integrate(integrate(q*Si(x,y,elemLength,elemWidth,i),(x,NL[EL[0]-1][0],NL[EL[1]-1][0])),(y,NL[EL[0]-1][1],NL[EL[3]-1][1]))
        A = integrate(integrate(q*Si(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))
        qterm[i] = simplify(A)
        #print(qterm[i])

    #Reuniendo el Sistema de ecuaciones para cada nodo juntando los terminos 
    eqSist=[0,0,0,0]
    listaEjemplo=[0,0,0,0,0,0,0,0,0]
    eqSist2=[0,0,0,0]
    for i in range (0,4):
        # eqSist[i]= Kxterm1[i] + Kxterm2[i] + Kyterm1[i] + Kyterm2[i] + qterm[i] 
        eqSist[i]= Kxterm2[i] + Kyterm2[i] + qterm[i] 
        #eqSist2[i]= Kxterm1[i] + Kyterm1[i] + eqSist[i]
        # print(eqSist[i])
        # print("--------")
        
    #Obteniendo el sistema de ecuaciones en forma matricial : (coeffMatrix)(Ti, Tn, Tj, Tm)trans + independentVector = 0
    # coeffMatrix, independentVector = linear_eq_to_matrix(eqSist, [T[0], T[1], T[2], T[3]])

        #Obteniendo el sistema de ecuaciones en forma matricial : (coeffMatrix)(Ti, Tn, Tj, Tm)trans + independentVector = 0

    Mk, Mq = linear_eq_to_matrix(eqSist, [T[0], T[1], T[2], T[3]])
    Mx,Vx = linear_eq_to_matrix(Kxterm1, [T[0], T[1], T[2], T[3]])
    My, Vy = linear_eq_to_matrix(Kyterm1, [T[0], T[1], T[2], T[3]])


    #Condiciones de convección en Mx,Vx y My,Vy
    for i in range(0,4):

        # print('-------> NODO'+str(i))

        if(NL[EL[i]-1][0]!=0 and NL[EL[i]-1][0]!=totallenght and NL[EL[i]-1][1]!=0 and NL[EL[i]-1][1]!=totalwidth):

                Mx[i]=[0,0,0,0]
                Vx[i]=[0]
                My[i]=[0,0,0,0]
                Vy[i]=[0]

        
        if(NL[EL[i]-1][0]==0 or NL[EL[i]-1][0]==totallenght):
            
            #codigo para cuando no hay conveccion en los lados externos 
            if ( NL[EL[i]-1][0]==0  and listaLadosConv [3]== False):
                Mx[i]=[0,0,0,0]
                Vx[i]=[0]
            if ( NL[EL[i]-1][0]==totallenght  and listaLadosConv [1]== False):
                Mx[i]=[0,0,0,0]
                Vx[i]=[0]

            if(NL[EL[i]-1][1]!=0 and NL[EL[i]-1][1]!=totalwidth):
                My[i]=[0,0,0,0]
                Vy[i]=[0]


        if(NL[EL[i]-1][1]==0 or NL[EL[i]-1][1]==totalwidth):
            if(NL[EL[i]-1][0]!=0 and NL[EL[i]-1][0]!=totallenght):
                Mx[i]=[0,0,0,0]
                Vx[i]=[0]

   
    coeffMatrix =Matrix(Mk+Mx+My)
    independentVector=Mq + Vx + Vy


    dfelement=pd.DataFrame(np.matrix(coeffMatrix))
    dfelement["indep"]=pd.DataFrame(np.matrix(independentVector))
    dfelement["nodo"]=pd.DataFrame(np.array(nodo))

    dfelement.rename(columns = {0: T[0],  1 :T[1], 2 :T[2], 3 :T[3] }, inplace = True)

    return dfelement



