#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bonus.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

import pygame
from pygame.locals import *

from mobile import *

class Bonus(Mobile):
	def __init__(self, image, game, type_bonus):
		super(Bonus, self).__init__(image)
		
		# Id
		self.type_bonus = type_bonus
		
		self.dmg = 20
		
		# Mouvement
		self.speed = 2
		
		self.change_y = 3
		self.change_x = 0
	
	def update(self):
		newpos = self.rect.move(self.change_x, self.change_y)
		self.rect = newpos

