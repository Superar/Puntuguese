import json
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

parser = ArgumentParser()
parser.add_argument('--input', '-i',
                    help='Input JSON file to be fixed.',
                    required=True, type=Path)
parser.add_argument('--corpus', '-c',
                    help='Main corpus JSON file to compare duplicates.',
                    required=True, type=Path)
args = parser.parse_args()

with args.input.open(encoding='utf-8') as f:
    data = json.load(f)
with args.corpus.open(encoding='utf-8') as f:
    corpus = json.load(f)

# Remove duplicates inside `data`
data_df = pd.DataFrame([{'id': x['id'],
                         'text': x['text']}
                        for x in data])
clean_data_df = data_df.drop_duplicates(subset=['text'])
print(f'Dropped {len(data_df)-len(clean_data_df)} puns')

# Remove duplicates already in `corpus`
corpus_texts = [x['text'] for x in corpus]

duplicated = clean_data_df.loc[clean_data_df['text'].isin(corpus_texts), :]
clean_data_df = clean_data_df.loc[~clean_data_df['text'].isin(corpus_texts), :]
print(f'Dropped {len(duplicated)} puns')

new_data = [x for x in data if x['id'] in clean_data_df['id'].values]
savepath = args.input.with_stem(args.input.stem + '_no_duplicates')
with savepath.open('w', encoding='utf-8') as file_:
    json.dump(new_data, file_,
              ensure_ascii=False,
              indent=4)

