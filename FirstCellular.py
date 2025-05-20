import numpy as np

from numba import njit

from tqdm import tqdm
from time import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

from pprint import pprint
# import copy
import Rules


def GetAllNeigbours(array: np.ndarray):
    neighbours = np.pad(array, pad_width=1, mode="wrap")
    neighbours = np.lib.stride_tricks.sliding_window_view(neighbours, (3, 3))
    return neighbours


size = 800
every = 1
stages = 55
array = np.random.randint(0, stages, size=(size, size))
array = np.random.randint(0, stages, size=(1280, 1920))
neighbours = GetAllNeigbours(array)

iterations = 300
start_from = 30
save = []
sav = True

index_x, index_y = np.meshgrid(np.arange(array.shape[0], step=1), np.arange(array.shape[1], step=1))
for iteration in tqdm(
        range(iterations),
        desc="Processing",
        unit="step",
        bar_format="{l_bar}{bar:40}{r_bar}",
        colour='cyan',
        total=iterations
):

    # Rules.BriansBrain_vec(array, index_x, index_y, neighbours)
    array = Rules.Rule2_vec(array, stages)
    # for nx in range(array.shape[0]):
    #     for ny in range(array.shape[1]):
            # Rules.Rule110_2d(array, nx, ny)
            # Rules.BriansBrain(array, nx, ny, neighbours[nx, ny])
    neighbours = GetAllNeigbours(array)
    # array = rules_vectorized(array)
    if iteration % every == 0 and iteration > start_from:
        save.append(array.copy())

# if sav:
fig, ax = plt.subplots(1, figsize=(19.2, 10.8))
# else:
# fig, ax = plt.subplots(1, figsize=(6, 6))
fig.subplots_adjust(0, 0, 1, 1)
ax.set_axis_off()
# cmap = ListedColormap(['red', 'purple', 'green'])
automata = ax.imshow(save[0], cmap="PuRd", aspect='auto')


def update(frame):
    # plt.title(f"Iter {frame}")
    automata.set_data(save[frame])
    return automata


anim = animation.FuncAnimation(fig=fig, func=update, frames=len(save), interval=100)
if sav:
    anim.save(f"./Images/Hi{time()}.gif", dpi=100, fps=20)  #, savefig_kwargs={"bbox_inches":'tight',"transparent":True, "pad_inches":0}
else:
    plt.show()
