
import pickle
class PlaylistSyncer:
    def __init__(self):
        #Attempt to load in local list of tracks
        print("Attempting to load local tracks...")
        try:
            fp = open("local_tracks.pkl", "rb")
            obj = pickle.load(fp)
            fp.close()
            self.localTracks = obj['trackList']
            print("successfully loaded")
        except:
            self.localTracks = []
            obj = {'trackList': self.localTracks}
            fp = open("local_tracks.pkl", "wb")
            pickle.dump(obj, fp)
            fp.close()
            print("Created new local track list")

    #returns list of songs that are not in the local
    #playlist(youtube) yet to keep track of differences
    def getTrackDifferences(self, upstreamTrackList):
        differences = list(set(upstreamTrackList) - set(self.localTracks))
        #print("Track differences are: ", differences)
        return differences

    def addTracksToLocal(self, tracks):
        for track in tracks:
            self.localTracks.append(track)
        self.writeLocalTracks()
        print("Added tracks to local")

    def eraseLocalTracks(self):
        self.localTracks = []
        self.writeLocalTracks()
        print("Deleted local tracks")

    def writeLocalTracks(self):
        fp = open("local_tracks.pkl", "wb")
        obj = {'trackList': self.localTracks}
        pickle.dump(obj, fp)
        fp.close()
 