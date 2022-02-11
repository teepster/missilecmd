#!/usr/bin/env python3

import random
import pygame as pg
from pygame.math import Vector2
from util import blit_rotate

# locations of the launch pad
LaunchSite_Division = 8
One_Minus_Division = LaunchSite_Division - 1
LaunchSite_Height_Offset = 10

LAUNCHER_IMAGE_SCALE = 0.1

L_LAUNCHER_FRONT_PIECE = './assets/launcher/Left/front_arm.png'
L_LAUNCHER_TURRET_PIECE = './assets/launcher/Left/turret.png'
L_LAUNCHER_BACK_PIECE = './assets/launcher/Left/back_arm.png'
L_LAUNCHER_TURRET_PIVOT = (424, 703)

R_LAUNCHER_FRONT_PIECE = './assets/launcher/Right/front_arm.png'
R_LAUNCHER_TURRET_PIECE = './assets/launcher/Right/turret.png'
R_LAUNCHER_BACK_PIECE = './assets/launcher/Right/back_arm.png'
R_LAUNCHER_TURRET_PIVOT = (489, 703)

def get_base_positions( screen_w, screen_h ):
	return {
		1: (screen_w//LaunchSite_Division, screen_h - LaunchSite_Height_Offset),	
		2: (screen_w//2, screen_h - LaunchSite_Height_Offset),
		3: (One_Minus_Division*screen_w//LaunchSite_Division, screen_h - LaunchSite_Height_Offset)
	}

class ImageGroupData:
	def __init__(self, turret,
					turret_pivot,
					front_arm,
					back_arm):
		self.turret = pg.image.load(turret).convert_alpha()
		self.turret_pivot = turret_pivot
		self.front_arm = pg.image.load(front_arm).convert_alpha()
		self.back_arm = pg.image.load(back_arm).convert_alpha()

	def set_scale(self,scale):
		self.front_arm = pg.transform.rotozoom(self.front_arm,0,scale)
		self.turret = pg.transform.rotozoom(self.turret,0,scale)
		self.turret_pivot = tuple([ int(i*scale) for i in self.turret_pivot])
		self.back_arm = pg.transform.rotozoom(self.back_arm,0,scale)


class BaseEngine:
	def __init__(self, base_position:pg.Vector2):
		self.base_pos = base_position

		# self.image_group = None
		self.img_w, self.img_h = None, None
		self.turret_pivot = None
		self.pivot_offset = None

	def set_image_group(self, image_group):
		# self.image_group = image_group
		self.img_w, self.img_h = image_group.turret.get_size()
		self.pivot_offset = pg.Vector2(	(self.img_w//2 - image_group.turret_pivot[0]),
										(self.img_h - image_group.turret_pivot[1])
										)
		self.turret_pivot = image_group.turret_pivot
		self.pivot_screen_space = self.base_pos - self.pivot_offset

		self.orig_image = image_group.turret
		self.back_arm_img = image_group.back_arm
		self.back_arm_rect = self.back_arm_img.get_rect(midbottom=self.base_pos)
		self.front_arm_img = image_group.front_arm
		self.front_arm_rect = self.front_arm_img.get_rect(midbottom=self.base_pos)

	def update_with_target(self, target):
		# update the two static features

		# # create a vector from the world space pos of the rotation axis to the mouse location
		# now calculate the vector to the mouse_pos from new_pivot_screen_space
		to_target = pg.math.Vector2(target) - self.pivot_screen_space
		straight_up = pg.math.Vector2(0, -1)
		self.angle = straight_up.angle_to(to_target)

		self.turret_img, self.turret_rect = blit_rotate(self.orig_image, self.pivot_screen_space, self.turret_pivot, -self.angle)

LeftGroup = None
RightGroup = None

LeftBase = None
CenterBase = None
RightBase = None

BaseSelector = None


def setup_launcher_assets(base_positions):
	global LeftGroup,RightGroup
	global LeftBase,CenterBase,RightBase
	global BaseSelector

	LeftGroup = ImageGroupData(
		L_LAUNCHER_TURRET_PIECE,
		L_LAUNCHER_TURRET_PIVOT,
		L_LAUNCHER_FRONT_PIECE,
		L_LAUNCHER_BACK_PIECE
		)
	LeftGroup.set_scale(LAUNCHER_IMAGE_SCALE)

	RightGroup = ImageGroupData(
		R_LAUNCHER_TURRET_PIECE,
		R_LAUNCHER_TURRET_PIVOT,
		R_LAUNCHER_FRONT_PIECE,
		R_LAUNCHER_BACK_PIECE
		)
	RightGroup.set_scale(LAUNCHER_IMAGE_SCALE)

	LeftBaseEngine = BaseEngine(pg.Vector2(base_positions[1]))
	CenterBaseEngine = BaseEngine(pg.Vector2(base_positions[2]))
	RightBaseEngine = BaseEngine(pg.Vector2(base_positions[3]))

	LeftBaseEngine.set_image_group( LeftGroup )
	CenterBaseEngine.set_image_group( LeftGroup )
	RightBaseEngine.set_image_group( RightGroup )

	LeftBase = Turret(LeftBaseEngine)
	CenterBase = Turret(CenterBaseEngine)
	RightBase = Turret(RightBaseEngine)

	return LeftBase,CenterBase,RightBase

class Turret:
	def __init__(self,engine):
		self.engine = engine
		self.mouse_pos = pg.Vector2(960,0)

	def get_missile_launch_point(self):
		return self.engine.base_pos - self.engine.pivot_offset

	def update(self):
		self.engine.update_with_target(self.mouse_pos)

	def draw(self,screen):
		# draw the turret sandwiched between the two static arms
		screen.blits( 
						[
							(self.engine.back_arm_img, self.engine.back_arm_rect),
							(self.engine.turret_img, self.engine.turret_rect),
							(self.engine.front_arm_img, self.engine.front_arm_rect),		
						]
			)


# class MissileTurret:
# 	# NOT A SPRITE OBJECT!!!!
# 	# I am implementing my own update() and draw(screen) functions
# 	def __init__(self,turret,
# 					turret_pivot,
# 					left_arm,
# 					right_arm,
# 					base_positions,
# 					base_pos_number):

# 		self.turret_img = turret
# 		self.img_w, self.img_h = self.turret_img.get_size()
# 		# rotate_pivot_coords is in image space
# 		self.pivot_coords = turret_pivot
# 		self.base_positions_dict = base_positions
# 		self.base_pos = pg.Vector2(self.base_positions_dict[base_pos_number])
# 		self.current_base_number = base_pos_number

# 		# offset from base_pos (which is midbottom, so the x offset is from the middle of the image)
# 		self.pivot_offset = pg.Vector2(	(self.img_w//2 - self.pivot_coords[0]),
# 										(self.img_h - self.pivot_coords[1])
# 										)

		

# 		# A reference to the original image to preserve the quality.
# 		self.orig_image = self.turret_img
# 		self.turret_rect = self.turret_img.get_rect(midbottom=self.base_pos)
	
# 		# angle to tilt the sprite by
# 		self.angle = 0

# 		# this will get it to point upwards initially
# 		self.mouse_target = self.turret_rect.centerx, self.turret_rect.centery - 10 

# 		# well need this when drawing the two static features
# 		self.back_arm_img = right_arm
# 		self.back_arm_rect = self.back_arm_img.get_rect(midbottom=self.base_pos)
# 		self.front_arm_img = left_arm
# 		self.front_arm_rect = self.front_arm_img.get_rect(midbottom=self.base_pos)

# 	def update(self):		
# 		# update the two static features
# 		self.back_arm_rect.midbottom = self.base_pos
# 		self.front_arm_rect.midbottom = self.base_pos

# 		# update the rotating turret
# 		new_pivot_screen_space = self.base_pos - self.pivot_offset

# 		# # create a vector from the world space pos of the rotation axis to the mouse location
# 		# now calculate the vector to the mouse_pos from new_pivot_screen_space
# 		to_target = pg.math.Vector2(self.mouse_target) - new_pivot_screen_space
# 		straight_up = pg.math.Vector2(0, -1)
# 		self.angle = straight_up.angle_to(to_target)

# 		self.turret_img, self.turret_rect = blit_rotate(self.orig_image, new_pivot_screen_space, self.pivot_coords, -self.angle)

# 	def draw(self,screen):
# 		# draw the turret sandwiched between the two static arms
# 		screen.blits( 
# 						[
# 							(self.back_arm_img, self.back_arm_rect),
# 							(self.turret_img, self.turret_rect),
# 							(self.front_arm_img, self.front_arm_rect),		
# 						]
# 			)

# 	def change_position(self,position_number):
# 		self.current_base_number = position_number
# 		if self.current_base_number == 1 or self.current_base_number == 2:
# 			# setup for "Left" missile launcher images
# 			pass
# 		else:
# 			# setup for "Right" missile launcher images
# 			pass

# 		self.base_pos = pg.Vector2(self.base_positions_dict[position_number])
