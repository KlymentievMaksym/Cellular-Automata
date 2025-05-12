import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import copy

from Cell import Cell


def GetNeigbour(position, indexes, full_shape):
    neigbours_indexes = np.zeros_like(indexes)
    for pos_index in range(len(position)):
        neigbours_indexes[len(position) - 1 - pos_index] = (indexes[len(position) - 1 - pos_index] + position[pos_index]) % full_shape[pos_index]
    return neigbours_indexes


array = np.empty((40, 40), dtype=object)
for i in range(array.shape[0]):
    for j in range(array.shape[1]):
        array[i, j] = Cell()
dim = len(array.shape)

index = np.array([-1, 0, 1])
indexes = np.meshgrid(*list(index for _ in range(dim)))

for arr_index_x in range(array.shape[0]):
    for arr_index_y in range(array.shape[1]):
        center = (arr_index_x, arr_index_y)
        neigbours_indexes = GetNeigbour(center, indexes, array.shape)
        neigbours = array[*neigbours_indexes]
        array[*center].ConnectNeighbours(neigbours)
        array[*center].state = np.random.randint(-1, 2, 1)
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


def rule1(cell: Cell):
    if np.sum(cell.neighbours) > 2:
        cell.state = 0
    else:
        cell.state = 1


def count_on(neighbours: np.ndarray):
    count = 0
    for neighbour_row in range(neighbours.shape[0]):
        for neighbour_col in range(neighbours.shape[1]):
            if neighbour_row != neighbour_col:
                if neighbours[neighbour_row, neighbour_col] > 0:
                    count += 1
    return count


def rule2(cell: Cell):
    if cell.state == -1 and count_on(cell.neighbours) == 2:
        cell.state = 1
    elif cell.state == 0:
        cell.state == -1
    elif cell.state == 1:
        cell.state = 0

rules = [rule1, rule2]
rules = [rule2]
iterations = 10
save = []
for iteration in range(iterations):
    array_new = copy.deepcopy(array)
    print(array_new)
    for cell_row in range(array.shape[0]):
        for cell_col in range(array.shape[1]):
            for rule in rules:
                array_new[cell_row, cell_col] = array[cell_row, cell_col].ApplyRule(rule, array_new[cell_row, cell_col])
    array_show = array_new.astype(float)
    color = plt.imshow(array_show, cmap="Accent")
    plt.pause(0.1)
    array = copy.deepcopy(array_new)
plt.gcf().colorbar(color)
plt.show()
