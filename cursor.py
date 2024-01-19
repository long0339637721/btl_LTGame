import pygame

class Cursor:
    def __init__(self):
        self.spr = pygame.transform.scale(pygame.image.load('images/hammer.png').convert_alpha(), (64, 80))
        self.root = pygame.display.get_surface()
        self.x = 0 
        self.y = 0
        self.mouse_down = False
        self.rect = pygame.rect.Rect(self.x, self.y, 64, 80)
        
    def draw(self):
        self.root.blit(self.spr, (self.x, self.y))
    
    def update(self):
        self.x = pygame.mouse.get_pos()[0] - 10 if self.mouse_down == False else pygame.mouse.get_pos()[0] - 30
        self.y = pygame.mouse.get_pos()[1] - 30
        self.rect = pygame.rect.Rect(self.x, self.y, 64, 80)
        
    def set_hammer(self, mouse_down):
        if mouse_down:
            self.mouse_down = mouse_down
            self.spr = pygame.transform.rotate(self.spr, 60)
        else:
            self.spr = pygame.transform.scale(pygame.image.load('images/hammer.png').convert_alpha(), (64, 80))
        

    
    