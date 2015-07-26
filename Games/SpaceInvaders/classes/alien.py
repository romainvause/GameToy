#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  player.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

import pygame

from mobile import *
from tir import *
from vie import *

from random import randrange

class Alien(Mobile):
	def __init__(self, image, game, direction="right"):
		super(Alien, self).__init__(image)
		
		# Id
		self.id = "alien"
		self.id_code = randrange(10000, 100000)
		self.game = game
		self.vie_max = 100
		self.vie = self.vie_max
		self.dmg = 20
		
		# Images
		self.img_good = None
		self.img_middle = None
		self.img_bad = None
		self.img_vie = None
		
		# Patern
		self.new = True
		self.first_shock = True
		self.first_line = True
		
		# Position
		self.rect.y = 10
		
		# Mouvement
		self.speed = 2
		self.pause = False
		self.direction_x = ""
		self.direction_y = ""
		
		# Timer tir
		self.timer_shoot = 1000
		self.timer_shoot_old = pygame.time.get_ticks()
		
		chance = randrange(0, 2)
		if chance:
			self.go_down()
		else:
			self.go_up()
		
		chance = randrange(0, 2)
		if chance:
			self.go_left()
		else:
			self.go_right()

	def go_left(self):
		self.change_x = -self.speed
		self.direction_x = "left"
	def go_right(self):
		self.change_x = self.speed
		self.direction_x = "right"
	def go_down(self):
		self.change_y = self.speed
		self.direction_y = "down"
	def go_up(self):
		self.change_y = -self.speed
		self.direction_y = "up"
	def stop_x(self):
		self.change_x = 0
	def stop_y(self):
		self.change_y = 0

	def update(self):
		if (self.rect.x + 22 > 320):
			self.go_left()
		if (self.rect.x < 0):
			self.go_right()
		if (self.rect.y + 16 > 170):
			self.go_up()
		if (self.rect.y < 0):
			self.go_down()
		
		# Test de mort
		if (self.vie <= 0):
			self.game.alien_list.remove(self)
			self.game.alien_vie_list.remove(self.img_vie)
			self.game.has_killed = True
		
		# Déplacements
		if not self.pause:
			self.move(self.change_x, self.change_y)
		
		# Tests des collisions
		self.check_collision()
			
		# Determination de shoot
		act = pygame.time.get_ticks()
		if act > self.timer_shoot + self.timer_shoot_old:
			self.shoot()
			self.timer_shoot_old = act
	
	def move(self, x, y):
		newpos = self.rect.move(x, y)
		newposlife = self.rect.move(x + self.img_vie.decal_x, y + self.img_vie.decal_y)
		self.rect = newpos
		self.img_vie.rect = newposlife
	
	def check_collision(self):
		# Collisions entre aliens et aliens
		lst_entity = pygame.sprite.spritecollide(self, self.game.alien_list, False)
		for entity in lst_entity:
			if self.id_code != entity.id_code:
				if self.direction_x == "left":
					self.go_right()
				elif self.direction_x == "right":
					self.go_left()
				if self.direction_y == "up":
					self.go_down()
				elif self.direction_y == "down":
					self.go_up()
		
		# Collisions entre aliens et tir
		lst_entity = pygame.sprite.spritecollide(self, self.game.tir_list, True)
		for entity in lst_entity:
			# Dessin de la barre de vie
			self.vie -= self.game.player.dmg
			if self.vie > 0:
				self.img_vie.width -= self.img_vie.width_max / (self.vie_max / self.game.player.dmg)
			
			# Définition de la couleur de l'alien
			if self.vie >= 70 and self.vie <= 100:
				self.load_image(self.img_good)
			elif self.vie >= 40 and self.vie < 70:
				self.load_image(self.img_middle)
			elif self.vie >= 10 and self.vie < 40:
				self.load_image(self.img_bad)
	
	def shoot(self):
		if not self.pause:
			pos = (self.rect.x + self.rect.width / 2 - 1, self.rect.y)
			tir = Tir(self.shoot_image, pos, self.id, "bottom", dmg=self.dmg)
			self.game.tir_list_alien.add(tir)
	

