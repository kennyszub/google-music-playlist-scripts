#!/usr/bin/env python
from gmusicapi import Mobileclient
import sys

### Functions 

def get_playlist_tracks(name, playlists):
    for playlist in playlists:
        if playlist['name'].lower() == name.lower():
            tracks = playlist['tracks']
            return tracks
    print "ERROR: No playlist '" + name + "'found"
    exit(1)


def move_songs_to_top(api, tracks, num_tracks_to_move):
    num_tracks = len(tracks)
    preceding_entry = tracks[0]
    for x in range(0, num_tracks_to_move):
        entry_to_move = tracks[num_tracks - 1 - x]
        track_id = api.reorder_playlist_entry(entry_to_move, None, preceding_entry)
        if track_id[0] == entry_to_move['id']:
            print "Successfully moved track " + entry_to_move['id']
        else:
            print "Failed to move track " + entry_to_move['id']

### Main

if len(sys.argv) != 3:
    print "USAGE:"
    print "./add_last_songs_to_top_of_playlist.py 'PLAYLIST NAME' NUMBER_SONGS"
    print
    print "example: ./add_last_songs_to_top_of_playlist.py 'Ultimate Everything' 5"
    print "     will move the last 5 songs in 'Ultimate Everything' to the top of the playlist."
    exit(0)
else:
    playlist_name = sys.argv[1]
    num_songs = sys.argv[2]

# Setup the gmusicapi
api = Mobileclient()
api.__init__()


# Check to see if OAuth credentials available, ask user to setup if not
try:
    api.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
except:
    print "No OAuth credentials found! Please setup in the following screen!"
    api.perform_oauth()
    api.oauth_login(Mobileclient.FROM_MAC_ADDRESS) # If it fails here, it wasn't meant to be

# Then, move on to doing all the work
if api.is_authenticated():
    print "Successfully logged in. Moving " + num_songs + " tracks to top of playlist"
    playlists = api.get_all_user_playlist_contents()
    tracks = get_playlist_tracks(playlist_name, playlists)
    move_songs_to_top(api, tracks, int(num_songs))

print "Script completed successfully!"