import numpy as np
from time import time

import Rules
import CellularFucs as CF
import Music as Mc


if __name__ == "__main__":
    sizes = (1280, 1920)
    sizes = (100, 100)
    sizes = (3, 8)
    stages = 2

    Rules.USE_NUMBA = False

    array = CF.GenerateArray(sizes, stages)
    array = np.zeros(sizes, dtype=int)
    # array[0, :] = np.random.randint(0, 2, sizes[1])
    p_kick = 0.3
    p_snare = 0.05
    p_hihat = 0.05
    array[0, :] = np.random.choice([0, 1], sizes[1], p=[1 - p_kick, p_kick])
    array[1, :] = np.random.choice([0, 1], sizes[1], p=[1 - p_snare, p_snare])
    array[2, :] = np.random.choice([0, 1], sizes[1], p=[1 - p_hihat, p_hihat])
    # print(array)
    # array,  = CF.ApplyRulesAndSaveHistory(array, 1, [Rules.GameOfLife], do_save=False, stages=(stages - 1))
    # print(array)
    # array, save = CF.ApplyRulesAndSaveHistory(array, 4, [Rules.RuleEmpty], do_save=True, stages=(stages - 1))
    array, save = CF.ApplyRulesAndSaveHistory(array, 10, [Rules.RuleM1], do_save=True, stages=(stages - 1))
    # print(save)
    filename = Mc.CreateMusic(save, f"./Music/test_{time()}.mp3", note_duration=200, save=True)
    # Mc.Play(filename)
    # filename = Mc.automaton_music_with_drums(save, filename=f"./Music/test_{time()}.mp3", volume=-30, stages=stages)
    # Mc.Play(filename)
    # CF.Plot(save, (5, 5), do_animation=True)
