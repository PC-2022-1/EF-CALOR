
# TEST-DIFERENCIAS FINITAS

Se implementa el metodo de diferencias finitas para resolver la ecuación del calor para dos timpos de condiciones:

- En el caso de diferencias finitas progresivas, se considera el problema del calor con condiciones espaciales & temporales para 1 variable (t, x)
- En el caso de diferencias finitas centradas, se considera el problema del calor estacionario con condiciones bidimensionales (x, y)
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
=======
# EF-CALOR


Se conoce el modelo de elementos finitos como el proceso de discretización de intervalos continuos o infinitos, con el fin de evaluar el comportamiento de un ente geométrico o estructura según el comportamiento de todas su partes finitas, a la unión de las partes se le llama malla, esta a su vez puede ser mas refinada o dividida en mas y mas elementos, lo que conllevará a una mayor precisión en la descripción de las soluciones.

_El objetivo del modelo es dividir un problema complejo en partes mas simples para una mayor eficiencia computacional._

## Documentación

Los siguientes son links de documentación del modelo.

- [GetFEM - Examples](https://getfem-examples.readthedocs.io/en/latest/demo_unit_disk.html)

- [Fenics Project](https://fenicsproject.org/)
- [Sfepy](https://sfepy.org/doc-devel/index.html)

_De igual forma tambien podemos encontrar en los siguientes Links información teórica sobre el método_

- [Transferencia de Calor por elementos](https://www.overfitting.net/2021/02/transferencia-de-calor-por-elementos_10.html)
- Johnson, C., 2012. Numerical solution of partial differential equations by the finite element
method. Dover Publications.
- Alberty, J., Carstensen, C. and Funken, S.A., 1999. Remarks around 50 lines of Matlab: short
finite element implementation. Numerical algorithms, 20(2), pp.117-137.

**PASOS A SEGUIR**

1. _Generacion de mallas_

2. _Generacion de matriz de rigidez_

3. _Resolver el sistema_

4. _Generar simulaciones y contrastar_
