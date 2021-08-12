import requests as req
from bs4 import BeautifulSoup as Soup
import os
from time import sleep
from random import randint

ARTISTS_URL = 'http://www.fmderana.lk/sri-lankan-artists'
PREFIX_URL = 'http://www.fmderana.lk/'
BASE_DOWNLOAD = 'downloads/'

total_songs = 0
total_artists = 0
index = 0
total_size = 0
artist_index = 0
total_errors = 0


def scrape_artist_songs(page_url, name):
    global total_songs
    global index
    global total_size
    global artist_index
    global total_errors

    artist_index += 1

    if not os.path.isdir(BASE_DOWNLOAD + name):
        os.mkdir(BASE_DOWNLOAD + name)

    artists_page = req.get(page_url)
    soup = Soup(artists_page.content, 'html5lib')

    song_links = soup.find_all('div', class_='radio-item-icons d-none d-sm-block')

    print('\n')
    print('##########################################################################################################')
    print(' \t       All - (' + str(index)+ ') Errors - (' + str(total_errors) + ')  ' + str(artist_index) + '/' + str(total_artists) + ' Artist - ' + name.upper().replace("-", " ") + '    Songs - ' + str(len(song_links)))
    print('##########################################################################################################')

    temp = 0
    for song in song_links:

        song_attr = song.a['href']
        song_name = song_attr.split('=')[-1]
        path = BASE_DOWNLOAD + name + '/' + song_name
        
        if os.path.isfile(path):
            index += 1
            temp += 1
            size = os.path.getsize(path)
            mb = round(size/1024/1024,2)
            total_size += mb
            if mb == 0.0:
              total_errors += 1
            print(str(temp) + '. Already Downloaded - ' + song_name + ' (' + str(mb) + 'mb)')
            continue

        direct_link = PREFIX_URL + song_attr
        mp3_file = req.get(direct_link)

        f = open(path, 'wb')
        f.write(mp3_file.content)
        f.close()
        index += 1
        temp += 1
        size = os.path.getsize(path)
        mb = round(size/1024/1024,2)
        total_size += mb
        if mb == 0.0:
            total_errors += 1
        print(str(temp) + '. Downloaded - ' + song_name + ' (' + str(mb) + ' mb)')
        total_songs += 1

    interval = randint(3, 8)
    print(f'\n           >>>>>>>>>>>>>>>>>>>>>>>>>>>> Waiting {interval}s for next artist <<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    sleep(interval)


def scrape_artists():
    r = req.get(ARTISTS_URL)
    soup = Soup(r.content, 'html5lib')

    global total_artists

    artists = soup.find_all('div', class_='item col-6 col-sm-4 col-md-3 col-lg-4 col-xl-3')

    total_artists = len(artists)

    print('\n')
    print('##########################################################################################################')
    print('                                  TOTAL ARTISTS - ' + str(total_artists))
    print('##########################################################################################################')

    for artist in artists:
        artist_attr = artist.a['href']
        name = artist_attr.split('/')[-1]
        artist_page_url = PREFIX_URL + artist_attr

        scrape_artist_songs(artist_page_url, name)



if __name__ == '__main__':
    if not os.path.isdir(BASE_DOWNLOAD):
        os.mkdir(BASE_DOWNLOAD)
    scrape_artists()

    print('\n')
    print('##########################################################################################################')
    print(' Scraped - ' + str(total_songs) + ' songs of ' + str(total_artists) + ' artists, Size - ' + str(total_size) + ' Errors - ' + str(total_errors))
    print('##########################################################################################################')
    print('\n')
