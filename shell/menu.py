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
from PlaylistSyncer import PlaylistSyncer

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
	print("[s]:\tSynchronize Playlists")
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
					firstItemIndex = (currentPage - 1) * itemsPerPage
					lastItemIndex = (currentPage * itemsPerPage) - 1
					if lastItemIndex > len(ls) - 1:
						lastItemIndex = len(ls) - 1
					currentItemIndex = firstItemIndex
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


def linkPlaylists():
	#get youtube playlist stuff
	yt = YouTubeClient(os.environ.get("GOOGLE_API_KEY"), os.environ.get("PL_ID"))
	yt_lists = yt.getPlaylists()
	yt_titles = []
	for item in yt_lists:
		yt_titles.append(item[0])
	selected_index = printSelectList(yt_titles)
	selected_yt = yt_lists[selected_index]

	#get spotify playlist stuff
	sp = SpotifyClient(os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_SECRET"))
	if(not tokenIsFresh()):
		refreshAccessToken()

	#Wipe screen here
	displayTitle()
	sp_lists = sp.getPlaylists()
	sp_titles = []
	for item in sp_lists:
		sp_titles.append(item[0])
	selected_index = printSelectList(sp_titles)
	selected_sp = sp_lists[selected_index]

	link = (selected_yt[0], selected_yt[1], selected_sp[0], selected_sp[1])

	dbClient = DBClient()
	dbClient.insertLink(link)
	sleep(3)
	dbClient.showLinks()
	print("Dumping")
	sleep(5)


def printLinkedPlaylists():
	dbClient = DBClient()
	displayTitle()
	print()
	all_links = dbClient.showLinks()
	printList(all_links)


def synchronizePlaylists():
	#make sure spotify tokens are up to date
	if(not tokenIsFresh()):
		refreshAccessToken()
	spotify = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
	youtube = YouTubeClient(os.environ.get('GOOGLE_API_KEY'), os.environ.get('PL_ID'))
	ps = PlaylistSyncer()
	dbClient = DBClient()
	#get playlists to synchronize
	links = dbClient.getLinks()

	for link in links:
		yt_id = link[0]
		sp_id = link[1]
		#get youtube songs for playlist
		yt_songs = youtube.getPlaylistItems(yt_id)
		delta = dbClient.getTrackDifferences(yt_id, sp_id, yt_songs)
		print("Delta: ", delta)
		sleep(2)
		if delta:
			#make sure it's inserting to correct ps of id: sp_id
			processed = spotify.insertSongs(delta, sp_id)
			print("Processed: ", processed)
			sleep(2)
			if delta:
				dbClient.addTracksToLocal(yt_id, sp_id, delta)



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
	elif choice == 's':
		synchronizePlaylists()
	elif choice == 'q':
		clearScreen()
