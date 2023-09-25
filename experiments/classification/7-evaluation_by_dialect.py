# pipenv run python .\experiments\classification\7-evaluation_by_dialect.py -c .\data\classification_corpus_HumorRecognitionPT.json -f .\data\cross_validation -p .\results\predictions
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report

PT_PT_SOURCES = ['4']

parser = ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Path to the classification corpus JSON file.',
                    required=True, type=Path)
parser.add_argument('--fold', '-f',
                    help='Path to the cross validation folds data directory.',
                    required=True, type=Path)
parser.add_argument('--predictions', '-p',
                    help='Path to the predictions directory.',
                    required=True, type=Path)
args = parser.parse_args()


corpus_df = pd.read_json(args.corpus)

results = dict()
for method in args.predictions.iterdir():
    folds = dict()
    for pred_fold in method.iterdir():
        predictions_df = pd.read_json(pred_fold)
        fold_df = pd.read_json(args.fold / pred_fold.stem / 'test.json')
        predictions_df['Text'] = fold_df['Text']

        # Find corresponding indices and split by dialect
        df = predictions_df.join(corpus_df.set_index('Text'),
                                 on='Text',
                                 lsuffix='_FOLD')
        df = df.drop(columns='Label_FOLD').set_index('Index')
        df['Dialect'] = 'PT-BR'
        df.loc[df.index.str.split('.').str[0].isin(PT_PT_SOURCES),
               'Dialect'] = 'PT-PT'
        pt_br_df = df.loc[df['Dialect'] == "PT-BR", :]
        pt_pt_df = df.loc[df['Dialect'] == "PT-PT", :]

        # PT-BR
        evaluation_pt_br = classification_report(pt_br_df['Label'],
                                                 pt_br_df['Prediction'],
                                                 output_dict=True)
        evaluation_pt_br_df = pd.DataFrame.from_dict(evaluation_pt_br)

        # PT-PT
        evaluation_pt_pt = classification_report(pt_pt_df['Label'],
                                                 pt_pt_df['Prediction'],
                                                 output_dict=True)
        evaluation_pt_pt_df = pd.DataFrame.from_dict(evaluation_pt_pt)
        folds[pred_fold.stem] = pd.concat({'PT-BR': evaluation_pt_br_df,
                                           'PT-PT': evaluation_pt_pt_df},
                                          names=['Dialect'])
    results[method.stem] = pd.concat(folds, names=['Fold'])
results_df = pd.concat(results, names=['Method'])
results_df.to_csv('./results/general_results_by_dialect.csv', decimal=',')
