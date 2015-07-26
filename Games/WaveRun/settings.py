#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  settings.py
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

class Settings(object):
	"""Classe de Score"""
	def __init__(self, fen, settings):
		print("Settings")
		# Variable de programme principale
		self.fen = fen
		self.settings = settings
		
		# Parametres du sélecteur
		self.selector_level = 0
		
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
		self.home_selector = pygame.Surface((10,35))
		self.home_selector_pos = self.home_selector.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-18)
	
	def on_load_font(self):
		"""Chargement des polices du jeu"""
		# Gestion des polices
		if not pygame.font: print("Attention, les polices sont désactivees !")
		else:
			self.font       = pygame.font.Font(None, 24)
			self.font_score = pygame.font.Font(None, 22)
			
			self.text_screen = self.font.render("SETTINGS", 1, (255,255,255))
			self.text_screen_pos = self.text_screen.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-100)
			self.text_quit = self.font.render("QUITTER", 1, (255,255,255))
			self.text_quit_pos = self.text_quit.get_rect(centerx=(self.fen.get_width()/2)+105, centery=(self.fen.get_height()/2)+95)
			self.text_level = self.font.render("LEVEL : ", 1, (255,255,255))
			self.text_level_pos = self.text_level.get_rect(centerx=(self.fen.get_width()/2)-80, centery=(self.fen.get_height()/2)-40)
			self.text_levelC = self.font.render(self.settings["difficulty"], 1, (255,255,255))
			self.text_levelC_pos = self.text_levelC.get_rect(centerx=(self.fen.get_width()/2), centery=(self.fen.get_height()/2)-40)
			self.text_music = self.font.render("MUSIC : ", 1, (255,255,255))
			self.text_music_pos = self.text_music.get_rect(centerx=(self.fen.get_width()/2)-80, centery=(self.fen.get_height()/2))
			self.text_musicC = self.font.render(self.settings["music"], 1, (255,255,255))
			self.text_musicC_pos = self.text_musicC.get_rect(centerx=(self.fen.get_width()/2), centery=(self.fen.get_height()/2))
			self.text_sound = self.font.render("SOUND : ", 1, (255,255,255))
			self.text_sound_pos = self.text_sound.get_rect(centerx=(self.fen.get_width()/2)-80, centery=(self.fen.get_height()/2)+40)
			self.text_soundC = self.font.render(self.settings["sound"], 1, (255,255,255))
			self.text_soundC_pos = self.text_soundC.get_rect(centerx=(self.fen.get_width()/2), centery=(self.fen.get_height()/2)+40)
			
			
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
				if self.selector_level == 0: # LEVEL
					self.change_level()
				elif self.selector_level == 1: # MUSIC
					self.change_music()
				elif self.selector_level == 2: # SOUND
					self.change_sound()
				elif self.selector_level == 3: # QUITTER
					break
			
			# Traitement du sélecteur
			if self.selector_level < 0:
				self.selector_level = 3
			elif self.selector_level > 3:
				self.selector_level = 0
			
			if self.selector_level == 0: # LEVEL
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)-35, centery=(self.fen.get_height()/2)-40)
			elif self.selector_level == 1: # MUSIC
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)-35, centery=(self.fen.get_height()/2))
			elif self.selector_level == 2: # SOUND
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)-35, centery=(self.fen.get_height()/2)+40)
			elif self.selector_level == 3: # QUITTER
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
		
		if (self.selector_level > 2):
			self.home_selector = pygame.Surface((100,35))
		else:
			self.home_selector = pygame.Surface((190,35))

		pygame.draw.rect(self.fen, (255,255,255), self.home_selector_pos, 2)
		
		self.fen.blit(self.text_screen, self.text_screen_pos)
		self.fen.blit(self.text_quit, self.text_quit_pos)
		self.fen.blit(self.text_level, self.text_level_pos)
		self.fen.blit(self.text_levelC, self.text_levelC_pos)
		self.fen.blit(self.text_music, self.text_music_pos)
		self.fen.blit(self.text_musicC, self.text_musicC_pos)
		self.fen.blit(self.text_sound, self.text_sound_pos)
		self.fen.blit(self.text_soundC, self.text_soundC_pos)
	
	
	def change_level(self):
		diff = self.settings["difficulty"]
		if diff == "easy":
			diff = "medium"
		elif diff == "medium":
			diff = "hard"
		elif diff == "hard":
			diff = "easy"
		
		self.settings["difficulty"] = diff
		
		self.text_levelC = self.font.render(self.settings["difficulty"], 1, (255,255,255))
		self.write_settings()
	
	def change_music(self):
		music = self.settings["music"]
		if music == "on":
			music = "off"
			pygame.mixer.music.pause()
		elif music == "off":
			music = "on"
			pygame.mixer.music.unpause()
		
		self.settings["music"] = music
		
		self.text_musicC = self.font.render(self.settings["music"], 1, (255,255,255))
		self.write_settings()
	
	def change_sound(self):
		sound = self.settings["sound"]
		if sound == "on":
			sound = "off"
		elif sound == "off":
			sound = "on"
			
		
		self.settings["sound"] = sound
		
		self.text_soundC = self.font.render(self.settings["sound"], 1, (255,255,255))
		self.write_settings()
	
	def write_settings(self):
		settings_file = open(sys.path[0] + "\\files\\settings.txt", "w")
		
		settings_file.write("difficulty:" + self.settings["difficulty"] + "\n")
		settings_file.write("music:" + self.settings["music"] + "\n")
		settings_file.write("sound:" + self.settings["sound"])
		
		settings_file.close()
		
		
