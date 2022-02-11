#!/usr/bin/env python3

import pygame as pg
import random
import math
from colors import DARK_RED
from util import blit_rotate, get_sprites_from_spritesheet
from explosion import Explosion

def generateRandomEnemyPath(screen_dim):
	""" Figure out where along the top the enemy will appear,
		Figure out what their bottom destination is
		Figure out the speed.
	"""
	W,H = screen_dim
	TOP_EDGE = 4
	X_RANGE = 20, W-20
	source_pos = random.randint(X_RANGE[0],X_RANGE[1]), TOP_EDGE
	dest_pos = random.randint(X_RANGE[0],X_RANGE[1]), H
	return source_pos, dest_pos
	# where will the enemy appear?

class EnemyPath(pg.sprite.Sprite):
	def __init__(self,path):
		pg.sprite.Sprite.__init__(self)
		self.src, self.dest = path
		x,y,w,h = min(self.src[0],self.dest[0]), \
						0, \
						abs(self.src[0]-self.dest[0]), \
						self.dest[1]-self.src[1]

		self.image = pg.Surface((w,h),pg.SRCALPHA)
		if self.src[0] < self.dest[0]:
			pg.draw.line(self.image, DARK_RED, (0,0), (w,h), width=2)
		else:
			pg.draw.line(self.image, DARK_RED, (w,0), (0,h), width=2)

		self.rect = self.image.get_rect()
		self.rect.topleft = x,y

		
class Enemy(pg.sprite.Sprite):
	ASSET_FILE = "./assets/missiles/warship.png"
	REDUCTION_SCALE = 3
	PIVOTX = 52
	PIVOTY = 0
	VELOCITY = 14

	def __init__(self, launch_pos, destination_pos,game_object):
		pg.sprite.Sprite.__init__(self)

		self.game = game_object
	
		# get the path object
		self.path_object = EnemyPath( (launch_pos, destination_pos) )
		self.game.rockets_and_paths_sprites.add( self.path_object )
		
		# explosion object. Beware, since the explosion starts at y = image_height,
		# we have to offset it by half the image to get the explosion to appear where
		# the enemy ship lands.
		explosion_cached_sprite_list = get_sprites_from_spritesheet('ground_explosion') 
		self.explosion_object = Explosion( destination_pos, 
											explosion_cached_sprite_list,
											3,
											placement="midbottom" )

		load_image = pg.image.load(self.ASSET_FILE).convert_alpha()
		w,h = load_image.get_size()
		sw,sh = w//self.REDUCTION_SCALE, h//self.REDUCTION_SCALE
		self.upright_enemy_img = pg.transform.scale(load_image,(sw,sh))

		self.src_pos = launch_pos
		self.des_pos = destination_pos

		# what is my rotation?
		dest_x,dest_y = self.des_pos
		source_x,source_y = self.src_pos

		# i hate the pg coordinate system. :-(
		dx = source_x - dest_x
		dy = dest_y - source_y
		if dx == 0:
			self.rotation = 180
		else:
			self.rotation = 180 - math.degrees( math.atan( dx / dy ) ) 

		# trajectory precalculations
		# the following values are constant because rotation is constant
		self.scaled_pivot_x, self.scaled_pivot_y = self.PIVOTX//self.REDUCTION_SCALE, self.PIVOTY//self.REDUCTION_SCALE
		self.sinrotation = math.sin(math.radians(self.rotation))
		self.cosrotation = math.cos(math.radians(self.rotation))
		self.distance_per_tick = math.sqrt(self.VELOCITY*self.sinrotation * self.VELOCITY*self.sinrotation +\
											 self.VELOCITY*self.cosrotation * self.VELOCITY*self.cosrotation
											)
		self.max_distance = math.sqrt( dx*dx + dy*dy )
		
		self.distance_traveled = 0.0

		self.image, self.rect = blit_rotate(self.upright_enemy_img, 
											self.src_pos,
											(self.scaled_pivot_x, self.scaled_pivot_y), 
											self.rotation
											)
		self.mask = pg.mask.from_surface(self.image)

		# different sound when hitting the ground than other explosions
		self.ground_explosion_sound = pg.mixer.Sound("./assets/sounds/explode.wav")
		self.air_explosion_sound = pg.mixer.Sound("./assets/sounds/rock_breaking.wav")
	
	def update(self):
		# have you been hit?
		collision_list = pg.sprite.spritecollide(self, self.game.explosion_sprites, False, pg.sprite.collide_mask)
		if collision_list:
			print(f"Enemy Hit!!!")
			self.path_object.kill()
			self.kill()
			pg.mixer.Sound.play(self.air_explosion_sound)
			self.game.player_score += 1
		else:
			
			self.distance_traveled += self.distance_per_tick
			if self.distance_traveled > self.max_distance:
				print("City Hit!!!")		
				
				self.path_object.kill()
				self.kill()
				
				pg.mixer.Sound.play(self.ground_explosion_sound)
				self.game.enemy_score += 1
				# this needs to be done so that the explosion can start to render and update
				self.game.rockets_and_paths_sprites.add(self.explosion_object)
			else:
				dx,dy = self.distance_traveled*self.sinrotation, self.distance_traveled*self.cosrotation
				current_pos = self.src_pos[0] - int(dx), self.src_pos[1] - int(dy)

				self.image, self.rect = blit_rotate(self.upright_enemy_img, 
													current_pos,
													(self.scaled_pivot_x, self.scaled_pivot_y), 
													self.rotation
													)
				self.mask = pg.mask.from_surface(self.image)