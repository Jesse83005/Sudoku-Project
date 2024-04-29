from board import Board # Class
from gui import SudokuWindow

def main():
    window = SudokuWindow()
    # set the scene to grid and then display the menu
    scene = "grid"
    difficulty = window.menu()

    while True:
        if scene == "menu":
            difficulty = window.menu()
            scene = "grid"
        elif scene == "grid":
            scene = window.grid(Board(9, difficulty))
        elif scene == "win":
            window.win()
        elif scene == "lose":
            scene = window.loss()
        else:
            raise Exception("invalid")

if __name__ == "__main__":
    main()

