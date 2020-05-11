import requests
import json
from Levenshtein import distance as levenshtein_distance
import urllib.request
import os.path

API_KEY = open("../apis/lastfm.key").read().strip()
USER_AGENT = "Dataquest"
LIST = open("../log.log").read().strip().split("\n")


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def getClosestGuess(artist, albumName):
    headers = {"user-agent": USER_AGENT}

    payload = {
        "api_key": API_KEY,
        "method": "album.search",
        "format": "json",
        "album": albumName,
        "limit": 10,
    }

    r = requests.get(
        "http://ws.audioscrobbler.com/2.0/", headers=headers, params=payload
    )
    # print(r.albummatches.album)
    # print(r.json()['results']['albummatches']['album'])

    albums = r.json()["results"]["albummatches"]["album"]
    dist = 1000
    pos = -1

    for i in range(len(albums)):
        lev = levenshtein_distance(artist.lower(), albums[i]["artist"].lower())
        if lev < dist:
            dist = lev
            pos = i
    try:
        return albums[pos]["image"][-1]["#text"]
    except:
        print("ENTRY NOT FOUND " + albumName)

def downloadImage(url, imageName):
    try:
        urllib.request.urlretrieve(url, imageName)
    except:
        print("COULDNT FIND PIC: " + imageName)


# TODO: check existence before making any req


def processAlbum(artist, albumName):
    imageUrl = getClosestGuess(artist, albumName)
    fileName = getFileName(artist, albumName)
    if os.path.isfile(fileName):
        print("Something went wrong")
    else:
        downloadImage(imageUrl, fileName)


def getAllAlbums():
    albums = []
    for entry in LIST:
        if "-M-A-" in entry:
            albums.append(entry)
    return albums


def getArtistandTitle(entry):
    info = entry.split("-")
    artist = info[3]
    title = info[4]
    return artist, title


def getCArtist(artist):
    cArtist = artist.replace(" ", "")
    cArtist = cArtist.replace("|", "_")
    return cArtist


def getCAlbum(album):
    return album.replace(" ", "")


def getFileName(artist, album):
    cArtist = getCArtist(artist)
    cAlbumName = getCAlbum(album)
    return "../images/albums/" + cArtist + "-" + cAlbumName + ".jpg"


albums = getAllAlbums()
for album in albums:
    artist, title = getArtistandTitle(album)
    fileName = getFileName(artist, title)
    # print(artist, title, fileName)
    if os.path.isfile(fileName):
        # print('ALREDY EXISTS')
        continue
    else:
        processAlbum(artist, title)

# processAlbum('Jeff Rosenstock','WORRY.')
