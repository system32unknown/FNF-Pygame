from settings import *
from obj.Strumline import StrumNote

import math

class Note(pg.sprite.Sprite):
    time:float = 0.0
    wasHit:bool = False
    lane:int = 0

    def __init__(self, time:float, lane:int, pos:vec2):
        super().__init__()
        self.time = time
        self.lane = lane

        self.image = pg.Surface(NOTE_SIZE)
        self.image.convert_alpha()
        self.image.fill("WHITE")
        self.rect = self.image.get_rect()
        self.rect.center = (SRC_WIDTH // 2 + pos.x, SRC_HEIGHT // 2 + pos.y)

    def followStrum(self, strum:StrumNote, time):
        diff = math.fabs((self.time - time)) / PLAYBACK_RATE
        self.rect.y = strum + diff