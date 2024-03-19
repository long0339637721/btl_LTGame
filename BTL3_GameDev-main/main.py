import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
from Boss.boss import Boss
from Boss.fire_ball_boss import Fire_ball
import pygame
from pygame.locals import *
import sys

windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    

    while not menu.start:
        menu.update()

    mario = Mario(0, 0, level, screen, dashboard, sound)
    is_boss=False
    moving_sprites = pygame.sprite.Group()
    fire_ball = Fire_ball(20, 20,mario.camera,mario)
    boss = Boss(118,6,fire_ball,moving_sprites,screen,mario.camera,mario)
    moving_sprites.add(boss)

    clock = pygame.time.Clock()

    while not mario.restart:
        pygame.display.set_caption("Swordio running with {:d} FPS".format(int(clock.get_fps())))
        if mario.pause:
            mario.pauseObj.update()
        else:
            level.drawLevel(mario.camera)
            dashboard.update(mario.powerUpState)
            mario.update()
            if (mario.getPosIndexAsFloat().x > 110.0):
                is_boss=True
            if is_boss:
                pressedKeys = pygame.key.get_pressed()
                isAttacking = pressedKeys[K_SPACE]
                if isAttacking:
                    boss.take_hit()
                isAttacking = False
                boss.draw_health()
                boss.Behavior()

        moving_sprites.draw(screen)
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
