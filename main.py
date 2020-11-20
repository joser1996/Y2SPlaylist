from YouTubeClient import YouTubeClient
from SpotifyClient import SpotifyClient

import os


def main():
    PL_ID = 'PLLsUFwLen8AoiE-DRsusGl5mwr6ysteGR'
    api_key = os.environ.get('API_KEY')
    spotify_client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    spotify_client_secret = os.environ.get('SPOTIFY_SECRET')
    youtube = YouTubeClient(api_key, PL_ID)

    #get youtube playlist and print songs in playlist
    # youtube.getPlaylistItems()
    # youtube.printPlaylistItems()

    spotify = SpotifyClient(spotify_client_id, spotify_client_secret)
    #spotify.requestAuthorizationURL()
    #spotify.requestTokens()
    #spotify.getMyPlaylists()
    #spotify.refreshToken()
    #spotify.tokenIsCurrent()
    spotify.refreshToken()
    #spotify.getPlaylists()
    #spotify.printPlaylists()
    songs = [ "a lot 21 savage"]
    spotify.insertSongs(songs)
if __name__ == "__main__":
    main()
