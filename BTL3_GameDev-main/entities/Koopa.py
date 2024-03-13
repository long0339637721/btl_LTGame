import pygame

from classes.Animation import Animation
from classes.ColliderKoopa import ColliderKoopa
from classes.EntityCollider import EntityCollider
from classes.Maths import Vec2D
from entities.EntityBaseKoopa import EntityBaseKoopa
from traits.leftrightwalkKoopa import LeftRightWalkTraitKoopa


class Koopa(EntityBaseKoopa):
    def __init__(self, screen, spriteColl, x, y, level, sound):
        super(Koopa, self).__init__(x, y, 1.25)
        self.spriteCollection = spriteColl
        self.animation = Animation(
            [
                self.spriteCollection.get("koopa-1").image,
                self.spriteCollection.get("koopa-2").image,
                self.spriteCollection.get("koopa-3").image,
                self.spriteCollection.get("koopa-4").image,
                self.spriteCollection.get("koopa-5").image,
                self.spriteCollection.get("koopa-6").image,
                self.spriteCollection.get("koopa-7").image,
                self.spriteCollection.get("koopa-8").image,
            ]
        )
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTraitKoopa(self, level)
        self.timer = 0
        self.timeAfterDeath = 35
        self.type = "Mob"
        self.dashboard = level.dashboard
        self.collision = ColliderKoopa(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound

    def update(self, camera):
        if self.alive and self.active:
            self.updateAlive(camera)
            self.checkEntityCollision()
        elif self.alive and not self.active and not self.bouncing:
            self.sleepingInShell(camera)
            self.checkEntityCollision()
        elif self.bouncing:
            self.shellBouncing(camera)

    def drawKoopa(self, camera):
        if self.leftrightTrait.direction == -1:
            self.screen.blit(
                self.animation.image, (self.rect.x  + camera.x, self.rect.y)
            )
        else:
            self.screen.blit(
                pygame.transform.flip(self.animation.image, True, False),
                (self.rect.x   + camera.x, self.rect.y),
            )

    def shellBouncing(self, camera):
        self.leftrightTrait.speed = 3
        self.applyGravity()
        self.animation.image = self.spriteCollection.get("koopa-hiding").image
        self.drawKoopa(camera)
        self.leftrightTrait.update()

    def sleepingInShell(self, camera):
        if self.timer < self.timeAfterDeath:
            self.screen.blit(
                self.spriteCollection.get("koopa-hiding").image,
                (self.rect.x + camera.x, self.rect.y ),
            )
        else:
            self.alive = True
            self.active = True
            self.bouncing = False
            self.timer = 0
        self.timer += 0.1

    def updateAlive(self, camera):
        self.applyGravity()
        self.drawKoopa(camera)
        self.animation.update()
        self.leftrightTrait.update()

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            if ent is not self:
                collisionState = self.EntityCollider.check(ent)
                if collisionState.isColliding:
                    if ent.type == "Mob":
                        self._onCollisionWithMob(ent, collisionState)

    def _onCollisionWithMob(self, mob, collisionState):
        if collisionState.isColliding and mob.bouncing:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)
