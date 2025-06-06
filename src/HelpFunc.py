import numpy as np


def EnsureShape(array: np.ndarray, shape: tuple):
    for item_shape in range(len(shape)):
        if isinstance(shape[item_shape], int):
            try:
                if array.shape[item_shape] != shape[item_shape]:
                    raise Exception(f"Wrong shape! Expected {array.shape[item_shape]}, Received {shape[item_shape]}")
            except IndexError as e:
                print(e)
