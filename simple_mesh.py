import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import math
from numpy import ma
from scipy.spatial import Delaunay

#crear nodos
L=1
h=1


nb_element = 5


Nodes1= np.array([[0,0],[0,4],[4,0],[4,4]])
#plt.plot(Nodes1[:,0],Nodes1[:,1],'o')  #imprime las 4 esquinas
Nodes= []

for x in np.linspace(0,L,num=nb_element+1):
    for y in np.linspace(0,h,num=nb_element+1):
        Nodes.append([x,y])

points = np.array(Nodes)

print(points)
#print(len(points[:]))

#crear elementos


#----------------------------------------------------crear triangulos--------------------------------------------
a1 = [[i+j*(nb_element+1) , (i+1)+j*(nb_element+1) , i+(j+1)*(nb_element+1)] for i in range(nb_element) for j in range(nb_element)]
a2= [[(i+1)+(j+1)*(nb_element+1) , (i+1)+j*(nb_element+1) , i+(j+1)*(nb_element+1)] for i in range(nb_element) for j in range(nb_element)]
triang1 = tri.Triangulation((points[:,0]).flatten(), (points[:,1]).flatten(),a1)
triang2 = tri.Triangulation((points[:,0]).flatten(), (points[:,1]).flatten(),a2)
plt.triplot(triang1,color='red')
plt.triplot(triang2,color='red')


#plt.triplot(points[:,0],points[:,1],tri.simplices)     ##lineas diagonales
#plt.axhline(y=5, color='r', linestyle='-')
plt.plot(points[:,0],points[:,1],'.')
plt.show()




