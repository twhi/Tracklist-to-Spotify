import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import pandas as pd
import os
import pickle
import glob

class Nts:
    
    def __init__(self):
        self.session = requests.Session()
        
    def _grab_nts_html(self):
        raw_html = self.session.get(self.url).text
        soup = BeautifulSoup(raw_html, 'html.parser')
        tracklist_html = soup.findAll('li', {'class':'track'}) 
        return tracklist_html        
    
    def connect(self, url):
        self.url = url
        tracklist_html = self._grab_nts_html()        
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
    
class NtsToSpotify:
    
    def __init__(self):        
        # INITIALISE VARIABLES
        self.found_count = 0
        self.track_id_list = []
        
        # INITIALISE SPOTIFY API VARIABLES
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.redirect_uri = os.environ.get('REDIRECT_URI')
        self.username = os.environ.get('UNAME')          
        self.scope = 'user-library-read playlist-modify-public user-read-private'
        self.token = util.prompt_for_user_token(self.username, self.scope, self.client_id, self.client_secret, self.redirect_uri)
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
            
    def _make_playlist(self, sp, username, playlist_name):
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
    
    def create_playlist(self, track_dict, playlist_name, search_method):
        self.search_method = search_method
        self.playlist_name = playlist_name
        self.track_dict = track_dict
        self.playlist_id = self._make_playlist(self.sp, self.username, self.playlist_name)
        
        for track in self.track_dict:
            search_string = self._construct_search_string(track)
            results = self.sp.search(q=search_string, limit=10)
            track_id = self._get_track_id_from_search_results(results, track)     
            self._add_to_playlist(track_id)
        
        self._calculate_success()
    
    def _calculate_success(self):
        percent_found = round((self.found_count/len(self.track_dict))*100,2)
        print('Method #1 - Found ' + str(self.found_count) + ' tracks out of a possible ' + str(len(self.track_dict)) + ' (' + str(percent_found) + '% success rate)')
    
    def _add_to_playlist(self, track_id):
        if track_id:
            self.track_id_list.append(track_id)
            self.found_count += 1
            self.sp.user_playlist_add_tracks(user=self.username, playlist_id=self.playlist_id, tracks=track_id)
            return True
        else:
            self.track_id_list.append('')
            return False
    
    def _construct_search_string(self, track):
        if self.search_method == 1:
            track_title = track['title']
            search_string = track_title
        return search_string
    
    def _get_track_id_from_search_results(self, results, track):
        track_title = track['title']
        track_artists = track['artist']
        for result in results['tracks']['items']:
                if result['name'] in track_title and track_artists[0] in result['artists'][0]['name']:
                    track_id = [result['id']]
                    return track_id
        return False


    
nts = Nts()
tracklist = nts.connect(url = 'https://www.nts.live/shows/drae-da-skimask/episodes/drae-da-skimask-17th-august-2018')
spotify = NtsToSpotify()
tester = spotify.create_playlist(tracklist, playlist_name = 'Python/Spotify API Test', search_method = 1)