#!/usr/bin/env python3

import pygame as pg
import math
from util import blit_rotate, get_sprites_from_spritesheet
from colors import RED, GRAY, BLUE_GRAY
from explosion import Explosion

Target_BASE_SIZE = 8
TargetLockImage = pg.Surface((Target_BASE_SIZE,Target_BASE_SIZE))
TargetLockImage.fill(RED)

class Target(pg.sprite.Sprite):
	MAX_SIZE_SCALE = 2
	FREQUENCY = 8 

	def __init__(self, pos):
		pg.sprite.Sprite.__init__(self)
		self.image = TargetLockImage

		self.centerLocation = pos
		self.rect = self.image.get_rect()
		self.rect.center = self.centerLocation
 
	def update(self):
		# throb according to frequency.
		tks = pg.time.get_ticks()
		scaleFactor = 1 + self.MAX_SIZE_SCALE*abs(math.sin(self.FREQUENCY*tks/1000))
		w,h = TargetLockImage.get_size()
		sw,sh = int(scaleFactor*w), int(scaleFactor*h)
		self.image = pg.transform.scale(TargetLockImage,( sw, sh ))

		# reset the center position
		self.rect = self.image.get_rect()
		self.rect.center = self.centerLocation


class RocketPath(pg.sprite.Sprite):
	def __init__(self,launch_pos,destination_pos,screen_size):
		pg.sprite.Sprite.__init__(self)
		window_w,window_h = screen_size
		self.image = pg.Surface((window_w,window_h),pg.SRCALPHA)
		pg.draw.line(self.image, BLUE_GRAY, launch_pos, destination_pos, width=2)
		self.rect = pg.Rect(0,0,window_w,window_h)

class Rocket(pg.sprite.Sprite):
	ASSET_FILE = "./assets/missiles/missile_allred_cropped.png"
	REDUCTION_SCALE = 8
	PIVOTX = 213
	PIVOTY = 510
	VELOCITY = 24

	def __init__(self, launch_pos, destination_pos, game_obj):
		pg.sprite.Sprite.__init__(self)

		self.target_object = Target( destination_pos ) 
		self.path_object = RocketPath( launch_pos, destination_pos, game_obj.screen.get_size() )

		# link up to the sprite groups
		self.rockets_and_paths_sprites = game_obj.rockets_and_paths_sprites
		self.rockets_and_paths_sprites.add( self.target_object )
		self.rockets_and_paths_sprites.add( self.path_object )

		# don't add explosion yet. Add it when the rocket reaches its target.
		self.explosion_sprites = game_obj.explosion_sprites
		

		load_image = pg.image.load(self.ASSET_FILE).convert_alpha()
		w,h = load_image.get_size()
		sw,sh = w//self.REDUCTION_SCALE, h//self.REDUCTION_SCALE
		self.upright_rocket_img = pg.transform.scale(load_image,(sw,sh))

		self.src_pos = launch_pos
		self.des_pos = destination_pos

		# what is my rotation?
		dest_x,dest_y = self.des_pos
		source_x,source_y = self.src_pos

		# i hate the pg coordinate system. :-(
		dx = source_x-dest_x
		dy = source_y-dest_y
		if dx == 0:
			self.rotation = 0
		else:
			self.rotation = math.degrees( math.atan( dx / dy ) ) 

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

		self.image, self.rect = blit_rotate(self.upright_rocket_img, 
											self.src_pos,
											(self.scaled_pivot_x, self.scaled_pivot_y), 
											self.rotation
											)

	def update(self):
		self.distance_traveled += self.distance_per_tick
		if self.distance_traveled > self.max_distance:
			self.path_object.kill()
			self.target_object.kill()
			self.kill()

			# the rocket has reached the destination position. Set up the explosion
			explosion_cached_sprite_list = get_sprites_from_spritesheet('air_explosion') 
			explosion_object = Explosion( self.des_pos, explosion_cached_sprite_list, 1 )
			self.explosion_sprites.add(explosion_object)
		else:
			dx,dy = self.distance_traveled*self.sinrotation, self.distance_traveled*self.cosrotation
			current_pos = self.src_pos[0] - int(dx), self.src_pos[1] - int(dy)

			self.image, self.rect = blit_rotate(self.upright_rocket_img, 
												current_pos,
												(self.scaled_pivot_x, self.scaled_pivot_y), 
												self.rotation
												)
