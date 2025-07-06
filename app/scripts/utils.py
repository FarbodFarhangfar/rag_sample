import os
from urllib.request import urlretrieve


def download_file_if_not_exists(url, filename):
    # Check if file exists
    # if not exists download the file
   
    print(filename)
    print(os.path.exists(filename))
    if not os.path.exists(filename):
        urlretrieve(url, filename)

