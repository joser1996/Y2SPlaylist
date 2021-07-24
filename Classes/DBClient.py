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

	def insertLink(self, link):
		query = """
		INSERT INTO links
		(yt_playlist_name, yt_playlist_id, sp_playlist_name, sp_playlist_id)
		VALUES (%s, %s, %s, %s);
		"""
		cursor = self.db.cursor()
		try:
			cursor.execute(query, link)
			print("Inserting Link: ", link)
		except self.db.connector.Error as err:
			print("Error Number: ", err.errno)
			print("Error Message: ", err.msg)
			print("Error: ", err)
		print("Done inserting")
		self.db.commit()
		cursor.close()

	def showLinks(self):
		query = """
		SELECT * FROM links;
		"""
		cursor = self.db.cursor()
		try:

			cursor.execute(query)
		except self.db.connector.Error as err:
			print("Error Number: ", err.errno)
			print("Error Message: ", err.msg)
			print("Error: ", err)

		pairs = []		
		for (row_id, yt_playlist_name, yt_playlist_id, sp_playlist_name, sp_playlist_id) in cursor:
			# print("\tYT_Playlist: {}\t ID: {}".format(yt_playlist_name, yt_playlist_id))
			# print("\tSP_Playlist: {}\t ID: {}".format(sp_playlist_name, sp_playlist_id))
			# print("\n")
			pairs.append((yt_playlist_name, sp_playlist_name))
		cursor.close()
		return pairs

	def getLinks(self):
		query = """
		SELECT * FROM links;
		"""
		cursor = self.db.cursor()
		try:
			cursor.execute(query)
		except self.db.connector.Error as err:
			print("Error Number: ", err.errno)
			print("Error Message: ", err.msg)
			print("Error: ", err)
		links = []
		for(row_id, yt_playlist_name, yt_playlist_id, sp_playlist_name, sp_playlist_id) in cursor:
			links.append((yt_playlist_id, sp_playlist_id))
		cursor.close()
		return links


	def getLinkId(self, yt_pl_id,sp_pl_id):
		getIdQuery = """
		SELECT id FROM links WHERE yt_playlist_id = %s AND sp_playlist_id = %s 
		"""
		cursor = self.db.cursor()
		try:
			cursor.execute(getIdQuery, (yt_pl_id, sp_pl_id))
		except self.db.connector.Error as err:
			print("Error Number: ", err.errno)
			print("Error Message: ", err.msg)
			print("Error: ", err)
		lid = None
		for (link_id) in cursor:
			lid = link_id
			break
		cursor.close()
		return lid

	def getTrackDifferences(self, yt_pl_id, sp_pl_id, yt_songs):
		#first get link id using playlist ids
		link_id = self.getLinkId(yt_pl_id, sp_pl_id)
		print("Link ID found: ", link_id)
		sleep(2)

		#get tracks that have already been processed
		query = """
		SELECT track_name, track_uri FROM processed_tracks WHERE link_id = %s;
		"""
		cursor = self.db.cursor()
		try:
			cursor.execute(query, (link_id))
		except self.db.connector.Error as err:
			print("Error Number: ", err.errno)
			print("Error Message: ", err.msg)
			print("Error: ", err)

		processed_tracks = []
		for (track_name, track_uri) in cursor:
			processed_tracks.append(track_name)
		print("Processed Tracks in diff: ", processed_tracks)
		differences = list(set(yt_songs) - set(processed_tracks))
		print("Differences: ", differences)
		sleep(2)
		return differences


	def addTracksToLocal(self, yt_pl_id, sp_pl_id, processed):
		link_id = self.getLinkId(yt_pl_id, sp_pl_id)
		query = """
		INSERT INTO processed_tracks (link_id, track_name, track_uri) VALUES (%s, %s, %s);
		"""
		values = []
		for each in processed:
			values.append((link_id[0], each, "NA"))
		print("Values to insert: ", values)
		sleep(2)
		cursor = self.db.cursor()
		try:
			cursor.executemany(query, values)
			self.db.commit()
			print(cursor.rowcount, " was inserted")
		except self.db.connector.Error as err:
			print("Error Number: ", err.errno)
			print("Error Message: ", err.msg)
			print("Error: ", err)		
		cursor.close()


# CREATE TABLE processed_tracks(
# 	id INT NOT NULL AUTO_INCREMENT,
# 	link_id INT NOT NULL,
# 	track_name TEXT NOT NULL,
# 	track_uri TEXT NOT NULL, 
# 	PRIMARY KEY(id)
# );
