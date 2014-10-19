import pygame
import time
import os
from pygame.locals import *

jump_speed = 3
screen_width, screen_height = 640, 480
gravity = +0.1
all_objects = []
objectsprites = []
shot_time = 1
player = None

def load_png(name):
        """ Load image and return image object"""
        fullname = os.path.join('data', name)
        try:
                image = pygame.image.load(fullname)
                if image.get_alpha is None:
                        image = image.convert()
                else:
                        image = image.convert_alpha()
        except pygame.error as message:
                print('Cannot load image:', fullname)
                raise SystemExit(message)
        return image, image.get_rect()


class MoveableSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png('ball.png')
		self.x, self.y = 0, screen_height - self.image.get_height()
		self.speedx, self.speedy = 0, 0
		objectsprites.append(pygame.sprite.RenderPlain(self))

	def update(self):
		self.speedy += gravity
		self.x += self.speedx
		self.y += self.speedy
		self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
		if self.y + self.image.get_height() >= screen_height:
			self.speedy = 0
			self.y = screen_height - self.image.get_height()
		
		

class Player(MoveableSprite):
	shot_time = 0

	def __init__(self):
		MoveableSprite.__init__(self)

	def can_jump(self):
		if self.speedy == 0:
			return True 
		return False

	def can_shoot(self):
		if time.time() - self.shot_time >= shot_time:
			return True
		return False

	def jump(self):
		if self.can_jump():
			self.speedy = -5

	def shoot(self):
		if can_shoot:
			self.shot_time = time.time()

	

class Bullet(MoveableSprite):
	def __init__(self):
		MoveableSprite.__init__(self)

def main():
	#Initialize Pygame
	
	pygame.init()
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption('Hack Game')

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	screen.blit(background, (0, 0))
	pygame.display.flip()
	clock = pygame.time.Clock()

	global player
	player = Player()
	player.speedx = 1
	while True:
		clock.tick(60)
		for obj in all_objects:
			objects.update()

		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					player.jump()
					print("Jumping")
			elif event.type == K_LEFT or event.type == K_RIGHT:
				player.speed.x = 4

			#elif event.type == SHOOT and player.can_shoot:
			#	player.shoot()
		screen.blit(background, player.rect, player.rect)
		for sprite in objectsprites:
			sprite.update()
			sprite.draw(screen)
		pygame.display.flip()
main()
