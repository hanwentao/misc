#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
#import logging
import os
import os.path
import sys
import time
import urllib

import libgmbox

#logger = logging.getLogger('libgmbox')
#logger.setLevel(logging.DEBUG)

def decode(string, charset='utf-8'):
    if isinstance(string, unicode):
        string = string.encode(charset)
    return string

def report_progress(num_blocks_transferred, block_size, total_size):
    sys.stdout.write('.')
    sys.stdout.flush()

def main(argv=None):
    parser = argparse.ArgumentParser(description='download songs from Google Music (China).')
    parser.add_argument('-n', '--dry-run', action='store_true', dest='dry_run',
                        help='show what are to be done, not actually do things')
    parser.add_argument('artist_ids', metavar='ARTIST_ID', nargs='+',
                        help='ID of the artist whose songs are to be downloaded')
    args = parser.parse_args()

    num_artists = len(args.artist_ids)
    for artist_num, artist_id in enumerate(args.artist_ids):
        directory = libgmbox.DirArtistAlbum(artist_id)
        num_songlists = len(directory.songlists)
        for songlist_num, songlist in enumerate(directory.songlists):
            songlist.load_songs()
            artist = decode(songlist.artist)
            album = decode(songlist.name)
            num_songs = len(songlist.songs)
            for song_num, song in enumerate(songlist.songs):
                name = decode(song.name)
                dir_path = os.path.join(artist, album)
                downloaded_file_path = os.path.join(dir_path, name + '.mp3')
                downloading_file_path = downloaded_file_path + '.download'

                if os.path.exists(downloaded_file_path):
                    sys.stdout.write('Already downloaded "%s", skipped\n' % downloaded_file_path)
                    sys.stdout.flush()
                    continue

                sys.stdout.write('Downloading "%s" %d/%d %d/%d %d/%d\n' % (downloaded_file_path,
                                                                           artist_num, num_artists,
                                                                           songlist_num, num_songlists,
                                                                           song_num, num_songs))
                sys.stdout.flush()
                is_downloadable = True
                while True:
                    song.load_download()
                    if song.downloadUrl is None:
                        sys.stderr.write('Cannot download "%s", not downloadable\n' % downloaded_file_path)
                        sys.stderr.flush()
                        is_downloadable = False
                        break
                    elif not song.downloadUrl:
                        sys.stderr.write('Cannot download "%s", waiting for some minutes\n' % downloaded_file_path)
                        sys.stderr.flush()
                        time.sleep(600)
                    else:
                        break
                if not is_downloadable:
                    continue

                if not args.dry_run:
                    try:
                        os.makedirs(dir_path)
                    except OSError:
                        pass
                    urllib.urlretrieve(song.downloadUrl, downloading_file_path, report_progress)
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                    os.rename(downloading_file_path, downloaded_file_path)

if __name__ == '__main__':
    sys.exit(main())
