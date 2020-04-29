import getAlbumCovers
import requests
import json
from Levenshtein import distance as levenshtein_distance
import urllib.request
import os.path






albums = getAlbumCovers.getAllAlbums()
for album in albums:
    artist, title = getAlbumCovers.getArtistandTitle(album)
    fileName = getAlbumCovers.getFileName(artist, title)
    # print(artist, title, fileName)
    if os.path.isfile(fileName):
        # print('ALREDY EXISTS')
        continue
    else:
        print(fileName)