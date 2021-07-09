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

youtube = YouTubeClient(os.environ.get('GOOGLE_API_KEY'), os.environ.get('PL_ID'))
spotify = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
ps = PlaylistSyncer()

youtube.getPlaylistItems()

songs_to_add = ps.getTrackDifferences(youtube.songs)

if songs_to_add:
	spotify.insertSongs(songs_to_add)
	if(spotify.uris):
		ps.addTracksToLocal(songs_to_add)
else:
	print("Local seems up-to-date not pushing")

