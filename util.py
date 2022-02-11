#!/usr/bin/env python3

import pygame as pg

GlobalSpriteListDict = {}
GlobalSpriteListDict['air_explosion'] = {
	'filename': "./assets/explosions/peach_explosion.png",
	'sprite_size': (128,128),
	'sheet_grid':(5,8),
	'scale': 1.5,
	'sprite_images': []
}
GlobalSpriteListDict['ground_explosion'] = {
	'filename': "./assets/explosions/solunasoftware/Effect47.png",
	'sprite_size': (128,128),
	'sheet_grid':(4,4),
	'scale': 2,
	'sprite_images': []
}

def blit_rotate(image, pos, originPos, angle):
	# https://stackoverflow.com/questions/59909942/how-can-you-rotate-an-image-around-an-off-center-pivot-in-pygame
	image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
	offset_center_to_pivot = pg.math.Vector2(pos) - image_rect.center
	rotated_offset = offset_center_to_pivot.rotate(-angle)
	rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
	rotated_image = pg.transform.rotate(image, angle)
	rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
	return rotated_image, rotated_image_rect
  

def get_sprites_from_spritesheet(sprite_key):
	global GlobalSpriteListDict

	filename = GlobalSpriteListDict[sprite_key]['filename']
	sprite_size_wh = GlobalSpriteListDict[sprite_key]['sprite_size']
	sheet_grid_wh = GlobalSpriteListDict[sprite_key]['sheet_grid']
	scale = GlobalSpriteListDict[sprite_key]['scale']

	if GlobalSpriteListDict[sprite_key]['sprite_images'] == []:
		print(f"Loading sprites from {filename}.")
		spritesheet = pg.image.load(filename).convert()
		rows,cols = sheet_grid_wh
		sprite_w, sprite_h = sprite_size_wh
		sprites = []
		for row in range(rows):
			for col in range(cols):
				offset_x, offset_y = col*sprite_w, row*sprite_h
				#print(f"x = {offset_x} y = {offset_y}")
				sprite = pg.Surface(sprite_size_wh)
				sprite.set_colorkey((0,0,0))
				sprite.blit(spritesheet,(0,0),(offset_x,offset_y,sprite_w, sprite_h))

				sprite = pg.transform.scale( sprite, (int(sprite_w*scale), int(sprite_h*scale)))
				sprites.append(sprite)
		GlobalSpriteListDict[sprite_key]['sprite_images'] = sprites

	return GlobalSpriteListDict[sprite_key]['sprite_images']

def gradientRect( window, top_color, bottom_color, target_rect ):
	""" Draw a vertical-gradient filled rectangle covering <target_rect> """
	#https://stackoverflow.com/questions/62336555/how-to-add-color-gradient-to-rectangle-in-pygame
	color_rect = pg.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
	pg.draw.line( color_rect, top_color,  ( 0,0 ), ( 1,0 ) )            # left color line
	pg.draw.line( color_rect, bottom_color, ( 0,1 ), ( 1,1 ) )            # right color line
	color_rect = pg.transform.smoothscale( color_rect, ( target_rect.width, target_rect.height ) )  # stretch!
	window.blit( color_rect, target_rect ) 