import numpy as np

ar = np.zeros((4, 4))
x = np.arange(4)
ar[:] = x[:, None] - x[None, :]
# index = np.array([1, 2, 3])
# print(ar)
# print(index)
# print(-index)
# print(ar[index, -index])
index = np.array([-1, 0, 1])
index1, index2 = np.meshgrid(index, index)
for x in range(ar.shape[0]):
    for y in range(ar.shape[1]):
        print(ar[index1 + x - 1, index2 + y - 1])

# print(ar)
# print(index1)
# print(index2)
# print(ar[index1, index2])
# print()
