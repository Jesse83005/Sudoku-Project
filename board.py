from sudoku_generator import generate_sudoku

class Cell:
    # Constructor for the Cell class
    def __init__(self, value): 
        self.value = value
        self.gray_number = 0
        #mutable cell is set to true if not mutable cell is false
        if self.value == 0:
            self.is_mutable = True
        else:
            self.is_mutable = False

    # Setter for this cell’s value
    def set_cell_value(self, value): 
        self.value = value

    # Setter for this cell’s sketched value, (Grey number)
    def set_sketched_value(self, value):
        self.gray_number = value 
        
    # Getter for this cell’s value
    def get_cell_value(self): 
        return self.value

    # Getter for this cell’s sketched value
    def get_sketched_value(self):
        return self.gray_number
        
class Board:
    # Constructor for the Board class.
    # screen is a window from PyGame.
    # difficulty is a variable to indicate if the user chose easy, medium, or hard.
    def __init__(self, width, difficulty): 
        self.width = width
        self.selected_row = 0
        self.selected_col = 0
        if difficulty == "easy":
            difficulty = 30
        elif difficulty == "medium":
            difficulty = 40
        elif difficulty == "hard":
            difficulty = 50
        self.board = []
        for row in generate_sudoku(width,difficulty):
            temp = []
            for next_col in row:
                temp.append(Cell(next_col))
            self.board.append(temp)
        
            

    # Marks the cell at (row, col) in the board as the current selected cell.
    # Once a cell has been selected, the user can edit its value or sketched value.
    def select(self, row, col): 
        self.selected_row = row
        self.selected_col = col
                
    # getter function that returns the 2D list (2D list of Cell's not numbers)
    # the represents the sudoku board
    def get_board(self):
        return(self.board)

    # Clears the value cell. Note that the user can only remove the cell values and sketched value that are
    # filled by themselves.
    def clear(self): 
        cell = self.board[self.selected_row][self.selected_col]
        if cell.is_mutable:
            cell.set_cell_value(0)
            cell.set_sketched_value(0)
        else:
            pass
    # Sets the sketched value of the current selected cell equal to user entered value.
    # It will be displayed at the top left corner of the cell using the draw() function.
    def sketch(self, value): 
        cell = self.board[self.selected_row][self.selected_col]
        cell.set_sketched_value(value)

    # Sets the value of the current selected cell equal to user entered value.
    # Called when the user presses the Enter key.
    def place_number(self): 
        cell = self.board[self.selected_row][self.selected_col]
        if cell.is_mutable:
            cell.set_cell_value(cell.gray_number)
    # Reset all cells in the board to their original values (0 if cleared, otherwise the corresponding digit).
    def reset_to_original(self): 
        for row in self.board:
            for cell in row:
                if cell.is_mutable:
                    cell.set_cell_value(0)
                    cell.set_sketched_value(0)
        
    # Returns a Boolean value indicating whether the board is full or not.
    def is_full(self): 
        for row in self.board:
            for cell in row:
                if cell.value == 0:
                    return(False)
        return(True)
                
    # Check whether the Sudoku board is solved correctly(rows, cols, boxes).
    def check_board(self): 
        rows = self.board
        columns = []

        for i in range(self.width):
            temp = []
            for row in self.board:
                temp.append(row[i])
            columns.append(temp)

        boxes = []

        # TODO hard coding 3 is a crime!
        for row in range(0, self.width, 3):
            for col in range(0, self.width, 3):
                temp = []
                for i in range(3):
                    for j in range(3):
                        temp.append(self.board[row + i][col + j])
                boxes.append(temp)

        for row in rows:
            row = map(lambda cell: cell.value, row)
            if len(set(row)) != self.width:
                return(False)
        for col in columns:
            col = map(lambda cell: cell.value, col)
            if len(set(col)) != self.width:
                return(False)
        for box in boxes:
            box = map(lambda cell: cell.value, box)
            if len(set(box)) != self.width:
                return(False)
        return(True)

