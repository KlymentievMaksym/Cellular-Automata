import numpy as np

from tqdm import tqdm
from time import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from pprint import pprint
# import copy
# from Cell import Cell


def GetNeigbour(position: np.ndarray, indexes: np.ndarray, full_shape: tuple):
    neigbours_indexes = np.zeros_like(indexes)
    for pos_index in range(len(position)):
        neigbours_indexes[len(position) - 1 - pos_index] = (indexes[len(position) - 1 - pos_index] + position[pos_index]) % full_shape[pos_index]
    return neigbours_indexes


# def GetNeigbour(position: list, array: list, full_shape: list):
#     indexes = [-1, 0, 1]

#     neigbours = []

#     for nx in indexes:
#         for ny in indexes:
#             x = position[0] + nx
#             y = position[1] + ny
#             if (x >= 0 and x < full_shape[0]) and (y >= 0 and y < full_shape[1]) and (x != position[0] or y != position[1]):
#                 neigbours.append(array[x % full_shape[0]][y % full_shape[1]])
#             # if (x != position[0] or y != position[1]):
#             #     neigbours.append(array[x % full_shape[0]][y % full_shape[1]])
#     return neigbours

def GetAllNeigbours(array: np.ndarray):
    narray = np.pad(array, 1, mode="constant", constant_values=0)
    narray = array.copy()
    shifts = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    neighbours = []
    print(array)
    for dx, dy in shifts:
        if dx == -1 and dy == -1:
            arr = np.concatenate((narray[None, -1, :-1], narray[:-1, :-1]))
            print(arr)
            temp = narray[:-1, -1].copy()
            narray[0, -1], narray[1:, -1] = narray[-1, -1], temp
            arr = np.column_stack((narray[:, -1], arr))
            print(arr)
            # neighbours.append(array)
        # neighbours.append(narray[1+dx:1+dx+array.shape[0], 1+dy:1+dy+array.shape[1]])
    # print(array)
    # pprint(neighbours)
    # neighbours = np.stack(neighbours, axis=0)
    return neighbours


size = 4
every = 1
stages = 2
array = np.random.randint(0, stages, size=(size, size))
neighbours = GetAllNeigbours(array)

print(array.shape)
print(neighbours.shape)
# array = np.random.randint(0, stages, size=(1280, 1920))


# def rules(array, x, y):
#     x_00 = array[x][y]
#     if x_00 > 0:
#         array[x][y] -= 1
#     else:
#         array[x][y] = 50

# def rules(array, x, y):
#     x_10 = array[x - 2][y-1]
#     x_11 = array[x - 1][y-1]
#     x_12 = array[x][y-1]
#     if x_10 == 1 and x_11 == 1 and x_12 == 1:
#         array[x - 1][y-1] = 0
#     elif x_10 == 0 and x_11 == 0 and x_12 == 0:
#         array[x - 1][y-1] = 0
#     elif x_10 == 1 and x_11 == 0 and x_12 == 0:
#         array[x - 1][y-1] = 0
#     else:
#         array[x - 1][y-1] = 1


iterations = 100
save = []


# def rules_vectorized(arr):
#     return np.where(arr > 0, np.clip(arr - 1, 0, stages), stages)


for _ in tqdm(
        range(iterations),
        desc="Processing",
        unit="step",
        bar_format="{l_bar}{bar:40}{r_bar}",
        colour='cyan',
        total=iterations
):
    # array = rules_vectorized(array)
    if iterations % every == 0:
        save.append(array.copy())

# fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
# ax = plt.axes([0., 0., 1., 1.])
# ax.set_axis_off()
# automata = ax.imshow(array, cmap="binary", aspect='auto')


# def update(frame):
#     # plt.title(f"Iter {frame}")
#     automata.set_data(save[frame])
#     return automata


# anim = animation.FuncAnimation(fig=fig, func=update, frames=len(save), interval=100)
# anim.save(f"./Images/Hi{time()}.gif", dpi=100, fps=20)  #, savefig_kwargs={"bbox_inches":'tight',"transparent":True, "pad_inches":0}
# plt.show()
