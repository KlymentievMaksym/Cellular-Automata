import numpy as np
import numba


USE_NUMBA = True


def maybe_numba(use_numba):
    def decorator(func):
        return numba.njit(func) if use_numba else func
    return decorator


@maybe_numba(USE_NUMBA)
def count_(lst: np.ndarray, count: int):
    return np.count_nonzero(lst == count)


def RuleEmpty(array: np.ndarray, neighbours_cells: np.ndarray, stages: int, *args, **kwargs):
    pass


@maybe_numba(USE_NUMBA)
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


def Rule110_2d(array: np.ndarray, neighbours_cells: np.ndarray, stages: int, *args, **kwargs):
    _Rule110_2d(array)


@maybe_numba(USE_NUMBA)
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


@maybe_numba(USE_NUMBA)
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


@maybe_numba(USE_NUMBA)
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


@maybe_numba(USE_NUMBA)
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


@maybe_numba(USE_NUMBA)
def _MelodySpread(array):
    new_array = np.zeros_like(array)
    rows, cols = array.shape
    for i in range(rows):
        for j in range(cols):
            if array[i, j] == 1:
                new_array[i, j] = 1
                if j + 1 < cols:
                    if np.random.rand() < 0.4:
                        new_array[i, j + 1] = 1
                    if i > 0 and np.random.rand() < 0.2:
                        new_array[i - 1, j + 1] = 1
                    if i < rows - 1 and np.random.rand() < 0.2:
                        new_array[i + 1, j + 1] = 1
    return new_array


def MelodySpread(array: np.ndarray, neighbours_cells: np.ndarray, *args, **kwargs):
    array[:] = _MelodySpread(array)


@maybe_numba(USE_NUMBA)
def _RuleM1(array: np.ndarray, h_prob: float = 0.7, mut_prob: float = 0.5):
    for y in range(array.shape[1]):
        if array[2, y] != 0 and array[0, y] == 0:
            array[0, y + 1] = 1
        if y != 0 and array[0, y] == 0 and array[0, y-1] == 0:
            array[1, y + 1] = 1
        if array[0, y] != 0 and array[1, y] != 0 and np.random.rand() < h_prob:
            array[2, y] = 1
        if np.random.rand() < mut_prob:
            instrument_index = np.random.randint(0, array.shape[0])
            array[instrument_index, y] = 1 - array[instrument_index, y]
    # Rule: If a hi-hat is ON and the kick is OFF at a position, turn ON the kick in the next position.
    # Rule: If a kick is OFF in two consecutive positions, turn ON the snare in the next position. Similarly, if a snare is OFF in two consecutive positions, turn ON the kick in the next position.
    # Rule: If both kick and snare are ON at a position, turn ON the hi-hat at the same position with a probability determined by HIHAT_ON_PROBABILITY.
    # Rule: At each position, with a small probability (MUTATION_PROBABILITY), randomly toggle the state (ON/OFF) of one of the instruments (kick, snare, hi-hat).


def RuleM1(array: np.ndarray, neighbours_cells: np.ndarray, *args, **kwargs):
    _RuleM1(array, kwargs.get("h_prob", 0.7), kwargs.get("mut_prob", 0.5))
