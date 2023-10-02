from argparse import ArgumentParser
from pathlib import Path
import pandas as pd

parser = ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Pun corpus JSON file to convert to CSV.',
                    required=True, type=Path)
args = parser.parse_args()

df = pd.read_json(args.corpus).set_index('id')

new_dict = dict()
for row in df.itertuples():
    signs_list = list()
    for sign in row.signs:
        signs_list.append({'homograph': sign['homograph'],
                            'homophone': sign['homophone'],
                            'pun sign': sign['pun sign'],
                            'alternative sign': sign['alternative sign']})
    new_dict[(row.Index, row.text)] = pd.DataFrame(signs_list)
new_df = pd.concat(new_dict, names=['id', 'text', 'sign_id'])
new_df.to_csv(args.corpus.with_suffix('.csv'))