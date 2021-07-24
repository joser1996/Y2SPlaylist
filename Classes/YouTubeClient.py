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
        self.youtube = build('youtube', 'v3', developerKey=key)
        self.playlist = []
        self.songs = []
    # gets all track names for songs in playlist with playlistID
    # do i have to change the page# with each subsequent request???
    #return an arrary of arrays [[50 max results], [other 50 max], etc]
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

                # get playlist songs(extract them)
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
                    title = item['snippet']['title']
                    plId = item['id']
                    ls.append((title, plId))
                    #print("ID: ", item['id'])
                nextPageToken = response.get('nextPageToken')
                if not nextPageToken:
                    break
            return ls
        except:
            e = sys.exc_info()[0]
            print(e)
            print("Something went wrong")