# pipenv run python experiments/editions/editing_clustering.py -e data/split_annotation
import pandas as pd
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from argparse import ArgumentParser
from sklearn.cluster import KMeans


device = 'cuda:0' if torch.cuda.is_available() else 'cpu'


def edited_idx(row):
    token_pairs = zip(row['tokens'], row['edited tokens'])
    return [i for i, (t, e) in enumerate(token_pairs) if t != e and e]


def word_mean_pooling(data, tokenizer, model, uncased=False):
    if uncased:
        data = data.apply(lambda x: [t.lower() for t in x])

    encoded_input = tokenizer(data.to_list(),
                              is_split_into_words=True,
                              return_tensors='pt',
                              padding=True).to(device)
    with torch.no_grad():
        embedded_tokens = model(**encoded_input)[0]

    # Calculate word embeddings via subtoken mean pooling
    embedded_texts = list()
    for i in range(len(data)):
        spans = list()
        for j in encoded_input.word_ids(i):
            if j is not None and j >= len(spans):
                spans.append(encoded_input.word_to_tokens(i, j))

        mean_embeddings = torch.vstack([torch.mean(embedded_tokens[i, start:end, :], 0)
                                        for start, end in spans])
        embedded_texts.append(mean_embeddings)
    return embedded_texts


parser = ArgumentParser()
parser.add_argument('--editions', '-e',
                    help='Directory with edited puns JSON files.',
                    required=True, type=Path)
parser.add_argument('--model', '-m',
                    help='HuggingFace model to use.',
                    required=False, type=str,
                    default='neuralmind/bert-base-portuguese-cased')
parser.add_argument('--n_clusters', '-n',
                    help='Number of clusters.',
                    required=False, type=int,
                    default=20)
parser.add_argument('--uncased', '-u',
                    help='First turn every token into lowercase.',
                    required=False, action='store_true')
args = parser.parse_args()

editions = dict()
for filepath in args.editions.iterdir():
    edited = pd.read_json(filepath)
    editions[filepath.stem] = edited
df = pd.concat(editions)

# Filter edited texts
edited_df = df.query('tokens != `edited tokens`').copy()
edited_df['edition'] = edited_df.apply(edited_idx, axis='columns')
edited_df = edited_df.explode('edition').dropna()
edited_df['original token'] = edited_df.apply(lambda x: x['tokens'][x['edition']],
                                              axis='columns')
edited_df['edited token'] = edited_df.apply(lambda x: x['edited tokens'][x['edition']],
                                            axis='columns')

# Instantiate HF models
tokenizer = AutoTokenizer.from_pretrained(args.model)
model = AutoModel.from_pretrained(args.model).to(device)

# Original tokens -- Get word embeddings
print('Getting original tokens embeddings')
embedded_original_texts = word_mean_pooling(edited_df['tokens'],
                                            tokenizer,
                                            model,
                                            args.uncased)
# Original tokens -- Get only edited tokens
embedded_original_tokens = list()
for i in range(len(edited_df)):
    edition = edited_df.iloc[i]['edition']
    embedded_original_tokens.append(embedded_original_texts[i][edition].cpu())

# Original tokens -- Clustering
print('Doing original tokens clustering')
kmeans_original = KMeans(n_clusters=args.n_clusters, n_init='auto')
clusters = kmeans_original.fit_predict(embedded_original_tokens)
edited_df['original token cluster'] = clusters

# Original tokens -- Clean up memory
print('Cleaning up...')
del embedded_original_texts
del embedded_original_tokens

# Edited tokens -- Get word embeddings
print('Getting edited tokens embeddings')
embedded_edited_texts = word_mean_pooling(edited_df['edited tokens'],
                                          tokenizer,
                                          model,
                                          args.uncased)
# Edited tokens -- Get only edited tokens
embedded_edited_tokens = list()
for i in range(len(edited_df)):
    edition = edited_df.iloc[i]['edition']
    shift = len([t for t in edited_df.iloc[i]['edited tokens'][0:edition]
                 if t in ['', ' ']])
    edition -= shift  # Account for removed previous tokens

    embedded_edited_tokens.append(embedded_edited_texts[i][edition].cpu())

# Edited tokens -- Clustering
print('Doing edited tokens clustering')
kmeans_edited = KMeans(n_clusters=args.n_clusters, n_init='auto')
clusters = kmeans_edited.fit_predict(embedded_edited_tokens)
edited_df['edited token cluster'] = clusters

# Edited tokens -- Clean up memory
print('Cleaning up...')
del embedded_edited_texts
del embedded_edited_tokens

edited_df.to_csv('results/editing_clustering.csv',
                 index=False,
                 columns=['id', 'text',
                          'original token',
                          'original token cluster',
                          'edited token',
                          'edited token cluster'])
