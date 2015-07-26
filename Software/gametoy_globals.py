#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gametoy_globals.py
#  
#  Copyright 2015 Romain <Romain@ROMAIN-POR>

# Fenêtre
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240

# Dossier
SEP = "/"

GAME_FOLDER = "gametoy_games"
_GAME_FOLDER = GAME_FOLDER + SEP
GAME_PATH = "/media/GAMETOY"
_GAME_PATH = GAME_PATH + SEP

CONF_PATH = "settings"

# FICHIER
CONF_NAMEFILE = "conf.gtconf"
MAIN_FILE_GAME = "main.py"


# Erreurs
ERRORS = {1: "Le dossier de jeux \"{}\" est introuvable a l'endroit \"{}\"" .format(GAME_FOLDER, _GAME_PATH)}
