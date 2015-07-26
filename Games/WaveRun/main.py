#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2014 Romain <Romain@ROMAIN-PC>

# Imports systèmes
import pygame
from pygame.locals import *
from random import randrange
import sys, os

import RPi.GPIO as GPIO

# Imports locaux
import jeu, fonctions, score, settings
#~ , fonctions, classes

class Master(object):
	""" Classe maitre de l'application"""
	def __init__(self):
		print("Home screen")
		# Variable de programme principale
		# Timer
		self.timer_line = 25
		self.timer_add = 1000
		#~ self.timer_fun = 16200
		self.timer_fun = 16200000
		
		# Lines
		self.lines = []
		
		# Musique
		self.timer_music = 500
		self.volume = 0
		
		# Parametres du sélecteur
		self.selector_level = 1
		
		# Resolution fenetre master
		self.fen = pygame.display.set_mode((320, 240))
		
		# Chargement
		self.on_load_settings()
		self.on_load_item()
		self.on_load_font()
		
		# Lancement du programme
		self.on_run()
	
	def on_load_item(self):
		# Chargement de la musique
		pygame.mixer.music.load("musiques/musique5.ogg")
		pygame.mixer.music.play(-1)
		
		if (self.settings["music"] == "off"):
			pygame.mixer.music.pause()
		
		# Chargement du background
		self.background_image = pygame.image.load("images/background.gif").convert()
		
		# Chargement du sélecteur
		self.home_selector = pygame.Surface((100,35))
		self.home_selector_pos = self.home_selector.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-18)
		
	
	def on_load_font(self):
		# Gestion des polices
		if not pygame.font: print("Attention, les polices sont désactivees !")
		else:
			self.font = pygame.font.Font(None, 24)
			
			# Texte écran d'accueil
			self.text_home_screen = self.font.render("WaveRun", 1, (255,255,255))
			self.text_home_screen_pos = self.text_home_screen.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-100)
			self.text_home_screen2 = self.font.render("DESIGNED FOR GameToy", 1, (255,255,255))
			self.text_home_screen2_pos = self.text_home_screen2.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-83)
			self.text_home_play = self.font.render("JOUER", 1, (255,255,255))
			self.text_home_play_pos = self.text_home_play.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-16)
			self.text_home_settings = self.font.render("OPTIONS", 1, (255,255,255))
			self.text_home_settings_pos = self.text_home_settings.get_rect(centerx=(self.fen.get_width()/2), centery=(self.fen.get_height()/2)+16)
			self.text_home_about = self.font.render("SCORE", 1, (255,255,255))
			self.text_home_about_pos = self.text_home_about.get_rect(centerx=(self.fen.get_width()/2)-105, centery=(self.fen.get_height()/2)+95)
			self.text_home_quit = self.font.render("QUITTER", 1, (255,255,255))
			self.text_home_quit_pos = self.text_home_quit.get_rect(centerx=(self.fen.get_width()/2)+105, centery=(self.fen.get_height()/2)+95)

	
	def on_load_settings(self):
		dirname = os.path.dirname(os.path.realpath(__file__))
		file_settings = open(dirname + "\\files\\settings.txt", "r")
		data = file_settings.read().split("\n")
		
		self.settings = {}
		for i in data:
			content = i.split(":")
			self.settings[content[0]] = content[1]


	def on_run(self):
		old  = 0
		old2 = 0
		self.lines = [fonctions.genere_line_droite()]
		
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
				if self.selector_level == 0: # JOUER
					code = jeu.Jeu(self.fen, self.settings).code
					if code == "dead":
						if self.settings["music"] == "on":
							pygame.mixer.music.unpause()
					self.lines = []
					
				elif self.selector_level == 1: # OPTIONS
					self.settings = settings.Settings(self.fen, self.settings).settings
					if self.settings["music"] == "off":
						pygame.mixer.music.pause()	
					if self.settings["music"] == "on":
						pygame.mixer.music.unpause()
				elif self.selector_level == 2: # SCORE
					score.Score(self.fen)
				elif self.selector_level == 3: # QUITTER
					break
			
			# Timer line
			current = pygame.time.get_ticks()
			if current > old + self.timer_line:
				for line in self.lines:
					if line[3] < line[0]:
						line[3] += 1

				old = current
			
			if current > old2 + self.timer_add:
				self.lines.append(fonctions.genere_line_droite())
				old2 = current
			
			if current > self.timer_fun:
				self.timer_add = 1
				self.timer_line = 1
			
			# Traitement du sélecteur
			if self.selector_level < 0:
				self.selector_level = 3
			elif self.selector_level > 3:
				self.selector_level = 0
			
			if self.selector_level == 0: # JOUER
				self.home_selector_pos = self.home_selector.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-18)
			elif self.selector_level == 1: # OPTIONS
				self.home_selector_pos = self.home_selector.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)+15)
			elif self.selector_level == 2: # ABOUT
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)-105, centery=(self.fen.get_height()/2)+93)
			elif self.selector_level == 3: # QUITTER
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)+105, centery=(self.fen.get_height()/2)+93)
			
			# Rendu de l'affichage
			self.on_render()
			pygame.display.flip()
		
		print("END")
			
	def on_event(self):
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
		self.fen.fill((0,0,0))
		
		self.fen.blit(self.background_image, (0,0))
		
		for line in self.lines:
			if line[2] == "left":
				pygame.draw.line(self.fen, line[5], [0, line[1]], [line[3], line[1]], line[6])
			elif line[2] == "right":
				pygame.draw.line(self.fen, line[5], [320, line[1]], [320-line[3], line[1]], line[6])
		
		pygame.draw.rect(self.fen, (255,255,255), self.home_selector_pos, 2)
		self.fen.blit(self.text_home_screen, self.text_home_screen_pos)
		self.fen.blit(self.text_home_screen2, self.text_home_screen2_pos)
		self.fen.blit(self.text_home_play, self.text_home_play_pos)
		self.fen.blit(self.text_home_quit, self.text_home_quit_pos)
		self.fen.blit(self.text_home_about, self.text_home_about_pos)
		self.fen.blit(self.text_home_settings, self.text_home_settings_pos)
			

if __name__ == "__main__":
	pygame.init()
	m = Master()
