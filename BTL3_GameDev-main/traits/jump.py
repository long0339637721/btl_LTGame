class JumpTrait:
    def __init__(self, entity):
        self.verticalSpeed = -12
        self.jumpHeight = 120
        self.entity = entity
        self.entity.inAir = False
        self.initalHeight = 384
        self.deaccelerationHeight = self.jumpHeight - ((self.verticalSpeed*self.verticalSpeed)/(2*self.entity.gravity))
        self.canDoubleJump = True


    def jump(self, jumping):
        if jumping:
            if self.entity.onGround:
                self.entity.sound.play_sfx(self.entity.sound.jump)
                self.entity.vel.y = self.verticalSpeed
                self.initialHeight = self.entity.rect.y  # Set initial height only when starting to jump
                self.decelerationHeight = self.jumpHeight - ((self.verticalSpeed * self.verticalSpeed) / (2 * self.entity.gravity))
                self.entity.inAir = True
                self.entity.inJump = True
                self.entity.obeyGravity = False  # always reach maximum height
            elif self.entity.inAir and self.canDoubleJump:  # If already in air, set position to current to stand on air
                # self.entity.rect.y = self.initialHeight  # Keep the current position as temporary ground
                self.entity.inAir = False
                self.entity.inJump = False
                self.entity.vel.y = 0  # Stop vertical velocity

                self.entity.sound.play_sfx(self.entity.sound.jump)
                self.entity.vel.y = self.verticalSpeed
                self.initialHeight = self.entity.rect.y  # Set initial height only when starting to jump
                self.decelerationHeight = self.jumpHeight - ((self.verticalSpeed * self.verticalSpeed) / (2 * self.entity.gravity))
                self.entity.inAir = True
                self.entity.inJump = True
                self.entity.obeyGravity = False  # always reach maximum height


        if self.entity.inJump:
            if (self.initialHeight - self.entity.rect.y) >= self.decelerationHeight or self.entity.vel.y == 0:
                self.entity.inJump = False
                self.entity.obeyGravity = True

    def reset(self):
        self.entity.inAir = False
