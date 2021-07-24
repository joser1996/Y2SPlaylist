import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path("../.env"))
from time import sleep

class DBClient:
	def __init__(self):
		try:
			self.db = mysql.connector.connect(
				host="localhost",
				user="root",
				password=os.environ.get('DB_PASSWORD'),
				database="YTS_DATABASE"
			)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something is wrong with the username or password")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database doesn't exist")
			else:
				print(err)

	def processSQLError(self, err):
		print("Error Number: ", err.errno)
		print("Error Message: ", err.msg)
		print("Error: ", err)

	def insertLink(self, link):
		query = """
		INSERT INTO links
		(yt_playlist_name, yt_playlist_id, sp_playlist_name, sp_playlist_id)
		VALUES (%s, %s, %s, %s);
		"""
		cursor = self.db.cursor()
		try:
			cursor.execute(query, link)
		except self.db.connector.Error as err:
			self.processSQLError(err)
		self.db.commit()
		cursor.close()

	def getLinks(self):
		query = "SELECT * FROM links;"
		cursor = self.db.cursor()
		try:
			cursor.execute(query)
		except self.db.connector.Error as err:
			self.processSQLError(err)
		links = {}
		for(link_id, yt_name, yt_id, sp_name, sp_id) in cursor:
			links[link_id] = (yt_name, yt_id, sp_name, sp_id)

		cursor.close()
		return links

	def getLinkId(self, yt_pl_id,sp_pl_id):
		getIdQuery = "SELECT id FROM links WHERE yt_playlist_id = %s AND sp_playlist_id = %s;"
		cursor = self.db.cursor()
		try:
			cursor.execute(getIdQuery, (yt_pl_id, sp_pl_id))
		except self.db.connector.Error as err:
			self.processSQLError(err)
		lid = None
		if not cursor.rowcount:
			print("No results found for linkID")
			return lid
		for (link_id) in cursor:
			lid = link_id
			break
		cursor.close()
		return lid[0]

	#returns list of track names to be proccessed(YT Songs) else returns None
	def getTrackDifferences(self, yt_pl_id, sp_pl_id, yt_songs):
		link_id = self.getLinkId(yt_pl_id, sp_pl_id)
		if not link_id:
			print(f"No Link was found.")
			sleep(2)
			return None

		#get tracks that have already been processed
		query = "SELECT track_name FROM processed_tracks WHERE link_id = %s;"
		cursor = self.db.cursor()
		try:
			cursor.execute(query, (link_id))
		except self.db.connector.Error as err:
			self.processSQLError(err)
		processed_titles = []
		for (track_name) in cursor:
			processed_titles.append(track_name)
		songsToAdd = list(set(yt_songs) - set(processed_titles))
		return songsToAdd

	#processed has key:value pairs where key=uri, value = track name
	def addTracksToLocal(self, yt_pl_id, sp_pl_id, addedTracks):
		link_id = self.getLinkId(yt_pl_id, sp_pl_id)
		query = "INSERT INTO processed_tracks (link_id, track_name, track_uri) VALUES (%s, %s, %s);"
		values = []
		for uri in processed:
			track_name = processed[uri]
			values.append((link_id, track_name, uri))

		cursor = self.db.cursor()
		try:
			cursor.executemany(query, values)
			self.db.commit()
			print(cursor.rowcount, " was inserted")
			sleep(2)
		except self.db.connector.Error as err:
			self.processSQLError(err)
		cursor.close()

