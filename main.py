import pygame
import time
import os
import random
from pygame.locals import *

jump_speed = 3
screen_width, screen_h = 800, 500
screen_height = screen_h - 110
gravity = +0.1
objects = []
shot_time = 1
player = None
score = 0

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
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png(image)
		self.x, self.y = 0, screen_height - self.image.get_height()
		self.speedx, self.speedy = 0, 0
		self.renderer = pygame.sprite.RenderPlain(self)
		self.allow_gravity = True
		self.removing = False
		objects.append(self)

	def update(self):
		if self.allow_gravity:
			self.speedy += gravity
		self.x += self.speedx
		self.y += self.speedy
		self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
		if self.y + self.image.get_height() >= screen_height:
			self.speedy = 0
			self.y = screen_height - self.image.get_height()

		if self.x < -200 or self.x > screen_width + 200:
			self.remove()

	def remove(self):
		self.removing = True
		
class NonMoveableSprite(MoveableSprite):

	def update(self):
		self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
		return

class Player(MoveableSprite):
	shoot_delay = 0.5
	def __init__(self, image):
		MoveableSprite.__init__(self, image)
		self.shot_time = 0
		self.leftimage, self.leftrect = load_png('player_left.png')
		self.rightimage, self.rightrect = load_png('player_right.png')
		self.image = self.rightimage

	def can_jump(self):
		if self.speedy == 0:
			return True 
		return False

	def can_shoot(self):
		if time.time() - self.shot_time >= self.shoot_delay:
			return True
		return False

	def jump(self):
		if self.can_jump():
			self.speedy = -5

	def shoot(self):
		if self.can_shoot():
			self.shot_time = time.time()
			bullet = Bullet('bullet.png')
			bullet.y = self.y + self.image.get_height() / 2
			if self.image == self.rightimage:
				bullet.speedx = 6
				bullet.x = self.x + self.image.get_width()
			else:
				bullet.speedx = -6
				bullet.x = self.x

	def update(self):
		MoveableSprite.update(self)
		self.check_collision()
		if self.speedx < 0:
			self.image = self.leftimage
		elif self.speedx > 0:
			self.image = self.rightimage	

	def check_collision(self):
		for obj in objects:
			if type(obj) == Enemy:
				if self.rect.colliderect(obj.rect):
					obj.remove()			

class Bullet(MoveableSprite):
	def __init__(self, image):
		MoveableSprite.__init__(self, image)
		self.allow_gravity = False

	def update(self):
		MoveableSprite.update(self)
		self.check_collision()

	def check_collision(self):
		global score
		for obj in objects:
			if type(obj) == Enemy:
				if self.rect.colliderect(obj.rect):
					obj.remove()
					self.remove()
					score += 10

class Enemy(MoveableSprite):
	def __init__(self, image):
		MoveableSprite.__init__(self, image)
		self.speedx = -3
		self.x = screen_width
		self.y = screen_height - self.image.get_height()
		self.health = 1


def main():
	#Initialize Pygame
	pygame.init()
	screen = pygame.display.set_mode((screen_width, screen_h))
	pygame.display.set_caption('Hack Game')

	background_image = pygame.image.load("background.jpg").convert()

	font = pygame.font.Font(None,36)
	text = font.render("Score: " + str(score), 1, (50,0,200))
	textpos = text.get_rect()
	textpos.centerx = background_image.get_rect().centerx
	background_image.blit(text,textpos)

	screen.blit(background_image, (0, 0))
	pygame.display.flip()
	clock = pygame.time.Clock()

	heart1 = NonMoveableSprite('heart.png')
	heart1.x, heart1.y = 0, 0
	heart2 = NonMoveableSprite('heart.png')
	heart2.x, heart2.y = 64, 0
	heart3 = NonMoveableSprite('heart.png')
	heart3.x, heart3.y = 128, 0

	global player
	player = Player('player_right.png')
	leftdown, rightdown = False, False
	movespeed = 4	
	i = 0
	while True:
		i += 1
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					player.jump()
				elif event.key == K_LEFT:
					leftdown = True
					player.speedx = -movespeed
				elif event.key == K_RIGHT:
					rightdown = True
					player.speedx = movespeed
				elif event.key == K_z:
					player.shoot()					
			elif event.type == KEYUP:
				if event.key == K_LEFT:
					leftdown = False
				elif event.key == K_RIGHT:
					rightdown = False

		if not leftdown and not rightdown and player.speedx != 0:
			player.speedx = 0
		elif leftdown and not rightdown and player.speedx > 0:
			player.speedx = -movespeed
		elif rightdown and not leftdown and player.speedx < 0:
			player.speedx = movespeed
			
		for obj in objects:
			screen.blit(background_image, obj.rect, obj.rect)
			obj.renderer.update()
			obj.renderer.draw(screen)
			if obj.removing:
				objects.remove(obj)
				screen.blit(background_image, obj.rect, obj.rect)
		pygame.display.flip()
		

		if i % 100 == 0:
			Enemy(random.choice(['zelda.png', 'mario.png', 'megaman.png']))
main()