#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fonctions.py
#  
#  Copyright 2014 Romain <Romain@ROMAIN-PC>

import os, pygame

def load_png(name, color_key=None):
	fullname = os.path.join("images", name)
	try:
		image = pygame.image.load(fullname)
		image = image.convert()
			
		if color_key != None:
			image.set_colorkey(color_key)
			
	except pygame.error, message:
		print("Impossible de charger l'image : {}" .format(fullname))
		raise SystemExit, message
	
	return image, image.get_rect()

def render_score(score):
	"""Transformation du score (136 -> 000136)"""
	if len(str(score)) > 0 and len(str(score)) < 7:
		return "0"*(6-len(str(score))) + str(score)
	else:
		return "999999"

if __name__ == "__main__":
	print(render_score(1))
	print(render_score(11))
	print(render_score(111))
	print(render_score(1111))
	print(render_score(11111))
	print(render_score(111111))
	print(render_score(1111111))

