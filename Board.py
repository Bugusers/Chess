import math
import pygame as pg
from Cell import Cell
from Figures.Bishop import Bishop
from Figures.Queen import Queen
from Figures.King import King
from Figures.Knight import Knight
from Figures.Rook import Rook
from Figures.Pawn import Pawn


class Board:
    BLEDZOLOT = (238, 232, 170)
    OHRA = (160, 82, 45)

    def __init__(self, screen, square_size, player_color, white_player, black_player):
        self.screen = screen
        self.square_size = square_size

        self.player_color = player_color
        self.white_player = white_player
        self.black_player = black_player
        self.current_player = white_player

        self.cells = self.create_board()
        self.selected_figure = None
        self.selected_cell = None
        self.available_moves = []

        self.rescue_figures = []
        self.rescue_moves = []


    def create_board(self):
        cells = []
        for row in range(8):
            cell_row = []
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                color = self.BLEDZOLOT if (row + col) % 2 == 0 else self.OHRA
                cell = Cell(x, y, self.square_size, color, self)
                cell_row.append(cell)
            cells.append(cell_row)
        
        return cells


    def draw_board(self):
        for row in self.cells:
            for cell in row:
                cell.draw_cell(self.screen)
                self.highlight_cell(cell)


    def highlight_cell(self, cell):
        highlight_thickness = 3

        if cell == self.selected_cell:
            highlight_color = (255, 255, 0)  
        elif self.selected_figure is not None and cell in self.available_moves:
            highlight_color = (0, 255, 0)
        else:
            return    


        highlight_rect = pg.Rect(cell.x, cell.y, cell.size, cell.size)
        pg.draw.rect(self.screen, highlight_color, highlight_rect, highlight_thickness)        


    def handle_click(self, x, y):
        cell = self.get_cell(x, y)

        if self.is_check() and cell.figure is not None:
            self.get_rescue_figures()

            for i in self.rescue_figures:
                print(i.figure.name)

            if cell in self.rescue_moves:
                self.select_figure(cell.figure)
                self.selected_cell = cell
                self.rescue_figures = []  # Очищуємо список фігур для рятування

        elif self.selected_figure is None and cell.figure is not None and cell.figure.color == self.current_player.color:
            self.select_figure(cell.figure)
            self.selected_cell = cell

        elif cell in self.available_moves:
            self.move_figure(cell)
            self.switch_player()
        else:
            self.deselect_figure()

        self.rescue_moves = []  # Очищуємо список клітинок для рятування

                    

    def select_figure(self, figure):
        self.selected_figure = figure
        self.available_moves = self.get_available_moves(figure)


    def deselect_figure(self):
        self.selected_figure = None
        self.selected_cell = None
        self.available_moves = []


    def move_figure(self, target_cell):
        sourse_cell = self.selected_figure.cell
        self.selected_figure.move(target_cell)

        target_cell.set_figure(self.selected_figure)
        sourse_cell.set_figure(None)

        self.deselect_figure()


    def switch_player(self):
        if self.current_player is self.white_player:
            self.current_player = self.black_player
        else:
            self.current_player = self.white_player    


    def get_available_moves(self, figure):
        moves = []

        # if self.is_check(): 
        #     for cell in self.rescue_moves:
        #         if figure.can_move(cell):
        #             moves.append(cell)

        #     return moves        

        for row in self.cells:
            for cell in row:
                if figure.can_move(cell):
                    if figure.name == "KING":
                        if not self.is_cell_attacked(cell):
                            moves.append(cell)
                    else:
                        moves.append(cell)

        return moves


    def get_enemy_figures(self):
        enemy_figures = []

        for row in self.cells:
            for cell in row:
                figure = cell.figure
                if (figure is not None and figure.color != self.current_player.color):
                    enemy_figures.append(figure)   

        return enemy_figures
    

    def is_check(self):
        player_king = self.get_player_king(self.current_player)

        if self.is_cell_attacked(player_king):
            return True
        
        return False
    
    
    def get_player_king(self, curr_player):
        for row in self.cells:
            for cell in row:
                figure = cell.figure
                if figure is not None and figure.name == "KING" and figure.color == curr_player.color:
                    return cell
        return None
    

    def is_cell_attacked(self, cell):
        enemy_figures = self.get_enemy_figures()
        for figure in enemy_figures:
            if figure.can_attack(cell):
                return True
        return False 
    

    def get_attacking_figure(self, king):
        enemy_figures = self.get_enemy_figures()
        for enemy_figure in enemy_figures:
            if enemy_figure.can_attack(king):
                return enemy_figure

        return None
    

    def get_rescue_moves(self, attacking_figure, king):
        rescue_moves = []

        # Отримати координати короля
        king_x = king.x // 128
        king_y = king.y // 128
        
        
        # Отримати напрямок руху до короля
        attacking_figure_x = attacking_figure.cell.x // 128
        attacking_figure_y = attacking_figure.cell.y // 128
            
        if attacking_figure.name == "ROOK":
            if king_x == attacking_figure_x:
                dx = 0
                if king_y > attacking_figure_y:
                    dy = 1
                else:
                    dy = -1
            elif king_y == attacking_figure_y:
                dy = 0
                if king_x > attacking_figure_x:
                    dx = 1
                else:
                    dx = -1

        if attacking_figure.name == "BISHOP":
            if abs(king_x - attacking_figure_x) == abs(king_y - attacking_figure_y):
                if king_x < attacking_figure_x:
                    dx = 1
                else:
                    dx = -1

                if king_y < attacking_figure_y:
                    dy = 1
                else:
                    dy = -1

        
        if attacking_figure.name == "QUEEN":
            if king_x == attacking_figure_x:
                dx = 0
                if king_x > attacking_figure_x:
                    dy = 1
                else:
                    dy = -1
            elif king_y == attacking_figure_y:
                dy = 0
                if king_y > attacking_figure_y:
                    dx = 1
                else:
                    dx = -1
            elif abs(king_x - attacking_figure_x) == abs(king_y - attacking_figure_y):
                if king_x < attacking_figure_x:
                    dx = 1
                else:
                    dx = -1
                if king_y < attacking_figure_y:
                    dy = 1
                else:
                    dy = -1

        # Перебрати клітинки по напрямку до короля
        x = (attacking_figure.cell.x // 128)
        y = (attacking_figure.cell.y // 128)

        print(str(x) + " " + str(y))
        
        while True:
            x += dx
            y += dy
            print(str(x) + " " + str(y))

            # Перевірити чи координати знаходяться в межах дошки
            if not (0 <= x < 8) or not (0 <= y < 8):
                break

            target_cell = self.get_cell(x, y)
            

            # Перевірити чи може атакуюча фігура атакувати або рухатись на цю клітинку
            if attacking_figure.can_attack(target_cell) or attacking_figure.can_move(target_cell):
                rescue_moves.append(target_cell)

            # Зупинитись якщо знайдена клітинка з королем
            if target_cell.figure is not None and target_cell.figure.name == "KING":
                break

        self.rescue_moves = rescue_moves
    

    def get_rescue_figures(self):
        king = self.get_player_king(self.current_player)
        attacking_figure = self.get_attacking_figure(king)

        self.get_rescue_moves(attacking_figure, king)

        for row in self.cells:
            for cell in row:
                figure = cell.figure
                if figure is not None and figure.color == self.current_player.color:
                    for rescue_move in self.rescue_moves:
                        if figure.can_move(rescue_move) or figure.can_attack(rescue_move):
                            if figure not in self.rescue_figures:
                                self.rescue_figures.append(figure)


    def get_cell(self, x, y):
        return self.cells[y][x]


    def add_figures(self, positions, figure_class):
        for position in positions:
            x, y = position
            cell = self.get_cell(x, y) 
            
            color = self.player_color.WHITE if (y > 1) else self.player_color.BLACK

            figure = figure_class(color, cell)
            cell.set_figure(figure)
    

    def add_bishops(self):
        positions = [(2, 0), (5, 0), (2, 7), (5, 7)]
        self.add_figures(positions, Bishop)
    

    def add_queens(self):
        positions = [(3, 0), (3, 7)]
        self.add_figures(positions, Queen)


    def add_kings(self):
        positions = [(4, 0), (4, 7)]
        self.add_figures(positions, King)


    def add_rooks(self):
        positions = [(0, 0), (7, 0), (0, 7), (7, 7)]
        self.add_figures(positions, Rook)
    

    def add_knights(self):
        positions = [(1, 0), (6, 0), (1, 7), (6, 7)]
        self.add_figures(positions, Knight)


    def add_pawns(self): 
        for i in range(8):
            black_cell = self.get_cell(i, 1)
            white_cell = self.get_cell(i, 6)

            black_cell.set_figure(Pawn(self.player_color.BLACK, black_cell))
            white_cell.set_figure(Pawn(self.player_color.WHITE, white_cell))


    def add_figures_on_board(self):
        self.add_pawns()
        self.add_rooks()
        self.add_knights()
        self.add_bishops() 
        self.add_queens()   
        self.add_kings()
        