# SpotifyPlaylistGenerator

This project is a python program that creates a Spotify playlist with the top tracks from the user's favorite artists

How it does it?

The program asks for the user's spotify username and then redirects him/her to a Spotify authorization page where the user decides whether or not to grant permission.Once permission is granted, the program will receive a authorization token from Spotify which then it will use to make requests to Spotify Web API. Type of requests made during execution: query for artists, their top tracks, user's devices, creation and population of a new playlist.

Instructions:  
 - When prompted for your favorite artists, enter the name of the artist and press enter to proceed entering more artists. Press q to stop
 - The program will only let you input an artist's name once
 - When prompted if you want to start listening to your playlist on a device, if yes, make sure to choose either Smartphone or Computer and have the chosen device runnig on the backgroun
 - Enjoy your playlist!

What was learned?

- Spotipy library
- Spotify Web APIs

