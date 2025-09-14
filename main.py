import psutil
import json
import math

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
ScoreFont = pg.font.Font("assets/fonts/vcr.ttf", 18)

song_name = "Traumatism"

music_path = f"assets/song/{song_name}"
inst_path = music_path + "/Inst.ogg"

meta_path = music_path + "/meta.json"

meta_data = None
with open(meta_path, "rb") as f:
    meta_data = json.load(f)

inst_snd = pg.mixer.Sound(inst_path)
pg.mixer.music.load(inst_path)
pg.mixer.music.set_volume(.5)

countdown_sounds: list[pg.mixer.Sound] = [pg.mixer.Sound(f"assets/sounds/countdown/intro{3 - i}.ogg") for i in range(0, 4)]
countdown_sounds.reverse()

songStarted = False
wasReady = False

def beatHit(beat:int):
    global songStarted
    if not wasReady: return

    if beat < 0:
        countdown_beat = 4 + beat
        if countdown_beat != -1: countdown_sounds[countdown_beat].play()
    if not songStarted:
        if beat == 0:
            conductor.changeBpmAt(0, meta_data['bpm'], meta_data['TimeSignature']['numerator'], meta_data['TimeSignature']['denominator'])
            conductor.time = 0
            pg.mixer.music.play()
            songStarted = True

conductor = Conductor()
conductor.onBeat.append(beatHit)

curTime = 0
songPosition = -conductor.crochet * 4.5

noteGroup = pg.sprite.Group()

timeTxt = "0:00 / 0:00"

running = True
while running:
    ms = clock.tick(MAX_FPS)
    fpsCounter.update(ms)

    if songStarted:
        curTime = pg.mixer.music.get_pos() / 1000

    if wasReady:
        if not songStarted:
            songPosition += ms
        else: songPosition = pg.mixer.music.get_pos()
        conductor.time = songPosition

    if songStarted and not pg.mixer.music.get_busy():
        print("Finished.")

    for e in pg.event.get():
        if e.type == pg.QUIT: running = False
        if e.type == pg.KEYDOWN:
            match e.key:
                case pg.K_r:
                    if songStarted:
                        pg.mixer.music.pause()
                        pg.mixer.music.set_pos(0)
                        pg.mixer.music.play()
                        conductor.reset()
                case pg.K_RETURN:
                    if not wasReady: wasReady = True

    surface.fill("BLACK")

    text = StatsFont.render(f"{fpsCounter.curFPS}FPS\n{StringTools.format_bytes(psutil.Process().memory_info().rss)}", False, "Red" if fpsCounter.lagged() else "White")
    surface.blit(text, text.get_rect())

    if DEBUG_MODE and wasReady:
        text = StatsFont2.render(f"SH: {conductor.curStep} | BH: {conductor.curBeat} | MH: {conductor.curMeasure} | {conductor.bpm} BPM", False, "white")
        textpos = text.get_rect(centerx = SRC_WIDTH / 2)
        surface.blit(text, textpos)

    if not wasReady:
        text = StatsFont2.render(f"Press ENTER to start song.", False, "white")
        textpos = text.get_rect(center = (SRC_WIDTH / 2, SRC_HEIGHT / 2))
        surface.blit(text, textpos)

    if songStarted:
        timeTxt = f"{meta_data["songName"]} ({StringTools.format_time(curTime)} / {StringTools.format_time(inst_snd.get_length())})"
        text = StatsFont2.render(timeTxt, False, "white")
        textpos = text.get_rect(centerx = SRC_WIDTH / 2)
        surface.blit(text, (textpos.x, 20))

    text = ScoreFont.render(f"NPS: 0 | Score: 0 | Hits: 0", False, "white")
    textpos = text.get_rect(centerx = SRC_WIDTH / 2)
    surface.blit(text, (textpos.x, SRC_HEIGHT - 20))

    src.blit(surface)
    pg.display.update()

pg.quit()