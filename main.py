import pygame
import random
from pygame import *
import pygame.cursors
import asyncio
from cursor import Cursor

class GameManager:
    def __init__(self):
        # Define constants
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 640
        self.FPS = 60
        self.MOLE_WIDTH = 90
        self.MOLE_HEIGHT = 81
        self.FONT_SIZE = 31
        self.FONT_TOP_MARGIN = 26
        self.LEVEL_SCORE_GAP = 4
        self.LEFT_MOUSE_BUTTON = 1
        self.GAME_TITLE = "Whack A Mole - Game Programming - Assignment 1"
        self.TIMER = 120  # 120 seconds = 2 minutes
        # Initialize player's score, number of missed hits and level
        self.score = 0
        self.misses = 0
        self.level = 1
        self.speed = 1
        self.hit_rate = 0
        self.mode = "none"
        # Initialize screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        
        pygame.display.set_caption(self.GAME_TITLE)
        
        self.background = pygame.image.load("images/bg.png")
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        
        # Font object for displaying text
        self.font_obj = pygame.font.Font('./fonts/Ghostphobia.ttf', self.FONT_SIZE)
        
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
        self.hole_positions.append((145, 500))
        self.hole_positions.append((410, 500))
        self.hole_positions.append((357, 395))
        self.hole_positions.append((237, 430))
        self.hole_positions.append((125, 395))
        self.hole_positions.append((250, 337))
        self.hole_positions.append((395, 330))
        self.hole_positions.append((250, 304))
        self.hole_positions.append((30, 300))
        self.hole_positions.append((140, 250))
        self.hole_positions.append((350, 248))
        self.hole_positions.append((350, 215))
        self.hole_positions.append((142, 215))
        
        # Bam effect and positions of bam effect
        self.bam_effect = pygame.image.load("images/bam.png").subsurface(0, 0, 60, 40)
        self.bam_effect_positions = []
        self.bam_effect_positions.append((145, 550))
        self.bam_effect_positions.append((410, 550))
        self.bam_effect_positions.append((357, 445))
        self.bam_effect_positions.append((237, 480))
        self.bam_effect_positions.append((125, 445))
        self.bam_effect_positions.append((250, 387))
        self.bam_effect_positions.append((395, 380))
        self.bam_effect_positions.append((250, 354))
        self.bam_effect_positions.append((30, 350))
        self.bam_effect_positions.append((140, 300))
        self.bam_effect_positions.append((350, 298))
        self.bam_effect_positions.append((350, 265))
        self.bam_effect_positions.append((142, 265))
        
        # Init debugger
        self.debugger = Debugger("debug")
        # Sound effects
        self.soundEffect = SoundEffect()
        
    def get_interval_by_level(self, initial_interval):
        # Ensure the interval decreases more significantly for higher levels
        new_interval = initial_interval / (self.speed)  # Example formula

        # Ensure the interval doesn't become too low or negative
        min_interval = 0.1  # Set a minimum interval value
        return max(new_interval, min_interval)

    # Check whether the mouse click hit the hole or not
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
        current_level_string = "MODE: " + str(self.mode)
        level_text = self.font_obj.render(current_level_string, True, (255, 255, 255))
        level_text_pos = level_text.get_rect()
        level_text_pos.centerx = self.SCREEN_WIDTH / 10 * 1
        level_text_pos.centery = self.FONT_TOP_MARGIN
        self.screen.blit(level_text, level_text_pos)
    
    # Draw the pause menu
    def pause_menu(self):
        pygame.draw.rect(self.surface, (128, 128, 128, 150), [0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT])
        pygame.draw.rect(self.surface, 'dark gray', [20, 150, 600, 50])
        restartBtn = pygame.draw.rect(self.surface, 'white', [200, 220, 240, 50])
        self.surface.blit(self.font_obj.render('Game Paused', True, 'black'), (249, 160)) 
        self.surface.blit(self.font_obj.render('Restart', True, 'black'), (271, 230))
        self.screen.blit(self.surface, (0, 0))
        return restartBtn

    def show_menu(self):
        menu_font = self.font_obj
        title_font = pygame.font.Font('./fonts/Ghostphobia.ttf', 100)  # Larger font for the title
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            title = title_font.render("Whack The Zom", True, (255, 0, 0))
            title_rect = title.get_rect(center=(self.SCREEN_WIDTH/2, 150))
            current_x = pygame.mouse.get_pos()[0]
            current_y = pygame.mouse.get_pos()[1]

            easy_button = pygame.Rect((200, 250, 240, 50))
            medium_button = pygame.Rect((200, 320, 240, 50))
            hard_button = pygame.Rect((200, 390, 240, 50))

            if (200 <= current_x and current_x <= 440 and 250 <= current_y and current_y <= 300):
                pygame.draw.rect(self.screen, (255, 255, 255), easy_button)
                easy_border = pygame.Rect((198, 248, 244, 54))
                pygame.draw.rect(self.screen, (0, 0, 0), easy_border, 2)
            else: pygame.draw.rect(self.screen, (255, 255, 255), easy_button)
            
            if (200 <= current_x and current_x <= 440 and 320 <= current_y and current_y <= 370):
                pygame.draw.rect(self.screen, (255, 255, 255), medium_button)
                medium_border = pygame.Rect((198, 318, 244, 54))
                pygame.draw.rect(self.screen, (0, 0, 0), medium_border, 2)
            else: pygame.draw.rect(self.screen, (255, 255, 255), medium_button)
            
            if (200 <= current_x and current_x <= 440 and 390 <= current_y and current_y <= 440):
                pygame.draw.rect(self.screen, (255, 255, 255), hard_button)
                hard_border = pygame.Rect((198, 388, 244, 54))
                pygame.draw.rect(self.screen, (0, 0, 0), hard_border, 2)
            else: pygame.draw.rect(self.screen, (255, 255, 255), hard_button)

            easy_text = menu_font.render("Easy", True, (0, 0, 0))
            medium_text = menu_font.render("Medium", True, (0, 0, 0))
            hard_text = menu_font.render("Hard", True, (0, 0, 0))
            
            easy_text_center = easy_text.get_rect(center=(self.SCREEN_WIDTH/2, 275))
            medium_text_center = medium_text.get_rect(center=(self.SCREEN_WIDTH/2, 345))
            hard_text_center = hard_text.get_rect(center=(self.SCREEN_WIDTH/2, 415))
            
            self.screen.blit(title, title_rect)
            self.screen.blit(easy_text, easy_text_center)
            self.screen.blit(medium_text, medium_text_center)
            self.screen.blit(hard_text, hard_text_center)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if easy_button.collidepoint(mouse_pos):
                        return 1, "Easy"  # Easy level
                    if medium_button.collidepoint(mouse_pos):
                        return 2, "Medium"  # Medium level
                    if hard_button.collidepoint(mouse_pos):
                        return 3, "Hard"  # Hard level
                    
    def end_game_display(self):
        # Display the final score
        self.screen.blit(self.background, (0, 0))
        final_score_text = self.font_obj.render(f"Final Score: {self.score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2))
        self.screen.blit(final_score_text, final_score_rect)
            
        menu_font = self.font_obj
        play_again_button = pygame.Rect((200, 360, 240, 50))  
        pygame.draw.rect(self.screen, (255, 255, 255), play_again_button)
        play_again_text = menu_font.render("Play again", True, (0, 0, 0))
        play_again_text_center = play_again_text.get_rect(center=(self.SCREEN_WIDTH/2, 385))
        self.screen.blit(play_again_text, play_again_text_center) 
        
        new_game_button = pygame.Rect((200, 420, 240, 50))  
        pygame.draw.rect(self.screen, (255, 255, 255), new_game_button)
        new_game_text = menu_font.render("New game", True, (0, 0, 0))
        new_game_text_center = new_game_text.get_rect(center=(self.SCREEN_WIDTH/2, 445))
        self.screen.blit(new_game_text, new_game_text_center) 

        pygame.display.flip()
            
        # Wait for a key press to exit
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting_for_input = False
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if play_again_button.collidepoint(mouse_pos):
                        return "Play again"
                    if new_game_button.collidepoint(mouse_pos):
                        return "New game"
        return False
        
    # Start the game's main loop
    # Contains some logic for handling animations, mole hit events, etc..
    async def start(self, playAgain = False):
        self.score = 0
        self.misses = 0
        self.hit_rate = 0
        if not playAgain:
            self.level, self.mode = self.show_menu()
        self.speed = self.level
        
        # Play the theme based on the selected mode
        self.soundEffect.playTheme(self.mode)
            
        cycle_time = 0
        num = -1
        prev_num = -1
        loop = True
        pause = False
        is_down = False
        interval = 0.1
        initial_interval = 1
        is_stunned = False
        star_move_count = 0
        frame_num = 0
        left = 0
        restartButton = self.pause_menu()
        clock = pygame.time.Clock()
        c = Cursor()
        
        self.frame_change_rate = 1
        
        # Initialize the countdown timer (120 seconds = 2 minutes)
        # countdown_timer = self.TIMER
        countdown_timer = 10
        
        for i in range(len(self.mole)):
            self.mole[i].set_colorkey((0, 0, 0))
            self.mole[i] = self.mole[i].convert_alpha()
            
        while loop:
            mil = clock.tick(self.FPS)  # Time passed in milliseconds
            sec = mil / 1000.0  # Convert milliseconds to seconds

            if not pause:
                countdown_timer -= sec  # Decrement the countdown timer
            if countdown_timer <= 0:
                pygame.mouse.set_visible(True)  # Make sure the mouse is visible
                print("Game over")
                endGameChoise = self.end_game_display()
                if endGameChoise == "New game":
                    print("New game")
                    await self.start()  # Start a new game
                elif endGameChoise == "Play again":
                    print("Play again")
                    self.score = 0
                    self.misses = 0
                    self.hit_rate = 0
                    await self.start(True)
                # break  # Break out of the game loop
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                    pygame.quit()
                    exit()
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
                    if restartButton.collidepoint(event.pos):
                        # pause = False
                        # num = -1
                        # self.score = 0
                        # self.misses = -1
                        # self.level = 1
                        # self.hit_rate = 0
                        # is_down = False
                        # left = 0
                        self.score = 0
                        self.misses = 0
                        self.hit_rate = 0

                        await self.start(True)
                if event.type == MOUSEBUTTONDOWN and event.button == self.LEFT_MOUSE_BUTTON and not pause:
                    # mouse_x, mouse_y = event.pos  # Get the x, y position of the mouse click
                    # self.debugger.log(f"Mouse clicked at: ({mouse_x}, {mouse_y})")  # Log the position
                    
                    self.soundEffect.playFire()
                    c.set_hammer(True)
                    if self.is_mole_hit(mouse.get_pos(), self.hole_positions[frame_num]) and num > 0 and left == 0:
                        num = 3
                        left = 14
                        is_down = False
                        interval = 0
                        star_move_count = 0
                        is_stunned = True
                        self.score += 1  # Increase player's score
                        if (self.score and self.score % 10 == 0):
                            self.speed += 1
                        # print("level: ", self.level, ", speed: ", self.speed)
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
                    num += self.frame_change_rate  # Use frame change rate here
                else:
                    num -= self.frame_change_rate  # Use frame change rate here
                if num == 4:
                    interval = 0.3/(self.speed*2)
                elif num == 3:
                    num -= 1
                    is_down = True
                    self.soundEffect.playPop()
                    interval = self.get_interval_by_level(initial_interval)  # get the newly decreased interval value
                else:
                    interval = 0.1/(self.speed*2)
                cycle_time = 0
            # Update the display
            if not pause:
                self.screen.blit(self.background, (0, 0))
                self.update()
                
                # Update and draw the countdown timer
                timer_text = self.font_obj.render(f"Time Left: {int(countdown_timer)}s", True, (255, 255, 255))
                timer_text_pos = timer_text.get_rect()
                timer_text_pos.centerx = self.SCREEN_WIDTH / 2
                timer_text_pos.centery = self.FONT_TOP_MARGIN + 30
                self.screen.blit(timer_text, timer_text_pos)
                
                if num >= 0 and num <= 5:
                    if cycle_time > interval:
                        pic = self.mole[num] 
                        self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                    else:
                        pic = self.mole[prev_num]
                        self.screen.blit(pic, (self.hole_positions[frame_num][0] - left, self.hole_positions[frame_num][1]))
                c.draw()
                c.update()
                
            
            if is_stunned is True:
                if star_move_count <= 15:
                    star_move_count += 3
                    self.screen.blit(self.bam_effect, (self.bam_effect_positions[frame_num][0] - star_move_count, self.bam_effect_positions[frame_num][1] - star_move_count))
                else: 
                    is_stunned = False
                    
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
        
    def playTheme(self, mode):
        if mode == "Easy":
            pygame.mixer.music.load("sounds/grasswalk.mp3")
        elif mode == "Medium":
            pygame.mixer.music.load("sounds/loonboon.mp3")
        elif mode == "Hard":
            pygame.mixer.music.load("sounds/ultimate_battle.mp3")
            
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Play indefinitely

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
