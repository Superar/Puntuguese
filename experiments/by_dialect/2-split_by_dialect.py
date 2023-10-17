# pipenv run python experiments/by_dialect/2-split_by_dialect.py -c data/classification_corpus_preprocessed.json -o data/cv_by_dialect
import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedKFold

PT_PT_SOURCES = ['4']

parser = argparse.ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Preprocessed corpus JSON file to be split into folds.',
                    required=True, type=Path)
parser.add_argument('--output', '-o',
                    help='Output directory to which create the folds.',
                    required=True, type=Path)
args = parser.parse_args()

df = pd.read_json(args.corpus).set_index('Index')
df['Dialect'] = 'PT-BR'
df.loc[df.index.str.split('.').str[0].isin(PT_PT_SOURCES), 'Dialect'] = 'PT-PT'

# PT-BR
skf = StratifiedKFold(n_splits=10, shuffle=True)
pt_br_df = df.loc[df['Dialect'] == 'PT-BR', ~df.columns.isin(['Dialect'])]
X = pt_br_df.drop(columns='Label')
y = pt_br_df['Label']

folds = skf.split(X, y)
for i, (train_index, test_index) in enumerate(folds):
    train, test = pt_br_df.iloc[train_index], pt_br_df.iloc[test_index]
    fold_directory = args.output / f'PT_BR/fold_{i}'
    fold_directory.mkdir(parents=True, exist_ok=True)

    train.to_json(fold_directory / 'train.json', orient='records',
                  force_ascii=False, indent=4)
    test.to_json(fold_directory / 'test.json', orient='records',
                 force_ascii=False, indent=4)

# PT-PT
skf = StratifiedKFold(n_splits=10, shuffle=True)
pt_pt_df = df.loc[df['Dialect'] == 'PT-PT', ~df.columns.isin(['Dialect'])]
X = pt_pt_df.drop(columns='Label')
y = pt_pt_df['Label']

folds = skf.split(X, y)
for i, (train_index, test_index) in enumerate(folds):
    train, test = pt_pt_df.iloc[train_index], pt_pt_df.iloc[test_index]
    fold_directory = args.output / f'PT_PT/fold_{i}'
    fold_directory.mkdir(parents=True, exist_ok=True)

    train.to_json(fold_directory / 'train.json', orient='records',
                  force_ascii=False, indent=4)
    test.to_json(fold_directory / 'test.json', orient='records',
                 force_ascii=False, indent=4)
