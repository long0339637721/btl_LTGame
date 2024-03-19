import pygame, sys
import os

class Boss(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y, Fire_ball, move_sprite, screen, camera,mario):
		super().__init__()
		self.x=pos_x*37 - 800
		self.y=pos_y*37
		self.target_x=0
		self.camera = camera
		self.screen =screen
		self.mario=mario
		self.fire_ball = Fire_ball
		self.sprite_group = move_sprite
		
		self.scale= 1
		self.initial_scale = self.scale  # Save initial scale
		
		
		self.sprites_idle = self.load_images('./new_Boss/1_idle/', scale_factor=2)
		self.sprites_walk = self.load_images('./new_Boss/2_walk/', scale_factor=2)
		self.sprites_attack = self.load_images('./new_Boss/3_atk/', scale_factor=2)
		self.sprites_death = self.load_images('./new_Boss/5_death/', scale_factor=2)

		

		self.attack_animation = False
		self.attack_normal_animation = False
		self.walk_animation=True
		self.death_animation = False
		self.idle_animtion=False

		self.current_sprite_appear = len(self.sprites_death)-1

		self.current_sprite_walk = 0
		self.current_sprite_attack = 0
		self.current_sprite_idle = 0
		self.current_sprite_death = 0

		self.image = self.sprites_death[self.current_sprite_appear]

		self.rect = self.image.get_rect()
		self.rect.topleft = [700,225]

		self.idle_duration = 1000
		self.start_idle_timne=0
		self.cur_time_idle=0

		self.Walk_duration = 4000
		self.start_Walk_timne=0
		self.cur_time_Walk=0

		self.hitbox_take_hit = (self.x + 110, self.y, 70, 70)
		self.hitbox_hit_left = (self.x - 30, self.y, 50, 50)
		self.hitbox_hit_right = ((self.x + 150, self.y, 50, 50))
		self.hitbox_target = (10 + 110, 200 + 80, 70, 70)
		self.health = 100

	def Behavior(self):
		if self.death_animation:
			self.update_death(0.25)
			return
		
		self.rect.topleft = [self.x + self.camera.x,self.y - 55]
		self.target_x = self.mario.rect.x
		self.hitbox_target=self.mario.rect

		self.update_walk(0.25)
		self.update_attack_fire(0.25)
		self.update_idle(0.25)
		self.update_attack_Normal(0.25)
		self.Check_scale()

		if self.idle_animtion == False:
			self.move_boss()
		self.fire_ball.Fire_anim(0.25,self.scale*(-1))
		self.fire_ball.hotbox_target = self.mario.rect
		if self.fire_ball.ismove == False:
			if self.scale == 1:
				self.fire_ball.x = self.x
				self.fire_ball.y = self.y
				
			else:
				self.fire_ball.x = self.x + 200
				self.fire_ball.y = self.y
			self.fire_ball.update_pos(self.fire_ball.x,self.fire_ball.y)
			self.sprite_group.remove(self.fire_ball)
		else:
			self.sprite_group.add(self.fire_ball)
			self.fire_ball.move(-1 * self.scale)

	
	def take_hit(self):
		if self.health > 0:
			hpDecreased = self.mario.traits["attackTrait"].checkAttackBoss(self)
			if hpDecreased > 0:
				self.health -= hpDecreased 
		else:
			self.death_animation = True

	def draw_health(self):
		if self.death_animation == False:
			pygame.draw.rect(self.screen, (255,0,0), (self.x + 150 + self.camera.x, self.y - 10, 100, 10))
			pygame.draw.rect(self.screen, (0,128,0), (self.x + 150 + self.camera.x, self.y - 10, 100 - (10 * (10 - self.health/10)), 10))

	def Check_scale(self):
		if self.target_x > self.x + 125:
			self.scale = -1
		elif self.target_x - 125 < self.x:
			self.scale = 1

	def attack_normal(self):
		self.attack_normal_animation = True
	def attack(self):
		self.attack_animation = True
	def walk(self):
		self.walk_animation=True

	def idle(self):
		self.idle_animtion=True
	

	def death(self):
		self.death_animation=True

	def update_attack_fire(self,speed):
		if self.attack_animation == True:
			self.current_sprite_attack += speed
			if self.current_sprite_attack == 10:
				self.fire_ball.start_move = pygame.time.get_ticks()
				self.fire_ball.Fire()
			if int(self.current_sprite_attack) >= len(self.sprites_attack):
				self.current_sprite_attack = 0
				self.attack_animation = False
				self.idle_duration = 2000
				self.start_idle_timne=pygame.time.get_ticks()
				self.idle()
				return
			if self.scale == 1:
				self.image = self.sprites_attack[int(self.current_sprite_attack)]
			else:
				self.image = pygame.transform.flip(self.sprites_attack[int(self.current_sprite_attack)], True, False)
			
	
	def update_attack_Normal(self,speed):
		if self.attack_normal_animation == True:
			self.current_sprite_attack += speed
			if int(self.current_sprite_attack) >= len(self.sprites_attack):
				self.current_sprite_attack = 0
				self.attack_normal_animation = False
				self.idle_duration = 2000
				self.start_idle_timne=pygame.time.get_ticks()
				self.idle()
				return
			if self.scale == 1:
				self.image = self.sprites_attack[int(self.current_sprite_attack)]
			else:
				self.image = pygame.transform.flip(self.sprites_attack[int(self.current_sprite_attack)], True, False)

	def move_boss(self):
		if self.walk_animation == True:
			if self.scale == 1:
				self.x-=2
				self.rect.topleft = [self.x + self.camera.x,self.y-55]
				self.hitbox_take_hit = (self.x, self.y, 70, 70)
				self.hitbox_hit_left = (self.x - 30, self.y, 50, 50)
				self.hitbox_hit_right = ((self.x + 150, self.y, 50, 50))
			else:
				self.x+=2
				self.rect.topleft = [self.x + self.camera.x,self.y-55]
				self.hitbox_take_hit = (self.x, self.y, 70, 70)
				self.hitbox_hit_left = (self.x - 30, self.y, 50, 50)
				self.hitbox_hit_right = ((self.x + 150, self.y, 50, 50))

			self.cur_time_Walk=pygame.time.get_ticks()
			if (self.cur_time_Walk-self.start_Walk_timne) > self.Walk_duration:
				self.current_sprite_walk = 0
				self.walk_animation = False
				self.attack()
				return
			elif self.Collision_Boss():
				self.mario.powerUpState-=1
				
				print(self.mario.powerUpState)
				if self.mario.powerUpState < 0:
					self.mario.gameOver()

				self.current_sprite_walk = 0
				self.walk_animation = False
				self.attack_normal()

	def Collision_Boss(self):
		if self.hitbox_hit_left[1] + self.hitbox_hit_left[3] > self.hitbox_target[1] and self.hitbox_hit_left[1] - self.hitbox_hit_left[3] < self.hitbox_target[1]:
			if (self.x + self.hitbox_hit_left[2]*2 < self.hitbox_target[0] + self.hitbox_target[2] and self.scale == 1) or (self.hitbox_hit_right[0] + self.hitbox_hit_right[2]*1.5 > self.hitbox_target[0] + self.hitbox_target[2] and self.scale == -1):
				return True
		return False

	def update_walk(self,speed):
		if self.walk_animation == True:		
			self.current_sprite_walk += speed
			if self.scale == 1:
				self.image = self.sprites_walk[int(self.current_sprite_walk) % len(self.sprites_walk)]
			else:
				self.image = pygame.transform.flip(self.sprites_walk[int(self.current_sprite_walk) % len(self.sprites_walk)], True, False)

	def update_idle(self,speed):

		if self.idle_animtion == True:
			self.cur_time_idle=pygame.time.get_ticks()
			self.current_sprite_idle += speed
			if (self.cur_time_idle-self.start_idle_timne) > self.idle_duration:
				self.current_sprite_idle = 0
				self.idle_animtion = False
				self.start_Walk_timne = pygame.time.get_ticks()
				self.Check_scale()
				self.walk()
				return
			if self.scale == 1:
				self.image = self.sprites_idle[int(self.current_sprite_idle)%len(self.sprites_idle)]
			else:
				self.image = pygame.transform.flip(self.sprites_idle[int(self.current_sprite_idle)%len(self.sprites_idle)], True, False)
			
			

	def update_death(self,speed):
		if self.death_animation == True:
			self.current_sprite_death += speed
			if int(self.current_sprite_death) >= len(self.sprites_death):
				return
			if self.scale == 1:
				self.image = self.sprites_death[int(self.current_sprite_death)]
			else:
				self.image = pygame.transform.flip(self.sprites_death[int(self.current_sprite_death)], True, False)
    
	def load_images(self, path, scale_factor=1.8):
		images = []
		file_list = sorted(os.listdir(path))  # Sort files alphabetically
		for filename in file_list:
			image_path = os.path.join(path, filename)
			if os.path.isfile(image_path):
				image = pygame.image.load(image_path)
				# Scale up the image
				width, height = image.get_size()
				scaled_image = pygame.transform.scale(image, (width*scale_factor, height*scale_factor))
				images.append(scaled_image)
		return images


		