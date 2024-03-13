import pygame, sys
# from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,surf,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

pygame.init()
screen = pygame.display.set_mode((640, 480))
tmx_data = load_pygame('Level1-1.tmx')
sprite_group = pygame.sprite.Group()

# cycle through all layers
for layer in tmx_data.visible_layers:
	# if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
	if hasattr(layer,'data'):
		for x,y,surf in layer.tiles():
			pos = (x * 16, y * 16)
			Tile(pos = pos, surf = surf, groups = sprite_group)

# for obj in tmx_data.objects:
# 	pos = obj.x,obj.y
# 	if obj.type in ('Building', 'Vegetation'):
# 		Tile(pos = pos, surf = obj.image, groups = sprite_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('black')
	sprite_group.draw(screen)
	
	for obj in tmx_data.objects:
		pos = obj.x,obj.y
		if obj.type == 'Shape':
			if obj.name == 'Marker':
				pygame.draw.circle(screen,'red',(obj.x,obj.y),5)
			if obj.name == 'Rectangle':
				rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
				pygame.draw.rect(screen,'yellow',rect)

			if obj.name == 'Ellipse':
				rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
				pygame.draw.ellipse(screen,'blue',rect)

			if obj.name == 'Polygon':
				points = [(point.x,point.y) for point in obj.points]
				pygame.draw.polygon(screen,'green',points)
	
	pygame.display.update()