from numpy import *

# Inicialización de parametros:

f = lambda x : sin(pi/4 * x)
g1 = lambda t : 0*t
g2 = lambda t : exp(-pi^2 * t)

a, b, c, n, m = 2, .6, 4, 5, 78

# Analizar parametros y de U
h = a / (n-1)
k = b / (m-1)
r = c^2 * k / h^2
s = 1 - 2 * r
U = zeros(n, m)

V=linspace(0,b,m)


# Condiciones de Frontera
U[1, 1:m] = feval(g1,V)
U[n, 1:m] = feval(g2,V)

# Generar la primera fila
U[2:n-1, 1] = feval(f, h:h:(n-2)*h)'

# Generar las filas restantes de  U

for  j in range(1,n):
   for  i in range(1,n-1):
      U[i, j] = s * U(i, j-1) + r * (U(i-1, j-1) + U(i+1, j-1))

U = U.T