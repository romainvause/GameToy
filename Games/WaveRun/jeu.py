#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  jeu.py
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

class Jeu(object):
	"""Classe de jeu"""
	def __init__(self, fen, settings):
		print("Game")
		# Variable de programme principale
		self.fen      = fen
		self.settings = settings
		self.code     = -1
		
		print(settings["difficulty"])
		
		# EASY
		first = pygame.time.get_ticks()
		if (settings["difficulty"] == "easy"):
			self.list_pos = fonctions.generate_line(100000, 240, 20, 100)
			self.list2_pos = fonctions.generate_line(100000, 240, 120, 200, self.list_pos)
		# HARD
		else:
			self.list_pos  = fonctions.generate_line(10000, 240, 20, 200)
			self.list2_pos = fonctions.generate_line(10000, 240, 20, 200, self.list_pos)
		end = pygame.time.get_ticks()
		print("Temps ecoule : {}" .format(end-first))
		# Gameover
		self.game_over = False
		
		# Pionts
		self.niveau = 1
		self.score  = 0
		
		# Timer
		if (settings["difficulty"] == "easy"): # Easy
			self.timer 		= 5
			self.timer_move = 40
		elif (settings["difficulty"] == "medium"): # Medium
			self.timer 		= 5
			self.timer_move = 30
		else: # Hard
			self.timer 		= 1
			self.timer_move = 10
			
		self.timer_score = 1000
		
		# Positions écran
		self.movey 	   = "up"
		self.movex 	   = "left"
		self.movey_pos = 0
		self.movex_pos = 0
		self.limy      = 0
		self.limx      = 0
		
		# Chargement
		self.on_load_item()
		self.on_load_font()
		
		# Lancement du programme
		self.on_run()
		
	def on_load_item(self):
		"""Chargement des différents éléments de jeu"""
		# Chargement des images
		self.pixel  = pygame.image.load("images/pixel.png").convert()
		self.limite = pygame.image.load("images/limite.png").convert()
		self.line   = pygame.image.load("images/line.png").convert()
		self.player = pygame.image.load("images/player.png").convert()
		
		self.player.set_colorkey((255,255,255))
		
		# Chargement du background
		self.background_image = pygame.image.load("images/background.gif").convert()
		
		# Son de mort
		if (self.settings["sound"] == "on"):
			self.explosion_sound = pygame.mixer.Sound("sons/explosion.wav")
	
	def on_load_font(self):
		"""Chargement des polices du jeu"""
		# Gestion des polices
		if not pygame.font: print("Attention, les polices sont désactivees !")
		else:
			self.font = pygame.font.Font(None, 24)
			self.text_score = self.font.render("Score : {}" .format(fonctions.render_score(self.score)), 1, (255,255,255))
			self.text_score_pos = (5,5)
			
			self.font_game_over = pygame.font.Font(None, 32)
			self.text_game_over = self.font_game_over.render("Game 0ver", 1, (255,255,255))
			self.text_game_over_pos = self.text_game_over.get_rect(centerx=(self.fen.get_width()/2)-50, centery=(self.fen.get_height()/2)-20)
			
	def on_run(self):
		"""Programme principal"""
		old  = 0
		old2 = 0
		old3 = 0
		
		while 1:
			event_code = self.on_event()
			# Arrêt du programme
			if event_code == -1:
				break
			elif event_code == "dead":
				self.code = "dead"
				break
			
			# GESTION ECRAN
			# Gestion position écran haut/bas
			if self.movey_pos <= -self.limy:
				self.limy = randrange(5, 20)
				self.movey = "down"
			elif self.movey_pos >= self.limy:
				self.limy = randrange(5, 20)
				self.movey = "up"
			
			# Gestion position écran gauche/droite
			if self.movex_pos <= -self.limx:
				self.limx = randrange(5, 20)
				self.movex = "right"
			elif self.movex_pos >= 0:
				self.limx = randrange(5, 20)
				self.movex = "left"
			
			# Récupération temps actuel
			current = pygame.time.get_ticks()
			
			# Timer d'avancement du perso
			if (current > old+self.timer and not self.game_over): 
				self.list_pos.pop(0)
				self.list2_pos.pop(0)
				self.score += 1
				
				old = current
			
			# Timer de mouvement d'écran
			if (current > old2+self.timer_move and not self.game_over): 
				if self.movey == "up":
					self.movey_pos -= 1
				elif self.movey == "down":
					self.movey_pos += 1
					
				if self.movex == "left":
					self.movex_pos -= 1
				elif self.movex == "right":
					self.movex_pos +=1
					
				old2 = current
			
			# Timer de mouvement du score
			if (current > old3+self.timer_score and self.game_over):
				centerx = self.text_game_over.get_rect(centerx=(self.fen.get_width()/2))[0]
				centery = self.text_game_over.get_rect(centery=(self.fen.get_height()/2))[1]
				if (self.text_score_pos[0] < centerx+20):
					self.text_score_pos = (self.text_score_pos[0]+1, self.text_score_pos[1]+1)
				elif (self.text_score_pos[1] < centery):
					self.text_score_pos = (self.text_score_pos[0], self.text_score_pos[1]+1)
			
			# Rendu du score en haut à gauche
			self.text_score = self.font.render("Score : {}" .format(fonctions.render_score(self.score)), 1, (255,255,255))
			
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
					if self.game_over:
						return "dead"
					else:
						return -1
				elif (event.key == K_RETURN or event.key == K_SPACE) and not self.game_over: # ENTRER OU BARRE ESPACE
					# Définition d'une ligne de déplacement
					self.list_pos[100][3] = 1
					
					# Changement de niveau du perso
					if (self.niveau == 1):
						self.niveau = 2
					elif (self.niveau == 2):
						self.niveau = 1

	def on_render(self):
		"""Rendu du jeu"""
		self.fen.fill((0,0,0))
		
		# Affichage du background
		self.fen.blit(self.background_image, (0,0))
		
		# Affichage du score
		self.fen.blit(self.text_score, self.text_score_pos)
		
		# Affichage gameOver
		if self.game_over:
			self.fen.blit(self.text_game_over, self.text_game_over_pos)
		
		i = 0
		while i < 350 and not self.game_over:
			# Dessin du trajet du perso
			if (i == 97):
				if (self.niveau == 1):
					self.list_pos[i][2] = "green"
				elif (self.niveau == 2):
					self.list2_pos[i][2] = "green"
			
			# Sur niveau 1 : Test de mort et affichage du perso
			if (self.niveau == 1):
				if (self.list_pos[100][2] == "red"):
					self.game_over = True
					if (self.settings["music"] == "on"):
						pygame.mixer.music.pause()
					if (self.settings["sound"] == "on"):
						self.explosion_sound.play()
						
					# Ecriture du score dans le fichier
					file_score = open(sys.path[0] + "\\files\\score.txt", "a")
					file_score.write(self.settings["difficulty"] + ":" + str(self.score) + "\n")
					file_score.close()
					print("MORT")
				
				posx = 98 + self.movex_pos
				posy = self.list_pos[100][1]-2+self.movey_pos
				
				self.fen.blit(self.player, (posx, posy))
			
			# Sur niveau 2 : Test de mort et affichage du perso
			elif (self.niveau == 2):
				if (self.list2_pos[100][2] == "red"):
					self.game_over = True
					if (self.settings["music"] == "on"):
						pygame.mixer.music.pause()
					if (self.settings["sound"] == "on"):
						self.explosion_sound.play()
						
					# Ecriture du score dans le fichier
					file_score = open(sys.path[0] + "\\files\\score.txt", "a")
					file_score.write(self.settings["difficulty"] + ":" + str(self.score) + "\n")
					file_score.close()
					print("MORT")
				
				posx = 98 + self.movex_pos
				posy = self.list2_pos[100][1]-2+self.movey_pos
				
				self.fen.blit(self.player, (posx, posy))
			
			# Affichage du trajet
			posx = i + self.movex_pos
			posy = self.list_pos[i][1] + self.movey_pos # Niveau 1
			posy2 = self.list2_pos[i][1] + self.movey_pos # Niveau 2
			
			# Niveau 1
			if (self.list_pos[i][2] == "white"):		
				self.fen.blit(self.pixel, (posx, posy))
			elif (self.list_pos[i][2] == "red"):
				self.fen.blit(self.limite, (posx, posy))
			elif (self.list_pos[i][2] == "green"):
				self.fen.blit(self.line, (posx, posy))
			
			# Niveau 2
			if (self.list2_pos[i][2] == "white"):
				self.fen.blit(self.pixel, (posx, posy2))
			elif (self.list2_pos[i][2] == "red"):
				self.fen.blit(self.limite, (posx, posy2))
			elif (self.list2_pos[i][2] == "green"):
				self.fen.blit(self.line, (posx, posy2))
			
			# Dessin d'une ligne entre deux niveaux
			if (self.list_pos[i][3] == 1):
				deb = self.list_pos[i][1]
				end = self.list2_pos[i][1]
				pygame.draw.line(self.fen, (181,230,29), [i+self.movex_pos, deb+self.movey_pos], [i+self.movex_pos, end+self.movey_pos], 3)
		
			i+=1
