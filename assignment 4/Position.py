import random

class Position:
    def __init__(self, min_xcoord, max_xcoord, min_ycoord, max_ycoord, x=0, y=0, random_init=True):
        if random_init:
            self.x = random.choice(range(min_xcoord, max_xcoord))
            self.y = random.choice(range(min_ycoord, max_ycoord))
        elif x < min_xcoord or x > max_xcoord or y < min_ycoord or y > max_ycoord:
            print(f"x: {x}; y: {y}")
            raise ValueError("invalid x or y coordinate")
        else:
            self.x = x
            self.y = y
    
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

