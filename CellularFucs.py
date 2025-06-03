import numpy as np

from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib.animation as animation


def GetAllNeigbours(array: np.ndarray, Type: str = "Moore"):
    match len(array.shape):
        case 1:
            raise NotImplementedError
        case 2:
            match Type.lower():
                case "moore":
                    neighbours = np.pad(array, pad_width=1, mode="wrap")
                    neighbours = np.lib.stride_tricks.sliding_window_view(neighbours, (3, 3))
                    return neighbours
                case _:
                    raise NotImplementedError
        case _:
            raise NotImplementedError


def GenerateArray(sizes: tuple[int], stages: int) -> np.ndarray:
    # size = 800
    # stages = 55
    array_cells = np.random.randint(0, stages, size=sizes)
    # array = np.random.randint(0, stages, size=(1280, 1920))
    return array_cells


def ApplyRulesAndSaveHistory(array_cells: np.ndarray, iterations: int, rule_to_apply: callable, every_nth: int = 1, start_animation_from: int = 0, do_save: bool = False, **kwargs) -> tuple:
    array = array_cells.copy()
    neighbours_cells = GetAllNeigbours(array)
    save = []
    # index_x, index_y = np.meshgrid(np.arange(array.shape[0], step=1), np.arange(array.shape[1], step=1))
    for iteration in tqdm(
            range(iterations),
            desc="Processing",
            unit="step",
            bar_format="{l_bar}{bar:40}{r_bar}",
            colour='cyan',
            total=iterations
    ):

        rule_to_apply(array, neighbours_cells, **kwargs)
        neighbours_cells = GetAllNeigbours(array)

        if do_save and iteration > start_animation_from and iteration % every_nth == 0:
            save.append(array.copy())

    tuple_to_return = [array]
    if do_save:
        tuple_to_return.append(save)
    return tuple(tuple_to_return)


def Animate(save: np.ndarray, fig, ax, do_save: bool = False, save_path: str = "", fps: int = 20, dpi: int = None):
    automata = ax.imshow(save[0], cmap="PuRd", aspect='auto')

    def update(frame):
        # plt.title(f"Iter {frame}")
        automata.set_data(save[frame])
        return automata

    anim = animation.FuncAnimation(fig=fig, func=update, frames=len(save), interval=100)
    if do_save:
        try:
            anim.save(save_path, fps=fps, dpi=dpi)
        except Exception as e:
            print(e)

    return anim


def Plot(array: np.ndarray, figsize: tuple[float], do_animation: bool = False, *args, **kwargs):
    fig, ax = plt.subplots(1, figsize=figsize)  #(19.2, 10.8)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_axis_off()
    if do_animation:
        anim = Animate(array, fig, ax, *args, **kwargs)
    else:
        ax.imshow(array, cmap="PuRd", aspect='auto')

    plt.show()