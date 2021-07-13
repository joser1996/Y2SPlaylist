from googleapiclient.discovery import build
import json
import sys
import os
from dotenv import load_dotenv
import json
#Print available playlists
#show playlist ids
#Need to authorize requsets for google
class YouTubeClient:
    def __init__(self, key, playlistID):
        self.key = key
        #playlist we get songs from
        self.playlistID = playlistID
        self.youtube = build('youtube', 'v3', developerKey=key)
        self.playlist = []
        self.songs = []
    # gets all track names for songs in playlist with playlistID
    def getPlaylistItems(self):
        try:
            nextPageToken = None
            while True:
                request = self.youtube.playlistItems().list(
                    part='contentDetails, snippet',
                    playlistId=self.playlistID,
                    maxResults=50,
                    pageToken=nextPageToken
                )
                response = request.execute()
                self.playlist = response

                # get playlist songs
                self.getPlaylistSongs()

                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    break
        except:
            e = sys.exc_info()[0]
            print("Oops something went wrong")
            print(e)

    #Used to extract song titles
    def getPlaylistSongs(self):
        items = self.playlist["items"]
        for item in items:
            songTitle = item["snippet"]["title"]
            self.songs.append(songTitle)

    def printPlaylistItems(self):
        for song in self.songs:
            print(song)

    def printPlaylist(self):
        print(json.dumps(self.playlist, indent=2))
    
    def getPlaylists(self):
        try:
            nextPageToken = None
            ls = []
            while True:            
                request = self.youtube.playlists().list(
                    part='snippet, id',
                    pageToken=nextPageToken,
                    channelId=os.environ.get('YOUTUBE_CHANNEL_ID')
                )
                response = request.execute()                
                items = response['items']
                for item in items:
                    #print("Title: ", item['snippet']['title'])
                    ls.append(item['snippet']['title'])
                    #print("ID: ", item['id'])
                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    break
            return ls
        except:
            e = sys.exc_info()[0]
            print(e)
            print("Something went wrong")