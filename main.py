import pygame
import random
from pygame import *
import pygame.cursors
import asyncio
from cursor import Cursor

class GameManager:
    def __init__(self):
        # Define constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "Whack A Mole - Game Programming - Assignment 1"
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        self.hit_rate = 0
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption(self.GAME_TITLE)
        self.background = pygame.image.load("images/bg.jpeg")
        # Font object for displaying text
        self.font_obj = pygame.font.Font('./fonts/GROBOLD.ttf', self.FONT_SIZE)
        # 6 different states
        sprite_sheet = pygame.image.load("images/zombie.png")
        self.mole = []
        self.mole.append(sprite_sheet.subsurface(270, 0, 120, 100))
        self.mole.append(sprite_sheet.subsurface(309, 0, 120, 100))
        self.mole.append(sprite_sheet.subsurface(449, 0, 120, 100))
        self.mole.append(sprite_sheet.subsurface(575, 0, 120, 100))
        self.mole.append(sprite_sheet.subsurface(717, 0, 120, 100))
        self.mole.append(sprite_sheet.subsurface(853, 0, 120, 100))
        self.mole.append(sprite_sheet.subsurface(853, 0, 120, 100))

        # Positions of the holes in background
        self.hole_positions = []
        self.hole_positions.append((100, 227))
        self.hole_positions.append((200,227))
        self.hole_positions.append((285, 227))
        self.hole_positions.append((443, 227))
        self.hole_positions.append((534, 227))
        self.hole_positions.append((622, 227))
        self.hole_positions.append((104,365))
        self.hole_positions.append((205,365))
        self.hole_positions.append((293, 365))
        self.hole_positions.append((448, 365))
        self.hole_positions.append((539, 365))


        # Init debugger
        self.debugger = Debugger("debug")
        # Sound effects
        self.soundEffect = SoundEffect()

    # Calculate the player level according to his current score & the LEVEL_SCORE_GAP constant
    def get_player_level(self):
        newLevel = 1 + int(self.score / self.LEVEL_SCORE_GAP)
        if newLevel != self.level:
            # if player get a new level play this sound
            self.soundEffect.playLevelUp()
        return 1 + int(self.score / self.LEVEL_SCORE_GAP)

    # Get the new duration between the time the mole pop up and down the holes
    # It's in inverse ratio to the player's current level
    def get_interval_by_level(self, initial_interval):
        new_interval = initial_interval - self.level * 0.15
        if new_interval > 0:
            return new_interval
        else:
            return 0.05

    # Check whether the mouse click hit the mole or not
    def is_mole_hit(self, mouse_position, current_hole_position):
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        current_hole_x = current_hole_position[0]
        current_hole_y = current_hole_position[1]
        if (mouse_x > current_hole_x) and (mouse_x < current_hole_x + self.MOLE_WIDTH) and (mouse_y > current_hole_y) and (mouse_y < current_hole_y + self.MOLE_HEIGHT):
            return True
        else:
            return False

    # Update the game states, re-calculate the player's score, misses, level
    def update(self):
        # Update the player's score
        current_score_string = "SCORE: " + str(self.score)
        score_text = self.font_obj.render(current_score_string, True, (255, 255, 255))
        score_text_pos = score_text.get_rect()
        score_text_pos.centerx = self.SCREEN_WIDTH / 10 * 3.5
        score_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(score_text, score_text_pos)
        # Update the player's misses
        current_misses_string = "MISSES: " + str(self.misses)
        misses_text = self.font_obj.render(current_misses_string, True, (255, 255, 255))
        misses_text_pos = misses_text.get_rect()
        misses_text_pos.centerx = self.SCREEN_WIDTH / 10 * 6
        misses_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(misses_text, misses_text_pos)
        # Update the player's misses
        current_hitrate_string = "HIT RATE: " + str(f'{self.hit_rate:3.0f}%') 
        hit_rate_text = self.font_obj.render(current_hitrate_string, True, (255, 255, 255))
        hit_rate_text_pos = hit_rate_text.get_rect()
        hit_rate_text_pos.centerx = self.SCREEN_WIDTH / 10 * 8.5
        hit_rate_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(hit_rate_text, hit_rate_text_pos)
        # Update the player's level
        current_level_string = "LEVEL: " + str(self.level)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 10 * 1
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)
    
    # Draw the pause menu
    def pause_menu(self):
        pygame.draw.rect(self.surface, (128, 128, 128, 150), [0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        pygame.draw.rect(self.surface, 'dark gray', [100, 150, 600, 50])
        restartBtn = pygame.draw.rect(self.surface, 'white', [280, 220, 240, 50])
        self.surface.blit(self.font_obj.render('Game Paused', True, 'black'), (300, 160))
        self.surface.blit(self.font_obj.render('Restart', True, 'black'), (340, 230))
        self.screen.blit(self.surface, (0, 0))
        return restartBtn

    # Start the game's main loop
    # Contains some logic for handling animations, mole hit events, etc..
    async def start(self):
        cycle_time = 0
        num = -1
        prev_num = -1
        loop = True
        pause = False
        is_down = False
        interval = 0.1
        initial_interval = 1
        frame_num = 0
        left = 0
        restartBtn = self.pause_menu()
        # Time control variables
        clock = pygame.time.Clock()
        c = Cursor()
        
        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if pause:
                            pause = False
                        else:
                            self.pause_menu()
                            pause = True
                if pause:
                    pygame.mouse.set_visible(True)
                else:
                    pygame.mouse.set_visible(False)
                if event.type == MOUSEBUTTONDOWN and pause:
                    if restartBtn.collidepoint(event.pos):
                        pause = False
                        num = -1
                        self.score = 0
                        self.misses = -1
                        self.level = 1
                        self.hit_rate = 0
                        is_down = False
                        left = 0
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON and not pause:
                    self.soundEffect.playFire()
                    c.set_hammer(True)
                    if self.is_mole_hit(mouse.get_pos(), self.hole_positions[frame_num]) and num > 0 and left == 0:
                        num = 3
                        left = 14
                        is_down = False
                        interval = 0
                        self.score += 1  # Increase player's score
                        self.level = self.get_player_level()  # Calculate player's level
                        # Stop popping sound effect
                        self.soundEffect.stopPop()
                        # Play hurt sound
                        self.soundEffect.playHurt()
                        # self.update()
                    else:
                        self.misses += 1
                        # self.update()
                    if self.misses == 0:
                        self.hit_rate = 100
                    else:
                        self.hit_rate = (self.score / (self.misses + self.score ))*100
                    if self.hit_rate < 50:
                        self.soundEffect.stopFire()

                if event.type == MOUSEBUTTONUP and event.button == self.LEFT_MOUSE_BUTTON:
                    c.set_hammer(False)
            
            if num > 5:
                prev_num = num
                num = -1
                left = 0

            if num == -1:
                prev_num = num
                num = 0
                is_down = False
                interval = 0.5
                frame_num = random.randint(0, 10)

            mil = clock.tick(self.FPS)
            sec = mil / 1000.0
            cycle_time += sec
            if cycle_time > interval and not pause:
                prev_num = num
                if is_down is False:
                    num += 1
                else:
                    num -= 1
                if num == 4:
                    interval = 0.3
                elif num == 3:
                    num -= 1
                    is_down = True
                    self.soundEffect.playPop()
                    interval = self.get_interval_by_level(initial_interval)  # get the newly decreased interval value
                else:
                    interval = 0.1
                cycle_time = 0
            # Update the display
            if not pause:
                self.screen.blit(self.background, (0, 0))
                self.update()
                if num >= 0 and num <= 5:
                    if cycle_time > interval:
                        pic = self.mole[num] 
                        self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                    else:
                        pic = self.mole[prev_num]
                        self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                c.draw()
                c.update()
            pygame.display.flip()
            await asyncio.sleep(0)


# The Debugger class - use this class for printing out debugging information
class Debugger:
    def __init__(self, mode):
        self.mode = mode

    def log(self, message):
        if self.mode == "debug":
            print("> DEBUG: " + str(message))


class SoundEffect:
    def __init__(self):
        self.mainTrack = pygame.mixer.music.load("sounds/themesong.wav")
        self.fireSound = pygame.mixer.Sound("sounds/fire.wav")
        self.fireSound.set_volume(0.5)
        self.popSound = pygame.mixer.Sound("sounds/pop.wav")
        self.popSound.set_volume(0.1)
        self.hurtSound = pygame.mixer.Sound("sounds/hurt.wav")
        self.hurtSound.set_volume(0.1)
        self.levelSound = pygame.mixer.Sound("sounds/point.wav")
        self.levelSound.set_volume(0.1)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.05)

    def playFire(self):
        self.fireSound.play()

    def stopFire(self):
        self.fireSound.sop()

    def playPop(self):
        self.popSound.play()

    def stopPop(self):
        self.popSound.stop()

    def playHurt(self):
        self.hurtSound.play()

    def stopHurt(self):
        self.hurtSound.stop()

    def playLevelUp(self):
        self.levelSound.play()

    def stopLevelUp(self):
        self.levelSound.stop()

###############################################################
# Initialize the game
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# Run the main loop
my_game = GameManager()
asyncio.run(my_game.start())
# Exit the game if the main loop ends
pygame.quit()
