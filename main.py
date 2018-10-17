# -*- coding: utf-8 -*-

from tracklists import Nts
from ts import ToSpotify

shows = ['https://www.nts.live/shows/moxie/episodes/moxie-danny-daze-23rd-november-2016']

for idx, url in enumerate(shows):
    nts = Nts()
    tracklist = nts.get_data(url = url)
    spotify = ToSpotify()
    print('#######################################')
    print('Show #' + str(idx+1))
    print('#######################################')      
    returned4 = spotify.create_playlist(track_dict=tracklist,playlist_name='house',search_method=4,add_tracks=True)