import pygame as pg

vec2 = pg.Vector2

MAX_FPS = 60
DEBUG_MODE = True

SRC_WIDTH, SRC_HEIGHT = 800, 600
SRC_SIZE = [SRC_WIDTH, SRC_HEIGHT]

NOTE_SIZE = [100, 100]

PLAYBACK_RATE = 1

DEFAULT_KEYBINDS = {
    ["GAME_LEFT"]: pg.K_d,
    ["GAME_RIGHT"]: pg.K_f,
    ["GAME_UP"]: pg.K_j,
    ["GAME_DOWN"]: pg.K_k
}