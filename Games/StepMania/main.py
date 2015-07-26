#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  testcombi.py
#  
#  Copyright 2015 Jordan_DI_SALVO_-_classe6tb

import pygame 
from pygame.locals import *
import os, sys
import time

import RPi.GPIO as GPIO

class Master(object):
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		inputs = {
			"A": [17, 0],
			"B": [18, 0],
			
			"START" : [27, 0],
			"SELECT": [22, 0],
			
			"BAS"   : [23, 0],
			"HAUT"  : [24, 0],
			"GAUCHE": [25, 0],
			"DROITE": [21, 0]
		}

		for name in inputs:
			GPIO.setup(inputs[name][0], GPIO.IN, GPIO.PUD_UP)

		pygame.init()
		pygame.mouse.set_visible(False)

		difficulte=0
		infinimenu=1
		infinijeux=1
		infinitot=1
		infinilvl=1
		infiniscore=1
		clock = pygame.time.Clock()
		#------------------ musique menu
		pygame.mixer.pre_init()
		pygame.mixer.music.load("musique/musique_menu.mp3")
		pygame.mixer.music.play()
		#------------------ musique menu
		#~ fenetre = pygame.display.set_mode((320, 240))
		fenetre = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
		pygame.display.set_caption("StepMania")
		menu_image = pygame.image.load("image/interface2.png").convert()

		while infinitot: #------------------ boucle principale
			while infinimenu: #------------------ boucle menu Jouer/Quitter

				fenetre.blit(menu_image, (0,0))
				
				for name in inputs:
					button = inputs[name][0]
					
					if GPIO.input(button) == False and inputs[name][1] == 0:
						inputs[name][1] = 1
						
						if name == "SELECT":
							print("exit")
							infinimenu=0
							infinitot=0
							infinijeux=0
							infinilvl=0
							infini=0
							quitter = 1
							break
						elif name == "START":
							infinimenu=0
							infinijeux=1
							infinilvl=1
							quitter = 0
					
					elif GPIO.input(button) == True and inputs[name][1] == 1:
						inputs[name][1] = 0
				
				pygame.display.flip()
				positionsouris=pygame.mouse.get_pos()
				for event in pygame.event.get():
					if event.type == QUIT:
						infinimenu=0
						infinitot=0
						infinijeux=0
						infinilvl=0
						infini=0
					#------------------------------------------ Choix jouer / quitter / score   
					elif event.type == KEYDOWN:
						if event.key == K_RETURN:
							print(infinimenu)
							infinimenu=0
							infinijeux=1
							infinilvl=1
							print("sortie menu play")
							
						elif event.key == K_ESCAPE:
							infinitot=0
							infinimenu=0
							infinijeux=0
							infinilvl=0
							infini=0
							print("sortie jeux exit")

			pygame.mixer.pre_init()
			pygame.mixer.music.load("musique/Avicii_You Make Me.mp3")
			map_jeux = open("map_jeux_normal.txt", "r")
			difficulte=5
			print("Normal")
			infinilvl=0
			infinimenu=0
			infinijeux=1
			score_difficulte="Normal"
			
			if quitter == 1:
				break
			
			frame_count = 0 #------------------ Nombre d'images
			frame_rate = 240 #------------------ Rafraichissement
			start_time = 239 #------------------ temps de la musique en secondes

			bad = 0

			while infinijeux: #------------------ boucle de la fenetre du jeu
				print("Debut de la partie")  
				#---------------------------------------------------------------------- Remplissage_fond
				fond = pygame.image.load("image/interface.png").convert()
				fenetre.blit(fond, (0,0))
				
				#---------------------------------------------------------------------- Collage des fleches fixes
				fleche_gauche_inv=pygame.image.load("image/fleche_gauche_inv.png").convert()
				fleche_gauche_inv.set_colorkey((255,255,255))
				fenetre.blit(fleche_gauche_inv,(10,80))
				#--
				fleche_bas_inv=pygame.image.load("image/fleche_bas_inv.png").convert()
				fleche_bas_inv.set_colorkey((255,255,255))
				fenetre.blit(fleche_bas_inv,(60,80))
				#--
				fleche_haut_inv=pygame.image.load("image/fleche_haut_inv.png").convert()
				fleche_haut_inv.set_colorkey((255,255,255))
				fenetre.blit(fleche_haut_inv,(110,80))
				#--
				fleche_droite_inv=pygame.image.load("image/fleche_droit_inv.png").convert()
				fleche_droite_inv.set_colorkey((255,255,255))
				fenetre.blit(fleche_droite_inv,(160,80))
				#--
				a_inv=pygame.image.load("image/a_inv.png").convert()
				a_inv.set_colorkey((255,255,255))
				fenetre.blit(a_inv,(210,80))
				#--
				b_inv=pygame.image.load("image/b_inv.png").convert()
				b_inv.set_colorkey((255,255,255))
				fenetre.blit(b_inv,(210,80))
				#---------------------------------------------------------------------- Chargement des fleches mobiles
				fleche_gauche = pygame.image.load("image/fleche_gauche.png").convert()
				fleche_gauche.set_colorkey((255,255,255))
				position_fleche_gauche = (10, 320)
				#--
				fleche_bas=pygame.image.load("image/fleche_bas.png").convert()
				fleche_bas.set_colorkey((255,255,255))
				position_fleche_bas = (60, 320)

				#--
				fleche_haut=pygame.image.load("image/fleche_haut.png").convert()
				fleche_haut.set_colorkey((255,255,255))
				position_fleche_haut = (110, 320)

				#--
				fleche_droit=pygame.image.load("image/fleche_droit.png").convert()
				fleche_droit.set_colorkey((255,255,255))
				position_fleche_droit = (160, 320)
				#--
				a=pygame.image.load("image/a.png").convert()
				a.set_colorkey((255,255,255))
				position_a = (210,320)
				#--
				b=pygame.image.load("image/b.png").convert()
				b.set_colorkey((255,255,255))
				position_b = (260,320)
				#----------------------------------------Police/couleur
				white=(255,255,255)
				font = pygame.font.SysFont("impact", 31)
				font2 = pygame.font.SysFont("impact", 25)
				font3 = pygame.font.SysFont("impact", 25)
				font4 = pygame.font.SysFont("impact", 25)
				#-----------------------------------------Police/couleur       
				temps = 5
				old_temps = 0
				score=0
				infini=1
				ligne = map_jeux.read() #--------------------Lecture de la carte
				index = 0
				block_line = True
				pygame.mixer.music.play()
				stage=1
				
				limite_px = 0
				
				while infini :
					pygame.display.flip()
					temps_actuel = pygame.time.get_ticks()
					nombre = ligne[index]
					

					if temps_actuel > temps + old_temps:
					#----------------------------------------------------------------------- ACTION
						if block_line:
							if nombre == "1": #----------------------------------------------------------------------- Gauche
								
								position_fleche_gauche = (position_fleche_gauche[0], position_fleche_gauche[1] -difficulte)
								if position_fleche_gauche[1] <= limite_px:
									position_fleche_gauche = (10, 320)
									block_line = False
										
							elif nombre == "2" : #----------------------------------------------------------------------- Bas
								
								position_fleche_bas = (position_fleche_bas[0], position_fleche_bas[1] -difficulte)
								if position_fleche_bas[1] <= limite_px:
									position_fleche_bas = (60, 320)
									block_line = False
							
							elif nombre == "3" : #----------------------------------------------------------------------- Haut
							
								position_fleche_haut = (position_fleche_haut[0], position_fleche_haut[1] -difficulte)
								if position_fleche_haut[1] <= limite_px:
									position_fleche_haut = (110, 320)
									block_line = False  

							elif nombre == "4": #----------------------------------------------------------------------- Droit
								
								position_fleche_droit = (position_fleche_droit[0], position_fleche_droit[1] -difficulte)
								if position_fleche_droit[1] <= limite_px:
									position_fleche_droit = (160, 320)
									block_line = False  
								
							elif nombre == "5": #----------------------------------------------------------------------- Fin partie
								pygame.mixer.music.stop()
								infinijeux=0
								infini=0
								infinimenu=1
								iniinitot=1
								infinilvl=1
								pygame.time.wait(3500)
								pygame.mixer.pre_init()
								pygame.mixer.music.load("musique/musique_menu.mp3")
								pygame.mixer.music.play()
								break
							
							elif nombre =="A":#--------------------------------------------------------gauche-droite
								
								position_fleche_gauche = (position_fleche_gauche[0], position_fleche_gauche[1] -difficulte)
									
								if position_fleche_gauche[1] <= limite_px:
									position_fleche_gauche = (10, 320)
									block_line = False
								position_fleche_droit = (position_fleche_droit[0], position_fleche_droit[1] -difficulte)
								if position_fleche_droit[1] <= limite_px:
									position_fleche_droit = (160, 320)
									block_line = False  
								
							elif nombre =="B":#--------------------------------------------------------haut-bas
								
								position_fleche_haut = (position_fleche_haut[0], position_fleche_haut[1] -difficulte)
								if position_fleche_haut[1] <= limite_px:
									position_fleche_haut = (110, 320)
									block_line = False
								
								position_fleche_bas = (position_fleche_bas[0], position_fleche_bas[1] -difficulte)
								if position_fleche_bas[1] <= limite_px:
									position_fleche_bas = (60, 320)
									block_line = False  
								
							elif nombre =="C":#-------------------------------------------------------gauche-haut
								
								position_fleche_gauche = (position_fleche_gauche[0], position_fleche_gauche[1] -difficulte)
								if position_fleche_gauche[1] <= limite_px:
									position_fleche_gauche = (10, 320)
									block_line = False
									
								position_fleche_haut = (position_fleche_haut[0], position_fleche_haut[1] -difficulte)
								if position_fleche_haut[1] <= limite_px:
									position_fleche_haut = (110, 320)
									block_line = False
								
								
							elif nombre =="D":#------------------------------------------------------gauche-bas
								
								position_fleche_gauche = (position_fleche_gauche[0], position_fleche_gauche[1] -difficulte)
								if position_fleche_gauche[1] <= limite_px:
									position_fleche_gauche = (10, 320)
									block_line = False
								position_fleche_bas = (position_fleche_bas[0], position_fleche_bas[1] -difficulte)
								if position_fleche_bas[1] <= limite_px:
									position_fleche_bas = (60, 320)
									block_line = False  
								
								
							elif nombre =="E":#-----------------------------------------------------droite-haut
								
								position_fleche_droit = (position_fleche_droit[0], position_fleche_droit[1] -difficulte)
								if position_fleche_droit[1] <= limite_px:
									position_fleche_droit = (160, 320)
									block_line = False
								position_fleche_haut = (position_fleche_haut[0], position_fleche_haut[1] -difficulte)
								if position_fleche_haut[1] <= limite_px:
									position_fleche_haut = (110, 320)
									block_line = False  
									
							
							elif nombre =="F":#------------------------------------------------------droite-bas
								
								position_fleche_droit = (position_fleche_droit[0], position_fleche_droit[1] -difficulte)
								if position_fleche_droit[1] <= limite_px:
									position_fleche_droit = (160, 320)
									block_line = False
								position_fleche_bas = (position_fleche_bas[0], position_fleche_bas[1] -difficulte)
									
								if position_fleche_bas[1] <= limite_px:
									position_fleche_bas = (60, 320)
									block_line = False

								
							elif nombre== "7": #-----------------------------------------------------Toutes
								
								position_fleche_gauche = (position_fleche_gauche[0], position_fleche_gauche[1] -difficulte)
									
								if position_fleche_gauche[1] <= limite_px:
									position_fleche_gauche = (10, 320)
									block_line = False
								position_fleche_bas = (position_fleche_bas[0], position_fleche_bas[1] -difficulte)
									
								if position_fleche_bas[1] <= limite_px:
									position_fleche_bas = (60, 320)
									block_line = False
								position_fleche_haut = (position_fleche_haut[0], position_fleche_haut[1] -difficulte)
								if position_fleche_haut[1] <= limite_px:
									position_fleche_haut = (110, 320)
									block_line = False  
								position_fleche_droit = (position_fleche_droit[0], position_fleche_droit[1] -difficulte)
								if position_fleche_droit[1] <= limite_px:
									position_fleche_droit = (160, 320)
									block_line = False  
									stage=stage+1
								
							elif nombre == "X":
								position_a = (position_a[0], position_a[1] -difficulte)
									
								if position_a[1] <= limite_px:
									position_a = (210, 320)
									block_line = False
							
							elif nombre == "Y":
								position_b = (position_b[0], position_b[1] -difficulte)
									
								if position_b[1] <= limite_px:
									position_b = (260, 320)
									block_line = False
							
							elif nombre == "Z":
								position_b = (position_b[0], position_b[1] -difficulte)
									
								if position_b[1] <= limite_px:
									position_b = (260, 320)
									block_line = False
									
								position_a = (position_a[0], position_a[1] -difficulte)
								
								if position_a[1] <= limite_px:
									position_a = (210, 320)
									block_line = False

										
						else:
							index += 1
							block_line = True
							bad = 0
							
						old_temps = temps_actuel
						
					#---------------------------------------------------------------------- Verification d'actions au clavier
					limite_y1 = 65
					limite_y2 = 95
					
					for name in inputs:
						button = inputs[name][0]
					
						if GPIO.input(button) == False and inputs[name][1] == 0:
							inputs[name][1] = 1
							
							if name == "SELECT":
								pygame.mixer.music.stop()
								infinijeux=0
								infini=0
								infinimenu=1
								infinitot=1
								infinilvl=1
								pygame.mixer.pre_init()
								pygame.mixer.music.load("musique/musique_menu.mp3")
								pygame.mixer.music.play()
								break
							elif name == "GAUCHE":
								if  position_fleche_gauche[1] > limite_y1 and position_fleche_gauche[1] < limite_y2 :
									score=score+1
									bad = "good"
								else:
									if position_fleche_gauche[1] > limite_y2:
										bad = "tot"
									else:
										bad = "tard"
									score=score-1
							elif name == "BAS":
								if position_fleche_bas[1] > limite_y1 and position_fleche_bas[1] < limite_y2:
									score=score+1
									bad = "good"
								else:
									if position_fleche_bas[1] > limite_y2:
										bad = "tot"
									else:
										bad = "tard"
									score=score-1
							elif name == "HAUT":
								if position_fleche_haut[1] > limite_y1  and position_fleche_haut[1] < limite_y2:
									score=score+1
									bad = "good"
								else:
									score=score-1
									if position_fleche_haut[1] > limite_y2:
										bad = "tot"
									else:
										bad = "tard"
							elif name == "DROITE":
								if position_fleche_droit[1] > limite_y1 and position_fleche_droit[1] < limite_y2:
									score=score+1
									bad = "good"
								else:
									score=score-1
									if position_fleche_droit[1] > limite_y2:
										bad = "tot"
									else:
										bad = "tard"
							elif name == "A":
								if position_a[1] > limite_y1 and position_a[1] < limite_y2:
									score=score+1
									bad = "good"
								else:
									score=score-1
									if position_a[1] > limite_y2:
										bad = "tot"
									else:
										bad = "tard"
							elif name == "B":
								if position_b[1] > limite_y1 and position_b[1] < limite_y2:
									score=score+1
									bad = "good"
								else:
									score=score-1
									if position_b[1] > limite_y2:
										bad = "tot"
									else:
										bad = "tard"

							elif name == "START":
								# PAUSE
								pass
					
						elif GPIO.input(button) == True and inputs[name][1] == 1:
							inputs[name][1] = 0
								
					for event in pygame.event.get():
						if event.type == KEYDOWN:

							if event.key == K_LEFT :
								if  (10,85) > position_fleche_gauche < (10,75) :
									score=score+1
								else:
									score=score-1
								
							if event.key == K_DOWN :
								if (60,85) > position_fleche_bas < (60,75):
									score=score+1
								else:
									score=score-1
									
							if event.key == K_UP :
								if (110,85)> position_fleche_haut < (110,75):
									score=score+1
								else:
									score=score-1
									
							if event.key == K_RIGHT :
								if (160,85) > position_fleche_droit < (160,75):
									score=score+1
								else:
									score=score-1
							
							if event.key == K_a :
								if (210,85) > position_a < (210,75):
									score=score+1
								else:
									score=score-1
							
							if event.key == K_b :
								if (260,85) > position_b < (260,75):
									score=score+1
								else:
									score=score-1
									
							if event.key == K_ESCAPE : #---------------------------------- Quitter la partie
								date=(time.strftime('%d/%m/%y %H:%M',time.localtime())) 
								score_file = open("score.txt", "a")
								score_file.write(date)
								score_file.write("   ")
								score_file.write(str(score_difficulte))
								score_file.write("     ")
								score_file.write(str(score))
								score_file.write('\n')
								score_file.close()

								infinijeux=0
								infini=0
								infinimenu=1
								iniinitot=1
								infinilvl=1
								pygame.mixer.music.stop()
								pygame.mixer.pre_init()
								pygame.mixer.music.load("musique/musique_menu.mp3")
								pygame.mixer.music.play()

				#---------------------------------------------------------------------- affichage du score                          
					if score < 0 :
						score = 0
					else:
						pass
					text = font.render("Score : {}" .format(str(score)),True,(0,0,0))
					fenetre.blit(fond,(0,0))
				#---------------------------------------------------------------------- Timer tps actuel/ temps restant
				#----------- by  Sample Python/Pygame Programs Simpson College Computer Science
					fonttimer = pygame.font.SysFont("impact", 19)
					total_seconds = frame_count // frame_rate
					minutes = total_seconds // 60
					seconds = total_seconds % 60
					output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
					text = fonttimer.render(output_string, True,(0,0,0))
					fenetre.blit(text, [570, 18])
					total_seconds = start_time - (frame_count // frame_rate)
					if total_seconds < 0:
						total_seconds = 0
					minutes = total_seconds // 60
					seconds = total_seconds % 60
					output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
					text = fonttimer.render(output_string, True, (0,0,0))
					fenetre.blit(text, [670, 18])
					frame_count += 1
					clock.tick(60)

				#---------------------------------------------------------------------- Re-blit les fleche en dessous de la fenetre
					fenetre.blit(fleche_gauche,position_fleche_gauche)
					fenetre.blit(fleche_bas,position_fleche_bas)
					fenetre.blit(fleche_haut,position_fleche_haut)
					fenetre.blit(fleche_droit,position_fleche_droit)
					fenetre.blit(a,position_a)
					fenetre.blit(b,position_b)
				#---------------------------------------------------------------------- fleche_fixe
					fenetre.blit(fleche_gauche_inv,(10,80))     
					fenetre.blit(fleche_bas_inv,(60,80))
					fenetre.blit(fleche_haut_inv,(110,80))      
					fenetre.blit(fleche_droite_inv,(160,80))
					fenetre.blit(a_inv,(210,80))
					fenetre.blit(b_inv,(260,80))
				#---------------------------------------------------------------------- rafraichissement
					fond2 = pygame.image.load("image/bann_score.png").convert()
					fenetre.blit(fond2, (0,0))
					text = font.render("Score : {}" .format(str(score)),True,(0,0,0))
					fenetre.blit(text, (5,2))
					
					if bad == "tot":
						text2 = font.render("Trop tot !", True, (255,255,0))
					elif bad == "tard":
						text2 = font.render("Trop tard !", True, (255,0,0))
					elif bad == "good":
						text2 = font.render("Parfait !", True, (0,255,0))
					elif bad == 0:
						text2 = font.render("", True, (0,255,0))
					
					fenetre.blit(text2, (60, 210))
					
					pygame.display.update()
				
				
