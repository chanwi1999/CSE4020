import numpy as np

M = np.arange(2,27)
print(M)
print("\n")

M = M.reshape(5,5)
print(M)
print("\n")

M[1:4,1:4] = 0
print(M)
print("\n")

M = M@M
print(M)
print("\n")

v = M[0,]
v = v*v
x = 0
for i in range(0,5):
		x = x+v[i]
print(np.sqrt(x))
