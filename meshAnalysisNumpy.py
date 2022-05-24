from matplotlib.axis import XAxis
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

nx, ny = (5, 5)

X = np.linspace(0, 1, nx)

Y = np.linspace(0, 2, ny)

xmesh, ymesh = np.meshgrid(X, Y)

diags = np.zeros((nx, ny))

Trans = np.array([[1, 2, 0.5, 0.75, 1.], 
[0., 1, 0.5, 0.75, 1.],
[0., 0.25, 1, 6, 3],
[0., 0.25, 0.5, 1, 2],
[0., 8, 0.5, 0.75, 1]])

#ymesh =  ymesh@Trans

print(xmesh, '\n', ymesh)

plt.plot(xmesh, ymesh, '-ob')
plt.plot(np.transpose(xmesh), np.transpose(ymesh), 'b')

ymesh = ymesh.T

for index, row in enumerate(ymesh):
    if index%2 != 0:
        row = row.tolist()
        ymesh[index] = np.array([0] + row[:-1])

plt.plot(np.transpose(xmesh), np.transpose(ymesh.T), 'r')
plt.show()