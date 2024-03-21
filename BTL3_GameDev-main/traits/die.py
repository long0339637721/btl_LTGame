class DieTrait:
    def __init__(self, entity, animation=None, screen=None, deltaTime=7 ):
        self.entity = entity
        self.timer = 0
        self.dieTimer = 0
        self.deltaTime = deltaTime
        self.animation = animation
        self.screen = screen
    
    # def update(self):
    #     position = (self.entity.getPos()[0] , self.entity.getPos()[1])
    #     if self.entity.inDead:
    #         if (self.entity.invincibilityFrames//2) % 2 == 0:
    #             self.animation.update(True, False, False, False, True) # Is character and is dead
    #             self.animation.die() 
    #             self.screen.blit(self.animation.image, position)
                
    def die(self):
        if self.entity.inDead == False:
            self.entity.inDead = True