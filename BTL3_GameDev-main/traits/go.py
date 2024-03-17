from pygame.transform import flip


class GoTrait:
    def __init__(self, animation, screen, camera, ent):
        self.animation = animation
        self.direction = 0
        self.heading = 1
        self.accelVel = 0.4
        self.decelVel = 0.25
        self.maxVel = 3.0
        self.screen = screen
        self.boost = False
        self.camera = camera
        self.entity = ent
        self.preY = 288

    def update(self):
        if self.boost:
            self.maxVel = 5.0
            self.animation.deltaTime = 4
        else:
            self.animation.deltaTime = 7
            if abs(self.entity.vel.x) > 3.2:
                self.entity.vel.x = 3.2 * self.heading
            self.maxVel = 3.2

        if self.direction != 0:
            self.heading = self.direction
            if self.heading == 1:
                if self.entity.vel.x < self.maxVel:
                    self.entity.vel.x += self.accelVel * self.heading
            else:
                if self.entity.vel.x > -self.maxVel:
                    self.entity.vel.x += self.accelVel * self.heading

            if not self.entity.inAir:
                self.animation.update(True, self.entity.inAir, self.entity.inAttack, True)
            else:
                if (self.entity.getPos()[1] < self.preY):
                    self.animation.inAir(1)
                else:
                    self.animation.inAir(2)
                self.preY = self.entity.getPos()[1]
        else:
            self.animation.update(True, self.entity.inAir, self.entity.inAttack, False)   
            if self.entity.vel.x >= 0:
                self.entity.vel.x -= self.decelVel
            else:
                self.entity.vel.x += self.decelVel
            if int(self.entity.vel.x) == 0:
                self.entity.vel.x = 0
                if self.entity.inAir:
                    if (self.entity.getPos()[1] < self.preY):
                        self.animation.inAir(1)
                    else:
                        self.animation.inAir(2)
                    self.preY = self.entity.getPos()[1]
                elif self.entity.inAttack:
                    self.animation.inAttack()
                    self.startJumping = False
                else:
                    self.animation.idle()
                    self.startJumping = False
        if (self.entity.invincibilityFrames//2) % 2 == 0:
            self.drawEntity()

    def updateAnimation(self, animation):
        self.animation = animation
        self.update()

    def drawEntity(self):
        position = (self.entity.getPos()[0] , self.entity.getPos()[1])
        if self.heading == 1:
            if self.animation.state == 2:
                position =(self.entity.getPos()[0] - 80 , self.entity.getPos()[1])
            elif self.animation.state == 1:
                position = (self.entity.getPos()[0] - 80 , self.entity.getPos()[1])
            elif self.animation.state == 3:
                position =(self.entity.getPos()[0] - 75 , self.entity.getPos()[1] - 76)
            elif self.animation.state == 0:
                position =(self.entity.getPos()[0] - 83 , self.entity.getPos()[1])
            self.screen.blit(self.animation.image, position)
        elif self.heading == -1:
            if self.animation.state == 0:
                position = (self.entity.getPos()[0] - 32 , self.entity.getPos()[1])
            elif self.animation.state == 2:
                position =(self.entity.getPos()[0] - 25 , self.entity.getPos()[1])
            elif self.animation.state == 1:
                position = (self.entity.getPos()[0] - 25 , self.entity.getPos()[1])
            elif self.animation.state == 3:
                position =(self.entity.getPos()[0] - 193 , self.entity.getPos()[1] - 76)
            self.screen.blit(
                flip(self.animation.image, True, False), position
            )
            # self.screen.blit(
            #         flip(self.animation.image, True, False), self.entity.getPos()
            # )
