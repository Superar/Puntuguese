# pipenv run python experiments/pun_types_statistics.py --corpus data/puns.json
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

parser = ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Directory with the corpus JSON file.',
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

only_homophone = new_df.query('homophone == True & homograph == False')
only_homograph = new_df.query('homophone == False & homograph == True')
both = new_df.query('homophone == True & homograph == True')
none = new_df.query('homophone == False & homograph == False')

print(f'Only homophonic puns: {len(only_homophone)}')
print(f'Only homographic puns: {len(only_homograph)}')
print(f'Both homophonic and homographic: {len(both)}')
print(f'Not homophonic nor homographic: {len(none)}')
