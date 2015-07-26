#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  vie.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

import pygame

class Vie(pygame.sprite.Sprite):
	def __init__(self, width_max, height, decal, fixe=False):
		super(Vie, self).__init__()
		
		self.state = fixe
		self.x = 0
		self.y = 0
		
		self.width_max = width_max
		self.width = self.width_max
		self.height = height
		
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill((255,0,0))
		
		self.rect = self.image.get_rect()
		
		self.decal_x = decal[0]
		self.decal_y = decal[1]
	
	def update(self):
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
