import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util

def grab_nts_html(url):
    session = requests.Session()
    raw_html = session.get(url).text
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup

def construct_track_dict(tracklist_html):
    tracks_dict = []
    
    for count_track, track in enumerate(tracklist_html):
        current_item = {'artist':{},'title':{}}
        track_name = track.find('span', {'class':'track__title'}).decode_contents() 
        current_item['title'] = track_name
        artist_name_list = track.findAll('span', {'class':'track__artist'})
        artist_list = []
        
        for artist in artist_name_list:
            artist_list.append(artist.decode_contents())
            
        current_item['artist'] = artist_list
        tracks_dict.append(current_item)    
    return tracks_dict

def get_session_token():
    client_id = '' # client id
    client_secret = '' # client secret
    redirect_uri = '' # redirect uri
    scope = 'user-library-read playlist-modify-public user-read-private'
    username = '' # username
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return token

def create_playlist(sp, username, playlist_name):
    playlist_exists = False
    existing_playlists = sp.user_playlists(username)['items']
    
    for playlist in existing_playlists:
        if playlist_name in playlist['name']:
            playlist_exists = True
            playlist_id = playlist['id']
            break
    
    if not playlist_exists:
        playlist = sp.user_playlist_create(username, name=playlist_name, public=True)
        playlist_id = playlist['id']
        
    return playlist_id


def search_spotify(sp, query):
    results = sp.search(q=query, limit=50)
    return results

def add_tracks(sp, tracks_dict):
    for track in tracks_dict:
        print(track)

# declare URL of radio show
url = 'https://www.nts.live/shows/utopian-project/episodes/utopia-project-3rd-october-2017'
username = 'tom1'
soup = grab_nts_html(url)
tracklist_html = soup.findAll('li', {'class':'track'}) 
tracks_dict = construct_track_dict(tracklist_html)
token = get_session_token()
if token:
    sp = spotipy.Spotify(auth=token)
    playlist_name = 'Python/Spotify API Test'
    playlist_id = create_playlist(sp=sp, username = username, playlist_name = playlist_name)    
    add_tracks(sp, tracks_dict)


        