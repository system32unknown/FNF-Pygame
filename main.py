import pygame as pg
import psutil

from backend.FPS import FPS
from backend.Conductor import Conductor
from utils.StringTools import StringTools
from settings import *

pg.init()
pg.font.init()
pg.mixer.init()

src = pg.display.set_mode(SRC_SIZE)
surface = pg.Surface(src.get_size()).convert_alpha()

clock = pg.time.Clock()

fpsCounter = FPS()
StatsFont = pg.font.Font(None, 18)
StatsFont2 = pg.font.Font("assets/fonts/vcr.ttf", 16)

song_path = "assets/song/Inst.ogg"

preloaded_music = pg.mixer.Sound(song_path)
pg.mixer.music.load(song_path)
pg.mixer.music.set_volume(.5)
pg.mixer.music.play()

conductor = Conductor(522)

running = True
while running:
    curTime = c.get_pos() / 1000
    conductor.time = pg.mixer.music.get_pos()

    if not pg.mixer.music.get_busy():
        print("Finished.")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN:
            match e.key:
                case pg.K_r:
                    pg.mixer.music.pause()
                    pg.mixer.music.set_pos(0)
                    pg.mixer.music.play()
                    conductor.reset()

    surface.fill("BLACK")

    text = StatsFont.render(f"{fpsCounter.curFPS}FPS\n{StringTools.format_bytes(psutil.Process().memory_info().rss)}", False, "Red" if fpsCounter.lagged() else "White")
    surface.blit(text, text.get_rect())

    text = StatsFont2.render(f"SH: {conductor.curStep} | BH: {conductor.curBeat} | MH: {conductor.curMeasure} | {conductor.bpm}BPM", False, "white")
    textpos = text.get_rect(centerx = SRC_WIDTH / 2)
    surface.blit(text, textpos)

    text = StatsFont2.render(f"{StringTools.format_time(curTime)} / {StringTools.format_time(preloaded_music.get_length())}", False, "white")
    textpos = text.get_rect(centerx = SRC_WIDTH / 2)
    surface.blit(text, (textpos.x, 20))

    src.blit(surface)
    pg.display.update()

    ms = clock.tick(MAX_FPS)
    fpsCounter.update(ms)

pg.quit()