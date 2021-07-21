import os
import sys
from time import sleep
from dotenv import load_dotenv
from pathlib import Path
import math

load_dotenv(Path('../.env'))
sys.path.append(os.environ.get('CLASS_FOLDER_PATH'))
sys.path.append(os.environ.get('ROOT_FOLDER_PATH'))
from SpotifyClient import SpotifyClient
from YouTubeClient import YouTubeClient
from DBClient import DBClient
from helpers import *

def printMessage(string):
	print("Message: ", string)

def clearScreen():
	os.system('clear')

def displayTitle():
	clearScreen()
	print("\t\t**********************************************")
	print("\t\t*******  Welcome - Harambe and friends *******")
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

def printYoutubePlaylists():
	dotenv_path = Path('../.env')
	load_dotenv()
	yt = YouTubeClient(os.environ.get('GOOGLE_API_KEY'), os.environ.get('PL_ID'))
	playlists = yt.getPlaylists()
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
	RUNNING = True
	while RUNNING:
		if (currentItem + 1) >= len(ls):
			printRow(ls[currentItem], None)
		else:
			printRow(ls[currentItem], ls[currentItem + 1])
		currentItem = currentItem + 2
		if(currentItem >= lastItem):
			choice = ''			
			print("\n\n")
			print(f"\t\t\t\tPage: {currentPage}/{numberOfPages}")
			print("[P]:\tPrevious")
			print("[N]:\tNext")
			print("[B]:\tQuit")
			while True:
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
					displayTitle()
					print()
					break
				elif choice == 'n':
					currentPage = currentPage + 1
					if currentPage > numberOfPages:
						currentPage = numberOfPages
					firstItem = (currentPage - 1) * itemsPerPage
					lastItem = (currentPage * itemsPerPage) - 1
					if lastItem > len(ls) - 1:
						lastItem = len(ls) - 1
					currentItem = firstItem
					displayTitle()
					print()
					break
				elif choice == 'b':
					RUNNING = False
					break

def printSelectList(ls):
	itemsPerPage = 6
	numberOfPages = math.ceil(len(ls) / itemsPerPage)
	currentPage = 1
	firstItemIndex = (currentPage - 1) * itemsPerPage
	lastItemIndex = (currentPage * itemsPerPage) - 1
	if lastItemIndex > len(ls) - 1:
		lastItemIndex = len(ls) - 1
	currentItemIndex = firstItemIndex
	print()
	RUNNING = True
	while RUNNING:
		if (currentItemIndex + 1) >= len(ls):
			printRowWithIndex(ls[currentItemIndex], None, currentItemIndex)
		else:
			printRowWithIndex(ls[currentItemIndex], ls[currentItemIndex + 1], currentItemIndex)
		currentItemIndex += 2
		if(currentItemIndex >= lastItemIndex):
			choice = ''
			print("\n\n")
			print(f"\t\t\t\tPage: {currentPage}/{numberOfPages}")
			print("[p]:\tPrevious Page")
			print("[n]:\tNext Page")
			print("Select playlist number.")
			while True:
				choice = input("Input: ")
				if choice == 'p':
					currentPage = currentPage - 1
					if currentPage <= 0:
						currentPage = 1
					firstItemIndex = (currentPage - 1) * itemsPerPage
					lastItemIndex = (currentPage * itemsPerPage) - 1
					if lastItemIndex > len(ls) - 1:
						lastItemIndex = len(ls) - 1
					currentItemIndex = firstItemIndex
					displayTitle()
					print()
					break
				elif choice == 'n':
					currentPage = currentPage + 1
					if currentPage > numberOfPages:
						currentPage = numberOfPages
					firstItem = (currentPage - 1) * itemsPerPage
					lastItem = (currentPage * itemsPerPage) - 1
					if lastItem > len(ls) - 1:
						lastItem = len(ls) - 1
					currentItem = firstItem
					displayTitle()
					print()
					break
				elif choice.isnumeric():
					number = int(choice)
					maxIndex = len(ls)
					if number < 0 or number >= maxIndex:
						continue
					return number



def printRow(item1, item2):
	print("\t****************************************************************")
	print("\t\t", item1, "\t\t\t", item2)
	print("\t****************************************************************")
	print()


def printRowWithIndex(item1, item2, firstItemIndex):
	if item2 is not None:
		print("\t****************************************************************")
		print("\t\t", f"[{firstItemIndex}]{item1}", "\t\t\t", f"[{firstItemIndex+1}]{item2}")
		print("\t****************************************************************")
	else:
		print("\t****************************************************************")
		print("\t\t", f"[{firstItemIndex}]{item1}", "\t\t\t", item2)
		print("\t****************************************************************")		


#TODO: Create database to store linked playlist information
def linkPlaylists():
	#get youtube playlist stuff
	yt = YouTubeClient(os.environ.get("GOOGLE_API_KEY"), os.environ.get("PL_ID"))
	yt_lists = yt.getPlaylists()
	yt_titles = []
	for item in yt_lists:
		yt_titles.append(item[0])
	printSelectList(yt_titles)
	return
	link = (yt_name, yt_id, sp_name, sp_id)
	dbClient = DBClient()
	dbClient.insertLink(link)



#TODO: Display linked playlists form the sqldatabase
def printLinkedPlaylists():
	print("Printing linked playlists")
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
