import os
import spotipy
import spotipy.util as util
import re 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class ToSpotify:
    
    def __init__(self):            
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
    
    def create_playlist(self, track_dict, playlist_name, search_method, add_tracks=False):
        '''
        Will create a spotify playlist named playlist_name. 
        Track dict must be in the following format:
        track_dict = [
                        {
                        'artist':[artist1, artist2, ...],
                        'track':'trackname'
                        },
                        {
                        'artist':[artist1, artist2, ...],
                        'track':'trackname'
                        }, 
                        ...
                    ]
        '''
        self.found_count = 0
        self.track_id_list = []
        self.add_tracks = add_tracks
        self.search_method = search_method
        self.playlist_name = playlist_name
        self.track_dict = track_dict
        self.playlist_id = self._make_playlist(self.sp, self.username, self.playlist_name)
        
        for track in self.track_dict:
#            print('--')
            search_string = self._construct_search_string(track)
#            print('Searching for - ' + search_string)
            results = self.sp.search(q=search_string, limit=10)
            track_id = self._get_track_id_from_search_results(results, track)     
            self._add_to_playlist(track_id)
        
        self._calculate_success()
        self.found_count = 0
        return self.track_id_list
    
    def _calculate_success(self):
        percent_found = round((self.found_count/len(self.track_dict))*100,2)
        print('Method #' + str(self.search_method) + ' - Found ' + str(self.found_count) + ' tracks out of a possible ' + str(len(self.track_dict)) + ' (' + str(percent_found) + '% success rate)')
    
    def _add_to_playlist(self, track_id):
        if track_id:
            self.track_id_list.append(track_id)
            self.found_count += 1
            if self.add_tracks:
                self.sp.user_playlist_add_tracks(user=self.username, playlist_id=self.playlist_id, tracks=track_id)
            return True
        else:
            self.track_id_list.append('')
            return False
    
    def _construct_search_string(self, track):
        if self.search_method == 1:
            # SEARCHES BY TRACK TITLE
            track_title = track['title']
            search_string = track_title
        elif self.search_method == 2:
            # SEARCHES BY A COMBINATION OF TRACK TITLE AND ARTIST
            track_title = track['title']
            track_artists = track['artist']
            search_string = track_artists[0] + ' ' + track_title
        elif self.search_method == 3:
            # SEARCHES BY A COMBINATION OF TRACK TITLE AND ARTIST BUT REMOVES ALL TEXT WITHIN BRACKETS
            track_title = re.sub("[\(\[].*?[\)\]]", "", track['title']).strip()
            track_artists = track['artist']
            search_string = track_artists[0] + ' ' + track_title
        elif self.search_method == 4:
            # SEARCHES BY A COMBINATION OF TRACK TITLE AND ARTIST BUT REMOVES ALL TEXT WITHIN BRACKETS, ALSO REMOVES APOSTROPHES 
            track_title = re.sub("[\(\[].*?[\)\]]", "", track['title']) # REMOVE BRACKETS
            track_title = re.sub(r'([^\s\w]|_)+', '', track_title) # REMOVE PUNCTUATION
            track_title.strip() # REMOVE LEADING AND TRAILING WHITESPACE
            track_artists = track['artist']
            search_string = track_artists[0] + ' ' + track_title
        return search_string
  
#    3RD GENERATION MATCHING FUNCTION - USES FUZZY STRING MATCHING, MORE ACCURATE THAN GEN 2 BUT NEEDS REFINING  
    def _get_track_id_from_search_results(self, results, track):
        track_artists = track['artist']
        for result in results['tracks']['items']:
                result_artists = result['artists']
                result_artists_combined = [''.join(x['name'].lower()) for x in result_artists]
                best_result = process.extractOne(track_artists[0].lower().strip(), result_artists_combined, scorer=fuzz.ratio)
                score = best_result[1]
#                print(' ...Best result is - ' + best_result[0] + ' at ' + str(score) + '% accuracy', end='')
                if score > 90:
                    track_id = [result['id']]
#                    print(' SUCCESSFUL')
                    return track_id
#                else:
#                    print(' FAILURE')
        return False
   
##    2ND GENERATION RESULT MATCHING FUNCTION
#    def _get_track_id_from_search_results(self, results, track):
#        track_artists = track['artist']
#        for result in results['tracks']['items']:
#                result_artists = result['artists']
#                result_artists_combined = [''.join(x['name'].lower()) for x in result_artists]
#                if track_artists[0].lower().strip() in result_artists_combined:
#                    track_id = [result['id']]
#                    return track_id
#        return False
    
    
##    ORIGINAL RESULT MATCHING FUNCTION
#    def _get_track_id_from_search_results(self, results, track):
#        track_title = track['title']
#        track_artists = track['artist']
#        for result in results['tracks']['items']:
#                result_title = result['name'] 
#                result_artists = result['artists']         
#                if result_title in track_title and track_artists[0] in result_artists[0]['name']:
#                    track_id = [result['id']]
#                    return track_id
#        return False
