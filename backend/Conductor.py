import math
from typing import Callable, List

# Original Code by SGWLC, Converted to Py.
class Conductor:
    # Event callbacks
    onStep: List[Callable[[int], None]] = []
    onBeat: List[Callable[[int], None]] = []
    onMeasure: List[Callable[[int], None]] = []

    # Core timing
    stepCrochet: float = 150
    crochet: float = 600
    measureCrochet: float = 2400
    bpm: float = 100

    # State
    active: bool = False
    _time: float = 0

    # Trackers
    curStep: float = 0
    curBeat: float = 0
    curMeasure: float = 0

    _stepTracker: float = 0
    _beatTracker: float = 0
    _measureTracker: float = 0

    stepOffset: float = 0
    beatOffset: float = 0
    measureOffset: float = 0
    offsetTime: float = 0

    numerator: float = 4
    denominator: float = 4

    rate:float = 1

    def __init__(self, initial_bpm:float = 100, initial_numerator:float = 4, initial_denominator:float = 4):
        self.changeBpmAt(0, initial_bpm, initial_numerator, initial_denominator)
        self.active = True

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float):
        self._time = value
        calc = (self._time - self.offsetTime)
        self._stepTracker = math.floor(self.stepOffset + calc / self.stepCrochet)
        self._beatTracker = math.floor(self.beatOffset + calc / self.crochet)
        self._measureTracker = math.floor(self.measureOffset + calc / self.measureCrochet)

        if self.active:
            if self.curStep != self._stepTracker:
                self.curStep = self._stepTracker
                for cb in self.onStep: cb(self.curStep)

            if self.curBeat != self._beatTracker:
                self.curBeat = self._beatTracker
                for cb in self.onBeat: cb(self.curBeat)

            if self.curMeasure != self._measureTracker:
                self.curMeasure = self._measureTracker
                for cb in self.onMeasure: cb(self.curMeasure)
        else:
            self.curStep = self._stepTracker
            self.curBeat = self._beatTracker
            self.curMeasure = self._measureTracker

        return value

    def changeBpmAt(self, position: float, new_bpm: float = 0, new_numerator: float = 4, new_denominator: float = 4):
        calc = (position - self.offsetTime)
        self.stepOffset += calc / self.stepCrochet
        self.beatOffset += calc / self.crochet
        self.measureOffset += calc / self.measureCrochet
        self.offsetTime = position

        if new_bpm > 0:
            self.bpm = new_bpm
            self.stepCrochet = (15000 / self.bpm)

        self.crochet = self.stepCrochet * new_numerator
        self.measureCrochet = self.crochet * new_denominator

        self.numerator = new_numerator
        self.denominator = new_denominator

    def reset(self):
        self.stepOffset, self.beatOffset, self.measureOffset = 0, 0, 0
        self.offset_time, self.time = 0, 0
        self.changeBpmAt(0)