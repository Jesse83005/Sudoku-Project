import math
import random


# This class generates a 2D array of values in accordance to the rules of sudoku and can remove values
class SudokuGenerator:
    # The Constructor creates a sudoku board - initializes class variables (row length, removed cells)
    # Sets up the 2D board
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        # Square root of row_length from math module to get the box length (correspondant to row_length)
        self.box_length = int(math.sqrt(row_length))
        self.board = []
        # Define board to generate within array [[col in range(row_length)] row in range(row_length)]
        # Cell can be identified as board[row][col]
        for i in range(self.row_length):
            self.board.append([])
            for j in range(self.row_length):
                self.board[i].append(0)

    # Getter function returns self.board array of an array
    def get_board(self):
        return self.board

    # Prints each cell in correct orientation of the board from the 2D list (Used for testing purposes)
    def print_board(self):
        for i in range(self.row_length):
            for j in range(self.row_length):
                print(self.board[i][j], end=" ")
            print()

    # Checks row for number (return True if valid)
    def valid_in_row(self, row, num):
        if num in self.board[row]:
            return False
        return True

    # Checks columns for number (return True if valid)
    def valid_in_col(self, col, num):
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    # Checks if the number already exists in small boxes (return True if valid)
    def valid_in_box(self, row_start, col_start, num):
        # find the top left corner of the box
        top_left_row_index = (row_start // self.box_length) * self.box_length
        top_left_col_index = (col_start // self.box_length) * self.box_length

        # Iterates through small box elements only
        for row in range(self.box_length):
            for col in range(self.box_length):
                if self.board[top_left_row_index + row][top_left_col_index + col] == num:
                    return False
        return True

    # Determines if it is valid to enter num at the row, col, box in the board (return True if valid)
    def is_valid(self, row, col, num):
        # Check row, check col, check box
        if not self.valid_in_row(row, num) \
                or not self.valid_in_col(col, num) \
                or not self.valid_in_box(row - row % 3, col - col % 3, num):
            return False
        # If all checks pass return True
        return True

    # Fills the specified box with appropriate values
    # Generates a random digit 1-9 that has not yet been used in the box
    def fill_box(self, row_start, col_start):
        # List of available numbers
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        # Iterate through box checking if valid and places values (uses is_valid)
        for row in range(self.box_length):
            for col in range(self.box_length):
                num = nums[row * self.box_length + col]
                if self.is_valid(row_start, col_start, num):
                    self.board[row_start + row][col_start + col] = num
                else:
                    return False
        return True

    # Fills the diagonal boxes of the board with random values (uses fill_box)
    def fill_diagonal(self):
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    # Fills the remaining cells of the board after fill_diagonal (also returns True if solvable)
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

    # Calls on fill_diagonal and fill_remaining to fill all the cells of the board with values
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    # Removes cells at random for player to solve
    def remove_cells(self):
        count = 0
        # Uses count to track how many cells are removed during while loop
        while count < self.removed_cells:
            row = random.randint(0, 8)
            col = random.randint(0, 8)

            # Checks if cell equals 0: if True, reiterates loop; if False, assigns 0 and increments count
            if self.board[row][col] == 0:
                continue
            else:
                self.board[row][col] = 0
                count += 1


# Given number of rows and cells to remove, this function creates:
# SudokuGenerator object, fills all cells with values, removes number of cells, and returns the board (2D list)
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


if __name__ == "__main__":
    b = generate_sudoku(9, 10)  # Sets a Test board 9x9 with 10 removed values
    for r in b:                 # Prints the board in correct orientation
        print(r)
