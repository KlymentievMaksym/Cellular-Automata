import numpy as np
from time import time

import src.Rules as Rules
import src.CellularFucs as CF
import src.Music as Mc


if __name__ == "__main__":
    sizes = (1280, 1920)
    sizes = (100, 100)
    sizes = (3, 80)
    stages = 60

    Rules.USE_NUMBA = True


    PAUSE_PROBABILITY = 0.05
    PAUSE_PROBABILITY = 0.1
    BPM = 120
    TIME = 10

    pitches = CF.GenerateMusicArray(bpm=BPM, time=TIME, p_pause=PAUSE_PROBABILITY, p_change_pitch=0.0)
    # pitches, durations = CF.GenerateMusicArray(bpm=BPM, time=TIME, p_pause=PAUSE_PROBABILITY, p_change_pitch=0.0)
    # pitches = [52., 54., 51., 54., 54., 56., 52., 46., 40.]
    # durations = [0.5,  0.25, 0.5,  0.5,  0.25, 0.5,  0.25, 0.25, 0.25]
    # print(pitches)
    # print(durations)

    # seq = Mc.MusicSequence(bpm=BPM, instruments=["Acoustic Grand Piano", "Trumpet"]).from_array(pitches, durations)
    # seq = Mc.MusicSequence(bpm=BPM, instruments=["Trumpet"]).from_array(pitches, durations)

    seq = Mc.MusicSequence(bpm=BPM, instruments=["Acoustic Grand Piano"]).from_array(pitches)
    # seq = Mc.MusicSequence(bpm=BPM, instruments=["Trumpet"]).from_array(pitches)

    engine = Mc.MIDIEngine(seq, _dev=True)
    engine.save(f"./Music/test_{time()}.mp3", seconds=TIME)

    # array = CF.GenerateArray(sizes, stages)
    # array = CF.GenerateArray(sizes, stages, [1, 2])
    # array[1], array[2] = np.where(array[1] > array[2], [array[2], array[1]], [array[1], array[2]])

    # array = np.zeros(sizes, dtype=int)

    # array[0, :] = np.random.randint(0, 2, sizes[1])

    # p_kick = 0.3
    # p_snare = 0.05
    # p_hihat = 0.05
    # array[0, :] = np.random.choice([0, 1], sizes[1], p=[1 - p_kick, p_kick])
    # array[1, :] = np.random.choice([0, 1], sizes[1], p=[1 - p_snare, p_snare])
    # array[2, :] = np.random.choice([0, 1], sizes[1], p=[1 - p_hihat, p_hihat])

    # print(array.shape)
    # print(array)

    # array,  = CF.ApplyRulesAndSaveHistory(array, 1, [Rules.GameOfLife], do_save=False, stages=(stages - 1))

    # array, save = CF.ApplyRulesAndSaveHistory(array, 4, [Rules.RuleEmpty], do_save=True, stages=(stages - 1))
    # array, save = CF.ApplyRulesAndSaveHistory(array, 100, [Rules.RuleM1], do_save=True, stages=(stages - 1))

    # print(save)

    # filename = Mc.CreateMusic(save, f"./Music/test_{time()}.mp3", note_duration=200, save=True)
    # filename = Mc.automaton_music_with_drums(save, filename=f"./Music/test_{time()}.mp3", volume=-30, stages=stages)
    # notes = Mc.array_to_notes(array, time=15)
    # filename = Mc.notes_to_midi(notes, f"./Music/test_{time()}.mp3", instruments_name=["Acoustic Grand Piano"])  # , "Steel Drums"

    # CF.Plot(save, (5, 5), do_animation=True)
