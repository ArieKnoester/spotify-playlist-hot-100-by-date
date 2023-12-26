# spotify-playlist-hot-100-by-date

## Description:
- A user enters a date in the console (YYYY-MM-DD)
- The program goes to the Billboard Hot 100 website for that date and scrapes
the list of songs.
- The program then goes to Spotify's api and searches for the uri of each song,
creates a new playlist, and populates it with the songs returned from search.

### Notes:
- The result returned when using Spotify's search endpoint do not always return
what you expect. Currently, the search terms used are the song title, name of the
artist, and the year (taken from the user input date). Spotify's api might return
a cover or remix of the song instead of the exact song from Billboard's list. Most
of the results have been correct in my testing, but there may be a few songs out
of 100 that are not exactly correct.
