#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  score.py
#  
#  Copyright 2014 Romain <Romain@ROMAIN-PC>

# Imports systèmes
import pygame
from pygame.locals import *
from random import randrange
import sys

# Imports locaux
import main, fonctions
#~ , fonctions, classes

class Score(object):
	"""Classe de Score"""
	def __init__(self, fen):
		print("Score")
		# Variable de programme principale
		self.fen = fen
		
		# Parametres du sélecteur
		self.selector_level = 1
		
		# Chargement
		self.on_load_item()
		self.on_load_font()
		
		# Lancement du programme
		self.on_run()
		
	def on_load_item(self):
		"""Chargement des différents éléments de jeu"""
		# Chargement du background
		self.background_image = pygame.image.load("images/background.gif").convert()
		
		# Chargement du sélecteur
		self.home_selector = pygame.Surface((100,35))
		self.home_selector_pos = self.home_selector.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-18)
	
	def on_load_font(self):
		"""Chargement des polices du jeu"""
		# Gestion des polices
		if not pygame.font: print("Attention, les polices sont désactivees !")
		else:
			self.font       = pygame.font.Font(None, 24)
			self.font_score = pygame.font.Font(None, 22)
			
			self.text_screen = self.font.render("SCORE", 1, (255,255,255))
			self.text_screen_pos = self.text_screen.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-100)
			self.text_quit = self.font.render("QUITTER", 1, (255,255,255))
			self.text_quit_pos = self.text_quit.get_rect(centerx=(self.fen.get_width()/2)+105, centery=(self.fen.get_height()/2)+95)
			self.text_reset = self.font.render("RESET", 1, (255,255,255))
			self.text_reset_pos = self.text_reset.get_rect(centerx=(self.fen.get_width()/2)-105, centery=(self.fen.get_height()/2)+95)
			self.text_easy = self.font.render("Easy :", 1, (255,255,255))
			self.text_easy_pos = self.text_easy.get_rect(centerx=(self.fen.get_width()/2)-130, centery=(self.fen.get_height()/2)-40)
			self.text_medium = self.font.render("Medium :", 1, (38,200,33))
			self.text_medium_pos = self.text_medium.get_rect(centerx=(self.fen.get_width()/2)-6, centery=(self.fen.get_height()/2)-40)
			self.text_hard = self.font.render("Hard :", 1, (227,42,58))
			self.text_hard_pos = self.text_hard.get_rect(centerx=(self.fen.get_width()/2)+92, centery=(self.fen.get_height()/2)-40)
			
			# Chargement des scores
			self.get_score()
			
			self.lst_easy = []
			self.lst_medium = []
			self.lst_hard = []
			for i, item in enumerate(self.score_easy): # EASY
				text = self.font_score.render(str(i+1) + ".  " + fonctions.render_score(item), 1, (255,255,255))
				text_pos = (7, (13*i)+95)
				
				self.lst_easy.append((text, text_pos))
				
			for i, item in enumerate(self.score_medium): # MEDIUM
				text = self.font_score.render(str(i+1) + ".  " + fonctions.render_score(item), 1, (38,200,33))
				text_pos = (117, (13*i)+95)
				
				self.lst_easy.append((text, text_pos))
				
			for i, item in enumerate(self.score_hard): # HARD
				text = self.font_score.render(str(i+1) + ".  " + fonctions.render_score(item), 1, (227,42,58))
				text_pos = (230, (13*i)+95)
				
				self.lst_easy.append((text, text_pos))
			
			
	def on_run(self):
		"""Programme principal"""

		while 1:
			event_code = self.on_event()
			# Arrêt du programme
			if event_code == -1:
				break
			# Déplacement du séleccteur
			elif event_code == "selector+1": # up
				self.selector_level += 1
			elif event_code == "selector-1": # down
				self.selector_level -= 1
			elif event_code == "chosedHome":
				if self.selector_level == 0: # RESET
					print("Reset")
				elif self.selector_level == 1: # QUITTER
					break
			
			# Traitement du sélecteur
			if self.selector_level < 0:
				self.selector_level = 1
			elif self.selector_level > 1:
				self.selector_level = 0
			
			elif self.selector_level == 0: # RESET
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)-105, centery=(self.fen.get_height()/2)+93)
			elif self.selector_level == 1: # QUITTER
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)+105, centery=(self.fen.get_height()/2)+93)
			
			
			# Rendu de l'écran
			self.on_render()
			pygame.display.flip()
			
		print("Home screen")
	
	def on_event(self):
		"""Gestion des évènement"""
		# Boucle d'événement
		for event in pygame.event.get():
			# Demande d'arrêt
			if event.type == QUIT:
				return -1
			
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return -1
				elif event.key == K_DOWN or event.key == K_RIGHT:
					return "selector+1"
				elif event.key == K_UP or event.key == K_LEFT:
					return "selector-1"
				elif event.key == K_RETURN:
					return "chosedHome"

	def on_render(self):
		"""Rendu du jeu"""
		self.fen.fill((0,0,0))
		
		self.fen.blit(self.background_image, (0,0))

		pygame.draw.rect(self.fen, (255,255,255), self.home_selector_pos, 2)
		self.fen.blit(self.text_screen, self.text_screen_pos)
		self.fen.blit(self.text_quit, self.text_quit_pos)
		self.fen.blit(self.text_reset, self.text_reset_pos)
		
		# Affichage des scores
		self.fen.blit(self.text_easy, self.text_easy_pos)
		self.fen.blit(self.text_medium, self.text_medium_pos)
		self.fen.blit(self.text_hard, self.text_hard_pos)
		
		for i in self.lst_easy:
			self.fen.blit(i[0], i[1])
	
	
	def get_score(self):
		score_file = open(sys.path[0] + "\\files\\score.txt")
		data = score_file.read().split("\n")
		data = sorted(data)
		# Suppresion des données vide
		for i, score in enumerate(data):
			if score == "":
				data.pop(i)
				
		# Récupération des score
		score_easy   = [0 for x in range(5)]
		score_medium = [0 for x in range(5)]
		score_hard   = [0 for x in range(5)]
		
		for score in data:
			content = score.split(":")
			if content[0] == "easy":
				score_easy.append(int(content[1]))
			if content[0] == "medium":
				score_medium.append(int(content[1]))
			if content[0] == "hard":
				score_hard.append(int(content[1]))
		
		self.score_easy = sorted(score_easy)[len(score_easy)-5: len(score_easy)]
		self.score_easy.reverse()
		self.score_medium = sorted(score_medium)[len(score_medium)-5: len(score_medium)]
		self.score_medium.reverse()
		self.score_hard = sorted(score_hard)[len(score_hard)-5: len(score_hard)]
		self.score_hard.reverse()

		score_file.close()
