from settings import *

class FPS:
    def __init__(self, clampFPS:bool = False):
        self.times = []
        self.sum = 0
        self.slice_cnt = 0
        self.curFPS = 0
        self.totalFPS = 0
        self.avgFPS = 0.0
        self.clampFPS = clampFPS
        self.cache_count = 0

    def update(self, dt):
        self.slice_cnt = 0
        delta = round(dt)
        self.times.append(delta)
        self.sum += delta

        while self.sum > 1000:
            self.sum -= self.times[self.slice_cnt]
            self.slice_cnt += 1
        if self.slice_cnt > 0:
            del self.times[:self.slice_cnt]

        cur_count = len(self.times)
        self.totalFPS = round(self.curFPS + cur_count / 8)
        if cur_count != self.cache_count:
            self.avgFPS = 1000 / (self.sum / cur_count) if cur_count > 0 else 0.0
            round_avg_fps = round(self.avgFPS)
            self.curFPS = min(round_avg_fps, MAX_FPS) if self.clampFPS else round_avg_fps
        self.cache_count = cur_count