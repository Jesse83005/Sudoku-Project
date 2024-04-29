import pygame
import sys

pygame.init()

class SudokuWindow:


    # window width and height
    WIDTH = 1000
    HEIGHT = 1000

    # grid stuff
    CELL_GAP = 10
    BUTTON_SPACE = 150
    CELL_WIDTH = ( min(WIDTH, HEIGHT)-BUTTON_SPACE )//9 - CELL_GAP

    # start menu button stuff
    MENU_BUTTON_WIDTH = 200
    MENU_BUTTON_HEIGHT = 100
    MENU_BUTTON_Y_CORD = 700

    # buttons under the grid stuff
    GRID_BUTTON_WIDTH = 250
    GRID_BUTTON_HEIGHT = 100
    GRID_BUTTON_Y_CORD = 880


    # any colors
    WHITE = (255, 255, 255)

    BLACK = (0, 0, 0)

    BUTTON_BG = (255, 255, 0)

    BEST_GREY = (225, 255, 255)

    BG_COLOR = (32,69,91)

    SELECTED_CELL_BG = (95, 255, 95)

    # fonts for the start menu
    FONT_BIG=pygame.font.SysFont("timesnewroman", 250)
    FONT_MEDIUM=pygame.font.SysFont("timesnewroman", 100)
    FONT_SMALL=pygame.font.SysFont("timesnewroman",80)

    # text for welcome menu
    WELCOME = FONT_BIG.render("Sudoku", True, BLACK)
    GAME_MODE = FONT_MEDIUM.render("Difficulty Level", True, WHITE)
    EASY = FONT_SMALL.render("Easy", True, WHITE)
    MEDIUM = FONT_SMALL.render("Medium", True, WHITE)
    HARD = FONT_SMALL.render("Hard", True, WHITE)

    # text for the buttons under the grid
    RESET = FONT_SMALL.render("Reset", True, BLACK)
    RESTART = FONT_SMALL.render("Main Menu", True, BLACK)
    EXIT = FONT_SMALL.render("Quit", True, BLACK)

    # text for win and loss screens
    WIN_MSG = FONT_BIG.render("Congatulations You WON!", True, BLACK)
    LOSE_MSG = FONT_BIG.render("Wasted", True, BLACK)

    def __init__(self):
        # create the window
        self.WIN = pygame.display.set_mode(( self.WIDTH, self.HEIGHT ))
        pygame.display.set_caption("Sudoku")

        icon = pygame.image.load("iconsoduko.jpeg")
        pygame.display.set_icon(icon)

        # returns a 2D list of Rect's that make up the grid
        self.grid_rects = self.create_the_grid()

        # vars for tracking the selected cell
        self.selected_col = 0
        self.selected_row = 0


    def create_the_grid(self):
        center_offset = self.center_with_offset(self.WIDTH, 9*(self.CELL_WIDTH+self.CELL_GAP))

        x_pos = center_offset
        y_pos = self.CELL_GAP

        board = []

        for _ in range(9):
            row = []
            for _ in range(9):
                r = pygame.Rect(x_pos, y_pos, self.CELL_WIDTH, self.CELL_WIDTH)
                row.append(r)
                x_pos += self.CELL_WIDTH + self.CELL_GAP
            board.append(row)
            y_pos += self.CELL_WIDTH + self.CELL_GAP
            x_pos = center_offset

        return board

    def get_displayed_cell_value_and_color_or_none(self, cell):
        cell_value = cell.get_cell_value()
        sketched_value = cell.get_sketched_value()


        if cell_value > 0:
            return (cell_value, self.BLACK)


        elif sketched_value > 0:
            return (sketched_value, self.BEST_GREY)


        else:
            return None


    def draw_game(self, sudoku_board, selected_cell_color=(185, 107, 17)):
        # make the bg
        self.WIN.fill(self.BG_COLOR)

        img = pygame.image.load('sudoku2.png')
        imgsize = (1000, 1000)
        image = pygame.transform.scale(img, imgsize)

        self.WIN.blit(image, (0, 0))

        # draw the grid
        for i, row in enumerate(self.grid_rects):
            for j, r in enumerate(row):
                # draw the rect
                cell_color = self.SELECTED_CELL_BG if i == self.selected_row and j == self.selected_col else selected_cell_color
                pygame.draw.rect(self.WIN, cell_color, r)

                # draw the number (if its not 0)
                cell = sudoku_board[i][j]
                cell_value_and_color_or_none = self.get_displayed_cell_value_and_color_or_none(cell)
                if cell_value_and_color_or_none != None:
                    cell_value = cell_value_and_color_or_none[0]
                    cell_color = cell_value_and_color_or_none[1]
                    # the actual image of the number (1, 2, 3, etc.)
                    NUMBER = self.FONT_SMALL.render(str(cell_value), True, cell_color)
                    # finding how to position the number
                    number_text_pos = NUMBER.get_rect(center=r.center)
                    # writing the number
                    self.WIN.blit(NUMBER, number_text_pos)

        # draw reset, exit, and restart buttons
        b1 = pygame.Rect(30, self.GRID_BUTTON_Y_CORD, self.GRID_BUTTON_WIDTH, self.GRID_BUTTON_HEIGHT)

        b2 = pygame.Rect(290, 860, 400, 130)

        b3_x_cord = self.WIDTH//2 + self.center_with_offset(self.WIDTH//2, self.GRID_BUTTON_WIDTH)
        b3 = pygame.Rect(700, self.GRID_BUTTON_Y_CORD, self.GRID_BUTTON_WIDTH, self.GRID_BUTTON_HEIGHT)



        #in game buttons at the bottom
        pygame.draw.ellipse(self.WIN, self.BUTTON_BG, b1)
        pygame.draw.ellipse(self.WIN, self.BUTTON_BG, b2)
        pygame.draw.ellipse(self.WIN, (204, 0 ,0), b3)

        # learned this from here: https://stackoverflow.com/questions/19117062/how-to-add-text-into-a-pygame-rectangle
        # center the text on the rects
        b1_text_pos = self.RESET.get_rect(center=b1.center)
        b2_text_pos = self.RESTART.get_rect(center=b2.center)
        b3_text_pos = self.EXIT.get_rect(center=b3.center)

        self.WIN.blit(self.RESET, b1_text_pos)
        self.WIN.blit(self.RESTART, b2_text_pos)
        self.WIN.blit(self.EXIT, b3_text_pos)

        # update the display
        pygame.display.update()

    @staticmethod
    def center_with_offset(surface_size, item_length):
        return (surface_size-item_length)//2

    def blit_text_centered(self, text, y_cord):
        text_width = text.get_size()[0]
        x_cord = self.center_with_offset(self.WIDTH, text_width)
        self.WIN.blit(text, (x_cord, y_cord))


    def handle_arrow_key_press(self, key):
        if key == pygame.K_LEFT and self.selected_col > 0:
            self.selected_col -= 1
        elif key == pygame.K_RIGHT and self.selected_col < 8:
            self.selected_col += 1
        elif key == pygame.K_UP and self.selected_row > 0:
            self.selected_row -= 1
        elif key == pygame.K_DOWN and self.selected_row < 8:
            self.selected_row += 1

        return (self.selected_row, self.selected_col)


    @staticmethod
    def key_is_a_number(key):
        if key == pygame.K_0 or key == pygame.K_KP0:
            return 0

        elif key == pygame.K_1 or key == pygame.K_KP1:
            return 1

        elif key == pygame.K_2 or key == pygame.K_KP2:
            return 2

        elif key == pygame.K_3 or key == pygame.K_KP3:
            return 3

        elif key == pygame.K_4 or key == pygame.K_KP4:
            return 4

        elif key == pygame.K_5 or key == pygame.K_KP5:
            return 5

        elif key == pygame.K_6 or key == pygame.K_KP6:
            return 6

        elif key == pygame.K_7 or key == pygame.K_KP7:
            return 7

        elif key == pygame.K_8 or key == pygame.K_KP8:
            return 8

        elif key == pygame.K_9 or key == pygame.K_KP9:
            return 9

        else:
            return None


    def check_if_cell_was_clicked(self):
        mouse_pos = pygame.mouse.get_pos()

        for i, row in enumerate(self.grid_rects):
            for j, rect in enumerate(row):
                if rect.collidepoint(mouse_pos):
                    self.selected_row = i
                    self.selected_col = j
                    return (i, j)

        return None

    def check_if_grid_button_was_pressed(self):
        # need these to check for collisions
        b1 = pygame.Rect(self.center_with_offset(self.WIDTH//2, self.GRID_BUTTON_WIDTH), self.GRID_BUTTON_Y_CORD, self.GRID_BUTTON_WIDTH, self.GRID_BUTTON_HEIGHT)
        b2 = pygame.Rect(self.center_with_offset(self.WIDTH, self.GRID_BUTTON_WIDTH), self.GRID_BUTTON_Y_CORD, self.GRID_BUTTON_WIDTH, self.GRID_BUTTON_HEIGHT)
        b3_x_cord = self.WIDTH//2 + self.center_with_offset(self.WIDTH//2, self.GRID_BUTTON_WIDTH)
        b3 = pygame.Rect(b3_x_cord, self.GRID_BUTTON_Y_CORD, self.GRID_BUTTON_WIDTH, self.GRID_BUTTON_HEIGHT)

        mouse_pos = pygame.mouse.get_pos()

        if b1.collidepoint(mouse_pos):
            return "reset"
        if b2.collidepoint(mouse_pos):
            return "menu"
        if b3.collidepoint(mouse_pos):
            sys.exit(0)
        else:
            return None


    def check_if_menu_button_was_pressed(self):
        # need button rects here too to check for collisions
        b1 = pygame.Rect(self.center_with_offset(self.WIDTH//2, self.MENU_BUTTON_WIDTH), self.MENU_BUTTON_Y_CORD, self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT)
        b2 = pygame.Rect(self.center_with_offset(self.WIDTH, self.MENU_BUTTON_WIDTH), self.MENU_BUTTON_Y_CORD, self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT)
        b3_x_cord = self.WIDTH//2 + self.center_with_offset(self.WIDTH//2, self.MENU_BUTTON_WIDTH)
        b3 = pygame.Rect(b3_x_cord, self.MENU_BUTTON_Y_CORD, self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT)

        #current mouse position
        mouse_pos = pygame.mouse.get_pos()

        if b1.collidepoint(mouse_pos):
            return "easy"
        if b2.collidepoint(mouse_pos):
            return "medium"
        if b3.collidepoint(mouse_pos):
            return "hard"
        else:
            return None

    def check_if_win_button_was_pressed(self):
        b1 = pygame.Rect(self.center_with_offset(self.WIDTH, self.MENU_BUTTON_WIDTH), self.MENU_BUTTON_Y_CORD, self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT)

        mouse_pos = pygame.mouse.get_pos()

        if b1.collidepoint(mouse_pos):
            sys.exit(0)
        else:
            return None

    def check_if_loss_button_was_pressed(self):
        b1 = pygame.Rect(self.center_with_offset(self.WIDTH, self.MENU_BUTTON_WIDTH), self.MENU_BUTTON_Y_CORD, self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT)

        mouse_pos = pygame.mouse.get_pos()

        if b1.collidepoint(mouse_pos):
            return "menu"
        else:
            return None

    def draw_win_screen(self):
        self.WIN.fill(self.BG_COLOR)

        won_image = pygame.image.load("sudokuwin.jpg")
        win_image_size = (1000, 800)
        win_image = pygame.transform.scale(won_image,win_image_size)

        self.WIN.blit(win_image, (0, 0))


        #self.blit_text_centered(self.WIN_MSG, 50)

        # button TODO, should this be the same as the menu button
        b1 = pygame.Rect(self.center_with_offset(self.WIDTH, self.MENU_BUTTON_WIDTH), 850, self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT)

        pygame.draw.ellipse(self.WIN, self.BUTTON_BG, b1)


        b1_text_pos = self.EXIT.get_rect(center=b1.center)

        self.WIN.blit(self.EXIT, b1_text_pos)

        pygame.display.update()

    def draw_lose_screen(self):
        self.WIN.fill(self.BG_COLOR)

        wasted_image = pygame.image.load("sudokulost.jpg")
        lost_sizing = (1000, 650)
        lost_image = pygame.transform.scale(wasted_image, lost_sizing)

        self.WIN.blit(lost_image, (0, 20))


        self.blit_text_centered(self.LOSE_MSG, 50)

        b1 = pygame.Rect(250, 750, 500, 200)

        pygame.draw.ellipse(self.WIN, self.BUTTON_BG, b1)

        b1_text_pos = self.RESTART.get_rect(center=b1.center)

        self.WIN.blit(self.RESTART, b1_text_pos)

        pygame.display.update()




    #Main Menu screen
    def draw_start_menu(self):
        self.WIN.fill(self.BG_COLOR)

        img = pygame.image.load('sudoku2.png')
        imgsize = (1000, 1000)
        image = pygame.transform.scale(img, imgsize)

        self.WIN.blit(image, (0,280))




        # centered
        self.blit_text_centered(self.WELCOME, 0)


        b1 = pygame.Rect(25, 650, 300, 200)


        b2 = pygame.Rect(338, 650, 320, 200)



        b3_x_cord = self.WIDTH//2 + self.center_with_offset(self.WIDTH//1.5, self.MENU_BUTTON_WIDTH)
        b3 = pygame.Rect(670, 650, 300, 200)

        #button easy
        pygame.draw.ellipse(self.WIN, (0, 153, 0), b1)
        #button medium
        pygame.draw.ellipse(self.WIN, (204, 204, 0), b2)
        #button hard
        pygame.draw.ellipse(self.WIN, (153,0,0), b3)

        # learned this from here: https://stackoverflow.com/questions/19117062/how-to-add-text-into-a-pygame-rectangle
        # center the text on the rects
        b1_text_pos = self.EASY.get_rect(center=b1.center)
        b2_text_pos = self.MEDIUM.get_rect(center=b2.center)
        b3_text_pos = self.HARD.get_rect(center=b3.center)

        self.WIN.blit(self.EASY, b1_text_pos)
        self.WIN.blit(self.MEDIUM, b2_text_pos)
        self.WIN.blit(self.HARD, b3_text_pos)

        pygame.display.update()
        

    def menu(self):
        while True:
            # handle events
            for event in pygame.event.get():
                # make the x in the top right work
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONUP:
                    ans = self.check_if_menu_button_was_pressed()
                    if ans != None:
                        return ans

            # draw to the screen
            self.draw_start_menu()


    def grid(self, sudoku_board):
        # always start in the top left corner
        self.selected_row = 0
        self.selected_col = 0
        while True:
            # handle events
            for event in pygame.event.get():
                # make the x in the top right work
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    # check for arrow key press
                    cords = self.handle_arrow_key_press(event.key)

                    # update the selected cell in sudoku_board
                    sudoku_board.select(cords[0], cords[1])

                    # check for num key presses
                    # (and update sketched values accordingly)
                    number_or_none = self.key_is_a_number(event.key)
                    if number_or_none != None:
                        sudoku_board.sketch(number_or_none)

                    # confirm sketched cell choice
                    # TODO is return the enter key?
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        sudoku_board.place_number()

                if event.type == pygame.MOUSEBUTTONUP:
                    # check for cell clicks
                    cords_or_none = self.check_if_cell_was_clicked()

                    # update the selected cell in sudoku_board, if needed
                    if cords_or_none != None:
                        sudoku_board.select(cords_or_none[0], cords_or_none[1])

                    # check for button clicks
                    ans = self.check_if_grid_button_was_pressed()
                    if ans == "reset":
                        sudoku_board.reset_to_original()
                    elif ans == None:
                        pass
                    else:
                        return ans

            # here I check if the board is done
            # and check if they won or lost
            if sudoku_board.is_full():
                return "win" if sudoku_board.check_board() else "lose"

            # draw to the screen

            self.draw_game(sudoku_board.get_board())

            ####testing purposes
            #self.draw_win_screen()
            #self.draw_lose_screen()

    # Win Screen
    def win(self):
        while True:
            # handle events
            for event in pygame.event.get():
                # make the x in the top right work
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONUP:
                    ans = self.check_if_win_button_was_pressed()
                    if ans != None:
                        return ans

            # draw to the screen
            self.draw_win_screen()

    #Loss Screen
    def loss(self):
        while True:
            # handle events
            for event in pygame.event.get():
                # make the x in the top right work
                if event.type == pygame.QUIT:
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONUP:
                    ans = self.check_if_loss_button_was_pressed()
                    if ans != None:
                        return ans

            # draw to the screen
            self.draw_lose_screen()

