#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mobile.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

import pygame

class Mobile(pygame.sprite.Sprite):
	def __init__(self, image):
		super(Mobile, self).__init__()
		
		self.vitesse = 0
		
		self.image, self.rect = image
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		
		# Images
		self.img_vie = None
		
		# Positions
		self.rect.x = 0
		self.rect.y = 0
		
		# Déplacement
		self.change_x = 0
		self.change_y = 0
	
	
		
		
	def load_image(self, image):
		self.image = image[0]

	

