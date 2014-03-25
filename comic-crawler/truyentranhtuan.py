import os
import sys
import codecs
import unicodedata
import re
from os.path import basename
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import urlparse
from urllib.parse import urlunparse
from bs4 import BeautifulSoup

def process_chapter(serie_dir, chapter_url):
    chapter_num_txt = re.search("[0-9\-]+\/", chapter_url).group(0)[0:-1];
    try :
        f = urlopen(chapter_url)
    except Exception as e :
        print ("======= Processing chapter " + chapter_num_txt + ": " + chapter_url + " failed.")
        print(type(e))
        print(e.args)
        print(e)
        return;
    else :
        print ("======= Processing chapter " + chapter_num_txt + ": " + chapter_url + " - chapter " + chapter_num_txt)
    # f = codecs.open("test_chapter.html", "r", "utf-8")
    data = f.read().decode("utf-8")
    f.close()
    pages_txt = re.search("var slides_page\ \=\ \[.*\]", data).group(0)[19:-1];
    pages_url = pages_txt.split(",");
    o = urlparse(chapter_url)
    chapter_dir = serie_dir + "/chap" + chapter_num_txt
    if not os.path.exists(chapter_dir) :
        os.makedirs(chapter_dir)
    for page_url in pages_url :
        image_url = urlunparse((o.scheme, o.netloc, page_url[1:-1], "", "", ""))
        file_name = basename(image_url)
        file_path = chapter_dir + "/" + file_name
        if os.path.exists(file_path) :
            print ("File exists. Skip: " + file_name)
        else :
            attempts = 0;
            try:
                urlretrieve(image_url, file_path)
            except Exception as e :
                print("Failed to download: " + file_name)
                print(type(e))
                print(e.args)
                print(e)
            else :
                print ("Downloaded: " + file_name)

def process_serie(serie_url, root_dir):
    o = urlparse(serie_url)
    serie_name = re.search("[a-z0-9\-]+", o.path.lower()).group(0)
    serie_dir = root_dir + "/" + serie_name
    if not os.path.exists(serie_dir) :
        os.makedirs(serie_dir)
    print ("####### SERIE: " + serie_name)
    print ("####### URL: " + serie_url)
    f = urlopen(serie_url)
    # f = codecs.open("test_serie.html", "r", "utf-8")
    data = f.read()
    parsed_html = BeautifulSoup(data)
    chapter_spans = parsed_html.findAll("span", {"class" : "chapter-name"});
    for chapter_span in reversed(chapter_spans):
        chapter_link = chapter_span.a;
        process_chapter(serie_dir, chapter_link["href"])

def main():
    if (len(sys.argv) > 1) :
        serie_url = sys.argv[1]
    else :
        print ("Invalid serie url.")
        return

    root_dir = "/Users/u1194/Downloads/comic"
    if (len(sys.argv) > 2) :
        root_dir = sys.argv[2]
    if not os.path.exists(root_dir) :
        os.makedirs(root_dir)

    process_serie(serie_url, root_dir)

main()