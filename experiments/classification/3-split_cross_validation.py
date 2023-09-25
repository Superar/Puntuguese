# pipenv run python experiments/classification/3-split_cross_validation.py -c data/classification_corpus_preprocesses.json -o data/cross_validation
import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import StratifiedKFold

parser = argparse.ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Preprocessed corpus JSON file to be split into folds.',
                    required=True, type=Path)
parser.add_argument('--output', '-o',
                    help='Output directory to which create the folds.',
                    required=True, type=Path)
args = parser.parse_args()

df = pd.read_json(args.corpus).drop(columns='Index')
skf = StratifiedKFold(n_splits=10, shuffle=True)
X = df.drop(columns='Label')
y = df['Label']

folds = skf.split(X, y)
for i, (train_index, test_index) in enumerate(folds):
    train, test = df.iloc[train_index], df.iloc[test_index]
    fold_directory = args.output / f'fold_{i}'
    fold_directory.mkdir(exist_ok=True)

    train.to_json(fold_directory / 'train.json', orient='records',
                  force_ascii=False, indent=4)
    test.to_json(fold_directory / 'test.json', orient='records',
                 force_ascii=False, indent=4)
