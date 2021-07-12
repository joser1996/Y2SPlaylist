import os
import sys
from time import sleep
from dotenv import load_dotenv
from pathlib import Path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from SpotifyClient import SpotifyClient
from helpers import *
def printMessage(string):
	print("Message: ", string)

def clearScreen():
	os.system('clear')

def displayTitle():
	clearScreen()
	print("\t\t**********************************************")
	print("\t\t***  Welcome - Harambe and friends ***********")
	print("\t\t**********************************************")

def displayPrompts():
	print("\n[1]:\tSee Spotify playlists")
	print("[2]:\tSee YouTube playlists")
	print("[3]:\tLink playlists")
	print("[4]:\tSee Linked playlists")
	print("[q]:\tQuit")

def printSpotifyPlaylists():
	if not tokenIsFresh():
		refreshAccessToken()
	dotenv_path = Path('../.env')
	load_dotenv(dotenv_path=dotenv_path)
	sp = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
	sp.getPlaylists()
	sp.printPlaylists()

def processChoice(choice):
	if choice == '1':
		printSpotifyPlaylists()
	elif choice == '2':
		printYoutubePlaylists()
	elif choice == '3':
		linkPlaylists()
	elif choice == '4':
		printLinkedPlaylists()
