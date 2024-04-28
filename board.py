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
        self.board = []
        for i in SudokuGenerator.generate_sudoku(width, difficulty):
            new = []
            for j in i:
                new.append(Cell(j))
            self.board.append(new)

    def select(self, row, col):
        self.on_row = row
        self.on_col = col

    def clear(self):
        cell = self.board[self.on_row][self.on_col]
        if cell.is_mutable:
            cell.set_cell_value(0)

    def place_number(self, value):
        cell = self.board[self.on_row][self.on_col]
        if cell.is_mutable:
            cell.set_cell_value(value)

    def reset_to_original(self):
        for row in self.board:
            for cell in row:
                if cell.is_mutable:
                    cell.set_cell_value(0)

    def is_full(self):
        for i in self.board:
            for j in i:
                if j.value == 0:
                    return False
        return True

    def update_board(self):
        return self.board


    def check_board(self):
        full_board = self.board
        iterlist = []


        for i in range(self.width):
            new = []
            for j in self.board:
                new.append(j[i])
            iterlist.append(new)

        segment = []

        for i in range(self.width):
            for j in range(self.width):
                new = []
                for k in range(9):
                    for l in range(9):
                        new.append(self.board[i+k][j+l])
                segment.append(new)

        for i in full_board:
            row = map(lambda cell: cell.value, i)
            if len(set(row)) != self.width:
                return False
        for j in iterlist:
            col = map(lambda cell: cell.value, j)
            if len(set(col)) != self.width:
                return False
        for k in segment:
            seg = map(lambda cell: cell.value, k)
            if len(set(seg)) != self.width:
                return False
        return True
