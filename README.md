# Personal Spotify data and simple EDA

## Overview and Reason
I completed this project to examine various summary statistics as well as the distribution of my listening history and patterns in how I listen to music. This project is supposed to be similar to Spotify Wrapped, which happens every year, but I am able to check it whenever I like. It shows me top artists and songs, as well as things like what decades of music I am currently listening to.

## Steps and tools
* I used the developer Spotify API and the spotipy library to get all the data.
* The data is stored in a PostgreSQL DB using pgAdmin(I mainly did this for practice; it wasn't needed; data could have been easily stored in CSV files).
* A simple EDA is performed to see my listening stats as well as some general artist statistics, like trying to identify what makes a song popular.
* EXTRA: I attempt to make a DNN to see if I could predict a popular song given the numeric statistics. The model performed very poorly.

## Issues
* As of now, it takes a long time to run to obtain the data, mainly all of my current tracks I have saved(over 2000). This is due to the nested API calls for each song; I have to call it again to get the artist data along with the song data. 
** Possible Solution: Could be doing a catch for repeat artists(though this probably wouldn't speed this up much).
** Possible Solution: There may be a way where I could only get the new songs added because, as of now, I am just rereading all songs and overriding the database, but if I were to only read the new songs and write those into the database, the program would execute much quicker
NOTE: It takes 30-45 minutes to finish running as of n
