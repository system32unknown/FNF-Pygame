import numpy as np
from settings import *

class Input:
    keysArray = None
    keyBinds = DEFAULT_KEYBINDS

    def __init__(self, keys:int = 0, botPlay:bool = False):
        self.keys = keys
        self.keysArray = np.array([False] * self.keys)
        self.botPlay = botPlay

    def update(self):
        if self.botPlay:
            return

        keys_pressed = pg.key.get_pressed()

        for i, v in enumerate(self.keyBinds):
            self.keysArray[i] = keys_pressed[self.keyBinds[v]]

        if DEBUG_MODE:
            print(f"KEY ARRAYS: {self.keysArray}")

    def _input(self):
        pass

    def release(Self):
        pass