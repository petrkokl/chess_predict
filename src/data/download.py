import requests
from random import randint
from time import sleep
from pathlib import Path
from zipfile import ZipFile
import names
from bs4 import BeautifulSoup

FIRST_ARCHIVE_INDEX = 920
# find latest archive index
url = 'https://theweekinchess.com/twic'
random_first_name = names.get_first_name()
response = requests.get(url, headers={"User-Agent": f"{random_first_name}"})
soup = BeautifulSoup(response.text, 'html.parser')
last_archive_index = int(soup.find_all('td')[0].text)

# all files will be in './full_database' folder
full_database_path = Path('../../data/raw')

for i in range(FIRST_ARCHIVE_INDEX, last_archive_index + 1):
    url = f"https://theweekinchess.com/zips/twic{i}g.zip"
    zip_file_name = Path(url.split('/')[-1])  # twic{i}g.zip part of url
    zip_file_path = full_database_path / zip_file_name
    pgn_file_name = zip_file_path.stem[:-1] + '.pgn'
    pgn_file_path = full_database_path / pgn_file_name

    if zip_file_path.exists():
        # skip file if it has been already downloaded as zip file
        print(f'{zip_file_name} already exists')
        continue

    if pgn_file_path.exists():
        # skip file if it has been already downloaded as zip file and unzipped
        print(
            f'{zip_file_name} need not be downoaded: content already exists as a pgn file.')
        continue

    response = requests.get(
        url, headers={"User-Agent": f"{random_first_name}"})

    with open(zip_file_path, mode='wb') as file:
        file.write(response.content)
        print(f"{zip_file_name} was saved.")

    # wait some time to don't bother guys from theweekinchess.com
    sleep(randint(10, 20))

print(f'All files have been downloaded and placed into {full_database_path}')

print(f'Extracting zip archives into PGN files...')
sleep(5)

downloaded_archives = sorted(list(full_database_path.glob('*.zip')))
current_pgns = sorted(list(full_database_path.glob('*.pgn')))

for zip_file_path in downloaded_archives:
    zip_file_name = zip_file_path.stem + '.zip'
    pgn_file_name = zip_file_path.stem[:-1] + '.pgn'
    pgn_file_path = full_database_path / pgn_file_name

    if pgn_file_path.exists():
        print(
            f"{zip_file_name} has already been extracted as pgn file. So, file will be deleted")
        zip_file_path.unlink()
        continue

    with ZipFile(zip_file_path, 'r') as zipObj:
        # Extract all the contents of zip file
        zipObj.extractall(full_database_path)
        print(
            f"{zip_file_name} has been extracted into {pgn_file_name}. Zip file will be deleted.")
        zip_file_path.unlink()

print('Done.')
