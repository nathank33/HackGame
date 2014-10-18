import pygame
import time

jump_speed = 3
width, height = 640, 480
gravity = -0.5

class MoveableSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		#self.image, self.rect = load_png('ball.png') # Change this
		self.x, self.y = 0, 0
		self.speedx, self.speedy = 0, 0

class Player(MoveableSprite):
	def __init__(self):
		MoveableSprite.__init__(self)

	def jump(self):
		print("Handle Jump")

	def shoot(self):
		print("Handle Shooting")
	

class Bullet(MoveableSprite):
	def __init__(self):
		MoveableSprite.__init__(self)

def main():
	#Initialize Pygame
	player = Player('Hero')
	pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Hack Game')

	background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialise clock
    clock = pygame.time.Clock()

    while True:
    	clock.tick(60)
    	for event in pygame.event.get():
    		if event.type == QUIT:
    			return
    		elif event.type == JUMP and player.can_jump:
    			player.jump()
    		#elif event.type == SHOOT and player.can_shoot:
    		#	player.shoot()


    	# Handle all of the events