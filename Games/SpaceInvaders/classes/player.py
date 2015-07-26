#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  player.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

import pygame
from pygame.locals import *

from mobile import *
from tir import *
from vie import *

class Player(Mobile):
	def __init__(self, image, game):
		super(Player, self).__init__(image)
		
		# Id
		self.id = "player"
		self.game = game
		self.vie_max = 140
		self.vie = self.vie_max
		self.blocked = False
		
		# Position
		self.rect.y = 210
		self.rect.x = 100
		
		# Images
		self.img_vie = None
		
		# Attaque
		self.dmg = 20
		
		# Mouvement
		self.speed = 7
		
		self.can_shoot = True
	
	def go_left(self):
		if not self.blocked:
			self.change_x = -self.speed
	def go_right(self):
		if not self.blocked:
			self.change_x = self.speed
	def stop_x(self):
		self.change_x = 0
	
	def shoot(self, image):
		if not self.blocked:
			pos = (self.rect.x + self.rect.width / 2 - 1, self.rect.y)
			tir = Tir(image, pos, self.id, dmg=20)
			self.game.tir_list.add(tir)
		
	def update(self):
		self.move(self.change_x, self.change_y)
		self.check_collision()
		
		# Test de mort
		if self.vie <= 0:
			self.game.vitesse_scroll = 0
			self.stop_x()
			if not self.game.on_pause_blocked:
				self.game.pause()
			self.game.on_pause_blocked = True
			
			self.anim_death()
		
	def check_collision(self):
		# Collisions avec tir ennemis
		lst_entity = pygame.sprite.spritecollide(self, self.game.tir_list_alien, True)
		for entity in lst_entity:
			self.vie -= entity.dmg
			if self.vie >= 0:
				self.img_vie.width -= self.img_vie.width_max / (self.vie_max / entity.dmg)
			if self.vie <= 0:
				self.game.vaisseau_vie_list.empty()
		
		lst_entity = pygame.sprite.spritecollide(self, self.game.bonus_list, True)
		for entity in lst_entity:
			if entity.type_bonus == "bonus":
				self.vie += entity.dmg
				if self.vie + entity.dmg <= self.vie_max:
					self.img_vie.width += self.img_vie.width_max / (self.vie_max / entity.dmg)
				else:
					self.img_vie.width = self.img_vie.width_max
					self.vie = self.vie_max
				
			elif entity.type_bonus == "malus":
				self.vie -= entity.dmg
				self.img_vie.width -= self.img_vie.width_max / (self.vie_max / entity.dmg)
	
	def move(self, x, y):
		newpos = self.rect.move(x, y)
		newposlife = self.rect.move(x + self.img_vie.decal_x, y + self.img_vie.decal_y)
		
		self.rect = newpos
		self.img_vie.rect = newposlife
		
		if self.rect.x < 0:
			self.rect.x = 0
			self.img_vie.rect.x = 0
		
		if self.rect.x > 270:
			self.rect.x = 270
			self.img_vie.rect.x = 270
			
		
	def anim_death(self):
		act = pygame.time.get_ticks()
		
		if not self.blocked:
			# Définition des variables du timer
			self.on_anim_tremble = True
			self.on_anim_descente = False
			
			self.t_death = 1000
			self.to_death = act
			
			self.t_death2 = 1500
			self.to_death2 = act
			self.tf_death2 = 3000
			self.tfo_death2 = act
			
			self.t_left = 100
			self.to_left = act
			self.t_right = 100
			self.to_right = act + 50
			self.t_down = 50
			self.to_down = act
		
		# Timer général de l'animation de tremblement
		if act > self.t_death + self.to_death:
			self.on_anim_tremble = False
		
		# Timer du tremblement
		if self.on_anim_tremble:
			if act > self.t_left + self.to_left: # Gauche
				self.move(-2, 0)
				self.to_left = act
			
			if act > self.t_right + self.to_right: # Droite
				self.move(2, 0)
				self.to_right = act
		
		# Timer général de l'animation de descente
		if act > self.t_death2 + self.to_death2 and self.on_anim_descente != -1:
			self.on_anim_descente = True
			
		# Timer de la descente
		if self.on_anim_descente == True:
			if act > self.t_down + self.to_down:
				self.move(0, 2)
				self.to_down = act
		
		# Timer fin de l'animation de descente
		if act > self.tf_death2 + self.tfo_death2:
			self.on_anim_descente = -1
			
		
		self.blocked = True
	
if __name__ == "__main__":
	p = Player()
	p.update()
