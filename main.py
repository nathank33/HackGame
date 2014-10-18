import pygame
import time
import os
from pygame.locals import *

jump_speed = 3
width, height = 640, 480
gravity = -0.5
all_objects = []
shot_time = 1

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
		self.x, self.y = 0, 0
		self.speedx, self.speedy = 0, 0

	def update(self):
		self.x += self.speedx
		self.y += self.speedy
		self.rect.move([self.x, self.y])

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
		print("Handle Jump")


	def shoot(self):
		if can_shoot:
			self.shot_time = time.time()

	

class Bullet(MoveableSprite):
	def __init__(self):
		MoveableSprite.__init__(self)

def main():
	#Initialize Pygame
	
	pygame.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption('Hack Game')

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

    # Initialise clock
	clock = pygame.time.Clock()

	player = Player()
	while True:
		clock.tick(60)
		for obj in all_objects:
			objects.update()

		for event in pygame.event.get():
			if event.type == QUIT:
				return
			#elif event.type == JUMP and player.can_jump:
			#	player.jump()
			#elif event.type == SHOOT and player.can_shoot:
			#	player.shoot()
main()
