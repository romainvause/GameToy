#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

import pygame
import sys

import lib.parallax as parallax

from tir import *
from alien import *



class Game:
	def __init__(self, fen):
		# Système
		self.fen = fen
		self.on_pause = False
		self.on_pause_blocked = False
		
		# Scroller
		self.vitesse_scroll = 10
		self.bg_image = parallax.ParallaxSurface((320, 240), pygame.RLEACCEL)
		self.bg_image.add("images/bg.jpg", 10)
		
		# Score
		self.has_killed = False
		self.score = 0
		
		# Timer
		self.pop_alien = 1000
		self.old = 0
		
		# Groupes
		self.alien_list = pygame.sprite.Group()
		self.alien_vie_list = pygame.sprite.Group()
		self.vaisseau_list = pygame.sprite.Group()
		self.vaisseau_vie_list = pygame.sprite.Group()
		self.tir_list = pygame.sprite.Group()
		self.tir_list_alien = pygame.sprite.Group()
		self.bonus_list = pygame.sprite.Group()
		
	
	def draw(self):
		self.fen.fill((0,0,0))
		
		self.bg_image.draw(self.fen)
		
		self.vaisseau_list.draw(self.fen)
		self.vaisseau_vie_list.draw(self.fen)
		self.alien_list.draw(self.fen)
		self.alien_vie_list.draw(self.fen)
		self.tir_list.draw(self.fen)
		self.tir_list_alien.draw(self.fen)
		self.bonus_list.draw(self.fen)
	
	def update(self):	
		self.vaisseau_list.update()
		self.vaisseau_vie_list.update()
		self.alien_list.update()
		self.alien_vie_list.update()
		
		self.tir_list.update()
		self.tir_list_alien.update()
		self.check_pos_tir(self.tir_list)
		self.check_pos_tir(self.tir_list_alien)
		
		self.bonus_list.update()
		
		self.bg_image.scroll(self.vitesse_scroll, "vertical")

	
	def add_player(self, player):
		self.vaisseau_list.add(player)
		
	def check_pos_tir(self, tirs):
		for tir in tirs:
			if tir.rect.y < 0 or tir.rect.y > 240:
				tirs.remove(tir)
	
	def pause(self):
		if self.on_pause:
			for entity in self.alien_list:
				entity.pause = False
			self.on_pause = False
		else:
			for entity in self.alien_list:
				entity.pause = True
			self.on_pause = True


