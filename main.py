from tracklists import Nts, Bbc
from ts import ToSpotify
from urllib.parse import urlparse
    
def get_tracklist(url):
    tracklist = False
    website = urlparse(url).hostname.split('.')[1]
    if website == 'bbc':
        bbc = Bbc()
        tracklist = bbc.get_data(url = url)
    elif website == 'nts':
        nts = Nts()
        tracklist = nts.get_data(url = url)
    
    return tracklist

    
if __name__ == "__main__":
    
    shows = ['https://www.bbc.co.uk/programmes/m0000pc1', 
             'https://www.nts.live/shows/moxie/episodes/moxie-10th-october-2018',
             'https://stackoverflow.com/questions/1663807/how-to-iterate-through-two-lists-in-parallel']
    
    for idx, url in enumerate(shows):
        tracklist = get_tracklist(url)
        
        if tracklist:
            spotify = ToSpotify()
            print('#######################################')
            print('Show #' + str(idx+1))
            print('#######################################')      
            returned4 = spotify.create_playlist(track_dict=tracklist,playlist_name='newwuns',search_method=4,add_tracks=True)