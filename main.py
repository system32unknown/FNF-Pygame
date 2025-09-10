import pygame as pg
import psutil

from backend.FPS import FPS
from backend.Conductor import Conductor
from utils.StringTools import StringTools
from settings import *

pg.init()
pg.mixer.init()

src = pg.display.set_mode(SRC_SIZE)
surface = pg.Surface(src.get_size()).convert_alpha()

clock = pg.time.Clock()

fpsCounter = FPS()
StatsFont = pg.font.Font(None, 16)
StatsFont2 = pg.font.Font(None, 20)

StringTools = StringTools()

pg.mixer.music.load("assets/song/Inst.ogg")
pg.mixer.music.play()

conductor = Conductor(522)
print(f"BPM: {conductor.bpm}")

running = True
while running:
    curTime = pg.mixer.music.get_pos() / 1000
    conductor.time = pg.mixer.music.get_pos()

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_r:
                pg.mixer.music.pause()
                pg.mixer.music.set_pos(0)
                pg.mixer.music.play()

                conductor.reset()

    surface.fill("BLACK")

    text = StatsFont.render(f"{fpsCounter.curFPS}FPS\n{StringTools.format_bytes(psutil.Process().memory_info().rss)}", 1, "Red" if fpsCounter.lagged() else "White")
    surface.blit(text, text.get_rect())

    text = StatsFont2.render(f"STEP: {conductor.curStep} | BEAT: {conductor.curBeat} | MEASURE: {conductor.curMeasure}", 1, "white")
    textpos = text.get_rect(centerx = SRC_WIDTH / 2)
    surface.blit(text, textpos)

    src.blit(surface)

    pg.display.flip()
    pg.display.update()

    ms = clock.tick(MAX_FPS)
    fpsCounter.update(ms)
    pg.display.set_caption(f'{StringTools.format_time(curTime)} - {conductor.bpm}BPM')

pg.quit()