import psutil
import json

from backend.FPS import FPS
from backend.Conductor import Conductor
from obj.Note import Note
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

song_name = "Ntuzongere-Kugaruka"

song_path = f"assets/song/{song_name}/Inst.ogg"
meta_path = f"assets/song/{song_name}/meta.json"

meta_data = None
with open(meta_path, "rb") as f:
    meta_data = json.load(f)

preloaded_music = pg.mixer.Sound(song_path)
pg.mixer.music.load(song_path)
pg.mixer.music.set_volume(.5)

songStarted = False
def beatHit(beat:int):
    global songStarted
    if beat == 0 and not songStarted:
        conductor.changeBpmAt(0, meta_data['bpm'], meta_data['TimeSignature']['numerator'], meta_data['TimeSignature']['denominator'])
        conductor.time = 0
        pg.mixer.music.play()
        songStarted = True

conductor = Conductor()
conductor.onBeat.append(beatHit)

songPosition = -conductor.crochet * 4.5

noteGroup = pg.sprite.Group()

running = True
while running:
    ms = clock.tick(MAX_FPS)
    fpsCounter.update(ms)

    curTime = pg.mixer.music.get_pos() / 1000
    if not songStarted:
        songPosition += ms
    else: songPosition = pg.mixer.music.get_pos()
    conductor.time = songPosition

    if songStarted and not pg.mixer.music.get_busy():
        print("Finished.")

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_r and songStarted:
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

    if songStarted:
        text = StatsFont2.render(f"{StringTools.format_time(curTime)} / {StringTools.format_time(preloaded_music.get_length())}", False, "white")
        textpos = text.get_rect(centerx = SRC_WIDTH / 2)
        surface.blit(text, (textpos.x, 20))

    src.blit(surface)
    pg.display.update()

pg.quit()