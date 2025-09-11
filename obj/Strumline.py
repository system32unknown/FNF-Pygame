from settings import *

class StrumNote(pg.sprite.Sprite):
    downscroll:bool = False
    def __init__(self):
        super().__init__()

class Strumline(pg.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)