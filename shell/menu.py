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
	sleep(2)

def displayTitle():
	os.system('clear')
	print("\t\t**********************************************")
	print("\t\t*******  Welcome - Harambe and friends *******")
	print("\t\t**********************************************")

def displaySubTitle(subTitle):
	print(f"\t\t\t\t{subTitle}")


def displayPrompts():
	print("\n[1]:\tSee Spotify playlists")
	print("[2]:\tSee YouTube playlists")
	print("[3]:\tLink playlists")
	print("[4]:\tSee Linked playlists")
	print("[5]:\tEdit Playlists")
	print("[s]:\tSynchronize Playlists")
	print("[q]:\tQuit")

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
	elif choice == '5':
		editPlaylists()
	elif choice == 's':
		synchronizePlaylists()
	elif choice == 'q':
		os.system('clear')


def deleteSPPlaylist():
	spotify = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
	playlists = spotify.getPlaylists()
	titles = []
	for playlist in playlists:
		titles.append(playlist[0])

	titleIndex = printSelectList(titles)
	msg = f"Playlist: {titles[titleIndex]} will be deleted"
	delayedMessage(msg)
	playlistToDelete = playlists[titleIndex]
	spotify.deletePlaylist(playlistToDelete[1])
	delayedMessage("Deleted")
	return True

def createSPPlaylist():
	spotify = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
	# get playlist name from user
	playlistName = None
	desc = None
	while not playlistName:
		playlistName = input("Enter playlist name:\t")

	desc = input("Enter a short description:\t")

	string = f"Creating playlist: {playlistName}"
	delayedMessage(string)
	spotify.createPlaylist(playlistName, desc)
	delayedMessage("Done")
	return True

def editPrompts():
	displayTitle()
	print("[1]\tDelete Playlist")
	print("[2]\tCreate Playlist")
	print("[3]\tDisplay Playlists")
	print("[r]\tReturn")	

def editSpotifyPlaylists():
	editPrompts()
	DONE = False
	while not DONE:
		choice = input("Input: ")
		if choice == "1":
			DONE = deleteSPPlaylist()
			editPrompts()
		elif choice == "2":
			DONE = createSPPlaylist()
			editPrompts()
		elif choice == "3":
			displayTitle()
			printSpotifyPlaylists()
			print("Returned to edit sp")
			sleep(2)
			DONE = True
		elif choice == "r":
			return True

def deleteYTPlaylist():
	print("in deleteYTPlaylist")
	sleep(2)
	return True

def createYTPlaylist():
	print("In createYTPlaylist")
	sleep(2)
	return True

def delayedMessage(msg):
	print(msg)
	sleep(2)

def editYouTubePlaylists():
	editPrompts()
	DONE = False
	while not DONE:
		choice = input("Input: ")
		if choice == "1":
			DONE = deleteYTPlaylist()
		elif choice == "2":
			DONE = createYTPlaylist()
		elif choice == "3":
			displayTitle()
			printYoutubePlaylists()
			print("Returned to edit yt")
			sleep(2)
			DONE = True
		elif choice == "r":
			return True
	return True

def editPlaylists():
	displayTitle()
	print("[1]\tEdit YouTube playlists.")
	print("[2]\tEdit Spotify playlists.")
	print("[r]\tReturn")
	DONE = False
	while not DONE:
		choice = input("Input: ")
		if choice == '1':
			DONE = editYouTubePlaylists()
		elif choice == '2':
			DONE = editSpotifyPlaylists()
		elif choice == 'r':
			return

def printSpotifyPlaylists():
	if not tokenIsFresh():
		refreshAccessToken()
	sp = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
	playlist_items = sp.getPlaylists()
	playlist_titles = []
	for item in playlist_items:
		playlist_titles.append(item[0])
	printList(playlist_titles)

def printYoutubePlaylists():
	yt = YouTubeClient(os.environ.get('GOOGLE_API_KEY'))
	playlist_tupples = yt.getPlaylists()
	playlist_titles = []
	for tup in playlist_tupples:
		playlist_titles.append(tup[0])
	printList(playlist_titles)

def printList(ls):
	if(len(ls) == 0):
		msg = "No Items to show"
		ls.append(msg)
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
			print("[B]:\tReturn to previous menu")
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
	if(len(ls) == 0):
		msg = "No Items to show"
		ls.append(msg)
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
	if not item2:
		item2 = ""
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
	yt = YouTubeClient(os.environ.get("GOOGLE_API_KEY"))
	yt_lists = yt.getPlaylists()
	yt_titles = []
	for item in yt_lists:
		yt_titles.append(item[0])
	displaySubTitle("Youtube Playlists")
	selected_index = printSelectList(yt_titles)
	selected_yt = yt_lists[selected_index]

	#get spotify playlist stuff
	sp = SpotifyClient(os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_SECRET"))
	if(not tokenIsFresh()):
		refreshAccessToken()

	#Wipe screen here
	displayTitle()
	displaySubTitle("Spotify Playlists")
	sp_lists = sp.getPlaylists()
	sp_titles = []
	for item in sp_lists:
		sp_titles.append(item[0])
	selected_index = printSelectList(sp_titles)
	selected_sp = sp_lists[selected_index]

	link = (selected_yt[0], selected_yt[1], selected_sp[0], selected_sp[1])

	dbClient = DBClient()
	dbClient.insertLink(link)

def printLinkedPlaylists():
	dbClient = DBClient()
	displayTitle()
	print()
	all_links = dbClient.getLinks()
	links = []
	for key in all_links:
		link = all_links[key]
		string = link[0] + " <----> " + link[2]
		links.append(string)
	printList(links)

def synchronizePlaylists():
	#make sure spotify tokens are up to date
	if(not tokenIsFresh()):
		refreshAccessToken()
	spotify = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
	youtube = YouTubeClient(os.environ.get('GOOGLE_API_KEY'))
	dbClient = DBClient()
	#get playlists to synchronize
	results = dbClient.getLinks()
	print("Synchronizing")
	for key in results:
		link = results[key]
		yt_id = link[1]
		sp_id = link[3]
		print(f"Syncing Link: Id:{key} {link[0]} <----> {link[2]}")
		sleep(2)
		#get youtube songs for playlist
		yt_songs = youtube.getPlaylistItems(yt_id)
		delta = dbClient.getTrackDifferences(yt_id, sp_id, yt_songs)
		#IF None is returned
		if not delta:
			return 
		if delta:
			#make sure it's inserting to correct ps of id: sp_id
			processed_tracks = spotify.insertSongs(delta, sp_id)
			if processed_tracks:
				dbClient.addTracksToLocal(yt_id, sp_id, processed_tracks)
	
