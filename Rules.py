import numpy as np
import numba


@numba.njit
def count_(lst: np.ndarray, count: int):
    return np.count_nonzero(lst == count)


@numba.njit
def _Rule110_2d(array: np.ndarray):
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            x_10 = array[x - 2][y-1]
            x_11 = array[x - 1][y-1]
            x_12 = array[x][y-1]
            if x_10 == 1 and x_11 == 1 and x_12 == 1:
                array[x - 1][y-1] = 0
            elif x_10 == 0 and x_11 == 0 and x_12 == 0:
                array[x - 1][y-1] = 0
            elif x_10 == 1 and x_11 == 0 and x_12 == 0:
                array[x - 1][y-1] = 0
            else:
                array[x - 1][y-1] = 1


def Rule110_2d(array: np.ndarray, *args, **kwargs):
    _Rule110_2d(array)


@numba.njit
def _Rule2(array: np.ndarray, stages: int):
    # stages = kwargs.get("stages", 0)
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            x_00 = array[x][y]
            if x_00 > 0:
                array[x][y] -= 1
            else:
                array[x][y] = stages


def Rule2(array: np.ndarray, neighbours_cells: np.ndarray, stages: int, *args, **kwargs):
    _Rule2(array, stages)


def Rule2_vec(array: np.ndarray, neighbours_cells: np.ndarray, stages: int):
    # stages = kwargs.get("stages", 0)
    return np.where(array > 0, np.clip(array - 1, 0, stages), stages)


@numba.njit
def _BriansBrain(array: np.ndarray, neighbours_cells: np.ndarray):
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            neighbour = neighbours_cells[x, y]
            neighbour = np.delete(neighbour.flatten(), 4)
            if array[x, y] == 0 and count_(neighbour, 2) == 2:
                array[x, y] = 2
            elif array[x, y] == 2:
                array[x, y] = 1
            else:
                array[x, y] = 0


def BriansBrain(array: np.ndarray, neighbours_cells: np.ndarray, *args, **kwargs):
    _BriansBrain(array, neighbours_cells)


BriansBrain_vec = np.vectorize(_BriansBrain, excluded=(0, "array"), signature="(), (), (a, b) -> ()")


@numba.njit
def _Rule3(array: np.ndarray, neighbours_cells: np.ndarray):
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            neighbour = neighbours_cells[x, y]
            neighbour = np.delete(neighbour.flatten(), 4)
            if array[x, y] == 0 and (count_(neighbour, 2) == 2 or count_(neighbour, 1) == 1):
                array[x, y] = 2
            elif array[x, y] == 2:
                array[x, y] = 1
            else:
                array[x, y] = 0


def Rule3(array: np.ndarray, neighbours_cells: np.ndarray, *args, **kwargs):
    _Rule3(array, neighbours_cells)


@numba.njit
def _GameOfLife(array: np.ndarray, neighbours_cells: np.ndarray):
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            neighbour = neighbours_cells[x, y]
            neighbour = np.delete(neighbour.flatten(), 4)
            cnt = count_(neighbour, 1)
            if array[x, y] == 0 and (cnt == 3):
                array[x, y] = 1
            elif array[x, y] == 1 and (cnt == 2 or cnt == 3):
                array[x, y] = 1
            else:
                array[x, y] = 0


def GameOfLife(array: np.ndarray, neighbours_cells: np.ndarray, *args, **kwargs):
    _GameOfLife(array, neighbours_cells)
