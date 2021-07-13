import os
import json
import requests
import urllib
import base64
import time
import sys
import pickle
import re

class SpotifyClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.uris = []
        self.playlists = []
    # Method to insert a song or possiblly a list of songs
    #default to the test playlist
    #need to get spotify ID from url on playlist homepage on spotify webplayer
    def insertSongs(self, songs, id='5O7l46N1wPZuqHDjOygRuF'):
        endPoint = 'https://api.spotify.com/v1/playlists/' + id +'/tracks'
        tokens = pickle.load(open('tokens.pkl', 'rb'))
        a_token = self.getCurrentToken()
        ar = []
        for song in songs:
            try:
                uri = self.getTrackURI(song)
                ar.append(uri)
            except:
                print("Song: ", song, " NOT FOUND!")

        #print("URIS: ", ar)
        self.uris = ar
        if not ar:
            return

        body = {'uris': ar, 'position': 0}
        header = {
            'Authorization': 'Bearer {}'.format(a_token),
            'Content-Type': 'application/json'
        }
        res = requests.post(
            url=endPoint,
            json=body,
            headers=header
        )
        print("Insert Response: ", res.json())

    def getCurrentToken(self):
        tokens = pickle.load(open('tokens.pkl', 'rb'))
        return tokens['access_token']

    def getTrackURI(self, songName):
        #this is a GET request
        endPoint = 'https://api.spotify.com/v1/search?'
        header = {'Authorization': 'Bearer ' + self.getCurrentToken()}
        q = self.makeQuery(songName)
        print("Q: ", q)
        url = endPoint + q
        res = requests.get(url=url, headers=header)
        res_json = res.json()
        #print(json.dumps(res_json, indent=2))
        return res_json['tracks']['items'][0]['uri']


    def makeQuery(self, songName):
        #attempt to seperate into artist and song
        query = "q="
        #some pre processing remove (), anything after ft.
        splitString = songName.split("ft.")[0]
        if splitString:
            songName = splitString

        splitString = songName.split("(")[0]
        if splitString:
            songName = splitString

        splitString = songName.split("[")[0]
        if splitString:
            songName = splitString
        try:
            maxSplit = 1
            splittedString = songName.split('-', maxSplit)
            if splittedString[1][0] == ' ':
                splittedString[1] = splittedString[1][1:]

            artist = splittedString[0].replace(" ", "%20")
            trackName = splittedString[1].replace(" ", "%20")
            query = query + "artist:" + artist
            query = query + "track:" + trackName
            query = query + "&type=track&limit=1"
            return query
        except:
            trackname = songName.replace(" ", "%20")
            query = query + "track:" + trackName + "&type=track&limit=1"
            return query

    def getPlaylists(self):
        url = 'https://api.spotify.com/v1/me/playlists'
        #load in the current access token
        access_token = self.getCurrentToken()
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }
        response = requests.get(
            url=url,
            headers=header
        )
        res_json = response.json()
        pls = {}
        ls = []
        try:
            for item in res_json["items"]:
                id = item['id']
                name = item['name']
                pls[id] = name
                ls.append(name)
        except:
            print("updateMyPlaylists Failed")
            print(res_json)
        pickle_out = open("playlists.pkl", "wb")
        pickle.dump(pls, pickle_out)
        pickle_out.close()
        return ls

    def printPlaylists(self):
        fp = open("playlists.pkl", "rb")
        dict = pickle.load(fp)
        for id in dict:
            print(dict[id])
        fp.close()


# TODO:  Look at response or figure out which songs were successfully inserted
 