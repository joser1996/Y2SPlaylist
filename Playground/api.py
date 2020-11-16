import os
import json
from googleapiclient.discovery import build

api_key = os.environ.get('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
playListID = 'PLLsUFwLen8AoiE-DRsusGl5mwr6ysteGR'
channelID = 'UCgaOpYFPdxWMWI2xXaylKGA'
request = youtube.playlistItems().list(
    part='contentDetails, snippet',
    playlistId=playListID
    )

#response seems to be a dicitonary
response = request.execute()

#pretty print the dict object
print(json.dumps(response, indent=2))
