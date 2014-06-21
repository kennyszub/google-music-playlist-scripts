#!/usr/bin/env python
from gmusicapi import Mobileclient
import sys


# TODO remove this unused function, previously used to return tracks from a given playlist
def get_playlist_tracks(name, playlists):
    for playlist in playlists:
        if playlist['name'].lower() == name.lower():
            tracks = playlist['tracks'] 
            return tracks 
    print "ERROR: No playlist '" + name + "'found"
    exit(1)

def find_and_remove_dups(api, tracks):
    track_set = set()
    for track in tracks:
        trackId = track['trackId']
        entryId = track['id']
        if trackId in track_set:
            print "    found duplicate with trackId: " + trackId + ", deleting"
            api.remove_entries_from_playlist(entryId)
        else:
            track_set.add(trackId)
            

if len(sys.argv) != 1:
    print "USAGE:"
    print "./delete_dups_from_playlists.py"
    print
    print "     Will delete all duplicate songs within each playlist" 
    exit(0)

api = Mobileclient()
logged_in = api.login('username', 'password')

if logged_in:
    print "Successfully logged in. Finding duplicates in playlists"
    playlists = api.get_all_user_playlist_contents()

    for playlist in playlists:
        print "Deleting duplicates from " + playlist['name'] + "..."
        tracks = playlist['tracks']
        find_and_remove_dups(api, tracks)

