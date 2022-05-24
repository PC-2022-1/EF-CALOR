import numpy as np
import matplotlib.pyplot as plt
import math
from numpy import ma
from scipy.spatial import Delaunay




#crear nodos
L=0.1
h=0.05
r=0.02


nb_element = 5



Nodes1= np.array([[0,0],[0,1],[1,0],[1,1]])
Nodes= []

for x in np.linspace(0,L,num=nb_element):
    for y in np.linspace(0,h,num=nb_element):
        Nodes.append([x,y])

points = np.array(Nodes)
#plt.plot(points[:,0],points[:,1],'o')
#print(Nodes)

#crear elementos
tri=Delaunay(points)

"""z = 50 * Z1
z[:5, :5] = -1
z = ma.masked_where(z <= 0, z)
"""
#plt.contourf(X, Y,z, locator = ticker.LogLocator())
plt.triplot(points[:,0],points[:,1],tri.simplices)
plt.plot(points[:,0],points[:,1],'o')
plt.show()






#exportar
nb_nodes= len(points)               #nodos en la malla
nb_elements= len(tri.simplices)     #elementos en la malla

print(tri.simplices)

file= open("malla.txt","w")
file.write(f"Nodos: {nb_nodes}\nElementos: {nb_elements}\n")
file.write(f"Lista de Nodos:\n")
for i,node in enumerate(Nodes):
    file.write(f"{i:5d} {node[0]:14.5f} {node[1]:14.5f}\n")
file.write(f"Lista de Elementos:\n")
for j,elem in enumerate(tri.simplices):
    file.write(f"{j:5d} {elem[0]:10d} {elem[1]:10d} {elem[2]:10d}\n")


file.close

