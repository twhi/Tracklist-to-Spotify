# -*- coding: utf-8 -*-

from tracklists import Nts
from ts import ToSpotify

nts = Nts()
tracklist = nts.get_data(url = 'https://www.nts.live/shows/the-do-you-breakfast-show/episodes/the-do-you-breakfast-show-w-charlie-bones-jack-rollo-1st-october-2018')
spotify = ToSpotify()
returned = spotify.create_playlist(track_dict=tracklist,playlist_name='Python/Spotify API Test',search_method=1)