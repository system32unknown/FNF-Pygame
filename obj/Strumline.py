from settings import *

class Strumline(pg.sprite.Group):
    ai:bool = False
    keyCount:int = 0

    healthMult:float = 1
    desiredWidth:float = 160

    sizeMult:float = 0
    spacing:float = 0

    def __init__(self):
        super().__init__()

    def regenerate(self):
        self.empty()

        for i in range(self.keyCount):

            strum = Receptor(self, i)
            self.add(strum)

    def update(self, e):
        return super().update(e)

class Receptor(pg.sprite.Sprite):
    parent:Strumline = None
    queueStatic:bool = False
    holdTime:float = 0.0

    eRecepter:float = 0.0

    def __init__(self, parent:Strumline, lane:int):
        super().__init__()

        self.parent = parent