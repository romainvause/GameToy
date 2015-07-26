#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fonctions.py
#  
#  Copyright 2014 Romain <Romain@ROMAIN-PC>

from random import randrange

def generate_line(largeur, hauteur, min_hauteur, max_hauteur, lst2=None):
	"""Génètre un trajet aléatoirement"""
	lst = []
	
	# Position de la ligne
	x = 0
	y = (max_hauteur + min_hauteur) // 2
	
	# Booléans de test
	blocked  = False
	on_ampli = False
	on_line  = False
	on_obs   = False
	can_obs  = True
	
	# Écart entre les différents obstacle
	ecart = 0
	l_obs = 0 # Longueur d'obstacle
	
	# Variable de droite
	h = 0 # Hauteur droite
	l = 0 # Longueur droite
	
	g = "white"
	
	sens = "+"
	
	for i in range(largeur):
		lst.append([x,y,g,0])
		if (not on_obs and x > 500 and x > ecart+randrange(100,1000)):
			if (randrange(0,10) == 0):
				if (lst2 != None):
					l_obs = randrange(x+20, x+51)
					pure_l_obs = l_obs - x
					
					can_obs = True
					
					tmp = lst2[x-20-pure_l_obs:x]
					for i in tmp:
						if ("red" in i):
							can_obs = False
					tmp = lst2[x:x+20+pure_l_obs]
					for i in tmp:
						if ("red" in i):
							can_obs = False
					
					if (can_obs):
						on_obs = True
						g = "red"
					
				elif (lst2 == None):
					g = "red"
					l_obs = randrange(x+20, x+51)
					on_obs = True

		elif (on_obs):
			if (x > l_obs):
				g = "white"
				on_obs = False
				ecart = x
		
		if (not on_ampli):
			if (on_line):
				if (x > l):
					on_line = False
				else:
					sens = "="
			else:
				h = randrange(min_hauteur, max_hauteur+1)
				on_ampli = True
				
		if (on_ampli):
			if (y > h):
				sens = "-"
			elif (y < h):
				sens = "+"
			if (y == h):
				on_ampli = False
				on_line = True
				l = randrange(x+5, x+51)
				h = 0
			
		
		if (y == (hauteur//2)):
			blocked = False
			on_ampli = False
		
		if (y >= max_hauteur and not blocked):
			sens = "-"
			blocked = True
		elif (y <= min_hauteur and not blocked):
			sens = "+"
			blocked = True
		
		
		if (sens == "+"):
			y+=1
		elif (sens == "-"):
			y-=1
		elif (sens == "="):
			y=y
		x+=1
		
	return lst
	
def genere_line_droite():
	"""Génère une ligne droite pour l'écran d'accueil"""
	longueur = randrange(40,120)
	#~ longueur = 120
	y = randrange(0, 241)
	nb = randrange(0, 2)
	if nb:
		cote = "left"
	else:
		cote = "right"
	
	color = (randrange(0,256), randrange(0,256), randrange(0,256))
	width = randrange(1, 7)
	
	return [longueur, y, cote, 0, False, color, width]

def render_score(score):
	"""Transformation du score (136 -> 000136)"""
	if len(str(score)) > 0 and len(str(score)) < 7:
		return "0"*(6-len(str(score))) + str(score)
	else:
		return "999999"

if __name__ == "__main__":
	generate_line(320, 240, 40, 200)
	print(render_score(147))
