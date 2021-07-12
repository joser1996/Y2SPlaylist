import os
import sys
from time import sleep
from dotenv import load_dotenv
from pathlib import Path
import math
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
	playlists = sp.getPlaylists()
	printList(playlists)

def printList(ls):
	itemsPerPage = 6
	numberOfPages = math.ceil(len(ls) / itemsPerPage)
	currentPage = 1
	firstItem = (currentPage - 1) * itemsPerPage
	lastItem = (currentPage * itemsPerPage) - 1
	if lastItem > len(ls) - 1:
		lastItem = len(ls) - 1
	currentItem = firstItem
	print()
	while currentPage <= numberOfPages:
		if (currentItem + 1) >= len(ls):
			printRow(ls[currentItem], None)
		else:
			printRow(ls[currentItem], ls[currentItem + 1])
		currentItem = currentItem + 2
		if(currentItem >= lastItem):
			choice = ''			
			print("\n\n")
			print("[P]:\tPrevious")
			print("[N]:\tNext")
			print("[Q]:\tQuit")
			choice = input("What?")
			if choice == 'p':
				currentPage = currentPage - 1
				if currentPage <= 0:
					currentPage = 1
				firstItem = (currentPage - 1) * itemsPerPage
				lastItem = (currentPage * itemsPerPage) - 1
				if lastItem > len(ls) - 1:
					lastItem = len(ls) - 1
				currentItem = firstItem
			elif choice == 'n':
				currentPage = currentPage + 1
				firstItem = (currentPage - 1) * itemsPerPage
				lastItem = (currentPage * itemsPerPage) - 1
				if lastItem > len(ls) - 1:
					lastItem = len(ls) - 1
				currentItem = firstItem
			elif choice == 'q':
				break
			displayTitle()
			print()


def printRow(item1, item2):
	print("\t****************************************************************")
	print("\t\t", item1, "\t\t\t", item2)
	print("\t****************************************************************")
	print()

def processChoice(choice):
	displayTitle()
	if choice == '1':
		printSpotifyPlaylists()
	elif choice == '2':
		printYoutubePlaylists()
	elif choice == '3':
		linkPlaylists()
	elif choice == '4':
		printLinkedPlaylists()
	elif choice == 'q':
		clearScreen()
