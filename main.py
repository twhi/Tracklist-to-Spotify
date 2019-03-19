from tracklists import Nts, Bbc
from ts import ToSpotify
from urllib.parse import urlparse


def get_tracklist(url):
    website = urlparse(url).hostname.split('.')[1]
    if website == 'bbc':
        instance = Bbc()
    elif website == 'nts':
        instance = Nts()
    else:
        return False

    t = instance.get_data(url)
    return t


if __name__ == "__main__":

	tracklist = ''
	while True:
		show = input('Please enter the URL of the radio show you\'d like to get tracks from: ')
		if show:
			try:
				tracklist = get_tracklist(show)
			except:
				pass

		if tracklist:
			print('Tracklist found. Adding tracks to Spotify.')
			spotify = ToSpotify()
			returned = spotify.create_playlist(track_dict=tracklist, playlist_name='newwuns', add_tracks=True)
		else:
			print('Show not found. Please try again.\n')
