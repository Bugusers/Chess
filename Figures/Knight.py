import pygame as pg
from Figures.Figure import Figure

class Knight(Figure): 
    def __init__(self, color, cell):
        super().__init__(color, cell)
        self.name = "KNIGHT"
        self.image = pg.image.load("assets/blackKnight.png") if self.color == (0, 0, 0) else pg.image.load("assets/whiteKnight.png")

    def can_move(self, target):
        if not super().can_move(target):
            return False    
        
        d_x = abs(self.cell.x // 128 - target.x // 128) 
        d_y = abs(self.cell.y // 128 - target.y // 128)

        return (d_x == 1 and d_y == 2) or (d_x == 2 and d_y == 1)      
    
    def can_attack(self, target):
        if self.can_move(target):
            return True
            
        return False

    