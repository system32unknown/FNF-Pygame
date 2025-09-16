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
        
        self._input()
        self._released()

    def _input(self):
        keys_pressed = pg.key.get_pressed()
        for i, v in enumerate(self.keyBinds):
            if self.keysArray[i]: continue
            self.keysArray[i] = keys_pressed[v]
        print(self.keysArray)

    def _released(self):
        for i, _ in enumerate(self.keyBinds):
            if not self.keysArray[i]: continue
            self.keysArray[i] = False