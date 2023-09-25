# pipenv run python experiments/classification/1-convert_to_HumorRecognitionPT.py -c data/classification_corpus.json
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='JSON classification corpus file.',
                    required=True, type=Path)
args = parser.parse_args()

with args.corpus.open('r', encoding='utf-8') as file_:
    corpus = json.load(file_)

corpus_HumorRecognitionPT = [{'Index': k,
                              'Text': corpus[k]['text'],
                              'Label': 'H' if corpus[k]['label'] == 1 else 'N'}
                             for k in corpus]
save_filepath = args.corpus.with_stem(args.corpus.stem + '_HumorRecognitionPT')
with save_filepath.open('w', encoding='utf-8') as file_:
    json.dump(corpus_HumorRecognitionPT, file_,
              ensure_ascii=False, indent=4)
