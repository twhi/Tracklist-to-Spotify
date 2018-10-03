import requests
from bs4 import BeautifulSoup

class Nts:
    
    def __init__(self):
        self.session = requests.Session()
        
    def _grab_nts_html(self):
        raw_html = self.session.get(self.url).text
        soup = BeautifulSoup(raw_html, 'html.parser')
        tracklist_html = soup.findAll('li', {'class':'track'}) 
        return tracklist_html        
    
    def get_data(self, url):
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