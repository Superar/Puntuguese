# pipenv run python experiments/classification/2-preprocessing.py -c data/classification_corpus_HumorRecognitionPT.json -o data/classification_corpus_preprocessed.json
import argparse
from pathlib import Path

import pandas as pd
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Corpus JSON file to be preprocessed.',
                    required=True, type=Path)
parser.add_argument('--output', '-o',
                    help='File path to save preprocessed corpus.',
                    required=True, type=Path)
args = parser.parse_args()

df = pd.read_json(args.corpus)
nlp = spacy.load('pt_core_news_sm')
docs = list(nlp.pipe(df['Text']))

df['Tokens'] = [[token.text for token in doc] for doc in docs]
df['POS Tags'] = [[token.pos_ for token in doc] for doc in docs]
df['Lemma'] = [[token.lemma_ for token in doc] for doc in docs]
NER_MAP = {'': '',
           'PER': 'PESSOA',
           'MISC': 'OUTRO',
           'LOC': 'LOCAL',
           'ORG': 'ORGANIZACAO'}
df['NER'] = [[token.ent_iob_ if token.ent_iob_ == 'O' else f'{token.ent_iob_}-{NER_MAP[token.ent_type_]}'
              for token in doc]
             for doc in docs]

df.to_json(args.output, orient='records',
           force_ascii=False, indent=4)
