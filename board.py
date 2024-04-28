from cell import Cell
from sudoku_generator import SudokuGenerator

class Board:
    def __init__(self, width, difficulty):
        self.width = width
        self.on_row = 0
        self.on_col = 0
        if difficulty == "easy":
            difficulty = 30
        elif difficulty == "medium":
            difficulty = 40
        elif difficulty == "HARD":
            difficulty = 50
        self.create = []
        for i in SudokuGenerator.generate_sudoku(width, difficulty):
            new = []
            for j in i:
                new.append(Cell(j))
            self.create.append(new)

