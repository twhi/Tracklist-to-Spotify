import requests
from bs4 import BeautifulSoup

# declare URL of radio show
test_url = 'https://www.nts.live/shows/utopian-project/episodes/utopia-project-3rd-october-2017'

# create requests session and get radio show HTML
session = requests.Session()
raw_html = session.get(test_url).text
soup = BeautifulSoup(raw_html, 'html.parser')

# get tracklist from HTML
tracklist_html = soup.findAll('li', {'class':'track'})

# declare dictionary to store the retrieved data
tracks_dict = {}

for count_track, track in enumerate(tracklist_html):
    # define the first level of the dictionary (one entry for each track in the show)
    tracks_dict['track' + str(count_track+1)] = {}
    
    # find the track name
    track_name = track.find('span', {'class':'track__title'}).decode_contents() 
    
    # get a list of the track artists
    artist_name_list = track.findAll('span', {'class':'track__artist'})
    # for each item in the artist list add this to its own artist key in the dictionary
    for count_artist, artist in enumerate(artist_name_list):
        tracks_dict['track' + str(count_track+1)]['artist' + str(count_artist+1)] = artist.decode_contents()

    # add track title to the dictionary
    tracks_dict['track' + str(count_track+1)]['title'] = track_name
        