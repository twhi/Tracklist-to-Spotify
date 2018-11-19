from tracklists import Nts, Bbc
from ts import ToSpotify
from urllib.parse import urlparse
    
def get_tracklist(url):
    tracklist = False
    website = urlparse(url).hostname.split('.')[1]
    if website == 'bbc':
        instance = Bbc()
    elif website == 'nts':
        instance = Nts()
    
    tracklist = instance.get_data(url)
    return tracklist

    
if __name__ == "__main__":
    
    shows = ['https://www.nts.live/shows/ygg/episodes/ygg-15th-november-2018',
             'https://www.nts.live/shows/real-bitch-radio/episodes/realbitchradio-w-violet-waters-15th-november-2018',
             'https://www.nts.live/shows/naomi/episodes/naomi-aaron-j-14th-november-2018',
             'https://www.bbc.co.uk/programmes/m00015b0']
    
    for idx, url in enumerate(shows):
        tracklist = get_tracklist(url)
        
        if tracklist:
            spotify = ToSpotify()
            print('#######################################')
            print('Show #' + str(idx+1))
            print('#######################################')      
            returned4 = spotify.create_playlist(track_dict=tracklist,playlist_name='newwuns',search_method=4,add_tracks=True)