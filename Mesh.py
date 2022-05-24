import numpy as np
import matplotlib.pyplot as plt

def uniform_mesh(d1,d2,p,m,element_type):
    PD=2
    q=np.array([[0,0],[d1,0],[0,d2],[d1,d2]]) #4 esquinas
    numeroDeNodos= (p+1)*(m+1)
    numeroDeElementos= p*m
    nodosPorElemento=4
            ##Nodos##
    NL=np.zeros([numeroDeNodos,PD])
    a= (q[1,0]-q[0,0])/p    #incremento horizontal #a= d1/p
    b= (q[2,1]-q[0,1])/m    #incremento vertical  #b= d2/m
    
    
    n= 0                    #permite ir por las filas en NL
    for i in range(1,m+2):
        for j in range(1,p+2):
            NL[n,0] = q[0,0] + (j-1)*a      #incrementos en x
            NL[n,1] = q[0,1] + (i-1)*b      #incrementos en y
            n+=1

           ##elementos##
    EL= np.zeros([numeroDeElementos,nodosPorElemento])

    for i in range(1,m+1):
        for j in range(1,p+1):

            if j==1:
                EL[(i-1)*p+j-1, 0] = (i-1)*(p+1) + j
                EL[(i-1)*p+j-1, 1] = EL[(i-1)*p+j-1, 0] +1
                EL[(i-1)*p+j-1, 3] = EL[(i-1)*p+j-1, 0] + (p+1)
                EL[(i-1)*p+j-1, 2] = EL[(i-1)*p+j-1, 3] + 1

            else:
                EL[(i-1)*p+j-1, 0] = EL[(i-1)*p+j-2, 1]
                EL[(i-1)*p+j-1, 3] = EL[(i-1)*p+j-2, 2]
                EL[(i-1)*p+j-1, 1] = EL[(i-1)*p+j-1, 0] + 1
                EL[(i-1)*p+j-1, 2] = EL[(i-1)*p+j-1, 3] + 1

    if element_type== 'TRIANGULO':
        nodosPorElementoNew=3
        numeroDeElementosNew=2*numeroDeElementos
        EL_new=np.zeros([numeroDeElementosNew,nodosPorElementoNew])

        for i in range (1, numeroDeElementos+1):
            EL_new[2*(i-1), 0]= EL[i-1,0] 
            EL_new[2*(i-1), 1]= EL[i-1,1] 
            EL_new[2*(i-1), 2]= EL[i-1,2] 

            EL_new[2*(i-1)+1, 0]= EL[i-1,0] 
            EL_new[2*(i-1)+1, 1]= EL[i-1,2] 
            EL_new[2*(i-1)+1, 2]= EL[i-1,3]

        EL=EL_new

    EL=EL.astype(int) 
    
    return (NL, EL)


def graph_mesh(element_type,NL,EL):
    numeroDeNodos = np.size(NL,0)
    numeroDeElementos = np.size(EL,0)


    count = 1 #anotar el numero de nodos

    if element_type == 'CUADRADO':
        count2 = 1 #anotar el numero de elementos
        for j in range(0,numeroDeElementos):
            plt.annotate(count2, xy = ((NL[EL[j,0]-1,0]+NL[EL[j,1]-1,0]+NL[EL[j,2]-1,0]+NL[EL[j,3]-1,0])/4,
            (NL[EL[j,0]-1,1]+NL[EL[j,1]-1,1]+NL[EL[j,2]-1,1]+NL[EL[j,3]-1,1])/4), c ='blue')
            count2+=1
        #lineas del plot

        x0,y0 = NL[EL[:,0]-1,0] , NL[EL[:,0]-1,1]
        x1,y1 = NL[EL[:,1]-1,0] , NL[EL[:,1]-1,1]
        x2,y2 = NL[EL[:,2]-1,0] , NL[EL[:,2]-1,1]
        x3,y3 = NL[EL[:,3]-1,0] , NL[EL[:,3]-1,1]
        plt.plot(np.array([x0,x1]),np.array([y0,y1]), 'grey', linewidth=3)
        plt.plot(np.array([x1,x2]),np.array([y1,y2]), 'grey', linewidth=3)
        plt.plot(np.array([x2,x3]),np.array([y2,y3]), 'grey', linewidth=3)
        plt.plot(np.array([x3,x0]),np.array([y3,y0]), 'grey', linewidth=3)
        

    if element_type=='TRIANGULO':
        count2 = 1 #anotar el numero de elementos
        for j in range(0,numeroDeElementos):
            plt.annotate(count2, xy = ((NL[EL[j,0]-1,0]+NL[EL[j,1]-1,0]+NL[EL[j,2]-1,0])/3,
            (NL[EL[j,0]-1,1]+NL[EL[j,1]-1,1]+NL[EL[j,2]-1,1])/3), c ='blue')
            count2+=1
        #lineas del plot

        x0,y0 = NL[EL[:,0]-1,0] , NL[EL[:,0]-1,1]
        x1,y1 = NL[EL[:,1]-1,0] , NL[EL[:,1]-1,1]
        x2,y2 = NL[EL[:,2]-1,0] , NL[EL[:,2]-1,1]
        plt.plot(np.array([x0,x1]),np.array([y0,y1]), 'grey', linewidth=3)
        plt.plot(np.array([x1,x2]),np.array([y1,y2]), 'grey', linewidth=3)
        plt.plot(np.array([x2,x0]),np.array([y2,y0]), 'grey', linewidth=3)
        

    for i in range(0, numeroDeNodos):
        plt.annotate(count, xy =([NL[i,0],NL[i,1]]))
        plt.plot(NL[i,1],NL[i,0], 'ok')
        count+=1

    plt.show()