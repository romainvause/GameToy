#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2014 Romain <Romain@ROMAIN-PC>

# Imports systèmes
import pygame
from pygame.locals import *
from pygame.examples import *
import RPi.GPIO as GPIO

# Imports locaux
import jeu, fonctions

class Master(object):
	""" Classe maitre de l'application"""
	def __init__(self):
		pygame.mouse.set_visible(False)
		print("Home screen")
		# Variable de programme principale
		# Parametres du sélecteur
		self.selector_level = 0
		
		# Resolution fenetre master
		self.fen = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
		
		# Chargement
		self.on_load_item()
		self.on_load_font()
		
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
		
		# Lancement du programme
		self.on_run()
	
	def on_load_item(self):
		self.home_selector = pygame.Surface((100,35))
		self.home_selector_pos = self.home_selector.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-18)
		self.bg_image = pygame.image.load("images/bg.jpg")
	
	def on_load_font(self):
		# Gestion des polices
		if not pygame.font: print("Attention, les polices sont désactivees !")
		else:
			self.font = pygame.font.Font(None, 24)
			
			# Texte écran d'accueil
			self.text_home_screen = self.font.render("SpaceInvaders", 1, (255,255,255))
			self.text_home_screen_pos = self.text_home_screen.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-100)
			self.text_home_screen2 = self.font.render("DESIGNED FOR GameToy", 1, (255,255,255))
			self.text_home_screen2_pos = self.text_home_screen2.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-83)
			self.text_home_play = self.font.render("JOUER", 1, (255,255,255))
			self.text_home_play_pos = self.text_home_play.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-16)
			#~ self.text_home_settings = self.font.render("OPTIONS", 1, (255,255,255))
			#~ self.text_home_settings_pos = self.text_home_settings.get_rect(centerx=(self.fen.get_width()/2), centery=(self.fen.get_height()/2)+16)
			#~ self.text_home_about = self.font.render("ABOUT", 1, (255,255,255))
			#~ self.text_home_about_pos = self.text_home_about.get_rect(centerx=(self.fen.get_width()/2)-105, centery=(self.fen.get_height()/2)+95)
			self.text_home_quit = self.font.render("QUITTER", 1, (255,255,255))
			self.text_home_quit_pos = self.text_home_quit.get_rect(centerx=(self.fen.get_width()/2)+105, centery=(self.fen.get_height()/2)+95)
	
	def on_run(self):
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
					jeu.Jeu(self.fen)
				elif self.selector_level == 1: # QUITTER
					break
				
			# Traitement du sélecteur
			if self.selector_level < 0:
				self.selector_level = 1
			elif self.selector_level > 1:
				self.selector_level = 0
			
			if self.selector_level == 0: # JOUER
				self.home_selector_pos = self.home_selector.get_rect(centerx=self.fen.get_width()/2, centery=(self.fen.get_height()/2)-18)
			elif self.selector_level == 1: # QUITTER
				self.home_selector_pos = self.home_selector.get_rect(centerx=(self.fen.get_width()/2)+105, centery=(self.fen.get_height()/2)+93)
			
			# Rendu de l'affichage
			self.on_render()
			pygame.display.flip()
		
		print("END")
			
	def on_event(self):
		# Vitesse de boucle
		pygame.time.Clock().tick(60)
		
		for name in self.inputs:
			button = self.inputs[name][0]
			
			if GPIO.input(button) == False and self.inputs[name][1] == 0:
				self.inputs[name][1] = 1
				#~ 
				if name == "SELECT":
					return -1
				elif name == "BAS":
					return "selector+1"
				elif name == "HAUT":
					return "selector-1"
				elif name == "A":
					return "chosedHome"
			#~ 
			elif GPIO.input(button) == True and self.inputs[name][1] == 1:
				self.inputs[name][1] = 0
		
		# Boucle d'événement
		for event in pygame.event.get():
			# Demande d'arrêt
			if event.type == QUIT:
				return -1
			
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return -1
				elif event.key == K_DOWN:
					return "selector+1"
				elif event.key == K_UP:
					return "selector-1"
				elif event.key == K_RETURN:
					return "chosedHome"
	
	def on_render(self):
		self.fen.fill((0,0,0))
			
		self.fen.blit(self.bg_image, (0,0))
			
		pygame.draw.rect(self.fen, (255,255,255), self.home_selector_pos, 2)

		self.fen.blit(self.text_home_screen, self.text_home_screen_pos)
		self.fen.blit(self.text_home_screen2, self.text_home_screen2_pos)
		self.fen.blit(self.text_home_play, self.text_home_play_pos)
		self.fen.blit(self.text_home_quit, self.text_home_quit_pos)
		#~ self.fen.blit(self.text_home_about, self.text_home_about_pos)
		#~ self.fen.blit(self.text_home_settings, self.text_home_settings_pos)
			

if __name__ == "__main__":
	pygame.init()
	m = Master()
