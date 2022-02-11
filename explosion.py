#!/usr/bin/env python3

import pygame as pg

GROUND_EXPLOSION_Y_NUDGE = 8

class Explosion(pg.sprite.Sprite):
	def __init__(self, pos, spritelist, animation_delay, placement="center"):
		pg.sprite.Sprite.__init__(self)

		self.images = spritelist
		self.imageIndex = 0
		self.maxImageIndex = len(spritelist)
		self.image = self.images[self.imageIndex]
		self.mask = pg.mask.from_surface(self.image)
		self.animation_delay = animation_delay
		self.ticks = 0

		self.rect = self.image.get_rect()
		# there are two kinds of explosions: mid-air and on-the-ground.
		# the mid-air explosions are placed by the center coordinate
		# the on ground explosions are placed with respect to the midbottom coordinate
		setattr(self.rect,placement,pos)
		if placement=="midbottom":
			self.rect.y = self.rect.y + GROUND_EXPLOSION_Y_NUDGE

	def update(self):
		# count ticks until reach animation_delay before advance, once that has reached, update the sprite image
		# otherwise skip
		self.ticks += 1
		
		# should we do anything now?
		if self.ticks >= self.animation_delay:
			# advance frame
			self.imageIndex = self.imageIndex + 1
			if self.imageIndex >= self.maxImageIndex:
				self.imageIndex = 0
				self.kill()
			else:
				self.image = self.images[self.imageIndex]
				self.mask = pg.mask.from_surface(self.image)
			self.ticks = 0
		else:
			pass # skip updating.
