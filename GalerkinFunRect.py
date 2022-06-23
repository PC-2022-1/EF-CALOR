#Se desarrolla la funcion que arroja las 4 ecuaciones (por elemento)
#en terminos de las temperaturas de cada nodo perteneciente al elemento
#Para un elemento rectangular
 
#Se importan librerias
import numpy as np
import matplotlib.pyplot as plt
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
import pandas as pd
from scipy.integrate import dblquad




#S es la funcion "HAT" para un elemento de 4 nodos
#la cual es 0 en cualquier nodo distinto a su posicion
def Si(x, y, l , w, i): #l y w son el ancho y el alto de cada elemento, no de la malla
    if  i==0: 
        return (1-(x/l))*(1-(y/w))
    elif i==1:
        return  (x/l)*(1-(y/w)) 
    elif i==2:
        return (x/l)*(y/w)
    elif i==3:
        return (1-(x/l))*(y/w)    

def DevS_x(x, y, l , w, i): #l y w son el ancho y el alto de cada elemento, no de la malla
    if  i==0: 
        return (-w + y) / (l* w)
    elif i==1: 
        return  (w-y)/(l*w)
    elif i==2:
        return  y/(l*w)
    elif i==3:
        return  -y/(l*w) 

def DevS_y(x, y, l , w, i): #l y w son el ancho y el alto de cada elemento, no de la malla
    if  i==0: 
        return (-l + x )/ (l*w)
    elif i==1:
        return  -x/(l*w)
    elif i==2:
        return x/(l*w)
    elif i==3:
        return (l-x) / (l*w)

#Funciones de Galerkin para un elemento de 4 nodos
def galerkinMethodRect(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i, totallenght, totalwidth, listaLadosConv):

    
    x=symbols('x')
    y=symbols('y')

    #Se define la función de temperatura aproximada, 
    #El argumento E son las temperaturas incognitas cuyos subindices dependen de
    #los nodos pertenecientes al elemento
    def Taprox(x, y, l, w, E):
        return E[0] + (x/l)*(E[1]-E[0]) + y/w *((E[3]+(x/l)*(E[2]-E[3])) - 
        (E[0]+(x/l)*(E[1]-E[0])))

    ''' CONSTRUCCION DE LA INTEGRAL: 
        integral(KxTerm + KyTerm + q)Sidxdy = 0  donde: 
        KxTerm = Kxterm1 + Kxterm2
        KyTerm = KyTerm1 + Kyterm2 '''

    
    
    EL=EL[i] #La lista de elementos entra como argumento, 
    #como la funcion soluciona para un elemento, solo se toma una lista (i) del arreglo de 
    # elementos 

    #Se genera una lista con las incoginitas correspondientes a la temperatura 
    #del nodo del elemento. El orden de solucion es antihorario 
    T=[]
    nodo=[]
    #Generación de la lista 
    for j in EL:
        T.append(symbols("T"+str(j)))
        nodo.append(j) #Se hace una lista con los numeros de los nodos (en orden)


    #Se genera un arreglo para el Kxterm1, donde cada entrada corresponde a un nodo.
    #Viene de aplicar las condiciones de equilibrio.
    #Inicialmente se asume que todos los lados tienen conveccion. 
    #Ademas se integra deacuerdo a la posicion del nodo en el elemento
    #Se evalua en su condicion en x
    Kxterm1 = [0, 0, 0, 0]
    
    Kxterm1[0] = -h* (1/6)*elemWidth*(-3*Tf+2*T[0]+T[3])
    Kxterm1[1] = -h* (1/6)*elemWidth*(-3*Tf+2*T[1]+T[2])
    Kxterm1[2] = -h* (1/6)*elemWidth*(-3*Tf+T[1]+2*T[2])
    Kxterm1[3] = -h* (1/6)*elemWidth*(-3*Tf+T[0]+2*T[3])

    #Se genera un arreglo para el Kyterm1, donde cada entrada corresponde a un nodo.
    #Viene de aplicar las condiciones de equilibrio.
    #Inicialmente se asume que todos los lados tienen conveccion. 
    #Ademas se integra deacuerdo a la posicion del nodo en el elemento
    #Se evalua en su condicion en y
    Kyterm1 = [0, 0, 0, 0]
    Kyterm1[0] = -h* (1/6)*elemLength*(-3*Tf+2*T[0]+T[1])
    Kyterm1[1] = -h* (1/6)*elemLength*(-3*Tf+T[0]+2*T[1])
    Kyterm1[2] = -h* (1/6)*elemLength*(-3*Tf+2*T[2]+T[3])
    Kyterm1[3] = -h* (1/6)*elemLength*(-3*Tf+T[2]+2*T[3])


    #print("h")
    #Kxterm2 se compone de 4 integrales (cada una por nodo). Es la relacion entre los 4 nodos del elemento en x
    Kxterm2=[0,0,0,0]
    for i in range (0, 4):
        A=T[0]*(dblquad(lambda x, y : (-kx*DevS_x(x,y,elemLength,elemWidth,0)*DevS_x(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])
        B=T[1]*(dblquad(lambda x, y : (-kx*DevS_x(x,y,elemLength,elemWidth,1)*DevS_x(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])
        C=T[2]*(dblquad(lambda x, y : (-kx*DevS_x(x,y,elemLength,elemWidth,2)*DevS_x(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])
        D=T[3]*(dblquad(lambda x, y : (-kx*DevS_x(x,y,elemLength,elemWidth,3)*DevS_x(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])


        #A=T[0]*integrate(integrate(-kx*DevS_x(x,y,elemLength,elemWidth,0)*DevS_x(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))
        #B=integrate(integrate(-kx*T[1]*DevS_x(x,y,elemLength,elemWidth,1)*DevS_x(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))
        #C=integrate(integrate(-kx*T[2]*DevS_x(x,y,elemLength,elemWidth,2)*DevS_x(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))
        #D=integrate(integrate(-kx*T[3]*DevS_x(x,y,elemLength,elemWidth,3)*DevS_x(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))

        sum = A+B+C+D

        Kxterm2[i] = sum

    
    #Kyterm2 se compone de 4 integrales (cada una por nodo). Es la relacion entre los 4 nodos del elemento en y
    Kyterm2=[0,0,0,0]
    for i in range (0, 4):
   
        A=T[0]*(dblquad(lambda x, y : (-ky*DevS_y(x,y,elemLength,elemWidth,0)*DevS_y(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])
        B=T[1]*(dblquad(lambda x, y : (-ky*DevS_y(x,y,elemLength,elemWidth,1)*DevS_y(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])
        C=T[2]*(dblquad(lambda x, y : (-ky*DevS_y(x,y,elemLength,elemWidth,2)*DevS_y(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])
        D=T[3]*(dblquad(lambda x, y : (-ky*DevS_y(x,y,elemLength,elemWidth,3)*DevS_y(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0])

        # A=integrate(integrate(-ky*T[0]*DevS_y(x,y,elemLength,elemWidth,0)*DevS_y(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))
        # B=integrate(integrate(-ky*T[1]*DevS_y(x,y,elemLength,elemWidth,1)*DevS_y(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))    
        # C=integrate(integrate(-ky*T[2]*DevS_y(x,y,elemLength,elemWidth,2)*DevS_y(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))
        # D=integrate(integrate(-ky*T[3]*DevS_y(x,y,elemLength,elemWidth,3)*DevS_y(x,y,elemLength,elemWidth,i),(x,0,elemLength)),(y,0,elemWidth))

        sum = A+B+C+D
        
        Kyterm2[i] = sum


    #print("y")
    #Termino q: termino independiente de la ecuacion del calor
    qterm = [0,0,0,0]
    for i in range (0, 4):
        qterm[i] = dblquad( lambda x, y : (q*Si(x,y,elemLength,elemWidth,i)),0, elemWidth, lambda x: 0, lambda x: elemLength)[0]


    #Reuniendo el Sistema de ecuaciones para cada nodo juntando los terminos Kxterm2, Kyterm2 y qterm
    #Se agrupa en una lista "eqSist"
    eqSist=[0,0,0,0]
    for i in range (0,4):
        eqSist[i]= Kxterm2[i] + Kyterm2[i] + qterm[i] 

        
    #Obteniendo el sistema de ecuaciones en forma matricial : (coeffMatrix)(Ti, Tn, Tj, Tm)trans + independentVector = 0
    # coeffMatrix, independentVector = linear_eq_to_matrix(eqSist, [T[0], T[1], T[2], T[3]])

        #Obteniendo el sistema de ecuaciones en forma matricial : (coeffMatrix)(Ti, Tn, Tj, Tm)trans + independentVector = 0

    #Se generan las matrices correspondientes. 
    #Mk genera la matriz con las ecuaciones en la lista eqSist con las incognitas correspondientes
    #Mq es el vector independiente
    Mk, Mq = linear_eq_to_matrix(eqSist, [T[0], T[1], T[2], T[3]])
    #Mx genera la matriz con las ecuaciones en la lista Kxterm1 con las incognitas correspondientes
    #Vx es el vector independiente
    Mx, Vx = linear_eq_to_matrix(Kxterm1, [T[0], T[1], T[2], T[3]])
    #My genera la matriz con las ecuaciones en la lista Kyterm1 con las incognitas correspondientes
    #Vy es el vector independiente
    My, Vy = linear_eq_to_matrix(Kyterm1, [T[0], T[1], T[2], T[3]])


    #Las matrices Mx, My y los vectores Vx y Vy dependen de 
    # las condiciones de convección en el nodo, por lo que 
    # se deben cancelar las columnas correspondientes 
    # donde no haya convección (flujo de calor) en esa dirección
    
    
    #Si hay un nodo en la frontera y no pertenece a las esquinas, no tendra flujo de calor en 
    #la direccion ortogonal al lado donde pertenece
    for i in range(0,4):

        #Para los nodos internos (sus coordenadas no estan en las fronteras) no existe convección.
        if(NL[EL[i]-1][0]!=0 and NL[EL[i]-1][0]!=totallenght and NL[EL[i]-1][1]!=0 and NL[EL[i]-1][1]!=totalwidth):
                Mx[i]=[0,0,0,0]
                Vx[i]=[0]
                My[i]=[0,0,0,0]
                Vy[i]=[0]

        # Para los nodos en la frontera en los lados i-n y j-m
        if(NL[EL[i]-1][0]==0 or NL[EL[i]-1][0]==totallenght):
            
            #codigo para cuando no hay conveccion en los lados externos. Falta complementar 
            if ( NL[EL[i]-1][0]==0  and listaLadosConv [3]== False): #Cuando es un nodo en i-n y no hay conveccion
                Mx[i]=[0,0,0,0]
                Vx[i]=[0]
            if ( NL[EL[i]-1][0]==totallenght  and listaLadosConv [1]== False): #Cuando es un nodo en j-m y no hay conveccion
                Mx[i]=[0,0,0,0]
                Vx[i]=[0]

            #Si el nodo no es una esquina: 
            if(NL[EL[i]-1][1]!=0 and NL[EL[i]-1][1]!=totalwidth):
                My[i]=[0,0,0,0]
                Vy[i]=[0]

        #Para los nodos en la frontera en los lados i-j y n-m
        if(NL[EL[i]-1][1]==0 or NL[EL[i]-1][1]==totalwidth):

            #codigo para cuando no hay conveccion en los lados externos. Falta complementar 
            if ( NL[EL[i]-1][1]==0  and listaLadosConv [0]== False): #Cuando es un nodo en i-n y no hay conveccion
                My[i]=[0,0,0,0]
                Vy[i]=[0]
            if ( NL[EL[i]-1][1]==totalwidth  and listaLadosConv [2]== False): #Cuando es un nodo en j-m y no hay conveccion
                My[i]=[0,0,0,0]
                Vy[i]=[0]

            if(NL[EL[i]-1][0]!=0 and NL[EL[i]-1][0]!=totallenght): #Si no es una esquina
                Mx[i]=[0,0,0,0]
                Vx[i]=[0]

   
    #Se reagrupan las matrices MK Mx y My teniendo en cuenta los ajustes de convección, al igual
    #que los terminos independientes
    coeffMatrix =Matrix(Mk+Mx+My)
    independentVector=Mq + Vx + Vy


    #Se convierte la matriz de coef en un dataframe
    dfelement=pd.DataFrame(np.matrix(coeffMatrix))
    #Se añade una columna con el termino independiente
    dfelement["indep"]=pd.DataFrame(np.matrix(independentVector))
    #Se agrega una columna con el numero del nodo 
    dfelement["nodo"]=pd.DataFrame(np.array(nodo))

    #Se renombran las columnas en terminos de la incognita correspondiente
    dfelement.rename(columns = {0: T[0],  1 :T[1], 2 :T[2], 3 :T[3] }, inplace = True)

    #La funcion retorna el dataframe correspondiente al elemento i
    return dfelement