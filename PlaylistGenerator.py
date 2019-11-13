import os
import sys
import json
import spotipy
import webbrowser
import random
import spotipy.util as util
from json.decoder import JSONDecodeError


# Get token after user authenticates
def getToken(userName):
    return util.prompt_for_user_token(userName, scope, client_id='daf3c80c9b314ba6a7d99562e5198c92', client_secret='7f495db3a97e47429d0273fa24dc6876', redirect_uri='http://localhost:8000')

# Prints Json response as readable output (Used for testing purposes)
def printJson(input):
    print(json.dumps(input, sort_keys=True, indent=4))

# Populates a playlist with tracks given in the parameters
def PopulatePlaylist(userId, newPlaylistId, newPlaylistUri, tracks, spotifyObject):
    populatePlaylistQuery = spotifyObject.user_playlist_add_tracks(userId, newPlaylistId, tracks)

# Starts playing the playlist on the user's device (Smartphone or Phone)
def startPlayback(devices, spotifyObject, newPlaylistUri):
    #-------------------------------Prompt user-------------------------------------------
    # Ask user if he/she wants to play the new playlist on his/her device
    print("\nYour playlist was sucessfully created!")
    playOnDevice = input("\nWould you like to start listening to your playlist: \"" +  playListName + "\"? Answer: y/n\n" )
    deviceId = ''
    deviceOfChoice = ''
    if playOnDevice == 'y':
        deviceOfChoice = input("\nWhere would you like to start listening? Options: Smartphone or Computer. Note: Your device of choice must be running on the background\n")
        while deviceOfChoice != "Smartphone" and deviceOfChoice != "Computer":
            deviceOfChoice = input("\nWrong input. Please select: \"Smartphone\" or \"Computer\"\n")

        #Look for device
        for device in devices:
            if device['type'] == deviceOfChoice:
                deviceId = device['id']
                break
        
        if deviceId == '':
            print("You do not have a " + deviceOfChoice + " connected to your Spotify account :(\n")
        else:
            #start playback on device
            startPlayBackQuery = spotifyObject.start_playback(deviceId, context_uri = newPlaylistUri)


# Main program
if __name__ == "__main__":

    #----------------------------Initialization-----------------------------------

    #Ask user for his/her Spotify username
    userName = input('\nWhat is your Spotify username?\n')
    scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public playlist-modify-private'

    # Erase cache and prompt for user permission
    try:
        token = getToken(userName)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{userName}")
        token = getToken(userName)

    # Create our spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)

    # Get current user
    user = spotifyObject.current_user()
    userId = user['id']
    display_name = user['display_name']

    # Get playlist name
    print("\nHello, " + display_name + "!. I'm a program that generates a Spotify playlist with the most popular songs from your favorite artists.\n")

    # Get user's devices
    devices = spotifyObject.devices()['devices'] 

    while True: 
        #-----------------------------Get artists' names-------------------------------------
        playListName = input("How would you like to name your playlist?\n")
        artists = []
        tracks = []

        artist = ''
        print('Enter your favorite artists. Press q to stop')
        while True:
            artist = input()
            if artist == 'q':
                print('Artists were sucessfully collected!')
                break
            while (artist in artists):
                print("\nLast artist was already inputted. Please enter a new artist\n")
                artist = input()
            artists.append(artist)
         
        print("-----------------Artists collected " + str(len(artists)) + ":--------------------")
        for artist in artists:
            print(artist)
        
        #--------------------------Query for artists' top tracks----------------------------------

        # Query for top tracks of each inputted artist using artist_id. 
        # Generate a list of tracks' ids
        
        for artist in artists:
            print("Collecting top tracks from " + artist)
            if artist != '':
                artistQuery = spotifyObject.search(artist, type='artist', limit=1)
                if artistQuery['artists']['total'] == 0:
                    print()
                    print("| WARNING: Artist: " + artist + " was not Found in Spotify |")
                    print()
                else: 
                    artistId = artistQuery['artists']['items'][0]['id']
                    tracksQuery = spotifyObject.artist_top_tracks(artistId)
                    artistTopTracks = tracksQuery['tracks']
                    for track in artistTopTracks:
                        tracks.append(track['id'])
            
        print("\nTotal number of tracks collected: " + str(len(tracks)) + '\n')
        #----------------------------Generate new playlist-------------------------------------

        #Have to split the additions of tracks into playlist into hundreds

        #Create and Populate new playlist
        newTracks = []
        counter = 0

        if len(tracks) == 0:
            print("\nNo tracks were collected. No playlist was created\n")
        else:
            createPlaylistQuery = spotifyObject.user_playlist_create(userId, name=playListName, public=True)
            newPlaylistId = createPlaylistQuery['id']
            newPlaylistUri = createPlaylistQuery['uri']
            if len(tracks) > 100:
                print("Wow a lot of tracks!!\n")
                for i  in range(int((len(tracks)/100) + 1)): # Some Songs get lost 
                    newTracks = []
                    for j in range(i + counter, counter + 100, 1):
                        if j > len(tracks) - 1:
                            break
                        newTracks.append(tracks[j])
                    counter = counter + 100
                    PopulatePlaylist(userId, newPlaylistId, newPlaylistUri, newTracks, spotifyObject)
                    #populatePlaylistQuery = spotifyObject.user_playlist_add_tracks(userId, newPlaylistId, newTracks)
            else:
                #populatePlaylistQuery = spotifyObject.user_playlist_add_tracks(userId, newPlaylistId, tracks)
                PopulatePlaylist(userId, newPlaylistId, newPlaylistUri, tracks, spotifyObject)

            startPlayback(devices, spotifyObject, newPlaylistUri)

        # Ask user if he/she would like to continue

        choice = input("\nWould you like to create a new playlist? Answer: y/n\n\n")
        if choice != 'y':
            print("Thanks for trying me out. Enjoy your music! :)")
            break

        #--------------------------------------------------------------------------------------