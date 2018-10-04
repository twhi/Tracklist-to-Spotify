# -*- coding: utf-8 -*-

from tracklists import Nts
from ts import ToSpotify

shows = ['https://www.nts.live/shows/circadian-rhythms/episodes/circadian-rhythms-w-last-japan-blackwax-2nd-august-2018',
         'https://www.nts.live/shows/the-do-you-breakfast-show/episodes/the-do-you-breakfast-show-w-charlie-bones-7th-september-2018',
         'https://www.nts.live/shows/goth-money/episodes/goth-money-18th-april-2018',
         'https://www.nts.live/shows/drae-da-skimask/episodes/drae-da-skimask-17th-august-2018']

#shows = ['https://www.nts.live/shows/drae-da-skimask/episodes/drae-da-skimask-17th-august-2018']

for url in shows:
    nts = Nts()
    tracklist = nts.get_data(url = url)
    spotify = ToSpotify()
    returned = spotify.create_playlist(track_dict=tracklist,playlist_name='Python/Spotify API Test',search_method=1)
    returned = spotify.create_playlist(track_dict=tracklist,playlist_name='Python/Spotify API Test',search_method=2)