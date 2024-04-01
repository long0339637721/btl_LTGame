import pygame, sys

class Fire_ball(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,camera,mario, screen):
      super().__init__()
      self.camera=camera
      self.mario=mario
      self.screen = screen
      self.x=pos_x
      self.y=pos_y

      self.sprites = []
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_0.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_1.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_2.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_3.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_4.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_5.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_6.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_7.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_8.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_9.png'))
      self.sprites.append(pygame.image.load('./Boss/fire_ball/1_10.png'))
      self.cur_sprite=0
      self.ismove = False
      self.image = self.sprites[0]
      self.rect = self.image.get_rect()
      self.duration_move=3000
      self.start_move = 0
      self.current_time = 0
      self.hitbox = (self.x + 100000, self.y - 10000, 0, 0)
      self.hitbox_target = mario.rect
      self.is_evade=False

    #update
    def Collision_fire(self,scale):
       if not(self.y - self.hitbox[3] < self.hitbox_target[1]) and ((self.hitbox[0] - 10 + self.hitbox[2] < self.hitbox_target[0] + self.hitbox_target[2] and scale == -1)or (self.hitbox[0] + 75  + self.hitbox[2] > self.hitbox_target[0] + self.hitbox_target[2] and scale == 1)):
            self.is_evade=True
       
       pygame.draw.rect(self.screen, (255,0,0), (self.x + 25 + self.camera.x, self.y + 40, 50, 25))
       pygame.draw.rect(self.screen, (255,0,0), (self.hitbox_target[0] + self.camera.x, self.hitbox_target[1], self.hitbox_target[2], self.hitbox_target[3]))
       
       fireBallArea = pygame.Rect(self.x + 25, self.y + 40, 50, 25)
       playerArea = pygame.Rect(self.hitbox_target[0], self.hitbox_target[1], self.hitbox_target[2], self.hitbox_target[3])
       
       if playerArea.colliderect(fireBallArea):
          if self.is_evade == False:
               self.ismove = False
               self.mario.powerUpState-=1
               print(self.mario.powerUpState)
               if self.mario.powerUpState < 0:
                  self.mario.gameOver()  
               print("hit_fire")
               
      #  if self.y + self.hitbox[3] > self.hitbox_target[1] and self.y - self.hitbox[3] < self.hitbox_target[1]:
      #    if (self.hitbox[0] - 10 + self.hitbox[2] < self.hitbox_target[0] + self.hitbox_target[2] and scale == -1) or (self.hitbox[0] + 75  + self.hitbox[2] > self.hitbox_target[0] + self.hitbox_target[2] and scale == 1):
      #       if self.is_evade == False:
      #          self.ismove = False
      #          self.mario.powerUpState-=1
      #          print(self.mario.powerUpState)
      #          if self.mario.powerUpState < 0:
      #             self.mario.gameOver()  
      #          print("hit_fire")


    def update_pos(self, pos_x, pos_y):
       self.rect.topleft = (pos_x + self.camera.x, pos_y)

    #move
    def move(self,scale):
      self.Collision_fire(scale)
      self.current_time = pygame.time.get_ticks()
      if (self.current_time - self.start_move) < self.duration_move:
         if scale == -1:
            self.x -= 5
            self.hitbox = (self.x + 20, self.y, 10, 10)
            self.update_pos(self.x,self.y)
         else:
            self.x += 5
            self.hitbox = (self.x + 20, self.y, 10, 10)
            self.update_pos(self.x,self.y)
      else:
         self.is_evade = False
         self.ismove = False

    #animation
    def Fire(self):
       self.ismove = True

    def Fire_anim(self,speed,scale):
        if self.ismove == True:
            self.cur_sprite += speed
            if scale==1:
               self.image = self.sprites[int(self.cur_sprite)%len(self.sprites)]
            else:
               self.image = pygame.transform.flip(self.sprites[int(self.cur_sprite)%len(self.sprites)], True, False)
          
    
    