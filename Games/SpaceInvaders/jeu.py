#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  jeu.py
#  
#  Copyright 2014 Romain <Romain@ROMAIN-PC>

# Imports systèmes
import pygame
from pygame.locals import *
import sys
import RPi.GPIO as GPIO

# Imports locaux
from fonctions import *

sys.path.append("classes")
from game import *
from mobile import *
from player import *
from alien import *
from vie import *
from bonus import *

from random import randrange

class Jeu(object):
	"""Classe de jeu"""
	def __init__(self, fen):
		print("Game")
		# Variable de programme principale
		self.fen = fen
		
		# Clock
		self.clock = pygame.time.Clock()
		
		# GPIO
		self.inputs = {
			"A": [17, 0],
			"B": [18, 0],
			
			"START" : [27, 0],
			"SELECT": [22, 0],
			
			"BAS"   : [23, 0],
			"HAUT"  : [24, 0],
			"GAUCHE": [25, 0],
			"DROITE": [21, 0]
		}
		
		for name in self.inputs:
			GPIO.setup(self.inputs[name][0], GPIO.IN, GPIO.PUD_UP)
			
		# Chargement
		self.on_load_level(5)
		self.on_load_item()
		self.on_load_font()
		
		# Lancement du programme
		self.on_run()
	
	def on_load_level(self, nb_level):
		self.n_level = 1
		
		self._level = {}
		
		counter_alien = 1
		alien_dommage = 10
		for level in range(nb_level):
			if level % 3 == 0 and level > 1:
				self._level[level+1] = {
					"type": "bonus"
				}
			
			else:
				score = 5 + (level * 5)
				
				if level % 3 == 0:
					alien_dommage += 10
					
				self._level[level+1] = {
					"nb_alien": counter_alien,
					"score": score,
					"alien_dommage": alien_dommage
				}
			
			counter_alien += 1
			if counter_alien > 3:
				counter_alien = 0
		
		print(self._level)
		
		self.level = {
			1: {"nb_alien": 1,
				"score": 10,
				"alien_dommage": 10,
				"type": "alien"},
			2: {"nb_alien": 2,
				"score": 15,
				"alien_dommage": 10,
				"type": "alien"},
			3: {"nb_alien": 3,
				"score": 20,
				"alien_dommage": 10,
				"type": "alien"},
			4: {"type": "bonus"},
			5: {"nb_alien": 1,
				"score": 25,
				"alien_dommage": 20,
				"type": "alien"},
			6: {"nb_alien": 2,
				"score": 30,
				"alien_dommage": 20,
				"type": "alien"},
			7: {"nb_alien": 3,
				"score": 35,
				"alien_dommage": 20,
				"type": "alien"},
			8: {"type": "bonus"},
			9: {"nb_alien": 1,
				"score": 40,
				"alien_dommage": 30,
				"type": "alien"},
			10: {"nb_alien": 2,
				"score": 45,
				"alien_dommage": 30,
				"type": "alien"},
			11: {"nb_alien": 3,
				"score": 50,
				"alien_dommage": 30,
				"type": "alien"},
			12: {"type": "bonus"},
			13: {"nb_alien": 1,
				"score": 55,
				"alien_dommage": 40,
				"type": "alien"},
			14: {"nb_alien": 2,
				"score": 60,
				"alien_dommage": 40,
				"type": "alien"},
			15: {"nb_alien": 3,
				"score": 65,
				"alien_dommage": 40,
				"type": "alien"},
			16: {"type": "bonus"},
			17: {"nb_alien": 1,
				"score": 70,
				"alien_dommage": 50,
				"type": "alien"},
			18: {"nb_alien": 2,
				"score": 75,
				"alien_dommage": 50,
				"type": "alien"},
			19: {"nb_alien": 3,
				"score": 80,
				"alien_dommage": 50,
				"type": "alien"},
		}
		
	def on_load_item(self):
		self.game = Game(self.fen)
		
		self.score = 0
		self._on_bonus_level = False
		self.on_fight_level = True
		self.on_tempo = False
		self.next_bool = False
		self.next_bool2 = False
		self.next_bool3 = True
		
		self.player = Player(load_png("vaisseau.png", (255,255,255)), self.game)
		self.player.img_vie = Vie(50, 3, [0, 20], True)
		self.player.img_vie.x = 5
		self.player.img_vie.y = 5
		self.game.vaisseau_vie_list.add(self.player.img_vie)
		self.game.player = self.player
		self.game.add_player(self.player)
		
		timer = 500
		act = pygame.time.get_ticks()
		
		# Generation aliens
		nb_alien = 1
		self.load_alien(self.level[self.n_level]["nb_alien"])
		
		# Timers
		self.timer_tir = 1000
		self._timer_tir = 0
		
		self.timer_level_bonus = 10000
		self._timer_level_bonus = 0
		self.timer_repop_monster = 2000
		self._timer_repop_monster = 0
		self.pop_bonus = 2500
		self._pop_bonus = 0
		self.pop_malus = 250
		self._pop_malus = 500
	
	
	def load_alien(self, nb_alien):
		i = 0
		while i < nb_alien:
			type_alien = self.level[self.n_level]["type"]
			alien = Alien(load_png("{}1.png" .format(type_alien), (255,255,255)), self.game)
				
			alien.img_good = load_png("{}1.png" .format(type_alien), (255,255,255))
			alien.img_middle = load_png("{}2.png" .format(type_alien), (255,255,255))
			alien.img_bad = load_png("{}3.png" .format(type_alien), (255,255,255))
			alien.img_vie = Vie(30, 3, [-4, -6])
			alien.dmg = self.level[self.n_level]["alien_dommage"]
			
			alien.rect.x = randrange(10, 289) 
			alien.rect.y = randrange(10, 159)
			alien.shoot_image = load_png("tir2.png")
			
			self.game.alien_list.add(alien)
			self.game.alien_vie_list.add(alien.img_vie)
			
			i+=1
	
	def on_load_font(self):
		# Gestion des polices
		if not pygame.font: print("Attention, les polices sont désactivees !")
		else:
			self.font = pygame.font.Font(None, 24)
			
			self.text_score = self.font.render("Score : {}" .format(render_score(self.game.score)), 1, (255,255,255))
			self.text_score_pos = (5,5)
			

	def on_run(self):
		while 1:
			self.clock.tick(60)
			
			event_code = self.on_event()
			# Arrêt du programme
			if event_code == -1:
				break
			
			self.on_timer()
			self.game.update()
			
			# Changement du score par kill
			if self.game.has_killed:
				self.game.score += self.level[self.n_level]["score"]
				self.game.has_killed = False
			
			# Changement de vitesse de scroll et de niveau
			if len(self.game.alien_list) == 0:
				if not self._on_bonus_level and not self.on_tempo and self.next_bool3:
					self.n_level += 1
					self.next_bool = True
					self.on_tempo = False
					self.next_bool3 = False
					
				if self.level[self.n_level]["type"] == "bonus": # Bonus level
					if self.next_bool and not self.on_tempo:
						self._timer_level_bonus = pygame.time.get_ticks()
						self._on_bonus_level = True
						self.next_bool = False
		
					self.on_fight_level = False
					
				
				elif self.level[self.n_level]["type"] == "alien" and self.on_fight_level:
					self.load_alien(self.level[self.n_level]["nb_alien"])
					self.next_bool3 = True
			
			# Rendu de l'affichage
			self.on_render()
			pygame.display.flip()
			
		print("Home screen")
	
	def popper_bonus(self, type_bonus):
		if type_bonus == "bonus":
			name_file = "heal.png"
		elif type_bonus == "malus":
			name_file = "malus.png"
			
		bonus = Bonus(load_png(name_file, (255,255,255)), self.game, type_bonus)
		bonus.rect.x = randrange(32, 288)
		bonus.rect.y = -32
		self.game.bonus_list.add(bonus)
		
	
	def on_timer(self):
		# Gestion des timer
		current = pygame.time.get_ticks()
		
		if current > self.timer_tir + self._timer_tir:
			self.player.can_shoot = True
			self._timer_tir = current
		
		if self._on_bonus_level:
			# Pop bonus
			if current > self.pop_bonus + self._pop_bonus:
				self.popper_bonus("bonus")
				self._pop_bonus = current
			
			# Pop malus
			if current > self.pop_malus + self._pop_malus:
				self.popper_bonus("malus")
				self._pop_malus = current
			
			# Test de fin du niveau bonus
			if current > self.timer_level_bonus + self._timer_level_bonus:
				self._on_bonus_level = False
				self.on_tempo = True
				self.next_bool2 = True
				self._timer_repop_monster = current
		
		if self.next_bool2 and self.on_tempo:
			if current > self.timer_repop_monster + self._timer_repop_monster:
				self.n_level += 1
				self.game.vitesse_scroll += 10
				self.on_fight_level = True
				self.on_tempo = False
				self._on_bonus_level = False
				self.next_bool3 = False
				
	
	def on_event(self):
		# Boucle d'événement
		exclued = ["GAUCHE", "DROITE"]
		for name in self.inputs:
			button = self.inputs[name][0]
			
			if GPIO.input(button) == False and self.inputs[name][1] == 0:
				if name not in exclued:
					self.inputs[name][1] = 1
				
				if name == "SELECT":
					return -1
				elif name == "GAUCHE":
					self.player.go_left()
				elif name == "DROITE":
					self.player.go_right()
				elif name == "A":
					self.player.shoot(load_png("tir.png"))
				elif name == "START":
					if not self.game.on_pause_blocked:
						self.game.pause()
			
			elif GPIO.input(button) == True and self.inputs[name][1] == 1:
				self.inputs[name][1] = 0
			elif GPIO.input(button) == True and name in exclued:
				if name == "GAUCHE" and GPIO.input(self.inputs["DROITE"][0]) == True:
					self.player.stop_x()
				elif name == "DROITE" and GPIO.input(self.inputs["GAUCHE"][0]) == True:
					self.player.stop_x()
		
		for event in pygame.event.get():
			# Demande d'arrêt
			if event.type == QUIT:
				return -1
			
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return -1
				if event.key == K_LEFT:
					self.player.go_left()
				if event.key == K_RIGHT:
					self.player.go_right()
				if event.key == K_SPACE:
					self.player.shoot(load_png("tir.png"))
				if event.key == K_p:
					if not self.game.on_pause_blocked:
						self.game.pause()
			
			if event.type == KEYUP:
				if event.key == K_LEFT and self.player.change_x < 0:
					self.player.stop_x()
				if event.key == K_RIGHT and self.player.change_x > 0:
					self.player.stop_x()

	def on_render(self):
		self.game.draw()
		
		self.text_score = self.font.render("Score : {}" .format(render_score(self.game.score)), 1, (255,255,255))
		self.fen.blit(self.text_score, self.text_score_pos)
		
		
		


