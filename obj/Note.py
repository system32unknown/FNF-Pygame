import pygame as pg

class Note(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)