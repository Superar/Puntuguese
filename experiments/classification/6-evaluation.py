# pipenv run python experiments/classification/6-evaluation.py -i results/predictions
import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i',
                    help='Path to the predictions directory.',
                    required=False, type=Path)
args = parser.parse_args()

results = dict()
for method in args.input.iterdir():
    folds = dict()
    for fold in method.iterdir():
        fold_df = pd.read_json(fold)
        evaluation = classification_report(fold_df['Label'],
                                           fold_df['Prediction'],
                                           output_dict=True)
        evaluation_df = pd.DataFrame.from_dict(evaluation)
        folds[fold.stem] = evaluation_df
    results[method.stem] = pd.concat(folds, names=['Fold'])
results_df = pd.concat(results, names=['Method'])
results_df.to_csv('./results/results.csv', decimal=',')
