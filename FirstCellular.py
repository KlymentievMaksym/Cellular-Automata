# from time import time

import Rules
import CellularFucs as CF

if __name__ == "__main__":
    sizes = (1280, 1920)
    sizes = (100, 100)
    stages = 3
    array = CF.GenerateArray(sizes, stages)
    array, save = CF.ApplyRulesAndSaveHistory(array, 100, Rules.BriansBrain, do_save=True, stages=stages)
    CF.Plot(save, (5, 5), do_animation=True)
