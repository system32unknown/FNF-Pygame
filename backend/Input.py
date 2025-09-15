import numpy as np
from settings import *

class Input:
    keysArray = None
    keyBinds = DEFAULT_KEYBINDS

    def __init__(self, keys:int = 0):
        self.keys = keys
        self.keysArray = np.array([False] * (self.keys * 2))

    def update(self):
        keys_pressed = pg.key.get_pressed()