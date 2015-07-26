#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tir.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

from mobile import *

class Tir(Mobile):
	def __init__(self, image, rect, propritary, direction="top", dmg=20):
		super(Tir, self).__init__(image)
		
		# Id
		self.id = propritary
		self.dmg = dmg
		
		# Position
		self.rect.x = rect[0]
		self.rect.y = rect[1]
		
		# Mouvement
		self.speed = 10
		
		if direction == "top":
			self.change_y = -10
		elif direction == "bottom":
			self.change_y = 10
	
	def update(self):
		newpos = self.rect.move(self.change_x, self.change_y)
		self.rect = newpos
	
if __name__ == "__main__":
	p = Player()
	p.update()
