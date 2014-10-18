import pygame

class MoveableSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image, self.rect = load_png('ball.png') # Change this
		self.x, self.y = 0, 0
		self.speedx, self.speedy = 0, 0

class Player(MoveableSprite):
	def __init__(self):
		MoveableSprite.__init__(self)

	def can_jump(self):
		if self.speedy == 0:
			return True
		return False

	def can_shoot(self):

	def jump(self):
		print("Handle Jump")

	def shoot(self):
		print("Handle Shooting")
	

class Bullet(MoveableSprite):
	def __init__(self):
		MoveableSprite.__init__(self)

width, height = 640, 480
def main():
	#Initialize Pygame
	pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Hack Game')

	background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    while True:
    	clock.tick(60)

    	# Handle all of the events