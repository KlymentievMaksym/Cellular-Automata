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
array = np.random.randint(0, 2, size=(size,))
# print(np.unique_counts(array))
dim = len(array.shape)
index = np.array([-1, 0, 1])
# indexes = np.meshgrid(*list(index for _ in range(dim)))
print(array[None, :])
plt.axis('off')
automata = plt.imshow(array[None, :], cmap="cool")
# plt.show()


def rules(array, x):
    if array[x - 1] == 1 and array[x] == 1 and array[(x + 1) % array.shape[0]] == 1:
        array[x] = 0
    elif array[x - 1] == 0 and array[x] == 0 and array[(x + 1) % array.shape[0]] == 0:
        array[x] = 0
    elif array[x - 1] == 1 and array[x] == 0 and array[(x + 1) % array.shape[0]] == 0:
        array[x] = 0
    else:
        array[x] = 1


iterations = 100
save = []

for iteration in tqdm(
        range(iterations),
        desc="Processing",
        unit="step",
        bar_format="{l_bar}{bar:40}{r_bar}",
        colour='cyan',
        total=iterations
):
    array_to_change = array.copy()
    for index_x in range(array.shape[0]):
        rules(array_to_change, index_x)
    array = array_to_change.copy()
    save.append(array)


def update(frame):
    plt.title(f"Iter {frame}")
    automata.set_data(save[frame][None, :])
    return automata


anim = animation.FuncAnimation(fig=plt.gcf(), func=update, frames=len(save), interval=100, repeat=True)
# anim.save(f"Hi{time()}.gif", fps=30)
plt.show()

# def count_on(array, x, y, what_count):
#     # counts = 0
#     # counts = np.unique_counts(array[*GetNeigbour([x, y], indexes, array.shape)])
#     neigbours = array[*GetNeigbour([x, y], indexes, array.shape)]
#     counts = np.unique_counts(neigbours)
#     # for neighbour in neighbours:
#     #     if neighbour > 1:
#     #         count += 1
#     # print(counts.counts[what_count])
#     return counts._asdict().get(what_count, 0)


# def rule1(array, x, y):
#     # count_on(array, x, y, 1) > 2
#     if array[x, y] == 0 and count_on(array, x, y, 2) == 2:
#         array[x, y] = 2
#     elif array[x, y] == 2:
#         array[x, y] = 1
#     elif array[x, y] == 1:
#         array[x, y] = 0


# rules = [rule1]
# iterations = 10
# save = []

# # rule1(array, 1, 1)

# plt.axis('off')
# automata = plt.imshow(array, "cool")
# color = plt.gcf().colorbar(automata)
# states = np.max(array) - np.min(array)
# color.set_ticks(range(0, states + 1))
# color.set_ticklabels([str(i) for i in range(0, states + 1)])

# for iteration in tqdm(
#         range(iterations),
#         desc="Processing",
#         unit="step",
#         bar_format="{l_bar}{bar:40}{r_bar}",
#         colour='cyan',
#         total=iterations
# ):
#     array_to_change = array.copy()
#     for index_x in range(array.shape[0]):
#         for index_y in range(array.shape[1]):
#             for rule in rules:
#                 rule(array_to_change, index_x, index_y)
#     array = array_to_change.copy()
#     save.append(array)


# def update(frame):
#     # plt.title(f"Iter {frame}")
#     automata.set_data(save[frame])
#     return automata


# anim = animation.FuncAnimation(fig=plt.gcf(), func=update, frames=len(save), interval=300, repeat=True)
# # anim.save(f"Hi{time()}.gif", fps=30)
# plt.show()


# neigbours_index_array = np.zeros((size, size, 2, 8))
# array = np.zeros((size,) * 2)
# print(neigbours_index_array)
# array = [[Cell() for _ in range(size)] for _ in range(size)]
# arr = [[0 for _ in range(size)] for _ in range(size)]
# dim_x = len(array)
# dim_y = len(array[0])
# shape = (dim_x, dim_y)

# for index_x in range(dim_x):
#     for index_y in range(dim_y):
#         center = (index_x, index_y)
#         array[index_x][index_y].ConnectNeighbours(GetNeigbour(center, array, shape))
#         array[index_x][index_y].state = np.random.randint(0, 3)
#         arr[index_x][index_y] = array[index_x][index_y].state


# def count_on(neighbours: list):
#     count = 0
#     for neighbour in neighbours:
#         if neighbour > 1:
#             count += 1
#     return count


# def rule1(cell: Cell):
#     if cell.state == 0 and count_on(cell.neighbours) > 1:
#         cell.state = 2
#     elif cell.state == 2:
#         cell.state = 1
#     elif cell.state == 1:
#         cell.state = 0


# rules = [rule1]
# iterations = 300
# save = []
# for iteration in tqdm(
#         range(iterations),
#         desc="Processing",
#         unit="step",
#         bar_format="{l_bar}{bar:40}{r_bar}",
#         colour='cyan',
#         total=iterations
# ):
#     for cell_row in array:
#         for cell in cell_row:
#             # print(cell)
#             for rule in rules:
#                 cell.ApplyRule(rule)
#     # print(array)
#     for index_x in range(dim_x):
#         for index_y in range(dim_y):
#             arr[index_x][index_y] = array[index_x][index_y].state
#     # print(arr)
#     save.append(copy.deepcopy(arr))
#     # print(save)

# plt.axis('off')
# automata = plt.imshow(arr, "cool")
# # color = plt.gcf().colorbar(automata)
# # color.set_ticks(range(0, 2 + 1))
# # color.set_ticklabels([str(i) for i in range(0, 2 + 1)])


# def update(frame):
#     # plt.title(f"Iter {frame}")
#     automata.set_data(save[frame])
#     return automata


# anim = animation.FuncAnimation(fig=plt.gcf(), func=update, frames=len(save), interval=300, repeat=True)
# anim.save(f"Hi{time()}.gif", fps=30)
# plt.show()

#     plt.title(f"Iter {iteration}")
#     color = plt.imshow(arr, cmap="cool")
#     plt.pause(0.01)
# color = plt.gcf().colorbar(color)
# color.set_ticks(range(0, 2 + 1))
# color.set_ticklabels([str(i) for i in range(0, 2 + 1)])
# plt.show()

# array = np.empty((40, 40), dtype=object)
# for i in range(array.shape[0]):
#     for j in range(array.shape[1]):
#         array[i, j] = Cell()
# dim = len(array.shape)

# index = np.array([-1, 0, 1])
# indexes = np.meshgrid(*list(index for _ in range(dim)))

# for arr_index_x in range(array.shape[0]):
#     for arr_index_y in range(array.shape[1]):
#         center = (arr_index_x, arr_index_y)
#         neigbours_indexes = GetNeigbour(center, indexes, array.shape)
#         neigbours = array[*neigbours_indexes]
#         array[*center].ConnectNeighbours(neigbours)
#         array[*center].state = np.random.randint(-1, 2, 1)
# print(*center)
# print(array[*center])

# print()
# print(array[1, 1])
# print(array[1, 2].neighbours)
# print(type(array[1, 1]))
# print(array)
# print()
# array_show = np.array(array, dtype=float)
# plt.imshow(array_show)
# plt.show()


# def rule1(cell: Cell):
#     if np.sum(cell.neighbours) > 2:
#         cell.state = 0
#     else:
#         cell.state = 1