from copy import copy

from entities.EntityBase import EntityBase
from entities.Item import Item


class Pot(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, item, sound, dashboard, level, gravity=0):
        super(Pot, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("pot1"))
        self.type = "Block"
        self.triggered = False
        self.time = 0
        self.maxTime = 10
        self.sound = sound
        self.dashboard = dashboard
        self.vel = 1
        self.item = item
        self.level = level

    def update(self, cam):
        if self.alive and not self.triggered:
            pass
        else:
            self.animation.image = self.spriteCollection.get("pot2").image
            if self.item == 'Potion':
                self.level.addPotion(self.rect.y // 32 - 1, self.rect.x // 32)
                self.sound.play_sfx(self.sound.powerup_appear)
            self.item = None
            if self.time < self.maxTime:
                self.time += 1
                self.rect.y -= self.vel
            else:
                if self.time < self.maxTime * 2:
                    self.time += 1
                    self.rect.y += self.vel
        self.screen.blit(
            self.spriteCollection.get("sky").image,
            (self.rect.x + cam.x, self.rect.y + 2),
        )
        self.screen.blit(self.animation.image, (self.rect.x + cam.x, self.rect.y - 1))
