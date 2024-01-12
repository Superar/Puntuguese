import json
import re
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import spacy

parser = ArgumentParser()
parser.add_argument('--corpus', '-c',
                    help='Pun corpus JSON file.',
                    required=True, type=Path)
parser.add_argument('--output', '-o',
                    help='Output JSON file to save.',
                    required=True, type=Path)


# Read data
args = parser.parse_args()
with args.corpus.open('r', encoding='utf-8') as file_:
    corpus = json.load(file_)

nlp = spacy.load('pt_core_news_sm')

# Create humor anchoring data
anchoring_data = list()
for pun in corpus:
    doc = nlp(pun['text'])
    labels = np.zeros((len(doc),), dtype=np.int32)
    for sign in pun['signs']:
        sign_locs = list()
        sign_regex_variations = [rf'\b{re.escape(sign["pun sign"])}\b',
                                 rf'\b{re.escape(sign["pun sign"])}',
                                 rf'{re.escape(sign["pun sign"])}']
        for sign_regex in sign_regex_variations:
            sign_locs = re.finditer(sign_regex, pun['text'], re.IGNORECASE)
            if sign_locs:
                break
        for sign_loc in sign_locs:
            sign_start, sign_end = sign_loc.span()
            tokens_idx = [i for i, token in enumerate(doc)
                          if token.idx < sign_end and
                          (token.idx + len(token)) > sign_start]
            labels[tokens_idx] = 1
    anchoring_data.append({'id': pun['id'],
                           'text': [token.text for token in doc],
                           'labels': labels.tolist()})

with args.output.open('w', encoding='utf-8') as file_:
    json.dump(anchoring_data, file_,
              ensure_ascii=False, indent=4)
