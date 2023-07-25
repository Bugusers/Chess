import pygame as pg


class Cell(pg.sprite.Sprite):
    def __init__(self, x, y, size, color, board):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.board = board
        self.figure = None
        self.rect = pg.Rect(x, y, size, size)
        

    def draw_cell(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        self.draw_figure(screen)


    def draw_figure(self, screen):
        if self.figure is not None:
            self.figure.draw(screen, self.x, self.y, self.size)


    def set_figure(self, figure):
        self.figure = figure


    def is_enemy(self, target):
        if target.figure:
            return self.figure.color != target.figure.color
        return False


    def is_empty(self):
        return self.figure is None


    def is_empty_horisontal(self, target):
        if self.y != target.y:
            return False
        
        min_x = round(min(self.x // 128, target.x // 128))
        max_x = round(max(self.x // 128, target.x // 128))

        for x in range(min_x + 1, max_x): 
            if not self.board.get_cell(x, self.y // 128).is_empty():
                return False

        return True    


    def is_empty_vertical(self, target):
        if self.x != target.x:
            return False
        
        min_y = round(min(self.y // 128, target.y // 128))
        max_y = round(max(self.y // 128, target.y // 128))

        for y in range(min_y + 1, max_y):
            if not self.board.get_cell(self.x // 128, y).is_empty():
                return False

        return True    
    

    def is_empty_diagonal(self, target):
        abs_x = abs(target.x // 128 - self.x // 128)
        abs_y = abs(target.y // 128 - self.y // 128)

        if abs_x != abs_y :
            return False

        dy = 1 if self.y < target.y else -1 
        dx = 1 if self.x < target.x else -1 

        for i in range(1, abs_y):
            if not self.board.get_cell((self.x // 128 )+ dx * i, (self.y // 128) + dy * i).is_empty():
                return False

        return True  
        
        
    