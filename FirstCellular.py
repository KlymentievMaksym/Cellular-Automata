import numpy as np

from tqdm import tqdm
from time import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# from pprint import pprint
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


size = 1000
every = 1
stages = 50
array = np.random.randint(0, stages + 1, size=(size, size))
array = np.random.randint(0, stages + 1, size=(1280, 1920))


def rules(array, x, y):
    x_00 = array[x][y]
    if x_00 > 0:
        array[x][y] -= 1
    else:
        array[x][y] = 50

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


def rules_vectorized(arr):
    # if np.random.rand() < 0.8:
    #     return np.where(arr > 0, np.clip(arr - 1, 0, stages), stages)
    # else:
    return np.where(arr < stages, np.clip(arr + 1, 0, stages), 0)

# Основний цикл з векторизованими правилами
for _ in tqdm(
        range(iterations),
        desc="Processing",
        unit="step",
        bar_format="{l_bar}{bar:40}{r_bar}",
        colour='cyan',
        total=iterations
):
    array = rules_vectorized(array)
    if iterations % every == 0:
        save.append(array.copy())
# rules_vec = np.vectorize(rules, excluded=[0])

# for iteration in tqdm(
#         range(iterations),
#         desc="Processing",
#         unit="step",
#         bar_format="{l_bar}{bar:40}{r_bar}",
#         colour='cyan',
#         total=iterations
# ):
#     array_to_change = array.copy()
#     # index_x = np.arange(array.shape[0], step=1)
#     # index_y = np.arange(array.shape[1], step=1)
#     # index_x, index_y = np.meshgrid(index_x, index_y)
#     for index_x in range(array.shape[0]):
#         for index_y in range(array.shape[1]):
#             rules(array_to_change, index_x, index_y)
#     array = array_to_change.copy()
#     save.append(array.copy())

fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
# fig.set_size_inches(1080, 1920)
# fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
# ax = plt.Axes(fig, [0., 0., 1., 1.])
ax = plt.axes([0., 0., 1., 1.])
ax.set_axis_off()
# fig.add_axes(ax)
# plt.axis('off')
automata = ax.imshow(array, cmap="binary", aspect='auto')
# plt.show()


def update(frame):
    # plt.title(f"Iter {frame}")
    automata.set_data(save[frame])
    return automata


# fig = plt.gcf()
anim = animation.FuncAnimation(fig=fig, func=update, frames=len(save), interval=100)
# plt.tight_layout(pad=0, rect=(0, 0, 0, 0))
anim.save(f"./Images/Hi{time()}.gif", dpi=100, fps=20)  #, savefig_kwargs={"bbox_inches":'tight',"transparent":True, "pad_inches":0}
# plt.show()
