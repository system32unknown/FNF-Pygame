class MathTools:
    @staticmethod
    def lerp(a:float, b:float, ratio:float) -> float:
        return a + ratio * (b - a)
    
    @staticmethod
    def remapToRange(value:float, start1:float, stop1:float, start2:float, stop2:float) -> float:
        return start2 + (value - start1) * ((stop2 - start2) / (stop1 - start1))
        
    @staticmethod
    def bound(Value: float, Min: float = None, Max: float = None) -> float:
        lowerBound = Min if Min is not None and Value < Min else Value
        return Max if Max is not None and lowerBound > Max else lowerBound