# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 10:54:32 2018

@author: whitehet
"""

import glob
import pandas as pd

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