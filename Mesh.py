import numpy as np
import matplotlib.pyplot as plt

def uniform_mesh(d1,d2,p,m,element_type):
    dimension = 2
    esquinas = np.array([[0,0],[d1,0],[0,d2],[d1,d2]]) #Arreglo de arreglos con las 4 esquinas
    print(esquinas)
    numeroDeNodos       =(p+1)*(m+1)
    numeroDeElementos   =p*m
    nodosPorElemento    =4 #La base son los cuadrados, por lo que inicialmente este numero es 4
            
    #----------------------NODOS---------------------------#
    listaNodos=np.zeros([numeroDeNodos,dimension])
    a = d1/p    #incremento horizontal #a= d1/p
    b = d2/m    #incremento vertical  #b= d2/m
    
    Nodes= []
    for y in np.linspace(0,d2,m+1):
        for x in np.linspace(0,d1,p+1):
            Nodes.append([x,y])

    listaNodos = np.array(Nodes)

    # n = 0       #permite ir por las filas en listaNodos
    # for i in range(1,m+2):
    #     for j in range(1,p+2):
    #         listaNodos[n,0] = 0 + (j-1)*a      #incrementos en x
    #         listaNodos[n,1] = 0 + (i-1)*b      #incrementos en y
    #         n+=1
    #     #print(listaNodos)
    
    #----------------------ELEMENTOS---------------------------#
    listaElementos = np.zeros([numeroDeElementos,nodosPorElemento])

    for i in range(1,m+1):
        for j in range(1,p+1):
            if j==1:
                listaElementos[(i-1)*p+j-1, 0] = (i-1)*(p+1) + j
                listaElementos[(i-1)*p+j-1, 1] = listaElementos[(i-1)*p+j-1, 0] +1
                listaElementos[(i-1)*p+j-1, 3] = listaElementos[(i-1)*p+j-1, 0] + (p+1)
                listaElementos[(i-1)*p+j-1, 2] = listaElementos[(i-1)*p+j-1, 3] + 1

            else:
                listaElementos[(i-1)*p+j-1, 0] = listaElementos[(i-1)*p+j-2, 1]
                listaElementos[(i-1)*p+j-1, 3] = listaElementos[(i-1)*p+j-2, 2]
                listaElementos[(i-1)*p+j-1, 1] = listaElementos[(i-1)*p+j-1, 0] + 1
                listaElementos[(i-1)*p+j-1, 2] = listaElementos[(i-1)*p+j-1, 3] + 1

    if element_type== 'TRIANGULO':
        nodosPorElementoNew=3
        numeroDeElementosNew=2*numeroDeElementos
        listaElementos_new=np.zeros([numeroDeElementosNew,nodosPorElementoNew])

        for i in range (1, numeroDeElementos+1):
            listaElementos_new[2*(i-1), 0]= listaElementos[i-1,0] 
            listaElementos_new[2*(i-1), 1]= listaElementos[i-1,1] 
            listaElementos_new[2*(i-1), 2]= listaElementos[i-1,2] 

            listaElementos_new[2*(i-1)+1, 0]= listaElementos[i-1,0] 
            listaElementos_new[2*(i-1)+1, 1]= listaElementos[i-1,2] 
            listaElementos_new[2*(i-1)+1, 2]= listaElementos[i-1,3]

        listaElementos=listaElementos_new

    listaElementos=listaElementos.astype(int) 
    
    return (listaNodos, listaElementos)


def graph_mesh(element_type,listaNodos,listaElementos):
    numeroDeNodos = np.size(listaNodos,0)
    numeroDeElementos = np.size(listaElementos,0)


    count = 1 #anotar el numero de nodos

    if element_type == 'CUADRADO':
        count2 = 1 #anotar el numero de listaElementos
        for j in range(0,numeroDeElementos):
            plt.annotate(count2, xy = ((listaNodos[listaElementos[j,0]-1,0]+listaNodos[listaElementos[j,1]-1,0]+listaNodos[listaElementos[j,2]-1,0]+listaNodos[listaElementos[j,3]-1,0])/4,
            (listaNodos[listaElementos[j,0]-1,1]+listaNodos[listaElementos[j,1]-1,1]+listaNodos[listaElementos[j,2]-1,1]+listaNodos[listaElementos[j,3]-1,1])/4), c ='blue')
            count2+=1
        #lineas del plot

        x0,y0 = listaNodos[listaElementos[:,0]-1,0] , listaNodos[listaElementos[:,0]-1,1]
        x1,y1 = listaNodos[listaElementos[:,1]-1,0] , listaNodos[listaElementos[:,1]-1,1]
        x2,y2 = listaNodos[listaElementos[:,2]-1,0] , listaNodos[listaElementos[:,2]-1,1]
        x3,y3 = listaNodos[listaElementos[:,3]-1,0] , listaNodos[listaElementos[:,3]-1,1]
        plt.plot(np.array([x0,x1]),np.array([y0,y1]), 'grey', linewidth=3)
        plt.plot(np.array([x1,x2]),np.array([y1,y2]), 'grey', linewidth=3)
        plt.plot(np.array([x2,x3]),np.array([y2,y3]), 'grey', linewidth=3)
        plt.plot(np.array([x3,x0]),np.array([y3,y0]), 'grey', linewidth=3)
        

    if element_type=='TRIANGULO':
        count2 = 1 #anotar el numero de listaElementos
        for j in range(0,numeroDeElementos):
            plt.annotate(count2, xy = ((listaNodos[listaElementos[j,0]-1,0]+listaNodos[listaElementos[j,1]-1,0]+listaNodos[listaElementos[j,2]-1,0])/3,
            (listaNodos[listaElementos[j,0]-1,1]+listaNodos[listaElementos[j,1]-1,1]+listaNodos[listaElementos[j,2]-1,1])/3), c ='blue')
            count2+=1
        #lineas del plot

        x0,y0 = listaNodos[listaElementos[:,0]-1,0] , listaNodos[listaElementos[:,0]-1,1]
        x1,y1 = listaNodos[listaElementos[:,1]-1,0] , listaNodos[listaElementos[:,1]-1,1]
        x2,y2 = listaNodos[listaElementos[:,2]-1,0] , listaNodos[listaElementos[:,2]-1,1]
        plt.plot(np.array([x0,x1]),np.array([y0,y1]), 'grey', linewidth=3)
        plt.plot(np.array([x1,x2]),np.array([y1,y2]), 'grey', linewidth=3)
        plt.plot(np.array([x2,x0]),np.array([y2,y0]), 'grey', linewidth=3)
        

    for i in range(0, numeroDeNodos):
        plt.annotate(count, xy =([listaNodos[i,0],listaNodos[i,1]]))
        plt.plot(listaNodos[i,0],listaNodos[i,1], 'ok')
        count+=1

    plt.show()