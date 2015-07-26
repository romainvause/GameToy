#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gametoy_main.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

import pygame
from pygame.locals import *

import sys
import os.path as Path
import os as Os
import random
import RPi.GPIO as GPIO

from PyQt4 import QtGui
from PyQt4.QtCore import *

from gametoy_globals import *
	

class Graphical(QtGui.QWidget):
	def __init__(self, system):
		super(Graphical, self).__init__()
		
		self.system = system
		
		# Paramètres de la fenêtre
		self.setGeometry(320, 240, WINDOW_WIDTH, WINDOW_HEIGHT)
		self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.setMaximumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
		self.setWindowTitle("GameToy - Menu")
		
		self.games_folder = self.system.get_games_folder()
		self.nb_games = len(self.games_folder)
		
		# Gestion du menu
		self.level = 0
		self.pos = 0
		self.decal_y = 0
		self.items = []
		self.direct = ""
		
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
		self.connect_inputs()
		
		self.initUI()
		self.showFullScreen()
		self.show()
	
	def connect_inputs(self):
		for name in self.inputs:
			GPIO.add_event_detect(self.inputs[name][0], GPIO.RISING, callback=self.callback, bouncetime=200)
	
	def disconnect_inputs(self):
		for name in self.inputs:
			GPIO.remove_event_detect(self.inputs[name][0])
	
	def find_channel_name(self, channel):
		inputs = {
			17: "A",
			18: "B",
			
			27: "START",
			22: "SELECT",
			
			23: "BAS",
			24: "HAUT",
			25: "GAUCHE",
			21: "DROITE"
		}
		
		return inputs[channel]
	
	def callback(self, channel):
		func = self.find_channel_name(channel)
		
		if func == "BAS":
			print("DOWN")
			self.level += 1
			self.direct = "down"
		elif func == "HAUT":
			print("UP")
			self.level -= 1
			self.direct = "up"
		elif func == "A":
			if self.items[self.level][2][1]:
				self.disconnect_inputs()
				self.system.select_game(self.items[self.level][2][0])
				self.connect_inputs()
		
		self.refresh_menu()
	
	def keyPressEvent(self, e):
		self.direct = "none"
		
		if e.key() == Qt.Key_Down:
			self.level += 1
			self.direct = "down"
		elif e.key() == Qt.Key_Up:
			self.level -= 1
			self.direct = "up"
		elif e.key() == Qt.Key_Return:
			if self.items[self.level][2][1]:
				self.system.select_game(self.items[self.level][2][0])
		
		self.refresh_menu()
	
	def refresh_menu(self):
		if self.level > self.nb_games-1:
			self.level -= 1
			return 0
		if self.level < 0:
			self.level = 0
			return 0
		
		if self.direct == "down":
			if self.pos > 4:
				self.decal_y += 1
			
			if self.pos < 5:
				self.pos += 1
		
		elif self.direct == "up":
			if self.pos < 1:
				self.decal_y -= 1
				
			if self.pos > 0:
				self.pos -= 1
		
		self.refresh_games()
		
		selector_x = 260
		selector_y = 52 + (30 * self.pos)
		self.selector.move(selector_x, selector_y)
	
	def refresh_games(self):
		for i, item in enumerate(self.items):
			label_x = 10
			label_y = (57 + (30 * i)) - (30 * self.decal_y)
			image_x = 0
			image_y = (50 + (30 * i)) - (30 * self.decal_y)
			none_x = 4
			none_y = (53 + (30 * i)) - (30 * self.decal_y)
			
			item[0].move(image_x, image_y)
			item[1].move(label_x, label_y)
			item[3].move(none_x, none_y)
	
	def initUI(self):
		font = QtGui.QFont()
		font.setPointSize(15)
		font2 = QtGui.QFont()
		font2.setPointSize(7)
		
		self.refresh_games()
		
		for i, name_game in enumerate(self.games_folder):
			image = QtGui.QLabel(self)
			image.setPixmap(QtGui.QPixmap("item.png"))
			image.move(50, 50)
			
			label = QtGui.QLabel(self)
			label.setText("{}.    {}" .format(i+1, name_game[0].upper()))
			
			label_x = 10
			label_y = (57 + (30 * i)) - (30 * self.decal_y)
			image_x = 0
			image_y = (50 + (30 * i)) - (30 * self.decal_y)
			none_x = 4
			none_y = (53 + (30 * i)) - (30 * self.decal_y)
			
			if (name_game[1] == 0):
				none = QtGui.QLabel(self)
				none.setPixmap(QtGui.QPixmap("none.png"))
				none.move(none_x, none_y)
			else:
				none = QtGui.QLabel(self)
			
			label.move(label_x, label_y)
			image.move(image_x, image_y)
			
			self.items.append((image, label, name_game, none))
		
		if self.nb_games > 0:
			self.selector = QtGui.QLabel(self)
			self.selector.setPixmap(QtGui.QPixmap("selector.png"))
			self.selector.move(260, 52)
		
		header = QtGui.QLabel(self)
		header.setPixmap(QtGui.QPixmap("bann.png"))
		
		label = QtGui.QLabel(self)
		label.setFont(font2)
		label.setText("Nombre de jeux : {}" .format(self.nb_games))
		label.move(230, 2)

def delete_module(modname, paranoid=None):
	from sys import modules
	try:
		thismod = modules[modname]
	except KeyError:
		raise ValueError(modname)
	these_symbols = dir(thismod)
	if paranoid:
		try:
			paranoid[:]  # sequence support
		except:
			raise ValueError('must supply a finite list for paranoid')
		else:
			these_symbols = paranoid[:]
	del modules[modname]
	for mod in modules.values():
		try:
			delattr(mod, modname)
		except AttributeError:
			pass
		if paranoid:
			for symbol in these_symbols:
				if symbol[:2] == '__':  # ignore special symbols
					continue
				try:
					delattr(mod, symbol)
				except AttributeError:
					pass

class System(object):
	def __init__(self):
		"""Tente l'existence des dossiers et des chemins d'accès spécifiés dans le fichier de constantes"""
		self.path = GAME_PATH + SEP + GAME_FOLDER
		
		self.modules = sys.modules.keys()
		
	def check_existence(self):
		error = 0
		
		if not Path.exists(self.path) and not Path.isdir(self.path):
			error = 1
		
		self.error(error, perm_exit=True)
	
	def say(self, message, begin=">>", say=0):
		if say:
			print("{} {}" .format(begin, message))
	
	def error(self, error, perm_exit=False):
		if error > 0:
			self.say("Erreur gt-{} :\n\t{}" .format(error, ERRORS[error]))
			
			if perm_exit:
				exit(error)

	def get_games_folder(self):
		self.games_folder = []
		games_folder = Os.listdir(self.path)
		number_folder = len(games_folder)
		
		if number_folder > 0:
			self.say("Nombre de dossier compatible trouve dans le repertoire \"{}\" : {}" .format(GAME_FOLDER, number_folder))
			
			for i, folder in enumerate(games_folder):
				can_be_lunched = True
				
				self.say("{}" .format(folder), begin="-"*3)
				
				main_file_path = self.path+SEP+folder+SEP+MAIN_FILE_GAME
				self.say("Tentative d'existence du fichier {}" .format(main_file_path), begin="-"*5)
				if Path.isfile(main_file_path):
					self.say("Fichier {} trouve" .format(MAIN_FILE_GAME), begin="-"*8)
				else:
					self.say("Fichier {} non-trouve" .format(MAIN_FILE_GAME), begin="!"*8)
					can_be_lunched = False
					
				if not can_be_lunched:
					self.say("Le jeu ne peut pas etre lance", begin="!"*5)
					self.games_folder.append((folder, 0))
				else:
					self.say("Le jeu peut etre lance", begin="-"*5)
					self.games_folder.append((folder, 1))
					
				print("\n")				
		else:
			self.say("Aucun dossier trouvé")
		
		return self.games_folder		
	
	def select_game(self, name_choiced):
		# Generate name and path for launching game
		folder_to_launch = "{}{}{}{}{}" .format(GAME_PATH, SEP, GAME_FOLDER, SEP, name_choiced)
		file_to_launch = "{}{}{}" .format(folder_to_launch, SEP, MAIN_FILE_GAME)
		
		# Adding relative path of the game to the main program
		Os.chdir(folder_to_launch)
		sys.path.append(folder_to_launch)
		
		self.launch_game()
		
	def launch_game(self):
		import main
		reload(main)
		
		pygame.init()
		m = main.Master()
		
		pygame.quit()
		self.refresh_modules()
	
	def refresh_modules(self):
		new_modules = list(set(sys.modules.keys()) - set(self.modules))
		for i in new_modules:
			delete_module(i)
			
		sys.path = []
	
def main():
	#~ _sys = System()
	#~ _sys.check_existence()
	#~ _sys.get_games_folder()
	#~ _sys.say("Nombre de jeux compatibles : {}" .format(len(_sys.games_folder)))
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	
	app = QtGui.QApplication(sys.argv)
	m = Graphical(System())
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
