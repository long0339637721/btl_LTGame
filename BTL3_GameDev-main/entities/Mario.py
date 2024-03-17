import pygame

from classes.Animation import Animation
from classes.Camera import Camera
from classes.ColliderCharacter import ColliderCharacter
from classes.EntityCollider import EntityCollider
from classes.Input import Input
from classes.Sprites import Sprites
from entities.EntityBaseCharacter import EntityBaseCharacter
from entities.Mushroom import RedMushroom
from entities.Potion import Potion
from traits.bounce import bounceTrait
from traits.go import GoTrait
from traits.jump import JumpTrait
from traits.attack import AttackTrait
from classes.Pause import Pause

spriteCollection = Sprites().spriteCollection
smallAnimation = Animation(
    # [
    #     spriteCollection["mario_run1"].image,
    #     spriteCollection["mario_run2"].image,
    #     spriteCollection["mario_run3"].image,
    #     spriteCollection["mario_run4"].image,
    #     spriteCollection["mario_run5"].image,
    #     spriteCollection["mario_run6"].image,
    #     spriteCollection["mario_run7"].image,
    #     spriteCollection["mario_run8"].image,
    # ],
    [
        spriteCollection["character-run-1"].image,
        spriteCollection["character-run-2"].image,
        spriteCollection["character-run-3"].image,
        spriteCollection["character-run-4"].image,
        spriteCollection["character-run-5"].image,
        spriteCollection["character-run-6"].image,
        spriteCollection["character-run-7"].image,
        spriteCollection["character-run-8"].image,
    ],
    # spriteCollection["mario_idle"].image,
    # spriteCollection["character-idle-1"].image,
    [
      spriteCollection["character-idle-1"].image,
      spriteCollection["character-idle-2"].image,
      spriteCollection["character-idle-3"].image,
      spriteCollection["character-idle-4"].image,  
      spriteCollection["character-idle-5"].image,
      spriteCollection["character-idle-6"].image,
      spriteCollection["character-idle-7"].image,
      spriteCollection["character-idle-8"].image,
    ],
    # spriteCollection["mario_jump"].image,
    [
        spriteCollection["character-jump-2"].image,
        spriteCollection["character-jump-16"].image,
    ],
    # [
    #     spriteCollection["mario_attack1"].image,
    #     spriteCollection["mario_attack2"].image,
    #     spriteCollection["mario_attack3"].image,
    #     spriteCollection["mario_attack4"].image,
    #     spriteCollection["mario_attack5"].image,
    #     spriteCollection["mario_attack6"].image,
    #     spriteCollection["mario_attack7"].image,
    #     spriteCollection["mario_attack8"].image,
    # ],
    [
        spriteCollection["character-attack-1"].image,
        spriteCollection["character-attack-2"].image,
        spriteCollection["character-attack-3"].image,
        spriteCollection["character-attack-4"].image,
        spriteCollection["character-attack-5"].image,
        spriteCollection["character-attack-6"].image,
        spriteCollection["character-attack-7"].image,
        spriteCollection["character-attack-8"].image,
        spriteCollection["character-attack-9"].image,
        spriteCollection["character-attack-10"].image,
        spriteCollection["character-attack-11"].image,
        spriteCollection["character-attack-12"].image,
        spriteCollection["character-attack-13"].image,
        spriteCollection["character-attack-14"].image,
        spriteCollection["character-attack-15"].image,
        spriteCollection["character-attack-16"].image,
        spriteCollection["character-attack-17"].image,
        spriteCollection["character-attack-18"].image,
        spriteCollection["character-attack-19"].image,
        spriteCollection["character-attack-20"].image,
        spriteCollection["character-attack-21"].image,
        spriteCollection["character-attack-22"].image,
        spriteCollection["character-attack-23"].image,
        spriteCollection["character-attack-24"].image,
        spriteCollection["character-attack-25"].image,
        spriteCollection["character-attack-26"].image,
        spriteCollection["character-attack-27"].image,
        spriteCollection["character-attack-28"].image,
    ],
)
bigAnimation = Animation(
    [
        spriteCollection["mario_big_run1"].image,
        spriteCollection["mario_big_run2"].image,
        spriteCollection["mario_big_run3"].image,
    ],
    spriteCollection["mario_big_idle"].image,
    spriteCollection["mario_big_jump"].image,
)


class Mario(EntityBaseCharacter):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.8):
        super(Mario, self).__init__(x, y, gravity)
        self.camera = Camera(self.rect, self)
        self.sound = sound
        self.input = Input(self)
        self.inAir = False
        self.inJump = False
        self.inAttack = False
        self.powerUpState = 3
        self.invincibilityFrames = 0
        self.traits = {
            "jumpTrait": JumpTrait(self),
            "goTrait": GoTrait(smallAnimation, screen, self.camera, self),
            "bounceTrait": bounceTrait(self),
            "attackTrait": AttackTrait(self),
        }

        self.levelObj = level
        self.collision = ColliderCharacter(self, level)
        self.screen = screen
        self.EntityCollider = EntityCollider(self)
        self.dashboard = dashboard
        self.restart = False
        self.pause = False
        self.pauseObj = Pause(screen, self, dashboard)

    def update(self):
        if self.invincibilityFrames > 0:
            self.invincibilityFrames -= 1
        self.updateTraits()
        self.moveMario()
        self.camera.move()
        self.applyGravity()
        self.checkEntityCollision()
        self.input.checkForInput()

    def moveMario(self):
        self.rect.y += self.vel.y
        self.collision.checkY()
        self.rect.x += self.vel.x
        self.collision.checkX()

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Item":
                    self._onCollisionWithItem(ent)
                elif ent.type == "Block":
                    self._onCollisionWithBlock(ent)
                elif ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)
    
    def checkSwordMobCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.checkSword(ent)
            if collisionState:
                if ent.type == "Mob" and not isinstance(ent, Potion):
                    self.killEntityBySword(ent)
                elif ent.type == "Block":
                    print(ent.triggered)
                    ent.triggered = True
            

    def _onCollisionWithItem(self, item):
        self.levelObj.entityList.remove(item)
        self.dashboard.points += 100
        self.dashboard.coins += 1
        self.sound.play_sfx(self.sound.coin)

    def _onCollisionWithBlock(self, block):
        if not block.triggered:
            self.dashboard.coins += 1
            self.sound.play_sfx(self.sound.bump)
        block.triggered = True

    def _onCollisionWithMob(self, mob, collisionState):
        if isinstance(mob, RedMushroom) and mob.alive:
            # self.powerup(1)
            self.killEntity(mob)
            self.sound.play_sfx(self.sound.powerup)
        elif isinstance(mob, Potion) and mob.alive:
            # self.powerup(1)
            self.powerUpState += 1
            self.dashboard.lives = self.powerUpState
            self.killEntity(mob)
            self.sound.play_sfx(self.sound.powerup)
        elif collisionState.isTop and (mob.alive or mob.bouncing):
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            self.bounce()
            self.killEntity(mob)
        elif collisionState.isTop and mob.alive and not mob.active:
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            mob.timer = 0
            self.bounce()
            mob.alive = False
        elif collisionState.isColliding and mob.alive and not mob.active and not mob.bouncing:
            mob.bouncing = True
            if mob.rect.x < self.rect.x:
                mob.leftrightTrait.direction = -1
                mob.rect.x += -5
                self.sound.play_sfx(self.sound.kick)
            else:
                mob.rect.x += 5
                mob.leftrightTrait.direction = 1
                self.sound.play_sfx(self.sound.kick)
        elif collisionState.isColliding and mob.alive and not self.invincibilityFrames:
            if self.powerUpState == 0:
                self.gameOver()
            elif self.powerUpState > 0:
                self.powerUpState -= 1
                self.dashboard.lives = self.powerUpState
                # self.traits['goTrait'].updateAnimation(smallAnimation)
                # x, y = self.rect.x, self.rect.y
                # self.rect = pygame.Rect(x, y + 32, 32, 32)
                self.invincibilityFrames = 60
                self.sound.play_sfx(self.sound.pipe)

    def bounce(self):
        self.traits["bounceTrait"].jump = True

    def killEntity(self, ent):
        if ent.__class__.__name__ != "Koopa":
            ent.alive = False
        else:
            ent.timer = 0
            ent.leftrightTrait.speed = 1
            ent.alive = True
            ent.active = False
            ent.bouncing = False
        self.dashboard.points += 100
    
    def killEntityBySword(self, ent):
        if ent.__class__.__name__ == "Koopa":
            ent.bouncing = False
            
        ent.alive = False
        self.dashboard.points += 100
        
    def gameOver(self):
        srf = pygame.Surface((640, 480))
        srf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        srf.set_alpha(128)
        self.sound.music_channel.stop()
        self.sound.music_channel.play(self.sound.death)

        for i in range(500, 20, -2):
            srf.fill((0, 0, 0))
            pygame.draw.circle(
                srf,
                (255, 255, 255),
                (int(self.camera.x + self.rect.x) + 16, self.rect.y + 16),
                i,
            )
            self.screen.blit(srf, (0, 0))
            pygame.display.update()
            self.input.checkForInput()
        while self.sound.music_channel.get_busy():
            pygame.display.update()
            self.input.checkForInput()
        self.restart = True

    def getPos(self):
        return self.camera.x + self.rect.x, self.rect.y

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def powerup(self, powerupID):
        if self.powerUpState == 0:
            if powerupID == 1:
                self.powerUpState = 1
                self.traits['goTrait'].updateAnimation(bigAnimation)
                self.rect = pygame.Rect(self.rect.x, self.rect.y-32, 32, 64)
                self.invincibilityFrames = 20
