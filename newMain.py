from dotenv import load_dotenv
import os
from YouTubeClient import YouTubeClient
from SpotifyClient import SpotifyClient
from PlaylistSyncer import PlaylistSyncer
from helpers import *
load_dotenv()

#check if need to refresh token
if(not tokenIsFresh()):
	refreshAccessToken()

spotify = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))

youtube = YouTubeClient(os.environ.get('GOOGLE_API_KEY'), os.environ.get('PL_ID'))
youtube.getPlaylistItems()

ps = PlaylistSyncer()

#compares songs from youtube to song titles in 'local_tracks.pkl'
#Songs not found in local_tracks are songs that have not been 
#attempted to be added in spotify playlist
songs_to_add = ps.getTrackDifferences(youtube.songs)

if songs_to_add:
	spotify.insertSongs(songs_to_add)
	if(spotify.uris):
		ps.addTracksToLocal(songs_to_add)
else:
	print("Local seems up-to-date not pushing")

