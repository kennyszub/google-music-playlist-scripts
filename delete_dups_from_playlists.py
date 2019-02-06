#!/usr/bin/env python
from gmusicapi import Mobileclient
import sys
import time

### Functions

def find_and_remove_dups(api, tracks):
    track_set = set()
    for track in tracks:
        tries = 0
        trackId = track['trackId']
        entryId = track['id']
        if trackId in track_set:
            print "    found duplicate with trackId: " + trackId
            while tries < 3:
                try:
                    sys.stdout.write("      attempting to delete... ") # Makes it so no newline appears, cleaner output
                    api.remove_entries_from_playlist(entryId)
                    #break
                except:
                    tries += 1
                    sys.stdout.write(str(tries) + "... ")
                    if tries == 3:
                        print "Failed too many times, exiting!"
                        api.logout()
                        exit(1)
                    time.sleep(1)
                print "Success!"
                break
            time.sleep(1) # Helps prevent Google from creating backend errors
        else:
            track_set.add(trackId)

### Main

# Display help and exit if arguments present            
if len(sys.argv) != 1:
    print "USAGE:"
    print "./delete_dups_from_playlists.py"
    print
    print "     Will delete all duplicate songs within each playlist" 
    exit(0)

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
    print "Successfully logged in. Finding duplicates in playlists"
    playlists = api.get_all_user_playlist_contents()

    for playlist in playlists:
        print "Deleting duplicates from " + playlist['name'] + "..."
        tracks = playlist['tracks']
        find_and_remove_dups(api, tracks)
    api.logout()
else:
    print "Not logged in! Exiting..."
    exit(1)

print "Script has finished successfully!"