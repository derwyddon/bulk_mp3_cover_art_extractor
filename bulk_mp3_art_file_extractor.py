import eyed3    # pip install eyed3: library used to manipulate ID3 tags from mp3 files
from PIL import Image  # pip install pillow: library used to store jpg image files

from slugify import slugify  # pip install python-slugify # https://github.com/un33k/python-slugify
# library used for getting failsafe filenames (album has sometimes some not failsafe chars to be used in filenames)

import sys
import os
import json
import io
import argparse  # used for easy command line argument parser

IMAGE_EXTENSION = '.jpg'
SONGS_EXTENSION = '.mp3'
EXCLUDED_SUBDIR = 'TEMP'  # subdirs with this name are skipped from searching inside
COVER_ART_DATA_FILE = '000-song-album-cover-data.json'  # json file with full data from extracted cover art files
'''
        album_data['song'] = MP3 song filename
        album_data['album'] = MP3 album ID3 tag
        album_data['cover_name'] = Cover Art (extracted from MP3 file) jpg filename
        album_data['cover_size'] = Cover Art dimensions (horizontal pixels x vertical pixels format)
'''


def get_data_files(data_files_directory, file_type):
    """
    :param data_files_directory: directory filename where the files are stored
    :param file_type: filename extension to search inside directory
    :return:  files_list: list with the filenames found
    """

    total_files = 0
    subfolder_files = 0
    files_list = list()

    try:
        for input_file in os.listdir(data_files_directory):
            full_path_input_file = os.path.join(data_files_directory, input_file)
            if os.path.isdir(full_path_input_file):
                # subdirectories processed in recursive way
                if input_file == EXCLUDED_SUBDIR:
                    # The TEMP processing subdir created by the app is not processed!
                    continue
                # recursive call!!!!
                inside_list = list()
                inside_list = get_data_files(full_path_input_file, file_type)
                total_files += len(inside_list)
                files_list.extend(inside_list)
                continue

            file_name, file_extension = os.path.splitext(input_file)

            if file_extension.lower() == (file_type):
                files_list.append(full_path_input_file)
                total_files += 1
                subfolder_files += 1

    except Exception as e:  # we verify the creation of output folder

        print('get-Data-Files: '
              + 'File Type: ' + str(file_type) + ' Data Directory: ' + str(data_files_directory)
              + ' has not been possible to read the files inside'
              )
        print('get-Data-Files: Exception 001: ' + str(e))
        exit(1)

    print('get-Data-Files: '
          + 'File Type: ' + str(file_type) + ' Data Directory: ' + str(data_files_directory)
          + ' has ' + str(subfolder_files) + ' files inside'
          )

    return files_list


if __name__ == '__main__':
    """
    :param directory: directory filename where the files are stored
    :return:  
        n jpg files: extracted cover art jpg from every mp3 with cover art file embebed
        json COVER_ART_DATA_FILE with full info about the extracted cover art files
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', required=True, help='folder to parse mp3 files')

    args = parser.parse_args()
    mp3_directory = args.directory

    # mp3_directory = r'D:\L01 Downloads\Music\[MP3]\2021 - VA - Karaoke Hits Essentials'
    # mp3_directory = r'D:\L01 Downloads\Music\[MP3]\2021 - VA - Disco Hits Essentials'
    # mp3_directory = r'D:\L01 Downloads\Music\[MP3]\2021 - VA - Karaoke Hits Essentials\TEMP'

    print('MP3 Input Directory used:' + mp3_directory)

    files_type = SONGS_EXTENSION
    mp3_files = get_data_files(mp3_directory, files_type)

    # print(*mp3_files, sep='\n') # Pretty Print https://stackoverflow.com/a/35211376

    print('MP3 Files to review: ' + str(len(mp3_files)))
    images_stored = 0
    album_data_list = list()
    for song_file in mp3_files:
        album_data = dict()

        song = eyed3.load(song_file)
        ##################################################################################################
        #                                  BUILDING COVER ART FILENAME                                   #
        #                                                                                                #
        ##################################################################################################
        dir_name = os.path.split(song_file)[0]
        cover_name = os.path.splitext(os.path.split(song_file)[1])[0]  # file_name without ext
        ext_name = IMAGE_EXTENSION
        album_name = song.tag.album
        try:

            size_name = str(Image.Image.getdata(Image.open(io.BytesIO(song.tag.images[0].image_data))).size[0]) + "x" \
                        + str(Image.Image.getdata(Image.open(io.BytesIO(song.tag.images[0].image_data))).size[1])

        except Exception as e:  # Exception: we cannot recover the cover art dimensions
            print("Problem extracting cover art from " + song_file)
            print('get-size-from-cover-art: Exception 002:' + str(e))
            continue

        # https://stackoverflow.com/a/46590727 #getting failsafe filenames (album has some not failsafe characthers sometimes)
        safe_cover_name = cover_name + "_" + slugify(album_name,
                                                     entities=True,
                                                     decimal=True,
                                                     hexadecimal=True,
                                                     max_length=0,
                                                     word_boundary=False,
                                                     separator=' ',
                                                     save_order=False,
                                                     stopwords=(),
                                                     regex_pattern=None,
                                                     lowercase=False,
                                                     replacements=(),
                                                     allow_unicode=False) + "_" + size_name
        album_data['song'] = cover_name = os.path.splitext(os.path.split(song_file)[1])[0]
        album_data['album'] = album_name
        album_data['cover_name'] = safe_cover_name + ext_name
        album_data['cover_size'] = size_name

        cover_name = os.path.join(os.path.split(song_file)[0],
                                  safe_cover_name + ext_name)
        print('MP3 File trying to retrieve ART cover:' + song_file)
        ##################################################################################################
        #                                 END BUILDING COVER ART FILENAME                                #
        #                                                                                                #
        ##################################################################################################
        # if there contains many images
        # https://stackoverflow.com/a/63145832
        try:
            img = Image.open(io.BytesIO(song.tag.images[0].image_data))
            img.save(cover_name)
            print("Cover Art has been stored inside " + cover_name)
            images_stored += 1
            album_data_list.append(album_data)

        except Exception as e:  # Exception: we cannot recover the cover art and store it at the output file
            print("Problem extracting cover art from " + song_file)
            print('get&store-cover-art: Exception 003:' + str(e))
            continue

    try:
        json_name = os.path.join(mp3_directory, #os.path.split(song_file)[0],
                                 COVER_ART_DATA_FILE)
        if album_data_list:
            with open(json_name, 'w') as fp:
                # we store the extracted cover art files info inside a json file stored at root mp3 input directory
                json.dump(album_data_list, fp)

    except Exception as e:  # Exception: we cannot store the restult json file
        print("Problem storing json file with cover album data: " + json_name)
        print('store-final-json: Exception 004:' + str(e))

    print("Images stored to disk: " + str(images_stored))
    sys.exit()
