import pygame 
from Board import Board
from Color import Color
from Player import Player

class Chess():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.player_color = Color()
        self.white_player = Player(self.player_color.WHITE)
        self.black_player = Player(self.player_color.BLACK)

        self.running = True

        self.FPS = 60
        self.size = 8
        self.square_size = 128

        self.screen = pygame.display.set_mode((self.square_size * self.size, self.square_size * self.size))

        self.board = Board(self.screen, self.square_size, self.player_color, self.white_player, self.black_player)

    def run(self):
        self.board.add_figures_on_board()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                        x = mouse_pos[0] // self.square_size
                        y = mouse_pos[1] // self.square_size
                        self.board.handle_click(x, y)
        

            self.board.draw_board()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

if __name__ == '__main__':
    chess_game = Chess()
    chess_game.run()
