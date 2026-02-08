import numpy as np
from collections import deque

class CanvasLogic:
    def __init__(self):
        self.strokes = []  # List of list of points: [[(x,y,color,size), ...], ...]
        self.current_stroke = []
        self.undo_stack = []
        
        # Smoothing parameters
        self.smooth_factor = 0.5
        self.previous_point = None

    def start_stroke(self):
        self.current_stroke = []
        self.previous_point = None

    def add_point(self, x, y, color, size):
        if self.previous_point:
            # Simple Weighted Moving Average
            px, py = self.previous_point
            sx = int(self.smooth_factor * px + (1 - self.smooth_factor) * x)
            sy = int(self.smooth_factor * py + (1 - self.smooth_factor) * y)
        else:
            sx, sy = x, y
        
        point = (sx, sy, color, size)
        self.current_stroke.append(point)
        self.previous_point = (sx, sy)
        return sx, sy

    def end_stroke(self):
        if self.current_stroke:
            self.strokes.append(self.current_stroke)
            self.undo_stack.append(self.current_stroke) # Assuming basic undo (pop last stroke)
            self.current_stroke = []

    def undo(self):
        if self.strokes:
            self.strokes.pop()
            return True
        return False

    def clear(self):
        self.strokes = []
        self.current_stroke = []
        self.undo_stack = []

    def get_strokes(self):
        return self.strokes

    def get_current_stroke(self):
        return self.current_stroke
