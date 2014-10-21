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
boss_timer = 0
level_timer = 0
player = None
generate = True
heart1, heart2, heart3 = None, None, None
regular_monster_list = ['zelda.png', 'fish.png', 'megaman.png', 'charizard.png']

def memo(f):
    cache = {}
    def memoized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memoized

@memo
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
	def __init__(self, rightimage, leftimage=None):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_png(rightimage)
		self.rightimage = self.image
		if leftimage == None:
			self.leftimage = pygame.transform.flip(self.rightimage, True, False)
		else:
			self.leftimage = load_png(leftimage)[0]
		self.renderer = pygame.sprite.RenderPlain(self)

		self.x, self.y = 0, screen_height - self.image.get_height()
		self.speedx, self.speedy = 0, 0
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

		if self.x < -300 or self.x > screen_width + 200:
			self.remove()

		if self.image == self.rightimage and self.speedx < 0:
			self.image = self.leftimage
		elif self.image == self.leftimage and self.speedx > 0:
			self.image = self.rightimage

	def remove(self):
		self.removing = True
		
class NonMoveableSprite(MoveableSprite):
	def update(self):
		self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
		return

class Player(MoveableSprite):
	shoot_delay = 0
	score = 0
	movespeed = 4
	def __init__(self, rightimage='player.png'):
		MoveableSprite.__init__(self, rightimage)
		self.shot_time = 0
		self.x = screen_width / 2
		self.image = self.rightimage
		self.is_alive = True

	def can_jump(self):
		if self.speedy == 0:
			return True 
		return False

	def can_shoot(self):
		if self.is_alive and time.time() - self.shot_time >= self.shoot_delay:
			return True
		return False

	def jump(self):
		if self.can_jump():
			self.speedy = -5

	def shoot(self):
		self.shot_time = time.time()
		bullet = Bullet()
		if self.image == self.rightimage:
			bullet.speedx = 6
			bullet.x = self.x + self.image.get_width()
		else:
			bullet.speedx = -6
			bullet.x = self.x - 20
		bullet.y = self.y + self.image.get_height() / 2

	def update(self):
		MoveableSprite.update(self)
		self.check_collision()
		if self.speedx < 0:
			self.image = self.leftimage
		elif self.speedx > 0:
			self.image = self.rightimage	

	def check_collision(self):
		for obj in objects:
			if issubclass(type(obj), Enemy):
				if self.rect.colliderect(obj.rect):
					obj.remove()	
					if heart3 in objects:
						heart3.remove()
					elif heart2 in objects:
						heart2.remove()
					else:
						heart1.remove()
						self.speedy = -1.5
						self.allow_gravity = False
						self.is_alive = False

class Attribute(NonMoveableSprite):
	print('do somethin')

class Bullet(MoveableSprite):
	def __init__(self, image='bullet.png'):
		MoveableSprite.__init__(self, image)
		self.allow_gravity = False

	def update(self):
		MoveableSprite.update(self)
		self.check_collision()

	def check_collision(self):
		global score
		for obj in objects:
			if isinstance(obj, Enemy):
				if self.rect.colliderect(obj.rect):
					obj.health -= 1
					self.remove()
					if obj.health == 0:
						obj.remove()
						Player.score += obj.score

class Gun(object):
	print ('do somethin')

class Enemy(MoveableSprite):
	score = 10
	def __init__(self, image, health = 1):
		MoveableSprite.__init__(self, image)
		self.speedx = -3
		self.x = screen_width
		self.y = screen_height - self.image.get_height()
		self.health = health

class Boss(Enemy):
	def __init__(self, image = 'Bowser_right.png', health=200):
		Enemy.__init__(self, image, health)
		self.speedx = -.3
		self.x = screen_width + 10

class Scoreboard(Player):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Score: %d" % (Player.score)
        self.image = self.font.render(self.text, 1, (75, 0, 130))
        self.rect = self.image.get_rect(center = (400, 17))


def main():
	#Initialize Pygame
	pygame.init()
	screen = pygame.display.set_mode((screen_width, screen_h))
	pygame.display.set_caption('Hack Game')

	background_image = pygame.image.load("data/background.jpg").convert()
	screen.blit(background_image, (0, 0))
	pygame.display.flip()
	clock = pygame.time.Clock()

	global heart1, heart2, heart3
	heart1 = NonMoveableSprite('heart.png')
	heart1.x, heart1.y = 5, 0
	heart2 = NonMoveableSprite('heart.png')
	heart2.x, heart2.y = 69, 0
	heart3 = NonMoveableSprite('heart.png')
	heart3.x, heart3.y = 133, 0

	scoreboard = Scoreboard()
	scoreSprite = pygame.sprite.Group(scoreboard)
	pygame.mixer.music.load('music.mp3')
	# pygame.mixer.music.play(0, 120)

	global player
	player = Player()
	leftdown, rightdown = False, False	
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
					player.speedx = -Player.movespeed
				elif event.key == K_RIGHT:
					rightdown = True
					player.speedx = Player.movespeed
				elif event.key == K_z and player.can_shoot():
					player.shoot()					
			elif event.type == KEYUP:
				if event.key == K_LEFT:
					leftdown = False
				elif event.key == K_RIGHT:
					rightdown = False

		if not leftdown and not rightdown and player.speedx != 0:
			player.speedx = 0
		elif leftdown and not rightdown and player.speedx > 0:
			player.speedx = -Player.movespeed
		elif rightdown and not leftdown and player.speedx < 0:
			player.speedx = Player.movespeed

		# Clears current scoreboard, and updates it with new score	
		scoreSprite.clear(screen, background_image)
		scoreSprite.update()
		scoreSprite.draw(screen)

		for obj in objects:
			screen.blit(background_image, obj.rect, obj.rect)
			obj.renderer.update()
			obj.renderer.draw(screen)
			if obj.removing:
				objects.remove(obj)
				screen.blit(background_image, obj.rect, obj.rect)
		pygame.display.flip()

		global generate, level_timer
		if generate:
			generateMonsters()

		if Boss not in [type(obj) for obj in objects]:
			generate = True

		if heart1.removing:
			font = pygame.font.Font(None,100)
			text = font.render("YOU DIED!", 1, (255,0,00))
			textpos = text.get_rect()
			textpos.centerx = background_image.get_rect().centerx
			background_image.blit(text,textpos)
			screen.blit(background_image, (0, 0))

		if Player.score == 200 and time.time() - level_timer > 50:
			background_image = pygame.image.load("data/level_2.jpg").convert()
			screen.blit(background_image, (0, 0))
			level_timer = time.time()

		monsters = [obj for obj in objects if issubclass(type(obj), Enemy)]

		if Boss not in [type(obj) for obj in objects] and Player.score + len(monsters)*10 != 200:
			generate = True
		else:
			generate = False


def generateMonsters():
	if Player.score == 200:
		global generate, boss_timer
		generate = False
		boss_timer = time.time()
		Boss()
		pygame.mixer.music.play(0, 130)

	if random.randint(1, 70) == 1: 
		enemy = Enemy(random.choice(regular_monster_list))
		enemy.speedx *= 0.65 + random.random()
		if random.randint(1, 3) == 1:
			enemy.speedx *= -1
			enemy.x = -50
		if random.randint(1, 3) == 1:
			enemy.speedy = -random.randint(3,8)
		
main()