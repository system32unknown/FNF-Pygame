class Conductor:
    def __init__(self):
        self.curSection = 0
        self.stepsToDo = 0

        self.curStep = 0
        self.curBeat = 0

        self.fStep = 0.0
        self.fBeat = 0.0

    def reset(self):
        self.curSection = 0
        self.stepsToDo = 0

        self.curStep = self.fStep = 0
        self.curBeat = self.fBeat = 0