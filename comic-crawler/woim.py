import os
import sys
import codecs
import unicodedata
import re
from os.path import basename
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
from bs4 import BeautifulSoup
import requests

def process_track(root_dir, track_url) :
    print ("======= Process track: " + track_url)
    f = urlopen(track_url)
    # f = codecs.open("test_chapter.html", "r", "utf-8")
    data = f.read()
    f.close()
    parsed_html = BeautifulSoup(data)
    param = parsed_html.find("param", {"name" : "flashvars"});
    songs_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', param["value"])
    for songs_url in songs_urls:
        f2 = urlopen(songs_url)
        data2 = f2.read()
        parsed_html2 = BeautifulSoup(data2)
        tracks = parsed_html2.findAll("track")
        for track in tracks :
            song_url = track["location"]
            o = urlparse(song_url)
            file_name = basename(song_url)
            file_path = root_dir + "/" + file_name
            if os.path.exists(file_path) :
                print ("File exists. Skip: " + file_path)
            else :
                print ("Download: " + file_name)
                urlretrieve(song_url, file_path)

def process_album(album_url, root_dir):
    f = urlopen("http://www.woim.net/album/265/dreamland.html")
    # f = codecs.open("test_woim.html", "r", "utf-8")
    data = f.read()
    parsed_html = BeautifulSoup(data)
    track_elements = parsed_html.findAll("tr", {"class" : "tracklist"})
    for track_element in track_elements :
        track_url = track_element.a["href"]
        process_track(root_dir, track_url)

def login():
    url = 'http://www.woim.net/user/login'
    login_data = urlencode({'username':'NHA_DIEN','password':'Ch!ck3n1989','submit':'Đăng nhập'})
    binary_data = login_data.encode("utf-8")
    payload = {'username':'NHA_DIEN','password':'Ch!ck3n1989','submit':'Login'}
    r = requests.post(url, payload)
    data = r.content
    parsed_html = BeautifulSoup(unicodedata.normalize('NFKD', data.decode("utf-8")).encode('ascii','ignore'))
    titles = parsed_html.findAll("div", {"class" : "title"});
    print (titles)
    print ("------------------")
    r = requests.post("http://www.woim.net/album/265/dreamland.html");
    titles = parsed_html.findAll("div", {"class" : "title"});
    print (titles)


def main():
    if (len(sys.argv) > 1) :
        album_url = sys.argv[1]
    else :
        print ("Invalid serie url.")
        return

    root_dir = "./download"
    if (len(sys.argv) > 2) :
        root_dir = sys.argv[2]
    if not os.path.exists(root_dir) :
        os.makedirs(root_dir)

    process_album(album_url, root_dir)

login()