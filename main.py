import pygame
import time
import os
import random
from math import sin, cos, atan2, degrees
from pygame.locals import *

lives = 3
jump_speed = 3
screen_width, screen_h = 800, 500
screen_height = screen_h - 110
gravity = +0.1
sprites = []
monsters = []
shot_time = 1
boss_timer = 0
level_timer = 0
player = None
generate = True
heart1, heart2, heart3 = None, None, None
bosses_spawned = []

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
		self.allow_ground = True
		self.removing = False
		sprites.append(self)

	def update(self):
		if self.allow_gravity:
			self.speedy += gravity
		self.x += self.speedx
		self.y += self.speedy
		self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
		
		if self.allow_ground:
			if self.y + self.image.get_height() >= screen_height:
				self.speedy = 0
				self.y = screen_height - self.image.get_height()

		if self.x < -300 or self.x > screen_width + 200 or self.y < -300 or self.y > screen_height + 200:
			self.remove()

		if self.image == self.rightimage and self.speedx < 0:
			self.face_left()
		elif self.image == self.leftimage and self.speedx > 0:
			self.face_right()

	def face_right(self):
		""" Sets the current image to the rightward image """
		self.image = self.rightimage

	def face_left(self):
		""" Sets the current image to the leftward image """
		self.image = self.leftimage

	def remove(self):
		""" Tells the main thread that this instance needs to be removed """
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
		self.health = 3

	def can_jump(self):
		""" Returns true if the player can jump """
		if self.speedy == 0:
			return True 
		return False

	def can_shoot(self):
		""" Returns true if the player can shoot """
		if self.is_alive and time.time() - self.shot_time >= self.shoot_delay:
			return True
		return False

	def jump(self):
		""" Attempts to cause the player to jump """
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

	def shoot_mouse(self, pos):
		""" Shoots a bullet based on the position of a mouse click """
		self.shot_time = time.time()
		xdiff = pos[0] - self.x
		ydiff = pos[1] - self.y
		theta = atan2(ydiff, xdiff)
		bullet = Bullet()
		bullet.speedx = cos(theta) * 6
		bullet.speedy = sin(theta) * 6
		bullet.refresh_image()
		bullet.y = self.y + self.image.get_height() / 2
		bullet.x = self.x + self.image.get_width() / 2
		if self.image == self.leftimage:
			bullet.x = self.x - self.image.get_width() / 2
			
		

	def update(self):
		MoveableSprite.update(self)
		self.check_collision()
		if self.speedx < 0:
			self.image = self.leftimage
		elif self.speedx > 0:
			self.image = self.rightimage	

	def check_collision(self):
		""" Checks if the player has collided with an enemy """
		for obj in sprites:
			if issubclass(type(obj), Enemy):
				if self.rect.colliderect(obj.rect):
					obj.remove()	
					self.health -= 1

class Attribute(NonMoveableSprite):
	print('do somethin')

class Bullet(MoveableSprite):
	def __init__(self, image='bullet.png'):
		MoveableSprite.__init__(self, image)
		self.allow_gravity = False
		self.allow_ground = False

	def update(self):
		MoveableSprite.update(self)
		self.check_collision()

	def refresh_image(self):
		""" Rotates the image based on the bullet direction """
		theta = atan2(self.speedy, self.speedx)
		rotated = pygame.transform.rotate(self.image, degrees(-theta))
		self.image, self.leftimage, self.rightimage = rotated, rotated, rotated

	def check_collision(self):
		""" Checks if the bullet has collided with an enemy
		and then calls the enemy's bullet collision method """
		global score
		for obj in sprites:
			if isinstance(obj, Enemy):
				if self.rect.colliderect(obj.rect):
					obj.bullet_collision(self)
					

class Gun(object):
	print ('do somethin')

############# Enemies ###########
class Enemy(MoveableSprite):
	score = 10
	def __init__(self, image, health = 1):
		MoveableSprite.__init__(self, image)
		self.speedx = -3
		self.x = screen_width
		self.y = screen_height - self.image.get_height()
		self.health = health
		monsters.append(self)

	def bullet_collision(self, bullet):
		bullet.remove()
		self.health -= 1
		if self.health == 0:
			self.remove()
			Player.score += self.score

	def remove(self):
		MoveableSprite.remove(self)
		if self in monsters:
			monsters.remove(self)

class Boss(Enemy):
	score = 100
	jump_time = 0
	def __init__(self, image = 'Bowser.png', health=100):
		Enemy.__init__(self, image, health)
		self.speedx = -.5
		self.x = screen_width + 10

	def update(self):
		if self.speedy == 0:
			if time.time() - self.jump_time > 10:
				self.speedy = -6
				self.jump_time = time.time()
		Enemy.update(self)

class Fish(Enemy):
	""" A fish has the sporatic behavior of jumping up and down randomly """
	score = 8
	def __init__(self):
		Enemy.__init__(self, 'fish.png')
		self.speedy = 0

	def update(self):
		if self.speedy == 0:
			if random.randint(1,11) < 7:
				self.speedy = -random.random() * 2
			else:
				self.speedy = -(random.random() * 6)
		Enemy.update(self)

class Phantom(Enemy):
	""" A phantom flies straight until it gets close to the player, 
	then it dive bombs the player """
	score = 12
	def __init__(self):
		Enemy.__init__(self, 'phantom.png')
		self.allow_gravity = False
		self.y = random.randint(50, 200)


	def update(self):
		diffx = abs(self.x - player.x)
		diffy = self.y - player.y
		if diffx < 200 and diffx > 100:
			self.speedy = diffy * -0.04
		Enemy.update(self)

class Megaman(Enemy):
	""" The megaman enemy can reflect the players bullets. """
	def __init__(self):
		Enemy.__init__(self, 'megaman.png')

	def bullet_collision(self, bullet):
		if random.random() < 0.50:
			bullet.speedx = -bullet.speedx
			bullet.speedy = -bullet.speedy
			bullet.x += bullet.speedx
			bullet.y += bullet.speedy
		else:
			Enemy.bullet_collision(self, bullet)


####################################


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

	global player
	player = Player()
	hearts = []
	for i in range(player.health):
		heart = NonMoveableSprite('heart.png')
		hearts.append(heart)
		heart.x = i * 70 + 5
		heart.y = 0

	scoreboard = Scoreboard()
	scoreSprite = pygame.sprite.Group(scoreboard)
	pygame.mixer.music.load('music.mp3')
	# pygame.mixer.music.play(0, 120)

	global generate, level_timer
	leftdown, rightdown = False, False	
	i = 0
	while True:
		i += 1
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_SPACE or event.key == K_w or event.key == K_UP:
					player.jump()
				elif event.key == K_LEFT or event.key == K_a:
					leftdown = True
					player.speedx = -Player.movespeed
				elif event.key == K_RIGHT or event.key == K_d:
					rightdown = True
					player.speedx = Player.movespeed
				elif event.key == K_z and player.can_shoot():
					player.shoot()	
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and player.can_shoot():
					player.shoot_mouse(event.pos)			
			elif event.type == KEYUP:
				if event.key == K_LEFT or event.key == K_a:
					leftdown = False
				elif event.key == K_RIGHT or event.key == K_d:
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

		# Update and paint sprites
		for obj in sprites:
			screen.blit(background_image, obj.rect, obj.rect)
			obj.renderer.update()
			obj.renderer.draw(screen)
			if obj.removing:
				sprites.remove(obj)
				screen.blit(background_image, obj.rect, obj.rect)
		pygame.display.flip()

		# Update health
		if player.health < len(hearts) and hearts != []:
			heart = hearts[len(hearts) - 1]
			heart.remove()
			hearts.remove(heart)


		if len(hearts) == 0:
			player.speedy = -1.5
			player.allow_gravity = False
			player.is_alive = False
			font = pygame.font.Font(None,100)
			text = font.render("YOU DIED!", 1, (255,0,00))
			textpos = text.get_rect()
			textpos.centerx = background_image.get_rect().centerx
			background_image.blit(text,textpos)
			screen.blit(background_image, (0, 0))

		global boss_timer
		if Player.score >= 200 and time.time() - level_timer > 50 and "bowser" not in bosses_spawned:
			bosses_spawned.append("bowser")
			background_image = pygame.image.load("data/level_2.jpg").convert()
			screen.blit(background_image, (0, 0))
			level_timer = time.time()
			boss_timer = time.time()
			Boss()
			pygame.mixer.music.play(0, 130)

		if Boss not in [type(monster) for monster in monsters]:
			generate = True

		if generate and time.time() - boss_timer > 30:
			generateMonsters()


def generateMonsters():
	if random.randint(1, 50) == 1: 
		chance = random.randint(1,4)
		if chance == 1:
			enemy = Fish()
		elif chance == 2:
			enemy = Phantom()
		elif chance == 3:
			enemy = Enemy('charizard.png')
		elif chance == 4:
			enemy = Megaman()
		enemy.speedx *= .65 + random.random()

		if random.random() < 0.50:
			enemy.speedx = -enemy.speedx
			enemy.x = -enemy.image.get_width()
	
main()