# EF-CALOR

El presente código genera mallas triangulares con la finalidad de implementar el modelo de elementos finitos para la ecuacion de calor.

Se conoce el modelo de elementos finitos como el proceso de discretización de intervalos continuos o infinitos, con el fin de evaluar el comportamiento de un ente geométrico o estructura según el comportamiento de todas su partes finitas, a la unión de las partes se le llama malla, esta a su vez puede ser mas refinada o dividida en mas y mas elementos, lo que conllevará a una mayor precisión en la descripción de las soluciones.

El objetivo del modelo es dividir un problema complejo en partes mas simples para una mayor eficiencia computacional.

Los siguientes son links de documentación del modelo.

https://getfem-examples.readthedocs.io/en/latest/demo_unit_disk.html
https://fenicsproject.org/
https://sfepy.org/doc-devel/index.html

El siguiente link es para documentación teorica sobre la ecuación de calor

https://www.overfitting.net/2021/02/transferencia-de-calor-por-elementos_10.html

#GENERACIÓN DE MALLAS

#EJERICIO Y EJEMPLO TOMADO DE https://www.youtube.com/watch?v=Aua3eLpnGao PARA EL APRENDIZAJE Y CONSTRUCCION DE MALLAS

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

#1 Crear Nodos
#Nodos=np.array([[0,0],[0,1],[1,0],[1,1]])

Nodos=[]
#Creación de nodos en todo el rectángulo

#for x in np.linspace(0,L,num=nb_elemento):
#    for y in np.linspace(0,h,num=nb_elemento):
#        Nodos.append([x,y])

#1.2 Mostrar Nodos
puntos=np.array(Nodos)

plt.plot(puntos[:,0],puntos[:,1],"o")
plt.show()


#3  Crear Elementos

from scipy.spatial import Delaunay
tri = Delaunay(puntos)

#4  Visualización de la malla
plt.triplot(puntos[:,0], puntos[:,1], tri.simplices)
plt.plot(puntos[:,0], puntos[:,1], 'o')
plt.show()





