from pathlib import Path
import chess.pgn
import pandas as pd
from datetime import date

csv_datasets_folder = Path('../../data/interim')
raw_data_folder = Path('../../data/raw')

pgn_files = sorted(raw_data_folder.glob('*.pgn'))

datasets = []

for path in pgn_files:
    print(f'parsing {path}')
    games = []
    with open(path) as pgn_file:
        while pgn_file:
            try:
                headers = chess.pgn.read_headers(pgn_file)
            except UnicodeDecodeError:
                print(
                    f'UnicodeDecodeError occurs while parsing {path} after the game {headers}. Going to the next game...')
                continue
            if headers is None:
                break
            games.append(pd.Series(headers))

        df = pd.DataFrame(games)
        datasets.append(df)

final_df = pd.concat(datasets)
today_str = date.today().strftime('%d_%m_%Y')
csv_file_name = csv_datasets_folder / f"{today_str}.csv"
final_df.to_csv(csv_file_name)

print(f'csv file {csv_file_name} was saved.')
