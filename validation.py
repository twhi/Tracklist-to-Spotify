import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import pandas as pd
import os
import pickle
import glob

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


def construct_search_string(track):
    track_title = track['title']
    track_artists = track['artist']
    search_string = track_title
    return search_string

def add_tracks(sp, tracks_dict, mode):
    id_list = []
    found_count = 0
    for track in tracks_dict:
        search_string = construct_search_string(track)
        results = sp.search(q=search_string, limit=10)
        track_id = get_track_id_from_search_results(results, track)     
        
        if track_id:
            id_list.append(track_id)
            found_count += 1
            sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_id)
        else:
            id_list.append('')
            
    percent_found = round((found_count/len(tracks_dict))*100,2)
    print('Method #1 - Found ' + str(found_count) + ' tracks out of a possible ' + str(len(tracks_dict)) + ' (' + str(percent_found) + '% success rate)')
    print(type(id_list))
    return id_list

def add_tracks_1(sp, tracks_dict):
    id_list = []
    found_count = 0
    for track in tracks_dict:
        track_title = track['title']
        track_artists = track['artist']
        results = sp.search(q=track_title, limit=10)
        track_id = get_track_id_from_search_results(results, track_title, track_artists)     
        
        if track_id:
            id_list.append(track_id)
            found_count += 1
#            sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_id)
        else:
            id_list.append('')
            
    percent_found = round((found_count/len(tracks_dict))*100,2)
    print('Method #1 - Found ' + str(found_count) + ' tracks out of a possible ' + str(len(tracks_dict)) + ' (' + str(percent_found) + '% success rate)')
    print(type(id_list))
    return id_list
          
def get_track_id_from_search_results(results, track):
    track_title = track['title']
    track_artists = track['artist']
    for result in results['tracks']['items']:
            if result['name'] in track_title and track_artists[0] in result['artists'][0]['name']:
                track_id = [result['id']]
                return track_id
    return False


def add_tracks_2(sp, tracks_dict):
    id_list = []
    found_count = 0
    for track in tracks_dict:
        track_title = track['title']
        track_artists = track['artist']
        search_query = track_artists[0] + ' ' + track_title
        results = sp.search(q=search_query, limit=10)
        track_id = get_track_id_from_search_results(results, track_title, track_artists)     
        
        if track_id:
            id_list.append(track_id)
            found_count += 1
#            sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_id)
        else:
            id_list.append('')

    percent_found = round((found_count/len(tracks_dict))*100,2)
    print('Method #2 - Found ' + str(found_count) + ' tracks out of a possible ' + str(len(tracks_dict)) + ' (' + str(percent_found) + '% success rate)')
    return id_list  

def get_validation_data():
    filenames = glob.glob(".\data\*.pkl")
    datasets = {}
    for idx, filename in enumerate(filenames):
        datasets[idx] = {}
        with open(filename, 'rb') as fp:
            dataset = pickle.load(fp)
            datasets[idx].update(dataset)
    return datasets
    

def csv_to_pkl():
    # get data file names
    path =r'C:\Users\whitehet.UKOUP\Desktop\NTS-to-Spotify-Playlist\data'
    filenames = glob.glob(path + "/*.csv")
    i = 0
    for filename in filenames:
        i += 1
        df = pd.read_csv(filename)
        show_url = list(df.columns.values)[4]
        df.drop(df.columns[[3,4]], axis=1, inplace=True)
        df['Track ID'] = df['Track ID'].str[14:]
        df.to_pickle('./data/' + str(i) + '.pkl')


def run_validation():
    shows = ['https://www.nts.live/shows/circadian-rhythms/episodes/circadian-rhythms-w-last-japan-blackwax-2nd-august-2018',
         'https://www.nts.live/shows/the-do-you-breakfast-show/episodes/the-do-you-breakfast-show-w-charlie-bones-7th-september-2018',
         'https://www.nts.live/shows/goth-money/episodes/goth-money-18th-april-2018',
         'https://www.nts.live/shows/drae-da-skimask/episodes/drae-da-skimask-17th-august-2018']

    datasets = get_validation_data()

    # CREATE SPOTIFY API TOKEN
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    redirect_uri = os.environ.get('REDIRECT_URI')
    username = os.environ.get('UNAME')     
    scope = 'user-library-read playlist-modify-public user-read-private'
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    if not token:
        exit()
    
    for idx, url in enumerate(shows):
        print('#####################')
        print('GETTING DATA FOR SHOW NUMBER ' + str(idx+1))
        print(url)    
        
        # GET PAGE URL
        soup = grab_nts_html(url)
    
        # EXTRACT THE USEFUL BITS
        tracklist_html = soup.findAll('li', {'class':'track'}) 
        tracks_dict = construct_track_dict(tracklist_html)
    
        # DO THE SPOTIFY STUFF
        sp = spotipy.Spotify(auth=token)
        df_1 = add_tracks_1(sp, tracks_dict)
        df_2 = add_tracks_2(sp, tracks_dict)
        
        maximum_possible = datasets[idx]['Track ID'].count()
        total_tracks = len(datasets[idx]['Track ID'])
        max_percent = round((maximum_possible/total_tracks)*100,2)
        
        print('Maximum possible accuracy - ' + str(maximum_possible) + ' out of ' + str(total_tracks) + ' (' + str(max_percent) + '%)')
        print('#####################')
              

