class State:
    def __init__(self, x, y, fuel_limit = None, time_limit = None):
        self.x = x
        self.y = y
        self.fuel = fuel_limit
        self.time = time_limit

    def __eq__(self, other: 'State') -> bool:
        return (self.x == other.x and 
                self.y == other.y and 
                self.fuel == other.fuel and 
                self.time == other.time)
    
    def __ne__(self, other: 'State') -> bool:
        return not (self == other) 

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.fuel, self.time))
    
    def __repr__(self) -> str:
        return f"State(x={self.x}, y={self.y}, fuel={self.fuel}, time={self.time})"
