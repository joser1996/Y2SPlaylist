from googleapiclient.discovery import build
import json
import sys

class YouTubeClient:
    def __init__(self, key, playlistID):
        self.key = key
        self.playlistID = playlistID
        self.youtube = build('youtube', 'v3', developerKey=key)
        self.playlist = []
        self.songs = []

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
 