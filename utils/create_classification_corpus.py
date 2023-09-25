import json
from argparse import ArgumentParser
from pathlib import Path

from nltk.tokenize.treebank import TreebankWordDetokenizer


def list_to_dict(list_):
    return {item['id']: item for item in list_}


parser = ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Pun corpus JSON file.',
                    required=True, type=Path)
parser.add_argument('--editions', '-e',
                    help='Directory with edited puns JSON files.',
                    required=True, type=Path)


# Read data
args = parser.parse_args()
with args.corpus.open('r', encoding='utf-8') as file_:
    corpus = json.load(file_)
editions = list()
for filepath in args.editions.iterdir():
    with filepath.open('r', encoding='utf-8') as file_:
        edited = json.load(file_)
        editions.append(edited)

# Dictionaries are easier to handle
corpus_dict = list_to_dict(corpus)
editions_list = [list_to_dict(e) for e in editions]
editions_dict = {k: e[k] for e in editions_list for k in e}


# Create classification data
classification_corpus = dict()
for k in corpus_dict:
    if editions_dict[k]['tokens'] == editions_dict[k]['edited tokens']:
        continue
    classification_corpus[k + '.H'] = {'text': corpus_dict[k]['text'],
                                       'label': 1}
    # Detokenize
    twd = TreebankWordDetokenizer()
    detokenized_text = twd.detokenize(editions_dict[k]['edited tokens'])
    classification_corpus[k + '.N'] = {'text': detokenized_text,
                                       'label': 0}
classification_corpus_path = args.corpus.parent / 'classification_corpus.json'
with classification_corpus_path.open('w', encoding='utf-8') as file_:
    json.dump(classification_corpus, file_,
              ensure_ascii=False, indent=4)
