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
        track_name = track.find('span', {'class':'track__title'}).text 
        current_item['title'] = track_name
        artist_name_list = track.findAll('span', {'class':'track__artist'})
        artist_list = []
        
        for artist in artist_name_list:
            artist_list.append(artist.text)
            
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
    found_count = 0
    for track in tracks_dict:
        track_title = track['title']
        track_artists = track['artist']
        results = sp.search(q=track_title, limit=50)
        track_id = get_track_id_from_search_results(results, track_title, track_artists)     
        if track_id:
            found_count += 1
            sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_id)
    percent_found = round((found_count/len(tracks_dict))*100,2)
    print('Found ' + str(found_count) + ' tracks out of a possible ' + str(len(tracks_dict)) + ' (' + str(percent_found) + '% success rate)')
     
def get_track_id_from_search_results(results, track_title, track_artists):
    for result in results['tracks']['items']:
            if result['name'] in track_title and track_artists[0] in result['artists'][0]['name']:
                track_id = [result['id']]
                return track_id
                break
    return False

url = 'https://www.nts.live/shows/creepzone/episodes/creepzone-10th-september-2018'
username = '' # your username

print('Getting show HTML')
soup = grab_nts_html(url)

print('Parsing HTML and extracting track info')
tracklist_html = soup.findAll('li', {'class':'track'}) 

tracks_dict = construct_track_dict(tracklist_html)
token = get_session_token()
if token:
    sp = spotipy.Spotify(auth=token)
    playlist_name = 'Python/Spotify API Test'
    playlist_id = create_playlist(sp=sp, username = username, playlist_name = playlist_name)   
    print('Searching for tracks and adding to Spotify')
    add_tracks(sp, tracks_dict)

            


        