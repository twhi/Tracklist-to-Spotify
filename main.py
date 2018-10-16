# -*- coding: utf-8 -*-

from tracklists import Nts
from ts import ToSpotify

shows = ['https://www.nts.live/shows/the-do-you-breakfast-show/episodes/the-do-you-breakfast-show-11th-october-2018']

for idx, url in enumerate(shows):
    nts = Nts()
    tracklist = nts.get_data(url = url)
    spotify = ToSpotify()
    print('#######################################')
    print('Show #' + str(idx+1))
    print('#######################################')      
#    returned1 = spotify.create_playlist(track_dict=tracklist,playlist_name='newwuns',search_method=1,add_tracks=False)
#    returned2 = spotify.create_playlist(track_dict=tracklist,playlist_name='newwuns',search_method=2,add_tracks=False)
#    returned3 = spotify.create_playlist(track_dict=tracklist,playlist_name='newwuns',search_method=3,add_tracks=False)
    returned4 = spotify.create_playlist(track_dict=tracklist,playlist_name='newwuns',search_method=4,add_tracks=True)