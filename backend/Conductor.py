import math
from typing import Callable, List

#Original Code by SGWLC, Converted to Py.
class Conductor:
    # Event callbacks
    on_step: List[Callable[[int], None]] = []
    on_beat: List[Callable[[int], None]] = []
    on_measure: List[Callable[[int], None]] = []

    # Core timing
    step_crochet: float = 150.0
    crochet: float = 600.0
    measure_crochet: float = 2400.0
    bpm: float = 100.0
    
    numerator:float = 4
    denominator:float = 4

    # State
    active: bool = False
    _time: float = 0.0

    # Trackers
    offset_time: float = 0.0
    step_offset: float = 0.0
    beat_offset: float = 0.0
    measure_offset: float = 0.0

    cur_step: int = 0
    cur_beat: int = 0
    cur_measure: int = 0

    step_tracker:int = 0
    beat_tracker:int = 0
    measure_tracker:int = 0

    def __init__(self, initialBpm:float = 100, initialNumerator:float = 4, initialDenominator:float = 4):
        self.changeBpmAt(0, initialBpm, initialNumerator, initialDenominator)
        self.active = True

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float):
        self._time = value
        calc = (self._time - self.offset_time)

        self.step_tracker = math.floor(self.step_offset + calc / self.step_crochet)
        self.beat_tracker = math.floor(self.beat_offset + calc / self.crochet)
        self.measure_tracker = math.floor(self.measure_offset + calc / self.measure_crochet)

        if self.active:
            if self.cur_step != self.step_tracker:
                self.cur_step = self.step_tracker
                for cb in self.on_step:
                    cb(self.cur_step)

            if self.cur_beat != self.beat_tracker:
                self.cur_beat = self.beat_tracker
                for cb in self.on_beat:
                    cb(self.cur_beat)

            if self.cur_measure != self.measure_tracker:
                self.cur_measure = self.measure_tracker
                for cb in self.on_measure:
                    cb(self.cur_measure)
        else:
            self.cur_step = self.step_tracker
            self.cur_beat = self.beat_tracker
            self.cur_measure = self.measure_tracker

    def changeBpmAt(self, position:float, newBpm:float = 0, newNumerator:float = 4, newDenominator:float = 4):
        calc = (position - self.offset_time)
        self.step_offset += calc / self.step_crochet
        self.beat_offset += calc / self.crochet
        self.measure_offset += calc / self.measure_crochet
        self.offset_time = position

        if newBpm > 0:
            self.bpm = newBpm
            self.stepCrochet = (15000 / self.bpm)

        self.crochet = self.step_crochet * newNumerator
        self.measureCrochet = self.crochet * newDenominator

        self.numerator = newNumerator
        self.denominator = newDenominator

    def reset(self):
        self.step_offset, self.beat_offset, self.measure_offset = 0
        self.offset_time, self.time = 0
        self.changeBpmAt(0)