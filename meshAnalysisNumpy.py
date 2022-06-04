from matplotlib.axis import XAxis
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

# --------- Generation of Matrix Values -------- #
nx, ny = (5, 5)

# X - Values
X = np.linspace(0, 1, nx)

# Y - Values
Y = np.linspace(0, 2, ny)

# X, Y Mesh Values
xmesh, ymesh = np.meshgrid(X, Y)

# ----------- Plotting of Mesh Values ---------- #

# Generation of diagonals
xdiag = xmesh.copy().T
ydiag = ymesh.copy().T

# Formatting of y-Values for diagonals
for index, row in enumerate(ydiag):
    if index%2 != 0:
        row = row.tolist()
        ydiag[index] = np.array([0] + row[:-1])

# Formatting of output diagonals
xdiag, ydiag = xdiag[:, 1:], ydiag[:, 1:]

plt.plot(xmesh, ymesh, '-ob')
plt.plot(xmesh.T, ymesh.T, 'b')

plt.plot(xdiag, ydiag, 'r')   
plt.show()