import pygame as pg
import psutil, gc

from backend.FPS import FPS
from backend.Conductor import Conductor
from utils.StringTools import StringTools
from settings import *

gc.get_count()

pg.init()
pg.mixer.init()

src = pg.display.set_mode(SRC_SIZE)
surface = pg.Surface(src.get_size())
surface = surface.convert_alpha()
surface.fill("BLACK")

clock = pg.time.Clock()
fpsCounter = FPS()
FPSfont = pg.font.Font(None, 16)

conductor = Conductor(522)

StringTools = StringTools()

pg.mixer.music.load("assets/song/Inst.ogg")
pg.mixer.music.play()

def on_step_handler(step):
    print("Step changed:", step)

running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    surface.fill("BLACK")

    text = FPSfont.render(f"{fpsCounter.curFPS}FPS\n{StringTools.format_bytes(psutil.Process().memory_info().rss)}", 1, "White")
    textpos = text.get_rect()
    surface.blit(text, textpos)
    src.blit(surface)

    pg.display.flip()
    pg.display.update()

    ms = clock.tick(MAX_FPS)
    fpsCounter.update(ms)

    curTime = pg.mixer.music.get_pos() / 1000
    conductor.time = curTime
    conductor.on_step.append(on_step_handler)
    pg.display.set_caption(f'FlxPy ({StringTools.format_time(curTime)})')

pg.quit()