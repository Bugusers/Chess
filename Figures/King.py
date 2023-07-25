import pygame as pg
from Figures.Figure import Figure

class King(Figure): 
    def __init__(self, color, cell):
        super().__init__(color, cell)
        self.name = "KING"
        self.image = pg.image.load("assets/blackKing.png") if self.color == (0, 0, 0) else pg.image.load("assets/whiteKing.png")

    def can_move(self, target):
        if not super().can_move(target):
            return False    
        
        d_x = False if abs(self.cell.x // 128 - target.x // 128) > 1 else True
        d_y = False if abs(self.cell.y // 128 - target.y // 128) > 1 else True

        return d_x and d_y     
    
    def can_attack(self, target):
        if self.can_move(target):
            return True
            
        return False
        