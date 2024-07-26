class Grid:
    def __init__(self, matrix):
        self.matrix = matrix
        self.num_row = len(matrix)
        self.num_col = 0 if self.num_row == 0 else len(matrix[0])
        for row in self.matrix:
            if len(row) != self.num_col:
                raise ValueError('error with input matrix')
    
    def is_cell(self, x: int, y: int):
        return 0 <= x < self.num_row and 0 <= y < self.num_col
    
    def is_move_cell(self, x: int, y: int):
        return self.is_cell(x, y) and self.matrix[x][y] != -1 
    
    def is_gas_station(self, x: int, y: int):
        return self.is_cell(x, y) and self.matrix[x][y] < -1 
    
    def is_toll_booth(self, x: int, y: int):
        return self.is_cell(x, y) and self.matrix[x][y] > 0 
    
    def is_blank_cell(self, x: int, y: int):
        return self.is_cell(x, y) and self.matrix[x][y] == 0
    
    def time_2_in(self, x: int, y: int):
        if self.matrix[x][y] == -1: 
            return None
        return self.matrix[x][y] + 1 if self.matrix[x][y] > -1 else -self.matrix[x][y]
