import numpy as np

from tqdm import tqdm

import matplotlib.pyplot as plt
import matplotlib.animation as animation

MIN_PITCH = 36
MAX_PITCH = 84

BEATS_AMOUNT = 16

# def mutate(pitch: int):
#     # min_ = max(pitch - 8)
#     # max_ = min(pitch + 8)

#     probabilities = [0.1, 0.14, 0.14, 0.14, 0.14, 0.14, 0.1, 0.05, 0.05]
#     values = np.arange(0, 9, 1)
#     coef = np.random.choice([-1, 1])
#     return np.clip(pitch + coef * np.random.choice(values, p=probabilities), MIN_PITCH, MAX_PITCH)


def mutate(pitch: int) -> int:
    """
    Slightly mutate a pitch within a range using weighted probabilities.
    Mutation step size is biased toward small intervals (musically natural).
    """
    step_choices = np.arange(9)  # 0 to 8 semitones
    step_probs = [0.1, 0.14, 0.14, 0.14, 0.14, 0.14, 0.1, 0.05, 0.05]
    step = np.random.choice(step_choices, p=step_probs)
    direction = np.random.choice([-1, 1])
    new_pitch = pitch + direction * step
    return int(np.clip(new_pitch, MIN_PITCH, MAX_PITCH))


def generate_duration():
    possible_durations = [0.125, 0.25, 0.5, 1.0]
    duration_probs = [0.1, 0.3, 0.5, 0.1]
    duration = np.random.choice(possible_durations, p=duration_probs)
    return duration

# def GenerateMusicArray(bpm: int, time: int, p_pause: float, p_change_pitch: float):
#     size = int(bpm * time / 60)
#     print(size)
#     # np.random.choice([], size=size)
#     array_cells = np.ones((2, size), dtype=int)/4
#     array_cells[0] = -1
#     array_cells[0, 0] = np.random.randint(MIN_PITCH, MAX_PITCH)
#     prev_val = array_cells[0, 0]
#     for col in range(1, array_cells.shape[1]):
#         if np.random.rand() >= p_pause:
#             # if np.random.rand() < p_change_pitch:
#             #     array_cells[col] = np.random.randint(MIN_PITCH, MAX_PITCH)
#             # else:
#             # print(array_cells[0, col])
#             array_cells[0, col] = mutate(prev_val)
#             # print(array_cells[0, col])
#             if array_cells[0, col] != -1:
#                 prev_val = array_cells[0, col]
#     return array_cells
"""
def GenerateMusicArray(bpm: int, time: int, p_pause: float, p_change_pitch: float) -> tuple[np.ndarray]:
    \"""
    Generate a 2-row array representing a sequence of pitches and durations.

    Row 0: pitch (or -1 for pause)
    Row 1: duration (in beats, currently fixed at 1/4 beat)

    Parameters:
    - bpm: tempo in beats per minute
    - time: total duration in seconds
    - p_pause: probability of inserting a pause
    - p_change_pitch: probability of changing pitch randomly instead of mutating
    \"""
    size = int(bpm * time / 60)
    pitches = np.zeros((size)) - 1  # default duration = quarter beat
    # pitches[0] = -1  # initialize all notes as rests

    # Start with a random pitch
    initial_pitch = np.random.randint(MIN_PITCH, MAX_PITCH)
    pitches[0] = initial_pitch
    prev_pitch = initial_pitch

    for col in range(1, size):
        if np.random.rand() >= p_pause:
            if np.random.rand() < p_change_pitch:
                new_pitch = np.random.randint(MIN_PITCH, MAX_PITCH)
            else:
                new_pitch = mutate(prev_pitch)
            pitches[col] = new_pitch
            prev_pitch = new_pitch

    possible_durations = [0.25, 0.5, 1.0]  # 1/4, 1/2, whole beat
    duration_probs = [0.6, 0.3, 0.1]
    duration = np.random.choice(possible_durations, size=pitches.shape, p=duration_probs)
    # duration = np.ones_like(pitches)

    return pitches, duration

"""


class NoteEvent:
    def __init__(self, pitch: int, position: int, duration: float):
        """Creates Note that has pitch, position and duration

        Args:
            pitch (int): [36, 84], int.
            position (int): [0, BEATS_AMOUNT], int.
            duration (float): [0, 1], float.
        """

        self.pitch = pitch
        self.position = position
        if self.position / BEATS_AMOUNT + duration > 1:
            duration = 1 - self.position / BEATS_AMOUNT
        self.duration = duration

    def change_values(self, pitch: int, duration: float = None):
        """Replaces Notes' pitch, and duration

        Args:
            pitch (int): [36, 84], int.
            duration (float, optional): [0, 1], float. Defaults to None.
        """

        self.pitch = pitch
        if duration is not None:
            if self.position / BEATS_AMOUNT + duration > 1:
                duration = 1 - self.position / BEATS_AMOUNT
            self.duration = duration


    def __repr__(self):
        return str(self.pitch)


def GenerateMusicArray(bpm: int, time: int, p_pause: float, p_change_pitch: float, step: int = 1) -> tuple[np.ndarray]:
    """
    Generate a array representing a sequence of NotesEvents.

    Row 0: pitch (or -1 for pause)
    Row 1: duration (in beats, currently fixed at 1/4 beat)

    Parameters:
    - bpm: tempo in beats per minute
    - time: total duration in seconds
    - p_pause: probability of inserting a pause
    - p_change_pitch: probability of changing pitch randomly instead of mutating
    """
    size = int(bpm * time / 60)
    assert size > 1, f"Wrong Size, Excpected greater or equal 1, Received {size}"
    print(f"[?] Size: {size}, BPM: {bpm}, SECONDS: {time}")

    pitches = [[NoteEvent(-2, halfbit, 0) for halfbit in range(BEATS_AMOUNT)] for _ in range(int(np.ceil(size / 4)))]
    # pitches = np.zeros([int(np.ceil(size / 4)), BEATS_AMOUNT]) - 2

    # pitches = np.zeros((size)) - 1  # default duration = quarter beat
    # pitches[0] = -1  # initialize all notes as rests

    # Start with a random pitch
    initial_pitch = NoteEvent(np.random.randint(MIN_PITCH, MAX_PITCH), 0, 1)
    pitches[0][0] = initial_pitch

    # print(pitches.shape)
    # print(pitches)
    # print(pitches[0][-1].duration)

    prev_pitch = initial_pitch.pitch

    def DoProbabilites(barline: list[NoteEvent], index: int, p_pause: float):
        nonlocal prev_pitch
        if np.random.rand() < p_pause:
            # barline[index].change_values(-1, np.random.rand())
            barline[index].change_values(-1, generate_duration())
        else:
            # barline[index].change_values(mutate(prev_pitch), np.random.rand())
            barline[index].change_values(mutate(prev_pitch), generate_duration())
            prev_pitch = barline[index].pitch

    for barline in pitches[:1]:
        for index in range(step, len(barline), step):
            DoProbabilites(barline, index, p_pause)

    for barline in pitches[1:]:
        for index in range(0, len(barline), step):
            DoProbabilites(barline, index, p_pause)

    print("[?] Pitches: ", pitches)
    return pitches

    # for col in range(1, size):
    #     if np.random.rand() >= p_pause:
    #         if np.random.rand() < p_change_pitch:
    #             new_pitch = np.random.randint(MIN_PITCH, MAX_PITCH)
    #         else:
    #             new_pitch = mutate(prev_pitch)
    #         pitches[col] = new_pitch
    #         prev_pitch = new_pitch

    # possible_durations = [0.25, 0.5, 1.0]  # 1/4, 1/2, whole beat
    # duration_probs = [0.6, 0.3, 0.1]
    # duration = np.random.choice(possible_durations, size=pitches.shape, p=duration_probs)
    # duration = np.ones_like(pitches)

    # return pitches, duration


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


def GenerateArray(sizes: tuple[int], stages: int, normalize: list[int] = []) -> np.ndarray:
    # size = 800
    # stages = 55
    array_cells = np.random.randint(0, stages, size=sizes).astype(float)
    if normalize:
        array_cells[normalize] = array_cells[normalize]/array_cells[normalize].max()
    # array = np.random.randint(0, stages, size=(1280, 1920))
    return array_cells


def ApplyRulesAndSaveHistory(array_cells: np.ndarray, iterations: int, rule_to_apply: list[callable], every_nth: int = 1, start_animation_from: int = 0, do_save: bool = False, **kwargs) -> tuple:
    array = array_cells.copy()
    neighbours_cells = GetAllNeigbours(array)
    save = []
    # index_x, index_y = np.meshgrid(np.arange(array.shape[0], step=1), np.arange(array.shape[1], step=1))
    for iteration in tqdm(
            range(iterations),
            desc="Mutating",
            unit="step",
            bar_format="{l_bar}{bar:40}{r_bar}",
            colour='cyan',
            total=iterations
    ):
        if callable(rule_to_apply):
            rule_to_apply(array, neighbours_cells, **kwargs)
        else:
            for rule in rule_to_apply:
                if callable(rule):
                    rule(array, neighbours_cells, **kwargs)
                else:
                    print(f"{rule} is not callable")
        neighbours_cells = GetAllNeigbours(array)

        if do_save and iteration >= start_animation_from and iteration % every_nth == 0:
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
    print("[?] Started Plotting")
    fig, ax = plt.subplots(1, figsize=figsize)  #(19.2, 10.8)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_axis_off()
    if do_animation:
        anim = Animate(array, fig, ax, *args, **kwargs)
    else:
        ax.imshow(array, cmap="PuRd", aspect='auto')

    plt.show()
    print("[?] Finished Plotting")
