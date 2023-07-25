import pygame as pg
from Figures.Figure import Figure
from Color import Color

class Pawn(Figure): 
    def __init__(self, color, cell):
        super().__init__(color, cell)
        self.name = "PAWN"
        self.image = pg.image.load("assets/blackPawn.png") if self.color == (0, 0, 0) else pg.image.load("assets/whitePawn.png")
        self.is_first_step = True

    def can_move(self, target):
        if not super().can_move(target):
            return False

        direction = 1 if self.cell.figure.color == Color.BLACK else -1
        first_step_direction = 2 if self.cell.figure.color == Color.BLACK else -2


        target_x = target.x // 128
        target_y = target.y // 128
        cell_x = self.cell.x // 128
        cell_y = self.cell.y // 128

        if (
            target_y == cell_y + direction or
            (self.is_first_step and target_y == cell_y + first_step_direction)
        ) and target_x == cell_x and self.cell.board.get_cell(target_x, target_y).is_empty():
            return True
    

        if (
            target_y == cell_y + direction and
            (target_x == cell_x + 1 or target_x == cell_x - 1) and
            self.cell.is_enemy(target)
        ):
            return True
    

        return False
    
    def move(self, target):
        super().move(target)
        self.is_first_step = False

    def can_attack(self, target):
        if self.can_move(target):
            return True
            
        return False
    
        
        