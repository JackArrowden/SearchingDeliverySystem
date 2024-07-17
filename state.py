class State:
    def __init__(self, x, y, fuel_limit = None, time_limit = None):
        self.x = x
        self.y = y
        self.fuel = fuel_limit
        self.time = time_limit
