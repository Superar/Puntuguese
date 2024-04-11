from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

parser = ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Pun corpus JSON file.',
                    required=True, type=Path)
parser.add_argument('--classification', '-t',
                    help='Classification corpus JSON file.',
                    required=True, type=Path)
parser.add_argument('-location', '-l',
                    help='Pun location corpus JSON file.',
                    required=True, type=Path)
parser.add_argument('--output', '-o',
                    help='Output Directory to save split files.',
                    required=True, type=Path)
args = parser.parse_args()

puns_df = pd.read_json(args.corpus, dtype={'id': str})
classification_df = pd.read_json(args.classification).T
pun_location_df = pd.read_json(args.location)

df = classification_df.join((pun_location_df.set_index('id')
                             .rename(columns={'text': 'tokens'})),
                            how='left')

puns_df['country'] = 'PT'
puns_df.loc[puns_df['id'].str.startswith('5.'), 'country'] = 'BR'

homographs = list()
homophones = list()
for row in puns_df.itertuples():
    homograph = False
    homophone = False
    for sign in row.signs:
        if homograph and homophone:
            break
        if not homograph:
            homograph = sign['homograph']
        if not homophone:
            homophone = sign['homophone']
    homographs.append(homograph)
    homophones.append(homophone)
puns_df['homograph'] = homographs
puns_df['homophone'] = homophones
puns_df = puns_df.set_index('id')

strat_info_H = (puns_df['country'] + '.' +
                puns_df['homograph'].astype(str) + '.' +
                puns_df['homophone'].astype(str)).reset_index()
strat_info_N = strat_info_H.copy()
strat_info_H['id'] = strat_info_H['id'] + '.H'
strat_info_N['id'] = strat_info_N['id'] + '.N'
strat_info_H = strat_info_H.set_index('id')
strat_info_N = strat_info_N.set_index('id')
strat_info = pd.concat([strat_info_H, strat_info_N])

df = df.join(strat_info)
df[0] = df[0] + '.' + df['label'].astype(str)
df = df.reset_index(names='id')

train_val, test = train_test_split(df, test_size=0.2, stratify=df[0])
train, val = train_test_split(train_val, test_size=0.125,
                              stratify=train_val[0])

train = train.drop(columns=0)
val = val.drop(columns=0)
test = test.drop(columns=0)

args.output.mkdir(exist_ok=True)
train.to_json(args.output / 'train.jsonl', force_ascii=False,
              orient='records', lines=True)
val.to_json(args.output / 'validation.jsonl', force_ascii=False,
            orient='records', lines=True)
test.to_json(args.output / 'test.jsonl', force_ascii=False,
             orient='records', lines=True)
