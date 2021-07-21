import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path("../.env"))

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
