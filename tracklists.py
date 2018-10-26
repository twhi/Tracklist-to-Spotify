import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Nts:
    
    def __init__(self):
        self.session = requests.Session()
        
    def _grab_nts_html(self):
        raw_html = self.session.get(self.url).text
        soup = BeautifulSoup(raw_html, 'html.parser')
        tracklist_html = soup.findAll('li', {'class':'track'}) 
        return tracklist_html        
    
    def _get_artists_from_html(self):
        artist_list = []
        for track in self.tracklist_html:
            artist_name_list = track.findAll('span', {'class':'track__artist'})
            current_list = []
            for artist in artist_name_list:
                current_list.append(artist.text)
            artist_list.append(current_list)
        return artist_list
    
    def _get_tracks_from_html(self):
        track_list = []
        for track in self.tracklist_html:
            track_name = track.find('span', {'class':'track__title'}).text 
            track_list.append(track_name)
        return track_list   
    
    def _contruct_setlist(self):
        setlist = []
        for track, artist in zip(self.track_list, self.artist_list):
            current_item = {'artist':artist,'title':track}
            setlist.append(current_item)
        return setlist
    
    def get_data(self, url):
        self.url = url
        self.tracklist_html = self._grab_nts_html()        
        self.artist_list = self._get_artists_from_html()
        self.track_list = self._get_tracks_from_html()
        setlist = self._contruct_setlist()
        return setlist
    
class Bbc:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
    
    def _grab_bbc_html(self):
        return self.driver.get(self.url) 
    
    def _get_artists_from_html(self):
        artists = self.driver.find_elements_by_xpath('//h3[@class="gamma no-margin"]')
        artist_list=[]
        for artist in artists:
            artist_list.append(artist.text.split('&'))        
        return artist_list
    
    def _get_tracks_from_html(self):
        tracks = self.driver.find_elements_by_xpath('//div[@class="segment__track"]//p')
        track_list=[]
        for track in tracks:
            track_list.append(track.text)
        return track_list
    
    def _contruct_setlist(self):
        setlist = []
        for track, artist in zip(self.track_list, self.artist_list):
            current_item = {'artist':artist,'title':track}
            setlist.append(current_item)
        return setlist
    
    def get_data(self, url):
        self.url = url
        self.tracklist_html = self._grab_bbc_html()
        self.artist_list = self._get_artists_from_html()
        self.track_list = self._get_tracks_from_html()
        setlist = self._contruct_setlist()
        return setlist
        
        