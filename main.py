from YouTubeClient import YouTubeClient
from SpotifyClient import SpotifyClient
from PlaylistSyncer import PlaylistSyncer
import os


def main():
    PL_ID = 'PLLsUFwLen8AoiE-DRsusGl5mwr6ysteGR'
    api_key = os.environ.get('API_KEY')
    #Initialize spotify and youtube client
    youtube = YouTubeClient(api_key, PL_ID)
    spotify = SpotifyClient(os.environ.get('SPOTIFY_CLIENT_ID'), os.environ.get('SPOTIFY_SECRET'))
    ps = PlaylistSyncer()

    #Deleting local tracks to retry
    #ps.eraseLocalTracks()

    #get song titles from YT(upstream) playlist
    youtube.getPlaylistItems()

    #Find the difference b/w local list and pulled list
    songsToAdd = ps.getTrackDifferences(youtube.songs)

    if  songsToAdd:
        #Makesure spotify access token is still valid
        spotify.refreshAccessToken()

        #Attempt to insert songs to spotify playlist
        spotify.insertSongs(songsToAdd)
        if(spotify.uris):
            #Update local list(write)
            ps.addTracksToLocal(songsToAdd)


    else:
        print("Local seems up-to-date. Not pushing.")

if __name__ == "__main__":
    main()
