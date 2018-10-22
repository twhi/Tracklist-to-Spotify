# -*- coding: utf-8 -*-

from tracklists import Nts
from ts import ToSpotify

shows = ['https://www.nts.live/shows/moxie/episodes/moxie-10th-october-2018']

for idx, url in enumerate(shows):
    nts = Nts()
    tracklist = nts.get_data(url = url)
    spotify = ToSpotify()
    print('#######################################')
    print('Show #' + str(idx+1))
    print('#######################################')      
    returned4 = spotify.create_playlist(track_dict=tracklist,playlist_name='newwuns',search_method=4,add_tracks=True)