import sys
import os
from pathlib import Path
from utils import *

artists = get_artists()
artist = '동방신기'
id = get_artist_id(artist)
print(artist, id)
get_songs_list(id)
