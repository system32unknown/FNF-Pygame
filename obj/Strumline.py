import pygame as pg

class StrumNote(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Strumline(pg.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)