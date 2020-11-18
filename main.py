from YouTubeClient import YouTubeClient
import os


def main():
    PL_ID = 'PLLsUFwLen8AoiE-DRsusGl5mwr6ysteGR'
    api_key = os.environ.get('API_KEY')
    youtube = YouTubeClient(api_key, PL_ID)

    #get youtube playlist and print songs in playlist
    youtube.getPlaylistItems()
    youtube.printPlaylistItems()

if __name__ == "__main__":
    main()
