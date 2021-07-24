from googleapiclient.discovery import build
import json
import sys
import os
from dotenv import load_dotenv
import json

class YouTubeClient:
    def __init__(self, key, playlistID):
        self.youtube = build('youtube', 'v3', developerKey=key)

    #returns list of track names in plalist with id: playlistID
    def getPlaylistItems(self, playlistID):
        try:
            nextPageToken = None
            # an array of arrays potentially
            songs = [] 
            while True:
                request = self.youtube.playlistItems().list(
                    part='contentDetails, snippet',
                    playlistId=playlistID,
                    maxResults=50,
                    pageToken=nextPageToken
                )
                response = request.execute()

                # get playlist song titles in response(extract them)
                array = self.extractPlaylistSongs(response)
                for title in array:
                    songs.append(title)
                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    return songs
        except:
            e = sys.exc_info()[0]
            print("Oops something went wrong")
            print(e)

    #Used to extract song titles
    def extractPlaylistSongs(self, pl):
        items = pl["items"]
        songs = []
        for item in items:
            songTitle = item["snippet"]["title"]
            songs.append(songTitle)
        return songs

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
                    title = item['snippet']['title']
                    plId = item['id']
                    ls.append((title, plId))
                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    return ls
            
        except:
            e = sys.exc_info()[0]
            print(e)
            print("Something went wrong")