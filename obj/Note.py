import pygame as pg

class Note(pg.sprite.Sprite):
    time:float = 0.0
    wasHit:bool = False
    lane:int = 0

    def __init__(self, time:float, lane:int):
        super().__init__()
        self.time = time
        self.lane = lane