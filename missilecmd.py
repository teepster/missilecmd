#!/usr/bin/env python3

from glob import escape
import pygame as pg
import random
import sys

from colors import BLACK, DARK_RED, DEEP_BLUE, WHITE, BLUE_GRAY, GRAY
from util import gradientRect
import rotating_turret as RT
#from rotating_turret import load_launcher_assets, MissileTurret, get_base_positions
from rocket import Rocket
from enemy import generateRandomEnemyPath, Enemy

SCREEN_W = 1920
SCREEN_H = 1200

FPS = 60

ENEMY_SPAWN_EVENT = pg.USEREVENT + 0
ENEMY_SPWAN_FREQ = 800 # milliseconds
# what is the likelihood that we will create an enemy when the event occurs
ENEMY_SPAWN_LIKELIHOOD = 0.65 

class Game:
	bg_color = (0,0,0)

	def __init__(self):
		self.screen = pg.display.set_mode((SCREEN_W,SCREEN_H))
		pg.display.set_caption('Missile Command')

		self.setup_objects()
		
		self.done = False
		self.clock = pg.time.Clock()
		
		self.player_score = 0
		self.enemy_score = 0

		# spawn enemies
		pg.time.set_timer(ENEMY_SPAWN_EVENT,ENEMY_SPWAN_FREQ)

	def init_launch_site(self):
		# scaled surfaces
		# turret,turret_pivot,front_arm,back_arm = get_launcher_surfaces()
		# base_positions = rotating_turret.get_base_positions(SCREEN_W, SCREEN_H)
		# left_B,center_B,right_B = rotating_turret.setup_launcher_assets(base_positions)
		# self.missile_launcher = MissileTurret(turret,
		# 										turret_pivot,
		# 										front_arm,
		# 										back_arm,
		# 										base_positions,
		# 										2)
		base_dict = RT.get_base_positions(SCREEN_W,SCREEN_H)
		self.L, self.C, self.R = RT.setup_launcher_assets(base_dict)
		self.active_launch_site = self.C	


	def setup_objects(self):
		self.font = pg.font.Font("./assets/font/BebasNeue-Regular.ttf",72)

		# set up launch site
		self.init_launch_site()

		# this includes
		# 	- Rockets
		# 	- RocketPaths
		#	- RocketTargets
		#	- EnemiesPaths
		#	- EnemiesExplosions
		self.rockets_and_paths_sprites = pg.sprite.Group()
		# this is just the enemy missiles
		self.enemies_sprites = pg.sprite.Group()
		# this is just the explosions from the rockets
		self.explosion_sprites = pg.sprite.Group()

	def run(self):
		while not self.done:
			self.event_loop()
			self.update()
			self.draw()

			pg.display.flip()
			self.clock.tick(FPS)

	def draw(self):
		self.screen.fill(self.bg_color)

		ground_rect = pg.Rect(0,SCREEN_H-18,SCREEN_W,18)
		# Update the window bg
		gradientRect( self.screen, BLACK, DEEP_BLUE, self.screen.get_rect() )
		gradientRect( self.screen, GRAY, DARK_RED, ground_rect )

		self.draw_score()	
		self.draw_sprites()
		self.active_launch_site.draw(self.screen)

	def draw_score(self):
		pscore = self.font.render(f"Player: {self.player_score}",True,BLUE_GRAY)
		escore = self.font.render(f"Enemy: {self.enemy_score}",True,BLUE_GRAY)
		self.screen.blits(blit_sequence=[(pscore,(200,200)),(escore,(1500,200))])

	def draw_sprites(self):
		self.rockets_and_paths_sprites.draw(self.screen)
		self.enemies_sprites.draw(self.screen)
		self.explosion_sprites.draw(self.screen)
		# self.launcher_sprite_group.draw(self.screen)

	def event_loop(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.done = True
			elif event.type == pg.MOUSEMOTION:
				self.active_launch_site.mouse_pos = pg.mouse.get_pos()
			## SWITCH LAUNCH SITE
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_1:
					print("Change to launch site 1")
					self.active_launch_site = self.L
				if event.key == pg.K_2:
					print("Change to launch site 2")
					self.active_launch_site = self.C
				if event.key == pg.K_3:
					print("Change to launch site 3")
					self.active_launch_site = self.R
				if event.key == pg.K_ESCAPE:
					self.done = True
			## LAUNCH MISSILE !!!
			elif event.type == pg.MOUSEBUTTONDOWN:
				dest = pg.mouse.get_pos()
				src = self.active_launch_site.get_missile_launch_point()
				# create a new rocket and add it to the sprite group.
				rocket = Rocket(src, dest, self)
				self.rockets_and_paths_sprites.add(rocket)
			## NEW ENEMY IS SPAWNED
			elif event.type == ENEMY_SPAWN_EVENT:
				if random.random() < ENEMY_SPAWN_LIKELIHOOD:
					# we've got an enemy
					s,d = generateRandomEnemyPath((SCREEN_W,SCREEN_H))
					# print(f"Spawn!!! {s} --> {d}")
					newEnemy = Enemy(s, d, self)
					self.enemies_sprites.add(newEnemy)
				else:
					pass
					# print("Failure to spawn enemy this time around.")
			else:
				pass

	def update(self):
		# self.launcher_sprite_group.update()
		self.active_launch_site.update()
		self.explosion_sprites.update()
		self.rockets_and_paths_sprites.update()
		self.enemies_sprites.update()
		# see

if __name__ == '__main__':
	pg.init()
	game = Game()
	game.run()
	pg.quit()