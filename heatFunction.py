
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

def stima3(vertices):
    d  = np.size(vertices, 1)

    G1 = np.vstack((np.ones((1,d+1)),vertices.transpose()))  
    G2 = np.vstack((np.zeros((1,d)),np.eye(d)))
    G = np.linalg.solve(G1, G2)

    MM=np.linalg.det(np.vstack((np.ones((1,d+1)),vertices.transpose())))*G
    MM=np.dot(MM,G.transpose())
    M=MM / np.prod([i for i in range (0,d)])    

    return M

def stima4(vertices):

    D_phi = np.vstack((vertices[1,:] - vertices[0,:], vertices[3,:] - vertices[0,:]))
    D_phiTrans = D_phi.transpose()
   
    B = np.linalg.inv (D_phiTrans @ D_phi )

    C1matrix= [[[2, -2],[-2,2]], [[3, 0],[0,-3]],  [[2, 1],[1,2]] ]

    C1 = np.array(C1matrix[0]) * B[0,0] + np.array(C1matrix[1]) * B[0,1] + np.array(C1matrix[2]) * B[1,1] 

    C2matrix= [[[-1, 1],[1,-1]], [[-3, 0],[0,3]],  [[-1, -2],[-2,-1]] ]
    C2 = np.matrix(C2matrix[0]) * B[0,0] + np.matrix(C2matrix[1]) * B[0,1] + np.matrix(C2matrix[2]) * B[1,1] 

    M = (np.linalg.det(D_phiTrans) * np.vstack((np.hstack((C1, C2)), np.hstack((C2, C1))))) / 6
    return M


def f(u): 
    value = np.ones((np.size(u.reshape(1,2), 0), 1))
    return value

def g(u): 
    value = np.zeros((np.size(u, 0), 1))
    return value

def u_d(u):
    w = u.copy()
    w = w[:, 0] * w[:, -1]
    w = w.reshape(np.zeros((np.size(u, 0), 1)).shape)
    f = lambda x : np.tan(x)
    value = f(w)
    return value

def show(elements4, coordinates, u):
    
    fig = plt.figure()
    ax = fig.add_subplot(projection= '3d')

    X, Y = coordinates[:, 0], coordinates[:, -1]
    result = ax.plot_trisurf(X, Y, u, triangles= elements4, linewidth=0.2,  cmap='jet')

    fig.colorbar(result)

    plt.show()