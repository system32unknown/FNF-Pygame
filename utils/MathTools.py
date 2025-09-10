class MathTools:
    def lerp(a:float, b:float, ratio:float) -> float:
        return a + ratio * (b - a)