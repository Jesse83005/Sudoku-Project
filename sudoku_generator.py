import math,random

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = []
        self.box_length = int(row_length**2)

        for i in range(self.row_length):
            self.board.append([])
            for j in range(self.row_length):
                self.board[i].append(0)
    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        else:
            return True


    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
            else:
                return True

    def valid_in_box(self, row_start, col_start, num):
        row_iter = (row_start // self.box_length)
        col_iter = (col_start // self.box_length)
        for row in range(self.box_length):
            for col in range(self.box_length):
                if self.board[row_iter + row][col_iter + col] == num:
                    return False
                else:
                    return True

    def is_valid(self, row, col, num):
        if self.valid_in_row(row, num) == False:
            return False
        elif self.valid_in_col(col, num) == False:
            return False
        elif self.valid_in_box(row-row%3, col-col%3, num) == False:
            return False
        else:
            return True

    def fill_box(self, row_start, col_start):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(values)

        for i in range(self.box_length):
            for j in range(self.box_length):
                val = values[i * self.box_length + j]
                if self.is_valid(row_start, col_start, val):
                    self.board[row_start + i][col_start + j] = val
                    return True
                else:
                    return False

    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        num = 0
        #repeat until num of removed cells equals difficulty setting
        while self.removed_cells > num:
            #integer of the position in board
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            # doesn't increase num if cell already empty
            if self.board[row][col] == 0:
                continue
            else:
                self.board[row][col] = 0
                num += 1



def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

print(generate_sudoku(1, 0))