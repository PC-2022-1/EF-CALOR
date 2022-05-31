# MESH BRANCH

En esta rama se situan los archivos para la generación de mallas, el cual es el primer paso en el algoritmo FEM


# Sobre genMesh.py y mesh.py

El archivo genMesh.py es el archivo principal ("main") donde se llama al archivo mesh.py en el cual se grafica y se genera la malla. 
Ejercicio y ejemplo tomado de https://www.youtube.com/watch?v=kIiVQirjvyo 

Librerias
numpy
matplotlib.pyplot

![image](https://user-images.githubusercontent.com/93160881/170480726-9567c8d4-b1c8-4b0f-b7a6-60fdcff18a64.png)
# Sobre simple_mesh.py: 

Ejercicio y ejemplo tomado de https://www.youtube.com/watch?v=Aua3eLpnGao para el aprendizaje y construcción de mallas.

Librerias
numpy
matplotlib.pyplot
math
scipy.spatial
Delaunay #Para la triangulación de la malla en conjunto de nodos

![image](https://user-images.githubusercontent.com/105617335/170422656-e824d89d-83e3-4b46-929a-41c9f0b70603.png)
#Medidas del objeto al cual se le generará malla
L=0.1
h=0.05
r=0.02
#Elementos o nodos en los ejes
nb_elemento=20

#1Creación de nodos en todo el rectángulo

#for x in np.linspace(0,L,num=nb_elemento):
    for y in np.linspace(0,h,num=nb_elemento):
        Nodos.append([x,y])

#2 Mostrar Nodos
puntos=np.array(Nodos)

plt.plot(puntos[:,0],puntos[:,1],"o")
plt.show()


#3  Crear Elementos

from scipy.spatial import Delaunay
tri = Delaunay(puntos)

#4  Creacion de hueco circular en la esquina

for x in np.linspace(0,L,num=nb_elemento):
    if(x<r):
        y0=math.sqrt(r**2-x**2)
        for y in np.linspace(y0,h,num=nb_elemento):
            Nodos.append([x,y])
            
    else:
        for y in np.linspace(0,h,num=nb_elemento): 
            Nodos.append([x,y])
            
#5  Refinamiento de figura circular
p=[]
r1=0.0195
for x in np.linspace(0,r1,10):
            p.append([x,math.sqrt(r1**2-x**2)])
            
#6 Crear un nuevo objeto sin la problematica de intersecciones en el circulo
malla=np.delete(tri.simplices,[0,153,154,21],0)


Elementos que que se intersectan en el circulo
tri.find_simplex(p) #función de scipy

#7  Visualización de la malla
plt.triplot(puntos[:,0], puntos[:,1], malla)
plt.plot(puntos[:,0], puntos[:,1], 'o')
plt.show()

![output_12_0](https://user-images.githubusercontent.com/105617335/170425055-5dcc3a9d-24e7-4f8e-8ccd-542dfa1a8137.png)

