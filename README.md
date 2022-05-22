# bulk_mp3_cover_art_extractor

### THE PROBLEM
Extract cover art images for large mp3 music libraries.  Useful to backup individual cover art from compilations before you unify their covers.

### EXISTING SOLUTIONS

1. Manual extraction

### THIS SOLUTION
This Python package will batch-extract your entire library without manual interaction for each album.
It supports all the subfolders you have inside the main directory (it works recursivelly) and only skips the folders named like the constant EXCLUDED_SUBDIR

It uses three known python libraries to do the job: eyed3, PIL and slugify.

The scripts produces a jpg file close to each mp3 original file with cover art, named like song-album-size.jpg
Finally the scripts writes the job done to a json file in the root input directory with the following four fields (for each cover extracted):
  - file_data['song'] = MP3 song filename
  - file_data['album'] = MP3 album ID3 tag
  - file_data['cover_name'] = Cover Art (extracted from MP3 file) jpg filename
  - file_data['cover_size'] = Cover Art dimensions (horizontal pixels x vertical pixels format)

## Supported formats (so far)
- MP3


## Setup

### Requirements
- Python 3.8 or greater (may be it works with other versions, but not tested)
- Python packages: 
  - eye3d https://eyed3.readthedocs.io/en/latest/ pip install eyed3 - alternative to mutagen
  - PIL: https://pillow.readthedocs.io/en/latest/ pip install pillow - library used to store jpg image files
  - slugify: https://github.com/un33k/python-slugify pip install python-slugify - library used for getting failsafe filenames

### Installation

You can download this repository from GitHub


## Usage

### From the Command Line
```
[python -m] bulk_mp3_art_file_extractor [--directory=<path_to_audio_folder>]

  --directory PATH           audio folder (recursive)

```
