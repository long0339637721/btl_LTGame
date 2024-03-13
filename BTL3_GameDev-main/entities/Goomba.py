import pygame

from classes.Animation import Animation
from classes.ColliderGoomba import ColliderGoomba
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBaseGoomba import EntityBaseGoomba
from traits.leftrightwalkGoomba import LeftRightWalkTraitGoomba


class Goomba(EntityBaseGoomba):
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(Goomba, self).__init__(y, x - 1, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("goomba-1").image,
                self.spriteCollection.get("goomba-2").image,
                self.spriteCollection.get("goomba-3").image,
                self.spriteCollection.get("goomba-4").image,
                self.spriteCollection.get("goomba-5").image,
                self.spriteCollection.get("goomba-6").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTraitGoomba(self, level)
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = ColliderGoomba(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound
        self.textPos = Vec2D(0, 0)

    def update(self, camera):
        if self.alive:
            self.applyGravity()
            self.drawGoomba(camera)
            self.leftrightTrait.update()
            self.checkEntityCollision()
        else:
            self.onDead(camera)

    def drawGoomba(self, camera):
        if self.leftrightTrait.direction == -1:
            self.screen.blit(self.animation.image, (self.rect.x  + camera.x, self.rect.y ))
        else:
            self.screen.blit(
                pygame.transform.flip(self.animation.image, True, False),
                (self.rect.x  + camera.x , self.rect.y ),
            )
        self.animation.update()

    def onDead(self, camera):
        if self.timer == 0:
            self.setPointsTextStartPosition(self.rect.x + 3, self.rect.y)
        if self.timer < self.timeAfterDeath:
            self.movePointsTextUpAndDraw(camera)
            self.drawFlatGoomba(camera)
        else:
            self.alive = None
        self.timer += 0.1

    def drawFlatGoomba(self, camera):
        self.screen.blit(
            self.spriteCollection.get("goomba-flat").image,
            (self.rect.x + camera.x, self.rect.y),
        )

    def setPointsTextStartPosition(self, x, y):
        self.textPos = Vec2D(x, y)

    def movePointsTextUpAndDraw(self, camera):
        self.textPos.y += -0.5
        self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8)
    
    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)

    def _onCollisionWithMob(self, mob, collisionState):
        if collisionState.isColliding and mob.bouncing:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)
